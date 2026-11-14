# -*- coding: utf-8 -*-
import sys, json, re, subprocess, os
import core
from core import *
import part_a as A, part_b as B

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]


def assemble(pages):
    core._fig[0] = 0; core._tab[0] = 0; core.TOC.clear()
    body = [A.s_exec(), A.s_method(), A.s_macro(), A.s_market(), A.s_geo(), A.s_comp(), A.s_price(), B.s_strategy(),
            B.s_marketing(), B.s_org(), B.s_ops(), B.s_tech(), B.s_fin(), B.s_risk(), B.s_decision(), B.s_sources()]
    return render([A.cover(), A.front(), A.toc_page(pages)] + body)



def pdf(html):
    open(f"{HERE}/report.html", "w", encoding="utf-8").write(html)
    subprocess.run(["node", f"{HERE}/pdf.js", f"{HERE}/report.html", OUT], check=True)


pdf(assemble({}))
n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", OUT], capture_output=True, text=True).stdout).group(1))
pages = {}
d = subprocess.run(["pdfinfo", "-dests", OUT], capture_output=True, text=True).stdout
for m in re.finditer(r"^\s*(\d+)\s.*?\"(S\d\d)\"", d, re.M): pages[m.group(2)] = int(m.group(1))
print("pages", n, pages)
html = assemble(pages).replace('<span class="mark">QQ', '<span class="mark" style="display:none">QQ')
pdf(html)
