"""Angelsta competitor and comparables analysis. Usage: python make_competitor_report.py charts_dir out.docx"""
import sys
import os
import json
import competitors as C
from docbase import Doc

CH, OUT = sys.argv[1], sys.argv[2]
N = json.load(open(os.path.join(CH, "model_numbers.json")))
fig = lambda n: os.path.join(CH, n)


def m(x):
    return f"${x / 1e6:.1f}m" if abs(x) >= 1e6 else f"${x / 1e3:,.0f}k"


d = Doc("ANGELSTA  |  COMPETITOR AND COMPARABLES ANALYSIS")
d.cover("Angelsta", "Competitor and Comparables Analysis",
        "Startup and investor operating systems across Egypt, Qatar, the GCC, MENA, Africa, the emerging markets and globally, and what buyers pay for them",
        [["Item", "Detail"], ["Scope", f"{len(C.DIRECTORY)} companies and alternatives; 34 mapped module by module; 12 scored on eight dimensions; transaction and valuation comparables"],
         ["Evidence base", "Angelsta SaaS Marketing Competitive Analysis (supplied, research cut-off 19 August 2026) as the controlling source, extended with public sources to November 2026"],
         ["Markets", "Egypt (home), Qatar (second), Saudi Arabia, UAE, Kuwait, Bahrain, Oman; rest of MENA and Africa; global self serve"],
         ["Prepared", "November 2026, as an investment analyst's view for the pre-seed round"],
         ["Companion files", "Angelsta Pricing Strategy v2.0; Angelsta Financial Model 2027 to 2031 v2.0"]])
d.contents(["Executive summary", "Scope, method and evidence", "The market: Egypt, Qatar, the GCC, MENA and Africa", "Market map and the fragmented workflow",
            "Competitive positioning and module coverage", "Competitive scoring", "Regional deep dives", "High-relevance competitor profiles",
            "Pricing benchmarks", "Threat assessment and battlecards", "Comparables: funding, transactions and multiples",
            "Market gaps and where Angelsta must prove itself", "Strategic implications for the round", "Full competitor and alternative directory", "References"])

# 1 -----------------------------------------------------------------------
d.h1("1. Executive summary")
d.kpis([(str(len(C.DIRECTORY)), "companies and\nalternatives mapped"), ("11 of 11", "modules Angelsta\ncovers"), ("9.5", "most by any rival,\nRasMal, Saudi Arabia"),
        (m(N["ask"]), "Angelsta pre-seed,\nfrom year one cost"), (f"Month {N['be_month']}", "Angelsta break even,\ninside year two")])
d.bullets([
    ("The workflow is fragmented. ", "No product in the region runs the whole chain from the founder's financial model and valuation, through the cap table, data room and fundraising, to the investor's diligence and portfolio monitoring. Most competitors cover two to five of the eleven modules. Angelsta's claim is the shared record across all of them."),
    ("The closest regional rival is RasMal and its investor arm Pentugram, in Saudi Arabia. ", "It covers about 9.5 of 11 modules, raised $4.8m pre-Series A at LEAP 2025 and has a Saudi Unicorns Programme seal. It is the competitor to plan against in the GCC, and it is not present in Egypt or Qatar."),
    ("The strongest global two-sided reference is Visible. ", "It scored 34 of 40 in the primary research, with 7,050+ founders and VC funds. It does not offer native financial modelling, valuation, MENA market analysis or stress testing, and it has no Arabic or regional presence."),
    ("Investor-side tooling is crowded and quote-based. ", "Standard Metrics, Vestberry, Rundit and Dynamo are mature, but they are sold to funds outside the region and priced on request. That leaves room for a transparent Institutional plan at $499 to $599 a month."),
    ("Founder-side cap table tools are price-anchored low in the region. ", "Govy sells at $24.99 a month flat. Angelsta should not try to win on cap table price. It should lead with the valuation, the model and the investor network."),
    ("Egypt and Qatar have no local operating system. ", "Egypt has angel networks (Cairo Angels, AUC Angels) and deal marketplaces, but no founder or investor OS. Qatar has capital (QIA's $3bn Fund of Funds, a record QR214m VC year) but no tooling. Both are open ground for a first mover."),
    ("Comparables support a disciplined valuation. ", f"2026 multiples are low: public SaaS at 3.2 to 3.4 times revenue and private SaaS M&A at 3.1 to 4.0 times. The model uses 4 times ARR at exit. The pre-seed is priced at {m(N['pre'])} pre-money for an ask of {m(N['ask'])}, which is {N['own']:.1%} and a 20 per cent discount to the model's fair value."),
    ("Capital efficient by design. ", f"Year one expenses of {m(N['y1'])}, a Cairo team paid in Egyptian pounds and marketing as the largest use of funds take Angelsta to monthly break even in month {N['be_month']}, inside year two, with no further round required in the base case."),
])
d.figure(fig("c1_positioning.png"), "Competitive positioning: Angelsta is the only product in the top right on both sides", width=16.5)

# 2 -----------------------------------------------------------------------
d.h1("2. Scope, method and evidence")
d.para("Angelsta is the benchmark, and every competitor is compared with its current SaaS scope. The supplied competitive analysis is the controlling evidence. Where it and later public sources differ, the supplied figures are kept, and the newer source is noted.")
d.table([["Type", "Meaning for Angelsta"], ["Direct or closest", "Covers substantial functionality across both startup and investor sides, or closely reproduces Angelsta's workflow"],
         ["Partial", "Competes strongly with one side or one major module: valuation, portfolio monitoring, market data, fundraising or data rooms"],
         ["Alternative", "Does not reproduce Angelsta as a platform but gets the same job done: spreadsheets, advisers, networks, marketplaces"],
         ["Partner or customer", "Angel networks, funds and ecosystem programmes that Angelsta sells to or through"]], widths=[4, 13.2], first_bold=True)
d.para("Module coverage uses the supplied 11-module matrix for 27 platforms. For seven more (Trackify, Capital Connect Africa, Dynamo, Clara, Equidam, Lemina and FundNaija), the coverage is an analyst mapping from the supplied startup-side and investor-side feature matrices. Scores are the supplied primary research scores (1 to 5 on eight dimensions). Prices are entry paid plans, on annual billing where offered.")

# 3 -----------------------------------------------------------------------
d.h1("3. The market: Egypt, Qatar, the GCC, MENA and Africa")
d.figure(fig("c6_ecosystem.png"), "2025 startup funding by market", source="MAGNiTT FY2025; QDB and MAGNiTT; Arab News; Partech Africa Tech VC Report 2025")
d.table([["Market", "2025 capital", "Ecosystem facts", "What it means for Angelsta"],
         ["Egypt, month 1", "USD 304m over 69 VC deals (MAGNiTT); USD 614m including debt (planning ministry)", "Cairo Angels, about 50 active angels; AUC Angels; 12 M&A exits in 2025", "Home market for founders; price at 60 per cent in EGP"],
         ["Qatar, month 4", "QR 214m, about USD 59m, a record, up 81 per cent", "QIA Fund of Funds raised to USD 3bn, more than USD 1bn committed, 12 managers in Doha; Rasmal Ventures; QDB, QSTP", "Institutional buyers arriving with no local tooling; Web Summit Qatar"],
         ["Saudi Arabia, month 10", "USD 1.72bn over 257 deals, 45 per cent of MENA funding", "OQAL 600+ angels; 65+ VC firms, angel groups and accelerators; RasMal and Govy local", "Biggest market and strongest local competition"],
         ["UAE, month 13", "USD 1.58bn over 231 deals", "DIFC and ADGM managers; MAGNiTT, Clara, Dynamo present", "Institutional and family office demand"],
         ["Kuwait, Bahrain, Oman, month 19", "Small, family office led; Bahrain USD 22m startup private debt", "Self serve and partners", "Self serve plus country lead"],
         ["Africa, self serve", "USD 4.1bn, equity USD 2.4bn over 462 deals, debt USD 1.6bn", "Kenya USD 1.04bn, South Africa USD 715m, Egypt USD 604m, Nigeria USD 572m", "Trackify, Capital Connect Africa, Lemina are early local rivals"]],
        widths=[2.6, 4.0, 5.4, 5.2], font=7.6, first_bold=True, caption="Market context by roll-out order")
d.figure(fig("c10_roadmap.png"), "Angelsta's market entry sequence")

# 4 -----------------------------------------------------------------------
d.h1("4. Market map and the fragmented workflow")
d.figure(fig("c5_market_map.png"), "Who is in the market, by category and region", width=16)
d.para("The map shows the structure. Equity management and FP&A tools cluster in the global and emerging-market columns. Angel networks and marketplaces cluster in Egypt and the GCC. Portfolio monitoring is split between enterprise global vendors and one regional player, Pentugram. No category in Egypt or Qatar has a software operating system.")
d.figure(fig("c9_workflow.png"), "The fragmented founder-to-investor workflow, and Angelsta's single record", width=16.5)

# 5 -----------------------------------------------------------------------
d.h1("5. Competitive positioning and module coverage")
d.figure(fig("c2_heatmap.png"), "Module coverage for 34 platforms", width=15)
rows = [["Platform", "Region", "Founder side, of 6", "Investor side, of 5", "Total, of 11", "Coverage basis"]]
for nm, v in sorted(C.COVER.items(), key=lambda kv: -C.coverage_score(kv[1][6])[2]):
    fs, is_, tot = C.coverage_score(v[6])
    rows.append([nm, v[0], f"{fs:.1f}", f"{is_:.1f}", f"{tot:.1f}", {"S12": "Supplied matrix", "A": "Analyst mapping", "Product scope": "Product scope"}[v[7]]])
d.table(rows, widths=[3.8, 3.0, 2.4, 2.4, 2.2, 3.4], font=7.4, first_bold=True, caption="Coverage scores, full module = 1, partial = 0.5", highlight=lambda r: r[0] == "Angelsta")

# 6 -----------------------------------------------------------------------
d.h1("6. Competitive scoring")
d.figure(fig("c3_scores.png"), "Scores out of 40 from the primary research", width=15.5)
d.figure(fig("c4_radar.png"), "The five highest-scoring competitors by dimension", width=12)
d.para("Visible leads on breadth, ease and price transparency. Trackify scores high on overlap but low on traction and pricing access. Standard Metrics, Dynamo and Vestberry score 5 on the investor side but 1.5 on the startup side. MAGNiTT and Clara score 5 on MENA relevance but are a data product and a legal and admin product. None scores above 3 on MENA relevance and above 4 on both sides at the same time, which is the position Angelsta is built for.")

# 7 -----------------------------------------------------------------------
d.h1("7. Regional deep dives")
groups = [("7.1 Egypt and North Africa", lambda r: r[1] in ("Egypt", "Egypt and MENA")),
          ("7.2 Qatar", lambda r: r[1] == "Qatar"),
          ("7.3 Saudi Arabia, UAE and the wider GCC", lambda r: r[1] in ("GCC", "Global and GCC", "MENA serving", "MENA")),
          ("7.4 Africa", lambda r: r[1] == "Africa"),
          ("7.5 Emerging markets: India, South East Asia, Europe", lambda r: r[1] == "Emerging markets")]
for ttl, fn in groups:
    d.h2(ttl)
    rows = [["Company", "HQ", "Side", "Category", "Threat", "Pricing", "Note"]]
    for r in C.DIRECTORY:
        if fn(r):
            rows.append([r[0], r[2], r[3], r[4], r[5], r[6], r[7]])
    d.table(rows, widths=[2.6, 1.9, 1.3, 2.3, 1.4, 2.3, 5.4], font=7, first_bold=True)
d.callout("Reading the regional tables", "Egypt and Qatar have capital and networks but no operating system, so Angelsta sells to and through Cairo Angels, AUC Angels, Rasmal Ventures, QDB and QSTP rather than against them. The GCC has the real software competition, from RasMal, Pentugram, Govy and EquityList, which are founder-side heavy apart from RasMal.")

# 8 -----------------------------------------------------------------------
d.h1("8. High-relevance competitor profiles")
d.table([["Company", "Type and geography", "Strongest overlap", "Facts, pricing, traction", "Gap against Angelsta"],
         ["Visible", "Direct, global", "Fundraising CRM, updates, data rooms, KPIs; investor portfolio monitoring", "Founded 2015; 7,050+ founders and funds; $0, $59, $129, $199 a month", "No native model, valuation, MENA market analysis or stress testing"],
         ["RasMal and Pentugram", "Direct, Saudi Arabia", "Cap table, ESOP, valuation, data rooms, deal flow and investor reporting", "Founded 2019; $4.8m pre-Series A at LEAP 2025; Saudi Unicorns Programme", "Not in Egypt or Qatar; no public pricing; limited AI agent layer"],
         ["Trackify", "Direct, Africa", "Founder OS and Investor OS", "1,000+ monthly active users reported", "Depth, security and pricing not verifiable"],
         ["Standard Metrics", "Direct investor side, global", "Portfolio data collection, KPIs, AI parsing, LP reporting", "$23.7m Series A 2022; 150+ firms, 10,000+ companies; SOC 2", "Post-investment only; sales-led pricing"],
         ["Dynamo", "Partial, global and UAE", "Institutional portfolio monitoring, valuation, reporting", "Since 1998; Dubai office 2022; quote based", "Enterprise, not founder-centric"],
         ["Govy", "Partial, Saudi Arabia", "Cap table, ESOP, governance, data room", "$24.99 a month flat", "No valuation, model or investor OS"],
         ["EquityList", "Partial, MENA serving", "Cap table, ESOP, valuations, data rooms", "$2.2m seed; Tabby a customer", "Quote pricing; no investor portfolio OS"],
         ["MAGNiTT", "Partial, UAE", "Startup, investor and deal data, benchmarks", "Since 2013; $2,400 to $30,000+ a year", "Data, not a workspace; a potential data partner"],
         ["Clara", "Partial, UAE", "Formation, legal docs, cap table, data room", "5,000+ businesses; acquired by Ascentium Feb 2026", "No model, valuation, KPIs or portfolio"],
         ["Capital Connect Africa", "Adjacent, Kenya", "Readiness, forecasts, valuation, investor matching", "Founded 2022; 5,200+ investors; $49.99 to $99.99 services", "Readiness, not ongoing portfolio"],
         ["Equidam", "Partial, global", "Valuation and projections", "160,000 companies valued; $412 to $1,990 a year", "Valuation point solution"],
         ["Carta", "Partial, global", "Cap table, 409A, fund admin", "$500m ARR 2025; $3.5bn secondary valuation", "US-centric pricing; no MENA presence or Arabic"]],
        widths=[2.4, 2.4, 3.8, 4.4, 4.2], font=7.2, first_bold=True)

# 9 -----------------------------------------------------------------------
d.h1("9. Pricing benchmarks")
d.figure(fig("p3_founder_prices.png"), "Founder side entry prices", width=14.5)
d.figure(fig("p4_investor_prices.png"), "Investor side entry prices", width=14.5)
d.figure(fig("p5_value_map.png"), "Value map: modules covered against entry price", width=15)
d.para("Founder tools publish self serve prices, between $25 and $163 a month. Institutional tools are quoted, and reported prices start at about $170 per user a month. Angelsta's Institutional plan publishes a price at the level of Zapflow's five-seat plan while covering eleven modules. The pricing strategy keeps that transparency as a deliberate edge.")

# 10 ----------------------------------------------------------------------
d.h1("10. Threat assessment and battlecards")
d.figure(fig("c11_threats.png"), "Threat level by region", width=14.5)
d.table([["Competitor", "Why it matters", "How Angelsta wins", "What to prove"],
         ["Spreadsheets, Drive, email", "The real incumbent everywhere, free", "One record replaces 3+ tools; the model, valuation and data room are built from data already entered", "Time saved per round; investor update cycle time"],
         ["RasMal and Pentugram", "Closest two-sided regional rival, Saudi backed", "Egypt and Qatar first; Arabic and English; AI agents; transparent pricing; the community", "SOC 2 and data residency before the KSA push"],
         ["Visible", "Strongest global two-sided brand", "Model, valuation, stress tests, MENA data, Arabic, local billing", "Investor adoption: founders invite investors for free"],
         ["Govy", "Low regional price anchor", "Do not compete on cap table price; lead with valuation and investor side", "Pro conversion triggered by the raise, not the cap table"],
         ["Carta and Pulley", "Global category owners", "A third of the price; regional legal templates; the investor network", "Migration tooling from Carta exports"],
         ["Standard Metrics, Vestberry, Rundit, Dynamo", "Mature investor-side tooling", "Published price; founders on the same record, so KPI collection costs nothing", "Pilot conversion; LP pack quality"],
         ["MAGNiTT", "Owns MENA venture data", "Partner for benchmarks rather than build data", "Data partnership terms"]],
        widths=[3.2, 3.8, 5.6, 4.6], font=7.4, first_bold=True)

# 11 ----------------------------------------------------------------------
d.h1("11. Comparables: funding, transactions and multiples")
d.figure(fig("c7_competitor_funding.png"), "Disclosed funding of regional and emerging-market competitors", width=14.5)
d.figure(fig("c8_comparables.png"), "Transaction comparables and 2026 revenue multiples", width=16.5)
d.table([["Comparable", "Year", "Value", "Relevance"]] + [[a, str(b), f"${c:,}m", e] for a, b, c, e in C.DEALS] +
        [[a, str(b), "Undisclosed", e] for a, b, e in C.DEALS_UNDISCLOSED],
        widths=[5.0, 1.4, 2.4, 8.4], font=7.6, first_bold=True, caption="Transaction comparables")
d.table([["Benchmark", "Multiple"]] + [[a, f"{b:.1f}x"] for a, b in C.MULTIPLES], widths=[12, 5], font=8, first_bold=True,
        caption="Revenue multiples, 2026", highlight=lambda r: r[0].startswith("Angelsta"))
d.table([["Private round comparable", "Stage", "Raised", "Read across"],
         ["RasMal, Saudi Arabia", "Pre-Series A, 2025", "$4.8m", "Regional two-sided equity platform; sets the GCC benchmark Angelsta must grow into"],
         ["Qapita, Singapore", "Series B, Oct 2025", "$26.5m, $79.3m total", "Emerging market equity management at scale"],
         ["Standard Metrics, USA", "Series A, 2022", "$23.7m", "Investor-side AI data collection"],
         ["Clara, UAE", "Seed", "about $3.5m, then acquired 2026", "MENA founder admin; exit to a strategic buyer"],
         ["EquityList, India and MENA", "Seed", "$2.2m", "Founder equity platform selling into MENA"],
         ["Angelsta, Egypt and Qatar", "Pre-seed, 2026", m(N["ask"]), f"{m(N['pre'])} pre-money, {N['own']:.1%} offered; built from year one cost"]],
        widths=[4.2, 3.0, 3.2, 6.8], font=7.6, first_bold=True, caption="Private funding comparables", highlight=lambda r: r[0].startswith("Angelsta"))
d.callout("What the comparables mean for the valuation",
          f"Buyers of private-markets software paid from about $90m (Pry) to $3.2bn (Preqin). In 2026, SaaS trades at 3.1 to 4.0 times revenue in private M&A. The model values Angelsta at exit on 4.0 times ARR ({m(N['arr'][4])} in 2031), "
          f"and prices the pre-seed at {m(N['pre'])} pre-money. That price is a weighted blend of discounted cash flow, the venture capital method, a scorecard against the MENA pre-seed median, and Berkus.")

# 12 ----------------------------------------------------------------------
d.h1("12. Market gaps, and where Angelsta must prove itself")
d.table([["Gap in the market", "Evidence", "Angelsta's answer"],
         ["Founder-to-investor data continuity", "Few products run model, valuation, KPIs, data room, diligence and monitoring together", "One shared record"],
         ["Modelling, valuation and readiness together", "Equidam (valuation), Foundersuite (fundraising) and Capital Connect Africa (readiness) each cover one part", "Model to valuation to investor pack, automated"],
         ["Investor-side risk and stress testing", "Strong only at Vestberry and Dynamo", "Issuer-published shocks and five-level stress tests"],
         ["Fragmented MENA specialisation", "Clara (legal), MAGNiTT (data), RasMal, Govy and EquityList (equity) each cover a piece", "Regional OS in Arabic and English"],
         ["Egypt and Qatar have no operating system", "Only networks, marketplaces and programmes", "First mover in both"]],
        widths=[4.6, 6.6, 6.0], font=7.8, first_bold=True)
d.para("Where Angelsta must prove itself:", bold=True)
d.bullets(["AI extraction is now common (Standard Metrics, Vestberry, Rundit, Dynamo, Visible, Trackify), so 'AI-powered' is not a differentiator on its own. The agents must show time saved.",
           "Security expectations are high. Standard Metrics and Papermark carry SOC 2 and ISO 27001, and the model funds certification in month 20.",
           "Spreadsheet compatibility matters. Excel and Sheets import and export must be first-class.",
           "Pricing is split: transparent for founders, quote-based for institutions. Angelsta publishes both, and must hold that line in enterprise deals."])

# 13 ----------------------------------------------------------------------
d.h1("13. Strategic implications for the round")
d.figure(fig("c13_break_even.png"), "Break even in year two on the pre-seed alone", width=16)
d.figure(fig("c12_use_of_funds.png"), "The pre-seed, sized from year one expenses, and where it goes", width=14)
d.bullets([
    ("Win Egypt and Qatar before RasMal arrives. ", "A lean Cairo team sells Egypt from month 1 and Qatar from month 4, with Cairo-based account executives and founders travelling to Doha, before Saudi Arabia in month 10."),
    ("Be profitable before the competition scales. ", f"The model breaks even in month {N['be_month']} on a {m(N['ask'])} pre-seed and needs no further capital. RasMal raised $4.8m to reach its stage; Angelsta's capital efficiency is its edge."),
    ("Spend the round on demand. ", "Marketing and community is 36 per cent of the use of funds, the largest line, because network effects reward the first platform to hold both founders and their investors."),
    ("Sell to the networks, not against them. ", "Cairo Angels, AUC Angels, OQAL, Rasmal Ventures and the QIA Fund of Funds managers are customers and channels."),
    ("Lead with valuation and the investor side. ", "That is where regional cap table tools are weakest and where Visible stops."),
    ("Partner with MAGNiTT for data. ", "Licensing benchmarks is cheaper than building them, and it removes a competitor from the investor-side pitch."),
    ("Certify early. ", "SOC 2 and ISO 27001 by month 20 and KSA data residency before the Saudi institutional push in 2029."),
])

# 14 ----------------------------------------------------------------------
d.landscape()
d.h1("14. Full competitor and alternative directory")
rows = [["Company", "Region", "HQ", "Side", "Category", "Threat", "Pricing", "Note"]]
order = {r: i for i, r in enumerate(C.REGION_ORDER)}
for r in sorted(C.DIRECTORY, key=lambda x: (order.get(x[1], 99), x[0])):
    rows.append(list(r))
d.table(rows, widths=[3.6, 2.4, 2.6, 1.5, 3.0, 1.6, 3.6, 7.2], font=6.8, first_bold=True, caption=f"All {len(C.DIRECTORY)} companies and alternatives")
d.portrait()

# 15 ----------------------------------------------------------------------
d.h1("15. References")
refs = [("Supplied primary research", "Angelsta SaaS Marketing Competitive Analysis, MENA, Africa, Global, research cut-off 19 August 2026, including its 36 source URLs (visible.vc, standardmetrics.io, clara.co, mytrackify.com, magnitt.com, dynamosoftware.com, capitalconnect.africa, lemina.co, fundnaija.com, rundit.com, vestberry.com, foundersuite.com, equidam.com, papermark.com)"),
        ("MENA venture 2025", "MAGNiTT FY2025 MENA VC Report, magnitt.com ; Wamda 2025 year review ; Arab News"),
        ("Egypt 2025", "MAGNiTT via TechCabal and Enterprise AM ; Egypt planning ministry via Ahram Online ; Cairo Angels interview, CairoScene ; VC4A, AUC Angels"),
        ("Qatar", "QIA Fund of Funds, qia.qa ; QNA ; Gulf Times ; Semafor ; QDB and MAGNiTT report via Gulf Times"),
        ("Saudi Arabia and GCC", "MAGNiTT Saudi FY2025 with SVC ; Stride Ventures GCC private debt via Arab News"),
        ("Africa", "Partech 2025 Africa Tech VC Report ; Briter Africa Investment Report 2025"),
        ("Competitor funding", "RasMal via Fintech News UAE, Finextra, Wamda ; Qapita via DealStreetAsia, YourStory, CB Insights ; Clara via MENAbytes, IBS Intelligence, Wamda ; Thndr via Arab Founders"),
        ("Transactions", "Morningstar 10-Q and 10-K, PitchBook ; supplied directory for Preqin, DocSend, Pry, Global Shares, Causal, Finmark"),
        ("Multiples", "Aventis Advisors SaaS Valuation Multiples 2015 to 2026 ; SEG via SaaSRise ; Multiples.vc"),
        ("Pricing", "Vendor pricing pages; CostBench; PricingSaaS; Capterra; G2; see the Pricing Strategy references")]
d.table([["Topic", "Source"]] + [[a, b] for a, b in refs], widths=[4.2, 13.0], font=7.4, first_bold=True, zebra=False)
d.note("Company-reported traction is shown as reported, not audited. Analyst mappings are marked as such. Missing fields are left missing, not estimated.")
d.save(OUT)
print("saved", OUT)
