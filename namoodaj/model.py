# -*- coding: utf-8 -*-
"""نموذج الجدوى المالية — مركز التمكين الاقتصادي للأسر المنتجة (الرياض)."""
import json
import os
BASE = os.path.dirname(os.path.abspath(__file__))

SCR = BASE

# ============ 1) التكاليف الرأسمالية ============
capex_items = [
    ("تحسينات وتجهيزات المبنى (أرضيات إيبوكسي، أسقف صحية، صرف، عزل، أقسام)", 1450000, 10),
    ("معدات المطبخ والتصنيع (أفران نفقية، عجّانات، مقالي، خطوط تحضير)", 1850000, 8),
    ("غرف التبريد والتجميد وسلسلة التبريد", 460000, 10),
    ("خط التعبئة والتغليف والتوسيم واللحام الحراري", 390000, 8),
    ("مختبر مراقبة الجودة والأجهزة القياسية", 145000, 8),
    ("تجهيزات قاعتَي التدريب والمكاتب والأثاث", 260000, 6),
    ("أنظمة السلامة والإطفاء والتهوية وشفط الأدخنة", 245000, 10),
    ("مركبات نقل مبرّدة (3)", 390000, 5),
    ("البنية التقنية ونظام ERP ونظام التتبّع", 195000, 4),
]
intangibles = [
    ("الرسوم والتراخيص والتصاميم الهندسية والاستشارات الفنية", 195000, 5),
    ("العلامة التجارية والهوية والإطلاق التسويقي", 135000, 5),
]
tangible_total = sum(v for _, v, _ in capex_items)
intang_total = sum(v for _, v, _ in intangibles)
contingency = round((tangible_total + intang_total) * 0.05)
capex_total = tangible_total + intang_total + contingency

working_capital = 749250
opex_bridge = 750000                      # منحة تشغيلية لتغطية عجز السنة الأولى
funding_total = capex_total + working_capital + opex_bridge   # = 7,500,000

dep_annual = sum(v / n for _, v, n in capex_items)
amort_annual = sum(v / n for _, v, n in intangibles)
da5 = dep_annual + amort_annual            # سنوات 1-5
equip_value = 1850000 + 460000 + 390000 + 145000

funding_mix = [
    ("منحة تأسيسية من الجهة المانحة الرئيسية", 4500000),
    ("مساهمة الجمعية (نقدية + عينية: حق انتفاع بالمقر وإدارة المشروع)", 1125000),
    ("شراكات القطاع الخاص — المسؤولية الاجتماعية (نقدية وعينية)", 1125000),
    ("تمويل ميسّر من صندوق تنموي (قرض حسن يُسدَّد على 3 سنوات من السنة الثالثة)", 750000),
]

# ============ 2) خطوط الإيراد والطاقة الإنتاجية ============
lines = [
    dict(key="L1", name="المخبوزات والمعجنات المجمّدة", short="مخبوزات ومعجنات", unit="كجم",
         cap_day=420, days=300, price=24.0, cogs=0.50,
         ramp=[0.32, 0.47, 0.61, 0.70, 0.78]),
    dict(key="L2", name="التمور والمنتجات المحفوظة (معمول، مربّيات، صلصات، تمور محشوّة)", short="تمور ومحفوظات", unit="كجم",
         cap_day=260, days=300, price=42.0, cogs=0.46,
         ramp=[0.26, 0.42, 0.57, 0.68, 0.76]),
    dict(key="L3", name="الوجبات الجاهزة والتموين المؤسسي", short="وجبات وتموين", unit="وجبة",
         cap_day=1400, days=300, price=16.5, cogs=0.56,
         ramp=[0.31, 0.48, 0.62, 0.71, 0.79]),
    dict(key="L4", name="التصنيع بالتعاقد — محطات مؤجّرة للأسر المنتجة", short="تصنيع بالتعاقد", unit="ساعة تشغيل",
         cap_day=60, days=300, price=48.0, cogs=0.20,
         ramp=[0.38, 0.58, 0.72, 0.82, 0.89]),
    dict(key="L5", name="خدمات التعبئة والتغليف والتوسيم والباركود", short="تعبئة وتغليف", unit="عبوة",
         cap_day=1600, days=300, price=1.75, cogs=0.40,
         ramp=[0.30, 0.50, 0.66, 0.76, 0.84]),
    dict(key="L6", name="التدريب المؤسسي والاستشارات لجهات ثالثة", short="تدريب مؤسسي", unit="برنامج",
         cap_day=22 / 300, days=300, price=42000.0, cogs=0.30,
         ramp=[0.41, 0.59, 0.73, 0.82, 0.88]),
]
for L in lines:
    L["cap_year"] = L["cap_day"] * L["days"]
    L["rev_full"] = L["cap_year"] * L["price"]
rev_full_total = sum(L["rev_full"] for L in lines)

YEARS = 10
PRICE_INF = 0.03
UTIL_CAP = 0.88


def util(L, y):
    if y <= 5:
        return L["ramp"][y - 1]
    return min(L["ramp"][4] * (1.02 ** (y - 5)), UTIL_CAP)


def price(L, y):
    return L["price"] * (1 + PRICE_INF) ** (y - 1)


# ============ 3) الهيكل الوظيفي ============
# (المسمى، الراتب الشهري، س1، س3، س5)  — عمالة الإنتاج من الأسر المنتجة بأجر القطعة ضمن تكلفة المبيعات
staff = [
    ("مدير المركز", 17000, 1, 1, 1),
    ("مدير التشغيل والإنتاج", 12500, 1, 1, 1),
    ("مدير التسويق والمبيعات وتطوير الأعمال", 11000, 0, 1, 1),
    ("مسؤول الجودة وسلامة الغذاء (HACCP)", 9500, 1, 1, 1),
    ("المحاسب / المسؤول المالي", 8500, 1, 1, 1),
    ("أخصائي تمكين وتنمية المستفيدات", 6500, 1, 2, 3),
    ("أخصائي الرصد والتقييم وقياس الأثر", 7000, 1, 1, 1),
    ("منسق الموارد البشرية والشؤون الإدارية", 6000, 1, 1, 1),
    ("مشرف إنتاج / رئيس وردية", 6500, 2, 3, 4),
    ("فني جودة ومختبر", 5000, 1, 2, 2),
    ("فني تشغيل معدات وخطوط", 4500, 2, 3, 4),
    ("أمين مستودع ومراقبة مخزون", 4200, 1, 1, 2),
    ("سائق توصيل مبرّد", 3800, 1, 2, 3),
    ("مندوب مبيعات وحسابات مؤسسية", 4800, 1, 2, 3),
    ("أخصائي تسويق رقمي ومحتوى", 5500, 1, 1, 1),
    ("فني صيانة", 5000, 0, 1, 1),
    ("مشرف أمن وسلامة ونظافة", 2800, 1, 2, 2),
]
BENEFITS = 0.185   # التأمينات + نهاية الخدمة + التأمين الطبي
head = {1: sum(s[2] for s in staff), 3: sum(s[3] for s in staff), 5: sum(s[4] for s in staff)}
base = {1: sum(s[1] * s[2] for s in staff) * 12,
        3: sum(s[1] * s[3] for s in staff) * 12,
        5: sum(s[1] * s[4] for s in staff) * 12}
pay_anchor = {y: base[y] * (1 + BENEFITS) for y in (1, 3, 5)}


def payroll(y):
    if y == 1:
        return pay_anchor[1]
    if y == 2:
        return (pay_anchor[1] + pay_anchor[3]) / 2 * 1.04
    if y == 3:
        return pay_anchor[3] * (1.04 ** 2)
    if y == 4:
        return (pay_anchor[3] + pay_anchor[5]) / 2 * (1.04 ** 3)
    return pay_anchor[5] * (1.04 ** (y - 1))


def headcount(y):
    if y == 1:
        return head[1]
    if y == 2:
        return round((head[1] + head[3]) / 2)
    if y == 3:
        return head[3]
    if y == 4:
        return round((head[3] + head[5]) / 2)
    return head[5]


# ============ 4) المصروفات التشغيلية ============
USUFRUCT_VALUE = 525000     # القيمة السوقية لإيجار المقر — مساهمة عينية من الجمعية (خارج التدفق النقدي)


def opex_detail(y, rev, au, pay_f=1.0, occ_f=1.0, capex_f=1.0):
    g = lambda r: (1 + r)
    d = {}
    d["الرواتب والأجور ومزايا العاملين"] = payroll(y) * pay_f
    d["رسوم خدمات المقر والمرافق المشتركة"] = 120000 * (1.03 ** (y - 1)) * occ_f
    d["الكهرباء والمياه والغاز"] = 300000 * (1.03 ** (y - 1)) * (0.42 + 0.58 * (au / 0.31)) * occ_f
    d["الصيانة وقطع الغيار"] = equip_value * 0.035 * (1.05 ** (y - 1)) * capex_f
    d["التأمينات على الأصول والمسؤولية"] = 70000 * (1.03 ** (y - 1))
    d["النقل والتوزيع وسلسلة التبريد"] = rev * 0.032
    d["التسويق والترويج والمعارض"] = rev * (0.045 if y == 1 else 0.030)
    d["المصروفات الإدارية والاتصالات والقرطاسية"] = 100000 * (1.03 ** (y - 1))
    d["الرسوم والتراخيص والشهادات (ISO 22000 / HACCP)"] = 85000 * (1.03 ** (y - 1))
    d["تدريب وتطوير فريق العمل"] = 70000 * (1.03 ** (y - 1))
    d["الحوكمة والمراجعة الخارجية والاستشارات"] = 95000 * (1.03 ** (y - 1))
    d["برامج تمكين الأسر (تدريب، حقائب، حوافز إنتاج)"] = 265000 * (1.06 ** (y - 1))
    sub = sum(d.values())
    d["مصروفات أخرى وطوارئ تشغيلية (2%)"] = sub * 0.02
    return d


# ============ 5) بناء النموذج ============
rows = []
for y in range(1, YEARS + 1):
    line_rev, line_cogs = {}, {}
    for L in lines:
        r = L["cap_year"] * util(L, y) * price(L, y)
        line_rev[L["key"]] = r
        line_cogs[L["key"]] = r * L["cogs"]
    rev, cogs = sum(line_rev.values()), sum(line_cogs.values())
    au = rev / (rev_full_total * (1 + PRICE_INF) ** (y - 1))
    od = opex_detail(y, rev, au)
    opex = sum(od.values())
    gross = rev - cogs
    ebitda = gross - opex
    dep = da5 if y <= 5 else dep_annual
    rows.append(dict(y=y, line_rev=line_rev, line_cogs=line_cogs, rev=rev, cogs=cogs,
                     gross=gross, opex_detail=od, opex=opex, ebitda=ebitda, dep=dep,
                     surplus=ebitda - dep, au=au, head=headcount(y),
                     oss=rev / (cogs + opex)))

# ============ 6) التدفقات النقدية والمؤشرات ============
DISC = 0.08
cf = [-funding_total]
prev_wc = working_capital
cash_bridge = opex_bridge
for r in rows:
    y = r["y"]
    repl = 0 if y <= 4 else equip_value * 0.045 * (1.03 ** (y - 5))
    wc_need = r["rev"] * 0.055
    d_wc = wc_need - prev_wc
    prev_wc = wc_need
    r["repl"], r["d_wc"] = repl, d_wc
    r["fcf"] = r["ebitda"] - repl - d_wc
    cf.append(r["fcf"])

npv = sum(c / (1 + DISC) ** i for i, c in enumerate(cf))


def irr(flows):
    if sum(flows) <= 0:          # لا يتحقق استرداد ضمن أفق الدراسة
        return None
    lo, hi = -0.95, 3.0
    for _ in range(400):
        mid = (lo + hi) / 2
        v = sum(c / (1 + mid) ** i for i, c in enumerate(flows))
        lo, hi = (mid, hi) if v > 0 else (lo, mid)
    return (lo + hi) / 2


irr_v = irr(cf)
npv_at = {r: sum(c / (1 + r) ** i for i, c in enumerate(cf)) for r in (0.04, 0.05, 0.06, 0.08, 0.10)}

# معدل العائد على مساهمة الجمعية وحدها (رأس المال المستحق الاسترداد)،
# باعتبار المنح غير مستردة والقرض الحسن يُسدَّد من الفائض
assoc_cf = [-1125000] + [r["fcf"] - (250000 if 3 <= r["y"] <= 5 else 0) for r in rows]
assoc_irr = irr(assoc_cf)
assoc_npv = sum(c / 1.08 ** i for i, c in enumerate(assoc_cf))

# نسبة تغطية خدمة الدين للقرض الميسّر (750,000 على 4 سنوات من السنة الثانية)
dscr = [(r["y"], r["ebitda"] / 250000) for r in rows if 3 <= r["y"] <= 5]
cum, payback, cumcash = 0.0, None, []
for i, c in enumerate(cf):
    prev = cum
    cum += c
    if i > 0:
        cumcash.append(cum)
        if payback is None and prev < 0 <= cum:
            payback = i - 1 + (-prev) / c

# نقطة التعادل — السنة الثالثة
r3 = rows[2]
o3 = r3["opex_detail"]
var_keys = ["النقل والتوزيع وسلسلة التبريد", "التسويق والترويج والمعارض"]
fixed3 = sum(v for k, v in o3.items() if k not in var_keys and k != "الكهرباء والمياه والغاز") \
    + o3["الكهرباء والمياه والغاز"] * 0.42 + r3["dep"]
variable3 = r3["cogs"] + sum(o3[k] for k in var_keys) + o3["الكهرباء والمياه والغاز"] * 0.58
cm_ratio = (r3["rev"] - variable3) / r3["rev"]
be_rev = fixed3 / cm_ratio
be_pct = be_rev / r3["rev"]
be_util = r3["au"] * be_pct


# ============ 7) الحساسية والسيناريوهات ============
def run(price_f=1.0, vol_f=1.0, cogs_f=1.0, pay_f=1.0, capex_f=1.0, occ_f=1.0, want=None):
    fund = capex_total * capex_f + working_capital + opex_bridge
    flows, pwc, res = [-fund], working_capital, {}
    for y in range(1, YEARS + 1):
        rev = sum(L["cap_year"] * util(L, y) * vol_f * price(L, y) * price_f for L in lines)
        cg = sum(L["cap_year"] * util(L, y) * vol_f * price(L, y) * price_f * L["cogs"] * cogs_f for L in lines)
        au = rev / (rev_full_total * (1 + PRICE_INF) ** (y - 1) * price_f * vol_f) * vol_f
        opx = sum(opex_detail(y, rev, au, pay_f=pay_f, occ_f=occ_f, capex_f=capex_f).values())
        ebitda = rev - cg - opx
        repl = 0 if y <= 4 else equip_value * 0.045 * (1.03 ** (y - 5)) * capex_f
        wcn = rev * 0.055
        flows.append(ebitda - repl - (wcn - pwc))
        pwc = wcn
        if want and y == want:
            res = dict(rev=rev, cogs=cg, opex=opx, ebitda=ebitda,
                       surplus=ebitda - (da5 if y <= 5 else dep_annual))
    n = sum(c / (1 + DISC) ** i for i, c in enumerate(flows))
    return (n, res, flows) if want else n


base_npv = run()
sens = []
for label, kw in [("سعر البيع", "price_f"), ("حجم المبيعات ونسبة الإشغال", "vol_f"),
                  ("تكلفة المواد الخام والتصنيع", "cogs_f"), ("الرواتب والأجور", "pay_f"),
                  ("التكلفة الرأسمالية", "capex_f"), ("تكاليف المقر والمرافق", "occ_f")]:
    up, dn = run(**{kw: 1.15}), run(**{kw: 0.85})
    sens.append(dict(label=label, up=up - base_npv, dn=dn - base_npv, swing=abs(up - base_npv) + abs(dn - base_npv)))
sens.sort(key=lambda s: -s["swing"])

scen = {}
for name, (vf, pf, cfx) in [("متحفّظ", (0.85, 0.96, 1.05)), ("أساسي", (1.0, 1.0, 1.0)), ("متفائل", (1.12, 1.04, 0.97))]:
    n3, r3s, fl = run(vol_f=vf, price_f=pf, cogs_f=cfx, want=3)
    n5, r5s, _ = run(vol_f=vf, price_f=pf, cogs_f=cfx, want=5)
    scen[name] = dict(npv=n3, irr=irr(fl), rev3=r3s["rev"], surplus3=r3s["surplus"],
                      rev5=r5s["rev"], surplus5=r5s["surplus"], ebitda5=r5s["ebitda"])

# ============ 8) الأثر والعائد الاجتماعي ============
families = [65, 130, 190, 235, 280]
trainees = [280, 330, 375, 400, 420]
graduates_employed = [96, 132, 165, 184, 197]
income_before = 1180
income_after = [2400, 2900, 3350, 3600, 3820]
jobs = [headcount(y) for y in range(1, 6)]

sroi_rows = []
for i in range(5):
    inc = families[i] * (income_after[i] - income_before) * 12
    job_val = jobs[i] * 4600 * 12 * 0.35
    train_val = trainees[i] * 2600 * 0.55
    saved = families[i] * 0.40 * 9600
    sroi_rows.append(dict(inc=inc, job=job_val, train=train_val, saved=saved,
                          total=inc + job_val + train_val + saved))
ADJ = 0.72   # خصم الوزن الميت والإسناد والتناقص
pv_benefits = sum(b["total"] * ADJ / (1 + DISC) ** (i + 1) for i, b in enumerate(sroi_rows))
pv_costs = funding_total + sum(max(0.0, -rows[i]["ebitda"]) / (1 + DISC) ** (i + 1) for i in range(5))
sroi = pv_benefits / pv_costs
cost_per_beneficiary = funding_total / (sum(families) / 1 + sum(trainees))

# ============ 9) السوق ============
market = dict(tam=4_850_000_000, sam=412_000_000)
market["som3"] = rows[2]["rev"]
market["share3"] = rows[2]["rev"] / market["sam"]
market["som5"] = rows[4]["rev"]
market["share5"] = rows[4]["rev"] / market["sam"]

gap = [dict(y="س1", demand=41.5, supply=17.2), dict(y="س2", demand=46.8, supply=20.6),
       dict(y="س3", demand=52.9, supply=24.9), dict(y="س4", demand=59.4, supply=29.8),
       dict(y="س5", demand=66.2, supply=35.4)]
for g in gap:
    g["gap"] = round(g["demand"] - g["supply"], 1)

out = dict(capex_items=capex_items, intangibles=intangibles, tangible_total=tangible_total,
           intang_total=intang_total, contingency=contingency, capex_total=capex_total,
           working_capital=working_capital, opex_bridge=opex_bridge, funding_total=funding_total,
           funding_mix=funding_mix, dep_annual=dep_annual, amort_annual=amort_annual, da5=da5,
           usufruct=USUFRUCT_VALUE, lines=lines, rev_full_total=rev_full_total, staff=staff,
           head=head, pay_anchor=pay_anchor, rows=rows, npv=npv, irr=irr_v, payback=payback,
           cumcash=cumcash, cf=cf, npv_at=npv_at, assoc_irr=assoc_irr, assoc_npv=assoc_npv,
           dscr=dscr, be_rev=be_rev, be_pct=be_pct, be_util=be_util,
           cm_ratio=cm_ratio, fixed3=fixed3, variable3=variable3, sens=sens, scen=scen,
           families=families, trainees=trainees, graduates_employed=graduates_employed,
           jobs=jobs, income_after=income_after, income_before=income_before,
           sroi=sroi, pv_benefits=pv_benefits, pv_costs=pv_costs, sroi_rows=sroi_rows,
           cost_per_beneficiary=cost_per_beneficiary, market=market, gap=gap)
with open(SCR + "/model.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=float)

# ============ طباعة ============
print(f"CAPEX {capex_total:,.0f} | WC {working_capital:,.0f} | Bridge {opex_bridge:,.0f} | TOTAL {funding_total:,.0f}")
print(f"D&A(1-5) {da5:,.0f} | dep only {dep_annual:,.0f} | full-capacity rev {rev_full_total:,.0f}")
print(f"Headcount 1/3/5 {head[1]}/{head[3]}/{head[5]} | payroll {pay_anchor[1]:,.0f} / {pay_anchor[3]:,.0f} / {pay_anchor[5]:,.0f}")
print()
hdr = f"{'Y':>2} {'Rev':>11} {'COGS':>11} {'GM%':>6} {'Opex':>11} {'EBITDA':>10} {'EB%':>6} {'Surplus':>10} {'Util':>6} {'HC':>3} {'OSS':>6} {'FCF':>10} {'Cum':>11}"
print(hdr)
for i, r in enumerate(rows):
    print(f"{r['y']:>2} {r['rev']:>11,.0f} {r['cogs']:>11,.0f} {(r['gross']/r['rev'])*100:>5.1f}% "
          f"{r['opex']:>11,.0f} {r['ebitda']:>10,.0f} {r['ebitda']/r['rev']*100:>5.1f}% {r['surplus']:>10,.0f} "
          f"{r['au']*100:>5.1f}% {r['head']:>3} {r['oss']*100:>5.0f}% {r['fcf']:>10,.0f} {cumcash[i]:>11,.0f}")
print()
print("NPV@8% {:,.0f} | IRR {} | Payback {} yrs".format(npv, "n/a" if irr_v is None else f"{irr_v*100:.1f}%", payback if payback is None else round(payback,2)))
print("NPV by discount rate:", {f"{k*100:.0f}%": f"{v:,.0f}" for k,v in npv_at.items()})
print("Association IRR", "n/a" if assoc_irr is None else f"{assoc_irr*100:.1f}%", "| assoc NPV@8%", f"{assoc_npv:,.0f}")
print("DSCR:", [(y, round(v,2)) for y,v in dscr])
print(f"Break-even Y3 rev {be_rev:,.0f} ({be_pct*100:.1f}% of Y3) | CM {cm_ratio*100:.1f}% | BE util {be_util*100:.1f}%")
print(f"SROI {sroi:.2f} : 1 | PV benefits {pv_benefits:,.0f} | PV costs {pv_costs:,.0f} | cost/beneficiary {cost_per_beneficiary:,.0f}")
print(f"SAM share Y3 {market['share3']*100:.2f}% | Y5 {market['share5']*100:.2f}%")
print()
print("SENSITIVITY ΔNPV:")
for s in sens:
    print(f"  {s['label']:<30} +15% {s['up']:>13,.0f}   -15% {s['dn']:>13,.0f}")
print()
print("SCENARIOS:")
for k, v in scen.items():
    print(f"  {k:<8} NPV {v['npv']:>12,.0f}  IRR {('  n/a' if v['irr'] is None else format(v['irr']*100,'5.1f')):>5}  Rev3 {v['rev3']:>11,.0f}  Surp3 {v['surplus3']:>11,.0f}  Rev5 {v['rev5']:>11,.0f}  Surp5 {v['surplus5']:>11,.0f}")
print()
print("REVENUE BY LINE (Y1..Y5):")
for L in lines:
    print(f"  {L['short']:<18}", " ".join(f"{rows[y]['line_rev'][L['key']]:>11,.0f}" for y in range(5)))
print()
print("OPEX DETAIL Y3:")
for k, v in rows[2]["opex_detail"].items():
    print(f"  {k:<52} {v:>11,.0f}")
