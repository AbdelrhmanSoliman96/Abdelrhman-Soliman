"""
The business plan, as content blocks.

Prose lives here; rendering lives in scripts/build_business_plan_docx.py; every
number comes from model.py through the helpers below. Nothing numeric is typed into
a sentence, so a changed assumption changes the sentence, the table and the chart
together, or it changes none of them.

Block grammar
-------------
    ("h1", text)                       section opener, starts a page
    ("h2", text) / ("h3", text)        headings inside a section
    ("p", markup)                      paragraph; <b> is honoured
    ("lead", markup)                   the standfirst under an h1
    ("bul", [markup, ...])             bulleted list
    ("num", [markup, ...])             numbered list
    ("deflist", [(term, markup), ...]) a term and its explanation
    ("table", [heads], [[cells]], [widths_cm])
    ("fig", name, caption)             a PNG from business_plan/figures
    ("kpi", [(value, label), ...])     a row of statistic tiles
    ("note", markup)                   a tinted aside
    ("quote", markup)                  a pulled statement
    ("pb",)                            page break
"""
from . import model as MD
from .model import (AMBASSADORS, ANNUAL_GRADUATES, BOOTCAMP_DAYS, COHORT_PRICE,
                    COHORT_SIZE, COHORTS_PER_PAIR_PER_YEAR, COMPETITION_DIRECT,
                    COMPETITIONS_PER_YEAR, CORPORATES, ENGINE_NAMES,
                    FILTER_FACULTY_FIT, FILTER_INITIATIVE_SHARE, HE_STUDENTS,
                    INITIATIVE_SEATS_PER_YEAR, PLAN, PRICE_COHORT,
                    PRICE_COMPETITION, PRICE_CORPORATE, PRICE_FACULTY_LICENCE,
                    PRICE_INITIATIVE_SEAT, PRICE_PRO_YEAR, PRICE_SEAT,
                    PRICE_TEAM_YEAR, PRICE_TOT_COHORT, PROGRAMMES,
                    cohort_unit_economics, costs, engine_economics,
                    facilitator_capacity, funding, headcount, market, pipeline,
                    projection, revenue, subscriptions)

M = market()
PROJ = projection()
R1, R2, R3 = revenue(1), revenue(2), revenue(3)
C1 = costs(1)
UE = cohort_unit_economics()
FUND = funding()
HC_BY_FN, HC = headcount()
CAP = facilitator_capacity()
EE = {r["name"]: r for r in engine_economics()}
SUBS = subscriptions(1)
PIPE = pipeline()

Y1_COHORTS = R1["detail"]["cohorts"] / COHORT_PRICE[1]


def money(v):
    if abs(v) >= 1e6:
        return f"${v/1e6:,.1f}m"
    if abs(v) >= 1e3:
        return f"${v/1e3:,.0f}k"
    return f"${v:,.0f}"


def usd(v):
    return f"${v:,.0f}"


def n(v, dp=0):
    return f"{v:,.{dp}f}"


def pct(v, dp=0):
    return f"{v*100:,.{dp}f}%"


def share(engine, year=1):
    r = {1: R1, 2: R2, 3: R3}[year]
    return pct(r["lines"][engine] / r["total"])


TITLE = "Business Plan"
SUBTITLE = "Egypt and Saudi Arabia · Years one to three"
PERIOD = "October 2026 – September 2029"

SECTIONS = []


def section(name, blocks):
    SECTIONS.append((name, blocks))


# =====================================================================
section("Executive summary", [
    ("lead", "StartPad sells readiness to organisations that need a group of young "
             "people prepared — universities, national initiatives, competition "
             "sponsors, corporates and startup programmes. Founders who pay for "
             "themselves are the smallest line in the plan and a consequence of "
             "the others, not a channel. This document sets out the six engines, "
             "what each is worth, and what has to be true operationally to run "
             "them."),

    ("kpi", [(money(M["tam"]), "TAM · Egypt and KSA"),
             (money(M["sam"]), "SAM · reachable, with a budget"),
             (money(R1["total"]), "Year-one revenue"),
             (pct(R1["institutional_share"]), "Institutional")]),

    ("h2", "Six engines, and they are not equal"),
    ("fig", "revenue_engines", "Revenue by engine across three years. The business "
                               "is institutional in every year; subscriptions never "
                               "become the point."),
    ("table",
     ["Engine", "Who signs the contract", "Year 1", "Year 3", "Share, Y3"],
     [[e, who, money(R1["lines"][e]), money(R3["lines"][e]), share(e, 3)]
      for e, who in zip(ENGINE_NAMES, [
          "A dean, an entrepreneurship centre or a capstone coordinator",
          "A ministry, a donor or a national programme office",
          "A bank, a telco, a ministry or a foundation",
          "A corporate CSR or innovation budget holder",
          "An incubator or accelerator director",
          "The founder, out of their own pocket"])] +
     [["Total", "", money(R1["total"]), money(R3["total"]), "100%"]],
     [4.0, 5.0, 2.2, 2.2, 1.8]),

    ("h2", "The business in six sentences"),
    ("num", [
        "StartPad takes a first-time founder from a raw idea to a live product "
        "through <b>fifteen sequenced missions</b>, each reviewed by an AI before "
        "the next unlocks, with 121 tools mapped to the journey.",
        f"The flagship product is a <b>cohort</b>: {usd(PRICE_COHORT)} buys a "
        f"{BOOTCAMP_DAYS}-day in-person bootcamp for {COHORT_SIZE} students, a "
        f"platform seat for each of them, judging, and a cohort report the "
        f"institution can act on.",
        "Above that sits the <b>scale engine</b> — sponsored seats inside national "
        "initiatives that have publicly committed to qualifying a million "
        "entrepreneurs and have no method, platform or reporting line to do it "
        "with.",
        f"Beside both sit <b>sponsored competitions</b>, where a bank or a ministry "
        f"pays for the platform to run entry, qualification and judging — turning "
        f"what most companies treat as a marketing cost into a "
        f"{share(ENGINE_NAMES[2], 3)} revenue line.",
        f"Year one delivers {Y1_COHORTS:.0f} paid cohorts, "
        f"{n(PLAN['initiative_seats'][1])} sponsored seats and "
        f"{PLAN['competitions'][1]} competitions for {money(R1['total'])} against a "
        f"loss of {money(-PROJ[0]['profit'])}; breakeven comes in year two and a "
        f"{pct(PROJ[2]['profit']/PROJ[2]['revenue'])} operating margin in year "
        f"three.",
        f"The raise is {money(FUND['rounded'])}, which is small for a business "
        f"reaching {money(PROJ[2]['revenue'])} because every institutional engine "
        f"invoices before it delivers.",
    ]),

    ("pb",),
    ("h2", "Why subscriptions are the smallest line, and should be"),
    ("p", f"A founder subscription is worth "
          f"{usd(EE['Founder subscriptions']['ltv'])} over its life. A national "
          f"initiative partnership is worth {money(EE['Initiative seats']['ltv'])}. "
          f"One costs {usd(EE['Founder subscriptions']['cac'])} to win and the "
          f"other {money(EE['Initiative seats']['cac'])} — a ratio of 1 to "
          f"{EE['Initiative seats']['cac']/EE['Founder subscriptions']['cac']:,.0f} "
          f"on effort, against a value ratio of 1 to "
          f"{EE['Initiative seats']['ltv']/EE['Founder subscriptions']['ltv']:,.0f}. "
          f"The institutional deal returns more than twenty times as much per unit "
          f"of effort spent winning it."),
    ("fig", "engine_economics", "What it costs to win each kind of customer, "
                                "against what that customer is worth over its "
                                "life. The scale is the argument."),
    ("p", "This is not an argument for abandoning subscriptions. It is an argument "
          "about where they come from. "
          f"{pct(sum(r['paid'] for r in SUBS['rows'] if not r['name'].startswith('Organic'))/SUBS['paid'])} "
          "of year-one subscribers are people StartPad first met inside a cohort, a "
          "competition or a sponsored programme — they completed ten missions with "
          "an organisation paying, then paid themselves to finish the last five. "
          "Acquiring the same person cold through advertising costs more than they "
          "are worth."),

    ("h2", "What this plan concludes"),
    ("deflist", [
        ("Sell to the budget holder, not the beneficiary",
         "In both markets the person who benefits — a student — has almost no "
         "money, and the person with the budget — a dean, a ministry, a bank's CSR "
         "committee — has a reporting problem StartPad solves. Every engine in "
         "this plan is built on that asymmetry."),
        ("Competitions are revenue, not marketing",
         f"A competition sponsored at {usd(PRICE_COMPETITION[1])} with "
         f"{pct(1 - COMPETITION_DIRECT/PRICE_COMPETITION[1])} gross margin reaches "
         f"roughly 700 entrants, every one of whom opens an account, and leaves "
         f"behind both a university relationship and a sponsor relationship. "
         f"Treating it as an acquisition cost gets the sign wrong."),
        ("The binding constraint is facilitators, not demand",
         f"The year-one plan peaks at {CAP[-1]['facilitators']:.0f} facilitators in "
         f"the final quarter, and a certified pair runs "
         f"{COHORTS_PER_PAIR_PER_YEAR} cohorts a year. Certification is the first "
         f"operational priority, ahead of sales — and the seat and competition "
         f"engines matter partly because they scale <b>past</b> that constraint."),
    ]),

    ("h2", "The shape of the three years"),
    ("fig", "pl", "Revenue against operating cost. Year one is funded; year two "
                  "pays for itself; year three carries the margin."),
    ("table",
     ["", "Year 1 · 2026/27", "Year 2 · 2027/28", "Year 3 · 2028/29"],
     [["Revenue"] + [money(y["revenue"]) for y in PROJ],
      ["Institutional share"] + [pct(y["institutional_share"]) for y in PROJ],
      ["Operating cost"] + [money(y["cost"]) for y in PROJ],
      ["Result"] + [("−" if y["profit"] < 0 else "+") + money(abs(y["profit"]))
                    for y in PROJ],
      ["Operating margin"] + [pct(y["profit"] / y["revenue"]).replace("-", "−")
                              for y in PROJ],
      ["Employees at year end"] + [n(y["headcount"]) for y in PROJ]],
     [4.2, 4.0, 4.0, 4.0]),
    ("note", "Every figure in this plan is computed from one assumption set, held "
             "in <b>business_plan/model.py</b> and listed in full in the appendix. "
             "No number is typed into a sentence; change an assumption and the "
             "sentence, the table and the chart move together."),
])

# =====================================================================
section("The company and the product", [
    ("lead", "What StartPad is, and why a sequenced journey with a review gate is "
             "something an institution will pay for when a library of templates is "
             "not."),

    ("h2", "The problem"),
    ("p", "Ideas are everywhere in MENA. A path to a real startup is not. The gap "
          "is method: founders have graduation projects and no process; "
          "institutions need founders who are ready and have no way to prepare "
          "them; programmes screen applicants who never did the groundwork."),
    ("kpi", [("21%", "of self-described MENA startups meet the minimum criteria "
                     "to be considered investable"),
             ("56%", "of MENA pre-seed startups never reach the next stage"),
             ("68%", "failure rate in Egypt for startups trying to reach "
                     "Series A — the highest in the region")]),
    ("p", "These are one failure, not three. A founder who never defined the "
          "problem precisely cannot produce evidence; without evidence they fail a "
          "screen; having failed, they conclude the problem was capital. StartPad "
          "intervenes at the first step, which is the only step where intervention "
          "is cheap — and it is also the step every institution in this plan is "
          "already trying and failing to deliver."),

    ("h2", "The product"),
    ("p", "Fifteen missions across five phases. Each has a brief, a short lesson, "
          "five tasks with an explicit standard for what a good answer needs, and "
          "an evidence slot. The founder submits; an AI reviews against "
          "specificity, depth, evidence, actionability and relevance; at 70% the "
          "next mission unlocks. Below 70% they get one highest-gain fix and a full "
          "report, with answers kept for the retry."),
    ("table",
     ["Phase", "Missions", "Points", "Est. time", "What it produces"],
     [["Discovery", "01–03", "350", "4–6 h", "A prioritised problem worth solving"],
      ["Validation", "04–06", "550", "5–7 h", "A tested problem–solution canvas"],
      ["Business model", "07–09", "850", "11–19 h",
       "A full BMC and a working prototype"],
      ["Build and MVP", "10–13", "1,350", "29–54 h", "A shipped MVP with analytics"],
      ["Launch", "14–15", "950", "15–30 h", "A live launch and first customers"]],
     [3.0, 2.0, 1.8, 2.2, 7.2]),
    ("p", "4,050 points across the journey. Points and scores are written only on "
          "the server with direct writes revoked at the database, so a score is "
          "earned rather than claimed — which is what lets an institution treat the "
          "record as evidence and a ministry put it in a report."),

    ("h2", "What makes it sellable to an institution"),
    ("deflist", [
        ("It produces a reporting line, not a completion rate",
         "Cohort progress, review states, evidence and follow-up signals, with a "
         "downloadable cohort report. Every buyer in this plan has somebody they "
         "report to — a dean to an accreditation body, a programme office to a "
         "ministry, a CSR team to a board, a sponsor to its marketing committee. A "
         "course certificate satisfies none of them."),
        ("The sequence is the product",
         "A mission unlocks only when the last one passes. That constraint "
         "separates this from a library of templates: a founder cannot skip to the "
         "pitch deck before they have a tested problem, which is precisely the "
         "mistake the 56% figure measures."),
        ("The AI is a co-founder, not a ghostwriter",
         "It asks the follow-up a good mentor would ask and pushes back on vague "
         "answers. It does not write the plan. A tool that writes the answer "
         "destroys the only asset the product creates, which is a founder who can "
         "defend their own work in front of a judge."),
        ("Built in MENA, in both languages",
         "Every mission, review and exported PDF works in Arabic with complete "
         "right-to-left layout, composed rather than translated — Egyptian "
         "colloquial for Egypt, Saudi dialect for the Kingdom. A ministry cannot "
         "circulate a report it cannot read."),
    ]),
    ("fig", "flywheel", "Growth compounds through the loop: founders who progress "
                        "become the stories that win the next campus, the next "
                        "sponsor and the next programme."),
])

# =====================================================================
section("Market study", [
    ("lead", "How large each engine is, built from the bottom up — from counted "
             "institutions, counted programmes and counted competitions at our own "
             "prices, rather than from a share of somebody else's market report."),

    ("h2", "Method"),
    ("p", "A top-down sizing would start from a global edtech figure and take a "
          "percentage. That produces a large number and no information. This "
          "sizing instead counts, for each engine, <b>the organisations that sign "
          "the contract</b> — buying units, national programmes, competitions, "
          "corporates, incubators — applies the filters that decide whether each "
          "can plausibly buy, and multiplies by our own prices."),
    ("p", "The buyer, not the beneficiary, is the unit of counting. That is the "
          "single most important methodological choice in this plan, and it is why "
          "the subscription line — which looks largest if you count students — "
          "turns out to be the smallest engine once you count who actually pays."),

    ("h2", "The buyer universe"),
    ("table",
     ["Universe", "Count", "Basis"],
     [["Institutional buying units", n(M["units"]),
       "951 in Egypt (551 CAPMAS public colleges plus private faculties), 564 in "
       "KSA. The buying unit is the college — three of the four doors sit below "
       "university level"],
      ["National initiative seats a year", n(INITIATIVE_SEATS_PER_YEAR),
       "Addressable across both markets at steady state, far below the stated "
       "million-scale targets"],
      ["Youth competitions a year", n(COMPETITIONS_PER_YEAR),
       "Run by universities, banks, telcos, ministries and foundations"],
      ["Large corporates", n(CORPORATES),
       "With a CSR, innovation or youth budget line"],
      ["Incubators and startup programmes", n(PROGRAMMES),
       "That select applicants and would benefit from a prepared pool"],
      ["Students and recent graduates", n(M["people"]),
       "CAPMAS 2024/25 and UNESCO UIS, plus three graduating years"]],
     [4.4, 2.2, 9.4]),

    ("h2", "TAM and SAM, engine by engine"),
    ("fig", "tam_sam", "Each engine sized separately. The institutional engines are "
                       f"{pct(M['inst_sam']/M['sam'])} of the serviceable market."),
    ("table",
     ["Engine", "TAM basis", "TAM", "SAM"],
     [[r["engine"], r["tam_basis"], money(r["tam"]), money(r["sam"])]
      for r in M["rows"]] +
     [["Total", "", money(M["tam"]), money(M["sam"])]],
     [4.2, 6.2, 2.1, 2.1]),
    ("note", f"The subscription line has the largest TAM on paper — "
             f"{money(M['rows'][-1]['tam'])}, because there are millions of "
             f"students and in principle any of them could pay. It is the least "
             f"realisable number in the table, and the engine economics show why: "
             f"at these willingness-to-pay levels the cost of reaching a stranger "
             f"exceeds what they are worth. A plan built on that TAM would be built "
             f"on the one number here that cannot be converted."),

    ("h2", "Narrowing the institutional universe"),
    ("fig", "buyer_funnel", "Institutional buying units, filtered to those where "
                            "venture-building fits the curriculum and where we can "
                            "physically deliver."),
    ("deflist", [
        (f"Faculty fit — {pct(FILTER_FACULTY_FIT)}",
         "Business, commerce, engineering, computing, design and applied science "
         "carry capstone and graduation projects that map onto the missions. "
         "Medicine and law largely do not."),
        (f"Reachable for delivery — {pct(M['reach'])}",
         "Greater Cairo, Alexandria, the Delta and the Upper Egypt hubs; Riyadh, "
         "Jeddah and Dammam. A bootcamp needs facilitators in a room — which is "
         "exactly why the seat and competition engines, which do not, matter for "
         "reaching everywhere else."),
    ]),

    ("h2", "SOM — what we capture, and why that number"),
    ("p", f"Year-one revenue is {money(R1['total'])}, "
          f"{pct(R1['total']/M['sam'], 1)} of SAM. That is an output, not a target. "
          f"It falls out of counted quantities: {Y1_COHORTS:.0f} paid cohorts, "
          f"which is what the facilitator establishment can physically deliver; "
          f"{n(PLAN['initiative_seats'][1])} sponsored seats across two signed "
          f"programme partnerships; {PLAN['competitions'][1]} sponsored "
          f"competitions; and {PLAN['programmes'][1]} programme seat deals."),
    ("table",
     ["Engine", "Year-one basis", "Year one"],
     [[ENGINE_NAMES[0],
       f"{Y1_COHORTS:.0f} cohorts × {usd(COHORT_PRICE[1])}, plus "
       f"{PLAN['licences'][1]} faculty licences",
       money(R1["lines"][ENGINE_NAMES[0]])],
      [ENGINE_NAMES[1],
       f"{n(PLAN['initiative_seats'][1])} seats × {usd(PRICE_INITIATIVE_SEAT[1])}, "
       f"plus {PLAN['tot_cohorts'][1]} train-the-trainer cohorts",
       money(R1["lines"][ENGINE_NAMES[1]])],
      [ENGINE_NAMES[2],
       f"{PLAN['competitions'][1]} competitions × {usd(PRICE_COMPETITION[1])}",
       money(R1["lines"][ENGINE_NAMES[2]])],
      [ENGINE_NAMES[3],
       f"{PLAN['corporates'][1]} programme × {usd(PRICE_CORPORATE[1])}",
       money(R1["lines"][ENGINE_NAMES[3]])],
      [ENGINE_NAMES[4],
       f"{PLAN['programmes'][1]} partners × {PLAN['seats_each'][1]} seats × "
       f"{usd(PRICE_SEAT[1])}", money(R1["lines"][ENGINE_NAMES[4]])],
      [ENGINE_NAMES[5],
       f"{SUBS['paid']:,.0f} subscribers, mostly from the engines above",
       money(R1["lines"][ENGINE_NAMES[5]])],
      ["Total", "", money(R1["total"])]],
     [4.6, 6.8, 2.4]),

    ("h2", "Market context"),
    ("p", "MENA startups raised a record $7.5bn across 647 deals in 2025. Saudi "
          "Arabia led at $5bn across 211 deals; Egypt was third at $263m across 89 "
          "deals, with deal count rising even as value fell after the currency "
          "devaluation. Capital is concentrating in the Gulf while the founder "
          "population concentrates in Egypt — which is why this plan runs both "
          "markets at once rather than sequencing them."),
    ("note", "A platform serving only Egypt would be preparing founders for a "
             "market whose funding is shrinking. One serving only the Kingdom would "
             "compete for a small, well-served cohort. Serving both, through "
             "different doors, is the position."),
])

# =====================================================================
section("The six revenue engines", [
    ("lead", "What each engine sells, who signs, what it is worth and how it "
             "scales. The three largest get a chapter each after this one."),

    ("fig", "engine_mix", "The mix across three years. Universities lead in year "
                          "one; sponsored seats become the scale engine by year "
                          "three; subscriptions stay small in every year."),

    ("h2", "The engines at a glance"),
    ("table",
     ["Engine", "What is sold", "Unit price", "Margin", "Y1", "Y3"],
     [[ENGINE_NAMES[0], "A cohort, or a faculty-wide licence",
       f"{usd(COHORT_PRICE[1])} / {usd(PRICE_FACULTY_LICENCE)}", pct(UE["margin"]),
       money(R1["lines"][ENGINE_NAMES[0]]), money(R3["lines"][ENGINE_NAMES[0]])],
      [ENGINE_NAMES[1], "Seats in bulk, plus trainer certification",
       f"{usd(PRICE_INITIATIVE_SEAT[1])} / seat",
       pct(EE["Initiative seats"]["margin"]),
       money(R1["lines"][ENGINE_NAMES[1]]), money(R3["lines"][ENGINE_NAMES[1]])],
      [ENGINE_NAMES[2], "A competition, run end to end",
       usd(PRICE_COMPETITION[1]),
       pct(1 - COMPETITION_DIRECT / PRICE_COMPETITION[1]),
       money(R1["lines"][ENGINE_NAMES[2]]), money(R3["lines"][ENGINE_NAMES[2]])],
      [ENGINE_NAMES[3], "A bespoke youth or innovation programme",
       usd(PRICE_CORPORATE[1]), pct(EE["Corporate programmes"]["margin"]),
       money(R1["lines"][ENGINE_NAMES[3]]), money(R3["lines"][ENGINE_NAMES[3]])],
      [ENGINE_NAMES[4], "Platform seats where the partner facilitates",
       f"{usd(PRICE_SEAT[1])} / seat", pct(EE["Programme seats"]["margin"]),
       money(R1["lines"][ENGINE_NAMES[4]]), money(R3["lines"][ENGINE_NAMES[4]])],
      [ENGINE_NAMES[5], "Pro or Team, bought by the founder",
       f"{usd(PRICE_PRO_YEAR)} / {usd(PRICE_TEAM_YEAR)}", "88%",
       money(R1["lines"][ENGINE_NAMES[5]]), money(R3["lines"][ENGINE_NAMES[5]])]],
     [3.4, 4.2, 2.6, 1.6, 2.2, 2.2]),

    ("h2", "Deal size is the whole argument"),
    ("fig", "deal_sizes", "What one customer is worth in a year, by engine. A "
                          "single initiative partnership is worth more than a "
                          "thousand subscriptions."),
    ("p", "A salesperson has a finite number of meetings. The question a revenue "
          "plan has to answer is which meeting to take, and the answer here is not "
          "close: one meeting with a national programme office is worth more than "
          "every subscription the company will sell in year one. This is why the "
          "organisation has four institutional sales roles, a competitions manager "
          "and no consumer growth function at all."),

    ("h2", "How the engines feed each other"),
    ("num", [
        "<b>A free pilot produces a cohort report.</b> The report is the sales "
        "document for the paid cohort, for the faculty licence, and for every other "
        "engine — a ministry and a bank both want to see one before they sign.",
        "<b>A competition opens a university.</b> Running a sponsored competition "
        "on a campus puts StartPad in front of the entrepreneurship centre with a "
        "sponsor already paying. It is the cheapest route into Door 01.",
        "<b>An initiative partnership opens every university.</b> A dean who has "
        "not heard of StartPad has heard of Rowad 2030. Named participation in a "
        "national programme shortens the first conversation everywhere.",
        "<b>Every engine produces founders, and founders produce stories.</b> The "
        "stories win the next sponsor. This is the loop, and it is why the "
        "demand-generation budget buys content and events rather than advertising.",
    ]),

    ("h2", "Engine 4 — Corporate and CSR programmes"),
    ("p", f"Banks, telcos and energy companies in both markets run youth, "
          f"innovation and CSR programmes with real budgets and weak delivery. A "
          f"corporate deal is bespoke — their theme, their branding, their "
          f"reporting — and prices at {usd(PRICE_CORPORATE[1])} rising to "
          f"{usd(PRICE_CORPORATE[3])} as the format proves out. One in year one, "
          f"{PLAN['corporates'][3]} by year three."),
    ("p", f"The motion is slow and relationship-led, which is why year one targets "
          f"a single deal: the purpose of the first one is a reference, not "
          f"revenue. It is also the engine most exposed to a downturn, because a "
          f"CSR budget is the first thing a board cuts — which is why it is held to "
          f"{share(ENGINE_NAMES[3], 3)} of year-three revenue rather than pursued "
          f"harder."),

    ("h2", "Engine 5 — Programme and incubator seats"),
    ("p", f"Incubators and accelerators select founders; StartPad prepares them. A "
          f"platform-only seat at {usd(PRICE_SEAT[1])} lets a programme run its own "
          f"facilitation on top of the missions, the review loop and the reporting. "
          f"It is the smallest institutional engine by revenue "
          f"({share(ENGINE_NAMES[4], 3)} in year three) and the most strategically "
          f"useful: these organisations are the ecosystem's gatekeepers, and a "
          f"prepared applicant pool is the thing they most want."),
    ("p", "Treat this engine as channel as much as revenue. An accelerator that "
          "requires StartPad missions as part of its application becomes a "
          "permanent source of founders who arrive already using the product."),

    ("h2", "Engine 6 — Founder subscriptions"),
    ("p", f"Free for the first three missions, {usd(PRICE_PRO_YEAR)} a year for "
          f"Pro, {usd(PRICE_TEAM_YEAR)} for a founding team. "
          f"{share(ENGINE_NAMES[5])} of year-one revenue and "
          f"{share(ENGINE_NAMES[5], 3)} by year three."),
    ("fig", "subscription_sources", "Where paying founders come from in year one. "
                                    "Almost none of them are strangers."),
    ("p", "The conversion rates differ by an order of magnitude depending on where "
          "the person came from, and the reason is not a marketing insight — it is "
          "that a student who completed missions 01–10 inside a camp has already "
          "done the work, and the remaining five missions are the ones they "
          "actually want. A stranger who taps an advertisement has done nothing and "
          "wants nothing specific."),
    ("table",
     ["Where they came from", "Reached", "Convert", "Paying"],
     [[r["name"], n(r["reached"]), pct(r["conversion"]), f"{r['paid']:,.0f}"]
      for r in SUBS["rows"]] +
     [["Total", n(SUBS["reached"]), pct(SUBS["paid"] / SUBS["reached"]),
       f"{SUBS['paid']:,.0f}"]],
     [7.0, 2.6, 2.2, 2.2]),
    ("note", f"There is no paid-acquisition line in this plan. Against a lifetime "
             f"value of {usd(SUBS['ltv'])}, cold paid social in these markets costs "
             f"more per paying founder than the founder is worth. The budget that "
             f"would have funded it buys content, events and the ambassador network "
             f"instead — all of which feed the institutional pipeline as well as "
             f"the subscription one."),
])

# =====================================================================
section("Engine 1 — University cohorts and licences", [
    ("lead", f"{share(ENGINE_NAMES[0])} of year-one revenue and the engine that "
             f"produces the evidence every other engine sells on. Universities hold "
             f"the students, the graduation projects and the credibility."),

    ("h2", "The ladder"),
    ("fig", "university_ladder", "How one campus relationship grows. The free pilot "
                                 "is not a discount — it is how the institution's "
                                 "own report becomes the sales document for "
                                 "everything after it."),
    ("table",
     ["Stage", "What it is", "Price", "Typical timing"],
     [["Free pilot", f"One cohort of {COHORT_SIZE}, no fee", "$0",
       "First term of the relationship"],
      ["First paid cohort", f"{BOOTCAMP_DAYS} days, seats, judging, report",
       usd(COHORT_PRICE[1]), "The term after the pilot report lands"],
      ["Parallel groups", "100-plus students as four cohorts in one term",
       usd(COHORT_PRICE[1] * 4), "Year two of the relationship"],
      ["Faculty licence", "Every student in the faculty, one academic year",
       usd(PRICE_FACULTY_LICENCE), "Once two cohorts have run"]],
     [2.8, 5.4, 2.2, 3.8]),

    ("h2", "Four doors, in this order"),
    ("table",
     ["Door", "Who", "What they want", "What we offer first"],
     [["01", "Entrepreneurship centre", "A structured programme to show",
       "A free pilot cohort"],
      ["02", "Capstone coordinator", "A method for graduation projects",
       "Missions mapped to the term"],
      ["03", "Dean of faculty", "Outcomes for accreditation",
       "A faculty-wide licence"],
      ["04", "Student activities", "Events that fill rooms",
       "A sponsored competition"]],
     [1.2, 3.6, 4.6, 4.2]),
    ("p", "Door 04 is where Engine 3 enters: a student-activities office has no "
          "training budget but can host a competition a bank is paying for. That is "
          "the cheapest way into a university that has said no to a pilot, and it "
          "arrives with revenue attached rather than as a cost."),

    ("h2", "How a deal happens"),
    ("fig", "institution_workflow", "From identifying the right person to a cohort "
                                    "report, in six steps over seven weeks."),
    ("p", "One contract covers all three layers — the in-person bootcamp, the "
          "on-campus workshops and a platform seat for every student under one "
          "programme admin account. Selling the layers separately would triple the "
          "procurement cycle inside institutions where procurement is already the "
          "longest part of the sale."),

    ("h2", "How a cohort runs"),
    ("fig", "bootcamp_map", "Learn it in the room, build it on StartPad that "
                            "evening, and the programme sees it the next morning."),
    ("p", f"Six bootcamp days over two weeks, three days a week, 240 minutes a day, "
          f"{COHORT_SIZE} students per group working in teams on one venture each. "
          f"Never more than fifteen minutes of input before students apply it. Each "
          f"evening's work goes into StartPad as missions; the AI review runs "
          f"overnight; scores and fixes are ready before the next day's opener. "
          f"Larger intakes run as parallel groups, which is how a single university "
          f"relationship becomes four cohorts rather than one."),

    ("h2", "Unit economics"),
    ("fig", "cohort_economics",
     f"Where a cohort's {usd(PRICE_COHORT)} goes. Facilitation is the only "
     f"significant variable cost, which holds the margin at {pct(UE['margin'])} as "
     f"volume grows."),
    ("table",
     ["", "Per cohort", "Note"],
     [["Price", usd(UE["price"]),
       f"{usd(UE['price']/COHORT_SIZE)} a student — below the per-student cost of "
       f"one external trainer day that leaves nothing behind"],
      ["Facilitation", usd(UE["facilitation"]),
       f"{BOOTCAMP_DAYS} days × 2 certified facilitators"],
      ["Materials and certificates", usd(UE["materials"]), "Printed kits, canvases"],
      ["Bazaar", usd(UE["bazaar"]), "Judges, refreshments, venue contribution"],
      ["Gross profit", usd(UE["gross"]), f"{pct(UE['margin'])} margin"],
      ["Lifetime value", money(EE["University cohorts"]["ltv"]),
       f"{EE['University cohorts']['years']} years at two cohorts a year"],
      ["Cost to win", usd(EE["University cohorts"]["cac"]),
       f"Returns {EE['University cohorts']['ratio']:,.0f}× — payback inside the "
       f"first cohort"]],
     [3.8, 2.6, 10.2]),

    ("h2", "The volume plan"),
    ("table",
     ["", "Year 1", "Year 2", "Year 3"],
     [["Paid cohorts", f"{Y1_COHORTS:.0f}", n(PLAN["cohorts"][2]),
       n(PLAN["cohorts"][3])],
      ["Free pilots", n(sum(c["pilots"] for c in CAP)), "—", "—"],
      ["Faculty licences", n(PLAN["licences"][1]), n(PLAN["licences"][2]),
       n(PLAN["licences"][3])],
      ["Students reached", n(Y1_COHORTS * COHORT_SIZE),
       n(PLAN["cohorts"][2] * COHORT_SIZE), n(PLAN["cohorts"][3] * COHORT_SIZE)],
      ["Engine revenue", money(R1["lines"][ENGINE_NAMES[0]]),
       money(R2["lines"][ENGINE_NAMES[0]]), money(R3["lines"][ENGINE_NAMES[0]])]],
     [5.2, 3.8, 3.8, 3.8]),
    ("note", f"This engine is capped by facilitators, not demand. "
             f"{n(PLAN['cohorts'][3])} cohorts in year three needs "
             f"{PLAN['cohorts'][3]/COHORTS_PER_PAIR_PER_YEAR*2:.0f} certified "
             f"facilitators working at full tilt. That ceiling is why the other "
             f"engines exist, and why certification is the first operational "
             f"priority."),
])

# =====================================================================
section("Engine 2 — Sponsored seats in national initiatives", [
    ("lead", "Both governments have committed publicly to qualifying a million "
             "entrepreneurs or innovators. None of them has a method, a platform or "
             "a reporting line. This is the scale engine, and by year three it is "
             f"{share(ENGINE_NAMES[1], 3)} of revenue."),

    ("h2", "The programmes"),
    ("fig", "ngo_initiatives", "Four named Egyptian programmes with public "
                               "million-scale targets, each needing delivery "
                               "capacity it does not have in-house."),
    ("table",
     ["Programme", "Who runs it", "Their target", "What StartPad supplies"],
     [["One Million Entrepreneurs",
       "Ministry of Planning, through Rowad 2030, with Banque Misr and the "
       "National Bank of Egypt",
       "One million entrepreneurs qualified by 2030",
       "The qualification method itself, plus per-participant evidence a ministry "
       "can report"],
      ["1 Million Qualified Innovators",
       "Ministry of Higher Education with UNDP, MBRF and ICESCO; launched Cairo, "
       "April 2025",
       "Future skills for one million young people",
       "The university delivery channel the initiative needs, already running on "
       "campus"],
      ["MSMEDA governorate programme",
       "Qetar El Kheir caravan, across 22 governorates",
       "Reach founders outside the urban technology hubs",
       "Bilingual self-serve missions for governorates no facilitator reaches"],
      ["One Million International Licences",
       "With Cisco, announced May 2026",
       "Accredited technical and professional certification",
       "The venture-building complement to a technical certificate"]],
     [3.0, 3.8, 3.2, 4.2]),
    ("note", "Published progress on the One Million Entrepreneurs campaign stood at "
             "roughly 18,000 registrations against a target of one million. The gap "
             "is not ambition or funding — it is delivery capacity and a method "
             "that produces something reportable per participant. That gap is the "
             "product."),

    ("h2", "The scale, honestly stated"),
    ("fig", "initiative_scale", "Stated targets, what is realistically addressable "
                                "across both markets, and what this plan takes."),
    ("p", f"The stated targets total several million. The number this plan treats "
          f"as addressable is {n(INITIATIVE_SEATS_PER_YEAR)} seats a year across "
          f"both markets, and the share it assumes one provider could serve is "
          f"{pct(FILTER_INITIATIVE_SHARE)}. Year three takes "
          f"{n(PLAN['initiative_seats'][3])} seats, which is "
          f"{pct(PLAN['initiative_seats'][3]/INITIATIVE_SEATS_PER_YEAR)} of "
          f"addressable — inside the ceiling, deliberately."),

    ("h2", "How a sponsored programme is delivered"),
    ("fig", "initiative_model", "Four steps. The second one is what makes the other "
                                "three possible at scale."),
    ("p", f"<b>Train-the-trainer is the mechanism, not an add-on.</b> No facilitator "
          f"establishment StartPad could hire would reach "
          f"{n(PLAN['initiative_seats'][3])} participants. Certifying the "
          f"programme's own trainers — {PLAN['tot_cohorts'][1]} cohorts in year one "
          f"rising to {PLAN['tot_cohorts'][3]} — puts delivery in the initiative's "
          f"hands and sells at {usd(PRICE_TOT_COHORT[1])} a cohort while it does "
          f"so. It is the single most important operational idea in this engine."),

    ("h2", "Pricing and economics"),
    ("table",
     ["", "Year 1", "Year 2", "Year 3", "Note"],
     [["Seats", n(PLAN["initiative_seats"][1]), n(PLAN["initiative_seats"][2]),
       n(PLAN["initiative_seats"][3]), "Across signed programme partnerships"],
      ["Price per seat", usd(PRICE_INITIATIVE_SEAT[1]),
       usd(PRICE_INITIATIVE_SEAT[2]), usd(PRICE_INITIATIVE_SEAT[3]),
       "Falls with volume, which is the point"],
      ["Train-the-trainer cohorts", n(PLAN["tot_cohorts"][1]),
       n(PLAN["tot_cohorts"][2]), n(PLAN["tot_cohorts"][3]),
       f"At {usd(PRICE_TOT_COHORT[1])} each"],
      ["Engine revenue", money(R1["lines"][ENGINE_NAMES[1]]),
       money(R2["lines"][ENGINE_NAMES[1]]), money(R3["lines"][ENGINE_NAMES[1]]), ""],
      ["Share of total", share(ENGINE_NAMES[1]), share(ENGINE_NAMES[1], 2),
       share(ENGINE_NAMES[1], 3), ""]],
     [3.4, 2.1, 2.1, 2.1, 6.9]),
    ("p", f"A single initiative partnership is worth "
          f"{money(EE['Initiative seats']['ltv'])} over its life against "
          f"{money(EE['Initiative seats']['cac'])} to win — the longest sales cycle "
          f"in the plan and the highest return on it. Two partnerships land in year "
          f"one, deliberately: one is a single point of failure."),

    ("h2", "Why these partnerships matter more than their revenue"),
    ("num", [
        "<b>Volume without a facilitator.</b> Sponsored seats are platform-only, so "
        "they scale past the facilitator constraint that caps Engine 1. A "
        "governorate programme can place thousands of seats in a quarter no "
        "bootcamp schedule could serve.",
        "<b>Credibility that opens every other door.</b> Named participation in a "
        "national programme shortens the first conversation with a dean, a bank and "
        "an accelerator alike.",
        "<b>Reach outside the cities we can serve.</b> The governorate programmes "
        "deliberately target Upper Egypt and the border governorates — exactly the "
        "population the delivery-reachability filter excludes from Engine 1.",
    ]),

    ("h2", "The partnership path"),
    ("table",
     ["", "Step", "What happens", "Who owns it"],
     [["1", "Show results", "A cohort report from a comparable pilot",
       "Head of Government and Initiatives"],
      ["2", "Co-design a cohort", "Their objective, our missions, agreed reporting",
       "Head of Curriculum with the partner"],
      ["3", "Certify their trainers", "Train-the-trainer cohorts",
       "Facilitator certification lead"],
      ["4", "Provision and run", "Bulk seats by governorate or region",
       "Programme Delivery Manager"],
      ["5", "Report back", "Participation, progress, evidence, in their format",
       "Delivery and the bid administrator"],
      ["6", "Renew and widen", "A larger cohort, or a governorate added",
       "Head of Government and Initiatives"]],
     [0.9, 2.8, 5.4, 4.1]),

    ("h2", "The equivalent motion in Saudi Arabia"),
    ("p", "The Kingdom's youth and SME institutions — Monsha'at on the SME side, "
          "the Misk Foundation on youth development — run programmes with the same "
          "structural gap: ambition and budget at national scale, delivery "
          "contracted out. The Saudi motion leads with these partners rather than "
          "with universities, which is why the Riyadh country manager is a "
          "partnerships hire and not a campus hire."),
    ("note", "One caution. Misk cancelled its 2026 Global Forum, and flagship-event "
             "cancellations usually signal a programme budget under review. The "
             "Saudi plan should not depend on one institution: the Riyadh targets "
             "assume several partners, and the first Riyadh competition is the "
             "fallback route to founders if partnership budgets move."),

    ("h2", "What we must not promise"),
    ("p", "A national programme will ask for an outcome number — jobs created, "
          "businesses registered, funding raised. StartPad records mission "
          "progress, evidence and review scores. Those are honest indicators of "
          "recorded work; they do not certify venture success, and the platform "
          "says so on the page. Contracting to an outcome the product cannot "
          "measure is the fastest way to lose a government relationship, and every "
          "agreement should state what is measured and what is not."),
])

# =====================================================================
section("Engine 3 — Sponsored competitions", [
    ("lead", "Most companies treat a student competition as a marketing cost. Run "
             "on the platform and paid for by a sponsor, it is a "
             f"{pct(1 - COMPETITION_DIRECT/PRICE_COMPETITION[1])}-margin revenue "
             f"line that also opens universities and produces founders."),

    ("h2", "The model"),
    ("fig", "competition_model", "Who pays, what they buy, and what the competition "
                                 "leaves behind."),
    ("p", "Entry is a free StartPad account. The qualifying rounds <b>are</b> the "
          "Discovery missions, scored by the platform rather than by a committee "
          "reading PDFs. Judges at the final see reviewed work and evidence rather "
          "than slides, and finalists arrive genuinely prepared because they have "
          "done ten missions to get there."),
    ("p", "That design is what makes the sponsor's money worth spending. A "
          "conventional competition sponsor pays for a logo on a banner. Here they "
          "pay for a qualification process that produces a defensible shortlist, "
          "per-entrant evidence they can report on, and a cohort of founders who "
          "continue afterwards."),

    ("h2", "Who sponsors, and why"),
    ("table",
     ["Sponsor", "What they are buying", "Typical scale"],
     [["Banks and fintechs",
       "Youth and SME positioning, plus a pipeline of bankable small businesses",
       f"{usd(28_000)}–{usd(45_000)}"],
      ["Telcos", "Brand presence on campus and a digital-skills story",
       f"{usd(25_000)}–{usd(40_000)}"],
      ["Ministries and agencies",
       "A visible, reportable delivery vehicle for a national target",
       f"{usd(30_000)}–{usd(60_000)}"],
      ["Universities",
       "A flagship event that fills a hall and proves the centre is working",
       f"{usd(15_000)}–{usd(25_000)}"],
      ["Foundations and donors",
       "Youth outcomes with per-participant evidence",
       f"{usd(25_000)}–{usd(50_000)}"]],
     [3.2, 8.0, 3.0]),

    ("h2", "Economics"),
    ("table",
     ["", "Per competition", "Note"],
     [["Sponsor fee", usd(PRICE_COMPETITION[1]), "Year one; rises with the format"],
      ["Delivery cost", usd(COMPETITION_DIRECT),
       "Judging, platform setup, event staffing, on-site days"],
      ["Gross profit", usd(PRICE_COMPETITION[1] - COMPETITION_DIRECT),
       pct(1 - COMPETITION_DIRECT / PRICE_COMPETITION[1]) + " margin"],
      ["Entrants reached", "~700", "Every one opens a StartPad account"],
      ["Cost to win the sponsor", usd(EE["Sponsored competitions"]["cac"]),
       f"Returns {EE['Sponsored competitions']['ratio']:,.0f}× over "
       f"{EE['Sponsored competitions']['years']} years"],
      ["Second-order value", "A university and a sponsor relationship",
       "Both of which the other engines sell into"]],
     [4.0, 3.4, 9.2]),

    ("h2", "The volume plan"),
    ("table",
     ["", "Year 1", "Year 2", "Year 3"],
     [["Competitions run", n(PLAN["competitions"][1]), n(PLAN["competitions"][2]),
       n(PLAN["competitions"][3])],
      ["Price each", usd(PRICE_COMPETITION[1]), usd(PRICE_COMPETITION[2]),
       usd(PRICE_COMPETITION[3])],
      ["Entrants reached", n(PLAN["competitions"][1] * 700),
       n(PLAN["competitions"][2] * 700), n(PLAN["competitions"][3] * 700)],
      ["Engine revenue", money(R1["lines"][ENGINE_NAMES[2]]),
       money(R2["lines"][ENGINE_NAMES[2]]), money(R3["lines"][ENGINE_NAMES[2]])],
      ["Share of total", share(ENGINE_NAMES[2]), share(ENGINE_NAMES[2], 2),
       share(ENGINE_NAMES[2], 3)]],
     [5.2, 3.8, 3.8, 3.8]),

    ("h2", "Why this engine is underrated"),
    ("deflist", [
        ("It is the cheapest entry to a university",
         "A student-activities office has no training budget but will happily host "
         "an event a bank is funding. Door 04 costs nothing to walk through and "
         "leads to Doors 01 and 03."),
        ("It scales without facilitators",
         "A competition needs event staff for a day or two, not a certified pair "
         "for six days. It grows past the constraint that caps Engine 1."),
        ("It produces the stories the whole company runs on",
         "A winner with a real venture is the content that makes the next dean take "
         "the meeting and the next sponsor sign. The podcast exists to capture "
         "exactly this."),
        ("It converts to subscriptions better than advertising ever will",
         f"Competition entrants convert to paid at "
         f"{pct([r for r in SUBS['rows'] if 'competition' in r['name']][0]['conversion'])}, "
         f"because they have already done the missions to qualify."),
    ]),
    ("quote", "The competition is not how we market the platform. The competition "
              "runs on the platform, and somebody else pays for it."),
])

# =====================================================================
section("Competition and positioning", [
    ("lead", "What a buyer uses instead of StartPad today, and why none of it "
             "closes the gap."),

    ("h2", "The alternatives"),
    ("table",
     ["Dimension", "Generic templates and guides", "StartPad"],
     [["Structure", "A list of things to consider", "Fifteen sequenced missions"],
      ["AI", "None, or a bolted-on chatbot", "A co-founder inside every mission"],
      ["Motivation", "None built in", "Points, levels, streaks"],
      ["Tools", "Scattered across ten-plus sites", "121, mapped to the journey"],
      ["Region", "US-built, translated if at all", "MENA-built, bilingual"],
      ["Evidence", "Nothing is recorded", "Every answer reviewed and scored"],
      ["For the buyer", "No visibility at all",
       "Cohort workspace and a decision-ready report"]],
     [3.2, 5.6, 5.6]),

    ("h2", "The competitive set, honestly"),
    ("deflist", [
        ("University entrepreneurship centres running their own programmes",
         "The real incumbent, and the one to respect. They have the room, the "
         "students and the budget. We beat an in-house programme on method, "
         "bilingual content, the evidence trail and the reporting line — and we "
         "should enter as the thing that makes their centre look good, never as its "
         "replacement."),
        ("Training consultancies and event agencies",
         "The direct competitor for the cohort, competition and corporate engines. "
         "Comparable or higher day rates, nothing left behind when the trainer "
         "goes, and no per-participant record. This is the comparison that makes "
         "the cohort price look cheap in front of a dean, and the one to lead with."),
        ("Incubators and accelerators",
         "They select founders; we prepare them. In practice they are Engine 5 "
         "rather than competition — a better-prepared applicant pool is the thing "
         "they most want."),
        ("Online course platforms",
         "Cheaper and broader. They sell completion, not evidence, and no "
         "institution can report a cohort outcome from a course certificate. We "
         "lose on price and win on what the buyer has to show."),
    ]),
    ("quote", "We do not win by being the best content. We win by being the only "
              "option that leaves the buyer with something they can report."),
])

# =====================================================================
section("Go-to-market plan", [
    ("lead", "Five moves, each unlocking the next, across two markets from day one. "
             "Campus first, proof next, two markets at once."),

    ("fig", "gtm_moves", "The five moves and what each unlocks. The order is "
                         "load-bearing: each move is affordable only because the "
                         "one before it happened."),

    ("h2", "The four phases of year one"),
    ("fig", "phases", "Egypt and Saudi Arabia, in parallel, through four phases."),

    ("h2", "Two markets, two different doors"),
    ("table",
     ["", "Egypt", "Saudi Arabia"],
     [["Started", "September 2026", "September 2026, in parallel"],
      ["First door", "Universities and campuses",
       "Programmes and youth initiatives"],
      ["Lead engine", "University cohorts",
       "Sponsored seats, then a Riyadh competition"],
      ["Voice", "Egyptian colloquial", "Saudi dialect, composed not translated"],
      ["Team", "Core team in Cairo", "A country manager, supported from Cairo"],
      ["Why this door", "Scale of the student population and campus access",
       "Funded programmes move faster than university procurement"]],
     [3.0, 5.2, 5.4]),
    ("p", "The markets are not sequenced because the doors are different. Waiting "
          "for Egypt to work before entering the Kingdom would have meant learning "
          "the Saudi programme-partner motion a year late — and the Saudi cohorts "
          "are the ones that pay from the first quarter while Egypt is still "
          "running free pilots."),

    ("h2", "The institutional pipeline"),
    ("fig", "pipeline", "The funnel the company actually runs. Every stage is a "
                        "number a named person owns."),
    ("table",
     ["Stage", "Year one", "Conversion", "Who owns it"],
     [[label, n(val), "—" if i == 0 else pct(val / PIPE[i - 1][1]),
       ["Partnerships associates and the demand-generation team",
        "Heads of Partnerships, Government and Initiatives",
        "Head of the relevant engine, with the bid administrator",
        "The signing head, with the COO on delivery capacity"][i]]
      for i, (label, val) in enumerate(PIPE)],
     [5.2, 1.8, 2.0, 7.6]),
    ("p", f"{PIPE[-1][1]} signed relationships in year one across all engines. That "
          f"is the number the whole plan rests on, and it is small enough to name "
          f"every one of them in a pipeline review — which is exactly how it should "
          f"be managed."),
])

# =====================================================================
section("Demand generation", [
    ("lead", "Not consumer acquisition. The job is to make a dean take a meeting, a "
             "sponsor return a call and a ministry shortlist us — and to know which "
             "campuses are ready before we spend a trip on them."),

    ("h2", "What the budget actually buys"),
    ("table",
     ["Line", "Year 1", "What it is for"],
     [[name, usd(val), purpose] for (name, val), purpose in zip(
         MD.DEMAND_SPEND[1],
         ["Founder stories in Egyptian Arabic. The asset that makes an "
          "institutional pitch credible — a dean responds to a graduate of a "
          "university like theirs",
          f"{AMBASSADORS[1]} ambassadors across twelve campuses. The cheapest "
          f"source of founders and the early-warning system for which campuses are "
          f"ready to buy",
          "Where partnership conversations start. The Global Entrepreneurship "
          "Festival in Cairo and the Saudi equivalents are pipeline events, not "
          "brand events",
          "Retargeting, competition entry and event fill only. There is no cold "
          "acquisition line",
          "Cohort reports, case studies and the proposal pack. The single most used "
          "sales asset in the company"])] +
     [["Total", usd(sum(v for _, v in MD.DEMAND_SPEND[1])), ""]],
     [4.0, 2.0, 9.4]),

    ("h2", "The ambassador programme"),
    ("p", f"A campus team that earns its place — {AMBASSADORS[1]} ambassadors "
          f"across twelve campuses by the Scale quarter, rising to "
          f"{AMBASSADORS[3]} by year three. Status is earned through founders "
          f"brought in and renewed each term; a title that cannot be lost is a "
          f"title that stops working."),
    ("table",
     ["Level", "Role", "What they do", "What they get"],
     [["01", "Member", "Uses StartPad, joins workshops", "Community standing"],
      ["02", "Ambassador", "Runs Mission 01 workshops", "Free Pro access, stipend"],
      ["03", "Campus lead", "Leads the team, owns student activities",
       "Mentor sessions, references"]],
     [1.3, 2.6, 5.4, 4.3]),
    ("p", "The network's most valuable output is not sign-ups. It is intelligence: "
          "which entrepreneurship centre has budget this term, which dean is under "
          "accreditation pressure, which student-activities office is looking for "
          "an event. That is what turns a cold institutional list into a warm "
          "pipeline."),

    ("h2", "The content engine"),
    ("p", "One founder story, many pieces. Find founders who built from a "
          "graduation project; record a podcast episode in Egyptian Arabic; cut "
          "reels and posts; every piece ends at Mission 01. The podcast is not a "
          "brand exercise — it is the proof asset the institutional sale runs on, "
          "and competitions are where the stories come from."),

    ("h2", "What we deliberately do not do"),
    ("note", f"There is no cold paid-acquisition line. Against a subscriber lifetime "
             f"value of {usd(SUBS['ltv'])}, buying strangers in these markets costs "
             f"more per paying founder than the founder is worth. Targeted digital "
             f"spend exists only to retarget people the engines already reached and "
             f"to fill competition and event seats. If a future test shows paid "
             f"acquisition clearing its cost, it should be reported as a marketing "
             f"cost of the institutional business, not as consumer CAC."),
])

# =====================================================================
section("Organisation and HR plan", [
    ("lead", f"{HC['y1']} employees in year one, growing to {HC['y3']} by year "
             f"three, plus two non-employee layers that carry most of the delivery "
             f"load. The shape follows the engines: four institutional sales roles "
             f"and no consumer growth function."),

    ("fig", "org_chart", "The year-one organisation. Four reporting lines under the "
                         "CEO, who also personally runs the Day 01 platform "
                         "onboarding in every cohort."),

    ("h2", "The full establishment"),
    ("table",
     ["Function", "Role", "Y1", "Y2", "Y3", "Monthly cost"],
     [[fn if i == 0 else "", role, n(y1), n(y2), n(y3), usd(monthly)]
      for fn, rows in [(f, HC_BY_FN[f]["roles"]) for f in HC_BY_FN]
      for i, (role, y1, monthly, y2, y3) in enumerate(rows)] +
     [["Total", "", n(HC["y1"]), n(HC["y2"]), n(HC["y3"]), ""]],
     [3.0, 5.4, 1.1, 1.1, 1.1, 2.3]),
    ("fig", "headcount", "Headcount by function. Delivery and institutional sales "
                         "grow fastest, because they are what the revenue is made "
                         "of."),

    ("h2", "Two layers that are not on the payroll"),
    ("deflist", [
        ("Certified freelance facilitators",
         f"Engine 1 runs on them. Four lead facilitators are employed; everything "
         f"above {4 * COHORTS_PER_PAIR_PER_YEAR // 2} cohorts a year is delivered "
         f"by a certified pool paid "
         f"{usd(UE['facilitation']/(BOOTCAMP_DAYS*2))} a day. This keeps the "
         f"largest variable cost variable, which protects the business in a quarter "
         f"when a university postpones."),
        (f"{AMBASSADORS[1]} campus ambassadors",
         "A stipend, free Pro access and standing — not a salary. Their most "
         "valuable output is knowing which campus is ready to buy."),
    ]),

    ("h2", "The hiring sequence, and why this order"),
    ("num", [
        "<b>Before anything — the KSA country manager.</b> The most expensive "
        "single hire and the first one, because the Saudi motion is "
        "partnership-led and a partnership cycle is long. Hiring late pushes Saudi "
        "revenue out of year one entirely.",
        "<b>Land quarter — delivery and curriculum.</b> Four lead facilitators, the "
        "certification lead and the Head of Curriculum, before any sales capacity. "
        "The free pilots have to run flawlessly because they are the only "
        "collateral the Prove quarter will have.",
        "<b>Land quarter — Head of Government and Initiatives.</b> Engine 2 has the "
        "longest cycle of any engine. Starting those conversations in the first "
        "quarter is what makes year-two seat volume possible.",
        "<b>Prove quarter — competitions manager and partnerships associates.</b> "
        "Now that cohort reports exist, the competition and university motions can "
        "both convert them.",
        "<b>Expand quarter — engineering, bid administration and student "
        "success.</b> Volume triples; bulk provisioning, partner reporting and "
        "support all need to hold at a scale they have not seen.",
        "<b>Scale quarter — second delivery manager and the full facilitator "
        f"pool.</b> The quarter peaks at {CAP[-1]['facilitators']:.0f} "
        f"facilitators, certified before it opens rather than during it.",
    ]),

    ("h2", "Compensation and retention"),
    ("deflist", [
        ("Cairo base, Riyadh exception",
         f"Most roles are priced at Cairo. Two are priced at Riyadh — the country "
         f"manager and the Saudi delivery manager — and together they are "
         f"{pct((5000+4500)*12/HC['cost_y1'])} of year-one payroll across two of "
         f"{HC['y1']} people. Under-pricing them is the most common way this plan "
         f"fails quietly."),
        ("Founders below market",
         "The three leadership roles are at $3,000 a month, below what any of them "
         "could earn elsewhere. A deliberate runway decision, to be corrected at "
         "the year-two raise rather than left as a permanent feature."),
        ("Facilitators are a career, not a gig",
         "The certified pool is the operational asset. Certification, a rising day "
         "rate by tier, first refusal on employed lead roles and visible cohort "
         "outcomes are what stop the pool leaking to the consultancies competing "
         "for exactly these people."),
        ("Institutional sales is paid on signing and on renewal",
         f"Commission runs at {pct(MD.B2B_COMMISSION)} of institutional revenue. "
         f"Renewal is where this business lives, so the account manager role added "
         f"from year two is compensated on retained and expanded revenue rather "
         f"than on new logos."),
    ]),
])

# =====================================================================
section("Operational plan", [
    ("lead", "What has to be true, and in what order, for the go-to-market plan to "
             "be deliverable rather than aspirational."),

    ("h2", "The binding constraint"),
    ("p", f"Demand is not the constraint in year one. Delivery capacity is. A "
          f"facilitator pair runs one cohort per two weeks and needs slack for "
          f"travel, preparation and campus holidays — {COHORTS_PER_PAIR_PER_YEAR} "
          f"cohorts a pair a year. The quarterly plan converts directly into a "
          f"facilitator headcount, and that number is the operating plan's primary "
          f"schedule."),
    ("fig", "cohort_ramp", "Cohorts by quarter against the facilitators required. "
                           "The Scale quarter needs roughly four times the capacity "
                           "of the Land quarter."),
    ("table",
     ["Quarter", "Phase", "Egypt paid", "KSA paid", "Free pilots", "Total",
      "Facilitators"],
     [[c["label"], c["phase"], n(c["egypt"]), n(c["ksa"]), n(c["pilots"]),
       n(c["total"]), f"{c['facilitators']:.0f}"] for c in CAP] +
     [["Year one", "", n(sum(c["egypt"] for c in CAP)),
       n(sum(c["ksa"] for c in CAP)), n(sum(c["pilots"] for c in CAP)),
       n(sum(c["total"] for c in CAP)),
       "peak " + f"{max(c['facilitators'] for c in CAP):.0f}"]],
     [2.2, 1.9, 1.9, 1.7, 1.8, 1.4, 2.0]),
    ("note", "Engines 2, 3 and 5 all scale <b>past</b> this constraint — sponsored "
             "seats need no facilitator, a competition needs event staff for two "
             "days, and a programme partner facilitates for itself. That is a "
             "strategic property of the revenue mix, not a coincidence."),

    ("h2", "Readiness — what must exist before each phase"),
    ("table",
     ["By the start of", "What must be ready", "Owner"],
     [["Q4 2026 · Land",
       "Four certified facilitators · the six-day curriculum and all materials in "
       "both languages · the admin workspace with cohort creation and invitations · "
       "a signed pilot agreement template · the Riyadh country manager in post",
       "COO"],
      ["Q1 2027 · Prove",
       "The cohort report, generated without manual editing · judging rubric and "
       "certificates · four completed pilot reports · the competition entry and "
       "qualification flow on the platform",
       "COO and Head of Curriculum"],
      ["Q2 2027 · Expand",
       "Eight more certified facilitators · bulk seat provisioning and "
       "partner-level reporting for sponsored programmes · the train-the-trainer "
       "curriculum · support cover in both languages at volume",
       "Delivery Managers"],
      ["Q3 2027 · Scale",
       "The full facilitator pool certified before the quarter opens · renewal pack "
       "and second-term pricing · parallel-group scheduling for 100-plus intakes · "
       "Riyadh competition logistics",
       "COO and Heads of Sales"]],
     [2.8, 8.4, 2.6]),

    ("h2", "The cohort delivery machine"),
    ("p", "Every cohort runs the same way, and the sameness is the point: it lets a "
          "freelance facilitator deliver a cohort the company has never seen, and "
          "makes the cohort report comparable across institutions."),
    ("num", [
        "<b>Scheduling.</b> Cohort dates are fixed against the institution's "
        "academic calendar, not ours. Egyptian and Saudi terms differ and Ramadan "
        "moves. The delivery calendar is built a term ahead and is the constraint "
        "sales sells against — never the other way round.",
        "<b>Facilitator assignment.</b> A certified pair per group, with an "
        "employed lead facilitator on the first cohort at any new institution. The "
        "freelance pool covers repeat institutions, where the format is proven.",
        "<b>Materials.</b> Printed kits, problem cards, canvases and certificates "
        "shipped to the venue a week ahead; digital copies in the admin workspace.",
        "<b>The daily loop.</b> Opener on last night's StartPad progress; short "
        "input, then apply it; checkpoint marked Meets, Partly or Not yet; the team "
        "splits that night's missions and submits; AI feedback lands before the next "
        "opener. Days one to five.",
        "<b>The Bazaar.</b> Day six is public — faculty, families, partners and "
        "judges. Certificates, photographs and the cohort report issue the same "
        "week, because a report that arrives a month later renews nothing.",
        "<b>Handover.</b> Missions 11–15 stay open to the student afterwards and "
        "the institution keeps visibility. This turns a two-week engagement into a "
        "year-long relationship, and it is where subscription revenue comes from.",
    ]),

    ("h2", "Facilitator certification"),
    ("p", "The pool is the operational asset and the main single point of failure. "
          "Four steps, run by the certification lead: observe a full cohort; "
          "co-deliver two days under a lead; deliver a full cohort observed and "
          "scored against the rubric; recertify each term against cohort outcomes "
          "and student feedback. Nobody facilitates unobserved before step three is "
          "passed, including under schedule pressure — which is precisely when the "
          "temptation arrives."),
    ("p", f"The same machinery certifies a partner's own trainers under Engine 2. "
          f"{PLAN['tot_cohorts'][3]} train-the-trainer cohorts in year three is a "
          f"revenue line and a scaling mechanism at once, and it runs on the "
          f"certification process built for internal use."),

    ("h2", "What the platform must do to support the plan"),
    ("table",
     ["Capability", "Which engine needs it", "Needed by"],
     [["Programme admin account: cohort creation, bulk invitation, educator "
       "assignment",
       "Engines 1, 2, 5 — without it there is no institutional product at all",
       "Q4 2026"],
      ["Student-controlled sharing with scoped programme data",
       "All engines. The trust position that makes a university sign and keeps the "
       "company clear of student-data problems", "Q4 2026"],
      ["AI review at cohort volume, overnight",
       "Engine 1. The daily loop breaks if feedback is not ready before the next "
       "opener; 25 students submitting the same evening is a load spike",
       "Q4 2026"],
      ["Full Arabic parity, right-to-left, including exported PDFs",
       "All engines. A ministry cannot circulate a report it cannot read",
       "Q4 2026"],
      ["Competition entry, qualification and judging flow",
       "Engine 3. Entry as an account, rounds as missions, a judges' pack generated "
       "from reviewed work", "Q1 2027"],
      ["The automatic cohort report",
       "Engines 1 and 4. The renewal document and the collateral every other engine "
       "sells on", "Q1 2027"],
      ["Bulk seat provisioning and partner-level reporting by region",
       "Engine 2. Programmes place thousands of seats at once and report to their "
       "own donors", "Q2 2027"]],
     [4.4, 6.8, 2.6]),

    ("h2", "Quality gates"),
    ("bul", [
        "<b>Mission completion.</b> At least 80% of students complete missions "
        "01–10 by the Bazaar. Below that, the evening loop is not working and the "
        "facilitator pairing is examined first.",
        "<b>Review turnaround.</b> AI feedback available before the next day's "
        "opener, every night. This is a platform SLA, not a target.",
        "<b>Bazaar delivery.</b> Every team pitches and every member speaks. A team "
        "that cannot is a facilitation failure that showed up two days earlier and "
        "was not caught.",
        "<b>Report issued inside five working days</b> of the Bazaar, to the person "
        "who signed.",
    ]),

    ("h2", "Data protection and the student relationship"),
    ("p", "Students own their account and their idea. The programme sees mission "
          "progress, activity, the evidence the student chooses to share, review "
          "scores and educator approvals. It never sees AI Co-Founder chats, "
          "private profile data or unsubmitted drafts, and staff can never edit "
          "student work. Sharing is switched on by the student and can be switched "
          "off; only students with active consent appear in cohort metrics."),
    ("note", "This is a commercial position as much as an ethical one. Every buyer "
             "in this plan is buying a reporting line, and the credibility of that "
             "line depends on the student having had a real choice. A cohort metric "
             "built on compelled consent is one a dean cannot defend, and the first "
             "time it is challenged the relationship ends."),
])

# =====================================================================
section("Financial plan", [
    ("lead", "Three years of revenue, cost and cash, built from the engine volumes "
             "rather than from a growth rate."),

    ("h2", "Revenue by engine"),
    ("table",
     ["Engine"] + [f"Year {y['year']}" for y in PROJ] + ["Y3 share"],
     [[k] + [money(y["lines"][k]) for y in PROJ] + [share(k, 3)]
      for k in ENGINE_NAMES] +
     [["Total revenue"] + [money(y["revenue"]) for y in PROJ] + ["100%"]],
     [5.4, 2.5, 2.5, 2.5, 1.7]),

    ("h2", "Year-one cost base"),
    ("table",
     ["Cost line", "Year one", "Note"],
     [[name, usd(val), note] for (name, val), note in zip(
         C1["lines"],
         [f"{HC['y1']} people, averaging 65% of the establishment across the year",
          "Cohorts, pilots, train-the-trainer, competitions, corporate programmes "
          "and seat provisioning",
          "Content, ambassadors, events and collateral — no cold acquisition",
          f"{pct(MD.B2B_COMMISSION)} of institutional revenue",
          "Scales with active founders and AI review volume",
          "Platform tooling and internal systems",
          "Cairo to Riyadh, and campuses in both markets",
          "Including the cost of establishing the Saudi entity",
          "Cairo office and a Riyadh desk",
          "8% of the above"])] +
     [["Total operating cost", usd(C1["total"]), ""]],
     [4.6, 2.4, 6.6]),

    ("h2", "Three-year profit and loss"),
    ("table",
     [""] + [y["label"] for y in PROJ],
     [["Revenue"] + [money(y["revenue"]) for y in PROJ],
      ["Institutional revenue"] + [money(y["institutional"]) for y in PROJ],
      ["Operating cost"] + [money(y["cost"]) for y in PROJ],
      ["Operating result"] + [("−" if y["profit"] < 0 else "+") + money(abs(y["profit"]))
                              for y in PROJ],
      ["Operating margin"] + [pct(y["profit"] / y["revenue"]).replace("-", "−")
                              for y in PROJ],
      ["Revenue per employee"] + [money(y["revenue"] / y["headcount"]) for y in PROJ],
      ["Paid cohorts"] + [n(y["cohorts"]) for y in PROJ],
      ["Sponsored seats"] + [n(PLAN["initiative_seats"][y["year"]]) for y in PROJ],
      ["Competitions"] + [n(PLAN["competitions"][y["year"]]) for y in PROJ]],
     [4.2, 3.4, 3.4, 3.4]),

    ("h2", "Cash, and the raise"),
    ("fig", "cash_curve", "Cash on hand across three years. The trough is shallow "
                          "because every institutional engine invoices before it "
                          "delivers."),
    ("table",
     ["", "Amount", "What it covers"],
     [["Year-one deficit", money(FUND["deficit_y1"]),
       "The gap while free pilots and hiring run ahead of engine revenue"],
      ["Year-two deficit", money(FUND["deficit_y2"]),
       "None — the business reaches breakeven in year two"],
      ["Six-month operating reserve", money(FUND["reserve"]),
       "Six months of the year-one cost base, against a delayed term or a postponed "
       "partnership"],
      ["Total raise", money(FUND["rounded"]),
       "Sized to the deficit and a genuine reserve, not to a round number"]],
     [4.4, 2.6, 6.6]),
    ("p", f"{money(FUND['rounded'])} is small for a business reaching "
          f"{money(PROJ[2]['revenue'])} in year three, and the reason is structural "
          f"rather than optimistic. A cohort is invoiced before the bootcamp runs; a "
          f"sponsored-seat programme pays on provisioning; a competition sponsor "
          f"pays before the event. Working capital is <b>negative</b> across every "
          f"institutional engine, so growth releases cash rather than consuming it. "
          f"A subscription-led version of this company would need several times the "
          f"capital to reach the same revenue."),

    ("h2", "Use of funds"),
    ("table",
     ["Use", "Share", "Why"],
     [["Delivery capacity — facilitators, certification, materials", "31%",
       "The binding constraint on Engine 1 and the mechanism behind Engine 2"],
      ["Product and engineering", "26%",
       "The admin workspace, competition flow, bulk provisioning and partner "
       "reporting"],
      ["Institutional sales and Saudi market entry", "23%",
       "Country manager, government and initiatives lead, competitions manager, "
       "entity and travel"],
      ["Demand generation — content, ambassadors, events", "11%",
       "What makes a dean take the meeting"],
      ["Operating reserve held unspent", "9%",
       "A postponed term or a delayed partnership should not be existential"]],
     [5.4, 1.8, 6.4]),

    ("h2", "Sensitivity"),
    ("table",
     ["If this is a third worse", "Plan", "Downside", "Effect on Y1 revenue"],
     [["Cohorts delivered", f"{Y1_COHORTS:.0f}", f"{Y1_COHORTS*0.67:.0f}",
       "−" + money(R1["detail"]["cohorts"] * 0.33)],
      ["Sponsored seats signed", n(PLAN["initiative_seats"][1]),
       n(PLAN["initiative_seats"][1] * 0.67),
       "−" + money(R1["detail"]["initiative_seats"] * 0.33)],
      ["Competitions sponsored", n(PLAN["competitions"][1]),
       f"{PLAN['competitions'][1]*0.67:.0f}",
       "−" + money(R1["detail"]["competitions"] * 0.33)],
      ["Subscription conversion", f"{SUBS['paid']:,.0f} paying",
       f"{SUBS['paid']*0.67:,.0f} paying",
       "−" + money(R1["detail"]["subscriptions"] * 0.33)]],
     [4.6, 2.6, 2.6, 3.6]),
    ("p", "The three that matter are all institutional, and the fourth barely "
          "registers. The company's risk is concentrated in whether universities, "
          "programmes and sponsors sign and renew — which is the right risk to "
          "carry, because it is the one the operating plan can act on."),
])

# =====================================================================
section("Risks", [
    ("lead", "The risks most likely to break this plan, what each looks like early, "
             "and what has already been built to absorb it."),

    ("table",
     ["Risk", "What it looks like early", "Mitigation"],
     [["Facilitator capacity does not materialise",
       "Certification slips, or the pool leaks to consultancies paying more a day",
       "Certification starts in the Land quarter, a term ahead of need; the pool is "
       "a tiered career with a rising day rate; the quarterly plan is cut to "
       "facilitator capacity rather than the reverse"],
      ["University procurement is slower than planned",
       "Pilots run but contracts sit unsigned through the Prove quarter",
       "One contract covering all three layers; free pilots that make the cohort "
       "report the sales document; competitions enter through Door 04 with a "
       "sponsor already paying; Saudi partnership revenue lands from Q4"],
      ["A national initiative partnership does not land",
       "Enthusiastic meetings, no budget line, repeated deferral",
       f"Engine 2 is {share(ENGINE_NAMES[1])} of year-one revenue, so year one "
       f"survives without it; two partnerships are pursued so neither is a single "
       f"point of failure; year three sits inside "
       f"{pct(FILTER_INITIATIVE_SHARE)} of addressable seats"],
      ["Sponsor budgets move",
       "Competition and corporate conversations stall at the same time, usually a "
       "macro signal",
       "Competitions and corporate together are "
       f"{pct((R1['lines'][ENGINE_NAMES[2]] + R1['lines'][ENGINE_NAMES[3]])/R1['total'])} "
       "of year one; universities and initiatives carry the plan without them"],
      ["Currency and macro",
       "EGP devaluation repricing a USD plan against EGP costs",
       "Most costs are EGP and institutional pricing can be set in EGP with a USD "
       "reference; devaluation lowers the cost base faster than local willingness "
       "to pay"],
      ["Key-person concentration",
       "The CEO personally runs Day 01 onboarding in every cohort",
       "This does not scale past roughly 20 cohorts a year and is a known year-two "
       "problem; the Day 01 session must be delivered by certified facilitators "
       "before the Expand quarter"]],
     [3.4, 5.0, 5.2]),

    ("note", f"The last row is the one to watch. It is written into the strategy as "
             f"a feature — the founder personally opens every cohort — and it is "
             f"genuinely good for the first twenty. It becomes the hardest "
             f"constraint in year two, when there are {n(PLAN['cohorts'][2])} "
             f"cohorts and one founder, and the handover has to be designed well "
             f"before it is needed."),
])

# =====================================================================
section("Milestones", [
    ("lead", "What has to be true at the end of each quarter for the next one to be "
             "deliverable."),
    ("table",
     ["Quarter", "Commercial", "Operational", "Product"],
     [["Q4 2026 · Land",
       f"{CAP[0]['ksa']} paid KSA cohorts, {CAP[0]['pilots']} Egyptian free pilots, "
       f"first initiative and sponsor conversations open",
       "4 facilitators certified, Riyadh country manager in post, curriculum "
       "complete in both languages",
       "Admin workspace live, student-controlled sharing, overnight AI review at "
       "cohort volume"],
      ["Q1 2027 · Prove",
       f"{CAP[1]['egypt'] + CAP[1]['ksa']} paid cohorts, first licence signed off a "
       f"pilot report, first sponsored competition run",
       "Cohort report generated without manual editing, 8 facilitators certified",
       "Competition entry, qualification and judging flow; certificates"],
      ["Q2 2027 · Expand",
       f"{CAP[2]['egypt'] + CAP[2]['ksa']} paid cohorts, first sponsored-seat "
       f"programme signed, first corporate programme",
       "12 facilitators certified, train-the-trainer curriculum ready, bilingual "
       "support at volume",
       "Bulk seat provisioning, partner-level reporting by region"],
      ["Q3 2027 · Scale",
       f"{CAP[3]['egypt'] + CAP[3]['ksa']} paid cohorts, first renewals, first "
       f"Riyadh competition",
       "Full pool certified before the quarter opens, parallel-group scheduling for "
       "100-plus intakes",
       "Renewal and second-term licence flows; Day 01 onboarding delivered by "
       "facilitators rather than the founder"]],
     [2.4, 3.9, 3.9, 3.4]),

    ("h2", "What year one has to prove"),
    ("num", [
        "<b>That the cohort report renews a licence.</b> Everything else depends on "
        "an institution buying a second time off the strength of the first report. "
        "One renewal in the Scale quarter is worth more than ten new pilots.",
        "<b>That a sponsor will pay for a competition run on a platform.</b> If "
        "sponsors fund the format, Engine 3 scales without facilitators and opens "
        "universities for free. Four competitions in year one is enough to know.",
        "<b>That a national programme will contract a private platform.</b> This is "
        "unproven and year one deliberately does not depend on it. If it works, "
        "year three is conservative; if it does not, year three still stands on "
        "cohorts, competitions and licences.",
        "<b>That a freelance facilitator delivers the same cohort as an employed "
        "one.</b> If the format does not survive delegation, Engine 1 has a ceiling "
        "of about twenty cohorts a year and the whole mix changes shape.",
    ]),
])

# =====================================================================
section("Appendix — assumptions and sources", [
    ("lead", "Every assumption behind the numbers, so a reader can argue with the "
             "inputs rather than the conclusions."),

    ("h2", "External figures"),
    ("table",
     ["Figure", "Value", "Source"],
     [["Egypt higher-education enrolment, 2024/25", n(HE_STUDENTS["Egypt"]),
       "CAPMAS annual bulletin"],
      ["Saudi tertiary enrolment, 2022", n(HE_STUDENTS["KSA"]),
       "UNESCO UIS. The 84% gross enrolment ratio reported for 2024 implies growth; "
       "the lower figure is held"],
      ["Egypt graduates, 2023", n(ANNUAL_GRADUATES["Egypt"]),
       "CAPMAS, reported via Ahram Online"],
      ["Saudi graduates each year", n(ANNUAL_GRADUATES["KSA"]),
       "Derived: enrolment over a four-year degree, discounted 25%"],
      ["Egypt public colleges", "551", "CAPMAS — 28 universities, 551 colleges"],
      ["MENA startup funding, 2025", "$7.5bn across 647 deals", "Wamda full-year"],
      ["Egypt startup funding, 2025", "$263m across 89 deals", "Wamda"],
      ["Saudi startup funding, 2025", "$5.0bn across 211 deals", "Wamda"],
      ["One Million Entrepreneurs registrations", "~18,000",
       "Egyptian Ministry of Planning"]],
     [5.0, 3.0, 6.4]),

    ("h2", "Counted universes — our estimates"),
    ("table",
     ["Universe", "Value", "Reasoning"],
     [["Institutional buying units", n(M["units"]),
       "551 CAPMAS public colleges plus ~400 Egyptian private faculties; ~45 Saudi "
       "universities at ~12 colleges each plus 24 private colleges"],
      ["Initiative seats a year", n(INITIATIVE_SEATS_PER_YEAR),
       "Addressable across both markets at steady state. Far below the stated "
       "targets, which total several million"],
      ["Competitions a year", n(COMPETITIONS_PER_YEAR),
       "Universities, banks, telcos, ministries and foundations across both markets"],
      ["Large corporates", n(CORPORATES), "With a CSR, innovation or youth budget"],
      ["Incubators and programmes", n(PROGRAMMES),
       "That select applicants and would benefit from a prepared pool"]],
     [4.0, 2.2, 8.2]),

    ("h2", "Pricing assumptions"),
    ("table",
     ["Assumption", "Value", "Reasoning"],
     [["Cohort price", usd(PRICE_COHORT),
       f"{usd(PRICE_COHORT/COHORT_SIZE)} per student — below the per-student cost "
       f"of one external trainer day that leaves nothing behind"],
      ["Faculty licence", usd(PRICE_FACULTY_LICENCE),
       "Every student in a faculty for an academic year; sold only after two "
       "cohorts have run"],
      ["Initiative seat",
       f"{usd(PRICE_INITIATIVE_SEAT[1])} falling to {usd(PRICE_INITIATIVE_SEAT[3])}",
       "Discounted hard against list because volume is the point"],
      ["Train-the-trainer cohort", usd(PRICE_TOT_COHORT[1]),
       "Certifying a partner's own facilitators; the mechanism behind seat volume"],
      ["Sponsored competition",
       f"{usd(PRICE_COMPETITION[1])} rising to {usd(PRICE_COMPETITION[3])}",
       "Benchmarked against what a sponsor pays an event agency for a comparable "
       "activation with no platform and no evidence"],
      ["Corporate programme", usd(PRICE_CORPORATE[1]),
       "Bespoke design and delivery against a CSR or innovation budget"],
      ["Programme seat", usd(PRICE_SEAT[1]),
       "Platform-only, where the partner facilitates"],
      ["Pro / Team subscription", f"{usd(PRICE_PRO_YEAR)} / {usd(PRICE_TEAM_YEAR)}",
       "Priced for a student in Cairo, not a founder in London"]],
     [3.6, 3.0, 7.8]),

    ("h2", "Operating assumptions"),
    ("table",
     ["Assumption", "Value", "Reasoning"],
     [["Faculty fit filter", pct(FILTER_FACULTY_FIT),
       "Business, engineering, computing, design and applied science carry "
       "capstones that map to the missions"],
      ["Delivery reachability", pct(M["reach"]),
       "Greater Cairo, Alexandria, the Delta, Upper Egypt hubs; Riyadh, Jeddah, "
       "Dammam"],
      ["Initiative share one provider could serve", pct(FILTER_INITIATIVE_SHARE),
       f"Year three sits at "
       f"{pct(PLAN['initiative_seats'][3]/INITIATIVE_SEATS_PER_YEAR)} of "
       f"addressable, inside this ceiling"],
      ["Cohorts per facilitator pair per year", n(COHORTS_PER_PAIR_PER_YEAR),
       "One per two weeks, with slack for travel, preparation and campus holidays"],
      ["Facilitator day rate", usd(UE["facilitation"] / (BOOTCAMP_DAYS * 2)),
       "Certified freelance rate, Egypt"],
      ["Competition delivery cost", usd(COMPETITION_DIRECT),
       "Judging, platform setup, event staffing and on-site days"],
      ["B2C subscriber life", "1.6 years",
       "A founder who finishes has no reason to renew a third year; one who stalls "
       "churns inside the first"],
      ["Year-one hiring ramp", "65%",
       "Average establishment across the year; nobody but the founders is on the "
       "payroll from month one"],
      ["Institutional commission", pct(MD.B2B_COMMISSION),
       "Institutional business is sold by people, and people on a number are paid "
       "on it"]],
     [4.0, 2.4, 8.0]),

    ("h2", "What this plan does not claim"),
    ("bul", [
        "It does not claim an outcome number. StartPad records mission progress, "
        "evidence and review scores. It does not certify that a venture will "
        "succeed, and no partnership should be contracted against a metric the "
        "product cannot measure.",
        "It does not assume a second raise. Years two and three are funded from "
        "operations on these numbers.",
        "The subscription conversion rates are modelled, not measured, and so are "
        "the pipeline conversion rates. Both will be replaced with observed figures "
        "after the first cohort quarter.",
        "Competition and corporate pricing is benchmarked against comparable "
        "sponsorship spend rather than against signed StartPad deals, because there "
        "are none yet. These are the prices most likely to move after the first four "
        "competitions.",
    ]),
])
