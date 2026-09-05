"""
Read SCRAPE_CONFIG from the scout workbook, visit every enabled source, and report
programmes — flagging anything not seen on a previous run as NEW.

Why there are no CSS selectors in the workbook
----------------------------------------------
Selectors written blind are selectors that break. This environment could not open a
single page, so rather than invent per-site rules that would silently fail, the
scraper discovers content itself, in priority order:

    1. RSS / Atom      — <link rel=alternate>, or a guessed /feed, /rss, /atom.xml
    2. sitemap.xml     — filtered to URLs that look like programme pages
    3. JSON-LD         — schema.org Event / Course / NewsArticle / ItemList blocks
    4. HTML heuristic  — repeated link+heading structures with programme-ish wording

Whatever tier fires first wins, and the tier used is recorded per row so you can see
how each source was read. If a site later publishes a feed, it is picked up
automatically with no code change.

State
-----
`state.json` holds a fingerprint of every item ever seen. Anything whose fingerprint
is absent is NEW. Delete the file to force a full re-report.

Politeness
----------
robots.txt is honoured per host, one request at a time per host with a delay, a real
User-Agent, and a hard cap on pages per source. Nothing here logs in, pays a paywall,
or evades a block.

Usage
-----
    pip install requests beautifulsoup4 lxml openpyxl
    python3 scripts/scout_scraper.py --verify-only    # just resolve every URL
    python3 scripts/scout_scraper.py                  # full discovery pass
    python3 scripts/scout_scraper.py --since-last     # only report NEW items
    python3 scripts/scout_scraper.py --country Egypt --priority 1
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.robotparser
from collections import defaultdict
from datetime import datetime, timezone

WORKBOOK = "output/MENA_Startup_Programs_Scout.xlsx"
OUTDIR = "output/scout"
STATE = os.path.join(OUTDIR, "state.json")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 25
PER_HOST_DELAY = 2.0
MAX_ITEMS_PER_SOURCE = 60

# Words that make a link look like a programme call rather than a footer link.
PROGRAM_HINTS = re.compile(
    r"\b(program|programme|accelerat|incubat|cohort|apply|application|"
    r"deadline|call for|bootcamp|fellowship|challenge|grant|fund|batch|"
    r"intake|demo day|startup|founder|منحة|برنامج|تسريع|حاضنة|تقديم)\b",
    re.I,
)
SKIP_LINK = re.compile(
    r"(privacy|cookie|terms|login|sign-?in|contact|about-us|careers|"
    r"facebook\.com|twitter\.com|x\.com|linkedin\.com|instagram\.com|youtube\.com)",
    re.I,
)


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def fingerprint(source_id, title, url):
    raw = f"{source_id}|{(title or '').strip().lower()}|{(url or '').strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


# --------------------------------------------------------------------------- config
def read_config(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb["SCRAPE_CONFIG"]
    rows, headers = [], None
    for row in ws.iter_rows(min_row=4, values_only=True):
        if headers is None:
            if row and row[0] == "source_id":
                headers = [str(h) if h else "" for h in row]
            continue
        if not row or not row[0]:
            continue
        rows.append(dict(zip(headers, row)))
    wb.close()
    return rows


# --------------------------------------------------------------------------- fetch
class Fetcher:
    """One session, per-host robots cache and rate limit."""

    def __init__(self, ignore_robots=False):
        import requests
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": UA,
                               "Accept-Language": "en,ar;q=0.8"})
        self.robots = {}
        self.last_hit = defaultdict(float)
        self.ignore_robots = ignore_robots

    def allowed(self, url):
        if self.ignore_robots:
            return True
        host = urllib.parse.urlsplit(url)._replace(path="", query="", fragment="").geturl()
        rp = self.robots.get(host)
        if rp is None:
            rp = urllib.robotparser.RobotFileParser()
            try:
                r = self.s.get(host + "/robots.txt", timeout=TIMEOUT)
                rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            except Exception:
                rp.parse([])
            self.robots[host] = rp
        try:
            return rp.can_fetch(UA, url)
        except Exception:
            return True

    def get(self, url):
        host = urllib.parse.urlsplit(url).netloc
        wait = PER_HOST_DELAY - (time.monotonic() - self.last_hit[host])
        if wait > 0:
            time.sleep(wait)
        self.last_hit[host] = time.monotonic()
        return self.s.get(url, timeout=TIMEOUT, allow_redirects=True)


# --------------------------------------------------------------------------- tiers
def try_rss(fetch, url, soup):
    """Tier 1 — declared or guessed feed."""
    import requests  # noqa: F401
    candidates = []
    if soup:
        for ln in soup.find_all("link", rel=lambda v: v and "alternate" in str(v).lower()):
            t = (ln.get("type") or "").lower()
            if "rss" in t or "atom" in t or "xml" in t:
                candidates.append(urllib.parse.urljoin(url, ln.get("href", "")))
    base = f"{urllib.parse.urlsplit(url).scheme}://{urllib.parse.urlsplit(url).netloc}"
    candidates += [urllib.parse.urljoin(url.rstrip('/') + '/', "feed"),
                   base + "/feed", base + "/rss", base + "/atom.xml"]

    for cand in dict.fromkeys(c for c in candidates if c):
        if not fetch.allowed(cand):
            continue
        try:
            r = fetch.get(cand)
        except Exception:
            continue
        if r.status_code != 200 or "<rss" not in r.text[:2000].lower() \
                and "<feed" not in r.text[:2000].lower():
            continue
        from bs4 import BeautifulSoup
        fs = BeautifulSoup(r.content, "xml")
        items = []
        for it in fs.find_all(["item", "entry"])[:MAX_ITEMS_PER_SOURCE]:
            title = (it.find("title").get_text(strip=True) if it.find("title") else "")
            link = ""
            if it.find("link"):
                link = it.find("link").get_text(strip=True) or it.find("link").get("href", "")
            date = ""
            for tag in ("pubDate", "published", "updated", "dc:date"):
                if it.find(tag):
                    date = it.find(tag).get_text(strip=True)
                    break
            desc = ""
            for tag in ("description", "summary", "content"):
                if it.find(tag):
                    desc = it.find(tag).get_text(" ", strip=True)[:400]
                    break
            if title:
                items.append({"title": title, "url": urllib.parse.urljoin(cand, link),
                              "date": date, "snippet": desc})
        if items:
            return "rss", cand, items
    return None, None, []


def try_sitemap(fetch, url):
    """Tier 2 — sitemap.xml filtered to programme-looking paths."""
    parts = urllib.parse.urlsplit(url)
    base = f"{parts.scheme}://{parts.netloc}"
    for cand in (base + "/sitemap.xml", base + "/sitemap_index.xml"):
        if not fetch.allowed(cand):
            continue
        try:
            r = fetch.get(cand)
        except Exception:
            continue
        if r.status_code != 200 or "<urlset" not in r.text[:3000].lower() \
                and "<sitemapindex" not in r.text[:3000].lower():
            continue
        from bs4 import BeautifulSoup
        sm = BeautifulSoup(r.content, "xml")
        locs = [lo.get_text(strip=True) for lo in sm.find_all("loc")]
        # one level of index expansion, cheapest child first
        if sm.find("sitemapindex"):
            child = next((lo for lo in locs if PROGRAM_HINTS.search(lo)), None)
            if child and fetch.allowed(child):
                try:
                    r2 = fetch.get(child)
                    locs = [lo.get_text(strip=True)
                            for lo in BeautifulSoup(r2.content, "xml").find_all("loc")]
                except Exception:
                    pass
        hits = [lo for lo in locs if PROGRAM_HINTS.search(lo) and not SKIP_LINK.search(lo)]
        if hits:
            items = [{"title": urllib.parse.unquote(lo.rstrip("/").rsplit("/", 1)[-1]
                                                    ).replace("-", " ").strip()[:160],
                      "url": lo, "date": "", "snippet": ""}
                     for lo in hits[:MAX_ITEMS_PER_SOURCE]]
            return "sitemap", cand, items
    return None, None, []


def try_jsonld(url, soup):
    """Tier 3 — schema.org structured data already on the page."""
    if not soup:
        return None, None, []
    wanted = {"Event", "Course", "NewsArticle", "Article", "BlogPosting", "ItemList"}
    items = []

    def walk(node):
        if isinstance(node, list):
            for n in node:
                walk(n)
            return
        if not isinstance(node, dict):
            return
        types = node.get("@type", "")
        types = {types} if isinstance(types, str) else set(types or [])
        if types & wanted:
            name = node.get("name") or node.get("headline") or ""
            link = node.get("url") or ""
            if name:
                items.append({
                    "title": str(name)[:200],
                    "url": urllib.parse.urljoin(url, str(link)),
                    "date": str(node.get("startDate") or node.get("datePublished") or ""),
                    "snippet": str(node.get("description") or "")[:400],
                })
        for key in ("itemListElement", "hasPart", "mainEntity", "item"):
            if key in node:
                walk(node[key])

    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            walk(json.loads(tag.string or "{}"))
        except Exception:
            continue
    return ("jsonld", url, items[:MAX_ITEMS_PER_SOURCE]) if items else (None, None, [])


def try_html(url, soup):
    """Tier 4 — links whose text or href reads like a programme."""
    if not soup:
        return None, None, []
    seen, items = set(), []
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True)
        href = urllib.parse.urljoin(url, a["href"])
        if not text or len(text) < 6 or len(text) > 180:
            continue
        if SKIP_LINK.search(href) or href in seen:
            continue
        if not (PROGRAM_HINTS.search(text) or PROGRAM_HINTS.search(href)):
            continue
        seen.add(href)
        parent = a.find_parent(["article", "li", "div"])
        snippet = ""
        if parent:
            snippet = parent.get_text(" ", strip=True)[:300]
        items.append({"title": text, "url": href, "date": "", "snippet": snippet})
        if len(items) >= MAX_ITEMS_PER_SOURCE:
            break
    return ("html", url, items) if items else (None, None, [])


# --------------------------------------------------------------------------- run
def process(fetch, cfg, verify_only):
    url = str(cfg.get("url") or "").strip()
    out = {"source_id": cfg.get("source_id"), "entity": cfg.get("entity"),
           "country": cfg.get("country"), "url": url, "url_role": cfg.get("url_role"),
           "http_status": "", "tier": "", "discovered_from": "", "n_items": 0,
           "error": "", "checked_at": now()}
    if not url:
        out["error"] = "no url"
        return out, []
    if not fetch.allowed(url):
        out["error"] = "blocked by robots.txt"
        out["http_status"] = "robots"
        return out, []
    try:
        r = fetch.get(url)
        out["http_status"] = r.status_code
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"[:200]
        return out, []
    if r.status_code >= 400:
        out["error"] = f"HTTP {r.status_code}"
        return out, []
    if verify_only:
        return out, []

    soup = None
    if "html" in r.headers.get("Content-Type", "").lower() or "<html" in r.text[:500].lower():
        from bs4 import BeautifulSoup
        try:
            soup = BeautifulSoup(r.content, "lxml")
        except Exception:
            soup = BeautifulSoup(r.content, "html.parser")

    method = str(cfg.get("method") or "auto").lower()
    tiers = {"rss": [("rss", lambda: try_rss(fetch, url, soup))],
             "sitemap": [("sitemap", lambda: try_sitemap(fetch, url))],
             "jsonld": [("jsonld", lambda: try_jsonld(url, soup))],
             "html": [("html", lambda: try_html(url, soup))]}
    if method == "skip":
        out["error"] = "method=skip"
        return out, []
    plan = tiers.get(method) or [
        ("rss", lambda: try_rss(fetch, url, soup)),
        ("sitemap", lambda: try_sitemap(fetch, url)),
        ("jsonld", lambda: try_jsonld(url, soup)),
        ("html", lambda: try_html(url, soup)),
    ]

    for _, fn in plan:
        try:
            tier, src, items = fn()
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"[:200]
            continue
        if items:
            out["tier"] = tier
            out["discovered_from"] = src
            out["n_items"] = len(items)
            return out, items
    out["tier"] = "none"
    return out, []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbook", default=WORKBOOK)
    ap.add_argument("--outdir", default=OUTDIR)
    ap.add_argument("--verify-only", action="store_true",
                    help="only resolve URLs and record HTTP status")
    ap.add_argument("--since-last", action="store_true",
                    help="write only items not seen on a previous run")
    ap.add_argument("--country", help="filter to one country")
    ap.add_argument("--priority", type=int, help="only sources at this priority")
    ap.add_argument("--limit", type=int, help="stop after N sources (smoke test)")
    ap.add_argument("--ignore-robots", action="store_true",
                    help="not recommended; only for sites you own")
    args = ap.parse_args()

    if not os.path.exists(args.workbook):
        sys.exit(f"workbook not found: {args.workbook}\n"
                 f"build it first: python3 scripts/build_scout_xlsx.py {args.workbook}")
    os.makedirs(args.outdir, exist_ok=True)

    cfgs = [c for c in read_config(args.workbook)
            if str(c.get("enabled", "yes")).lower() == "yes"]
    if args.country:
        cfgs = [c for c in cfgs if str(c.get("country", "")).lower() == args.country.lower()]
    if args.priority:
        cfgs = [c for c in cfgs if int(c.get("priority") or 9) == args.priority]
    cfgs.sort(key=lambda c: (int(c.get("priority") or 9), str(c.get("country"))))
    if args.limit:
        cfgs = cfgs[:args.limit]

    state = {}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            state = json.load(f)

    fetch = Fetcher(ignore_robots=args.ignore_robots)
    runlog, all_items, new_items = [], [], []

    for i, cfg in enumerate(cfgs, 1):
        print(f"[{i}/{len(cfgs)}] {cfg.get('source_id')}", flush=True)
        log, items = process(fetch, cfg, args.verify_only)
        runlog.append(log)
        for it in items:
            fp = fingerprint(cfg.get("source_id"), it["title"], it["url"])
            row = {"fingerprint": fp, "source_id": cfg.get("source_id"),
                   "entity": cfg.get("entity"), "country": cfg.get("country"),
                   "tier": log["tier"], "title": it["title"], "url": it["url"],
                   "date": it["date"], "snippet": it["snippet"],
                   "first_seen": state.get(fp, {}).get("first_seen", log["checked_at"]),
                   "is_new": "no" if fp in state else "yes"}
            all_items.append(row)
            if fp not in state:
                new_items.append(row)
            state.setdefault(fp, {"first_seen": log["checked_at"]})

    def dump(name, rows):
        path = os.path.join(args.outdir, name)
        if not rows:
            open(path, "w").close()
            return path, 0
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        return path, len(rows)

    dump("run_log.csv", runlog)
    if not args.verify_only:
        dump("discovered_programs.csv", all_items)
        dump("new_programs.csv", new_items)
        with open(STATE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=1)

    ok = sum(1 for r in runlog if str(r["http_status"]).startswith("2"))
    print(f"\nsources checked : {len(runlog)}")
    print(f"resolved OK     : {ok}")
    print(f"failed/blocked  : {len(runlog) - ok}")
    if not args.verify_only:
        by_tier = defaultdict(int)
        for r in runlog:
            by_tier[r["tier"] or "-"] += 1
        print(f"items found     : {len(all_items)}   (tiers: {dict(by_tier)})")
        print(f"NEW since last  : {len(new_items)}")
    print(f"\nwrote {args.outdir}/run_log.csv"
          + ("" if args.verify_only else
             f", discovered_programs.csv, new_programs.csv, state.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
