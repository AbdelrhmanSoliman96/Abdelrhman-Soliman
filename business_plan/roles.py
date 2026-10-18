"""
Role descriptions for the organisation plan.

One entry per role on the establishment: who it reports to, the purpose it exists
for, the responsibilities that belong to it and nobody else, and the one measure
it is held to. An organisation chart that does not say who decides is a picture
rather than a structure.

The establishment is deliberately small, so most roles here are merged:
curriculum owns certification, the COO carries finance in year one, one head
covers every Egyptian engine until each earns its own owner. Where a role carries
two jobs the description says so rather than pretending otherwise, and names when
it is expected to split.

Keyed to ROLES in model.py — counts and costs live there, the job lives here, and
the builder checks every role on the establishment has a description.
"""

# (role, reports to, purpose, [responsibilities], success measure)
ROLE_SPECS = [
    # ---------------------------------------------------------------- Leadership
    ("Chief Executive Officer", "the board",
     "Owns the institutional relationships the company is built on, and the story "
     "that opens them.",
     ["Carry the first conversation at ministry, donor and university-leadership "
      "level, where the counterparty expects a principal rather than a salesperson",
      "Personally deliver the Day 01 platform onboarding in every cohort until "
      "that is handed to certified facilitators in the Expand quarter",
      "Own the narrative: the podcast, the keynote, the founder stories that make "
      "a dean take a meeting",
      "Set the annual plan with the COO and CTO, and arbitrate when delivery "
      "capacity and sales ambition disagree — which they will, every quarter",
      "Hold the external face of the company in both markets, including the "
      "Riyadh relationships the country manager cannot open alone"],
     "Signed relationships at the level only a founder can reach: national "
     "programmes, university leadership and anchor sponsors."),

    ("Chief Operating Officer", "CEO",
     "Makes sure everything sold can actually be delivered, to the same standard, "
     "by people the customer has never met. In year one this role also carries "
     "finance and administration.",
     ["Own the delivery calendar across all cohort types in both markets, and the "
      "rule that sales sells against capacity rather than the reverse",
      "Own the four quality gates and the review that follows any cohort failing "
      "one of them",
      "Own safeguarding and child-protection compliance before the first school "
      "cohort runs — a legal obligation before it is an operational one",
      "Run the readiness checklist for each roadmap phase and report honestly "
      "when a gate will not be met",
      "Carry finance, invoicing and statutory compliance in year one with an "
      "outsourced accountant, handing it over in year two"],
     "Every scheduled cohort delivered, on standard, with the report issued "
     "inside five working days."),

    ("Chief Technology Officer", "CEO",
     "Owns the platform the whole commercial plan assumes exists, and writes code "
     "as well as directing it.",
     ["Sequence engineering against the roadmap gates rather than feature "
      "requests — the admin workspace before the competition flow, the "
      "competition flow before bulk provisioning",
      "Own the AI review pipeline and the overnight SLA the daily cohort loop "
      "depends on, personally in year one",
      "Own data protection, student-controlled sharing and the scoping that keeps "
      "institutional visibility separate from private student data",
      "Keep Arabic right-to-left parity a release condition rather than a backlog "
      "item",
      "Hold platform cost per active user as volume moves from hundreds to tens "
      "of thousands of sponsored seats"],
     "Each roadmap gate met in the quarter it is due, and the overnight review "
     "SLA held every night of every cohort."),

    # ------------------------------------------------- Product and Engineering
    ("Senior full-stack engineer", "CTO",
     "Builds the institutional product — the part of the platform the buyer, not "
     "the student, uses.",
     ["Build the programme admin workspace: cohort creation, bulk invitation, "
      "educator assignment, review states",
      "Build the automatic cohort report, which is the renewal document for every "
      "education and public engine",
      "Build the competition entry, qualification and judging flow, then bulk "
      "seat provisioning and partner reporting",
      "Hold performance under the load spike of an entire cohort submitting on "
      "the same evening",
      "Carry their own testing and release quality — there is no separate QA "
      "function until the platform is larger than the team"],
     "Institutional features shipped by their gate quarter, with no manual "
     "intervention needed to produce a cohort report."),

    ("AI and data engineer", "CTO",
     "Owns the review loop that makes a StartPad score mean something, and the "
     "data that proves it. Joins in year two.",
     ["Maintain and tune the review rubric across specificity, depth, evidence, "
      "actionability and relevance, in both languages",
      "Keep the AI Co-Founder asking the follow-up a mentor would ask, and stop "
      "it writing the founder's answer",
      "Calibrate scoring against human educator review on real cohorts and "
      "publish the agreement rate internally",
      "Build the anonymised dataset behind the annual readiness report",
      "Manage inference cost per review as seat volume grows"],
     "Educator agreement with AI scores above the internal threshold, and review "
     "turnaround inside the overnight SLA."),

    ("Product designer", "CTO",
     "Makes the product usable by a sixteen-year-old in a technical school and by "
     "a programme administrator in a ministry, without building two products. "
     "Joins in year three; carried by the CTO and engineers before that.",
     ["Own the mission, dashboard and review interfaces in both languages and "
      "both reading directions",
      "Design the institutional workspace for someone trained once and then left "
      "alone with it",
      "Run usability testing inside live cohorts rather than in a lab",
      "Own the design system so a bilingual interface does not drift"],
     "Students complete missions without facilitator help by the second evening, "
     "and administrators use the workspace without raising a ticket."),

    # ------------------------------------------------- Curriculum and Delivery
    ("Head of Curriculum and Certification", "COO",
     "Owns what is taught, how it is assessed, and who is fit to teach it. These "
     "are one job in a company this size, and separating them would weaken both.",
     ["Own the fifteen missions, the 121 tools and the standard for what a good "
      "answer needs",
      "Own the school and technical variants — what is cut, what is reframed, "
      "and why",
      "Run the four-step facilitator certification and sign off every "
      "certification decision personally",
      "Certify partner and ministry trainers under the train-the-trainer engine, "
      "which is what makes seat volume deliverable without StartPad headcount",
      "Co-design programmes with initiative and donor partners so their objective "
      "maps onto missions without bespoke content being written each time",
      "Own the judging rubric used at every showcase and competition"],
     "Certified pairs available ahead of every quarter's plan, and cohort "
     "completion above the quality gate."),

    ("Bilingual curriculum producer", "Head of Curriculum and Certification",
     "Produces and localises everything a facilitator and a student actually "
     "touch, in both languages. One role in year one, specialising by segment as "
     "the team grows.",
     ["Produce mission briefs, short lessons, evidence prompts and facilitator "
      "packs for every format",
      "Compose — not translate — Egyptian colloquial and Saudi dialect versions "
      "of every mission, review and exported report",
      "Own right-to-left correctness in every artefact a student or a ministry "
      "sees",
      "Build the teacher-delivery pack so a trained teacher can run a school club "
      "without StartPad in the room",
      "Fold facilitator and student feedback into the next revision each term"],
     "Material revised each term, usable without adaptation, with no cohort where "
     "language is cited as a barrier."),

    ("Lead facilitator", "COO",
     "Delivers cohorts at the standard the freelance pool is certified against, "
     "and is the reason the pool can exist at all.",
     ["Deliver the first cohort at every new institution, where the relationship "
      "is most fragile",
      "Observe, co-deliver with and score facilitator candidates through "
      "certification",
      "Mark daily checkpoints honestly, including Not yet, and coach the teams "
      "that need it",
      "Hold safeguarding practice in the room as non-negotiable on school and "
      "technical cohorts",
      "Feed what failed in the room back to curriculum within the same week"],
     "Cohorts above the completion gate, and candidates certified on schedule."),

    ("Programme delivery coordinator", "COO",
     "Turns a signed contract into a delivered cohort: calendar, pairing, "
     "materials, logistics. Joins in year two, when volume outgrows the COO.",
     ["Hold the delivery calendar a term ahead, against each institution's "
      "academic calendar and around Ramadan",
      "Assign certified pairs and escalate when a cohort has no qualified pair "
      "available",
      "Own materials logistics to venues across both markets, printing locally in "
      "each rather than shipping across a border",
      "Issue the cohort report inside five working days of the showcase"],
     "Cohorts delivered on the agreed dates with reports issued on time."),

    # --------------------------------------------------- Institutional Sales
    ("Head of Partnerships — Egypt", "CEO",
     "Owns the Egyptian institutional pipeline across every engine in year one, "
     "and the university engine specifically once the others earn their own "
     "owners.",
     ["Own the four-door approach into every target university and the "
      "pilot-to-licence ladder",
      "Convert pilot cohort reports into paid cohorts, parallel groups and "
      "faculty licences",
      "Carry schools, competitions, donors and corporates in year one until each "
      "is handed to its own head",
      "Hold the renewal conversation before the term ends, not after",
      "Keep the pipeline honest against the delivery calendar — never sell a "
      "cohort there is no certified pair for"],
     "Paid cohorts and licences signed to plan, and second-term renewal rate."),

    ("Head of Schools and Technical Education", "CEO",
     "Opens an entirely different buyer — schools, applied-technology schools and "
     "technical institutes. Joins in year two, once the school variant has been "
     "proven in the Expand quarter.",
     ["Build relationships with school groups, operators and technical institute "
      "directors in both markets",
      "Own the school club, cohort, technical and whole-school licence ladder",
      "Navigate ministry approval where a school needs it before buying",
      "Work with curriculum on national-framework alignment, which is often the "
      "condition of the sale"],
     "School and technical cohorts signed to plan, and the first whole-school "
     "licences."),

    ("Head of Government, Initiatives and Donors", "CEO",
     "Owns the longest sales cycles and the largest contracts in the company — "
     "national programmes and donor-funded work, which buy the same way.",
     ["Open and hold relationships with national programme offices, ministries, "
      "foundations and INGO country offices in both markets",
      "Convert a public target or a donor logframe into a scoped, funded order "
      "with a reporting format attached",
      "Own the train-the-trainer proposition that makes seat volume deliverable",
      "Own bid and proposal quality, and the reporting that is the condition of "
      "the next grant",
      "Protect the company from contracting to outcomes the product cannot "
      "measure"],
     "Signed seat orders and programmes, delivered against, and renewed or "
     "widened."),

    ("Country Manager — KSA (Riyadh)", "CEO",
     "Runs Saudi Arabia as a market rather than an export destination, and owns "
     "every engine inside it.",
     ["Own all Saudi revenue across every engine — in that market the "
      "relationship comes before the product line",
      "Build relationships with Monsha'at, Misk, TVTC, universities and corporate "
      "sponsors",
      "Establish and maintain the Saudi entity, compliance and local partnerships",
      "Build Saudi delivery capacity — a certified local pool, not facilitators "
      "flown from Cairo",
      "Localise the commercial approach to Saudi procurement norms and timelines"],
     "Saudi revenue to plan from the first quarter, with local delivery capacity "
     "behind it."),

    ("Partnerships associate", "the relevant Head",
     "Carries the volume of the institutional pipeline below principal level. "
     "Joins in year two.",
     ["Research and qualify institutions, programmes and sponsors",
      "Book and prepare first meetings for the heads",
      "Maintain pipeline hygiene — every stage, every next action, dated",
      "Run pilot-to-contract administration so a head is never the bottleneck on "
      "paperwork"],
     "Qualified meetings booked and pipeline accuracy at review."),

    ("Account manager — renewals", "COO",
     "Owns the revenue the company already won, which is where this business "
     "actually lives. Joins in year three, when the signed base outgrows the "
     "heads who sold it.",
     ["Own renewal for every signed institution, programme and sponsor",
      "Run the post-cohort review that turns a report into the next order",
      "Expand accounts: more cohorts, more faculties, more governorates, a "
      "licence",
      "Flag at-risk accounts a term before the renewal date"],
     "Renewal rate and net revenue retention across the signed base."),

    # ------------------------------------------------- Growth and Operations
    ("Growth and community manager", "CEO",
     "Makes the institutional pipeline warm before anyone makes a cold call, and "
     "runs everything that touches young people directly. One role covering "
     "content, community, ambassadors and competitions in year one.",
     ["Run the content engine: founder stories, the podcast, reels — every piece "
      "ending at Mission 01",
      "Recruit, train and tier the ambassador network, and route the campus "
      "intelligence it produces to sales",
      "Sell and run sponsored competitions in year one, handing delivery to a "
      "coordinator as volume grows",
      "Own the annual readiness report that turns a vendor into a cited reference",
      "Supply sales with collateral answering the buyer's real question: what "
      "will I be able to report",
      "Hold the line against cold paid acquisition"],
     "Share of pipeline arriving warm — referred, inbound or ambassador-sourced — "
     "and competitions sold to plan."),

    ("Ambassador and events coordinator", "Growth and community manager",
     "Runs the campus network and the competition calendar as execution, freeing "
     "the growth manager to sell and position. Joins in year two.",
     ["Recruit, train and renew ambassadors term by term across target campuses",
      "Collect and route campus intelligence: which centre has budget, which dean "
      "is under accreditation pressure",
      "Run competitions end to end — entry, qualification rounds, judging, final "
      "and awards",
      "Deliver every sponsor's reporting and brand obligations in full"],
     "Active ambassadors per campus, competitions delivered, and qualified "
     "institutional leads sourced from the network."),

    ("Student success (bilingual)", "COO",
     "Keeps young people moving, which is what every buyer is actually paying "
     "for. Joins in year two, when cohort and seat volume makes it a full-time "
     "job.",
     ["Cover the support queue in both languages, weighted to cohort weeks when "
      "load spikes",
      "Act on follow-up signals — inactivity, repeated failed reviews, unstarted "
      "missions",
      "Own activation of issued sponsored seats, which is where seat programmes "
      "usually fail",
      "Escalate product problems with the evidence attached"],
     "Activation and completion rates inside cohorts and sponsored programmes."),

    ("Finance, bids and administration", "COO",
     "Keeps the company solvent, compliant and able to invoice a ministry. Joins "
     "in year two; carried by the COO and an outsourced accountant before that.",
     ["Own invoicing and collections, including the public-sector payment cycle, "
      "which is slow and unforgiving of paperwork errors",
      "Own payroll across two jurisdictions and the freelance facilitator pool",
      "Assemble bids, tenders and grant proposals to the funder's exact format",
      "Maintain the pre-qualification library — registrations, policies, "
      "certifications, references — because a missing document loses a bid more "
      "often than a weak proposal does",
      "Track contractual deliverables and reporting deadlines across every signed "
      "programme"],
     "Clean audit, on-time payroll, collections inside terms, and no contractual "
     "reporting deadline missed."),
]

BY_ROLE = {r[0]: r for r in ROLE_SPECS}
