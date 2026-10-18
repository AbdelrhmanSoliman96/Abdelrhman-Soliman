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
StartPad sells to organisations that buy readiness for a group of young people.
There are six such engines and they are not equal. In order of size:

    1  University cohorts and faculty licences
    2  Sponsored seats inside national initiatives
    3  Sponsored competitions
    4  Corporate and CSR innovation programmes
    5  Programme and incubator seats
    6  Founder subscriptions

The sixth is the smallest and is a consequence of the other five rather than a
channel in its own right: a student who completed ten missions inside a camp, a
competition or a sponsored cohort is the person who pays to finish the last five.
Modelling subscriptions as a standalone consumer funnel — buying strangers through
paid social and converting them — produces a business that loses money on every
conversion. It is modelled here as downstream of institutional reach, which is both
what it is and what makes it work.

Currency is USD throughout.
"""

# =====================================================================
#  PART 1 — THE BUYER UNIVERSE (external figures)
# =====================================================================

# Higher-education enrolment, the two launch markets.
# Egypt: CAPMAS annual bulletin 2024/25 — 3.9m enrolled in higher education.
# KSA:   UNESCO UIS tertiary enrolment 2022 — 1.57m.
HE_STUDENTS = {"Egypt": 3_900_000, "KSA": 1_600_000}

# Annual graduates. Egypt: 547,200 in 2023 (CAPMAS via Ahram Online).
# KSA: not published as one figure; derived from enrolment over a four-year
# degree, discounted 25% for longer programmes and attrition. ASSUMPTION.
ANNUAL_GRADUATES = {"Egypt": 547_200, "KSA": 300_000}

# Institutional buying units. StartPad does not sell to "a university" — three of
# the four doors (entrepreneurship centre, capstone coordinator, dean of faculty)
# sit at college level, and one university routinely runs several unrelated
# cohorts. Egypt: 551 public colleges (CAPMAS) + ~400 private/national faculties.
# KSA: ~45 universities x ~12 colleges + 24 private colleges. ASSUMPTION on both
# private counts.
BUYING_UNITS = {"Egypt": 951, "KSA": 564}

# Incubators, accelerators and startup programmes across both markets that select
# applicants and would benefit from a prepared pool. ASSUMPTION, from ecosystem
# directories rather than a single published count.
PROGRAMMES = 250

# Large corporates in both markets running CSR, innovation or youth programmes
# with a budget line. ASSUMPTION.
CORPORATES = 900

# Youth and student entrepreneurship competitions run each year across both
# markets by universities, banks, telcos, ministries and foundations. ASSUMPTION.
COMPETITIONS_PER_YEAR = 600

# National initiative seats. Egypt alone has three public programmes with
# million-scale targets (One Million Entrepreneurs under Rowad 2030; 1 Million
# Qualified Innovators with UNDP, MBRF and ICESCO; One Million International
# Licences with Cisco), plus MSMEDA's governorate programme. Saudi equivalents sit
# with Monsha'at and the Misk Foundation. Addressable seats a year at steady state
# across both markets, which is far below the stated targets. ASSUMPTION.
INITIATIVE_SEATS_PER_YEAR = 400_000


# =====================================================================
#  PART 2 — PRICING (assumptions, with reasoning)
# =====================================================================

# --- Engine 1: university cohorts and licences -----------------------
# The cohort price is all-in: six bootcamp days, the on-campus workshops, a seat
# for every student, the admin workspace, judging and the cohort report. At 25
# students that is ~$300 a student, below what the same institution pays per
# student for a one-day external trainer who leaves nothing behind.
PRICE_COHORT = 7_500.0           # ASSUMPTION
COHORT_SIZE = 25                 # deck: 20–30 students per group
PRICE_FACULTY_LICENCE = 25_000.0  # ASSUMPTION — every student, one academic year

# A buying unit at saturation spends on either cohorts or a licence, not both.
# Blended annual spend per unit, used for sizing so the two are not double-counted.
UNIT_ANNUAL_SPEND = 18_000.0     # ASSUMPTION

# --- Engine 2: sponsored seats in national initiatives ---------------
# Volume is the point, so the seat is discounted hard against list. Train-the-
# trainer is sold alongside: the initiative's own facilitators are certified to
# deliver, which is the only way a programme reaches tens of thousands.
PRICE_INITIATIVE_SEAT = {1: 22.0, 2: 20.0, 3: 18.0}   # ASSUMPTION, falls with volume
PRICE_TOT_COHORT = {1: 12_000.0, 2: 12_500.0, 3: 13_000.0}  # train-the-trainer

# --- Engine 3: sponsored competitions --------------------------------
# A competition is run for a sponsor — a bank, a telco, a ministry, a university.
# The sponsor pays for the platform as the entry and qualification system, the
# judging infrastructure, the branding and the prepared finalists. Priced per
# competition by scale.
PRICE_COMPETITION = {1: 28_000.0, 2: 32_000.0, 3: 36_000.0}  # ASSUMPTION

# --- Engine 4: corporate and CSR innovation programmes ---------------
PRICE_CORPORATE = {1: 45_000.0, 2: 55_000.0, 3: 60_000.0}    # ASSUMPTION

# --- Engine 5: programme and incubator seats -------------------------
PRICE_SEAT = {1: 40.0, 2: 42.0, 3: 44.0}                     # ASSUMPTION

# --- Engine 6: founder subscriptions ---------------------------------
PRICE_PRO_YEAR = 59.0      # ASSUMPTION — ~EGP 2,900/yr at Oct 2026 rates
PRICE_TEAM_YEAR = 179.0    # ASSUMPTION — one payment covering a founding team
MIX_PRO, MIX_TEAM = 0.75, 0.25
B2C_LIFE_YEARS = 1.6
B2C_GROSS_MARGIN = 0.88
B2C_RECOGNITION = {1: 0.50, 2: 0.78, 3: 0.82}


# =====================================================================
#  PART 3 — SAM FILTERS (assumptions, with reasoning)
# =====================================================================

# Venture-building fits some faculties and not others. Business, commerce,
# engineering, computing, design and applied science carry capstone and graduation
# projects that map onto the missions. Medicine and law largely do not.
FILTER_FACULTY_FIT = 0.35

# Physically reachable for bootcamp delivery in the planning horizon: Greater
# Cairo, Alexandria, the Delta and the Upper Egypt hubs; Riyadh, Jeddah, Dammam.
FILTER_REACHABLE = {"Egypt": 0.70, "KSA": 0.80}

# Share of each other universe that is realistically addressable.
FILTER_INITIATIVE_SHARE = 0.25   # what one provider could serve of national seats
FILTER_COMPETITION_FIT = 0.40    # competitions with budget and format fit
FILTER_PROGRAMME_FIT = 0.60      # programmes that select and would pre-qualify
FILTER_CORPORATE_FIT = 0.20      # corporates with a live youth or CSR budget

# Founder subscriptions: the share of all students and recent graduates who would
# ever self-pay for a tool like this at this price. Deliberately low, and the
# reason is the finding rather than caution — see `engines()`.
FILTER_SELF_PAY = 0.06


# =====================================================================
#  PART 4 — THE YEAR-BY-YEAR PLAN, PER ENGINE
# =====================================================================
#
# Every one of these is a quantity the operating plan has to staff and sell. None
# of them is a growth rate applied to a previous year.

# Paid university cohorts by quarter. Q4 2026 is the Land phase: Egypt runs free
# pilots to earn the yes, so Egypt contributes no cohort revenue in Q4. KSA enters
# through programme partners, who pay from the start.
COHORTS_BY_QUARTER = [
    # (label, phase, Egypt paid, KSA paid, Egypt free pilots)
    ("Q4 2026", "Land",   0,  2, 4),
    ("Q1 2027", "Prove",  6,  4, 0),
    ("Q2 2027", "Expand", 12, 7, 0),
    ("Q3 2027", "Scale",  16, 9, 0),
]

PLAN = {
    # ---- Engine 1: university cohorts and faculty licences
    "cohorts":        {2: 150, 3: 320},        # year one comes from the quarters
    "licences":       {1: 2, 2: 8, 3: 22},

    # ---- Engine 2: sponsored seats in national initiatives
    "initiative_seats": {1: 6_000, 2: 30_000, 3: 95_000},
    "tot_cohorts":      {1: 2, 2: 11, 3: 34},

    # ---- Engine 3: sponsored competitions
    "competitions":   {1: 4, 2: 14, 3: 34},

    # ---- Engine 4: corporate and CSR programmes
    "corporates":     {1: 1, 2: 5, 3: 14},

    # ---- Engine 5: programme and incubator seats
    "programmes":     {1: 14, 2: 40, 3: 90},
    "seats_each":     {1: 60, 2: 75, 3: 85},
}

# Cohort price rises modestly as the cohort report becomes proven collateral.
COHORT_PRICE = {1: PRICE_COHORT, 2: 7_900.0, 3: 8_300.0}


# ------------------------------------------------- founder subscriptions
#
# Subscriptions are modelled as downstream of the institutional engines, not as a
# consumer funnel. Each row is a population StartPad already reached through an
# organisation, and the rate at which that population then pays for itself.
#
# A student who finished missions 01–10 inside a camp converts far better than a
# stranger who tapped an advertisement, because they have already done the work
# and the remaining five missions are the ones they actually want.
#
# (source, Y1 reached, Y2, Y3, conversion to paid)
SUBSCRIPTION_SOURCES = [
    ("Students from university cohorts",  1_400, 3_750, 8_000, 0.120),
    ("Entrants in sponsored competitions", 2_800, 9_800, 23_800, 0.060),
    ("Participants on sponsored seats",    6_000, 30_000, 95_000, 0.030),
    ("Programme and corporate participants", 1_340, 4_000, 9_500, 0.050),
    ("Organic — content, community, word of mouth", 4_500, 14_000, 34_000, 0.050),
]


# =====================================================================
#  PART 5 — DIRECT COST OF DELIVERY
# =====================================================================

FACILITATORS_PER_COHORT = 2
BOOTCAMP_DAYS = 6
FACILITATOR_DAY_RATE = 120.0     # ASSUMPTION — certified freelance rate, Egypt
COHORT_MATERIALS = 450.0
COHORT_BAZAAR = 300.0

# A facilitator pair runs one cohort per two weeks and needs slack for travel,
# preparation and the weeks a campus is closed.
COHORTS_PER_PAIR_PER_YEAR = 18

# Direct cost of the other engines.
TOT_DIRECT = 3_200.0             # a train-the-trainer cohort, delivered by leads
COMPETITION_DIRECT = 11_000.0    # judging, platform setup, event staffing, on-site days
CORPORATE_DIRECT = 13_000.0      # bespoke design and delivery
INITIATIVE_SEAT_DIRECT = 3.40    # inference, support and provisioning per seat
SEAT_DIRECT = 3.40


# =====================================================================
#  PART 6 — HEADCOUNT (the HR plan, costed)
# =====================================================================
#
# (function, role, Y1 count, monthly fully-loaded USD, Y2 count, Y3 count)
# Riyadh roles are priced at Riyadh, which is the single largest line-item
# surprise in the plan.

ROLES = [
    ("Leadership", "Chief Executive Officer", 1, 3_000, 1, 1),
    ("Leadership", "Chief Operating Officer", 1, 3_000, 1, 1),
    ("Leadership", "Chief Technology Officer", 1, 3_000, 1, 1),

    ("Product and Engineering", "Senior full-stack engineer", 2, 2_400, 4, 7),
    ("Product and Engineering", "AI engineer (Co-Founder, review scoring)", 1, 2_800, 2, 3),
    ("Product and Engineering", "Product designer", 1, 1_800, 2, 3),
    ("Product and Engineering", "QA and platform reliability", 1, 1_300, 2, 3),

    ("Curriculum and Content", "Head of Curriculum", 1, 2_400, 1, 1),
    ("Curriculum and Content", "Curriculum producer", 1, 1_200, 3, 6),
    ("Curriculum and Content", "Localisation lead (EG / KSA dialect)", 1, 1_200, 2, 3),

    ("Delivery", "Programme Delivery Manager — Egypt", 1, 1_800, 2, 4),
    ("Delivery", "Programme Delivery Manager — KSA", 1, 4_500, 2, 3),
    ("Delivery", "Lead facilitator", 4, 1_500, 9, 18),
    ("Delivery", "Facilitator certification lead", 1, 1_700, 1, 2),
    ("Delivery", "Mentor network manager", 1, 1_300, 2, 3),

    ("Institutional Sales", "Head of Institutional Partnerships — Egypt", 1, 2_200, 1, 1),
    ("Institutional Sales", "Country Manager — KSA (Riyadh)", 1, 5_000, 1, 1),
    ("Institutional Sales", "Head of Government and Initiatives", 1, 2_600, 1, 1),
    ("Institutional Sales", "Competitions and events manager", 1, 1_800, 2, 4),
    ("Institutional Sales", "University partnerships associate", 2, 1_200, 5, 10),
    ("Institutional Sales", "Corporate partnerships associate", 0, 1_400, 2, 4),
    ("Institutional Sales", "Account manager — renewals and expansion", 0, 1_600, 3, 8),

    ("Demand Generation", "Head of Demand Generation", 1, 2_400, 1, 1),
    ("Demand Generation", "Ambassador programme manager", 1, 1_200, 3, 5),
    ("Demand Generation", "Video and podcast producer", 1, 1_300, 2, 4),

    ("Operations and Finance", "Finance and administration manager", 1, 1_500, 2, 3),
    ("Operations and Finance", "Bid and contract administrator", 1, 1_300, 2, 3),
    ("Operations and Finance", "Student success (bilingual)", 2, 900, 6, 14),
]

RAMP = {1: 0.65, 2: 0.85, 3: 0.90}

# Ambassadors are not employees. They receive Pro access, a stipend and standing.
AMBASSADORS = {1: 96, 2: 220, 3: 480}
AMBASSADOR_STIPEND_MONTH = 25.0
AMBASSADOR_ACTIVE_MONTHS = 7

# Institutional business is sold by people, and people on a number are paid on it.
B2B_COMMISSION = 0.06

# ----------------------------------------------- demand generation budget
#
# This is not consumer acquisition. It is the cost of filling an institutional
# pipeline: the content that makes a dean take the meeting, the ambassador network
# that tells us which campuses are ready, and the events where partnerships start.
DEMAND_SPEND = {
    1: [("Founder podcast and video content", 24_000),
        ("Ambassador network", 16_800),
        ("Conferences, events and ecosystem presence", 18_000),
        ("Targeted digital — retargeting and event fill", 12_000),
        ("Collateral, case studies and cohort reports", 9_000)],
    2: [("Founder podcast and video content", 48_000),
        ("Ambassador network", 38_500),
        ("Conferences, events and ecosystem presence", 42_000),
        ("Targeted digital — retargeting and event fill", 26_000),
        ("Collateral, case studies and cohort reports", 19_000)],
    3: [("Founder podcast and video content", 92_000),
        ("Ambassador network", 84_000),
        ("Conferences, events and ecosystem presence", 88_000),
        ("Targeted digital — retargeting and event fill", 52_000),
        ("Collateral, case studies and cohort reports", 38_000)],
}

OTHER_COSTS = {
    1: [("Cloud, AI inference and third-party APIs", 26_000),
        ("Software and tooling", 18_000),
        ("Travel — Cairo, Riyadh and campuses", 34_000),
        ("Legal, audit and the KSA entity", 38_000),
        ("Office — Cairo, plus a Riyadh desk", 30_000)],
    2: [("Cloud, AI inference and third-party APIs", 78_000),
        ("Software and tooling", 34_000),
        ("Travel — Cairo, Riyadh and campuses", 82_000),
        ("Legal, audit and compliance", 46_000),
        ("Offices — Cairo and Riyadh", 64_000)],
    3: [("Cloud, AI inference and third-party APIs", 185_000),
        ("Software and tooling", 58_000),
        ("Travel — Cairo, Riyadh and campuses", 168_000),
        ("Legal, audit and compliance", 72_000),
        ("Offices — Cairo and Riyadh", 118_000)],
}

CONTINGENCY = 0.08


# =====================================================================
#  PART 7 — INSTITUTIONAL ACQUISITION ECONOMICS
# =====================================================================
#
# What it costs to win each kind of buyer, and what that buyer is worth. These are
# the numbers that should drive the company, and they are the ones the previous
# draft of this plan buried under a consumer funnel.
#
# (engine, cost to win one, deals in Y1, annual value, years retained,
#  gross margin)
ACQUISITION = [
    ("University cohorts",  1_450,  18, 15_000, 2.8, 0.708),
    ("Faculty licences",    3_200,   2, 25_000, 3.2, 0.880),
    ("Initiative seats",   22_000,   2, 132_000, 2.5, 0.845),
    ("Sponsored competitions", 4_800, 4, 28_000, 2.2, 0.679),
    ("Corporate programmes", 6_500,   1, 45_000, 2.4, 0.756),
    ("Programme seats",       900,   14,  2_400, 2.6, 0.915),
]


# =====================================================================
#  COMPUTATION — nothing below here is an assumption
# =====================================================================

def _y1_cohorts():
    return sum(e + k for _, _, e, k, _ in COHORTS_BY_QUARTER)


def _y1_pilots():
    return sum(p for *_, p in COHORTS_BY_QUARTER)


def cohorts_for(year):
    return _y1_cohorts() if year == 1 else PLAN["cohorts"][year]


# ---------------------------------------------------------------- subscriptions

def subscriptions(year):
    """Paying subscribers, derived from populations the engines already reached."""
    idx = {1: 1, 2: 2, 3: 3}[year]
    rows = []
    for name, y1, y2, y3, conv in SUBSCRIPTION_SOURCES:
        reached = {1: y1, 2: y2, 3: y3}[idx]
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

ENGINE_NAMES = [
    "University cohorts and licences",
    "Sponsored seats in national initiatives",
    "Sponsored competitions",
    "Corporate and CSR programmes",
    "Programme and incubator seats",
    "Founder subscriptions",
]


def revenue(year):
    """Revenue by engine, with the components that make each one up."""
    coh = cohorts_for(year) * COHORT_PRICE[year]
    lic = PLAN["licences"][year] * PRICE_FACULTY_LICENCE
    seats = PLAN["initiative_seats"][year] * PRICE_INITIATIVE_SEAT[year]
    tot = PLAN["tot_cohorts"][year] * PRICE_TOT_COHORT[year]
    comp = PLAN["competitions"][year] * PRICE_COMPETITION[year]
    corp = PLAN["corporates"][year] * PRICE_CORPORATE[year]
    prog = PLAN["programmes"][year] * PLAN["seats_each"][year] * PRICE_SEAT[year]
    subs = subscriptions(year)["revenue"]

    lines = {
        ENGINE_NAMES[0]: coh + lic,
        ENGINE_NAMES[1]: seats + tot,
        ENGINE_NAMES[2]: comp,
        ENGINE_NAMES[3]: corp,
        ENGINE_NAMES[4]: prog,
        ENGINE_NAMES[5]: subs,
    }
    detail = {
        "cohorts": coh, "licences": lic, "initiative_seats": seats,
        "tot": tot, "competitions": comp, "corporates": corp,
        "programme_seats": prog, "subscriptions": subs,
    }
    total = sum(lines.values())
    return dict(lines=lines, detail=detail, total=total,
                institutional=total - subs,
                institutional_share=(total - subs) / total)


def direct_cost(year):
    ue = cohort_unit_economics(COHORT_PRICE[year])
    return (cohorts_for(year) * ue["direct"]
            + (_y1_pilots() * ue["direct"] if year == 1 else 0)
            + PLAN["tot_cohorts"][year] * TOT_DIRECT
            + PLAN["competitions"][year] * COMPETITION_DIRECT
            + PLAN["corporates"][year] * CORPORATE_DIRECT
            + PLAN["initiative_seats"][year] * INITIATIVE_SEAT_DIRECT
            + PLAN["programmes"][year] * PLAN["seats_each"][year] * SEAT_DIRECT
            + subscriptions(year)["revenue"] * (1 - B2C_GROSS_MARGIN))


# ---------------------------------------------------------------- unit economics

def cohort_unit_economics(price=PRICE_COHORT):
    facilitation = FACILITATORS_PER_COHORT * BOOTCAMP_DAYS * FACILITATOR_DAY_RATE
    direct = facilitation + COHORT_MATERIALS + COHORT_BAZAAR
    return dict(price=price, facilitation=facilitation, materials=COHORT_MATERIALS,
                bazaar=COHORT_BAZAAR, direct=direct, gross=price - direct,
                margin=(price - direct) / price)


def engine_economics():
    """Deal size, margin, cost to win and lifetime value, per engine."""
    subs = subscriptions(1)
    rows = []
    for name, cac, deals, value, years, margin in ACQUISITION:
        ltv = value * years * margin
        rows.append(dict(name=name, cac=cac, deals=deals, value=value,
                         years=years, margin=margin, ltv=ltv,
                         ratio=ltv / cac, payback=cac / (value * margin) * 12))
    # Subscriptions sit on the same axis so the comparison is like for like.
    b2c_cac = 34.0   # blended, organic and institution-derived only
    rows.append(dict(name="Founder subscriptions", cac=b2c_cac, deals=subs["paid"],
                     value=subs["arpu"], years=B2C_LIFE_YEARS,
                     margin=B2C_GROSS_MARGIN, ltv=subs["ltv"],
                     ratio=subs["ltv"] / b2c_cac,
                     payback=b2c_cac / (subs["arpu"] * B2C_GROSS_MARGIN) * 12))
    return rows


# ---------------------------------------------------------------- market sizing

def market():
    """TAM and SAM, built per engine from the buyer that signs the contract."""
    units = sum(BUYING_UNITS.values())
    students = sum(HE_STUDENTS.values())
    recent = sum(ANNUAL_GRADUATES.values()) * 3
    people = students + recent
    reach = sum(HE_STUDENTS[m] * FILTER_REACHABLE[m] for m in HE_STUDENTS) / students
    unit_fit = FILTER_FACULTY_FIT * reach

    arpu = MIX_PRO * PRICE_PRO_YEAR + MIX_TEAM * PRICE_TEAM_YEAR

    rows = [
        dict(engine=ENGINE_NAMES[0],
             tam_basis=f"{units:,} buying units × {UNIT_ANNUAL_SPEND:,.0f} a year",
             tam=units * UNIT_ANNUAL_SPEND,
             sam_basis=f"{units * unit_fit:,.0f} that fit and are reachable",
             sam=units * unit_fit * UNIT_ANNUAL_SPEND),
        dict(engine=ENGINE_NAMES[1],
             tam_basis=f"{INITIATIVE_SEATS_PER_YEAR:,} seats a year × "
                       f"${PRICE_INITIATIVE_SEAT[2]:,.0f}",
             tam=INITIATIVE_SEATS_PER_YEAR * PRICE_INITIATIVE_SEAT[2],
             sam_basis=f"{FILTER_INITIATIVE_SHARE*100:.0f}% — what one provider "
                       f"could serve",
             sam=INITIATIVE_SEATS_PER_YEAR * FILTER_INITIATIVE_SHARE
                 * PRICE_INITIATIVE_SEAT[2]),
        dict(engine=ENGINE_NAMES[2],
             tam_basis=f"{COMPETITIONS_PER_YEAR:,} competitions a year × "
                       f"${PRICE_COMPETITION[2]:,.0f}",
             tam=COMPETITIONS_PER_YEAR * PRICE_COMPETITION[2],
             sam_basis=f"{FILTER_COMPETITION_FIT*100:.0f}% with budget and format fit",
             sam=COMPETITIONS_PER_YEAR * FILTER_COMPETITION_FIT * PRICE_COMPETITION[2]),
        dict(engine=ENGINE_NAMES[3],
             tam_basis=f"{CORPORATES:,} corporates × one programme every four years",
             tam=CORPORATES * 0.25 * PRICE_CORPORATE[2],
             sam_basis=f"{FILTER_CORPORATE_FIT*100:.0f}% with a live youth or CSR budget",
             sam=CORPORATES * 0.25 * FILTER_CORPORATE_FIT * PRICE_CORPORATE[2]),
        dict(engine=ENGINE_NAMES[4],
             tam_basis=f"{PROGRAMMES:,} programmes × 150 seats × ${PRICE_SEAT[2]:,.0f}",
             tam=PROGRAMMES * 150 * PRICE_SEAT[2],
             sam_basis=f"{FILTER_PROGRAMME_FIT*100:.0f}% that select and would pre-qualify",
             sam=PROGRAMMES * FILTER_PROGRAMME_FIT * 150 * PRICE_SEAT[2]),
        dict(engine=ENGINE_NAMES[5],
             tam_basis=f"{FILTER_SELF_PAY*100:.0f}% of {people/1e6:,.1f}m who would "
                       f"ever self-pay × ${arpu:,.0f}",
             tam=people * FILTER_SELF_PAY * arpu,
             sam_basis="Those reached through an organisation, plus organic",
             sam=subscriptions(3)["reached"] * 1.6 * arpu),
    ]
    tam = sum(r["tam"] for r in rows)
    sam = sum(r["sam"] for r in rows)
    inst_tam = tam - rows[-1]["tam"]
    inst_sam = sam - rows[-1]["sam"]
    return dict(rows=rows, tam=tam, sam=sam, units=units, people=people,
                students=students, recent=recent, reach=reach, unit_fit=unit_fit,
                inst_tam=inst_tam, inst_sam=inst_sam,
                buyer_funnel=[
                    ("Institutional buying units in both markets", units),
                    ("In faculties where venture-building fits", units * FILTER_FACULTY_FIT),
                    ("In cities we can reach for delivery", units * unit_fit),
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


# ---------------------------------------------------------------- cost and P&L

def costs(year):
    _, hc = headcount()
    rev = revenue(year)
    demand = sum(v for _, v in DEMAND_SPEND[year])
    other = sum(v for _, v in OTHER_COSTS[year])
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
    """
    What has to be raised, and what it buys.

    The institutional engines are cash-generative from the first paid cohort and
    every one of them invoices before delivery, so working capital is negative —
    the customer funds the work. The raise is sized as the cumulative deficit plus
    a genuine operating reserve, not as a number chosen to look like a seed round.
    """
    yrs = projection()
    d1 = max(0.0, -yrs[0]["profit"])
    d2 = max(0.0, -yrs[1]["profit"])
    cumulative = d1 + d2
    reserve = yrs[0]["cost"] / 12 * 6
    ask = cumulative + reserve
    return dict(deficit_y1=d1, deficit_y2=d2, cumulative=cumulative,
                reserve=reserve, ask=ask, rounded=round(ask / 50_000) * 50_000)


def facilitator_capacity():
    out = []
    for label, phase, eg, ksa, pilots in COHORTS_BY_QUARTER:
        total = eg + ksa + pilots
        pairs = total / (COHORTS_PER_PAIR_PER_YEAR / 4)
        out.append(dict(label=label, phase=phase, egypt=eg, ksa=ksa, pilots=pilots,
                        total=total, pairs=pairs, facilitators=pairs * 2))
    return out


def pipeline():
    """
    The institutional pipeline that produces year one, stage by stage.

    This is the replacement for a consumer acquisition funnel: it is the funnel
    the company actually runs, and every stage is a number the sales team owns.
    """
    stages = [
        ("Institutions and sponsors identified", 420),
        ("First meeting held", 168),
        ("Pilot, proposal or bid submitted", 84),
        ("Signed in year one", 41),
    ]
    return stages


if __name__ == "__main__":
    m = market()
    print(f"TAM ${m['tam']/1e6:,.1f}m  (institutional ${m['inst_tam']/1e6:,.1f}m)")
    print(f"SAM ${m['sam']/1e6:,.1f}m  (institutional ${m['inst_sam']/1e6:,.1f}m)")
    for y in projection():
        print(f"  {y['label']}: rev ${y['revenue']:>10,.0f}  cost ${y['cost']:>10,.0f}  "
              f"profit ${y['profit']:>10,.0f}  "
              f"inst {y['institutional_share']*100:4.1f}%  hc {y['headcount']}")
        for k, v in y["lines"].items():
            print(f"       {k:<44s} ${v:>10,.0f}  {v/y['revenue']*100:4.1f}%")
    f = funding()
    print(f"  ask ${f['rounded']:,.0f}")
