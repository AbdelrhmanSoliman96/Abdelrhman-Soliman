"""
Render a document to page images so the layout can be inspected.

A PDF checker can prove the text is present and the pages are the right count. It
cannot see a label colliding with a bar or a figure running off the column. This
renders the same HTML at A4 and slices it into pages for eyeballing.

    python3 scripts/preview_whitepapers.py wp01 [first_page last_page]
"""

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image                                  # noqa: E402
from playwright.sync_api import sync_playwright        # noqa: E402

from whitepapers import common as C                    # noqa: E402
from whitepapers.library import LIBRARY                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = os.path.join(ROOT, "output", "resources", "_preview")
A4_W, A4_H = 794, 1123      # A4 at 96dpi


def main(argv):
    slug = argv[1] if len(argv) > 1 else LIBRARY[0]["slug"]
    doc = next(d for d in LIBRARY if d["slug"].startswith(slug))
    os.makedirs(PREVIEW, exist_ok=True)

    html_path = os.path.join(PREVIEW, f"{doc['slug']}.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(C.document_html(doc))

    binary = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))[-1]
    shot = os.path.join(PREVIEW, f"{doc['slug']}_full.png")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=binary,
                                     args=["--font-render-hinting=none"])
        page = browser.new_page(viewport={"width": A4_W, "height": A4_H},
                                device_scale_factor=2)
        page.goto("file://" + html_path, wait_until="networkidle")
        page.emulate_media(media="print")
        page.screenshot(path=shot, full_page=True)
        browser.close()

    img = Image.open(shot)
    scale = img.width / A4_W
    ph = int(A4_H * scale)
    pages = []
    for i in range(0, img.height, ph):
        crop = img.crop((0, i, img.width, min(i + ph, img.height)))
        out = os.path.join(PREVIEW, f"{doc['slug']}_p{len(pages) + 1:02d}.png")
        crop.resize((A4_W, int(crop.height / scale))).save(out)
        pages.append(out)
    print(f"{doc['slug']}: {len(pages)} preview page(s) in output/resources/_preview/")
    for p in pages:
        print("  " + os.path.relpath(p, ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
