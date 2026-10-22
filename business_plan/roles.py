"""
Role descriptions for the organisation plan.

One entry per role on the establishment: who it reports to, the purpose it
exists for, the responsibilities that belong to it and nobody else, who it
works with to get them done, and the one measure it is held to. An
organisation chart that does not say who decides is a picture rather than a
structure, and one that does not say who each person talks to is a list of job
titles rather than a company.

Fifteen roles, capped at six, nine, twelve, sixteen and twenty across the five
years. That cap is only honest if the merged roles are admitted, so each
description says plainly where a role carries two jobs, which of them is
temporary, and the year the role splits. A plan that hides the merge is a plan
that quietly needs twenty-five people in year two.

Keyed to ROLES in finmodel/plan.py: counts, salaries and start months live
there, the job lives here, and `scripts/check_plan_matches_model.py` checks
that every role on the establishment has a description and that no description
describes a role nobody holds.
"""

# (role, reports to, purpose, [responsibilities], [how it engages], measure)
ROLE_SPECS = [
    # ------------------------------------------------------ Leadership
    ("Chief Executive Officer", "the board",
     "Owns the institutional relationships the company is built on, the story "
     "that opens them, and the quality standard that makes them renew.",
     ["Carry the first conversation at ministry, agency, donor and university "
      "leadership level, where the counterparty expects a principal rather "
      "than a salesperson",
      "Own the rule that sales sells against certified capacity rather than "
      "the reverse, and publish the trade every quarter so the company can "
      "see it being made",
      "Host Mission Zero and own the narrative that makes a dean take a "
      "meeting",
      "Hold the quality gates personally in years one and two: a cohort that "
      "fails one is reviewed by the chief executive, not delegated, because "
      "the standard is the product",
      "Run the board, the raise and the relationship with the investors who "
      "funded the seed"],
     ["Inside: weekly with the chief commercial officer on the pipeline, "
      "monthly with the chief technology officer on what the platform must do "
      "next, and in the quality review with the head of curriculum",
      "Outside: vice-chancellors, ministry desk officers, donor country "
      "directors and the board. These are the conversations that do not "
      "delegate",
      "On the podcast: interviews every guest personally, which is also how "
      "roughly a sixth of the institutional pipeline starts"],
     "Signed relationships at the level only a founder can reach, and no "
     "quarter in which more cohorts were sold than the network could "
     "deliver."),

    ("Chief Technology Officer", "the chief executive",
     "Owns the platform, the AI review that makes it defensible, and the data "
     "that turns a delivered cohort into a report a buyer will pay for again.",
     ["Build and run the mission platform, the AI co-founder and the review "
      "engine, and keep the cost per active learner inside the model",
      "Own the cohort report: the artefact the institution actually buys, "
      "generated rather than written",
      "Hold the line on what the AI does and does not do, which is that it "
      "asks and never writes the answer",
      "Carry engineering alone through year one, and hire the first engineer "
      "in month thirteen rather than before",
      "Own security, data protection and the safeguarding controls the "
      "schools engine depends on"],
     ["Inside: with the head of curriculum on how a mission becomes a "
      "reviewable artefact, and with the delivery coordinator on what breaks "
      "in a live cohort",
      "Outside: the institution's own IT and registry teams, who decide "
      "whether a platform can be used at all, and the data protection office "
      "where there is one",
      "With the founders: the chief technology officer is in the room for any "
      "deal that promises a feature, because a promise made in a meeting is "
      "a roadmap item"],
     "Platform cost per active learner inside the model, and no cohort "
     "delayed by a platform failure."),

    ("Chief Commercial Officer", "the chief executive",
     "Owns the number. Every engine that signs a contract reports here, and "
     "the commercial team is built and held to its conversion rates by this "
     "role.",
     ["Own the pipeline across all six buyer types, and the forecast the "
      "board is given",
      "Build the commercial team: the business development and sponsorship "
      "managers from month one, government and donor from month thirteen, "
      "Saudi Arabia from month twenty-five",
      "Hold the conversion rates in the model honest, and replace each "
      "modelled rate with an observed one as soon as there is a quarter of "
      "evidence",
      "Price. Every discount below the list in the financial model is this "
      "role's decision, and is recorded against the contract",
      "Own renewals until the account manager arrives in year five"],
     ["Inside: daily with business development and sponsorship, weekly with "
      "the chief executive on the pipeline, and with the head of curriculum "
      "before committing to any delivery date",
      "Outside: carries the second meeting on most institutional deals, after "
      "the chief executive has opened the door, and the whole of it on "
      "sponsor and corporate deals",
      "With marketing: sets what the inbound engine must produce, and is the "
      "internal customer for every lead it generates"],
     "Contracts signed against plan, and cost per contract won inside the "
     "model."),

    # -------------------------------------------- Institutional Partnerships
    ("Business development manager", "the chief commercial officer",
     "Turns universities, schools and technical institutes into signed "
     "cohort contracts. The single highest-volume seller in the company.",
     ["Run direct outreach to deans, entrepreneurship centre directors and "
      "capstone coordinators, which is the largest single source of "
      "institutional leads in the model",
      "Run campus workshops as a selling instrument rather than a marketing "
      "one: a workshop that produces no booked meeting has failed",
      "Carry the deal from first meeting through proposal to signature, and "
      "hand over a signed contract with a delivery date the network has "
      "already agreed",
      "Keep the account warm through the first cohort, because the second "
      "cohort is sold in the room where the first one is judged",
      "Grow from one person to three across the five years, and train the "
      "second and third"],
     ["Inside: with the partner network manager before promising any date, "
      "and with the delivery coordinator once a contract is signed",
      "Outside: deans, entrepreneurship centres, capstone coordinators, "
      "school group heads and technical institute directors",
      "At the showcase: attends the judging day of every cohort sold, which "
      "is where the renewal conversation actually happens"],
     "Contracts signed, and the share of first cohorts that produce a second."),

    ("Sponsorship and partnerships manager", "the chief commercial officer",
     "Sells the things a brand buys rather than a budget holder: competition "
     "seasons, Mission Zero sponsorship and corporate programmes.",
     ["Own the sponsored competition engine end to end, from the sponsor "
      "conversation to the season that carries their name",
      "Sell Mission Zero season sponsorship against a production calendar "
      "that is fixed before the sponsor is found",
      "Own the youth and channel organisation relationships, Enactus and "
      "INJAZ among them, which bring teams rather than money",
      "Carry the corporate and CSR engine, where the buyer is an innovation "
      "or CSR budget holder rather than an educator",
      "Protect the rule that a sponsor buys visibility and never editorial "
      "control of a mission or a review"],
     ["Inside: with the chief technology officer on what a sponsor can and "
      "cannot be shown, and with the content associate on what a season "
      "actually delivers",
      "Outside: bank and telco marketing directors, foundation programme "
      "leads, corporate CSR and innovation teams, and the youth organisations "
      "that supply teams",
      "With the chief executive: joint on any sponsor conversation above the "
      "list price of a season"],
     "Sponsored seasons and corporate programmes signed, and sponsor renewal "
     "rate."),

    ("Government and donor programmes manager", "the chief commercial officer",
     "Carries the longest and largest deals in the company: national "
     "initiatives, ministries and the donor programmes that fund them. "
     "Arrives in month thirteen, once there are delivered cohorts to show.",
     ["Own the national initiative and government pipeline, where the cycle "
      "is long, the procurement is formal and the first meeting is rarely "
      "with the decision maker",
      "Write bids. Donor and ministry money arrives through a document, not "
      "a pitch, and this role owns that document",
      "Own the NGO, donor and foundation engine alongside it, where the buyer "
      "is a country office or a development agency",
      "Hold the compliance and reporting obligations these contracts carry, "
      "which are heavier than anything in the university engine",
      "Attach train-the-trainer to every initiative that needs trainers, "
      "which is how a seat order becomes a relationship"],
     ["Inside: with the chief executive, who opens ministry doors, and with "
      "the head of curriculum on what can be localised and how fast",
      "Outside: ministry desk officers, national programme offices, donor "
      "country directors, INGO programme managers and the local aggregators "
      "who distribute seats",
      "With the delivery coordinator: bulk seat provisioning is an operation, "
      "not a transaction, and it is planned before signature"],
     "Initiative seats contracted, and the share of bids submitted that are "
     "won."),

    ("Country manager, KSA (Riyadh)", "the chief commercial officer",
     "The company's presence in Saudi Arabia. Arrives in month twenty-five, "
     "which is when the Saudi engine opens, because a market is not entered "
     "from another country.",
     ["Own every Saudi relationship: universities, TVTC institutes, Monsha'at "
      "programmes and the sponsors who fund them",
      "Localise the commercial approach to a market where the buyer, the "
      "procurement and the calendar are all different from Egypt's",
      "Build the Saudi delivery network, because cohorts cannot be staffed "
      "across the border at the facilitator day rate in the model",
      "Hold the Arabic dialect question: curriculum composed for Egypt needs "
      "work before it is credible in Riyadh",
      "Open the Riyadh office and run it"],
     ["Inside: with the partner network manager on certifying Saudi "
      "facilitators, and with the head of curriculum on dialect and "
      "localisation",
      "Outside: Saudi university leadership, TVTC, Monsha'at, and the Saudi "
      "corporate and bank sponsors who fund youth programmes",
      "Reports into the chief commercial officer but runs as a country "
      "business, with its own pipeline review"],
     "Saudi contracts signed, and Saudi cohorts delivered by a Saudi "
     "network."),

    ("Account manager, renewals", "the chief commercial officer",
     "Keeps what the company has already won. Arrives in year five, when the "
     "contract book is large enough that losing accounts quietly costs more "
     "than winning new ones.",
     ["Own the renewal of every institutional contract, which in this model "
      "is a twelve month life that must be re-won",
      "Run the expansion path: a delivered cohort becomes a second, two "
      "cohorts at one faculty become a licence",
      "Hold the account health view, so a relationship that is going cold is "
      "visible before the renewal date rather than at it",
      "Free the business development managers to sell new logos rather than "
      "defend old ones"],
     ["Inside: with the delivery coordinator, who sees an account going wrong "
      "first, and with the business development managers at handover",
      "Outside: the day-to-day contacts at every signed institution, which is "
      "a different person from the one who signed",
      "With the chief commercial officer: owns the renewal forecast"],
     "Renewal rate, and revenue expanded from existing accounts."),

    # ------------------------------------------------ Growth and Content
    ("Marketing manager", "the chief commercial officer",
     "Builds the demand that the commercial team converts, and the direct "
     "engine that turns reached learners into paying accounts. On the "
     "establishment from month one.",
     ["Own the online channels and the cost per click, per lead and per paid "
      "account that the model is built on",
      "Own the three stage funnel: click to lead, lead to registered account, "
      "registered account to paid account, and the conversion rate at each "
      "stage",
      "Run the ambassador network, which is the cheapest reach the company "
      "has and the hardest to manage",
      "Produce the content that makes an institutional enquiry arrive "
      "unprompted, which the model counts as inbound per thousand accounts "
      "reached",
      "Hold the truth that paid acquisition cannot pay for a fifteen dollar "
      "subscription, and keep online spend pointed at institutional demand"],
     ["Inside: with the chief commercial officer, who is the internal "
      "customer for every lead, and with the content associate once that "
      "role arrives in year five",
      "Outside: student creators and influencers, campus societies, and the "
      "ambassadors themselves",
      "With the platform: the conversion from free account to paid is a "
      "product problem as much as a marketing one, and this role works it "
      "with the chief technology officer"],
     "Institutional leads delivered against plan, cost per paid account, and "
     "the registered to paid conversion rate."),

    ("Content and community associate", "the marketing manager",
     "Runs the parts of the direct engine that need a person every day: the "
     "community, the published content and the ambassador programme at the "
     "scale it reaches by year five.",
     ["Run the community beside the missions, which is where a stalled "
      "learner is unstuck by a peer rather than by support",
      "Produce and publish the content calendar in Arabic and English, "
      "including the written mission note that accompanies every Mission "
      "Zero episode",
      "Manage the ambassador network day to day once it passes two hundred "
      "people, which is beyond what the marketing manager can hold alongside "
      "the funnel",
      "Own the showcase and competition content that gives institutions "
      "something to share, which is the cheapest institutional marketing the "
      "company has"],
     ["Inside: with the marketing manager on the calendar and with the "
      "student success side of delivery on what learners are actually stuck "
      "on",
      "Outside: ambassadors, campus societies, alumni and the founders who "
      "appear on Mission Zero",
      "With sponsorship: a season that carries a sponsor has deliverables, "
      "and this role produces them"],
     "Community activity per active learner, and organic registered accounts "
     "per month."),

    # -------------------------------------------- Product and Engineering
    ("Full stack engineer", "the chief technology officer",
     "The first engineering hire, in month thirteen. Exists so the chief "
     "technology officer can stop being the only person who can change the "
     "platform.",
     ["Build and maintain the mission platform, the educator view and the "
      "decision maker view",
      "Own the integrations institutions ask for: single sign on, registry "
      "data, and the export formats a university actually uses",
      "Carry the bilingual requirement in the product rather than in "
      "translation: Arabic is the default, not a localisation",
      "Take the on-call rota, because a cohort runs for six days and cannot "
      "wait"],
     ["Inside: with the chief technology officer daily, and with the delivery "
      "coordinator on what breaks in a live cohort",
      "Outside: the institution's IT teams during onboarding",
      "With curriculum: a mission is a product specification, and this role "
      "builds from it"],
     "Platform availability during cohort weeks, and integration requests "
     "delivered inside the sales cycle."),

    ("AI and data engineer", "the chief technology officer",
     "Owns the review engine and the evidence record, which are the two "
     "things a competitor cannot copy quickly. Arrives in month thirty-seven, "
     "when there is enough reviewed work to learn from.",
     ["Own the AI review: the specificity, depth, evidence, actionability and "
      "relevance scores, and the gate that decides whether a mission "
      "unlocks",
      "Keep the review calibrated against human judgement, which means "
      "sampling and comparing rather than assuming",
      "Own the cohort report generation and the analytics the institution "
      "buys",
      "Hold inference cost per active learner inside the model as volume "
      "grows"],
     ["Inside: with the head of curriculum, who owns what good looks like, "
      "and with the chief technology officer on cost",
      "Outside: nothing routine. This role is deliberately internal",
      "With delivery: a review that facilitators do not trust is a review "
      "that gets overridden, so facilitator feedback is a primary input"],
     "Review agreement with human scoring, and inference cost per active "
     "learner."),

    # ------------------------------------------- Curriculum and Delivery
    ("Head of curriculum and certification", "the chief executive",
     "Owns what good looks like, and who is allowed to say so. Arrives in "
     "month thirteen; until then the chief executive holds it.",
     ["Own the fifteen missions, the tool library and the rubric the AI "
      "reviews against",
      "Own certification: the only person who can pass or fail a facilitator, "
      "which is the control that keeps quality from drifting as delivery is "
      "delegated",
      "Build the school and technical variants of the curriculum, including "
      "the safeguarding that the school engine cannot open without",
      "Own localisation into Saudi dialect alongside the country manager",
      "Review every cohort that fails a quality gate"],
     ["Inside: with the chief technology officer on how a mission becomes "
      "reviewable, with the partner network manager on who gets certified, "
      "and with the commercial team before any delivery commitment",
      "Outside: the facilitator pool, the certified partner organisations, "
      "and academic staff at partner institutions who want to co-teach",
      "At the gate: this role is the quality control, and the plan depends "
      "on it not being overruled by a delivery date"],
     "Facilitator pass rate at certification, and cohort review scores "
     "holding as delivery is delegated."),

    ("Partner network manager", "the head of curriculum and certification",
     "Builds and audits the delivery network that lets twenty people stand "
     "behind two hundred cohorts. Arrives in month twenty-five, when "
     "partner-delivered volume starts.",
     ["Recruit, certify and retain the facilitator pool, which the model "
      "sizes from the cohorts actually sold rather than guessing",
      "Certify partner organisations and audit them, because a partner "
      "delivering badly under licence damages the standard faster than a bad "
      "employee would",
      "Run the four step certification: observe, co-deliver, deliver "
      "observed, recertify each term",
      "Hold the rule that nobody facilitates unobserved before step three, "
      "including under schedule pressure, which is the only time the rule "
      "matters",
      "Own the facilitator economics: the day rate, the utilisation and the "
      "share of cohorts delivered by partners"],
     ["Inside: with the head of curriculum, who signs off every "
      "certification, and with the delivery coordinator on scheduling",
      "Outside: freelance facilitators, training providers, university "
      "innovation centres and youth NGOs who deliver under licence",
      "With commercial: gives the capacity number that sales sells against, "
      "and is the person who says no to a date"],
     "Certified pool against the cohorts sold, and partner audit scores."),

    ("Programme delivery coordinator", "the head of curriculum and "
     "certification",
     "Runs the cohorts. Arrives in month thirty-seven, when the number of "
     "simultaneous cohorts is beyond what the partner network manager can "
     "schedule alongside certification.",
     ["Own the delivery calendar: which cohort runs where, staffed by whom, "
      "on which six days",
      "Run mobilisation, the period between a signed contract and the first "
      "delivery day, which the model treats as real time and which is where "
      "most slippage would happen",
      "Own bulk seat provisioning for initiative and programme partners, "
      "where thousands of accounts arrive at once",
      "Run the showcase and judging day logistics, which is the artefact the "
      "institution remembers",
      "Escalate early: a cohort at risk is a renewal at risk"],
     ["Inside: with the partner network manager on staffing, with engineering "
      "on anything that breaks live, and with the account manager on any "
      "account going wrong",
      "Outside: the institution's programme administrators, who are the "
      "people StartPad actually works with day to day",
      "With the learners: owns the bilingual support queue until a dedicated "
      "role exists"],
     "Cohorts delivered on the committed date, and seat activation rate on "
     "sponsored seats."),
]

BY_ROLE = {r[0]: r for r in ROLE_SPECS}
