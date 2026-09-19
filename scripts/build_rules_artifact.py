# -*- coding: utf-8 -*-
"""
Build the participant-facing Mission Zero rules page from competition/rules.py.

Same source as the .docx, so what an entrant reads on their phone and what a judge
reads in the printed rules cannot disagree. Both languages ship in the HTML with
their own `dir`, Arabic first and visible at rest — this page is read mostly on
phones by Arabic speakers, so Arabic is the default state, not a toggle away.
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from competition.rules import VERSIONS  # noqa: E402

TODO = re.compile(r"\[([^\]]+)\]")
LABELS = {
    "ar": {"toggle": "English", "when": "متى", "what": "ماذا", "detail": "التفاصيل"},
    "en": {"toggle": "العربية", "when": "When", "what": "What", "detail": "Detail"},
}


def esc(text):
    out = html.escape(str(text)).replace("\n", "<br>")
    return TODO.sub(lambda m: '<mark class="todo">[%s]</mark>' % m.group(1), out)


def render_version(v):
    lang = v["lang"]
    L = LABELS[lang]
    hero = v["hero"]
    parts = ['<section class="hero">',
             '<p class="eyebrow">%s</p>' % esc(hero["eyebrow"]),
             '<h1>%s</h1>' % esc(hero["h1"]),
             '<p class="tagline">%s</p>' % esc(v["tagline"]),
             '<p class="sub">%s</p>' % esc(hero["sub"]),
             '<ul class="points">%s</ul>' % "".join(
                 "<li>%s</li>" % esc(p) for p in hero["points"]),
             '<a class="cta" href="https://startpad.me/" target="_blank" '
             'rel="noopener">%s</a>' % esc(hero["cta"]),
             '<p class="reassure">%s</p>' % esc(hero["reassurance"]),
             '</section>',
             '<main class="doc">',
             '<p class="stamp">%s &nbsp;·&nbsp; %s</p>' % (
                 esc(v["doc_title"]), esc(v["version_line"]))]

    for block in v["blocks"]:
        kind = block[0]
        if kind == "h":
            parts.append("<h2>%s</h2>" % esc(block[1]))
        elif kind == "p":
            parts.append("<p>%s</p>" % esc(block[1]))
        elif kind == "b":
            parts.append("<ul>%s</ul>" % "".join("<li>%s</li>" % esc(i)
                                                 for i in block[1]))
        elif kind == "n":
            parts.append("<ol>%s</ol>" % "".join("<li>%s</li>" % esc(i)
                                                 for i in block[1]))
        elif kind == "t":
            heads = "".join("<th>%s</th>" % esc(h) for h in block[1])
            rows = "".join(
                "<tr>%s</tr>" % "".join("<td>%s</td>" % esc(c) for c in row)
                for row in block[2])
            parts.append('<div class="tw"><table><thead><tr>%s</tr></thead>'
                         "<tbody>%s</tbody></table></div>" % (heads, rows))
        elif kind == "cal":
            rows = "".join(
                '<li><span class="when">%s</span>'
                '<span class="what"><b>%s</b>%s</span></li>' % (
                    esc(w), esc(t), "<em>%s</em>" % esc(d) if d else "")
                for w, t, d in block[1])
            parts.append('<ol class="cal">%s</ol>' % rows)

    parts.append("</main>")
    return ('<div class="page" dir="%s" lang="%s" data-lang-block="%s">%s</div>'
            % (v["dir"], lang, lang, "".join(parts)))


TEMPLATE = """<title>Mission Zero Rulebook</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Sora:wght@600;700&family=Karla:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --plum:#3B1B4D; --plum-deep:#2A1238; --citron:#C9E23F; --citron-ink:#5C6B12;
  --ground:#FBFAFC; --panel:#F2EFF5; --ink:#1A1220; --body:#3B3244;
  --muted:#6E6478; --rule:#E2DCE8; --rule-soft:#EFEAF3;
  --link:#6A2E8C; --warn:#9A5B12; --warn-wash:#F8EEDF;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --plum:#2B1338; --plum-deep:#1C0C26; --citron:#C9E23F; --citron-ink:#D7EC6B;
  --ground:#151019; --panel:#1E1725; --ink:#F2EDF6; --body:#CFC6D6;
  --muted:#958BA0; --rule:#2E2537; --rule-soft:#221B2A;
  --link:#D0A6E6; --warn:#DDA85C; --warn-wash:#2A1F10;
}}
:root[data-theme="dark"]{
  --plum:#2B1338; --plum-deep:#1C0C26; --citron:#C9E23F; --citron-ink:#D7EC6B;
  --ground:#151019; --panel:#1E1725; --ink:#F2EDF6; --body:#CFC6D6;
  --muted:#958BA0; --rule:#2E2537; --rule-soft:#221B2A;
  --link:#D0A6E6; --warn:#DDA85C; --warn-wash:#2A1F10;
}

*{box-sizing:border-box}
body{background:var(--ground);color:var(--body);
  font-family:"Karla","Cairo",system-ui,sans-serif;font-size:17px;line-height:1.65;
  -webkit-font-smoothing:antialiased}
[dir="rtl"]{font-family:"Cairo",system-ui,sans-serif;line-height:1.95}

/* top bar */
.bar{position:sticky;top:0;z-index:20;background:var(--plum);
  border-bottom:1px solid rgba(201,226,63,.28)}
.bar-in{max-width:46rem;margin:0 auto;padding:.6rem 1.15rem;display:flex;
  align-items:center;justify-content:space-between;gap:.8rem}
.bar .mark{font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--citron)}
.langbtn{font-family:"IBM Plex Mono",monospace;font-size:.7rem;letter-spacing:.08em;
  padding:.32rem .7rem;border-radius:100px;cursor:pointer;
  border:1px solid rgba(201,226,63,.5);background:transparent;color:#F3EFF7}
.langbtn:hover{background:rgba(201,226,63,.14)}
.langbtn:focus-visible{outline:2px solid var(--citron);outline-offset:2px}

/* hero */
.hero{background:var(--plum);color:#F4F0F8;padding:3rem 1.15rem 2.6rem}
.hero>*{max-width:46rem;margin-inline:auto}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.16em;
  text-transform:uppercase;color:var(--citron);margin:0 0 1rem}
[dir="rtl"] .eyebrow{font-family:"Cairo",sans-serif;letter-spacing:0;font-size:.82rem}
.hero h1{font-family:"Sora",system-ui,sans-serif;font-weight:700;
  font-size:clamp(2.6rem,10vw,4.2rem);line-height:.98;letter-spacing:-.03em;
  margin:0 0 .5rem;color:#fff}
[dir="rtl"] .hero h1{font-family:"Cairo",sans-serif;font-weight:700;line-height:1.2;
  letter-spacing:0;font-size:clamp(2.3rem,9vw,3.6rem)}
.tagline{font-size:1.08rem;color:var(--citron);margin:0 0 1.5rem;font-weight:600}
.sub{font-size:1.12rem;color:#E4DCEC;margin:0 0 1.5rem;max-width:34rem}
.points{list-style:none;padding:0;margin:0 0 1.9rem;max-width:36rem;display:grid;
  gap:.7rem}
.points li{position:relative;padding-inline-start:1.5rem;font-size:1rem;color:#EDE7F2}
.points li::before{content:"";position:absolute;inset-inline-start:0;top:.62em;
  width:.62rem;height:.62rem;background:var(--citron);border-radius:2px}
.cta{display:inline-block;background:var(--citron);color:#2A3305;font-weight:700;
  font-size:1.02rem;padding:.75rem 1.9rem;border-radius:100px;text-decoration:none;
  font-family:inherit}
.cta:hover{background:#D8EE5C}
.cta:focus-visible{outline:3px solid #fff;outline-offset:3px}
.reassure{margin:1.2rem 0 0;font-size:.93rem;color:#C9BDD4;max-width:34rem}

/* document */
.doc{max-width:46rem;margin:0 auto;padding:2.4rem 1.15rem 4.5rem}
.stamp{font-family:"IBM Plex Mono",monospace;font-size:.7rem;letter-spacing:.08em;
  color:var(--muted);margin:0 0 2rem;text-transform:uppercase}
[dir="rtl"] .stamp{font-family:"Cairo",sans-serif;letter-spacing:0;text-transform:none;
  font-size:.82rem}
h2{font-family:"Sora",system-ui,sans-serif;font-weight:600;font-size:1.3rem;
  line-height:1.3;color:var(--ink);margin:2.6rem 0 .6rem;padding-top:1.2rem;
  border-top:1px solid var(--rule);text-wrap:balance;position:relative}
h2::after{content:"";position:absolute;top:-1px;inset-inline-start:0;width:2.4rem;
  height:2px;background:var(--citron)}
[dir="rtl"] h2{font-family:"Cairo",sans-serif;font-weight:700;line-height:1.6;
  font-size:1.35rem}
.doc p{margin:0 0 1rem}
ul,ol{margin:0 0 1.2rem;padding-inline-start:1.3rem}
li{margin-bottom:.5rem}
li::marker{color:var(--link);font-weight:600}
b,strong{color:var(--ink)}

/* schedule */
.cal{list-style:none;padding:0;margin:.4rem 0 1.6rem;
  border-top:1px solid var(--rule-soft)}
.cal li{display:grid;grid-template-columns:7.5rem minmax(0,1fr);gap:0 1rem;
  padding:.75rem 0;border-bottom:1px solid var(--rule-soft);margin:0}
.cal .when{font-family:"IBM Plex Mono",monospace;font-size:.8rem;color:var(--link);
  font-weight:500;padding-top:.12rem}
[dir="rtl"] .cal .when{font-family:"Cairo",sans-serif;font-size:.92rem}
.cal .what b{display:block;color:var(--ink);font-weight:600}
.cal .what em{font-style:normal;font-size:.92rem;color:var(--muted)}

/* tables */
.tw{overflow-x:auto;margin:.6rem 0 1.6rem;border:1px solid var(--rule);
  border-radius:4px}
table{border-collapse:collapse;width:100%;font-size:.93rem;min-width:30rem}
th,td{text-align:start;padding:.62rem .8rem;border-bottom:1px solid var(--rule-soft);
  vertical-align:top}
thead th{background:var(--panel);font-family:"IBM Plex Mono",monospace;font-size:.66rem;
  letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500}
[dir="rtl"] thead th{font-family:"Cairo",sans-serif;letter-spacing:0;
  text-transform:none;font-size:.85rem;font-weight:600}
tbody tr:last-child td{border-bottom:0}
tbody td:first-child{color:var(--ink);font-weight:600}

.todo{background:var(--warn-wash);color:var(--warn);padding:.05em .35em;
  border-radius:2px;border-bottom:1px dashed var(--warn);font-weight:600}

[data-lang-block][hidden]{display:none!important}

@media (max-width:560px){
  body{font-size:16px}
  .cal li{grid-template-columns:minmax(0,1fr);gap:.15rem}
  .hero{padding:2.2rem 1.15rem 2.2rem}
}
@media print{.bar{display:none}[data-lang-block]{display:block!important}
  .hero{background:none;color:#000}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<header class="bar">
  <div class="bar-in">
    <span class="mark">Mission Zero &nbsp;×&nbsp; Techne</span>
    <div role="group" aria-label="Language">
      <button class="langbtn" type="button" data-set="ar" aria-pressed="true">العربية</button>
      <button class="langbtn" type="button" data-set="en" aria-pressed="false">English</button>
    </div>
  </div>
</header>

__PAGES__

<script>
(function () {
  var blocks = document.querySelectorAll("[data-lang-block]");
  var buttons = document.querySelectorAll(".langbtn");
  function show(lang) {
    blocks.forEach(function (b) { b.hidden = b.getAttribute("data-lang-block") !== lang; });
    buttons.forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-set") === lang));
    });
    try { localStorage.setItem("mission-zero-lang", lang); } catch (e) {}
  }
  buttons.forEach(function (b) {
    b.addEventListener("click", function () { show(b.getAttribute("data-set")); });
  });
  var saved = null;
  try { saved = localStorage.getItem("mission-zero-lang"); } catch (e) {}
  show(saved === "en" ? "en" : "ar");
})();
</script>
"""


def build(out_path):
    pages = []
    for v in VERSIONS:
        rendered = render_version(v)
        if v["lang"] != "ar":
            rendered = rendered.replace('data-lang-block="en"',
                                        'data-lang-block="en" hidden')
        pages.append(rendered)
    page = TEMPLATE.replace("__PAGES__", "\n".join(pages))
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/mission_zero_rules.html"
    p = build(out)
    print("wrote", p, os.path.getsize(p), "bytes")
