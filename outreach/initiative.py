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
        gets="The method for their own beneficiaries, their staff trained to host sessions, a measured evidence base for their next donor proposal, and access to the sponsor coalition.",
        asked_for="In-kind, reach and co-funding"),
    "Community supporter": dict(
        short="Community supporter",
        who="Youth foundations and student organisations with members on "
            "campuses: Enactus, INJAZ, AIESEC, JCI, Hult Prize chapters, "
            "technical student branches and the youth volunteer networks.",
        gives="Their students and members, their chapters as hosts for info sessions, and their leadership trained to run them.",
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


# ------------------------------------------------------------------ pricing
EGP_PER_USD = 53.22          # the rate in finmodel/plan.py


def egp(usd):
    return usd * EGP_PER_USD


# ------------------------------------------------------------------- tiers
# Three tiers. Not four, not six. A sponsorship menu that takes a page to
# read is a menu nobody signs, and this initiative is funded entirely by
# partners, so the ask has to be as easy to say yes to as possible.
TIERS = [
    dict(name="Founding Partner", price=50_000.0, slots=2,
         role="CSR sponsor",
         gives="Cash, plus a seat on the steering committee.",
         benefits=[
             "Named as a Founding Partner of a national initiative, in "
             "Arabic and English, in front of a million young Egyptians.",
             "A seat on the steering committee, which sets the plan and "
             "signs off the national report.",
             "A sector or a governorate group carried under their name for "
             "the whole wave.",
             "The quarterly direction report on what young Egyptians are "
             "building, by sector, governorate, gender and age, before it "
             "is published.",
             "A themed call into the ideas bank: a question put to every "
             "participant in their sector, with consented responses "
             "returned to them.",
             "Four live webinars under their name, to an audience in the "
             "tens of thousands.",
             "First look at the ventures from the national showcase.",
             "A closing report with completion rates, governorate and "
             "gender disaggregation and SDG mapping, written to go "
             "straight into their own annual report.",
         ]),
    dict(name="Partner", price=20_000.0, slots=5,
         role="CSR sponsor",
         gives="Cash.",
         benefits=[
             "Named as a Partner across the initiative's surfaces.",
             "A seat on the partner council, which meets monthly.",
             "Two live webinars under their name.",
             "The quarterly direction report.",
             "The closing report, disaggregated and SDG mapped.",
         ]),
    dict(name="Supporting Partner", price=5_000.0, slots=10,
         role="CSR sponsor",
         gives="Cash. The entry tier, and the one a mid-sized Egyptian "
               "company or a second-tier foundation can sign inside a "
               "month.",
         benefits=[
             "One of the fifteen missions carried under their name, which "
             "every participant in the country passes through.",
             "One live webinar under their name.",
             "Their sector's slice of the direction report.",
             "Named on the platform and in the closing report.",
         ]),
    dict(name="In-kind Partner", price=0.0, slots=0,
         role="CSR sponsor or NGO and development partner",
         gives="Reach, airtime, venues or services, valued at market rate "
               "and credited at the cash tier it matches.",
         benefits=[
             "Credited at the tier their contribution values at, with the "
             "same benefits.",
             "For a telecom or a broadcaster this is the most valuable "
             "thing anyone can give this initiative, because reach is what "
             "the whole model runs on, and it is usually faster to approve "
             "than cash.",
         ]),
    dict(name="Community Supporter", price=0.0, slots=0,
         role="Community supporter",
         gives="Members, chapters and leadership time. No cash is asked "
               "for, ever.",
         benefits=[
             "Every member gets the full fifteen-mission programme free, "
             "which everybody gets, because the whole thing is free.",
             "Up to 10 of their leadership trained to host info sessions "
             "and webinars, a credential they keep after their term ends.",
             "Their chapter on the national leaderboard, by registrations "
             "and by completions.",
             "Their own chapter's data: what their members are building.",
             "Teams going into their own competition season already "
             "through fifteen missions.",
         ]),
]

# ---------------------------------------------------------------- delivery
# Everything is online. There are no in-person cohorts in this wave, and
# that is the decision that makes a million possible: a cohort serves 25
# people for $3,000, and a webinar serves 20,000 for $500.
WEBINARS = 24
WEBINAR_COST = 500.0
INFO_SESSIONS = 300
INFO_SESSION_KIT = 20.0

DELIVERY_NOTE = (
    "Live webinars in Arabic, one a week for the whole wave, recorded and "
    "left on the platform. Offline info sessions happen where a partner "
    "asks for them and hosts them: their venue, their people, our kit and "
    "our training. The initiative pays for the kit and the training, not "
    "for the room.")

# Every event, and every piece of live delivery. There are no in-person
# cohorts: this is the whole of what happens in a room or on a call.
EVENTS = [
    ("National launch, Cairo", 1, 8_000.0, "March 2027",
     "The coalition on stage, the patron ministries present, the press in "
     "the room, and a million-person target announced in public, which is "
     "what makes it real."),
    ("Regional showcases", 6, 3_000.0, "May to July 2027",
     "Six regions, run with the chapters and the partners who host them. "
     "Venue, judges, prizes and media."),
    ("National demo day", 1, 7_000.0, "August 2027",
     "The best teams in the country, travelled and accommodated, in front "
     "of the coalition and the ministries. The top fifty ambassadors come "
     "too."),
    ("Partner council meetings", 6, 200.0, "Monthly",
     "One hour, one dashboard, and the room where partners meet each "
     "other."),
    ("Judge and mentor briefings", 4, 200.0, "Before each showcase",
     "Sponsor staff cannot judge well without being briefed."),
]

DELIVERY = [
    ("Live webinars in Arabic", WEBINARS, WEBINAR_COST, "Weekly",
     "One a week for the whole wave, recorded and left on the platform. "
     "A webinar serves twenty thousand people for the price of a quarter "
     "of a cohort."),
    ("Info session kits and host training", INFO_SESSIONS,
     INFO_SESSION_KIT, "On partner request",
     "Offline sessions happen where a partner asks for one and hosts it: "
     "their venue, their people, our kit and our training. We pay for the "
     "kit, not for the room."),
    ("Mission localisation and production", 1, 7_000.0, "Before the wave",
     "The fifteen missions and the review rubric, produced for an "
     "Egyptian audience rather than translated for one."),
]


def events_total():
    return sum(n * c for _, n, c, _, _ in EVENTS)


def delivery_total():
    return sum(n * c for _, n, c, _, _ in DELIVERY)


# ------------------------------------------------------------------ budget
# Six lines. The whole thing is funded by the coalition: StartPad puts in no
# cash at all, and takes no margin.
BUDGET = [
    ("Platform, AI review and hosting", 60_000.0,
     "The only line that grows with the number of entrepreneurs. A million "
     "accounts, several million mission submissions, and the review behind "
     "each one."),
    ("Content, webinars and the info session kit", 25_000.0,
     f"The fifteen missions localised, {WEBINARS} live webinars in Arabic "
     f"across the wave, and the kit that lets a partner run an info "
     f"session without us in the room."),
    ("Community: ambassadors and chapters", 30_000.0,
     "1,000 student ambassadors and 150 chapters. This is the line that "
     "produces the reach, and it is the cheapest reach in the country."),
    ("Events: launch, regional showcases, demo day", 35_000.0,
     "One national launch, six regional showcases and a national demo "
     "day. The showcase is what makes the last mission worth finishing."),
    ("Measurement, reporting and evaluation", 15_000.0,
     "The dashboard every partner sees, the direction report, the month 12 "
     "follow-up and an independent evaluation."),
    ("Programme coordination", 35_000.0,
     "A team of four for six months at Egyptian salaries: a programme "
     "manager, a community manager, a content producer and a part-time "
     "analyst."),
]


def budget_total():
    return sum(v for _, v, _ in BUDGET)


def target_money():
    """Full coalition value if every capped slot sells."""
    return sum(t["price"] * t["slots"] for t in TIERS)


# -------------------------------------------------------------- the million
# How a million is actually reached, which is not by buying it. Seed reach
# from partners and chapters, then a referral loop. The viral coefficient is
# the single riskiest number in this whole document and it is stated here so
# it can be argued with rather than buried.
SEED = [
    ("Telecom, bank and corporate partner messaging", 3, 60_000,
     "A telecom partner messaging its own base, a bank in its app, a "
     "retailer to its customers. Pure in-kind, and the largest single "
     "lever in the plan."),
    ("Community supporter chapters", 150, 1_000,
     "150 university and youth chapters inviting their own members. The "
     "highest converting channel, because the invitation comes from "
     "somebody the student knows."),
    ("Ambassadors", 1_000, 60,
     "1,000 student ambassadors with a referral code, ranked publicly on a "
     "national leaderboard."),
    ("NGO and development partner networks", 18, 3_000,
     "Branch networks, beneficiary lists and governorate programmes, "
     "mostly outside Cairo."),
    ("Mission Zero, press and organic", 1, 56_000,
     "The founder podcast clipped for short video, launch and showcase "
     "press, and organic traffic."),
]

VIRAL_K = 0.50

VIRAL_LOOPS = [
    ("The first three missions are free, for everyone, forever",
     "No sponsor, no institution, no code. The thing that spreads has to "
     "be the thing itself, and nothing spreads that asks for a credit card "
     "on the first screen."),
    ("Unlock by inviting",
     "Mission 04 opens when a founder brings two others who finish mission "
     "01. That is the referral loop, it is built into the product rather "
     "than bolted on as a campaign, and it is where the viral coefficient "
     "comes from."),
    ("A shareable card for every mission finished",
     "Arabic, designed to be posted, with the founder's name and what they "
     "built. Fifteen chances for every participant to advertise the "
     "initiative to their own network."),
    ("The chapter leaderboard",
     "Universities ranked publicly by registrations and by completions. "
     "Student organisations will compete for a ranking harder than they "
     "will work for a fee."),
    ("The ambassador leaderboard",
     "1,000 ambassadors, each with a code, ranked weekly. The top fifty go "
     "to the national demo day."),
    ("Challenge weeks",
     "Four seven-day national challenges across the wave, each with one "
     "shareable output and a deadline. A deadline is what turns a "
     "registration into a submission."),
    ("Governorate rivalry",
     "A public map, updated weekly, by registrations per thousand young "
     "people. Upper Egypt against the Delta is a better growth engine than "
     "any advertising budget."),
    ("Short video from Mission Zero",
     "Every podcast episode cut into vertical clips. Founder stories are "
     "the content that travels, and we are making it anyway."),
    ("Partner amplification on a schedule",
     "Every partner commits to a messaging calendar at signature, not when "
     "they get round to it. One telco push in week one is worth more than "
     "six months of organic."),
]

RATES = [
    ("Registered to Mission 01 complete", 0.45,
     "Free, online, no facilitator. Lower than a supported cohort would "
     "be, and honestly so."),
    ("Mission 01 to Missions 01-03 complete", 0.50,
     "The end of the free tier, and the point the referral unlock bites."),
    ("Missions 01-03 to all 15 complete", 0.12,
     "Fifteen missions is real work with no facilitator standing over "
     "anyone. Twelve per cent of a very large number is still a large "
     "number."),
    ("Ideas entering the bank, as a share of Mission 01 completers", 0.68,
     "Mission 01 is where a problem becomes a stated idea."),
    ("Ventures trading at month 12, as a share of full completers", 0.06,
     "Measured a year after the wave, and deliberately conservative "
     "because nobody held their hand."),
]


def rate(label):
    return next(v for k, v, _ in RATES if k.startswith(label))


def seed_total():
    return sum(n * per for _, n, per, _ in SEED)


def registered():
    """Seed registrations, multiplied by the referral loop."""
    return seed_total() / (1 - VIRAL_K)


def funnel():
    reg = registered()
    m01 = reg * rate("Registered to Mission 01")
    m03 = m01 * rate("Mission 01 to Missions 01-03")
    full = m03 * rate("Missions 01-03 to all 15")
    ideas = m01 * rate("Ideas entering the bank")
    trading = full * rate("Ventures trading at month 12")
    return [
        ("Seed registrations, from partners and chapters", seed_total(),
         "What the coalition's own channels produce before anybody "
         "shares anything."),
        ("Registered entrepreneurs", reg,
         f"Seed multiplied by the referral loop at a viral coefficient of "
         f"{VIRAL_K:.2f}. This is the million."),
        ("Mission 01 completed", m01,
         "The first real act of work, and the first honest number."),
        ("Missions 01 to 03 completed", m03, "The free tier finished."),
        ("All 15 missions completed", full,
         "An idea taken to a tested model, a prototype and a launch "
         "plan."),
        ("Ideas in the bank", ideas,
         "Consented, structured, and the asset the wave leaves behind."),
        ("Ventures trading at month 12", trading,
         "Measured twelve months after the wave closes, not at the end of "
         "it."),
    ]


def unit_costs():
    total = budget_total()
    f = dict((k, v) for k, v, _ in funnel())
    return [
        ("Cost per registered entrepreneur",
         total / f["Registered entrepreneurs"]),
        ("Cost per entrepreneur who finishes the free tier",
         total / f["Missions 01 to 03 completed"]),
        ("Cost per entrepreneur who finishes all 15 missions",
         total / f["All 15 missions completed"]),
        ("Cost per idea in the bank", total / f["Ideas in the bank"]),
        ("Cost per venture trading at month 12",
         total / f["Ventures trading at month 12"]),
    ]


# ----------------------------------------------------------------- in kind
INKIND = [
    ("Media and airtime", "Telecom, broadcast, outdoor",
     "Reach is the initiative's scarcest input and the cheapest thing a "
     "media owner can give. Valued at rate card.", "High"),
    ("Venues and halls", "Universities, corporates, hotels, youth centres",
     "An info session needs a room for an evening. A sponsor with branches in nine governorates can host sessions in nine governorates, and that is the whole offline footprint of this wave.", "High"),
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
     "Gets the team to the regional showcases and the winners to the demo day.", "Low"),
    ("Printing and materials", "Printing, paper, FMCG",
     "Workbooks and showcase materials.", "Low"),
    ("Catering", "FMCG, food and beverage",
     "Info sessions and showcases feed people. Easy for a food company to approve.", "Low"),
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
         "missions and an AI review on every one of them. A sponsor's "
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
         "A corporate that builds this alone pays for curriculum, platform, content and measurement before it reaches its first participant, and then reaches a few thousand people. Twenty cents a head is not a number a corporate programme can reach on its own."),
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
         "Partner staff are trained to run info sessions and to use the curriculum with their own beneficiaries. When the wave closes the organisation still has the capability and the access, which is the opposite of how most funded projects leave their implementers."),
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
         "Up to ten of a chapter's leadership are trained to host info sessions and webinars on the national standard. They keep it after their term ends, and it is the first line on a CV that is otherwise all committee titles."),
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


# The million is the wave. What comes after it is depth, not more reach.
PATH_TO_MILLION = [
    ("Wave 1", "March to August 2027", "One million registered",
     "The wave this framework covers. Free, online, viral, funded "
     "entirely by the coalition."),
    ("After the wave", "From September 2027", "Depth, not reach",
     "The question stops being how many registered and becomes how many "
     "are still building. Paid cohorts, institutional programmes and "
     "accelerator places are sold commercially to the people this wave "
     "found."),
    ("Wave 2", "2028", "The region",
     "The same model, the same coalition, run across Saudi Arabia and the "
     "wider region with the content and the loops already built."),
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
     "First approaches to the Founding and Partner tiers, and to the "
     "patron ministries. Nothing is announced until both Founding "
     "Partners have signed."),
    ("November 2026", "Patron endorsement",
     "Memoranda with the national initiative and the relevant ministries. "
     "These cost them nothing and are worth more than their money."),
    ("December 2026", "Community supporters",
     "Charters signed with the youth foundations and student "
     "organisations, and the first 1,000 ambassadors recruited. Their "
     "leadership years are already underway, so this is the right moment, "
     "not the summer."),
    ("January 2027", "Train the hosts",
     "Chapter leadership and partner staff trained to run info sessions "
     "and webinars before the wave opens, not during it."),
    ("February 2027", "Localise and load test",
     "Arabic content finalised, the platform load tested for a million "
     "accounts, the referral loop rehearsed with a partner NGO. Ramadan "
     "month; no public launch."),
]

# (label, when, title, what happens, cumulative share of registrations).
# The share is multiplied by the funnel when the document is written, so a
# month target can never drift away from the total it is a share of.
MONTHS = [
    ("Month 1", "March 2027", "Launch",
     "National launch after Eid al-Fitr. All 150 chapters and 1,000 "
     "ambassadors activate in the same week, every partner sends its first "
     "message on a committed date, and the first challenge week runs "
     "immediately. A launch that trickles does not go viral.", 0.22),
    ("Month 2", "April 2027", "The loop takes over",
     "The strongest campus month of the Egyptian year, and the month the "
     "referral unlock starts carrying more registrations than the partner "
     "channels do. Weekly webinars, the chapter leaderboard live.", 0.46),
    ("Month 3", "May 2027", "Exams, so go offline",
     "University exams run through May. Campus activity stops, so the "
     "wave moves to the NGO networks, the youth centres and partner-hosted "
     "info sessions, and the second challenge week runs in the "
     "governorates. Mid-wave report.", 0.63),
    ("Month 4", "June 2027", "Summer opens",
     "Exams end mid-month and summer begins, which is when young people "
     "have time to finish missions rather than start them. Completion "
     "becomes the number that matters, not registration.", 0.78),
    ("Month 5", "July 2027", "Regional showcases",
     "Six regional showcases run in parallel with the third challenge "
     "week. The first national read of the ideas bank goes to partners.",
     0.92),
    ("Month 6", "August 2027", "Demo day and close",
     "The national demo day, the closing report, the independent "
     "evaluation commissioned, and the decision about what comes after "
     "taken with the partners in the room.", 1.00),
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
     "StartPad is accountable for the platform, the content, the webinars and the measurement. One organisation is accountable so that when something fails there is no argument about whose it was."),
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
    ("Webinar and session reach", "Per event", "Event report",
     "Attendance, completion of the mission it supported, and the rating. A partner hosting a session keeps this one."),
    ("Direction report", "Quarterly", "Report to partners",
     "What participants are building, by sector, governorate, gender, age "
     "and stage. Partners receive it before publication."),
    ("Ventures formed", "Month 6, month 12, month 18", "Follow-up survey",
     "Registered, trading, employing, or funded. Measured after the wave "
     "closes, because measuring at the end of a programme measures "
     "enthusiasm."),
    ("Cost per outcome", "Month 6 and month 12", "Closing report",
     "Per registered entrepreneur, per free-tier completer, per full fifteen-mission completer and per venture trading. Published with the assumptions next to them."),
    ("SDG mapping", "Month 6", "Closing report",
     "SDG 4 quality education, 5 gender equality, 8 decent work and "
     "economic growth, 9 industry innovation and infrastructure, 10 "
     "reduced inequalities, with the indicator each claim rests on."),
]

RISKS = [
    ("The referral loop does not fire",
     "The single largest risk in the plan. If the viral coefficient comes "
     "in at 0.25 rather than 0.50, the wave reaches 667,000 rather than a "
     "million. Mitigated by building the loop into the product rather than "
     "running it as a campaign, by measuring it weekly from day one, and "
     "by having the partner messaging calendars committed at signature so "
     "there is a second engine.", "Measured weekly"),
    ("The coalition does not fill",
     "The capped tiers raise $250,000 and the wave needs $200,000, so "
     "there is headroom for four or five refusals. Below $140,000 the "
     "events and the ambassador programme shrink before anything that "
     "touches a participant does.", "Planned for"),
    ("Registration without completion",
     "The commonest failure in free digital programmes, and the honest "
     "expectation here: 45 per cent finish mission 01. Mitigated by "
     "challenge weeks with deadlines, by the shareable card after every "
     "mission, and by publishing the completion rate rather than the "
     "registration number as the headline.", "Mitigated"),
    ("Platform load",
     "A million accounts and several million submissions on a platform "
     "that has served thousands. Load tested in February, before the "
     "launch, with the inference cost per review as the number to watch.",
     "Tested before launch"),
    ("A partner expects exclusivity over the ideas",
     "Refused in writing, in the charter and in the sponsorship "
     "agreement. The founder owns the idea.", "Governed"),
    ("Safeguarding, with minors in an open registration",
     "An open, viral, national registration will bring under-18s whether "
     "or not it invites them. Age is asked at registration, under-18s are "
     "in the aggregate only, no identified data about them reaches any "
     "partner under any tier, and there is a named lead with a written "
     "policy.", "Governed"),
    ("Religious and academic calendar",
     "Ramadan in February, exams in May, summer from June. Built into the "
     "month plan rather than discovered in it.", "Planned for"),
    ("Cost per head rises with scale",
     "Inference is the one cost that grows with every participant. If the "
     "cost per review comes in above plan the free tier stays free and the "
     "deeper missions queue, rather than the platform line eating the "
     "events budget.", "Monitored"),
]

JOIN = [
    ("Step one, a conversation",
     "Twenty minutes. We show the platform, the direction report mock-up and the referral loop, and ask what the partner's own programme is trying to achieve. No deck."),
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
    "M": "Partner",
    "S": "Partner",
    "XS": "Supporting Partner",
}

CONTRIBUTION = {
    "CSR sponsor": "Cash or in-kind reach",
    "NGO and development partner": "Reach, networks, session hosting",
    "Community supporter": "Members, chapters, ambassadors. No cash",
}

# What each role is actually offered, in one line, for the invitation column.
OFFER = {
    "CSR sponsor":
        "A named tier in the coalition, webinars under their name, the "
        "direction report before it is published, and the closing "
        "report.",
    "NGO and development partner":
        "Their staff trained to host sessions, the method for their own "
        "beneficiaries, a shared evidence base, and a seat in the "
        "coalition.",
    "Community supporter":
        "The full programme free for every member, ten of their "
        "leadership trained as hosts, their chapter on the national "
        "leaderboard, and their own chapter's data.",
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


# ------------------------------------------------- what StartPad gets back
# StartPad puts in no cash. Not a token amount, none. The wave is funded
# entirely by the coalition, and the company takes no margin from it either.
# What it contributes is what it already owns and already pays for.
#
# Prices come from the company's financial model rather than from this
# document, so a reader who has both cannot find two different numbers for
# the same product.
from finmodel.plan import PRICES, SUBSCRIPTION            # noqa: E402

PRICE_PRO = SUBSCRIPTION["p_pro"][1]
PRICE_UNI_COHORT = PRICES["p_uni"][2][0]
PRICE_CORPORATE = PRICES["p_corp"][2][0]
PRICE_NGO = PRICES["p_ngo"][2][0]

# What share of the capped slots has to sell to fund the wave.
TARGET_FILL = 0.80


def raised(fill=None):
    return target_money() * (TARGET_FILL if fill is None else fill)


STARTPAD_CONTRIBUTION = [
    ("The platform",
     "Built, running and paid for. The initiative funds hosting and "
     "inference at a million-account scale, not the product."),
    ("The fifteen missions and the review rubric",
     "Four years of curriculum work, contributed. The initiative funds "
     "localisation and production, not the method."),
    ("The team's time",
     "Already on the payroll in the financial model. No part of the "
     "founders' or the engineers' salaries is charged to the coalition."),
    ("The brand and the coalition work",
     "Five months of approaches and memoranda before any money arrives, "
     "carried by the company because sponsorship cannot be spent before "
     "it is raised."),
]

RETURN_RATES = [
    ("Free-tier completers who buy Pro", 0.02,
     f"At ${PRICE_PRO:,.0f} a year. Two per cent of people who finished "
     f"three missions for nothing and want the rest without waiting for "
     f"a sponsor."),
    ("Info session hosts that buy a commercial programme", 0.04,
     f"At ${PRICE_UNI_COHORT:,.0f}. An institution that hosted a session "
     f"and saw its own students register is the warmest lead the company "
     f"can have."),
    ("Sponsors that continue commercially", 0.20,
     f"At ${PRICE_CORPORATE:,.0f} for a corporate or CSR programme. A "
     f"sponsor who has seen the reporting buys the programme next year "
     f"instead of sponsoring it."),
    ("NGO partners that bring a funded programme", 0.08,
     f"At ${PRICE_NGO:,.0f}. The evidence base from the wave is what wins "
     f"these."),
]


def _rr(prefix):
    return next(v for k, v, _ in RETURN_RATES if k.startswith(prefix))


def startpad_return():
    """The twelve months after the wave, at the model's own prices."""
    f = dict((k, v) for k, v, _ in funnel())
    completers = f["Missions 01 to 03 completed"]
    hosts = 120                          # distinct institutions hosting
    sponsors = sum(t["slots"] for t in TIERS) * TARGET_FILL
    ngos = 18

    subs = completers * _rr("Free-tier completers")
    progs = hosts * _rr("Info session hosts")
    corp = sponsors * _rr("Sponsors that continue")
    ngo = ngos * _rr("NGO partners")
    return [
        (f"Pro subscriptions from {completers:,.0f} free-tier completers",
         subs * PRICE_PRO,
         f"{subs:,.0f} subscriptions at ${PRICE_PRO:,.0f}"),
        ("Commercial programmes sold to info session hosts",
         progs * PRICE_UNI_COHORT,
         f"{progs:,.0f} programmes at ${PRICE_UNI_COHORT:,.0f}"),
        ("Corporate and CSR programmes from sponsors",
         corp * PRICE_CORPORATE,
         f"{corp:,.0f} programmes at ${PRICE_CORPORATE:,.0f}"),
        ("NGO and donor programmes won on the evidence base",
         ngo * PRICE_NGO,
         f"{ngo:,.0f} programme{'' if round(ngo) == 1 else 's'} at "
         f"${PRICE_NGO:,.0f}"),
    ]


def startpad_assets():
    f = dict((k, v) for k, v, _ in funnel())
    return [
        (f"{f['Registered entrepreneurs']:,.0f} registered entrepreneurs",
         f"The direct engine's entire addressable base, several times "
         f"over, acquired at ${budget_total() / f['Registered entrepreneurs']:,.2f} "
         f"a head with somebody else's money."),
        (f"{f['Ideas in the bank']:,.0f} consented ideas",
         "The ideas bank and the direction report. No competitor in Egypt "
         "has a sample remotely like it, and it is the basis of the "
         "company's own incubation product as well as a partner benefit."),
        ("A referral loop that has been run at national scale",
         "The viral mechanics in Section 12 either work or they do not, "
         "and after this wave the company will know, with a measured "
         "coefficient, which is worth more than the wave itself."),
        ("A coalition of national partners",
         "Fifteen to twenty organisations that have worked with the "
         "company for six months and have seen its reporting."),
        ("An audited delivery record at national scale",
         "What makes donor and ministry procurement possible, and what a "
         "young company cannot otherwise buy."),
    ]
