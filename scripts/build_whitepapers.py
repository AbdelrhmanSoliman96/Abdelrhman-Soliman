"""
Render the founder resource library to PDF.

Pipeline: content module -> HTML with embedded font and vector figures -> headless
Chromium -> PDF -> metadata rewritten so each file identifies itself as a StartPad
publication.

Chromium is used rather than a PDF drawing library because these documents are
mostly typography, and a browser is the only thing here that can hyphenate, keep a
heading with its paragraph, and avoid breaking a worksheet across a page. The
figures stay vector all the way through, so they are sharp at any zoom.

    python3 scripts/build_whitepapers.py            # everything
    python3 scripts/build_whitepapers.py tk01 wp02  # a subset, by slug prefix
"""

import glob
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright        # noqa: E402
from pypdf import PdfReader, PdfWriter                 # noqa: E402

from whitepapers import brand as B                     # noqa: E402
from whitepapers import common as C                    # noqa: E402
from whitepapers.library import LIBRARY                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output", "resources")
HTML_OUT = os.path.join(ROOT, "output", "resources", "_html")

# A fixed build date keeps the PDFs byte-stable between runs, so a rebuild that
# changed nothing produces no diff.
FIXED_DATE = datetime.datetime(2026, 1, 1, 0, 0, 0)


def chromium_binary():
    """
    Find the installed Chromium.

    The Playwright package and the browser bundle on this machine are not always the
    same revision, and Playwright refuses to start when they disagree. Resolving the
    binary ourselves means the build works against whichever bundle is present.
    """
    for pattern in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                    "/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell"):
        found = sorted(glob.glob(pattern))
        if found:
            return found[-1]
    return None


def footer_template(doc):
    """
    The running foot. It carries the page number, which needs Chromium's own
    templating, and is suppressed on the cover by that page's zero margin: with no
    bottom margin there is nowhere for it to render.
    """
    return f"""
<div style="width:100%;font-family:sans-serif;font-size:7pt;color:{B.INK_FAINT};
            padding:0 20mm;display:flex;justify-content:space-between;
            -webkit-print-color-adjust:exact;">
  <span>{C.F.esc(doc['title'])} &nbsp;·&nbsp; {B.URL}</span>
  <span class="pageNumber"></span>
</div>"""


def build_one(page, doc):
    slug = doc["slug"]
    html = C.document_html(doc)
    html_path = os.path.join(HTML_OUT, f"{slug}.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    page.goto("file://" + html_path, wait_until="networkidle")
    page.emulate_media(media="print")
    pdf_path = os.path.join(OUT, f"{doc['file']}.pdf")
    page.pdf(
        path=pdf_path,
        format="A4",
        print_background=True,
        display_header_footer=True,
        header_template="<div></div>",
        footer_template=footer_template(doc),
        margin={"top": "19mm", "bottom": "17mm", "left": "20mm", "right": "20mm"},
        prefer_css_page_size=True,
    )
    stamp_metadata(pdf_path, doc)
    return pdf_path


def stamp_metadata(path, doc):
    """
    Rewrite the document information dictionary.

    A browser leaves its own name in /Producer and /Creator. These files are
    published under StartPad's name, so the metadata says so and nothing else.
    """
    reader = PdfReader(path)
    writer = PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    writer.add_metadata({
        "/Title": doc["title"],
        "/Author": "StartPad",
        "/Subject": doc["standfirst_plain"],
        "/Keywords": ", ".join(doc["keywords"]),
        "/Creator": "StartPad",
        "/Producer": "StartPad",
        "/CreationDate": FIXED_DATE.strftime("D:%Y%m%d%H%M%S+00'00'"),
        "/ModDate": FIXED_DATE.strftime("D:%Y%m%d%H%M%S+00'00'"),
    })
    with open(path, "wb") as fh:
        writer.write(fh)


def main(argv):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(HTML_OUT, exist_ok=True)
    wanted = [a.lower() for a in argv[1:]]
    docs = [d for d in LIBRARY if not wanted or any(d["slug"].startswith(w) for w in wanted)]
    if not docs:
        print("no documents matched", wanted)
        return 1

    with sync_playwright() as pw:
        binary = chromium_binary()
        browser = pw.chromium.launch(executable_path=binary,
                                     args=["--font-render-hinting=none"])
        page = browser.new_page()
        for doc in docs:
            path = build_one(page, doc)
            n = len(PdfReader(path).pages)
            size = os.path.getsize(path) / 1024
            print(f"  {os.path.basename(path):<58} {n:>3} pages  {size:>6.0f} KB")
        browser.close()
    print(f"\n{len(docs)} document(s) written to output/resources/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
