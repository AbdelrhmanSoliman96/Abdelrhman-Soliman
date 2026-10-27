# -*- coding: utf-8 -*-
"""
Build the press-kit page from press/release.py.

Same source as the .docx and the .md exports, so the page a journalist reads and
the document they are sent cannot say different things. Both languages ship in
the HTML with their own `dir` attribute rather than being swapped by script, so
the page is correct at rest and the toggle only chooses which one is shown.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from press.release import NOTES_SOURCES, VERSIONS  # noqa: E402

# Bracketed spans are the fields the founder still has to fill in. They are marked
# in the page so they can't be published by accident.
TODO = re.compile(r"\[([^\]]+)\]")

LABELS = {
    "ar": {"toggle": "English", "sources": "مصادر التحقّق من الأرقام",
           "sources_note": "كل رقم في هذا البيان مأخوذ من المصادر التالية وقت "
                           "الصياغة. يُرجى مراجعتها قبل التوزيع.",
           "todo": "يحتاج استكمالًا", "end": "انتهى البيان"},
    "en": {"toggle": "العربية", "sources": "Fact-check sources",
           "sources_note": "Every figure in this release was taken from the pages "
                           "below at drafting time. Re-check them before "
                           "distribution.",
           "todo": "to complete", "end": "end of release"},
}

# The founder asked for three movements: the product, the deal, the acquirer.
# The document numbers them, so the rail numbers them too — it is describing a real
# sequence, not decorating one.
ORDINALS = {"ar": ["١", "٢", "٣"], "en": ["1", "2", "3"]}


def esc(text):
    out = html.escape(text)
    return TODO.sub(lambda m: '<mark class="todo">[%s]</mark>' % m.group(1), out)


def render_version(v):
    lang, direction = v["lang"], v["dir"]
    L = LABELS[lang]
    parts = []
    ordinal_i = [0]

    def rail(mark, cls="rail-mark"):
        return '<div class="%s">%s</div>' % (cls, mark)

    def row(mark, body, cls=""):
        return ('<div class="row %s">%s<div class="col">%s</div></div>'
                % (cls, mark, body))

    parts.append(row(
        rail(""),
        '<p class="kicker">%s</p>'
        '<h1 class="headline">%s</h1>'
        '<p class="subhead">%s</p>'
        '<p class="dateline">%s</p>' % (
            esc(v["kicker"]), esc(v["headline"]), esc(v["subhead"]),
            esc(v["dateline"])),
        "lede"))

    for block in v["blocks"]:
        kind = block[0]
        if kind == "h":
            # Only the three numbered movements get an ordinal in the rail.
            is_movement = ordinal_i[0] < 3 and (
                block[1].startswith(("أولًا", "ثانيًا", "ثالثًا", "1.", "2.", "3.")))
            if is_movement:
                mark = rail(ORDINALS[lang][ordinal_i[0]], "rail-mark rail-num")
                ordinal_i[0] += 1
            else:
                mark = rail("")
            parts.append(row(mark, '<h2>%s</h2>' % esc(block[1]), "sec"))
        elif kind == "p":
            parts.append(row(rail(""), '<p>%s</p>' % esc(block[1])))
        elif kind == "b":
            items = "".join("<li>%s</li>" % esc(i) for i in block[1])
            parts.append(row(rail(""), "<ul>%s</ul>" % items))
        elif kind == "q":
            proposed = "PROPOSED QUOTE" in block[1] or "اقتباس مقترح" in block[1]
            parts.append(row(
                rail("&ldquo;", "rail-mark rail-quote"),
                '<blockquote class="%s"><p>%s</p><cite>%s</cite></blockquote>' % (
                    "proposed" if proposed else "", esc(block[1]), esc(block[2])),
                "quote-row"))
        elif kind == "kv":
            rows = "".join(
                '<div class="kv"><dt>%s</dt><dd>%s</dd></div>' % (esc(k), esc(val))
                for k, val in block[1])
            parts.append(row(rail(""), '<dl class="kvlist">%s</dl>' % rows))

    src = "".join(
        '<li><span>%s</span><a href="%s" target="_blank" rel="noopener">%s</a></li>'
        % (html.escape(label), html.escape(url), html.escape(url))
        for label, url in NOTES_SOURCES)
    parts.append(row(rail(""),
                     '<div class="endmark">### <span>%s</span></div>' % L["end"],
                     "end-row"))
    parts.append(row(rail(""),
                     '<section class="sources"><h2>%s</h2><p class="note">%s</p>'
                     '<ul class="srclist">%s</ul></section>'
                     % (L["sources"], L["sources_note"], src),
                     "sec"))

    return ('<article class="doc" dir="%s" lang="%s" data-lang-block="%s">%s</article>'
            % (direction, lang, lang, "".join(parts)))


TEMPLATE = """<title>StartPad Launch Newsroom</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=Amiri:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {
  --ground:#FCFCFB; --surface:#F2F4F2; --ink:#14211F; --body:#26332F;
  --muted:#5F706B; --rule:#D8DEDA; --rule-soft:#E7ECE9;
  --accent:#0F5C4B; --accent-ink:#0F5C4B; --accent-wash:#E8F1ED;
  --bronze:#8A6E3C; --bronze-wash:#F5EFE3; --blue:#1D6FA3;
  --shadow:0 1px 0 rgba(20,33,31,.04);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground:#0E1513; --surface:#16201D; --ink:#EDF2EF; --body:#C9D4D0;
    --muted:#8CA09A; --rule:#2A3733; --rule-soft:#1E2A27;
    --accent:#5FBFA3; --accent-ink:#7FD3B9; --accent-wash:#15251F;
    --bronze:#C8A468; --bronze-wash:#221B0F; --blue:#6FB4DE;
    --shadow:none;
  }
}
:root[data-theme="dark"] {
  --ground:#0E1513; --surface:#16201D; --ink:#EDF2EF; --body:#C9D4D0;
  --muted:#8CA09A; --rule:#2A3733; --rule-soft:#1E2A27;
  --accent:#5FBFA3; --accent-ink:#7FD3B9; --accent-wash:#15251F;
  --bronze:#C8A468; --bronze-wash:#221B0F; --blue:#6FB4DE;
  --shadow:none;
}

* { box-sizing:border-box; }
body {
  background:var(--ground); color:var(--body);
  font-family:"IBM Plex Sans","IBM Plex Sans Arabic",system-ui,sans-serif;
  font-size:16px; line-height:1.62; -webkit-font-smoothing:antialiased;
}
[dir="rtl"] { font-family:"IBM Plex Sans Arabic","IBM Plex Sans",system-ui,sans-serif; }

/* ---- masthead ---- */
.masthead {
  position:sticky; top:0; z-index:10;
  background:color-mix(in srgb, var(--ground) 88%, transparent);
  backdrop-filter:blur(8px);
  border-bottom:1px solid var(--rule);
}
.masthead-in {
  max-width:64rem; margin:0 auto; padding:.85rem 1.5rem;
  display:flex; align-items:center; justify-content:space-between; gap:1rem;
}
.brand {
  font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:.72rem; letter-spacing:.16em; text-transform:uppercase;
  color:var(--accent-ink); font-weight:500;
}
.brand b { color:var(--ink); font-weight:500; }
.langs { display:flex; gap:.4rem; }
.langbtn {
  font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:.72rem; letter-spacing:.1em; text-transform:uppercase;
  padding:.34rem .7rem; border-radius:2px; cursor:pointer;
  border:1px solid var(--rule); background:transparent; color:var(--muted);
}
.langbtn[aria-pressed="true"] {
  background:var(--accent); border-color:var(--accent);
  color:var(--ground); font-weight:500;
}
.langbtn:focus-visible { outline:2px solid var(--blue); outline-offset:2px; }

/* ---- document grid: a rail for press marks, a column for reading ---- */
.doc { max-width:64rem; margin:0 auto; padding:2.6rem 1.5rem 4rem; }
.row {
  display:grid; grid-template-columns:4.5rem minmax(0,66ch);
  gap:0 1.6rem; align-items:start;
}
.col { min-width:0; }
.rail-mark {
  font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:.8rem; color:var(--muted); padding-top:.42rem;
  text-align:end; user-select:none;
}
.rail-num {
  font-size:1.35rem; color:var(--accent-ink); font-weight:500;
  padding-top:1.55rem; font-variant-numeric:tabular-nums;
}
[dir="rtl"] .rail-num { font-family:"IBM Plex Sans Arabic",sans-serif; }
.rail-quote { font-size:2.4rem; color:var(--rule); line-height:1; padding-top:.3rem; }

/* ---- release type ---- */
.kicker {
  font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:.7rem; letter-spacing:.18em; text-transform:uppercase;
  color:var(--bronze); margin:0 0 1.1rem;
}
[dir="rtl"] .kicker { font-family:"IBM Plex Sans Arabic",sans-serif; letter-spacing:0; }
.headline {
  font-family:"Newsreader",Georgia,serif; font-weight:600;
  font-size:clamp(1.9rem,4.2vw,2.9rem); line-height:1.16; letter-spacing:-.01em;
  color:var(--ink); margin:0 0 .9rem; text-wrap:balance;
}
[dir="rtl"] .headline {
  font-family:"Amiri",serif; font-weight:700; line-height:1.45;
  letter-spacing:0; font-size:clamp(1.75rem,3.9vw,2.6rem);
}
.subhead {
  font-family:"Newsreader",Georgia,serif; font-style:italic;
  font-size:1.16rem; line-height:1.5; color:var(--muted);
  margin:0 0 1.6rem; text-wrap:pretty;
}
[dir="rtl"] .subhead { font-family:"Amiri",serif; font-size:1.24rem; line-height:1.75; }
.dateline {
  font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:.78rem; letter-spacing:.06em; color:var(--ink);
  margin:0; padding:.55rem 0; border-top:2px solid var(--accent);
  border-bottom:1px solid var(--rule);
}
[dir="rtl"] .dateline { font-family:"IBM Plex Sans Arabic",sans-serif; letter-spacing:0; }
.lede .col { padding-bottom:1.4rem; }

h2 {
  font-family:"Newsreader",Georgia,serif; font-weight:600;
  font-size:1.42rem; line-height:1.3; color:var(--ink);
  margin:2.4rem 0 .7rem; padding-top:1.5rem;
  border-top:1px solid var(--rule-soft); text-wrap:balance;
}
[dir="rtl"] h2 { font-family:"Amiri",serif; font-weight:700; line-height:1.5; }
.doc p { margin:0 0 1rem; }
[dir="rtl"] .doc p { line-height:1.95; }
ul { margin:0 0 1.1rem; padding-inline-start:1.1rem; }
li { margin-bottom:.55rem; }
[dir="rtl"] li { line-height:1.9; }
li::marker { color:var(--accent); }

blockquote {
  margin:.2rem 0 1.6rem; padding-inline-start:1.1rem;
  border-inline-start:2px solid var(--accent);
}
blockquote p {
  font-family:"Newsreader",Georgia,serif; font-size:1.14rem; font-style:italic;
  line-height:1.6; color:var(--ink); margin:0 0 .6rem;
}
[dir="rtl"] blockquote p {
  font-family:"IBM Plex Sans Arabic",sans-serif; font-style:normal;
  font-size:1.05rem; line-height:1.95;
}
cite {
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-style:normal;
  font-size:.74rem; letter-spacing:.06em; text-transform:uppercase;
  color:var(--accent-ink);
}
[dir="rtl"] cite {
  font-family:"IBM Plex Sans Arabic",sans-serif; letter-spacing:0;
  text-transform:none; font-size:.84rem;
}
blockquote.proposed {
  border-inline-start-color:var(--bronze);
  background:var(--bronze-wash); padding:.9rem 1.1rem; border-radius:0 3px 3px 0;
}
[dir="rtl"] blockquote.proposed { border-radius:3px 0 0 3px; }
blockquote.proposed cite { color:var(--bronze); }

.kvlist { margin:0 0 1.2rem; display:grid; gap:.45rem; }
.kv { display:grid; grid-template-columns:9rem minmax(0,1fr); gap:.2rem .9rem; }
.kv dt {
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.74rem;
  letter-spacing:.06em; text-transform:uppercase; color:var(--muted);
  padding-top:.22rem;
}
[dir="rtl"] .kv dt {
  font-family:"IBM Plex Sans Arabic",sans-serif; letter-spacing:0;
  text-transform:none; font-size:.9rem;
}
.kv dd { margin:0; color:var(--body); }

.todo {
  background:var(--bronze-wash); color:var(--bronze);
  padding:.05em .35em; border-radius:2px;
  border-bottom:1px dashed var(--bronze); font-weight:500;
}

.endmark {
  font-family:"IBM Plex Mono",ui-monospace,monospace; color:var(--muted);
  letter-spacing:.3em; margin:2.2rem 0 .5rem; font-size:.9rem;
  display:flex; align-items:center; gap:.9rem;
}
.endmark span {
  letter-spacing:.1em; font-size:.68rem; text-transform:uppercase;
  color:var(--rule); }
[dir="rtl"] .endmark span { font-family:"IBM Plex Sans Arabic",sans-serif; }

.sources { margin-top:.5rem; }
.sources .note { color:var(--muted); font-size:.92rem; }
.srclist { list-style:none; padding:0; margin:1rem 0 0; display:grid; gap:.7rem; }
.srclist li {
  display:grid; gap:.15rem; padding-inline-start:.9rem;
  border-inline-start:2px solid var(--rule-soft); margin:0;
}
.srclist span { font-size:.9rem; color:var(--ink); }
.srclist a {
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.72rem;
  color:var(--blue); word-break:break-all; text-decoration:none;
  border-bottom:1px solid transparent; direction:ltr; display:inline-block;
}
.srclist a:hover { border-bottom-color:var(--blue); }
.srclist a:focus-visible { outline:2px solid var(--blue); outline-offset:2px; }

[data-lang-block][hidden] { display:none !important; }

@media (max-width:720px) {
  .row { grid-template-columns:minmax(0,1fr); }
  .rail-mark { display:none; }
  .rail-num { display:block; text-align:start; padding:1.6rem 0 0; }
  .kv { grid-template-columns:minmax(0,1fr); }
  .doc { padding:1.8rem 1.15rem 3rem; }
}
@media print {
  .masthead { display:none; }
  [data-lang-block] { display:block !important; }
  .row { grid-template-columns:minmax(0,1fr); }
  .rail-mark { display:none; }
}
@media (prefers-reduced-motion:reduce) { * { transition:none !important; } }
</style>

<header class="masthead">
  <div class="masthead-in">
    <span class="brand"><b>StartPad</b> &times; GrowthLabs &nbsp;/&nbsp; Press</span>
    <div class="langs" role="group" aria-label="Language">
      <button class="langbtn" type="button" data-set="ar" aria-pressed="true">العربية</button>
      <button class="langbtn" type="button" data-set="en" aria-pressed="false">English</button>
    </div>
  </div>
</header>

__DOCS__

<script>
(function () {
  var blocks = document.querySelectorAll("[data-lang-block]");
  var buttons = document.querySelectorAll(".langbtn");
  function show(lang) {
    blocks.forEach(function (b) { b.hidden = b.getAttribute("data-lang-block") !== lang; });
    buttons.forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-set") === lang));
    });
    try { localStorage.setItem("startpad-press-lang", lang); } catch (e) {}
  }
  buttons.forEach(function (b) {
    b.addEventListener("click", function () { show(b.getAttribute("data-set")); });
  });
  var saved = null;
  try { saved = localStorage.getItem("startpad-press-lang"); } catch (e) {}
  show(saved === "en" ? "en" : "ar");
})();
</script>
"""


def build(out_path):
    docs = []
    for v in VERSIONS:
        rendered = render_version(v)
        if v["lang"] != "ar":
            rendered = rendered.replace('data-lang-block="en"',
                                        'data-lang-block="en" hidden')
        docs.append(rendered)
    page = TEMPLATE.replace("__DOCS__", "\n".join(docs))
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/startpad_press_kit.html"
    p = build(out)
    print("wrote", p, os.path.getsize(p), "bytes")
