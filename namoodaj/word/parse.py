# -*- coding: utf-8 -*-
"""يحوّل وثيقة HTML المبنية إلى بنية JSON وسيطة يستهلكها مولّد ملف Word."""
import json, os, re
from bs4 import BeautifulSoup, NavigableString, Tag

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(BASE))
HTML = os.path.join(REPO, "dirasat-jadwa-markaz-tamkeen.html")
soup = BeautifulSoup(open(HTML, encoding="utf-8").read(), "html.parser")
figs = {f["i"]: f for f in json.load(open(BASE + "/figs/figs.json", encoding="utf-8"))}


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


def runs(el):
    """يحوّل محتوى عنصر إلى قائمة مقاطع نصية مع سماتها."""
    out = []

    def walk(node, b=False, i=False):
        if isinstance(node, NavigableString):
            t = re.sub(r"\s+", " ", str(node))
            if t.strip() or (out and t == " "):
                out.append({"text": t, "b": b, "i": i})
            return
        if not isinstance(node, Tag):
            return
        if node.name in ("script", "style"):
            return
        nb = b or node.name in ("strong", "b", "th")
        ni = i or node.name in ("em", "i")
        for c in node.children:
            walk(c, nb, ni)

    for c in el.children:
        walk(c)
    # دمج المقاطع المتجاورة المتطابقة السمات وتشذيب الأطراف
    merged = []
    for r in out:
        if merged and merged[-1]["b"] == r["b"] and merged[-1]["i"] == r["i"]:
            merged[-1]["text"] += r["text"]
        else:
            merged.append(dict(r))
    for r in merged:
        r["text"] = re.sub(r"\s+", " ", r["text"])
    if merged:
        merged[0]["text"] = merged[0]["text"].lstrip()
        merged[-1]["text"] = merged[-1]["text"].rstrip()
    return [r for r in merged if r["text"]]


def parse_table(tbl):
    cap = clean(tbl.caption.get_text()) if tbl.caption else ""
    head, body = [], []
    thead = tbl.find("thead")
    if thead:
        for tr in thead.find_all("tr"):
            head.append([{"runs": runs(c), "span": int(c.get("colspan", 1)),
                          "num": "num" in (c.get("class") or [])}
                         for c in tr.find_all(["th", "td"])])
    for tr in (tbl.find("tbody") or tbl).find_all("tr"):
        if thead and tr.find_parent("thead"):
            continue
        cls = tr.get("class") or []
        body.append({
            "cls": ("total" if "total" in cls else "sub" if "sub" in cls else ""),
            "cells": [{"runs": runs(c), "span": int(c.get("colspan", 1)),
                       "num": "num" in (c.get("class") or []),
                       "th": c.name == "th",
                       "pos": "pos" in (c.get("class") or []),
                       "neg": "neg" in (c.get("class") or [])}
                      for c in tr.find_all(["th", "td"])],
        })
    ncol = max([sum(c["span"] for c in r["cells"]) for r in body] +
               [sum(c["span"] for c in h) for h in head] + [1])
    return {"t": "table", "caption": cap, "head": head, "rows": body, "ncol": ncol}


def parse_list(el):
    items = []
    for li in el.find_all("li", recursive=False):
        items.append(runs(li))
    return {"t": "list", "ordered": el.name == "ol", "items": items}


def parse_box(el, kind):
    blocks = []
    h = el.find(["h4"])
    title = clean(h.get_text()) if h else ""
    for ch in el.children:
        if not isinstance(ch, Tag):
            continue
        if ch.name == "h4":
            continue
        if ch.name == "p":
            blocks.append({"t": "p", "runs": runs(ch)})
        elif ch.name in ("ul", "ol"):
            blocks.append(parse_list(ch))
    return {"t": "box", "kind": kind, "title": title, "blocks": blocks}


def parse_exhibit(el, idx):
    out = []
    tag = clean(el.select_one(".ex-tag").get_text()) if el.select_one(".ex-tag") else ""
    title = clean(el.select_one(".ex-title").get_text()) if el.select_one(".ex-title") else ""
    swot = el.select_one(".swot")
    if swot:
        quads = []
        for q in swot.find_all("div", recursive=False):
            quads.append({"title": clean(q.h4.get_text()) if q.h4 else "",
                          "items": [clean(li.get_text()) for li in q.find_all("li")]})
        out.append({"t": "swot", "tag": tag, "title": title, "quads": quads})
    elif idx in figs:
        f = figs[idx]
        out.append({"t": "fig", "file": f["file"], "tag": tag, "title": title,
                    "cap": f["cap"], "w": f["w"], "h": f["h"]})
    # جداول العرض البديل داخل <details> والملاحظات
    for d in el.select("details.tv table"):
        out.append(parse_table(d))
    note = el.select_one(".ex-note")
    if note:
        out.append({"t": "p", "runs": runs(note), "small": True})
    return out


def parse_container(node, ex_counter):
    blocks = []
    for ch in node.children:
        if not isinstance(ch, Tag):
            continue
        cls = ch.get("class") or []
        if ch.name == "p":
            blocks.append({"t": "p", "runs": runs(ch), "lead": "lead" in cls})
        elif ch.name == "h3":
            blocks.append({"t": "h2", "text": clean(ch.get_text())})
        elif ch.name == "h4":
            blocks.append({"t": "h3", "text": clean(ch.get_text())})
        elif ch.name in ("ul", "ol"):
            blocks.append(parse_list(ch))
        elif ch.name == "hr":
            continue
        elif "tbl-wrap" in cls:
            t = ch.find("table")
            if t:
                blocks.append(parse_table(t))
        elif "exhibit" in cls:
            blocks += parse_exhibit(ch, ex_counter[0])
            ex_counter[0] += 1
        elif "callout" in cls:
            kind = "warn" if "warn" in cls else "crit" if "crit" in cls else "note"
            blocks.append(parse_box(ch, kind))
        elif "disclaimer" in cls:
            blocks.append(parse_box(ch, "disclaimer"))
        elif "cards" in cls:
            items = []
            for card in ch.select(".card"):
                items.append({
                    "num": clean(card.select_one(".c-num").get_text()) if card.select_one(".c-num") else "",
                    "title": clean(card.h4.get_text()) if card.h4 else "",
                    "runs": runs(card.find("p")) if card.find("p") else [],
                })
            blocks.append({"t": "cards", "items": items})
        elif "tiles" in cls:
            items = []
            for tile in ch.select(".tile"):
                items.append({
                    "k": clean(tile.select_one(".k").get_text()) if tile.select_one(".k") else "",
                    "v": clean(tile.select_one(".v").get_text()) if tile.select_one(".v") else "",
                    "d": clean(tile.select_one(".d").get_text()) if tile.select_one(".d") else "",
                })
            blocks.append({"t": "tiles", "items": items})
        elif "sec-head" in cls:
            continue
        else:
            blocks += parse_container(ch, ex_counter)
    return blocks


# ═══ الغلاف ═══
cover = soup.select_one("header.cover")
doc = {
    "cover": {
        "eyebrow": clean(cover.select_one(".eyebrow").get_text()),
        "title": clean(cover.h1.get_text()),
        "lede": clean(cover.select_one(".lede").get_text()),
        "meta": [{"k": clean(d.dt.get_text()), "v": clean(d.dd.get_text())}
                 for d in cover.select(".meta > div")],
    },
    "toc": [{"n": clean(a.select_one(".n").get_text()),
             "t": clean(a.select_one("span:not(.n)").get_text())}
            for a in soup.select(".rail a")],
    "sections": [],
}

ex_counter = [0]
for sec in soup.select("main > section"):
    head = sec.select_one(".sec-head")
    doc["sections"].append({
        "num": clean(head.select_one(".sec-num").get_text()),
        "title": clean(head.h2.get_text()),
        "kicker": clean(head.select_one(".kicker").get_text()) if head.select_one(".kicker") else "",
        "blocks": parse_container(sec, ex_counter),
    })

foot = soup.select_one("footer.doc-foot")
doc["footer"] = [clean(p.get_text()) for p in foot.find_all("p")] if foot else []

json.dump(doc, open(BASE + "/doc.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ═══ ملخص ═══
from collections import Counter
c = Counter()
def count(bs):
    for b in bs:
        c[b["t"]] += 1
        if b["t"] == "box":
            count(b["blocks"])
for s in doc["sections"]:
    count(s["blocks"])
print("أقسام:", len(doc["sections"]), "| فهرس:", len(doc["toc"]))
print("كتل:", dict(c))
