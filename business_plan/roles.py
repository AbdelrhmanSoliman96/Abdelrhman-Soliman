"""
Role descriptions for the organisation plan.

One entry per role on the establishment: who it reports to, the purpose it exists
for, the responsibilities that belong to it and nobody else, and the one measure
it is held to. An organisation chart that does not say who decides is a picture
rather than a structure.

The establishment is capped at six, nine and twelve people in the first three
years, and twenty by year five. That cap is only honest if the merged roles are
admitted, so each description below says plainly where a role carries two jobs,
which of them is temporary, and the year the role splits. A plan that hides the
merge is a plan that quietly needs eighteen people in year two.

Keyed to ROLES in model.py — counts and costs live there, the job lives here, and
the builder checks that every role on the establishment has a description and
that no description describes a role nobody holds.
"""

# (role, reports to, purpose, [responsibilities], success measure)
ROLE_SPECS = [
    # ---------------------------------------------------------------- Leadership
    ("Chief Executive Officer", "the board",
     "Owns the institutional relationships the company is built on, the story "
     "that opens them, and — until year four — operations as well.",
     ["Carry the first conversation at ministry, agency, donor and university-"
      "leadership level, where the counterparty expects a principal rather than "
      "a salesperson",
      "Own the delivery calendar and the rule that sales sells against certified "
      "capacity rather than the reverse — this is the chief operating officer's "
      "job and the CEO holds it until the partner network passes roughly a dozen "
      "organisations, which the plan puts in year four",
      "Host Mission Zero and own the narrative that makes a dean take a meeting",
      "Hold the quality gates personally in years one and two: a cohort that "
      "fails one is reviewed by the CEO, not delegated, because the standard is "
      "the product",
      "Arbitrate between delivery capacity and sales ambition every quarter, "
      "and publish the decision so the company can see the trade being made"],
     "Signed relationships at the level only a founder can reach, and no quarter "
     "in which more cohorts were sold than the network could deliver."),

    ("Chief Technology Officer", "CEO",
     "Owns the platform the whole commercial plan assumes exists, and writes "
     "code as well as directing it.",
     ["Sequence engineering against the roadmap gates rather than feature "
      "requests — the admin workspace before the competition flow, the "
      "competition flow before bulk seat provisioning",
      "Own the bilingual AI mentor: its prompts, its evaluation harness, its "
      "cost per learner, and the Arabic quality that most of the market gets "
      "wrong",
      "Build the certification and audit tooling that lets twelve people stand "
      "behind a network of certified facilitators and partner organisations",
      "Own data protection, the safeguarding architecture for accounts held by "
      "minors, and Saudi data-residency obligations",
      "Carry product management and design until year five, with the Head of "
      "Curriculum as the second opinion on anything a learner touches"],
     "Every roadmap gate met in the quarter it is due, and inference cost per "
     "learner falling year on year."),

    ("Chief Operating Officer", "CEO",
     "Takes operations off the CEO once the partner network is too large for "
     "one person to hold alongside the company's external relationships. Arrives "
     "in year four, deliberately late.",
     ["Own the delivery calendar, the partner network and the certification "
      "regime as a single system rather than three functions",
      "Own the four quality gates and the review that follows any cohort failing "
      "one of them",
      "Own safeguarding and child-protection compliance across both markets, and "
      "the external attestation that makes it mean something",
      "Run the readiness review for each roadmap phase and report honestly when "
      "a gate will not be met",
      "Manage the outsourced finance, legal and audit relationships, which "
      "remain outsourced"],
     "Every scheduled cohort delivered, on standard, with its report issued "
     "inside five working days — at any network size."),

    # -------------------------------------------------- Product and Engineering
    ("Senior full-stack engineer", "CTO",
     "Builds and runs the platform. Two of these are the entire engineering team "
     "through year three, which means breadth over specialism.",
     ["Ship the mission engine, the programme admin workspace, the competition "
      "flow and bulk provisioning, in the order the gates demand",
      "Own one vertical slice end to end — database to interface — rather than a "
      "layer, because a two-engineer team cannot afford hand-offs",
      "Carry on-call for a platform used in live cohort rooms, where an outage "
      "is twenty-five people and a facilitator standing still",
      "Build the reporting that produces a cohort report automatically, since "
      "that report is what every other engine is sold on",
      "Keep the Arabic interface first-class rather than translated, including "
      "right-to-left layout that is tested rather than assumed"],
     "Gate features shipped on time, and no cohort disrupted by a platform "
     "failure."),

    ("AI and data engineer", "CTO",
     "Makes the mentor good enough to be trusted with a learner, and the "
     "evidence record good enough to be trusted by a donor. Arrives in year four, "
     "when seat volume makes inference cost and assessment quality the binding "
     "problems.",
     ["Own the mentor's evaluation harness: a fixed set of learner situations, "
      "scored every release, in both languages",
      "Drive inference cost per learner down as seat volume rises, which is the "
      "difference between a seat business that works and one that does not",
      "Build the assessment model behind the readiness score, and document it "
      "well enough that a ministry's evaluator can interrogate it",
      "Own the data pipeline that turns cohort activity into the per-participant "
      "evidence record donors and initiatives require"],
     "Mentor quality scores rising while cost per learner falls, and a readiness "
     "score no evaluator has successfully challenged."),

    ("Product designer", "CTO",
     "Owns what a learner and a facilitator actually see. Arrives in year five; "
     "until then the CTO and the Head of Curriculum share the work and the plan "
     "says so rather than pretending design is free.",
     ["Own the learner experience in Arabic first, with English as the "
      "translation rather than the reverse",
      "Design for the room: a facilitator with twenty-five people and six days "
      "needs different screens from a learner at home",
      "Own the accessibility and reading-age standard for school and technical "
      "cohorts, where the audience is younger than the platform was built for",
      "Maintain the design system so two engineers can ship interface work "
      "without a designer in the loop"],
     "Measured task completion in the cohort room, and no facilitator workaround "
     "that exists because a screen was wrong."),

    # -------------------------------------------------- Curriculum and Delivery
    ("Head of Curriculum and Certification", "CEO",
     "Owns the standard — what is taught, what is assessed, and who is allowed "
     "to teach it. In a company that certifies rather than delivers, this is the "
     "role that protects the asset.",
     ["Own the mission curriculum and its three variants — university, school and "
      "technical — and the rule that a variant is a different programme, not a "
      "shortened one",
      "Own facilitator certification: the assessment, the pass mark, the "
      "re-certification cycle, and the willingness to fail candidates the "
      "company commercially needs to pass",
      "Own the certification standard that delivery partner organisations are "
      "audited against, and conduct the audits in year one and two",
      "Own the train-the-trainer curriculum that makes public-sector volume "
      "possible at all",
      "Own the mapping to external methodologies — the ILO's Start and Improve "
      "Your Business framework in particular — that donor procurement requires",
      "Carry product input on anything a learner touches, as the CTO's second "
      "opinion, until a designer arrives in year five"],
     "Cohort quality scores that do not fall as the network grows — the single "
     "number that says certification is real."),

    ("Partner network manager", "COO (the CEO until year four)",
     "Recruits, certifies, supports and audits the organisations and freelancers "
     "who deliver every cohort in this plan. The leverage of the whole business "
     "model sits in this one role.",
     ["Recruit and qualify delivery partner organisations — training providers, "
      "university innovation centres, youth NGOs — against a written standard, "
      "and reject the ones that do not meet it",
      "Run the facilitator pipeline from sourcing to certification to first "
      "supervised delivery, holding a pool large enough for peak quarters and "
      "small enough to keep busy",
      "Own partner economics: the revenue share, the invoicing, and the "
      "conversation when a partner wants a larger share than the standard",
      "Audit on sample and escalate any partner whose cohort scores drift, "
      "including withdrawal of the licence",
      "Hold the capacity forecast that sales is required to sell against, "
      "quarter by quarter"],
     "Certified capacity ahead of booked demand in every quarter, with no cohort "
     "cancelled for want of a facilitator."),

    ("Programme delivery coordinator", "COO (the CEO until year four)",
     "Makes the calendar happen: scheduling, logistics, reports and the hundred "
     "small failures that would otherwise reach the Head of Curriculum.",
     ["Schedule every cohort across both markets against certified capacity, and "
      "own the re-scheduling when a campus closes or a partner pulls out",
      "Provision accounts, materials and venues, and confirm readiness a week "
      "before each cohort rather than the day before",
      "Issue every cohort report inside five working days of the showcase",
      "Run the post-cohort data collection that feeds the evidence record, "
      "including chasing the facilitators who have not submitted",
      "Be the first line of support for partners and facilitators in delivery "
      "week"],
     "Every cohort starting on its scheduled date, and every report out inside "
     "five working days."),

    ("Bilingual curriculum producer", "Head of Curriculum and Certification",
     "Turns the standard into the material a facilitator can pick up and run "
     "without asking a question. Arrives in year five; until then the Head of "
     "Curriculum produces, with freelance editors on volume.",
     ["Produce facilitator guides, learner workbooks and slide decks in Arabic "
      "and English for all three format variants",
      "Produce the Mission Zero episode notes that attach each episode to the "
      "mission it illustrates",
      "Maintain version control so a partner in Riyadh and a partner in Assiut "
      "are demonstrably running the same release",
      "Manage the freelance translation and copy-editing panel against a "
      "published quality standard"],
     "No facilitator question that the material should have answered."),

    # ----------------------------------------------- Institutional Partnerships
    ("Head of Partnerships — Egypt", "CEO",
     "Owns every Egyptian institutional relationship until the engines are large "
     "enough to split. In year one that is universities, schools, competitions "
     "and sponsors in one pair of hands, and the plan is explicit that this is a "
     "merged role.",
     ["Open and close university cohort and faculty licence business across "
      "Egypt, working the four doors into an institution rather than the "
      "front one",
      "Carry competitions and corporate sponsors in year one, handing "
      "competitions to the government and initiatives head as that role lands "
      "in year three",
      "Carry schools and technical institutes until a dedicated head arrives in "
      "year four, with the honest consequence that the school engine is "
      "deliberately slower in years one and two",
      "Convert delivered cohorts into faculty licences, which is where the "
      "margin is and where most of this role's quota should come from",
      "Feed the named-target list and the engagement play applied to each, so "
      "pipeline is a plan rather than a list of contacts"],
     "Signed Egyptian revenue against quota, and the ratio of licences to "
     "one-off cohorts rising each year."),

    ("Country Manager — KSA (Riyadh)", "CEO",
     "Is the company in Saudi Arabia: a resident, Arabic-speaking principal who "
     "can sit with Monsha'at, the Misk Foundation and TVTC without an "
     "introduction.",
     ["Own the Saudi entity's commercial relationships across every engine — "
      "there is no engine split in Saudi Arabia until year five",
      "Open the three Saudi doors that matter most: the SME authority's academy, "
      "the youth foundations and the technical training corporation, each "
      "through the engagement play the plan specifies for it",
      "Recruit and hold the Saudi facilitator pool, where day rates, visas and "
      "availability work differently from Egypt",
      "Own Saudi compliance in practice: the entity, data residency, procurement "
      "registration and the paperwork that decides whether a public body can pay "
      "an invoice at all",
      "Localise rather than translate: Saudi institutions buy a Saudi programme, "
      "and a visibly Egyptian one will lose on preference alone"],
     "Saudi revenue per Saudi head above the Egyptian equivalent, which is what "
     "justifies the cost of the role."),

    ("Head of Government, Initiatives and Donors", "CEO",
     "Works the longest sales cycles in the company — ministries, agencies, "
     "national initiatives, donors and international organisations — and starts "
     "them years before they pay.",
     ["Own the seat-rider and trainer-certification plays into national "
      "initiatives, entering through a university or a governorate branch rather "
      "than through head office",
      "Own the donor logframe subcontract play: track published portfolios, "
      "identify components in design six to nine months out, and get StartPad "
      "named in the proposal before the call opens",
      "Own public procurement mechanics in both markets — registration, "
      "pre-qualification, bid formats and the paperwork that disqualifies "
      "otherwise winning bids",
      "Own the evidence record as a commercial asset, working with the Head of "
      "Curriculum so what a donor's monitoring function needs is what the "
      "platform already produces",
      "Carry competitions from year three, since the sponsors and the public "
      "bodies are substantially the same room"],
     "Pipeline measured in named opportunities with a dated decision point, not "
     "in meetings held."),

    ("Head of Schools and Technical Education", "COO",
     "Owns the engine with the largest population and the smallest budget per "
     "head, where volume has to come from ministries, chains and partners rather "
     "than from individual schools. Arrives in year four.",
     ["Own school and technical institute business across both markets, selling "
      "to chains, groups and ministry programmes rather than one school at a time",
      "Own the applied-technology and TVET relationships where the buyer is a "
      "public body and the play is certification",
      "Own safeguarding in the commercial conversation, since no school signs "
      "before it is satisfied and no school asks about it last",
      "Convert school cohorts into school licences, which is the only way this "
      "engine's unit economics work"],
     "School and technical revenue per sales day comparable to the university "
     "engine, despite a lower price point."),

    ("Partnerships and bids associate", "the relevant Head",
     "Does the work that would otherwise stop a head from selling: research, "
     "proposals, bids, contracting and the follow-up nobody has time for.",
     ["Maintain the named-target list — organisation, engine, engagement play, "
      "named contact, dated next step — as the company's actual pipeline",
      "Assemble proposals, tender responses and donor budget annexes against "
      "deadlines that do not move",
      "Run contracting and purchase-order chasing through to a payable invoice, "
      "which in public-sector work is a distinct skill",
      "Prepare the cohort reports and case studies that each head takes into the "
      "next meeting"],
     "No bid missed for an administrative reason, and no signed deal waiting on "
     "paperwork."),

    ("Account manager — renewals", "COO",
     "Exists because the second year of an institutional relationship is worth "
     "more than the first and is nobody's job while everyone is hunting. Arrives "
     "in year five, when the renewal book is large enough to justify it.",
     ["Own renewal and expansion for every institution past its first delivered "
      "cohort",
      "Run the structured review that turns a delivered cohort into the case for "
      "a faculty or school licence",
      "Hold the relationship through the staff turnover that is the real cause "
      "of institutional churn in this market",
      "Report renewal rate and expansion rate by engine, honestly"],
     "Renewal rate by engine at or above the retention assumed in the plan."),

    # ------------------------------------------------------ Growth and Content
    ("Head of Growth and Content", "CEO",
     "Owns demand: Mission Zero, the ambassador network, the content that makes "
     "an institution call first, and the community the subscription engine is "
     "drawn from.",
     ["Own Mission Zero end to end — guest booking, the campus recording "
      "schedule, the freelance crew, publication and the clip calendar — as a "
      "pipeline instrument measured in enquiries, not in views",
      "Run the campus ambassador network: recruitment, training, the stipend, "
      "and the monthly rhythm that keeps a volunteer network alive rather than "
      "nominal",
      "Own the annual readiness report, which is the company's single most "
      "effective door-opener into institutions and ministries",
      "Own organic acquisition into subscriptions, which the plan treats as a "
      "consequence of the institutional engines rather than a channel of its own",
      "Own brand consistency across two languages and every partner's "
      "co-branded material"],
     "Institutional enquiries attributable to content and Mission Zero, and cost "
     "per subscription from organic channels."),

    ("Student success (bilingual)", "COO",
     "Keeps the learners who arrived through somebody else's programme. Arrives "
     "in year five, when sponsored-seat volume makes activation the difference "
     "between a renewed seat order and a cancelled one.",
     ["Own activation of sponsored and initiative seats, where an unactivated "
      "seat is a line item the funder will not pay for twice",
      "Run the bilingual support queue for learners and for partner "
      "administrators",
      "Own the progression path from a completed cohort to a paid subscription, "
      "which is the entire subscription engine",
      "Feed recurring learner problems back to curriculum and product as "
      "evidence rather than anecdote"],
     "Seat activation rate, and the share of cohort completers who continue on "
     "a paid subscription."),
]

BY_ROLE = {r[0]: r for r in ROLE_SPECS}
