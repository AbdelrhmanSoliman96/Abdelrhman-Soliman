# -*- coding: utf-8 -*-
"""يولّد رسوم SVG من مخرجات النموذج المالي — كل إحداثي مشتق من البيانات."""
import json, os
import os
BASE = os.path.dirname(os.path.abspath(__file__))

SCR = BASE
M = json.load(open(SCR + "/model.json", encoding="utf-8"))
rows = M["rows"]

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]      # light
SERIES_D = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]    # dark
OUT = {}


def sv(name, w, h, body, label, cls="chart"):
    OUT[name] = (f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
                 f'preserveAspectRatio="xMidYMid meet">\n{body}\n</svg>')


def nfmt(v, d=0):
    return f"{v:,.{d}f}"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def grid(x0, x1, y0, y1, ticks, fmt, w=None):
    """شبكة أفقية + محور قيَم على اليمين (RTL)."""
    out = []
    for t in ticks:
        y = t["y"]
        out.append(f'<line class="grid" x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}"/>')
        out.append(f'<text class="ax" x="{x1 + 8}" y="{y + 4:.1f}" text-anchor="start">{fmt(t["v"])}</text>')
    return "\n".join(out)


# ═══════════════ 1) الإيرادات حسب خط الإنتاج — أعمدة مكدّسة ═══════════════
def chart_revenue_stack():
    W, H = 760, 400
    L, R, T, B = 62, 76, 30, 62          # L = هامش أيسر، R = هامش أيمن (محور القيم)
    x0, x1 = L, W - R
    y0, y1 = T, H - B
    keys = [l["key"] for l in M["lines"]]
    names = [l["short"] for l in M["lines"]]
    ymax = 15_000_000
    sy = lambda v: y1 - (v / ymax) * (y1 - y0)
    n = 5
    band = (x1 - x0) / n
    bw = band * 0.52
    s = []
    # شبكة
    for v in range(0, 16_000_000, 3_000_000):
        y = sy(v)
        s.append(f'<line class="grid" x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}"/>')
        s.append(f'<text class="ax" x="{x1 + 10}" y="{y + 4:.1f}" text-anchor="start">{v//1_000_000}م</text>')
    for i in range(n):
        r = rows[i]
        cx = x1 - band * (i + 0.5)       # الزمن من اليمين إلى اليسار
        acc = 0.0
        for j, k in enumerate(keys):
            v = r["line_rev"][k]
            yt, yb = sy(acc + v), sy(acc)
            hgt = max(0.0, yb - yt - 2)  # فجوة 2px بين الشرائح
            if hgt > 0.5:
                s.append(f'<rect class="mark" x="{cx - bw/2:.1f}" y="{yt:.1f}" width="{bw:.1f}" '
                         f'height="{hgt:.1f}" rx="2" fill="var(--s{j+1})" tabindex="0" '
                         f'data-tip="{esc(names[j])} — السنة {i+1}: {nfmt(v)} ر.س"/>')
            acc += v
        s.append(f'<text class="val" x="{cx:.1f}" y="{sy(acc) - 10:.1f}" text-anchor="middle">'
                 f'{acc/1_000_000:.1f}م</text>')
        s.append(f'<text class="ax" x="{cx:.1f}" y="{y1 + 24:.1f}" text-anchor="middle">السنة {i+1}</text>')
    s.append(f'<line class="axis" x1="{x0}" x2="{x1}" y1="{y1}" y2="{y1}"/>')
    s.append(f'<text class="unit" x="{x1 + 10}" y="{y0 - 12}" text-anchor="start">مليون ر.س</text>')
    sv("rev_stack", W, H, "\n".join(s),
       "أعمدة مكدّسة تُظهر نمو الإيرادات السنوية موزّعة على ستة خطوط إيراد خلال السنوات الخمس الأولى")


# ═══════════════ 2) التدفق النقدي التراكمي ═══════════════
def chart_cash():
    W, H = 760, 380
    L, R, T, B = 62, 84, 34, 58
    x0, x1, y0, y1 = L, W - R, T, H - B
    cum = [-M["funding_total"]] + M["cumcash"]
    lo, hi = min(cum), max(cum)
    lo, hi = -8_500_000, 3_500_000
    sy = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)
    sx = lambda i: x1 - (i / (len(cum) - 1)) * (x1 - x0)
    s = []
    for v in range(-8_000_000, 4_000_000, 2_000_000):
        y = sy(v)
        s.append(f'<line class="grid" x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}"/>')
        s.append(f'<text class="ax" x="{x1 + 10}" y="{y + 4:.1f}" text-anchor="start">{v/1_000_000:.0f}م</text>')
    yz = sy(0)
    s.append(f'<line class="zero" x1="{x0}" x2="{x1}" y1="{yz:.1f}" y2="{yz:.1f}"/>')
    pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(cum))
    area = f"{sx(0):.1f},{yz:.1f} " + pts + f" {sx(len(cum)-1):.1f},{yz:.1f}"
    s.append(f'<polygon class="area" points="{area}"/>')
    s.append(f'<polyline class="line s1" points="{pts}"/>')
    for i, v in enumerate(cum):
        s.append(f'<circle class="dot s1" cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="4" tabindex="0" '
                 f'data-tip="{"التأسيس (سنة 0)" if i==0 else f"نهاية السنة {i}"}: {nfmt(v)} ر.س"/>')
    # نقطة تعادل التدفق التراكمي
    pb = M["payback"]
    xpb = sx(pb)
    s.append(f'<line class="mark-v" x1="{xpb:.1f}" x2="{xpb:.1f}" y1="{y0}" y2="{y1}"/>')
    s.append(f'<text class="note" x="{xpb - 8:.1f}" y="{y0 + 14}" text-anchor="end">'
             f'استرداد رأس المال — السنة {pb:.1f}</text>')
    for i in (0, 5, 10):
        lbl = "التأسيس" if i == 0 else f"س{i}"
        s.append(f'<text class="ax" x="{sx(i):.1f}" y="{y1 + 26:.1f}" text-anchor="middle">{lbl}</text>')
    s.append(f'<text class="ax" x="{sx(len(cum)-1):.1f}" y="{y1 + 26:.1f}" text-anchor="middle"></text>')
    s.append(f'<text class="unit" x="{x1 + 10}" y="{y0 - 14}" text-anchor="start">مليون ر.س</text>')
    sv("cash", W, H, "\n".join(s),
       "خط يوضح رصيد التدفق النقدي التراكمي من سنة التأسيس حتى السنة العاشرة وتقاطعه مع الصفر عند السنة 8.5")


# ═══════════════ 3) الطلب مقابل العرض والفجوة ═══════════════
def chart_gap():
    W, H = 760, 380
    L, R, T, B = 62, 80, 34, 66
    x0, x1, y0, y1 = L, W - R, T, H - B
    g = M["gap"]
    ymax = 72
    sy = lambda v: y1 - v / ymax * (y1 - y0)
    band = (x1 - x0) / len(g)
    bw = band * 0.24
    s = []
    for v in range(0, 73, 12):
        y = sy(v)
        s.append(f'<line class="grid" x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}"/>')
        s.append(f'<text class="ax" x="{x1 + 10}" y="{y + 4:.1f}" text-anchor="start">{v}</text>')
    for i, d in enumerate(g):
        cx = x1 - band * (i + 0.5)
        xd = cx + bw / 2 + 1
        xs = cx - bw * 1.5 - 1
        s.append(f'<rect class="mark" x="{xd:.1f}" y="{sy(d["demand"]):.1f}" width="{bw:.1f}" '
                 f'height="{y1 - sy(d["demand"]):.1f}" rx="2" fill="var(--s1)" tabindex="0" '
                 f'data-tip="الطلب — {d["y"]}: {d["demand"]} ألف ساعة"/>')
        s.append(f'<rect class="mark" x="{xs:.1f}" y="{sy(d["supply"]):.1f}" width="{bw:.1f}" '
                 f'height="{y1 - sy(d["supply"]):.1f}" rx="2" fill="var(--s2)" tabindex="0" '
                 f'data-tip="العرض المتاح — {d["y"]}: {d["supply"]} ألف ساعة"/>')
        # وسم الفجوة
        ym = (sy(d["demand"]) + sy(d["supply"])) / 2
        s.append(f'<line class="gapline" x1="{xs + bw/2:.1f}" x2="{xd + bw/2:.1f}" '
                 f'y1="{sy(d["demand"]):.1f}" y2="{sy(d["demand"]):.1f}"/>')
        s.append(f'<text class="gapval" x="{cx:.1f}" y="{ym + 4:.1f}" text-anchor="middle">{d["gap"]}</text>')
        s.append(f'<text class="ax" x="{cx:.1f}" y="{y1 + 24:.1f}" text-anchor="middle">{d["y"]}</text>')
    s.append(f'<line class="axis" x1="{x0}" x2="{x1}" y1="{y1}" y2="{y1}"/>')
    s.append(f'<text class="unit" x="{x1 + 10}" y="{y0 - 14}" text-anchor="start">ألف ساعة/سنة</text>')
    s.append(f'<text class="note" x="{x1}" y="{y1 + 50}" text-anchor="end">'
             f'الرقم داخل المسافة = حجم الفجوة غير الملبّاة</text>')
    sv("gap", W, H, "\n".join(s),
       "أعمدة متجاورة تقارن الطلب على خدمات التصنيع بالتعاقد بالعرض المتاح، مع تحديد الفجوة غير الملبّاة لكل سنة")


# ═══════════════ 4) تحليل الحساسية — Tornado ═══════════════
def chart_tornado():
    W, H = 760, 330
    L, R, T, B = 40, 200, 26, 44
    x0, x1, y0, y1 = L, W - R, T, H - B
    sens = M["sens"]
    mx = max(max(abs(s["up"]), abs(s["dn"])) for s in sens) * 1.08
    cx = (x0 + x1) / 2
    sx = lambda v: cx + (v / mx) * (x1 - x0) / 2
    rowh = (y1 - y0) / len(sens)
    bh = rowh * 0.46
    s = []
    for v in (-6_000_000, -3_000_000, 0, 3_000_000, 6_000_000):
        if abs(v) > mx:
            continue
        x = sx(v)
        s.append(f'<line class="grid" x1="{x:.1f}" x2="{x:.1f}" y1="{y0}" y2="{y1}"/>')
        s.append(f'<text class="ax" x="{x:.1f}" y="{y1 + 20}" text-anchor="middle">'
                 f'{"" if v==0 else f"{v/1_000_000:+.0f}م"}</text>')
    for i, sn in enumerate(sens):
        yc = y0 + rowh * (i + 0.5)
        for val, col in ((sn["dn"], "var(--s2)"), (sn["up"], "var(--s1)")):
            a, b = sorted((cx, sx(val)))
            s.append(f'<rect class="mark" x="{a:.1f}" y="{yc - bh/2:.1f}" width="{max(1.0, b - a - 1):.1f}" '
                     f'height="{bh:.1f}" rx="2" fill="{col}" tabindex="0" '
                     f'data-tip="{esc(sn["label"])} — تغيّر {"−" if val is sn["dn"] else "+"}15%: '
                     f'{nfmt(val)} ر.س على صافي القيمة الحالية"/>')
        s.append(f'<text class="cat" x="{x1 + 14}" y="{yc + 4:.1f}" text-anchor="start">{esc(sn["label"])}</text>')
    s.append(f'<line class="zero" x1="{cx:.1f}" x2="{cx:.1f}" y1="{y0}" y2="{y1}"/>')
    s.append(f'<text class="unit" x="{cx:.1f}" y="{y1 + 38}" text-anchor="middle">'
             f'الأثر على صافي القيمة الحالية (مليون ر.س)</text>')
    sv("tornado", W, H, "\n".join(s),
       "مخطط إعصاري يرتّب متغيرات المشروع حسب أثر تغيّرها بنسبة 15% صعودًا وهبوطًا على صافي القيمة الحالية")


# ═══════════════ 5) نقطة التعادل ═══════════════
def chart_breakeven():
    W, H = 760, 380
    L, R, T, B = 62, 84, 30, 60
    x0, x1, y0, y1 = L, W - R, T, H - B
    fixed, cm = M["fixed3"], M["cm_ratio"]
    rmax = 14_000_000
    sy = lambda v: y1 - v / rmax * (y1 - y0)
    sx = lambda v: x1 - v / rmax * (x1 - x0)          # الإيراد يتزايد نحو اليسار
    s = []
    for v in range(0, 15_000_000, 4_000_000):
        y, x = sy(v), sx(v)
        s.append(f'<line class="grid" x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}"/>')
        s.append(f'<text class="ax" x="{x1 + 10}" y="{y + 4:.1f}" text-anchor="start">{v/1_000_000:.0f}م</text>')
        s.append(f'<text class="ax" x="{x:.1f}" y="{y1 + 22:.1f}" text-anchor="middle">{v/1_000_000:.0f}م</text>')
    # التكلفة الكلية = ثابتة + متغيرة
    tc0, tc1 = fixed, fixed + rmax * (1 - cm)
    s.append(f'<line class="line s2" x1="{sx(0):.1f}" y1="{sy(tc0):.1f}" x2="{sx(rmax):.1f}" y2="{sy(tc1):.1f}"/>')
    s.append(f'<line class="line dash" x1="{sx(0):.1f}" y1="{sy(fixed):.1f}" x2="{sx(rmax):.1f}" y2="{sy(fixed):.1f}"/>')
    s.append(f'<line class="line s1" x1="{sx(0):.1f}" y1="{sy(0):.1f}" x2="{sx(rmax):.1f}" y2="{sy(rmax):.1f}"/>')
    be = M["be_rev"]
    bx, by = sx(be), sy(be)
    s.append(f'<line class="mark-v" x1="{bx:.1f}" x2="{bx:.1f}" y1="{by:.1f}" y2="{y1}"/>')
    s.append(f'<circle class="dot be" cx="{bx:.1f}" cy="{by:.1f}" r="6"/>')
    s.append(f'<text class="note" x="{bx + 14:.1f}" y="{by - 30:.1f}" text-anchor="start">'
             f'نقطة التعادل {be/1_000_000:.2f}م ر.س</text>')
    s.append(f'<text class="note sm" x="{bx + 14:.1f}" y="{by - 14:.1f}" text-anchor="start">'
             f'عند {M["be_util"]*100:.0f}% من الطاقة الإنتاجية</text>')
    # موقع السنوات
    for i in (2, 3, 4):
        r = rows[i]
        s.append(f'<circle class="dot yr" cx="{sx(r["rev"]):.1f}" cy="{sy(r["rev"]):.1f}" r="4" tabindex="0" '
                 f'data-tip="السنة {r["y"]}: إيراد {nfmt(r["rev"])} ر.س"/>')
        s.append(f'<text class="ax" x="{sx(r["rev"]) - 4:.1f}" y="{sy(r["rev"]) + 20:.1f}" '
                 f'text-anchor="middle">س{r["y"]}</text>')
    s.append(f'<line class="axis" x1="{x0}" x2="{x1}" y1="{y1}" y2="{y1}"/>')
    s.append(f'<text class="unit" x="{x1 + 10}" y="{y0 - 12}" text-anchor="start">التكلفة (م ر.س)</text>')
    s.append(f'<text class="unit" x="{x0}" y="{y1 + 46}" text-anchor="start">الإيرادات (م ر.س)</text>')
    sv("breakeven", W, H, "\n".join(s),
       "مخطط نقطة التعادل يقارن خط الإيرادات بخط التكلفة الكلية والتكاليف الثابتة، ويحدد التعادل عند 10.64 مليون ريال")


# ═══════════════ 6) هيكل التكاليف — السنة الثالثة ═══════════════
def chart_costs():
    r = rows[2]
    items = [("تكلفة المواد الخام وأجور تصنيع الأسر", r["cogs"])]
    od = r["opex_detail"]
    order = ["الرواتب والأجور ومزايا العاملين", "الكهرباء والمياه والغاز",
             "النقل والتوزيع وسلسلة التبريد", "التسويق والترويج والمعارض",
             "برامج تمكين الأسر (تدريب، حقائب، حوافز إنتاج)", "الصيانة وقطع الغيار"]
    for k in order:
        items.append((k, od[k]))
    rest = sum(v for k, v in od.items() if k not in order)
    items.append(("مصروفات إدارية وحوكمة ورسوم وتأمين وأخرى", rest))
    items.append(("الإهلاك والإطفاء", r["dep"]))
    total = sum(v for _, v in items)
    W = 760
    rowh, T, B = 34, 26, 40
    H = T + B + rowh * len(items)
    L, R = 40, 330
    x0, x1 = L, W - R
    mx = max(v for _, v in items) * 1.34   # مساحة لوسم القيمة خارج العمود
    s = []
    for i, (k, v) in enumerate(items):
        yc = T + rowh * i + rowh / 2
        w = (v / mx) * (x1 - x0)
        s.append(f'<rect class="mark" x="{x1 - w:.1f}" y="{yc - 9:.1f}" width="{w:.1f}" height="18" rx="2" '
                 f'fill="var(--s{1 if i==0 else (3 if i==len(items)-1 else 1)})" '
                 f'opacity="{1 if i in (0,) else (0.55 if i==len(items)-1 else 0.82)}" tabindex="0" '
                 f'data-tip="{esc(k)}: {nfmt(v)} ر.س — {v/total*100:.1f}% من إجمالي التكاليف"/>')
        s.append(f'<text class="cat" x="{x1 + 14}" y="{yc + 4:.1f}" text-anchor="start">{esc(k)}</text>')
        s.append(f'<text class="val" x="{x1 - w - 10:.1f}" y="{yc + 4:.1f}" text-anchor="end">'
                 f'{v/1_000_000:.2f}م · {v/total*100:.0f}%</text>')
    s.append(f'<text class="unit" x="{x1}" y="{H - 14}" text-anchor="end">'
             f'إجمالي التكاليف في السنة الثالثة: {nfmt(total)} ر.س</text>')
    sv("costs", W, H, "\n".join(s),
       "أعمدة أفقية تفصّل هيكل تكاليف السنة الثالثة مرتبة تنازليًا، وأكبر بنودها تكلفة المواد الخام ثم الرواتب")


# ═══════════════ 7) الاكتفاء التشغيلي الذاتي ═══════════════
def chart_oss():
    W, H = 760, 300
    L, R, T, B = 56, 76, 30, 54
    x0, x1, y0, y1 = L, W - R, T, H - B
    vals = [r["oss"] for r in rows[:5]]
    lo, hi = 0.75, 1.20
    sy = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)
    band = (x1 - x0) / 5
    s = []
    for v in (0.8, 0.9, 1.0, 1.1, 1.2):
        y = sy(v)
        cls = "zero" if v == 1.0 else "grid"
        s.append(f'<line class="{cls}" x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}"/>')
        s.append(f'<text class="ax" x="{x1 + 10}" y="{y + 4:.1f}" text-anchor="start">{v*100:.0f}%</text>')
    pts = " ".join(f"{x1 - band*(i+0.5):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
    s.append(f'<polyline class="line s1" points="{pts}"/>')
    for i, v in enumerate(vals):
        cx = x1 - band * (i + 0.5)
        s.append(f'<circle class="dot {"s3" if v>=1 else "s2"}" cx="{cx:.1f}" cy="{sy(v):.1f}" r="5" '
                 f'tabindex="0" data-tip="السنة {i+1}: نسبة الاكتفاء التشغيلي {v*100:.0f}%"/>')
        s.append(f'<text class="val" x="{cx:.1f}" y="{sy(v) - 14:.1f}" text-anchor="middle">{v*100:.0f}%</text>')
        s.append(f'<text class="ax" x="{cx:.1f}" y="{y1 + 24:.1f}" text-anchor="middle">السنة {i+1}</text>')
    s.append(f'<text class="note" x="{x0}" y="{sy(1.0) - 10:.1f}" text-anchor="start">'
             f'خط الاكتفاء الكامل — 100%</text>')
    sv("oss", W, H, "\n".join(s),
       "خط يوضح ارتفاع نسبة الاكتفاء التشغيلي الذاتي من 87% في السنة الأولى إلى 111% في السنة الخامسة، متجاوزًا خط المئة بالمئة من السنة الثانية")


# ═══════════════ 8) خريطة المخاطر ═══════════════
RISKS = [
    ("م1", "تأخّر إصدار التراخيص والتصاريح البلدية والصحية", 3, 4),
    ("م2", "تجاوز التكلفة الرأسمالية المقدّرة", 3, 3),
    ("م3", "بطء اكتساب العقود المؤسسية للتموين", 4, 5),
    ("م4", "ارتفاع أسعار المواد الخام", 4, 3),
    ("م5", "تسرّب المستفيدات وضعف الالتزام بالإنتاج", 3, 4),
    ("م6", "حادثة سلامة غذائية أو استدعاء منتج", 2, 5),
    ("م7", "عجز في تدفق التمويل من الجهة المانحة", 2, 5),
    ("م8", "صعوبة استقطاب كفاءات فنية متخصصة", 3, 3),
    ("م9", "أعطال المعدات وانقطاع سلسلة التبريد", 3, 4),
    ("م10", "دخول منافس مؤسسي بأسعار أقل", 3, 3),
    ("م11", "تغيّر الاشتراطات التنظيمية للأغذية", 2, 3),
    ("م12", "ضعف قدرات الفريق على إدارة مشروع إنتاجي", 3, 4),
    ("م13", "الاعتماد المفرط على عميل مؤسسي واحد", 3, 4),
    ("م14", "مخاطر سمعة عبر وسائل التواصل", 2, 3),
]


def chart_risk():
    W, H = 700, 470
    L, R, T, B = 118, 40, 30, 62
    x0, x1, y0, y1 = L, W - R, T, H - B
    cw, ch = (x1 - x0) / 5, (y1 - y0) / 5
    s = []
    lvl = lambda p, i: p * i
    for r_ in range(5):        # الأثر 1..5 من الأسفل للأعلى
        for c in range(5):     # الاحتمال 1..5 من اليمين لليسار
            imp, prob = 5 - r_, c + 1
            sc = imp * prob
            tone = "lo" if sc <= 5 else ("md" if sc <= 10 else ("hi" if sc <= 15 else "xh"))
            x = x1 - cw * (prob)
            y = y0 + ch * r_
            s.append(f'<rect class="cell {tone}" x="{x:.1f}" y="{y:.1f}" width="{cw-2:.1f}" height="{ch-2:.1f}" rx="3"/>')
    # تجميع المخاطر المتطابقة في الخلية ثم توزيعها شبكيًا داخلها
    cells = {}
    for r_ in RISKS:
        cells.setdefault((r_[2], r_[3]), []).append(r_)
    for (p, imp), group in cells.items():
        n = len(group)
        cols = 1 if n == 1 else (2 if n <= 4 else 3)
        rowsn = -(-n // cols)
        cxc = x1 - cw * (p - 0.5)
        cyc = y0 + ch * (5 - imp + 0.5)
        for k, (cid, name, _, _) in enumerate(group):
            r_i, c_i = divmod(k, cols)
            x = cxc + (c_i - (cols - 1) / 2) * 31
            y = cyc + (r_i - (rowsn - 1) / 2) * 30
            s.append(f'<circle class="rdot" cx="{x:.1f}" cy="{y:.1f}" r="13" tabindex="0" '
                     f'data-tip="{cid} — {esc(name)} · الاحتمال {p}/5 · الأثر {imp}/5 · الدرجة {p*imp}"/>')
            s.append(f'<text class="rlab" x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle">{cid}</text>')
    for c in range(5):
        s.append(f'<text class="ax" x="{x1 - cw*(c+0.5):.1f}" y="{y1 + 22:.1f}" text-anchor="middle">{c+1}</text>')
    for r_ in range(5):
        s.append(f'<text class="ax" x="{x1 + 14:.1f}" y="{y0 + ch*(r_+0.5) + 4:.1f}" text-anchor="start">{5-r_}</text>')
    s.append(f'<text class="unit" x="{(x0+x1)/2:.1f}" y="{y1 + 48:.1f}" text-anchor="middle">الاحتمالية ←</text>')
    s.append(f'<text class="unit" x="{x0 - 78:.1f}" y="{(y0+y1)/2:.1f}" text-anchor="middle" '
             f'transform="rotate(-90 {x0-78:.1f} {(y0+y1)/2:.1f})">شدّة الأثر ←</text>')
    sv("risk", W, H, "\n".join(s),
       "مصفوفة خمسة في خمسة توزّع أربعة عشر خطرًا حسب احتمالية الوقوع وشدة الأثر، وأشدها خطر بطء اكتساب العقود المؤسسية")


# ═══════════════ 9) الجدول الزمني — Gantt ═══════════════
TASKS = [
    ("التأسيس والحوكمة", [
        ("اعتماد الدراسة وتشكيل لجنة الإشراف", 1, 1),
        ("توقيع اتفاقية المنحة وفتح الحساب المخصص", 1, 2),
        ("استقطاب مدير المركز والفريق التأسيسي", 2, 4),
    ]),
    ("التراخيص والمقر", [
        ("تعاقد المقر واستكمال الرخصة البلدية والصحية", 2, 5),
        ("التصاميم الهندسية والمخططات التنفيذية", 2, 4),
        ("أعمال التشطيب والتحسينات الإنشائية", 4, 8),
    ]),
    ("التجهيز الفني", [
        ("طرح المناقصات وترسية توريد المعدات", 4, 6),
        ("توريد وتركيب المعدات وغرف التبريد", 7, 10),
        ("اختبارات التشغيل والمعايرة والتصاريح النهائية", 10, 11),
        ("تأسيس نظام HACCP ونظام التتبّع وERP", 8, 12),
    ]),
    ("التمكين والتشغيل", [
        ("حصر المستفيدات والفرز والاختيار (الدفعة الأولى)", 5, 8),
        ("تنفيذ البرنامج التدريبي التأسيسي", 8, 12),
        ("التشغيل التجريبي وضبط الجودة", 11, 13),
        ("الإطلاق الرسمي والتشغيل الكامل", 13, 14),
    ]),
    ("التسويق والسوق", [
        ("بناء العلامة التجارية والهوية والتغليف", 5, 9),
        ("التعاقدات المؤسسية المبكّرة (خطابات نوايا)", 7, 12),
        ("إطلاق قنوات البيع والمتجر الإلكتروني", 12, 15),
    ]),
    ("الرصد والتقييم", [
        ("بناء خط الأساس ومنظومة المؤشرات", 3, 6),
        ("التقييم التكويني الأول وتقرير الأثر", 15, 18),
    ]),
]


def chart_gantt():
    W = 900
    L, R, T = 40, 300, 56
    rowh, grph = 26, 16
    nrows = sum(len(v) for _, v in TASKS)
    H = T + rowh * nrows + grph * len(TASKS) + 56
    x0, x1 = L, W - R
    months = 18
    cw = (x1 - x0) / months
    sx = lambda m: x1 - cw * m          # الشهر 0 عند اليمين
    s = []
    for m in range(months + 1):
        s.append(f'<line class="grid{" q" if m % 3 == 0 else ""}" x1="{sx(m):.1f}" x2="{sx(m):.1f}" '
                 f'y1="{T - 18}" y2="{H - 34}"/>')
    for m in range(0, months, 3):
        s.append(f'<text class="ax" x="{sx(m + 1.5):.1f}" y="{T - 26}" text-anchor="middle">'
                 f'الربع {m//3 + 1}</text>')
    y = T
    for gi, (grp, tasks) in enumerate(TASKS):
        s.append(f'<text class="grp" x="{x1 + 16}" y="{y + 4:.1f}" text-anchor="start">{esc(grp)}</text>')
        s.append(f'<line class="grpline" x1="{x0}" x2="{x1}" y1="{y - 10:.1f}" y2="{y - 10:.1f}"/>')
        y += grph
        for (name, a, b) in tasks:
            xa, xb = sx(b), sx(a - 1)
            s.append(f'<rect class="bar g{gi%3}" x="{xa:.1f}" y="{y - 7:.1f}" width="{xb - xa:.1f}" '
                     f'height="14" rx="3" tabindex="0" '
                     f'data-tip="{esc(name)} — من الشهر {a} إلى الشهر {b} ({b-a+1} شهرًا)"/>')
            s.append(f'<text class="task" x="{x1 + 16}" y="{y + 4:.1f}" text-anchor="start">{esc(name)}</text>')
            y += rowh
    # معالم رئيسية
    for j, (m, lab) in enumerate(((5, "اكتمال التراخيص"), (11, "جاهزية الخط الإنتاجي"), (14, "الإطلاق الرسمي"))):
        x = sx(m)
        dy = 0 if j % 2 == 0 else 14      # تبديل الارتفاع لتفادي تداخل الوسوم المتجاورة
        s.append(f'<polygon class="ms" points="{x:.1f},{H-34} {x-7:.1f},{H-24} {x+7:.1f},{H-24}"/>')
        s.append(f'<line class="grpline" x1="{x:.1f}" x2="{x:.1f}" y1="{H-24}" y2="{H-16+dy}"/>')
        s.append(f'<text class="msl" x="{x:.1f}" y="{H - 6 + dy}" text-anchor="middle">{lab}</text>')
    sv("gantt", W, H, "\n".join(s),
       "مخطط جانت يوزّع عشرين نشاطًا على ستة محاور خلال ثمانية عشر شهرًا، مع ثلاثة معالم رئيسية للتراخيص والجاهزية والإطلاق",
       cls="chart gantt")


# ═══════════════ 10) حجم السوق TAM/SAM/SOM ═══════════════
def chart_market():
    W, H = 760, 300
    mk = M["market"]
    tiers = [("السوق الكلي (TAM)", mk["tam"], "سوق الأغذية المصنّعة والتموين المؤسسي بمنطقة الرياض"),
             ("السوق المتاح المخدوم (SAM)", mk["sam"], "الشرائح المستهدفة: تموين متوسط الحجم، أغذية حرفية، تصنيع بالتعاقد"),
             ("الحصة المستهدفة (SOM) — السنة 5", mk["som5"], f"{mk['share5']*100:.1f}% من السوق المتاح المخدوم")]
    L, R, T = 40, 300, 28
    x0, x1 = L, W - R
    rowh = 78
    s = []
    for i, (lab, v, sub) in enumerate(tiers):
        w = (x1 - x0) * (0.34 + 0.66 * (i == 0)) if False else (x1 - x0) * [1.0, 0.52, 0.20][i]
        y = T + rowh * i
        s.append(f'<rect class="tier t{i}" x="{x1 - w:.1f}" y="{y:.1f}" width="{w:.1f}" height="52" rx="4" '
                 f'tabindex="0" data-tip="{esc(lab)}: {nfmt(v)} ر.س"/>')
        big = f"{v/1_000_000_000:.2f} مليار" if v >= 1e9 else f"{v/1_000_000:.1f} مليون"
        # الشريحة الأصغر أضيق من وسمها، فيوضع الوسم خارجها على يسارها
        inside = w > 150
        vx = (x1 - 16) if inside else (x1 - w - 12)
        cls = "tierv inv" if (inside and i == 2) else "tierv"
        s.append(f'<text class="{cls}" x="{vx:.1f}" y="{y + 33:.1f}" text-anchor="end">{big} ر.س</text>')
        s.append(f'<text class="cat" x="{x1 + 16}" y="{y + 22:.1f}" text-anchor="start">{esc(lab)}</text>')
        s.append(f'<text class="task" x="{x1 + 16}" y="{y + 40:.1f}" text-anchor="start">{esc(sub)}</text>')
    sv("market", W, H, "\n".join(s),
       "ثلاث شرائح متدرجة تُظهر السوق الكلي ثم السوق المتاح المخدوم ثم الحصة المستهدفة للمشروع في السنة الخامسة")


# ═══════════════ 11) الأثر — الأسر ودخلها ═══════════════
def chart_impact():
    W, H = 760, 320
    L, R, T, B = 50, 60, 40, 56
    midgap = 56
    half = (W - L - R - midgap) / 2
    s = []
    # يمين: عدد الأسر المنتجة
    fx1 = W - R
    fx0 = fx1 - half
    y0, y1 = T, H - B
    fam = M["families"]
    fmax = 320
    sy = lambda v: y1 - v / fmax * (y1 - y0)
    band = (fx1 - fx0) / 5
    for v in (0, 80, 160, 240, 320):
        y = sy(v)
        s.append(f'<line class="grid" x1="{fx0}" x2="{fx1}" y1="{y:.1f}" y2="{y:.1f}"/>')
        s.append(f'<text class="ax" x="{fx0 - 8}" y="{y + 4:.1f}" text-anchor="end">{v}</text>')
    for i, v in enumerate(fam):
        cx = fx1 - band * (i + 0.5)
        bw = band * 0.5
        s.append(f'<rect class="mark" x="{cx - bw/2:.1f}" y="{sy(v):.1f}" width="{bw:.1f}" '
                 f'height="{y1 - sy(v):.1f}" rx="2" fill="var(--s1)" tabindex="0" '
                 f'data-tip="السنة {i+1}: {v} أسرة منتجة متعاقدة"/>')
        s.append(f'<text class="val" x="{cx:.1f}" y="{sy(v) - 8:.1f}" text-anchor="middle">{v}</text>')
        s.append(f'<text class="ax" x="{cx:.1f}" y="{y1 + 20:.1f}" text-anchor="middle">س{i+1}</text>')
    s.append(f'<text class="sub" x="{fx1}" y="{T - 16}" text-anchor="end">الأسر المنتجة المتعاقدة (أسرة)</text>')
    s.append(f'<line class="axis" x1="{fx0}" x2="{fx1}" y1="{y1}" y2="{y1}"/>')
    # يسار: متوسط الدخل الشهري
    gx1 = fx0 - midgap
    gx0 = gx1 - half
    inc = M["income_after"]
    imax = 4200
    sy2 = lambda v: y1 - v / imax * (y1 - y0)
    band2 = (gx1 - gx0) / 5
    for v in (0, 1000, 2000, 3000, 4000):
        y = sy2(v)
        s.append(f'<line class="grid" x1="{gx0}" x2="{gx1}" y1="{y:.1f}" y2="{y:.1f}"/>')
        s.append(f'<text class="ax" x="{gx0 - 8}" y="{y + 4:.1f}" text-anchor="end">{v//1000 if v else 0}{"ك" if v else ""}</text>')
    yb = sy2(M["income_before"])
    s.append(f'<line class="zero" x1="{gx0}" x2="{gx1}" y1="{yb:.1f}" y2="{yb:.1f}"/>')
    s.append(f'<text class="note sm" x="{gx0 + 6}" y="{yb - 8:.1f}" text-anchor="start">'
             f'خط الأساس {M["income_before"]:,} ر.س</text>')
    pts = " ".join(f"{gx1 - band2*(i+0.5):.1f},{sy2(v):.1f}" for i, v in enumerate(inc))
    s.append(f'<polyline class="line s3" points="{pts}"/>')
    for i, v in enumerate(inc):
        cx = gx1 - band2 * (i + 0.5)
        s.append(f'<circle class="dot s3" cx="{cx:.1f}" cy="{sy2(v):.1f}" r="4.5" tabindex="0" '
                 f'data-tip="السنة {i+1}: متوسط دخل الأسرة {v:,} ر.س شهريًا"/>')
        s.append(f'<text class="ax" x="{cx:.1f}" y="{y1 + 20:.1f}" text-anchor="middle">س{i+1}</text>')
    s.append(f'<text class="val" x="{gx1 - band2*4.5:.1f}" y="{sy2(inc[4]) - 12:.1f}" text-anchor="middle">'
             f'{inc[4]:,}</text>')
    s.append(f'<text class="sub" x="{gx1}" y="{T - 16}" text-anchor="end">متوسط دخل الأسرة الشهري (ر.س)</text>')
    s.append(f'<line class="axis" x1="{gx0}" x2="{gx1}" y1="{y1}" y2="{y1}"/>')
    sv("impact", W, H, "\n".join(s),
       "رسمان متجاوران: أعمدة لعدد الأسر المنتجة المتعاقدة، وخط لارتفاع متوسط الدخل الشهري للأسرة مقابل خط الأساس")


for f in (chart_revenue_stack, chart_cash, chart_gap, chart_tornado, chart_breakeven,
          chart_costs, chart_oss, chart_risk, chart_gantt, chart_market, chart_impact):
    f()

os.makedirs(SCR + "/parts", exist_ok=True)
with open(SCR + "/parts/charts.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, ensure_ascii=False)
print("generated:", ", ".join(f"{k} ({len(v)//1024}KB)" if len(v) > 1024 else k for k, v in OUT.items()))
