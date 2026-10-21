"""
The business plan, as content blocks.

Structure follows the thirteen-part format in the founder's guide, with Part 11
(Financial Plan) and Part 12 (Funding Request) omitted — those are being built
separately — and a Go-to-Market Roadmap added between Sales and Operations,
because nothing in this plan starts on day one and a plan that does not say when
each engine opens is a plan that has assumed its own ramp away.

Prose lives here; rendering lives in scripts/build_business_plan_docx.py; every
number comes from model.py and every role description from roles.py. Nothing
numeric is typed into a sentence.

Block grammar
-------------
    ("h2", text) / ("h3", text)        headings inside a part
    ("p", markup)                      paragraph; <b> is honoured
    ("lead", markup)                   the standfirst under a part opener
    ("bul", [...])  ("num", [...])     lists
    ("deflist", [(term, markup), ...]) a term and its explanation
    ("table", [heads], [[cells]], [widths_cm])
    ("fig", name, caption)             a PNG from business_plan/figures
    ("kpi", [(value, label), ...])     a row of statistic tiles
    ("note", markup)  ("quote", markup)
    ("roles", [role names])            full role cards from roles.py
    ("pb",)                            page break
"""
from . import model as MD
from .model import (AMBASSADORS, ANNUAL_GRADUATES, BOOTCAMP_DAYS, COHORT_PRICE,
                    COHORT_SIZE, COHORTS_PER_PAIR, COMPETITION_DIRECT,
                    COMPETITIONS_PER_YEAR, CORPORATES, ENGINE_NAMES,
                    FILTER_FACULTY_FIT, FILTER_INITIATIVE_SHARE, HE_STUDENTS,
                    INITIATIVE_SEATS_PER_YEAR, NGOS, PRICE_COHORT,
                    PRICE_COMPETITION, PRICE_CORPORATE, PRICE_FACULTY_LICENCE,
                    PRICE_INITIATIVE_SEAT, PRICE_NGO_PROGRAMME, PRICE_PRO_YEAR,
                    PRICE_SCHOOL_COHORT, PRICE_SCHOOL_LICENCE, PRICE_SEAT,
                    PRICE_TEAM_YEAR, PRICE_TOT_COHORT, PRICE_TVET_COHORT,
                    PROGRAMMES, QUARTERS, SCHOOLS_WITH_BUDGET, SECONDARY_STUDENTS,
                    TVET_INSTITUTIONS, TVET_STUDENTS, cohort_unit_economics,
                    engine_economics, facilitator_capacity, headcount, market,
                    pipeline, plan, projection, revenue, school_unit_economics,
                    subscriptions, tvet_unit_economics)

M = market()
PROJ = projection()
R1, R2, R3 = revenue(1), revenue(2), revenue(3)
UE = cohort_unit_economics()
SU = school_unit_economics()
TU = tvet_unit_economics()
HC_BY_FN, HC = headcount()
CAP = facilitator_capacity()
EE = {r["name"]: r for r in engine_economics()}
SUBS = subscriptions(1)
PIPE = pipeline()
LEV = MD.leverage()
PC = MD.PODCAST
PLAYS = MD.ENGAGEMENT_PLAYS


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
SUBTITLE = "Egypt and Saudi Arabia \u00b7 Years one to five"
PERIOD = "October 2026 to September 2031"

SECTIONS = []


def section(name, blocks):
    SECTIONS.append((name, blocks))


# =====================================================================
section("Executive Summary", [
    ("lead", "StartPad turns a first-time founder with an idea into someone the "
             "ecosystem takes seriously, and sells that capability to the "
             "organisations responsible for producing them: universities, schools "
             "and technical institutes, national initiatives, donors, competition "
             "sponsors and corporates. The young person uses it. Somebody else "
             "pays for it."),

    ("h2", "Company description"),
    ("p", "StartPad is a gamified, AI-native venture-building platform built in "
          "MENA for MENA founders. Fifteen sequenced missions across five phases "
          "take a raw idea to a live product, with an AI Co-Founder inside every "
          "mission and 121 tools mapped to the journey. Every submission is "
          "reviewed before the next mission unlocks, which is what turns "
          "participation into evidence an institution can report on."),

    ("h2", "The problem"),
    ("p", "Ideas are everywhere in MENA; a path to a real startup is not. Founders "
          "have graduation projects and no method. Institutions are measured on "
          "employability and entrepreneurship outcomes they have no way to "
          "produce. National programmes have announced million-scale targets with "
          "no delivery capacity behind them. The common failure is not talent or "
          "capital — it is that nobody owns the first step."),
    ("kpi", [("21%", "of self-described MENA startups meet the minimum criteria "
                     "to be considered investable"),
             ("56%", "of MENA pre-seed startups never reach the next stage"),
             ("68%", "failure rate in Egypt for startups trying to reach "
                     "Series A — the highest in the region")]),

    ("h2", "The solution"),
    ("p", "A method with a gate. A mission opens only when the last one passes a "
          "review scored on specificity, depth, evidence, actionability and "
          "relevance. Around that platform sits an in-person layer — bootcamps, "
          "workshops, competitions — and above it an institutional workspace that "
          "gives the organisation paying a live view of progress, review states "
          "and a downloadable cohort report, without ever taking ownership of the "
          "student's work."),

    ("h2", "Market opportunity"),
    ("p", f"Across Egypt and Saudi Arabia the plan addresses "
          f"{n(M['people']/1e6, 1)} million young people and first-time founders — "
          f"university students, recent graduates, technical and vocational "
          f"students, senior secondary students and micro-enterprise owners — "
          f"through {n(M['units'] + M['schools'] + M['tvet_inst'])} institutional "
          f"buying units, {n(NGOS)} NGOs and donors, {n(CORPORATES)} corporates "
          f"and roughly {n(COMPETITIONS_PER_YEAR)} youth competitions a year. "
          f"Total addressable market is {money(M['tam'])} a year, of which "
          f"{money(M['sam'])} is serviceable and "
          f"{pct(M['inst_sam']/M['sam'])} of that is institutional."),
    ("fig", "segments", "The population served, across both markets. Secondary and "
                        "technical students roughly match the university "
                        "population, and are almost entirely unserved."),

    ("h2", "Competitive advantage"),
    ("p", "Generic guides give advice; StartPad gives a path. The defensible layer "
          "is not the software — it is the certified facilitator pool, the "
          "bilingual MENA-composed curriculum, the institutional relationships and "
          "the cohort evidence record that a buyer would have to abandon to switch. "
          "Those take years to build and are the reason a well-funded imitator "
          "cannot simply copy the product."),

    ("h2", "The eight engines"),
    ("fig", "engine_mix", "Revenue mix across five years. The business is "
                          "institutional in every year; founder subscriptions "
                          "never become the point."),
    ("table",
     ["Engine", "Who signs the contract", "Share, Y1", "Share, Y3"],
     [[e, who, share(e, 1), share(e, 3)]
      for e, who in zip(ENGINE_NAMES, [
          "A dean, an entrepreneurship centre or a capstone coordinator",
          "A school group, a principal or a technical institute director",
          "A ministry, a donor or a national programme office",
          "A foundation, an INGO country office or a development agency",
          "A bank, a telco, a ministry or a foundation",
          "A corporate CSR or innovation budget holder",
          "An incubator or accelerator director",
          "The founder, out of their own pocket"])],
     [4.0, 6.4, 2.1, 2.1]),

    ("h2", "What this plan concludes"),
    ("deflist", [
        ("Sell to the budget holder, not the beneficiary",
         "The person who benefits has almost no money; the person with the budget "
         "has a reporting problem StartPad solves. Every engine is built on that "
         "asymmetry, and it is why founder subscriptions are the smallest line."),
        ("Nothing starts on day one",
         f"Eight engines open on eight different gates across twelve quarters. A "
         f"faculty licence cannot be sold before two cohorts have run; a ministry "
         f"will not contract a platform that cannot show a cohort report. Only "
         f"university cohorts earn in the Land quarter."),
        ("The constraint is certified delivery, not demand",
         f"Delivery peaks at {max(c['facilitators'] for c in CAP):.0f} "
         f"facilitator-equivalents in a quarter, and a certified pair runs "
         f"{COHORTS_PER_PAIR['university']} university cohorts a year. "
         f"Certification is therefore the first operational priority, and the "
         f"seat, competition and partner engines matter partly because they "
         f"scale <b>past</b> that constraint."),
        ("Twelve people in year three, twenty in year five",
         f"The establishment is capped: {HC['y1']} in year one, {HC['y2']} in "
         f"year two, {HC['y3']} in year three, {HC['y4']} in year four and "
         f"{HC['y5']} in year five. StartPad does not deliver cohorts at scale — "
         f"it certifies and audits the organisations and freelancers who do. "
         f"By year three, {LEV[2]['cohorts']} cohorts are delivered by a pool of "
         f"{LEV[2]['pool']} certified facilitators and "
         f"{LEV[2]['partners']} certified partner organisations, which is how "
         f"{HC['y3']} employees stand behind "
         f"{n(LEV[2]['learners_per_employee'])} learners each."),
        ("Every engine enters through a named programme that already exists",
         "StartPad does not create demand; it attaches to budgets already "
         "committed. The plan names the organisations — Rowad 2030 and MSMEDA in "
         "Egypt, Monsha'at, Misk and TVTC in Saudi Arabia, Enactus Egypt, INJAZ "
         "and the bank-sponsored competition seasons — and states the route into "
         "each as one of six repeatable engagement plays."),
    ]),
    ("fig", "leverage", "The whole argument for a twelve-person company in one "
                        "figure: employees against the certified network that "
                        "delivers for them."),
])

# =====================================================================
section("Company Description", [
    ("lead", "Who StartPad is, what it is for, and what has to be true for it to "
             "work."),

    ("h2", "Mission"),
    ("quote", "To give every first-time founder in MENA a method — and every "
              "institution that teaches them a way to prove it worked."),

    ("h2", "Vision"),
    ("p", "That within a decade, a young person in Cairo, Assiut, Riyadh or Jeddah "
          "who has an idea has an obvious first step, and the university, school, "
          "ministry or foundation around them has a standard way to support it. "
          "StartPad intends to be that standard: the layer the region's "
          "entrepreneurship education runs on, in Arabic, with the evidence "
          "attached."),

    ("h2", "Core values"),
    ("deflist", [
        ("Earn the yes",
         "Free pilots before licences, results before scale. We do not ask an "
         "institution to believe us; we ask them to look at their own cohort "
         "report."),
        ("The founder does the work",
         "The AI asks the question a mentor would ask. It never writes the answer. "
         "A platform that does the thinking destroys the only thing it was "
         "supposed to create."),
        ("Composed, not translated",
         "Arabic is the first language of this product, in the dialect of the room "
         "it is used in. A translated product is a foreign product."),
        ("Status is earned",
         "Ambassadors, facilitators and partners renew on results each term. A "
         "title that cannot be lost stops working."),
        ("Honest indicators",
         "We report recorded progress and evidence. We do not certify that a "
         "venture will succeed, and we will not contract to a metric the product "
         "cannot measure."),
    ]),

    ("h2", "Key success factors"),
    ("num", [
        "<b>A certified facilitator pool.</b> Everything in-person depends on "
        "people who can deliver a StartPad cohort without StartPad in the room.",
        "<b>A cohort report worth renewing on.</b> The automatic report is the "
        "sales document for every engine; if it is not good enough to circulate, "
        "nothing else works.",
        "<b>Two markets, two doors.</b> Universities in Egypt, programme partners "
        "in Saudi Arabia. The same product, a local route in each.",
        "<b>Institutional trust.</b> Student-controlled sharing, scoped data and a "
        "refusal to over-claim outcomes are commercial assets, not compliance "
        "overhead.",
        "<b>Engine diversity.</b> Eight buyers means no single procurement freeze, "
        "budget cut or ministry reshuffle is existential.",
    ]),

    ("h2", "Current situation"),
    ("p", "The platform is built: fifteen missions, five phases, 121 tools, the AI "
          "Co-Founder, the review loop, the institutional workspace and full "
          "bilingual support with right-to-left layout. The bootcamp curriculum is "
          "designed across six days with signature activities, daily deliverables "
          "and a judged public Bazaar. The company is pre-revenue and entering its "
          "first commercial year in both markets simultaneously from September "
          "2026."),

    ("h2", "Motivation for expansion"),
    ("p", "Two things make this the moment. First, both governments have made "
          "youth entrepreneurship an explicit national priority with named "
          "programmes and published targets — and none of those programmes has a "
          "method or a reporting line. Second, Egypt's technical education reform "
          "and Saudi Arabia's vocational expansion have created a segment of "
          "several million students whose entire purpose is employability and who "
          "are served by almost nobody."),
])

# =====================================================================
section("Market Analysis", [
    ("lead", "The industry, the segments, the size of each, and the gaps that make "
             "a method sellable."),

    ("h2", "Industry overview"),
    ("p", "MENA startups raised a record $7.5bn across 647 deals in 2025. Saudi "
          "Arabia led at $5bn across 211 deals; Egypt was third at $263m across 89 "
          "deals, with deal count rising even as value fell after the currency "
          "devaluation. Capital is concentrating in the Gulf while the founder "
          "population concentrates in Egypt — which is the structural case for "
          "operating in both markets rather than sequencing them."),
    ("p", "Underneath the funding headlines sits an education and employability "
          "industry that is far larger and far less reported: higher education, "
          "technical and vocational training, secondary schooling, "
          "donor-funded youth programmes and corporate social investment. That is "
          "the industry StartPad actually sells into."),

    ("h2", "Target customer segments"),
    ("p", "There are two distinct customers and only one of them pays. The "
          "<b>beneficiary</b> is a young person or first-time founder. The "
          "<b>buyer</b> is an organisation responsible for preparing them."),
    ("table",
     ["Beneficiary segment", "Size", "Who pays for them"],
     [["University students", n(M["he"]),
       "Universities, faculties, national initiatives, competition sponsors"],
      ["Recent graduates, within three years", n(M["grads"]),
       "Incubators, NGO programmes, national initiatives, themselves"],
      ["Technical and vocational students", n(M["tvet_students"]),
       "Technical institutes, ministries, donor employability programmes"],
      ["Secondary students, final two years", n(M["secondary"]),
       "Schools, school groups, CSR programmes, competition sponsors"],
      ["Micro and small enterprise owners", n(M["msme"]),
       "Banks, MSME agencies, NGOs, themselves"],
      ["Total", n(M["people"]), ""]],
     [4.4, 2.4, 9.2]),
    ("fig", "segments", "Population by segment across Egypt and Saudi Arabia."),

    ("h2", "The buyer universe"),
    ("table",
     ["Buyer universe", "Count", "Basis"],
     [["University buying units", n(M["units"]),
       "951 in Egypt (551 CAPMAS public colleges plus private faculties), 564 in "
       "KSA. The buying unit is the college — three of the four doors sit below "
       "university level"],
      ["Schools with a budget", n(M["schools"]),
       "Private, international, national and applied-technology schools. A "
       "government school on a fixed ministry budget is reached through a national "
       "programme instead"],
      ["Technical and vocational institutions", n(M["tvet_inst"]),
       "Egyptian technical schools plus 314 TVTC institutions in the Kingdom"],
      ["National initiative seats a year", n(INITIATIVE_SEATS_PER_YEAR),
       "Addressable seats at steady state across both markets — far below the "
       "stated targets, which total several million"],
      ["NGOs, donors and foundations", n(NGOS),
       "With a youth employability or entrepreneurship mandate and a budget"],
      ["Youth competitions a year", n(COMPETITIONS_PER_YEAR),
       "Run by universities, schools, banks, telcos, ministries and foundations"],
      ["Large corporates", n(CORPORATES), "With a CSR, innovation or youth budget"],
      ["Incubators and startup programmes", n(PROGRAMMES),
       "That select applicants and would benefit from a prepared pool"]],
     [4.2, 2.2, 9.6]),

    ("h2", "Market size and growth"),
    ("p", "Sizing is bottom-up and counts, for each engine, the organisation that "
          "signs the contract — not the student who benefits. That choice is the "
          "most important methodological decision in this plan: counting students "
          "produces a large and unconvertible number, while counting buyers "
          "produces a number a sales team can actually work."),
    ("fig", "tam_sam", "TAM and SAM, engine by engine."),
    ("table",
     ["Engine", "TAM basis", "TAM", "SAM"],
     [[r["engine"], r["tam_basis"], money(r["tam"]), money(r["sam"])]
      for r in M["rows"]] +
     [["Total", "", money(M["tam"]), money(M["sam"])]],
     [4.0, 6.4, 2.1, 2.1]),
    ("note", f"The subscription line has the largest TAM on paper — "
             f"{money(M['rows'][-1]['tam'])} — because there are millions of young "
             f"people and in principle any of them could pay. It is the least "
             f"realisable number in the table. A plan built on it would be built "
             f"on the one figure here that cannot be converted at these "
             f"willingness-to-pay levels."),

    ("h2", "Who already runs these programmes"),
    ("p", "A market sized from populations is an argument; a market with named "
          "buyers running named programmes is a plan. Every organisation below "
          "already runs something StartPad would sit inside, and already has the "
          "budget line. None of them is a signed partner, and no revenue in this "
          "plan is attributed to any one of them — they are listed so a reader "
          "can verify that the demand described is observable rather than "
          "inferred. The route into each is set out in the Engagement Model."),
    ("fig", "named_targets", "Named target organisations by engine, each tagged "
                             "with the engagement plays that open it. Not signed "
                             "partners: evidence that the buyers exist."),
    ("fig", "ngo_initiatives", "The public programmes in detail, and what StartPad "
                               "supplies to each."),
    ("table",
     ["Programme or organisation", "Market", "What it already runs"],
     [[row[0], row[1], row[2]] for row in MD.NAMED_INITIATIVES],
     [4.4, 1.7, 10.5]),
    ("note", "The common shape is worth naming: every one of these has a target "
             "or a mandate it cannot meet with the delivery capacity it owns. "
             "Rowad 2030 is committed to a million entrepreneurs and delivers a "
             "three-stage online curriculum; Monsha'at Academy has run more than "
             "two hundred training events with no build stage after them; TVTC "
             "has 314 institutions and a self-employment mandate. That gap — "
             "between a published commitment and the means to deliver it — is "
             "the market this plan is addressed to."),

    ("h2", "Market drivers"),
    ("bul", [
        "<b>Published national targets.</b> Egypt's One Million Entrepreneurs "
        "(Rowad 2030), 1 Million Qualified Innovators (with UNDP, MBRF and "
        "ICESCO) and One Million International Licences (with Cisco) all have "
        "million-scale goals and reported progress far behind them.",
        "<b>Technical education reform.</b> Egypt's applied-technology schools and "
        "technical secondary system — over two million students — exist explicitly "
        "to produce employability outcomes.",
        "<b>Vision 2030 and vocational expansion in the Kingdom.</b> TVTC reported "
        "336,150 trainees across 314 institutions in 2024, with continued "
        "expansion planned.",
        "<b>Formalisation incentives.</b> Egypt's Law 6 of 2025 offers tax "
        "incentives for informal businesses to formalise, creating a cohort of "
        "first-time formal founders who need method and documentation.",
        "<b>Accreditation pressure.</b> Universities increasingly need "
        "demonstrable entrepreneurship and employability outcomes for "
        "accreditation, and have no systematic way to produce them.",
        "<b>Donor and CSR appetite.</b> Youth employability remains one of the "
        "most consistently funded themes in both markets.",
    ]),

    ("h2", "Market needs and gaps"),
    ("table",
     ["Who", "What they need", "What exists today", "The gap"],
     [["Universities", "Entrepreneurship outcomes they can report",
       "Ad-hoc workshops and in-house clubs",
       "No method, no evidence trail, nothing comparable across cohorts"],
      ["Schools and technical institutes",
       "Employability content that fits a term",
       "Imported curricula, usually in English",
       "Nothing age-appropriate, bilingual and outcome-recorded"],
      ["National programmes", "Delivery capacity at scale with per-participant "
                              "evidence",
       "Events, awareness campaigns, fragmented training",
       "No platform that can serve a governorate and report on it"],
      ["Donors and NGOs", "Logframe-compatible youth programmes",
       "Bespoke training contracts, rebuilt each time",
       "No repeatable product with per-participant records"],
      ["Sponsors", "A credible competition that produces real finalists",
       "Pitch competitions judged on slides",
       "No qualification process and no evidence behind the shortlist"],
      ["Founders", "A first step and a path",
       "Scattered templates, English-language courses",
       "No sequence, no feedback, no proof of work"]],
     [2.6, 3.6, 4.2, 5.6]),

    ("h2", "Regulatory environment"),
    ("deflist", [
        ("Student data and institutional access",
         "Institutional visibility is scoped to progress, activity, shared "
         "evidence and review states, switched on by the student. Private account "
         "data and AI chats are excluded and staff can never edit student work. "
         "This is designed as a commercial asset — a cohort metric built on "
         "compelled consent is one a dean cannot defend."),
        ("Safeguarding and child protection",
         "The schools engine serves minors. Facilitator vetting, safeguarding "
         "training, parental consent and incident procedures are a condition of "
         "entry to that market, carried as a standing cost rather than improvised "
         "per contract."),
        ("Public procurement, in two jurisdictions",
         "Ministry and donor contracts require pre-qualification documentation, "
         "audited accounts and formal reporting — a capability, not paperwork. A "
         "Saudi entity, local employment compliance and cross-border invoicing "
         "are first-year requirements, not year-two conveniences."),
    ]),
])

# =====================================================================
section("Competitive Analysis", [
    ("lead", "Who a buyer uses instead, how StartPad compares, and what would "
             "actually be hard to copy."),

    ("h2", "Direct competitors"),
    ("deflist", [
        ("University entrepreneurship centres running their own programmes",
         "The real incumbent and the one to respect. They have the room, the "
         "students and the budget. We beat an in-house programme on method, "
         "bilingual content, the evidence trail and the reporting line — and we "
         "enter as the thing that makes their centre look good, never as its "
         "replacement."),
        ("Training consultancies and event agencies",
         "The direct competitor for cohorts, competitions and corporate "
         "programmes. Comparable or higher day rates, nothing left behind when "
         "the trainer goes, no per-participant record. This comparison is what "
         "makes the cohort price look cheap in front of a dean."),
        ("Regional entrepreneurship education providers",
         "Fragmented, mostly project-based, usually without a platform. They win "
         "on local relationships and lose on repeatability."),
    ]),

    ("h2", "Indirect competitors"),
    ("deflist", [
        ("Online course platforms",
         "Cheaper and broader. They sell completion, not evidence; no institution "
         "can report a cohort outcome from a course certificate."),
        ("Generic AI assistants",
         "Will write a business plan on request — which is precisely the failure "
         "mode. They produce a document and no founder capability, and they leave "
         "no record an institution can inspect."),
        ("Incubators and accelerators",
         "They select founders; we prepare them. In practice they are a channel "
         "rather than a competitor — a better-prepared applicant pool is what "
         "they most want."),
        ("Doing nothing",
         "The most common competitor in every segment, and the reason the free "
         "pilot exists."),
    ]),

    ("h2", "Competitive comparison"),
    ("table",
     ["Dimension", "Generic guides and courses", "Training consultancies",
      "StartPad"],
     [["Structure", "A list of things to consider", "A trainer's own deck",
       "Fifteen sequenced missions with a gate"],
      ["AI", "None, or a bolted-on chatbot", "None",
       "A co-founder inside every mission"],
      ["Evidence", "Nothing recorded", "Attendance",
       "Every answer reviewed, scored and retained"],
      ["For the buyer", "No visibility", "A feedback form",
       "Cohort workspace and a decision-ready report"],
      ["Language", "English, translated at best", "Local, inconsistent",
       "Arabic composed by dialect, full right-to-left"],
      ["After the programme", "Nothing", "Nothing",
       "Missions 11–15 stay open; progress stays visible"],
      ["Cost per student", "Low", "High", "Low to moderate"]],
     [2.6, 3.6, 3.2, 5.0]),

    ("h2", "Barriers to entry and defensibility"),
    ("fig", "moat", "What is actually defensible, ordered by how long it would "
                    "take a well-funded competitor to replicate."),
    ("p", "The platform is the least defensible layer and the one most people "
          "mistake for the moat. What is hard is everything around it: a certified "
          "pool in two markets, a curriculum composed in two dialects, "
          "institutional relationships that move at procurement speed, and a "
          "cohort evidence record a buyer would have to abandon to switch away."),

    ("h2", "Porter's Five Forces"),
    ("fig", "porter", "The five forces, with the intensity of each and what "
                      "mitigates it."),

    ("h2", "Market positioning"),
    ("quote", "We do not win by being the best content. We win by being the only "
              "option that leaves the buyer with something they can report."),
    ("p", "StartPad positions as <b>infrastructure for entrepreneurship "
          "education</b>, not as a course and not as a startup programme. The "
          "competitive frame we want in a buyer's head is not \"versus another "
          "course\" but \"versus building and staffing this yourself\" — a "
          "comparison we win on cost, speed, language and evidence."),
])

# =====================================================================
section("Products and Services", [
    ("lead", "What is actually sold, to whom, in what format, and at what price."),

    ("h2", "The platform"),
    ("p", "Fifteen missions across five phases, 4,050 points, 121 tools. Each "
          "mission has a brief, a short lesson, five tasks with an explicit "
          "standard for what a good answer needs, and an evidence slot. Submission "
          "triggers an AI review across specificity, depth, evidence, actionability "
          "and relevance; at 70% the next mission unlocks, below it the founder "
          "gets one highest-gain fix and a full report with answers retained."),
    ("table",
     ["Phase", "Missions", "Points", "Est. time", "What it produces"],
     [["Discovery", "01–03", "350", "4–6 h", "A prioritised problem worth solving"],
      ["Validation", "04–06", "550", "5–7 h", "A tested problem–solution canvas"],
      ["Business model", "07–09", "850", "11–19 h",
       "A full BMC and a working prototype"],
      ["Build and MVP", "10–13", "1,350", "29–54 h", "A shipped MVP with analytics"],
      ["Launch", "14–15", "950", "15–30 h", "A live launch and first customers"]],
     [3.0, 2.0, 1.8, 2.2, 7.2]),

    ("h2", "Features and what each is for"),
    ("table",
     ["Feature", "What it does", "Who it is really for"],
     [["Mission journey", "Fifteen sequenced missions with a review gate",
       "The founder — it removes the blank page"],
      ["AI Co-Founder", "Asks the follow-up a mentor would ask",
       "The founder — and the institution, which cannot staff 1:1 mentoring"],
      ["Tool library", "121 canvases and frameworks mapped to missions",
       "The founder and the facilitator"],
      ["Question Writer", "Interview and survey questions, exported to Forms",
       "The founder doing real validation"],
      ["Programme admin workspace", "Cohort progress, review states, follow-up",
       "The buyer — this is the product they are purchasing"],
      ["Automatic cohort report", "A decision-ready export per cohort",
       "The buyer's own reporting line, and our renewal"],
      ["Student-controlled sharing", "Consent switch per student",
       "The student — and the institution's defensibility"],
      ["Community, mentors, leaderboard", "Peers, bookable experts, progress",
       "Retention between the in-person days"]],
     [3.4, 5.0, 6.2]),

    ("h2", "The in-person layer"),
    ("p", f"Three formats, because a university student, a sixteen-year-old and a "
          f"technical trainee are not the same room. All three end in a public "
          f"showcase judged on reviewed work rather than slides."),
    ("table",
     ["Format", "Length", "Group", "What it ends with", "Price"],
     [["University bootcamp", f"{BOOTCAMP_DAYS} days over 2 weeks",
       f"{COHORT_SIZE} students", "Final Projects Bazaar, certificates, report",
       usd(PRICE_COHORT)],
      ["School cohort", f"{SU['days']} days", f"{SU['size']} students",
       "Public showcase and certificates", usd(SU["price"])],
      ["Technical institute cohort", f"{TU['days']} days", "25–30 trainees",
       "Employability showcase", usd(TU["price"])],
      ["Train-the-trainer", "3 days", "Partner facilitators",
       "Certified trainers who deliver independently", usd(PRICE_TOT_COHORT[1])]],
     [3.2, 3.0, 2.6, 5.0, 2.2]),
    ("fig", "bootcamp_map", "The university format: learn it in the room, build it "
                            "on StartPad that evening, and the programme sees it "
                            "the next morning."),

    ("h2", "Pricing strategy"),
    ("p", "Price is anchored against what the buyer already spends on the "
          "alternative, not against software. A cohort at "
          f"{usd(PRICE_COHORT)} across {COHORT_SIZE} students is "
          f"{usd(PRICE_COHORT/COHORT_SIZE)} a student — below what the same "
          f"institution pays per student for a single external trainer day that "
          f"leaves nothing behind. Seats in national programmes are priced for "
          f"volume and fall as volume rises. Competitions are priced against event "
          f"sponsorship, not against training."),
    ("table",
     ["Line", "Buyer", "Price", "Anchored against"],
     [["University cohort", "Faculty or centre", usd(PRICE_COHORT),
       "An external trainer day with no platform"],
      ["Faculty licence", "Dean", f"{usd(PRICE_FACULTY_LICENCE)} / year",
       "The cost of running it in-house"],
      ["School cohort", "School or group", usd(PRICE_SCHOOL_COHORT[1]),
       "An enrichment or activities budget"],
      ["Whole-school licence", "School group", f"{usd(PRICE_SCHOOL_LICENCE)} / year",
       "Per-student enrichment spend"],
      ["Technical institute cohort", "Institute director", usd(PRICE_TVET_COHORT[1]),
       "Employability programme budgets"],
      ["Sponsored seat", "Ministry or donor", f"{usd(PRICE_INITIATIVE_SEAT[1])} / seat",
       "Cost per beneficiary in comparable programmes"],
      ["Train-the-trainer", "Partner programme", usd(PRICE_TOT_COHORT[1]),
       "External facilitator day rates"],
      ["NGO programme", "Foundation or INGO", usd(PRICE_NGO_PROGRAMME[1]),
       "A bespoke training contract"],
      ["Sponsored competition", "Bank, telco, ministry", usd(PRICE_COMPETITION[1]),
       "Event sponsorship with no platform or evidence"],
      ["Corporate programme", "CSR or innovation lead", usd(PRICE_CORPORATE[1]),
       "Agency-delivered CSR activation"],
      ["Platform seat", "Incubator", f"{usd(PRICE_SEAT[1])} / seat / term",
       "Per-participant tooling spend"],
      ["Pro / Team", "The founder",
       f"{usd(PRICE_PRO_YEAR)} / {usd(PRICE_TEAM_YEAR)} a year",
       "A student's discretionary spend in Cairo"]],
     [3.2, 3.0, 3.0, 7.4]),

    ("h2", "Development stage and intellectual property"),
    ("p", "The platform is built and operating in demo with full bilingual "
          "support. The university curriculum is complete; the school and "
          "technical variants are a Prove-quarter build. The proprietary assets "
          "are the mission sequence and its review rubric, the 121-tool mapping, "
          "the facilitator certification rubric, the bootcamp curriculum and the "
          "bilingual composed content — all held as trade secret and copyright, "
          "with trademark protection on the name and mark in both markets."),
])

# =====================================================================
section("Marketing Strategy", [
    ("lead", "Not consumer acquisition. The job is to make a dean take a meeting, "
             "a sponsor return a call and a ministry shortlist us — and to know "
             "which institutions are ready before we spend a trip on them."),

    ("h2", "Value proposition, by audience"),
    ("table",
     ["Audience", "What we say", "Why it works"],
     [["Dean or university leader",
       "Entrepreneurship outcomes you can put in an accreditation file",
       "Their problem is evidence, not enthusiasm"],
      ["Entrepreneurship centre",
       "A structured programme your centre runs, that makes your centre look good",
       "They are measured on activity and have no method"],
      ["School principal or group",
       "A term-length programme that ends in a showcase parents attend",
       "Visible outcomes to families are the school's currency"],
      ["Technical institute director",
       "Turn a trade into a business — employability you can demonstrate",
       "Their mandate is employment, and they are judged on it"],
      ["Ministry or programme office",
       "The delivery method and per-participant evidence your target needs",
       "They have the target and no way to hit or report it"],
      ["Donor or foundation",
       "A repeatable youth programme with logframe-ready reporting",
       "Reporting burden is their real constraint"],
      ["Competition sponsor",
       "A qualification process that produces finalists worth photographing",
       "They are tired of funding pitch theatre"],
      ["CSR lead",
       "A programme with named beneficiaries and a report for the board",
       "CSR spend is judged on demonstrable impact"],
      ["The founder",
       "A path, not advice — and the first three missions are free",
       "They do not know what to do next"]],
     [3.2, 5.4, 5.0]),

    ("h2", "The two customer journeys"),
    ("fig", "customer_journey", "Two journeys, because there are two customers and "
                                "only one of them pays. They meet in the room: the "
                                "buyer's pilot is the young person's activation."),
    ("p", "<b>Activation is finishing Mission 01, not creating an account.</b> "
          "This is the single most important definition in the marketing plan, "
          "because it separates channels that work from channels that look like "
          "they work. An account that never completes a mission is "
          "indistinguishable from no account at all — and for an institutional "
          "buyer, a cohort of unactivated accounts is worse than nothing, because "
          "it appears in their report."),

    ("h2", "Marketing channels"),
    ("fig", "channel_mix", "Where institutional pipeline comes from in year one, "
                           "and what each channel is actually for."),
    ("deflist", [
        ("The ambassador network — intelligence first, sign-ups second",
         f"{AMBASSADORS[1]} ambassadors across twelve campuses in year one, rising "
         f"to {AMBASSADORS[3]} by year three. Their most valuable output is not "
         f"registrations: it is knowing which entrepreneurship centre has budget "
         f"this term, which dean is under accreditation pressure and which "
         f"student-activities office is looking for an event. That is what turns a "
         f"cold institutional list into a warm pipeline."),
        (f"{PC['name']} — the credibility asset, set out in full below",
         "One founder story, many pieces: an episode in Egyptian Arabic or Saudi "
         "dialect, recorded on a partner campus, cut into reels and posts, every "
         "piece ending at Mission 01. This is not a brand exercise. A dean "
         "responds to a graduate of a university like theirs, and an institution "
         "whose students appear on camera distributes the episode itself."),
        ("Competitions as a marketing channel that pays for itself",
         "A sponsored competition puts StartPad on a campus with a bank already "
         "paying, reaches roughly 700 entrants who each open an account, and "
         "leaves behind both a university relationship and a sponsor "
         "relationship. It is the only marketing channel in the plan that is also "
         "a revenue line."),
        ("Ecosystem events and conferences — where partnerships start",
         "The Global Entrepreneurship Festival in Cairo and the Saudi equivalents "
         "are pipeline events, not brand events. Attendance is judged on meetings "
         "booked, not on stand traffic."),
        ("The annual readiness report — becoming a reference",
         "Published sector research on founder readiness in both markets, built "
         "from anonymised cohort data. It is how a vendor becomes a reference "
         "that ministries and journalists cite, and it is the single highest-"
         "leverage content investment in the plan."),
        ("Targeted digital — retargeting and event fill only",
         "There is no cold paid-acquisition line. Digital spend retargets people "
         "the engines already reached and fills competition and event seats."),
    ]),

    ("pb",),
    ("h2", f"{PC['name']} — the founder podcast"),
    ("lead", f"{PC['name']} · {PC['arabic']}. {PC['premise']}"),
    ("p", "The podcast is in this plan as a demand-generation instrument with a "
          "measurable job, not as brand decoration. It does three things no "
          "advertisement does. It gives a dean a reason to say yes, because their "
          "students appear on camera. It gives a sponsor something deliverable to "
          "attach a name to. And it produces curriculum material as a "
          "by-product, because each episode is mapped to the mission it "
          "illustrates and handed to the learner stuck on exactly that problem."),
    ("fig", "podcast", "How an episode becomes institutional pipeline. The last "
                       "link feeds the first: a founder who has been featured is "
                       "how the next founder is persuaded to appear."),

    ("h3", "Format"),
    ("deflist", [(k, v) for k, v in PC["format"]]),

    ("h3", "Where it is published"),
    ("table",
     ["Channel", "What goes there"],
     [[k, v] for k, v in PC["distribution"]],
     [3.6, 11.4]),

    ("h3", "What it is held to"),
    ("p", "Views are the last row on purpose. A podcast that reaches thirty "
          "thousand people and produces no institutional conversation has failed "
          "at the job it was funded for."),
    ("table",
     ["Measure", "Year 1", "Year 2", "Year 3"],
     [[k, n(a), n(b), n(c)] for k, a, b, c in PC["targets"]],
     [7.2, 2.4, 2.4, 2.4]),
    ("fig", "podcast_targets", "Each row scaled to its own year-three value, so "
                               "measures in different units can be compared by "
                               "shape rather than by size."),
    ("note", "Guest supply is the risk, and it is managed structurally rather "
             "than hoped for: every cohort showcase, every competition final and "
             "every partner event in this plan is also a recording opportunity, "
             "and the student pitch segment means a guest is giving eight minutes "
             "of mentoring rather than sitting for an interview. Founders decline "
             "interviews; they rarely decline students."),

    ("h2", "Brand strategy"),
    ("p", "The brand has to carry two audiences without splitting in half. To a "
          "young person it is energetic, Arabic-first and achievable — points, "
          "levels, missions, a path. To an institution it is credible, evidenced "
          "and safe to sign. The resolution is that both audiences see the same "
          "proof: a cohort of real students with real recorded work."),
    ("deflist", [
        ("Position", "Infrastructure for entrepreneurship education in MENA — not "
                     "a course, not an accelerator."),
        ("Voice", "Direct and unsentimental. Egyptian colloquial in Egypt, Saudi "
                  "dialect in the Kingdom, composed not translated. No "
                  "motivational language, because the product's value is rigour."),
        ("Proof", "Cohort reports, named institutions, founder stories and "
                  "published research — in that order of weight with a buyer."),
        ("What we never say", "Outcome claims the product cannot measure. We do "
                              "not promise jobs created or ventures funded."),
    ]),

    ("h2", "Content marketing"),
    ("table",
     ["Asset", "Audience", "Purpose", "Cadence"],
     [[f"{PC['name']}, the founder podcast", "Young people and deans",
       "Credibility, story supply and curriculum material",
       "Weekly in season; three seasons a year"],
      ["Reels and short video", "Young people",
       "Reach and Mission 01 sign-ups", "3–5 a week"],
      ["Cohort case studies", "Every institutional buyer",
       "The core sales asset", "One per flagship cohort"],
      ["The annual readiness report", "Ministries, donors, press",
       "Become a cited reference", "Annual, with a quarterly data note"],
      ["Facilitator and educator guides", "Partner institutions",
       "Reduce delivery friction and support cost", "Per curriculum release"],
      ["Competition coverage", "Sponsors and campuses",
       "Sponsor obligation and next-sale collateral", "Per competition"]],
     [3.6, 4.0, 4.6, 3.4]),

    ("h2", "Marketing budget"),
    ("table",
     ["Line", "Year 1", "What it is for"],
     [[name, usd(val), purpose] for (name, val), purpose in zip(
         MD.DEMAND_SPEND[1],
         [f"{PC['name']}: founder stories in both dialects, recorded on partner "
          f"campuses — the asset that makes an institutional pitch credible",
          f"{AMBASSADORS[1]} ambassadors: the cheapest source of founders and the "
          f"early-warning system for which campuses are ready to buy",
          "Where partnership conversations start; judged on meetings booked",
          "Retargeting, competition entry and event fill only — no cold "
          "acquisition",
          "Cohort reports, case studies and the proposal pack: the most used "
          "sales assets in the company",
          "Published research that turns a vendor into a reference"])] +
     [["Total", usd(sum(v for _, v in MD.DEMAND_SPEND[1])), ""]],
     [4.2, 2.0, 9.2]),
    ("note", f"Against a subscriber lifetime value of {usd(SUBS['ltv'])}, buying "
             f"strangers through cold paid social in these markets costs more per "
             f"paying founder than the founder is worth. The budget that would "
             f"have funded it buys content, ambassadors and events instead — all "
             f"of which feed the institutional pipeline as well as the "
             f"subscription one."),
])

# =====================================================================
section("Sales Strategy", [
    ("lead", "Eight engines, four selling motions, and one rule: never sell a "
             "cohort there is no certified pair to deliver."),

    ("h2", "The sales model"),
    ("table",
     ["Motion", "Engines", "Cycle", "Who sells it", "Decision maker"],
     [["Land-and-expand", "Universities; schools and technical",
       "1–2 terms", "Heads plus associates",
       "Centre director, capstone coordinator, dean, principal"],
      ["Public tender and grant", "National initiatives; NGO and donor",
       "9–15 months", "Head of Government; Head of NGO, with the bid "
                      "administrator", "Programme office, donor committee"],
      ["Sponsorship", "Competitions; corporate and CSR",
       "2–5 months", "Competitions manager; CEO on anchor deals",
       "Marketing, CSR or communications budget holder"],
      ["Product-led partner", "Programme and incubator seats; subscriptions",
       "2–8 weeks", "Associates; self-serve for subscriptions",
       "Programme director; the founder"]],
     [2.8, 3.4, 1.8, 4.0, 4.6]),

    ("h2", "Sales team structure"),
    ("p", f"Eight engines, and at no point more than "
          f"{max(HC_BY_FN['Institutional Partnerships'][f'y{y}'] for y in MD.YEARS_5)} "
          f"people selling them. Heads own a <b>buyer type</b> rather than a "
          f"territory, because the buying behaviour of a ministry and a bank have "
          f"nothing in common and the skills do not transfer. The Saudi country "
          f"manager is the deliberate exception and owns every engine in the "
          f"Kingdom, because there the relationship precedes the product line. "
          f"Where a head does not yet exist, the engine is carried by somebody "
          f"else and the plan says who."),
    ("table",
     ["Role", "Engines owned", "Y1", "Y2", "Y3", "Y4", "Y5"],
     [[r, owns] + [n(dict(zip(MD.YEARS_5, counts))[y]) for y in MD.YEARS_5]
      for r, owns, counts in [
          (role, owns, counts)
          for (fn, role, monthly, *counts) in MD.ROLES
          if fn == "Institutional Partnerships"
          for owns in [{
              "Head of Partnerships — Egypt":
                  "Engines 1 and 7 in Egypt; carries 2, 5 and 6 until their own "
                  "heads arrive",
              "Country Manager — KSA (Riyadh)":
                  "Every engine in Saudi Arabia",
              "Head of Government, Initiatives and Donors":
                  "Engines 3 and 4; takes engine 5 from year three",
              "Partnerships and bids associate":
                  "Proposals, tenders and the named-target list, across all "
                  "engines",
              "Head of Schools and Technical Education":
                  "Engine 2 in both markets",
              "Account manager — renewals":
                  "The signed base, across all engines",
          }[role]]]],
     [4.0, 5.4, 0.9, 0.9, 0.9, 0.9, 0.9]),
    ("note", "Three engines have no dedicated owner in year one and two have none "
             "until year four. That is a stated cost of the headcount cap, not an "
             "oversight: the Egyptian partnerships head carries competitions, "
             "schools and corporate sponsors through year one, which is exactly "
             "why the roadmap gates those engines late and why the school engine "
             "ramps more slowly than its population would justify."),

    ("h2", "The sales process"),
    ("fig", "institution_workflow", "From identifying the right person to a cohort "
                                    "report, in six steps over seven weeks."),
    ("p", "One contract covers all three layers — the in-person bootcamp, the "
          "on-campus workshops and a platform seat for every student under one "
          "programme admin account. Selling the layers separately would triple the "
          "procurement cycle inside institutions where procurement is already the "
          "longest part of the sale."),

    ("h2", "The four doors into a university"),
    ("table",
     ["Door", "Who", "What they want", "What we offer first"],
     [["01", "Entrepreneurship centre", "A structured programme to show",
       "A free pilot cohort"],
      ["02", "Capstone coordinator", "A method for graduation projects",
       "Missions mapped to the term"],
      ["03", "Dean of faculty", "Outcomes for accreditation",
       "A faculty-wide licence"],
      ["04", "Student activities", "Events that fill rooms",
       "A sponsored competition — their budget is zero and ours is a sponsor's"]],
     [1.2, 3.4, 4.2, 5.8]),
    ("fig", "university_ladder", "The land-and-expand ladder. The free pilot is not "
                                 "a discount — it is how the institution's own "
                                 "report becomes the sales document for everything "
                                 "after it."),
    ("fig", "school_ladder", "The same ladder in schools and technical education, "
                             "with a shorter format and a different frame."),

    ("h2", "The institutional pipeline"),
    ("fig", "pipeline", "The funnel the company actually runs. Every stage is a "
                        "number a named person owns."),
    ("table",
     ["Stage", "Year one", "Conversion", "Who owns it"],
     [[label, n(val), "—" if i == 0 else pct(val / PIPE[i - 1][1]),
       ["The bids associate and the ambassador network",
        "The relevant head, or the country manager in Saudi Arabia",
        "Head of the relevant engine, with the bids associate",
        "The signing head, against the partner network manager's capacity "
        "forecast"][i]]
      for i, (label, val) in enumerate(PIPE)],
     [5.2, 1.8, 2.0, 7.6]),

    ("h2", "Strategic partnerships"),
    ("deflist", [
        ("Banks", "Sponsor competitions, fund MSME programmes and reach "
                  "first-time founders they want as future customers. The most "
                  "commercially aligned partner type in the plan."),
        ("Incubators and accelerators", "Require StartPad missions as part of "
                                        "their application and get a prepared "
                                        "pool. Channel as much as revenue."),
        ("School groups and operators", "One relationship, many schools — the "
                                        "fastest route to volume in Engine 2."),
        ("Implementing partners for donors", "The organisations that actually "
                                             "deliver donor programmes; they "
                                             "need a method and we need their "
                                             "contracts."),
        ("Ministries", "The largest contracts and the longest cycles. Pursued in "
                       "pairs so no single relationship is existential."),
    ]),

    ("h2", "Sales metrics"),
    ("bul", [
        "<b>Qualified meetings booked</b> per head per month — the only leading "
        "indicator that moves early.",
        "<b>Pilot-to-paid conversion</b>, by engine. The number that proves the "
        "cohort report does its job.",
        "<b>Second-term renewal rate</b> — the single most important number in "
        "the company.",
        "<b>Net revenue retention</b> across the signed base, owned by the account "
        "manager from year two.",
        "<b>Capacity-constrained losses</b>: deals not pursued because no "
        "certified pair was available. If this is zero, we are under-selling; if "
        "it is large, certification is behind.",
    ]),
])

# =====================================================================
section("Engagement Model", [
    ("lead", "Naming the organisations is half the work. This part says how "
             "StartPad actually gets inside each of them: the six ways in, who is "
             "approached, what the first ask is, how the money moves, and what "
             "has to be true before the ask can be made at all."),

    ("h2", "StartPad is never the programme — it is inside somebody else's"),
    ("p", "This is the governing idea of the whole commercial plan and it is "
          "worth stating before the mechanics. StartPad does not ask an "
          "institution to start something new. It attaches to a programme that "
          "already exists, already has a budget, already has a target it is "
          "measured against, and is already failing to meet it in a specific way. "
          "A competition already runs; it cannot tell a good team from a "
          "well-coached one. An academy already has two hundred courses; nothing "
          "happens after a learner finishes one. A ministry has committed to a "
          "million entrepreneurs; it has an online curriculum and no build stage. "
          "In every case the sale is a component, not a programme — which is why "
          "it can be bought out of money already committed, and why the decision "
          "does not have to reach a minister."),
    ("deflist", [
        ("Enter at the edge, never at the centre",
         "A campus team, a governorate branch, a single chapter, one college. The "
         "edge can authorise a first; head office can only authorise a precedent. "
         "Every route in this plan starts one level below where an outsider would "
         "aim, and that is deliberate."),
        ("Pay for the proof yourself",
         "The first cohort inside a new organisation is funded by StartPad. It "
         "costs roughly the price of a sales trip and it produces the one asset "
         "every later conversation needs: a completed cohort with their name on "
         "the report. Year one runs eight of these."),
        ("Sell the component, not the programme",
         "The ask is always a line inside something they already fund — a build "
         "stage before their competition, a block of seats on their initiative, a "
         "capstone to their course. New programmes need new budget and new "
         "approval; components need neither."),
        ("End at certification, wherever volume is the point",
         "No provider can staff a national initiative, and proposing to signals "
         "that the scale has not been understood. The destination for every "
         "public engine is that the institution's own trainers are certified, "
         "audited and licensed by StartPad."),
    ]),

    ("h2", "The six engagement plays"),
    ("p", "These are the only six ways StartPad ever enters an organisation. They "
          "are ordered by how little the counterparty has to risk in order to say "
          "yes, which is also the order a single relationship moves through as it "
          "matures — most of the named targets in this plan are a sequence of two "
          "or three of them rather than one."),
    ("fig", "engagement_plays", "The six plays, with the person approached and the "
                                "way money moves in each. An engagement model that "
                                "names neither is a diagram of a hope."),
    ("table",
     ["", "The play", "The first ask", "How long it takes"],
     [[code, name, ask, how_long] for code, name, who, ask, money, pre, how_long
      in PLAYS],
     [0.9, 3.2, 7.4, 3.5]),

    ("h3", "What must exist before each play can be run"),
    ("p", "The sequencing in the roadmap is not arbitrary. Each play is gated on "
          "an asset the company does not have on day one, and the order in which "
          "those assets are built is the order in which the engines open."),
    ("table",
     ["What has to exist", "Unlocks", "By", "Why it lands then"],
     [[what, play, when, why] for what, play, when, why
      in MD.ENGAGEMENT_PREREQUISITES],
     [5.0, 1.4, 1.8, 6.8]),

    ("h2", "The route in, step by step"),
    ("fig", "engagement_route", "The same five steps every time. The route is a "
                                "repeatable procedure, not a series of fortunate "
                                "introductions."),
    ("num", [
        "<b>Find the edge.</b> Identify the smallest unit inside the target that "
        "can authorise a pilot without a committee — a campus chapter, a "
        "governorate branch, one college, one school with an employer partner. "
        "Name the individual, not the organisation.",
        "<b>Fund the proof.</b> Run one cohort at StartPad's cost, inside their "
        "programme, under their name, with a showcase their leadership is invited "
        "to attend. Ask for nothing in return except permission to publish the "
        "report with their name on it.",
        "<b>Publish it.</b> The cohort report, a Mission Zero episode recorded on "
        "their site, and the case study. The institution now has something to "
        "circulate internally, which is the mechanism by which the decision moves "
        "upward without StartPad pushing it.",
        "<b>Price the block.</b> Take the report to the budget holder and ask for "
        "a line inside an existing programme: a season, a seat block, a term. "
        "Never a new programme; never a platform licence in isolation.",
        "<b>Certify them.</b> Where the volume is larger than any provider could "
        "staff, move the relationship to trainer certification. StartPad keeps "
        "the standard, the assessment and the audit; the institution gains "
        "capacity it owns. This is where the engagement becomes an annuity.",
    ]),
    ("note", "The five steps compress or stretch, but they do not reorder. "
             "Attempting step four before step two — asking for budget before "
             "there is a report with their name on it — is the single most common "
             "way an institutional sale in this market dies, and it dies slowly, "
             "consuming a quarter before it does."),

    ("pb",),
    ("h2", "National initiatives and government: the route into each"),
    ("p", "The longest cycles in the company and the largest eventual volumes. "
          "Each row names the plays in sequence and the specific door."),
    ("table",
     ["Organisation", "Plays", "How StartPad gets engaged"],
     [[row[0], row[4], row[5]] for row in MD.NAMED_INITIATIVES],
     [4.3, 1.8, 10.5]),

    ("pb",),
    ("h2", "Competitions and youth organisations: the route into each"),
    ("p", "The fastest engine to enter and the one that reaches the most young "
          "people per deal, because somebody else has already assembled them. The "
          "structural fact that governs every row below: the organiser has no "
          "budget and the sponsor does, so the organiser is the partner and the "
          "sponsor is the customer."),
    ("table",
     ["Competition", "Plays", "How StartPad gets engaged"],
     [[row[0], row[4], row[5]] for row in MD.NAMED_COMPETITIONS],
     [4.3, 1.8, 10.5]),

    ("pb",),
    ("h2", "Delivery partners, donors and sponsors: the route into each"),
    ("p", "The organisations in this table are mostly not customers. They are the "
          "delivery capacity, the funding and the distribution that let a company "
          f"of {HC['y3']} people operate at national scale, and several are worth "
          f"considerably more as partners than they would ever be worth as "
          f"accounts."),
    ("table",
     ["Organisation", "Plays", "How StartPad gets engaged"],
     [[row[0], row[4], row[5]] for row in MD.NAMED_PARTNERS],
     [4.3, 1.8, 10.5]),

    ("h2", "What StartPad gives away, and why"),
    ("p", f"A certified delivery partner keeps "
          f"{pct(MD.PARTNER_REVENUE_SHARE)} of the cohort fee. A competition "
          f"organiser keeps its own brand on the competition. A ministry that "
          f"certifies its trainers stops buying delivery altogether and buys only "
          f"the standard and the seats. Each of these is margin, brand or revenue "
          f"deliberately surrendered, and each buys the same thing: volume that "
          f"does not have to be hired for. The margin given away is the margin "
          f"StartPad does not have to carry a payroll against — which is the "
          f"arithmetic behind an establishment of {HC['y3']} people in year three "
          f"and {HC['y5']} in year five."),
    ("note", "The limit is equally deliberate. StartPad never gives away the "
             "certification standard, the assessment rubric, the evidence record "
             "or the right to withdraw a licence. A partner may own the "
             "relationship and the room; it never owns the definition of what "
             "good looks like. The moment that is conceded, the company is a "
             "training supplier rather than a standard, and everything "
             "defensible about it is gone."),
])

# =====================================================================
section("Go-to-Market Roadmap", [
    ("lead", "Eight engines, eight different starting lines. This is the part of "
             "the plan that says when each one opens and what has to be true "
             "first."),

    ("h2", "Nothing starts on day one"),
    ("p", "A plan that shows eight revenue lines running from the first quarter is "
          "a plan that has not been thought through. A faculty licence cannot be "
          "sold before two cohorts have run at that faculty. A ministry will not "
          "contract a platform that cannot show a cohort report. A school cohort "
          "needs a school variant of the curriculum that does not exist in the "
          "Land quarter. Each engine therefore opens on a <b>gate</b> — a "
          "condition, not a date."),
    ("fig", "roadmap", "The twelve-quarter roadmap. Each engine's bar begins at "
                       "its gate; a grey cell means the engine is not yet open."),

    ("h2", "The gates"),
    ("fig", "gates", "What has to be true before each engine can sell anything, "
                     "and why."),

    ("h2", "The four phases of year one"),
    ("fig", "phases", "Egypt and Saudi Arabia, in parallel, through four phases."),
    ("table",
     ["Quarter", "Phase", "What opens", "What is being proven"],
     [["Q4 2026", "Land",
       "University cohorts only — paid in KSA through programme partners, free "
       "pilots in Egypt",
       "That a cohort can be delivered to standard, and that the report is worth "
       "circulating"],
      ["Q1 2027", "Prove",
       "Paid Egyptian cohorts, the first sponsored competition, programme and "
       "incubator seats",
       "That a pilot report converts to a paid cohort, and that a sponsor will "
       "fund a competition"],
      ["Q2 2027", "Expand",
       "School and technical cohorts, NGO and donor programmes",
       "That the method transfers to a younger room and to a donor logframe"],
      ["Q3 2027", "Scale",
       "Faculty licences, national initiative seats, corporate programmes, "
       "train-the-trainer",
       "That an institution renews and widens, and that a ministry will contract "
       "a private platform"]],
     [1.9, 1.6, 5.4, 7.7]),

    ("h2", "Delivery volume, quarter by quarter"),
    ("fig", "quarterly_volumes", "What the company is physically delivering each "
                                 "quarter, across all in-person formats."),

    ("h2", "The five moves"),
    ("fig", "gtm_moves", "The five moves and what each unlocks. The order is "
                         "load-bearing: each move is affordable only because the "
                         "one before it happened."),

    ("h2", "The critical path"),
    ("p", "One chain determines whether year one works, and every item on it is an "
          "input to the next."),
    ("num", [
        "<b>Certify four facilitators and finish the bilingual curriculum</b> "
        "before the Land quarter opens. Nothing else can start.",
        "<b>Deliver four free Egyptian pilots flawlessly.</b> They are the only "
        "sales collateral the Prove quarter will have.",
        "<b>Ship the automatic cohort report.</b> Until it generates without "
        "manual editing, every engine is selling a promise.",
        "<b>Convert a pilot into a paid cohort.</b> This single event validates "
        "the land-and-expand motion the whole education family depends on.",
        "<b>Open government conversations in the Land quarter</b> even though "
        "they cannot close for a year. Starting late pushes seat volume out of "
        "year two entirely.",
        "<b>Build the school variant in Prove</b> so Engine 2 can open in Expand. "
        "It is the largest unserved segment and the one most likely to slip.",
    ]),
    ("note", "If the roadmap slips anywhere, it should slip at the engines with "
             "the shortest cycles — competitions and programme seats can be "
             "recovered within a quarter. The two that must not slip are "
             "facilitator certification and the government conversations, because "
             "neither can be compressed later."),

    ("h2", "Two markets, two doors"),
    ("table",
     ["", "Egypt", "Saudi Arabia"],
     [["First door", "Universities and campuses",
       "Programmes and youth initiatives"],
      ["Lead engine", "University cohorts",
       "Sponsored seats, then a Riyadh competition"],
      ["Why this door", "Scale of the student population and campus access",
       "Funded programmes move faster than university procurement"],
      ["Voice", "Egyptian colloquial", "Saudi dialect, composed not translated"],
      ["Team", "Core team in Cairo", "A country manager, supported from Cairo"],
      ["Paid revenue from", "Q1 2027, after the pilots",
       "Q4 2026, from the first quarter"]],
     [2.8, 5.2, 5.6]),
    ("fig", "flywheel", "Why it compounds: founders who progress become the "
                        "stories that win the next campus, sponsor and programme."),
])

# =====================================================================
section("Operations Plan", [
    ("lead", "How a signed contract becomes a delivered cohort, repeatedly, by "
             "people the customer has never met — and what breaks first if it "
             "does not."),

    ("h2", "The operating model"),
    ("p", "StartPad runs a <b>hybrid delivery model</b>: a software platform with "
          "near-zero marginal cost, wrapped in an in-person layer with real "
          "marginal cost. The economics and the risks of the business both sit in "
          "that second layer, and so does this plan's binding constraint."),
    ("table",
     ["Layer", "What it is", "Marginal cost", "Scales by"],
     [["Platform", "Missions, AI review, workspace, reporting", "Near zero",
       "Engineering and inference capacity"],
      ["In-person delivery", "Bootcamps, school cohorts, technical cohorts",
       "High — two certified facilitators for four to six days",
       "Certified facilitators"],
      ["Events", "Competitions, Bazaars, showcases", "Moderate, per event",
       "Event staff and calendar"],
      ["Partner-delivered", "Train-the-trainer, programme seats, school clubs",
       "Low after certification", "Certified partner trainers"]],
     [2.8, 5.2, 3.6, 4.0]),
    ("p", "The strategic consequence: engines that scale through the first and "
          "fourth rows — sponsored seats, programme seats, train-the-trainer — "
          "grow past the facilitator ceiling, while engines in the second row do "
          "not. That is why the revenue mix shifts the way it does."),

    ("h2", "Twelve people, three hundred cohorts"),
    ("p", f"The establishment is capped at {HC['y3']} people in year three. That "
          f"cap is the central design constraint of this plan rather than an "
          f"aspiration attached to it, and it is only survivable because StartPad "
          f"does not deliver cohorts itself at scale. It certifies the "
          f"organisations and the freelancers who do, audits them, and employs "
          f"the people who define the standard. Headcount therefore grows with "
          f"the number of partners to audit, not with the number of cohorts to "
          f"run — which is the difference between a company that can reach "
          f"national volume and a training provider that cannot."),
    ("fig", "leverage", "Employees against the network that delivers for them, "
                        "across five years, on one scale."),
    ("table",
     ["", "Year 1", "Year 2", "Year 3"],
     [["StartPad employees"] + [n(r["staff"]) for r in LEV],
      ["Certified facilitators in the pool"] + [n(r["pool"]) for r in LEV],
      ["Certified partner organisations"] + [n(r["partners"]) for r in LEV],
      ["Cohorts delivered in the year"] + [n(r["cohorts"]) for r in LEV],
      ["Learners reached, cohorts and seats"] + [n(r["learners"]) for r in LEV],
      ["Learners per employee"]
      + [n(r["learners_per_employee"]) for r in LEV]],
     [5.6, 3.1, 3.1, 3.1]),
    ("deflist", [
        ("Two ratios hold the whole structure up",
         f"One partner network manager can hold roughly "
         f"{MD.PARTNERS_PER_NETWORK_MANAGER} certified partner organisations, and "
         f"one delivery coordinator can schedule and report on roughly "
         f"{n(MD.COHORTS_PER_COORDINATOR)} cohorts a year. Those two numbers, not "
         f"the revenue, are what determine when the next person is hired. They "
         f"are stated here so that a reader who disbelieves the cap can argue "
         f"with the ratio rather than with the conclusion."),
        ("A certified facilitator is part-time, and that is the design",
         f"Each gives StartPad about {pct(MD.FACILITATOR_UTILISATION)} of a "
         f"delivery year — they are university staff, trainers and practitioners "
         f"with other work. That is why the pool is large "
         f"({LEV[2]['pool']} by year three) while the payroll is not, and why a "
         f"quarter in which a university postpones costs the company almost "
         f"nothing."),
        ("A certified partner organisation runs its own cohorts",
         f"Roughly {MD.COHORTS_PER_PARTNER} a year each, under licence, keeping "
         f"{pct(MD.PARTNER_REVENUE_SHARE)} of the fee. StartPad supplies the "
         f"curriculum, the platform, the certification and the audit, and takes "
         f"no delivery risk at all on those cohorts."),
    ]),

    ("h2", "The binding constraint"),
    ("p", f"A facilitator pair runs {COHORTS_PER_PAIR['university']} university "
          f"cohorts a year once travel, preparation and campus holidays are taken "
          f"out — {COHORTS_PER_PAIR['school']} of the shorter school format and "
          f"{COHORTS_PER_PAIR['tvet']} technical cohorts. The quarterly delivery "
          f"plan therefore converts directly into a facilitator headcount, and "
          f"that number, not the sales target, is the operating plan's primary "
          f"schedule."),
    ("fig", "cohort_ramp", "Delivery load against the facilitator capacity it "
                           "requires, across all twelve quarters."),
    ("table",
     ["Year", "Cohorts delivered", "Facilitator days needed",
      "Certified pool", "Days the pool gives", "Utilisation"],
     [[c["label"], n(c["total"], 1), n(c["days"]), n(c["facilitators"]),
       n(c["available"]), pct(c["utilisation"])] for c in CAP],
     [1.4, 2.3, 2.6, 2.0, 2.4, 1.8]),

    ("h2", "Certification — the only thing StartPad does not delegate"),
    ("p", "The certified pool and the certified partner network are the "
          "operational asset and the main single point of failure. Four steps, "
          "run by the partner network manager and signed off by the Head of "
          "Curriculum, who is the only person who can pass or fail a candidate."),
    ("num", [
        "<b>Observe</b> a full cohort end to end, without delivering.",
        "<b>Co-deliver</b> two days under a facilitator already certified at "
        "lead tier.",
        "<b>Deliver</b> a full cohort observed and scored against the facilitator "
        "rubric.",
        "<b>Recertify</b> each term against cohort outcomes and student feedback.",
    ]),
    ("note", "Nobody facilitates unobserved before step three is passed, "
             "including under schedule pressure — which is precisely the only "
             "time the rule matters. Recruitment runs a quarter ahead of the "
             "delivery plan, never against it. A company whose entire argument is "
             "that certification substitutes for employment cannot afford a "
             "certification that passes everybody, and the Head of Curriculum's "
             "success measure is written to make failing candidates the correct "
             "behaviour rather than an awkward one."),
    ("p", "Partner organisations are certified on the same principle one level "
          "up: a certification cohort for their facilitators, one supervised "
          "delivery, then sample audits each term, with licence withdrawal as a "
          "real and occasionally used sanction. A licence that has never been "
          "withdrawn from anybody is not a licence."),
    ("p", f"The same machinery certifies partner and ministry trainers under the "
          f"train-the-trainer engine. That is what makes "
          f"{n(plan('initiative_seats', 3))} sponsored seats in year three "
          f"deliverable by an organisation of this size: StartPad certifies, the "
          f"partner delivers."),

    ("h2", "Service delivery — the cohort machine"),
    ("p", "Every cohort runs the same way, and the sameness is the point: it lets "
          "a freelance facilitator deliver a cohort the company has never seen, "
          "and makes the report comparable across institutions."),
    ("num", [
        "<b>Scheduling.</b> Dates are fixed against the institution's academic "
        "calendar, not ours. Egyptian and Saudi terms differ and Ramadan moves. "
        "The calendar is built a term ahead and is the constraint sales sells "
        "against.",
        "<b>Facilitator assignment.</b> A certified pair per group, with a "
        "lead-tier facilitator on the first cohort at any new institution and on "
        "any cohort a newly certified partner delivers. There are no employed "
        "facilitators: the tier, not the contract, is what earns the "
        "assignment.",
        "<b>Materials.</b> Printed kits, problem cards, canvases and certificates "
        "shipped to the venue a week ahead; digital copies in the workspace.",
        "<b>The daily loop.</b> Opener on last night's progress; short input, then "
        "apply it; checkpoint marked Meets, Partly or Not yet; the team splits "
        "that night's missions and submits; AI feedback lands before the next "
        "opener.",
        "<b>The showcase.</b> The final day is public — faculty, families, "
        "partners and judges, who see reviewed work rather than slides.",
        "<b>Report and handover.</b> Certificates and the cohort report issue "
        "within five working days. Missions beyond the camp stay open to the "
        "student, and the institution keeps visibility.",
    ]),

    ("h2", "Supply chain and facilities"),
    ("table",
     ["Input", "Source", "Risk", "Mitigation"],
     [["Certified facilitators", "Recruited and certified in-house",
       "The highest-risk input in the business",
       "Certify a quarter ahead; tiered day rates; a progression path"],
      ["Certified partner organisations",
       "Youth NGOs, training providers, university centres",
       "A partner that under-delivers damages the standard, not just a cohort",
       "Sample audit each term; published standard; licence withdrawal"],
      ["Venues", "Provided by the institution under contract",
       "Cancellation or double-booking",
       "Venue confirmed in the contract; a standing fallback per city"],
      ["Printed materials", "Local print partners in Cairo and Riyadh",
       "Lead time and customs on cross-border shipment",
       "Print locally in each market; never ship kits across a border"],
      ["Cloud and AI inference", "Major cloud and model providers",
       "Cost per review at seat scale; provider outage",
       "Cost monitored per active user; fallback provider for review"],
      ["Mentors and judges", "The mentor network", "Availability at Bazaar season",
       "Network managed continuously, not per event"]],
     [2.8, 3.6, 4.2, 6.0]),
    ("p", "Facilities are deliberately light: one office in Cairo, a desk in "
          "Riyadh, and from year three small regional hubs in Upper Egypt, the "
          "Delta and Jeddah — placed where facilitators live rather than where "
          "management does, because travel time is the hidden cost in cohort "
          "delivery."),

    ("h2", "Technology infrastructure"),
    ("table",
     ["Capability", "Which engine needs it", "Needed by"],
     [["Programme admin workspace: cohort creation, bulk invitation, educator "
       "assignment", "Engines 1, 2, 4, 7 — without it there is no institutional "
                     "product", "Q4 2026"],
      ["Student-controlled sharing with scoped programme data",
       "All engines — the trust position that makes an institution sign",
       "Q4 2026"],
      ["AI review at cohort volume, overnight",
       "Engines 1 and 2 — the daily loop breaks without it", "Q4 2026"],
      ["Full Arabic parity, right-to-left, including exported PDFs",
       "All engines — a ministry cannot circulate a report it cannot read",
       "Q4 2026"],
      ["Competition entry, qualification and judging flow",
       "Engine 5 — entry as an account, rounds as missions, a generated judges' "
       "pack", "Q1 2027"],
      ["The automatic cohort report",
       "Every education and public engine — the renewal document", "Q1 2027"],
      ["Safeguarding controls and parental consent records",
       "Engine 2 — a legal condition of selling to schools", "Q2 2027"],
      ["Bulk seat provisioning and partner reporting by region",
       "Engine 3 — programmes place thousands of seats at once", "Q3 2027"]],
     [4.4, 6.8, 2.6]),

    ("h2", "Quality control"),
    ("p", "Four gates are measured on every cohort. A cohort failing any one of "
          "them triggers a review before another is scheduled at that institution."),
    ("bul", [
        "<b>Mission completion.</b> At least 80% of students complete the "
        "programme's required missions by the showcase. Below that, the evening "
        "loop is not working and facilitator pairing is examined first.",
        "<b>Review turnaround.</b> AI feedback available before the next day's "
        "opener, every night. This is a platform SLA, not a target.",
        "<b>Showcase delivery.</b> Every team presents and every member speaks. A "
        "team that cannot is a facilitation failure that showed up two days "
        "earlier and was not caught.",
        "<b>Report issued inside five working days</b> to the person who signed.",
    ]),

    ("h2", "Regulatory compliance"),
    ("deflist", [
        ("Safeguarding and child protection",
         "Facilitator and partner vetting, safeguarding training, parental "
         "consent and a written incident procedure — owned by the CEO until the "
         "COO arrives in year four, and externally attested in both markets "
         "because an internal attestation is worth nothing here. Non-negotiable "
         "before any school cohort runs, including a partner's."),
        ("Data protection", "Scoped institutional visibility, student-controlled "
                            "sharing, server-side scoring, and documented "
                            "retention periods."),
        ("Two jurisdictions", "An Egyptian operating company and a Saudi entity, "
                              "with local employment and invoicing compliance in "
                              "each."),
        ("Procurement readiness", "A maintained pre-qualification library — "
                                  "registrations, policies, certifications and "
                                  "references — because a missing document loses "
                                  "a bid more often than a weak proposal does."),
    ]),

    ("h2", "Operational KPIs"),
    ("table",
     ["KPI", "Why it matters", "Target"],
     [["Certified pairs available vs. plan", "The constraint on everything",
       "Ahead of plan every quarter"],
      ["Mission completion rate per cohort", "What the buyer is paying for",
       "80% or above"],
      ["Overnight review SLA met", "The daily loop depends on it", "100% of nights"],
      ["Report issued within five working days", "Renewal depends on it", "100%"],
      ["Seat activation rate (sponsored programmes)",
       "Where seat programmes actually fail", "70% or above"],
      ["Facilitator retention, term on term", "Protects the core asset",
       "85% or above"],
      ["Safeguarding incidents", "Licence to operate in schools", "Zero"],
      ["Cohorts declined for lack of capacity", "Honesty about the constraint",
       "Tracked and reported, not hidden"],
      ["Certified capacity vs. booked demand, next quarter",
       "The number the whole headcount cap rests on",
       "Capacity ahead in every quarter"],
      ["Partner-delivered cohort scores vs. StartPad-run",
       "Whether certification actually transfers the standard",
       "Within five points, or the partner is audited"],
      ["Partner audits completed per term",
       "An audit nobody runs is not a control",
       "Every active partner, every term"],
      [f"Institutional enquiries credited to {PC['name']}",
       "Whether the content budget is pipeline or decoration",
       f"{n(PC['targets'][5][1])} in year one, rising"]],
     [4.6, 5.8, 3.2]),
])

# =====================================================================
section("Management and Organization", [
    ("lead", f"{HC['y1']} employees in year one, {HC['y3']} in year three and "
             f"{HC['y5']} in year five — a hard cap, not a forecast — in five "
             f"reporting lines, plus three layers that are not on the payroll and "
             f"carry almost all of the delivery."),

    ("h2", "The cap, and why it is a cap"),
    ("p", f"Most plans state a headcount and then discover it. This one states a "
          f"ceiling and designs backwards from it: {HC['y1']}, {HC['y2']}, "
          f"{HC['y3']}, {HC['y4']}, {HC['y5']}. Four rules hold it there, and "
          f"each has a visible cost that is admitted elsewhere in this part "
          f"rather than hidden."),
    ("num", [
        "<b>Employ the people who define and audit the standard; contract the "
        "people who deliver it.</b> Every cohort in this plan is run by a "
        "certified freelance facilitator or a certified partner organisation, "
        "never by an employee. Cohort growth therefore cannot become payroll "
        "growth, which is the only reason the cap survives contact with the "
        "delivery plan.",
        "<b>No role is created until it is genuinely full-time.</b> Until then it "
        "is part of a larger role, the role description says so, and it names the "
        "year it splits out. The cost is real: the Egyptian partnerships head "
        "carries competitions, schools and sponsors through year one, which is "
        "precisely why the school engine ramps slowly.",
        "<b>Standard, regulated functions are bought, not hired.</b> Bookkeeping, "
        "payroll, audit, corporate legal, the Saudi entity, video production and "
        "translation quality assurance sit with firms and freelance panels. They "
        "appear in operating costs and not on the establishment.",
        "<b>The chief executive carries operations until the network outgrows one "
        "person.</b> The plan puts that in year four, and the chief operating "
        "officer arrives then and not before. This is the single largest key-"
        "person risk in the plan, and it is named in the risk register rather "
        "than argued away.",
    ]),
    ("fig", "team_arc", "Six to twenty, and the reason for each step. Every hire "
                        "in years four and five is a function the earlier years "
                        "deliberately merged into somebody else's job."),

    ("h2", "Organisational structure"),
    ("fig", "org_chart", "The year-one organisation. The grey notes matter more "
                         "than the boxes: they say what is carried by somebody "
                         "whose title says something else."),
    ("p", "The structure follows the engines, not the functions. Institutional "
          "sales is organised by <b>buyer type</b> — university, school, "
          "government, donor, sponsor — because the buying behaviour of a ministry "
          "and a bank have nothing in common and the skills do not transfer. The "
          "Saudi country manager is the one exception: in that market the "
          "relationship comes before the product line, so one person owns every "
          "engine."),
    ("fig", "headcount", "The establishment across five years against the cap it "
                         "commits to. Bars that touch the dashed line and never "
                         "cross it are the whole argument."),
    ("table",
     ["Function", "Y1", "Y2", "Y3", "Y4", "Y5", "What it owns"],
     [[fn] + [n(HC_BY_FN[fn][f"y{y}"]) for y in MD.YEARS_5] + [owns]
      for fn, owns in [
         ("Leadership", "Direction, institutional relationships, and arbitration "
                        "between sales ambition and certified capacity"),
         ("Product and Engineering", "The platform, the review pipeline, the "
                                     "mentor and institutional reporting"),
         ("Curriculum and Delivery", "What is taught, who is fit to teach it, and "
                                     "the network that teaches it"),
         ("Institutional Partnerships", "All eight engines, organised by buyer "
                                        "type"),
         ("Growth and Content", "Mission Zero, ambassadors, the readiness report "
                                "and learner retention")]],
     [3.0, 0.9, 0.9, 0.9, 0.9, 0.9, 8.1]),
    ("p", "The structure follows the buyer, not the function. Institutional "
          "partnerships is organised by <b>buyer type</b> — university, school, "
          "government, donor, sponsor — because the buying behaviour of a "
          "ministry and a bank have nothing in common and the skills do not "
          "transfer. The Saudi country manager is the deliberate exception: in "
          "that market the relationship precedes the product line, so one person "
          "owns every engine."),

    ("h2", "Three layers that are not on the payroll"),
    ("p", "These carry almost all of the delivery, and they are the reason the "
          "establishment can be capped at all. Treating them as an afterthought "
          "would misread the company entirely: the certified network is the "
          "operating model, and the employees exist to define and defend it."),
    ("deflist", [
        ("The certified freelance facilitator pool",
         f"Every in-person engine runs on them — there are no employed "
         f"facilitators in this plan at all. Paid "
         f"{usd(UE['facilitation']/(BOOTCAMP_DAYS*2))} a day, each giving about "
         f"{pct(MD.FACILITATOR_UTILISATION)} of a delivery year, rising from "
         f"{LEV[0]['pool']} certified at the end of year one to "
         f"{LEV[2]['pool']} by year three. This keeps the largest variable cost "
         f"genuinely variable, which is what protects the business in a quarter "
         f"when a university postpones."),
        ("Certified delivery partner organisations",
         f"Youth NGOs, training providers and university innovation centres that "
         f"deliver StartPad cohorts under licence, keeping "
         f"{pct(MD.PARTNER_REVENUE_SHARE)} of the fee: "
         f"{LEV[0]['partners']} in year one, {LEV[2]['partners']} by year three, "
         f"each running roughly {MD.COHORTS_PER_PARTNER} cohorts a year. They "
         f"bring the geography and the youth pipeline StartPad would otherwise "
         f"have to build."),
        (f"{AMBASSADORS[1]} campus ambassadors, rising to {AMBASSADORS[3]}",
         "A stipend, free Pro access and standing — not a salary. Their most "
         "valuable output is intelligence about which institution is ready to "
         "buy, not registrations."),
    ]),

    ("h2", "Bought, not hired"),
    ("p", "The functions below are deliberately absent from the establishment. "
          "Each is listed with who supplies it and why buying beats hiring, "
          "because an organisation plan that simply omits finance and legal is "
          "not lean, it is incomplete."),
    ("table",
     ["Function", "Who supplies it", "Why it is bought"],
     [[fn, who, why] for fn, who, why in MD.OUTSOURCED],
     [4.2, 5.0, 6.4]),

    ("h2", "Hiring plan"),
    ("p", f"{HC['y1']} people in year one. Each row below states what the hire "
          f"unlocks and what was being carried by somebody else until it "
          f"arrived."),
    ("table",
     ["When", "Who", "Why then"],
     [["Before Q4 2026",
       "Chief executive, chief technology officer, Head of Curriculum and "
       "Certification",
       "Nothing can be certified or sold until the standard and the platform "
       "have owners. The CEO carries operations, finance and the quality gates "
       "from here until year four"],
      ["Q4 2026 · Land",
       "One senior full-stack engineer, Head of Partnerships — Egypt, Head of "
       "Growth and Content",
       "The admin workspace must exist before a cohort can run, the funded "
       "pilots need somebody to open the doors, and Mission Zero has to start "
       "recording in the quarter the first cohorts happen or there is nothing "
       "to record"],
      ["Year 2 · 3 added",
       "Country Manager — KSA (Riyadh), a second engineer, partner network "
       "manager",
       "A resident principal is the only way Saudi Arabia moves, and the "
       "partner network manager is the hire the entire operating model rests "
       "on — the first certified partners cannot be signed without one"],
      ["Year 3 · 3 added",
       "Head of Government, Initiatives and Donors; programme delivery "
       "coordinator; partnerships and bids associate",
       "Public money arrives on a cycle that had to be worked for two years "
       "before it paid, the delivery calendar outgrows the CEO, and bids start "
       "being lost for administrative reasons rather than commercial ones"],
      ["Year 4 · 4 added",
       "Chief operating officer, AI and data engineer, Head of Schools and "
       "Technical Education, second delivery coordinator",
       "The partner network passes what one person can hold, seat volume makes "
       "inference cost and assessment quality binding, and the school engine "
       "finally gets a dedicated owner"],
      ["Year 5 · 4 added",
       "Account manager — renewals, student success, product designer, "
       "bilingual curriculum producer",
       "The first roles that protect an existing book rather than win a new "
       "one. Renewal becomes the main revenue event and nobody owned it before"]],
     [2.4, 5.6, 8.6]),
    ("note", f"What is conspicuously absent: no facilitators, no finance "
             f"manager, no marketing team, no customer support function and no "
             f"regional offices. Delivery is certified rather than employed; "
             f"finance and legal are bought from firms; marketing is one person "
             f"and a podcast; support arrives in year five when sponsored-seat "
             f"volume finally justifies it. Each absence is a decision with a "
             f"stated cost, and the costs are gathered in the risk register "
             f"rather than scattered where they are easy to miss."),

    ("pb",),
    ("h2", "Role descriptions"),
    ("p", "Every role on the establishment, with the purpose it exists for, the "
          "responsibilities that belong to it and nobody else, and the one measure "
          "it is held to."),
    ("roles", ["Chief Executive Officer", "Chief Technology Officer",
               "Chief Operating Officer"]),
    ("roles", ["Senior full-stack engineer", "AI and data engineer",
               "Product designer"]),
    ("roles", ["Head of Curriculum and Certification", "Partner network manager",
               "Programme delivery coordinator",
               "Bilingual curriculum producer"]),
    ("roles", ["Head of Partnerships — Egypt", "Country Manager — KSA (Riyadh)",
               "Head of Government, Initiatives and Donors",
               "Partnerships and bids associate",
               "Head of Schools and Technical Education",
               "Account manager — renewals"]),
    ("roles", ["Head of Growth and Content", "Student success (bilingual)"]),

    ("h2", "Company culture"),
    ("deflist", [
        ("Delivery is the product",
         "The highest-status work in this company is running a cohort well. "
         "Everyone, including engineers and the CEO, spends time in a room with "
         "students each term."),
        ("Say the number",
         "Completion rates, declined cohorts, failed gates and missed SLAs are "
         "reported as they are. A plan this dependent on capacity cannot survive "
         "optimistic reporting."),
        ("Bilingual by default",
         "Internal documents that matter exist in both languages. A company that "
         "works in English and sells in Arabic eventually builds an English "
         "product."),
        ("Refuse gracefully",
         "Declining a cohort there is no certified pair for, or a contract with an "
         "outcome we cannot measure, is correct behaviour and is treated as such."),
    ]),

    ("h2", "Compensation structure"),
    ("deflist", [
        ("Cairo base, one Riyadh exception",
         f"Every role is priced at Cairo except one. The Saudi country manager is "
         f"priced at Riyadh and is {pct(5000*12*MD.RAMP[2]/HC['cost_y2'])} of "
         f"year-two payroll as a single person out of {HC['y2']}. Under-pricing "
         f"that role is the most common way a plan like this fails quietly, and "
         f"the alternative — covering Saudi Arabia from Cairo — fails loudly."),
        ("Founders below market",
         "The three leadership roles sit below what any of them could earn "
         "elsewhere. A deliberate runway decision, to be corrected at the next "
         "raise rather than left as a permanent feature."),
        ("Facilitators are a career, not a gig",
         "Certification, a rising day rate by tier, first refusal on lead-tier "
         "assignments and visible cohort outcomes are what stop the pool leaking "
         "to the consultancies competing for exactly these people. In a company "
         "with no employed facilitators at all, this is not a staff-welfare "
         "policy — it is supply-chain management for the only input that "
         "cannot be bought at short notice."),
        ("Sales paid on signing and on renewal",
         f"Commission at {pct(MD.B2B_COMMISSION)} of institutional revenue. The "
         f"The account manager added in year five is compensated on retained and "
         f"expanded revenue rather than on new logos, because renewal is where "
         f"this business lives."),
    ]),

    ("h2", "Advisors and governance"),
    ("p", "The board should carry four competencies the executive team does not "
          "have in depth: public-sector procurement in Egypt, Saudi institutional "
          "relationships, education policy and safeguarding, and scaled "
          "operations. An advisory bench of practising founders and "
          "entrepreneurship-centre directors doubles as the mentor network's "
          "senior tier and as reference customers."),

    ("h2", "Professional development"),
    ("bul", [
        "Facilitator tiering with a published progression path from certified to "
        "lead to certification trainer.",
        "Every employee observes at least one full cohort a year, whatever their "
        "function.",
        "Arabic and English language support where a role requires the second "
        "language.",
        "Curriculum and delivery staff rotate into partner train-the-trainer "
        "cohorts, which is the fastest way to find out what does not travel.",
    ]),
])

# =====================================================================
#  FINANCIAL PLAN
# =====================================================================
#
# Every figure in this part is read from the recalculated financial model
# through business_plan.finlink. Nothing here is typed, so the plan and the
# workbook cannot disagree.

FL = MD.FL
_HEAD = FL.headline()
_YL = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
_PACE = FL.pace()
_CASH = FL.cash_profile()
_WC = FL.working_capital()
_TAX = FL.tax_basis()
_EXP = FL.expense_lines()
_FUN = FL.funnel()
_CAPY = FL.capacity()
_FUND = MD.funding()


def _full(v):
    """A statement line, in full dollars. A balance sheet does not round."""
    return f"({abs(v):,.0f})" if v < 0 else f"{v:,.0f}"


# Lines on the three statements that are rates or multiples, not money. The
# statements used to print every one of them through the money formatter, so a
# gross margin of 58 per cent appeared as "$1".
_RATE_WORDS = ("margin", "growth", "ratio", "rate", "per cent", "check",
               "multiple", "times")


def _is_rate(label):
    low = label.lower()
    return any(w in low for w in _RATE_WORDS)


def _stmt_value(v, kind="money", year=None, label=""):
    """
    Format one statement cell by the kind the workbook says it is.

    Guessing from the label or the magnitude is how a count of 107 cohorts
    prints as $107 and a 58 per cent margin prints as $1. The number format
    on the cell is the answer, and finlink carries it through.
    """
    if isinstance(v, str):
        return v
    if label == "Annual growth" and year == 1:
        return ""          # there is no year nought to grow from
    if kind == "pct":
        return f"{v*100:,.1f}%"
    if kind == "mult":
        return f"{v:,.2f}x"
    if kind == "days":
        return f"{v:,.0f} days"
    if kind == "money":
        return _full(v)
    if kind == "money2":
        return f"({abs(v):,.2f})" if v < 0 else f"{v:,.2f}"
    if kind.startswith("num") and kind[3:].isdigit():
        return f"{v:,.{int(kind[3:])}f}"
    if abs(v - round(v)) < 1e-9:
        return f"{v:,.0f}"
    return f"{v:,.1f}"


def _row(label, values, fmt=money, indent=False):
    head = ("    " if indent else "") + label
    return [head] + [fmt(v) for v in values]


def _statement_rows(rows):
    out = []
    for r in rows:
        if r.get("heading") or r["values"] is None:
            out.append([r["label"]] + [""] * FL.YEARS)
        else:
            out.append([("    " if r["indent"] else "") + r["label"]]
                       + [_stmt_value(v, r.get("kind", "money"), i + 1,
                                      r["label"])
                          for i, v in enumerate(r["values"])])
    return out


_STMT_W = [4.6, 1.9, 1.9, 1.9, 1.9, 1.9]


section("Financial Plan", [
    ("lead", f"Five years, October 2026 to September 2031, in US dollars. "
             f"Revenue reaches {money(_HEAD[4]['revenue'])} in year five "
             f"against {money(_HEAD[4]['total_expense'])} of cost, and the "
             f"company turns a profit in year {MD.FL.first_profitable_year()}. "
             f"Year one spends {money(_HEAD[0]['total_expense'])}, which is "
             f"not a budget anybody set: it is what the activity plan, the "
             f"hiring plan and the cost drivers add up to."),

    ("h2", "How this model is built, and why that matters"),
    ("p", "An input is a decision or a rate: how many campus workshops the "
          "team runs, who is on the payroll and what they are paid, what a "
          "cohort is priced at, how long a buyer takes to sign, what share of "
          "proposals are won. Everything else is produced from those and is "
          "typed nowhere."),
    ("p", "There is no volume plan. A cohort exists in a given month because "
          "somebody ran a workshop earlier and a contract was won; cut the "
          "activity and the cohort disappears with it. The chain runs:"),
    ("num", [
        "<b>Activity</b> produces leads, online through cost per click and "
        "offline through workshops, events, partner sessions and direct "
        "outreach.",
        "<b>Leads</b> split across six buyer types, each with its own "
        "conversion and its own clock.",
        "<b>Meetings, proposals and wins</b> follow those conversion rates, "
        "with signature lagged by the buyer's sales cycle.",
        "<b>Mobilisation</b> lags again, between signature and the first "
        "delivery day.",
        "<b>The contract book</b> holds every live contract, and each one "
        "delivers a fixed number of units evenly across its life.",
        "<b>Revenue, cost, profit and tax</b> fall out of that volume.",
    ]),
    ("note", "The same discipline applies to cost. The year one total is an "
             "output of the Expenses sheet, not a ceiling typed into it. "
             "Doubling direct outreach in the model raises it immediately, "
             "which is the test that it is genuinely produced."),

    ("h2", "What the model opens on"),
    ("p", "Not forecasts. The position the company is actually in on day one, "
          "carried into the model as fact."),
    ("table",
     ["What is already true", "Value", "Note"],
     [[t["label"], (n(t["value"]) if t["unit"] in ("#", "EGP")
                    else money(t["value"])), t["note"]]
      for t in FL.traction()],
     [4.6, 2.0, 7.6]),
    ("p", "The five signed memoranda are not a special case in the "
          "arithmetic. They enter as contracts already signed, mobilising "
          "across the first three months, and run through the same contract "
          "book as anything the funnel wins later. That is why year one is "
          "produced rather than asserted."),

    ("pb",),
    ("h2", "Acquisition assumptions"),
    ("h3", "Online channels"),
    ("p", "Budget divided by cost per click gives paid clicks. Organic and "
          "referral traffic are taken as a stated share of paid, never "
          "assumed free. Then the first conversion stage, click to lead."),
    ("table",
     ["Channel", "Monthly budget, Y1", "Y5", "Cost per click",
      "Organic", "Referral", "Click to lead"],
     [[c["label"], usd(c["budget"][0]), usd(c["budget"][4]),
       f"${c['cpc']:,.2f}", pct(c["organic"]), pct(c["referral"]),
       pct(c["click_to_lead"], 1)] for c in FL.online_channels()],
     [3.5, 2.0, 1.6, 1.7, 1.6, 1.6, 1.8]),
    ("note", f"Online spend is sized as business to business inbound, not as "
             f"a consumer channel. At {usd(FL.book().assumption('Subscription, Pro, annual'))} "
             f"a year for Pro, a paid click cannot pay for itself, so most "
             f"paying accounts arrive free, from learners who sat in a cohort."),

    ("h3", "Offline activity, what the team actually does"),
    ("table",
     ["Activity", "Per month, Y1", "Y5", "Cost each", "Free sign ups",
      "Institutional leads"],
     [[c["label"], n(c["activities"][0], 1), n(c["activities"][4], 1),
       money(c["cost"]), n(c["signups"]), n(c["leads"], 1)]
      for c in FL.offline_channels()],
     [4.4, 1.9, 1.5, 1.7, 2.0, 2.3]),

    ("pb",),
    ("h3", "Who buys, and how long each kind takes"),
    ("p", "Complexity shows up twice: once as the sales cycle before "
          "signature, once as mobilisation between signature and the first "
          "delivery day."),
    ("table",
     ["Buyer type", "Share of leads", "Lead to meeting", "Meeting to proposal",
      "Proposal to win", "Sales cycle", "Mobilisation"],
     [[b["label"], pct(b["share"]), pct(b["lead_to_meeting"]),
       pct(b["meeting_to_proposal"]), pct(b["proposal_to_win"]),
       f"{b['cycle']} mo", f"{b['mobilisation']} mo"]
      for b in FL.buyers()],
     [3.5, 1.6, 1.7, 1.8, 1.6, 1.9, 2.1]),
    ("fig", "fin_funnel", "Year one, from marketing spend to signed "
                          "contracts, with the conversion at each stage."),

    ("pb",),
    ("h2", "Revenue assumptions"),
    ("h3", "What a won contract turns into"),
    ("p", "Each engine takes a share of one buyer type's contracts and "
          "delivers a fixed number of units evenly across a contract life. A "
          "contract is signed with a buyer, not with an engine, so a buyer's "
          "contracts are spread across whichever of that buyer's engines are "
          "open."),
    ("table",
     ["Engine", "Buyer", "Share", "Units per contract", "Contract life",
      "Unit"],
     [[e["label"], e["buyer"], pct(e["share"]), n(e["units"]),
       f"{e['life']} mo", e["unit"]] for e in FL.engines()],
     [4.2, 1.5, 1.4, 2.3, 1.8, 2.0]),

    ("h3", "Pricing"),
    ("table",
     ["Price", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
     [[p["label"]] + [usd(v) if v < 100 else money(v) for v in p["values"]]
      for p in FL.prices()],
     _STMT_W),
    ("note", f"The direct engine is priced for the market it is in: "
             f"{usd(FL.book().assumption('Subscription, Pro, annual'))} a year "
             f"for Pro and "
             f"{usd(FL.book().assumption('Subscription, Team, annual'))} for "
             f"Team. It is a reach product, not the business."),

    ("h3", "Delivery pace, and the year one ceiling"),
    ("p", f"A contract signed is not a contract delivered at full tilt. In "
          f"year one an institution is still localising the curriculum and "
          f"training its own faculty, so cohorts run at "
          f"{pct(_PACE[0])} of the rate the contract settles at, rising to "
          f"{pct(_PACE[1])} from year two. This is also where the year one "
          f"spending ceiling is held: it is a decision about how fast to go, "
          f"and year one lands at {money(_HEAD[0]['total_expense'])} because "
          f"of it."),
    ("fig", "fin_revenue_mix", "Revenue by family across five years, with the "
                               "total on each column."),

    ("pb",),
    ("h2", "Expense assumptions"),
    ("p", "Nothing here is a flat monthly figure chosen by eye. Every line "
          "has a driver: a desk per employee, facilitator days per cohort, "
          "inference per active learner, travel per head on the road."),
    ("h3", "Direct cost of delivery"),
    ("table",
     ["Direct cost line", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
     [_row(l["label"], l["values"], _full) for l in _EXP["direct"]]
     + [_row("Total direct cost", _EXP["direct_total"], _full)],
     _STMT_W),
    ("h3", "Operating cost"),
    ("table",
     ["Operating cost line", "Year 1", "Year 2", "Year 3", "Year 4",
      "Year 5"],
     [_row(l["label"], l["values"], _full) for l in _EXP["operating"]]
     + [_row("Total operating cost", _EXP["operating_total"], _full),
        _row("Total expenses, direct and operating", _EXP["total"], _full)],
     _STMT_W),
    ("fig", "fin_cost_stack", "What the money is spent on each year, against "
                              "the revenue it produces."),

    ("h2", "Working capital, funding and tax"),
    ("table",
     ["Basis", "Value", "Why it is set there"],
     [["Days sales outstanding, institutional", f"{_WC['dso']:.0f} days",
       "Universities and ministries pay slowly. This is the largest single "
       "cash risk in the model"],
      ["Days sales outstanding, subscriptions", f"{_WC['dso_sub']:.0f} days",
       "Card payment, collected on the day"],
      ["Days payable outstanding", f"{_WC['dpo']:.0f} days",
       "What suppliers and freelance facilitators are paid on"],
      ["Accrued payroll", f"{_WC['accrued']:.0f} days",
       "Salaries earned but not yet paid at a month end"],
      ["Invoiced in advance", pct(_WC["advance"]),
       "The share of institutional contracts billed up front, which creates "
       "deferred revenue"],
      ["Seed round", money(_CASH["seed"]),
       f"Landing in month {_CASH['seed_month']}, sized on the cash trough "
       f"rather than on a round number"],
      ["Corporate income tax", pct(_TAX["rate"]),
       f"Egyptian corporate income tax, paid in month {_TAX['month']} of the "
       f"following year, after losses carried forward"]],
     [4.4, 2.2, 7.6]),
    ("fig", "fin_cash", "Cash month by month across sixty months, with the "
                        "trough marked."),
    ("note", f"The trough is {money(_CASH['trough'])} in month "
             f"{_CASH['trough_month']}, against a stated minimum buffer of "
             f"{money(_CASH['buffer'])}. The round is sized on that trough: "
             f"the ask is {money(_FUND['rounded'])}."),

    ("pb",),
    ("h2", "Income statement"),
    ("p", "Five years to 30 September. Every line is a formula over the "
          "assumptions above."),
    ("table",
     ["Income statement"] + _YL,
     _statement_rows(FL.income_statement()),
     _STMT_W),

    ("pb",),
    ("h2", "Balance sheet"),
    ("p", "At each year end. The check line is the test that the statement "
          "balances, and it reads nil in every column."),
    ("table",
     ["Balance sheet", "At inception"] + _YL,
     [[r["label"]] + ([""] * (FL.YEARS + 1) if r.get("heading")
                      else [("" if r["opening"] is None
                             else _stmt_value(r["opening"], r.get("kind")))]
                      + [_stmt_value(v, r.get("kind"), i + 1, r["label"])
                         for i, v in enumerate(r["values"])])
      for r in FL.balance_sheet()],
     [3.9, 1.7, 1.7, 1.7, 1.7, 1.7, 1.8]),

    ("pb",),
    ("h2", "Cash flow statement"),
    ("p", "Indirect method, built monthly and summed to the year. Cash moves "
          "only through working capital, capital expenditure and funding, so "
          "the closing balance reconciles to the balance sheet by "
          "construction."),
    ("table",
     ["Cash flow"] + _YL,
     _statement_rows(FL.cash_flow()),
     _STMT_W),

    ("pb",),
    ("h2", "What the numbers say"),
    ("table",
     ["Indicator"] + _YL,
     [[i["label"]] + [_stmt_value(v, i.get("kind", "num"), None, i["label"])
                      for v in i["values"]] for i in FL.indicators()],
     _STMT_W),
    ("h3", "Capacity, checked rather than assumed"),
    ("p", "The plan is only credible if the people exist to run the activity "
          "and the network exists to deliver what is sold. Both are tested "
          "every month in the model, and neither is ever exceeded."),
    ("table",
     ["Capacity"] + _YL,
     [["Activity utilisation"] + [pct(v) for v in _CAPY["activity_use"]],
      ["Meeting utilisation"] + [pct(v) for v in _CAPY["meeting_use"]],
      ["Certified facilitators in the pool"]
      + [n(v) for v in _CAPY["facilitators"]],
      ["Certified delivery partners"] + [n(v) for v in _CAPY["partners"]],
      ["Contracts live at year end"] + [n(v, 1) for v in _CAPY["live"]],
      ["Activity asked for beyond capacity"]
      + [n(v, 2) for v in _CAPY["activity_short"]],
      ["Meetings asked for beyond capacity"]
      + [n(v, 2) for v in _CAPY["meeting_short"]]],
     _STMT_W),
    ("note", "The last two rows must read nil in every month of every year, "
             "and do. If either moved off nil the plan would be selling work "
             "nobody is free to do."),

    ("h2", "How the model is checked"),
    ("p", "A model can contain nothing but formulas and still be wrong, if "
          "those formulas point at the wrong cells. Three independent checks "
          "run against the workbook, and all three have to pass before any "
          "figure in this part is quoted."),
    ("deflist", [
        ("No static values",
         "Every cell is audited for a number sitting outside a designated "
         "input, and for any number buried inside a formula that is not "
         "structural. Both report zero."),
        ("Every figure recomputes",
         "The whole acquisition engine is rebuilt a second time, in Python, "
         "from the input cells read back out of the workbook, and compared "
         "month by month: leads, meetings, proposals, contracts signed after "
         "each buyer's cycle, contracts mobilised after each lag, the live "
         "contract book, and the volume each engine delivers. Then every "
         "revenue line against volume times price, cost against its drivers, "
         "and the balance sheet and cash flow identities."),
        ("The whole model moves",
         "Fourteen inputs are changed at once and the workbook recalculated, "
         "to confirm that outputs across every calculating sheet respond and "
         "that the balance sheet still checks to nil."),
    ]),

    ("h2", "What still needs a decision"),
    ("bul", [
        f"<b>The cash trough.</b> {money(_CASH['trough'])} in month "
        f"{_CASH['trough_month']} is thin against a "
        f"{money(_CASH['buffer'])} buffer. A larger round, or pulling "
        f"institutional collection in from {_WC['dso']:.0f} days, closes it. "
        f"Both are inputs.",
        "<b>The sales cycles.</b> Every buyer type is currently modelled at "
        "one month from proposal to signature. That is fast for a ministry "
        "or a donor, and it is the assumption most likely to be challenged "
        "in a funding conversation. Lengthening it pushes revenue right "
        "without changing anything else.",
        "<b>Exit and valuation inputs.</b> Pre-money at each round, the "
        "dilution assumed from later rounds and the exit multiples are "
        "negotiating positions rather than facts, which is why they are "
        "inputs rather than results.",
    ]),
])


# =====================================================================
section("Strategic Analysis", [
    ("lead", "An honest view of where the company is strong, where it is exposed, "
             "and what it will do when something goes wrong."),

    ("h2", "SWOT analysis"),
    ("fig", "swot", "Strengths, weaknesses, opportunities and threats."),

    ("h2", "PESTLE analysis"),
    ("fig", "pestle", "The external environment across six dimensions."),

    ("h2", "Risk analysis and mitigation"),
    ("table",
     ["Risk", "What it looks like early", "Mitigation"],
     [["Facilitator capacity does not materialise",
       "Certification slips, or the pool leaks to consultancies paying more a day",
       "Certification starts in the Land quarter, a term ahead of need; a tiered "
       "career with a rising day rate; the plan is cut to capacity rather than "
       "the reverse"],
      ["University procurement is slower than planned",
       "Pilots run but contracts sit unsigned through the Prove quarter",
       "One contract covering all three layers; free pilots that make the report "
       "the sales document; competitions enter through Door 04 with a sponsor "
       "paying; Saudi revenue lands from Q4"],
      ["The school variant does not transfer",
       "School cohorts miss the completion gate, or safeguarding proves "
       "prohibitive",
       "A separate curriculum variant rather than a shortened one, and a "
       "separately certified facilitator tier for school work; safeguarding "
       "carried as a standing cost from before the first school visit; the "
       "engine is gated to Expand so there is time to find out"],
      ["Key-person dependency on the chief executive",
       "Operations, finance, the quality gates and every senior institutional "
       "relationship sit with one person until the COO arrives in year four",
       "The single largest structural risk created by the headcount cap, and "
       "accepted knowingly. Mitigated by making the quality gates documented and "
       "auditable rather than judgement-based, by the partner network manager "
       "owning the capacity forecast independently from year two, and by the "
       "COO being a dated commitment in the hiring plan rather than a "
       "contingency. If institutional volume arrives earlier than planned, that "
       "hire moves forward — it is the one line in the establishment the plan "
       "would willingly bring forward at the expense of another"],
      ["The certified network dilutes the standard",
       "Cohort scores drift at partner-delivered sites while StartPad-run "
       "cohorts hold, or a partner quietly sends uncertified facilitators",
       "Sample audits every term; the pass mark owned by the Head of Curriculum "
       "and by nobody with a revenue target; licence withdrawal used at least "
       "once early, visibly, so that the network understands the audit is real"],
      ["No national initiative partnership lands",
       "Enthusiastic meetings, no budget line, repeated deferral",
       f"Engine 3 is {share(ENGINE_NAMES[2])} of year-one revenue, so year one "
       f"survives without it; two partnerships pursued in parallel; the year-three "
       f"plan sits inside {pct(FILTER_INITIATIVE_SHARE)} of addressable seats"],
      ["Sponsor and CSR budgets move",
       "Competition and corporate conversations stall simultaneously — usually a "
       "macro signal",
       "Those two engines together are "
       f"{pct((R1['lines'][ENGINE_NAMES[4]] + R1['lines'][ENGINE_NAMES[5]])/R1['total'])} "
       "of year one; the education and public families carry the plan without them"],
      ["Currency and macro shock",
       "EGP devaluation repricing costs against institutional budgets",
       "Most costs are EGP and institutional pricing can be set in EGP with a USD "
       "reference; devaluation lowers the cost base faster than local willingness "
       "to pay"],
      ["Key-person concentration",
       "The CEO personally opens every cohort and carries every senior "
       "relationship",
       "Day 01 onboarding is handed to certified facilitators before the Expand "
       "quarter; four buyer-type heads hold relationships independently"],
      ["A safeguarding incident",
       "Any incident involving a minor in a school cohort",
       "Vetting, training, consent records and a written incident procedure "
       "before the first school cohort; this is a licence-to-operate risk, not a "
       "reputational one"]],
     [3.2, 4.8, 5.6]),

    ("h2", "Contingency planning"),
    ("table",
     ["If this happens", "Then"],
     [["Certification is behind at the end of any quarter",
       "Cut the next quarter's cohort plan to the certified pairs actually "
       "available and reallocate sales effort to seat, competition and partner "
       "engines, which do not consume facilitator capacity"],
      ["The automatic cohort report slips past Q1 2027",
       "Produce reports manually for the pilot institutions only, cap new cohort "
       "sales at the manual capacity, and treat the report as the single highest "
       "engineering priority"],
      ["No paid Egyptian cohort by the end of Q1 2027",
       "Treat the pilot proposition as unproven: run two further pilots at "
       "different institution types before scaling the sales team, and lean on "
       "Saudi partner revenue meanwhile"],
      ["A national programme contracts a competitor exclusively",
       "Redirect Engine 3 effort to governorate-level and ministry-of-education "
       "routes, and to the Saudi equivalents, rather than competing for the same "
       "central contract"],
      ["School safeguarding approval proves prohibitive in one market",
       "Run Engine 2 in the other market first and serve the blocked market "
       "through technical institutes, which are post-compulsory"],
      ["Demand exceeds capacity materially",
       "Raise price before raising volume, and shift the mix toward "
       "train-the-trainer so partners absorb the delivery"]],
     [5.0, 11.6]),
])

# =====================================================================
section("Appendix", [
    ("lead", "Every figure behind the plan, so a reader can argue with the inputs "
             "rather than the conclusions."),

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
      ["Egypt technical secondary students", n(TVET_STUDENTS["Egypt"]),
       "CAPMAS 2021/22, reported via Statista. The Ministry reported 595,848 "
       "passing first-term technical diploma exams in 2024/25 at a 70.47% pass "
       "rate, implying roughly 845,000 sitting"],
      ["Saudi TVTC trainees, 2024", n(TVET_STUDENTS["KSA"]),
       "TVTC — 336,150 trainees across 314 institutions, 98,716 graduates"],
      ["Egypt public colleges", "551", "CAPMAS — 28 universities, 551 colleges"],
      ["MENA startup funding, 2025", "$7.5bn across 647 deals", "Wamda full-year"],
      ["Egypt startup funding, 2025", "$263m across 89 deals", "Wamda"],
      ["Saudi startup funding, 2025", "$5.0bn across 211 deals", "Wamda"],
      ["One Million Entrepreneurs registrations", "~18,000",
       "Egyptian Ministry of Planning"]],
     [4.6, 2.6, 7.0]),

    ("h2", "Our estimates"),
    ("p", "These are not published figures. Each is derived, the derivation is "
          "stated, and each is a number a reader may reasonably dispute."),
    ("table",
     ["Estimate", "Value", "How it was derived"],
     [["Saudi graduates a year", n(ANNUAL_GRADUATES["KSA"]),
       "Enrolment over a four-year degree, discounted 25% for longer programmes "
       "and attrition"],
      ["Secondary students, final two years", n(M["secondary"]),
       "Egypt derived from total secondary less the technical stream; KSA from "
       "population and enrolment ratios"],
      ["Micro and small enterprise owners", n(M["msme"]),
       "Widely cited formal and informal MSME counts in both markets"],
      ["University buying units", n(M["units"]),
       "551 CAPMAS public colleges plus ~400 Egyptian private faculties; ~45 "
       "Saudi universities at ~12 colleges each plus 24 private colleges"],
      ["Schools with a budget", n(M["schools"]),
       "Private, international, national and applied-technology schools in both "
       "markets"],
      ["Egyptian technical institutions", n(TVET_INSTITUTIONS["Egypt"]),
       "Technical secondary schools; the Saudi figure of 314 is published by TVTC"],
      ["Initiative seats a year", n(INITIATIVE_SEATS_PER_YEAR),
       "Addressable at steady state across both markets, far below the stated "
       "targets which total several million"],
      ["NGOs and donors with a budget", n(NGOS),
       "Donors, foundations, bank foundations and INGO country offices with a "
       "youth employability mandate"],
      ["Competitions a year", n(COMPETITIONS_PER_YEAR),
       "Universities, schools, banks, telcos, ministries and foundations"],
      ["Large corporates", n(CORPORATES),
       "With a CSR, innovation or youth budget line"]],
     [4.0, 2.2, 8.0]),

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
       f"{pct(plan('initiative_seats', 3)/INITIATIVE_SEATS_PER_YEAR)} of "
       f"addressable, inside this ceiling"],
      ["University cohorts per pair per year", n(COHORTS_PER_PAIR["university"]),
       "One per two weeks, with slack for travel, preparation and campus holidays"],
      ["School cohorts per pair per year", n(COHORTS_PER_PAIR["school"]),
       "A shorter format fits more into the same year"],
      ["Technical cohorts per pair per year", n(COHORTS_PER_PAIR["tvet"]),
       "Five days, between the other two"],
      ["Facilitator day rate", usd(UE["facilitation"] / (BOOTCAMP_DAYS * 2)),
       "Certified freelance rate, Egypt"],
      ["Subscriber life", "1.6 years",
       "A founder who finishes has no reason to renew a third year; one who "
       "stalls churns inside the first"],
      ["Institutional commission", pct(MD.B2B_COMMISSION),
       "Institutional business is sold by people, and people on a number are paid "
       "on it"]],
     [4.2, 2.2, 7.8]),

    ("h2", "What this plan does not claim"),
    ("bul", [
        "It does not claim an outcome number. StartPad records mission progress, "
        "evidence and review scores. It does not certify that a venture will "
        "succeed, and no partnership should be contracted against a metric the "
        "product cannot measure.",
        "The financial plan in this document is produced by the financial "
        "model, not written beside it. Every figure in it is read from the "
        "recalculated workbook, so the two cannot disagree. What the model "
        "cannot do is make its inputs true: the sales cycles, the conversion "
        "rates and the prices are decisions and estimates, not observations.",
        "Subscription conversion rates and pipeline conversion rates are "
        "modelled, not measured. Both will be replaced with observed figures "
        "after the first cohort quarter.",
        "Competition, corporate and NGO pricing is benchmarked against comparable "
        "sponsorship and contract spend rather than against signed StartPad deals, "
        "because there are none yet. These are the prices most likely to move.",
        "Several population figures are derived rather than published, and are "
        "marked as such above. Where a published figure exists we use it even "
        "when it is older than we would like.",
    ]),
])
