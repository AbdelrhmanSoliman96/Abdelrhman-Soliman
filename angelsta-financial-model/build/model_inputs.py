"""Assumption Setting sheet: everything typed lives here (plus the payroll establishment on Payroll)."""
import datetime
from xl import *
import params as P

ASN = "'Assumption Setting'"
YC = ["C", "D", "E", "F", "G"]


class Inputs:
    def __init__(self, ws):
        self.ws = ws
        self.r = 4
        self.k = {}
        title(ws, "Assumption Setting",
              "Everything typed in this model is on this sheet, except the payroll establishment, which sits on Payroll. Blue on yellow is an input; change it and the whole model moves.")
        ws.column_dimensions["A"].width = 60
        ws.column_dimensions["B"].width = 14
        for c in "CDEFG":
            ws.column_dimensions[c].width = 13
        for c in "HIJK":
            ws.column_dimensions[c].width = 14
        ws.column_dimensions["L"].width = 60

    # references -------------------------------------------------------
    def s(self, key):
        return f"{ASN}!$C${self.k[key]}"

    def y(self, key, m_or_year, is_month=True):
        yy = yr(m_or_year) if is_month else m_or_year
        return f"{ASN}!${YC[yy - 1]}${self.k[key]}"

    def c(self, key, col):
        return f"{ASN}!${col}${self.k[key]}"

    # writers -----------------------------------------------------------
    def section(self, text, sub=None):
        self.r += 1
        section(self.ws, self.r, text, 12)
        self.r += 1
        if sub:
            note(self.ws, self.r, sub)
            self.r += 1

    def yhdr(self, first="Item"):
        hdr(self.ws, self.r, [first, "Unit", "2027 Y1", "2028 Y2", "2029 Y3", "2030 Y4", "2031 Y5"])
        self.r += 1

    def single(self, key, text, unit, value, fmt=NUM, src=None):
        label(self.ws, self.r, text)
        label(self.ws, self.r, unit, col=2, size=8, color=GREY)
        put(self.ws, f"C{self.r}", value, fmt, kind="input")
        if src:
            note(self.ws, self.r, src, col=12)
        self.k[key] = self.r
        self.r += 1

    def yearly(self, key, text, unit, values, fmt=NUM, src=None):
        label(self.ws, self.r, text)
        label(self.ws, self.r, unit, col=2, size=8, color=GREY)
        for i, v in enumerate(values):
            put(self.ws, f"{YC[i]}{self.r}", v, fmt, kind="input")
        if src:
            note(self.ws, self.r, src, col=12)
        self.k[key] = self.r
        self.r += 1

    def calc(self, key, text, unit, formula, fmt=NUM):
        label(self.ws, self.r, text)
        label(self.ws, self.r, unit, col=2, size=8, color=GREY)
        put(self.ws, f"C{self.r}", formula, fmt, kind="calc")
        self.k[key] = self.r
        self.r += 1


def build_inputs(ws):
    A = Inputs(ws)
    # 1 ------------------------------------------------------------------
    A.section("1. MODEL BASIS")
    A.single("ccy", "Reporting currency", "", "USD", "@")
    A.single("start", "First calendar month of the model", "date", datetime.date(2027, 1, 1), DATE)
    A.single("egp", "Egyptian pounds to the dollar at the start", "EGP", 50.96, NUM2, "Same basis as the Btakka model, January 2027")
    A.single("egp_dep", "Annual change in the pound against the dollar", "%", 0.055, PCT)
    A.single("addons", "Add-on revenue switch, 1 on, 0 off. Base case is subscription only", "switch", 0, NUM,
             "Section 9 add-ons only earn when this is 1")

    # 2 ------------------------------------------------------------------
    A.section("2. THE OPENING POSITION AT 31 DECEMBER 2026, WHAT IS ALREADY TRUE",
              "Not forecasts. Replace with the closing figures at 31 December 2026 before the model is shared.")
    A.single("op_f_reg", "Registered founder workspaces on the platform", "#", 50, NUM, "Deck roadmap: first 50 founders onboarded in Q4 2026")
    A.single("op_i_reg", "Registered investor accounts on the platform", "#", 20, NUM, "Deck: 15 investor leads plus community sign ups")
    A.single("op_f_paid", "Paying founder accounts", "#", 0, NUM, "Paid plans go live in Q1 2027")
    A.single("op_i_paid", "Paying investor accounts", "#", 0, NUM)
    A.single("op_acc", "Accelerator and incubator partners signed", "#", 2, NUM)
    A.single("op_net", "Angel network and syndicate partners signed", "#", 1, NUM)
    A.single("op_cash", "Opening cash at 31 December 2026, equal to paid in capital", "USD", 15000, USD, "Placeholder, confirm with the founders")
    A.single("op_prod", "Founder capital already spent building the product, contributed as an intangible", "USD", 45000, USD,
             "Placeholder: engineering, design and four contractors to date. Non cash, capitalized in month 1")

    # 3 ------------------------------------------------------------------
    A.section("3. ACQUISITION, ONLINE CHANNELS",
              "Budget divided by cost per click gives paid clicks; organic and referral traffic lifts them; a share of clicks register. The last column splits registrations between founders and investors.")
    hdr(ws, A.r, ["Online channel, monthly budget", "Unit", "2027 Y1", "2028 Y2", "2029 Y3", "2030 Y4", "2031 Y5",
                  "Cost per click", "Organic uplift", "Click to sign up", "Share founders"])
    A.r += 1
    channels = [
        ("ch1", "LinkedIn Ads, founders and startup operators", [400, 900, 1500, 2200, 3000], 3.5, 0.15, 0.06, 1.0),
        ("ch2", "Meta and Instagram, founders", [300, 600, 1000, 1500, 2000], 0.6, 0.20, 0.025, 1.0),
        ("ch3", "Google Search, cap table and data room intent", [300, 700, 1100, 1600, 2200], 1.6, 0.10, 0.07, 1.0),
        ("ch4", "LinkedIn Ads, angels, family offices and fund managers", [400, 1000, 1700, 2500, 3400], 5.5, 0.15, 0.04, 0.0),
        ("ch5", "Google Search, portfolio management intent", [200, 500, 800, 1200, 1700], 2.5, 0.10, 0.05, 0.0),
        ("ch6", "SEO, newsletter and MENA private markets data reports", [300, 600, 1000, 1400, 1800], 0.35, 0.50, 0.02, 0.7),
    ]
    for key, name, bud, cpc, upl, conv, shf in channels:
        label(ws, A.r, name)
        label(ws, A.r, "USD", col=2, size=8, color=GREY)
        for i, v in enumerate(bud):
            put(ws, f"{YC[i]}{A.r}", v, USD, kind="input")
        put(ws, f"H{A.r}", cpc, USD2, kind="input")
        put(ws, f"I{A.r}", upl, PCT, kind="input")
        put(ws, f"J{A.r}", conv, PCT, kind="input")
        put(ws, f"K{A.r}", shf, PCT, kind="input")
        A.k[key] = A.r
        A.r += 1
    note(ws, A.r, "Cost per click: LinkedIn B2B in the GCC runs USD 3 to 7, Meta in Egypt under USD 1. Conversion reflects a free sign up, not a purchase.")
    A.r += 1

    # 4 ------------------------------------------------------------------
    A.section("4. ACQUISITION, EVENTS, COMMUNITY AND PARTNERS",
              "This is the engine room. Angelsta's cheapest sign ups come from the ecosystem: events, its own community circles, accelerators and angel networks.")
    A.yhdr("Offline and partner activity")
    A.yearly("ev_n", "Ecosystem events attended, Web Summit Qatar, LEAP, Biban, GITEX, RiseUp", "per month", [0.5, 0.75, 1, 1.25, 1.5], NUM2)
    A.single("ev_f", "Founder sign ups per event", "#", 30)
    A.single("ev_i", "Investor sign ups per event", "#", 10)
    A.yearly("ev_cost", "Cost per event attended, pass, booth share and travel", "USD", [1500, 1800, 2000, 2200, 2400], USD)
    A.yearly("mu_n", "Angelsta community meetups and founder investor circles hosted", "per month", [1, 2, 3, 4, 5], NUM1)
    A.single("mu_f", "Founder sign ups per meetup", "#", 10)
    A.single("mu_i", "Investor sign ups per meetup", "#", 5)
    A.yearly("mu_cost", "Cost per meetup, venue and hospitality", "USD", [300, 350, 400, 450, 500], USD)
    A.yearly("acc_n", "Accelerator and incubator partners active at year end", "#", [6, 12, 18, 24, 30])
    A.single("acc_f", "Startups onboarded per accelerator partner per month", "#", 2.5, NUM1)
    A.yearly("net_n", "Angel networks and syndicates active at year end", "#", [3, 6, 9, 12, 15])
    A.single("net_i", "Investors onboarded per angel network per month", "#", 3, NUM1)
    A.yearly("ob_n", "Outbound to institutions, contacts reached", "per month", [150, 350, 600, 850, 1100])
    A.single("inv_per_f", "Investors invited per newly activated founder, the cap table brings its investors", "#", 2.5, NUM1)
    A.yearly("inv_acc", "Share of invited investors who register", "%", [0.30, 0.32, 0.35, 0.38, 0.40], PCT)
    A.single("f_ref", "Founder referrals per active founder per month", "#", 0.01, NUM2)
    A.single("i_ref", "Founders referred into the platform per paying investor per month, deal flow", "#", 0.10, NUM2)

    # 5 ------------------------------------------------------------------
    A.section("5. THE FOUNDER FUNNEL, PRICED PER COMPANY",
              "A registration is worth nothing until the founder builds the cap table or opens a data room. Conversion is a monthly rate on the active free base.")
    A.yhdr("Founder funnel")
    A.yearly("f_act", "Registration to activated workspace", "%", [0.45, 0.48, 0.50, 0.52, 0.54], PCT)
    A.single("f_idle", "Monthly decay of the active free base, founders going quiet", "%", 0.03, PCT)
    A.yearly("f_conv", "Monthly self serve conversion of active free founders to paid", "%", [0.012, 0.014, 0.016, 0.018, 0.020], PCT,
             "Freemium benchmark 2.6 to 3.7 per cent within the first months; this is applied monthly to the base")
    A.yearly("f_promix", "Share of self serve conversions choosing Pro, the rest Team", "%", [0.85, 0.80, 0.77, 0.74, 0.72], PCT)
    A.single("f_demo", "Activated founders who book a demo", "%", 0.04, PCT)
    A.single("f_win", "Demo to paid, founders", "%", 0.30, PCT)
    A.single("f_cshare", "Share of founder demo wins on Custom, once open", "%", 0.15, PCT)
    A.yearly("ch_pro", "Monthly churn, founder Pro", "%", [0.045, 0.040, 0.035, 0.032, 0.030], PCT, "SMB SaaS 3 to 7 per cent a month")
    A.yearly("ch_team", "Monthly churn, founder Team", "%", [0.030, 0.026, 0.023, 0.020, 0.018], PCT)
    A.yearly("ch_sc", "Monthly churn, founder Custom", "%", [0.015, 0.012, 0.010, 0.010, 0.009], PCT)
    A.single("up_pt", "Monthly upgrades from Pro to Team", "%", 0.01, PCT)

    # 6 ------------------------------------------------------------------
    A.section("6. THE INVESTOR FUNNEL, PRICED PER ACCOUNT",
              "Angels convert self serve. Institutions, family offices, VC, PE and CVC, are sold: outbound contact, meeting, demo, pilot, contract.")
    A.yhdr("Investor funnel")
    A.yearly("i_act", "Registration to activated, holdings added", "%", [0.40, 0.43, 0.46, 0.48, 0.50], PCT)
    A.single("i_idle", "Monthly decay of the active free base, investors going quiet", "%", 0.03, PCT)
    A.yearly("i_conv", "Monthly self serve conversion of active free investors to Angel", "%", [0.015, 0.017, 0.019, 0.021, 0.023], PCT)
    A.yearly("i_c2m", "Outbound contact to meeting", "%", [0.05, 0.055, 0.06, 0.065, 0.07], PCT)
    A.single("i_m2d", "Meeting to demo", "%", 0.65, PCT)
    A.single("i_inst", "Share of activated investors who are institutions", "%", 0.15, PCT)
    A.single("i_inb", "Activated institutions who request a demo", "%", 0.20, PCT)
    A.single("i_lag", "Sales cycle, demo to signed contract", "months", 2)
    A.yearly("i_win", "Demo to signed contract, institutions", "%", [0.22, 0.25, 0.28, 0.30, 0.30], PCT)
    A.single("i_cshare", "Share of institutional wins on Custom, once open", "%", 0.15, PCT)
    A.yearly("ch_ang", "Monthly churn, investor Angel", "%", [0.035, 0.030, 0.027, 0.025, 0.023], PCT)
    A.yearly("ch_inst", "Monthly churn, investor Institutional", "%", [0.015, 0.013, 0.011, 0.010, 0.009], PCT, "Mid market 1 to 3, enterprise 0.5 to 1 per cent a month")
    A.yearly("ch_ic", "Monthly churn, investor Custom", "%", [0.010, 0.009, 0.008, 0.007, 0.007], PCT)
    A.single("up_ai", "Monthly upgrades from Angel to Institutional", "%", 0.003, PCT)
    A.yearly("x_seats", "Extra seats per Institutional account above the five included", "#", [1, 1.5, 2, 2.5, 3], NUM1)
    A.yearly("x_pc", "Extra portfolio companies per Institutional account above the fifty included", "#", [5, 8, 12, 15, 18], NUM1)

    # 7 ------------------------------------------------------------------
    A.section("7. CAPACITY, WHO RUNS THE ACTIVITY",
              "The activity plan is only credible if somebody on the payroll can run it. GTM Capacity and Timing tests every month.")
    hdr(ws, A.r, ["Activity", "Unit", "Per person", "Per founder"])
    A.r += 1
    for key, txt, a, b in [("cap_demo", "Institutional demos run, per account executive or head of sales", 25, 6),
                           ("cap_ob", "Outbound contacts reached, per sales development rep", 450, 100),
                           ("cap_ev", "Events covered, per community and partnerships head", 1, 0.3),
                           ("cap_mu", "Meetups hosted, per community and partnerships head", 4, 0.5),
                           ("cap_cs", "New paying accounts onboarded, per customer success head", 60, 10)]:
        label(ws, A.r, txt)
        label(ws, A.r, "per month", col=2, size=8, color=GREY)
        put(ws, f"C{A.r}", a, NUM1, kind="input")
        put(ws, f"D{A.r}", b, NUM1, kind="input")
        A.k[key] = A.r
        A.r += 1

    # 8 ------------------------------------------------------------------
    A.section("8. REVENUE, PRICING BY YEAR",
              "List prices in USD on the GCC list, per account per month. Every plan is sold monthly or annually; the annual plan is about 17 per cent cheaper. See the Pricing Strategy document.")
    A.yhdr("Price list, USD per account per month")
    for side, d, pre in [("Founder", P.STARTUP, "s"), ("Investor", P.INVESTOR, "i")]:
        for tier, v in d.items():
            if tier == "Free":
                continue
            tk = f"{pre}_{tier.lower()[:4]}"
            A.yearly(tk + "_m", f"{side} {tier}, monthly plan, per month", "USD", v["monthly"], USD)
            A.yearly(tk + "_a", f"{side} {tier}, annual plan, per month", "USD", v["annual"], USD)
    A.single("seat_p", "Institutional, extra seat per month", "USD", P.INST_EXTRA_SEAT, USD)
    A.single("pc_p", "Institutional, extra portfolio company per month", "USD", P.INST_EXTRA_PORTCO, USD)
    A.yearly("ann_self", "Share of self serve accounts on annual plans, Pro, Team and Angel", "%", P.ANNUAL_SHARE_SELF, PCT)
    A.yearly("ann_sales", "Share of sales led accounts on annual plans, Institutional and Custom", "%", P.ANNUAL_SHARE_SALES, PCT)
    A.yearly("realize", "Price realization after founding member and negotiated discounts", "%", P.PRICE_REALIZATION, PCT)
    A.yearly("eg_share", "Egypt share of paying accounts", "%", P.EGYPT_SHARE, PCT)
    A.single("eg_idx", "Egypt price list as a share of the GCC list", "%", P.EGYPT_PRICE_INDEX, PCT)
    note(ws, A.r, "Add-ons below earn only when the switch in section 1 is set to 1.")
    A.r += 1
    A.single("ad_ai_att", "AI credit top up packs bought per paying account per month", "#", 0.04, NUM2)
    A.single("ad_ai_p", "AI credit top up pack, 500 credits", "USD", 20, USD)
    A.single("ad_val_att", "Analyst reviewed valuation reports per paying founder per month", "#", 0.02, NUM2)
    A.single("ad_val_p", "Analyst reviewed valuation report", "USD", 249, USD)
    A.yearly("ad_wl_n", "White label licences live, accelerators, angel networks, banks", "#", [0, 1, 3, 5, 8])
    A.single("ad_wl_p", "White label licence per year", "USD", 6000, USD)
    A.yearly("ad_spv_n", "Syndicates and SPVs administered per year", "#", [0, 0, 4, 10, 18])
    A.single("ad_spv_sz", "Average SPV size", "USD", 400000, USD)
    A.single("ad_spv_fee", "SPV administration fee, one off", "%", 0.02, PCT)
    A.yearly("ad_spon", "Event and data report sponsorship per year", "USD", [0, 10000, 25000, 40000, 60000], USD)

    # 9 ------------------------------------------------------------------
    A.section("9. WHEN EACH ENGINE OPENS", "An engine earns nothing before the month it opens. Month 1 is January 2027.")
    hdr(ws, A.r, ["Engine or market", "Unit", "First month"])
    A.r += 1
    for key, txt, m in [("o_pro", "Founder Pro", 2), ("o_team", "Founder Team", 2), ("o_sc", "Founder Custom", 7),
                        ("o_ang", "Investor Angel", 2), ("o_inst", "Investor Institutional", 4), ("o_ic", "Investor Custom", 10),
                        ("o_ai", "Add-on, AI credit top ups", 6), ("o_val", "Add-on, analyst reviewed valuation reports", 4),
                        ("o_wl", "Add-on, white label licences", 13), ("o_spv", "Add-on, syndicate and SPV administration", 25),
                        ("o_spon", "Add-on, sponsorship", 13), ("o_ksa", "Market, Saudi Arabia", 7), ("o_uae", "Market, United Arab Emirates", 13),
                        ("o_gcc", "Market, Qatar and the wider GCC", 25)]:
        A.single(key, txt, "month", m)

    # 10 -----------------------------------------------------------------
    A.section("10. EXPENSES, DIRECT COST OF DELIVERY")
    A.yhdr("Direct cost driver")
    A.yearly("dc_pay", "Payment gateway and collection, share of revenue", "%", [0.029, 0.028, 0.027, 0.026, 0.025], PCT, "Stripe UAE 2.9% + AED 1; Paymob Egypt 2.75% + EGP 3")
    A.yearly("dc_app", "Share of subscriptions billed through the mobile app stores", "%", [0.05, 0.08, 0.10, 0.10, 0.10], PCT)
    A.single("dc_appfee", "App store commission on those subscriptions", "%", 0.15, PCT)
    A.yearly("dc_ai", "AI inference cost per AI credit", "USD", P.AI_COST_PER_CREDIT, '\\$#,##0.000')
    hdr(ws, A.r, ["AI credits used per account per month, average below the allowance", "Unit", "Credits"])
    A.r += 1
    for key, txt, v in [("ai_free", "Free account, active, either side", P.AI_USE["Free"]), ("ai_pro", "Founder Pro", P.AI_USE["S-Pro"]),
                        ("ai_team", "Founder Team", P.AI_USE["S-Team"]), ("ai_sc", "Founder Custom", P.AI_USE["S-Custom"]),
                        ("ai_ang", "Investor Angel", P.AI_USE["I-Angel"]), ("ai_inst", "Investor Institutional", P.AI_USE["I-Inst"]),
                        ("ai_ic", "Investor Custom", P.AI_USE["I-Custom"])]:
        A.single(key, txt, "credits", v)
    A.yhdr("Direct cost driver")
    A.yearly("dc_hf", "Hosting, storage and infrastructure per active free account per month", "USD", [0.08, 0.07, 0.06, 0.055, 0.05], USD2)
    A.yearly("dc_hp", "Hosting, storage and data rooms per paying account per month", "USD", [1.2, 1.1, 1.0, 0.95, 0.9], USD2)
    A.yearly("dc_data", "Market data and benchmark feeds per Institutional or Custom investor per month", "USD", [25, 25, 22, 20, 20], USD2)
    A.yearly("dc_sup", "Support of paying accounts, tools and outsourced tier one, per account per month", "USD", [1.5, 1.4, 1.3, 1.2, 1.1], USD2)
    A.single("dc_val", "Delivery cost per analyst reviewed valuation report", "USD", 80, USD)
    A.single("dc_wl", "Delivery cost of white label and SPV administration, share of that revenue", "%", 0.30, PCT)

    # 11 -----------------------------------------------------------------
    A.section("11. EXPENSES, REVENUE SHARE WITH PARTNERS", "Accelerators and angel networks are paid for the accounts they bring.")
    A.yhdr("Partner economics")
    A.yearly("ps_f", "Share of founder subscription revenue sourced by accelerator partners", "%", [0.15, 0.20, 0.22, 0.24, 0.25], PCT)
    A.yearly("ps_i", "Share of investor subscription revenue sourced by angel networks", "%", [0.08, 0.10, 0.12, 0.12, 0.12], PCT)
    A.single("ps_rate", "Partner revenue share on the revenue they source", "%", 0.15, PCT)
    A.yearly("comm", "Sales commission on sales led subscription revenue", "%", [0.08, 0.08, 0.07, 0.07, 0.06], PCT)

    # 12 -----------------------------------------------------------------
    A.section("12. EXPENSES, OPERATING COST DRIVERS", "Nothing here is a flat figure chosen to fit. Each line is per head, per account or a fixed monthly service.")
    A.yhdr("Operating cost driver")
    rows = [
        ("ox_desk", "Co working desk and office services, per employee per month", "USD", [70, 20, 20, 20, 20]),
        ("ox_rent", "Office rent, Cairo from year two and Riyadh from year three, per month", "USD", [0, 1500, 2500, 3500, 4500]),
        ("ox_util", "Utilities, internet and communications, per employee per month", "USD", [25, 28, 30, 32, 34]),
        ("ox_soft", "Software and tooling, per employee per month", "USD", [70, 80, 90, 95, 100]),
        ("ox_cloud", "Cloud base platform and third party APIs, fixed per month", "USD", [600, 1200, 2000, 2800, 3600]),
        ("ox_crm", "CRM, product analytics and data tools, per month", "USD", [250, 450, 700, 950, 1200]),
        ("ox_pros", "Prospecting and private markets databases, per month", "USD", [300, 500, 750, 1000, 1200]),
        ("ox_trav", "Travel, per commercial head per month, GCC coverage", "USD", [250, 300, 330, 360, 380]),
        ("ox_rec", "Recruitment cost per new hire", "USD", [350, 400, 450, 500, 550]),
        ("ox_train", "Training and enablement, per employee per year", "USD", [200, 250, 300, 350, 400]),
        ("ox_fin", "Outsourced finance, legal and audit, per month", "USD", [900, 1400, 2000, 2600, 3200]),
        ("ox_reg", "Regulatory, licensing and data protection compliance, per month", "USD", [300, 1200, 2200, 3000, 3800]),
        ("ox_sec", "Security testing and certification upkeep, SOC 2 and ISO 27001, per month", "USD", [0, 800, 1500, 2000, 2500]),
        ("ox_ins", "Insurance, bank charges and sundries, per month", "USD", [150, 300, 450, 600, 750]),
        ("ox_brand", "Brand, creative and content production, per month", "USD", [800, 1400, 2200, 3000, 3800]),
        ("ox_inc", "Partner incentives and referral credits, per month", "USD", [300, 700, 1200, 1700, 2200]),
        ("ox_onb", "Customer onboarding cost per new paying account", "USD", [10, 9, 8, 7, 6]),
    ]
    for key, txt, unit, vals in rows:
        A.yearly(key, txt, unit, vals, USD)
    A.yearly("ox_cont", "Contingency on operating cost", "%", [0.07, 0.06, 0.05, 0.05, 0.05], PCT)

    # 13 -----------------------------------------------------------------
    A.section("13. WORKING CAPITAL, FUNDING AND TAX",
              "The pre-seed ask is not typed. Funding and Use of Funds sizes it from the year one expense the model produces.")
    A.single("dso_self", "Days sales outstanding, self serve card billing", "days", 2)
    A.single("dso_sales", "Days sales outstanding, invoiced sales led accounts", "days", 30)
    A.single("dso_add", "Days sales outstanding, add-ons and partner revenue", "days", 30)
    A.single("dpo", "Days payable outstanding", "days", 30)
    A.single("dacc", "Accrued payroll, days outstanding", "days", 10)
    A.single("prepaid", "Average months still to deliver on an annual plan", "months", 5.5, NUM1)
    A.single("ps_buf", "Pre-seed: months of year one cash cost held as a buffer on top of year one", "months", 3, NUM1)
    A.single("ps_round", "Pre-seed: round the ask up to the nearest", "USD", 25000, USD)
    A.single("ps_m", "Month the pre-seed lands, January 2027 is month 1", "month", 1)
    A.single("sd_m", "Month the seed round lands", "month", 15)
    A.single("sd_n", "Months of net cash need the seed round is sized to fund", "months", 18)
    A.single("sd_round", "Seed: round up to the nearest", "USD", 50000, USD)
    A.single("sa_m", "Month the Series A lands", "month", 33)
    A.single("sa_n", "Months of net cash need the Series A is sized to fund, capped at month 60", "months", 24)
    A.single("sa_round", "Series A: round up to the nearest", "USD", 100000, USD)
    A.single("buffer", "Minimum cash buffer to hold", "USD", 50000, USD)
    A.single("tax", "Corporate income tax rate, Egypt", "%", 0.225, PCT)
    A.single("tax_m", "Month of the following year in which tax is paid", "month", 4)
    A.single("tax_loss", "Tax losses carried forward at inception", "USD", 0, USD)

    # 14 -----------------------------------------------------------------
    A.section("14. ASSETS, DRIVEN BY HEADCOUNT", "Platform development is expensed through payroll, not capitalized. Only the build to date is carried as an intangible.")
    hdr(ws, A.r, ["Per employee asset", "Unit", "Cost per unit", "Units per hire", "Life, months"])
    A.r += 1
    for key, txt, cost, units, life in [("as_lap", "Laptop", 900, 1, 36), ("as_mon", "Monitor and peripherals", 180, 1, 48),
                                        ("as_ph", "Mobile handset and line set up", 200, 1, 24), ("as_desk", "Desk and chair", 150, 1, 60)]:
        label(ws, A.r, txt)
        label(ws, A.r, "USD", col=2, size=8, color=GREY)
        put(ws, f"C{A.r}", cost, USD, kind="input")
        put(ws, f"D{A.r}", units, NUM, kind="input")
        put(ws, f"E{A.r}", life, NUM, kind="input")
        A.k[key] = A.r
        A.r += 1
    hdr(ws, A.r, ["Shared and intangible asset", "Type", "Month acquired", "Cost", "Life, months"])
    A.r += 1
    for key, txt, typ, m, cost, life in [
        ("sa_prod", "Product already built, founder investment to date", "Intangible", 1, f"={A.s('op_prod')}", 60),
        ("sa_ip", "Trademark, entity formation, IP and app store accounts", "Intangible", 1, 3000, 60),
        ("sa_ksa", "Saudi entity, MISA licence and commercial registration", "Intangible", 13, 12000, 60),
        ("sa_cert", "SOC 2 Type I and ISO 27001 initial certification", "Intangible", 18, 15000, 36),
        ("sa_cai", "Cairo office fit out", "Equipment", 13, 10000, 60),
        ("sa_ruh", "Riyadh office set up", "Equipment", 25, 8000, 60),
        ("sa_av", "Event booth, studio and community kit", "Equipment", 3, 2500, 36),
    ]:
        label(ws, A.r, txt)
        label(ws, A.r, typ, col=2, size=8, color=GREY)
        put(ws, f"C{A.r}", m, NUM, kind="input")
        if isinstance(cost, str):
            put(ws, f"D{A.r}", cost, USD, kind="calc")
        else:
            put(ws, f"D{A.r}", cost, USD, kind="input")
        put(ws, f"E{A.r}", life, NUM, kind="input")
        A.k[key] = A.r
        A.r += 1
    return A
