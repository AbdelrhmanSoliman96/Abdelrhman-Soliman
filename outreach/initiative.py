"""
One Million First-Time Founders in Egypt: the sponsorship framework.

This module holds the initiative itself: the three partner roles, the
sponsorship tiers, the in-kind menu, the value each kind of partner gets for
joining, the six-month plan for 2027, the arithmetic behind the number, and
the rules that govern the ideas bank.

It also re-cuts the prospect registry in outreach/prospects.py into the
invitation list, because the two files answer different questions. The
registry asks who in Egypt could fund entrepreneurship work at all. This file
asks who we invite to sponsor one named initiative, in what role, for what
contribution, and what they get back.

Government bodies and business chambers are deliberately not in the
invitation list. They are in the framework instead: ministries and national
initiatives as the patron and endorsement layer, which costs them nothing
and is worth more than their money, and chambers as the channel that reaches
thirty sponsors in one committee meeting.

Every number below is an assumption with its driver written next to it. None
of them is a measured result, because the initiative has not run yet. They
are here so a sponsor can check the arithmetic rather than be asked to trust
a round number.
"""

from outreach.prospects import PROSPECTS

# ------------------------------------------------------------------- naming
NAME = "One Million First-Time Founders"
NAME_AR = ("مليون رائد "
           "أعمال لأول "
           "مرة")
STRAPLINE = ("Every first-time founder in Egypt gets a method, not a "
             "motivational speech.")
WAVE = "Wave 1, March to August 2027"

# ------------------------------------------------------------------- roles
ROLES = {
    "CSR sponsor": dict(
        short="CSR sponsor",
        who="Corporates with a CSR, sustainability or community investment "
            "budget, and the corporate and family foundations attached to "
            "them.",
        gives="Cash sponsorship at one of the tiers, in-kind support from "
              "the menu, and employee mentors and judges.",
        gets="Named association with a national initiative, a reporting "
             "pack that survives audit, a pre-qualified venture pipeline, "
             "and the quarterly read on what young Egyptians are actually "
             "trying to build.",
        asked_for="Cash and in-kind"),
    "NGO and development partner": dict(
        short="NGO partner",
        who="Egyptian and international NGOs, philanthropic foundations, "
            "development agencies and UN agencies working on youth, "
            "livelihoods, employment or education.",
        gives="Reach into their own beneficiary networks and governorates, "
              "staff time, venues, co-funding where they hold a relevant "
              "budget, and co-applicant status on joint proposals.",
        gets="The method and the facilitator certification for their own "
             "staff, which they keep afterwards, a measured evidence base "
             "for their next donor proposal, and access to the sponsor "
             "coalition.",
        asked_for="In-kind, reach and co-funding"),
    "Community supporter": dict(
        short="Community supporter",
        who="Youth foundations and student organisations with members on "
            "campuses: Enactus, INJAZ, AIESEC, JCI, Hult Prize chapters, "
            "technical student branches and the youth volunteer networks.",
        gives="Their students and members, their chapters as local hosts, "
              "and their leadership as certified facilitators.",
        gets="The full programme free for every member, a credential their "
             "leadership keeps after their term ends, a national stage at "
             "the showcase, better-prepared teams for their own "
             "competitions, and their own chapter's data.",
        asked_for="Community reach, no cash"),
}

# Which role each registry category plays in this initiative.
ROLE_OF_CATEGORY = {
    "Telecom and technology": "CSR sponsor",
    "Bank and financial services": "CSR sponsor",
    "Energy, oil and gas": "CSR sponsor",
    "FMCG, food and retail": "CSR sponsor",
    "Industry, construction and real estate": "CSR sponsor",
    "Pharma and healthcare": "CSR sponsor",
    "Corporate and family foundation": "CSR sponsor",
    "Bilateral donor and development agency": "NGO and development partner",
    "UN agency and multilateral": "NGO and development partner",
    "International NGO and implementer": "NGO and development partner",
    "Egyptian NGO and social enterprise": "NGO and development partner",
    "Youth and student organisation": "Community supporter",
}

# Categories that are not invited to sponsor, and what they are instead.
NOT_INVITED = {
    "Government initiative and public agency":
        "Patron and endorsement layer. A ministry or national initiative "
        "that lends its name, opens its institutions and counts the "
        "participants towards its own target is worth more than its budget, "
        "and asking it for money slows everything down.",
    "Chamber, business association and network":
        "Channel, not sponsor. One CSR committee meeting reaches thirty of "
        "the organisations on the invitation list.",
}

# Organisations whose role differs from their category's default.
ROLE_OVERRIDE = {
    "Enactus Egypt": "Community supporter",
    "INJAZ Egypt": "Community supporter",
    "Life Makers Foundation (Sonaa Al Hayah)": "Community supporter",
    "Teach For Egypt": "Community supporter",
    "Sawiris Foundation for Social Development": "NGO and development partner",
    "Misr El Kheir Foundation": "NGO and development partner",
    "Drosos Foundation": "NGO and development partner",
    "Alfanar Venture Philanthropy": "NGO and development partner",
    "Ford Foundation, Cairo office": "NGO and development partner",
    "Abdul Latif Jameel Community Initiatives and comparable Gulf family "
    "foundations": "NGO and development partner",
}


# ------------------------------------------------------------------- tiers
# Slots are capped on purpose. A tier that anybody can buy is not worth
# buying, and a coalition of forty equal logos gives nobody a reason to be
# the first to sign.
TIERS = [
    dict(name="Founding Partner", price=150_000, slots=3,
         role="CSR sponsor",
         gives="Cash, plus a seat on the steering committee.",
         benefits=[
             "Named as a Founding Partner of the initiative, in Arabic and "
             "English, on every surface it has: the platform, the launch, "
             "the showcase, the national report.",
             "A seat on the steering committee, which sets the governorate "
             "plan and signs off the national report.",
             "A governorate or a sector of their choosing carried under "
             "their name for the whole wave.",
             "The quarterly direction report on what young Egyptians are "
             "building, by sector, governorate, gender and age, before it "
             "is published.",
             "A themed call into the ideas bank: a question put to every "
             "participant in their sector, with consented responses "
             "returned to them.",
             "First look at the ventures from the showcase, for their own "
             "accelerator, prize, procurement or hiring.",
             "Up to 40 of their staff certified as mentors and judges, "
             "with hours logged and reported back for their own employee "
             "engagement numbers.",
             "A closing report with named participants, completion rates, "
             "governorate and gender disaggregation, and SDG mapping, "
             "written to go straight into their own annual report.",
         ]),
    dict(name="Lead Partner", price=75_000, slots=6,
         role="CSR sponsor",
         gives="Cash.",
         benefits=[
             "Named as a Lead Partner across the initiative's surfaces.",
             "A seat on the partner council, which meets monthly.",
             "One governorate wave or one competition season under their "
             "name.",
             "The quarterly direction report.",
             "Up to 20 staff certified as mentors and judges.",
             "The closing report, disaggregated and SDG mapped.",
         ]),
    dict(name="Governorate Partner", price=30_000, slots=12,
         role="CSR sponsor",
         gives="Cash, usually from a community investment budget tied to "
               "where they operate.",
         benefits=[
             "One named governorate for the wave, which is the version of "
             "this that an oil, cement or industrial sponsor can fund out "
             "of an existing licence-to-operate budget.",
             "Cohorts, a local showcase and a governorate report with "
             "named participants.",
             "The direction report for their governorate.",
             "Up to 10 staff as mentors and judges.",
         ]),
    dict(name="Mission Partner", price=12_000, slots=15,
         role="CSR sponsor",
         gives="Cash. The entry tier, and the one a mid-sized Egyptian "
               "company or a second-tier foundation can sign inside a "
               "quarter.",
         benefits=[
             "One of the fifteen missions carried under their name, which "
             "every participant in the country passes through.",
             "Their sector's slice of the direction report.",
             "Named on the platform and in the closing report.",
             "Staff as mentors on their own mission.",
         ]),
    dict(name="In-kind Partner", price=0, slots=0,
         role="CSR sponsor or NGO and development partner",
         gives="Anything on the in-kind menu, valued at its market rate and "
               "credited at the cash tier it matches.",
         benefits=[
             "Credited at the tier their contribution values at, with the "
             "same benefits. Media airtime at a rate card value of $75,000 "
             "is a Lead Partner.",
             "This is how a telco, a broadcaster or a venue owner joins "
             "without a cash approval, and it is usually faster.",
         ]),
    dict(name="Community Supporter", price=0, slots=0,
         role="Community supporter",
         gives="Members, chapters and leadership time. No cash is asked "
               "for, ever.",
         benefits=[
             "Every member gets the full fifteen-mission programme free "
             "for the wave.",
             "Up to 10 of their leadership certified as facilitators, a "
             "credential they keep after their term ends.",
             "Their chapter named as a host, and their university on the "
             "national map.",
             "Their own chapter's data: what their members are building, "
             "which they can show their faculty and their own sponsors.",
             "Teams going into their own competition season already "
             "through fifteen missions.",
         ]),
]

# ----------------------------------------------------------------- in kind
INKIND = [
    ("Media and airtime", "Telecom, broadcast, outdoor",
     "Reach is the initiative's scarcest input and the cheapest thing a "
     "media owner can give. Valued at rate card.", "High"),
    ("Venues and halls", "Universities, corporates, hotels, youth centres",
     "Every cohort needs a room for six days. A sponsor with branches in "
     "nine governorates solves delivery in nine governorates.", "High"),
    ("Connectivity and devices", "Telecom, technology",
     "Data bundles and loan devices are the difference between a "
     "registered account and a completed mission in low-income "
     "governorates.", "High"),
    ("Cloud and AI credits", "Technology, hyperscalers",
     "Directly reduces the cost per review, which is the one cost that "
     "scales with participants.", "High"),
    ("Mentor and judge hours", "Every sponsor",
     "Logged, reported back, and the cheapest employee engagement a CSR "
     "team will ever buy.", "Medium"),
    ("Prizes and seed grants", "Banks, foundations, corporates",
     "What turns a showcase into a reason to finish. Small amounts, large "
     "effect on completion.", "Medium"),
    ("Company formation and legal", "Law firms, accountants",
     "Registration, tax card and a first set of accounts for the ventures "
     "that make it. The step most first-time founders stall on.", "High"),
    ("Bank accounts and payments", "Banks, fintech",
     "A business account opened for a new venture is worth more to it than "
     "a certificate, and it makes the sponsor the venture's first bank.",
     "High"),
    ("Internships and first contracts", "Corporates",
     "For participants whose idea does not become a business, which is "
     "most of them. This is the honest second outcome.", "Medium"),
    ("Transport and logistics", "Logistics, automotive",
     "Moves facilitators and participants between governorates, which is "
     "a real line in the budget.", "Low"),
    ("Printing and materials", "Printing, paper, FMCG",
     "Workbooks and showcase materials.", "Low"),
    ("Catering", "FMCG, food and beverage",
     "Six-day cohorts feed people. Easy for a food company to approve.",
     "Low"),
]


# ------------------------------------------------------------------ values
# Why each kind of partner joins. This is the part of the framework that has
# to be right, because every organisation in the invitation list is being
# asked to fund something that is not its own programme.
VALUES = {
    "CSR sponsor": [
        ("See the direction of youth thinking before anyone else",
         "Every participant states a problem before they state an idea. "
         "Across hundreds of thousands of them that becomes the first "
         "national read on what young Egyptians actually want to build: by "
         "sector, by governorate, by gender, by age, and by whether they "
         "are students, graduates or already trading. Nobody in Egypt "
         "publishes this today because nobody has the sample. A partner "
         "gets it quarterly, before it is published."),
        ("Model your incubation and accelerator programmes on real demand",
         "Most corporate accelerators are designed around what the sponsor "
         "finds interesting and then struggle to fill their cohorts. The "
         "direction report lets a sponsor design the opposite way round: "
         "open the track the applicants already exist for, in the "
         "governorate they are already in, at the stage they are actually "
         "at. For a partner who already runs an accelerator, this is the "
         "most valuable single thing in the package."),
        ("Reach into the ideas bank",
         "Every idea developed on the platform, with the founder's "
         "consent, enters a searchable bank: the problem, the sector, the "
         "stage, the governorate, the team shape. Partners see the "
         "distribution by default and can run a themed call into it, which "
         "puts their own question to every participant in their sector and "
         "returns the consented answers. It is market research that pays "
         "for itself, and it is a recruitment and deal pipeline at the "
         "same time."),
        ("A pre-qualified pipeline, not an application pile",
         "The ventures that reach the showcase have been through fifteen "
         "missions, a facilitator and an AI review. A sponsor's "
         "accelerator, prize or procurement team gets a shortlist that has "
         "already been filtered by work rather than by a form."),
        ("A generation that knows how a startup is actually built",
         "The awareness outcome is the one that outlives the wave. A "
         "million young people who understand how an idea becomes a "
         "customer, a cost structure and a company is a larger future "
         "market, a better talent pool and a healthier economy. It is also "
         "the single clearest thing a sponsor can say it paid for."),
        ("Reporting that survives an audit",
         "Named participants, completion rates, governorate and gender "
         "disaggregation, cost per participant and cost per venture "
         "formed, mapped to SDG 4, 5, 8, 9 and 10, and written so it can "
         "go into an annual or GRI report without being rewritten."),
        ("Cost per outcome far below running it yourself",
         "A corporate that builds this alone pays for curriculum, "
         "platform, facilitator recruitment and measurement before it "
         "reaches its first participant. Joining a coalition that already "
         "has all four means the whole contribution goes to delivery."),
        ("Employee engagement that is measured, not photographed",
         "Staff serve as mentors and judges, hours are logged, and the "
         "hours come back in the closing report. CSR teams are asked for "
         "this number every year and usually have to estimate it."),
        ("Name recognition tied to something real",
         "A governorate, a sector or one of the fifteen missions carried "
         "under the partner's name, in Arabic and English, in front of "
         "every participant in the country."),
    ],
    "NGO and development partner": [
        ("Keep the method after the programme ends",
         "Partner staff are certified as facilitators on the same standard "
         "as everyone else. When the wave closes, the organisation still "
         "has the capability, the curriculum access and the certification, "
         "which is the opposite of how most funded projects leave their "
         "implementers."),
        ("An evidence base for the next proposal",
         "A measured programme with baselines, disaggregation and an "
         "independent evaluation is the hardest thing for an NGO to fund "
         "on its own and the first thing its next donor asks for. The "
         "initiative produces it and shares it."),
        ("Move beneficiaries from relief to income",
         "Productive families grants, savings groups and vocational "
         "training all stop at the point where a business has to be "
         "designed. That is exactly where the fifteen missions start. This "
         "is the transition every social programme is asked to evidence "
         "and almost none can."),
        ("Reach the corporates you cannot reach alone",
         "The sponsor coalition is in the room every month. For an "
         "Egyptian NGO, the partner council is access to twenty corporate "
         "CSR decision makers that would otherwise take two years to "
         "build."),
        ("See where ambition actually is",
         "The direction report, broken down by governorate, tells a "
         "development organisation where young people are trying to build "
         "and in what sectors. That shapes their own programme design, "
         "their site selection and their own funding case."),
        ("No cash is required",
         "A partner's contribution can be entirely reach, staff time, "
         "venues and beneficiary networks. Co-funding is welcome where a "
         "relevant budget exists, and is never the price of entry."),
        ("Joint proposals, with the platform cost already carried",
         "On a shared bid the NGO is the implementer with the community "
         "relationships and the registration; the initiative supplies the "
         "method, the technology and the measurement. Neither side has to "
         "fund the other's half."),
    ],
    "Community supporter": [
        ("Your members get the whole thing free",
         "Every member of a community supporter gets the full "
         "fifteen-mission programme for the wave, not the free first "
         "three. That is a concrete, nameable member benefit, which is the "
         "currency every student organisation is short of."),
        ("Your leadership leaves with a credential",
         "Up to ten of a chapter's leadership are certified as "
         "facilitators on the national standard. They keep it after their "
         "term ends, and it is the first line on a CV that is otherwise "
         "all committee titles."),
        ("Better teams in your own competition",
         "An Enactus, Hult or Social Venture Prize team that has been "
         "through fifteen missions arrives at its own national round with "
         "a tested problem, a model and a prototype rather than a deck. "
         "The chapters that do this will place higher, and placing higher "
         "is what their own sponsors pay for."),
        ("A national stage",
         "Chapters host, chapters are named, and the best teams from every "
         "chapter reach the national showcase in front of the sponsor "
         "coalition and the patron ministries."),
        ("Your own chapter's data",
         "Each chapter gets its own read: what its members are building, "
         "how it compares to the national picture, and how its completion "
         "rates track. It is the first evidence a chapter has ever been "
         "able to show its faculty or its own sponsors."),
        ("Help raising your own sponsorship",
         "Co-branding with a national initiative and a named sponsor "
         "coalition makes a chapter's own sponsorship request materially "
         "easier, and the initiative will say so in writing to their "
         "prospects."),
        ("Nobody asks you for money",
         "Community supporters are never asked to sponsor. The "
         "relationship is members and chapters in, programme and "
         "certification out, and it is written that way in the charter."),
    ],
}

# What everyone gets, whatever their role.
SHARED_VALUE = [
    ("The direction report",
     "A quarterly national read on what young Egyptians are trying to "
     "build, by sector, governorate, gender, age and stage. Partners see it "
     "before it is published."),
    ("The ideas bank",
     "The consented, searchable record of the problems and ideas the wave "
     "produced, which is the asset the initiative leaves behind."),
    ("The national showcase",
     "One day, the best teams from every governorate, the sponsor "
     "coalition, the patron ministries and the press."),
    ("The closing report",
     "Named, disaggregated, SDG mapped, independently evaluated, and "
     "shared with every partner for their own reporting."),
    ("The coalition itself",
     "Twenty to thirty organisations that do not normally sit in the same "
     "room, meeting monthly for six months around one number."),
]

# ------------------------------------------------------------- ideas bank
# The part that has to be right or the whole proposition is extractive.
IDEAS_BANK = [
    ("What it is",
     "Every participant states a problem before they state an idea, and "
     "works it through fifteen missions. The bank is the structured record "
     "of that: problem, sector, stage, governorate, team shape, and what "
     "the venture became."),
    ("What partners see by default",
     "Distribution and direction only. Counts, shares, trends, and "
     "breakdowns by sector, governorate, gender, age and stage. No "
     "individual idea, no individual founder, no contact details."),
    ("What a themed call is",
     "A partner may put one question to every participant in a sector or "
     "governorate. Participants choose whether to answer and whether to be "
     "identified. Only the answers of those who opt in are returned, and "
     "they are told who is asking and why before they answer."),
    ("Consent",
     "Consent is asked for at registration, in Arabic, in plain language, "
     "separately for the anonymous aggregate and for any identified "
     "sharing. It can be withdrawn at any time from the account, and "
     "withdrawal removes the record from future reports."),
    ("Who owns the idea",
     "The founder. Nothing in the initiative transfers, licenses or "
     "encumbers a participant's intellectual property, and no partner "
     "acquires any right of first refusal over a venture by sponsoring. "
     "Any partner who wants a commercial relationship with a venture "
     "negotiates it with the venture, directly, afterwards."),
    ("Under-18s",
     "Participants under eighteen are in the aggregate only. No identified "
     "sharing, no themed calls, no contact, under any tier, with guardian "
     "consent recorded at registration and safeguarding rules above it."),
    ("What is never sold",
     "The bank is not a lead list and is not sold. Access is a benefit of "
     "partnership for the wave, it ends when the partnership ends, and it "
     "carries a written undertaking not to re-identify or re-sell."),
]


# -------------------------------------------------------------- arithmetic
# The funnel for Wave 1, built from the coalition rather than asserted. Each
# channel is (label, partners, reach per partner, registration rate).
CHANNELS = [
    ("Community supporter chapters", 150, 3_000, 0.22,
     "150 university and youth chapters, each reaching about 3,000 members "
     "and fellow students. The highest converting channel because the "
     "invitation comes from someone the student already knows."),
    ("CSR sponsor channels", 24, 20_000, 0.12,
     "24 sponsors reaching their own employees, customers, retail "
     "networks, social audiences and foundation beneficiaries."),
    ("NGO and development partner networks", 18, 10_000, 0.16,
     "18 partners reaching their branch networks, beneficiary lists and "
     "governorate programmes, mostly outside Cairo."),
    ("Mission Zero, press and organic", 1, 90_000, 0.14,
     "The founder podcast, launch and showcase press, and organic traffic "
     "to the platform."),
]

RATES = [
    ("Registered account to Mission 01 complete", 0.53,
     "The free first three missions are the filter. Roughly half of "
     "registrations finish the first one."),
    ("Mission 01 complete to Missions 01-03 complete", 0.56,
     "The free tier ends here. This is the honest conversion from "
     "curiosity to effort."),
    ("Sponsored full journeys, as a share of 01-03 completers", 0.33,
     "Sponsorship pays for the remaining twelve missions for a third of "
     "those who finish the free tier."),
    ("In-person cohort seats, as a share of full journeys", 0.15,
     "The premium layer: a facilitator, a room and six days. Held at 15 "
     "per cent because the delivery budget is sized against the business "
     "plan's own direct cost of $1,770 for a cohort of 30, and a larger "
     "in-person share would cost more than the whole wave raises."),
    ("Ideas entering the bank, as a share of Mission 01 completers", 0.68,
     "Mission 01 is where a problem becomes a stated idea."),
    ("Ventures trading at month 12, as a share of full journeys", 0.10,
     "The number that matters and the one nobody else reports. Ten per "
     "cent is deliberately conservative."),
]

COHORT_SIZE = 30

# Wave 1 budget, at the sponsorship fill assumed below.
TARGET_FILL = 0.50
BUDGET_SPLIT = [
    ("Delivery: facilitators, cohorts, venues, travel", 0.38),
    ("Platform, AI review and infrastructure", 0.18),
    ("Community activation: chapters, ambassadors, campus", 0.12),
    ("Content, localisation and Arabic production", 0.10),
    ("Events: launch, governorate showcases, national demo day", 0.09),
    ("Programme management and overhead", 0.07),
    ("Measurement, evaluation and reporting", 0.06),
]


def reach():
    return sum(n * per for _, n, per, _, _ in CHANNELS)


def registered():
    return sum(n * per * rate for _, n, per, rate, _ in CHANNELS)


def rate(label):
    return next(v for k, v, _ in RATES if k.startswith(label))


def funnel():
    """The Wave 1 funnel, every line derived from CHANNELS and RATES."""
    reg = registered()
    m01 = reg * rate("Registered account to Mission 01")
    m03 = m01 * rate("Mission 01 complete to Missions 01-03")
    full = m03 * rate("Sponsored full journeys")
    seats = full * rate("In-person cohort seats")
    ideas = m01 * rate("Ideas entering the bank")
    trading = full * rate("Ventures trading at month 12")
    return [
        ("People reached", reach(),
         "Sum of every channel's reach, before anybody registers."),
        ("Registered founders", reg,
         "Accounts created on the platform during the wave."),
        ("Mission 01 completed", m01,
         "The first real act of work, and the first honest number."),
        ("Missions 01 to 03 completed", m03,
         "The end of the free tier."),
        ("Sponsored full journeys, all 15 missions", full,
         "What sponsorship actually buys."),
        ("In-person cohort seats", seats,
         f"Delivered in cohorts of {COHORT_SIZE}, with certified "
         f"facilitators."),
        ("Cohorts run", seats / COHORT_SIZE,
         "Each one is six days, a room, a facilitator and a showcase."),
        ("Ideas in the bank", ideas,
         "Consented, structured, and the asset the wave leaves behind."),
        ("Ventures trading at month 12", trading,
         "Measured twelve months after the wave closes, not at the end of "
         "it."),
    ]


def target_money():
    """Full coalition value if every capped tier sells."""
    return sum(t["price"] * t["slots"] for t in TIERS)


def budget():
    """Wave 1 budget at the assumed fill, split by line."""
    total = target_money() * TARGET_FILL
    return total, [(label, share, total * share)
                   for label, share in BUDGET_SPLIT]


def unit_costs():
    total, _ = budget()
    f = dict((k, v) for k, v, _ in funnel())
    return [
        ("Cost per person reached", total / f["People reached"]),
        ("Cost per registered founder", total / f["Registered founders"]),
        ("Cost per founder completing the free tier",
         total / f["Missions 01 to 03 completed"]),
        ("Cost per sponsored full journey",
         total / f["Sponsored full journeys, all 15 missions"]),
        ("Cost per in-person seat", total / f["In-person cohort seats"]),
        ("Cost per venture trading at month 12",
         total / f["Ventures trading at month 12"]),
    ]


# The million is not a six-month number and the framework says so.
PATH_TO_MILLION = [
    ("Wave 1", "March to August 2027", "Egypt, 12 governorates",
     "The wave this framework covers. Proves the unit economics and builds "
     "the coalition."),
    ("Wave 2", "September 2027 to February 2028", "Egypt, 20 governorates",
     "The extension. Same coalition, wider geography, lower cost per "
     "founder because the facilitator pool and the chapters already "
     "exist."),
    ("Wave 3", "March to August 2028", "Egypt, all 27 governorates",
     "National coverage, with the schools and technical education systems "
     "carrying volume the university system cannot."),
    ("Wave 4", "September 2028 to February 2029", "Egypt, plus the region",
     "The million is crossed inside this wave on these rates. Anything "
     "faster needs either a national initiative mandating participation or "
     "a step change in sponsorship."),
]


# ---------------------------------------------------------------- calendar
# Why March to August and not January to June: Ramadan falls in February and
# the first days of March 2027, with Eid al-Fitr in the first half of March,
# so a January start loses its second month. Egyptian university exams run
# through May and into mid-June, which is why month three is planned as an
# online month rather than hoped through. Confirm the religious dates nearer
# the time; they are given here as approximate.
PRE_WAVE = [
    ("October 2026", "Assemble the coalition",
     "First approaches to the Founding and Lead tiers, and to the patron "
     "ministries. Nothing is announced until three Founding Partners have "
     "signed."),
    ("November 2026", "Patron endorsement",
     "Memoranda with the national initiative and the relevant ministries. "
     "These cost them nothing and are worth more than their money."),
    ("December 2026", "Community supporters",
     "Charters signed with the youth foundations and student "
     "organisations. Their leadership years are already underway, so this "
     "is the right moment, not the summer."),
    ("January 2027", "Certify the facilitators",
     "The facilitator pool and the chapter leadership are certified before "
     "the wave opens, not during it."),
    ("February 2027", "Localise and rehearse",
     "Arabic content finalised, platform load tested, two rehearsal "
     "cohorts run with a partner NGO. Ramadan month; no public launch."),
]

# (label, when, title, what happens, cumulative share of registrations,
#  share of the wave's cohorts). The two shares are multiplied by the funnel
# above when the document is written, so a month target can never drift away
# from the total it is a share of.
MONTHS = [
    ("Month 1", "March 2027", "Launch",
     "National launch after Eid al-Fitr, with the coalition on stage and "
     "the patron ministries present. Platform opens. All 150 chapters "
     "activate in the same week, which is the only way a launch number "
     "looks like a launch.", 0.30, 0.05),
    ("Month 2", "April 2027", "Campus peak",
     "The strongest campus month of the Egyptian year. Ambassador "
     "recruitment, the first governorate waves, and the first cohorts in "
     "volume.", 0.61, 0.31),
    ("Month 3", "May 2027", "Exams, so go online",
     "University exams run through May. Campus activity stops and the wave "
     "moves to the NGO networks, the youth centres and online delivery. "
     "Mid-wave report to the partner council.", 0.81, 0.07),
    ("Month 4", "June 2027", "Summer opens",
     "Exams end mid-month and the summer intensives begin, which is when "
     "young people have six consecutive days to give.", 0.91, 0.26),
    ("Month 5", "July 2027", "Peak delivery",
     "The heaviest in-person month of the wave, with governorate showcases "
     "running in parallel. The first national read of the ideas bank goes "
     "to partners.", 0.97, 0.31),
    ("Month 6", "August 2027", "Showcase and close",
     "National showcase and demo day: the best teams from every "
     "governorate, in front of the coalition, the ministries and the "
     "press. Closing report, independent evaluation commissioned, and the "
     "extension decision taken with the partners in the room.", 1.00, 0.00),
]


# -------------------------------------------------------------- governance
GOVERNANCE = [
    ("Steering committee",
     "The Founding Partners, StartPad, and an observer from each patron "
     "ministry. Meets at month zero, three and six. Sets the governorate "
     "plan, approves the national report, and decides the extension."),
    ("Partner council",
     "Every partner at every tier, plus the community supporter leads. "
     "Monthly, one hour, one dashboard. This is also where partners meet "
     "each other, which several of them will value more than the "
     "reporting."),
    ("Community council",
     "The chapter and youth foundation leads, monthly, run by them rather "
     "than by us. It owns the charter, the chapter league table and the "
     "showcase selection rules."),
    ("Delivery",
     "StartPad is accountable for delivery, the platform, the facilitator "
     "standard and the measurement. One organisation is accountable so "
     "that when something fails there is no argument about whose it was."),
    ("Safeguarding lead",
     "A named person, with a written policy, a reporting route and "
     "vetting for everyone who works with under-18s. Non-negotiable, and "
     "the first thing a serious partner will ask for."),
    ("Data protection lead",
     "A named person accountable for consent, the ideas bank rules, "
     "retention and the Egyptian data protection law. Partners receive "
     "the policy before they sign, not after."),
    ("Independent evaluation",
     "Commissioned at month six from an evaluator the steering committee "
     "chooses and StartPad does not, and published whatever it says."),
]

MEASUREMENT = [
    ("Reach and registration", "Weekly", "Dashboard",
     "By channel, by partner, by governorate. Every partner sees their own "
     "line and the national total."),
    ("Completion", "Weekly", "Dashboard",
     "Mission 01, missions 01 to 03, and full journeys. Disaggregated by "
     "sex, age band, governorate and whether the participant is a student, "
     "a graduate or already trading."),
    ("Cohort quality", "Per cohort", "Cohort report",
     "Attendance, completion, facilitator rating and the showcase result. "
     "The institution keeps this one."),
    ("Direction report", "Quarterly", "Report to partners",
     "What participants are building, by sector, governorate, gender, age "
     "and stage. Partners receive it before publication."),
    ("Ventures formed", "Month 6, month 12, month 18", "Follow-up survey",
     "Registered, trading, employing, or funded. Measured after the wave "
     "closes, because measuring at the end of a programme measures "
     "enthusiasm."),
    ("Cost per outcome", "Month 6 and month 12", "Closing report",
     "Per registered founder, per full journey, per in-person seat and "
     "per venture trading. Published with the assumptions next to them."),
    ("SDG mapping", "Month 6", "Closing report",
     "SDG 4 quality education, 5 gender equality, 8 decent work and "
     "economic growth, 9 industry innovation and infrastructure, 10 "
     "reduced inequalities, with the indicator each claim rests on."),
]

RISKS = [
    ("The coalition does not fill",
     "Likely, at least at first. The wave is designed to run at 50 per "
     "cent of the capped tiers, and the funnel above is quoted at that "
     "fill. Below 30 per cent the governorate count drops rather than the "
     "quality.", "Planned for"),
    ("Registration without completion",
     "The commonest failure in free digital programmes. Mitigated by the "
     "chapter channel, which converts because the invitation is personal, "
     "and by publishing the completion rate rather than the registration "
     "number as the headline.", "Mitigated"),
    ("Delivery capacity",
     "259 cohorts could not be staffed; 97 can. The in-person share is "
     "set by the certified facilitator pool, which is certified before the "
     "wave opens rather than recruited during it.", "Mitigated"),
    ("A partner expects exclusivity over the ideas",
     "Refused in writing, in the charter and in the sponsorship agreement. "
     "The founder owns the idea. A partner who cannot accept this is not a "
     "partner for this initiative.", "Governed"),
    ("Safeguarding incident involving a minor",
     "The risk that ends the initiative if it is handled badly. Named "
     "lead, written policy, vetting, no identified data on under-18s, and "
     "a reporting route that goes to the steering committee the same "
     "week.", "Governed"),
    ("Religious and academic calendar",
     "Ramadan in February, exams in May, summer from June. Built into the "
     "month plan rather than discovered in it.", "Planned for"),
    ("Currency and cost",
     "Sponsorship priced in dollars, cost base largely in Egyptian "
     "pounds. Devaluation helps delivery and hurts nothing in this wave; "
     "the reverse would be absorbed by reducing governorate count.",
     "Monitored"),
    ("The million is read as a six-month promise",
     "It is not, and the framework says so in the arithmetic. Wave 1 "
     "delivers roughly 198,000 registered founders. Any partner who signs "
     "believing otherwise will be a problem at month six, so the number is "
     "stated plainly before they sign.", "Stated"),
]

JOIN = [
    ("Step one, a conversation",
     "Twenty minutes. We show one cohort report and the direction report "
     "mock-up, and ask what the partner's own programme is trying to "
     "achieve. No deck."),
    ("Step two, a tier and a shape",
     "Cash tier, in-kind equivalent, or community charter. A written "
     "one-page summary of what they give, what they get, and which "
     "governorate or sector carries their name."),
    ("Step three, the paperwork",
     "Sponsorship agreement or community charter, the safeguarding and "
     "data policies, and the partner's own due diligence pack. Two weeks "
     "for a corporate, longer for a foundation board."),
    ("Step four, the council",
     "They are in the partner council from the month they sign, whether or "
     "not the wave has started."),
]


# ------------------------------------------------------- the invitation list
# The registry re-cut for this initiative: who we invite, in what role, for
# what contribution, and at which tier.
TIER_FOR_BAND = {
    "XL": "Founding Partner",
    "L": "Founding Partner",
    "M": "Lead Partner",
    "S": "Governorate Partner",
    "XS": "Mission Partner or in-kind",
}

CONTRIBUTION = {
    "CSR sponsor": "Cash, in-kind, mentors",
    "NGO and development partner": "Reach, staff time, venues, co-funding",
    "Community supporter": "Members, chapters, leadership. No cash",
}

# What each role is actually offered, in one line, for the invitation column.
OFFER = {
    "CSR sponsor":
        "A named tier in the coalition: a governorate, a sector or one of "
        "the fifteen missions under their name, with the direction report "
        "and the closing report.",
    "NGO and development partner":
        "Facilitator certification for their own staff, the method for "
        "their own beneficiaries, a shared evidence base, and a seat in "
        "the coalition.",
    "Community supporter":
        "The full programme free for every member, certification for ten "
        "of their leadership, their chapter on the national map, and "
        "their own chapter's data.",
}


def role_of(prospect):
    """The role this organisation would play, or None if it is not invited."""
    if prospect["name"] in ROLE_OVERRIDE:
        return ROLE_OVERRIDE[prospect["name"]]
    return ROLE_OF_CATEGORY.get(prospect["cat"])


def tier_for(prospect, role):
    if role == "Community supporter":
        return "Community Supporter"
    return TIER_FOR_BAND[prospect["band"]]


def invitation_list():
    """The sponsor-facing cut of the registry, ordered by role then tier."""
    tier_rank = {t["name"]: i for i, t in enumerate(TIERS)}
    tier_rank["Mission Partner or in-kind"] = tier_rank["Mission Partner"]
    role_rank = {r: i for i, r in enumerate(ROLES)}
    out = []
    for p in PROSPECTS:
        role = role_of(p)
        if role is None:
            continue
        tier = tier_for(p, role)
        row = dict(p)
        # The registry's "tier" column is its A/B/C priority; this file's
        # "tier" is the sponsorship tier. Rename the first so neither
        # shadows the other.
        row["tier_abc"] = p["tier"]
        row["role"] = role
        row["tier"] = tier
        row["contribution"] = CONTRIBUTION[role]
        row["offer"] = OFFER[role]
        out.append(row)
    # Role, then tier, then the registry's own A/B/C priority, then name.
    return sorted(out, key=lambda r: (role_rank[r["role"]],
                                      tier_rank[r["tier"]],
                                      {"A": 0, "B": 1, "C": 2}[r["tier_abc"]],
                                      r["name"]))


def coverage():
    """Invited rows against the slots the tiers actually have."""
    rows = invitation_list()
    out = []
    for t in TIERS:
        if t["slots"]:
            n = sum(1 for r in rows if r["tier"].startswith(t["name"]))
            out.append((t["name"], t["slots"], n, t["price"],
                        t["slots"] * t["price"]))
    return out
