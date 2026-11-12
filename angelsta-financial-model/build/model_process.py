"""Process sheets: Payroll, Acquisitions, GTM Capacity and Timing, Revenue Streams, Total Revenue."""
from xl import *

ROLES = [
    ("Co-founder and Chief Executive Officer, investment", "Leadership", 1, [1, 1, 1, 1, 1], "EGP", 35000),
    ("Managing Co-founder and Chief Operating Officer", "Leadership", 1, [1, 1, 1, 1, 1], "EGP", 35000),
    ("Technical Co-founder and Chief Technology Officer", "Leadership", 1, [1, 1, 1, 1, 1], "EGP", 35000),
    ("Senior Full Stack Engineer, lead", "Technology", 1, [1, 1, 2, 4, 6], "EGP", 75000),
    ("Senior AI and Machine Learning Engineer", "Technology", 2, [1, 1, 2, 4, 6], "EGP", 85000),
    ("Full Stack Engineer", "Technology", 6, [1, 2, 3, 7, 10], "EGP", 45000),
    ("Mobile Engineer", "Technology", 13, [0, 1, 2, 3, 4], "EGP", 50000),
    ("QA and DevOps Engineer", "Technology", 13, [0, 1, 1, 3, 4], "EGP", 40000),
    ("Data Engineer", "Technology", 31, [0, 0, 1, 2, 3], "EGP", 60000),
    ("Product Designer, UI and UX", "Product", 1, [1, 1, 2, 3, 4], "EGP", 35000),
    ("Product Manager", "Product", 27, [0, 0, 1, 3, 4], "EGP", 65000),
    ("Head of Sales, Institutional, Cairo based", "Sales", 30, [0, 0, 1, 1, 1], "EGP", 90000),
    ("Account Executive, Institutional, Cairo based, covers Qatar and GCC", "Sales", 7, [1, 2, 4, 8, 12], "EGP", 50000),
    ("Sales Development Representative, Arabic and English", "Sales", 5, [1, 2, 3, 6, 8], "EGP", 20000),
    ("Head of Marketing", "Marketing", 28, [0, 0, 1, 1, 1], "EGP", 90000),
    ("Growth Marketing Lead", "Marketing", 1, [1, 1, 1, 1, 1], "EGP", 50000),
    ("Performance Marketing Specialist", "Marketing", 3, [1, 1, 2, 4, 6], "EGP", 25000),
    ("Content and Research Analyst, Arabic and English", "Marketing", 7, [1, 1, 2, 4, 5], "EGP", 22000),
    ("Community and Partnerships Lead, Egypt and Qatar", "Community and Partnerships", 2, [1, 1, 2, 4, 6], "EGP", 35000),
    ("Customer Success Specialist", "Customer", 7, [1, 2, 4, 8, 12], "EGP", 25000),
    ("Customer Support Agent, Arabic and English", "Customer", 13, [0, 1, 3, 6, 9], "EGP", 16000),
    ("Operations, HR and Finance Officer", "Operations", 13, [0, 1, 2, 3, 4], "EGP", 25000),
    ("Finance Manager", "Finance and Legal", 33, [0, 0, 1, 2, 3], "EGP", 45000),
    ("Legal and Compliance Officer", "Finance and Legal", 34, [0, 0, 1, 1, 1], "EGP", 50000),
]
FUNCS = ["Leadership", "Technology", "Product", "Sales", "Marketing", "Community and Partnerships", "Customer", "Operations", "Finance and Legal"]


def prevref(row, m, opening):
    return opening if m == 1 else f"{mcol(m - 1)}{row}"


# ---------------------------------------------------------------------------
def build_payroll(ws, A, REG):
    title(ws, "Payroll", "Twenty four roles, every one based in Cairo and paid in Egyptian pounds; Qatar and the GCC are covered by the founders, the account executives and travel. Heads are set by year and ramp in month by month; salaries are gross monthly in the currency of the role, converted at the monthly rate.")
    set_time_widths(ws, 54)
    ws.column_dimensions["B"].width = 26
    t = TS(ws, REG, 4)
    section(ws, t.r, "ESTABLISHMENT, INPUTS")
    t.r += 1
    hdr(ws, t.r, ["Role", "Function", "First month", "Heads Y1", "Y2", "Y3", "Y4", "Y5", "Currency", "Gross salary, month, Y1"])
    t.r += 1
    first = t.r
    for i, (role, fn, fm, heads, ccy, sal) in enumerate(ROLES):
        r = first + i
        label(ws, r, role)
        label(ws, r, fn, col=2, size=8, color=GREY)
        put(ws, f"C{r}", fm, NUM, kind="input")
        for j, h in enumerate(heads):
            put(ws, f"{'DEFGH'[j]}{r}", h, NUM, kind="input")
        put(ws, f"I{r}", ccy, "@", kind="input")
        put(ws, f"J{r}", sal, NUM, kind="input")
    last = first + len(ROLES) - 1
    t.r = last + 1
    label(ws, t.r, "Total establishment at the end of each year", bold=True)
    for j in range(5):
        cl = "DEFGH"[j]
        put(ws, f"{cl}{t.r}", f"=SUM({cl}{first}:{cl}{last})", NUM, bold=True)
    t.r += 2
    keys = {}
    for key, txt, val, fmt in [("bur_egp", "Employer burden on EGP salaries, social insurance and medical", 0.155, PCT),
                               ("bur_usd", "Employer burden on USD salaries in the GCC, GOSI, medical, visas", 0.12, PCT),
                               ("inc_egp", "Annual salary increase, EGP roles", 0.14, PCT),
                               ("inc_usd", "Annual salary increase, USD roles", 0.04, PCT)]:
        label(ws, t.r, txt)
        put(ws, f"C{t.r}", val, fmt, kind="input")
        keys[key] = f"$C${t.r}"
        t.r += 1
    note(ws, t.r, "Salaries: Cairo market rates for 2026, mid level engineers EGP 30k to 60k and senior EGP 50k to 90k a month. Founders take a reduced salary of EGP 35,000 a month until the business breaks even.")
    t.r += 2

    t.section("EXCHANGE RATE")
    t.line("mi", "Month index", lambda m: str(m), NUM, total=None)
    t.line("fx", "Egyptian pounds to the dollar", lambda m: f"{A.s('egp')}*(1+{A.s('egp_dep')})^(({m}-1)/12)", NUM2, total="avg")
    t.blank()

    def heads_formula(r, m):
        y = yr(m)
        hy = f"${'DEFGH'[y - 1]}${r}"
        hp = "0" if y == 1 else f"${'DEFGH'[y - 2]}${r}"
        return f"IF({m}<$C${r},0,IF({hy}<={hp},{hy},ROUNDUP({hp}+({hy}-{hp})*{miy(m)}/12,0)))"

    t.section("MONTHLY HEADCOUNT")
    for i, (role, *_rest) in enumerate(ROLES):
        r = first + i
        t.line(f"h{i}", role, lambda m, r=r: heads_formula(r, m), NUM, total="end")
    hr0, hr1 = REG[ws.title]["h0"], REG[ws.title][f"h{len(ROLES) - 1}"]
    t.line("heads", "Total headcount", lambda m: f"SUM({mcol(m)}{hr0}:{mcol(m)}{hr1})", NUM, total="end", bold=True)
    t.line("hires", "New employees joining in the month",
           lambda m: f"{mcol(m)}{REG[ws.title]['heads']}" if m == 1 else f"MAX(0,{mcol(m)}{REG[ws.title]['heads']}-{mcol(m - 1)}{REG[ws.title]['heads']})", NUM)
    t.blank()

    t.section("MONTHLY PAYROLL, FULLY LOADED, USD")
    fx = REG[ws.title]["fx"]
    for i, (role, *_rest) in enumerate(ROLES):
        r = first + i
        hrow = REG[ws.title][f"h{i}"]
        t.line(f"p{i}", role, lambda m, r=r, hrow=hrow:
               f"{mcol(m)}{hrow}*$J${r}*IF($I${r}=\"EGP\",(1+{keys['inc_egp']})^{yr(m) - 1}*(1+{keys['bur_egp']})/{mcol(m)}{fx},(1+{keys['inc_usd']})^{yr(m) - 1}*(1+{keys['bur_usd']}))",
               USD)
    pr0, pr1 = REG[ws.title]["p0"], REG[ws.title][f"p{len(ROLES) - 1}"]
    t.line("payroll", "Total payroll, fully loaded", lambda m: f"SUM({mcol(m)}{pr0}:{mcol(m)}{pr1})", USD, bold=True)
    t.blank()

    t.section("HEADCOUNT AND PAYROLL BY FUNCTION")
    for fn in FUNCS:
        idx = [i for i, rl in enumerate(ROLES) if rl[1] == fn]
        t.line(f"fh_{fn}", f"Heads, {fn}", lambda m, idx=idx: "+".join(f"{mcol(m)}{REG[ws.title][f'h{i}']}" for i in idx), NUM, total="end")
    for fn in FUNCS:
        idx = [i for i, rl in enumerate(ROLES) if rl[1] == fn]
        t.line(f"fp_{fn}", f"Payroll, {fn}", lambda m, idx=idx: "+".join(f"{mcol(m)}{REG[ws.title][f'p{i}']}" for i in idx), USD)
    g = REG[ws.title]
    t.line("chk", "Check, functions against total payroll", lambda m: f"ROUND(SUM({mcol(m)}{g['fp_Leadership']}:{mcol(m)}{g['fp_Finance and Legal']})-{mcol(m)}{g['payroll']},2)", USD, kind="check")
    t.line("comm_heads", "Commercial heads, sales and community, who travel",
           lambda m: f"{mcol(m)}{g['fh_Sales']}+{mcol(m)}{g['fh_Community and Partnerships']}", NUM, total="end")
    # specific roles used by the capacity sheet
    idx = lambda pre: [i for i, rl in enumerate(ROLES) if rl[0].startswith(pre)]
    t.line("ae_heads", "Account executives", lambda m: "+".join(f"{mcol(m)}{g[f'h{i}']}" for i in idx("Account Executive")), NUM, total="end")
    t.line("sdr_heads", "Sales development reps", lambda m: "+".join(f"{mcol(m)}{g[f'h{i}']}" for i in idx("Sales Development")), NUM, total="end")
    t.line("cp_heads", "Community and partnerships heads", lambda m: f"{mcol(m)}{g['fh_Community and Partnerships']}", NUM, total="end")
    t.line("cs_heads", "Customer success heads", lambda m: "+".join(f"{mcol(m)}{g[f'h{i}']}" for i in idx("Customer Success")), NUM, total="end")
    t.line("fd_heads", "Founders", lambda m: f"{mcol(m)}{g['fh_Leadership']}", NUM, total="end")
    return keys


# ---------------------------------------------------------------------------
def build_acquisitions(ws, A, REG):
    title(ws, "Acquisitions", "Spend and activity become registrations, registrations become active free accounts, active accounts convert to paid plans, sold accounts come through the sales funnel. Nothing on this sheet is typed.")
    set_time_widths(ws, 58)
    t = TS(ws, REG, 3)
    g = REG.setdefault(ws.title, {})
    label(ws, 3, "Month index, used by the lag formulas", size=8, color=GREY)
    for m in range(1, NM + 1):
        put(ws, f"{mcol(m)}3", m, NUM, kind="note")
    g["mi"] = 3
    t.r = 4
    R = lambda key, m: f"{mcol(m)}{tok(ws.title, key)}"
    P = lambda key, m, opening="0": opening if m == 1 else f"{mcol(m - 1)}{tok(ws.title, key)}"

    t.section("1. ONLINE CHANNELS, SPEND TO REGISTRATIONS")
    chans = ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"]
    names = ["LinkedIn Ads, founders", "Meta and Instagram, founders", "Google Search, cap table and data room intent",
             "LinkedIn Ads, investors and fund managers", "Google Search, portfolio management intent", "SEO, newsletter and data reports",
             "Qatar founders, family offices and funds", "Global self serve, any country"]
    for ch, nm in zip(chans, names):
        t.line(f"{ch}_sp", nm, lambda m, ch=ch: A.y(ch, m), USD)
        t.line(f"{ch}_cl", "Paid clicks", lambda m, ch=ch: f"IFERROR({R(ch + '_sp', m)}/{A.c(ch, 'H')},0)", NUM, indent=1)
        t.line(f"{ch}_tc", "Total clicks after organic and referral", lambda m, ch=ch: f"{R(ch + '_cl', m)}*(1+{A.c(ch, 'I')})", NUM, indent=1)
        t.line(f"{ch}_rg", "Registrations", lambda m, ch=ch: f"{R(ch + '_tc', m)}*{A.c(ch, 'J')}", NUM1, indent=1)
    t.line("on_sp", "Online spend", lambda m: "+".join(R(c + "_sp", m) for c in chans), USD, bold=True)
    t.line("on_f", "Founder registrations from online", lambda m: "+".join(f"{R(c + '_rg', m)}*{A.c(c, 'K')}" for c in chans), NUM1, bold=True)
    t.line("on_i", "Investor registrations from online", lambda m: "+".join(f"{R(c + '_rg', m)}*(1-{A.c(c, 'K')})" for c in chans), NUM1, bold=True)
    t.blank()

    t.section("2. EVENTS, COMMUNITY AND PARTNERS")
    t.line("ev", "Ecosystem events attended", lambda m: A.y("ev_n", m), NUM2)
    t.line("ev_sp", "Event cost", lambda m: f"{R('ev', m)}*{A.y('ev_cost', m)}", USD, indent=1)
    t.line("ev_f", "Founder registrations from events", lambda m: f"{R('ev', m)}*{A.s('ev_f')}", NUM1, indent=1)
    t.line("ev_i", "Investor registrations from events", lambda m: f"{R('ev', m)}*{A.s('ev_i')}", NUM1, indent=1)
    t.line("mu", "Community meetups and circles hosted", lambda m: A.y("mu_n", m), NUM1)
    t.line("mu_sp", "Meetup cost", lambda m: f"{R('mu', m)}*{A.y('mu_cost', m)}", USD, indent=1)
    t.line("mu_f", "Founder registrations from meetups", lambda m: f"{R('mu', m)}*{A.s('mu_f')}", NUM1, indent=1)
    t.line("mu_i", "Investor registrations from meetups", lambda m: f"{R('mu', m)}*{A.s('mu_i')}", NUM1, indent=1)

    def ramp(key, opening, m):
        y = yr(m)
        cur = A.y(key, y, False)
        prev = A.s(opening) if y == 1 else A.y(key, y - 1, False)
        return f"{prev}+({cur}-{prev})*{miy(m)}/12"
    t.line("acc", "Accelerator and incubator partners active", lambda m: ramp("acc_n", "op_acc", m), NUM1, total="end")
    t.line("acc_f", "Founder registrations from accelerator cohorts", lambda m: f"{R('acc', m)}*{A.s('acc_f')}", NUM1, indent=1)
    t.line("net", "Angel networks and syndicates active", lambda m: ramp("net_n", "op_net", m), NUM1, total="end")
    t.line("net_i", "Investor registrations from angel networks", lambda m: f"{R('net', m)}*{A.s('net_i')}", NUM1, indent=1)
    t.line("ob", "Outbound contacts to institutions, planned", lambda m: A.y("ob_n", m), NUM)
    t.line("off_sp", "Events and community spend", lambda m: f"{R('ev_sp', m)}+{R('mu_sp', m)}", USD, bold=True)
    t.blank()

    t.section("3. THE FOUNDER FUNNEL")
    op_free_f = f"{A.s('op_f_reg')}*{A.y('f_act', 1, False)}"
    t.line("f_ref", "Founder registrations from founder referrals",
           lambda m: f"({P('f_free', m, op_free_f)}+{P('f_paid', m, A.s('op_f_paid'))})*{A.s('f_ref')}", NUM1)
    t.line("f_inv", "Founder registrations referred by paying investors, deal flow",
           lambda m: f"{P('i_paid', m, A.s('op_i_paid'))}*{A.s('i_ref')}", NUM1)
    t.line("f_new", "New founder registrations",
           lambda m: f"{R('on_f', m)}+{R('ev_f', m)}+{R('mu_f', m)}+{R('acc_f', m)}+{R('f_ref', m)}+{R('f_inv', m)}", NUM1, bold=True)
    t.line("f_reg", "Registered founder workspaces, cumulative", lambda m: f"{P('f_reg', m, A.s('op_f_reg'))}+{R('f_new', m)}", NUM, total="end")
    t.line("f_actn", "Newly activated founder workspaces", lambda m: f"{R('f_new', m)}*{A.y('f_act', m)}", NUM1)
    t.line("f_ss", "Self serve conversions to paid",
           lambda m: f"IF({m}<MIN({A.s('o_pro')},{A.s('o_team')}),0,{P('f_free', m, op_free_f)}*{A.y('f_conv', m)})", NUM2)
    t.line("f_dem", "Demos booked by founders", lambda m: f"IF({m}<{A.s('o_team')},0,{R('f_actn', m)}*{A.s('f_demo')})", NUM2)
    t.line("f_win", "Demo led wins, one month later", lambda m: "0" if m == 1 else f"{P('f_dem', m)}*{A.s('f_win')}", NUM2)
    t.line("f_free", "Active free founder workspaces",
           lambda m: f"MAX(0,{P('f_free', m, op_free_f)}*(1-{A.s('f_idle')})+{R('f_actn', m)}-{R('f_ss', m)}-{R('f_win', m)})", NUM, total="end")
    t.line("n_pro", "New Pro accounts", lambda m: f"{R('f_ss', m)}*{A.y('f_promix', m)}", NUM2, indent=1)
    t.line("n_team", "New Team accounts", lambda m: f"{R('f_ss', m)}*(1-{A.y('f_promix', m)})+{R('f_win', m)}*(1-IF({m}>={A.s('o_sc')},{A.s('f_cshare')},0))", NUM2, indent=1)
    t.line("n_sc", "New founder Custom accounts", lambda m: f"{R('f_win', m)}*IF({m}>={A.s('o_sc')},{A.s('f_cshare')},0)", NUM2, indent=1)
    t.line("u_pt", "Upgrades from Pro to Team", lambda m: f"{P('a_pro', m, A.s('op_f_paid'))}*{A.s('up_pt')}", NUM2, indent=1)
    t.line("a_pro", "Paying founder accounts on Pro",
           lambda m: f"{P('a_pro', m, A.s('op_f_paid'))}*(1-{A.y('ch_pro', m)})-{R('u_pt', m)}+{R('n_pro', m)}", NUM2, total="end")
    t.line("a_team", "Paying founder accounts on Team",
           lambda m: f"{P('a_team', m)}*(1-{A.y('ch_team', m)})+{R('n_team', m)}+{R('u_pt', m)}", NUM2, total="end")
    t.line("a_sc", "Paying founder accounts on Custom",
           lambda m: f"{P('a_sc', m)}*(1-{A.y('ch_sc', m)})+{R('n_sc', m)}", NUM2, total="end")
    t.line("f_paid", "Paying founder accounts", lambda m: f"{R('a_pro', m)}+{R('a_team', m)}+{R('a_sc', m)}", NUM, total="end", bold=True)
    t.line("f_newp", "New paying founder accounts", lambda m: f"{R('n_pro', m)}+{R('n_team', m)}+{R('n_sc', m)}", NUM1)
    t.line("f_churn", "Founder accounts lost to churn",
           lambda m: f"{P('a_pro', m, A.s('op_f_paid'))}*{A.y('ch_pro', m)}+{P('a_team', m)}*{A.y('ch_team', m)}+{P('a_sc', m)}*{A.y('ch_sc', m)}", NUM1)
    t.blank()

    t.section("4. THE INVESTOR FUNNEL")
    op_free_i = f"{A.s('op_i_reg')}*{A.y('i_act', 1, False)}"
    t.line("i_inv", "Investor registrations invited by founders, the cap table effect",
           lambda m: f"{R('f_actn', m)}*{A.s('inv_per_f')}*{A.y('inv_acc', m)}", NUM1)
    t.line("i_new", "New investor registrations",
           lambda m: f"{R('on_i', m)}+{R('ev_i', m)}+{R('mu_i', m)}+{R('net_i', m)}+{R('i_inv', m)}", NUM1, bold=True)
    t.line("i_reg", "Registered investor accounts, cumulative", lambda m: f"{P('i_reg', m, A.s('op_i_reg'))}+{R('i_new', m)}", NUM, total="end")
    t.line("i_actn", "Newly activated investor accounts", lambda m: f"{R('i_new', m)}*{A.y('i_act', m)}", NUM1)
    t.line("i_ss", "Self serve conversions to Angel", lambda m: f"IF({m}<{A.s('o_ang')},0,{P('i_free', m, op_free_i)}*{A.y('i_conv', m)})", NUM2)
    t.line("i_free", "Active free investor accounts",
           lambda m: f"MAX(0,{P('i_free', m, op_free_i)}*(1-{A.s('i_idle')})+{R('i_actn', m)}-{R('i_ss', m)})", NUM, total="end")
    t.line("i_mtg", "Institutional meetings from outbound", lambda m: f"{R('ob', m)}*{A.y('i_c2m', m)}", NUM1)
    t.line("i_dem", "Institutional demos, outbound and inbound",
           lambda m: f"{R('i_mtg', m)}*{A.s('i_m2d')}+{R('i_actn', m)}*{A.s('i_inst')}*{A.s('i_inb')}", NUM1)
    t.line("i_win", "Institutional contracts signed, after the sales cycle",
           lambda m: f"IF({m}<{A.s('o_inst')},0,IFERROR(INDEX($C{g['i_dem']}:$BN{g['i_dem']},MATCH({m}-{A.s('i_lag')},$C$3:$BN$3,0)),0)*{A.y('i_win', m)})", NUM2)
    t.line("n_ang", "New Angel accounts", lambda m: R("i_ss", m), NUM2, indent=1)
    t.line("n_inst", "New Institutional accounts", lambda m: f"{R('i_win', m)}*(1-IF({m}>={A.s('o_ic')},{A.s('i_cshare')},0))", NUM2, indent=1)
    t.line("n_ic", "New investor Custom accounts", lambda m: f"{R('i_win', m)}*IF({m}>={A.s('o_ic')},{A.s('i_cshare')},0)", NUM2, indent=1)
    t.line("u_ai", "Upgrades from Angel to Institutional", lambda m: f"{P('a_ang', m, A.s('op_i_paid'))}*{A.s('up_ai')}", NUM2, indent=1)
    t.line("a_ang", "Paying investor accounts on Angel",
           lambda m: f"{P('a_ang', m, A.s('op_i_paid'))}*(1-{A.y('ch_ang', m)})-{R('u_ai', m)}+{R('n_ang', m)}", NUM2, total="end")
    t.line("a_inst", "Paying investor accounts on Institutional",
           lambda m: f"{P('a_inst', m)}*(1-{A.y('ch_inst', m)})+{R('n_inst', m)}+{R('u_ai', m)}", NUM2, total="end")
    t.line("a_ic", "Paying investor accounts on Custom",
           lambda m: f"{P('a_ic', m)}*(1-{A.y('ch_ic', m)})+{R('n_ic', m)}", NUM2, total="end")
    t.line("i_paid", "Paying investor accounts", lambda m: f"{R('a_ang', m)}+{R('a_inst', m)}+{R('a_ic', m)}", NUM, total="end", bold=True)
    t.line("i_newp", "New paying investor accounts", lambda m: f"{R('n_ang', m)}+{R('n_inst', m)}+{R('n_ic', m)}", NUM1)
    t.line("i_churn", "Investor accounts lost to churn",
           lambda m: f"{P('a_ang', m, A.s('op_i_paid'))}*{A.y('ch_ang', m)}+{P('a_inst', m)}*{A.y('ch_inst', m)}+{P('a_ic', m)}*{A.y('ch_ic', m)}", NUM1)
    t.blank()

    t.section("5. BOTH SIDES TOGETHER")
    t.line("mk_sp", "Marketing and community spend", lambda m: f"{R('on_sp', m)}+{R('off_sp', m)}", USD, bold=True)
    t.line("reg_new", "New registrations, founders and investors", lambda m: f"{R('f_new', m)}+{R('i_new', m)}", NUM)
    t.line("reg", "Registered accounts, cumulative", lambda m: f"{R('f_reg', m)}+{R('i_reg', m)}", NUM, total="end")
    t.line("free", "Active free accounts", lambda m: f"{R('f_free', m)}+{R('i_free', m)}", NUM, total="end")
    t.line("paid", "Paying accounts", lambda m: f"{R('f_paid', m)}+{R('i_paid', m)}", NUM, total="end", bold=True)
    t.line("newp", "New paying accounts", lambda m: f"{R('f_newp', m)}+{R('i_newp', m)}", NUM1)
    t.line("churn", "Paying accounts lost to churn", lambda m: f"{R('f_churn', m)}+{R('i_churn', m)}", NUM1)
    t.line("salesled", "Paying accounts on sales led plans, Custom and Institutional", lambda m: f"{R('a_sc', m)}+{R('a_inst', m)}+{R('a_ic', m)}", NUM, total="end")
    t.line("ai_cr", "AI credits consumed",
           lambda m: f"{R('free', m)}*{A.s('ai_free')}+{R('a_pro', m)}*{A.s('ai_pro')}+{R('a_team', m)}*{A.s('ai_team')}+{R('a_sc', m)}*{A.s('ai_sc')}+{R('a_ang', m)}*{A.s('ai_ang')}+{R('a_inst', m)}*{A.s('ai_inst')}+{R('a_ic', m)}*{A.s('ai_ic')}", NUM)
    t.line("cpr", "Marketing cost per registration", lambda m: f"IFERROR({R('mk_sp', m)}/{R('reg_new', m)},0)", USD2, total="avg")
    t.line("cpp", "Marketing cost per new paying account", lambda m: f"IFERROR({R('mk_sp', m)}/{R('newp', m)},0)", USD, total="avg")
    t.line("mkts", "Home and GCC markets live, Egypt, Qatar, Saudi Arabia, UAE, rest of GCC", lambda m: "+".join(f"IF({m}>={A.c(k, 'I')},1,0)" for k in ["g_egy", "g_qat", "g_ksa", "g_uae", "g_gcc"]), NUM, total="end")


# ---------------------------------------------------------------------------
def build_gtm(ws, A, REG):
    title(ws, "GTM Capacity and Timing", "Who runs the activity, whether there are enough of them, and when each engine and market opens.")
    set_time_widths(ws, 58)
    t = TS(ws, REG, 4)
    PR, AQ = REG["Payroll"], REG["Acquisitions"]
    p = lambda k, m: f"Payroll!{mcol(m)}{PR[k]}"
    q = lambda k, m: f"Acquisitions!{mcol(m)}{AQ[k]}"
    g = REG[ws.title]
    R = lambda key, m: f"{mcol(m)}{g[key]}"
    t.section("1. THE PEOPLE ON THE PAYROLL")
    for fn in FUNCS:
        t.line(f"h_{fn}", fn, lambda m, fn=fn: p(f"fh_{fn}", m), NUM, total="end")
    t.line("tot", "Total headcount", lambda m: p("heads", m), NUM, total="end", bold=True)
    t.blank()
    t.section("2. ACTIVITY THE PLAN NEEDS, AGAINST ACTIVITY THE TEAM CAN RUN")
    rows = [("ev", "Ecosystem events attended", "ev", "cp_heads", "cap_ev"),
            ("mu", "Community meetups hosted", "mu", "cp_heads", "cap_mu"),
            ("ob", "Outbound contacts to institutions", "ob", "sdr_heads", "cap_ob"),
            ("dm", "Institutional demos", "i_dem", "ae_heads", "cap_demo"),
            ("cs", "New paying accounts to onboard", "newp", "cs_heads", "cap_cs")]
    for key, txt, aq, heads, cap in rows:
        t.line(f"{key}_p", f"{txt}, planned", lambda m, aq=aq: q(aq, m), NUM1)
        t.line(f"{key}_c", "Capacity, the people who can run it", lambda m, heads=heads, cap=cap:
               f"{p(heads, m)}*{A.c(cap, 'C')}+{p('fd_heads', m)}*{A.c(cap, 'D')}", NUM1, indent=1)
        t.line(f"{key}_h", "Headroom", lambda m, key=key: f"{R(key + '_c', m)}-{R(key + '_p', m)}", NUM1, indent=1)
    t.line("over", "Activity the plan asks for beyond what the team can run",
           lambda m: "+".join(f"MAX(0,{R(k + '_p', m)}-{R(k + '_c', m)})" for k, *_ in rows), NUM1, kind="check")
    t.line("util", "Activity utilisation",
           lambda m: f"IFERROR(({'+'.join(R(k + '_p', m) for k, *_ in rows)})/({'+'.join(R(k + '_c', m) for k, *_ in rows)}),0)", PCT, total="avg")
    note(ws, t.r, "The over capacity row should read nil in every month. Where it does not, the plan needs a hire earlier or less activity.")
    t.r += 2
    t.section("3. WHEN EACH ENGINE AND MARKET IS LIVE, 1 MEANS LIVE")
    for key, txt in [("o_pro", "Founder Pro"), ("o_team", "Founder Team"), ("o_sc", "Founder Custom"), ("o_ang", "Investor Angel"),
                     ("o_inst", "Investor Institutional"), ("o_ic", "Investor Custom")]:
        t.line(f"l_{key}", txt, lambda m, key=key: f"IF({m}>={A.s(key)},1,0)", NUM, total="end")
    import params as P
    for key, txt, *_ in P.GEO:
        t.line(f"l_{key}", txt, lambda m, key=key: f"IF({m}>={A.c(key, 'I')},1,0)", NUM, total="end")
    t.blank()
    t.section("4. FROM SPEND TO A PAYING ACCOUNT")
    for k, txt, fmt, tot in [("mk_sp", "Marketing and community spend", USD, "sum"), ("reg_new", "New registrations", NUM, "sum"),
                             ("f_actn", "Newly activated founders", NUM, "sum"), ("i_actn", "Newly activated investors", NUM, "sum"),
                             ("newp", "New paying accounts", NUM1, "sum"), ("paid", "Paying accounts", NUM, "end")]:
        t.line(f"s_{k}", txt, lambda m, k=k: q(k, m), fmt, total=tot)


# ---------------------------------------------------------------------------
def build_revenue(ws, A, REG):
    title(ws, "Revenue Streams", "Seven subscription engines and five add-ons. Every volume is an output of the funnel; every price comes from section 8 of the Assumption Setting.")
    set_time_widths(ws, 58)
    t = TS(ws, REG, 4)
    AQ = REG["Acquisitions"]
    q = lambda k, m: f"Acquisitions!{mcol(m)}{AQ[k]}"
    g = REG[ws.title]
    R = lambda key, m: f"{mcol(m)}{g[key]}"
    t.section("VOLUME, PRODUCED BY THE FUNNEL")
    for k, txt in [("a_pro", "Paying accounts, founder Pro"), ("a_team", "Paying accounts, founder Team"), ("a_sc", "Paying accounts, founder Custom"),
                   ("a_ang", "Paying accounts, investor Angel"), ("a_inst", "Paying accounts, investor Institutional"), ("a_ic", "Paying accounts, investor Custom")]:
        t.line(f"v_{k}", txt, lambda m, k=k: q(k, m), NUM2, total="end")
    t.blank()

    t.section("EFFECTIVE PRICE PER ACCOUNT PER MONTH, AFTER BILLING MIX, DISCOUNTS AND EGYPT PRICING",
              "Monthly and annual list prices blended by the share on annual plans, then price realization, then each market's price index weighted by where accounts come from.")
    import params as P
    region = lambda m: "(" + "+".join(f"{A.y(k, m)}*{A.c(k, 'H')}" for k, *_ in P.GEO) + ")"

    def eff(tk, share, m):
        return f"({A.y(tk + '_m', m)}*(1-{A.y(share, m)})+{A.y(tk + '_a', m)}*{A.y(share, m)})*{A.y('realize', m)}*{region(m)}"
    for key, tk, share, txt in [("p_pro", "s_pro", "ann_self", "Founder Pro"), ("p_team", "s_team", "ann_self", "Founder Team"),
                                ("p_sc", "s_cust", "ann_sales", "Founder Custom"), ("p_ang", "i_ange", "ann_self", "Investor Angel"),
                                ("p_inst", "i_inst", "ann_sales", "Investor Institutional, base"), ("p_ic", "i_cust", "ann_sales", "Investor Custom")]:
        t.line(key, txt, lambda m, tk=tk, share=share: eff(tk, share, m), USD2, total="avg")
    t.line("p_ix", "Investor Institutional, extra seats and portfolio companies per account",
           lambda m: f"({A.y('x_seats', m)}*{A.s('seat_p')}+{A.y('x_pc', m)}*{A.s('pc_p')})*{A.y('realize', m)}*{region(m)}", USD2, total="avg")
    t.blank()

    t.section("REVENUE BY STREAM")
    t.line("r_pro", "Founder Pro", lambda m: f"{R('v_a_pro', m)}*{R('p_pro', m)}", USD)
    t.line("r_team", "Founder Team", lambda m: f"{R('v_a_team', m)}*{R('p_team', m)}", USD)
    t.line("r_sc", "Founder Custom", lambda m: f"{R('v_a_sc', m)}*{R('p_sc', m)}", USD)
    t.line("r_ang", "Investor Angel", lambda m: f"{R('v_a_ang', m)}*{R('p_ang', m)}", USD)
    t.line("r_inst", "Investor Institutional, base", lambda m: f"{R('v_a_inst', m)}*{R('p_inst', m)}", USD)
    t.line("r_ix", "Investor Institutional, extra seats and companies", lambda m: f"{R('v_a_inst', m)}*{R('p_ix', m)}", USD)
    t.line("r_ic", "Investor Custom", lambda m: f"{R('v_a_ic', m)}*{R('p_ic', m)}", USD)
    sw = A.s("addons")
    t.line("n_val", "Analyst reviewed valuation reports sold", lambda m: f"{sw}*IF({m}>={A.s('o_val')},{q('f_paid', m)}*{A.s('ad_val_att')},0)", NUM2)
    t.line("r_ai", "Add-on, AI credit top ups", lambda m: f"{sw}*IF({m}>={A.s('o_ai')},{q('paid', m)}*{A.s('ad_ai_att')}*{A.s('ad_ai_p')},0)", USD)
    t.line("r_val", "Add-on, analyst reviewed valuation reports", lambda m: f"{R('n_val', m)}*{A.s('ad_val_p')}", USD)
    t.line("r_wl", "Add-on, white label licences", lambda m: f"{sw}*IF({m}>={A.s('o_wl')},{A.y('ad_wl_n', m)}*{A.s('ad_wl_p')}/12,0)", USD)
    t.line("r_spv", "Add-on, syndicate and SPV administration", lambda m: f"{sw}*IF({m}>={A.s('o_spv')},{A.y('ad_spv_n', m)}/12*{A.s('ad_spv_sz')}*{A.s('ad_spv_fee')},0)", USD)
    t.line("r_spon", "Add-on, event and data report sponsorship", lambda m: f"{sw}*IF({m}>={A.s('o_spon')},{A.y('ad_spon', m)}/12,0)", USD)
    t.line("rev", "Total revenue", lambda m: f"SUM({mcol(m)}{g['r_pro']}:{mcol(m)}{g['r_ic']})+SUM({mcol(m)}{g['r_ai']}:{mcol(m)}{g['r_spon']})", USD, bold=True)
    t.line("r_fs", "Founder subscriptions", lambda m: f"{R('r_pro', m)}+{R('r_team', m)}+{R('r_sc', m)}", USD)
    t.line("r_is", "Investor subscriptions", lambda m: f"{R('r_ang', m)}+{R('r_inst', m)}+{R('r_ix', m)}+{R('r_ic', m)}", USD)
    t.line("r_svc", "Add-ons and services", lambda m: f"{R('r_ai', m)}+{R('r_val', m)}", USD)
    t.line("r_plat", "Platform and partner", lambda m: f"{R('r_wl', m)}+{R('r_spv', m)}+{R('r_spon', m)}", USD)
    t.line("r_self", "Self serve subscription revenue, Pro, Team and Angel", lambda m: f"{R('r_pro', m)}+{R('r_team', m)}+{R('r_ang', m)}", USD)
    t.line("r_sales", "Sales led subscription revenue, Custom and Institutional", lambda m: f"{R('r_sc', m)}+{R('r_inst', m)}+{R('r_ix', m)}+{R('r_ic', m)}", USD)
    t.line("geo_f", "Regional price factor, weighted across markets", lambda m: region(m), PCT, total="avg")
    for k, txt, *_ in P.GEO:
        t.line(f"rg_{k}", f"Subscription revenue, {txt}", lambda m, k=k: f"({R('r_fs', m)}+{R('r_is', m)})*{A.y(k, m)}*{A.c(k, 'H')}/{R('geo_f', m)}", USD)
    t.line("r_ann", "Revenue from accounts on annual prepaid plans",
           lambda m: f"{R('r_self', m)}*{A.y('ann_self', m)}+{R('r_sales', m)}*{A.y('ann_sales', m)}", USD)


def build_total_revenue(ws, A, REG):
    title(ws, "Total Revenue", "The twelve engines gathered into four families, with MRR and ARR.")
    set_time_widths(ws, 54)
    t = TS(ws, REG, 4)
    RS = REG["Revenue Streams"]
    r = lambda k, m: f"'Revenue Streams'!{mcol(m)}{RS[k]}"
    g = REG[ws.title]
    R = lambda key, m: f"{mcol(m)}{g[key]}"
    t.section("REVENUE BY FAMILY")
    t.line("fs", "Founder subscriptions", lambda m: r("r_fs", m), USD, bold=True)
    for k, txt in [("r_pro", "Pro"), ("r_team", "Team"), ("r_sc", "Custom")]:
        t.line(k, txt, lambda m, k=k: r(k, m), USD, indent=1)
    t.line("is", "Investor subscriptions", lambda m: r("r_is", m), USD, bold=True)
    for k, txt in [("r_ang", "Angel"), ("r_inst", "Institutional, base"), ("r_ix", "Institutional, extra seats and companies"), ("r_ic", "Custom")]:
        t.line(k, txt, lambda m, k=k: r(k, m), USD, indent=1)
    t.line("svc", "Add-ons and services", lambda m: r("r_svc", m), USD, bold=True)
    for k, txt in [("r_ai", "AI credit top ups"), ("r_val", "Analyst reviewed valuation reports")]:
        t.line(k, txt, lambda m, k=k: r(k, m), USD, indent=1)
    t.line("plat", "Platform and partner", lambda m: r("r_plat", m), USD, bold=True)
    for k, txt in [("r_wl", "White label licences"), ("r_spv", "Syndicate and SPV administration"), ("r_spon", "Sponsorship")]:
        t.line(k, txt, lambda m, k=k: r(k, m), USD, indent=1)
    t.blank()
    t.line("rev", "Total revenue", lambda m: f"{R('fs', m)}+{R('is', m)}+{R('svc', m)}+{R('plat', m)}", USD, bold=True)
    t.line("sub", "Subscription revenue, MRR", lambda m: f"{R('fs', m)}+{R('is', m)}", USD)
    t.line("arr", "Annual recurring revenue, ARR, at the month end", lambda m: f"{R('sub', m)}*12", USD, total="end", bold=True)
    t.line("subsh", "Subscription share of revenue", lambda m: f"IFERROR({R('sub', m)}/{R('rev', m)},0)", PCT, total="avg")
    t.line("invsh", "Investor side share of subscription revenue", lambda m: f"IFERROR({R('is', m)}/{R('sub', m)},0)", PCT, total="avg")
    t.line("mom", "Month on month growth", lambda m: "0" if m == 1 else f"IFERROR({R('rev', m)}/{mcol(m - 1)}{g['rev']}-1,0)", PCT, total="avg")
    t.line("chk", "Check, families against the Revenue Streams total", lambda m: f"ROUND({R('rev', m)}-{r('rev', m)},2)", USD, kind="check")
