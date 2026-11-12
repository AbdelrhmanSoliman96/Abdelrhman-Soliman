"""Angelsta pricing strategy v2, with charts. Usage: python make_pricing_doc.py charts_dir out.docx"""
import sys
import json
import os
import params as P
import competitors as C
from docbase import Doc, GREY, ACCENT

CH, OUT = sys.argv[1], sys.argv[2]
N = json.load(open(os.path.join(CH, "model_numbers.json")))
fig = lambda n: os.path.join(CH, n)
S, I = P.STARTUP, P.INVESTOR


def usd(x):
    return "$0" if x == 0 else f"${x:,.0f}"


def m(x):
    return f"${x / 1e6:.1f}m" if abs(x) >= 1e6 else f"${x / 1e3:,.0f}k"


d = Doc("ANGELSTA  |  PRICING STRATEGY, FOUNDERS AND INVESTORS")
d.cover("Angelsta", "Pricing Strategy for Founders and Investors",
        "Freemium subscriptions, monthly or annual, for the operating system that founders and private investors share. Egypt first, then Qatar, then the GCC, open to any country",
        [["Item", "Detail"], ["Document", "Pricing strategy and the pricing inputs used by the 2027 to 2031 financial model"],
         ["Company", "Angelsta: the operating system for founders and private investors. A Cairo team selling to Egypt, Qatar and the GCC"],
         ["Version", "v2.0, November 2026. Adds market focus, charts, regional price lists and the full MENA, Africa and global landscape"],
         ["Currency", "US dollar list price. Local billing in EGP, QAR, SAR, AED, KWD, BHD and OMR"],
         ["Companion files", "Angelsta Competitor and Comparables Analysis; Angelsta Financial Model 2027 to 2031 v2.0"]])
d.contents(["Executive summary", "Market focus: Egypt, Qatar, the GCC, and any country", "What the market charges",
            "Startup and investor operating systems in MENA, Africa and the region", "Pricing principles", "Founder plans",
            "Investor plans", "Monthly and annual billing, and price by market", "Trials, demos and the sales motion",
            "Discounts and commercial policy", "Add-ons, switched off in the base case", "Unit economics by plan",
            "What the financial model projects from this pricing", "Risks and price tests", "References"])

# 1 ------------------------------------------------------------------------
d.h1("1. Executive summary")
d.para("Angelsta sells two products on one shared record. Founders get a workspace with the cap table, data room, investor updates, financial model, valuation and exit scenarios. "
       "Investors get a portfolio operating system with live holdings, MOIC, TVPI, DPI and IRR, stress tests and deal access. Both sides start free. Every free founder brings their investors, and every investor brings deal flow. "
       "Paid plans unlock the AI layer (valuations, scenarios, diligence and portfolio agents, matching) and the controls a raising company or a fund needs (permissions, NDA gating, audit trail).")
d.kpis([("$0", "free on both sides,\nforever"), ("$49", "founder Pro,\nannual, per month"), ("$65", "investor Angel,\nannual, per month"),
        ("$499", "Institutional,\n5 seats, 50 companies"), ("17%", "saved on every\nannual plan")])
d.kpis([(m(N["ask"]), "pre-seed, built from\nyear one expenses"), (f"Month {N['be_month']}", "monthly break even,\ninside year two"), ("36%", "of funds go to\nmarketing and community"),
        ("Cairo", "lean team, paid\nin EGP"), (m(N["arr"][4]), "ARR at the end\nof 2031")], fill="0E5A5F")
d.figure(fig("p1_price_ladder.png"), "The price list: every plan can be paid monthly or annually")
d.table([["Founders, priced per company", "Free", "Pro", "Team", "Custom"],
         ["Monthly plan, per month", "$0", usd(S["Pro"]["monthly"][0]), usd(S["Team"]["monthly"][0]), "From " + usd(S["Custom"]["monthly"][0])],
         ["Annual plan, per month", "$0", usd(S["Pro"]["annual"][0]), usd(S["Team"]["annual"][0]), "From " + usd(S["Custom"]["annual"][0])],
         ["Annual plan, per year", "$0", usd(S["Pro"]["annual"][0] * 12), usd(S["Team"]["annual"][0] * 12), "From " + usd(S["Custom"]["annual"][0] * 12)],
         ["How it is bought", "Sign up", "Self serve, 14-day trial", "Self serve or demo", "Demo and proposal"]],
        widths=[4.4, 2.2, 3.2, 3.6, 3.6], first_bold=True, caption="Founder price list, USD")
d.table([["Investors, priced per account", "Free", "Angel", "Institutional", "Custom"],
         ["Monthly plan, per month", "$0", usd(I["Angel"]["monthly"][0]), usd(I["Institutional"]["monthly"][0]) + " base", "From " + usd(I["Custom"]["monthly"][0])],
         ["Annual plan, per month", "$0", usd(I["Angel"]["annual"][0]), usd(I["Institutional"]["annual"][0]) + " base", "From " + usd(I["Custom"]["annual"][0])],
         ["Annual plan, per year", "$0", usd(I["Angel"]["annual"][0] * 12), usd(I["Institutional"]["annual"][0] * 12) + " base", "From " + usd(I["Custom"]["annual"][0] * 12)],
         ["Included", "5 holdings", "40 holdings, 2 seats", "50 companies, 5 seats", "Unlimited, multi fund"],
         ["How it is bought", "Sign up", "Self serve, 14-day trial", "Demo and 30-day pilot", "Demo, pilot, proposal"]],
        widths=[4.4, 2.2, 3.2, 3.6, 3.6], first_bold=True, caption="Investor price list, USD")
d.figure(fig("p10_upgrade_paths.png"), "Upgrade paths on each side of the platform")
d.para("The decisions that shape the model:", bold=True)
d.bullets([
    ("Separate price lists for founders and investors. ", "A startup buys one company workspace. An investor buys an account that holds many companies, so investor prices scale with seats and portfolio companies."),
    ("One Institutional plan for family offices, VC, PE, CVC and angel networks. ", "It scales with use, at $49 per extra seat and $10 per extra portfolio company."),
    ("Every plan is sold monthly or annually. ", "The annual plan saves about 17 per cent, which is two months free. The model assumes 25 per cent of self serve accounts pay annually in 2027, rising to 40 per cent, and 70 to 80 per cent of sales-led accounts."),
    ("Egypt first, then Qatar, then the GCC, and any country can subscribe. ", "Egypt bills from an EGP list at 60 per cent of list. Qatar and the GCC pay list. The rest of MENA and Africa pays 70 per cent. The rest of the world pays list, self serve."),
    ("Deliberately below the US tools. ", "Founder Pro is about a third of Carta or Pulley. Institutional sits at Zapflow Pro's level and below one Affinity seat per user. Prices rise 5 to 9 per cent a year from 2029."),
    ("Subscription only in the base case. ", "Add-ons are built into the model behind a switch that is off."),
])

# 2 ------------------------------------------------------------------------
d.h1("2. Market focus: Egypt, Qatar, the GCC, and any country")
d.para("Angelsta is SaaS. Anyone in any country can sign up, pay by card and use the platform from the first day. Sales, community and partnerships are sequenced, though, so the team's time goes where it can win first.")
d.figure(fig("c10_roadmap.png"), "Market entry sequence used in the financial model")
d.table([["Market", "Opens", "Why now", "Price list", "Share of paying accounts, 2027 to 2031"]] +
        [[g[1].split(",")[0], f"Month {g[4]}", w, f"{g[3]:.0%} of list", " / ".join(f"{x:.0%}" for x in g[2])] for g, w in zip(P.GEO, [
            "Home market; founding team, community and first 50 founders; USD 304m VC in 2025",
            "Web Summit Qatar network; QIA USD 3bn Fund of Funds with 12 managers in Doha; QDB and QSTP programmes",
            "Largest MENA market by deals, USD 1.72bn over 257 deals; OQAL 600+ angels",
            "USD 1.58bn over 231 deals; DIFC and ADGM fund managers",
            "Active family offices; served self serve and through partners",
            "Self serve from day one; Africa USD 4.1bn in 2025 incl. debt",
            "Self serve from day one; product-led, English and Arabic"])],
        widths=[2.8, 1.6, 6.6, 2.0, 4.0], font=7.8, first_bold=True, caption="Markets, timing and price lists")
d.figure(fig("c6_ecosystem.png"), "2025 startup funding by market", source="MAGNiTT FY2025; QDB and MAGNiTT; Partech Africa 2025")

# 3 ------------------------------------------------------------------------
d.h1("3. What the market charges")
d.para("Most private-market software is priced for US customers. Founder tools usually publish self serve prices, while institutional investor systems are usually quote-based and sales-led. The charts below set out what a MENA founder or investor compares Angelsta with.")
d.figure(fig("p3_founder_prices.png"), "Founder side: entry price of paid plans", width=15)
d.figure(fig("p4_investor_prices.png"), "Investor side: entry price of paid plans", width=15)
d.table([["Product", "Published or reported price", "Unit", "What it means for Angelsta"],
         ["Carta", "Launch free to 25 stakeholders; Build about $1,600 a year plus $80 per stakeholder after 20; Grow about $3,900", "Per company", "The global anchor; Pro is about a third of Build"],
         ["Pulley", "$1,200 to $3,500 a year, annual only", "Per company", "Team at $1,488 a year matches it and adds data room, valuation and AI"],
         ["Visible", "Founders $59 to $249 a month; investors quote based, reported about $449 a month", "Per company or firm", "Updates alone sell for $59 and up"],
         ["Foundersuite", "$745, $1,069 and $1,609 a year", "Per company", "Fundraising CRM only"],
         ["Equidam", "Advanced $412.25, Expert $1,063.25, 409A $1,990 a year", "Per company", "Valuation only; Angelsta includes 5 methods in Pro"],
         ["Papermark", "Free; EUR 24 Pro; EUR 59 Business; EUR 99 Data Rooms a month", "Per team", "Data room only"],
         ["Govy (Saudi Arabia)", "$24.99 a month flat", "Per company", "Lowest regional anchor; no AI, valuation or investor OS"],
         ["Capital Connect Africa", "Free base; $69.99 advisory; $99.99 valuation; $49.99 investor database", "Per service", "Africa readiness point services"],
         ["Affinity", "$2,000 to $2,700 per user a year", "Per user", "One seat costs a third of an Angelsta Institutional team"],
         ["Zapflow", "$99 a month for 1 user; $495 for 5; $3,995 for 15", "Seats", "Closest structural match to Institutional"],
         ["MAGNiTT", "$2,400 to $30,000+ a year", "Per firm", "Data, not a workspace; a partner as much as a competitor"],
         ["Dealroom, Tracxn, PitchBook", "$5,000 to $70,000+ a year", "Per team", "Data platforms, thin in MENA"],
         ["Standard Metrics, Vestberry, Rundit, Dynamo", "Quote based", "Per fund", "Enterprise portfolio monitoring"]],
        widths=[3.2, 6.2, 2.2, 5.6], font=7.6, first_bold=True, caption="Price benchmarks, founder and investor side")
d.figure(fig("p5_value_map.png"), "Value map: modules covered against entry price", width=15)

# 4 ------------------------------------------------------------------------
d.h1("4. Startup and investor operating systems in MENA, Africa and the region")
d.para("The landscape Angelsta prices into, by market. The full analysis, with 80 companies, scores and comparables, is in the companion Competitor and Comparables Analysis.")
rows = [["Company", "Market", "Side", "Category", "Pricing", "Note"]]
for nm, reg, hq, side, cat, threat, price, notev in C.DIRECTORY:
    if reg in ("Global",) or cat in ("Data room",):
        continue
    rows.append([nm, reg, side, cat, price, notev[:110]])
d.table(rows, widths=[3.0, 2.2, 1.4, 2.6, 2.8, 5.2], font=7, first_bold=True, caption="Regional and emerging-market operating systems, networks and alternatives")
d.figure(fig("c1_positioning.png"), "Positioning: founder-side against investor-side coverage", width=16.5)

# 5 ------------------------------------------------------------------------
d.h1("5. Pricing principles")
d.table([["Principle", "How it is applied"],
         ["Free is the growth engine, not a trial", "Free plans never expire. A free founder workspace invites its investors, and a free investor account receives updates and deal flow. The community stays free for every member."],
         ["Charge for each side's value metric", "Founders pay per company workspace. Institutions pay for seats and portfolio companies, which is how their workload grows."],
         ["Paid plans unlock AI and control", "Free accounts get a taste of every AI feature. Paid plans unlock volume, governance and the agents that do the analyst work."],
         ["AI credits as a fair-use guardrail", "Each plan has a monthly allowance. One credit is about one agent action; a valuation uses about 20 and a diligence memo about 60."],
         ["Price below the US tools, sell on outcomes", "Pro is about a third of Carta or Pulley. It is sold on a measurable outcome: a data room, model and valuation ready for diligence in days."],
         ["Local currency, local price", "EGP list in Egypt at 60 per cent; QAR, SAR, AED, KWD, BHD and OMR at list; the rest of MENA and Africa at 70 per cent."],
         ["One upgrade path per side", "Each step is triggered by a limit the customer can see, not by a feature hidden behind a sales call."]],
        widths=[4.5, 12.7], first_bold=True, font=8.2)

# 6 ------------------------------------------------------------------------
d.h1("6. Founder plans, priced per company")
d.table([["", "Free", "Pro", "Team", "Custom"],
         ["Who it is for", "Pre-seed founders setting up", "A startup raising its next round", "A funded startup with a finance lead", "Groups, holdcos, later stage"],
         ["Monthly plan, per month", "$0", "$59", "$149", "From $479"], ["Annual plan, per month", "$0", "$49", "$124", "From $399"],
         ["Annual plan, per year", "$0", "$588", "$1,488", "From $4,788"], ["Seats", "1", "3", "10", "Unlimited"],
         ["Cap table stakeholders", "Up to 15", "Up to 50", "Up to 150", "Unlimited"], ["ESOP, vesting, dilution", "View only", "Yes", "Yes", "Multi entity"],
         ["Secure data rooms", "1 room, 1 GB, 10 viewers", "3 rooms, 10 GB, NDA gating", "Unlimited, 100 GB, audit trail", "Retention, watermarks, SSO"],
         ["Guided valuation, 5 methods", "1 a quarter", "5 a month", "Unlimited", "Analyst sign-off option"],
         ["Exit and stress scenarios", "1", "3", "Unlimited", "Unlimited"], ["Financial model, 3 statements, 5 years", "Sample", "1 live model", "Unlimited, versions", "Custom templates"],
         ["Investor updates", "Monthly template", "Update Writer agent", "KPI linked, scheduled", "White label"],
         ["AI credits per month", "25", "300", "1,500", "4,000 or pooled"], ["AI investor matching", "Top 3 matches", "10 intros a month", "30 a month", "Unlimited"],
         ["Investor pipeline and CRM", "25 investors", "250", "Unlimited", "Unlimited, API"], ["Community", "Full", "Full", "Full", "Full"],
         ["Support", "Help centre", "Email, 48 hours", "Priority, 24 hours", "Success manager, SLA"],
         ["Trial and demo", "Not needed", "14-day trial, no card", "Trial or demo", "Demo and proposal"]],
        widths=[4.4, 2.6, 3.4, 3.4, 3.4], first_bold=True, font=7.6, caption="Founder plans and limits")

# 7 ------------------------------------------------------------------------
d.h1("7. Investor plans, priced per account")
d.table([["", "Free", "Angel", "Institutional", "Custom"],
         ["Who it is for", "Any investor following deals", "Active angels, syndicate leads", "Family offices, VC, PE, CVC, angel networks", "Multi fund managers, banks"],
         ["Monthly plan, per month", "$0", "$79", "$599 base", "From $1,799"], ["Annual plan, per month", "$0", "$65", "$499 base", "From $1,499"],
         ["Annual plan, per year", "$0", "$780", "$5,988 base", "From $17,988"], ["Seats", "1", "2", "5, then $49 each a month", "Unlimited"],
         ["Portfolio companies", "5", "40", "50, then $10 each a month", "Unlimited, multi fund"],
         ["MOIC, TVPI, DPI, RVPI, IRR", "MOIC", "Full, benchmarked", "Fund and LP level", "Custom metrics"], ["Valuation and waterfall", "1 a month", "15 a month", "Unlimited", "Audit-ready packs"],
         ["Stress testing and simulator", "Base case", "Unlimited", "Saved snapshots", "Custom shocks"],
         ["KPI collection from portfolio", "None", "Issuer-shared KPIs", "Request KPIs; founders join free", "Automated integrations"],
         ["AI agents: Diligence, Portfolio monitor, Deal scout", "Preview", "Diligence 10 memos, Deal scout", "All three, team", "Custom agents"],
         ["AI credits per month", "25", "500", "3,000", "8,000 or pooled"], ["Reports and LP packs", "None", "Personal", "LP pack, Arabic and English", "Branded LP portal"],
         ["Audit and permissions", "None", "Basic", "Full audit, roles", "SSO, SAML, data residency"],
         ["Trial and demo", "Not needed", "14-day trial", "Demo, 30-day pilot", "Demo, pilot, proposal"]],
        widths=[4.4, 2.6, 3.2, 3.6, 3.4], first_bold=True, font=7.6, caption="Investor plans and limits")
d.callout("Example Institutional bill", "A $50m VC fund in Doha with 7 users and 60 portfolio companies, paid annually: $499 base + 2 extra seats at $49 + 10 extra companies at $10 = $697 a month, or $8,364 a year. Billed in QAR at about QR 30,450 a year.")

# 8 ------------------------------------------------------------------------
d.h1("8. Monthly and annual billing, and price by market")
d.figure(fig("p2_annual_savings.png"), "What the annual plan saves each customer", width=14)
d.figure(fig("p6_regional_prices.png"), "Effective price by market, annual plan, USD per month", width=15)
FX = [("Egypt", "EGP", 50.96, 0.60), ("Qatar", "QAR", 3.64, 1.0), ("Saudi Arabia", "SAR", 3.75, 1.0), ("UAE", "AED", 3.6725, 1.0),
      ("Kuwait", "KWD", 0.307, 1.0), ("Bahrain", "BHD", 0.376, 1.0), ("Oman", "OMR", 0.385, 1.0), ("Rest of MENA and Africa", "USD", 1.0, 0.70), ("Rest of world", "USD", 1.0, 1.0)]
rows = [["Market", "Currency", "Pro monthly", "Pro annual, per month", "Team annual, per month", "Angel annual, per month", "Institutional annual, per month"]]
for mk, ccy, fx, idx in FX:
    dec = 1 if ccy in ("KWD", "BHD", "OMR") else 0
    fmt = (lambda v: f"{v:,.{dec}f}")
    rows.append([mk, ccy, fmt(59 * idx * fx), fmt(49 * idx * fx), fmt(124 * idx * fx), fmt(65 * idx * fx), fmt(499 * idx * fx)])
d.table(rows, widths=[3.6, 1.6, 2.2, 2.4, 2.4, 2.4, 2.6], font=7.8, first_bold=True, caption="Local currency price list, 2027, before rounding to price points")
d.note("FX: EGP 50.96 at January 2027 as in the model; GCC currencies at their dollar pegs. Local prices will be rounded to clean price points, for example EGP 1,499 for Pro annual.")

# 9 ------------------------------------------------------------------------
d.h1("9. Trials, demos and the sales motion")
d.table([["Plan", "Path to purchase", "Who sells it", "Cycle"],
         ["Founder Pro, Investor Angel", "14-day full trial, no card; in-product nudges at each limit; card checkout in local currency", "The product and growth marketing", "Same day to 30 days"],
         ["Founder Team", "Trial, or a booked 30-minute demo for funded companies", "Product and customer success", "2 to 4 weeks"],
         ["Investor Institutional", "Demo, then a 30-day guided pilot importing up to 15 holdings, then an annual proposal", "SDR books, Cairo account executive runs demo and pilot, founder joins in Qatar and the GCC", "6 to 10 weeks; model uses 2 months"],
         ["Custom, both sides", "Discovery, tailored demo, security review, proposal, contract", "Account executive with a co-founder; head of sales from 2029", "2 to 4 months"]],
        widths=[3.6, 6.4, 4.2, 3.0], first_bold=True, font=8)
d.para("The demo opens on a pre-loaded sample portfolio, then imports the prospect's own top three holdings live. Pilots convert best when the investor's own data is in the product by day 7.")

# 10 -----------------------------------------------------------------------
d.h1("10. Discounts and commercial policy")
d.table([["Policy", "Terms", "Where it sits in the model"],
         ["Monthly or annual billing", "Every plan, including Custom, monthly or annually; annual saves about 17 per cent", "Prices by tier and year; share of accounts on annual plans"],
         ["Price by market", "Egypt 60 per cent; Qatar and GCC list; rest of MENA and Africa 70 per cent; rest of world list", "Market mix and price index by market"],
         ["Founding member offer", "30 per cent off the first year for the first 150 paying accounts on each side", "Price realization 85 per cent in 2027, rising to 96 per cent"],
         ["Accelerator programme", "Cohort startups get Pro free for 3 months; partner earns 15 per cent of first-year revenue", "Partner-sourced share of founder revenue"],
         ["Angel network programme", "Members get 20 per cent off Angel; the network gets an Institutional seat bundle", "Partner-sourced share of investor revenue"],
         ["Price changes", "Launch prices held through 2028; 5 to 9 per cent a year from 2029; annual customers protected until renewal", "List price by year"],
         ["Refunds", "Monthly cancels at period end; annual refundable within 14 days", "Churn by tier"],
         ["Ecosystem bodies", "Up to 50 per cent off Team or Institutional for non-profit, university and government programmes", "Price realization"]],
        widths=[4.0, 7.2, 6.0], first_bold=True, font=8)

# 11 -----------------------------------------------------------------------
d.h1("11. Add-ons, switched off in the base case")
d.table([["Add-on", "Price", "Opens", "Notes"],
         ["AI credit top-up pack", "$20 per 500 credits", "Month 6", "For heavy diligence periods"], ["Analyst-reviewed valuation report", "$249", "Month 4", "Signed off by an Angelsta valuation analyst"],
         ["White-label licence", "$6,000 a year", "Month 13", "Accelerators, angel networks, banks"], ["Syndicate and SPV administration", "2 per cent of SPV size", "Month 25", "Needs a licensed partner or an FRA, QFC, CMA or FSRA licence"],
         ["Event and data report sponsorship", "$10k to $60k a year", "Month 13", "Community events and MENA data reports"]],
        widths=[4.2, 3.4, 2.0, 7.6], first_bold=True, font=8)

# 12 -----------------------------------------------------------------------
d.h1("12. Unit economics by plan")
d.figure(fig("p9_unit_economics.png"), "Price against cost to serve, 2027", width=15)
d.para("Gross margins run from about 85 to 89 per cent per plan because AI inference is metered through credits and the data room storage is shared infrastructure. The model's blended gross margin rises from 82 per cent in 2027 to 90 per cent in 2031 as AI cost per credit falls from $0.012 to $0.006.")

# 13 -----------------------------------------------------------------------
d.page_break()
d.h1("13. What the financial model projects from this pricing")
d.kpis([(m(N["ask"]), "pre-seed ask, built\nfrom year one cost"), (f"Month {N['be_month']}", "monthly break even,\ninside year two"), ("$0", "further capital\nneeded, base case"),
        (m(N["arr"][4]), "ARR at the end\nof 2031"), (f"{N['own']:.1%}", f"equity offered at\n{m(N['pre'])} pre-money")])
d.callout("Why the numbers work for an investor",
          f"A {m(N['ask'])} pre-seed, built from year one expenses of {m(N['y1'])}, reaches monthly break even in month {N['be_month']} (inside year two) and needs no further capital in the base case. "
          f"Marketing and community is the largest use of funds. The team is in Cairo and paid in Egyptian pounds, so each dollar of payroll goes three to four times further than in the Gulf. "
          f"The round is priced at {m(N['pre'])} pre-money, a 20 per cent discount to the model's fair value, for {N['own']:.1%} of the company.")
d.figure(fig("c13_break_even.png"), "Monthly revenue against monthly cash cost: break even in year two", width=16)
d.figure(fig("c12_use_of_funds.png"), "Use of funds: marketing and community is the largest line", width=14)
d.figure(fig("p7_revenue_by_plan.png"), "Revenue by plan, 2027 to 2031", width=15)
d.figure(fig("p8_revenue_by_market.png"), "Subscription revenue by market", width=15)
d.figure(fig("p11_funnel.png"), "The freemium funnel in 2029", width=14)
rows = [["Model input, USD per month"] + [str(y) for y in P.YEARS]]
for side, dd in [("Founder", S), ("Investor", I)]:
    for tier, v in dd.items():
        if tier == "Free":
            continue
        rows.append([f"{side} {tier}, monthly plan"] + [usd(x) for x in v["monthly"]])
        rows.append([f"{side} {tier}, annual plan, per month"] + [usd(x) for x in v["annual"]])
rows.append(["Self serve accounts on annual plans"] + [f"{x:.0%}" for x in P.ANNUAL_SHARE_SELF])
rows.append(["Sales-led accounts on annual plans"] + [f"{x:.0%}" for x in P.ANNUAL_SHARE_SALES])
rows.append(["Price realization after discounts"] + [f"{x:.0%}" for x in P.PRICE_REALIZATION])
for g in P.GEO:
    rows.append([f"Share of paying accounts, {g[1].split(',')[0]}"] + [f"{x:.0%}" for x in g[2]])
rows.append(["AI inference cost per credit"] + [f"${x:.3f}" for x in P.AI_COST_PER_CREDIT])
d.table(rows, widths=[6.7, 2.1, 2.1, 2.1, 2.1, 2.1], first_bold=True, font=7.4, caption="Pricing inputs on the Assumption Setting sheet, section 8")

# 14 -----------------------------------------------------------------------
d.h1("14. Risks and price tests")
d.table([["Risk", "Signal", "Response"],
         ["Free too generous; conversion under 1 per cent a month", "Activated free accounts never reach a limit", "Tighten Free to 10 stakeholders and 1 valuation every 6 months"],
         ["Egypt willingness to pay below 60 per cent", "Egypt trial-to-paid under half the Qatar rate", "EGP-only Pro Lite at 40 per cent, annual only"],
         ["Qatar and GCC institutional cycle longer than 2 months", "Pilots past day 45", "Fixed-scope pilot with data imported by Angelsta in week one"],
         ["Regional low-price anchors, Govy at $24.99", "Lost deals citing price", "Lead with valuation, model and investor side; Govy has neither"],
         ["AI cost per credit does not fall", "Inference over 8 per cent of revenue", "Route routine actions to smaller models; lower allowances"],
         ["Founder churn after the round closes", "Pro cancellations within 60 days of close", "Annual-only discount at close; Team bundles post-close reporting"]],
        widths=[5.0, 5.2, 7.0], first_bold=True, font=8)
d.para("Price tests in the first six months: Pro at $49 against $59 monthly; Institutional at $499 against $699 annual base; EGP Pro at EGP 999 against EGP 1,499; QAR Institutional at QR 1,799 against QR 2,199 a month. Each test runs six weeks with at least 300 trials per arm, or 20 pilots for Institutional.")

# 15 -----------------------------------------------------------------------
d.h1("15. References")
refs = [
    ("Angelsta SaaS Marketing Competitive Analysis, research cut-off 19 August 2026", "Supplied primary research: profiles, feature matrices, scoring, 11-module matrix, 77-entry directory, 36 source URLs"),
    ("Carta pricing and partner pricing", "carta.com/partners/partner-pricing ; costbench.com/software/equity-management/carta ; roundfunded.com/en/alternatives/carta"),
    ("Pulley", "pricingsaas.com/companies/pulley ; frontdeskreview.com/software/cap-table-management/pulley"),
    ("Cake Equity", "cakeequity.com/pricing ; costbench.com/software/equity-management/cake-equity"),
    ("Eqvista", "eqvista.com/pricing ; eqvista.com/support/premium-plan-pricing"),
    ("Visible", "visible.vc/pricing ; visible.vc/investor-pricing ; startupik.com review, September 2026"),
    ("Foundersuite, Equidam, Papermark, Capital Connect Africa", "foundersuite.com ; equidam.com ; papermark.com ; capitalconnect.africa/services"),
    ("Govy, RasMal, EquityList, Pentugram", "Supplied directory ; fintechnews.ae RasMal $4.8m pre-Series A ; wamda.com"),
    ("Affinity, Zapflow, Synaptic, FundCount", "affinity.co/product/pricing ; saasworthy.com/product/zapflow/pricing ; fundcount.com"),
    ("AngelList", "angellist.com/startups/pricing ; allocations.com AngelList fees 2026"),
    ("MENA venture funding 2025", "magnitt.com FY2025 MENA VC Report ; wamda.com 2025 year review ; arabnews.com"),
    ("Egypt venture funding 2025", "MAGNiTT via techcabal.com and enterpriseam.com ; Egypt planning ministry via ahram.org.eg ; Partech"),
    ("Qatar venture and QIA Fund of Funds", "qia.qa/en/Fund-of-Funds ; qna.org.qa ; gulf-times.com ; semafor.com ; QDB and MAGNiTT report"),
    ("Saudi Arabia and GCC", "MAGNiTT FY2025 Saudi report with SVC ; Stride Ventures GCC private debt via arabnews.pk"),
    ("Africa tech funding 2025", "partechpartners.com 2025 Africa Tech VC Report ; Briter Africa Investment Report"),
    ("Egypt angel networks", "Cairo Angels interview, cairoscene.com 2025 ; vc4a.com AUC Angels"),
    ("Freemium conversion benchmarks", "userpilot.com freemium SaaS ; crazyegg.com free-to-paid ; productled.com PLG benchmarks"),
    ("SaaS churn benchmarks", "shno.co SaaS churn benchmarks ; recurly.com churn research"),
    ("Payments in MENA", "ziina.com top payment gateways UAE ; dodopayments.com Paymob and Tap alternatives"),
    ("SaaS valuation multiples 2026", "aventis-advisors.com SaaS valuation multiples 2015 to 2026 ; multiples.vc ; SEG via saasrise.com"),
]
d.table([["Topic", "Source"]] + [[a, b] for a, b in refs], widths=[5.2, 12.0], font=7.4, first_bold=True, zebra=False)
d.note("Vendor prices are indications from vendor pages and aggregators; most institutional plans are quoted on request. Angelsta's live pricing page could not be reached during this research, so the deck's $79 and $199 plans are replaced by the plans above.")
d.save(OUT)
print("saved", OUT)
