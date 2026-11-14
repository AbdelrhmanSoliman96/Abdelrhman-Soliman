# -*- coding: utf-8 -*-
import json, base64, os
from charts import *
from model import run, montecarlo, ROLES, CAPEX, PREOP, DEPOSIT, BASE

HERE = os.path.dirname(os.path.abspath(__file__))
M = run()
YRS = ["السنة 1", "السنة 2", "السنة 3", "السنة 4", "السنة 5"]
CAL = ["2027", "2028", "2029", "2030", "2031"]
_fig = [0]; _tab = [0]
TOC = []


def mn(v, d=2):
    return num(v / 1e6, d)


def pct(v, d=1):
    return f"{v * 100:.{d}f}%"


def sec(num_, title, lead=""):
    sid = f"S{num_:02d}"
    TOC.append((sid, num_, title))
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return (f'<section class="sec" id="{sid}"><div class="sec-head">'
            f'<div class="sec-num">{num_:02d}</div><h1>{title}</h1></div>{l}')


def end():
    return "</section>"


def h2(t): return f"<h2>{t}</h2>"
def h3(t): return f"<h3>{t}</h3>"
def p(t): return f"<p>{t}</p>"


def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def fig(body, title, source="تحليل فريق الدراسة", note=""):
    _fig[0] += 1
    n = f'<div class="fnote">{note}</div>' if note else ""
    return (f'<figure><figcaption><b>شكل ({_fig[0]}):</b> {title}</figcaption><div class="fig-body">{body}</div>'
            f'{n}<div class="src">المصدر: {source}</div></figure>')


def table(headers, rows, title, source="تحليل فريق الدراسة", cls="", widths=None, foot=None):
    _tab[0] += 1
    cg = ""
    if widths: cg = "<colgroup>" + "".join(f'<col style="width:{w}%">' for w in widths) + "</colgroup>"
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = ""
    for r in rows:
        rc = ""
        if isinstance(r, dict): rc, r = r["cls"], r["cells"]
        trs += f'<tr class="{rc}">' + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    ft = f'<div class="fnote">{foot}</div>' if foot else ""
    return (f'<div class="tbl {cls}"><div class="tcap"><b>جدول ({_tab[0]}):</b> {title}</div><table>{cg}<thead><tr>{th}</tr></thead>'
            f'<tbody>{trs}</tbody></table>{ft}<div class="src">المصدر: {source}</div></div>')


def kpis(items, cols=4):
    out = f'<div class="kpis c{cols}">'
    for v, lab, note in items:
        out += f'<div class="kpi"><div class="kv">{v}</div><div class="kl">{lab}</div><div class="kn">{note}</div></div>'
    return out + "</div>"


def callout(title, text, kind=""):
    return f'<div class="callout {kind}"><div class="ct">{title}</div><div>{text}</div></div>'


def grid(cells, cols=2, cls=""):
    return f'<div class="grid g{cols} {cls}">' + "".join(cells) + "</div>"


def card(title, body, cls=""):
    return f'<div class="card {cls}"><div class="card-t">{title}</div>{body}</div>'


def font_css():
    out = ""
    for fam, pref, ws in (("IBM Plex Sans Arabic", "ibm-plex-sans-arabic-arabic", (300, 400, 500, 600, 700)),
                          ("IBM Plex Sans", "ibm-plex-sans-latin", (400, 500, 600, 700))):
        for w in ws:
            b = base64.b64encode(open(f"{HERE}/fonts/{pref}-{w}-normal.woff2", "rb").read()).decode()
            out += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2');}}\n"
    return out


CSS = """
@page { size: A4; margin: 24mm 19mm 21mm 19mm;
  @top-right { content: "دراسة الجدوى الاقتصادية لمكتب تصميم داخلي في مصر"; font-family: 'IBM Plex Sans Arabic'; font-size: 8pt; color: #7C8691; border-bottom: .5pt solid #D5D9DE; padding-bottom: 2mm; vertical-align: bottom; }
  @top-left { content: "نوفمبر 2026  |  سري"; font-family: 'IBM Plex Sans Arabic'; font-size: 8pt; color: #7C8691; border-bottom: .5pt solid #D5D9DE; padding-bottom: 2mm; vertical-align: bottom; }
  @top-center { content: ""; border-bottom: .5pt solid #D5D9DE; }
  @bottom-left { content: counter(page); font-family: 'IBM Plex Sans'; font-size: 9pt; color: #12304A; font-weight: 600; }
  @bottom-right { content: "إدارة الاستشارات ودراسات الجدوى"; font-family: 'IBM Plex Sans Arabic'; font-size: 7.5pt; color: #9AA3AD; }
}
@page cover { margin: 0; @top-right{content:none;border:0} @top-left{content:none;border:0} @top-center{content:none;border:0} @bottom-left{content:none} @bottom-right{content:none} }
* { box-sizing: border-box; }
html { direction: rtl; }
body { margin: 0; font-family: 'IBM Plex Sans Arabic','IBM Plex Sans',sans-serif; font-size: 10.2pt; line-height: 1.82; color: #16212C; text-align: justify; text-justify: inter-word; -webkit-print-color-adjust: exact; print-color-adjust: exact; font-variant-numeric: lining-nums tabular-nums; }
p { margin: 0 0 3.2mm 0; orphans: 3; widows: 3; }
h1,h2,h3 { text-align: right; color: #12304A; line-height: 1.45; break-after: avoid; }
h1 { font-size: 21pt; font-weight: 700; margin: 0; }
h2 { font-size: 13.5pt; font-weight: 700; margin: 7mm 0 2.6mm; padding-right: 3mm; border-right: 3pt solid #C97A1E; }
h3 { font-size: 11pt; font-weight: 600; margin: 5mm 0 1.8mm; color: #1E4566; }
.sec { break-before: page; }
.sec-head { display: flex; align-items: center; gap: 5mm; border-bottom: 1.2pt solid #12304A; padding-bottom: 4mm; margin-bottom: 6mm; position: relative; }
.sec-num { font-family: 'IBM Plex Sans'; font-size: 34pt; font-weight: 700; color: #C97A1E; line-height: 1; }
.mark { position: absolute; left: 0; top: 0; font-size: 3pt; color: #fdfdfd; font-family: 'IBM Plex Sans'; direction: ltr; }
.lead { font-size: 11pt; color: #33414E; line-height: 1.9; margin-bottom: 5mm; }
ul { margin: 0 0 3.2mm; padding: 0 5mm 0 0; }
li { margin-bottom: 1.3mm; padding-right: 1mm; }
li::marker { color: #C97A1E; }
b, strong { font-weight: 600; }
.ltr { direction: ltr; unicode-bidi: isolate; font-family: 'IBM Plex Sans'; }
figure, .tbl { margin: 4.5mm 0 6mm; }
figure { break-inside: avoid; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
.tcap { break-after: avoid; }
.tbl .src, .tbl .fnote { break-before: avoid; }
figcaption, .tcap { font-size: 9.6pt; color: #12304A; text-align: right; margin-bottom: 2mm; font-weight: 500; }
figcaption b, .tcap b { font-weight: 700; }
.fig-body { border: .6pt solid #DDE1E6; border-radius: 2mm; padding: 3.5mm 3mm 2mm; background: #fff; }
svg.chart { width: 100%; height: auto; display: block; }
.src, .fnote { font-size: 7.8pt; color: #7C8691; text-align: right; margin-top: 1.4mm; line-height: 1.6; }
table { width: 100%; border-collapse: collapse; font-size: 8.9pt; line-height: 1.55; text-align: right; }
thead th { background: #12304A; color: #fff; font-weight: 600; padding: 2.1mm 2.4mm; text-align: right; border-left: .5pt solid #2C4B66; }
thead th:last-child { border-left: 0; }
tbody td { padding: 1.8mm 2.4mm; border-bottom: .5pt solid #E1E5E9; vertical-align: top; text-align: right; }
tbody tr:nth-child(even) td { background: #F6F8FA; }
tr.tot td { font-weight: 700; background: #EAF0F5 !important; border-top: .8pt solid #12304A; color: #12304A; }
tr.sub td { font-weight: 600; background: #F1F4F7 !important; }
.numt td:not(:first-child), .numt th:not(:first-child) { text-align: left; direction: ltr; font-family: 'IBM Plex Sans','IBM Plex Sans Arabic'; white-space: nowrap; }
.kpis { display: grid; gap: 3mm; margin: 4mm 0 6mm; break-inside: avoid; }
.kpis.c4 { grid-template-columns: repeat(4,1fr); } .kpis.c3 { grid-template-columns: repeat(3,1fr); } .kpis.c5 { grid-template-columns: repeat(5,1fr); }
.kpi { border: .6pt solid #DDE1E6; border-top: 2.4pt solid #12304A; border-radius: 1.5mm; padding: 3mm 3mm 2.6mm; text-align: right; background: #fff; }
.kv { font-family: 'IBM Plex Sans','IBM Plex Sans Arabic'; font-size: 16pt; font-weight: 700; color: #12304A; line-height: 1.25; }
.kl { font-size: 8.8pt; font-weight: 600; color: #16212C; margin-top: 1mm; line-height: 1.5; }
.kn { font-size: 7.6pt; color: #7C8691; line-height: 1.5; margin-top: .6mm; }
.callout { background: #F4F7FA; border-right: 3pt solid #12304A; padding: 3.2mm 4mm; margin: 4mm 0 5mm; border-radius: 1mm; break-inside: avoid; font-size: 9.7pt; }
.callout.cop { border-right-color: #C97A1E; background: #FBF6EE; }
.callout.good { border-right-color: #2E7D4F; background: #F0F7F2; }
.ct { font-weight: 700; color: #12304A; margin-bottom: 1mm; }
.grid { display: grid; gap: 3mm; margin: 4mm 0 5mm; }
.g2 { grid-template-columns: repeat(2,minmax(0,1fr)); } .g3 { grid-template-columns: repeat(3,minmax(0,1fr)); } .g4 { grid-template-columns: repeat(4,minmax(0,1fr)); } .g5 { grid-template-columns: repeat(5,minmax(0,1fr)); }
.card { border: .6pt solid #DDE1E6; border-radius: 1.6mm; padding: 3mm 3.4mm; font-size: 9pt; line-height: 1.7; text-align: right; break-inside: avoid; background: #fff; }
.card-t { font-weight: 700; color: #12304A; font-size: 10pt; margin-bottom: 1.4mm; padding-bottom: 1.2mm; border-bottom: .6pt solid #E1E5E9; }
.card ul { padding-right: 4mm; margin: 0; } .card li { margin-bottom: .8mm; }
.card.s { border-top: 2.4pt solid #2E7D4F; } .card.w { border-top: 2.4pt solid #B23A3A; } .card.o { border-top: 2.4pt solid #2A6DB0; } .card.t { border-top: 2.4pt solid #C98A00; }
.card.nv { background: #12304A; color: #fff; border: 0; } .card.nv .card-t { color: #fff; border-color: #35546F; }
.pill { display: inline-block; font-size: 7.8pt; font-weight: 600; padding: .3mm 2.2mm; border-radius: 3mm; background: #E8EEF4; color: #12304A; white-space: nowrap; }
.pill.g { background: #E2F1E7; color: #1F6A3D; } .pill.a { background: #FBF0D9; color: #8A5E00; } .pill.r { background: #F7E1E1; color: #972C2C; }
.flow { display: flex; gap: 1.5mm; margin: 4mm 0; break-inside: avoid; }
.step { flex: 1; background: #F4F7FA; border-radius: 1.4mm; padding: 2.6mm 2.2mm; text-align: center; font-size: 8.2pt; line-height: 1.55; border-bottom: 2.4pt solid #12304A; }
.step b { display: block; color: #12304A; font-size: 8.9pt; margin-bottom: .8mm; }
.step .n { font-family: 'IBM Plex Sans'; font-weight: 700; color: #C97A1E; font-size: 12pt; display: block; line-height: 1.2; }
.step small { color: #7C8691; font-size: 7.4pt; display: block; margin-top: .8mm; }
.org { text-align: center; margin: 4mm 0; break-inside: avoid; }
.org .row { display: flex; justify-content: center; gap: 1.5mm; margin-bottom: 5mm; position: relative; }
.org .box { background: #fff; border: .7pt solid #12304A; border-radius: 1.4mm; padding: 1.8mm 2.4mm; font-size: 7.6pt; line-height: 1.5; min-width: 0; flex: 1 1 0; max-width: 42mm; }
.org .box.top { background: #12304A; color: #fff; max-width: 60mm; } .org .box.mid { background: #EAF0F5; font-weight: 600; }
.org .box small { display: block; color: #7C8691; font-size: 7.3pt; } .org .box.top small { color: #C9D4DE; }
.org .row:not(:last-child)::after { content: ""; position: absolute; bottom: -5mm; right: 50%; height: 5mm; border-right: .7pt solid #12304A; }
.gantt td, .gantt th { padding: 1.5mm 1.6mm; font-size: 8.2pt; } .gantt td.on { background: #2A6DB0 !important; border-left: 1pt solid #fff; } .gantt td.ms { background: #C97A1E !important; border-left: 1pt solid #fff; }
.gantt td:not(:first-child), .gantt th:not(:first-child) { text-align: center; width: 6.4%; }
.rm { border-collapse: separate; border-spacing: 1mm; font-size: 8.4pt; } .rm td { text-align: center; height: 11mm; width: 16%; border: 0; border-radius: 1mm; font-family: 'IBM Plex Sans'; font-weight: 700; color: #16212C; background: #fff !important; }
.rm td.lab { background: transparent !important; font-family: 'IBM Plex Sans Arabic'; font-weight: 500; font-size: 8pt; color: #4A5561; width: 20%; }
.rm td.l1 { background: #DDEEDF !important; } .rm td.l2 { background: #F7EBC2 !important; } .rm td.l3 { background: #F3CF9C !important; } .rm td.l4 { background: #E9A9A0 !important; }
.cover { page: cover; height: 297mm; position: relative; background: #12304A; color: #fff; overflow: hidden; break-after: page; }
.cover .art { position: absolute; inset: 0; }
.cover .inner { position: absolute; right: 22mm; left: 22mm; top: 34mm; text-align: right; }
.cover .tag { font-size: 10.5pt; letter-spacing: .3pt; color: #E3B77E; font-weight: 500; }
.cover h1 { color: #fff; font-size: 33pt; line-height: 1.5; margin: 9mm 0 5mm; font-weight: 700; }
.cover .sub { font-size: 14pt; color: #D4DDE6; font-weight: 300; line-height: 1.8; max-width: 125mm; }
.cover .rule { width: 26mm; height: 2.2pt; background: #C97A1E; margin: 9mm 0; }
.cover .meta { position: absolute; right: 22mm; left: 22mm; bottom: 24mm; display: flex; justify-content: space-between; font-size: 9.6pt; color: #C9D4DE; line-height: 1.9; border-top: .6pt solid #3A5973; padding-top: 5mm; }
.cover .meta b { color: #fff; display: block; font-size: 10.5pt; }
.front { break-after: page; }
.front h1 { font-size: 19pt; border-bottom: 1.2pt solid #12304A; padding-bottom: 4mm; margin-bottom: 7mm; }
.toc { width: 100%; font-size: 10.4pt; } .toc td { border: 0; border-bottom: .5pt dotted #B9C1C9; padding: 2.5mm 1mm; background: transparent !important; }
.toc a { color: inherit; text-decoration: none; }
.toc td.n { width: 11mm; font-family: 'IBM Plex Sans'; font-weight: 700; color: #C97A1E; } .toc td.pg { width: 14mm; text-align: left; font-family: 'IBM Plex Sans'; font-weight: 600; color: #12304A; }
.verdict { background: #12304A; color: #fff; border-radius: 2mm; padding: 6mm 7mm; margin: 5mm 0; break-inside: avoid; }
.verdict .vt { font-size: 9.5pt; color: #E3B77E; font-weight: 500; } .verdict .vh { font-size: 19pt; font-weight: 700; line-height: 1.5; margin: 1mm 0 2mm; } .verdict p { color: #DCE4EB; margin: 0; font-size: 10pt; }
.two { display: grid; grid-template-columns: minmax(0,1.15fr) minmax(0,1fr); gap: 5mm; align-items: start; }
.small { font-size: 8.8pt; color: #4A5561; }
"""


def render(parts, title="دراسة جدوى مكتب تصميم داخلي"):
    html = (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{font_css()}{CSS}</style></head><body>' + "".join(parts) + "</body></html>")
    return html


_mc = montecarlo(10000)
_v = sorted(x[0] for x in _mc); _n = len(_mc)
MCS = dict(vals=[x[0] / 1e6 for x in _mc], p_tv=sum(x[0] > 0 for x in _mc) / _n, p_5y=sum(x[2] > 0 for x in _mc) / _n,
           p_cash=sum(x[3] < 0 for x in _mc) / _n, p5=_v[_n // 20] / 1e6, p50=_v[_n // 2] / 1e6, p95=_v[-_n // 20] / 1e6,
           mean=sum(_v) / _n / 1e6, p_irr=sum(x[1] > BASE['wacc'] for x in _mc) / _n)
