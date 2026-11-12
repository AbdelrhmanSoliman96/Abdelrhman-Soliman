"""Analysis and front sheets: BEP, PB, Sensitivity, Stress Test, Exit, Valuation, Summary, Market Research, Cover, Actuals, dividers."""
from xl import *
from model_output import Ann, T, TY, TE, TA, TC, MR, YCOLS

FU = "Funding and Use of Funds"


def fu(k):
    return f"'{FU}'!$C${tok(FU, k)}"


def build_bep(ws, A, REG):
    title(ws, "Break Even Analysis", "Break even revenue, and the month the business turns.")
    a = Ann(ws, REG)
    R = lambda k, y: f"{YCOLS[y - 1]}{tok(ws.title, k)}"
    a.section("ANNUAL BREAK EVEN")
    a.line("rev", "Revenue", lambda y: TY("Total Revenue", "rev", y))
    a.line("vc", "Variable cost of delivery", lambda y: TY("Expenses", "direct", y))
    a.line("cm", "Contribution", lambda y: f"{R('rev', y)}-{R('vc', y)}")
    a.line("cmp", "Contribution margin", lambda y: f"IFERROR({R('cm', y)}/{R('rev', y)},0)", PCT)
    a.line("fc", "Fixed operating cost, including depreciation", lambda y: TY("Expenses", "opex_t", y))
    a.line("ber", "Break even revenue", lambda y: f"IFERROR({R('fc', y)}/{R('cmp', y)},0)", bold=True)
    a.line("berm", "Break even revenue per month", lambda y: f"{R('ber', y)}/12")
    a.line("mos", "Margin of safety", lambda y: f"IFERROR(({R('rev', y)}-{R('ber', y)})/{R('rev', y)},0)", PCT)
    a.line("bea", "Break even in paying accounts, at the year's average revenue per account", lambda y: f"IFERROR({R('berm', y)}/{TA('Financial Indicators', 'arpa', y)},0)", NUM)
    a.line("held", "Paying accounts actually held at year end", lambda y: TE("Acquisitions", "paid", y), NUM)
    a.blank()
    # monthly working
    set_time_widths(ws, 58, group=False)
    ws.freeze_panes = None
    for c in YCOLS:
        ws.column_dimensions[c].width = 15
    t = TS(ws, REG, a.r)
    t.section("THE MONTH IT TURNS, WORKING")
    t.line("w1", "First month with positive EBITDA", lambda m: f"IF({T('Expenses', 'ebitda', m)}>0,{m},9999)", NUM, total="min")
    t.line("w2", "First month with positive operating cash flow", lambda m: f"IF({T('Cash Flow Statement', 'cfo', m)}>0,{m},9999)", NUM, total="min")
    t.line("w3", "Month of the lowest cash balance", lambda m: f"IF({T('Cash Flow Statement', 'c1', m)}=MIN({MR('Cash Flow Statement', 'c1')}),{m},9999)", NUM, total="min")
    t.line("w4", "First month cumulative free cash flow turns positive", lambda m: f"IF({T('Cash Flow Statement', 'cumfcf', m)}>0,{m},9999)", NUM, total="min")
    a.r = t.r + 1
    a.section("THE ANSWER", cols=("Month",))
    for k, w, txt in [("m_ebitda", "w1", "First month with positive EBITDA"), ("m_cfo", "w2", "First month with positive operating cash flow"),
                      ("m_low", "w3", "Month of the lowest cash balance"), ("m_cum", "w4", "First month cumulative free cash flow turns positive")]:
        row = f"$C${tok(ws.title, w)}:$BN${tok(ws.title, w)}"
        a.kv(k, txt, f"=IF(MIN({row})=9999,\"beyond year five\",MIN({row}))", "General", bold=(k == "m_ebitda"))
    a.blank()
    a.section("HOW MUCH HEADROOM THE YEAR TWO BREAK EVEN HAS", cols=("Value",))
    a.kv("g1", "EBITDA in month thirty six as the plan stands", f"=Expenses!{mcol(36)}{tok('Expenses', 'ebitda')}")
    a.kv("g2", "The gap to close", f"=-MIN(0,$C${tok(ws.title, 'g1')})")
    a.kv("g3", "Extra revenue in that month that would close it", f"=IFERROR($C${tok(ws.title, 'g2')}/$E${tok(ws.title, 'cmp')},0)")
    a.kv("g4", "As a share of the revenue that month produces", f"=IFERROR($C${tok(ws.title, 'g3')}/'Total Revenue'!{mcol(36)}{tok('Total Revenue', 'rev')},0)", PCT)
    a.kv("g5", "Or, as a cut in that month's operating cost", f"=IFERROR($C${tok(ws.title, 'g2')}/Expenses!{mcol(36)}{tok('Expenses', 'opex')},0)", PCT)


def build_pb(ws, A, REG):
    title(ws, "Payback Analysis", "When the capital comes back, base and flexed.")
    a = Ann(ws, REG)
    R = lambda k: f"$C${tok(ws.title, k)}"
    a.section("CAPITAL IN", cols=("USD",))
    a.kv("k0", "Founder capital at inception, cash", f"={A.s('op_cash')}")
    a.kv("k1", "Pre-seed, sized by the model", f"={fu('ps_amt')}")
    a.kv("k2", "Seed round, sized by the model", f"={fu('sd_amt')}")
    a.kv("k3", "Series A, sized by the model", f"={fu('sa_amt')}")
    a.kv("kt", "Total capital invested", f"=SUM(C{a.r - 4}:C{a.r - 1})", bold=True)
    a.blank()
    a.section("CASH RETURNED, BASE CASE")
    Rr = lambda k, y: f"{YCOLS[y - 1]}{tok(ws.title, k)}"
    a.line("fcf", "Free cash flow in the year", lambda y: TA("Financial Indicators", "fcf", y))
    a.line("cum", "Cumulative free cash flow", lambda y: Rr("fcf", y) if y == 1 else f"{YCOLS[y - 2]}{tok(ws.title, 'cum')}+{Rr('fcf', y)}")
    a.line("rec", "Capital recovered", lambda y: f"IFERROR(MAX(0,{Rr('cum', y)})/{R('kt')},0)", PCT)
    a.line("out", "Capital still outstanding", lambda y: f"MAX(0,{R('kt')}-MAX(0,{Rr('cum', y)}))")
    a.blank()
    t = TS(ws, REG, a.r)
    set_time_widths(ws, 58, group=False)
    ws.freeze_panes = None
    for c in YCOLS:
        ws.column_dimensions[c].width = 15
    t.section("PAYBACK, WORKING")
    t.line("pw", "Month cumulative free cash flow covers all capital invested",
           lambda m: f"IF({T('Cash Flow Statement', 'cumfcf', m)}>={R('kt')},{m},9999)", NUM, total="min")
    a.r = t.r + 1
    a.section("THE ANSWER", cols=("Value",))
    row = f"$C${tok(ws.title, 'pw')}:$BN${tok(ws.title, 'pw')}"
    a.kv("pb", "Months to repay all capital invested", f"=IF(MIN({row})=9999,\"beyond year five, returned at exit\",MIN({row}))", "General", bold=True)
    a.blank()
    a.section("WHAT YEAR FIVE IS SENSITIVE TO", "Volume flexes revenue and direct cost together; the operating base is held.", cols=("Volume", "Y5 revenue", "Y5 EBITDA"))
    for v in [0.6, 0.75, 0.9, 1.0, 1.1, 1.25]:
        label(ws, a.r, f"Volume at {int(v * 100)} per cent of plan")
        put(ws, f"C{a.r}", v, PCT, kind="input")
        put(ws, f"D{a.r}", f"='Total Revenue'!BB{tok('Total Revenue', 'rev')}*C{a.r}", USD)
        put(ws, f"E{a.r}", f"=D{a.r}-Expenses!BB{tok('Expenses', 'direct')}*C{a.r}-Expenses!BB{tok('Expenses', 'opex')}", USD)
        a.r += 1


def build_sens(ws, A, REG):
    title(ws, "Sensitivity Analysis", "Three two way grids on the year five EBITDA.")
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 12
    for c in "CDEFG":
        ws.column_dimensions[c].width = 15
    rev, dirc, opx = (f"'Total Revenue'!BB{tok('Total Revenue', 'rev')}", f"Expenses!BB{tok('Expenses', 'direct')}", f"Expenses!BB{tok('Expenses', 'opex')}")
    fs, is_ = f"'Total Revenue'!BB{tok('Total Revenue', 'fs')}", f"'Total Revenue'!BB{tok('Total Revenue', 'is')}"
    r = 4
    grids = [
        ("YEAR FIVE EBITDA, VOLUME AGAINST PRICE", "Rows flex paying accounts, columns flex price. Direct cost moves with volume, not price.",
         "Volume change", [-0.3, -0.15, 0, 0.15, 0.3], [-0.2, -0.1, 0, 0.1, 0.2],
         lambda rr, cc: f"={rev}*(1+$B{rr})*(1+{cc})-{dirc}*(1+$B{rr})-{opx}"),
        ("YEAR FIVE EBITDA, VOLUME AGAINST OPERATING COST", "Columns flex the fixed operating base, the cost of holding the team.",
         "Volume change", [-0.3, -0.15, 0, 0.15, 0.3], [-0.15, -0.075, 0, 0.075, 0.15],
         lambda rr, cc: f"={rev}*(1+$B{rr})-{dirc}*(1+$B{rr})-{opx}*(1+{cc})"),
        ("YEAR FIVE EBITDA, FOUNDER SIDE AGAINST INVESTOR SIDE", "The two halves of the shared record. Rows flex founder subscription revenue, columns investor subscription revenue.",
         "Founder side change", [-0.4, -0.2, 0, 0.2, 0.4], [-0.4, -0.2, 0, 0.2, 0.4],
         lambda rr, cc: f"=({rev}+{fs}*$B{rr}+{is_}*{cc})-{dirc}*IFERROR(({rev}+{fs}*$B{rr}+{is_}*{cc})/{rev},1)-{opx}"),
    ]
    for ttl, sub, rl, rows, cols, fn in grids:
        section(ws, r, ttl, 7)
        note(ws, r + 1, sub)
        r += 2
        label(ws, r, "Change in", size=8, color=GREY)
        for j, cv in enumerate(cols):
            put(ws, f"{'CDEFG'[j]}{r}", cv, PCT, kind="input")
        hr = r
        r += 1
        for rv in rows:
            label(ws, r, rl)
            put(ws, f"B{r}", rv, PCT, kind="input")
            for j in range(5):
                put(ws, f"{'CDEFG'[j]}{r}", fn(r, f"{'CDEFG'[j]}${hr}"), USD)
            r += 1
        r += 1
    REG.setdefault(ws.title, {})


def build_stress(ws, A, REG):
    title(ws, "Stress Testing", "Four scenarios on volume, price and operating cost, and whether the capital raised carries each one.")
    a = Ann(ws, REG)
    ws.column_dimensions["H"].width = 22
    a.section("SCENARIO LEVERS", cols=None)
    hdr(ws, a.r, ["Scenario", "", "Volume", "Price", "Operating cost"])
    a.r += 1
    sc = [("Base case", 1, 1, 1), ("Upside", 1.25, 1.05, 1.03), ("Downside", 0.7, 0.9, 0.95), ("Severe", 0.45, 0.8, 0.85)]
    lever_rows = {}
    for nm, v, p, o in sc:
        label(ws, a.r, nm)
        put(ws, f"C{a.r}", v, PCT, kind="input")
        put(ws, f"D{a.r}", p, PCT, kind="input")
        put(ws, f"E{a.r}", o, PCT, kind="input")
        lever_rows[nm] = a.r
        a.r += 1
    note(ws, a.r, "Downside and severe assume management cuts the operating base in response; the cut is the operating cost lever.")
    a.r += 2
    rev = lambda y: TY("Total Revenue", "rev", y)
    dirc = lambda y: TY("Expenses", "direct", y)
    opx = lambda y: TY("Expenses", "opex", y)
    a.section("REVENUE UNDER STRESS")
    for nm, *_ in sc:
        lr = lever_rows[nm]
        a.line(f"rv_{nm}", nm, lambda y, lr=lr: f"{rev(y)}*$C${lr}*$D${lr}")
    a.blank()
    a.section("EBITDA UNDER STRESS")
    for nm, *_ in sc:
        lr = lever_rows[nm]
        a.line(f"eb_{nm}", nm, lambda y, lr=lr: f"{rev(y)}*$C${lr}*$D${lr}-{dirc(y)}*$C${lr}-{opx(y)}*$E${lr}")
    a.blank()
    a.section("FREE CASH FLOW UNDER STRESS", "Base case free cash flow, moved by the change in EBITDA each scenario produces.")
    base = lambda y: f"{YCOLS[y - 1]}{tok(ws.title, 'eb_Base case')}"
    for nm, *_ in sc:
        a.line(f"fc_{nm}", nm, lambda y, nm=nm: f"{TA('Financial Indicators', 'fcf', y)}+{YCOLS[y - 1]}{tok(ws.title, 'eb_' + nm)}-{base(y)}")
    a.blank()
    a.section("CASH AND WHAT IT WOULD TAKE TO SURVIVE", cols=None)
    hdr(ws, a.r, ["Scenario", "", "Capital available", "Five year free cash flow", "Lowest cumulative free cash flow", "Capital left at the low point", "Survives on the capital raised"])
    a.r += 1
    for nm, *_ in sc:
        label(ws, a.r, nm)
        put(ws, f"C{a.r}", f"={A.s('op_cash')}+{fu('raised')}", USD)
        er = tok(ws.title, f"fc_{nm}")
        put(ws, f"D{a.r}", f"=SUM(C{er}:G{er})", USD)
        put(ws, f"E{a.r}", f"=MIN(C{er},C{er}+D{er},C{er}+D{er}+E{er},C{er}+D{er}+E{er}+F{er},SUM(C{er}:G{er}))", USD)
        put(ws, f"F{a.r}", f"=C{a.r}+MIN(0,E{a.r})", USD)
        put(ws, f"G{a.r}", f"=IF(F{a.r}>=0,\"Yes\",\"No, needs \"&TEXT(-F{a.r},\"$#,##0\"))", "@")
        a.r += 1
    note(ws, a.r, "Measured on year end balances. The base case low point matches the Cash Flow Statement at each year end.")


def build_valuation(ws, A, REG):
    title(ws, "Valuation", "Five methods on one page. The DCF methods start from the cost of capital; the venture capital, scorecard and Berkus methods are the ones a pre-seed investor in MENA actually uses.")
    a = Ann(ws, REG, a=66)
    R = lambda k: f"$C${tok(ws.title, k)}"
    a.section("1. COST OF CAPITAL, BUILT UP FROM ITS PARTS", "A pre-seed investment in a Cairo company selling into the GCC carries risks a listed US company does not. Each is priced separately.", cols=("Rate",))
    for k, txt, v in [("rf", "Risk free rate, US ten year treasury", 0.042), ("erp", "Mature market equity risk premium", 0.046),
                      ("crp", "Country risk premium, blended for Egypt costs and GCC revenue", 0.045), ("size", "Size premium, micro capitalisation", 0.055),
                      ("stage", "Stage and execution premium", 0.055)]:
        a.kv(k, txt, v, PCT, kind="input")
    a.kv("ke", "Cost of equity, before any marketability adjustment", f"=SUM(C{a.r - 5}:C{a.r - 1})", PCT, bold=True)
    a.blank()
    a.section("2. THE ADJUSTMENTS, EACH MADE ONCE", cols=("Value",))
    a.kv("surv", "Probability the company is still trading in year five", 0.30, PCT, kind="input")
    a.kv("dlom", "Discount for lack of marketability, DLOM", 0.30, PCT, kind="input")
    a.kv("mult", "Exit multiple on year five ARR, private vertical SaaS", 4.0, MULT, kind="input")
    a.kv("ltg", "Long term growth after year five", 0.04, PCT, kind="input")
    a.kv("tr", "Target return a pre-seed investor underwrites to", 0.50, PCT, kind="input")
    a.kv("sd_pre", "Seed round pre money valuation assumed", 6000000, USD, kind="input")
    a.kv("sa_pre", "Series A pre money valuation assumed", 20000000, USD, kind="input")
    a.kv("pool", "Employee option pool created after the pre-seed", 0.10, PCT, kind="input")
    a.kv("ret", "Share of a pre-seed holding retained after seed, Series A and the pool",
         f"=(1-IFERROR({fu('sd_amt')}/({R('sd_pre')}+{fu('sd_amt')}),0))*(1-IFERROR({fu('sa_amt')}/({R('sa_pre')}+{fu('sa_amt')}),0))*(1-{R('pool')})", PCT)
    a.kv("inv", "Pre-seed investment, sized by the model", f"={fu('ps_amt')}")
    a.kv("cash0", "Cash already in the company", f"={A.s('op_cash')}")
    a.blank()
    a.section("3. THE CASH FLOWS BEING VALUED")
    Rr = lambda k, y: f"{YCOLS[y - 1]}{tok(ws.title, k)}"
    a.line("rev", "Revenue", lambda y: TA("Financial Indicators", "rev", y))
    a.line("arr", "ARR at year end", lambda y: TA("Financial Indicators", "arr", y))
    a.line("fcf", "Free cash flow", lambda y: TA("Financial Indicators", "fcf", y))
    a.line("df", "Discount factor at the cost of equity", lambda y: f"1/(1+{R('ke')})^{y}", '0.000')
    a.line("pv", "Present value of free cash flow", lambda y: f"{Rr('fcf', y)}*{Rr('df', y)}")
    a.kv("pv5", "Present value of the five forecast years", f"=SUM(C{tok(ws.title, 'pv')}:G{tok(ws.title, 'pv')})")
    a.blank()
    G = lambda k: f"$G${tok(ws.title, k)}"
    a.section("4. METHOD ONE, DISCOUNTED CASH FLOW WITH AN EXIT MULTIPLE", cols=("Value",))
    a.kv("m1a", "Terminal value, year five ARR at the exit multiple", f"={G('arr')}*{R('mult')}")
    a.kv("m1b", "Present value of the terminal value", f"={R('m1a')}*{G('df')}")
    a.kv("m1c", "Equity value, success case, with cash held", f"={R('pv5')}+{R('m1b')}+{R('cash0')}")
    a.kv("m1d", "Weighted for the probability of reaching year five", f"={R('m1c')}*{R('surv')}")
    a.kv("m1", "Method one, pre money value after DLOM", f"=MAX(0,{R('m1d')}*(1-{R('dlom')}))", bold=True)
    a.blank()
    a.section("5. METHOD TWO, DISCOUNTED CASH FLOW ON A LONG TERM GROWTH RATE", cols=("Value",))
    a.kv("m2a", "Terminal value, year five free cash flow grown in perpetuity", f"=IFERROR(MAX(0,{G('fcf')})*(1+{R('ltg')})/({R('ke')}-{R('ltg')}),0)")
    a.kv("m2b", "Present value of the terminal value", f"={R('m2a')}*{G('df')}")
    a.kv("m2c", "Weighted for the probability of reaching year five", f"=({R('pv5')}+{R('m2b')}+{R('cash0')})*{R('surv')}")
    a.kv("m2", "Method two, pre money value after DLOM", f"=MAX(0,{R('m2c')}*(1-{R('dlom')}))", bold=True)
    a.blank()
    a.section("6. METHOD THREE, THE VENTURE CAPITAL METHOD", "What a pre-seed investor can pay and still hit the return they underwrite, after later dilution.", cols=("Value",))
    a.kv("m3a", "Exit value in year five", f"={G('arr')}*{R('mult')}")
    a.kv("m3b", "Value the pre-seed stake must reach by year five", f"={R('inv')}*(1+{R('tr')})^5")
    a.kv("m3c", "Ownership required at exit", f"=IFERROR({R('m3b')}/{R('m3a')},0)", PCT)
    a.kv("m3d", "Ownership required today, grossed up for dilution", f"=IFERROR({R('m3c')}/{R('ret')},0)", PCT)
    a.kv("m3e", "Post money value implied", f"=IFERROR({R('inv')}/{R('m3d')},0)")
    a.kv("m3", "Method three, pre money value", f"=MAX(0,{R('m3e')}-{R('inv')})", bold=True)
    a.blank()
    a.section("7. METHOD FOUR, SCORECARD AGAINST THE MENA PRE-SEED MEDIAN", "Angelsta's own guided valuation tool uses this method. Factors above 100 per cent mean Angelsta is stronger than the median pre-seed company.", cols=("Weight", "Factor"))
    a.kv("sc_med", "Median pre money of a MENA pre-seed technology round", 2000000, USD, kind="input")
    f0 = a.r
    for txt, w, fct in [("Strength of the team, both sides of the table", 0.30, 1.20), ("Size of the opportunity, MENA private markets", 0.25, 1.15),
                        ("Product and technology, two portals live, AI layer", 0.15, 1.30), ("Competitive environment, marketplaces not operating systems", 0.10, 1.05),
                        ("Marketing, sales channels and partnerships", 0.10, 1.00), ("Need for additional investment", 0.05, 0.90), ("Other, traction and community", 0.05, 0.95)]:
        label(ws, a.r, txt)
        put(ws, f"C{a.r}", w, PCT, kind="input")
        put(ws, f"D{a.r}", fct, PCT, kind="input")
        a.r += 1
    a.kv("sc_sum", "Weighted factor", f"=SUMPRODUCT(C{f0}:C{a.r - 1},D{f0}:D{a.r - 1})", PCT)
    a.kv("sc_w", "Weights must total 100 per cent", f"=SUM(C{f0}:C{a.r - 2})", PCT, kind="check")
    a.kv("m4", "Method four, pre money value", f"={R('sc_med')}*{R('sc_sum')}", bold=True)
    a.blank()
    a.section("8. METHOD FIVE, BERKUS", "Up to USD 500,000 of value for each of five risks the company has already retired.", cols=("Value credited",))
    f0 = a.r
    for txt, v in [("Sound idea, the basic value", 400000), ("Prototype, here a live product on web and mobile", 450000),
                   ("Quality management team", 400000), ("Strategic relationships, Web Summit, Biban, LEAP, accelerators", 250000),
                   ("Product roll out or sales, paid plans from Q1 2027", 150000)]:
        a.kv(None, txt, v, USD, kind="input")
    a.kv("m5", "Method five, pre money value", f"=SUM(C{f0}:C{a.r - 1})", bold=True)
    a.blank()
    a.section("9. WHAT THE FIVE METHODS CONCLUDE", cols=("Pre money", "Weight", "Weighted"))
    f0 = a.r
    for k, txt, w in [("m1", "One, discounted cash flow on an exit multiple", 0.15), ("m2", "Two, discounted cash flow on long term growth", 0.05),
                      ("m3", "Three, the venture capital method", 0.30), ("m4", "Four, scorecard", 0.30), ("m5", "Five, Berkus", 0.20)]:
        label(ws, a.r, txt)
        put(ws, f"C{a.r}", f"={R(k)}", USD)
        put(ws, f"D{a.r}", w, PCT, kind="input")
        put(ws, f"E{a.r}", f"=C{a.r}*D{a.r}", USD)
        a.r += 1
    a.kv("wchk", "Weights must total 100 per cent", f"=SUM(D{f0}:D{a.r - 1})", PCT, kind="check")
    a.kv("wpre", "Weighted pre money valuation", f"=SUM(E{f0}:E{a.r - 2})", bold=True)
    a.kv("lo", "Lowest of the five methods", f"=MIN(C{f0}:C{f0 + 4})")
    a.kv("hi", "Highest of the five methods", f"=MAX(C{f0}:C{f0 + 4})")
    a.blank()
    a.section("10. THE ROUND AT THIS VALUATION", cols=("Value",))
    a.kv("disc", "Discount to fair value offered to pre-seed investors, their entry upside", 0.20, PCT, kind="input")
    a.kv("pre", "Pre money valuation we are asking for, rounded", f"=ROUND({R('wpre')}*(1-{R('disc')})/100000,0)*100000", bold=True)
    a.kv("ask", "The pre-seed ask, from Funding and Use of Funds", f"={fu('ps_amt')}")
    a.kv("post", "Post money valuation", f"={R('pre')}+{R('ask')}")
    a.kv("own", "Equity the pre-seed buys", f"=IFERROR({R('ask')}/{R('post')},0)", PCT, bold=True)
    a.kv("band", "Inside the 10 to 20 per cent a pre-seed round normally sells", f"=IF(AND({R('own')}>=0.1,{R('own')}<=0.2),\"Yes\",\"No, revisit\")", "@")
    a.kv("x2", "Post money as a multiple of year two ARR", f"=IFERROR({R('post')}/$D${tok(ws.title, 'arr')},0)", MULT)


def build_exit(ws, A, REG):
    title(ws, "Investor Return and Exit Simulation", "Pre-seed returns, the dilution between now and exit, and the routes out.")
    a = Ann(ws, REG, a=66)
    R = lambda k: f"$C${tok(ws.title, k)}"
    V = lambda k: f"Valuation!$C${tok('Valuation', k)}"
    a.section("THE ROUND", cols=("Value",))
    a.kv("inv", "Amount invested, the pre-seed ask", f"={fu('ps_amt')}")
    a.kv("pre", "Pre money valuation, from the Valuation sheet", f"={V('pre')}")
    a.kv("post", "Post money valuation", f"={R('pre')}+{R('inv')}")
    a.kv("own0", "Ownership at entry", f"=IFERROR({R('inv')}/{R('post')},0)", PCT)
    a.kv("ret", "Share of that holding retained after seed, Series A and the pool", f"={V('ret')}", PCT)
    a.kv("own1", "Ownership at exit", f"={R('own0')}*{R('ret')}", PCT, bold=True)
    a.blank()
    a.section("WHAT THE COMPANY IS WORTH AT EXIT", "Three ARR bases and an EBITDA cross check, because no single multiple is defensible on its own.", cols=("Multiple", "Year 5 metric", "Exit value"))
    rows = [("e1", "Year five ARR multiple, conservative, 2026 private SaaS M&A median", 3), ("e2", "Year five ARR multiple, central", 4), ("e3", "Year five ARR multiple, strong, vertical SaaS with network effects", 6)]
    for k, txt, mlt in rows:
        label(ws, a.r, txt)
        put(ws, f"C{a.r}", mlt, MULT, kind="input")
        put(ws, f"D{a.r}", f"='Financial Indicators'!G{tok('Financial Indicators', 'arr')}", USD)
        put(ws, f"E{a.r}", f"=C{a.r}*D{a.r}", USD)
        a.reg[k] = a.r
        a.r += 1
    label(ws, a.r, "Year five EBITDA multiple")
    put(ws, f"C{a.r}", 12, MULT, kind="input")
    put(ws, f"D{a.r}", f"='Financial Indicators'!G{tok('Financial Indicators', 'ebitda')}", USD)
    put(ws, f"E{a.r}", f"=MAX(0,C{a.r}*D{a.r})", USD)
    a.reg["e4"] = a.r
    a.r += 2
    a.section("RETURN TO THE PRE-SEED INVESTOR", cols=("Conservative", "Central", "Strong"))
    a.kv("yrs", "Years held from entry to exit", 5, NUM, kind="input")
    label(ws, a.r, "Proceeds at exit")
    for j, k in enumerate(["e1", "e2", "e3"]):
        put(ws, f"{'CDE'[j]}{a.r}", f"=E{tok(ws.title, k)}*{R('own1')}", USD)
    a.reg["proc"] = a.r
    a.r += 1
    label(ws, a.r, "Multiple of money returned", bold=True)
    for j in range(3):
        put(ws, f"{'CDE'[j]}{a.r}", f"=IFERROR({'CDE'[j]}{a.r - 1}/{R('inv')},0)", MULT, bold=True)
    a.reg["moic"] = a.r
    a.r += 1
    label(ws, a.r, "Annualized return, IRR")
    for j in range(3):
        put(ws, f"{'CDE'[j]}{a.r}", f"=IFERROR({'CDE'[j]}{a.r - 1}^(1/{R('yrs')})-1,0)", PCT)
    a.reg["irr"] = a.r
    a.r += 2
    a.section("THE ROUTES OUT", cols=None)
    for txt in ["Strategic sale to a global equity management or private markets platform buying MENA distribution, Arabic product and the founder investor network.",
                "Sale to a regional exchange, bank or wealth platform that wants private markets infrastructure for its clients; Saudi and UAE groups have been active buyers.",
                "Sale to a fund administrator or regional data business that buys the shared record of companies, rounds and holdings.",
                "Secondary sale of the pre-seed stake at the Series A or Series B, the most likely liquidity for an early investor.",
                "Continue and distribute, once subscription revenue covers the operating base from year four."]:
        label(ws, a.r, "    " + txt, size=8.6)
        a.r += 1


def build_summary(ws, A, REG):
    title(ws, "Summary", "The whole model on one page.")
    a = Ann(ws, REG, a=60)
    FI = lambda k, y: TA("Financial Indicators", k, y)
    a.section("HEADLINES")
    for k, txt, fmt, b in [("rev", "Total revenue", USD, True), ("arr", "ARR at year end", USD, True), ("gr", "Revenue growth", PCT, False),
                           ("gm", "Gross margin", PCT, False), ("ebitda", "EBITDA", USD, True), ("ebitdam", "EBITDA margin", PCT, False),
                           ("np", "Net profit", USD, False), ("texp", "Total expenses, direct and operating", USD, False),
                           ("cash", "Cash at year end", USD, True), ("minc", "Lowest cash balance in the year", USD, False),
                           ("heads", "Employees at year end", NUM, False), ("fpaid", "Paying founder accounts at year end", NUM, False),
                           ("ipaid", "Paying investor accounts at year end", NUM, False), ("freg", "Registered founder workspaces", NUM, False),
                           ("ireg", "Registered investor accounts", NUM, False), ("cac", "Blended CAC", USD, False), ("ltvcac", "LTV to CAC", MULT, False),
                           ("churn", "Blended monthly logo churn", PCT, False)]:
        a.line(k, txt, lambda y, k=k: FI(k, y), fmt, bold=b)
    a.blank()
    a.section("THE ASK, PRODUCED BY THE MODEL", cols=("Value",))
    a.kv("ask", "Pre-seed sought now", f"={fu('ps_amt')}", bold=True)
    a.kv("y1", "Total cash required in year one, expense and capital", f"={fu('y1')}")
    a.kv("buf", "Plus buffer, months of year one cost", f"={fu('bufm')}", NUM1)
    a.kv("run", "Months the pre-seed funds on its own", f"={fu('run')}", NUM)
    a.kv("pre", "Pre money valuation, weighted across five methods", f"=Valuation!$C${tok('Valuation', 'pre')}")
    a.kv("own", "Equity offered", f"=Valuation!$C${tok('Valuation', 'own')}", PCT)
    a.kv("sd", "Seed round the model needs, and when", f"={fu('sd_amt')}")
    put(ws, f"D{a.r - 1}", f"=\"month \"&{fu('sd_m')}", "@")
    a.kv("sa", "Series A the model needs, and when", f"={fu('sa_amt')}")
    put(ws, f"D{a.r - 1}", f"=\"month \"&{fu('sa_m')}", "@")
    a.kv("be", "First month with positive EBITDA", f"='BEP Analysis'!$C${tok('BEP Analysis', 'm_ebitda')}", "General")
    a.blank()
    a.section("USE OF FUNDS", cols=("Of the ask", "Share"))
    for k, txt in [("u_mkt", "Marketing and community"), ("u_sales", "Sales and customer success"), ("u_prod", "Product and AI engineering"), ("u_ai", "AI agents, cloud and delivery"), ("u_ops", "Leadership, operations, legal and set up")]:
        label(ws, a.r, txt)
        put(ws, f"C{a.r}", f"='{FU}'!$E${tok(FU, k)}", USD)
        put(ws, f"D{a.r}", f"='{FU}'!$D${tok(FU, k)}", PCT)
        a.r += 1
    a.blank()
    a.section("THE CHECKS THAT MATTER, EACH MUST READ NIL", cols=("Value",))
    a.kv("c1", "Balance sheet, sum of the five yearly checks", f"=SUM('Balance Sheet'!C{tok('Balance Sheet', 'chk')}:G{tok('Balance Sheet', 'chk')})", USD, kind="check")
    a.kv("c2", "Income statement EBITDA against the Expenses sheet", f"=SUM('Income Statement'!C{tok('Income Statement', 'chk')}:G{tok('Income Statement', 'chk')})", USD, kind="check")
    a.kv("c3", "Payroll by function against total payroll", f"=SUM(Payroll!B{tok('Payroll', 'chk')}:BN{tok('Payroll', 'chk')})", USD, kind="check")
    a.kv("c4", "Use of funds buckets against total cash cost", f"=SUM(Expenses!B{tok('Expenses', 'uf_chk')}:BN{tok('Expenses', 'uf_chk')})", USD, kind="check")
    a.kv("c5", "Revenue families against revenue streams", f"=SUM('Total Revenue'!B{tok('Total Revenue', 'chk')}:BN{tok('Total Revenue', 'chk')})", USD, kind="check")
    a.kv("c6", "Pre-seed build up against the Expenses sheet", f"={fu('y1chk')}", USD, kind="check")
    a.kv("c7", "Months in which cash falls below zero", f"=COUNTIF({MR('Cash Flow Statement', 'c1')},\"<0\")", NUM, kind="check")
    a.kv("c9", "Market shares of paying accounts, five years", f"=SUM('Assumption Setting'!C{A.k['geo_chk']}:G{A.k['geo_chk']})-5", PCT, kind="check")
    a.kv("c8", "Activity planned beyond team capacity, five year total", f"=SUM('GTM Capacity and Timing'!C{tok('GTM Capacity and Timing', 'over')}:BN{tok('GTM Capacity and Timing', 'over')})/2", NUM1, kind="check")
    a.blank()
    a.section("WHAT THIS MODEL OPENS ON", cols=("Value",))
    for k, txt in [("op_f_reg", "Registered founder workspaces"), ("op_i_reg", "Registered investor accounts"), ("op_f_paid", "Paying founder accounts"),
                   ("op_i_paid", "Paying investor accounts"), ("op_acc", "Accelerator partners signed"), ("op_net", "Angel networks signed")]:
        a.kv(None, txt, f"={A.s(k)}", NUM)
    a.kv(None, "Opening cash", f"={A.s('op_cash')}", USD)
    a.kv(None, "Product already built, contributed by the founders", f"={A.s('op_prod')}", USD)


def build_market(ws, A, REG):
    import competitors as C
    title(ws, "Market Research", "Egypt first, then Qatar, then the GCC, with self serve from any country. Who else is in the market, and what they charge. No revenue in the model is attributed to any figure on this page.")
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 20
    ws.column_dimensions["E"].width = 18
    ws.column_dimensions["F"].width = 26
    ws.column_dimensions["G"].width = 70
    r = 4

    def tbl(r, ttl, head, rows, n=7):
        section(ws, r, ttl, n)
        r += 1
        hdr(ws, r, head)
        r += 1
        for row in rows:
            for j, v in enumerate(row):
                c = ws.cell(r, j + 1, v)
                c.font = f(8.6 if j else 9, j == 0, color=INK if j < len(row) - 1 else GREY)
                c.alignment = Alignment(wrap_text=True, vertical="top")
            r += 1
        return r + 1
    r = tbl(r, "THE MARKET, COUNTED, BY ROLL OUT ORDER", ["Market", "Figure", "Basis", "Source"], [
        ["Egypt, venture funding 2025", "USD 304m across 69 VC deals", "Counted", "MAGNiTT 2025; Egypt planning ministry reports USD 614m including debt; Partech USD 604m"],
        ["Egypt, angel networks", "Cairo Angels about 50 active angels; AUC Angels", "Counted", "Cairo Angels interview 2025; VC4A"],
        ["Qatar, venture funding 2025", "QR 214m, about USD 59m, record, +81%", "Counted", "QDB and MAGNiTT joint report"],
        ["Qatar, QIA Fund of Funds", "USD 3bn programme, over USD 1bn committed, 12 managers in Doha", "Counted", "QIA, QNA, Gulf Times 2026"],
        ["Saudi Arabia, venture funding 2025", "USD 1.72bn, 257 deals, first in MENA by deals", "Counted", "MAGNiTT FY2025 with SVC"],
        ["UAE, venture deals 2025", "USD 1.58bn, 231 deals", "Counted", "MAGNiTT via Arab News"],
        ["GCC private debt to startups 2025", "USD 4.1bn, Saudi Arabia 95 per cent", "Counted", "Stride Ventures via Arab News"],
        ["MENA venture funding 2025", "USD 3.8bn across 688 deals, +74%", "Counted", "MAGNiTT FY2025"],
        ["Africa tech funding 2025", "USD 4.1bn, equity USD 2.4bn over 462 deals, debt USD 1.6bn", "Counted", "Partech Africa Tech VC Report 2025"],
        ["Saudi angels, OQAL", "600+ registered angels", "Counted", "Supplied competitive analysis"],
        ["MENA family groups active in venture", "58 per cent; 70 per cent source deals through networks", "Counted", "Arab News, March 2025"],
    ], 4)
    r = tbl(r, "THE SERVICEABLE MARKET, DERIVED FOR THIS MODEL", ["Market", "Startups that run a cap table and raise", "Institutional investors", "Active angels", "Serviceable revenue, USD m a year", "How it is built"], [
        ["Egypt", "2,500", "250", "1,200", "3.1", "About 70 funded a year times a 30x pipeline; EGP price list at 60 per cent"],
        ["Qatar", "600", "120", "500", "1.4", "QDB, QSTP and QIA programmes; GCC price list"],
        ["Saudi Arabia", "3,500", "450", "2,000", "7.9", "257 deals a year; OQAL 600+ angels; 65+ VC firms and angel groups"],
        ["UAE", "3,000", "450", "1,500", "7.0", "231 deals a year; DIFC and ADGM fund managers"],
        ["Kuwait, Bahrain, Oman", "800", "150", "400", "1.9", "Smaller ecosystems with active family offices"],
        ["Rest of MENA and Africa, self serve", "6,000", "400", "2,500", "6.0", "Africa 462 equity deals; Morocco, Jordan, Tunisia; 70 per cent price index"],
        ["Total, home and regional", "16,400", "1,820", "8,100", "27.3", "Before any rest of world self serve demand"],
    ], 6)
    rows = []
    for nm, reg, hq, side, cat, threat, price, notev in C.DIRECTORY:
        rows.append([nm, reg, hq, side, cat, threat + ", " + price, notev])
    r = tbl(r, "WHO ELSE IS IN THIS MARKET: STARTUP AND INVESTOR OPERATING SYSTEMS, MENA, AFRICA, REGIONAL AND GLOBAL", ["Company", "Region", "HQ", "Side", "Category", "Threat, pricing", "What it means for Angelsta"], rows)
    note(ws, r, "Sources: Angelsta SaaS Marketing Competitive Analysis (research cut-off 19 August 2026), MAGNiTT, Partech, QDB, QIA, Arab News, vendor pricing pages. Vendor prices are indications; most institutional plans are quoted on request.")
    REG.setdefault(ws.title, {})


def build_actuals(ws, A, REG):
    title(ws, "Actuals", "The opening position, and a grid to record each month as it closes.")
    set_time_widths(ws, 54)
    r = 4
    section(ws, r, "OPENING POSITION AT 31 DECEMBER 2026")
    r += 1
    for txt, val in [("Cash at bank", f"={A.s('op_cash')}"), ("Product built to date, contributed by the founders", f"={A.s('op_prod')}"),
                     ("Trade receivables", 0), ("Trade and other payables", 0), ("Deferred revenue", 0),
                     ("Paid in share capital, cash plus the product contributed", f"={A.s('op_cash')}+{A.s('op_prod')}")]:
        label(ws, r, txt)
        put(ws, f"B{r}", val, USD, kind=None if isinstance(val, str) else "calc")
        r += 1
    r += 1
    t = TS(ws, REG, r)
    t.section("MONTHLY ACTUALS, ENTER AS EACH MONTH CLOSES", "Leave a month blank until it has closed. Nothing downstream reads this grid; it feeds the variance block only.")
    act = [("a_rev", "Revenue, actual"), ("a_dir", "Direct cost, actual"), ("a_opx", "Operating cost, actual"), ("a_cash", "Closing cash, actual"),
           ("a_freg", "New founder registrations, actual"), ("a_ireg", "New investor registrations, actual"), ("a_fpaid", "Paying founder accounts, actual"),
           ("a_ipaid", "Paying investor accounts, actual")]
    for k, txt in act:
        rr = t.line(k, txt, lambda m: None, NUM)
        for m in range(1, NM + 1):
            c = ws[f"{mcol(m)}{rr}"]
            c.value = None
            c.fill = fill(YELLOW)
            c.font = f(9, color=BLUE)
    t.blank()
    t.section("VARIANCE AGAINST THE MODEL")
    for k, txt, src in [("a_rev", "Revenue", ("Total Revenue", "rev")), ("a_dir", "Direct cost", ("Expenses", "direct")),
                        ("a_opx", "Operating cost", ("Expenses", "opex_t")), ("a_cash", "Closing cash", ("Cash Flow Statement", "c1"))]:
        t.line(f"f_{k}", f"{txt}, forecast", lambda m, src=src: T(src[0], src[1], m), USD)
        t.line(f"v_{k}", f"{txt}, variance", lambda m, k=k: f"IF({mcol(m)}{tok(ws.title, k)}=\"\",0,{mcol(m)}{tok(ws.title, k)}-{mcol(m)}{tok(ws.title, 'f_' + k)})", USD, indent=1)


def build_divider(ws, name, items):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 90
    ws["B2"] = name
    ws["B2"].font = f(20, True, color=BRAND)
    r = 5
    for nm, desc in items:
        ws.cell(r, 2, nm).font = f(9, True)
        ws.cell(r, 3, desc).font = f(9, color=GREY)
        r += 1
    ws.sheet_properties.tabColor = BRAND


CONTENTS = [
    ("Front", [("Cover", "This page: what the model is and how to read it"), ("Summary", "The whole model on one page, with the ask and the checks"),
               ("Market Research", "The market Angelsta sells into, who else is in it and what they charge")]),
    ("Input", [("Assumption Setting", "In the order the model runs: basis, opening position, acquisition, the two funnels, capacity, pricing, engines, cost, funding, assets"),
               ("Capital Expenditure", "Assets driven by new hires, plus shared and intangible assets"), ("Actuals", "The opening position and a grid to record each month")]),
    ("Process", [("Acquisitions", "Spend and ecosystem activity to registrations, active free accounts, paid plans and sold institutional contracts"),
                 ("GTM Capacity and Timing", "Who runs the activity, whether there are enough of them, and when each engine and market opens"),
                 ("Revenue Streams", "Seven subscription engines and five add-ons, every one an output of the funnel"),
                 ("Total Revenue", "Gathered into four families, with MRR and ARR"), ("Payroll", "Thirty roles, monthly, with heads set by year, EGP and USD salaries"),
                 ("Depreciation and Amortization", "Straight line by asset class"),
                 ("Expenses", "Direct cost, partner revenue share, operating cost, and the first twelve months in full")]),
    ("Output", [("Income Statement", "Five years to 31 December"), ("Balance Sheet", "Five years, with the balance check"),
                ("Cash Flow Statement", "Monthly working and the annual statement"), ("Financial Indicators", "Growth, SaaS metrics, profitability, unit economics, cash"),
                ("Funding and Use of Funds", "The pre-seed ask built from year one expenses, use of funds, runway, and the follow on rounds the model sizes")]),
    ("Analysis", [("BEP Analysis", "Break even revenue and the month it turns"), ("PB Analysis", "When the capital comes back, base and flexed"),
                  ("Sensitivity", "Three two way grids on the year five result"), ("Stress Test", "Four scenarios on volume, price and cost"),
                  ("Exit Angel and VC", "Pre-seed returns and the routes out"), ("Valuation", "Five methods, built up from the cost of capital, and the round they imply")]),
]


def build_cover(ws, A, REG):
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = BRAND
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 42
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 96
    ws["B2"] = "Angelsta"
    ws["B2"].font = f(26, True, color=BRAND)
    ws["B3"] = "Operational Financial Model, 2027 to 2031"
    ws["B3"].font = f(12)
    r = 6
    ws.cell(r, 2, "ABOUT THIS MODEL").font = f(9.5, True, color=BRAND)
    r += 1
    for k, v in [("Business name", "Angelsta"), ("Industry", "Private markets software: the operating system for founders and private investors"),
                 ("Markets", "Egypt from month 1, Qatar from month 4, Saudi Arabia from month 10, UAE from month 13, Kuwait, Bahrain and Oman from month 19; self serve from any country from day one"),
                 ("Products", "Founder workspace (Free, Pro, Team, Custom) and investor portfolio OS (Free, Angel, Institutional, Custom)"),
                 ("Business model", "Freemium subscriptions on both sides, monthly or annual; add-ons modelled behind a switch, off in the base case"),
                 ("Model currency", "USD, with Egyptian pound salaries converted at the monthly rate on the Assumption sheet"),
                 ("Model start", "January 2027"), ("Forecast period", "5 years, 60 months"),
                 ("The ask", "Not typed. Funding and Use of Funds builds it from the year one expense the model produces")]:
        ws.cell(r, 2, k).font = f(9)
        ws.cell(r, 4, v).font = f(9)
        r += 1
    r += 1
    ws.cell(r, 2, "HOW TO READ IT").font = f(9.5, True, color=BRAND)
    r += 1
    for txt in ["Blue figures on a yellow fill are typed inputs. Change those and the whole model moves. Black figures are formulas on the same sheet; green figures are links to another sheet.",
                "Red figures are checks. The Summary sheet gathers every check; each must read nil.",
                "On every monthly sheet the year total comes first, then that year's twelve months. The month columns are grouped, so each year can be collapsed.",
                "No volume is typed. Registrations, active accounts, paying accounts and contracts all come out of the funnel on Acquisitions.",
                "The pre-seed ask is an output: year one cash cost, less opening cash, plus a buffer of months, rounded up. The seed and Series A are sized the same way.",
                "Opening figures in section 2 of the Assumption Setting are placeholders until the founders confirm the 31 December 2026 position."]:
        c = ws.cell(r, 2, txt)
        c.font = f(9)
        r += 1
    r += 1
    ws.cell(r, 2, "CONTENTS").font = f(9.5, True, color=BRAND)
    r += 1
    for grp, items in CONTENTS:
        ws.cell(r, 2, grp).font = f(9.5, True, color=BRAND)
        r += 1
        for nm, desc in items:
            c = ws.cell(r, 2, f'=HYPERLINK("#\'{nm}\'!A1","   {nm}")')
            c.font = f(9, color="1F4E79")
            ws.cell(r, 4, desc).font = f(9, color=GREY)
            r += 1
