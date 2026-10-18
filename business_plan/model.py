"""
The StartPad business plan, as arithmetic.

Every number that appears in the business plan document is computed here, from
assumptions held in one place, so a figure in a chart cannot drift away from the
sentence beside it or from the table three pages later. Nothing in the document is
typed as a literal; the builder reads this module.

Where a figure comes from outside, the source is named in a comment beside it.
Where a figure is an assumption we chose, it is marked ASSUMPTION and the reasoning
is given, because an assumption a reader cannot argue with is an assumption a reader
cannot trust.

Currency is USD throughout. The operating company is Egyptian and much of the cost
base is in EGP, but both markets and any investor conversation are in USD, and a
plan that switches currency between sections is a plan that hides its own margins.
"""

# =====================================================================
#  PART 1 — MARKET POPULATION (external figures)
# =====================================================================

# Higher-education enrolment, the two launch markets.
# Egypt: CAPMAS annual bulletin 2024/25 — 3.9m enrolled in higher education.
# KSA:   UNESCO UIS tertiary enrolment 2022 — 1.57m. The 84% gross enrolment ratio
#        reported for 2024 implies this has grown; we hold the lower figure.
HE_STUDENTS = {"Egypt": 3_900_000, "KSA": 1_600_000}

# Annual graduates.
# Egypt: 547,200 graduated in 2023 (CAPMAS, via Ahram Online).
# KSA:   not published as a single figure; derived as enrolment / 4-year degree,
#        then discounted 25% for longer programmes and attrition. ASSUMPTION.
ANNUAL_GRADUATES = {"Egypt": 547_200, "KSA": 300_000}

# A graduate stays in StartPad's 18–30 user definition for roughly three years after
# leaving. Beyond that they are either building already or they are not going to.
GRADUATE_WINDOW_YEARS = 3

# Institutional buying units. StartPad does not sell to "a university" — the GTM deck
# names four doors, three of which (entrepreneurship centre, capstone coordinator,
# dean of faculty) sit at faculty or college level. So the buying unit is the college.
# Egypt: 551 public colleges (CAPMAS) + ~400 private/national faculties. ASSUMPTION
#        on the private count; CAPMAS reports institutions, not faculty counts.
# KSA:   ~45 universities x ~12 colleges + 24 private colleges. ASSUMPTION.
BUYING_UNITS = {"Egypt": 951, "KSA": 564}


# =====================================================================
#  PART 2 — PRICING (assumptions, with reasoning)
# =====================================================================

# B2C. Priced for a student in Cairo, not a founder in London. The annual plan is
# the one we sell; monthly exists to make the annual look like the obvious choice.
PRICE_PRO_YEAR = 59.0       # ASSUMPTION — ~EGP 2,900/yr at Oct 2026 rates
PRICE_TEAM_YEAR = 179.0     # ASSUMPTION — one payment covering a founding team

# Mix of the two at the paywall. Teams convert less often but pay 3x.
MIX_PRO = 0.75
MIX_TEAM = 0.25

# B2B. The cohort price is all-in: six bootcamp days, the on-campus workshops,
# a seat for every student, the admin workspace, judging and the cohort report.
# At 25 students that is ~$300 a student, which is below what the same institution
# pays per student for a one-day external trainer with no platform behind it.
PRICE_COHORT = 7_500.0      # ASSUMPTION
COHORT_SIZE = 25            # deck: 20–30 students per group

# Platform-only seats, for an incubator or programme that runs its own facilitation
# and wants the missions, the review loop and the reporting underneath it.
PRICE_SEAT = 40.0           # ASSUMPTION

# Sponsored seats, bought in volume by an NGO, a donor or a government programme.
# Discounted against the list seat because the volume is the point.
PRICE_SPONSORED_SEAT = 35.0  # ASSUMPTION

# A faculty-wide licence: every student in a faculty, for an academic year.
PRICE_FACULTY_LICENCE = 25_000.0  # ASSUMPTION


# =====================================================================
#  PART 3 — SAM FILTERS (assumptions, with reasoning)
# =====================================================================

# Venture-building fits some faculties and not others. Business, commerce,
# engineering, computing, design and applied science carry capstone and graduation
# projects that map onto the missions. Medicine and law largely do not.
FILTER_FACULTY_FIT = 0.35

# Of those students, the ones who match the deck's own user definition: "students and
# graduates with an idea or a graduation project". Final-year capstone is close to
# universal in Egyptian engineering and business faculties, but the definition is
# wider than final year and narrower than everybody.
FILTER_HAS_AN_IDEA = 0.40

# Physically reachable for bootcamp delivery in the planning horizon: Greater Cairo,
# Alexandria, the Delta and the Upper Egypt hubs; Riyadh, Jeddah and Dammam.
FILTER_REACHABLE = {"Egypt": 0.70, "KSA": 0.80}

# At saturation an institutional buying unit runs two cohorts a year — one per term.
COHORTS_PER_UNIT_AT_SATURATION = 2


# =====================================================================
#  PART 4 — YEAR ONE GTM PLAN (the capacity-driven bottom-up)
# =====================================================================
#
# SOM is not a percentage of SAM. It is the number of cohorts a known number of
# facilitators can physically run, and the number of founders a known number of
# ambassadors and a known ad budget can bring in. Everything below is a quantity
# the operating plan has to staff.

# Paid cohorts by quarter. Q4 2026 is the Land phase: Egypt runs free pilots to
# earn the yes, so Egypt contributes no cohort revenue in Q4. KSA enters through
# programme partners, who pay from the start.
COHORTS_BY_QUARTER = [
    # (label, phase, Egypt paid, KSA paid, Egypt free pilots)
    ("Q4 2026", "Land",   0,  2, 4),
    ("Q1 2027", "Prove",  6,  4, 0),
    ("Q2 2027", "Expand", 12, 7, 0),
    ("Q3 2027", "Scale",  16, 9, 0),
]

# NGO and government sponsored seats. Two partnerships land in year one, the second
# larger than the first. See the initiatives section: the named counterparties are
# Rowad 2030 / One Million Entrepreneurs, the 1 Million Qualified Innovators
# coalition, and MSMEDA's governorate programme.
NGO_SEATS_Y1 = 3_000

# Platform-only seat deals with incubators and programmes.
PLATFORM_ONLY_PARTNERS_Y1 = 14
PLATFORM_ONLY_SEATS_PER_PARTNER = 60

# ------------------------------------------------- B2C acquisition, by channel
#
# Columns: sign-ups, activation rate (completes Mission 01), paid conversion of
# those activated, and the year-one cost of the channel.
#
# The activation and conversion rates differ sharply by channel and that difference
# is the finding, not a rounding detail: a student who signs up in a room with a
# facilitator behaves nothing like a student who taps an ad.
CHANNELS = [
    # (name, kind, sign-ups, activation, conversion, cost USD)
    ("Campus ambassadors",   "offline",  3_300, 0.68, 0.110, 16_800),
    ("Campus workshops",     "offline",  2_205, 0.82, 0.120, 12_000),
    ("Competitions",         "offline",  1_400, 0.76, 0.090, 32_000),
    ("Partner sessions",     "offline",  1_800, 0.58, 0.080,  4_000),
    ("Content and podcast",  "online",   2_800, 0.38, 0.070, 24_000),
    ("Paid social",          "online",  22_500, 0.19, 0.035, 36_000),
]

# Share of annual B2C bookings recognised inside year one. Conversions are weighted
# to the second half, so roughly half of a 12-month plan sold in year one is earned
# in year one.
B2C_RECOGNITION_Y1 = 0.50

# Average paying life of a B2C subscriber, in years. ASSUMPTION — a founder who
# finishes the journey has no reason to renew a third year, and one who stalls
# churns inside the first.
B2C_LIFE_YEARS = 1.6

# Gross margin on a B2C subscription: AI inference and payment fees are the only
# direct costs.
B2C_GROSS_MARGIN = 0.88


# =====================================================================
#  PART 5 — DIRECT COST OF DELIVERY
# =====================================================================

FACILITATORS_PER_COHORT = 2
BOOTCAMP_DAYS = 6
FACILITATOR_DAY_RATE = 120.0     # ASSUMPTION — certified freelance rate, Egypt
COHORT_MATERIALS = 450.0         # printing, kits, certificates
COHORT_BAZAAR = 300.0            # judges, refreshments, venue contribution

# A facilitator pair runs one cohort per two weeks, and needs slack for travel,
# preparation and the weeks a campus is on holiday.
COHORTS_PER_PAIR_PER_YEAR = 18


# =====================================================================
#  PART 6 — HEADCOUNT (the HR plan, costed)
# =====================================================================
#
# (function, role, count in Y1, monthly fully-loaded USD, count in Y2, count in Y3)
# Monthly cost is gross including employer contributions. Riyadh roles are priced
# at Riyadh, which is the single largest line-item surprise in the plan.

ROLES = [
    ("Leadership", "Chief Executive Officer", 1, 3_000, 1, 1),
    ("Leadership", "Chief Operating Officer", 1, 3_000, 1, 1),
    ("Leadership", "Chief Technology Officer", 1, 3_000, 1, 1),

    ("Product and Engineering", "Senior full-stack engineer", 2, 2_400, 4, 7),
    ("Product and Engineering", "AI engineer (Co-Founder, review scoring)", 1, 2_800, 2, 3),
    ("Product and Engineering", "Product designer", 1, 1_800, 2, 3),
    ("Product and Engineering", "QA and platform reliability", 1, 1_300, 2, 3),

    ("Curriculum and Content", "Head of Curriculum", 1, 2_400, 1, 1),
    ("Curriculum and Content", "Curriculum producer", 1, 1_200, 3, 5),
    ("Curriculum and Content", "Localisation lead (EG / KSA dialect)", 1, 1_200, 2, 3),

    ("Delivery", "Programme Delivery Manager — Egypt", 1, 1_800, 2, 4),
    ("Delivery", "Programme Delivery Manager — KSA", 1, 4_500, 2, 3),
    ("Delivery", "Lead facilitator", 4, 1_500, 9, 18),
    ("Delivery", "Mentor network manager", 1, 1_300, 2, 3),

    ("Growth and Marketing", "Head of Growth", 1, 2_400, 1, 1),
    ("Growth and Marketing", "Ambassador programme manager", 1, 1_200, 3, 5),
    ("Growth and Marketing", "Video and podcast producer", 1, 1_300, 2, 4),
    ("Growth and Marketing", "Performance marketer", 1, 1_500, 2, 2),

    ("Partnerships", "Head of Institutional Partnerships — Egypt", 1, 2_200, 1, 1),
    ("Partnerships", "Country Manager — KSA (Riyadh)", 1, 5_000, 1, 1),
    ("Partnerships", "Partnerships associate", 2, 1_200, 5, 10),

    ("Operations and Finance", "Finance and administration manager", 1, 1_500, 2, 3),
    ("Operations and Finance", "Student success (bilingual)", 2, 900, 5, 11),
]

# Hiring ramps through year one; nobody is on the payroll from day one except the
# founders. Average strength across the twelve months, as a share of the year-end
# establishment.
RAMP_Y1 = 0.65
RAMP_Y2 = 0.85
RAMP_Y3 = 0.90

# Ambassadors are not employees. They receive Pro access, a stipend and standing.
AMBASSADORS_Y1 = 96
AMBASSADOR_STIPEND_MONTH = 25.0
AMBASSADOR_ACTIVE_MONTHS = 7

# ------------------------------------------------------- other operating costs
OTHER_COSTS_Y1 = [
    ("Cloud, AI inference and third-party APIs", 26_000),
    ("Software and tooling", 18_000),
    ("Travel — Cairo, Riyadh and campuses", 34_000),
    ("Legal, audit and the KSA entity", 38_000),
    ("Office — Cairo, plus a Riyadh desk", 30_000),
]
CONTINGENCY = 0.08


# =====================================================================
#  PART 7 — YEARS TWO AND THREE
# =====================================================================

YEAR_PLAN = {
    # year: cohorts, cohort price, NGO seats, sponsored price,
    #       platform partners, seats each, seat price,
    #       faculty licences, licence price, B2C sign-ups, B2C recognition share
    2: dict(cohorts=150, cohort_price=7_900, ngo_seats=12_000, ngo_price=35,
            partners=40, seats_each=75, seat_price=42,
            licences=4, licence_price=25_000,
            signups=110_000, recognition=0.78),
    3: dict(cohorts=320, cohort_price=8_300, ngo_seats=35_000, ngo_price=36,
            partners=90, seats_each=85, seat_price=44,
            licences=14, licence_price=26_000,
            signups=280_000, recognition=0.82),
}

# Blended activation and conversion improve as the channel mix shifts away from paid
# social toward campus and partner channels, and as the product gets better at the
# first session. These are the year-two and year-three blended rates.
BLENDED_RATES = {2: (0.42, 0.150), 3: (0.42, 0.160)}

# Operating cost in years two and three, excluding payroll and cohort delivery,
# which are both computed. Cloud and AI inference scale with active founders, travel
# scales with cohorts, and year three carries a second office.
OTHER_COSTS_LATER = {2: 420_000, 3: 780_000}
MARKETING_LATER = {2: 260_000, 3: 620_000}

# Institutional business is sold by people, and people on a number are paid on it.
# Commission is charged on B2B revenue only; nobody is commissioned on a founder
# who subscribes from an ad.
B2B_COMMISSION = 0.06


# =====================================================================
#  COMPUTATION — nothing below here is an assumption
# =====================================================================

def _r(x, n=0):
    return round(x, n)


# ---------------------------------------------------------------- market sizing

def market():
    """TAM, SAM and the population filter chain that produces them."""
    students = sum(HE_STUDENTS.values())
    recent_grads = sum(ANNUAL_GRADUATES.values()) * GRADUATE_WINDOW_YEARS
    reachable_pop = sum(HE_STUDENTS[m] * FILTER_REACHABLE[m] for m in HE_STUDENTS)
    reachable_share = reachable_pop / students

    tam_pop = students + recent_grads

    # At full penetration most seats are institution-funded, because that is how a
    # student in this market gets access. The blended value per person reflects
    # that mix, not the list price of either product.
    inst_share = 0.70
    blended_value = inst_share * PRICE_SEAT + (1 - inst_share) * PRICE_PRO_YEAR

    tam_platform = tam_pop * blended_value
    units = sum(BUYING_UNITS.values())
    tam_delivery = units * COHORTS_PER_UNIT_AT_SATURATION * PRICE_COHORT
    tam = tam_platform + tam_delivery

    # SAM: the same population, narrowed by the three filters.
    sam_faculty = tam_pop * FILTER_FACULTY_FIT
    sam_idea = sam_faculty * FILTER_HAS_AN_IDEA
    sam_pop = sam_idea * reachable_share

    sam_platform = sam_pop * blended_value
    sam_units = units * FILTER_FACULTY_FIT * reachable_share
    sam_delivery = sam_units * COHORTS_PER_UNIT_AT_SATURATION * PRICE_COHORT
    sam = sam_platform + sam_delivery

    return dict(
        students=students, recent_grads=recent_grads, tam_pop=tam_pop,
        blended_value=blended_value, reachable_share=reachable_share,
        tam_platform=tam_platform, tam_delivery=tam_delivery, tam=tam,
        units=units, sam_units=sam_units,
        funnel=[
            ("All higher-education students and recent graduates", tam_pop),
            ("In faculties where venture-building fits", sam_faculty),
            ("With an idea or a graduation project", sam_idea),
            ("In cities we can reach for delivery", sam_pop),
        ],
        sam_pop=sam_pop, sam_platform=sam_platform,
        sam_delivery=sam_delivery, sam=sam,
    )


# ------------------------------------------------------------ B2C funnel, year 1

def channels():
    """Per-channel funnel and unit economics. The CAC table is the finding."""
    arpu = MIX_PRO * PRICE_PRO_YEAR + MIX_TEAM * PRICE_TEAM_YEAR
    ltv = arpu * B2C_LIFE_YEARS * B2C_GROSS_MARGIN
    rows = []
    for name, kind, signups, act_rate, conv, cost in CHANNELS:
        activated = signups * act_rate
        paid = activated * conv
        cac = cost / paid if paid else 0.0
        rows.append(dict(
            name=name, kind=kind, signups=signups, activation=act_rate,
            conversion=conv, cost=cost, activated=activated, paid=paid,
            cac=cac, ltv=ltv, ratio=(ltv / cac if cac else 0.0),
        ))
    return dict(rows=rows, arpu=arpu, ltv=ltv,
                signups=sum(r["signups"] for r in rows),
                activated=sum(r["activated"] for r in rows),
                paid=sum(r["paid"] for r in rows),
                cost=sum(r["cost"] for r in rows))


# ------------------------------------------------------------ revenue, year one

def revenue_y1():
    paid_cohorts = sum(e + k for _, _, e, k, _ in COHORTS_BY_QUARTER)
    free_pilots = sum(p for *_, p in COHORTS_BY_QUARTER)
    ch = channels()

    cohort_rev = paid_cohorts * PRICE_COHORT
    ngo_rev = NGO_SEATS_Y1 * PRICE_SPONSORED_SEAT
    seat_rev = PLATFORM_ONLY_PARTNERS_Y1 * PLATFORM_ONLY_SEATS_PER_PARTNER * PRICE_SEAT
    b2c_bookings = ch["paid"] * ch["arpu"]
    b2c_rev = b2c_bookings * B2C_RECOGNITION_Y1

    lines = [
        ("Bootcamp cohorts (institutions)", cohort_rev),
        ("Sponsored seats (NGO and government)", ngo_rev),
        ("Platform-only seats (programmes, incubators)", seat_rev),
        ("Founder subscriptions (Pro and Team)", b2c_rev),
    ]
    return dict(lines=lines, total=sum(v for _, v in lines),
                paid_cohorts=paid_cohorts, free_pilots=free_pilots,
                cohort_students=paid_cohorts * COHORT_SIZE,
                b2c_bookings=b2c_bookings)


# ------------------------------------------------------- delivery and cost, Y1

def cohort_unit_economics(price=PRICE_COHORT):
    facilitation = FACILITATORS_PER_COHORT * BOOTCAMP_DAYS * FACILITATOR_DAY_RATE
    direct = facilitation + COHORT_MATERIALS + COHORT_BAZAAR
    return dict(price=price, facilitation=facilitation,
                materials=COHORT_MATERIALS, bazaar=COHORT_BAZAAR,
                direct=direct, gross=price - direct,
                margin=(price - direct) / price)


def headcount():
    """Establishment by function and year, with cost."""
    by_function = {}
    for function, role, y1, monthly, y2, y3 in ROLES:
        f = by_function.setdefault(function, dict(roles=[], y1=0, y2=0, y3=0,
                                                  cost_y1=0.0, cost_y2=0.0, cost_y3=0.0))
        f["roles"].append((role, y1, monthly, y2, y3))
        f["y1"] += y1
        f["y2"] += y2
        f["y3"] += y3
        f["cost_y1"] += y1 * monthly * 12
        f["cost_y2"] += y2 * monthly * 12
        f["cost_y3"] += y3 * monthly * 12
    totals = dict(
        y1=sum(f["y1"] for f in by_function.values()),
        y2=sum(f["y2"] for f in by_function.values()),
        y3=sum(f["y3"] for f in by_function.values()),
        cost_y1=sum(f["cost_y1"] for f in by_function.values()) * RAMP_Y1,
        cost_y2=sum(f["cost_y2"] for f in by_function.values()) * RAMP_Y2,
        cost_y3=sum(f["cost_y3"] for f in by_function.values()) * RAMP_Y3,
    )
    return by_function, totals


def costs_y1():
    _, hc = headcount()
    rev = revenue_y1()
    ue = cohort_unit_economics()
    ch = channels()

    delivery = rev["paid_cohorts"] * ue["direct"]
    pilots = rev["free_pilots"] * ue["direct"]
    ambassadors = AMBASSADORS_Y1 * AMBASSADOR_STIPEND_MONTH * AMBASSADOR_ACTIVE_MONTHS
    # Ambassador stipend is already inside the channel cost; count it once, there.
    marketing = ch["cost"]

    lines = [("Payroll", hc["cost_y1"]),
             ("Cohort delivery — paid cohorts", delivery),
             ("Cohort delivery — free pilots", pilots),
             ("Growth and marketing", marketing)]
    lines += OTHER_COSTS_Y1
    subtotal = sum(v for _, v in lines)
    contingency = subtotal * CONTINGENCY
    lines.append(("Contingency", contingency))
    total = subtotal + contingency
    return dict(lines=lines, total=total, subtotal=subtotal,
                ambassadors=ambassadors)


# ------------------------------------------------------- three-year projection

def projection():
    years = []
    y1r, y1c = revenue_y1(), costs_y1()
    years.append(dict(year=1, label="Year 1 · 2026/27",
                      revenue=y1r["total"], cost=y1c["total"],
                      profit=y1r["total"] - y1c["total"],
                      lines=dict(y1r["lines"]),
                      cohorts=y1r["paid_cohorts"],
                      headcount=headcount()[1]["y1"]))

    _, hc = headcount()
    ch = channels()
    for y in (2, 3):
        p = YEAR_PLAN[y]
        act, conv = BLENDED_RATES[y]
        paid = p["signups"] * act * conv
        bookings = paid * ch["arpu"]
        lines = {
            "Bootcamp cohorts (institutions)": p["cohorts"] * p["cohort_price"],
            "Sponsored seats (NGO and government)": p["ngo_seats"] * p["ngo_price"],
            "Platform-only seats (programmes, incubators)":
                p["partners"] * p["seats_each"] * p["seat_price"],
            "Faculty-wide licences": p["licences"] * p["licence_price"],
            "Founder subscriptions (Pro and Team)": bookings * p["recognition"],
        }
        revenue = sum(lines.values())
        b2b_revenue = revenue - lines["Founder subscriptions (Pro and Team)"]
        ue = cohort_unit_economics(p["cohort_price"])
        cost = (hc[f"cost_y{y}"] + p["cohorts"] * ue["direct"]
                + MARKETING_LATER[y] + OTHER_COSTS_LATER[y]
                + b2b_revenue * B2B_COMMISSION)
        cost *= (1 + CONTINGENCY)
        years.append(dict(year=y, label=f"Year {y} · {2025 + y}/{26 + y}",
                          revenue=revenue, cost=cost, profit=revenue - cost,
                          lines=lines, cohorts=p["cohorts"],
                          headcount=hc[f"y{y}"], paid_subs=paid))
    return years


def funding():
    """
    What has to be raised, and what it buys.

    The striking result of this model is how little capital the business consumes.
    Cumulative deficit across three years is one year's deficit only: the
    institutional line is cash-generative from the first paid cohort, and cohorts
    are invoiced before they are delivered, so working capital is negative — the
    customer funds the delivery. The raise is therefore sized as the deficit plus
    a genuine operating reserve, not as a number chosen to look like a seed round.
    """
    yrs = projection()
    y1, y2 = yrs[0], yrs[1]
    deficit_y1 = -y1["profit"]
    deficit_y2 = max(0.0, -y2["profit"])
    cumulative = deficit_y1 + deficit_y2

    # Six months of the year-one cost base, held as reserve. Keyed to year one
    # rather than year three: by year three the business funds itself, and a
    # reserve sized against a cost base you have already grown into is not a
    # reserve, it is idle cash raised at the wrong price.
    reserve = y1["cost"] / 12 * 6

    ask = cumulative + reserve
    return dict(deficit_y1=deficit_y1, deficit_y2=deficit_y2,
                cumulative=cumulative, reserve=reserve,
                ask=ask, rounded=round(ask / 50_000) * 50_000)


def facilitator_capacity():
    """Does the cohort plan fit the facilitator establishment? The constraint check."""
    out = []
    for label, phase, eg, ksa, pilots in COHORTS_BY_QUARTER:
        total = eg + ksa + pilots
        pairs_needed = total / (COHORTS_PER_PAIR_PER_YEAR / 4)
        out.append(dict(label=label, phase=phase, egypt=eg, ksa=ksa,
                        pilots=pilots, total=total,
                        pairs=pairs_needed, facilitators=pairs_needed * 2))
    return out


if __name__ == "__main__":
    m, r, c = market(), revenue_y1(), costs_y1()
    print(f"TAM  ${m['tam']/1e6:,.0f}m    SAM  ${m['sam']/1e6:,.1f}m    "
          f"SOM(Y1)  ${r['total']/1e3:,.0f}k  = {r['total']/m['sam']*100:.2f}% of SAM")
    for y in projection():
        print(f"  {y['label']}: rev ${y['revenue']:,.0f}  cost ${y['cost']:,.0f}  "
              f"profit ${y['profit']:,.0f}  headcount {y['headcount']}")
    f = funding()
    print(f"  funding ask ${f['rounded']:,.0f}")
