"""Capex, D&A, Expenses, Income Statement, Cash Flow, Balance Sheet, Financial Indicators, Funding and Use of Funds."""
from xl import *

YCOLS = "CDEFG"


class Ann:
    """Annual sheet writer, Year 1 to Year 5 in columns C to G."""

    def __init__(self, ws, REG, start=4, a=58):
        self.ws, self.r = ws, start
        self.reg = REG.setdefault(ws.title, {})
        ws.column_dimensions["A"].width = a
        ws.column_dimensions["B"].width = 16
        for c in YCOLS:
            ws.column_dimensions[c].width = 15
        ws.column_dimensions["H"].width = 16

    def section(self, text, sub=None, cols=("Year 1, 2027", "Year 2, 2028", "Year 3, 2029", "Year 4, 2030", "Year 5, 2031")):
        section(self.ws, self.r, text, 8)
        self.r += 1
        if sub:
            note(self.ws, self.r, sub)
            self.r += 1
        if cols:
            hdr(self.ws, self.r, ["Line item", ""] + list(cols))
            self.r += 1

    def line(self, key, text, fn, fmt=USD, bold=False, indent=0, kind=None):
        label(self.ws, self.r, text, bold=bold, indent=indent)
        for y in range(1, 6):
            v = fn(y)
            if v is None:
                continue
            if isinstance(v, str) and not v.startswith("="):
                v = "=" + v
            c = put(self.ws, f"{YCOLS[y - 1]}{self.r}", v, fmt, kind=kind, bold=bold, size=8.6 if bold else 8.2)
            if bold:
                c.fill = fill(YFILL)
        if key:
            self.reg[key] = self.r
        self.r += 1
        return self.r - 1

    def kv(self, key, text, value, fmt=USD, kind=None, bold=False, unit=None, col="C"):
        label(self.ws, self.r, text, bold=bold)
        if unit:
            label(self.ws, self.r, unit, col=2, size=8, color=GREY)
        if isinstance(value, str) and not value.startswith("=") and kind != "input" and fmt != "@":
            value = "=" + value
        put(self.ws, f"{col}{self.r}", value, fmt, kind=kind, bold=bold, size=9 if bold else 8.4)
        if key:
            self.reg[key] = self.r
        self.r += 1
        return self.r - 1

    def blank(self, n=1):
        self.r += n


def T(sheet, key, m):
    """Monthly cell on another sheet."""
    return f"'{sheet}'!{mcol(m)}{tok(sheet, key)}"


def TY(sheet, key, y):
    """Year total cell on a time sheet."""
    return f"'{sheet}'!{ycol(y)}{tok(sheet, key)}"


def TE(sheet, key, y):
    """Last month of the year on a time sheet."""
    return f"'{sheet}'!{mcol(12 * y)}{tok(sheet, key)}"


def TA(sheet, key, y):
    """Annual sheet cell, columns C to G."""
    return f"'{sheet}'!{YCOLS[y - 1]}{tok(sheet, key)}"


def TC(sheet, key):
    return f"'{sheet}'!$C${tok(sheet, key)}"


def MR(sheet, key, y=None):
    """The twelve monthly cells of year y, or all sixty months."""
    if y is None:
        return f"'{sheet}'!$C${tok(sheet, key)}:$BN${tok(sheet, key)}"
    return f"'{sheet}'!{mcol(12 * y - 11)}{tok(sheet, key)}:{mcol(12 * y)}{tok(sheet, key)}"


PPE = [("as_lap", "Laptop"), ("as_mon", "Monitor and peripherals"), ("as_ph", "Mobile handset and line set up"), ("as_desk", "Desk and chair")]
SHARED = [("sa_prod", "Product already built, founder investment to date", "I"), ("sa_ip", "Trademark, entity, IP and app store accounts", "I"),
          ("sa_qat", "Qatar entity, QFC or QSTP licence", "I"), ("sa_ksa", "Saudi entity, MISA licence and registration", "I"),
          ("sa_cert", "SOC 2 and ISO 27001 initial certification", "I"), ("sa_cai", "Cairo office fit out", "E"), ("sa_ruh", "Riyadh office set up", "E"),
          ("sa_doh", "Doha co working set up and launch kit", "E"), ("sa_av", "Event booth, studio and community kit", "E")]


def build_capex(ws, A, REG):
    title(ws, "Capital Expenditure", "Assets follow the hiring plan. Platform development is expensed through payroll; only the build to date is carried as an intangible, contributed by the founders.")
    set_time_widths(ws, 54)
    t = TS(ws, REG, 4)
    g = REG[ws.title]
    t.section("ADDITIONS IN THE MONTH")
    for key, txt in PPE:
        t.line(f"x_{key}", txt, lambda m, key=key: f"{T('Payroll', 'hires', m)}*{A.c(key, 'C')}*{A.c(key, 'D')}", USD)
    for key, txt, _ in SHARED:
        t.line(f"x_{key}", txt, lambda m, key=key: f"IF({m}={A.c(key, 'C')},{A.c(key, 'D')},0)", USD)
    keys = [k for k, _ in PPE] + [k for k, _, _ in SHARED]
    t.line("tot", "Total additions to the asset register", lambda m: "+".join(f"{mcol(m)}{g['x_' + k]}" for k in keys), USD, bold=True)
    t.line("nc", "Of which contributed by the founders, no cash paid", lambda m: f"{mcol(m)}{g['x_sa_prod']}", USD)
    t.line("cash", "Capital expenditure paid in cash", lambda m: f"{mcol(m)}{g['tot']}-{mcol(m)}{g['nc']}", USD, bold=True)
    t.blank()
    t.section("GROSS COST, CUMULATIVE")
    for k in keys:
        t.line(f"g_{k}", dict(PPE + [(a, b) for a, b, _ in SHARED])[k],
               lambda m, k=k: f"{mcol(m)}{g['x_' + k]}" if m == 1 else f"{mcol(m - 1)}{tok(ws.title, 'g_' + k)}+{mcol(m)}{g['x_' + k]}", USD, total="end")
    t.line("gtot", "Total gross assets", lambda m: "+".join(f"{mcol(m)}{tok(ws.title, 'g_' + k)}" for k in keys), USD, total="end", bold=True)


def build_da(ws, A, REG):
    title(ws, "Depreciation and Amortization", "Straight line by asset class over the useful life on the Assumption sheet.")
    set_time_widths(ws, 54)
    t = TS(ws, REG, 4)
    keys = [k for k, _ in PPE] + [k for k, _, _ in SHARED]
    names = dict(PPE + [(a, b) for a, b, _ in SHARED])
    life = {k: A.c(k, "E") for k, _ in PPE}
    life.update({k: A.c(k, "E") for k, _, _ in SHARED})
    t.section("MONTHLY CHARGE")
    for k in keys:
        t.line(f"d_{k}", names[k], lambda m, k=k: f"{mcol(m)}{tok(ws.title, 'a_' + k)}" if m == 1 else f"{mcol(m)}{tok(ws.title, 'a_' + k)}-{mcol(m - 1)}{tok(ws.title, 'a_' + k)}", USD)
    t.line("da", "Total depreciation and amortization", lambda m: "+".join(f"{mcol(m)}{tok(ws.title, 'd_' + k)}" for k in keys), USD, bold=True)
    t.blank()
    t.section("ACCUMULATED DEPRECIATION AND NET BOOK VALUE")
    for k in keys:
        gross = lambda m, k=k: T("Capital Expenditure", "g_" + k, m)
        t.line(f"a_{k}", names[k], lambda m, k=k, gross=gross:
               f"MIN(IFERROR({gross(m)}/{life[k]},0),{gross(m)})" if m == 1 else
               f"MIN({mcol(m - 1)}{tok(ws.title, 'a_' + k)}+IFERROR({gross(m)}/{life[k]},0),{gross(m)})", USD, total="end")
    t.line("acc", "Total accumulated depreciation", lambda m: "+".join(f"{mcol(m)}{tok(ws.title, 'a_' + k)}" for k in keys), USD, total="end")
    ppe = [k for k, _ in PPE] + [k for k, _, ty in SHARED if ty == "E"]
    intg = [k for k, _, ty in SHARED if ty == "I"]
    t.line("ppe", "Property and equipment, net book value",
           lambda m: "+".join(f"{T('Capital Expenditure', 'g_' + k, m)}-{mcol(m)}{tok(ws.title, 'a_' + k)}" for k in ppe), USD, total="end", bold=True)
    t.line("int", "Intangible assets, net book value",
           lambda m: "+".join(f"{T('Capital Expenditure', 'g_' + k, m)}-{mcol(m)}{tok(ws.title, 'a_' + k)}" for k in intg), USD, total="end", bold=True)


OPEX = [("o_pay", "Payroll, fully loaded", "People"), ("o_comm", "Sales commission on sales led subscriptions", "Sales and marketing"),
        ("o_onl", "Marketing, online channels", "Sales and marketing"), ("o_off", "Events, meetups and community", "Sales and marketing"),
        ("o_brand", "Brand, creative and content production", "Sales and marketing"), ("o_inc", "Partner incentives and referral credits", "Sales and marketing"),
        ("o_onb", "Customer onboarding", "Sales and marketing"), ("o_pros", "Prospecting and private markets databases", "Sales and marketing"),
        ("o_trav", "Travel, GCC coverage", "Sales and marketing"), ("o_desk", "Co working desk and office services", "General and administrative"),
        ("o_rent", "Office rent", "General and administrative"), ("o_util", "Utilities, internet and communications", "General and administrative"),
        ("o_soft", "Software and tooling", "Technology"), ("o_cloud", "Cloud base platform and third party APIs", "Technology"),
        ("o_crm", "CRM, product analytics and data tools", "Technology"), ("o_sec", "Security testing and certification upkeep", "Technology"),
        ("o_rec", "Recruitment", "People"), ("o_train", "Training and enablement", "People"),
        ("o_fin", "Outsourced finance, legal and audit", "General and administrative"),
        ("o_reg", "Regulatory, licensing and data protection compliance", "General and administrative"),
        ("o_ins", "Insurance, bank charges and sundries", "General and administrative")]
DIRECT = [("d_pay", "Payment gateway and collection"), ("d_app", "App store commission"), ("d_ai", "AI inference, agents and valuations"),
          ("d_host", "Hosting, storage and data rooms"), ("d_data", "Market data and benchmark feeds"), ("d_sup", "Support of paying accounts"),
          ("d_val", "Valuation report delivery"), ("d_wl", "White label and SPV administration delivery"),
          ("d_psf", "Revenue share, accelerator partners"), ("d_psi", "Revenue share, angel networks")]


def build_expenses(ws, A, REG):
    title(ws, "Expenses", "Direct cost of delivery, revenue share to partners, operating cost, and the first twelve months in full: the expense the pre-seed ask is sized on.")
    set_time_widths(ws, 54)
    t = TS(ws, REG, 4)
    g = REG[ws.title]
    R = lambda k, m: f"{mcol(m)}{tok(ws.title, k)}"
    aq = lambda k, m: T("Acquisitions", k, m)
    rs = lambda k, m: T("Revenue Streams", k, m)
    pr = lambda k, m: T("Payroll", k, m)
    t.section("DIRECT COST OF DELIVERY")
    fx = {
        "d_pay": lambda m: f"{T('Total Revenue', 'rev', m)}*{A.y('dc_pay', m)}",
        "d_app": lambda m: f"{T('Total Revenue', 'sub', m)}*{A.y('dc_app', m)}*{A.s('dc_appfee')}",
        "d_ai": lambda m: f"{aq('ai_cr', m)}*{A.y('dc_ai', m)}",
        "d_host": lambda m: f"{aq('free', m)}*{A.y('dc_hf', m)}+{aq('paid', m)}*{A.y('dc_hp', m)}",
        "d_data": lambda m: f"({aq('a_inst', m)}+{aq('a_ic', m)})*{A.y('dc_data', m)}",
        "d_sup": lambda m: f"{aq('paid', m)}*{A.y('dc_sup', m)}",
        "d_val": lambda m: f"{rs('n_val', m)}*{A.s('dc_val')}",
        "d_wl": lambda m: f"({rs('r_wl', m)}+{rs('r_spv', m)})*{A.s('dc_wl')}",
        "d_psf": lambda m: f"{rs('r_fs', m)}*{A.y('ps_f', m)}*{A.s('ps_rate')}",
        "d_psi": lambda m: f"{rs('r_is', m)}*{A.y('ps_i', m)}*{A.s('ps_rate')}",
    }
    for k, txt in DIRECT:
        t.line(k, txt, fx[k], USD)
    t.line("direct", "Total direct cost", lambda m: "+".join(R(k, m) for k, _ in DIRECT), USD, bold=True)
    t.line("gp", "Gross profit", lambda m: f"{T('Total Revenue', 'rev', m)}-{R('direct', m)}", USD, bold=True)
    t.line("gm", "Gross margin", lambda m: f"IFERROR({R('gp', m)}/{T('Total Revenue', 'rev', m)},0)", PCT, total=None)
    for y in range(1, 6):
        c = put(ws, f"{ycol(y)}{g['gm']}", f"=IFERROR({ycol(y)}{g['gp']}/'Total Revenue'!{ycol(y)}{tok('Total Revenue', 'rev')},0)", PCT, bold=True, size=8.6)
        c.fill = fill(YFILL)
    t.blank()
    t.section("OPERATING COST")
    ox = {
        "o_pay": lambda m: pr("payroll", m),
        "o_comm": lambda m: f"{rs('r_sales', m)}*{A.y('comm', m)}",
        "o_onl": lambda m: aq("on_sp", m),
        "o_off": lambda m: aq("off_sp", m),
        "o_brand": lambda m: A.y("ox_brand", m),
        "o_inc": lambda m: A.y("ox_inc", m),
        "o_onb": lambda m: f"{aq('newp', m)}*{A.y('ox_onb', m)}",
        "o_pros": lambda m: A.y("ox_pros", m),
        "o_trav": lambda m: f"{pr('comm_heads', m)}*{A.y('ox_trav', m)}",
        "o_desk": lambda m: f"{pr('heads', m)}*{A.y('ox_desk', m)}",
        "o_rent": lambda m: A.y("ox_rent", m),
        "o_util": lambda m: f"{pr('heads', m)}*{A.y('ox_util', m)}",
        "o_soft": lambda m: f"{pr('heads', m)}*{A.y('ox_soft', m)}",
        "o_cloud": lambda m: A.y("ox_cloud", m),
        "o_crm": lambda m: A.y("ox_crm", m),
        "o_sec": lambda m: A.y("ox_sec", m),
        "o_rec": lambda m: f"{pr('hires', m)}*{A.y('ox_rec', m)}",
        "o_train": lambda m: f"{pr('heads', m)}*{A.y('ox_train', m)}/12",
        "o_fin": lambda m: A.y("ox_fin", m),
        "o_reg": lambda m: A.y("ox_reg", m),
        "o_ins": lambda m: A.y("ox_ins", m),
    }
    for k, txt, _ in OPEX:
        t.line(k, txt, ox[k], USD)
    t.line("o_cont", "Contingency", lambda m: f"({'+'.join(R(k, m) for k, _, _ in OPEX)})*{A.y('ox_cont', m)}", USD)
    t.line("opex", "Operating cost before depreciation", lambda m: f"{'+'.join(R(k, m) for k, _, _ in OPEX)}+{R('o_cont', m)}", USD, bold=True)
    t.line("da", "Depreciation and amortization", lambda m: T("Depreciation and Amortization", "da", m), USD)
    t.line("opex_t", "Total operating cost", lambda m: f"{R('opex', m)}+{R('da', m)}", USD, bold=True)
    t.blank()
    t.section("RESULT")
    t.line("tot", "Total expenses, direct and operating", lambda m: f"{R('direct', m)}+{R('opex_t', m)}", USD, bold=True)
    t.line("ebitda", "EBITDA", lambda m: f"{R('gp', m)}-{R('opex', m)}", USD, bold=True)
    t.line("ebit", "EBIT, operating profit", lambda m: f"{R('ebitda', m)}-{R('da', m)}", USD, bold=True)
    t.line("cashx", "Cash operating cost excluding payroll", lambda m: f"{R('opex', m)}-{R('o_pay', m)}", USD)
    t.line("cashcost", "Total cash cost, direct and operating, before capital spend", lambda m: f"{R('direct', m)}+{R('opex', m)}", USD, bold=True)
    t.blank()
    t.section("CATEGORIES AND USE OF FUNDS BUCKETS")
    cats = ["People", "Sales and marketing", "Technology", "General and administrative"]
    for cat in cats:
        ks = [k for k, _, c in OPEX if c == cat]
        t.line(f"cat_{cat}", cat, lambda m, ks=ks: "+".join(R(k, m) for k in ks), USD)
    t.line("cat_direct", "Direct cost of delivery", lambda m: R("direct", m), USD)
    t.line("cat_cont", "Contingency", lambda m: R("o_cont", m), USD)
    fp = lambda fn, m: T("Payroll", "fp_" + fn, m)
    t.line("uf_prod", "Product and AI engineering",
           lambda m: f"{fp('Technology', m)}+{fp('Product', m)}+{R('o_soft', m)}+{R('o_sec', m)}", USD)
    t.line("uf_grow", "Community, growth and sales",
           lambda m: f"{fp('Sales', m)}+{fp('Marketing', m)}+{fp('Community and Partnerships', m)}+{fp('Customer', m)}+{R('cat_Sales and marketing', m)}", USD)
    t.line("uf_ai", "AI agents, cloud and delivery", lambda m: f"{R('direct', m)}+{R('o_cloud', m)}+{R('o_crm', m)}", USD)
    t.line("uf_ops", "Leadership, operations and legal",
           lambda m: f"{fp('Leadership', m)}+{fp('Operations', m)}+{fp('Finance and Legal', m)}+{R('cat_General and administrative', m)}+{R('o_rec', m)}+{R('o_train', m)}+{R('o_cont', m)}", USD)
    t.line("uf_chk", "Check, buckets against total cash cost",
           lambda m: f"ROUND({R('uf_prod', m)}+{R('uf_grow', m)}+{R('uf_ai', m)}+{R('uf_ops', m)}-{R('cashcost', m)},2)", USD, kind="check")
    t.blank()
    # The first twelve months in full
    section(ws, t.r, "THE FIRST TWELVE MONTHS IN FULL, WHAT THE PRE-SEED HAS TO PAY FOR")
    t.r += 1
    note(ws, t.r, "Every expense line above, totaled over months one to twelve. This is the figure the ask on Funding and Use of Funds is built from.")
    t.r += 1
    hdr(ws, t.r, ["Expense line", "Category", "Year 1 total, USD", "Share of year 1 spend", "Monthly average"])
    t.r += 1
    first = t.r
    lines = [(k, txt, "Direct cost of delivery") for k, txt in DIRECT] + [(k, txt, c) for k, txt, c in OPEX] + [("o_cont", "Contingency", "General and administrative")]
    tot_row = first + len(lines) + 1
    for k, txt, cat in lines:
        label(ws, t.r, txt)
        label(ws, t.r, cat, col=2, size=8, color=GREY)
        put(ws, f"C{t.r}", f"=B{g[k]}", USD)
        put(ws, f"D{t.r}", f"=IFERROR(C{t.r}/$C${tot_row},0)", PCT)
        put(ws, f"E{t.r}", f"=C{t.r}/12", USD)
        t.r += 1
    label(ws, t.r, "Depreciation and amortization, non cash")
    label(ws, t.r, "Non cash", col=2, size=8, color=GREY)
    put(ws, f"C{t.r}", f"=B{g['da']}", USD)
    t.r += 1
    label(ws, t.r, "Total year one expense, produced by this sheet", bold=True)
    put(ws, f"C{t.r}", f"=SUM(C{first}:C{t.r - 1})", USD, bold=True)
    put(ws, f"D{t.r}", f"=IFERROR(C{t.r}/$C${tot_row},0)", PCT)
    put(ws, f"E{t.r}", f"=C{t.r}/12", USD)
    g["y1_tot"] = t.r
    t.r += 1
    label(ws, t.r, "Of which cash expense")
    put(ws, f"C{t.r}", f"=C{t.r - 1}-C{t.r - 2}", USD)
    g["y1_cash"] = t.r
    t.r += 1
    label(ws, t.r, "Capital expenditure paid in cash in year one")
    put(ws, f"C{t.r}", f"='Capital Expenditure'!B{tok('Capital Expenditure', 'cash')}", USD)
    t.r += 1
    label(ws, t.r, "Total cash out in year one, expense and capital", bold=True)
    put(ws, f"C{t.r}", f"=C{t.r - 2}+C{t.r - 1}", USD, bold=True)
    g["y1_out"] = t.r


def build_income(ws, A, REG):
    title(ws, "Income Statement", "Five years to 31 December.")
    a = Ann(ws, REG)
    TRv = lambda k, y: TY("Total Revenue", k, y)
    EX = lambda k, y: TY("Expenses", k, y)
    g = a.reg
    R = lambda k, y: f"{YCOLS[y - 1]}{tok(ws.title, k)}"
    a.section("STATEMENT OF PROFIT OR LOSS, USD")
    a.line("rev", "Total revenue", lambda y: TRv("rev", y), bold=True)
    a.line("gr", "Annual growth", lambda y: "0" if y == 1 else f"IFERROR({R('rev', y)}/{YCOLS[y - 2]}{tok(ws.title, 'rev')}-1,0)", PCT)
    for k, txt in [("fs", "Founder subscriptions"), ("is", "Investor subscriptions"), ("svc", "Add-ons and services"), ("plat", "Platform and partner")]:
        a.line(k, txt, lambda y, k=k: TRv(k, y), indent=1)
    a.blank()
    a.line("cor", "Cost of revenue", lambda y: EX("direct", y))
    a.line("gp", "Gross profit", lambda y: f"{R('rev', y)}-{R('cor', y)}", bold=True)
    a.line("gm", "Gross profit margin", lambda y: f"IFERROR({R('gp', y)}/{R('rev', y)},0)", PCT)
    a.blank()
    label(ws, a.r, "Operating expenses", bold=True)
    a.r += 1
    for k, txt, _ in OPEX:
        a.line(k, txt, lambda y, k=k: EX(k, y), indent=1)
    a.line("o_cont", "Contingency", lambda y: EX("o_cont", y), indent=1)
    a.line("opex", "Total operating expenses before depreciation", lambda y: EX("opex", y), bold=True)
    a.blank()
    a.line("ebitda", "EBITDA", lambda y: f"{R('gp', y)}-{R('opex', y)}", bold=True)
    a.line("ebitdam", "EBITDA margin", lambda y: f"IFERROR({R('ebitda', y)}/{R('rev', y)},0)", PCT)
    a.line("da", "Depreciation and amortization", lambda y: EX("da", y))
    a.line("ebit", "EBIT, operating profit", lambda y: f"{R('ebitda', y)}-{R('da', y)}", bold=True)
    a.blank()
    a.line("pbt", "Profit before tax", lambda y: R("ebit", y))
    a.line("tlo", "Tax losses carried forward, opening", lambda y: A.s("tax_loss") if y == 1 else f"{YCOLS[y - 2]}{tok(ws.title, 'tlc')}")
    a.line("tlc", "Tax losses carried forward, closing", lambda y: f"MAX(0,{R('tlo', y)}-MAX(0,{R('pbt', y)}))+MAX(0,-{R('pbt', y)})")
    a.line("txb", "Taxable profit", lambda y: f"MAX(0,{R('pbt', y)}-{R('tlo', y)})")
    a.line("tax", "Corporate income tax", lambda y: f"{R('txb', y)}*{A.s('tax')}")
    a.line("np", "Net profit for the year", lambda y: f"{R('pbt', y)}-{R('tax', y)}", bold=True)
    a.line("npm", "Net profit margin", lambda y: f"IFERROR({R('np', y)}/{R('rev', y)},0)", PCT)
    a.blank()
    a.line("chk", "Check, EBITDA against the Expenses sheet", lambda y: f"ROUND({R('ebitda', y)}-{EX('ebitda', y)},2)", kind="check")
    ws.freeze_panes = "C4"


def build_cashflow(ws, A, REG):
    title(ws, "Cash Flow Statement", "Monthly working, then the annual statement. The pre-seed, seed and Series A amounts come from Funding and Use of Funds, where the model sizes them.")
    set_time_widths(ws, 56)
    t = TS(ws, REG, 3)
    g = REG[ws.title]
    label(ws, 3, "Month index", size=8, color=GREY)
    for m in range(1, NM + 1):
        put(ws, f"{mcol(m)}3", m, NUM, kind="note")
    g["mi"] = 3
    t.r = 4
    R = lambda k, m: f"{mcol(m)}{tok(ws.title, k)}"
    P = lambda k, m, op="0": op if m == 1 else f"{mcol(m - 1)}{tok(ws.title, k)}"
    rs = lambda k, m: T("Revenue Streams", k, m)
    IS = lambda k, y: f"'Income Statement'!${YCOLS[y - 1]}${tok('Income Statement', k)}"
    t.section("OPERATING ACTIVITIES")
    t.line("ebit", "EBIT, operating profit", lambda m: T("Expenses", "ebit", m), USD)
    t.line("tax", "Corporate income tax charge", lambda m: f"{IS('tax', yr(m))}/12", USD)
    t.line("np", "Net profit", lambda m: f"{R('ebit', m)}-{R('tax', m)}", USD, bold=True)
    t.line("da", "Add back depreciation and amortization", lambda m: T("Expenses", "da", m), USD)
    t.blank()
    t.section("WORKING CAPITAL BALANCES AT MONTH END")
    t.line("ar", "Trade receivables", lambda m: f"{rs('r_self', m)}*{A.s('dso_self')}/30+{rs('r_sales', m)}*{A.s('dso_sales')}/30+({rs('r_svc', m)}+{rs('r_plat', m)})*{A.s('dso_add')}/30", USD, total="end")
    t.line("ap", "Trade and other payables", lambda m: f"({T('Expenses', 'direct', m)}+{T('Expenses', 'cashx', m)})*{A.s('dpo')}/30", USD, total="end")
    t.line("accp", "Accrued payroll", lambda m: f"{T('Payroll', 'payroll', m)}*{A.s('dacc')}/30", USD, total="end")
    t.line("defr", "Deferred revenue on annual plans", lambda m: f"{rs('r_ann', m)}*{A.s('prepaid')}", USD, total="end")
    t.line("taxpd", "Corporate income tax paid", lambda m: f"IF(AND({miy(m)}={A.s('tax_m')},{yr(m)}>1),{IS('tax', max(1, yr(m) - 1))},0)" if yr(m) > 1 else "0", USD)
    t.line("taxp", "Tax payable", lambda m: f"{P('taxp', m)}+{R('tax', m)}-{R('taxpd', m)}", USD, total="end")
    t.blank()
    t.section("CASH FLOW")
    t.line("d_ar", "(Increase) decrease in receivables", lambda m: f"-({R('ar', m)}-{P('ar', m)})", USD)
    t.line("d_ap", "Increase (decrease) in payables", lambda m: f"{R('ap', m)}-{P('ap', m)}", USD)
    t.line("d_acc", "Increase (decrease) in accrued payroll", lambda m: f"{R('accp', m)}-{P('accp', m)}", USD)
    t.line("d_def", "Increase (decrease) in deferred revenue", lambda m: f"{R('defr', m)}-{P('defr', m)}", USD)
    t.line("d_tax", "Increase (decrease) in tax payable", lambda m: f"{R('taxp', m)}-{P('taxp', m)}", USD)
    t.line("cfo", "Net cash from operating activities",
           lambda m: f"{R('np', m)}+{R('da', m)}+{R('d_ar', m)}+{R('d_ap', m)}+{R('d_acc', m)}+{R('d_def', m)}+{R('d_tax', m)}", USD, bold=True)
    t.line("capex", "Capital expenditure", lambda m: f"-{T('Capital Expenditure', 'cash', m)}", USD)
    t.line("cfi", "Net cash used in investing activities", lambda m: R("capex", m), USD, bold=True)
    t.line("fcf", "Free cash flow, before any funding", lambda m: f"{R('cfo', m)}+{R('cfi', m)}", USD, bold=True)
    t.line("cumfcf", "Cumulative free cash flow", lambda m: f"{P('cumfcf', m)}+{R('fcf', m)}", USD, total="end")
    FU = lambda k: f"'Funding and Use of Funds'!$C${tok('Funding and Use of Funds', k)}"
    t.line("ps", "Pre-seed raised", lambda m: f"IF({m}={A.s('ps_m')},{FU('ps_amt')},0)", USD)
    t.line("sd", "Seed round raised", lambda m: f"IF({m}={A.s('sd_m')},{FU('sd_amt')},0)", USD)
    t.line("sa", "Series A raised", lambda m: f"IF({m}={A.s('sa_m')},{FU('sa_amt')},0)", USD)
    t.line("cff", "Net cash from financing activities", lambda m: f"{R('ps', m)}+{R('sd', m)}+{R('sa', m)}", USD, bold=True)
    t.line("net", "Net movement in cash", lambda m: f"{R('cfo', m)}+{R('cfi', m)}+{R('cff', m)}", USD)
    t.line("c0", "Cash at the start of the month", lambda m: P("c1", m, A.s("op_cash")), USD, total=None)
    t.line("c1", "Cash at the end of the month", lambda m: f"{R('c0', m)}+{R('net', m)}", USD, total="end", bold=True)
    t.line("head", "Headroom against the minimum cash buffer", lambda m: f"{R('c1', m)}-{A.s('buffer')}", USD, total="min")
    t.line("psa", "Cash on the pre-seed alone, before the seed round", lambda m: f"{A.s('op_cash')}+IF({m}>={A.s('ps_m')},{FU('ps_amt')},0)+{R('cumfcf', m)}", USD, total=None)
    t.line("psmin", "Lowest that balance has been up to this month", lambda m: R("psa", m) if m == 1 else f"MIN({P('psmin', m)},{R('psa', m)})", USD, total=None)
    t.blank()
    # annual statement
    section(ws, t.r, "CASH FLOW STATEMENT, ANNUAL")
    t.r += 1
    hdr(ws, t.r, ["Line item", "", "Year 1, 2027", "Year 2, 2028", "Year 3, 2029", "Year 4, 2030", "Year 5, 2031"])
    t.r += 1
    for k, txt, bold in [("np", "Net profit for the year", False), ("da", "Depreciation and amortization", False), ("d_ar", "(Increase) decrease in receivables", False),
                         ("d_ap", "Increase (decrease) in payables", False), ("d_acc", "Increase (decrease) in accrued payroll", False),
                         ("d_def", "Increase (decrease) in deferred revenue", False), ("d_tax", "Increase (decrease) in tax payable", False),
                         ("cfo", "Net cash from operating activities", True), ("cfi", "Net cash used in investing activities", True),
                         ("cff", "Net cash from financing activities", True), ("net", "Net movement in cash", True)]:
        label(ws, t.r, txt, bold=bold)
        for y in range(1, 6):
            put(ws, f"{YCOLS[y - 1]}{t.r}", f"={ycol(y)}{tok(ws.title, k)}", USD, bold=bold)
        t.r += 1
    label(ws, t.r, "Cash at the end of the year", bold=True)
    for y in range(1, 6):
        put(ws, f"{YCOLS[y - 1]}{t.r}", f"={mcol(12 * y)}{tok(ws.title, 'c1')}", USD, bold=True)


def build_balance(ws, A, REG):
    title(ws, "Balance Sheet", "Five years, with the balance check that must read nil in every column.")
    a = Ann(ws, REG)
    R = lambda k, y: f"{YCOLS[y - 1]}{tok(ws.title, k)}"
    CF = lambda k, y: TE("Cash Flow Statement", k, y)
    DA = lambda k, y: TE("Depreciation and Amortization", k, y)
    a.section("STATEMENT OF FINANCIAL POSITION AT 31 DECEMBER, USD")
    a.line("cash", "Cash and cash equivalents", lambda y: CF("c1", y))
    a.line("ar", "Trade receivables", lambda y: CF("ar", y))
    a.line("ppe", "Property and equipment, net", lambda y: DA("ppe", y))
    a.line("int", "Intangible assets, net", lambda y: DA("int", y))
    a.line("ta", "Total assets", lambda y: f"SUM({YCOLS[y - 1]}{tok(ws.title, 'cash')}:{YCOLS[y - 1]}{tok(ws.title, 'int')})", bold=True)
    a.blank()
    a.line("ap", "Trade and other payables", lambda y: CF("ap", y))
    a.line("accp", "Accrued payroll", lambda y: CF("accp", y))
    a.line("defr", "Deferred revenue", lambda y: CF("defr", y))
    a.line("taxp", "Tax payable", lambda y: CF("taxp", y))
    a.line("tl", "Total liabilities", lambda y: f"SUM({YCOLS[y - 1]}{tok(ws.title, 'ap')}:{YCOLS[y - 1]}{tok(ws.title, 'taxp')})", bold=True)
    a.blank()
    a.line("sc", "Share capital, founders, pre-seed, seed and Series A",
           lambda y: f"{A.s('op_cash')}+{A.s('op_prod')}+" + "+".join(TY("Cash Flow Statement", "cff", k) for k in range(1, y + 1)))
    a.line("re", "Retained earnings", lambda y: "+".join(TA("Income Statement", "np", k) for k in range(1, y + 1)))
    a.line("te", "Total equity", lambda y: f"{R('sc', y)}+{R('re', y)}", bold=True)
    a.line("tle", "Total liabilities and equity", lambda y: f"{R('tl', y)}+{R('te', y)}", bold=True)
    a.blank()
    a.line("chk", "CHECK, total assets less liabilities and equity", lambda y: f"ROUND({R('ta', y)}-{R('tle', y)},2)", kind="check")


def build_indicators(ws, A, REG):
    title(ws, "Financial Indicators", "The numbers the business is run on, taken from the model rather than retyped.")
    a = Ann(ws, REG)
    R = lambda k, y: f"{YCOLS[y - 1]}{tok(ws.title, k)}"
    IS = lambda k, y: TA("Income Statement", k, y)
    AQe = lambda k, y: TE("Acquisitions", k, y)
    AQy = lambda k, y: TY("Acquisitions", k, y)
    a.section("GROWTH AND SCALE")
    a.line("rev", "Total revenue", lambda y: IS("rev", y), bold=True)
    a.line("gr", "Revenue growth", lambda y: IS("gr", y), PCT)
    a.line("arr", "ARR at year end", lambda y: TE("Total Revenue", "arr", y), bold=True)
    a.line("nnarr", "Net new ARR in the year", lambda y: R("arr", y) if y == 1 else f"{R('arr', y)}-{YCOLS[y - 2]}{tok(ws.title, 'arr')}")
    a.line("subsh", "Subscription share of revenue", lambda y: f"IFERROR({TY('Total Revenue', 'sub', y)}/{TY('Total Revenue', 'rev', y)},0)", PCT)
    a.line("invsh", "Investor side share of subscription revenue", lambda y: f"IFERROR({TY('Total Revenue', 'is', y)}/{TY('Total Revenue', 'sub', y)},0)", PCT)
    a.line("freg", "Registered founder workspaces at year end", lambda y: AQe("f_reg", y), NUM)
    a.line("ireg", "Registered investor accounts at year end", lambda y: AQe("i_reg", y), NUM)
    a.line("free", "Active free accounts at year end", lambda y: AQe("free", y), NUM)
    a.line("fpaid", "Paying founder accounts at year end", lambda y: AQe("f_paid", y), NUM)
    a.line("ipaid", "Paying investor accounts at year end", lambda y: AQe("i_paid", y), NUM)
    a.line("inst", "Of which Institutional and Custom investors", lambda y: f"{AQe('a_inst', y)}+{AQe('a_ic', y)}", NUM, indent=1)
    a.line("paid", "Paying accounts at year end", lambda y: AQe("paid", y), NUM, bold=True)
    a.line("newp", "New paying accounts in the year", lambda y: AQy("newp", y), NUM)
    a.line("heads", "Employees at year end", lambda y: TE("Payroll", "heads", y), NUM)
    a.line("rpe", "Revenue per employee", lambda y: f"IFERROR({R('rev', y)}/{R('heads', y)},0)")
    a.blank()
    a.section("PROFITABILITY")
    a.line("gp", "Gross profit", lambda y: IS("gp", y))
    a.line("gm", "Gross margin", lambda y: IS("gm", y), PCT)
    a.line("ebitda", "EBITDA", lambda y: IS("ebitda", y), bold=True)
    a.line("ebitdam", "EBITDA margin", lambda y: IS("ebitdam", y), PCT)
    a.line("np", "Net profit", lambda y: IS("np", y))
    a.line("npm", "Net margin", lambda y: IS("npm", y), PCT)
    a.line("texp", "Total expenses, direct and operating", lambda y: TY("Expenses", "tot", y))
    a.blank()
    a.section("UNIT ECONOMICS AND THE FUNNEL")
    sm = lambda y: (f"{TY('Acquisitions', 'mk_sp', y)}+{TY('Payroll', 'fp_Sales', y)}+{TY('Payroll', 'fp_Marketing', y)}+"
                    f"{TY('Payroll', 'fp_Community and Partnerships', y)}+{TY('Expenses', 'o_comm', y)}+{TY('Expenses', 'o_onb', y)}+{TY('Expenses', 'o_brand', y)}+{TY('Expenses', 'o_inc', y)}")
    a.line("smc", "Sales and marketing cost, fully loaded", sm)
    a.line("cac", "Blended cost to acquire a paying account, CAC", lambda y: f"IFERROR({R('smc', y)}/{R('newp', y)},0)")
    a.line("arpa", "Average subscription revenue per paying account per month", lambda y: f"IFERROR({TY('Total Revenue', 'sub', y)}/SUM({MR('Acquisitions', 'paid', y)}),0)", USD2)
    a.line("churn", "Blended monthly logo churn", lambda y: f"IFERROR({AQy('churn', y)}/SUM({MR('Acquisitions', 'paid', y)}),0)", PCT)
    a.line("ltv", "Lifetime gross profit of a paying account, LTV", lambda y: f"IFERROR({R('arpa', y)}*{R('gm', y)}/{R('churn', y)},0)")
    a.line("ltvcac", "LTV to CAC", lambda y: f"IFERROR({R('ltv', y)}/{R('cac', y)},0)", MULT)
    a.line("payb", "CAC payback, months", lambda y: f"IFERROR({R('cac', y)}/({R('arpa', y)}*{R('gm', y)}),0)", NUM1)
    a.line("f2p", "New paying accounts per new registration", lambda y: f"IFERROR({R('newp', y)}/{AQy('reg_new', y)},0)", PCT)
    a.line("cpr", "Marketing cost per registration", lambda y: f"IFERROR({TY('Acquisitions', 'mk_sp', y)}/{AQy('reg_new', y)},0)", USD2)
    a.line("burnm", "Burn multiple, net burn over net new ARR", lambda y: f"IF({R('fcf', y)}>=0,0,IFERROR(-{R('fcf', y)}/{R('nnarr', y)},0))", MULT)
    a.line("r40", "Rule of 40, growth plus EBITDA margin", lambda y: "0" if y == 1 else f"{R('gr', y)}+{R('ebitdam', y)}", PCT)
    a.blank()
    a.section("CASH")
    a.line("cash", "Cash at year end", lambda y: TE("Cash Flow Statement", "c1", y), bold=True)
    a.line("minc", "Lowest cash balance in the year", lambda y: f"MIN({MR('Cash Flow Statement', 'c1', y)})")
    a.line("cfo", "Net cash from operations", lambda y: TY("Cash Flow Statement", "cfo", y))
    a.line("fcf", "Free cash flow", lambda y: TY("Cash Flow Statement", "fcf", y))
    a.line("burn", "Average monthly burn or generation", lambda y: f"{R('fcf', y)}/12")
    a.line("runway", "Months of runway on year end cash", lambda y: f"IF({R('fcf', y)}>=0,99,IFERROR({R('cash', y)}/(-{R('fcf', y)}/12),0))", NUM1)


def build_funding(ws, A, REG):
    title(ws, "Funding and Use of Funds", "The ask, produced by the year one expense the model calculates, what it buys, and the runway it produces. Nothing on this sheet is typed.")
    a = Ann(ws, REG, a=72)
    ws.column_dimensions["D"].width = 14
    R = lambda k: f"$C${tok(ws.title, k)}"
    EXB = lambda k: f"Expenses!$B${tok('Expenses', k)}"
    a.section("1. THE PRE-SEED ASK, BUILT FROM YEAR ONE EXPENSES", "Year one cash cost, less the cash already in the company, plus a buffer of months, rounded up. Year one revenue is not counted: it is the cushion.", cols=("Year 1, USD", "Share"))
    first = a.r
    for k, txt, f_ in [("c_people", "People, payroll, recruitment and training", EXB("cat_People")),
                       ("c_sm", "Sales, marketing and community", EXB("cat_Sales and marketing")),
                       ("c_tech", "Technology and platform", EXB("cat_Technology")),
                       ("c_ga", "General and administrative", EXB("cat_General and administrative")),
                       ("c_dir", "Direct cost of delivery, AI inference, hosting, payments, partners", EXB("cat_direct")),
                       ("c_cont", "Contingency", EXB("cat_cont")),
                       ("c_capex", "Capital expenditure paid in cash, equipment and set up", f"'Capital Expenditure'!$B${tok('Capital Expenditure', 'cash')}")]:
        a.kv(k, txt, f"={f_}")
        put(ws, f"D{a.r - 1}", f"=IFERROR(C{a.r - 1}/{R('y1')},0)", PCT)
    a.kv("y1", "Total cash required in year one", f"=SUM(C{first}:C{a.r - 1})", bold=True)
    put(ws, f"D{a.r - 1}", f"=IFERROR(C{a.r - 1}/{R('y1')},0)", PCT)
    a.kv("y1chk", "Check, against the total cash out on the Expenses sheet", f"=ROUND({R('y1')}-Expenses!$C${tok('Expenses', 'y1_out')},2)", kind="check")
    a.kv("opc", "Less, cash already in the company at the start", f"=-{A.s('op_cash')}")
    a.kv("avgm", "Average monthly cash cost in year one", f"={R('y1')}/12")
    a.kv("bufm", "Buffer, months of year one cash cost held beyond month twelve", f"={A.s('ps_buf')}", NUM1)
    a.kv("buf", "Buffer amount", f"={R('avgm')}*{R('bufm')}")
    a.kv("gross", "Gross requirement", f"={R('y1')}+{R('opc')}+{R('buf')}", bold=True)
    a.kv("ps_amt", "THE PRE-SEED ASK, rounded up", f"=ROUNDUP({R('gross')}/{A.s('ps_round')},0)*{A.s('ps_round')}", bold=True)
    a.kv("ps_m", "Month the pre-seed lands", f"={A.s('ps_m')}", NUM)
    a.kv("ps_mo", "The ask expressed in months of year one cash cost", f"=IFERROR({R('ps_amt')}/{R('avgm')},0)", NUM1)
    a.kv("y1rev", "Revenue collected in year one, not counted in the ask", f"='Total Revenue'!$B${tok('Total Revenue', 'rev')}")
    a.kv("y1burn", "Net cash consumed in year one, after that revenue", f"=-'Cash Flow Statement'!$B${tok('Cash Flow Statement', 'fcf')}")
    a.blank()
    a.section("2. USE OF FUNDS", "The year one cash cost split four ways, and the ask allocated in the same proportions.", cols=("Year 1 cost", "Share", "Of the ask"))
    ws.column_dimensions["E"].width = 15
    uf = [("u_prod", "Product and AI engineering", "uf_prod"), ("u_grow", "Community, growth and sales", "uf_grow"),
          ("u_ai", "AI agents, cloud and delivery", "uf_ai"), ("u_ops", "Leadership, operations, legal and set up", "uf_ops")]
    f0 = a.r
    for k, txt, ek in uf:
        extra = f"+'Capital Expenditure'!$B${tok('Capital Expenditure', 'cash')}" if k == "u_ops" else ""
        a.kv(k, txt, f"={EXB(ek)}{extra}")
        put(ws, f"D{a.r - 1}", f"=IFERROR(C{a.r - 1}/SUM($C${f0}:$C${f0 + 3}),0)", PCT)
        put(ws, f"E{a.r - 1}", f"=D{a.r - 1}*{R('ps_amt')}", USD)
    a.kv("u_tot", "Total", f"=SUM(C{f0}:C{f0 + 3})", bold=True)
    put(ws, f"D{a.r - 1}", f"=SUM(D{f0}:D{f0 + 3})", PCT)
    put(ws, f"E{a.r - 1}", f"=SUM(E{f0}:E{f0 + 3})", USD, bold=True)
    a.blank()
    CF = "'Cash Flow Statement'"
    idx = f"{CF}!$C$3:$BN$3"
    fcf = f"{CF}!$C${tok('Cash Flow Statement', 'fcf')}:$BN${tok('Cash Flow Statement', 'fcf')}"
    a.section("3. WHAT THE PRE-SEED BUYS", cols=("Value",))
    a.kv("run", "Months the pre-seed funds on its own, counted month by month", f"=COUNTIF({MR('Cash Flow Statement', 'psmin')},\">=0\")", NUM)
    a.kv("runb", "Months before the minimum cash buffer is touched, pre-seed alone", f"=COUNTIF({MR('Cash Flow Statement', 'psmin')},\">=\"&{A.s('buffer')})", NUM)
    a.kv("c12", "Cash at the end of year one", f"={CF}!{mcol(12)}{tok('Cash Flow Statement', 'c1')}")
    a.kv("ebm", "Month the business first turns EBITDA positive", f"='BEP Analysis'!$C${tok('BEP Analysis', 'm_ebitda')}", "General")
    a.blank()
    a.section("4. THE FOLLOW ON ROUNDS, SIZED BY THE MODEL", "Each round is sized to fund the net cash need over its window, plus the minimum buffer, less the cash already held when it lands. A round the business does not need sizes to nil.", cols=("Value",))
    a.kv("sd_m", "Seed round, month it lands", f"={A.s('sd_m')}", NUM)
    a.kv("sd_n", "Months of need it is sized to fund", f"={A.s('sd_n')}", NUM)
    a.kv("sd_cb", "Cash held the month before it lands", f"={A.s('op_cash')}+{R('ps_amt')}+SUMPRODUCT(({idx}>=1)*({idx}<={R('sd_m')}-1)*{fcf})")
    a.kv("sd_need", "Net cash consumed across the window", f"=-SUMPRODUCT(({idx}>={R('sd_m')})*({idx}<=MIN(60,{R('sd_m')}+{R('sd_n')}-1))*{fcf})")
    a.kv("sd_amt", "SEED ROUND, sized by the model", f"=MAX(0,ROUNDUP(({R('sd_need')}+{A.s('buffer')}-{R('sd_cb')})/{A.s('sd_round')},0)*{A.s('sd_round')})", bold=True)
    a.kv("sa_m", "Series A, month it lands", f"={A.s('sa_m')}", NUM)
    a.kv("sa_n", "Months of need it is sized to fund, capped at month 60", f"={A.s('sa_n')}", NUM)
    a.kv("sa_cb", "Cash held the month before it lands", f"={A.s('op_cash')}+{R('ps_amt')}+{R('sd_amt')}+SUMPRODUCT(({idx}>=1)*({idx}<={R('sa_m')}-1)*{fcf})")
    a.kv("sa_need", "Net cash consumed across the window", f"=-SUMPRODUCT(({idx}>={R('sa_m')})*({idx}<=MIN(60,{R('sa_m')}+{R('sa_n')}-1))*{fcf})")
    a.kv("sa_amt", "SERIES A, sized by the model", f"=MAX(0,ROUNDUP(({R('sa_need')}+{A.s('buffer')}-{R('sa_cb')})/{A.s('sa_round')},0)*{A.s('sa_round')})", bold=True)
    a.kv("raised", "Total external capital across the three rounds", f"={R('ps_amt')}+{R('sd_amt')}+{R('sa_amt')}", bold=True)
    a.kv("lowc", "Lowest cash balance across the five years", f"=MIN({MR('Cash Flow Statement', 'c1')})")
    a.kv("more", "Further capital required to hold the buffer", f"=MAX(0,{A.s('buffer')}-{R('lowc')})")
    a.blank()
    a.section("5. THE MILESTONES THE PRE-SEED IS SIZED AGAINST", cols=("Value",))
    AQe = lambda k, y: TE("Acquisitions", k, y)
    a.kv("ms1", "Paid plans live, Pro, Team and Angel", "Month 2", "@")
    a.kv("ms2", "Institutional plan live, first demos converting", "Month 4", "@")
    a.kv("ms3", "Qatar opened, Doha partnerships manager and entity in place", "Month 4", "@")
    a.kv("ms3b", "Saudi Arabia opened founder led; head of institutional sales hired in Doha", "Month 10", "@")
    a.kv("ms4", "Paying founder accounts at the end of year one", f"={AQe('f_paid', 1)}", NUM)
    a.kv("ms5", "Paying investor accounts at the end of year one", f"={AQe('i_paid', 1)}", NUM)
    a.kv("ms6", "Registered accounts at the end of year one, both sides", f"={AQe('reg', 1)}", NUM)
    a.kv("ms7", "ARR at the end of year one", f"={TE('Total Revenue', 'arr', 1)}")
    a.kv("ms8", "ARR at the end of year two, what the seed round is raised on", f"={TE('Total Revenue', 'arr', 2)}")
