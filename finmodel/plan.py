"""
The five-year operating plan the financial model is built from.

Sixty months, October 2026 to September 2031, in US dollars. Quarter one is
Q4 2026.

WHAT IS AN INPUT HERE, AND WHAT IS NOT

An input is a decision or a rate. How many campus workshops the team runs, how
many people are on the payroll and what they are paid, what a cohort is priced
at, how long a ministry takes to sign, what share of proposals are won.

An output is anything that follows from those. Cohorts delivered, seats
provisioned, programmes run, revenue, cost, the year one spend. None of those
are typed anywhere. Volume is produced by the acquisition engine:

    activity  ->  leads  ->  meetings  ->  proposals  ->  contracts won
              ->  mobilisation  ->  active contracts  ->  deliveries

so a cohort exists in month 40 because somebody ran a workshop in month 32,
and if the activity is cut the cohort disappears. That is the whole point of
the rebuild: the volume plan used to be typed and asked to be believed.

THREE THINGS THAT BOUND THE PLAN

1.  WHAT IS ALREADY TRUE IS THE STARTING POINT. Five signed university
    memoranda, a competition running now with 100 participants and EGP 100,000
    of prizes already committed, 300 registered users and 2 paying ones. The
    five memoranda enter the model as contracts already signed, mobilising in
    the first quarter, and they are most of year one.

2.  THE TEAM IS CAPPED at 6, 9, 12, 16 and 20 across the five years, and
    salaries are capped with it: the chief executive reaches 2,000 dollars a
    month in year five and not before. Delivery is carried by certified
    freelancers and partner organisations, so cohort growth cannot become
    payroll growth.

3.  CAPACITY IS CHECKED, NOT ASSUMED. Every activity names the function that
    runs it and how many one person can run in a month. The workbook fails if
    the plan asks for more activity, more meetings or more delivery days than
    the establishment and the certified pool can give.
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

# Contracts already signed on day one, by engine. These are not forecasts:
# they are the five memoranda and the Enactus relationship, entering the model
# through the same machinery as a contract the funnel wins later, so year one
# volume is produced rather than typed.
#
# (engine key, contracts, note)
OPENING_CONTRACTS = [
    ("uni_cohorts_eg", 5, "the five signed university memoranda"),
    ("prog_seats", 1, "Enactus Egypt, at heads of terms"),
]

# How an opening contract mobilises across the first three months.
OPENING_MOBILISATION = (0.5, 0.3, 0.2)

# The live competition. StartPad is paying the prizes itself, so it earns
# nothing and costs money. It is a proof investment and the model says so
# rather than quietly booking revenue against it.
SELF_FUNDED_COMPETITION_MONTH = 1


# =====================================================================
#  ACQUISITION - the online funnel
# =====================================================================
#
# Budget divided by cost per click gives paid clicks. Organic and referral
# traffic are a stated share of paid, never assumed free. Then three stages:
# click to lead, lead to registered account, registered account to paid.
#
# (key, label, monthly budget by year, cost per click, organic share,
#  referral share, stage 1 click to lead)
ONLINE_CHANNELS = [
    ("vid", "Short video, TikTok, Instagram, Facebook",
     (100, 300, 600, 900, 1_200), 0.10, 0.18, 0.05, 0.015),
    ("ads", "Paid social, targeted by age, city, university",
     (80, 250, 550, 850, 1_100), 0.18, 0.08, 0.03, 0.020),
    ("inf", "Influencers and student creators",
     (50, 200, 400, 650, 900), 0.14, 0.12, 0.06, 0.018),
    ("pod", "Mission Zero, the founder podcast",
     (40, 180, 350, 550, 750), 0.26, 0.20, 0.08, 0.028),
    ("web", "Webinars, live Mission 01 sessions",
     (30, 100, 200, 300, 400), 0.55, 0.06, 0.10, 0.140),
    ("seo", "SEO, content and the readiness report",
     (40, 150, 300, 450, 600), 0.05, 0.25, 0.04, 0.022),
]

STAGE_2 = (0.40, 0.42, 0.45, 0.47, 0.48)          # lead to registered
STAGE_3_ONLINE = (0.012, 0.015, 0.018, 0.021, 0.024)   # registered to paid
STAGE_3_INSTITUTIONAL = (0.035, 0.040, 0.045, 0.050, 0.055)

# Institutional enquiries per thousand accounts StartPad reached itself.
INBOUND_PER_THOUSAND = 8
# Share of online spend serving institutional demand rather than B2C.
ONLINE_INSTITUTIONAL_SHARE = 0.55


# =====================================================================
#  ACQUISITION - offline activity
# =====================================================================
#
# (key, label, activities per month by year, cost per activity,
#  free sign ups per activity, institutional leads per activity, note)
OFFLINE_CHANNELS = [
    ("ws", "Campus workshops", (1.0, 4, 8, 11, 14), 180, 30, 0.8,
     "Mission 01 finished live in an hour"),
    ("amb", "Ambassador campus activity", (2, 5, 9, 12, 15), 80, 22, 0.3,
     "run by the stipended ambassador network"),
    ("evt", "Events, fairs and conferences", (0.2, 1, 2, 2.5, 3), 600, 80,
     1.8, "judged on meetings booked, not stand traffic"),
    ("prt", "Partner sessions inside somebody else's cohort",
     (0.3, 1.5, 3, 4, 5), 150, 40, 1.0, ""),
    ("out", "Direct outreach by the commercial team", (30, 40, 55, 70, 85),
     0, 0, 1.0, "their own prospecting, the cost sits in payroll"),
]


# =====================================================================
#  ACQUISITION - who buys, how long they take
# =====================================================================
#
# A ministry and a bank do not buy the same way and are not modelled as if
# they did. Complexity shows up twice: once in the sales cycle before
# signature, and once in the mobilisation period after it.
#
# (key, label, share of leads, lead to meeting, meeting to proposal,
#  proposal to win, sales cycle months, mobilisation months, mobilisation why)
BUYERS = [
    ("inst", "Institutions, universities and schools", 0.40, 0.40, 0.45,
     0.28, 4, 2, "the cohort waits for the next semester window"),
    ("spon", "Sponsors, banks, telcos and corporates", 0.16, 0.35, 0.40,
     0.25, 5, 1, "a sponsor signs against a season already scheduled"),
    ("ngo", "NGOs, donors and development agencies", 0.14, 0.30, 0.35,
     0.20, 12, 3, "inception phase, baselining and a steering committee"),
    ("govt", "Government and national initiatives", 0.12, 0.25, 0.30,
     0.15, 11, 3, "purchase order, bulk provisioning, a pilot governorate"),
    ("csr", "CSR and corporate innovation budgets", 0.10, 0.30, 0.35,
     0.22, 7, 2, "budget release and an internal nomination round"),
    ("prog", "Accelerators, incubators and programme operators", 0.08, 0.45,
     0.50, 0.35, 3, 1, "the next intake is already dated"),
]

# Applied to the proposal to win stage only. A dean who has read two cohort
# reports from a neighbouring faculty is a different conversation from a cold
# one, and this is where that shows up.
WIN_UPLIFT = (1.00, 1.10, 1.20, 1.25, 1.30)


# =====================================================================
#  REVENUE - what a won contract turns into
# =====================================================================
#
# Each engine takes a share of one buyer type's contracts and delivers a fixed
# number of units over a contract life, evenly across it. A contract signed in
# month m becomes deliverable in month m + mobilisation and keeps delivering
# for `life` months. Volume is the active contract stock times units over
# life, so it is arithmetic on the funnel and nothing else.
#
# `gate` is the first month the engine can deliver at all, for reasons outside
# the funnel: a curriculum that does not exist yet, a country manager not in
# post, a licence that cannot precede two delivered cohorts.
#
# (key, label, buyer, share of that buyer's contracts, units per contract,
#  contract life in months, unit name, gate month, gate reason)
ENGINES = [
    ("uni_cohorts_eg", "University cohorts, Egypt", "inst", 0.50, 8, 24,
     "cohorts", 1, "already signed, delivering from month one"),
    ("uni_cohorts_ksa", "University cohorts, Saudi Arabia", "inst", 0.12, 8,
     24, "cohorts", 25, "no presence in market before the Riyadh country "
     "manager starts in month 25"),
    ("uni_licences", "Faculty licences", "inst", 0.08, 1, 12, "licences", 13,
     "cannot precede two delivered cohorts at the same faculty"),
    ("school_cohorts", "School cohorts", "inst", 0.20, 7, 24, "cohorts", 13,
     "safeguarding clearance, parental consent and the school variant of "
     "the curriculum do not exist in year one"),
    ("school_licences", "School licences", "inst", 0.04, 1, 12, "licences",
     25, "follows delivered school cohorts"),
    ("tvet_cohorts", "Technical and vocational cohorts", "inst", 0.06, 6, 24,
     "cohorts", 13, "follows the schools curriculum build"),
    ("initiative_seats", "National initiative seats", "govt", 0.70, 20_000,
     24,
     "seats", 13, "an eleven month cycle and three months of mobilisation "
     "put the first provisioned seat in month 14 at the earliest"),
    ("tot_cohorts", "Train the trainer cohorts", "govt", 0.30, 3, 18,
     "cohorts", 13, "attached to the initiative that needs the trainers"),
    ("ngo_programmes", "NGO and donor programmes", "ngo", 1.00, 3, 18,
     "programmes", 13, "a twelve month cycle and a three month inception "
     "phase"),
    ("competitions_sponsored", "Competitions, sponsored", "spon", 0.65, 3, 12,
     "competitions", 1, "a sponsor can sign against the season already "
     "running"),
    ("podcast_seasons", "Mission Zero seasons carrying a sponsor", "spon",
     0.35, 2, 12, "seasons", 1, "capped at the seasons actually produced"),
    ("corporates", "Corporate and CSR programmes", "csr", 1.00, 3, 12,
     "programmes", 13, "a seven month cycle and budget release"),
    ("prog_seats", "Programme and incubator seats", "prog", 1.00, 900, 24,
     "seats", 1, "Enactus is already at heads of terms"),
]

# Engines whose volume is additionally capped by something other than demand.
# The podcast is the only one: three seasons a year is the production
# ceiling, and a season nobody sponsors is still a cost.
PODCAST_SEASONS_PRODUCED = (1, 2, 3, 3, 3)

PRICES = {
    # key: (label, unit, five years, note)
    "p_uni": ("University cohort, all in programme fee", "USD",
              (3_500, 3_800, 4_200, 4_500, 4_800),
              "six delivery days, twenty five seats, judging and the "
              "cohort report"),
    "p_uni_lic": ("Faculty licence, annual", "USD",
                  (0, 8_000, 9_500, 11_000, 12_000),
                  "sold only after two delivered cohorts at the same "
                  "faculty"),
    "p_school": ("School cohort", "USD", (0, 2_600, 2_900, 3_100, 3_300), ""),
    "p_school_lic": ("School licence, annual", "USD",
                     (0, 5_000, 6_000, 6_500, 7_000), ""),
    "p_tvet": ("Technical and vocational cohort", "USD",
               (0, 2_800, 3_100, 3_300, 3_500), ""),
    "p_seat_init": ("National initiative seat", "USD",
                    (0, 8.00, 7.00, 6.50, 6.00),
                    "per participant, bulk provisioned, priced for a "
                    "ministry buying tens of thousands"),
    "p_tot": ("Train the trainer cohort", "USD",
              (0, 6_000, 6_800, 7_200, 7_600), ""),
    "p_ngo": ("NGO or donor programme", "USD",
              (0, 16_000, 18_000, 20_000, 22_000), ""),
    "p_comp": ("Sponsored competition season", "USD",
               (10_000, 12_000, 14_000, 16_000, 18_000),
               "paid by the sponsor, not by the organiser"),
    "p_corp": ("Corporate or CSR programme", "USD",
               (0, 18_000, 21_000, 24_000, 26_000), ""),
    "p_seat_prog": ("Programme or incubator seat", "USD",
                    (18, 20, 22, 24, 26), ""),
    "p_podcast": ("Mission Zero season sponsorship", "USD",
                  (5_000, 7_000, 9_000, 11_000, 13_000),
                  "a named season, twelve episodes"),
}

# The direct engine, repriced. Fifteen dollars a year is an Egyptian student
# price, not a western SaaS price, and the cost base below is sized for it.
SUBSCRIPTION = {
    "p_pro": ("Subscription, Pro, annual", 15),
    "p_team": ("Subscription, Team, annual", 35),
    "mix_team": ("Share of new subscribers taking Team", 0.15),
    "sub_churn": ("Subscription monthly churn", 0.06),
}

# How many people one delivered unit reaches, for the institutional side of
# the subscription funnel.
REACH = {
    "cohort_size": ("University cohort size", 25),
    "school_size": ("School and technical cohort size", 30),
    "entrants_comp": ("Entrants per competition", 400),
    "part_ngo": ("Participants per NGO programme", 120),
    "part_corp": ("Participants per corporate programme", 50),
}


# =====================================================================
#  THE ESTABLISHMENT - capped at 6, 9, 12, 16, 20
# =====================================================================
#
# (function, role, start month, monthly gross by year 1-5, headcount by year)
#
# Year one salaries are founder stipends, not market rates, and the ceiling on
# every role is stated rather than hidden in a blended average. The chief
# executive reaches two thousand dollars a month in year five.
ROLES = [
    ("Leadership", "Chief Executive Officer", 1,
     (900, 1_400, 1_700, 1_900, 2_000), (1, 1, 1, 1, 1)),
    ("Leadership", "Chief Technology Officer", 1,
     (900, 1_400, 1_700, 1_900, 2_000), (1, 1, 1, 1, 1)),
    ("Leadership", "Chief Commercial Officer", 1,
     (800, 1_300, 1_600, 1_800, 1_900), (1, 1, 1, 1, 1)),

    ("Institutional Partnerships", "Business development manager", 1,
     (600, 800, 1_000, 1_100, 1_200), (1, 1, 1, 2, 3)),
    ("Institutional Partnerships", "Sponsorship and partnerships manager", 1,
     (600, 800, 1_000, 1_100, 1_200), (1, 1, 1, 2, 2)),
    ("Institutional Partnerships", "Government and donor programmes manager",
     13, (0, 900, 1_100, 1_200, 1_300), (0, 1, 1, 1, 1)),
    ("Institutional Partnerships", "Country manager, KSA (Riyadh)", 25,
     (0, 0, 2_200, 2_400, 2_500), (0, 0, 1, 1, 1)),
    ("Institutional Partnerships", "Account manager, renewals", 49,
     (0, 0, 0, 0, 1_000), (0, 0, 0, 0, 1)),

    ("Growth and Content", "Marketing manager", 1,
     (600, 800, 1_000, 1_100, 1_200), (1, 1, 1, 1, 1)),
    ("Growth and Content", "Content and community associate", 49,
     (0, 0, 0, 0, 800), (0, 0, 0, 0, 1)),

    ("Product and Engineering", "Full stack engineer", 13,
     (0, 900, 1_100, 1_200, 1_300), (0, 1, 2, 2, 2)),
    ("Product and Engineering", "AI and data engineer", 37,
     (0, 0, 0, 1_300, 1_400), (0, 0, 0, 1, 1)),

    ("Curriculum and Delivery", "Head of curriculum and certification", 13,
     (0, 900, 1_200, 1_300, 1_400), (0, 1, 1, 1, 1)),
    ("Curriculum and Delivery", "Partner network manager", 25,
     (0, 0, 900, 1_000, 1_100), (0, 0, 1, 1, 1)),
    ("Curriculum and Delivery", "Programme delivery coordinator", 37,
     (0, 0, 0, 800, 900), (0, 0, 0, 1, 2)),
]

HEADCOUNT_CAP = (6, 9, 12, 16, 20)
EMPLOYER_BURDEN = 0.155


# =====================================================================
#  WHO DOES THE WORK - commercial and marketing capacity
# =====================================================================
#
# Four sources of capacity, because four kinds of people run these activities:
# the function that owns the activity, the founders who still carry a bag, the
# ambassadors on a stipend, and the certified delivery partner organisations.
#
# (key, label, owning function, per owner, per founder, per ambassador,
#  per partner organisation)
ACTIVITY_CAPACITY = [
    ("ws",  "Campus workshops", "Curriculum and Delivery",
     4.0, 1.0, 0.10, 0.50),
    ("amb", "Ambassador campus activity", "Growth and Content",
     2.0, 0.5, 0.60, 0.00),
    ("evt", "Events, fairs and conferences", "Institutional Partnerships",
     0.6, 0.3, 0.02, 0.10),
    ("prt", "Partner sessions inside somebody else's cohort",
     "Curriculum and Delivery", 1.5, 0.5, 0.00, 0.80),
    ("out", "Direct outreach by the commercial team",
     "Institutional Partnerships", 12.0, 4.0, 0.00, 0.00),
]

MEETINGS_PER_COMMERCIAL_HEAD = 14
MEETINGS_PER_FOUNDER = 6
MEETINGS_PER_GROWTH_HEAD = 4

# A certified facilitator is a freelancer with other work. Three and a half
# delivery days a month is what one reliably gives. The pool is an output, not
# an input: the model works out how many must be certified to deliver what the
# funnel has sold, and charges for certifying them.
FACILITATOR_DAYS_PER_MONTH = 3.5
FACILITATOR_BUFFER = 1.20
COHORTS_PER_DELIVERY_PARTNER = 2.0
