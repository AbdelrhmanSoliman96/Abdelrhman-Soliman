"""
The five-year operating plan the financial model is built from.

Sixty months, October 2026 to September 2031, in US dollars. Everything here is
an input: the builder writes these numbers into the workbook's yellow cells and
every other cell in the workbook is a formula over them.

Three constraints shaped this plan and are worth stating before the numbers.

1.  YEAR ONE SPENDS UNDER $150,000, IN TOTAL. Direct delivery, payroll,
    marketing, premises, professional fees - everything. That ceiling, not an
    ambition for revenue, is what sets the Year 1 volumes. A plan that spends
    $800,000 in its first year is a different company from this one.

2.  WHAT IS ALREADY TRUE IS THE STARTING POINT, not an assumption. Five signed
    university memoranda, a competition running now with 100 participants and
    EGP 100,000 of prizes already committed, 300 registered users and 2 paying
    ones. The model opens on those, not on zero.

3.  THE TEAM IS CAPPED at 4, 7, 12, 16 and 20 across the five years. Delivery
    is carried by certified freelancers and partner organisations, so cohort
    growth cannot become payroll growth.

Quarters are numbered 1-20 from Q1 = Oct-Dec 2026. Monthly figures are a
quarter's volume split by the phasing weights, so an annual total always ties
back to this file exactly.
"""

CURRENCY = "USD"
START_YEAR, START_MONTH = 2026, 10        # October 2026
YEARS = 5
MONTHS = YEARS * 12
QUARTERS = YEARS * 4

# Egyptian pound to the dollar, used to convert the prize money already
# committed on the live competition. ASSUMPTION - check before relying on it.
EGP_PER_USD = 48.5

YEAR_LABELS = ["Year 1, FY2026/27", "Year 2, FY2027/28", "Year 3, FY2028/29",
               "Year 4, FY2029/30", "Year 5, FY2030/31"]

# A quarter's volume split across its three months. Nothing lands evenly in an
# academic calendar: the first month of a quarter is setup, the last is
# delivery and invoicing.
PHASING = (0.28, 0.33, 0.39)


# =====================================================================
#  WHAT IS ALREADY TRUE - the opening position
# =====================================================================
#
# (key, item, value, unit, note)
TRACTION = [
    ("registered", "Registered users on the platform", 300, "#",
     "already signed up, before any paid cohort"),
    ("paid_users", "Paying subscribers", 2, "#",
     "the honest starting point for the direct engine"),
    ("comp_participants", "Live competition participants", 100, "#",
     "the competition running now"),
    ("prize_egp", "Prize money committed on the live competition", 100_000,
     "EGP", "converted to dollars at the rate above"),
    ("mous", "University memoranda signed", 5, "#",
     "MSA, Coventry Egypt, CIC, ESLSCA and Zewail"),
    ("near_signed", "Partnerships at heads of terms", 1, "#",
     "Enactus Egypt, close but not signed"),
    ("open_cash", "Opening cash", 50_000, "USD",
     "founder capital already contributed"),
]

# The five institutions that are already signed, and the one that is close.
# Names are normalised from the founder's note; confirm the official forms
# before this workbook goes to anybody outside the company.
SIGNED_INSTITUTIONS = [
    ("MSA University", "Egypt, signed", "October University for Modern "
     "Sciences and Arts", 3),
    ("Coventry University Egypt", "Egypt, signed",
     "Coventry's Egypt branch campus", 3),
    ("Canadian International College (CIC)", "Egypt, signed",
     "New Cairo and Sheikh Zayed campuses", 2),
    ("ESLSCA University Egypt", "Egypt, signed",
     "French business school, Cairo campus", 2),
    ("Zewail Academy", "Egypt, signed",
     "Zewail City of Science and Technology", 2),
    ("Enactus Egypt", "Egypt, heads of terms",
     "National competition, 30-35 finalist university teams", 0),
]


# =====================================================================
#  VOLUME PLAN - twenty quarters
# =====================================================================
#
# Year 1 is deliberately small. It is bounded by the $150,000 ceiling and by
# what five signed universities can actually absorb in their first year, not by
# what the market could take.

Q = {
    # --- Engine 1 - universities -------------------------------------
    # Y1 runs across the five signed memoranda: two free pilots to create the
    # first cohort reports, then paid cohorts on the strength of them.
    "uni_cohorts_eg":   [1, 2, 3, 4,    5, 6, 8, 9,    11, 13, 15, 17,
                         19, 21, 23, 25,  27, 29, 31, 33],
    "uni_cohorts_ksa":  [0, 0, 0, 0,    0, 1, 1, 2,     4,  5,  6,  7,
                          8,  9, 10, 11,  12, 13, 14, 15],
    "uni_pilots":       [2, 1, 1, 0,    1, 1, 1, 1,     1,  1,  1,  1,
                          1,  1,  1,  1,   1,  1,  1,  1],
    "uni_licences":     [0, 0, 0, 0,    0, 1, 1, 2,     3,  3,  4,  4,
                          5,  5,  6,  6,   7,  7,  8,  8],

    # --- Engine 2 - schools and technical education -------------------
    # Gated to year two: the school variant of the curriculum, safeguarding
    # clearance and parental consent do not exist in year one.
    "school_cohorts":   [0, 0, 0, 0,    0, 2, 3, 4,     6,  8, 10, 12,
                         14, 16, 18, 20,  22, 24, 26, 28],
    "school_licences":  [0, 0, 0, 0,    0, 0, 1, 1,     2,  2,  3,  3,
                          4,  4,  5,  5,   6,  6,  7,  7],
    "tvet_cohorts":     [0, 0, 0, 0,    0, 0, 1, 2,     3,  4,  5,  6,
                          7,  8,  9, 10,  11, 12, 13, 14],

    # --- Engine 3 - national initiatives ------------------------------
    # The longest cycle in the company. Conversations open in year one; the
    # first paid seats land in year two.
    "initiative_seats": [0, 0, 0, 0,
                         0, 0, 1_500, 2_500,
                         4_000, 6_000, 8_000, 10_000,
                         14_000, 17_000, 20_000, 23_000,
                         26_000, 29_000, 32_000, 35_000],
    "tot_cohorts":      [0, 0, 0, 0,    0, 0, 1, 1,     2,  2,  3,  3,
                          4,  4,  5,  5,   6,  6,  7,  7],

    # --- Engine 4 - NGO, donor and foundation programmes --------------
    "ngo_programmes":   [0, 0, 0, 0,    0, 1, 1, 2,     2,  3,  3,  4,
                          4,  5,  5,  6,   6,  7,  7,  8],

    # --- Engine 5 - competitions ---------------------------------------
    # The competition running now is self funded: StartPad is paying the
    # EGP 100,000 of prizes itself, so it earns nothing and costs money. It is
    # a proof investment, and the model says so rather than quietly booking
    # revenue against it. Sponsored seasons start in Q4, which is when the
    # first sponsor's calendar allows, not when a conversation starts.
    "competitions_self":      [1, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0,
                               0, 0, 0, 0,  0, 0, 0, 0],
    "competitions_sponsored": [0, 0, 0, 1,  1, 1, 1, 2,  2, 2, 3, 3,
                               3, 4, 4, 5,  5, 5, 6, 6],

    # --- Engine 6 - corporate and CSR ---------------------------------
    "corporates":       [0, 0, 0, 0,    0, 0, 0, 1,     1,  1,  2,  2,
                          2,  3,  3,  4,   4,  4,  5,  5],

    # --- Engine 7 - programme and incubator seats ---------------------
    "programme_partners": [0, 1, 1, 2,  3, 4, 5, 6,     7,  8,  9, 10,
                          11, 12, 13, 14, 15, 16, 17, 18],   # a stock
    "seats_per_partner":  [60, 60, 60, 60, 70, 70, 70, 70, 80, 80, 80, 80,
                           85, 85, 85, 85, 90, 90, 90, 90],  # a stock

    # --- Mission Zero - sponsored seasons ------------------------------
    # Three seasons a year is the production ceiling. The number here is the
    # seasons that carry a paying sponsor.
    "podcast_seasons":  [0, 0, 0, 1,    1, 0, 1, 0,     1,  1,  1,  0,
                          1,  1,  1,  0,   1,  1,  1,  0],

    # --- The delivery network, as a stock ------------------------------
    "certified_facilitators": [6, 9, 12, 15,  19, 24, 29, 34,
                               40, 46, 52, 58,  66, 74, 82, 90,
                               98, 106, 114, 122],
    "delivery_partners":      [0, 0, 1, 1,   2, 3, 4, 5,
                               6, 7, 8, 9,   10, 11, 12, 13,
                               14, 15, 16, 17],
}

STOCKS = {"programme_partners", "seats_per_partner", "certified_facilitators",
          "delivery_partners"}


# =====================================================================
#  THE ESTABLISHMENT - capped at 4, 7, 12, 16, 20
# =====================================================================
#
# (function, role, start month, monthly gross by year 1-5, headcount by year)
#
# Year-one salaries are founder stipends, not market rates. That is the only
# way a four-person team and a $150,000 ceiling can both be true, and it is
# stated here rather than hidden in a blended average. They step up sharply in
# year two, once year-one revenue exists to pay them.
ROLES = [
    ("Leadership", "Chief Executive Officer", 1,
     (900, 1_800, 2_600, 3_000, 3_200), (1, 1, 1, 1, 1)),
    ("Leadership", "Chief Technology Officer", 1,
     (900, 1_800, 2_600, 3_000, 3_200), (1, 1, 1, 1, 1)),
    ("Leadership", "Chief Operating Officer", 37,
     (0, 0, 0, 3_000, 3_200), (0, 0, 0, 1, 1)),

    ("Product and Engineering", "Senior full-stack engineer", 1,
     (800, 1_900, 2_400, 2_500, 2_600), (1, 2, 2, 2, 2)),
    ("Product and Engineering", "AI and data engineer", 37,
     (0, 0, 0, 2_800, 2_900), (0, 0, 0, 1, 1)),
    ("Product and Engineering", "Product designer", 49,
     (0, 0, 0, 0, 1_800), (0, 0, 0, 0, 1)),

    ("Curriculum and Delivery", "Head of Curriculum and Certification", 1,
     (650, 1_700, 2_400, 2_500, 2_600), (1, 1, 1, 1, 1)),
    ("Curriculum and Delivery", "Partner network manager", 25,
     (0, 0, 2_000, 2_100, 2_200), (0, 0, 1, 1, 1)),
    ("Curriculum and Delivery", "Programme delivery coordinator", 25,
     (0, 0, 1_500, 1_550, 1_600), (0, 0, 1, 2, 2)),
    ("Curriculum and Delivery", "Bilingual curriculum producer", 49,
     (0, 0, 0, 0, 1_300), (0, 0, 0, 0, 1)),

    ("Institutional Partnerships", "Head of Partnerships, Egypt", 13,
     (0, 1_600, 2_200, 2_300, 2_400), (0, 1, 1, 1, 1)),
    ("Institutional Partnerships", "Country Manager, KSA (Riyadh)", 25,
     (0, 0, 5_000, 5_200, 5_400), (0, 0, 1, 1, 1)),
    ("Institutional Partnerships", "Head of Government, Initiatives and Donors",
     25, (0, 0, 2_600, 2_700, 2_800), (0, 0, 1, 1, 1)),
    ("Institutional Partnerships", "Partnerships and bids associate", 25,
     (0, 0, 1_200, 1_250, 1_300), (0, 0, 1, 1, 1)),
    ("Institutional Partnerships", "Head of Schools and Technical Education",
     37, (0, 0, 0, 2_200, 2_300), (0, 0, 0, 1, 1)),
    ("Institutional Partnerships", "Account manager, renewals", 49,
     (0, 0, 0, 0, 1_600), (0, 0, 0, 0, 1)),

    ("Growth and Content", "Head of Growth and Content", 13,
     (0, 1_500, 2_000, 2_100, 2_200), (0, 1, 1, 1, 1)),
    ("Growth and Content", "Student success (bilingual)", 49,
     (0, 0, 0, 0, 900), (0, 0, 0, 0, 1)),
]

HEADCOUNT_CAP = (4, 7, 12, 16, 20)
