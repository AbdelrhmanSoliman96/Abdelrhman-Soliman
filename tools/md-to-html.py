#!/usr/bin/env python3
"""
Markdown -> styled HTML for StartPad / LEAP deliverables.

  python3 tools/md-to-html.py IN.md OUT.html "Title" [--rtl] [--print]

  (default)  English LTR, copy-button blocks on ```text fences
  --rtl      Arabic RTL, Noto Sans Arabic / IBM Plex Sans Arabic
  --print    A4 print stylesheet, local fonts, page break before each H2
             (pair with tools/html-to-pdf.js)
"""
import html
import re
import sys

COPY_JS = """document.querySelectorAll(".prompt").forEach(function(b){var t=b.querySelector(".copy"),p=b.querySelector("pre");
if(!t||!p)return;t.addEventListener("click",function(){var x=p.textContent,d=function(){t.textContent="Copied";
setTimeout(function(){t.textContent="Copy"},1600)};if(navigator.clipboard&&navigator.clipboard.writeText){
navigator.clipboard.writeText(x).then(d,function(){t.textContent="Press \\u2318C"})}else{var a=document.createElement("textarea");
a.value=x;document.body.appendChild(a);a.select();try{document.execCommand("copy");d()}catch(e){t.textContent="Press \\u2318C"}
document.body.removeChild(a)}})});"""

BASE = """
  *{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}}
  .wrap{max-width:62rem;margin:0 auto;padding:0 1.25rem 6rem}
  h1,h2,h3,h4{text-wrap:balance;margin:0;line-height:1.2}
  p{margin:.85rem 0}ul,ol{margin:.85rem 0;padding-inline-start:1.4rem}li{margin:.35rem 0}
  a{color:var(--accent);text-underline-offset:2px}
  a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:3px}
  hr{border:0;border-top:1px solid var(--rule-soft);margin:2.5rem 0}
  strong{font-weight:680}em{color:var(--ink-soft)}
  blockquote{margin:.9rem 0;padding:.4rem 1rem;border-inline-start:3px solid var(--accent);color:var(--ink-soft)}
  .table-scroll{overflow-x:auto;border:1px solid var(--rule);border-radius:3px;background:var(--surface);margin:1.25rem 0}
  table{border-collapse:collapse;width:100%;min-width:28rem;font-size:.92rem}
  th,td{text-align:start;padding:.6rem .8rem;border-bottom:1px solid var(--rule-soft);vertical-align:top}
  th{font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faint);
     font-weight:600;background:var(--surface-2)}
  tbody tr:last-child td{border-bottom:0}
  .prompt{border:1px solid var(--rule);border-radius:3px;background:var(--surface);overflow:hidden;margin:1rem 0 2rem}
  .prompt>header{display:flex;align-items:center;justify-content:space-between;gap:1rem;
     padding:.6rem .9rem;background:var(--surface-2);border-bottom:1px solid var(--rule)}
  .prompt>header .label{font-family:ui-monospace,Menlo,monospace;font-size:.7rem;letter-spacing:.08em;
     text-transform:uppercase;color:var(--ink-faint);font-weight:600;overflow:hidden;
     text-overflow:ellipsis;white-space:nowrap}
  .prompt>header .label b{color:var(--accent-ink);font-weight:700}
  .copy{font-family:ui-monospace,Menlo,monospace;font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;
     background:transparent;border:1px solid var(--rule);color:var(--ink-soft);padding:.25rem .55rem;
     border-radius:2px;cursor:pointer;white-space:nowrap;transition:background .15s,color .15s}
  .copy:hover{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}
  pre{margin:0;padding:1rem .9rem;overflow-x:auto;font-family:ui-monospace,Menlo,Consolas,monospace;
     font-size:.84rem;line-height:1.7;color:var(--ink);white-space:pre-wrap;word-wrap:break-word;background:var(--surface)}
  pre code{background:none;padding:0;font-size:inherit}
"""

LTR = """  :root{--paper:#F2F3F8;--surface:#FFFFFF;--surface-2:#EAEBF3;--ink:#14131C;--ink-soft:#4E4C60;
  --ink-faint:#7B7990;--rule:#D9DAE6;--rule-soft:#E7E8F0;--accent:#4530E8;--accent-ink:#2E1FB0;--on-accent:#FFF;}
  @media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#0F0E16;--surface:#191823;
  --surface-2:#221F30;--ink:#ECEBF3;--ink-soft:#A9A7BC;--ink-faint:#7D7B92;--rule:#2E2B3D;--rule-soft:#24222F;
  --accent:#9A88FF;--accent-ink:#C3B8FF;--on-accent:#14131C;}}
  :root[data-theme="dark"]{--paper:#0F0E16;--surface:#191823;--surface-2:#221F30;--ink:#ECEBF3;
  --ink-soft:#A9A7BC;--ink-faint:#7D7B92;--rule:#2E2B3D;--rule-soft:#24222F;--accent:#9A88FF;
  --accent-ink:#C3B8FF;--on-accent:#14131C;}
  body{margin:0;background:var(--paper);color:var(--ink);font-size:17px;line-height:1.65;
  -webkit-font-smoothing:antialiased;font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans Arabic",Arial,sans-serif}
  h1{font-size:clamp(2.1rem,5.5vw,3.2rem);font-weight:800;letter-spacing:-.04em;padding-block:3.25rem 1rem}
  h2{font-size:clamp(1.5rem,3.2vw,2rem);font-weight:800;margin-top:3rem;padding-top:2.25rem;
     border-top:2px solid var(--ink);letter-spacing:-.025em}
  h3{font-size:1.12rem;font-weight:700;margin-top:2.5rem;color:var(--accent-ink);
     font-family:ui-monospace,Menlo,monospace}
  h4{font-size:1rem;font-weight:700;margin:2rem 0 0}
  code{font-family:ui-monospace,Menlo,monospace;font-size:.88em;background:var(--surface-2);
     padding:.1em .35em;border-radius:2px}
"""

RTL = """  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');
  :root{--paper:#F5F4F0;--surface:#FFF;--surface-2:#EDEBE5;--ink:#15171C;--ink-soft:#4A4F5A;
  --ink-faint:#787F8C;--rule:#D8D5CC;--rule-soft:#E6E3DB;--accent:#0F5C4A;--accent-ink:#0B4437;
  --on-accent:#FFF;--warm:#8A6A28;}
  @media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#101215;--surface:#1A1D22;
  --surface-2:#23272E;--ink:#ECEDF0;--ink-soft:#A8AEB9;--ink-faint:#7B828F;--rule:#2F343C;
  --rule-soft:#262A31;--accent:#4FC9A9;--accent-ink:#79DCC0;--on-accent:#101215;--warm:#D9B26A;}}
  body{margin:0;background:var(--paper);color:var(--ink);font-size:17.5px;line-height:1.85;
  -webkit-font-smoothing:antialiased;font-family:'IBM Plex Sans Arabic',system-ui,Tahoma,sans-serif}
  .wrap{max-width:60rem}
  h1{font-size:clamp(1.9rem,5vw,2.9rem);font-weight:700;padding-block:3rem 1rem;color:var(--accent-ink);line-height:1.35}
  h2{font-size:clamp(1.35rem,3vw,1.85rem);font-weight:700;margin-top:3rem;padding-top:2rem;
     border-top:2px solid var(--ink);line-height:1.35}
  h3{font-size:1.15rem;font-weight:700;margin-top:2.25rem;color:var(--accent-ink);line-height:1.4}
  h4{font-size:1.02rem;font-weight:600;margin-top:1.75rem;color:var(--ink-soft)}
  em{font-style:normal}
  blockquote{background:var(--surface);border-radius:2px;border-inline-start-color:var(--warm)}
  code{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:.86em;background:var(--surface-2);
     padding:.12em .4em;border-radius:3px;direction:ltr;display:inline-block;unicode-bidi:embed}
  pre{direction:ltr;text-align:left;border:1px solid var(--rule);border-radius:4px;margin:1.2rem 0}
"""

PRINT = """  @font-face{font-family:'NSA';src:url('file:///root/.fonts/NotoSansArabic-400.ttf');font-weight:400}
  @font-face{font-family:'NSA';src:url('file:///root/.fonts/NotoSansArabic-500.ttf');font-weight:500}
  @font-face{font-family:'NSA';src:url('file:///root/.fonts/NotoSansArabic-600.ttf');font-weight:600}
  @font-face{font-family:'NSA';src:url('file:///root/.fonts/NotoSansArabic-700.ttf');font-weight:700}
  @page{size:A4;margin:22mm 16mm 20mm}
  :root{--paper:#fff;--surface:#F7F6F2;--surface-2:#F7F6F2;--ink:#15171C;--ink-soft:#4A4F5A;
  --ink-faint:#6E7480;--rule:#D8D5CC;--rule-soft:#EAE7E0;--accent:#0F5C4A;--accent-ink:#0F5C4A;
  --on-accent:#FFF;--warm:#8A6A28;}
  body{margin:0;background:#fff;color:var(--ink);font-family:'NSA','DejaVu Sans',sans-serif;
  font-size:10.2pt;line-height:1.82;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .wrap{max-width:none;margin:0;padding:0}
  h1,h2,h3,h4{break-after:avoid;page-break-after:avoid;line-height:1.4}
  h1{font-size:25pt;font-weight:700;color:var(--accent);padding:0 0 6pt}
  h2{font-size:15pt;font-weight:700;margin-top:20pt;padding-top:9pt;border-top:1.6pt solid var(--ink);
     break-before:page;page-break-before:always}
  h2:first-of-type{break-before:auto;page-break-before:auto}
  h3{font-size:11.6pt;font-weight:700;margin-top:15pt;color:var(--accent)}
  h4{font-size:10.4pt;font-weight:600;margin-top:12pt;color:var(--ink-soft)}
  p{margin:6pt 0;orphans:3;widows:3}
  .table-scroll{break-inside:avoid;page-break-inside:avoid;overflow:visible;margin:10pt 0}
  table{min-width:0;font-size:9pt}
  th,td{padding:4.5pt 7pt}th{font-size:7.8pt;text-transform:none;letter-spacing:.02em}
  code{font-family:'DejaVu Sans Mono',monospace;background:var(--surface);direction:ltr;
     display:inline-block;unicode-bidi:embed;padding:.1em .3em;border-radius:2px;font-size:.86em}
  pre{margin:10pt 0;padding:9pt;direction:ltr;text-align:left;break-inside:avoid;
     font-family:'DejaVu Sans Mono',monospace;font-size:8.4pt;line-height:1.65;
     border:.7pt solid var(--rule);border-radius:3px}
  .prompt{break-inside:avoid}
"""


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<![">=])(https?://[^\s<)]+)', r'<a href="\1">\1</a>', s)
    return s


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def convert(src, dst, title, rtl=False, printmode=False):
    lines = open(src, encoding="utf-8").read().split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("```"):
            lang = ln[3:].strip()
            body, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i]); i += 1
            i += 1
            text = html.escape("\n".join(body), quote=False)
            label = ""
            for prev in reversed(out):
                m = re.search(r"<h2[^>]*>(PROMPT [A-Z][^<]*)</h2>", prev)
                if m:
                    head, _, rest = m.group(1).partition(" — ")
                    label = f"<b>{head}</b> · {rest}"
                    break
            if lang == "text" and not rtl:
                out.append(f'<div class="prompt"><header><span class="label">{label}</span>'
                           f'<button class="copy" type="button">Copy</button></header>'
                           f'<pre dir="auto"><code>{text}</code></pre></div>')
            else:
                out.append(f'<pre dir="auto"><code>{text}</code></pre>')
            continue

        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            head = cells(ln); i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(cells(lines[i])); i += 1
            th = "".join(f'<th dir="auto">{inline(c)}</th>' for c in head)
            tb = "".join("<tr>" + "".join(f'<td dir="auto">{inline(c)}</td>' for c in r) + "</tr>"
                         for r in rows)
            out.append(f'<div class="table-scroll"><table><thead><tr>{th}</tr></thead>'
                       f"<tbody>{tb}</tbody></table></div>")
            continue

        if ln.startswith("#"):
            lvl = len(ln) - len(ln.lstrip("#"))
            out.append(f'<h{lvl} dir="auto">{inline(ln[lvl:].strip())}</h{lvl}>')
            i += 1; continue

        if ln.strip() in ("---", "***", "___"):
            out.append("<hr>"); i += 1; continue

        if ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:]); i += 1
            out.append(f'<blockquote dir="auto">{inline(" ".join(buf))}</blockquote>')
            continue

        if re.match(r"^\s*([-*]|\d+\.)\s+", ln):
            ordered = bool(re.match(r"^\s*\d+\.\s+", ln))
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i])); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f'<li dir="auto">{inline(x)}</li>' for x in items) + f"</{tag}>")
            continue

        if ln.strip():
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(#|\||```|>|\s*([-*]|\d+\.)\s)", lines[i]) and \
                    lines[i].strip() not in ("---", "***", "___"):
                buf.append(lines[i].strip()); i += 1
            if buf:
                out.append(f'<p dir="auto">{inline(" ".join(buf))}</p>'); continue
        i += 1

    css = (PRINT if printmode else (RTL if rtl else LTR)) + BASE
    attrs = ' dir="rtl" lang="ar"' if rtl or printmode else ""
    script = "" if printmode else f"<script>{COPY_JS}</script>"
    doc = (f"<title>{html.escape(title)}</title>\n<style>\n{css}\n</style>\n"
           f'<div class="wrap"{attrs}>\n' + "\n".join(out) + f"\n</div>\n{script}\n")
    open(dst, "w", encoding="utf-8").write(doc)
    print(f"written {dst} ({len(doc)} bytes)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    convert(args[0], args[1], args[2] if len(args) > 2 else "Document",
            rtl="--rtl" in flags, printmode="--print" in flags)
