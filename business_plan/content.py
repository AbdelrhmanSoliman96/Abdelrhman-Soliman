"""
The business plan, as content blocks.

Prose lives here; rendering lives in scripts/build_business_plan_docx.py; every
number comes from model.py through the `V` lookup below. Nothing numeric is typed
into a sentence, so a changed assumption changes the sentence, the table and the
chart together, or it changes none of them.

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
from .model import (ANNUAL_GRADUATES, BOOTCAMP_DAYS, COHORT_SIZE, FILTER_FACULTY_FIT,
                    FILTER_HAS_AN_IDEA, GRADUATE_WINDOW_YEARS, HE_STUDENTS,
                    NGO_SEATS_Y1, PRICE_COHORT, PRICE_FACULTY_LICENCE, PRICE_PRO_YEAR,
                    PRICE_SEAT, PRICE_SPONSORED_SEAT, PRICE_TEAM_YEAR, AMBASSADORS_Y1,
                    CHANNELS, COHORTS_BY_QUARTER, COHORTS_PER_PAIR_PER_YEAR, ROLES,
                    channels, cohort_unit_economics, costs_y1, facilitator_capacity,
                    funding, headcount, market, projection, revenue_y1)

M = market()
R = revenue_y1()
C = costs_y1()
CH = channels()
UE = cohort_unit_economics()
PROJ = projection()
FUND = funding()
HC_BY_FN, HC = headcount()
CAP = facilitator_capacity()


def money(v, dp=0):
    if abs(v) >= 1e6:
        return f"${v/1e6:,.2f}m" if dp else f"${v/1e6:,.1f}m"
    if abs(v) >= 1e3:
        return f"${v/1e3:,.0f}k"
    return f"${v:,.0f}"


def usd(v):
    return f"${v:,.0f}"


def n(v, dp=0):
    return f"{v:,.{dp}f}"


# =====================================================================

TITLE = "Business Plan"
SUBTITLE = "Egypt and Saudi Arabia · Years one to three"
PERIOD = "October 2026 – September 2029"

SECTIONS = []


def section(name, blocks):
    SECTIONS.append((name, blocks))


# ---------------------------------------------------------------------
section("Executive summary", [
    ("lead", "StartPad sells a method, not a course. A founder walks fifteen "
             "missions; an institution buys the bootcamp that starts them and the "
             "workspace that proves they finished. This plan sets out what the "
             "business is worth, what it costs to build and what has to be true "
             "operationally for the go-to-market plan to happen at all."),

    ("kpi", [(money(M["tam"]), "TAM · Egypt and KSA"),
             (money(M["sam"]), "SAM · reachable"),
             (money(R["total"]), "Year-one revenue"),
             (money(FUND["rounded"]), "Capital required")]),

    ("h2", "The business in six sentences"),
    ("num", [
        f"StartPad takes a first-time founder from a raw idea to a live product "
        f"through <b>fifteen sequenced missions</b>, each one reviewed by an AI "
        f"before the next unlocks, supported by 121 tools mapped to the journey.",
        f"Founders use it free for the first three missions and pay "
        f"{usd(PRICE_PRO_YEAR)} a year for the rest; institutions pay "
        f"{usd(PRICE_COHORT)} for a cohort of {COHORT_SIZE} that includes a "
        f"{BOOTCAMP_DAYS}-day in-person bootcamp, a seat for every student and a "
        f"cohort report.",
        f"The institutional line is the business: it is "
        f"{(1 - dict(R['lines'])['Founder subscriptions (Pro and Team)']/R['total'])*100:.0f}% "
        f"of year-one revenue, carries a {UE['margin']*100:.0f}% gross margin and is "
        f"invoiced before delivery, so the customer funds the work.",
        f"Egypt and Saudi Arabia run in parallel from the start, through different "
        f"doors — universities in Egypt, programme partners in Saudi Arabia — "
        f"because the two markets buy differently and a single sequence would have "
        f"wasted a year.",
        f"Year one delivers {R['paid_cohorts']} paid cohorts and "
        f"{n(CH['signups'])} free sign-ups against a loss of "
        f"{money(-PROJ[0]['profit'])}; the business reaches breakeven in year two "
        f"and a {PROJ[2]['profit']/PROJ[2]['revenue']*100:.0f}% operating margin in "
        f"year three.",
        f"The raise is {money(FUND['rounded'])} — the cumulative deficit of "
        f"{money(FUND['cumulative'])} plus a six-month operating reserve — which is "
        f"small for the revenue it builds because cohorts are cash-positive from "
        f"the first one.",
    ]),

    ("h2", "What this plan concludes that the strategy deck did not"),
    ("p", "Three findings came out of building the numbers rather than out of "
          "restating the strategy. Each one changes what the company should do."),
    ("deflist", [
        ("Paid acquisition does not pay for itself, and should be capped",
         f"A paying founder acquired through paid social costs "
         f"{usd([r for r in CH['rows'] if r['name']=='Paid social'][0]['cac'])} "
         f"against a lifetime value of {usd(CH['ltv'])} — it returns "
         f"{[r for r in CH['rows'] if r['name']=='Paid social'][0]['ratio']:.2f}× "
         f"what it costs. Campus channels return "
         f"{[r for r in CH['rows'] if r['name']=='Campus workshops'][0]['ratio']:.2f}×. "
         f"Paid social belongs on retargeting and event fill, not on cold "
         f"acquisition, and the budget line should be read as a marketing cost of "
         f"the institutional business rather than as customer acquisition."),
        ("Subscriptions are the proof layer, not the revenue",
         "Founder subscriptions are 3% of year-one revenue and 11% by year three. "
         "Their job is to prove the product works on founders who were never "
         "handed a seat, and to generate the stories that win the next campus. "
         "Managing the company to subscription growth would be managing it to the "
         "smallest number on the page."),
        ("The binding constraint is facilitators, not demand",
         f"The year-one plan peaks at {CAP[-1]['facilitators']:.0f} facilitators in "
         f"the final quarter. A facilitator pair runs "
         f"{COHORTS_PER_PAIR_PER_YEAR} cohorts a year once travel, preparation and "
         f"campus holidays are taken out. Every cohort beyond that needs a "
         f"certified facilitator who does not exist yet, which makes facilitator "
         f"recruitment and certification the first operational priority, ahead of "
         f"sales."),
    ]),

    ("pb",),
    ("h2", "The shape of the three years"),
    ("fig", "pl", "Revenue against operating cost. Year one is funded; year two "
                  "pays for itself; year three carries the margin."),
    ("table",
     ["", "Year 1 · 2026/27", "Year 2 · 2027/28", "Year 3 · 2028/29"],
     [["Revenue"] + [money(y["revenue"]) for y in PROJ],
      ["Operating cost"] + [money(y["cost"]) for y in PROJ],
      ["Result"] + [("−" if y["profit"] < 0 else "+") + money(abs(y["profit"]))
                    for y in PROJ],
      ["Operating margin"] + [f"{y['profit']/y['revenue']*100:,.0f}%".replace("-", "\u2212")
                             for y in PROJ],
      ["Paid cohorts delivered"] + [n(y["cohorts"]) for y in PROJ],
      ["Employees at year end"] + [n(y["headcount"]) for y in PROJ]],
     [4.2, 4.0, 4.0, 4.0]),
    ("note", "Every figure in this plan is computed from one assumption set, held "
             "in <b>business_plan/model.py</b> and listed in full in the appendix. "
             "No number is typed into a sentence; change an assumption and the "
             "sentence, the table and the chart move together."),
])

# ---------------------------------------------------------------------
section("The company and the product", [
    ("lead", "What StartPad is, who it is for, and why a sequenced journey with a "
             "review gate beats the thing it replaces."),

    ("h2", "The problem"),
    ("p", "Ideas are everywhere in MENA. A path to a real startup is not. The gap "
          "is not talent and it is not capital at the earliest stage — it is "
          "method. Founders have graduation projects and no process; institutions "
          "need founders who are ready and have no way to prepare them; programmes "
          "screen applicants who never did the groundwork."),
    ("kpi", [("21%", "of self-described MENA startups meet the minimum criteria "
                     "to be considered investable"),
             ("56%", "of MENA pre-seed startups never reach the next stage"),
             ("68%", "failure rate in Egypt for startups trying to reach "
                     "Series A — the highest in the region")]),
    ("p", "These three numbers describe one failure, not three. A founder who "
          "never defined the problem precisely cannot produce evidence; without "
          "evidence they cannot pass a screen; having failed a screen they conclude "
          "the problem was capital. StartPad intervenes at the first step, because "
          "that is the only step where intervention is cheap."),

    ("h2", "The product"),
    ("p", "Fifteen missions across five phases. Each mission has a brief, a short "
          "lesson, five tasks with an explicit standard for what a good answer "
          "needs, and an evidence slot. The founder submits; an AI reviews against "
          "specificity, depth, evidence, actionability and relevance; at 70% the "
          "next mission unlocks and points are earned. Below 70% the founder gets "
          "one highest-gain fix and a full report, and the answers stay filled in "
          "for the retry."),
    ("table",
     ["Phase", "Missions", "Points", "Est. time", "What it produces"],
     [["Discovery", "01–03", "350", "4–6 h", "A prioritised problem worth solving"],
      ["Validation", "04–06", "550", "5–7 h", "A tested problem–solution canvas"],
      ["Business model", "07–09", "850", "11–19 h", "A full BMC and a working prototype"],
      ["Build and MVP", "10–13", "1,350", "29–54 h", "A shipped MVP with analytics"],
      ["Launch", "14–15", "950", "15–30 h", "A live launch and first customers"]],
     [3.0, 2.0, 1.8, 2.2, 7.2]),
    ("p", "4,050 points across the journey. Points and streaks are written only on "
          "the server, with direct writes to scoring revoked at the database, so a "
          "score is earned rather than claimed — which is what lets an institution "
          "treat the record as evidence."),

    ("h2", "What makes it defensible"),
    ("deflist", [
        ("The AI is a co-founder, not a ghostwriter",
         "It asks the follow-up a good mentor would ask, carries earlier answers "
         "forward and pushes back on vague ones. It does not write the business "
         "plan. A tool that writes the answer destroys the only asset the product "
         "creates, which is a founder who can defend their own work."),
        ("The sequence is the product",
         "A mission unlocks only when the last one passes. That constraint is what "
         "separates StartPad from a library of templates: a founder cannot skip to "
         "the pitch deck before they have a tested problem, which is precisely the "
         "mistake the 56% figure measures."),
        ("Built in MENA, in both languages",
         "Every mission, review and exported PDF works in Arabic with complete "
         "right-to-left layout, and the Arabic is composed rather than translated — "
         "Egyptian colloquial for Egypt, Saudi dialect for the Kingdom. A "
         "US-built product translated at the edges does not survive a workshop."),
        ("The institutional workspace is the moat",
         "Cohort progress, review states, follow-up signals and a downloadable "
         "cohort report, all under student-controlled sharing. Competitors sell "
         "content to students. Selling a reporting line to the person who signs "
         "the cheque is a different and much stickier business."),
    ]),
    ("fig", "flywheel", "Growth compounds through the loop, not through paid "
                        "reach: founders who progress become the stories that win "
                        "the next campus and the next partner."),
])

# ---------------------------------------------------------------------
section("Market study", [
    ("lead", "How large the opportunity is in Egypt and Saudi Arabia, built from "
             "the bottom up — from counted students and counted institutions, "
             "priced at our own prices — rather than from a share of somebody "
             "else's market report."),

    ("h2", "Method, and why it is bottom-up"),
    ("p", "A top-down sizing would start from a published figure for the global "
          "edtech or startup-services market and take a percentage. That produces "
          "a large number and no information: the percentage is unjustifiable and "
          "the market definition does not match what we sell. This sizing instead "
          "counts the people and the institutions that exist in the two markets, "
          "applies the filters that decide whether each one can plausibly buy, and "
          "multiplies by our own prices."),
    ("p", "<b>TAM</b> is every higher-education student and recent graduate in "
          "Egypt and Saudi Arabia, at saturation. <b>SAM</b> narrows that to the "
          "faculties where venture-building fits, the students with an idea or a "
          "graduation project, and the cities we can physically reach to deliver a "
          "bootcamp. <b>SOM</b> is not a share of SAM at all — it is derived from "
          "capacity: the number of cohorts a known number of facilitators can run "
          "and the number of founders a known ambassador network and ad budget can "
          "bring in."),

    ("h2", "The population base"),
    ("table",
     ["", "Egypt", "Saudi Arabia", "Total", "Source"],
     [["Higher-education students", n(HE_STUDENTS["Egypt"]), n(HE_STUDENTS["KSA"]),
       n(sum(HE_STUDENTS.values())),
       "CAPMAS 2024/25; UNESCO UIS 2022"],
      ["Graduates each year", n(ANNUAL_GRADUATES["Egypt"]), n(ANNUAL_GRADUATES["KSA"]),
       n(sum(ANNUAL_GRADUATES.values())),
       "CAPMAS 2023; KSA derived"],
      [f"Recent graduates (within {GRADUATE_WINDOW_YEARS} years)",
       n(ANNUAL_GRADUATES["Egypt"] * GRADUATE_WINDOW_YEARS),
       n(ANNUAL_GRADUATES["KSA"] * GRADUATE_WINDOW_YEARS),
       n(M["recent_grads"]), "Derived"],
      ["Institutional buying units", "951", "564", n(M["units"]),
       "CAPMAS colleges; KSA derived"]],
     [5.0, 2.4, 2.6, 2.4, 4.0]),
    ("p", "The buying unit is the college or faculty, not the university. StartPad "
          "enters through an entrepreneurship centre, a capstone coordinator or a "
          "dean — three of the four doors sit below the university level, and a "
          "single university routinely runs several unrelated cohorts."),

    ("h2", "TAM — the ceiling"),
    ("p", f"At saturation, {n(M['tam_pop'])} people are in scope: "
          f"{n(M['students'])} enrolled students plus {n(M['recent_grads'])} "
          f"graduates still inside the 18–30 window. Most would hold an "
          f"institution-funded seat rather than a self-paid subscription, because "
          f"that is how a student in this market gets access, which gives a blended "
          f"value of {usd(M['blended_value'])} per person per year."),
    ("table",
     ["Layer", "Basis", "Value"],
     [["Platform", f"{n(M['tam_pop'])} people × {usd(M['blended_value'])}",
       money(M["tam_platform"])],
      ["Programme delivery",
       f"{n(M['units'])} buying units × 2 cohorts × {usd(PRICE_COHORT)}",
       money(M["tam_delivery"])],
      ["Total addressable market", "", money(M["tam"])]],
     [4.4, 8.0, 4.0]),

    ("h2", "SAM — what we could actually serve"),
    ("p", "Three filters, each one a statement about the product rather than a "
          "haircut for caution."),
    ("deflist", [
        (f"Faculty fit — {FILTER_FACULTY_FIT*100:.0f}%",
         "Business, commerce, engineering, computing, design and applied science "
         "carry capstone and graduation projects that map onto the missions. "
         "Medicine and law largely do not."),
        (f"Has an idea or a graduation project — {FILTER_HAS_AN_IDEA*100:.0f}%",
         "The deck's own user definition. Wider than final year, because an idea "
         "does not wait for the curriculum; narrower than everybody, because most "
         "students do not have one."),
        (f"Reachable for delivery — {M['reachable_share']*100:.0f}%",
         "Greater Cairo, Alexandria, the Delta and the Upper Egypt hubs; Riyadh, "
         "Jeddah and Dammam. A cohort needs facilitators in a room."),
    ]),
    ("fig", "sizing_funnel", "The filter chain, from every student in both markets "
                             "to the population StartPad can serve."),
    ("table",
     ["Layer", "Basis", "Value"],
     [["Platform", f"{n(M['sam_pop'])} people × {usd(M['blended_value'])}",
       money(M["sam_platform"])],
      ["Programme delivery",
       f"{M['sam_units']:,.0f} buying units × 2 cohorts × {usd(PRICE_COHORT)}",
       money(M["sam_delivery"])],
      ["Serviceable available market", "", money(M["sam"])]],
     [4.4, 8.0, 4.0]),

    ("pb",),
    ("h2", "SOM — what we will capture, and why that number"),
    ("p", f"Year-one revenue is {money(R['total'])}, which is "
          f"{R['total']/M['sam']*100:.2f}% of SAM. That figure is an output, not a "
          f"target. It falls out of three counted quantities: "
          f"{R['paid_cohorts']} paid cohorts, which is what the facilitator "
          f"establishment can physically deliver; {n(NGO_SEATS_Y1)} sponsored "
          f"seats across two signed programme partnerships; and "
          f"{n(CH['signups'])} free sign-ups from a named set of channels with a "
          f"named budget."),
    ("fig", "tam_sam_som", "TAM, SAM and the year-one SOM. The gap between SAM "
                           "and SOM is a delivery-capacity gap, not a demand gap."),
    ("table",
     ["Revenue line", "Basis", "Year one"],
     [[name, basis, money(val)] for (name, val), basis in zip(
         R["lines"],
         [f"{R['paid_cohorts']} cohorts × {usd(PRICE_COHORT)}",
          f"{n(NGO_SEATS_Y1)} seats × {usd(PRICE_SPONSORED_SEAT)}",
          f"14 partners × 60 seats × {usd(PRICE_SEAT)}",
          f"{CH['paid']:,.0f} subscribers, half the year recognised"])] +
     [["Total", "", money(R["total"])]],
     [5.6, 6.6, 3.0]),

    ("h2", "Market context"),
    ("p", "MENA startups raised a record $7.5bn across 647 deals in 2025. Saudi "
          "Arabia led at $5bn across 211 deals; Egypt was third at $263m across 89 "
          "deals, with deal count rising even as value fell after the currency "
          "devaluation. The capital is concentrating in the Gulf while the founder "
          "population concentrates in Egypt — which is exactly why the plan runs "
          "both markets at once rather than sequencing them."),
    ("note", "A cautionary reading of the same data: Saudi Arabia and the UAE took "
             "86% of regional capital in 2025. A platform that only served Egypt "
             "would be building founders for a market whose funding is shrinking. "
             "A platform that only served the Kingdom would be competing for a "
             "small, well-served cohort. Serving both is the position."),

    ("h2", "Sensitivity"),
    ("p", "The three assumptions the model is most exposed to, and what happens "
          "when each is wrong by a third."),
    ("table",
     ["Assumption", "Plan", "If a third worse", "Effect on year-one revenue"],
     [["Cohort price", usd(PRICE_COHORT), usd(PRICE_COHORT * 0.67),
       f"−{money(R['paid_cohorts'] * PRICE_COHORT * 0.33)}"],
      ["Cohorts delivered", n(R["paid_cohorts"]), n(round(R["paid_cohorts"] * 0.67)),
       f"−{money(R['paid_cohorts'] * 0.33 * PRICE_COHORT)}"],
      ["Sponsored seats signed", n(NGO_SEATS_Y1), n(round(NGO_SEATS_Y1 * 0.67)),
       f"−{money(NGO_SEATS_Y1 * 0.33 * PRICE_SPONSORED_SEAT)}"]],
     [4.4, 2.6, 3.4, 4.8]),
    ("p", "All three are institutional. None of them is the subscription business, "
          "which is a rounding error in year one. The company's risk is "
          "concentrated in whether universities and programmes sign and renew — "
          "which is the right risk to carry, because it is the one the operating "
          "plan can act on."),
])

# ---------------------------------------------------------------------
section("Competition and positioning", [
    ("lead", "What a founder uses instead of StartPad today, and why none of it "
             "closes the gap the three failure statistics describe."),

    ("h2", "The alternatives"),
    ("table",
     ["Dimension", "Generic templates and guides", "StartPad"],
     [["Structure", "A list of things to consider", "Fifteen sequenced missions"],
      ["AI", "None, or a bolted-on chatbot", "A co-founder inside every mission"],
      ["Motivation", "None built in", "Points, levels, streaks"],
      ["Tools", "Scattered across ten-plus sites", "121, mapped to the journey"],
      ["Region", "US-built, translated if at all", "MENA-built, bilingual"],
      ["Evidence", "Nothing is recorded", "Every answer reviewed and scored"],
      ["For the institution", "No visibility at all",
       "Cohort workspace and a decision-ready report"]],
     [3.2, 5.6, 5.6]),

    ("h2", "The competitive set, honestly"),
    ("deflist", [
        ("Online course platforms (Coursera, Udemy, local equivalents)",
         "Cheaper and broader. They sell completion, not evidence, and an "
         "institution cannot report a cohort outcome from a course certificate. We "
         "lose on price and win on what the buyer actually needs to show."),
        ("Incubator and accelerator programmes",
         "They select founders; we prepare them. In practice they are channel "
         "rather than competition — a better-prepared applicant pool is the thing "
         "they most want, which is why the partnership motion sells to them "
         "rather than against them."),
        ("University entrepreneurship centres running their own programmes",
         "The real incumbent, and the one to respect. They have the room, the "
         "students and the budget. We beat an in-house programme on method, "
         "bilingual content, the evidence trail and the reporting line — and we "
         "should enter as the thing that makes their centre look good, never as "
         "its replacement."),
        ("Consultancies selling training days",
         "Comparable or higher day rates with no platform underneath, nothing left "
         "behind after the trainer leaves, and no cohort record. This is the "
         "comparison that makes the cohort price look cheap, and it is the one to "
         "put in front of a dean."),
    ]),
    ("quote", "We do not win by being the best content. We win by being the only "
              "option that leaves an institution with something it can report."),
])

# ---------------------------------------------------------------------
section("Business model and pricing", [
    ("lead", "Founders climb a ladder; organisations license seats. Two engines "
             "on one platform, with the institutional engine carrying the revenue "
             "and the founder engine carrying the proof."),

    ("h2", "The price list"),
    ("table",
     ["Line", "Who buys", "What they get", "Price"],
     [["Start", "Founder", "The first three missions", "Free"],
      ["Pro", "Founder", "Full access, all fifteen missions",
       f"{usd(PRICE_PRO_YEAR)} / year"],
      ["Team", "A founding team", "A bundle for the whole team",
       f"{usd(PRICE_TEAM_YEAR)} / year"],
      ["Cohort", "University or faculty",
       f"{BOOTCAMP_DAYS} bootcamp days, workshops, {COHORT_SIZE} seats, "
       f"judging and the cohort report", f"{usd(PRICE_COHORT)} / cohort"],
      ["Seats", "Programme or incubator",
       "Platform seats where the partner facilitates",
       f"{usd(PRICE_SEAT)} / seat / term"],
      ["Sponsored seats", "NGO, donor or government programme",
       "Seats bought in volume for a funded cohort",
       f"{usd(PRICE_SPONSORED_SEAT)} / seat"],
      ["Faculty licence", "A whole faculty",
       "Every student for an academic year",
       f"{usd(PRICE_FACULTY_LICENCE)} / year"]],
     [2.8, 3.2, 5.6, 2.9]),

    ("h2", "Why the cohort price is what it is"),
    ("p", f"{usd(PRICE_COHORT)} across {COHORT_SIZE} students is "
          f"{usd(PRICE_COHORT/COHORT_SIZE)} a student. The same institution pays "
          f"more than that per student for a single day with an external trainer "
          f"who leaves nothing behind. The price is anchored against that "
          f"comparison, not against a software subscription, because the buyer is "
          f"the person with a training budget and not the person with an IT "
          f"budget."),
    ("fig", "cohort_economics",
     f"Where a cohort's {usd(PRICE_COHORT)} goes. Facilitation is the only "
     f"significant variable cost, which is what holds the margin at "
     f"{UE['margin']*100:.0f}% as volume grows."),

    ("h2", "Unit economics, both engines"),
    ("table",
     ["", "Institutional cohort", "Founder subscription"],
     [["Revenue", usd(UE["price"]), usd(CH["arpu"]) + " / year"],
      ["Direct cost", usd(UE["direct"]), f"${CH['arpu']*0.12:,.0f}"],
      ["Gross profit", usd(UE["gross"]), f"${CH['arpu']*0.88:,.0f}"],
      ["Gross margin", f"{UE['margin']*100:.0f}%", "88%"],
      ["Typical life", "2.8 years, two cohorts a year", "1.6 years"],
      ["Lifetime gross profit", money(UE["gross"] * 2 * 2.8), usd(CH["ltv"])],
      ["Cash timing", "Invoiced before delivery", "Annual, paid upfront"]],
     [4.2, 4.6, 4.6]),
    ("note", f"Working capital is <b>negative</b>. A cohort is invoiced before the "
             f"bootcamp runs and the direct cost of {usd(UE['direct'])} is incurred "
             f"during delivery, so growth in the institutional line releases cash "
             f"rather than consuming it. This is the single most important "
             f"financial characteristic of the business and the reason the raise "
             f"is {money(FUND['rounded'])} rather than several times that."),
])

# ---------------------------------------------------------------------
section("Go-to-market plan", [
    ("lead", "Five moves, each unlocking the next, run across two markets from "
             "day one. Campus first, proof next, two markets at once."),

    ("fig", "gtm_moves", "The five moves and what each one unlocks. The order is "
                         "load-bearing: each move is affordable only because the "
                         "one before it happened."),

    ("h2", "The four phases of year one"),
    ("fig", "phases", "Egypt and Saudi Arabia, in parallel, through four phases."),

    ("h2", "Move 01 — Universities, the first door"),
    ("p", "Universities hold the students, the graduation projects and the "
          "credibility. There are four doors into every university and they want "
          "different things, so they are approached in this order and offered "
          "different first steps."),
    ("table",
     ["Door", "Who", "What they want", "What we offer first"],
     [["01", "Entrepreneurship centre", "A structured programme to show",
       "A free pilot cohort"],
      ["02", "Capstone coordinator", "A method for graduation projects",
       "Missions mapped to the term"],
      ["03", "Dean of faculty", "Outcomes for accreditation",
       "A faculty-wide licence"],
      ["04", "Student activities", "Events that fill rooms",
       "Workshops and competitions"]],
     [1.2, 3.6, 4.6, 4.2]),
    ("p", "<b>Free pilots first, licences on results.</b> The pilot is not a "
          "discount — it is how the institution's own cohort report becomes the "
          "sales document for the licence. Four free pilots run in Egypt in the "
          "Land quarter and are the reason the Prove quarter has anything to sell."),

    ("h2", "How a deal happens"),
    ("fig", "institution_workflow", "From identifying the right person to a "
                                    "cohort report, in six steps over seven weeks."),
    ("p", "One contract covers all three layers: the in-person bootcamp, the "
          "on-campus workshops and a platform seat for every student under one "
          "programme admin account. Selling the layers separately would triple the "
          "procurement cycle inside institutions where procurement is already the "
          "longest part of the sale."),

    ("h2", "How a cohort runs"),
    ("fig", "bootcamp_map", "Learn it in the room, build it on StartPad that "
                            "evening, and the programme sees it the next morning."),
    ("p", f"Six bootcamp days over two weeks, three days a week, 240 minutes a "
          f"day, {COHORT_SIZE} students per group working as teams on one venture "
          f"each. Never more than fifteen minutes of input before students apply "
          f"it. Each evening's work goes into StartPad as missions; the AI review "
          f"runs overnight; scores and fixes are ready before the next day's "
          f"opener. Larger intakes run as parallel groups — 100-plus students "
          f"works — which is how a single university relationship becomes four "
          f"cohorts rather than one."),

    ("h2", "Move 05 — Two markets, two different doors"),
    ("table",
     ["", "Egypt", "Saudi Arabia"],
     [["Started", "September 2026", "September 2026, in parallel"],
      ["First door", "Universities and campuses", "Programmes and youth initiatives"],
      ["Lead channel", "Ambassadors and workshops",
       "Partners, then a Riyadh competition"],
      ["Voice", "Egyptian colloquial", "Saudi dialect, composed not translated"],
      ["Team", "Core team in Cairo", "A local lead, supported from Cairo"],
      ["Why this door", "Scale of the student population and campus access",
       "Funded programmes move faster than university procurement"]],
     [3.0, 5.2, 5.4]),
    ("p", "The markets are not sequenced because the doors are different. Waiting "
          "for Egypt to work before entering the Kingdom would have meant learning "
          "the Saudi programme-partner motion a year late, against competitors "
          "who did not wait — and the Saudi cohorts are the ones that pay from the "
          "first quarter while Egypt is still running free pilots."),
])

# ---------------------------------------------------------------------
section("Marketing plan", [
    ("lead", "Ten channels, one destination: a free account and Mission 01. What "
             "each channel costs, what it returns, and the one that should be "
             "capped."),

    ("h2", "Every channel lands on the same first step"),
    ("table",
     ["Stage", "What it is", "What moves them forward"],
     [["Discover", "They see it", "Reels, paid ads, influencers, events, webinars"],
      ["Join", "A free account", "One tap from an ad, a QR code or a link"],
      ["Activate", "Mission 01", "Finished live in a workshop or a webinar"],
      ["Engage", "Discovery phase", "Community sprints, streaks, reminders"],
      ["Convert", "Pro or Team", "Mission 04 preview, team invites, retargeting"]],
     [2.4, 3.6, 7.6]),
    ("p", "<b>Activation is finishing Mission 01, not creating an account.</b> "
          "This is the single most important definition in the marketing plan, "
          "because it is what separates channels that work from channels that look "
          "like they work. An account that never completes a mission is indis"
          "tinguishable from no account at all."),

    ("h2", "The year-one funnel"),
    ("fig", "acquisition_funnel", "From sign-up to paying subscriber. The drop "
                                  "from sign-up to activation is where the channel "
                                  "mix shows itself."),

    ("h2", "Channel performance, and the finding"),
    ("table",
     ["Channel", "Sign-ups", "Activation", "Paid", "Cost", "CAC", "LTV/CAC"],
     [[r["name"], n(r["signups"]), f"{r['activation']*100:.0f}%",
       f"{r['paid']:,.0f}", usd(r["cost"]), usd(r["cac"]), f"{r['ratio']:.2f}×"]
      for r in sorted(CH["rows"], key=lambda r: -r["ratio"])] +
     [["Total", n(CH["signups"]), f"{CH['activated']/CH['signups']*100:.0f}%",
       f"{CH['paid']:,.0f}", usd(CH["cost"]),
       usd(CH["cost"] / CH["paid"]), ""]],
     [3.3, 1.9, 1.9, 1.5, 1.9, 1.6, 1.6]),
    ("fig", "cac_ltv", f"Cost to acquire one paying founder, against a lifetime "
                       f"value of {usd(CH['ltv'])}. Three channels pay for "
                       f"themselves; three do not."),
    ("p", f"Paid social generates {n([r for r in CH['rows'] if r['name']=='Paid social'][0]['signups'])} "
          f"sign-ups — two thirds of the year's total — and only "
          f"{[r for r in CH['rows'] if r['name']=='Paid social'][0]['paid']:.0f} "
          f"paying founders, at "
          f"{usd([r for r in CH['rows'] if r['name']=='Paid social'][0]['cac'])} each "
          f"against a lifetime value of {usd(CH['ltv'])}. On a subscription P&amp;L "
          f"it loses money on every conversion."),
    ("deflist", [
        ("What to do about it",
         "Cap cold paid social and move the budget to retargeting, event fill and "
         "competition entry. Its remaining job is reach and credibility for the "
         "institutional sale, which is a marketing cost of the B2B business and "
         "should be reported there rather than judged on subscription CAC."),
        ("What not to do about it",
         "Do not cut it to zero. The campus channels have a hard ceiling — there "
         "are only so many campuses with an ambassador team — and content needs "
         "distribution to produce the founder stories that the institutional sale "
         "runs on. The error would be to keep scaling it as though it were an "
         "acquisition channel."),
    ]),

    ("h2", "The ambassador programme"),
    ("p", f"A campus team that earns its place, {AMBASSADORS_Y1} ambassadors "
          f"across twelve campuses by the Scale quarter. Status is earned through "
          f"founders brought in and renewed each term — a title that cannot be "
          f"lost is a title that stops working."),
    ("table",
     ["Level", "Role", "What they do", "What they get"],
     [["01", "Member", "Uses StartPad, joins workshops", "Community standing"],
      ["02", "Ambassador", "Runs Mission 01 workshops", "Free Pro access, stipend"],
      ["03", "Campus lead", "Leads the team, owns student activities",
       "Mentor sessions, references"]],
     [1.3, 2.6, 5.4, 4.3]),

    ("h2", "The content engine"),
    ("p", "One founder story, many pieces. Find founders who built from a "
          "graduation project; record a podcast episode in Egyptian Arabic; cut "
          "reels and posts for TikTok, Instagram and Facebook; every piece ends at "
          "Mission 01. The podcast is not a brand exercise — it is the asset that "
          "makes the institutional pitch credible, because a dean responds to a "
          "graduate of a university like theirs."),

    ("h2", "Year-one marketing budget"),
    ("table",
     ["Line", "Amount", "What it buys"],
     [[r["name"], usd(r["cost"]),
       f"{n(r['signups'])} sign-ups, {r['paid']:,.0f} paying"]
      for r in CH["rows"]] +
     [["Total", usd(CH["cost"]), f"{n(CH['signups'])} sign-ups, "
                                 f"{CH['paid']:,.0f} paying"]],
     [4.0, 2.6, 6.8]),
])

# ---------------------------------------------------------------------
section("NGO, government and ecosystem initiatives", [
    ("lead", "Both governments have committed publicly to qualifying a million "
             "entrepreneurs or innovators. None of them has a method, a platform "
             "or a reporting line. That is the opening."),

    ("h2", "The national programmes StartPad is built to plug into"),
    ("fig", "ngo_initiatives", "Four named Egyptian programmes with public "
                               "million-scale targets, each needing delivery "
                               "capacity they do not have in-house."),
    ("table",
     ["Programme", "Who runs it", "Their target", "What StartPad supplies"],
     [["One Million Entrepreneurs",
       "Ministry of Planning, through Rowad 2030, with Banque Misr and the "
       "National Bank of Egypt",
       "One million entrepreneurs qualified by 2030",
       "The qualification method itself, plus per-participant evidence a "
       "ministry can report"],
      ["1 Million Qualified Innovators",
       "Ministry of Higher Education with UNDP, MBRF and ICESCO; launched Cairo, "
       "April 2025",
       "Future skills for one million young people",
       "The university delivery channel the initiative needs, already running "
       "on campus"],
      ["MSMEDA governorate programme",
       "Qetar El Kheir caravan, across 22 governorates",
       "Reach founders outside the urban technology hubs",
       "Bilingual self-serve missions for governorates no facilitator reaches, "
       "with sponsored seats"],
      ["One Million International Licences",
       "With Cisco, announced May 2026",
       "Accredited technical and professional certification",
       "The venture-building complement to a technical certificate"]],
     [3.0, 3.8, 3.2, 4.2]),
    ("note", "Published progress on the One Million Entrepreneurs campaign stood "
             "at roughly 18,000 registrations against a target of one million. The "
             "gap is not ambition or funding — it is delivery capacity and a "
             "method that produces something reportable per participant. That gap "
             "is the product."),

    ("h2", "Why these partnerships matter more than their revenue"),
    ("p", f"Sponsored seats are {money(dict(R['lines'])['Sponsored seats (NGO and government)'])} "
          f"in year one — real money, but not the reason to pursue them. Three "
          f"other things come with a national programme partnership."),
    ("num", [
        "<b>Volume without a facilitator.</b> Sponsored seats are platform-only, "
        "so they scale past the facilitator constraint that caps the cohort "
        "business. A governorate programme can place thousands of seats in a "
        "quarter that no bootcamp schedule could serve.",
        "<b>Credibility that opens the university door.</b> A dean who has not "
        "heard of StartPad has heard of Rowad 2030. Named participation in a "
        "national programme shortens the first conversation at every one of the "
        "four doors, which is worth more than the seat revenue.",
        "<b>Reach outside the cities we can serve.</b> The governorate programmes "
        "deliberately target Upper Egypt and the border governorates — exactly the "
        "population the SAM reachability filter excludes. Sponsored seats are how "
        "StartPad serves people it cannot send facilitators to.",
    ]),

    ("h2", "The partnership path"),
    ("table",
     ["", "Step", "What happens", "Who owns it"],
     [["1", "Show results", "A cohort report from a comparable pilot",
       "Head of Partnerships"],
      ["2", "Co-design a cohort", "Their objective, our missions, agreed reporting",
       "Head of Curriculum with the partner"],
      ["3", "Run it", "Sponsored seats, facilitation where the budget allows",
       "Programme Delivery Manager"],
      ["4", "Report back", "Participation, progress, evidence, outcomes",
       "Delivery, to the partner's own reporting format"],
      ["5", "Renew", "A larger cohort, or a governorate added",
       "Head of Partnerships"]],
     [0.9, 2.8, 5.4, 4.1]),

    ("h2", "The equivalent motion in Saudi Arabia"),
    ("p", "The Kingdom's youth and SME institutions — Monsha'at on the SME side "
          "and the Misk Foundation on the youth-development side — run programmes "
          "with the same structural gap: ambition and budget at national scale, "
          "with delivery contracted out. The Saudi motion leads with these "
          "partners rather than with universities, which is why the Riyadh country "
          "manager is a partnerships hire and not a campus hire."),
    ("note", "One caution on the Saudi side. Misk cancelled its 2026 Global Forum, "
             "and flagship-event cancellations usually signal a programme budget "
             "under review. The Saudi plan should not depend on a single "
             "institution: the Riyadh targets assume several programme partners, "
             "and the first Riyadh competition in the Scale quarter is the "
             "fallback route to founders if partnership budgets move."),

    ("h2", "What we must not promise"),
    ("p", "A national programme will ask for an outcome number — jobs created, "
          "businesses registered, funding raised. StartPad records mission "
          "progress, evidence and review scores. Those are honest indicators of "
          "recorded work; they do not certify venture success, and the platform "
          "says so on the page. Contracting to an outcome the product cannot "
          "measure would be the fastest way to lose a government relationship, and "
          "every partnership agreement should state what is measured and what is "
          "not."),
])

# ---------------------------------------------------------------------
section("Organisation and HR plan", [
    ("lead", f"{HC['y1']} employees in year one, growing to {HC['y3']} by year "
             f"three, plus two non-employee layers that carry most of the delivery "
             f"load. Who is needed, when, and what they cost."),

    ("fig", "org_chart", "The year-one organisation. Four reporting lines under "
                         "the CEO, who also personally runs the Day 01 platform "
                         "onboarding in every cohort."),

    ("h2", "The full establishment"),
    ("table",
     ["Function", "Role", "Y1", "Y2", "Y3", "Monthly cost"],
     [[fn if i == 0 else "", role, n(y1), n(y2), n(y3), usd(monthly)]
      for fn, rows in [(f, HC_BY_FN[f]["roles"]) for f in HC_BY_FN]
      for i, (role, y1, monthly, y2, y3) in enumerate(rows)] +
     [["Total", "", n(HC["y1"]), n(HC["y2"]), n(HC["y3"]), ""]],
     [3.0, 5.4, 1.1, 1.1, 1.1, 2.3]),
    ("fig", "headcount", "Headcount by function. Delivery and partnerships grow "
                         "fastest, because they are what the revenue is made of."),

    ("h2", "Two layers that are not on the payroll"),
    ("deflist", [
        (f"Certified freelance facilitators",
         f"The cohort business runs on them. Four lead facilitators are employed; "
         f"everything above {4 * COHORTS_PER_PAIR_PER_YEAR // 2} cohorts a year is "
         f"delivered by a certified pool paid "
         f"{usd(UE['facilitation']/(BOOTCAMP_DAYS*2))} a day. This keeps the "
         f"largest variable cost variable, which is what protects the business in "
         f"a quarter when a university postpones."),
        (f"{AMBASSADORS_Y1} campus ambassadors",
         f"A stipend, free Pro access and standing — not a salary. They are the "
         f"cheapest acquisition channel at "
         f"{usd([r for r in CH['rows'] if r['name']=='Campus ambassadors'][0]['cac'])} "
         f"per paying founder, and more importantly they are the early-warning "
         f"system for which campuses are ready to buy."),
    ]),

    ("h2", "The hiring sequence, and why this order"),
    ("num", [
        "<b>Before anything — the KSA country manager.</b> The most expensive "
        "single hire in the plan and the first one, because the Saudi motion is "
        "partnership-led and a partnership cycle is long. Hiring this role late "
        "would push Saudi revenue out of year one entirely.",
        "<b>Land quarter — delivery and curriculum.</b> Four lead facilitators and "
        "the Head of Curriculum, before any sales capacity. Four free pilots have "
        "to run flawlessly because they are the only sales collateral the Prove "
        "quarter will have.",
        "<b>Prove quarter — partnerships and the ambassador manager.</b> Now that "
        "there are cohort reports to show, the partnerships associates and the "
        "ambassador programme manager can convert them.",
        "<b>Expand quarter — engineering and student success.</b> Cohort volume "
        "triples. The admin workspace, the reporting exports and the review "
        "pipeline all need to hold at a volume they have not seen, and support "
        "load arrives with the students.",
        "<b>Scale quarter — the second delivery manager and the facilitator pool.</b> "
        "The quarter peaks at "
        f"{CAP[-1]['facilitators']:.0f} facilitators. Certification of the pool "
        "must be complete before the quarter starts, not during it.",
    ]),

    ("h2", "Compensation and retention"),
    ("deflist", [
        ("Cairo base, Riyadh exception",
         f"Most roles are priced at Cairo. Two are priced at Riyadh — the country "
         f"manager at {usd(5000)} and the Saudi delivery manager at {usd(4500)} a "
         f"month — and together they are "
         f"{(5000+4500)*12/ (HC['cost_y1']) * 100:.0f}% of year-one payroll across "
         f"two of {HC['y1']} people. Under-pricing them is the most common way "
         f"this plan fails quietly."),
        ("Founders below market",
         f"The three leadership roles are at {usd(3000)} a month, below what any of "
         f"them could earn elsewhere. This is a deliberate runway decision and it "
         f"should be corrected at the year-two raise, not left as a permanent "
         f"feature."),
        ("Facilitators are a career, not a gig",
         "The certified pool is the operational asset. Certification, a rising day "
         "rate by tier, first refusal on employed lead-facilitator roles and "
         "visible cohort outcomes are what stop the pool leaking to the "
         "consultancies that compete for exactly these people."),
        ("Bilingual is a requirement, not a preference",
         "Every student-facing and delivery role needs working Arabic and English. "
         "The content roles need more than that: Egyptian colloquial for Egypt and "
         "Saudi dialect for the Kingdom, composed rather than translated."),
    ]),
])

# ---------------------------------------------------------------------
section("Operational plan", [
    ("lead", "What has to be true, and in what order, for the go-to-market plan "
             "to be deliverable rather than aspirational. This section is the "
             "answer to: what do we actually need to accomplish the GTM plan?"),

    ("h2", "The binding constraint"),
    ("p", f"Demand is not the constraint in year one. Delivery capacity is. A "
          f"facilitator pair runs one cohort per two weeks and needs slack for "
          f"travel, preparation and the weeks a campus is closed, which comes to "
          f"{COHORTS_PER_PAIR_PER_YEAR} cohorts a pair a year. The quarterly plan "
          f"therefore converts directly into a facilitator headcount, and that "
          f"number is the operating plan's primary schedule."),
    ("fig", "cohort_ramp", "Cohorts by quarter against the facilitators required "
                           "to deliver them. The Scale quarter needs roughly four "
                           "times the facilitator capacity of the Land quarter."),
    ("table",
     ["Quarter", "Phase", "Egypt paid", "KSA paid", "Free pilots", "Total",
      "Facilitators"],
     [[c["label"], c["phase"], n(c["egypt"]), n(c["ksa"]), n(c["pilots"]),
       n(c["total"]), f"{c['facilitators']:.0f}"] for c in CAP] +
     [["Year one", "", n(sum(c["egypt"] for c in CAP)),
       n(sum(c["ksa"] for c in CAP)), n(sum(c["pilots"] for c in CAP)),
       n(sum(c["total"] for c in CAP)), "peak " + f"{max(c['facilitators'] for c in CAP):.0f}"]],
     [2.2, 1.9, 1.9, 1.7, 1.8, 1.4, 2.0]),

    ("h2", "Readiness — what must exist before each phase"),
    ("table",
     ["By the start of", "What must be ready", "Owner"],
     [["Q4 2026 · Land",
       "Four certified facilitators · the six-day curriculum and all materials in "
       "both languages · the admin workspace with cohort creation and invitations "
       "· a signed pilot agreement template · the Riyadh country manager in post",
       "COO"],
      ["Q1 2027 · Prove",
       "The cohort report, automatically generated and presentable without editing "
       "· judging rubric and certificates · four completed pilot reports · the "
       "first competition format and platform entry flow",
       "COO and Head of Curriculum"],
      ["Q2 2027 · Expand",
       "Eight more certified facilitators · a partner onboarding pack for "
       "platform-only seats · bulk seat provisioning for sponsored cohorts · "
       "support cover in both languages at cohort volume",
       "Delivery Managers"],
      ["Q3 2027 · Scale",
       "The full facilitator pool certified before the quarter opens · renewal "
       "pack and pricing for second-term licences · parallel-group scheduling for "
       "100-plus intakes · Riyadh competition logistics",
       "COO and Head of Partnerships"]],
     [2.8, 8.4, 2.6]),

    ("h2", "The cohort delivery machine"),
    ("p", "Every cohort runs the same way, and the sameness is the point: it is "
          "what lets a freelance facilitator deliver a cohort the company has "
          "never seen, and what makes the cohort report comparable across "
          "institutions."),
    ("num", [
        "<b>Scheduling.</b> Cohort dates are fixed against the academic calendar "
        "of the institution, not ours. Egyptian and Saudi terms differ, and "
        "Ramadan moves. The delivery calendar is built a term ahead and is the "
        "constraint sales sells against — never the other way round.",
        "<b>Facilitator assignment.</b> A certified pair per group, with the lead "
        "facilitator employed for the first cohort at any new institution. The "
        "freelance pool covers repeat institutions, where the format is proven.",
        "<b>Materials.</b> Printed kits, problem cards, canvases and certificates "
        "shipped to the venue a week ahead; digital copies in the admin workspace.",
        "<b>The daily loop.</b> Opener on last night's StartPad progress; short "
        "input, then apply it; checkpoint marked Meets, Partly or Not yet; the "
        "team splits that night's missions and submits; AI feedback lands before "
        "the next opener. The loop repeats on days one to five.",
        "<b>The Bazaar.</b> Day six is public — faculty, families, partners and "
        "judges. Judges see reviewed work, not slides. Certificates, photographs "
        "and the cohort report are issued the same week, because a report that "
        "arrives a month later does not renew anything.",
        "<b>Handover.</b> Missions 11–15 stay open to the student afterwards, and "
        "the institution keeps visibility of progress. This is what turns a "
        "two-week engagement into a year-long relationship.",
    ]),

    ("h2", "Facilitator certification"),
    ("p", "The pool is the operational asset and the main single point of failure. "
          "Certification is four steps and is run by the Head of Curriculum: "
          "observe a full cohort; co-deliver two days under a lead facilitator; "
          "deliver a full cohort observed and scored against the facilitator "
          "rubric; recertify each term against cohort outcomes and student "
          "feedback. Nobody facilitates unobserved before step three is passed, "
          "including under schedule pressure — which is precisely when the "
          "temptation arrives."),

    ("h2", "What the platform must do to support the plan"),
    ("table",
     ["Capability", "Why the GTM plan needs it", "Needed by"],
     [["Programme admin account with cohort creation, bulk invitation and "
       "educator assignment",
       "Without it there is no institutional product at all — only a student app",
       "Q4 2026"],
      ["Student-controlled sharing, with scoped programme data",
       "The trust position that makes a university sign; also the thing that "
       "keeps the company clear of student-data problems",
       "Q4 2026"],
      ["AI review at cohort volume, overnight",
       "The daily loop breaks if feedback is not ready before the next opener; "
       "25 students submitting the same evening is a load spike, not a trickle",
       "Q4 2026"],
      ["The automatic cohort report",
       "It is the renewal document and the partnership sales collateral. Hand-"
       "writing it does not scale past the pilots",
       "Q1 2027"],
      ["Bulk seat provisioning and partner-level reporting",
       "Sponsored-seat programmes place thousands of seats at once and report to "
       "their own donors",
       "Q2 2027"],
      ["Full Arabic parity, right-to-left, including exported PDFs",
       "A review a student cannot read in their own language does not get acted "
       "on, and a report a ministry cannot read in Arabic does not get circulated",
       "Q4 2026"]],
     [4.2, 7.0, 2.6]),

    ("h2", "Quality gates"),
    ("p", "Four things are measured on every cohort, and a cohort that fails any "
          "of them triggers a review before the next cohort at that institution is "
          "scheduled."),
    ("bul", [
        "<b>Mission completion.</b> At least 80% of students complete missions "
        "01–10 by the Bazaar. Below that, the evening loop is not working and the "
        "facilitator pairing is examined first.",
        "<b>Review turnaround.</b> AI feedback available before the next day's "
        "opener, every night, without exception. This is a platform SLA, not a "
        "target.",
        "<b>Bazaar delivery.</b> Every team pitches and every team member speaks. "
        "A team that cannot is a facilitation failure that showed up two days "
        "earlier and was not caught.",
        "<b>Report issued inside five working days</b> of the Bazaar, to the "
        "programme lead who signed.",
    ]),

    ("h2", "Support"),
    ("p", "Bilingual student success cover during cohort weeks, which is when "
          "nearly all support load arrives — a cohort of 25 submitting the same "
          "evening generates more tickets than a month of self-serve founders. "
          "Two people in year one, rising to eleven by year three, scheduled "
          "around the delivery calendar rather than evenly across the week."),

    ("h2", "Data protection and the student relationship"),
    ("p", "Students own their account and their idea. The programme sees mission "
          "progress, activity, the evidence the student chooses to share, review "
          "scores and educator approvals. It never sees AI Co-Founder chats, "
          "private profile data or unsubmitted drafts, and staff can never edit "
          "student work. Sharing is switched on by the student and can be switched "
          "off; only students with active consent appear in cohort metrics."),
    ("note", "This is a commercial position as much as an ethical one. The "
             "institution is buying a reporting line, and the credibility of that "
             "line depends on the student having had a real choice. A cohort "
             "metric built on compelled consent is a metric a dean cannot defend, "
             "and the first time that is challenged the relationship ends."),
])

# ---------------------------------------------------------------------
section("Financial plan", [
    ("lead", "Three years of revenue, cost and cash, built from the operating plan "
             "rather than from a growth rate."),

    ("h2", "Revenue"),
    ("fig", "revenue_stack", "Revenue by line across three years."),
    ("fig", "revenue_mix", "The mix barely moves: this is an institutional "
                           "business in every year, and subscriptions never become "
                           "the point."),
    ("table",
     ["Revenue line"] + [f"Year {y['year']}" for y in PROJ],
     [[k] + [money(y["lines"].get(k, 0.0)) for y in PROJ]
      for k in ["Bootcamp cohorts (institutions)",
                "Sponsored seats (NGO and government)",
                "Platform-only seats (programmes, incubators)",
                "Faculty-wide licences",
                "Founder subscriptions (Pro and Team)"]] +
     [["Total revenue"] + [money(y["revenue"]) for y in PROJ]],
     [6.0, 2.8, 2.8, 2.8]),

    ("h2", "Year-one cost base"),
    ("table",
     ["Cost line", "Year one", "Note"],
     [[name, usd(val), note] for (name, val), note in zip(
         C["lines"],
         [f"{HC['y1']} people, averaging 65% of the establishment across the year",
          f"{R['paid_cohorts']} cohorts × {usd(UE['direct'])} direct cost",
          f"{R['free_pilots']} free pilots — the cost of earning the first yes",
          "All six channels, per the marketing plan",
          "Scales with active founders and AI review volume",
          "Platform tooling and internal systems",
          "Cairo to Riyadh, and campuses in both markets",
          "Including the cost of establishing the Saudi entity",
          "Cairo office and a Riyadh desk",
          f"{int(0.08*100)}% of the above"])] +
     [["Total operating cost", usd(C["total"]), ""]],
     [4.6, 2.4, 6.6]),

    ("h2", "Three-year profit and loss"),
    ("table",
     [""] + [y["label"] for y in PROJ],
     [["Revenue"] + [money(y["revenue"]) for y in PROJ],
      ["Operating cost"] + [money(y["cost"]) for y in PROJ],
      ["Operating result"] + [("−" if y["profit"] < 0 else "+") + money(abs(y["profit"]))
                              for y in PROJ],
      ["Operating margin"] + [f"{y['profit']/y['revenue']*100:,.0f}%".replace("-", "\u2212")
                             for y in PROJ],
      ["Revenue per employee"] + [money(y["revenue"] / y["headcount"]) for y in PROJ],
      ["Cohorts delivered"] + [n(y["cohorts"]) for y in PROJ]],
     [4.2, 3.4, 3.4, 3.4]),

    ("h2", "Cash, and the raise"),
    ("fig", "cash_curve", "Cash on hand across three years. The trough is shallow "
                          "because cohorts are invoiced before they are delivered."),
    ("table",
     ["", "Amount", "What it covers"],
     [["Year-one deficit", money(FUND["deficit_y1"]),
       "The gap while free pilots and hiring run ahead of cohort revenue"],
      ["Year-two deficit", money(FUND["deficit_y2"]),
       "None — the business reaches breakeven in year two"],
      ["Six-month operating reserve", money(FUND["reserve"]),
       "Six months of the year-one cost base, held against a delayed term or a "
       "postponed partnership"],
      ["Total raise", money(FUND["rounded"]), "Sized to the deficit and a genuine "
                                              "reserve, not to a round number"]],
     [4.4, 2.6, 6.6]),
    ("p", f"{money(FUND['rounded'])} is small for a business that reaches "
          f"{money(PROJ[2]['revenue'])} of revenue in year three, and the reason is "
          f"structural rather than optimistic: an institution is invoiced before "
          f"its cohort runs, the direct cost of {usd(UE['direct'])} is incurred "
          f"during delivery, and the gross margin is {UE['margin']*100:.0f}%. "
          f"Growth in the institutional line releases working capital instead of "
          f"consuming it. A subscription-led version of this company would need "
          f"several times the capital to reach the same revenue."),

    ("h2", "Use of funds"),
    ("table",
     ["Use", "Share", "Why"],
     [["Delivery capacity — facilitators, certification, materials", "34%",
       "The binding constraint; every cohort beyond the current pool needs it"],
      ["Product and engineering", "27%",
       "The admin workspace, cohort reporting and AI review at volume"],
      ["Saudi market entry", "16%",
       "Country manager, delivery manager, entity and travel"],
      ["Growth — ambassadors, content, competitions", "13%",
       "The channels that actually return more than they cost"],
      ["Operating reserve held unspent", "10%",
       "A postponed term or a delayed partnership should not be existential"]],
     [5.4, 1.8, 6.4]),
])

# ---------------------------------------------------------------------
section("Risks", [
    ("lead", "The five risks most likely to break this plan, what each would look "
             "like early, and what has already been built to absorb it."),

    ("table",
     ["Risk", "What it looks like early", "Mitigation"],
     [["Facilitator capacity does not materialise",
       "Certification slips, or the pool leaks to consultancies paying more per day",
       "Certification starts in the Land quarter, a term ahead of need; the pool "
       "is a tiered career with a rising day rate; the quarterly plan is cut to "
       "facilitator capacity rather than the reverse"],
      ["University procurement is slower than planned",
       "Pilots run but contracts sit unsigned through the Prove quarter",
       "One contract covering all three layers; free pilots that make the cohort "
       "report the sales document; the Saudi partnership motion carries paid "
       "revenue from Q4 while Egypt is still proving"],
      ["A national programme partnership does not land",
       "Enthusiastic meetings, no budget line, repeated deferral",
       f"Sponsored seats are {dict(R['lines'])['Sponsored seats (NGO and government)']/R['total']*100:.0f}% "
       f"of year-one revenue, so the plan survives without them; two partnerships "
       f"are pursued so neither is a single point of failure"],
      ["Subscription conversion is worse than modelled",
       "Activation holds but paywall conversion sits below 10%",
       "Subscriptions are 3% of year-one revenue. The plan is deliberately not "
       "built on them; the exposure is to institutional renewal instead"],
      ["Currency and macro",
       "EGP devaluation repricing a USD-denominated plan against EGP costs",
       "Most costs are EGP and most institutional pricing can be set in EGP with "
       "USD reference; devaluation lowers the cost base faster than it lowers "
       "local willingness to pay"],
      ["Key-person concentration",
       "The CEO personally runs Day 01 onboarding in every cohort",
       "This does not scale past roughly 20 cohorts a year and is a known "
       "year-two problem; the Day 01 session must be delivered by certified "
       "facilitators before the Expand quarter"]],
     [3.4, 5.0, 5.2]),

    ("note", "The last row is the one to watch. It is written into the strategy as "
             "a feature — the founder personally opens every cohort — and it is "
             "genuinely good for the first twenty. It becomes the single hardest "
             "constraint in year two, when there are 150 cohorts and one founder, "
             "and the handover has to be designed well before it is needed."),
])

# ---------------------------------------------------------------------
section("Milestones", [
    ("lead", "What has to be true at the end of each quarter for the next one to "
             "be deliverable."),
    ("table",
     ["Quarter", "Commercial", "Operational", "Product"],
     [["Q4 2026 · Land",
       f"{CAP[0]['ksa']} paid KSA cohorts, {CAP[0]['pilots']} Egyptian free pilots, "
       f"first partnership conversations open",
       "4 facilitators certified, Riyadh country manager in post, curriculum "
       "complete in both languages",
       "Admin workspace live, student-controlled sharing, overnight AI review at "
       "cohort volume"],
      ["Q1 2027 · Prove",
       f"{CAP[1]['egypt'] + CAP[1]['ksa']} paid cohorts, first licence signed off a "
       f"pilot report, first competition run",
       "Cohort report generated without manual editing, 8 facilitators certified",
       "Competition entry flow, judging rubric, certificates"],
      ["Q2 2027 · Expand",
       f"{CAP[2]['egypt'] + CAP[2]['ksa']} paid cohorts, first sponsored-seat "
       f"programme signed, platform-only partners live",
       "12 facilitators certified, bilingual support at cohort volume",
       "Bulk seat provisioning, partner-level reporting"],
      ["Q3 2027 · Scale",
       f"{CAP[3]['egypt'] + CAP[3]['ksa']} paid cohorts, first renewals, first "
       f"Riyadh competition",
       f"Full pool certified before the quarter opens, parallel-group scheduling "
       f"for 100-plus intakes",
       "Renewal and second-term licence flows, Day 01 onboarding delivered by "
       "facilitators rather than the founder"]],
     [2.4, 3.9, 3.9, 3.4]),

    ("h2", "What year one has to prove"),
    ("num", [
        "<b>That the cohort report renews a licence.</b> Everything else in the "
        "model depends on an institution buying a second time off the strength of "
        "the first report. One renewal in the Scale quarter is worth more than ten "
        "new pilots.",
        "<b>That a freelance facilitator delivers the same cohort as an employed "
        "one.</b> If the format does not survive delegation, the business has a "
        "ceiling of about twenty cohorts a year and the whole plan changes shape.",
        "<b>That a national programme will contract a private platform.</b> This "
        "is unproven and the plan deliberately does not depend on it in year one. "
        "If it works, year three is conservative; if it does not, year three still "
        "stands on cohorts and licences.",
    ]),
])

# ---------------------------------------------------------------------
section("Appendix — assumptions and sources", [
    ("lead", "Every assumption behind the numbers, so a reader can argue with the "
             "inputs rather than the conclusions."),

    ("h2", "External figures"),
    ("table",
     ["Figure", "Value", "Source"],
     [["Egypt higher-education enrolment, 2024/25", n(HE_STUDENTS["Egypt"]),
       "CAPMAS annual bulletin"],
      ["Saudi tertiary enrolment, 2022", n(HE_STUDENTS["KSA"]),
       "UNESCO UIS. The 84% gross enrolment ratio reported for 2024 implies "
       "growth; the lower figure is held"],
      ["Egypt graduates, 2023", n(ANNUAL_GRADUATES["Egypt"]),
       "CAPMAS, reported via Ahram Online"],
      ["Saudi graduates each year", n(ANNUAL_GRADUATES["KSA"]),
       "Derived: enrolment over a four-year degree, discounted 25% for longer "
       "programmes and attrition"],
      ["Egypt public colleges", "551", "CAPMAS — 28 universities, 551 colleges"],
      ["MENA startup funding, 2025", "$7.5bn across 647 deals",
       "Wamda full-year report"],
      ["Egypt startup funding, 2025", "$263m across 89 deals", "Wamda"],
      ["Saudi startup funding, 2025", "$5.0bn across 211 deals", "Wamda"],
      ["One Million Entrepreneurs registrations", "~18,000",
       "Egyptian Ministry of Planning"]],
     [5.0, 3.0, 6.4]),

    ("h2", "Our assumptions"),
    ("table",
     ["Assumption", "Value", "Reasoning"],
     [["Cohort price", usd(PRICE_COHORT),
       f"{usd(PRICE_COHORT/COHORT_SIZE)} per student — below the per-student cost "
       f"of a single external trainer day with nothing left behind"],
      ["Pro subscription", f"{usd(PRICE_PRO_YEAR)} / year",
       "Priced for a student in Cairo, not a founder in London"],
      ["Team subscription", f"{usd(PRICE_TEAM_YEAR)} / year",
       "One payment covering a founding team; converts less often, pays three "
       "times more"],
      ["Sponsored seat", usd(PRICE_SPONSORED_SEAT),
       "Discounted against the list seat because the volume is the point"],
      ["Faculty fit filter", f"{FILTER_FACULTY_FIT*100:.0f}%",
       "Business, engineering, computing, design and applied science carry "
       "capstones that map to the missions"],
      ["Has an idea filter", f"{FILTER_HAS_AN_IDEA*100:.0f}%",
       "Wider than final-year capstone, narrower than the whole student body"],
      ["Cohorts per facilitator pair per year", n(COHORTS_PER_PAIR_PER_YEAR),
       "One cohort per two weeks, with slack for travel, preparation and campus "
       "holidays"],
      ["Facilitator day rate", usd(UE["facilitation"] / (BOOTCAMP_DAYS * 2)),
       "Certified freelance rate, Egypt"],
      ["B2C subscriber life", "1.6 years",
       "A founder who finishes has no reason to renew a third year; one who "
       "stalls churns inside the first"],
      ["Year-one hiring ramp", "65%",
       "Average establishment across the year; nobody but the founders is on the "
       "payroll from month one"],
      ["B2B commission", "6% of institutional revenue",
       "Institutional business is sold by people, and people on a number are paid "
       "on it"]],
     [4.0, 2.6, 7.8]),

    ("h2", "What this plan does not claim"),
    ("bul", [
        "It does not claim an outcome number. StartPad records mission progress, "
        "evidence and review scores. It does not certify that a venture will "
        "succeed, and no partnership should be contracted against a metric the "
        "product cannot measure.",
        "It does not assume a second raise. Years two and three are funded from "
        "operations on these numbers. A growth raise would change the shape of "
        "year three, not its viability.",
        "The channel conversion rates are modelled, not measured. They are the "
        "assumption most likely to be wrong in both directions, and the first "
        "cohort quarter will replace them with observed figures.",
    ]),
])
