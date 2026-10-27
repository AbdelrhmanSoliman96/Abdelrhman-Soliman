# -*- coding: utf-8 -*-
"""
Check that every property container in a .docx keeps its children in schema
order.

WordprocessingML property elements are xsd:sequence. Word reorders silently on
open, which hides the problem; other readers are stricter. This walks the parts
and reports any container whose children run out of order, so a hand-built
element appended in the wrong place is caught here rather than by a user whose
download will not open.

    python3 scripts/check_docx_order.py output/templates/en/01_lean-canvas_en.docx
    python3 scripts/check_docx_order.py output            # whole tree

Exit code is non-zero if anything is out of order, so it can gate a build.
"""
import os
import sys
import zipfile

from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts._ooxml import PPR, RPR, SECTPR, TBLPR, TCPR, TRPR  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CONTAINERS = {
    W + "pPr": PPR, W + "rPr": RPR, W + "tcPr": TCPR,
    W + "tblPr": TBLPR, W + "trPr": TRPR, W + "sectPr": SECTPR,
}


def short(tag):
    return "w:" + tag.rsplit("}", 1)[-1]


def check_part(xml, part, problems):
    root = etree.fromstring(xml)
    for container in root.iter():
        seq = CONTAINERS.get(container.tag)
        if seq is None:
            continue
        seen = [short(c.tag) for c in container if short(c.tag) in seq]
        idx = [seq.index(n) for n in seen]
        if idx != sorted(idx):
            out_of_place = [n for n, a, b in zip(seen, idx, sorted(idx)) if a != b]
            problems.append("%s · %s · order %s (misplaced: %s)"
                            % (part, short(container.tag), " ".join(seen),
                               ", ".join(out_of_place)))


def check(path):
    problems = []
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.startswith("word/") and name.endswith(".xml"):
                check_part(z.read(name), name, problems)
    return problems


def main(target):
    files = []
    if os.path.isdir(target):
        for root, _, names in os.walk(target):
            files += [os.path.join(root, n) for n in sorted(names)
                      if n.endswith(".docx")]
    else:
        files = [target]
    bad = 0
    for f in files:
        problems = check(f)
        rel = os.path.relpath(f)
        if problems:
            bad += 1
            print("FAIL %s" % rel)
            for p in problems[:6]:
                print("      " + p)
            if len(problems) > 6:
                print("      ... and %d more" % (len(problems) - 6))
        else:
            print("ok   %s" % rel)
    print("\n%d file(s) checked, %d with out-of-order properties" %
          (len(files), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "output"))
