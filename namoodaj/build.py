# -*- coding: utf-8 -*-
"""يجمّع أجزاء الوثيقة، ويحقن الخطوط والرسوم، ويوحّد الأرقام إلى الصيغة اللاتينية."""
import json, os, re, glob
import os
BASE = os.path.dirname(os.path.abspath(__file__))

SCR = BASE
OUT = os.path.join(os.path.dirname(BASE), "dirasat-jadwa-markaz-tamkeen.html")

charts = json.load(open(SCR + "/parts/charts.json", encoding="utf-8"))
fonts = open(SCR + "/fonts.css", encoding="utf-8").read()

parts = sorted(glob.glob(SCR + "/parts/*.html"))
html = "\n".join(open(p, encoding="utf-8").read() for p in parts)

# حقن الخطوط
assert "/*<!--FONTS-->*/" in html
html = html.replace("/*<!--FONTS-->*/", fonts)

# حقن الرسوم
missing = []
for m in re.findall(r"<!--CHART:([a-z_]+)-->", html):
    if m not in charts:
        missing.append(m)
assert not missing, f"رسوم مفقودة: {missing}"
html = re.sub(r"<!--CHART:([a-z_]+)-->", lambda m: charts[m.group(1)], html)
left = re.findall(r"<!--CHART:[a-z_]+-->", html)
assert not left, left

# تصحيح مرساة النص في الرسوم:
# الوثيقة بأكملها داخل سياق rtl، وخاصية direction تُورَّث إلى نصوص SVG، فتنعكس دلالة
# text-anchor — إذ تصبح "start" هي الحافة اليمنى و"end" هي الحافة اليسرى. وقد كُتبت
# إحداثيات الرسوم والمخططات بالمنطق الهندسي المعتاد (يسار/يمين)، فتُبدَّل القيمتان هنا
# مرة واحدة في مرحلة البناء بدلًا من عكسها يدويًا في عشرين رسمًا.
html = re.sub(r'text-anchor="(start|end)"',
              lambda m: 'text-anchor="%s"' % ("end" if m.group(1) == "start" else "start"),
              html)

# توحيد الأرقام: عربية-هندية ← لاتينية، وفواصل الآلاف والعشرية
trans = {ord(c): str(i) for i, c in enumerate("٠١٢٣٤٥٦٧٨٩")}
trans[ord("٬")] = ","
trans[ord("٫")] = "."
html = html.translate(trans)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)

size = os.path.getsize(OUT)
print(f"البناء: {len(parts)} أجزاء · {len(charts)} رسمًا · {size/1024/1024:.2f} ميغابايت → {OUT}")
for p in parts:
    print("  ", os.path.basename(p), f"{os.path.getsize(p)/1024:.0f} KB")

# فحوص سلامة سريعة
checks = {
    "أقسام": len(re.findall(r'<section id="s\d+"', html)),
    "جداول مرقّمة": len(set(re.findall(r"جدول (\d+)", html))),
    "أشكال مرقّمة": len(set(re.findall(r"شكل (\d+)", html))),
    "عناصر svg": html.count("<svg"),
    "أرقام عربية-هندية متبقية": sum(html.count(c) for c in "٠١٢٣٤٥٦٧٨٩"),
}
print(checks)
