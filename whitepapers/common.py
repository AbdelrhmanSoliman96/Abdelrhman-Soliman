"""
Page furniture: the stylesheet, the cover, the closing page, and the block renderer.

The documents in `whitepapers/library/` hold nothing but content. Everything about
how that content looks lives here, so restyling the whole library is one edit.

These are institutional documents — partnership material, things a founder shows to
someone else — which the guidelines put in **calm mode**: "restrained, generous,
minimal colour ... anything that has to be believed rather than shared." Two rules
follow from that and are enforced below rather than left to judgement:

* the chain pattern is not used anywhere. It "never sits under body copy, under the
  logo, or on anything that has to be believed". A whitepaper is one of those things.
* lime is a ground and never ink. It fills the closing band and marks what has been
  earned. No sentence in these files is set in lime.
"""

import base64
import os
from . import brand as B
from . import figures as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _data_uri(path, mime):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return f"data:{mime};base64,{base64.b64encode(fh.read()).decode('ascii')}"


def assets():
    return {
        "font": _data_uri(B.SATOSHI_FILE, "font/woff2"),
        "logo_ink": _data_uri(B.LOGO_INK, "image/png"),
        "logo_white": _data_uri(B.LOGO_WHITE, "image/png"),
        "logo_stacked_white": _data_uri(B.LOGO_STACKED_WHITE, "image/png"),
    }


# ------------------------------------------------------------------ stylesheet

def stylesheet(a):
    t = B.TYPE_SCALE
    return f"""
@font-face {{
  font-family: 'StartPad Sans';
  src: url('{a["font"]}') format('woff2');
  font-weight: 300 800; font-style: normal; font-display: block;
}}

@page {{ size: A4; margin: 19mm 20mm 17mm 20mm; }}
@page :first {{ margin: 0; }}

* {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}

html {{ font-size: 12pt; }}
body {{
  margin: 0; font-family: {B.FONT_STACK};
  font-size: {t["body"]}; line-height: 1.62; color: {B.INK};
  font-variant-numeric: proportional-nums;
  -webkit-font-smoothing: antialiased;
}}

/* ------------------------------------------------------------------ cover */
.cover {{
  position: relative; width: 210mm; height: 297mm; margin: 0;
  background: {B.ULTRAVIOLET}; color: #fff;
  page-break-after: always; break-after: page;
  padding: 24mm 22mm 20mm 22mm; display: flex; flex-direction: column;
}}
.cover .mark {{ width: 44mm; }}
.cover .series {{
  margin-top: 16mm; font-size: 8.5pt; font-weight: 700; letter-spacing: .16em;
  text-transform: uppercase; color: #BFB4FA;
}}
.cover h1 {{
  margin: 6mm 0 0 0; font-size: 34pt; line-height: 1.06; font-weight: 800;
  letter-spacing: -0.022em; max-width: 150mm;
}}
.cover .standfirst {{
  margin-top: 7mm; font-size: 12.5pt; line-height: 1.5; font-weight: 400;
  color: #DCD6FD; max-width: 128mm;
}}
.cover .spacer {{ flex: 1 1 auto; }}
.cover .rule {{ height: 3px; background: {B.LIME}; width: 46mm; margin-bottom: 7mm; }}
.cover .foot {{ display: flex; justify-content: space-between; align-items: flex-end;
  font-size: 9pt; color: #CFC8FB; }}
.cover .foot strong {{ color: #fff; font-weight: 700; }}
.cover .missions {{ display: flex; gap: 2px; margin-bottom: 8mm; }}
.cover .missions i {{ height: 5px; flex: 1; border-radius: 1px; display: block; }}

/* ------------------------------------------------------- headings & blocks */
.label {{
  font-size: {t["label"]}; font-weight: 700; letter-spacing: .15em;
  text-transform: uppercase; color: {B.INK_FAINT}; margin: 0 0 3mm 0;
}}
h1.section {{
  font-size: {t["h1"]}; font-weight: 800; letter-spacing: -0.02em; line-height: 1.12;
  margin: 0 0 4mm 0; max-width: 150mm; break-after: avoid;
}}
h2 {{
  font-size: {t["h2"]}; font-weight: 700; letter-spacing: -0.012em; line-height: 1.24;
  margin: 9mm 0 2.5mm 0; break-after: avoid;
}}
h3 {{
  font-size: {t["h3"]}; font-weight: 700; margin: 6mm 0 1.5mm 0; break-after: avoid;
}}
.statement {{
  font-size: {t["statement"]}; font-weight: 800; line-height: 1.16;
  letter-spacing: -0.022em; margin: 0 0 6mm 0; max-width: 152mm; break-after: avoid;
}}
.lead {{
  font-size: 11.6pt; line-height: 1.55; color: {B.INK_SECONDARY};
  margin: 0 0 5mm 0; max-width: 152mm;
}}
p {{ margin: 0 0 3.4mm 0; max-width: 158mm; }}
strong {{ font-weight: 700; }}
em {{ font-style: normal; font-weight: 700; color: {B.ULTRAVIOLET}; }}

ul, ol {{ margin: 0 0 4mm 0; padding-left: 5.5mm; max-width: 156mm; }}
li {{ margin-bottom: 1.8mm; padding-left: 1mm; }}
ul li::marker {{ color: {B.INK_FAINT}; }}
ol li::marker {{ color: {B.ULTRAVIOLET}; font-weight: 700; }}

.numlist {{ margin: 0 0 4mm 0; }}
.numlist .row {{ display: flex; gap: 5mm; margin-bottom: 3.6mm; break-inside: avoid; }}
.numlist .n {{
  flex: 0 0 8mm; font-size: 15pt; font-weight: 800; color: {B.ULTRAVIOLET};
  line-height: 1.1; letter-spacing: -0.03em;
}}
.numlist .b {{ flex: 1; }}
.numlist .b b {{ display: block; font-weight: 700; margin-bottom: 0.6mm; }}
.numlist .b span {{ color: {B.INK_SECONDARY}; }}

.kv {{ margin: 0 0 4mm 0; border-top: 1px solid {B.HAIRLINE}; }}
.kv .row {{ display: flex; gap: 6mm; padding: 2.2mm 0; border-bottom: 1px solid {B.HAIRLINE};
  break-inside: avoid; }}
.kv .k {{ flex: 0 0 52mm; font-weight: 700; font-size: 9.4pt; }}
.kv .v {{ flex: 1; color: {B.INK_SECONDARY}; font-size: 9.4pt; }}

table {{
  width: 100%; border-collapse: collapse; margin: 0 0 4mm 0; font-size: 9.2pt;
  break-inside: avoid;
}}
th {{
  text-align: left; font-weight: 700; font-size: 8pt; letter-spacing: .06em;
  text-transform: uppercase; color: {B.INK_SECONDARY};
  border-bottom: 1.5px solid {B.INK}; padding: 2mm 3mm 1.6mm 0; vertical-align: bottom;
}}
td {{ padding: 2.2mm 3mm 2.2mm 0; border-bottom: 1px solid {B.HAIRLINE};
  vertical-align: top; color: {B.INK_SECONDARY}; }}
td:first-child {{ color: {B.INK}; font-weight: 600; }}
tr {{ break-inside: avoid; }}

.callout {{
  background: {B.WASH}; border-left: 3px solid {B.ULTRAVIOLET};
  padding: 4mm 5mm; margin: 0 0 4.5mm 0; break-inside: avoid;
}}
.callout b {{ display: block; font-size: 9.6pt; font-weight: 700; margin-bottom: 1.2mm; }}
.callout span {{ font-size: 9.4pt; color: {B.INK_SECONDARY}; }}

blockquote {{
  margin: 0 0 5mm 0; padding: 0 0 0 6mm; border-left: 3px solid {B.LIME};
  break-inside: avoid;
}}
blockquote p {{ font-size: 12.5pt; line-height: 1.4; font-weight: 600;
  letter-spacing: -0.01em; margin-bottom: 1.6mm; }}
blockquote cite {{ font-style: normal; font-size: 8.4pt; font-weight: 600;
  letter-spacing: .1em; text-transform: uppercase; color: {B.INK_FAINT}; }}

.say {{ display: flex; gap: 0; margin: 0 0 5mm 0; break-inside: avoid; }}
.say > div {{ flex: 1; }}
.say .hd {{ font-size: 8pt; font-weight: 700; letter-spacing: .14em;
  text-transform: uppercase; padding: 1.8mm 3mm; color: #fff; }}
.say .a .hd {{ background: {B.ULTRAVIOLET}; }}
.say .b .hd {{ background: {B.INK_FAINT}; }}
.say .it {{ padding: 2.4mm 3mm; border-bottom: 1px solid {B.HAIRLINE}; font-size: 9.2pt; }}
.say .b .it {{ color: {B.INK_MUTED}; }}

/* ---------------------------------------------------------------- figures */
figure {{ margin: 5mm 0 6mm 0; break-inside: avoid; }}
figure svg {{ display: block; }}
figcaption {{
  margin-top: 2.6mm; padding-top: 2mm; border-top: 1px solid {B.HAIRLINE};
  font-size: {t["caption"]}; line-height: 1.5; color: {B.INK_MUTED};
}}
figcaption b {{ color: {B.INK}; font-weight: 700; }}
figcaption .src {{ display: block; margin-top: 1mm; color: {B.INK_FAINT}; font-size: 7.6pt; }}

/* ------------------------------------------------------------- worksheets */
.work {{
  border: 1.5px solid {B.INK}; padding: 5mm 5mm 4mm 5mm; margin: 0 0 5mm 0;
  break-inside: avoid;
}}
.work > .hd {{ display: flex; justify-content: space-between; align-items: baseline;
  border-bottom: 1.5px solid {B.INK}; padding-bottom: 2mm; margin-bottom: 3.5mm; }}
.work > .hd b {{ font-size: 11pt; font-weight: 800; letter-spacing: -0.01em; }}
.work > .hd span {{ font-size: 7.6pt; font-weight: 700; letter-spacing: .13em;
  text-transform: uppercase; color: {B.INK_FAINT}; }}
.work .intro {{ font-size: 9pt; color: {B.INK_MUTED}; margin-bottom: 3.5mm; }}
.field {{ margin-bottom: 3.2mm; }}
.field .fl {{ font-size: 8.6pt; font-weight: 700; margin-bottom: 1.4mm; }}
.field .fh {{ font-size: 8pt; color: {B.INK_FAINT}; font-weight: 500; margin-bottom: 1.4mm; }}
.field .lines {{ }}
.field .lines i {{ display: block; border-bottom: 1px solid {B.INK_FAINT}; height: 7mm; }}
.field .box {{ border: 1px solid {B.INK_FAINT}; background: {B.WASH}; }}

.grid {{ display: flex; flex-wrap: wrap; gap: 2mm; margin: 0 0 5mm 0; break-inside: avoid; }}
.grid .cell {{ border: 1px solid {B.INK}; padding: 2.6mm 3mm; background: #fff; }}
.grid .cell b {{ display: block; font-size: 8.6pt; font-weight: 800; margin-bottom: 0.8mm; }}
.grid .cell span {{ display: block; font-size: 7.8pt; line-height: 1.4; color: {B.INK_MUTED}; }}

.check {{ margin: 0 0 5mm 0; }}
.check .row {{ display: flex; gap: 3mm; align-items: flex-start; padding: 2mm 0;
  border-bottom: 1px solid {B.HAIRLINE}; break-inside: avoid; }}
.check .bx {{ flex: 0 0 4mm; height: 4mm; border: 1.5px solid {B.INK}; margin-top: 0.6mm; }}
.check .tx {{ flex: 1; font-size: 9.2pt; }}
.check .tx b {{ font-weight: 700; }}
.check .tx span {{ display: block; color: {B.INK_MUTED}; font-size: 8.4pt; }}

.note {{ font-size: 8.6pt; color: {B.INK_MUTED}; border-top: 1px solid {B.HAIRLINE};
  padding-top: 2mm; margin: 0 0 4mm 0; }}

.sources {{ font-size: 8.4pt; color: {B.INK_MUTED}; margin: 0; padding-left: 5mm; }}
.sources li {{ margin-bottom: 1.6mm; }}
.sources a {{ color: {B.ULTRAVIOLET}; text-decoration: none; word-break: break-all; }}

.pb {{ break-before: page; page-break-before: always; }}
.keep {{ break-inside: avoid; }}

/* --------------------------------------------------------- closing pages */
.about {{ break-before: page; page-break-before: always; }}
/* The mark sits on white, never on the lime band. The horizontal lockup's symbol
   IS lime, so lime-on-lime would erase the counters the mark is built from — one
   of the four documented ways it breaks. */
.about .mark {{ width: 40mm; display: block; margin: 0 0 5mm 0; }}
.about .band {{
  background: {B.LIME}; padding: 6.5mm 7mm; margin: 0 0 6mm 0;
}}
.about .band .one {{
  font-size: 15pt; font-weight: 800; line-height: 1.24; letter-spacing: -0.018em;
  color: {B.INK}; max-width: 130mm;
}}
.about h2 {{ margin-top: 6mm; }}
.about .cols {{ display: flex; gap: 7mm; margin: 4mm 0 0 0; }}
.about .cols > div {{ flex: 1; }}
.about .url {{
  margin-top: 7mm; border-top: 2px solid {B.INK}; padding-top: 3mm;
  display: flex; justify-content: space-between; align-items: baseline;
}}
.about .url b {{ font-size: 16pt; font-weight: 800; letter-spacing: -0.01em; }}
.about .url span {{ font-size: 8.4pt; color: {B.INK_MUTED}; }}
.steps {{ margin: 3mm 0 0 0; }}
.steps .s {{ display: flex; gap: 4mm; padding: 2.4mm 0; border-top: 1px solid {B.HAIRLINE}; }}
.steps .s i {{ flex: 0 0 14mm; font-size: 7.6pt; font-weight: 700; letter-spacing: .12em;
  text-transform: uppercase; color: {B.ULTRAVIOLET}; font-style: normal; padding-top: 0.6mm; }}
.steps .s div {{ flex: 1; font-size: 9.2pt; }}
.steps .s div b {{ display: block; font-weight: 700; }}
.steps .s div span {{ color: {B.INK_MUTED}; font-size: 8.6pt; }}
"""


# ------------------------------------------------------------- block renderer

def render_blocks(blocks):
    out = []
    for blk in blocks:
        kind = blk[0]

        if kind == "label":
            out.append(f'<p class="label">{F.esc(blk[1])}</p>')
        elif kind == "h1":
            out.append(f'<h1 class="section">{blk[1]}</h1>')
        elif kind == "h2":
            out.append(f"<h2>{blk[1]}</h2>")
        elif kind == "h3":
            out.append(f"<h3>{blk[1]}</h3>")
        elif kind == "statement":
            out.append(f'<p class="statement">{blk[1]}</p>')
        elif kind == "lead":
            out.append(f'<p class="lead">{blk[1]}</p>')
        elif kind == "p":
            out.append(f"<p>{blk[1]}</p>")
        elif kind == "ul":
            items = "".join(f"<li>{i}</li>" for i in blk[1])
            out.append(f"<ul>{items}</ul>")
        elif kind == "ol":
            items = "".join(f"<li>{i}</li>" for i in blk[1])
            out.append(f"<ol>{items}</ol>")
        elif kind == "num":
            rows = "".join(
                f'<div class="row"><div class="n">{n}</div>'
                f'<div class="b"><b>{t}</b><span>{d}</span></div></div>'
                for n, t, d in blk[1])
            out.append(f'<div class="numlist">{rows}</div>')
        elif kind == "kv":
            rows = "".join(f'<div class="row"><div class="k">{k}</div>'
                           f'<div class="v">{v}</div></div>' for k, v in blk[1])
            out.append(f'<div class="kv">{rows}</div>')
        elif kind == "table":
            head = "".join(f"<th>{h}</th>" for h in blk[1])
            body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                           for r in blk[2])
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
        elif kind == "callout":
            out.append(f'<div class="callout"><b>{blk[1]}</b><span>{blk[2]}</span></div>')
        elif kind == "quote":
            cite = f"<cite>{F.esc(blk[2])}</cite>" if len(blk) > 2 and blk[2] else ""
            out.append(f"<blockquote><p>{blk[1]}</p>{cite}</blockquote>")
        elif kind == "say":
            a = "".join(f'<div class="it">{s}</div>' for s, _ in blk[1])
            b = "".join(f'<div class="it">{n}</div>' for _, n in blk[1])
            out.append(f'<div class="say"><div class="a"><div class="hd">Say</div>{a}</div>'
                       f'<div class="b"><div class="hd">Never say</div>{b}</div></div>')
        elif kind == "fig":
            _, builder, args, caption = blk[0], blk[1], blk[2], blk[3]
            source = blk[4] if len(blk) > 4 else None
            svg = F.BUILDERS[builder](**args)
            src = f'<span class="src">{source}</span>' if source else ""
            out.append(f"<figure>{svg}<figcaption>{caption}{src}</figcaption></figure>")
        elif kind == "work":
            _, title, tag, intro, fields = blk
            fs = []
            for f in fields:
                if f[0] == "lines":
                    hint = f'<div class="fh">{f[3]}</div>' if len(f) > 3 and f[3] else ""
                    li = "".join("<i></i>" for _ in range(f[2]))
                    fs.append(f'<div class="field"><div class="fl">{f[1]}</div>{hint}'
                              f'<div class="lines">{li}</div></div>')
                elif f[0] == "box":
                    hint = f'<div class="fh">{f[3]}</div>' if len(f) > 3 and f[3] else ""
                    fs.append(f'<div class="field"><div class="fl">{f[1]}</div>{hint}'
                              f'<div class="box" style="height:{f[2]}mm"></div></div>')
            intro_html = f'<div class="intro">{intro}</div>' if intro else ""
            out.append(f'<div class="work"><div class="hd"><b>{title}</b>'
                       f'<span>{tag}</span></div>{intro_html}{"".join(fs)}</div>')
        elif kind == "grid":
            _, cells, per_row, height = blk
            w = f"calc({100 / per_row:.4f}% - {2 * (per_row - 1) / per_row:.2f}mm)"
            cs = "".join(
                f'<div class="cell" style="width:{w};height:{height}mm">'
                f"<b>{t}</b><span>{p}</span></div>" for t, p in cells)
            out.append(f'<div class="grid">{cs}</div>')
        elif kind == "check":
            rows = "".join(
                f'<div class="row"><div class="bx"></div><div class="tx"><b>{t}</b>'
                f"<span>{d}</span></div></div>" for t, d in blk[1])
            out.append(f'<div class="check">{rows}</div>')
        elif kind == "note":
            out.append(f'<p class="note">{blk[1]}</p>')
        elif kind == "sources":
            items = "".join(f"<li>{s}</li>" for s in blk[1])
            out.append(f'<ol class="sources">{items}</ol>')
        elif kind == "break":
            out.append('<div class="pb"></div>')
        elif kind == "rule":
            out.append(f'<hr style="border:0;border-top:1px solid {B.HAIRLINE};margin:5mm 0">')
        else:
            raise ValueError(f"unknown block: {kind}")
    return "\n".join(out)


# ----------------------------------------------------------------- the cover

def cover(doc, a):
    # On the ultraviolet cover the spectrum's own dark end would disappear into the
    # ground, so the ribbon switches to white: lit for the missions this document
    # serves, held back for the rest. Same device, legible surface.
    active = set(doc["missions"])
    stops = "".join(
        f'<i style="background:#fff;opacity:{1 if (i + 1) in active else 0.24}"></i>'
        for i in range(len(B.MISSION_SPECTRUM)))
    return f"""
<section class="cover">
  <img class="mark" src="{a['logo_white']}" alt="StartPad">
  <div class="series">{F.esc(doc['series'])} · {F.esc(doc['number'])}</div>
  <h1>{doc['title']}</h1>
  <div class="standfirst">{doc['standfirst']}</div>
  <div class="spacer"></div>
  <div class="missions">{stops}</div>
  <div class="rule"></div>
  <div class="foot">
    <div>{doc['cover_foot']}</div>
    <div><strong>{B.URL}</strong></div>
  </div>
</section>"""


# ---------------------------------------------------------- the closing page
#
# Required on every file in the library. Written to the SAY / NEVER SAY rules: it
# states what the platform does and what it does not take, and it claims nothing
# about the reader's outcome. "You finished it. We just kept the file."

ABOUT_TITLE = "StartPad tells you the truth about whether you are ready, gets you ready, and gives you the proof."

ABOUT_BODY = [
    ("h2", "What it is"),
    ("p", "A founder-readiness platform for Egypt and the wider MENA region. It takes a "
          "young person who has an idea and no company, moves them through fifteen "
          "structured missions, and turns them into someone the ecosystem will take "
          "seriously — then issues verifiable proof of that."),
    ("p", "It is not a course platform, not an education brand and not a youth club. "
          "Nothing here is graded. Every mission ends in an artefact you own."),
    ("h2", "Three moves, always in this order"),
]

ABOUT_STEPS = [
    ("Truth", "Where you actually stand",
     "Measured against what programmes actually ask for, stated plainly, before any encouragement."),
    ("Readiness", "Fifteen structured missions",
     "They close the specific gaps the assessment found, in the order that matters. A route, not a curriculum."),
    ("Proof", "A verifiable credential",
     "The ecosystem can check it without asking you. You apply with a file, not a hope."),
]

ABOUT_CLOSE = [
    ("h2", "On your idea"),
    ("p", "StartPad earns when a founder gets into somewhere — an accelerator, a "
          "programme, a room. Taking a founder's idea would end that. Work submitted "
          "to a mission is sealed and timestamped to the person who submitted it, and "
          "the seal is the product."),
    ("p", "Nothing in this document asks you to give anything up to use it. It is yours "
          "to fill in, print, and hand to whoever needs to see it."),
]


def about_page(a):
    steps = "".join(
        f'<div class="s"><i>{i}</i><div><b>{t}</b><span>{d}</span></div></div>'
        for i, t, d in ABOUT_STEPS)
    return f"""
<section class="about">
  <p class="label">About</p>
  <img class="mark" src="{a['logo_ink']}" alt="StartPad">
  <div class="band">
    <div class="one">{ABOUT_TITLE}</div>
  </div>
  {render_blocks(ABOUT_BODY)}
  <div class="steps">{steps}</div>
  {render_blocks(ABOUT_CLOSE)}
  <div class="url">
    <b>{B.URL}</b>
    <span>Start with the readiness assessment. It is free and it takes about twenty minutes.</span>
  </div>
</section>"""


def document_html(doc):
    a = assets()
    body = render_blocks(doc["blocks"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{F.esc(doc['title'])}</title>
<style>{stylesheet(a)}</style>
</head><body>
{cover(doc, a)}
<main>{body}</main>
{about_page(a)}
</body></html>"""
