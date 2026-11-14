# -*- coding: utf-8 -*-
import sys, json, re, subprocess, os
import core
from core import *
import part_a as A, part_b as B

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]


import part_c as P
core.DIV[0] = P.divider


def inj(html, extra, before=None):
    if before and before in html:
        i = html.index(before); return html[:i] + extra + html[i:]
    i = html.rindex("</section>"); return html[:i] + extra + html[i:]


def assemble(pages):
    core._fig[0] = 0; core._tab[0] = 0; core._sec[0] = 0; core.TOC.clear()
    body = [A.s_exec(), P.s_project(), A.s_method(), A.s_macro(),
            inj(A.s_market(), P.market_extra(), "<h2>الشرائح المستهدفة</h2>"), A.s_geo(),
            inj(A.s_comp(), P.comp_extra(), "<h2>الميزة التفاضلية المقترحة</h2>"), A.s_price(), B.s_strategy(),
            inj(B.s_marketing(), P.marketing_extra(), "<h2>رحلة العميل</h2>"), B.s_org(),
            inj(B.s_ops(), P.ops_extra(), "<h2>الجدول الزمني للتأسيس والافتتاح</h2>"),
            inj(B.s_tech(), P.tech_extra(), "<h2>الأجهزة والتجهيزات</h2>"),
            inj(B.s_fin(), P.fin_extra(), "<h2>مؤشرات الجدوى</h2>"), B.s_risk(), P.s_impact(),
            inj(B.s_decision(), P.roadmap(), "<h2>الخطوات التالية</h2>"), B.s_sources()]
    return render([A.cover(), P.letter(), A.front(), A.toc_page(pages)] + body)


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
