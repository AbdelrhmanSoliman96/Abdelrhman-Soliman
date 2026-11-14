# -*- coding: utf-8 -*-
"""Financial model: interior design office, New Cairo, Egypt. All figures EGP."""
import json, random, math, copy

BASE = dict(
    n_res=[26, 40, 52, 60, 66], n_com=[6, 10, 14, 18, 21],
    area_res=210, area_com=320, fee_res=520, fee_com=680,
    price_esc=[0, .12, .11, .10, .09],
    exec_m2=10000, ffe_m2=3800,
    sup_attach=[.30, .35, .38, .40, .40], sup_fee=.07,
    tk_attach=[.15, .20, .22, .25, .25], tk_fee=.15,
    ffe_attach=[.25, .30, .33, .35, .35], ffe_fee=.06,
    sal_esc=[0, .14, .13, .12, .11], cost_esc=[0, .13, .12, .11, .10],
    rent_m2=1000, office_m2=[120, 120, 180, 180, 180], rent_esc=.10,
    payroll_load=.15, tax=.225, wacc=.27, g=.08,
    debt_share=.35, debt_rate=.24, vol_mult=1.0, fee_mult=1.0, opex_mult=1.0,
)

ROLES = [  # name, monthly gross Y1, headcount Y1..Y5, design seat?
    ("المدير العام والمدير الإبداعي", 60000, [1, 1, 1, 1, 1], 1),
    ("مدير تصميم", 36000, [1, 1, 2, 2, 2], 1),
    ("مصمم داخلي", 20000, [2, 3, 4, 5, 5], 1),
    ("مصمم إظهار ثلاثي الأبعاد", 21000, [1, 2, 2, 3, 3], 1),
    ("مهندس مكتب فني ولوحات تنفيذية", 21000, [1, 1, 2, 2, 3], 1),
    ("مدير مشروعات التنفيذ", 38000, [0, 1, 1, 1, 1], 0),
    ("مهندس إشراف موقع", 23000, [1, 2, 3, 4, 4], 0),
    ("مهندس حصر ومشتريات", 20000, [0, 1, 1, 1, 2], 0),
    ("مسؤول تطوير أعمال وعلاقات عملاء", 20000, [0, 1, 1, 2, 2], 0),
    ("أخصائي تسويق رقمي ومحتوى", 17000, [1, 1, 1, 1, 1], 0),
    ("محاسب", 15000, [0, 1, 1, 1, 1], 0),
    ("منسق إداري واستقبال", 10000, [1, 1, 1, 1, 1], 0),
    ("خدمات معاونة", 8000, [1, 1, 1, 1, 1], 0),
]

SCALABLE = {2, 3, 4, 6, 7, 8}

CAPEX = [  # item, amount, class
    ("تجهيز وتشطيب المقر (120 م² × 9,500 جنيه)", 1140000, "fit"),
    ("أثاث مكتبي ومكتبة خامات وعينات", 520000, "furn"),
    ("محطات عمل تصميم عالية الأداء (5 × 110,000)", 550000, "it"),
    ("حواسب محمولة (3 × 65,000)", 195000, "it"),
    ("خادم إظهار ووحدة تخزين شبكي", 380000, "it"),
    ("راسمة A1 وطابعات", 240000, "it"),
    ("تجهيزات واقع افتراضي وشاشة عرض", 160000, "it"),
    ("شبكات وطاقة احتياطية وتكييف وأنظمة أمان", 310000, "furn"),
]
PREOP = [
    ("تأسيس الشركة والتراخيص والقيد المهني", 140000),
    ("الهوية البصرية والموقع الإلكتروني وتصوير الأعمال", 380000),
    ("حملة الإطلاق التسويقية", 450000),
    ("التوظيف والتدريب قبل التشغيل", 120000),
    ("إيجار فترة التجهيز (3 أشهر)", 360000),
    ("رواتب الفريق الأساسي قبل الافتتاح (شهران)", 320000),
    ("استشارات قانونية ومالية ودراسات", 100000),
]
DEPOSIT = 240000
DEP_RATE = {"fit": .20, "furn": .125, "it": .25}


def cum(esc):
    out, f = [], 1.0
    for e in esc:
        f *= (1 + e); out.append(f)
    return out


def irr(cfs):
    lo, hi = -0.99, 5.0
    f = lambda r: sum(c / (1 + r) ** i for i, c in enumerate(cfs))
    if f(lo) * f(hi) > 0:
        return float('nan')
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2


def run(p=None, detail=True):
    p = {**BASE, **(p or {})}
    Y = range(5)
    pe, se, ce = cum(p['price_esc']), cum(p['sal_esc']), cum(p['cost_esc'])
    R = {k: [] for k in ['res', 'com', 'sup', 'tk', 'ffe', 'total', 'projects']}
    for y in Y:
        nr, nc = p['n_res'][y] * p['vol_mult'], p['n_com'][y] * p['vol_mult']
        n = nr + nc
        area = (nr * p['area_res'] + nc * p['area_com'])
        res = nr * p['area_res'] * p['fee_res'] * pe[y] * p['fee_mult']
        com = nc * p['area_com'] * p['fee_com'] * pe[y] * p['fee_mult']
        execv = area * p['exec_m2'] * pe[y]
        sup = execv * p['sup_attach'][y] * p['sup_fee'] * p['fee_mult']
        tk = execv * p['tk_attach'][y] * p['tk_fee'] * p['fee_mult']
        ffe = area * p['ffe_m2'] * pe[y] * p['ffe_attach'][y] * p['ffe_fee'] * p['fee_mult']
        for k, v in zip(['res', 'com', 'sup', 'tk', 'ffe'], [res, com, sup, tk, ffe]): R[k].append(v)
        R['total'].append(res + com + sup + tk + ffe); R['projects'].append(n)
    # costs
    C = {k: [] for k in ['payroll', 'rent', 'software', 'marketing', 'commission', 'outsourced', 'site',
                         'utilities', 'professional', 'insurance', 'training', 'admin', 'baddebt', 'contingency', 'total']}
    head, seats = [], []
    for y in Y:
        # production roles follow workload (hiring is triggered by signed contracts, not by calendar)
        eff = [max(hc[0], hc[y] * p['vol_mult']) if i in SCALABLE and y > 0 else hc[y] for i, (_, _, hc, _) in enumerate(ROLES)]
        gross = sum(r[1] * e for r, e in zip(ROLES, eff)) * 12 * se[y]
        payroll = gross * (1 + p['payroll_load'])
        head.append(sum(eff))
        st = sum(e for r, e in zip(ROLES, eff) if r[3]); seats.append(st)
        rent = p['office_m2'][y] * p['rent_m2'] * 12 * (1 + p['rent_esc']) ** y * 1.08
        software = st * 95000 * ce[y]
        mk_rate = [.09, .07, .06, .06, .05][y]
        marketing = max(700000 * ce[y], mk_rate * R['total'][y])
        commission = .025 * R['total'][y]
        outsourced = .04 * (R['res'][y] + R['com'][y])
        site = .12 * (R['sup'][y] + R['tk'][y])
        utilities = 18000 * 12 * ce[y] * (p['office_m2'][y] / 120)
        professional = (180000 + (96000 if y == 0 else 0)) * ce[y]
        insurance = .008 * R['total'][y]
        training = .02 * payroll
        admin = 20000 * 12 * ce[y] * (head[y] / 10) ** .6
        baddebt = .015 * R['total'][y]
        vals = dict(payroll=payroll, rent=rent, software=software, marketing=marketing, commission=commission,
                    outsourced=outsourced, site=site, utilities=utilities, professional=professional,
                    insurance=insurance, training=training, admin=admin, baddebt=baddebt)
        sub = sum(vals.values()) * p['opex_mult']
        vals = {k: v * p['opex_mult'] for k, v in vals.items()}
        vals['contingency'] = .03 * sub
        vals['total'] = sub * 1.03
        for k, v in vals.items(): C[k].append(v)
    # capex schedule
    capex0 = sum(a for _, a, _ in CAPEX)
    preop = sum(a for _, a in PREOP)
    add_capex = [0.0] * 5
    add_cls = [dict(fit=0, furn=0, it=0) for _ in Y]
    for y in range(1, 5):
        new_seats = max(0, seats[y] - seats[y - 1])
        it = new_seats * 110000 * ce[y] + max(0, head[y] - head[y - 1] - new_seats) * 30000 * ce[y]
        fit = 0
        if p['office_m2'][y] > p['office_m2'][y - 1]:
            fit = (p['office_m2'][y] - p['office_m2'][y - 1]) * 9500 * ce[y] * 1.25
        if y == 3: it += 700000 * ce[y] * 0.9  # IT refresh
        add_cls[y] = dict(fit=fit, furn=0, it=it); add_capex[y] = fit + it
    base_cls = dict(fit=0, furn=0, it=0)
    for _, a, c in CAPEX: base_cls[c] += a
    dep = []
    for y in Y:
        d = 0
        for c, r in DEP_RATE.items():
            life = round(1 / r)
            if y < life: d += base_cls[c] * r
            for yy in range(1, y + 1):
                if y - yy < life: d += add_cls[yy][c] * r
        dep.append(d)
    # working capital
    nwc = []
    for y in Y:
        nonpay = C['total'][y] - C['payroll'][y]
        nwc.append(R['total'][y] * (45 - 20) / 365 - nonpay * 30 / 365)
    dnwc = [nwc[0]] + [nwc[y] - nwc[y - 1] for y in range(1, 5)]
    # funding: initial investment
    wc_reserve = p.get('wc_fixed') or C['total'][0] * 6 / 12
    invest = capex0 + preop + DEPOSIT + wc_reserve
    debt = invest * p['debt_share']; equity = invest - debt
    # loan: 5y, year-1 grace on principal, equal principal in years 2-5
    bal, interest, principal = debt, [], []
    for y in Y:
        interest.append(bal * p['debt_rate'])
        pr = 0 if y == 0 else debt / 4
        principal.append(pr); bal -= pr
    # income statement
    ebitda = [R['total'][y] - C['total'][y] for y in Y]
    ebit = [ebitda[y] - dep[y] for y in Y]
    ebit[0] -= 0  # pre-opening expensed in year 0
    # tax with loss carry-forward (pre-opening counted as year-0 loss)
    def taxes(pre):
        loss, out = preop, []
        for v in pre:
            if v <= 0: loss += -v; out.append(0)
            else:
                use = min(loss, v); loss -= use; out.append((v - use) * p['tax'])
        return out
    ebt = [ebit[y] - interest[y] for y in Y]
    tax = taxes(ebt)
    ni = [ebt[y] - tax[y] for y in Y]
    # project (unlevered) FCF
    utax = taxes(ebit)
    fcf = [ebitda[y] - utax[y] - add_capex[y] - dnwc[y] for y in Y]
    cf0 = -(capex0 + preop + DEPOSIT)
    tv = fcf[4] * (1 + p['g']) / (p['wacc'] - p['g'])
    flows = [cf0] + fcf
    flows_tv = flows[:-1] + [fcf[4] + tv]
    npv = sum(c / (1 + p['wacc']) ** i for i, c in enumerate(flows))
    npv_tv = sum(c / (1 + p['wacc']) ** i for i, c in enumerate(flows_tv))
    # equity cash flows
    fcfe = [ebitda[y] - tax[y] - interest[y] - principal[y] - add_capex[y] - dnwc[y] for y in Y]
    cash, c = [], wc_reserve
    for y in Y:
        c += fcfe[y]; cash.append(c)
    eq_flows = [-equity] + fcfe[:-1] + [fcfe[4] + tv - bal]
    # payback (project, undiscounted & discounted, on flows w/o TV)
    def payback(fl, r=0):
        acc = 0
        for i, v in enumerate(fl):
            dv = v / (1 + r) ** i
            if acc + dv >= 0 and i > 0:
                return i - 1 + (-acc) / dv
            acc += dv
        return float('nan')
    dscr = [(ebitda[y] - tax[y]) / (interest[y] + principal[y]) for y in Y]
    # break-even year by year: fixed vs variable
    var_rate = [(C['commission'][y] + C['outsourced'][y] + C['site'][y] + C['insurance'][y] + C['baddebt'][y]) / R['total'][y] for y in Y]
    fixed = [C['total'][y] - var_rate[y] * R['total'][y] + dep[y] + interest[y] for y in Y]
    be = [fixed[y] / (1 - var_rate[y]) for y in Y]
    out = dict(R=R, C=C, head=head, seats=seats, capex0=capex0, preop=preop, deposit=DEPOSIT, wc_reserve=wc_reserve,
               invest=invest, debt=debt, equity=equity, interest=interest, principal=principal, dep=dep,
               ebitda=ebitda, ebit=ebit, ebt=ebt, tax=tax, ni=ni, fcf=fcf, cf0=cf0, tv=tv, npv=npv, npv_tv=npv_tv,
               irr=irr(flows), irr_tv=irr(flows_tv), eq_irr=irr(eq_flows), fcfe=fcfe, cash=cash,
               payback=payback(flows), dpayback=payback(flows, p['wacc']), dpayback_tv=payback(flows_tv, p['wacc']),
               dscr=dscr, be=be, var_rate=var_rate, add_capex=add_capex, nwc=nwc, dnwc=dnwc, flows=flows,
               pi=(npv_tv - cf0) / -cf0, wacc=p['wacc'], pe=pe, se=se)
    return out


def tri(a, m, b):
    return random.triangular(a, b, m)


def montecarlo(n=10000, seed=7):
    random.seed(seed)
    res = []
    for _ in range(n):
        p = dict(vol_mult=tri(.65, 1.0, 1.2), fee_mult=tri(.82, 1.0, 1.12), opex_mult=tri(.94, 1.0, 1.18),
                 wacc=tri(.24, .27, .32))
        o = run(p)
        res.append((o['npv_tv'], o['irr_tv'], o['npv'], min(o['cash'])))
    return res


if __name__ == '__main__':
    o = run()
    f = lambda xs: [round(x / 1e6, 2) for x in xs]
    print('rev', f(o['R']['total'])); print('opex', f(o['C']['total'])); print('ebitda', f(o['ebitda']))
    print('ni', f(o['ni'])); print('fcf', f(o['fcf'])); print('fcfe', f(o['fcfe'])); print('cash', f(o['cash']))
    print('invest', o['invest'], 'debt', o['debt'], 'eq', o['equity'], 'wc', o['wc_reserve'])
    print('npv', o['npv'] / 1e6, 'npv_tv', o['npv_tv'] / 1e6, 'irr', o['irr'], 'irr_tv', o['irr_tv'], 'eq_irr', o['eq_irr'])
    print('payback', o['payback'], o['dpayback'], o['dpayback_tv'], 'dscr', [round(x, 2) for x in o['dscr']])
    print('be', f(o['be']), 'head', o['head'], 'tv', o['tv'] / 1e6, 'pi', o['pi'])
    for k, v in o['C'].items(): print(k, f(v))
    for k, v in o['R'].items(): print(k, f(v))
    mc = montecarlo(3000)
    print('P(npv_tv>0)', sum(1 for r in mc if r[0] > 0) / len(mc), 'P(npv>0)', sum(1 for r in mc if r[2] > 0) / len(mc),
          'P(cash<0)', sum(1 for r in mc if r[3] < 0) / len(mc))
