"""
The StartPad business plan, as arithmetic.

Every number in the business plan document is computed here, from assumptions held
in one place, so a figure in a chart cannot drift away from the sentence beside it.
Nothing in the document is typed as a literal; the builder reads this module.

Where a figure comes from outside, the source is named beside it. Where it is an
assumption we chose, it is marked ASSUMPTION and the reasoning is given, because an
assumption a reader cannot argue with is an assumption a reader cannot trust.

The shape of this business
--------------------------
StartPad sells readiness to organisations that need a group of young people
prepared. There are eight such engines in four families:

    EDUCATION       1  University cohorts and faculty licences
                    2  Schools and technical education
                    7  Programme and incubator seats

    PUBLIC          3  National initiatives and government programmes
                    4  NGO, donor and foundation programmes

    COMMERCIAL      5  Sponsored competitions
                    6  Corporate and CSR programmes

    DIRECT          8  Founder subscriptions

The eighth is the smallest and is a consequence of the other seven rather than a
channel in its own right: a young person who completed ten missions inside a camp,
a competition or a sponsored cohort is the one who pays to finish the rest.

Nothing starts on day one
-------------------------
Engines activate on a gate, not a date. A faculty licence cannot be sold before two
cohorts have run at that faculty; a ministry will not contract a platform that
cannot show a cohort report; a school programme needs a school variant of the
curriculum that does not exist in the Land quarter. The quarterly plan below is the
source of truth and the annual figures are summed from it, so the ramp cannot be
quietly assumed away.

Currency is USD throughout.
"""

# =====================================================================
#  PART 1 — THE POPULATION (external figures where they exist)
# =====================================================================

# --- Higher education -------------------------------------------------
# Egypt: CAPMAS annual bulletin 2024/25 — 3.9m enrolled in higher education.
# KSA:   UNESCO UIS tertiary enrolment 2022 — 1.57m.
HE_STUDENTS = {"Egypt": 3_900_000, "KSA": 1_600_000}

# Egypt: 547,200 graduated in 2023 (CAPMAS via Ahram Online).
# KSA: derived from enrolment over a four-year degree, discounted 25%. ASSUMPTION.
ANNUAL_GRADUATES = {"Egypt": 547_200, "KSA": 300_000}
GRADUATE_WINDOW_YEARS = 3

# --- Technical and vocational ----------------------------------------
# Egypt technical secondary: ~2.2m (CAPMAS, 2021/22, reported via Statista). The
# Ministry reported 595,848 students passing first-term technical diploma exams in
# 2024/25 at a 70.47% pass rate, implying ~845,000 sitting — a very large annual
# cohort and the reason this segment matters.
# KSA: TVTC reported 336,150 trainees across 314 institutions in 2024.
TVET_STUDENTS = {"Egypt": 2_200_000, "KSA": 336_000}
TVET_INSTITUTIONS = {"Egypt": 2_000, "KSA": 314}   # Egypt count is an ASSUMPTION

# --- General secondary, the final two years ---------------------------
# The years where a venture-building elective or a capstone actually fits.
# Egypt derived from ~4m total secondary less the technical stream; KSA derived
# from population and enrolment ratios. Both ASSUMPTION.
SECONDARY_STUDENTS = {"Egypt": 1_200_000, "KSA": 1_000_000}

# Secondary schools with a budget and the autonomy to spend it: private,
# international, national and applied-technology schools. A government school on a
# fixed ministry budget is reached through Engine 3, not sold to directly.
SCHOOLS_WITH_BUDGET = {"Egypt": 2_500, "KSA": 1_200}   # ASSUMPTION

# --- Founders outside education --------------------------------------
# Micro and small enterprise owners, informal-sector operators formalising under
# Egypt's Law 6 of 2025 tax incentives, and first-time founders who never went to
# university. Reached through banks, NGOs and government programmes rather than
# through a campus. ASSUMPTION on both counts.
MSME_OWNERS = {"Egypt": 3_700_000, "KSA": 600_000}

# --- Institutional buying units --------------------------------------
# Three of the four university doors sit at college level, and one university
# routinely runs several unrelated cohorts. Egypt: 551 public colleges (CAPMAS)
# plus ~400 private and national faculties. KSA: ~45 universities at ~12 colleges
# each plus 24 private colleges.
BUYING_UNITS = {"Egypt": 951, "KSA": 564}

# Incubators, accelerators and startup programmes that select applicants.
PROGRAMMES = 250

# Large and mid-size corporates with a CSR, innovation or youth budget line.
CORPORATES = 1_400

# NGOs, donors, foundations and development agencies with a youth employability or
# entrepreneurship mandate and a budget: international donors, local foundations,
# bank foundations and INGO country offices across both markets. ASSUMPTION.
NGOS = 1_800

# Youth and student entrepreneurship competitions run each year across both
# markets by universities, schools, banks, telcos, ministries and foundations.
COMPETITIONS_PER_YEAR = 1_100

# National initiative seats a year. Egypt alone has three public programmes with
# million-scale targets (One Million Entrepreneurs under Rowad 2030; 1 Million
# Qualified Innovators with UNDP, MBRF and ICESCO; One Million International
# Licences with Cisco), plus MSMEDA's governorate programme, the technical
# education reform and roughly 4,500 youth centres used as delivery sites. Saudi
# equivalents sit with Monsha'at, the Misk Foundation and TVTC. This is addressable
# seats at steady state across both markets, far below the stated targets.
INITIATIVE_SEATS_PER_YEAR = 1_200_000   # ASSUMPTION


# =====================================================================
#  PART 2 — PRICING (assumptions, with reasoning)
# =====================================================================

# --- Engine 1: universities ------------------------------------------
PRICE_COHORT = 7_500.0            # all-in: 6 bootcamp days, seats, judging, report
COHORT_SIZE = 25
PRICE_FACULTY_LICENCE = 25_000.0
UNIT_ANNUAL_SPEND = 18_000.0      # blended, for sizing without double-counting

# --- Engine 2: schools and technical education -----------------------
# A shorter, younger variant: four days for a school, five for a technical
# institute, larger groups, and an employability frame rather than an investment
# frame. Priced against a school's activity budget, not a university's.
PRICE_SCHOOL_COHORT = {1: 4_500.0, 2: 4_700.0, 3: 4_900.0}
SCHOOL_COHORT_SIZE = 30
SCHOOL_DAYS = 4
PRICE_SCHOOL_LICENCE = 12_000.0
PRICE_TVET_COHORT = {1: 5_000.0, 2: 5_200.0, 3: 5_400.0}
TVET_DAYS = 5
SCHOOL_UNIT_ANNUAL_SPEND = 9_000.0
TVET_UNIT_ANNUAL_SPEND = 11_000.0

# --- Engine 3: national initiatives ----------------------------------
PRICE_INITIATIVE_SEAT = {1: 22.0, 2: 20.0, 3: 18.0}
PRICE_TOT_COHORT = {1: 12_000.0, 2: 12_500.0, 3: 13_000.0}

# --- Engine 4: NGO, donor and foundation programmes ------------------
# Grant-funded, designed around the donor's logframe, delivered as cohorts with
# per-participant evidence. Larger than a university cohort because it carries
# facilitation, reporting and usually several sites.
PRICE_NGO_PROGRAMME = {1: 35_000.0, 2: 38_000.0, 3: 40_000.0}

# --- Engine 5: sponsored competitions --------------------------------
PRICE_COMPETITION = {1: 28_000.0, 2: 32_000.0, 3: 36_000.0}

# --- Engine 6: corporate and CSR -------------------------------------
PRICE_CORPORATE = {1: 45_000.0, 2: 55_000.0, 3: 60_000.0}

# --- Engine 7: programme and incubator seats -------------------------
PRICE_SEAT = {1: 40.0, 2: 42.0, 3: 44.0}

# --- Engine 8: founder subscriptions ---------------------------------
PRICE_PRO_YEAR = 59.0
PRICE_TEAM_YEAR = 179.0
MIX_PRO, MIX_TEAM = 0.75, 0.25
B2C_LIFE_YEARS = 1.6
B2C_GROSS_MARGIN = 0.88
B2C_RECOGNITION = {1: 0.50, 2: 0.78, 3: 0.82}


# =====================================================================
#  PART 3 — SAM FILTERS (assumptions, with reasoning)
# =====================================================================

FILTER_FACULTY_FIT = 0.35        # faculties where venture-building fits
FILTER_SCHOOL_FIT = 0.60         # schools with budget AND curriculum room
FILTER_TVET_FIT = 0.60           # technical institutes with an employability brief
FILTER_REACHABLE = {"Egypt": 0.70, "KSA": 0.80}
FILTER_SCHOOL_REACHABLE = 0.75   # schools cluster in the cities we serve
FILTER_INITIATIVE_SHARE = 0.25   # what one provider could serve of national seats
FILTER_NGO_FIT = 0.40            # with a live youth employability budget
FILTER_COMPETITION_FIT = 0.45
FILTER_PROGRAMME_FIT = 0.60
FILTER_CORPORATE_FIT = 0.20

# Share who would ever self-pay for a subscription at this price. Split, because a
# university student or an MSME owner might; a sixteen-year-old in a government
# technical school will not, and pretending otherwise is how a plan ends up built
# on its least convertible number.
FILTER_SELF_PAY_ADULT = 0.06
FILTER_SELF_PAY_YOUTH = 0.01

NGO_PROGRAMMES_PER_ORG = 0.40    # a year
CORPORATE_PROGRAMMES_PER_ORG = 0.30


# =====================================================================
#  PART 4 — THE QUARTERLY PLAN
# =====================================================================
#
# Twelve quarters. Everything downstream is summed from here, so a ramp cannot be
# assumed away and an engine cannot earn revenue before its gate opens.

QUARTERS = [
    ("Q4 2026", "Land",   1), ("Q1 2027", "Prove",  1),
    ("Q2 2027", "Expand", 1), ("Q3 2027", "Scale",  1),
    ("Q4 2027", "Widen",  2), ("Q1 2028", "Widen",  2),
    ("Q2 2028", "Deepen", 2), ("Q3 2028", "Deepen", 2),
    ("Q4 2028", "Scale",  3), ("Q1 2029", "Scale",  3),
    ("Q2 2029", "Lead",   3), ("Q3 2029", "Lead",   3),
]

QUARTERLY = {
    # --- Engine 1: universities
    "uni_cohorts_eg":  [0, 6, 12, 16,  20, 26, 30, 34,  48, 56, 64, 72],
    "uni_cohorts_ksa": [2, 4,  7,  9,   9, 10, 10, 11,  18, 20, 21, 21],
    "uni_pilots":      [4, 2,  1,  1,   1,  1,  1,  1,   1,  1,  1,  1],
    "uni_licences":    [0, 0,  0,  2,   1,  2,  2,  3,   4,  5,  6,  7],

    # --- Engine 2: schools and technical education
    "school_cohorts":  [0, 0,  6, 14,  22, 30, 38, 46,  55, 70, 85, 90],
    "school_licences": [0, 0,  0,  1,   2,  3,  4,  5,   8, 10, 12, 14],
    "tvet_cohorts":    [0, 0,  0,  5,  10, 14, 18, 22,  28, 34, 38, 40],

    # --- Engine 3: national initiatives
    "initiative_seats": [0, 0, 0, 2_500,
                         4_000, 6_000, 8_000, 10_000,
                         18_000, 24_000, 28_000, 30_000],
    "tot_cohorts":     [0, 0,  0,  2,   2,  2,  3,  4,   7,  8,  9, 10],

    # --- Engine 4: NGO, donor and foundation programmes
    "ngo_programmes":  [0, 0,  1,  2,   3,  4,  5,  6,   7,  8,  9, 10],

    # --- Engine 5: sponsored competitions
    "competitions":    [0, 1,  1,  2,   2,  3,  4,  5,   7,  8,  9, 10],

    # --- Engine 6: corporate and CSR
    "corporates":      [0, 0,  0,  1,   1,  1,  1,  2,   3,  3,  4,  4],

    # --- Engine 7: programme and incubator seats (new partners signed)
    "programmes":      [0, 3,  5,  6,   8,  9, 11, 12,  20, 22, 24, 24],
    "seats_each":      [60, 60, 60, 60, 75, 75, 75, 75, 85, 85, 85, 85],
}

# Each engine's first revenue quarter, and what must be true before it opens.
# The index is into QUARTERS; a plan that puts revenue earlier than its gate is a
# plan that has not been thought through.
ENGINE_GATES = [
    ("University cohorts", 0,
     "Four certified facilitators, the curriculum in both languages, and the "
     "programme admin workspace",
     "KSA pays from the first quarter through programme partners; Egypt runs free "
     "pilots in the Land quarter and sells from the Prove quarter on their reports"),
    ("Faculty licences", 3,
     "Two completed cohorts at the same institution, and an automatic cohort report",
     "A dean buys a faculty-wide licence off two reports, not off a pitch. The "
     "earliest an institution that piloted in Q4 2026 can reach that is Q3 2027"),
    ("School and technical cohorts", 2,
     "A school variant of the curriculum — four days, larger groups, an "
     "employability frame — plus safeguarding and parental consent",
     "The university format does not transfer to sixteen-year-olds. Building the "
     "variant is a Prove-quarter job; selling it starts in Expand"),
    ("Sponsored competitions", 1,
     "A competition entry and qualification flow on the platform, and one sponsor "
     "willing to go first",
     "The first competition can run with manual judging support; the platform flow "
     "lands in the Prove quarter and the format scales from Expand"),
    ("NGO and donor programmes", 2,
     "A cohort report from a comparable pilot, and the ability to report against "
     "a donor logframe",
     "Grant cycles are long but shorter than government. A programme designed in "
     "the Prove quarter is contracted in Expand"),
    ("National initiative seats", 3,
     "Cohort reports at volume, bulk seat provisioning, and a train-the-trainer "
     "curriculum",
     "The longest cycle of any engine — nine to fifteen months from first meeting "
     "to a signed seat order. Conversations open in the Land quarter and the "
     "first pilot seats land in Scale"),
    ("Corporate and CSR programmes", 3,
     "A reference programme and a case study a CSR committee can circulate",
     "A corporate budget is set annually. The first deal is a reference, not "
     "revenue, and it lands late in year one"),
    ("Programme and incubator seats", 1,
     "The platform-only seat product and partner onboarding",
     "Small deals with short cycles, available as soon as there is something to "
     "onboard a partner onto"),
    ("Founder subscriptions", 1,
     "Students who have completed missions inside a paid engine",
     "Subscriptions lag the engines that produce them by a quarter — a student "
     "who finishes a camp in the Prove quarter subscribes in Expand"),
]


# ------------------------------------------------- founder subscriptions
#
# Subscriptions are modelled as downstream of the institutional engines, not as a
# consumer funnel. Each row is a population StartPad already reached through an
# organisation, and the rate at which that population then pays for itself.
#
# (source, Y1 reached, Y2, Y3, conversion to paid)
SUBSCRIPTION_SOURCES = [
    ("Students from university cohorts",        1_400,  3_750,  8_000, 0.120),
    ("School and technical education students", 1_210,  9_380, 22_250, 0.020),
    ("Entrants in sponsored competitions",      2_800,  9_800, 23_800, 0.060),
    ("Participants on sponsored seats",         2_500, 28_000, 100_000, 0.030),
    ("NGO and corporate programme participants",  960,  6_600, 14_800, 0.045),
    ("Programme and incubator participants",      840,  3_000,  7_650, 0.055),
    ("Organic — content, community, word of mouth", 4_500, 14_000, 34_000, 0.050),
]


# =====================================================================
#  PART 5 — DIRECT COST OF DELIVERY
# =====================================================================

FACILITATORS_PER_COHORT = 2
BOOTCAMP_DAYS = 6
FACILITATOR_DAY_RATE = 120.0
COHORT_MATERIALS = 450.0
COHORT_BAZAAR = 300.0

SCHOOL_MATERIALS = 350.0
SCHOOL_SHOWCASE = 200.0
TVET_MATERIALS = 380.0
TVET_SHOWCASE = 220.0

# A facilitator pair runs one university cohort per two weeks and needs slack for
# travel, preparation and the weeks a campus is closed. Shorter formats fit more
# into the same year.
COHORTS_PER_PAIR = {"university": 18, "school": 26, "tvet": 22}

TOT_DIRECT = 3_200.0
NGO_DIRECT = 9_000.0
COMPETITION_DIRECT = 11_000.0
CORPORATE_DIRECT = 13_000.0
# Supporting a sponsored seat is not just inference. At governorate scale it is
# provisioning, a bilingual support queue, partner reporting and the reissue of
# accounts that never activated. Costing it at inference alone is the most common
# way a seat business looks more profitable than it is.
INITIATIVE_SEAT_DIRECT = 5.20
SEAT_DIRECT = 4.60


# =====================================================================
#  PART 6 — HEADCOUNT (the HR plan, costed)
# =====================================================================
#
# (function, role, Y1 count, monthly fully-loaded USD, Y2 count, Y3 count)

# The establishment is deliberately minimal. Three principles hold it down:
# employ the people who define the standard and contract the people who deliver
# it; merge functions until a role is genuinely full-time; and let partners and
# certified freelancers absorb volume rather than headcount. Every in-person
# engine runs on a certified freelance pool, so cohort growth does not become
# payroll growth.
ROLES = [
    ("Leadership", "Chief Executive Officer", 1, 3_000, 1, 1),
    ("Leadership", "Chief Operating Officer", 1, 3_000, 1, 1),
    ("Leadership", "Chief Technology Officer", 1, 3_000, 1, 1),

    ("Product and Engineering", "Senior full-stack engineer", 2, 2_400, 3, 6),
    ("Product and Engineering", "AI and data engineer", 0, 2_800, 1, 2),
    ("Product and Engineering", "Product designer", 0, 1_800, 0, 1),

    ("Curriculum and Delivery", "Head of Curriculum and Certification", 1, 2_400, 1, 1),
    ("Curriculum and Delivery", "Bilingual curriculum producer", 1, 1_300, 2, 4),
    ("Curriculum and Delivery", "Lead facilitator", 2, 1_500, 5, 12),
    ("Curriculum and Delivery", "Programme delivery coordinator", 0, 1_500, 1, 3),

    ("Institutional Sales", "Head of Partnerships — Egypt", 1, 2_200, 1, 1),
    ("Institutional Sales", "Head of Schools and Technical Education", 0, 2_200, 1, 1),
    ("Institutional Sales", "Head of Government, Initiatives and Donors", 0, 2_600, 1, 2),
    ("Institutional Sales", "Country Manager — KSA (Riyadh)", 1, 5_000, 1, 2),
    ("Institutional Sales", "Partnerships associate", 0, 1_200, 2, 5),
    ("Institutional Sales", "Account manager — renewals", 0, 1_600, 0, 3),

    ("Growth and Operations", "Growth and community manager", 1, 1_800, 1, 1),
    ("Growth and Operations", "Ambassador and events coordinator", 0, 1_200, 1, 2),
    ("Growth and Operations", "Student success (bilingual)", 0, 900, 2, 4),
    ("Growth and Operations", "Finance, bids and administration", 0, 1_500, 2, 4),
]

RAMP = {1: 0.62, 2: 0.85, 3: 0.90}

AMBASSADORS = {1: 96, 2: 220, 3: 480}
AMBASSADOR_STIPEND_MONTH = 25.0
AMBASSADOR_ACTIVE_MONTHS = 7

B2B_COMMISSION = 0.06

DEMAND_SPEND = {
    1: [("Founder podcast and video content", 24_000),
        ("Ambassador network", 16_800),
        ("Conferences, events and ecosystem presence", 22_000),
        ("Targeted digital — retargeting and event fill", 12_000),
        ("Collateral, case studies and cohort reports", 11_000),
        ("Sector research and the annual readiness report", 14_000)],
    2: [("Founder podcast and video content", 52_000),
        ("Ambassador network", 38_500),
        ("Conferences, events and ecosystem presence", 58_000),
        ("Targeted digital — retargeting and event fill", 28_000),
        ("Collateral, case studies and cohort reports", 26_000),
        ("Sector research and the annual readiness report", 28_000)],
    3: [("Founder podcast and video content", 118_000),
        ("Ambassador network", 84_000),
        ("Conferences, events and ecosystem presence", 148_000),
        ("Targeted digital — retargeting and event fill", 72_000),
        ("Collateral, case studies and cohort reports", 62_000),
        ("Sector research and the annual readiness report", 64_000)],
}

OTHER_COSTS = {
    1: [("Cloud, AI inference and third-party APIs", 30_000),
        ("Software and tooling", 20_000),
        ("Travel — Cairo, Riyadh, campuses and governorates", 42_000),
        ("Legal, audit and the KSA entity", 42_000),
        ("Safeguarding, child protection and compliance", 16_000),
        ("Office — Cairo, plus a Riyadh desk", 32_000)],
    2: [("Cloud, AI inference and third-party APIs", 104_000),
        ("Software and tooling", 42_000),
        ("Travel — Cairo, Riyadh, campuses and governorates", 128_000),
        ("Legal, audit and compliance", 58_000),
        ("Safeguarding, child protection and compliance", 34_000),
        ("Offices — Cairo and Riyadh", 78_000)],
    3: [("Cloud, AI inference and third-party APIs", 286_000),
        ("Software and tooling", 88_000),
        ("Travel — Cairo, Riyadh, campuses and governorates", 290_000),
        ("Legal, audit and compliance", 104_000),
        ("Safeguarding, child protection and compliance", 68_000),
        ("Regional delivery hubs — Upper Egypt, Delta, Jeddah", 160_000),
        ("Offices — Cairo and Riyadh", 158_000)],
}

CONTINGENCY = 0.08


# =====================================================================
#  PART 7 — ACQUISITION ECONOMICS, BY ENGINE
# =====================================================================
# (engine, cost to win one, annual value, years retained, gross margin)
ACQUISITION = [
    ("University cohorts",        1_450,  15_000, 2.8, 0.708),
    ("Faculty licences",          3_200,  25_000, 3.2, 0.880),
    ("School programmes",         1_100,   9_000, 3.4, 0.664),
    ("Technical institutes",      1_250,  11_000, 3.0, 0.640),
    ("Initiative seats",         22_000, 132_000, 2.5, 0.845),
    ("NGO and donor programmes",  7_500,  38_000, 2.6, 0.743),
    ("Sponsored competitions",    4_800,  28_000, 2.2, 0.607),
    ("Corporate programmes",      6_500,  45_000, 2.4, 0.711),
    ("Programme seats",             900,   2_400, 2.6, 0.915),
]


# =====================================================================
#  COMPUTATION — nothing below here is an assumption
# =====================================================================

ENGINE_NAMES = [
    "University cohorts and licences",
    "Schools and technical education",
    "National initiatives and government",
    "NGO, donor and foundation programmes",
    "Sponsored competitions",
    "Corporate and CSR programmes",
    "Programme and incubator seats",
    "Founder subscriptions",
]

ENGINE_FAMILY = {
    ENGINE_NAMES[0]: "Education", ENGINE_NAMES[1]: "Education",
    ENGINE_NAMES[6]: "Education",
    ENGINE_NAMES[2]: "Public", ENGINE_NAMES[3]: "Public",
    ENGINE_NAMES[4]: "Commercial", ENGINE_NAMES[5]: "Commercial",
    ENGINE_NAMES[7]: "Direct",
}


def q_year(i):
    return QUARTERS[i][2]


def quarters_of(year):
    return [i for i, q in enumerate(QUARTERS) if q[2] == year]


def plan(key, year):
    """Sum a quarterly series over a year."""
    return sum(QUARTERLY[key][i] for i in quarters_of(year))


def cohorts_for(year):
    return plan("uni_cohorts_eg", year) + plan("uni_cohorts_ksa", year)


# ---------------------------------------------------------------- subscriptions

def subscriptions(year):
    rows = []
    for name, y1, y2, y3, conv in SUBSCRIPTION_SOURCES:
        reached = {1: y1, 2: y2, 3: y3}[year]
        rows.append(dict(name=name, reached=reached, conversion=conv,
                         paid=reached * conv))
    arpu = MIX_PRO * PRICE_PRO_YEAR + MIX_TEAM * PRICE_TEAM_YEAR
    paid = sum(r["paid"] for r in rows)
    bookings = paid * arpu
    return dict(rows=rows, paid=paid, arpu=arpu, bookings=bookings,
                reached=sum(r["reached"] for r in rows),
                revenue=bookings * B2C_RECOGNITION[year],
                ltv=arpu * B2C_LIFE_YEARS * B2C_GROSS_MARGIN)


# ---------------------------------------------------------------- revenue

COHORT_PRICE = {1: PRICE_COHORT, 2: 7_900.0, 3: 8_300.0}


def quarter_revenue(i):
    """Revenue by engine in one quarter, at that year's prices."""
    y = q_year(i)
    Q = QUARTERLY
    uni = ((Q["uni_cohorts_eg"][i] + Q["uni_cohorts_ksa"][i]) * COHORT_PRICE[y]
           + Q["uni_licences"][i] * PRICE_FACULTY_LICENCE)
    school = (Q["school_cohorts"][i] * PRICE_SCHOOL_COHORT[y]
              + Q["school_licences"][i] * PRICE_SCHOOL_LICENCE
              + Q["tvet_cohorts"][i] * PRICE_TVET_COHORT[y])
    initiative = (Q["initiative_seats"][i] * PRICE_INITIATIVE_SEAT[y]
                  + Q["tot_cohorts"][i] * PRICE_TOT_COHORT[y])
    ngo = Q["ngo_programmes"][i] * PRICE_NGO_PROGRAMME[y]
    comp = Q["competitions"][i] * PRICE_COMPETITION[y]
    corp = Q["corporates"][i] * PRICE_CORPORATE[y]
    seats = Q["programmes"][i] * Q["seats_each"][i] * PRICE_SEAT[y]
    return {ENGINE_NAMES[0]: uni, ENGINE_NAMES[1]: school,
            ENGINE_NAMES[2]: initiative, ENGINE_NAMES[3]: ngo,
            ENGINE_NAMES[4]: comp, ENGINE_NAMES[5]: corp,
            ENGINE_NAMES[6]: seats, ENGINE_NAMES[7]: 0.0}


def quarterly_revenue():
    """Revenue by engine for all twelve quarters, subscriptions spread per year."""
    out = [quarter_revenue(i) for i in range(len(QUARTERS))]
    for y in (1, 2, 3):
        qs = quarters_of(y)
        subs = subscriptions(y)["revenue"]
        # Subscriptions lag the engines that produce them, so they are weighted to
        # the back half of each year rather than spread flat.
        weights = [0.10, 0.20, 0.32, 0.38]
        for w, i in zip(weights, qs):
            out[i][ENGINE_NAMES[7]] = subs * w
    return out


def revenue(year):
    qs = quarters_of(year)
    qr = quarterly_revenue()
    lines = {e: sum(qr[i][e] for i in qs) for e in ENGINE_NAMES}
    Q = QUARTERLY
    detail = {
        "uni_cohorts": cohorts_for(year) * COHORT_PRICE[year],
        "uni_licences": plan("uni_licences", year) * PRICE_FACULTY_LICENCE,
        "school_cohorts": plan("school_cohorts", year) * PRICE_SCHOOL_COHORT[year],
        "school_licences": plan("school_licences", year) * PRICE_SCHOOL_LICENCE,
        "tvet_cohorts": plan("tvet_cohorts", year) * PRICE_TVET_COHORT[year],
        "initiative_seats": plan("initiative_seats", year) * PRICE_INITIATIVE_SEAT[year],
        "tot": plan("tot_cohorts", year) * PRICE_TOT_COHORT[year],
        "ngo": plan("ngo_programmes", year) * PRICE_NGO_PROGRAMME[year],
        "competitions": plan("competitions", year) * PRICE_COMPETITION[year],
        "corporates": plan("corporates", year) * PRICE_CORPORATE[year],
        "programme_seats": sum(Q["programmes"][i] * Q["seats_each"][i] * PRICE_SEAT[year]
                               for i in qs),
        "subscriptions": lines[ENGINE_NAMES[7]],
    }
    total = sum(lines.values())
    subs = lines[ENGINE_NAMES[7]]
    return dict(lines=lines, detail=detail, total=total,
                institutional=total - subs,
                institutional_share=(total - subs) / total)


def cohort_unit_economics(price=PRICE_COHORT):
    facilitation = FACILITATORS_PER_COHORT * BOOTCAMP_DAYS * FACILITATOR_DAY_RATE
    direct = facilitation + COHORT_MATERIALS + COHORT_BAZAAR
    return dict(price=price, facilitation=facilitation, materials=COHORT_MATERIALS,
                bazaar=COHORT_BAZAAR, direct=direct, gross=price - direct,
                margin=(price - direct) / price)


def school_unit_economics(year=1):
    price = PRICE_SCHOOL_COHORT[year]
    fac = FACILITATORS_PER_COHORT * SCHOOL_DAYS * FACILITATOR_DAY_RATE
    direct = fac + SCHOOL_MATERIALS + SCHOOL_SHOWCASE
    return dict(price=price, facilitation=fac, direct=direct, gross=price - direct,
                margin=(price - direct) / price, size=SCHOOL_COHORT_SIZE,
                days=SCHOOL_DAYS)


def tvet_unit_economics(year=1):
    price = PRICE_TVET_COHORT[year]
    fac = FACILITATORS_PER_COHORT * TVET_DAYS * FACILITATOR_DAY_RATE
    direct = fac + TVET_MATERIALS + TVET_SHOWCASE
    return dict(price=price, facilitation=fac, direct=direct, gross=price - direct,
                margin=(price - direct) / price, days=TVET_DAYS)


def direct_cost(year):
    ue = cohort_unit_economics(COHORT_PRICE[year])
    su = school_unit_economics(year)
    tu = tvet_unit_economics(year)
    Q = QUARTERLY
    qs = quarters_of(year)
    return (cohorts_for(year) * ue["direct"]
            + plan("uni_pilots", year) * ue["direct"]
            + plan("school_cohorts", year) * su["direct"]
            + plan("tvet_cohorts", year) * tu["direct"]
            + plan("tot_cohorts", year) * TOT_DIRECT
            + plan("ngo_programmes", year) * NGO_DIRECT
            + plan("competitions", year) * COMPETITION_DIRECT
            + plan("corporates", year) * CORPORATE_DIRECT
            + plan("initiative_seats", year) * INITIATIVE_SEAT_DIRECT
            + sum(Q["programmes"][i] * Q["seats_each"][i] for i in qs) * SEAT_DIRECT
            + subscriptions(year)["revenue"] * (1 - B2C_GROSS_MARGIN))


def engine_economics():
    subs = subscriptions(1)
    rows = []
    for name, cac, value, years, margin in ACQUISITION:
        ltv = value * years * margin
        rows.append(dict(name=name, cac=cac, value=value, years=years,
                         margin=margin, ltv=ltv, ratio=ltv / cac))
    b2c_cac = 34.0
    rows.append(dict(name="Founder subscriptions", cac=b2c_cac, value=subs["arpu"],
                     years=B2C_LIFE_YEARS, margin=B2C_GROSS_MARGIN,
                     ltv=subs["ltv"], ratio=subs["ltv"] / b2c_cac))
    return rows


# ---------------------------------------------------------------- market sizing

def market():
    units = sum(BUYING_UNITS.values())
    schools = sum(SCHOOLS_WITH_BUDGET.values())
    tvet_inst = sum(TVET_INSTITUTIONS.values())
    he = sum(HE_STUDENTS.values())
    grads = sum(ANNUAL_GRADUATES.values()) * GRADUATE_WINDOW_YEARS
    tvet_s = sum(TVET_STUDENTS.values())
    sec = sum(SECONDARY_STUDENTS.values())
    msme = sum(MSME_OWNERS.values())
    people = he + grads + tvet_s + sec + msme

    reach = sum(HE_STUDENTS[m] * FILTER_REACHABLE[m] for m in HE_STUDENTS) / he
    unit_fit = FILTER_FACULTY_FIT * reach
    school_fit = FILTER_SCHOOL_FIT * FILTER_SCHOOL_REACHABLE
    tvet_fit = FILTER_TVET_FIT * FILTER_SCHOOL_REACHABLE

    arpu = MIX_PRO * PRICE_PRO_YEAR + MIX_TEAM * PRICE_TEAM_YEAR
    adults = he + grads + msme
    youth = tvet_s + sec
    subs_tam = (adults * FILTER_SELF_PAY_ADULT + youth * FILTER_SELF_PAY_YOUTH) * arpu

    rows = [
        dict(engine=ENGINE_NAMES[0],
             tam_basis=f"{units:,} university buying units × "
                       f"${UNIT_ANNUAL_SPEND:,.0f} a year",
             tam=units * UNIT_ANNUAL_SPEND,
             sam_basis=f"{units*unit_fit:,.0f} that fit and are reachable",
             sam=units * unit_fit * UNIT_ANNUAL_SPEND),
        dict(engine=ENGINE_NAMES[1],
             tam_basis=f"{schools:,} schools × ${SCHOOL_UNIT_ANNUAL_SPEND:,.0f} and "
                       f"{tvet_inst:,} technical institutes × "
                       f"${TVET_UNIT_ANNUAL_SPEND:,.0f}",
             tam=schools * SCHOOL_UNIT_ANNUAL_SPEND + tvet_inst * TVET_UNIT_ANNUAL_SPEND,
             sam_basis=f"{schools*school_fit:,.0f} schools and "
                       f"{tvet_inst*tvet_fit:,.0f} institutes",
             sam=(schools * school_fit * SCHOOL_UNIT_ANNUAL_SPEND
                  + tvet_inst * tvet_fit * TVET_UNIT_ANNUAL_SPEND)),
        dict(engine=ENGINE_NAMES[2],
             tam_basis=f"{INITIATIVE_SEATS_PER_YEAR:,} seats a year × "
                       f"${PRICE_INITIATIVE_SEAT[2]:,.0f}, plus trainer certification",
             tam=INITIATIVE_SEATS_PER_YEAR * PRICE_INITIATIVE_SEAT[2] * 1.25,
             sam_basis=f"{FILTER_INITIATIVE_SHARE*100:.0f}% — what one provider "
                       f"could serve",
             sam=INITIATIVE_SEATS_PER_YEAR * FILTER_INITIATIVE_SHARE
                 * PRICE_INITIATIVE_SEAT[2] * 1.25),
        dict(engine=ENGINE_NAMES[3],
             tam_basis=f"{NGOS:,} NGOs and donors × "
                       f"{NGO_PROGRAMMES_PER_ORG:.1f} programmes × "
                       f"${PRICE_NGO_PROGRAMME[2]:,.0f}",
             tam=NGOS * NGO_PROGRAMMES_PER_ORG * PRICE_NGO_PROGRAMME[2],
             sam_basis=f"{FILTER_NGO_FIT*100:.0f}% with a live youth employability "
                       f"budget",
             sam=NGOS * FILTER_NGO_FIT * NGO_PROGRAMMES_PER_ORG * PRICE_NGO_PROGRAMME[2]),
        dict(engine=ENGINE_NAMES[4],
             tam_basis=f"{COMPETITIONS_PER_YEAR:,} competitions a year × "
                       f"${PRICE_COMPETITION[2]:,.0f}",
             tam=COMPETITIONS_PER_YEAR * PRICE_COMPETITION[2],
             sam_basis=f"{FILTER_COMPETITION_FIT*100:.0f}% with budget and format fit",
             sam=COMPETITIONS_PER_YEAR * FILTER_COMPETITION_FIT * PRICE_COMPETITION[2]),
        dict(engine=ENGINE_NAMES[5],
             tam_basis=f"{CORPORATES:,} corporates × "
                       f"{CORPORATE_PROGRAMMES_PER_ORG:.1f} programmes × "
                       f"${PRICE_CORPORATE[2]:,.0f}",
             tam=CORPORATES * CORPORATE_PROGRAMMES_PER_ORG * PRICE_CORPORATE[2],
             sam_basis=f"{FILTER_CORPORATE_FIT*100:.0f}% with a live budget",
             sam=CORPORATES * FILTER_CORPORATE_FIT * CORPORATE_PROGRAMMES_PER_ORG
                 * PRICE_CORPORATE[2]),
        dict(engine=ENGINE_NAMES[6],
             tam_basis=f"{PROGRAMMES:,} programmes × 150 seats × ${PRICE_SEAT[2]:,.0f}",
             tam=PROGRAMMES * 150 * PRICE_SEAT[2],
             sam_basis=f"{FILTER_PROGRAMME_FIT*100:.0f}% that select and pre-qualify",
             sam=PROGRAMMES * FILTER_PROGRAMME_FIT * 150 * PRICE_SEAT[2]),
        dict(engine=ENGINE_NAMES[7],
             tam_basis=f"{FILTER_SELF_PAY_ADULT*100:.0f}% of {adults/1e6:,.1f}m adults "
                       f"and {FILTER_SELF_PAY_YOUTH*100:.0f}% of {youth/1e6:,.1f}m "
                       f"under-18s × ${arpu:,.0f}",
             tam=subs_tam,
             sam_basis="Those reached through an organisation, plus organic",
             sam=subscriptions(3)["reached"] * 1.6 * arpu),
    ]
    tam = sum(r["tam"] for r in rows)
    sam = sum(r["sam"] for r in rows)
    return dict(rows=rows, tam=tam, sam=sam,
                inst_tam=tam - rows[-1]["tam"], inst_sam=sam - rows[-1]["sam"],
                units=units, schools=schools, tvet_inst=tvet_inst,
                people=people, he=he, grads=grads, tvet_students=tvet_s,
                secondary=sec, msme=msme, reach=reach, unit_fit=unit_fit,
                segments=[
                    ("University students", he),
                    ("Recent graduates (3 years)", grads),
                    ("Technical and vocational students", tvet_s),
                    ("Secondary students, final two years", sec),
                    ("Micro and small enterprise owners", msme),
                ])


# ---------------------------------------------------------------- headcount

def headcount():
    by_function = {}
    for function, role, y1, monthly, y2, y3 in ROLES:
        f = by_function.setdefault(function, dict(roles=[], y1=0, y2=0, y3=0,
                                                  cost_y1=0.0, cost_y2=0.0,
                                                  cost_y3=0.0))
        f["roles"].append((role, y1, monthly, y2, y3))
        for y, c in ((1, y1), (2, y2), (3, y3)):
            f[f"y{y}"] += c
            f[f"cost_y{y}"] += c * monthly * 12
    totals = {}
    for y in (1, 2, 3):
        totals[f"y{y}"] = sum(f[f"y{y}"] for f in by_function.values())
        totals[f"cost_y{y}"] = sum(f[f"cost_y{y}"] for f in by_function.values()) * RAMP[y]
    return by_function, totals


def costs(year):
    _, hc = headcount()
    rev = revenue(year)
    demand = sum(v for _, v in DEMAND_SPEND[year])
    commission = rev["institutional"] * B2B_COMMISSION
    lines = [("Payroll", hc[f"cost_y{year}"]),
             ("Delivery — all engines", direct_cost(year)),
             ("Demand generation", demand),
             ("Sales commission", commission)]
    lines += OTHER_COSTS[year]
    subtotal = sum(v for _, v in lines)
    contingency = subtotal * CONTINGENCY
    lines.append(("Contingency", contingency))
    return dict(lines=lines, total=subtotal + contingency, subtotal=subtotal)


def projection():
    _, hc = headcount()
    out = []
    for y in (1, 2, 3):
        r, c = revenue(y), costs(y)
        out.append(dict(year=y, label=f"Year {y} · {2025+y}/{26+y}",
                        revenue=r["total"], cost=c["total"],
                        profit=r["total"] - c["total"],
                        lines=r["lines"], detail=r["detail"],
                        institutional=r["institutional"],
                        institutional_share=r["institutional_share"],
                        cohorts=cohorts_for(y), headcount=hc[f"y{y}"],
                        subs=subscriptions(y)))
    return out


def funding():
    yrs = projection()
    d1 = max(0.0, -yrs[0]["profit"])
    d2 = max(0.0, -yrs[1]["profit"])
    cumulative = d1 + d2
    reserve = yrs[0]["cost"] / 12 * 6
    ask = cumulative + reserve
    return dict(deficit_y1=d1, deficit_y2=d2, cumulative=cumulative,
                reserve=reserve, ask=ask, rounded=round(ask / 50_000) * 50_000)


def facilitator_capacity():
    """
    Does the cohort plan fit the facilitator establishment?

    Three formats with different lengths, so capacity is counted in pair-years
    rather than in cohorts: the constraint is facilitator time, not cohort count.
    """
    out = []
    for i, (label, phase, year) in enumerate(QUARTERS):
        Q = QUARTERLY
        uni = Q["uni_cohorts_eg"][i] + Q["uni_cohorts_ksa"][i] + Q["uni_pilots"][i]
        sch = Q["school_cohorts"][i]
        tv = Q["tvet_cohorts"][i]
        pairs = (uni / (COHORTS_PER_PAIR["university"] / 4)
                 + sch / (COHORTS_PER_PAIR["school"] / 4)
                 + tv / (COHORTS_PER_PAIR["tvet"] / 4))
        out.append(dict(label=label, phase=phase, year=year, uni=uni, school=sch,
                        tvet=tv, total=uni + sch + tv, pairs=pairs,
                        facilitators=pairs * 2))
    return out


def pipeline():
    return [("Institutions and sponsors identified", 760),
            ("First meeting held", 304),
            ("Pilot, proposal or bid submitted", 152),
            ("Signed in year one", 74)]


if __name__ == "__main__":
    m = market()
    print(f"TAM ${m['tam']/1e6:,.1f}m  (institutional ${m['inst_tam']/1e6:,.1f}m)")
    print(f"SAM ${m['sam']/1e6:,.1f}m  (institutional ${m['inst_sam']/1e6:,.1f}m)")
    print(f"Population reached across all segments: {m['people']/1e6:,.1f}m")
    for y in projection():
        print(f"\n  {y['label']}: rev ${y['revenue']:>11,.0f}  "
              f"cost ${y['cost']:>11,.0f}  profit ${y['profit']:>11,.0f}  "
              f"margin {y['profit']/y['revenue']*100:5.1f}%  "
              f"inst {y['institutional_share']*100:4.1f}%  hc {y['headcount']}")
        for k, v in y["lines"].items():
            print(f"       {k:<40s} ${v:>11,.0f}  {v/y['revenue']*100:4.1f}%")
    f = funding()
    print(f"\n  ask ${f['rounded']:,.0f}   "
          f"Y3 as share of SAM {projection()[2]['revenue']/m['sam']*100:.1f}%")
    print("  peak facilitators:",
          f"{max(c['facilitators'] for c in facilitator_capacity()):.0f}")
