"""
Link checker for the curated resource library.

The environment this mapping was compiled in blocked direct page fetches, so every
resource URL is search-index verified rather than fetch-verified. Run this from an
unrestricted network before publishing anything to startpad.me, and quarterly after.

    python3 scripts/check_links.py            # check all
    python3 scripts/check_links.py --json     # machine-readable

Exit code is non-zero if any link fails, so this can gate a publish step in CI.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from startpad.resources import BY_MISSION, FOUNDATION, FUNDRAISING  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 20


def collect():
    seen, out = set(), []
    buckets = [("foundation", FOUNDATION), ("fundraising", FUNDRAISING)]
    buckets += [(f"M{mid}", items) for mid, items in sorted(BY_MISSION.items())]
    for where, items in buckets:
        for kind, title, source, url, _, _, _ in items:
            if url in seen:
                continue
            seen.add(url)
            out.append({"where": where, "kind": kind, "title": title,
                        "source": source, "url": url})
    return out


def check(entry):
    req = urllib.request.Request(entry["url"], headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            entry["status"] = r.status
            entry["final_url"] = r.geturl()
            entry["ok"] = 200 <= r.status < 400
            # A YouTube video that has been removed still returns 200; look for the marker.
            if "youtube.com/watch" in entry["url"]:
                body = r.read(200_000).decode("utf-8", "ignore")
                if "isPlayable\":false" in body or "Video unavailable" in body:
                    entry["ok"] = False
                    entry["status"] = "200 but video unavailable"
    except urllib.error.HTTPError as e:
        entry["status"] = e.code
        entry["ok"] = False
    except Exception as e:  # noqa: BLE001 - report anything that stopped the fetch
        entry["status"] = f"{type(e).__name__}: {e}"
        entry["ok"] = False
    return entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    entries = collect()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        results = list(ex.map(check, entries))

    failed = [r for r in results if not r["ok"]]
    if args.json:
        print(json.dumps(results, indent=1, ensure_ascii=False))
    else:
        for r in results:
            mark = "OK  " if r["ok"] else "FAIL"
            print(f'{mark} [{r["where"]:>10}] {str(r["status"]):<28} {r["url"]}')
        print(f"\n{len(results) - len(failed)}/{len(results)} links OK")
        if failed:
            print("\nFailed:")
            for r in failed:
                print(f'  {r["where"]}  {r["title"]}\n    {r["url"]}  ->  {r["status"]}')
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
