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

Twelve people, three hundred cohorts
------------------------------------
The establishment is capped at twelve in year three and twenty in year five. That
cap is the central design constraint of this plan, not an aspiration bolted onto
it. It is only possible because StartPad does not deliver cohorts itself at scale:
it certifies delivery partners, training providers, university innovation
centres, youth NGOs, and a pool of certified freelance facilitators, and employs
the people who define, audit and sell the standard. Headcount therefore grows with
the number of partners to manage, not with the number of cohorts to run.

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
#  PART 1, THE POPULATION (external figures where they exist)
# =====================================================================

# --- Higher education -------------------------------------------------
# Egypt: CAPMAS annual bulletin 2024/25, 3.9m enrolled in higher education.
# KSA:   UNESCO UIS tertiary enrolment 2022, 1.57m.
HE_STUDENTS = {"Egypt": 3_900_000, "KSA": 1_600_000}

# Egypt: 547,200 graduated in 2023 (CAPMAS via Ahram Online).
# KSA: derived from enrolment over a four-year degree, discounted 25%. ASSUMPTION.
ANNUAL_GRADUATES = {"Egypt": 547_200, "KSA": 300_000}
GRADUATE_WINDOW_YEARS = 3

# --- Technical and vocational ----------------------------------------
# Egypt technical secondary: ~2.2m (CAPMAS, 2021/22, reported via Statista). The
# Ministry reported 595,848 students passing first-term technical diploma exams in
# 2024/25 at a 70.47% pass rate, implying ~845,000 sitting, a very large annual
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
# The named examples in NAMED_COMPETITIONS are the visible top of this universe;
# most of it is single-campus and single-sponsor.
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
#  PART 1b, THE NAMED TARGETS, AND HOW TO GET INSIDE THEM
# =====================================================================
#
# Every engine in this plan is sold to specific, named organisations that already
# run the programmes StartPad would sit inside. These are named targets and the
# published evidence that the budget line exists, not signed partners, and no
# revenue in this plan is attributed to any one of them.
#
# Naming them is only half the work. A plan that lists institutions without saying
# how to get through their door is a wish list. So each row carries the route in:
# which of the six engagement plays applies, who is actually approached, what the
# first ask is, and what has to be true before that ask can be made.
#
# THE SIX ENGAGEMENT PLAYS
# ------------------------
# These are the only six ways StartPad ever enters an organisation. Everything in
# the named tables below is one of them. They are ordered by how little the
# counterparty has to risk to say yes, which is also the order in which a new
# relationship moves through them.
#
# (code, name, who is approached, the first ask, how money moves, what must be
#  true first, how long it takes)

ENGAGEMENT_PLAYS = [
    ("P1", "The funded pilot",
     "The programme manager who owns delivery, never the chief executive, who "
     "will refer it down and lose a month doing so",
     "One cohort inside a programme you already run, at our cost, with your name "
     "on the report and your logo on the showcase",
     "No invoice in either direction. StartPad carries the facilitation and "
     "materials as a sales cost of roughly one and a half thousand dollars",
     "Nothing. This is the play that manufactures the proof every other play "
     "needs, which is why it exists and why year one runs eight of them",
     "Six to ten weeks from first meeting to showcase"),

    ("P2", "The competition platform",
     "The competition's operations lead, and separately the title sponsor's CSR "
     "or marketing manager, two conversations, held in that order",
     "Run your next season's entry, team formation, mentor matching, judging and "
     "scoring on our platform, under your brand, with a build cohort for teams "
     "between rounds",
     "The sponsor pays, not the organiser. This is the single most important "
     "thing to understand about this engine: a youth organisation has no budget "
     "and a sponsor has a budget it must spend visibly",
     "One competition already run end to end, and a judging rubric a sponsor "
     "can put its name beside",
     "One season: three to five months, because competitions buy on an annual "
     "calendar and a missed cycle costs a year"),

    ("P3", "The sponsored-seat rider",
     "The funder's programme officer, and the finance officer who will ask how "
     "the per-beneficiary cost is evidenced",
     "Add a block of seats to a budget that already exists, as a line item in "
     "your programme rather than a programme of ours",
     "Per seat, invoiced to the funder in tranches against activation and "
     "completion, not against delivery of accounts",
     "A per-participant evidence record the funder's own monitoring and "
     "evaluation function will accept without re-work",
     "Nine to fifteen months for a national programme; three to six for a "
     "foundation"),

    ("P4", "The certified delivery partner licence",
     "The head of training or head of programmes at an organisation that already "
     "has facilitators, classrooms and a youth pipeline",
     "Deliver StartPad cohorts yourselves under licence. We certify your "
     "facilitators, audit the delivery and keep the standard; you keep the "
     "relationship and the larger share of the fee",
     f"Revenue share: the partner keeps 40 per cent of the cohort fee, StartPad "
     f"keeps 60 per cent and the platform. The margin given away is the margin "
     f"StartPad does not have to hire for",
     "A written certification standard, a facilitator assessment that genuinely "
     "fails people, and an audit the partner knows can withdraw the licence",
     "A certification cohort plus one supervised delivery, about one quarter"),

    ("P5", "Trainer certification",
     "The director of training inside a ministry, agency or technical "
     "corporation, whose own staff are the delivery capacity",
     "Certify your trainers to run this themselves. You stop buying delivery "
     "and start buying the standard",
     "Per certification cohort, plus per-seat licensing for every participant "
     "those trainers go on to teach, the annuity is in the seats, not the "
     "certification",
     "A train-the-trainer curriculum, and cohort reports at enough volume that "
     "a public body can defend the choice internally",
     "Two to four quarters, and it is the only play that scales a public "
     "programme past what any provider could staff"),

    ("P6", "The logframe subcontract",
     "The international organisation's programme design lead, approached six to "
     "nine months before the funding call closes, not after",
     "Name StartPad as the delivery partner for the entrepreneurship component "
     "of the proposal you are writing now",
     "A budget line inside the awarded grant, paid against indicators achieved",
     "The ability to report against outcome indicators rather than activity "
     "counts, and alignment with a methodology the donor already accepts, the "
     "ILO's Start and Improve Your Business framework being the common one",
     "Twelve to eighteen months from first conversation to first delivery, "
     "which is why this engine must be started long before it is needed"),
]

PLAY_NAMES = {code: name for code, name, *_ in ENGAGEMENT_PLAYS}


# --- Engine 3: national initiatives and government --------------------
# (organisation, market, what it already runs, what StartPad supplies,
#  plays, the route in)

NAMED_INITIATIVES = [
    ("Rowad 2030: One Million Entrepreneurs, Ministry of Planning and Economic "
     "Development", "Egypt",
     "A state-backed programme to qualify one million entrepreneurs by 2030, "
     "delivered as a three-stage online curriculum with the Rowad Meter data "
     "platform tracking participants. Universities including Alexandria "
     "University have signed protocols funding seats for their own students, and "
     "AUC Venture Lab has run training under the programme with the Drosos "
     "Foundation.",
     "The build-and-pitch stage the online curriculum does not have: seats, "
     "missions, a bilingual AI mentor, and a per-participant evidence record the "
     "Rowad Meter can ingest.",
     "P1 > P3 > P5",
     "Do not approach the ministry first. Approach a university that has already "
     "signed a Rowad protocol and run a funded pilot (P1) for its students on "
     "the programme, so the first ministry conversation opens with a completed "
     "cohort inside their own initiative rather than a proposal about it. Take "
     "the report to the programme's delivery unit with one ask: a priced seat "
     "block for one governorate (P3). The destination is trainer certification "
     "(P5), a million seats cannot be facilitated by any provider, so the only "
     "version of this that reaches the stated target is one where the "
     "programme's own trainers are certified."),

    ("Micro, Small and Medium Enterprise Development Agency (MSMEDA)", "Egypt",
     "Governorate-level enterprise development and a national network of service "
     "centres reaching first-time owners far outside Cairo.",
     "A single platform standard across governorates, so a participant in Sohag "
     "and a participant in Alexandria are assessed the same way, plus "
     "certification for the agency's own field staff.",
     "P1 > P5 > P3",
     "Enter through one governorate branch, not head office. The branch manager "
     "can authorise a pilot; head office cannot authorise anything without a "
     "precedent. Run two funded cohorts in a governorate outside Cairo, the "
     "geography is the point, because the agency's internal problem is that "
     "quality collapses away from the capital. Certify that branch's own field "
     "officers (P5), then let the comparison between a certified branch and an "
     "uncertified one make the case at head office for a seat block (P3)."),

    ("Ministry of Communications and Information Technology, and ITIDA", "Egypt",
     "National digital-skills and youth-innovation programmes, including "
     "patronage of school-level competitions such as Startup Teen.",
     "A venture-building layer on top of digital skills, so a trained young "
     "person leaves with a tested idea rather than a certificate.",
     "P2 > P3",
     "The route is through the competitions the ministry already patronises "
     "rather than through the ministry. Win the platform role on one patronised "
     "competition (P2); the ministry's name is already on it, so the pilot is "
     "effectively a public-sector reference without a public-sector sales cycle. "
     "Convert that into a seat rider on a digital-skills programme (P3) at the "
     "next budget cycle."),

    ("Central Bank of Egypt: the FinYology initiative", "Egypt",
     "A university financial-technology initiative spanning more than thirty "
     "Egyptian universities, with the FinTech Got Talent competition as its "
     "annual showcase.",
     "The structured pre-competition cohort: the eight weeks in which a student "
     "team actually builds something worth judging.",
     "P1 > P2",
     "Enter at one participating university, through the faculty staff member "
     "who manages its FinYology involvement, with a funded build cohort (P1) "
     "ahead of the competition. Teams that went through a cohort and teams that "
     "did not are visibly different at the pitch, and that difference is the "
     "entire argument. Take it to the initiative's organisers as a platform "
     "proposal for the following season (P2), funded by one of the participating "
     "banks rather than by the central bank itself."),

    ("Ministry of Technical Education and Training: applied technology schools",
     "Egypt",
     "A reform programme converting technical secondary schools into applied "
     "technology schools with employer partnerships.",
     "The five-day technical variant of the curriculum, and an employability "
     "record the school can show an employer partner.",
     "P1 > P5",
     "Enter through a single applied technology school with an active employer "
     "partner, because that employer is the one who will say the graduates are "
     "not ready, and that complaint is the opening. Run a funded cohort (P1), "
     "then certify the school's own workshop instructors (P5), they already "
     "teach practical work and are a better fit for this curriculum than an "
     "academic. Safeguarding clearance must be in place before the first school "
     "visit, not negotiated during it."),

    ("Monsha'at: the Small and Medium Enterprises General Authority", "KSA",
     "Monsha'at Academy, an online academy that has run more than two hundred "
     "training events, bootcamps, workshops and self-paced programmes, across "
     "planning, finance, marketing, e-commerce and franchising.",
     "The missing practice layer: a cohort format, a mentor and a judged "
     "showcase that turns a completed course into a tested venture.",
     "P1 > P3",
     "The academy's own catalogue is the opening, because a two-hundred-course "
     "catalogue with no build stage has a completion problem its managers "
     "already know about. The country manager approaches the academy's "
     "programmes lead with a funded cohort (P1) run as the capstone to an "
     "existing Monsha'at course, measured on one number: how many participants "
     "finish with something. Price a seat block against that (P3). A Saudi "
     "entity and a Saudi bank account are prerequisites, not afterthoughts."),

    ("Misk Foundation", "KSA",
     "A youth foundation working in education and entrepreneurship since 2011, "
     "running its own programmes and partnered competitions including the MISK "
     "SDG Innovation Competition with UNDP.",
     "Cohort delivery and assessment infrastructure for Saudi youth programmes, "
     "in Arabic, with a comparable score across every cohort.",
     "P2 > P3",
     "Approach through the competition rather than the foundation: the SDG "
     "Innovation Competition has a UN partner, which means it already reports "
     "against indicators and therefore already has the problem StartPad solves "
     "(P2). Arabic-first delivery is not a feature here but an entry "
     "requirement; an English-led pitch will not survive the first meeting. A "
     "funded programme follows (P3)."),

    ("Technical and Vocational Training Corporation (TVTC)", "KSA",
     "336,150 trainees across 314 institutions in 2024, under a Vision 2030 "
     "mandate to connect training to employment and self-employment.",
     "A self-employment track inside the technical diploma, delivered by TVTC's "
     "own trainers once certified.",
     "P1 > P5",
     "This is a certification sale from the beginning, at 314 institutions, no "
     "external provider could ever staff it, and proposing to would signal "
     "misunderstanding. Run one funded cohort at a single college in Riyadh (P1) "
     "with the explicit framing that it is a certification pilot, then price "
     "trainer certification by region (P5). The annuity is the per-seat licence "
     "behind each certified trainer, not the certification fee."),

    ("Human Resources Development Fund (Hadaf) and the Social Development Bank",
     "KSA",
     "Subsidised training and finance for Saudi job-seekers and micro-enterprise "
     "owners, with per-beneficiary funding already in place.",
     "A readiness assessment before finance is advanced, the lender's own "
     "screening problem, solved as a by-product of the cohort.",
     "P3",
     "Lead with the lender's problem, not the learner's: default rates on "
     "micro-enterprise lending are a function of how ready the borrower was, and "
     "a cohort score is a screening instrument. Approach the credit or programme "
     "function with a seat rider on an existing subsidised cohort (P3), priced "
     "per beneficiary against the funding already allocated."),
]


# --- Engine 5: sponsored competitions ---------------------------------

NAMED_COMPETITIONS = [
    ("Enactus Egypt National Competition", "Egypt",
     "Thirty to thirty-five university teams reach the national finals each "
     "year, from a wider pool of campus entrants. Orange Egypt has sponsored it "
     "for seventeen consecutive years; ExxonMobil Egypt is a long-standing "
     "supporter.",
     "The qualification and judging layer, plus a build cohort for teams between "
     "the campus round and the national final.",
     "P1 > P2 > P4",
     "Start at one campus team, not at the national office. A university Enactus "
     "team is run by students who want to win and have no budget, which makes a "
     "funded build cohort (P1) an easy yes and a visible result at the national "
     "final. With one campus result, approach the national office for the "
     "platform role across the season (P2) and Orange Egypt's CSR function "
     "separately for the funding, the sponsor has renewed for seventeen years "
     "and needs new substance to renew against, which is the actual sale. "
     "Long-term, Enactus Egypt is a certified delivery partner (P4): it has "
     "campus presence StartPad will never build."),

    ("INJAZ Egypt: the Company Program and the Youth Entrepreneurship "
     "Celebration", "Egypt",
     "A six-month student venture programme with separate school and university "
     "tracks, culminating in an annual celebration now in its nineteenth edition "
     "and feeding the regional INJAZ Al-Arab final.",
     "Platform delivery of the six-month programme, mentor matching at scale, "
     "and a comparable score across both tracks.",
     "P1 > P4",
     "INJAZ's constraint is mentor matching: a corporate volunteer base that has "
     "to be paired with hundreds of student companies by hand, every cycle. Lead "
     "with that, not with curriculum, INJAZ has curriculum. Run one funded "
     "track (P1) with platform mentor matching, then move directly to a "
     "certified delivery partner licence (P4) rather than selling cohorts: "
     "INJAZ has the schools, the universities, the volunteers and the regional "
     "network, and is worth far more as a partner than as a customer."),

    ("Startup Teen (iSchool), under the patronage of the Ministry of "
     "Communications and Information Technology", "Egypt",
     "A school-age competition for thirteen to eighteen year-olds combining "
     "entrepreneurship with artificial intelligence; its first edition drew more "
     "than eight hundred students from forty schools in a hundred and forty "
     "teams.",
     "The school variant of the curriculum as the competition's training track, "
     "and safeguarded platform accounts for minors.",
     "P2",
     "A first-edition competition needs a second edition that looks more "
     "substantial than the first, and its organiser is a commercial education "
     "company that will recognise a platform proposition immediately (P2). The "
     "unlock is not the curriculum but compliance: age-appropriate accounts, "
     "parental consent, moderated mentor contact and safeguarded data. Bring "
     "that to the first meeting. Forty schools reached through one competition "
     "is the cheapest route into the school engine that exists."),

    ("FinTech Got Talent: Central Bank of Egypt FinYology initiative", "Egypt",
     "A university competition in its third edition, reaching across more than "
     "thirty Egyptian universities.",
     "The eight-week build cohort that precedes the pitch, run identically on "
     "every participating campus.",
     "P1 > P2",
     "Enter campus by campus with funded build cohorts (P1), then sell the "
     "season (P2) with one of the participating banks as sponsor. The argument "
     "is standardisation: thirty universities currently prepare teams thirty "
     "different ways, so the competition cannot tell a good team from a "
     "well-coached one."),

    ("Egypt Entrepreneurship Rally", "Egypt",
     "Run with the Arab Academy for Science, Technology and Maritime Transport "
     "and sponsored by the National Bank of Egypt since 2019.",
     "Entry management, team formation and judging, plus the sponsorship impact "
     "report the bank needs and does not currently get.",
     "P2",
     "The sponsor is the customer. A bank that has funded the same event for "
     "six years has an internal reporting problem, it cannot evidence what the "
     "money produced beyond attendance. Approach the bank's CSR or marketing "
     "function with the impact report as the product and the platform as the "
     "means of producing it (P2), and bring the academy in as co-signer rather "
     "than as buyer."),

    ("Rowad Domiat", "Egypt",
     "A governorate competition run by the International Labour Organization "
     "with ICSB and backed by Methanex Egypt, built on the ILO's Start and "
     "Improve Your Business methodology.",
     "A platform record that maps onto the ILO methodology, so the donor's "
     "framework and StartPad's missions report the same thing.",
     "P2 > P6",
     "This one is a bridge, not a revenue target. Winning the platform role on a "
     "small governorate competition (P2) buys something disproportionate: a "
     "working relationship with an ILO country programme and a demonstrated "
     "mapping to the Start and Improve Your Business framework. That mapping is "
     "the entry ticket to the logframe subcontract play (P6) across every donor "
     "that uses the same methodology, which is most of them."),

    ("Hult Prize on-campus programme", "Egypt and KSA",
     "A global student competition run through university chapters, with campus "
     "rounds feeding regional finals.",
     "The on-campus round delivered as a StartPad cohort: a chapter receives a "
     "programme instead of organising one.",
     "P1 > P4",
     "Campus chapters are run by student organisers with no budget and a hard "
     "deadline, which makes a delivered programme (P1) genuinely welcome. The "
     "value is not the fee but the door: a Hult chapter sits inside a university "
     "that has not yet bought anything, and a successful campus round is the "
     "warmest possible introduction to that university's entrepreneurship "
     "centre. Chapters that run it twice become certified (P4)."),

    ("MISK SDG Innovation Competition", "KSA",
     "A Misk Foundation competition run with UNDP on sustainable-development "
     "themes.",
     "Arabic-first cohort delivery and judging, with an impact record a UN "
     "partner can report against.",
     "P2 > P6",
     "A competition with a UN co-organiser is two engines at once: the "
     "competition itself (P2) and a relationship with a UNDP country office "
     "that commissions programmes (P6). Approach the foundation's programme "
     "lead and the UNDP focal point in the same week, with the same material, "
     "framed differently, the foundation buys a better competition, the UN "
     "office buys measurable indicators."),

    ("Entrepreneurship World Cup: Saudi national round", "KSA",
     "A global competition with a national Saudi round reaching students and "
     "early-stage founders.",
     "National-round qualification, plus a build track for entrants who arrive "
     "with an idea rather than a venture.",
     "P2",
     "The national round's organiser has a quality problem at the top of the "
     "funnel: most entrants are not ready to be judged. Sell the build track as "
     "the fix (P2), funded by a national sponsor. It is also the fastest "
     "credibility purchase available in the Saudi market, because the brand is "
     "recognised and the national round is small enough to influence."),
]


# --- Engines 2, 4, 6 and 7: delivery partners, donors and sponsors ----

NAMED_PARTNERS = [
    ("INJAZ Egypt and INJAZ Al-Arab", "Egypt and the Arab region",
     "A youth employability and entrepreneurship network with school and "
     "university tracks and a corporate volunteer mentor base.",
     "Certified delivery partner, running StartPad cohorts inside its own "
     "programmes, and the single highest-value partnership in this plan.",
     "P4",
     "Begin with the mentor-matching problem, prove it on one track, then "
     "negotiate a network licence rather than a per-cohort price. The regional "
     "network is the prize: a licence signed in Cairo is a route into nine other "
     "country offices without nine other sales processes."),

    ("Enactus Egypt", "Egypt",
     "A university social-entrepreneurship network with teams on dozens of "
     "campuses and long-standing corporate sponsors.",
     "Channel partner for the competition engine and, later, a certified "
     "delivery partner with its own campus footprint.",
     "P2 > P4",
     "Campus team first, national office second, sponsor third. Never reverse "
     "that order: the national office will ask what campus has done it, and the "
     "sponsor will ask what the national office thinks."),

    ("AUC Venture Lab", "Egypt",
     "A university-based accelerator, a partner of the Drosos Foundation and a "
     "collaborator on Rowad 2030 training programmes.",
     "Programme-seat partner, and the reference institution that makes every "
     "subsequent faculty licence easier to sell.",
     "P1 > P3",
     "Approach as a peer, not a vendor: V-Lab selects and accelerates, and does "
     "not need a curriculum. The offer is pre-acceleration, seats for the "
     "applicants it rejects, who are not bad founders but unready ones. That "
     "turns a rejection list into a pipeline and costs V-Lab nothing."),

    ("Sawiris Foundation for Social Development", "Egypt",
     "A major Egyptian foundation funding education and employability at scale.",
     "Funder of sponsored seats for students who cannot pay, through the NGO and "
     "donor engine.",
     "P3",
     "Approach with a seat block attached to a programme the foundation already "
     "funds, not a new programme. Foundations fund gaps in things they are "
     "already committed to far more readily than they fund new commitments."),

    ("Misr El Kheir Foundation", "Egypt",
     "A national foundation with a wide governorate footprint in education and "
     "community development.",
     "Certified delivery partner outside Cairo, where StartPad has no presence "
     "of its own and should not try to build one.",
     "P4",
     "This is a geography partnership. Lead with coverage: the foundation has "
     "staff in governorates StartPad cannot reach, and StartPad has a standard "
     "the foundation's programmes currently lack. Certify its field educators "
     "and audit on sample."),

    ("Drosos Foundation", "Egypt",
     "Funds youth economic-inclusion programmes, including work with AUC Venture "
     "Lab under the Rowad 2030 umbrella.",
     "Donor-funded programme buyer, and a bridge between the university engine "
     "and the national initiative engine.",
     "P6 > P3",
     "Enter through a grantee rather than the foundation: become the delivery "
     "component of a proposal an existing grantee is writing (P6). A foundation "
     "meets its best delivery partners through the organisations it already "
     "funds."),

    ("Life Makers Foundation", "Egypt",
     "A large youth volunteer and development organisation with branches across "
     "the governorates.",
     "Certified delivery partner, and the primary recruitment channel for the "
     "campus ambassador network.",
     "P4",
     "Two asks in one conversation: certify a first group of facilitators from "
     "its volunteer base, and open its branches to ambassador recruitment. The "
     "second costs nothing and makes the first worth more to both sides."),

    ("Nahdet El Mahrousa", "Egypt",
     "An incubator for social enterprises with a long track record and a "
     "selective intake.",
     "Programme-seat partner, supplying the structured pre-incubation its "
     "applicants lack.",
     "P3",
     "Same pre-acceleration argument as the V-Lab route, priced per seat. A "
     "selective incubator's rejection list is its most underused asset."),

    ("International Labour Organization: Start and Improve Your Business",
     "Egypt and the region",
     "A standard enterprise-training methodology used by governments and donors "
     "across the region, already visible in Egypt through Rowad Domiat.",
     "Methodology alignment, so a StartPad cohort reports in language donors "
     "already accept.",
     "P6",
     "Not a customer: a standard to be compatible with. Publish an explicit "
     "mapping between StartPad missions and the methodology's modules, have it "
     "reviewed by a certified trainer, and put it in every donor proposal. The "
     "mapping costs one quarter of curriculum work and removes the most common "
     "objection in donor procurement."),

    ("GIZ, UNDP, UNICEF and the British Council", "Egypt and KSA",
     "Multi-year youth employability and entrepreneurship portfolios with "
     "published logframes and procurement calendars.",
     "Programme buyer through the NGO and donor engine, on grant cycles that "
     "must be entered long before they open.",
     "P6",
     "Work the design phase, not the tender. Track each organisation's published "
     "portfolio, identify components being designed six to nine months out, and "
     "get named in the proposal. Responding to a published tender means "
     "competing on price against incumbents who helped write it."),

    ("Orange Egypt, ExxonMobil Egypt, the National Bank of Egypt and Banque Misr",
     "Egypt",
     "Established sponsors of youth entrepreneurship competitions and CSR "
     "programmes, several for more than a decade.",
     "Sponsors of competitions and of seats, through the commercial engines.",
     "P2 > P3",
     "Sell reporting, not goodwill. A sponsor renewing a decade-old commitment "
     "needs to show its board something new, and currently receives attendance "
     "figures and photographs. Offer a named season, a measurable outcome per "
     "participant and a report it can publish, then ask for the seat block as "
     "the second-year extension."),

    ("Monsha'at Academy", "KSA",
     "The Saudi SME authority's training arm, with a large catalogue and no "
     "practice layer.",
     "Platform partner for the build stage that follows a course.",
     "P1 > P3",
     "Attach to a specific existing course as its capstone, measured on "
     "completion and on ventures started. Do not propose a parallel programme; "
     "the academy's managers are judged on their own catalogue, not on "
     "somebody else's."),
]

# What StartPad must be able to show before each play can be run at all. The
# plan's sequencing exists to produce these in this order.
ENGAGEMENT_PREREQUISITES = [
    ("A completed cohort with a named institution on the report",
     "P1", "Q4 2026", "Eight funded pilots in the Land and Prove quarters exist "
     "for exactly this reason"),
    ("A judging rubric and competition flow on the platform",
     "P2", "Q1 2027", "Built during the Prove quarter against the first "
     "competition, which runs with manual support"),
    ("A per-participant evidence record in a format an M&E officer accepts",
     "P3", "Q2 2027", "Designed with the first NGO programme, which is bought "
     "partly to force this into existence"),
    ("A written certification standard, assessment and audit regime",
     "P4", "Q3 2027", "The first certified delivery partner cannot be signed "
     "before the standard that certifies it exists"),
    ("A train-the-trainer curriculum and cohort reports at volume",
     "P5", "Q3 2027", "The first train-the-trainer cohorts run alongside the "
     "first initiative seats"),
    ("A published mapping to the ILO Start and Improve Your Business methodology",
     "P6", "Q2 2027", "One quarter of curriculum work that unlocks donor "
     "procurement across the region"),
]


# =====================================================================
#  PART 1c, MISSION ZERO: THE FOUNDER PODCAST
# =====================================================================
#
# The podcast is in this plan as a demand-generation asset with a measurable job,
# not as brand decoration. It does three things no advertisement does: it gives a
# dean a reason to say yes (their students on camera), it gives a sponsor a
# deliverable (a named episode), and it produces curriculum material as a
# by-product (each episode is mapped to the mission it illustrates).

PODCAST = dict(
    name="Mission Zero",
    arabic="المهمة صفر",
    premise="A first-time founder walks through the one decision that nearly ended "
            "the venture, the mission they got wrong, and what they would do "
            "differently. No success stories; the failure is the content.",
    format=[
        ("Length", "Thirty to thirty-five minutes, video-first, published as video, "
                   "audio and a written mission note"),
        ("Language", "Arabic as the default, with English episodes for regional and "
                     "international guests, both subtitled in the other language"),
        ("Cadence", "Weekly within a season; twelve episodes a season, three seasons "
                    "a year with production breaks between them"),
        ("Guests", "Two in three are first-time founders two to five years in; one in "
                   "three are the people who decide, a dean, a programme director, "
                   "an investor, a judge"),
        ("The student segment", "Every episode closes with one cohort team pitching "
                                "to the guest for eight minutes, filmed on their own "
                                "campus"),
        ("Where it is made", "Recorded on campus during cohort weeks and at partner "
                             "events, not in a studio, so each episode carries the "
                             "institution's name"),
    ],
    distribution=[
        ("YouTube", "The primary home: full episodes, chapters, and the student pitch "
                    "published separately"),
        ("Spotify and Apple Podcasts", "Audio, for the commute audience that becomes "
                                       "the subscription audience"),
        ("Instagram, TikTok and LinkedIn", "Six to eight vertical clips per episode; "
                                           "LinkedIn carries the decision-maker cut"),
        ("The platform itself", "Episodes attached to the mission they illustrate, so "
                                "a learner stuck on pricing is handed the episode "
                                "about pricing"),
    ],
    # (metric, Y1 ... Y5). Episodes follow the seasons the financial model
    # actually funds, twelve to a season, so the podcast plan cannot promise
    # more episodes than the production budget pays for.
    targets=[
        ("Episodes published", 12, 24, 36, 36, 36),
        ("Founders featured", 8, 16, 24, 24, 24),
        ("Student teams featured on camera", 12, 24, 36, 36, 36),
        ("Partner institutions named in an episode", 10, 24, 40, 56, 72),
        ("Average views per episode", 4_000, 12_000, 30_000, 46_000, 60_000),
        ("Inbound institutional enquiries credited to it", 18, 55, 130, 190,
         240),
        ("Episodes mapped into the curriculum as mission material", 12, 36, 72,
         108, 144),
    ],
    # Why it earns its budget, in the order the effects arrive.
    chain=[
        ("A founder tells the truth about one bad decision",
         "The content is credible because it is not promotional"),
        ("A cohort team pitches to that founder, on their own campus",
         "The institution gets visible proof its students were taken seriously"),
        ("The institution shares the episode itself",
         "Distribution StartPad does not pay for, to exactly the right audience"),
        ("A dean at a neighbouring faculty sees it",
         "The next institutional conversation opens warm, not cold"),
        ("A sponsor asks to attach their name to a season",
         "The asset becomes partly self-funding through the commercial engines"),
        ("The episode is attached to the mission it illustrates",
         "Marketing spend turns into curriculum the platform keeps"),
    ],
)


# =====================================================================
#  PART 2, PRICING (assumptions, with reasoning)
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
#  PART 3, SAM FILTERS (assumptions, with reasoning)
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
#  PART 4, THE QUARTERLY PLAN
# =====================================================================
#
# Twelve quarters. Everything downstream is summed from here, so a ramp cannot be
# assumed away and an engine cannot earn revenue before its gate opens.
#
# The volumes below are bounded twice over: by the gates, and by the certified
# delivery capacity in the same table. No quarter schedules more cohorts than the
# partner network and facilitator pool of that quarter can physically run.

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
    "uni_cohorts_eg":  [0, 4,  7,  9,  11, 13, 15, 17,  20, 23, 25, 28],
    "uni_cohorts_ksa": [1, 2,  3,  4,   5,  5,  6,  6,   8,  9, 10, 11],
    "uni_pilots":      [4, 2,  1,  1,   1,  1,  1,  1,   1,  1,  1,  1],
    "uni_licences":    [0, 0,  0,  1,   1,  1,  2,  2,   3,  3,  4,  4],

    # --- Engine 2: schools and technical education
    "school_cohorts":  [0, 0,  3,  6,   9, 12, 14, 16,  20, 24, 26, 30],
    "school_licences": [0, 0,  0,  0,   1,  1,  2,  2,   3,  3,  4,  4],
    "tvet_cohorts":    [0, 0,  0,  2,   4,  5,  7,  8,  10, 12, 13, 15],

    # --- Engine 3: national initiatives
    "initiative_seats": [0, 0, 0, 2_000,
                         3_000, 4_000, 6_000, 8_000,
                         12_000, 15_000, 18_000, 20_000],
    "tot_cohorts":     [0, 0,  0,  1,   1,  2,  2,  3,   4,  5,  5,  6],

    # --- Engine 4: NGO, donor and foundation programmes
    "ngo_programmes":  [0, 0,  1,  1,   2,  2,  3,  3,   4,  4,  5,  5],

    # --- Engine 5: sponsored competitions
    "competitions":    [0, 1,  1,  2,   2,  2,  3,  3,   4,  4,  5,  5],

    # --- Engine 6: corporate and CSR
    "corporates":      [0, 0,  0,  1,   1,  1,  1,  1,   2,  2,  2,  3],

    # --- Engine 7: programme and incubator seats (new partners signed)
    "programmes":      [0, 2,  3,  4,   5,  6,  7,  8,  10, 11, 12, 13],
    "seats_each":      [60, 60, 60, 60, 70, 70, 70, 70, 80, 80, 80, 80],

    # --- The delivery network: a stock, not a flow. These are cumulative counts
    #     at the end of each quarter, and they are what makes a twelve-person
    #     company able to stand behind three hundred cohorts a year.
    "delivery_partners":     [0, 1,  2,  3,   5,  6,  8,  9,  10, 11, 12, 13],
    "certified_facilitators": [8, 12, 18, 24, 30, 36, 42, 48, 54, 60, 68, 76],
}

# Series that are stocks rather than flows, and must never be summed over a year.
STOCK_KEYS = {"delivery_partners", "certified_facilitators", "seats_each"}

# Each engine's first revenue quarter, and what must be true before it opens.
# The index is into QUARTERS; a plan that puts revenue earlier than its gate is a
# plan that has not been thought through.
ENGINE_GATES = [
    ("University cohorts", 0,
     "Eight certified facilitators, the curriculum in both languages, and the "
     "programme admin workspace",
     "KSA pays from the first quarter through programme partners; Egypt runs free "
     "pilots in the Land quarter and sells from the Prove quarter on their reports"),
    ("Faculty licences", 3,
     "Two completed cohorts at the same institution, and an automatic cohort report",
     "A dean buys a faculty-wide licence off two reports, not off a pitch. The "
     "earliest an institution that piloted in Q4 2026 can reach that is Q3 2027"),
    ("School and technical cohorts", 2,
     "A school variant of the curriculum, four days, larger groups, an "
     "employability frame, plus safeguarding and parental consent",
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
     "The longest cycle of any engine, nine to fifteen months from first meeting "
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
     "Subscriptions lag the engines that produce them by a quarter, a student "
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
    ("Students from university cohorts",         750,  1_950,  3_350, 0.120),
    ("School and technical education students",  330,  2_250,  4_500, 0.020),
    ("Entrants in sponsored competitions",     2_000,  5_000,  9_000, 0.060),
    ("Participants on sponsored seats",        2_000, 21_000, 65_000, 0.030),
    ("NGO and corporate programme participants", 540,  2_800,  5_400, 0.045),
    ("Programme and incubator participants",     540,  1_960,  3_680, 0.055),
    ("Organic: Mission Zero, content, community",
                                               3_200, 11_000, 26_000, 0.050),
]


# =====================================================================
#  PART 5, DIRECT COST OF DELIVERY
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

# A certified facilitator works part-time: this is the share of a full delivery
# year any one of them actually gives StartPad. It is why the pool is large and
# the payroll is not. ASSUMPTION.
FACILITATOR_UTILISATION = 0.45

# A certified delivery partner organisation, a training provider, a university
# innovation centre, a youth NGO, runs this many cohorts a year once it is past
# its own certification year. ASSUMPTION, set low on purpose.
COHORTS_PER_PARTNER = 9

# What one StartPad employee can actually hold. These two ratios are the whole
# argument for a twelve-person company, so they are stated rather than implied.
PARTNERS_PER_NETWORK_MANAGER = 7
COHORTS_PER_COORDINATOR = 120

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

# What a certified partner keeps of a cohort it delivers under licence. The margin
# StartPad gives away is the margin it does not have to hire for.
PARTNER_REVENUE_SHARE = 0.40


# =====================================================================
#  PART 6, HEADCOUNT (the HR plan, costed)
# =====================================================================
#
# (function, role, monthly fully-loaded USD, Y1, Y2, Y3, Y4, Y5)
#
# The establishment is capped: six in year one, nine in year two, TWELVE in year
# three, sixteen in year four, twenty in year five. Four rules hold it there.
#
#   1.  Employ the people who define and audit the standard. Contract the people
#       who deliver it. Every cohort in this plan is run by a certified freelance
#       facilitator or a certified partner organisation, never by an employee, so
#       cohort growth cannot become payroll growth.
#   2.  No role is created until it is genuinely full-time. Until then it is part
#       of a larger role, and the role description says so, and says when it splits.
#   3.  Functions that are standard and regulated, bookkeeping, payroll, audit,
#       legal, the KSA entity's compliance, are bought from firms, not hired.
#       They appear in operating costs, not on the establishment.
#   4.  The CEO carries operations until the partner network outgrows one person,
#       which the plan puts in year four. That is when the COO arrives, and not
#       before.
#
ROLES = [
    ("Leadership", "Chief Executive Officer",
     3_000, 1, 1, 1, 1, 1),
    ("Leadership", "Chief Technology Officer",
     3_000, 1, 1, 1, 1, 1),
    ("Leadership", "Chief Operating Officer",
     3_200, 0, 0, 0, 1, 1),

    ("Product and Engineering", "Senior full-stack engineer",
     2_400, 1, 2, 2, 2, 2),
    ("Product and Engineering", "AI and data engineer",
     2_800, 0, 0, 0, 1, 1),
    ("Product and Engineering", "Product designer",
     1_800, 0, 0, 0, 0, 1),

    ("Curriculum and Delivery", "Head of Curriculum and Certification",
     2_400, 1, 1, 1, 1, 1),
    ("Curriculum and Delivery", "Partner network manager",
     2_000, 0, 1, 1, 1, 1),
    ("Curriculum and Delivery", "Programme delivery coordinator",
     1_500, 0, 0, 1, 2, 2),
    ("Curriculum and Delivery", "Bilingual curriculum producer",
     1_300, 0, 0, 0, 0, 1),

    ("Institutional Partnerships", "Head of Partnerships, Egypt",
     2_200, 1, 1, 1, 1, 1),
    ("Institutional Partnerships", "Country Manager, KSA (Riyadh)",
     5_000, 0, 1, 1, 1, 1),
    ("Institutional Partnerships", "Head of Government, Initiatives and Donors",
     2_600, 0, 0, 1, 1, 1),
    ("Institutional Partnerships", "Partnerships and bids associate",
     1_200, 0, 0, 1, 1, 1),
    ("Institutional Partnerships", "Head of Schools and Technical Education",
     2_200, 0, 0, 0, 1, 1),
    ("Institutional Partnerships", "Account manager, renewals",
     1_600, 0, 0, 0, 0, 1),

    ("Growth and Content", "Head of Growth and Content",
     2_000, 1, 1, 1, 1, 1),
    ("Growth and Content", "Student success (bilingual)",
     900, 0, 0, 0, 0, 1),
]

HEADCOUNT_CAP = {1: 6, 2: 9, 3: 12, 4: 16, 5: 20}

# Functions deliberately bought rather than hired, and from whom.
OUTSOURCED = [
    ("Bookkeeping, payroll and statutory filing",
     "A Cairo accounting firm, with a Riyadh counterpart for the Saudi entity",
     "Monthly retainer. Hiring a finance manager before year five would cost more "
     "than the firm and deliver less compliance cover."),
    ("Audit, corporate legal and the KSA entity",
     "Regional firms on fixed scopes",
     "Needed a few weeks a year at a standard no single hire could match."),
    ("Video production and editing for Mission Zero",
     "A freelance two-person crew per shoot day, briefed by the Head of Growth "
     "and Content",
     "Production is bursty: three recording blocks a year. A staff videographer "
     "would be idle most of it."),
    ("Arabic copy-editing and translation quality assurance",
     "A certified freelance panel",
     "Volume arrives in waves with each curriculum release."),
    ("Facilitation, in every market and every format",
     "The certified facilitator pool and certified partner organisations",
     "This is the central design choice of the company: the people who deliver "
     "are certified, not employed."),
    ("Safeguarding training and background checks for school work",
     "An accredited provider in each market",
     "A legal obligation that must be externally attested to be worth anything."),
]

RAMP = {1: 0.62, 2: 0.85, 3: 0.90, 4: 0.92, 5: 0.94}

AMBASSADORS = {1: 60, 2: 160, 3: 340}
AMBASSADOR_STIPEND_MONTH = 25.0
AMBASSADOR_ACTIVE_MONTHS = 7

B2B_COMMISSION = 0.06

DEMAND_SPEND = {
    1: [("Mission Zero: production, editing and distribution", 26_000),
        ("Ambassador network", 10_500),
        ("Conferences, events and ecosystem presence", 20_000),
        ("Targeted digital: retargeting and event fill", 10_000),
        ("Collateral, case studies and cohort reports", 10_000),
        ("Sector research and the annual readiness report", 12_000)],
    2: [("Mission Zero: production, editing and distribution", 48_000),
        ("Ambassador network", 28_000),
        ("Conferences, events and ecosystem presence", 52_000),
        ("Targeted digital: retargeting and event fill", 24_000),
        ("Collateral, case studies and cohort reports", 22_000),
        ("Sector research and the annual readiness report", 24_000)],
    3: [("Mission Zero: production, editing and distribution", 96_000),
        ("Ambassador network", 59_500),
        ("Conferences, events and ecosystem presence", 118_000),
        ("Targeted digital: retargeting and event fill", 56_000),
        ("Collateral, case studies and cohort reports", 48_000),
        ("Sector research and the annual readiness report", 52_000)],
}

OTHER_COSTS = {
    1: [("Cloud, AI inference and third-party APIs", 28_000),
        ("Software and tooling", 16_000),
        ("Travel: Cairo, Riyadh, campuses and governorates", 38_000),
        ("Outsourced finance, legal, audit and the KSA entity", 46_000),
        ("Safeguarding, child protection and compliance", 14_000),
        ("Office: Cairo, plus a Riyadh desk", 26_000)],
    2: [("Cloud, AI inference and third-party APIs", 92_000),
        ("Software and tooling", 34_000),
        ("Travel: Cairo, Riyadh, campuses and governorates", 112_000),
        ("Outsourced finance, legal, audit and compliance", 64_000),
        ("Safeguarding, child protection and compliance", 30_000),
        ("Offices: Cairo and Riyadh", 62_000)],
    3: [("Cloud, AI inference and third-party APIs", 232_000),
        ("Software and tooling", 72_000),
        ("Travel: Cairo, Riyadh, campuses and governorates", 248_000),
        ("Outsourced finance, legal, audit and compliance", 116_000),
        ("Safeguarding, child protection and compliance", 58_000),
        ("Partner enablement: certification, audits and regional hubs", 140_000),
        ("Offices: Cairo and Riyadh", 128_000)],
}

CONTINGENCY = 0.08


# =====================================================================
#  PART 7, ACQUISITION ECONOMICS, BY ENGINE
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
#  COMPUTATION, nothing below here is an assumption
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
    """Sum a quarterly flow over a year."""
    if key in STOCK_KEYS:
        raise KeyError(f"{key} is a stock, not a flow, use stock()")
    return sum(QUARTERLY[key][i] for i in quarters_of(year))


def stock(key, year):
    """The value of a cumulative series at the end of a year."""
    return QUARTERLY[key][quarters_of(year)[-1]]


def cohorts_for(year):
    return plan("uni_cohorts_eg", year) + plan("uni_cohorts_ksa", year)


def all_cohorts(year):
    """Every in-person cohort of any format, including free pilots."""
    return (cohorts_for(year) + plan("uni_pilots", year)
            + plan("school_cohorts", year) + plan("tvet_cohorts", year))


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
             tam_basis=f"{units:,} university buying units x "
                       f"${UNIT_ANNUAL_SPEND:,.0f} a year",
             tam=units * UNIT_ANNUAL_SPEND,
             sam_basis=f"{units*unit_fit:,.0f} that fit and are reachable",
             sam=units * unit_fit * UNIT_ANNUAL_SPEND),
        dict(engine=ENGINE_NAMES[1],
             tam_basis=f"{schools:,} schools x ${SCHOOL_UNIT_ANNUAL_SPEND:,.0f} and "
                       f"{tvet_inst:,} technical institutes x "
                       f"${TVET_UNIT_ANNUAL_SPEND:,.0f}",
             tam=schools * SCHOOL_UNIT_ANNUAL_SPEND + tvet_inst * TVET_UNIT_ANNUAL_SPEND,
             sam_basis=f"{schools*school_fit:,.0f} schools and "
                       f"{tvet_inst*tvet_fit:,.0f} institutes",
             sam=(schools * school_fit * SCHOOL_UNIT_ANNUAL_SPEND
                  + tvet_inst * tvet_fit * TVET_UNIT_ANNUAL_SPEND)),
        dict(engine=ENGINE_NAMES[2],
             tam_basis=f"{INITIATIVE_SEATS_PER_YEAR:,} seats a year x "
                       f"${PRICE_INITIATIVE_SEAT[2]:,.0f}, plus trainer certification",
             tam=INITIATIVE_SEATS_PER_YEAR * PRICE_INITIATIVE_SEAT[2] * 1.25,
             sam_basis=f"{FILTER_INITIATIVE_SHARE*100:.0f}%, what one provider "
                       f"could serve",
             sam=INITIATIVE_SEATS_PER_YEAR * FILTER_INITIATIVE_SHARE
                 * PRICE_INITIATIVE_SEAT[2] * 1.25),
        dict(engine=ENGINE_NAMES[3],
             tam_basis=f"{NGOS:,} NGOs and donors x "
                       f"{NGO_PROGRAMMES_PER_ORG:.1f} programmes x "
                       f"${PRICE_NGO_PROGRAMME[2]:,.0f}",
             tam=NGOS * NGO_PROGRAMMES_PER_ORG * PRICE_NGO_PROGRAMME[2],
             sam_basis=f"{FILTER_NGO_FIT*100:.0f}% with a live youth employability "
                       f"budget",
             sam=NGOS * FILTER_NGO_FIT * NGO_PROGRAMMES_PER_ORG * PRICE_NGO_PROGRAMME[2]),
        dict(engine=ENGINE_NAMES[4],
             tam_basis=f"{COMPETITIONS_PER_YEAR:,} competitions a year x "
                       f"${PRICE_COMPETITION[2]:,.0f}",
             tam=COMPETITIONS_PER_YEAR * PRICE_COMPETITION[2],
             sam_basis=f"{FILTER_COMPETITION_FIT*100:.0f}% with budget and format fit",
             sam=COMPETITIONS_PER_YEAR * FILTER_COMPETITION_FIT * PRICE_COMPETITION[2]),
        dict(engine=ENGINE_NAMES[5],
             tam_basis=f"{CORPORATES:,} corporates x "
                       f"{CORPORATE_PROGRAMMES_PER_ORG:.1f} programmes x "
                       f"${PRICE_CORPORATE[2]:,.0f}",
             tam=CORPORATES * CORPORATE_PROGRAMMES_PER_ORG * PRICE_CORPORATE[2],
             sam_basis=f"{FILTER_CORPORATE_FIT*100:.0f}% with a live budget",
             sam=CORPORATES * FILTER_CORPORATE_FIT * CORPORATE_PROGRAMMES_PER_ORG
                 * PRICE_CORPORATE[2]),
        dict(engine=ENGINE_NAMES[6],
             tam_basis=f"{PROGRAMMES:,} programmes x 150 seats x ${PRICE_SEAT[2]:,.0f}",
             tam=PROGRAMMES * 150 * PRICE_SEAT[2],
             sam_basis=f"{FILTER_PROGRAMME_FIT*100:.0f}% that select and pre-qualify",
             sam=PROGRAMMES * FILTER_PROGRAMME_FIT * 150 * PRICE_SEAT[2]),
        dict(engine=ENGINE_NAMES[7],
             tam_basis=f"{FILTER_SELF_PAY_ADULT*100:.0f}% of {adults/1e6:,.1f}m adults "
                       f"and {FILTER_SELF_PAY_YOUTH*100:.0f}% of {youth/1e6:,.1f}m "
                       f"under-18s x ${arpu:,.0f}",
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

YEARS_5 = (1, 2, 3, 4, 5)


def headcount():
    by_function = {}
    order = []
    for function, role, monthly, *counts in ROLES:
        if function not in by_function:
            order.append(function)
        f = by_function.setdefault(function, dict(roles=[], **{f"y{y}": 0 for y in YEARS_5},
                                                  **{f"cost_y{y}": 0.0 for y in YEARS_5}))
        f["roles"].append((role, monthly, counts))
        for y, c in zip(YEARS_5, counts):
            f[f"y{y}"] += c
            f[f"cost_y{y}"] += c * monthly * 12
    totals = {}
    for y in YEARS_5:
        totals[f"y{y}"] = sum(f[f"y{y}"] for f in by_function.values())
        totals[f"cost_y{y}"] = (sum(f[f"cost_y{y}"] for f in by_function.values())
                                * RAMP[y])
    totals["order"] = order
    return by_function, totals


def headcount_check():
    """The cap is a promise. This is the test that the table keeps it."""
    _, hc = headcount()
    return [(y, hc[f"y{y}"], HEADCOUNT_CAP[y], hc[f"y{y}"] <= HEADCOUNT_CAP[y])
            for y in YEARS_5]


def costs(year):
    _, hc = headcount()
    rev = revenue(year)
    demand = sum(v for _, v in DEMAND_SPEND[year])
    commission = rev["institutional"] * B2B_COMMISSION
    lines = [("Payroll", hc[f"cost_y{year}"]),
             ("Delivery: all engines", direct_cost(year)),
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
        out.append(dict(year=y, label=f"Year {y} | {2025+y}/{26+y}",
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


# ---------------------------------------------------------------- capacity

def facilitator_capacity():
    """
    Does the cohort plan fit the delivery network?

    Three formats with different lengths, so capacity is counted in pair-years
    rather than in cohorts: the constraint is facilitator time, not cohort count.
    Each quarter also reports the certified pool and partner network of that
    quarter, so a reader can see that the plan never schedules more than the
    network it has built can run.
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
        pool = Q["certified_facilitators"][i]
        out.append(dict(label=label, phase=phase, year=year, uni=uni, school=sch,
                        tvet=tv, total=uni + sch + tv, pairs=pairs,
                        facilitators=pairs * 2,
                        pool=pool,
                        available=pool * FACILITATOR_UTILISATION,
                        partners=Q["delivery_partners"][i]))
    return out


def leverage():
    """
    The one table that justifies a twelve-person company.

    For each year: how many cohorts are delivered, by how many certified people
    and partner organisations, against how many StartPad employees.
    """
    _, hc = headcount()
    rows = []
    for y in (1, 2, 3):
        cohorts = all_cohorts(y)
        staff = hc[f"y{y}"]
        pool = stock("certified_facilitators", y)
        partners = stock("delivery_partners", y)
        seats = (plan("initiative_seats", y)
                 + sum(QUARTERLY["programmes"][i] * QUARTERLY["seats_each"][i]
                       for i in quarters_of(y)))
        rows.append(dict(year=y, staff=staff, cohorts=cohorts, pool=pool,
                         partners=partners, seats=seats,
                         cohorts_per_employee=cohorts / staff,
                         learners=cohorts * COHORT_SIZE + seats,
                         learners_per_employee=(cohorts * COHORT_SIZE + seats) / staff,
                         partner_delivered=partners * COHORTS_PER_PARTNER))
    return rows


def pipeline():
    return [("Institutions and sponsors identified", 620),
            ("First meeting held", 248),
            ("Pilot, proposal or bid submitted", 124),
            ("Signed in year one", 58)]



# =====================================================================
#  THE NUMBERS COME FROM THE FINANCIAL MODEL, NOT FROM HERE
# =====================================================================
#
# Everything above this line is the plan's own arithmetic, written before the
# financial model existed. It is kept because it documents the reasoning, the
# market sizing and the engine definitions, and because the market and
# positioning sections still read from it.
#
# But a number that appears in both documents must be one number, not two that
# are asked to agree. So every function below is redefined to read the
# recalculated workbook through `business_plan.finlink`. The workbook is the
# source of truth; the plan quotes it and cannot drift from it.
#
# Build order, because the plan cannot be built before the model:
#     python scripts/build_financial_model.py
#     python scripts/recalc.py output/StartPad_Financial_Model.xlsx 1500
#     python scripts/build_business_plan_docx.py

from business_plan import finlink as FL                          # noqa: E402

YEARS_5 = tuple(range(1, FL.YEARS + 1))
HEADCOUNT_CAP = {y: c for y, c in enumerate(FL.P.HEADCOUNT_CAP, start=1)}
PLAN_YEARS = FL.YEARS
PERIOD_LABEL = "October 2026 to September 2031"

# Which revenue streams on the model's Revenue Streams sheet roll up into
# which of the engines the plan talks about.
ENGINE_STREAMS = {
    ENGINE_NAMES[0]: ["University cohort programmes", "Faculty licences"],
    ENGINE_NAMES[1]: ["School cohorts", "School licences",
                      "Technical and vocational cohorts"],
    ENGINE_NAMES[2]: ["National initiative seats", "Train the trainer cohorts"],
    ENGINE_NAMES[3]: ["NGO and donor programmes"],
    ENGINE_NAMES[4]: ["Sponsored competitions", "Mission Zero sponsorship"],
    ENGINE_NAMES[5]: ["Corporate and CSR programmes"],
    ENGINE_NAMES[6]: ["Programme and incubator seats"],
    ENGINE_NAMES[7]: ["Founder subscriptions"],
}

_STREAM_KEY = {
    "University cohort programmes": "uni_cohorts",
    "Faculty licences": "uni_licences",
    "School cohorts": "school_cohorts",
    "School licences": "school_licences",
    "Technical and vocational cohorts": "tvet_cohorts",
    "National initiative seats": "initiative_seats",
    "Train the trainer cohorts": "tot",
    "NGO and donor programmes": "ngo",
    "Sponsored competitions": "competitions",
    "Corporate and CSR programmes": "corporates",
    "Programme and incubator seats": "programme_seats",
    "Mission Zero sponsorship": "podcast",
    "Founder subscriptions": "subscriptions",
}


def _lines_by_stream():
    return {l["stream"]: l for l in FL.revenue_lines()}


def revenue(year):
    """Revenue for one year, rolled up the way the plan talks about it."""
    by_stream = _lines_by_stream()
    i = year - 1
    lines = {}
    for engine, streams in ENGINE_STREAMS.items():
        lines[engine] = sum(by_stream[s]["revenue"][i] for s in streams
                            if s in by_stream)
    detail = {_STREAM_KEY[s]: l["revenue"][i] for s, l in by_stream.items()}
    total = sum(lines.values())
    subs = lines[ENGINE_NAMES[7]]
    return dict(lines=lines, detail=detail, total=total,
                institutional=total - subs,
                institutional_share=((total - subs) / total) if total else 0.0)


def volumes(year):
    """The volume behind each revenue stream, as the model produced it."""
    i = year - 1
    return {_STREAM_KEY[l["stream"]]: l["volume"][i]
            for l in FL.revenue_lines()}


def direct_cost(year):
    return FL.expense_lines()["direct_total"][year - 1]


def subscriptions(year):
    """The direct engine, as the model's funnel produced it."""
    f = FL.funnel()
    b = FL.book()
    i = year - 1
    arpu = b.year("Revenue Streams", "Blended annual subscription price", year)
    churn = b.assumption("Subscription monthly churn")
    margin = 1.0
    h = headline_rows()[i]
    if h["revenue"]:
        margin = h["gross_profit"] / h["revenue"]
    return dict(rows=[], paid=f["new_paid"][i], arpu=arpu,
                bookings=b.year("Revenue Streams",
                                "Subscription bookings, cash received", year),
                reached=f["registered"][i],
                active=f["active_paid"][i],
                revenue=b.year("Revenue Streams",
                               "Subscription revenue recognised", year),
                churn=churn,
                ltv=(arpu / 12 * margin / churn) if churn else 0.0)


def headline_rows():
    return FL.headline()


def headcount():
    """The establishment by function, from the model's own payroll sheet."""
    est = FL.establishment()
    by_function, order = {}, []
    for r in est["roles"]:
        fn = r["function"]
        if fn not in by_function:
            order.append(fn)
            by_function[fn] = dict(roles=[],
                                   **{f"y{y}": 0 for y in YEARS_5},
                                   **{f"cost_y{y}": 0.0 for y in YEARS_5})
        f = by_function[fn]
        f["roles"].append((r["role"], r["gross"], r["counts"], r["start"]))
        for y in YEARS_5:
            f[f"y{y}"] += r["counts"][y - 1]
    totals = {}
    for y in YEARS_5:
        totals[f"y{y}"] = est["headcount"][y - 1]
        totals[f"cost_y{y}"] = est["payroll"][y - 1]
    # Payroll by function comes from the model so the parts add to the whole.
    for fn in order:
        series = est["by_function"].get(fn)
        for y in YEARS_5:
            by_function[fn][f"y{y}"] = series[y - 1] if series else 0
    totals["order"] = order
    totals["cap"] = est["cap"]
    return by_function, totals


def headcount_check():
    _, hc = headcount()
    return [(y, hc[f"y{y}"], HEADCOUNT_CAP[y], hc[f"y{y}"] <= HEADCOUNT_CAP[y])
            for y in YEARS_5]


# How the model's expense lines roll up into the four cost headings the plan
# uses. Anything the model adds later that is not named here lands in
# "Running the company", so a new cost line can never go missing.
_COST_GROUPS = [
    ("Payroll", ["Payroll, fully loaded"]),
    ("Demand generation", ["Marketing, offline channels",
                           "Marketing, online channels",
                           "Ambassador stipends"]),
    ("Sales commission", ["Sales commission"]),
]


def costs(year):
    """Cost for one year, rolled up the way the plan talks about it."""
    i = year - 1
    ex = FL.expense_lines()
    op = {l["label"]: l["values"][i] for l in ex["operating"]}
    used, lines = set(), []
    lines.append(("Delivery, all engines", ex["direct_total"][i]))
    for heading, labels in _COST_GROUPS:
        total = 0.0
        for lbl in labels:
            if lbl in op:
                total += op[lbl]
                used.add(lbl)
        lines.append((heading, total))
    contingency = op.get("Contingency", 0.0)
    used.add("Contingency")
    rest = sum(v for k, v in op.items() if k not in used)
    lines.append(("Running the company", rest))
    subtotal = sum(v for _, v in lines)
    lines.append(("Contingency", contingency))
    return dict(lines=lines, total=subtotal + contingency, subtotal=subtotal,
                detail=ex)


def projection():
    """Five years, straight off the model's income statement."""
    _, hc = headcount()
    out = []
    cap = FL.capacity()
    for h in FL.headline():
        y = h["year"]
        r = revenue(y)
        out.append(dict(year=y, label=f"Year {y} | {2025 + y}/{(26 + y) % 100:02d}",
                        revenue=h["revenue"], cost=h["total_expense"],
                        profit=h["net"], ebitda=h["ebitda"],
                        gross_profit=h["gross_profit"],
                        gross_margin=h["gross_margin"],
                        net_margin=h["net_margin"],
                        cash_end=h["cash_end"],
                        lines=r["lines"], detail=r["detail"],
                        institutional=r["institutional"],
                        institutional_share=r["institutional_share"],
                        cohorts=FL.book().year("Revenue Streams",
                                               "All in person cohorts "
                                               "delivered", y),
                        facilitators=cap["facilitators"][y - 1],
                        headcount=hc[f"y{y}"],
                        subs=subscriptions(y)))
    return out


def funding():
    """
    The ask, sized on the cash trough the model actually produces rather than
    on a sum of accounting losses.
    """
    cp = FL.cash_profile()
    monthly = cp["monthly"]
    seed = cp["seed"]
    # What the trough would have been without the round already modelled.
    unfunded = min(c - seed if i + 1 >= cp["seed_month"] else c
                   for i, c in enumerate(monthly))
    need = max(0.0, -unfunded)
    reserve = max(0.0, cp["buffer"])
    ask = need + reserve
    losses = [h["net"] for h in FL.headline() if h["net"] < 0]
    return dict(deficit_y1=max(0.0, -FL.headline()[0]["net"]),
                deficit_y2=max(0.0, -FL.headline()[1]["net"]),
                cumulative=sum(-x for x in losses),
                trough=cp["trough"], trough_month=cp["trough_month"],
                seed=seed, seed_month=cp["seed_month"],
                reserve=reserve, ask=ask,
                rounded=max(seed, round(ask / 25_000) * 25_000))


def facilitator_capacity():
    """Delivery capacity, by year, as the capacity sheet computes it."""
    cap = FL.capacity()
    b = FL.book()
    out = []
    for y in YEARS_5:
        i = y - 1
        days = cap["fac_days"][i]
        pool = cap["facilitators"][i]
        available = pool * b.assumption("Delivery days one certified "
                                        "facilitator gives per month") * 12
        out.append(dict(label=f"Year {y}", year=y,
                        total=b.year("Revenue Streams",
                                     "All in person cohorts delivered", y),
                        days=days, facilitators=pool, available=available,
                        partners=cap["partners"][i],
                        utilisation=(days / available) if available else 0.0))
    return out


def pipeline():
    """The year one funnel, as the acquisition engine produced it."""
    f = FL.funnel()
    bs = FL.buyers()
    leads = f["leads"][0]
    meetings = sum(b["meetings"][0] for b in bs)
    proposals = sum(b["proposals"][0] for b in bs)
    return [("Institutions and sponsors reached", round(leads)),
            ("First meeting held", round(meetings)),
            ("Pilot, proposal or bid submitted", round(proposals)),
            ("Signed in year one", round(f["signed"][0]))]


def engine_economics():
    """Unit economics per engine, from the model's indicators."""
    f = FL.funnel()
    rows = []
    by_stream = _lines_by_stream()
    gm = FL.headline()[2]["gross_margin"]
    retention = FL.book().assumption("Years an institutional relationship is "
                                     "retained")
    cac = f["cac_inst"][2]
    for engine, streams in ENGINE_STREAMS.items():
        if engine == ENGINE_NAMES[7]:
            continue
        value = sum(by_stream[s]["revenue"][2] for s in streams
                    if s in by_stream)
        live = FL.capacity()["live"][2]
        per_contract = value / live if live else 0.0
        rows.append(dict(name=engine, cac=cac, value=per_contract,
                         years=retention, margin=gm,
                         ltv=per_contract * retention * gm,
                         ratio=(per_contract * retention * gm / cac)
                         if cac else 0.0))
    subs = subscriptions(3)
    b2c_cac = f["cac_b2c"][2]
    rows.append(dict(name=ENGINE_NAMES[7], cac=b2c_cac, value=subs["arpu"],
                     years=(1 / subs["churn"] / 12) if subs["churn"] else 0.0,
                     margin=gm, ltv=subs["ltv"],
                     ratio=(subs["ltv"] / b2c_cac) if b2c_cac else 0.0))
    return rows


# --- volumes, stocks and prices, so nothing downstream reads the old plan ----
#
# These names are still imported by the charts and by the prose. They are
# redefined here to read the financial model, so a figure that used to draw the
# typed quarterly plan now draws what the funnel actually produced.

_PLAN_TO_ENGINE = {
    "uni_cohorts_eg": "University cohorts, Egypt",
    "uni_cohorts_ksa": "University cohorts, Saudi Arabia",
    "uni_licences": "Faculty licences",
    "school_cohorts": "School cohorts",
    "school_licences": "School licences",
    "tvet_cohorts": "Technical and vocational cohorts",
    "initiative_seats": "National initiative seats",
    "tot_cohorts": "Train the trainer cohorts",
    "ngo_programmes": "NGO and donor programmes",
    "competitions": "Competitions, sponsored",
    "corporates": "Corporate and CSR programmes",
    "podcast_seasons": "Mission Zero seasons carrying a sponsor",
    "programme_seats": "Programme and incubator seats",
}


def plan(key, year):
    """Volume of one engine in one year, as the contract book delivered it."""
    if key == "uni_pilots":
        return 0.0          # there are no unpaid pilots in the model
    label = _PLAN_TO_ENGINE.get(key)
    if label is None:
        return 0.0
    return FL.book().year("Revenue Streams", label, year)


def stock(key, year):
    """A level rather than a flow, at the end of the year."""
    cap = FL.capacity()
    if key == "certified_facilitators":
        return cap["facilitators"][year - 1]
    if key == "delivery_partners":
        return cap["partners"][year - 1]
    if key in ("programmes", "programme_partners"):
        return FL.book().year("Acquisitions",
                              "Programme and incubator seats, contracts live",
                              year)
    return 0.0


def cohorts_for(year):
    """Paid university cohorts delivered in the year."""
    return (plan("uni_cohorts_eg", year) + plan("uni_cohorts_ksa", year))


def all_cohorts(year):
    return FL.book().year("Revenue Streams",
                          "All in person cohorts delivered", year)


def leverage():
    """What each employee carries, year by year."""
    _, hc = headcount()
    cap = FL.capacity()
    b = FL.book()
    out = []
    for y in YEARS_5:
        i = y - 1
        learners = b.year("Acquisitions", "Total new registered accounts", y)
        staff = hc[f"y{y}"]
        out.append(dict(year=y, staff=staff,
                        cohorts=all_cohorts(y),
                        pool=cap["facilitators"][i],
                        partners=cap["partners"][i],
                        learners=learners,
                        learners_per_employee=(learners / staff)
                        if staff else 0.0,
                        revenue_per_employee=(FL.headline()[i]["revenue"]
                                              / staff) if staff else 0.0))
    return out


def _price(key, year=1):
    for p in FL.prices():
        if p["key"] == key:
            return p["values"][year - 1]
    return 0.0


PRICE_COHORT = _price("p_uni")
COHORT_PRICE = {y: _price("p_uni", y) for y in YEARS_5}
PRICE_FACULTY_LICENCE = _price("p_uni_lic", 2)
PRICE_SCHOOL_COHORT = {y: _price("p_school", y) for y in YEARS_5}
PRICE_SCHOOL_LICENCE = _price("p_school_lic", 2)
PRICE_TVET_COHORT = {y: _price("p_tvet", y) for y in YEARS_5}
PRICE_INITIATIVE_SEAT = {y: _price("p_seat_init", y) for y in YEARS_5}
PRICE_TOT_COHORT = {y: _price("p_tot", y) for y in YEARS_5}
PRICE_NGO_PROGRAMME = {y: _price("p_ngo", y) for y in YEARS_5}
PRICE_COMPETITION = {y: _price("p_comp", y) for y in YEARS_5}
PRICE_CORPORATE = {y: _price("p_corp", y) for y in YEARS_5}
PRICE_SEAT = {y: _price("p_seat_prog", y) for y in YEARS_5}
PRICE_PODCAST = {y: _price("p_podcast", y) for y in YEARS_5}
PRICE_PRO_YEAR = FL.book().assumption("Subscription, Pro, annual")
PRICE_TEAM_YEAR = FL.book().assumption("Subscription, Team, annual")
COMPETITION_DIRECT = FL.book().assumption_years(
    "Delivery cost, sponsored competition")[0]
FACILITATOR_DAY_RATE = FL.book().assumption_years("Facilitator day rate")[0]


# =====================================================================
#  MARKET SIZING IS NOT STARTPAD'S PRICE LIST
# =====================================================================
#
# TAM is what the buyers in this market spend on this capability in a year. It
# does not shrink because StartPad decides to charge less, and it does not
# grow because StartPad raises a price. When the price constants above were
# repointed at the financial model, the market sized itself on StartPad's own
# fees and halved, which is wrong on its own terms and also broke the figure
# already presented to investors.
#
# So sizing has its own reference prices: what a buyer in this market
# typically pays for one unit of the thing, benchmarked rather than quoted.
# They are frozen here, and they are the basis of the TAM, SAM and SOM slide
# in the October 2026 investor deck.
#
# SOM is not a reference price at all. It is the plan's own year five revenue,
# read from the financial model, so the obtainable share of this market is the
# thing the rest of the document has already committed to.

MARKET_REFERENCE = {
    "initiative_seat": 20.0,      # per seat, bulk national programmes
    "ngo_programme": 38_000.0,    # per donor programme
    "competition": 32_000.0,      # per sponsored season
    "corporate": 55_000.0,        # per corporate or CSR programme
    "programme_seat": 42.0,       # per accelerator or incubator seat
    "subscription_arpu": 89.0,    # blended self-pay price in this market
    "subscription_reach": 116_930,   # people reachable through an organisation
}


def market():
    """
    TAM, SAM and SOM, bottom up, counting the organisation that signs.

    Identical to the figures on the market slide of the investor deck, because
    it is the same arithmetic on the same reference prices.
    """
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

    R = MARKET_REFERENCE
    arpu = R["subscription_arpu"]
    adults = he + grads + msme
    youth = tvet_s + sec
    subs_tam = (adults * FILTER_SELF_PAY_ADULT
                + youth * FILTER_SELF_PAY_YOUTH) * arpu

    rows = [
        dict(engine=ENGINE_NAMES[0],
             tam_basis=f"{units:,} university buying units x "
                       f"${UNIT_ANNUAL_SPEND:,.0f} a year",
             tam=units * UNIT_ANNUAL_SPEND,
             sam_basis=f"{units*unit_fit:,.0f} that fit and are reachable",
             sam=units * unit_fit * UNIT_ANNUAL_SPEND),
        dict(engine=ENGINE_NAMES[1],
             tam_basis=f"{schools:,} schools x "
                       f"${SCHOOL_UNIT_ANNUAL_SPEND:,.0f} and {tvet_inst:,} "
                       f"technical institutes x ${TVET_UNIT_ANNUAL_SPEND:,.0f}",
             tam=(schools * SCHOOL_UNIT_ANNUAL_SPEND
                  + tvet_inst * TVET_UNIT_ANNUAL_SPEND),
             sam_basis=f"{schools*school_fit:,.0f} schools and "
                       f"{tvet_inst*tvet_fit:,.0f} institutes",
             sam=(schools * school_fit * SCHOOL_UNIT_ANNUAL_SPEND
                  + tvet_inst * tvet_fit * TVET_UNIT_ANNUAL_SPEND)),
        dict(engine=ENGINE_NAMES[2],
             tam_basis=f"{INITIATIVE_SEATS_PER_YEAR:,} seats a year x "
                       f"${R['initiative_seat']:,.0f}, plus trainer "
                       f"certification",
             tam=INITIATIVE_SEATS_PER_YEAR * R["initiative_seat"] * 1.25,
             sam_basis=f"{FILTER_INITIATIVE_SHARE*100:.0f}%, what one "
                       f"provider could serve",
             sam=(INITIATIVE_SEATS_PER_YEAR * FILTER_INITIATIVE_SHARE
                  * R["initiative_seat"] * 1.25)),
        dict(engine=ENGINE_NAMES[3],
             tam_basis=f"{NGOS:,} NGOs and donors x "
                       f"{NGO_PROGRAMMES_PER_ORG:.1f} programmes x "
                       f"${R['ngo_programme']:,.0f}",
             tam=NGOS * NGO_PROGRAMMES_PER_ORG * R["ngo_programme"],
             sam_basis=f"{FILTER_NGO_FIT*100:.0f}% with a live youth "
                       f"employability budget",
             sam=(NGOS * FILTER_NGO_FIT * NGO_PROGRAMMES_PER_ORG
                  * R["ngo_programme"])),
        dict(engine=ENGINE_NAMES[4],
             tam_basis=f"{COMPETITIONS_PER_YEAR:,} competitions a year x "
                       f"${R['competition']:,.0f}",
             tam=COMPETITIONS_PER_YEAR * R["competition"],
             sam_basis=f"{FILTER_COMPETITION_FIT*100:.0f}% with budget and "
                       f"format fit",
             sam=(COMPETITIONS_PER_YEAR * FILTER_COMPETITION_FIT
                  * R["competition"])),
        dict(engine=ENGINE_NAMES[5],
             tam_basis=f"{CORPORATES:,} corporates x "
                       f"{CORPORATE_PROGRAMMES_PER_ORG:.1f} programmes x "
                       f"${R['corporate']:,.0f}",
             tam=CORPORATES * CORPORATE_PROGRAMMES_PER_ORG * R["corporate"],
             sam_basis=f"{FILTER_CORPORATE_FIT*100:.0f}% with a live budget",
             sam=(CORPORATES * FILTER_CORPORATE_FIT
                  * CORPORATE_PROGRAMMES_PER_ORG * R["corporate"])),
        dict(engine=ENGINE_NAMES[6],
             tam_basis=f"{PROGRAMMES:,} programmes x 150 seats x "
                       f"${R['programme_seat']:,.0f}",
             tam=PROGRAMMES * 150 * R["programme_seat"],
             sam_basis=f"{FILTER_PROGRAMME_FIT*100:.0f}% that select and "
                       f"pre-qualify",
             sam=PROGRAMMES * FILTER_PROGRAMME_FIT * 150
                 * R["programme_seat"]),
        dict(engine=ENGINE_NAMES[7],
             tam_basis=f"{FILTER_SELF_PAY_ADULT*100:.0f}% of "
                       f"{adults/1e6:,.1f}m adults and "
                       f"{FILTER_SELF_PAY_YOUTH*100:.0f}% of "
                       f"{youth/1e6:,.1f}m under-18s x ${arpu:,.0f}",
             tam=subs_tam,
             sam_basis="Those reached through an organisation, plus organic",
             sam=R["subscription_reach"] * 1.6 * arpu),
    ]
    tam = sum(r["tam"] for r in rows)
    sam = sum(r["sam"] for r in rows)
    som = FL.headline()[-1]["revenue"]
    buyers = units + schools + tvet_inst + NGOS + COMPETITIONS_PER_YEAR \
        + CORPORATES + PROGRAMMES
    return dict(rows=rows, tam=tam, sam=sam, som=som,
                som_share=(som / sam) if sam else 0.0,
                inst_tam=tam - rows[-1]["tam"],
                inst_sam=sam - rows[-1]["sam"],
                inst_share=((sam - rows[-1]["sam"]) / sam) if sam else 0.0,
                units=units, schools=schools, tvet_inst=tvet_inst,
                buyers=buyers,
                people=people, he=he, grads=grads, tvet_students=tvet_s,
                secondary=sec, msme=msme, reach=reach, unit_fit=unit_fit,
                segments=[
                    ("University students", he),
                    ("Recent graduates (3 years)", grads),
                    ("Technical and vocational students", tvet_s),
                    ("Secondary students, final two years", sec),
                    ("Micro and small enterprise owners", msme),
                ])


# The ambassador network is a cost line in the financial model, so its size
# is read from there rather than kept as a second opinion here. It used to
# say sixty rising to three hundred and forty, against a model that funds
# sixteen rising to two hundred and fifty.
AMBASSADORS = {y: int(v) for y, v in
               zip(YEARS_5, FL.book().assumption_years(
                   "Campus ambassadors on a stipend"))}

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
    print("\n  headcount cap:", headcount_check())
    print("  peak facilitator-equivalents:",
          f"{max(c['facilitators'] for c in facilitator_capacity()):.0f}")
    print("\n  leverage:")
    for r in leverage():
        print(f"    Y{r['year']}: {r['staff']:>2} staff | {r['cohorts']:>3} cohorts | "
              f"pool {r['pool']:>2} | partners {r['partners']:>2} | "
              f"{r['learners']:>7,.0f} learners | "
              f"{r['learners_per_employee']:>7,.0f} per employee")
    for c in facilitator_capacity():
        flag = "  OVER" if c["facilitators"] > c["available"] else ""
        print(f"    {c['label']}  cohorts {c['total']:>3}  need "
              f"{c['facilitators']:>5.1f}  have {c['available']:>5.1f}{flag}")
