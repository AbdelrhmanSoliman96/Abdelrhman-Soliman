"""
The prospect universe for One Million Entrepreneurs in Egypt.

One row per organisation. The fields are deliberately split between what is
specific to the organisation (its own CSR focus, why it fits, the route in)
and what is common to its type (the vehicle, the documents, the objection,
the cadence), which lives in PLAYBOOK below. Repeating the mechanics on a
hundred rows would have made the registry unreadable and would have hidden
the one thing that differs between two banks, which is the programme they
already fund.

CONFIDENCE is the honesty column, and it is about this file, not about the
organisation:

  high    The organisation exists, its CSR or programme area is well
          established and stable, and nothing in the row depends on a
          programme cycle that may have closed.
  medium  The organisation and its focus are established; the specific
          programme, budget line or route named here is the kind of thing
          that changes between cycles and must be re-checked before it is
          quoted to anyone.
  low     A reasoned prospect rather than a confirmed one. Verify that the
          programme still exists before spending a meeting on it.

No individual's name, email address or phone number appears anywhere in this
file, by choice. Named contacts go stale faster than anything else in a
registry, and a wrong one burns the introduction. Every route is an
organisational door: a published channel, a role to ask for, or an
intermediary who can make the introduction.
"""

# ----------------------------------------------------------------- vocabulary
CATEGORIES = [
    "Telecom and technology",
    "Bank and financial services",
    "Energy, oil and gas",
    "FMCG, food and retail",
    "Industry, construction and real estate",
    "Pharma and healthcare",
    "Corporate and family foundation",
    "Bilateral donor and development agency",
    "UN agency and multilateral",
    "International NGO and implementer",
    "Egyptian NGO and social enterprise",
    "Youth and student organisation",
    "Government initiative and public agency",
    "Chamber, business association and network",
]

TIERS = {
    "A": "Open in the first quarter. Either the budget line already exists or "
         "the relationship opens several others.",
    "B": "Open once there is a delivered cohort to point at. Real prospects "
         "that will ask for proof first.",
    "C": "Keep warm. The fit is real but the cycle is long, the budget is "
         "small, or the mandate is adjacent rather than central.",
}

BANDS = {
    "XS": "Under $5,000. In kind, a venue, a prize, or a single workshop.",
    "S": "$5,000 to $25,000. One cohort, one competition round, one campus.",
    "M": "$25,000 to $100,000. A governorate programme or a season.",
    "L": "$100,000 to $500,000. A multi-site programme inside a larger grant.",
    "XL": "Above $500,000. A consortium bid or a national component.",
}


def P(name, cat, sector, reach, focus, fit, want, ask, band, unit, route,
      window, tier, conf, note, arabic=""):
    return dict(name=name, arabic=arabic, cat=cat, sector=sector, reach=reach,
                focus=focus, fit=fit, want=want, ask=ask, band=band, unit=unit,
                route=route, window=window, tier=tier, conf=conf, note=note)


PROSPECTS = [

    # ------------------------------------------- Telecom and technology
    P("Vodafone Egypt Foundation", "Telecom and technology",
      "Telecommunications", "National",
      "The CSR arm of Vodafone Egypt, registered as a foundation with the "
      "Ministry of Social Solidarity. Education, digital skills and youth "
      "empowerment, delivered partly through the Ta3limy e-learning platform.",
      "Already runs entrepreneurship bootcamps rather than only funding them, "
      "so the conversation is about capacity and reach, not about whether the "
      "theme fits. Mission content in Arabic plus a certified facilitator pool "
      "is exactly the part they buy in.",
      "Reach numbers at national scale, a digital asset that keeps working "
      "after the money is spent, and Egyptian youth employability they can "
      "report to group CSR in London.",
      "A named cohort programme under the foundation's youth pillar, plus "
      "mission content hosted alongside Ta3limy.",
      "M", "Foundation director, and the head of the youth or education "
      "pillar beneath them",
      "The foundation page on web.vodafone.com.eg carries the registered "
      "entity and its contact channel. Warmer route: an NGO already "
      "implementing for them, or the AmCham CSR committee.",
      "Vodafone runs an April to March financial year, so the budget "
      "conversation is strongest between November and January.",
      "A", "high",
      "Confirmed this session: the foundation ran a Spark Bootcamp with the "
      "Momken platform for 40 early-stage tech entrepreneurs, with content "
      "folded into Ta3limy. Verify the current cohort cycle before quoting.",
      arabic="مؤسسة فودافون مصر"),

    P("Orange Egypt", "Telecom and technology",
      "Telecommunications", "National, with a Delta and Upper Egypt focus",
      "Orange Social Venture Prize, long-running Enactus Egypt sponsorship, "
      "and Orange Digital Centers. Entrepreneurship is a standing line, not "
      "a one-off campaign.",
      "The single most consistent corporate funder of student entrepreneurship "
      "in Egypt. They buy the competition and the training around it, which is "
      "two of our engines in one relationship.",
      "Visible national impact, a pipeline of ventures for the Social Venture "
      "Prize, and governorate coverage outside Cairo.",
      "Mission-based preparation for Social Venture Prize entrants, plus "
      "cohorts in the governorates their digital centres already serve.",
      "M", "CSR and sustainability manager, with the Orange Digital Center "
      "lead as the operational counterpart",
      "Orange Digital Center Cairo is the open door: it hosts programmes and "
      "its team can route an offer internally. Enactus Egypt can introduce.",
      "Calendar year budgeting, with the Social Venture Prize local round "
      "running in the first half of the year.",
      "A", "high",
      "Confirmed this session: twenty consecutive years sponsoring Enactus "
      "Egypt, and three Egyptian startups advanced to the Social Venture "
      "Prize international stage in the sixteenth edition.",
      arabic="أورانج مصر"),

    P("Etisalat by e& Egypt", "Telecom and technology",
      "Telecommunications", "National",
      "Digital inclusion, education and youth programmes under the group's "
      "sustainability framework.",
      "The third telco, and the one with the least crowded entrepreneurship "
      "shelf. A differentiated position is available to whoever brings a "
      "structured programme rather than a sponsorship request.",
      "A programme of its own rather than a share of someone else's, and "
      "numbers that stand up in the group sustainability report.",
      "An exclusive governorate programme branded with them, priced per "
      "cohort, with a published results report.",
      "S", "Sustainability or corporate communications manager",
      "Corporate sustainability contact on the e& Egypt site; the UAE parent "
      "publishes the group framework the local report rolls into.",
      "Calendar year, with group reporting pressure in the fourth quarter.",
      "B", "medium",
      "Entity and CSR theme are established; no current entrepreneurship "
      "programme confirmed in this session. Treat the programme angle as a "
      "proposal, not as a response to something they run."),

    P("Telecom Egypt (WE)", "Telecom and technology",
      "Telecommunications", "National",
      "State-linked operator with CSR anchored in digital literacy, "
      "connectivity for schools, and national initiative support.",
      "Follows the government agenda closely, so an initiative framed around "
      "the national one-million-entrepreneurs ambition travels well inside "
      "their approval chain.",
      "Alignment with national priorities and with Haya Karima style reach "
      "into underserved governorates.",
      "Connectivity plus seats for a governorate cohort series, co-branded "
      "with the national initiative.",
      "S", "CSR manager, under corporate communications",
      "Approach through the national initiative rather than cold: a letter "
      "from Rowad 2030 or MSMEDA naming them as a partner carries further.",
      "State fiscal year begins in July, so proposals land best in the "
      "February to April window.",
      "B", "medium",
      "CSR orientation is well established; the specific programme fit is "
      "inferred from their public positioning."),

    P("Huawei Egypt", "Telecom and technology",
      "Technology", "National",
      "Seeds for the Future, ICT Academy and ICT Competition, run with "
      "universities and the ICT ministry.",
      "Already operates a university-facing programme machine with ministry "
      "cover. Entrepreneurship is the missing layer on top of their technical "
      "training, and that layer is what we sell.",
      "University relationships, ministry visibility, and graduates who can "
      "be named in the programme report.",
      "An entrepreneurship track bolted onto ICT Academy cohorts, delivered "
      "by certified facilitators on their campuses.",
      "S", "Public affairs or CSR director, with the ICT Academy programme "
      "manager as the operational owner",
      "The ICT Academy university network is the route: a partner university "
      "can propose the add-on upward. ITIDA also convenes them.",
      "Programme cycles follow the academic year, so the window is May to "
      "August for the following year.",
      "B", "medium",
      "Programme names are well established regionally; confirm the Egypt "
      "cycle and the current academy partners before proposing."),

    P("Microsoft Egypt", "Telecom and technology",
      "Technology", "National",
      "Skills initiatives, nonprofit grants and cloud credits, with "
      "employability as the stated outcome.",
      "Buys employability outcomes at scale and works through implementing "
      "partners rather than running delivery itself, which is the shape of "
      "relationship this business is built for.",
      "Measurable skilling numbers, a credible local implementer, and "
      "alignment with their own skilling taxonomy.",
      "Delivery partner status for an entrepreneurship skilling track, with "
      "platform credits covering the technical cost.",
      "M", "Philanthropies or corporate social responsibility lead for the "
      "Middle East and Africa, with the Egypt country team sponsoring",
      "Microsoft philanthropies works through registered nonprofits: the "
      "cleanest route is as the delivery partner of an NGO already in their "
      "grantee list.",
      "Microsoft's financial year begins in July, so the proposal window is "
      "March to May.",
      "B", "medium",
      "Global programme structure is stable; the Egypt-specific budget line "
      "is not confirmed here."),

    P("Google", "Telecom and technology",
      "Technology", "Regional, with Egypt coverage",
      "Google.org grants, Hustle Academy and Google for Startups programmes "
      "across the Middle East and Africa.",
      "Funds entrepreneurship training directly and prefers scalable, "
      "content-led delivery. One million as a number is the kind of ambition "
      "their grant committee is built to read.",
      "Scale, digital delivery, and evidence of outcomes rather than outputs.",
      "A grant application under the small business or youth skilling theme, "
      "with the platform as the scaling mechanism.",
      "L", "Google.org regional lead, via an open call rather than a named "
      "contact",
      "Open calls on google.org, plus the Google for Startups community in "
      "Cairo as the informal route to intelligence on timing.",
      "Open calls appear irregularly. Subscribe rather than chase.",
      "C", "medium",
      "Programmes exist regionally; Egypt eligibility and current calls must "
      "be checked at the time of applying."),

    P("Meta", "Telecom and technology",
      "Technology", "Regional, with Egypt coverage",
      "Boost with Meta and small business training programmes, usually "
      "delivered through local implementing partners.",
      "Their small business training is weaker on venture formation than on "
      "marketing. A structured fifteen-step method is a complement rather "
      "than a competitor.",
      "Small business reach numbers and local language delivery.",
      "Co-delivery of a business formation module inside their existing "
      "small business training.",
      "S", "Public policy or community partnerships manager for North Africa",
      "Through an existing implementing partner. Direct approaches to Meta "
      "without one rarely land.",
      "Programme-driven rather than seasonal.",
      "C", "low",
      "Fit is reasoned, not confirmed. Verify that the Egypt programme is "
      "still running before investing time."),

    P("IBM Egypt", "Telecom and technology",
      "Technology", "National",
      "SkillsBuild and corporate citizenship grants focused on employability "
      "and digital skills.",
      "SkillsBuild is content plus certification with no entrepreneurship "
      "layer. The complement is obvious and the integration is low effort.",
      "Learner numbers, certification completion, and university partners.",
      "An entrepreneurship pathway inside SkillsBuild for Egyptian "
      "universities.",
      "S", "Corporate social responsibility lead, Egypt or Middle East and "
      "Africa",
      "Universities already inside SkillsBuild can propose the pathway "
      "upward, which is faster than a direct approach.",
      "Academic year cycles.",
      "C", "medium",
      "SkillsBuild is a stable global programme; the Egypt partner list "
      "needs checking."),

    P("Dell Technologies Egypt", "Telecom and technology",
      "Technology", "Greater Cairo",
      "Digital inclusion and youth skilling, with a large Egyptian delivery "
      "centre giving the local entity real weight.",
      "A large local employer with a CSR budget and a hiring interest in the "
      "same population we train.",
      "Local employer brand, a talent pipeline, and employee volunteering "
      "opportunities.",
      "A cohort series with employee mentors drawn from their own staff.",
      "XS", "Country general manager's office, through corporate "
      "communications",
      "Employee volunteering is the easiest entry: it needs a smaller "
      "approval than a cash sponsorship and it builds the relationship.",
      "Calendar year.",
      "C", "low",
      "Reasoned prospect. No specific Egyptian CSR programme confirmed."),

    P("Fawry", "Telecom and technology",
      "Fintech", "National",
      "Financial inclusion, merchant enablement and SME digitisation, with "
      "a CSR narrative built around small business.",
      "Their customer is the micro-business our learners are trying to "
      "become. Training that produces formalised micro-businesses is "
      "commercially useful to them, not only reputationally.",
      "Merchant acquisition that looks like social impact, and SME "
      "formalisation numbers.",
      "Sponsored cohorts in governorates where they are expanding, with "
      "their merchant services introduced inside the business model mission.",
      "S", "Marketing or sustainability director",
      "Direct, through corporate communications. Their SME team is the "
      "stronger internal sponsor than CSR.",
      "Calendar year, with budget set in the fourth quarter.",
      "B", "medium",
      "Commercial logic is strong; the CSR budget line is not confirmed."),

    P("e-finance Investment Group", "Telecom and technology",
      "Fintech, state-linked", "National",
      "Digital transformation of government services, with CSR tied to the "
      "national digital agenda.",
      "State-linked and therefore responsive to initiative framing. Their "
      "mandate touches every ministry that matters to this plan.",
      "Visible contribution to the national digital and entrepreneurship "
      "agenda.",
      "Sponsorship of an initiative component, framed as digital inclusion.",
      "S", "Chairman's office, through corporate communications",
      "Through the Ministry of Communications and Information Technology or "
      "ITIDA rather than cold.",
      "State fiscal year from July.",
      "C", "low",
      "Reasoned prospect based on mandate, not on a confirmed CSR line."),

    # --------------------------------------- Bank and financial services
    P("Commercial International Bank (CIB) and the CIB Foundation",
      "Bank and financial services", "Banking", "National",
      "The CIB Foundation receives a fixed share of the bank's net annual "
      "profit and concentrates on child health and nutrition. The bank "
      "itself runs sustainable finance, SME banking and financial literacy "
      "under responsible banking, separately from the foundation.",
      "Two doors, and the obvious one is the wrong one. The foundation's "
      "mandate is health, so the entrepreneurship ask belongs to the bank's "
      "SME and sustainable finance side, where the commercial logic of "
      "building bankable micro-businesses is strongest.",
      "A pipeline of formalised, bankable small businesses, financial "
      "literacy numbers, and sustainable finance reporting content.",
      "A financial literacy and business formation track inside their SME "
      "banking outreach, priced per cohort.",
      "M", "Head of sustainable finance, and separately the head of SME "
      "banking. The foundation's director only if the ask becomes health "
      "adjacent, which it should not",
      "Do not route this through the foundation. Approach through SME "
      "banking or through the Central Bank's NilePreneurs network, where "
      "CIB is an active participant.",
      "Calendar year, with the sustainability report published in the first "
      "quarter and budget set in the fourth.",
      "A", "high",
      "Confirmed this session: the foundation is health and nutrition "
      "focused, funded by a fixed percentage of net annual profit, and its "
      "2025 report covers 219 projects with 70 partners. Pitching "
      "entrepreneurship to the foundation would be a wasted meeting."),

    P("National Bank of Egypt (NBE)", "Bank and financial services",
      "Banking, state-owned", "National",
      "The largest CSR budget in Egyptian banking. Education, health, youth "
      "and national initiative support, plus direct sponsorship of student "
      "entrepreneurship competitions.",
      "Already sponsors Enactus Egypt's national competition, which is "
      "exactly our competitions engine. The relationship can widen from a "
      "competition sponsorship into the training that feeds it.",
      "National reach, visible association with youth achievement, and "
      "alignment with state priorities.",
      "Preparation cohorts for the competition they already sponsor, plus a "
      "governorate programme under the national initiative banner.",
      "L", "General manager for corporate social responsibility, under the "
      "chairman's office",
      "Enactus Egypt can introduce, having the sponsorship relationship "
      "already. Rowad 2030 is the other credible referrer.",
      "State-linked budgeting with the academic year driving competition "
      "timing. Approach by August for the following academic year.",
      "A", "high",
      "Confirmed this session: NBE took part in the Enactus Egypt local "
      "finals for the 2025/2026 academic year."),

    P("Banque Misr", "Bank and financial services",
      "Banking, state-owned", "National",
      "Four ESG pillars reported under the Global Reporting Initiative, with "
      "an inclusive society pillar covering youth and community programmes. "
      "Long-running entrepreneurship support through its innovation arm.",
      "Reports under GRI, which means it needs programmes that produce "
      "countable, attributable social outcomes. A cohort report with named "
      "institutions and completion rates is written for exactly that need.",
      "Reportable inclusive-society numbers, SME formalisation, and "
      "alignment with the Central Bank's sustainable finance principles.",
      "A named youth entrepreneurship component inside the inclusive society "
      "pillar, with quarterly reporting built in.",
      "L", "Head of sustainability or responsible banking, with the SME and "
      "innovation unit as co-sponsor",
      "The sustainability team is reachable through the responsible banking "
      "pages. NilePreneurs and the Central Bank network are the warm routes.",
      "Calendar year, with the GRI report cycle driving demand for "
      "attributable numbers in the fourth quarter.",
      "A", "high",
      "Confirmed this session: first state-owned bank to publish an annual "
      "GRI sustainability report for six consecutive years, organised "
      "around four ESG pillars including inclusive society."),

    P("QNB Alahli", "Bank and financial services",
      "Banking", "National",
      "Education, youth and community CSR, with SME banking as a strategic "
      "commercial line.",
      "Strong SME book and a CSR function that funds education. The bridge "
      "between the two is business formation training.",
      "SME customer acquisition that reports as social impact.",
      "A financial literacy plus business formation series for their SME "
      "customer base and for university cohorts in their catchment.",
      "M", "Head of communications and CSR, with SME banking as internal "
      "sponsor",
      "Direct through corporate communications, or through the Federation of "
      "Egyptian Banks working groups.",
      "Calendar year.",
      "B", "medium",
      "CSR and SME lines both established; no entrepreneurship programme "
      "confirmed in this session."),

    P("Arab African International Bank (AAIB)",
      "Bank and financial services", "Banking", "National",
      "One of the more sustainability-forward Egyptian banks, with a "
      "dedicated sustainability function and published commitments.",
      "A bank that has already built the internal machinery for programme "
      "funding and measurement, which shortens the approval path.",
      "Sustainability reporting content and visible youth impact.",
      "A sponsored cohort series with sustainability reporting attached.",
      "M", "Chief sustainability officer or head of sustainable development",
      "Direct, through the sustainability function rather than marketing.",
      "Calendar year.",
      "B", "medium",
      "Sustainability positioning is established; the specific budget line "
      "is unconfirmed."),

    P("Bank of Alexandria (Intesa Sanpaolo)",
      "Bank and financial services", "Banking", "National",
      "Micro and small enterprise lending, financial inclusion, and a "
      "parent group with a strong impact-banking tradition.",
      "Their microfinance customers are the graduates of exactly this kind "
      "of training. Impact banking at group level makes the internal case "
      "easier than at a purely domestic bank.",
      "Borrower quality, default reduction through better-prepared "
      "businesses, and group impact reporting.",
      "Pre-loan business formation training for microfinance applicants.",
      "M", "Head of micro and small enterprises, with CSR as co-sponsor",
      "Through the micro and small enterprise business line, where the "
      "commercial case is strongest.",
      "Calendar year, with group reporting in the first quarter.",
      "B", "medium",
      "Commercial logic strong; programme not confirmed."),

    P("HSBC Egypt", "Bank and financial services",
      "Banking, international", "Greater Cairo and Alexandria",
      "Future Skills and education grants under a global community "
      "investment framework, run through registered NGO partners.",
      "Funds through NGOs on an annual grant cycle with a published "
      "framework, so the process is knowable and repeatable rather than "
      "relationship-dependent.",
      "Employability and future skills outcomes that roll into global "
      "community investment reporting.",
      "An annual grant application, submitted with or through a registered "
      "NGO partner.",
      "M", "Head of corporate sustainability, Egypt",
      "Annual grant cycle through the corporate sustainability team. An "
      "existing grantee NGO as co-applicant materially improves the odds.",
      "Grant cycles typically open once a year. Ask the timing early.",
      "B", "medium",
      "Global framework is stable; the Egypt cycle and themes need "
      "confirming each year."),

    P("Credit Agricole Egypt", "Bank and financial services",
      "Banking, international", "National",
      "A structured CSR programme covering education, environment and "
      "community development, reported to the French parent.",
      "French parent reporting means a documented programme with a measured "
      "outcome is preferred over a logo sponsorship.",
      "Documented social impact for group reporting.",
      "A measured cohort programme with a published results report.",
      "S", "CSR manager",
      "Direct. Their CSR function is comparatively accessible.",
      "Calendar year.",
      "B", "medium",
      "CSR function established; specific fit unconfirmed."),

    P("Abu Dhabi Islamic Bank Egypt", "Bank and financial services",
      "Islamic banking", "National",
      "Community and youth CSR with a zakat and social finance dimension "
      "alongside conventional CSR.",
      "Islamic social finance instruments can fund training for low-income "
      "entrepreneurs where a conventional marketing budget could not.",
      "Social finance deployment that is both compliant and reportable.",
      "A cohort programme for low-income entrepreneurs funded through the "
      "social finance route.",
      "S", "Head of CSR, with sharia governance consulted on the funding "
      "route",
      "Direct. Expect the sharia compliance question early and prepare for "
      "it.",
      "Hijri and calendar considerations both apply. Ramadan is a strong "
      "giving window but a weak delivery one.",
      "C", "low",
      "Reasoned prospect. The social finance route needs verifying with "
      "them directly."),

    P("Export Development Bank of Egypt (EBank)",
      "Bank and financial services", "Development banking", "National",
      "SME and export development mandate, with sustainability and "
      "entrepreneurship support attached to it.",
      "A development mandate rather than a marketing budget, which means "
      "programme funding is a normal instrument rather than an exception.",
      "SME development numbers against a public mandate.",
      "A programme for export-capable small businesses, framed against "
      "their mandate.",
      "M", "Head of sustainability or SME development",
      "Direct, through the SME or sustainable development function.",
      "State-linked fiscal year from July.",
      "B", "medium",
      "Mandate is clear; programme fit to be confirmed."),

    P("Banque du Caire", "Bank and financial services",
      "Banking, state-owned", "National, strong governorate footprint",
      "Microfinance at scale, financial inclusion, and community CSR.",
      "One of the largest microfinance books in Egypt, reaching exactly the "
      "governorates a national initiative has to serve.",
      "Better-prepared microfinance borrowers and inclusion numbers.",
      "Business formation training attached to microfinance disbursement in "
      "target governorates.",
      "M", "Head of microfinance, with CSR as secondary",
      "Through the microfinance business line.",
      "State-linked fiscal year from July.",
      "B", "medium",
      "Microfinance scale is well established; programme fit is a proposal."),

    P("Visa", "Bank and financial services",
      "Payments", "Regional, with Egypt coverage",
      "Small business enablement and financial literacy programmes across "
      "the Middle East and North Africa, usually delivered through partners.",
      "Their small business programmes need local delivery capacity and "
      "Arabic content, which is what we supply.",
      "Merchant digitisation, financial literacy reach, and a credible "
      "local delivery partner.",
      "Delivery partner status for a small business enablement programme.",
      "M", "Social impact or government engagement lead for North Africa",
      "Through their Egyptian bank partners, who can sponsor the "
      "introduction, rather than cold to the regional office.",
      "Programme-driven.",
      "C", "medium",
      "Regional programmes are established; Egypt delivery partners and "
      "current cycle need checking."),

    P("Mastercard and the Mastercard Foundation",
      "Bank and financial services", "Payments and philanthropy",
      "Africa-wide, Egypt coverage varies",
      "Mastercard runs inclusive growth programmes; the Mastercard "
      "Foundation is a separate and very large funder of youth employment "
      "in Africa under Young Africa Works.",
      "The foundation is the largest youth employment funder on the "
      "continent and works in multi-year country partnerships. If Egypt is "
      "a partner country in the current strategy this is the single biggest "
      "cheque in this file. If it is not, it is a waste of a quarter.",
      "Dignified work at country scale, measured in young people employed "
      "or self-employed, over multi-year horizons.",
      "A consortium partnership, almost certainly as a delivery partner "
      "rather than as the lead.",
      "XL", "Country director if Egypt is a partner country; otherwise the "
      "regional programme team",
      "Verify Egypt's status in their current country strategy before "
      "anything else. If it is active, route through an existing country "
      "partner.",
      "Multi-year strategy cycles, not annual budgets.",
      "C", "low",
      "Egypt's status in the foundation's country strategy is NOT confirmed "
      "here and historically their focus has been sub-Saharan. Check first. "
      "This row is a lottery ticket, not a plan."),

    # ------------------------------------------------ Energy, oil and gas
    P("Shell Egypt", "Energy, oil and gas", "Oil and gas", "National",
      "Shell Intilaaqah, a long-running youth enterprise development "
      "programme, alongside STEM and scholarship work.",
      "Intilaaqah is a youth enterprise programme already operating in "
      "Egypt. This is the closest thing in the corporate sector to a "
      "pre-existing budget line for what we do.",
      "Continuity of a flagship programme, cost per beneficiary, and "
      "measurable business creation.",
      "Delivery or curriculum partner status for Intilaaqah cohorts, with "
      "the platform carrying the part their facilitators cannot.",
      "M", "Social investment or social performance manager",
      "Direct to social investment. Their current implementing partner can "
      "also sub-contract delivery, which is a faster first step.",
      "Calendar year, with social investment budgets set in the fourth "
      "quarter.",
      "A", "medium",
      "Intilaaqah is a long-established Shell programme in several "
      "countries including Egypt. Confirm the Egypt cycle and current "
      "implementing partner before proposing."),

    P("bp Egypt", "Energy, oil and gas", "Oil and gas",
      "National, with a strong Mediterranean and Delta footprint",
      "Social investment tied to the communities around its operations, "
      "covering education, employability and enterprise.",
      "Operates under a social investment obligation near its concessions, "
      "which means geography-specific programmes in the Delta and the north "
      "coast are easier to fund than national ones.",
      "Licence to operate in host communities, local employment and "
      "enterprise creation near operations.",
      "A governorate programme in their operating areas, costed per cohort "
      "and reported by community.",
      "M", "Social investment manager, with the local external affairs lead",
      "Direct to external affairs or social investment. Local governorate "
      "authorities can also refer.",
      "Calendar year, with multi-year social investment commitments.",
      "B", "medium",
      "Social investment practice is standard across their operations; the "
      "Egypt programme list is unconfirmed here."),

    P("ExxonMobil Egypt", "Energy, oil and gas",
      "Oil, gas and lubricants", "National",
      "Corporate citizenship covering education, women's economic "
      "opportunity and community investment. Named in this plan's partner "
      "list for competition sponsorship.",
      "Women's economic opportunity is a stated global priority and maps "
      "directly onto a women-focused cohort series.",
      "Women's economic empowerment numbers, and visible community "
      "investment.",
      "A women's entrepreneurship cohort series across three governorates.",
      "M", "Public and government affairs manager",
      "Direct to public and government affairs. AmCham Egypt is the warm "
      "route, where they are an active member.",
      "Calendar year.",
      "B", "medium",
      "Corporate citizenship themes are stable globally; the Egypt budget "
      "line is unconfirmed."),

    P("TotalEnergies Egypt", "Energy, oil and gas",
      "Energy and fuel retail", "National",
      "A corporate foundation with youth inclusion and education as stated "
      "priorities, plus road safety and energy access.",
      "Youth inclusion is the foundation's own language, and the French "
      "group structure means a documented programme with evaluation is "
      "preferred over sponsorship.",
      "Youth inclusion outcomes documented to foundation standards.",
      "A youth inclusion programme proposal to the foundation, with an "
      "external evaluation budgeted in.",
      "M", "Foundation or CSR coordinator, Egypt, reporting to the group "
      "foundation",
      "Direct, through the Egypt corporate affairs function, which routes "
      "to the group foundation.",
      "Group foundation cycles, typically annual with a documented call.",
      "B", "medium",
      "Foundation themes are published at group level; the Egypt pipeline "
      "is unconfirmed."),

    P("Eni Egypt (IEOC)", "Energy, oil and gas", "Oil and gas",
      "National, with Port Said and Mediterranean focus",
      "Local development programmes negotiated with the state as part of "
      "its concession commitments, covering education, health and "
      "vocational training.",
      "Their local development commitments are large, state-negotiated and "
      "long-term. Vocational training is already inside the envelope; "
      "enterprise creation is the natural extension.",
      "Delivery against concession-linked development commitments, in the "
      "specific governorates named in them.",
      "An enterprise track attached to an existing vocational training "
      "commitment.",
      "L", "Sustainability and local development manager",
      "Through the Ministry of Petroleum relationship or the existing "
      "vocational training implementer, not cold.",
      "Multi-year commitments reviewed annually.",
      "B", "low",
      "The commitment structure is real; whether an enterprise component "
      "can be added mid-cycle is unverified."),

    P("Apache Egypt and Khalda Petroleum", "Energy, oil and gas",
      "Oil and gas", "Western Desert and national",
      "One of the largest private social investment records in Egypt, "
      "historically centred on building and equipping schools for girls.",
      "A proven willingness to fund education at scale over many years. "
      "The schools they built are a delivery network for the schools "
      "engine, not only a funding source.",
      "Continuity of an education legacy, and girls' education and "
      "employability outcomes.",
      "An enterprise and employability track in the schools they already "
      "built, which is a low-friction ask.",
      "M", "Public affairs or community development manager",
      "Direct. The schools themselves are also a route upward.",
      "Calendar year.",
      "B", "medium",
      "The girls' education programme is a well-known, long-running "
      "commitment. Current scale and focus need confirming."),

    P("Schlumberger (SLB) Egypt", "Energy, oil and gas",
      "Oilfield services", "National",
      "STEM education, technical training and community programmes near "
      "operations.",
      "Technical education focus overlaps the technical and vocational "
      "engine, where employability framing is what sells.",
      "Technical talent pipeline and STEM outcomes.",
      "An enterprise module inside technical institute cohorts.",
      "S", "Community affairs or HR community programmes lead",
      "Through technical institutes they already support.",
      "Calendar year.",
      "C", "low", "Reasoned prospect; no Egypt programme confirmed."),

    P("Elsewedy Electric", "Energy, oil and gas",
      "Electrical industry and infrastructure", "National",
      "Technical education at scale, including its own technical academy "
      "and applied technology school partnerships with the state.",
      "They run applied technology schools in partnership with the Ministry "
      "of Technical Education. That is the schools engine's single most "
      "valuable private counterpart in Egypt.",
      "Employable technical graduates, and a flagship education story "
      "aligned with the state's technical education reform.",
      "An entrepreneurship and employability track across their applied "
      "technology schools and academy.",
      "M", "Head of the technical academy, with the group CSR or "
      "sustainability function",
      "Through the academy directly, and in parallel through the Ministry "
      "of Technical Education and Training, which co-owns the schools.",
      "Academic year, so approach between April and July.",
      "A", "medium",
      "Their applied technology school involvement is well established. "
      "Confirm the current school list and the academy's intake cycle."),

    # ------------------------------------------------ FMCG, food, retail
    P("Nestle Egypt", "FMCG, food and retail", "Food and beverage",
      "National",
      "Nestle Needs YOUth, a global youth employability and entrepreneurship "
      "commitment, plus agricultural and community programmes.",
      "Needs YOUth is a standing global commitment with country targets. "
      "Local programmes are expected to be delivered through partners, "
      "which is the role we are built for.",
      "Young people reached, jobs and businesses created, reported into the "
      "global commitment.",
      "A Needs YOUth entrepreneurship cohort series, costed per young "
      "person reached.",
      "M", "Corporate communications and public affairs manager, who "
      "typically owns Needs YOUth locally",
      "Direct to corporate affairs, naming the global commitment. AmCham is "
      "the warm route.",
      "Calendar year, with global commitment reporting in the first "
      "quarter.",
      "A", "medium",
      "Needs YOUth is a long-standing global programme; the Egypt country "
      "plan and partner list need confirming."),

    P("PepsiCo Egypt", "FMCG, food and retail", "Food and beverage",
      "National, with Upper Egypt agricultural presence",
      "PepsiCo Foundation and local community investment, covering "
      "agriculture, water, women's economic empowerment and youth.",
      "Women's economic empowerment and agricultural livelihoods are both "
      "funded themes, and both map onto cohorts in Upper Egypt where their "
      "supply chain sits.",
      "Supply chain community goodwill, women's economic participation, and "
      "foundation reporting.",
      "A women's and agricultural enterprise cohort series in their "
      "sourcing governorates.",
      "M", "Public policy and government affairs, with the PepsiCo "
      "Foundation for larger asks",
      "Direct to public affairs; the foundation requires a US-facing "
      "application usually sponsored by the country team.",
      "Calendar year.",
      "B", "medium",
      "Themes are established globally and the Egyptian agricultural "
      "footprint is real; the current programme list is unconfirmed."),

    P("The Coca-Cola Company and Coca-Cola Egypt",
      "FMCG, food and retail", "Beverages", "National",
      "Coca-Cola Foundation grants, water stewardship, and women's economic "
      "empowerment programmes with a long history in Egypt.",
      "Their women's economic empowerment work has run in Egypt for years "
      "through NGO partners, and micro-retail is the business type their "
      "distribution already touches.",
      "Women-owned micro-business creation, and retail network goodwill.",
      "A women's micro-enterprise programme tied to their retail network.",
      "M", "Public affairs, communications and sustainability manager",
      "Direct, and through the Coca-Cola Foundation grant route for larger "
      "amounts. An existing NGO partner shortens the path.",
      "Calendar year, with foundation grant cycles announced annually.",
      "B", "medium",
      "Women's economic empowerment work in Egypt is well established; the "
      "current partner and cycle are unconfirmed."),

    P("Unilever Mashreq", "FMCG, food and retail",
      "Consumer goods", "National",
      "Sustainable living programmes, women's empowerment through "
      "distribution networks, and youth skilling.",
      "Distribution-led women's entrepreneurship is a model they have run "
      "elsewhere in emerging markets and it needs exactly this kind of "
      "training content.",
      "Distributor network growth that reads as empowerment, plus skilling "
      "numbers.",
      "Business formation training for their women distributors and for "
      "youth cohorts in their market towns.",
      "S", "Sustainability or corporate affairs manager",
      "Direct to corporate affairs.",
      "Calendar year.",
      "C", "low", "Reasoned prospect based on their model elsewhere."),

    P("Juhayna Food Industries", "FMCG, food and retail",
      "Dairy and juice", "National, with agricultural supply chain",
      "Agricultural development, farmer support and community programmes, "
      "with a family foundation tradition behind the company.",
      "Farmer and agribusiness development is a stated interest, and "
      "agribusiness is one of the easiest venture types to teach and to "
      "evidence.",
      "Supply chain resilience and rural livelihoods.",
      "An agribusiness enterprise cohort series in their sourcing areas.",
      "S", "Corporate affairs, with the family foundation for larger asks",
      "Direct, or through the Egyptian Junior Business Association network "
      "where the family is active.",
      "Calendar year.",
      "C", "medium",
      "Agricultural community work is established; the entrepreneurship "
      "angle is a proposal."),

    P("Edita Food Industries", "FMCG, food and retail",
      "Packaged food", "National",
      "Community and education CSR, with a strong Upper Egypt and "
      "industrial town presence.",
      "Mid-sized corporate with a decision chain short enough to say yes "
      "within a quarter, which matters more than budget size early on.",
      "Local goodwill around plants, and employee engagement.",
      "A single-governorate cohort series near their operations.",
      "XS", "Corporate communications or HR director",
      "Direct. Mid-caps answer email.",
      "Calendar year.",
      "C", "low", "Reasoned prospect."),

    P("Mansour Group", "FMCG, food and retail",
      "Diversified: distribution, retail, automotive", "National",
      "Large family group with retail, distribution and automotive arms, "
      "and an associated family philanthropic tradition.",
      "Their retail and distribution networks are a delivery channel into "
      "micro-retail entrepreneurs, and the family foundation route carries "
      "larger amounts than a marketing budget would.",
      "Micro-retailer capability, family legacy, and national reach.",
      "A micro-retail enterprise programme using their distribution "
      "network as the channel.",
      "M", "Group corporate affairs, with the family foundation separately",
      "Through the Egyptian Businessmen's Association or AmCham, where the "
      "group is prominent.",
      "Calendar year.",
      "B", "low",
      "The group's scale is certain; the philanthropic route and its "
      "current priorities need verifying."),

    # --------------------- Industry, construction and real estate
    P("Orascom Construction and the Sawiris family companies",
      "Industry, construction and real estate", "Construction", "National",
      "Technical training and construction skills programmes, alongside the "
      "family's separate philanthropic vehicles.",
      "Construction trades are the clearest case for the technical and "
      "vocational engine: a trade turned into a small contracting business "
      "is a story their own workforce understands.",
      "A skilled trade pipeline and demonstrable local employment.",
      "An enterprise track for trained tradespeople, framed as "
      "self-employment rather than as entrepreneurship.",
      "M", "Corporate communications, with the technical training function "
      "as the operational counterpart",
      "Approach the technical training function first. The Sawiris "
      "Foundation is a separate organisation and a separate ask.",
      "Calendar year.",
      "B", "medium",
      "Technical training activity is established in the sector; the "
      "specific programme is unconfirmed."),

    P("Hassan Allam Holding", "Industry, construction and real estate",
      "Construction and infrastructure", "National",
      "Community investment around projects, technical training, and a "
      "growing sustainability function.",
      "Project-linked community investment means geographically targeted "
      "programmes are fundable where a national ask would not be.",
      "Community acceptance around projects and local employment.",
      "Cohorts in the communities around a named project.",
      "S", "Sustainability or corporate communications lead",
      "Direct, or through the project's community liaison.",
      "Project-driven rather than seasonal.",
      "C", "low", "Reasoned prospect."),

    P("Talaat Moustafa Group", "Industry, construction and real estate",
      "Real estate", "National",
      "Large-scale community development around its cities, plus education "
      "and sports facilities.",
      "They build cities and need the small businesses that make them work. "
      "Micro-business creation inside their developments is a commercial "
      "interest, not only a CSR one.",
      "Occupied retail units, serviced communities, and brand.",
      "A micro-business creation programme for residents and service "
      "providers inside their communities.",
      "S", "Corporate communications and community management",
      "Through community management rather than CSR.",
      "Calendar year.",
      "C", "low", "Reasoned prospect."),

    P("Madinet Masr", "Industry, construction and real estate",
      "Real estate", "Greater Cairo",
      "Community and youth programmes, and a named private-sector partner "
      "of the Orange Corners entrepreneurship programme in Egypt.",
      "Already a partner in a donor-funded entrepreneurship programme, "
      "which means the internal argument for entrepreneurship is already "
      "won. The question is only what they fund next.",
      "Association with a credible entrepreneurship programme and community "
      "development around their developments.",
      "A cohort series co-branded with their existing entrepreneurship "
      "involvement.",
      "S", "Corporate communications or sustainability lead",
      "Through Orange Corners Egypt, where the relationship already exists.",
      "Calendar year.",
      "A", "high",
      "Confirmed this session: named as a partner celebrating Orange "
      "Corners Egypt graduates in Delta and Upper Egypt."),

    P("SODIC", "Industry, construction and real estate",
      "Real estate", "Greater Cairo and North Coast",
      "Education and community CSR, with a record of funding named "
      "education initiatives.",
      "Mid-to-large developer with an established habit of funding "
      "education programmes rather than only facilities.",
      "Brand association with quality education and community impact.",
      "A sponsored cohort series with their name on the programme.",
      "S", "Marketing and communications director",
      "Direct. Developer marketing budgets move faster than CSR budgets.",
      "Calendar year.",
      "C", "medium", "Education CSR is established; fit is a proposal."),

    P("Ezz Steel", "Industry, construction and real estate",
      "Steel", "National, with Suez and Alexandria plants",
      "Industrial community investment and technical training near plants.",
      "Plant-town programmes are fundable where national ones are not, and "
      "industrial towns are underserved by every incubator in Cairo.",
      "Local licence to operate and technical employability.",
      "A plant-town cohort series.",
      "XS", "Public affairs",
      "Direct, or through the Federation of Egyptian Industries.",
      "Calendar year.",
      "C", "low", "Reasoned prospect."),

    P("Lafarge Egypt (Holcim)", "Industry, construction and real estate",
      "Cement and building materials", "National",
      "Sustainability programmes including construction skills, "
      "entrepreneurship among small contractors, and community development "
      "around quarries and plants.",
      "Small contractor development is a recognised programme type in the "
      "cement sector globally, because better small contractors sell more "
      "cement. Commercial and social cases align.",
      "Small contractor capability, which converts directly into demand.",
      "A contractor enterprise programme, co-funded by sales and "
      "sustainability.",
      "S", "Sustainability manager, with the retail or small contractor "
      "sales lead",
      "Direct, pitching to sales and sustainability jointly.",
      "Calendar year.",
      "B", "medium",
      "The programme type is well established in the sector; the Egypt "
      "instance is unconfirmed."),

    P("GB Corp (Ghabbour Auto)", "Industry, construction and real estate",
      "Automotive and financing", "National",
      "Community programmes, driver and technician training, and consumer "
      "financing with a microfinance arm.",
      "Their financing arm lends to exactly the micro-businesses this "
      "trains, and their technician training is a ready cohort source.",
      "Better borrowers and a skilled technician pipeline.",
      "Business formation training attached to their financing and "
      "technician programmes.",
      "S", "CSR lead, with the microfinance business line",
      "Through the financing arm, where the commercial case lands.",
      "Calendar year.",
      "C", "low", "Reasoned prospect."),

    # ------------------------------------------------ Pharma and health
    P("Eva Pharma", "Pharma and healthcare", "Pharmaceuticals", "National",
      "A notably active corporate social programme covering health access, "
      "capacity building and youth development, with an Africa dimension.",
      "One of the more programme-minded Egyptian corporates, with a habit "
      "of building capability rather than donating equipment.",
      "Capability built, youth developed, and an Africa and Egypt story.",
      "A youth capability programme, with a health or life sciences "
      "venture track where it fits their sector.",
      "S", "Head of corporate social responsibility",
      "Direct. They are approachable and comparatively fast.",
      "Calendar year.",
      "B", "medium",
      "CSR activity is well established; the entrepreneurship fit is a "
      "proposal."),

    P("EIPICO", "Pharma and healthcare", "Pharmaceuticals", "National",
      "Community health and education programmes near its operations.",
      "Mid-sized, locally owned, with a short decision chain.",
      "Community goodwill and employee pride.",
      "A single-governorate cohort series.",
      "XS", "Corporate communications",
      "Direct.",
      "Calendar year.",
      "C", "low", "Reasoned prospect."),

    P("AstraZeneca Egypt", "Pharma and healthcare",
      "Pharmaceuticals, international", "National",
      "Young Health Programme and health system capacity work, delivered "
      "through NGO partners.",
      "Their youth programme is health-behaviour focused, so the fit is "
      "through youth leadership and employability rather than through "
      "venture creation.",
      "Youth reach numbers and partner credibility.",
      "An employability and enterprise module inside an existing youth "
      "health programme.",
      "S", "Corporate affairs or sustainability manager",
      "Through their existing NGO implementing partner.",
      "Calendar year.",
      "C", "low", "Adjacent rather than central. Low priority."),

    P("Novo Nordisk, Sanofi, Pfizer and the multinational pharma group",
      "Pharma and healthcare", "Pharmaceuticals, international", "National",
      "Access to health, patient support and community programmes, usually "
      "with strict compliance rules on what can be funded.",
      "Pharma compliance makes general CSR sponsorship difficult, so the "
      "realistic fit is narrow: a health-sector venture track, or employee "
      "volunteering.",
      "Compliant, auditable community investment with no promotional risk.",
      "A health-sector venture track, or mentoring by their staff.",
      "XS", "Corporate affairs, with compliance consulted early",
      "Through AmCham's healthcare committee rather than individually.",
      "Calendar year.",
      "C", "low",
      "Grouped deliberately: individually these are small, compliance-heavy "
      "prospects. Treat as one line of effort, not ten meetings."),

    # ------------------------------------- Corporate and family foundation
    P("Sawiris Foundation for Social Development",
      "Corporate and family foundation", "National donor foundation",
      "National",
      "One of the first and largest Egyptian donor foundations, endowed by "
      "the Sawiris family in 2001. Works on poverty, unemployment, health "
      "and education for marginalised Egyptians, including training for "
      "sectors the market underserves.",
      "Unemployment and training are core mandate, not adjacent. They fund "
      "Egyptian implementers directly, at meaningful size, and they are "
      "named as a partner by other funders, which means a relationship here "
      "opens others.",
      "Jobs and livelihoods created per pound spent, Egyptian "
      "implementation capacity, and rigorous measurement. They evaluate.",
      "A multi-governorate livelihoods programme with an evaluation "
      "component, positioned as training infrastructure rather than as one "
      "more training project.",
      "L", "Programme manager for economic empowerment or livelihoods, "
      "under the executive director",
      "They publish calls and accept concept notes. Drosos lists them as a "
      "partner, so a Drosos relationship can introduce.",
      "Call-driven. Watch their announcements rather than waiting for a "
      "cycle.",
      "A", "high",
      "Confirmed this session: established 2001 with a family endowment, "
      "among the first national donor foundations in Egypt, with poverty, "
      "unemployment and training programmes.",
      arabic="مؤسسة ساويرس للتنمية الاجتماعية"),

    P("Misr El Kheir Foundation", "Corporate and family foundation",
      "National NGO and donor", "National, all governorates",
      "One of the largest Egyptian NGOs, working across education, health, "
      "scientific research, social solidarity and integrated development, "
      "with a dedicated stream for livelihoods.",
      "Reach into every governorate, including the ones no Cairo programme "
      "touches. They both fund and implement, so the relationship can be "
      "either a sale or a partnership.",
      "Cost per beneficiary, geographic reach into underserved areas, and "
      "alignment with their integrated development model.",
      "Either a funded cohort programme in their target governorates, or "
      "certification of their own staff as facilitators, which is the "
      "higher-leverage version.",
      "L", "Head of the livelihoods or productive families sector, under "
      "the executive director",
      "Direct, through their sector heads. They are approachable and used "
      "to partnership proposals.",
      "Their planning follows the calendar year with Ramadan fundraising "
      "shaping the annual envelope.",
      "A", "high",
      "A very large and well-established Egyptian NGO with national "
      "coverage. Confirm which sector owns enterprise training before "
      "writing.",
      arabic="مؤسسة مصر الخير"),

    P("Drosos Foundation", "Corporate and family foundation",
      "Swiss private foundation", "Greater Cairo, Alexandria, Fayoum, "
      "Qena, Luxor, Aswan",
      "Working in Egypt since 2005. Its doroob programme supports socially "
      "driven youth business ideas, with up to 1,100 young people helped to "
      "develop early-stage ideas and a subset carried through to growth. "
      "Focus on graduates and students in agri-business, tourism and "
      "health, with gender and disability inclusion built in.",
      "This is the closest match in the entire file. Their programme "
      "structure, early-stage idea development converting to a smaller "
      "number of startups, is the same funnel this plan runs, and their "
      "governorates are the ones outside Cairo that matter.",
      "Youth business ideas developed, startups created, inclusion of women "
      "and people with disabilities, and quality of partner organisations.",
      "Delivery or methodology partner on doroob, or a successor "
      "programme, supplying the structured curriculum and facilitator "
      "certification.",
      "L", "Country representative for Egypt, with the programme manager "
      "for the relevant thematic line",
      "They work through Egyptian partner organisations. Partnering with an "
      "existing Drosos grantee is the realistic entry, with a direct "
      "approach to the country office in parallel.",
      "Multi-year project cycles. The Passion to Profit project with Kheir "
      "we Barka and the New Woman Association ran March 2023 to February "
      "2026, so successor planning is live now.",
      "A", "high",
      "Confirmed this session: Egypt since 2005, the governorate list, the "
      "doroob targets and the Passion to Profit dates all from Drosos "
      "published material."),

    P("Alfanar Venture Philanthropy", "Corporate and family foundation",
      "Venture philanthropy", "Egypt and the Levant",
      "The Arab world's first venture philanthropy organisation, investing "
      "in social enterprises with capital plus hands-on management support, "
      "with education and women's employment as recurring themes.",
      "Venture philanthropy buys organisational capability, not projects. "
      "They would evaluate StartPad as an investee as readily as a "
      "supplier, which is a different and potentially better conversation.",
      "Scalable social enterprises with a route to financial "
      "sustainability, and measurable social return.",
      "Either investee status, or delivery partner for the social "
      "enterprises already in their portfolio.",
      "M", "Egypt country director or portfolio manager",
      "Direct. They publish an investment process and accept approaches.",
      "Rolling, portfolio-driven.",
      "A", "medium",
      "Listed as a partner by Drosos in this session's results. Their Egypt "
      "portfolio and current focus should be checked on their own site."),

    P("Mansour Foundation for Development",
      "Corporate and family foundation", "Family foundation", "National",
      "Family philanthropy linked to the Mansour Group, covering education, "
      "health and community development.",
      "Family foundation money is patient and relationship-driven, and the "
      "group's commercial networks are a distribution channel in their own "
      "right.",
      "Family legacy, education outcomes, and national reach.",
      "A multi-year education and enterprise programme.",
      "M", "Executive director",
      "Through the Egyptian Businessmen's Association or a board-level "
      "introduction. Cold approaches to family foundations rarely work.",
      "Relationship-driven rather than cyclical.",
      "B", "low",
      "The foundation's existence and themes need verifying before "
      "approaching."),

    P("Abdul Latif Jameel Community Initiatives and comparable Gulf family "
      "foundations", "Corporate and family foundation",
      "Regional family foundation", "Regional, Egypt coverage varies",
      "Job creation as an explicit philanthropic mandate, including "
      "enterprise support and employment programmes across the Arab world.",
      "Job creation as a stated mandate is rare and valuable. If Egypt is "
      "in scope, their programme logic matches ours almost exactly.",
      "Jobs created per dollar, and programmes that can be replicated "
      "across markets.",
      "A job creation programme priced per job or per business created.",
      "L", "Programme director for the relevant country portfolio",
      "Through the Saudi side of the business, which this plan already "
      "builds a presence in.",
      "Multi-year.",
      "C", "low",
      "Egypt scope is unverified. Relevant mainly once the Saudi entity "
      "exists."),

    P("Tahya Misr Fund (Long Live Egypt)",
      "Corporate and family foundation",
      "Sovereign-linked development fund", "National",
      "A presidential development fund channelling corporate and individual "
      "donations into national development priorities, including youth, "
      "education and small enterprise.",
      "Where large Egyptian corporates put money when they want it to "
      "count politically. A component inside a Tahya Misr programme reaches "
      "corporate money without approaching twenty corporates.",
      "Visible delivery against national priorities, at scale, with "
      "governorate coverage.",
      "A named training component inside an existing fund programme.",
      "XL", "Fund secretariat, through a line ministry sponsor",
      "Not directly. Through a ministry or a major corporate donor who "
      "proposes the component.",
      "State fiscal year from July, and campaign-driven.",
      "B", "medium",
      "The fund's role is well established; whether an external training "
      "provider can be contracted into it is unverified and is the first "
      "question to ask."),

    P("Ford Foundation, Cairo office", "Corporate and family foundation",
      "International private foundation", "Egypt and the region",
      "Social justice, economic inclusion and civil society strengthening, "
      "through multi-year institutional grants.",
      "Institutional support rather than project funding, which is the "
      "rarest and most useful money there is. The framing must be "
      "inclusion and voice, not business growth.",
      "Structural change, inclusion of marginalised groups, and "
      "strengthened local institutions.",
      "An institutional or programme grant framed around economic "
      "inclusion of young people outside the formal economy.",
      "L", "Programme officer for the relevant portfolio",
      "By invitation and relationship. Grantee introductions matter more "
      "than applications.",
      "Multi-year cycles.",
      "C", "low",
      "Portfolio and Egypt presence should be verified; their priorities "
      "have shifted over time."),

    P("Egyptian corporate foundations, second tier",
      "Corporate and family foundation", "Corporate foundations", "National",
      "A long tail of registered corporate foundations attached to "
      "Egyptian groups in retail, construction, food and finance, most "
      "funding education, health and community work.",
      "Individually small, collectively the largest pool of unattached CSR "
      "money in the country, and almost none of it is competed for with a "
      "structured programme offer.",
      "A credible programme with a report at the end, and a logo on it.",
      "A standard, repeatable single-cohort sponsorship package that can be "
      "sold many times without redesign.",
      "XS", "Foundation manager or corporate communications",
      "Through the Ministry of Social Solidarity's registry of foundations, "
      "which is public, and through the business associations.",
      "Calendar year.",
      "B", "medium",
      "This is a category row, not an organisation. Its purpose is to stop "
      "the pipeline being built only from famous names."),

    # ----------------------- Bilateral donor and development agency
    P("GIZ Egypt", "Bilateral donor and development agency",
      "German development cooperation", "National",
      "Employment promotion, technical and vocational education, private "
      "sector development and digital innovation, commissioned by the "
      "German federal ministry and implemented with Egyptian ministries. "
      "Partner of the Digital Egypt Innovation Hubs with Flat6Labs, and "
      "runs an employment promotion programme with the Ministry of "
      "Education that includes helping young people start businesses.",
      "The single most important organisation in this file. GIZ does not "
      "deliver training itself, it contracts providers, and its programmes "
      "already contain the exact activity this business sells. Becoming a "
      "known provider to GIZ Egypt changes the company's risk profile.",
      "Delivery against a commissioned result, documented to German public "
      "procurement standards, with gender and inclusion disaggregation.",
      "Registration as a service provider, then bids on training lots "
      "inside employment and private sector development programmes.",
      "L", "Programme manager (Auftragsverantwortlicher) of the relevant "
      "component, with the procurement unit running the process",
      "Two routes, run both. Formal: GIZ publishes tenders and maintains a "
      "supplier process; register and watch. Informal: the programme team "
      "shapes the terms of reference before a tender exists, and they meet "
      "providers at ecosystem events.",
      "German commissions run multi-year with annual work planning, "
      "typically set between September and December for the following "
      "year. Being known by October matters more than bidding well in "
      "March.",
      "A", "high",
      "Confirmed this session: GIZ partnership with Digital Egypt "
      "Innovation Hubs and Flat6Labs, and the employment promotion "
      "programme in Egypt including support for young people setting up "
      "businesses. Current programme list must be checked with the country "
      "office."),

    P("Orange Corners Egypt (Netherlands Enterprise Agency)",
      "Bilateral donor and development agency",
      "Dutch government entrepreneurship programme",
      "Luxor, Assiut, Alexandria, Menoufia, Dakahlia, Kafr El-Sheikh, "
      "Beheira and Cairo",
      "A Netherlands government programme delivering incubation to young "
      "entrepreneurs through local hubs and private partners, with "
      "cohort-based training and a strong gender record.",
      "A running, funded, governorate-level entrepreneurship programme "
      "with local delivery partners. Either we supply curriculum and "
      "facilitators into it, or we become a hub.",
      "Cohort completion, women-led ventures, and governorate coverage "
      "outside Cairo.",
      "Curriculum and facilitator supply to existing hubs, or hub status "
      "in a governorate they have not yet covered.",
      "M", "Programme manager at the Netherlands embassy in Cairo, with "
      "the local implementing partner for delivery",
      "Through an existing hub or the implementing partner, and through "
      "the Netherlands embassy's economic section.",
      "Cohort cycles run through the year; expansion decisions are annual.",
      "A", "high",
      "Confirmed this session: expansion into seven governorates in 2025, "
      "and a Delta cohort graduating 100 startups of which 52 were "
      "women-led, with Madinet Masr among the private partners."),

    P("European Union Delegation to Egypt",
      "Bilateral donor and development agency",
      "EU external action", "National",
      "Large multi-year programmes on job creation, TVET, migration and "
      "private sector development, contracted through calls for proposals "
      "and service contracts.",
      "The largest single pool of grant money for employment work in "
      "Egypt. Also the most procedurally demanding: PRAG rules, consortium "
      "requirements and co-financing.",
      "Policy-aligned results at national scale, strict financial "
      "compliance, and consortium partners with audited track records.",
      "Consortium membership as the training and technology partner, never "
      "as lead applicant in the first cycle.",
      "XL", "Programme manager in the cooperation section, with the "
      "contracting authority running procurement",
      "Monitor the EU funding and tenders portal, and position with the "
      "European implementing agencies who will lead the consortia: GIZ, "
      "Expertise France, AICS, Enabel and the member state agencies.",
      "Calls are published with long lead times. Annual action plans are "
      "set a year ahead, so influence happens early.",
      "B", "medium",
      "The instrument type is certain; the current Egypt pipeline must be "
      "read from the portal at the time of bidding. Do not bid as lead "
      "without an audited track record."),

    P("British Council Egypt", "Bilateral donor and development agency",
      "UK cultural relations and education", "National",
      "Skills, higher education partnerships, creative economy and social "
      "enterprise programmes, often with UK institutional partners.",
      "Named in this plan's partner list already. Their social enterprise "
      "and creative economy work is directly adjacent, and they contract "
      "local delivery.",
      "UK and Egypt institutional links, skills outcomes, and creative or "
      "social enterprise development.",
      "Delivery partner on a skills or social enterprise programme, "
      "preferably with a UK university partner attached.",
      "M", "Programme manager for skills or society, in the Cairo office",
      "Direct to the Cairo office programme teams, and through UK "
      "university partners who are already working with them.",
      "UK financial year from April, so proposals land best between "
      "November and February.",
      "A", "medium",
      "Presence and programme areas are well established; the current "
      "Egypt programme list needs confirming."),

    P("Expertise France and Agence Francaise de Developpement (AFD)",
      "Bilateral donor and development agency",
      "French development cooperation", "National",
      "Vocational training, employment, entrepreneurship and private sector "
      "development, frequently in partnership with Egyptian ministries and "
      "with EU co-financing.",
      "French cooperation funds TVET and employment heavily in Egypt, and "
      "Expertise France implements rather than only funds, which means "
      "sub-contracted delivery.",
      "Employment and TVET results aligned with Egyptian state priorities, "
      "French institutional visibility.",
      "Sub-contracted delivery of entrepreneurship modules inside a TVET "
      "or employment project.",
      "L", "Project director for the relevant programme",
      "Through the French embassy's economic service and the Expertise "
      "France Cairo project offices.",
      "Project cycles, with annual planning.",
      "B", "medium",
      "Sector presence is established; specific projects need checking."),

    P("Italian Agency for Development Cooperation (AICS) Cairo",
      "Bilateral donor and development agency",
      "Italian development cooperation", "National, with Upper Egypt focus",
      "Employment, vocational training, migration-related economic "
      "opportunity and support to Egyptian SMEs, including credit lines.",
      "Italian cooperation in Egypt is substantial and has an explicit "
      "focus on economic opportunity as an alternative to irregular "
      "migration, which funds youth enterprise work generously.",
      "Economic alternatives to migration in origin governorates, and "
      "Italy and Egypt business links.",
      "A youth enterprise component in a migration-and-development "
      "programme, in the origin governorates they target.",
      "L", "Programme officer at the AICS Cairo office",
      "Direct to the Cairo office, and through Italian NGOs implementing "
      "their programmes.",
      "Annual planning with multi-year projects.",
      "B", "medium",
      "Thematic focus is well established; the current call list needs "
      "checking."),

    P("Enabel, SIDA, Danida, Swiss SDC and the smaller bilateral agencies",
      "Bilateral donor and development agency",
      "Bilateral development cooperation", "National",
      "Employment, skills, governance and private sector programmes, each "
      "with a modest Egypt portfolio but a lower barrier to entry than the "
      "largest donors.",
      "Smaller portfolios mean smaller cheques but far shorter queues, and "
      "a first donor contract from any of them makes the next bid "
      "credible.",
      "Results inside a narrow thematic mandate, and low fiduciary risk.",
      "A single-project delivery contract, treated as a reference "
      "customer rather than as revenue.",
      "M", "Programme officer at the relevant embassy or agency office",
      "Through the embassies' development sections. Several publish calls.",
      "Varies by agency; most plan annually.",
      "B", "low",
      "Grouped deliberately. Verify which of these currently fund "
      "employment work in Egypt before allocating time."),

    P("KfW Development Bank", "Bilateral donor and development agency",
      "German development finance", "National",
      "Financial cooperation, including credit lines to Egyptian banks for "
      "SME lending, alongside TVET infrastructure.",
      "KfW funds the financial side rather than the training side, so the "
      "realistic route is as the technical assistance attached to a credit "
      "line, usually contracted through GIZ or a consultant.",
      "Portfolio quality on SME credit lines, and TVET capacity.",
      "Technical assistance delivery attached to an SME credit line.",
      "L", "Project manager in the Cairo office",
      "Through GIZ or the implementing consultant rather than directly.",
      "Multi-year financial cooperation agreements.",
      "C", "medium",
      "Instrument structure is standard; the Egypt pipeline is "
      "unconfirmed."),

    P("European Bank for Reconstruction and Development (EBRD)",
      "Bilateral donor and development agency",
      "Development finance institution", "National",
      "Advice for Small Businesses, Women in Business, and Youth in "
      "Business programmes, which pay for advisory services to SMEs.",
      "Their Advice for Small Businesses programme literally pays for "
      "consultants and trainers to work with Egyptian SMEs. There is a "
      "registration process for local service providers.",
      "SME growth measured in turnover, employment and productivity after "
      "the advisory engagement.",
      "Registration as an approved local consultant or training provider, "
      "then assignments under the programme.",
      "M", "Advice for Small Businesses country team in Cairo",
      "They maintain a consultant roster. Apply to it. This is one of the "
      "few donor routes with a published, open application.",
      "Rolling registration; assignments are continuous.",
      "A", "medium",
      "The programme structure is long-established across EBRD countries "
      "including Egypt. Confirm the current Egypt roster process."),

    P("World Bank and International Finance Corporation",
      "Bilateral donor and development agency",
      "Multilateral development finance", "National",
      "Lending to the Egyptian state for employment, education and SME "
      "development, and IFC advisory to private firms.",
      "Money reaches providers through state implementing units procuring "
      "under World Bank rules, not through the Bank itself. The "
      "relationship that matters is with the ministry running the project.",
      "Results against loan-linked indicators, and procurement that "
      "survives audit.",
      "A bid under a state project's procurement, with World Bank "
      "procurement rules applying.",
      "XL", "Project implementation unit at the borrowing ministry",
      "Through the implementing ministry, and by monitoring the Bank's "
      "procurement notices for Egypt.",
      "Project cycles of five years or more, with procurement plans "
      "published.",
      "C", "medium",
      "Mechanism is certain; which current Egypt projects include training "
      "procurement needs checking."),

    P("Islamic Development Bank and Arab funds",
      "Bilateral donor and development agency",
      "Multilateral and Arab development finance", "National",
      "Vocational training, youth employment and SME finance across member "
      "countries, often with a waqf or Islamic finance structure.",
      "Arab fund money is large, state-channelled and less contested by "
      "international NGOs than European money.",
      "Member country development priorities and Islamic finance "
      "compatibility.",
      "A component inside a state-executed project.",
      "L", "Country programme officer, through the Ministry of "
      "International Cooperation",
      "Through the Ministry of International Cooperation, which "
      "coordinates all of it.",
      "Multi-year.",
      "C", "low",
      "Access is through the state. Verify current Egypt portfolio."),

    # --------------------------------------- UN agency and multilateral
    P("International Labour Organization (ILO) Egypt",
      "UN agency and multilateral", "UN agency", "National",
      "Decent work, youth employment and enterprise development. Owns Start "
      "and Improve Your Business (SIYB), the most widely used enterprise "
      "training methodology in the world, and has run youth employment "
      "projects in Egypt under the FORSA programme.",
      "Two relationships, not one. As a buyer they contract delivery; as a "
      "methodology owner they certify master trainers in SIYB, and SIYB "
      "certification would give this company's facilitator pool an "
      "internationally recognised credential at low cost.",
      "Decent work outcomes, methodology fidelity, and national "
      "institutional capacity rather than project delivery.",
      "SIYB master trainer certification for the facilitator pool, plus "
      "delivery partner status on youth employment projects.",
      "M", "Chief technical adviser of the relevant project, and the "
      "enterprise development specialist in the Cairo office",
      "Direct to the Cairo office. The SIYB certification route is open "
      "and published, and is the cheapest credibility available in this "
      "file.",
      "Project cycles. The Egypt Youth Employment project under FORSA ran "
      "to 2024, so successor programming is the thing to ask about.",
      "A", "high",
      "Confirmed this session: SIYB is an ILO methodology, and an ILO "
      "Egypt Youth Employment project under FORSA ran 2020 to 2024. "
      "Confirm the current project portfolio."),

    P("United Nations Development Programme (UNDP) Egypt",
      "UN agency and multilateral", "UN agency", "National",
      "Works with the Ministry of Planning and Economic Development on "
      "SDG localisation, youth employment and innovation, including the "
      "ICT Trust Fund's youth employment work with the ICT ministry.",
      "UNDP sits beside the ministries that own the national "
      "entrepreneurship agenda, and it contracts implementation. It is "
      "also the most common channel for governorate-level programmes.",
      "SDG-aligned results, government ownership, and governorate reach.",
      "A responsible party agreement or service contract for delivery "
      "inside a youth employment project.",
      "L", "Programme analyst for inclusive growth or youth, in the Cairo "
      "country office",
      "UNDP procurement is published on its own portal and on UNGM. "
      "Register on UNGM first; it is a prerequisite for most UN work.",
      "Country programme documents run multi-year with annual work plans "
      "agreed early in the year.",
      "A", "high",
      "Confirmed this session: GIZ and UNDP both appear as partners of the "
      "ICT Trust Fund youth employment programme with the ICT ministry. "
      "Current projects need confirming."),

    P("UNICEF Egypt", "UN agency and multilateral", "UN agency",
      "National, with Upper Egypt focus",
      "Adolescent and youth development, skills for employability, and the "
      "Generation Unlimited partnership, plus child protection standards "
      "that any school-facing work must meet.",
      "The adolescent skills agenda covers under-18s, which is the schools "
      "engine. They also set the safeguarding bar, so working with them "
      "forces a compliance posture worth having anyway.",
      "Adolescent skills outcomes, equity of reach, and absolute "
      "compliance with child safeguarding.",
      "A skills and enterprise component for adolescents, with full "
      "safeguarding documentation.",
      "L", "Adolescent development and participation specialist",
      "Through UNGM and the Cairo office. Expect safeguarding due "
      "diligence before anything else.",
      "Country programme cycles with annual work plans.",
      "B", "high",
      "Named as a partner in this plan's existing list. Child safeguarding "
      "policy is a hard precondition, not a nice to have."),

    P("UN Women Egypt", "UN agency and multilateral", "UN agency",
      "National",
      "Women's economic empowerment, including enterprise development and "
      "access to finance for women.",
      "A women-only cohort series is a product this plan can run without "
      "modification, and women's economic empowerment is the best funded "
      "single theme in Egyptian development work.",
      "Women's economic participation, measured and disaggregated, with "
      "attention to unpaid care and mobility constraints.",
      "A women's enterprise programme with childcare and mobility costs "
      "budgeted explicitly, which is what distinguishes a serious proposal "
      "from a generic one.",
      "M", "Women's economic empowerment programme specialist",
      "Through UNGM and the Cairo office.",
      "Annual work plans.",
      "A", "medium",
      "Thematic fit is certain; the current Egypt project list is "
      "unconfirmed."),

    P("United Nations Industrial Development Organization (UNIDO) Egypt",
      "UN agency and multilateral", "UN agency", "National",
      "Entrepreneurship curriculum in secondary and technical education, "
      "agro-industry value chains, and SME upgrading.",
      "UNIDO has institutionalised entrepreneurship curriculum inside "
      "education systems in several countries. That is the same ambition "
      "as the schools engine, and they need delivery capacity.",
      "Institutionalisation inside the education system rather than "
      "standalone training, and industrial value chain outcomes.",
      "Curriculum and facilitator delivery inside an entrepreneurship "
      "curriculum programme.",
      "L", "Project manager for the entrepreneurship or agro-industry "
      "programme",
      "Through UNGM and the Cairo office.",
      "Project cycles.",
      "B", "medium",
      "The programme type is established at UNIDO globally; the Egypt "
      "instance needs confirming."),

    P("International Organization for Migration (IOM) Egypt",
      "UN agency and multilateral", "UN agency",
      "National, with migration-origin governorates",
      "Economic opportunity as an alternative to irregular migration, "
      "reintegration support for returning migrants, and livelihoods for "
      "migrants and host communities.",
      "Migration-linked money is large, politically backed and concentrated "
      "in specific governorates. Enterprise training is one of its standard "
      "instruments.",
      "Reduced migration pressure, measurable livelihoods in origin "
      "communities, and support reaching both migrants and hosts.",
      "An enterprise training component for returnees and youth in "
      "origin governorates.",
      "L", "Programme manager for labour mobility and human development",
      "Through UNGM and the Cairo office.",
      "Project cycles tied to European funding.",
      "B", "medium",
      "Instrument and geography are well established; current projects "
      "unconfirmed."),

    P("Food and Agriculture Organization (FAO) Egypt",
      "UN agency and multilateral", "UN agency",
      "Rural Egypt, Upper Egypt and the Delta",
      "Rural livelihoods, agribusiness development and farmer field "
      "schools.",
      "Agribusiness is the most teachable venture type in rural Egypt and "
      "FAO funds the training around it.",
      "Rural livelihoods and food system outcomes.",
      "An agribusiness enterprise track inside a rural livelihoods "
      "project.",
      "M", "Programme officer for rural development",
      "Through UNGM and the Cairo office.",
      "Project cycles.",
      "C", "medium", "Thematic fit is good; Egypt pipeline unconfirmed."),

    # --------------------------- International NGO and implementer
    P("Plan International Egypt", "International NGO and implementer",
      "International NGO", "Upper Egypt and the Delta",
      "Youth economic empowerment, girls' rights, and skills for "
      "employment, usually funded by European donors and implemented with "
      "Egyptian partners.",
      "They win donor money and need Egyptian delivery capacity. Being "
      "their training partner is faster than winning donor money directly, "
      "and it builds the audited track record that donors later require.",
      "Girls' and young women's economic empowerment, delivered to donor "
      "compliance standards.",
      "Sub-contracted delivery inside their youth economic empowerment "
      "projects.",
      "M", "Youth economic empowerment programme manager",
      "Direct. International NGOs are more accessible than their donors "
      "and answer email.",
      "Project-driven, with partner selection at proposal stage, so being "
      "known before a call closes is what matters.",
      "A", "medium",
      "Presence and thematic focus are well established in Egypt; current "
      "projects unconfirmed."),

    P("CARE Egypt", "International NGO and implementer",
      "International NGO", "Upper Egypt and the Delta",
      "Women's economic empowerment, village savings and loan "
      "associations, and entrepreneurship for low-income women.",
      "Their savings group model creates hundreds of thousands of "
      "micro-entrepreneurs with no business training attached. That gap is "
      "the product.",
      "Savings group graduation into viable micro-businesses, and women's "
      "economic resilience.",
      "A business formation curriculum layered on their savings groups.",
      "M", "Programme director for economic empowerment",
      "Direct.",
      "Project-driven.",
      "A", "medium",
      "Model and presence are well established; current Egypt portfolio "
      "unconfirmed."),

    P("Save the Children Egypt", "International NGO and implementer",
      "International NGO", "National",
      "Adolescent skills, child protection and youth employability.",
      "Adolescent employability work needs under-18-appropriate content, "
      "which the schools engine already produces.",
      "Adolescent outcomes with child-safe delivery.",
      "Delivery of an adolescent enterprise track.",
      "S", "Programme manager for education or youth",
      "Direct, with safeguarding documentation ready.",
      "Project-driven.",
      "B", "low", "Reasoned prospect; Egypt portfolio unconfirmed."),

    P("Catholic Relief Services, Caritas Egypt and the faith-based "
      "implementers", "International NGO and implementer",
      "Faith-based international NGO", "National, strong in Upper Egypt",
      "Livelihoods, vocational training and migrant support, with deep "
      "community networks in Upper Egypt.",
      "Community reach in exactly the governorates that are hardest to "
      "serve commercially, and a long record of vocational training.",
      "Livelihoods created in the communities they serve.",
      "Facilitator certification for their own staff, which scales "
      "without us staffing it.",
      "S", "Livelihoods programme manager",
      "Direct. These organisations are approachable.",
      "Project-driven.",
      "B", "medium",
      "Presence in Upper Egypt is well established; specific programmes "
      "unconfirmed."),

    P("Mercy Corps, DRC, Terre des Hommes and the European implementers",
      "International NGO and implementer", "International NGO", "National",
      "Livelihoods and economic inclusion projects funded by European "
      "donors, often covering refugees and host communities.",
      "They need local partners with a method and a registration. "
      "Refugee-inclusive cohorts also unlock funding that is closed to "
      "purely national programmes.",
      "Inclusion of refugees and host communities, and donor compliance.",
      "Delivery sub-contracts, with refugee-inclusive cohort design.",
      "M", "Programme manager for economic recovery or livelihoods",
      "Direct, and through the refugee response coordination groups.",
      "Project-driven.",
      "B", "low",
      "Grouped deliberately. Verify which currently operate in Egypt "
      "before allocating time."),

    P("Ashoka Arab World", "International NGO and implementer",
      "Social entrepreneurship network", "Egypt and the region",
      "Identifies and supports social entrepreneurs, and runs youth social "
      "innovation programmes.",
      "A network rather than a funder. Its value is the introductions, the "
      "fellows who become facilitators, and the credibility of "
      "association.",
      "Social impact at systems level, and young changemakers.",
      "A partnership on youth social innovation, and fellows as mentors.",
      "XS", "Country or regional director",
      "Direct. The network is open to partnership conversations.",
      "Rolling.",
      "B", "medium",
      "Long-established in Cairo; current programme set unconfirmed."),

    # ------------------------ Egyptian NGO and social enterprise
    P("INJAZ Egypt", "Egyptian NGO and social enterprise",
      "Youth education NGO, JA Worldwide member", "National",
      "The Company Program and youth entrepreneurship education, delivered "
      "in schools and universities by trained corporate volunteers, funded "
      "by corporate sponsors and part of the INJAZ Al-Arab and JA "
      "Worldwide networks.",
      "The closest thing in Egypt to a direct peer, and therefore either "
      "the best partner or the main competitor. They have the school "
      "access and the corporate funders; they do not have a platform, an "
      "AI review layer or a certified paid facilitator pool. Partnership "
      "is the stronger play.",
      "Volume of students reached, corporate sponsor satisfaction, and "
      "quality consistency across volunteers, which is their hardest "
      "problem and our product's answer.",
      "Platform and AI review under their programme, with their volunteers "
      "certified on the method.",
      "M", "Executive director, with the programmes director as the "
      "operational owner",
      "Direct. Also present at every ecosystem event, which is the easier "
      "first contact.",
      "Academic year, so approach between May and August.",
      "A", "high",
      "Named in this plan's existing partner list and confirmed in this "
      "session's search results as running the Company Program and youth "
      "entrepreneurship work in Egypt.",
      arabic="إنجاز مصر"),

    P("Enactus Egypt", "Egyptian NGO and social enterprise",
      "University student network", "National, 40+ universities",
      "University-based social entrepreneurship teams competing nationally "
      "and internationally, sponsored by Orange Egypt for twenty "
      "consecutive years and with National Bank of Egypt participation in "
      "the national finals.",
      "The single largest organised body of entrepreneurial university "
      "students in Egypt, with the corporate sponsors already attached. "
      "Reaching Enactus reaches the students, the universities and the "
      "sponsors in one relationship.",
      "Better-prepared teams, higher placement at the world cup, and "
      "sponsor retention.",
      "Mission-based preparation for competing teams, and facilitator "
      "certification for faculty advisers.",
      "S", "National director or country manager, with faculty advisers "
      "as the delivery counterpart",
      "Direct to the national office, and in parallel through faculty "
      "advisers at individual universities.",
      "Academic year, with the national competition driving the calendar.",
      "A", "high",
      "Confirmed this session: twenty years of Orange sponsorship, NBE "
      "participation in the 2025/2026 local finals, and the winning team "
      "representing Egypt at the world cup.",
      arabic="إناكتس مصر"),

    P("Nahdet El Mahrousa", "Egyptian NGO and social enterprise",
      "Social enterprise incubator", "National",
      "Describes itself as the first incubator for early-stage social "
      "enterprises in Egypt and the region. Incubation, seed funding and "
      "capacity building, with a network of more than 600 startups and 150 "
      "mentors, and a record on the Egypt@Work initiative that trained "
      "over 12,600 young people with 78 per cent going into work or "
      "self-employment.",
      "A proven Egyptian implementer with donor relationships and a mentor "
      "network. Their 78 per cent outcome figure is the kind of evidence "
      "donors trust, and a partnership borrows that credibility.",
      "Pipeline quality into incubation, mentor leverage, and donor "
      "reporting.",
      "Pre-incubation delivery at volume, feeding their incubation funnel, "
      "with their mentors certified as facilitators.",
      "M", "Executive director, with the incubation programme manager",
      "Direct. They are an established partnership organisation.",
      "Programme cycles; donor-driven.",
      "A", "high",
      "Confirmed this session: self-described first social enterprise "
      "incubator in Egypt and the Middle East, 600+ startups, 150+ "
      "mentors, and the Egypt@Work results with the International Youth "
      "Foundation.",
      arabic="نهضة المحروسة"),

    P("Life Makers Foundation (Sonaa Al Hayah)",
      "Egyptian NGO and social enterprise",
      "National youth NGO", "National, all governorates",
      "One of the largest youth volunteer organisations in Egypt, with "
      "branches across the governorates, running development, employment "
      "and community programmes through young volunteers.",
      "Volunteer reach into every governorate at a cost no commercial "
      "operation can match. Certifying their branch coordinators as "
      "facilitators is the cheapest national delivery network available.",
      "Volunteer development, programme quality, and funding for branch "
      "activity.",
      "Facilitator certification for branch coordinators, with a "
      "donor-funded programme behind it.",
      "S", "Executive director, with governorate branch coordinators as "
      "the delivery counterpart",
      "Direct to the national office. Branch coordinators can also "
      "initiate upward.",
      "Programme and funding driven.",
      "A", "medium",
      "A very large and long-established Egyptian youth organisation. The "
      "current programme portfolio needs confirming; this session's search "
      "returned nothing on it, which is a gap in this file, not evidence "
      "of absence.",
      arabic="مؤسسة صناع الحياة"),

    P("Alashanek ya Balady Association for Sustainable Development (AYB-SD)",
      "Egyptian NGO and social enterprise",
      "Youth and livelihoods NGO", "Greater Cairo and several governorates",
      "Started as a student initiative and became a development NGO "
      "focused on employability, vocational training and small enterprise "
      "for low-income young people.",
      "Their entire model is employability and enterprise for the "
      "population this initiative targets, and they implement with donor "
      "funding.",
      "Job placement and income improvement for low-income youth.",
      "Curriculum and facilitator supply to their enterprise track.",
      "S", "Programme director",
      "Direct.",
      "Project-driven.",
      "B", "medium",
      "Organisation and focus are well established; this session's search "
      "returned nothing current, so verify before approaching."),

    P("Etijah, Youth and Development Consultancy Institute",
      "Egyptian NGO and social enterprise",
      "Youth development NGO and consultancy", "National",
      "Youth participation, capacity building for youth organisations, and "
      "donor-funded youth programming.",
      "They build the capacity of other youth organisations, which makes "
      "them a multiplier: one relationship reaches many small NGOs.",
      "Capacity built across the youth sector, and donor results.",
      "Facilitator certification delivered through their capacity "
      "building network.",
      "S", "Executive director",
      "Direct.",
      "Project-driven.",
      "B", "low", "Verify current activity before approaching."),

    P("Educate Me Foundation", "Egyptian NGO and social enterprise",
      "Education NGO", "Greater Cairo",
      "Learner-centred education, teacher development and community "
      "schools, with a strong reputation for pedagogy.",
      "Pedagogical credibility rather than scale. Useful as a quality "
      "partner and as a source of facilitators who can actually teach.",
      "Learning quality and teacher capability.",
      "A pedagogy partnership and a facilitator pipeline.",
      "XS", "Executive director",
      "Direct.",
      "Rolling.",
      "C", "medium", "Reputation is established; fit is modest."),

    P("Teach For Egypt", "Egyptian NGO and social enterprise",
      "Education NGO, Teach For All network", "Several governorates",
      "Places graduate fellows as teachers in underserved schools for two "
      "years, with leadership development attached.",
      "Their fellows and alumni are a ready-made facilitator pool: young, "
      "trained in front of a classroom, and already placed in the schools "
      "the schools engine wants to reach.",
      "Fellow development, alumni impact, and school outcomes.",
      "Facilitator certification for fellows and alumni.",
      "XS", "Executive director or alumni director",
      "Direct.",
      "Fellowship cohort cycles, annual.",
      "B", "medium",
      "Network membership is established; Egypt scale needs confirming."),

    P("Ahead of the Curve", "Egyptian NGO and social enterprise",
      "Sustainability consultancy and social enterprise", "National",
      "Corporate sustainability advisory, CSR strategy and sustainability "
      "reporting for Egyptian corporates.",
      "Not a funder. A gatekeeper: they write the CSR strategies this "
      "file's corporate prospects then execute. Being in their "
      "recommendation set is worth more than most direct approaches.",
      "Credible programmes they can recommend to clients without risk to "
      "their own reputation.",
      "Preferred implementation partner status for the youth and "
      "employability themes in their client strategies.",
      "XS", "Managing director or practice lead",
      "Direct, as a partnership rather than as a sales call.",
      "Rolling.",
      "B", "low",
      "Positioning as a CSR advisory firm is known; current client base "
      "unverified."),

    P("CID Consulting", "Egyptian NGO and social enterprise",
      "Development consultancy", "National",
      "Development consultancy and CSR advisory, designing and evaluating "
      "programmes for corporates and donors.",
      "Same gatekeeper logic. They also sub-contract delivery on projects "
      "they design.",
      "Programmes that deliver what their design promised.",
      "Delivery sub-contracts and a place in their partner set.",
      "XS", "Partner or programme director",
      "Direct.",
      "Rolling.",
      "C", "low", "Verify current activity."),

    P("Misr El Kheir, Resala, Dar Al Orman, Orman and the mass charitable "
      "associations", "Egyptian NGO and social enterprise",
      "Large national charity", "National, all governorates",
      "Mass-membership Egyptian charities with enormous volunteer bases, "
      "zakat-funded, running productive families and income-generation "
      "programmes alongside direct relief.",
      "Their productive families programmes hand out sewing machines and "
      "livestock with no business training attached. Reach is unmatched; "
      "method is absent. That is precisely the gap this company fills.",
      "Beneficiaries moved off dependence and into income, and zakat "
      "deployed credibly.",
      "A business formation curriculum attached to productive families "
      "grants, with their own staff certified to deliver it.",
      "M", "Head of productive families or income generation",
      "Direct. Ramadan is their peak funding season and the worst delivery "
      "season; plan around it.",
      "Zakat and Ramadan driven, with programme planning before it.",
      "A", "medium",
      "Productive families programming is standard across these "
      "organisations. Which of them is currently strongest on income "
      "generation needs checking organisation by organisation."),

    # ------------------------------- Youth and student organisation
    P("AIESEC in Egypt", "Youth and student organisation",
      "International student organisation", "National, most universities",
      "Youth leadership development and international exchange, run "
      "entirely by university students across local committees.",
      "A student-run national network with committees on most campuses. "
      "They are a distribution channel and an ambassador pipeline, not a "
      "funder, and they cost almost nothing to activate.",
      "Member development, partner corporates, and leadership experiences "
      "for their members.",
      "Campus chapters as ambassador hubs, with their leadership trained "
      "as facilitators.",
      "XS", "National president or vice president for partnerships, with "
      "local committee presidents",
      "Direct to the national office, and through local committee "
      "presidents, who turn over annually and respond fast.",
      "Their leadership year turns over in the summer, so the useful "
      "approach window is July to September.",
      "A", "medium",
      "Presence in Egypt is long-established. Current committee list "
      "should be taken from their own site."),

    P("Junior Chamber International (JCI) Egypt",
      "Youth and student organisation", "Young professional network",
      "National, several chapters",
      "Young leaders and entrepreneurs network, running training, "
      "competitions and community projects.",
      "Membership is young professionals who are already starting "
      "businesses, which makes them both a market and a mentor pool.",
      "Member value, visible community projects, and national "
      "representation.",
      "Co-run competitions and mentor supply.",
      "XS", "National president or chapter presidents",
      "Direct.",
      "Annual leadership turnover.",
      "B", "low", "Verify current Egyptian chapter activity."),

    P("Hult Prize on-campus programme", "Youth and student organisation",
      "Global student competition", "Egypt and KSA campuses",
      "A student social venture competition run on campuses worldwide, "
      "with campus directors recruited from the student body.",
      "Already in this plan's named target list. Campus rounds need "
      "preparation content and judging infrastructure, which is the "
      "competitions engine exactly.",
      "Campus participation numbers and quality of ventures advancing.",
      "Preparation missions and a judging pack for campus rounds.",
      "XS", "Campus directors, with the regional team above them",
      "Through campus directors directly; they are students and are "
      "reachable.",
      "Academic year, with campus rounds in the autumn and winter.",
      "B", "high",
      "Named in this plan's existing target list."),

    P("Startup Teen (iSchool)", "Youth and student organisation",
      "School-age entrepreneurship competition", "Egypt",
      "A school-age entrepreneurship competition run under the patronage "
      "of the Ministry of Communications and Information Technology.",
      "Already in this plan's named target list. School-age competition "
      "with ministry cover is the schools engine's shortest path to "
      "credibility.",
      "Participation at school level, and ministry visibility.",
      "Preparation content for competing school teams.",
      "XS", "Programme lead at iSchool",
      "Direct, and through the ICT ministry patronage relationship.",
      "Academic year.",
      "B", "high", "Named in this plan's existing target list."),

    P("Rotaract and Rotary Egypt", "Youth and student organisation",
      "Service club network", "National, many clubs",
      "Youth service clubs running community projects, with Rotary "
      "international grant funding behind them.",
      "Rotary global grants can fund vocational training projects, and "
      "Rotaract clubs provide volunteers and local credibility in "
      "governorates.",
      "Service projects with measurable community benefit, and "
      "international grant eligibility.",
      "A vocational training global grant with a local club as host.",
      "S", "District governor and club presidents",
      "Through club presidents, who can propose grants upward.",
      "Rotary year begins in July; grant cycles follow it.",
      "B", "low",
      "The global grant mechanism is real and well documented; Egyptian "
      "club appetite is unverified."),

    P("IEEE, ACM and the engineering student branches",
      "Youth and student organisation", "Technical student societies",
      "National, engineering faculties",
      "Technical student branches running competitions, workshops and "
      "hackathons on engineering campuses.",
      "The technically strongest students in the country, with no business "
      "formation content anywhere in their calendar.",
      "Member activity, technical credibility and employability.",
      "An entrepreneurship track inside their event calendar.",
      "XS", "Student branch chairs, with faculty advisers",
      "Direct to branch chairs.",
      "Academic year.",
      "C", "medium",
      "These branches exist on most Egyptian engineering faculties; "
      "specific branches to be listed from their own directories."),

    P("Egyptian Scouts, youth centres and the Ministry of Youth network",
      "Youth and student organisation",
      "State youth infrastructure", "National, every governorate",
      "Thousands of state youth centres under the Ministry of Youth and "
      "Sports, reaching young people outside the university system "
      "entirely.",
      "The only infrastructure in Egypt that reaches non-university youth "
      "at national scale. For a one-million ambition, no purely "
      "university-based plan can arrive; this is how the number is "
      "reached.",
      "Youth centre activity, national coverage, and alignment with the "
      "ministry's own programmes.",
      "A train-the-trainer programme for youth centre coordinators, "
      "funded by a donor or by the ministry.",
      "L", "Ministry of Youth and Sports central administration for youth "
      "programmes, with governorate directorates",
      "Through the ministry centrally, with a donor paying. Governorate "
      "directorates cannot commit nationally but can pilot.",
      "State fiscal year from July.",
      "A", "medium",
      "The youth centre network's existence and scale are certain; the "
      "contracting route for an external provider is the thing to "
      "establish early."),

    # -------------------- Government initiative and public agency
    P("Rowad 2030", "Government initiative and public agency",
      "National entrepreneurship initiative, Ministry of Planning and "
      "Economic Development", "National",
      "The national entrepreneurship initiative, including its One Million "
      "Entrepreneurs ambition, running training, competitions and "
      "ecosystem coordination.",
      "This initiative is the reason this file exists. Alignment with "
      "Rowad is what makes every other door in this file open faster, and "
      "the name itself carries into corporate and donor conversations.",
      "Delivery against the national target, governorate coverage, and "
      "partners who make the ministry look competent.",
      "Recognised delivery partner status under the initiative, with a "
      "memorandum of understanding naming the contribution to the million.",
      "L", "Initiative director, under the Ministry of Planning and "
      "Economic Development",
      "Direct, and through the ecosystem events the initiative convenes. "
      "An MOU here is the single highest-leverage document in this plan.",
      "State fiscal year from July, with initiative milestones announced "
      "at events.",
      "A", "high",
      "Named in this plan's existing target list as Rowad 2030, One "
      "Million Entrepreneurs, under the Ministry of Planning and Economic "
      "Development.",
      arabic="رواد 2030"),

    P("Micro, Small and Medium Enterprise Development Agency (MSMEDA)",
      "Government initiative and public agency",
      "Public agency", "National, all governorates",
      "The state's MSME agency: finance, non-financial services, training "
      "and entrepreneurship support, with a large donor-funded portfolio "
      "behind it.",
      "Holds both the mandate and the money for MSME development, and "
      "contracts non-financial service providers. Also the counterpart for "
      "most donor MSME programmes, so a relationship here appears in other "
      "people's proposals.",
      "Enterprises created and formalised, loans performing, and "
      "governorate coverage.",
      "Non-financial service provider contracting, and training attached "
      "to their lending.",
      "L", "Central administration for entrepreneurship or non-financial "
      "services",
      "Direct, and through the donors who fund their programmes.",
      "State fiscal year from July.",
      "A", "high",
      "Named in this plan's existing target list."),

    P("ITIDA, TIEC and the Digital Egypt Innovation Hubs",
      "Government initiative and public agency",
      "ICT ministry agencies", "National, hub network",
      "Technology innovation and entrepreneurship support under the "
      "Ministry of Communications and Information Technology, including "
      "the Digital Egypt Innovation Hubs, which partner with GIZ and "
      "Flat6Labs on startup acceleration.",
      "The hubs are physical delivery infrastructure with a national "
      "footprint and a donor partner already attached. Curriculum and "
      "facilitation inside them is a direct fit.",
      "Investment-ready startups, hub utilisation, and donor partner "
      "satisfaction.",
      "Curriculum and facilitator supply across the hub network.",
      "M", "Hub programme management at TIEC, with ITIDA above it",
      "Direct to TIEC, and through GIZ, which is already a partner.",
      "State fiscal year from July, with hub programming continuous.",
      "A", "high",
      "Confirmed this session: the Digital Egypt Innovation Hubs "
      "partnership with GIZ and Flat6Labs, run through the ICT ministry."),

    P("NilePreneurs (Central Bank of Egypt)",
      "Government initiative and public agency",
      "Central bank initiative", "National, university-hosted hubs",
      "A Central Bank initiative hosted at universities, providing "
      "business development services, design centres and mentoring to "
      "SMEs, funded by the banking sector.",
      "University-hosted and bank-funded, which is both of this plan's "
      "main buyer types in one structure. Their hubs sit inside the "
      "universities the plan already targets.",
      "SMEs served, university engagement, and bank sector contribution "
      "visibility.",
      "Curriculum and facilitation inside the hub network.",
      "M", "Programme management at the host university, with the "
      "initiative's central team",
      "Through a host university, and through the Central Bank "
      "relationship.",
      "Academic year for hub activity.",
      "A", "medium",
      "The initiative is well established and bank-funded; the current hub "
      "list should be taken from the initiative directly."),

    P("Haya Karima (Decent Life)", "Government initiative and public agency",
      "Presidential rural development initiative",
      "Rural Egypt, 4,500+ villages",
      "The largest rural development programme in Egypt's history, "
      "covering infrastructure, services and economic development in the "
      "poorest villages.",
      "Nothing else reaches rural Egypt at this scale. Income generation "
      "and small enterprise are inside its scope, and corporate donors "
      "contribute to it directly.",
      "Village-level economic outcomes, and visible delivery of a "
      "presidential priority.",
      "An enterprise training component inside the economic development "
      "pillar, funded by the initiative's corporate contributors.",
      "XL", "The initiative's executive secretariat, with the Ministry of "
      "Local Development and Tahya Misr",
      "Through the Ministry of Local Development or through a corporate "
      "contributor who proposes the component.",
      "State fiscal year from July.",
      "B", "medium",
      "Scale and scope are certain; whether external training providers "
      "are contracted into it is the open question."),

    P("Ministry of Youth and Sports",
      "Government initiative and public agency", "Line ministry",
      "National",
      "Youth centres, youth leadership programmes, and the national youth "
      "agenda, including entrepreneurship activities for non-student "
      "youth.",
      "Owns the youth centre network and the non-student population. A "
      "memorandum with this ministry is what makes a one-million number "
      "arithmetically possible.",
      "National coverage, youth participation numbers, and programmes it "
      "can brand as its own.",
      "A memorandum of understanding for facilitator training across "
      "youth centres, with donor funding attached.",
      "L", "Central administration for youth programmes",
      "Direct, and with a donor already identified to pay, which changes "
      "the conversation entirely.",
      "State fiscal year from July.",
      "A", "medium",
      "The ministry's ownership of the youth centre network is certain; "
      "the partnership mechanism needs establishing."),

    P("Ministry of Technical Education and Training",
      "Government initiative and public agency", "Line ministry",
      "National, technical schools and applied technology schools",
      "Technical secondary education and the applied technology schools "
      "programme run with private partners, covering a system of over two "
      "million students.",
      "Already in this plan's named target list. The applied technology "
      "schools are run with corporate partners such as Elsewedy, which "
      "means the funding and the access are in the same room.",
      "Employability of technical graduates and the credibility of the "
      "technical education reform.",
      "An entrepreneurship and employability track across applied "
      "technology schools.",
      "L", "Applied technology schools unit",
      "Direct, and in parallel through the corporate school partners.",
      "Academic year, with state fiscal year from July.",
      "A", "high", "Named in this plan's existing target list."),

    P("Ministry of Social Solidarity",
      "Government initiative and public agency", "Line ministry",
      "National",
      "Registers and regulates all NGOs and foundations, runs Takaful and "
      "Karama, and operates productive families programmes.",
      "Dual relevance: it is the regulator whose registration rules govern "
      "every NGO partnership in this file, and it runs the largest "
      "productive families programme in the country.",
      "Beneficiaries moved into income generation, and compliant partners.",
      "A business formation curriculum for productive families "
      "beneficiaries.",
      "L", "Central administration for productive families",
      "Direct, and through the NGOs already implementing for them.",
      "State fiscal year from July.",
      "B", "medium",
      "Both roles are certain; the contracting route needs establishing."),

    P("Ministry of Higher Education and Scientific Research, and the "
      "Supreme Council of Universities",
      "Government initiative and public agency", "Line ministry",
      "National, 28 public universities and 551 colleges",
      "Governs public higher education, including innovation and "
      "entrepreneurship centres on campuses.",
      "A framework agreement at ministry level converts a college-by-"
      "college sale into a circular that reaches every campus.",
      "Graduate employability and the visibility of university innovation "
      "centres.",
      "A framework memorandum covering university entrepreneurship "
      "centres.",
      "L", "Sector for innovation and entrepreneurship, Supreme Council of "
      "Universities",
      "Through a university president who will champion it upward, not "
      "cold to the ministry.",
      "Academic year, with state fiscal year from July.",
      "A", "high", "Named in this plan's existing target list."),

    # --------------------- Chamber, business association and network
    P("American Chamber of Commerce in Egypt (AmCham)",
      "Chamber, business association and network",
      "Bilateral business chamber", "National",
      "A CSR committee and a large membership of exactly the multinational "
      "and large Egyptian corporates listed in this file, meeting "
      "regularly.",
      "The cheapest access to corporate CSR decision makers in Egypt. One "
      "committee presentation reaches thirty prospects who would each "
      "take a quarter to reach individually.",
      "Content that makes their committee meetings worth attending, and "
      "member value.",
      "A presentation to the CSR committee, and membership if the "
      "economics justify it.",
      "XS", "CSR committee chair, through the chamber secretariat",
      "Through the chamber secretariat, proposing a session.",
      "Committee calendar runs through the year.",
      "A", "medium",
      "AmCham Egypt and its committee structure are well established; the "
      "current CSR committee calendar should be confirmed with them."),

    P("Federation of Egyptian Industries and the industry chambers",
      "Chamber, business association and network",
      "Statutory industry federation", "National",
      "The statutory body for Egyptian industry, with chambers by sector "
      "and a training and skills agenda.",
      "Reaches industrial employers who fund technical training, and its "
      "sector chambers can circulate an offer to hundreds of members.",
      "Member skills supply and sector competitiveness.",
      "A skills and enterprise partnership circulated through sector "
      "chambers.",
      "S", "Training and skills unit, with sector chamber secretaries",
      "Through the federation's training function.",
      "Calendar year.",
      "B", "medium", "Role and structure are certain; fit is a proposal."),

    P("Egyptian Junior Business Association (EJB)",
      "Chamber, business association and network",
      "Young business leaders association", "National",
      "Young Egyptian business leaders, with an entrepreneurship and "
      "youth development agenda and an active committee structure.",
      "Members are young enough to still be building companies and senior "
      "enough to write a cheque or open a door. One of the best mentor "
      "pools in the country.",
      "Member engagement and a visible contribution to youth "
      "entrepreneurship.",
      "A mentor network partnership, and sponsorship from member "
      "companies.",
      "S", "Entrepreneurship or CSR committee chair",
      "Through a member introduction.",
      "Calendar year.",
      "B", "medium", "Association and agenda are established."),

    P("Egyptian Businessmen's Association and the bilateral business "
      "councils", "Chamber, business association and network",
      "Business associations", "National",
      "Senior business leadership across the largest Egyptian groups, plus "
      "the German, French, Italian, British and Gulf bilateral councils.",
      "The bilateral councils are the overlap between corporate money and "
      "donor money: the German-Arab chamber sits beside GIZ, the French "
      "beside AFD. One room, both funders.",
      "Member value and bilateral economic relations.",
      "A programme framed as a bilateral economic contribution, presented "
      "to the relevant council.",
      "S", "Secretary general of the relevant council",
      "Through the council secretariats, which are accessible.",
      "Calendar year.",
      "B", "medium",
      "The councils exist and are active; the specific route depends on "
      "which donor relationship is being built alongside."),
]


# ------------------------------------------------------------------ playbook
# One entry per category. These are the mechanics that would otherwise have
# been repeated on every row: the instrument the money arrives through, who
# actually decides, what they are measured on, the objection that kills the
# deal, and the proof that answers it.
PLAYBOOK = [
    dict(cat="Telecom and technology",
         money="Marketing or CSR budget, occasionally a registered "
               "foundation. Annual, discretionary, and easy to move inside "
               "the year if the story is good.",
         decides="CSR or sustainability manager proposes; the marketing or "
                 "corporate affairs director approves; the chief executive "
                 "signs anything with their logo on a national programme.",
         measured="Reach, brand association, employee engagement, and a "
                  "line in the sustainability report.",
         objection="We already do something like this.",
         proof="A comparison that shows what their existing programme does "
               "not do: certification, a report the institution keeps, and "
               "progress after the event ends.",
         cycle="Calendar year for most; Vodafone runs April to March. "
               "Budgets are set in the last quarter before the year starts.",
         first="A one-page programme offer with a number of beneficiaries, "
               "a cost per beneficiary, and the report they will receive."),

    dict(cat="Bank and financial services",
         money="CSR budget, a foundation with its own governance, or an SME "
               "banking marketing line. The third is the fastest and the "
               "least contested.",
         decides="Head of sustainability or CSR proposes; a board committee "
                 "approves foundation money; SME banking can commit its own "
                 "marketing budget without the committee.",
         measured="Financial inclusion numbers, sustainability report "
                  "content, SME customer acquisition, and compliance with "
                  "Central Bank sustainable finance principles.",
         objection="This is not banking.",
         proof="Frame the output as bankable businesses: a trained, "
               "formalised micro-business is a future borrower with a lower "
               "default risk, not a charitable beneficiary.",
         cycle="Calendar year, with sustainability reports published in the "
               "first quarter and budgets set in the fourth.",
         first="A short note to SME banking, not to CSR, with the borrower "
               "quality argument in the first paragraph."),

    dict(cat="Energy, oil and gas",
         money="Social investment, often a licence-to-operate obligation "
               "attached to specific concessions and governorates.",
         decides="Social investment or social performance manager, with the "
                 "country external affairs lead. Large commitments go to the "
                 "group.",
         measured="Community acceptance around operations, local "
                  "employment, and delivery against commitments made to the "
                  "state.",
         objection="We only fund in our operating areas.",
         proof="Do not argue with it. Propose the programme in their "
               "governorates by name, costed per community.",
         cycle="Calendar year, with multi-year commitments and annual "
               "review.",
         first="A geography-specific proposal naming their own operating "
               "communities, never a national one."),

    dict(cat="FMCG, food and retail",
         money="CSR or corporate affairs budget, sometimes a global "
               "commitment with a country target attached.",
         decides="Corporate affairs or public policy manager, with the "
                 "country general manager approving.",
         measured="Progress against the global commitment, supply chain "
                  "goodwill, and women's economic participation.",
         objection="Our global programme has its own partners.",
         proof="Offer to deliver inside the global programme rather than "
               "beside it, with the global commitment's own metric used as "
               "the reporting metric.",
         cycle="Calendar year, with global commitment reporting in the "
               "first quarter.",
         first="Name their global commitment in the subject line and "
               "propose a country contribution to it."),

    dict(cat="Industry, construction and real estate",
         money="CSR budget, community investment around projects, or a "
               "technical training budget that is not CSR at all.",
         decides="Corporate communications for sponsorship; the technical "
                 "training or community function for anything operational.",
         measured="Local employment, trade skills, community acceptance, "
                  "and occupied commercial space in the case of developers.",
         objection="We fund buildings, not programmes.",
         proof="Propose the programme inside a building they already "
               "funded: a school, an academy, a community centre.",
         cycle="Calendar year, project-driven for community investment.",
         first="An offer addressed to the technical training function, "
               "framed as self-employment for tradespeople."),

    dict(cat="Pharma and healthcare",
         money="Corporate affairs, tightly constrained by compliance rules "
               "on what may be funded and who may benefit.",
         decides="Corporate affairs, with compliance holding a veto.",
         measured="Auditable community investment with no promotional risk.",
         objection="Compliance will not allow it.",
         proof="Keep the ask narrow and non-promotional: employee "
               "volunteering, or a health-sector venture track with no "
               "product association.",
         cycle="Calendar year.",
         first="Through the AmCham healthcare committee rather than "
               "company by company."),

    dict(cat="Corporate and family foundation",
         money="Endowment income or a fixed share of corporate profit, "
               "governed by a board and a published mandate.",
         decides="Programme manager assesses; executive director "
                 "recommends; the board approves above a threshold.",
         measured="Cost per outcome, fidelity to the published mandate, "
                  "and the quality of the implementing organisation.",
         objection="This is outside our mandate.",
         proof="Read the mandate before writing. If enterprise is not in "
               "it, do not write. The CIB Foundation is health; that is a "
               "no, not a harder sell.",
         cycle="Call-driven or rolling, with board meetings setting the "
               "real calendar.",
         first="A two-page concept note in their own mandate's language, "
               "with a budget and an evaluation plan."),

    dict(cat="Bilateral donor and development agency",
         money="Public money from a foreign government, spent through "
               "tenders, grants and service contracts under that "
               "government's procurement law.",
         decides="The programme manager writes the terms of reference; a "
                 "procurement unit runs the process and cannot be "
                 "influenced once it starts.",
         measured="Delivery against a logframe, disaggregated by sex and "
                  "sometimes by disability and governorate, with financial "
                  "compliance that survives audit.",
         objection="You are not on our supplier list and you have no "
                   "audited track record.",
         proof="Get on the list first and bid later. Start as a "
               "sub-contractor to someone who is already on it, and "
               "register on every supplier portal before there is a tender "
               "to bid on.",
         cycle="Annual work planning, usually set between September and "
               "December for the following year. Being known before the "
               "terms of reference are written matters more than bidding "
               "well afterwards.",
         first="Supplier registration, then a capability statement to the "
               "programme team, then a meeting about what they are planning "
               "rather than what you sell."),

    dict(cat="UN agency and multilateral",
         money="Donor-funded project budgets, spent through UN procurement "
               "rules: service contracts, responsible party agreements and "
               "long-term agreements.",
         decides="The project's chief technical adviser or programme "
                 "specialist defines the need; procurement runs the "
                 "process; a contracts committee approves above thresholds.",
         measured="Results framework indicators, gender disaggregation, "
                  "and the agency's own standards on safeguarding, "
                  "conflict of interest and data.",
         objection="You are not registered and we cannot sole-source.",
         proof="Register on the United Nations Global Marketplace. It is "
               "free, it is a precondition for most contracts, and not "
               "having done it is an unforced error.",
         cycle="Country programme documents run several years; annual work "
               "plans are agreed early in the year and procurement follows.",
         first="UNGM registration, then a capability statement to the "
               "relevant specialist, then watch the procurement notices."),

    dict(cat="International NGO and implementer",
         money="Donor money they have already won, from which they "
               "sub-contract delivery.",
         decides="The project manager, within a budget already approved by "
                 "the donor.",
         measured="Delivery against the commitments in their own proposal, "
                  "to their donor's compliance standard.",
         objection="Our budget for this is already allocated.",
         proof="Be in the room before the proposal is written. Ask what "
               "they are bidding on next, and offer to be named as the "
               "delivery partner in the bid.",
         cycle="Proposal-driven. Partner selection happens weeks before a "
               "call closes, which is the only window that matters.",
         first="A partnership conversation about their pipeline, not a "
               "sales pitch about ours."),

    dict(cat="Egyptian NGO and social enterprise",
         money="Grants they have won, corporate sponsorship, zakat, or "
               "their own earned income. Usually tight.",
         decides="The executive director, quickly, because these "
                 "organisations are small enough to decide.",
         measured="Beneficiaries served, donor satisfaction, and whether "
                  "the partnership brings money rather than costs it.",
         objection="We cannot pay for this.",
         proof="Do not ask them to pay. Bring the funder, or certify their "
               "staff so they deliver it themselves. Revenue comes from "
               "the funder; reach comes from them.",
         cycle="Donor-driven, with Ramadan shaping the fundraising year "
               "for the zakat-funded organisations.",
         first="A partnership proposal in which the money comes from "
               "somewhere else."),

    dict(cat="Youth and student organisation",
         money="Almost none. Their currency is reach, volunteers and "
               "legitimacy.",
         decides="Student or young professional leadership that turns over "
                 "every year, which means both fast decisions and no "
                 "institutional memory.",
         measured="Member experience, chapter activity, and competition "
                  "results.",
         objection="What do we get out of it.",
         proof="Free access for their members, training for their "
               "leadership, and a named role in the programme. Never ask "
               "a student organisation for money.",
         cycle="Leadership turns over in the summer. Re-sign every "
               "relationship annually, and expect to.",
         first="An offer of value to their members, with a request for "
               "access rather than for budget."),

    dict(cat="Government initiative and public agency",
         money="State budget, donor-funded programmes attached to the "
               "agency, or corporate contributions channelled through the "
               "initiative.",
         decides="A committee, slowly, with the signature of a senior "
                 "official who needs to be certain nothing will embarrass "
                 "them.",
         measured="Delivery against a published national target, "
                  "governorate coverage, and the absence of procurement "
                  "irregularity.",
         objection="Procurement rules do not allow a direct award.",
         proof="Arrive with the funding already identified. A proposal "
               "where a donor or corporate pays and the ministry only "
               "grants access is a far easier signature than one that asks "
               "the ministry to spend.",
         cycle="State fiscal year begins in July. Proposals land best "
               "between February and April.",
         first="A memorandum of understanding that costs them nothing, "
               "grants access, and names their initiative in the title."),

    dict(cat="Chamber, business association and network",
         money="None directly. They are distribution.",
         decides="A committee chair and a secretariat.",
         measured="Member value and attendance.",
         objection="Members only.",
         proof="Join if the arithmetic works, or present as an invited "
               "speaker, which costs nothing.",
         cycle="Committee calendars run through the year.",
         first="A proposed session for their committee, offered as content "
               "rather than as a pitch."),
]


# ----------------------------------------------------------------- documents
# What has to exist before the first serious meeting, by who asks for it.
DOCUMENTS = [
    ("Commercial registration and tax card", "Everyone",
     "The first thing any procurement process asks for. No registration, no "
     "contract, however good the programme.", "Must have"),
    ("Audited financial statements, two to three years", "Donors, UN, EU",
     "The single most common disqualifier for a young company. Until these "
     "exist, bid as a sub-contractor to someone who has them.", "Must have"),
    ("Company profile and capability statement, Arabic and English",
     "Everyone",
     "Two pages: what the company does, what it has delivered, who it has "
     "delivered it to, and the team. Updated after every cohort.",
     "Must have"),
    ("Child safeguarding and protection policy",
     "UNICEF, schools, any work with under-18s",
     "A hard precondition for the schools engine and for UN work. Must name "
     "a responsible person, a reporting route and a vetting standard.",
     "Must have"),
    ("Data protection and student data policy",
     "Universities, schools, UN, EU",
     "Egyptian data protection law plus institutional rules. Universities "
     "ask before they let a platform touch student records.", "Must have"),
    ("Anti-fraud, anti-corruption and conflict of interest declarations",
     "Donors, UN, EU, government", "Standard annexes in every donor tender. "
     "Prepare once, reuse.", "Must have"),
    ("Methodology document with learning outcomes",
     "Donors, foundations, ministries",
     "The fifteen missions mapped to competencies and hours. This is what "
     "turns a product into a curriculum in a technical evaluation.",
     "Must have"),
    ("Facilitator certification standard and roster",
     "Everyone buying delivery",
     "Who may deliver, how they were certified, and how many there are. "
     "This is the capacity claim that sales sells against.", "Must have"),
    ("Monitoring and evaluation framework with a results chain",
     "Donors, UN, foundations",
     "Indicators, baselines, data collection method, and disaggregation by "
     "sex, age and governorate. Written before the project, not after.",
     "Must have"),
    ("Cohort report template", "Institutions, sponsors, donors",
     "The artefact the buyer actually keeps. Show it in the first meeting; "
     "it closes more than the pitch does.", "Must have"),
    ("Reference letters from delivered cohorts", "Everyone",
     "Three letters on institutional letterhead beat any amount of "
     "description. Ask for them while the goodwill is fresh.", "Build early"),
    ("UNGM registration", "All UN agencies",
     "Free, quick, and a precondition for most UN contracting. There is no "
     "reason not to have it.", "Build early"),
    ("Donor supplier registrations", "GIZ, EBRD, British Council, embassies",
     "Each has its own portal or roster. Register before a tender exists, "
     "because the window to register is never the window to bid.",
     "Build early"),
    ("Insurance and liability cover", "Institutions, government",
     "Public liability for in-person delivery on campuses and in schools. "
     "Asked for more often than expected.", "Build early"),
    ("Arabic contract templates and an MOU template", "Government, NGOs",
     "A ministry will not redraft your English contract. Arrive with Arabic "
     "that their legal department can sign.", "Build early"),
    ("Evidence of bilingual delivery", "Donors, ministries, Gulf buyers",
     "Materials in Arabic, not translated at the last minute. This is "
     "checked in technical evaluation and it is where most international "
     "providers lose.", "Differentiator"),
    ("Independent evaluation of an earlier cohort", "Foundations, donors",
     "Expensive, and worth more than everything above once it exists. "
     "Budget it into the first donor contract.", "Differentiator"),
]


# ------------------------------------------------------------------ messages
# First-contact templates. Written to be pasted and edited, not admired.
# [SQUARE BRACKETS] are the only things to change. Every one of them is short
# on purpose: the first message exists to get a meeting, not to explain the
# company.
MESSAGES = [
    ("Corporate CSR, first contact",
     "Telecom and technology / Bank / FMCG / Industry",
     "Subject: [THEIR PROGRAMME NAME] and 1,000 young entrepreneurs in "
     "[GOVERNORATE]\n\n"
     "Dear [ROLE],\n\n"
     "[COMPANY] funds [THEIR PROGRAMME OR THEME] in Egypt. We run the "
     "delivery side of exactly that: a fifteen-mission entrepreneurship "
     "programme, in Arabic, delivered in person by certified facilitators "
     "and supported by a platform that reviews every submission.\n\n"
     "A cohort is [N] young people over [DAYS] days. It costs [AMOUNT] and "
     "it ends with a report naming every participant, what they built and "
     "what they completed, which is the document that goes into your "
     "sustainability reporting.\n\n"
     "We have delivered [NUMBER] cohorts with [INSTITUTIONS]. Could we show "
     "you one report, in twenty minutes, at a time that suits you?\n\n"
     "[NAME]\n[TITLE], StartPad"),

    ("Development agency, first contact",
     "GIZ / EU / British Council / AICS / Expertise France",
     "Subject: Capability statement, entrepreneurship training delivery, "
     "Egypt\n\n"
     "Dear [ROLE],\n\n"
     "We are an Egyptian provider of entrepreneurship training delivery: "
     "bilingual curriculum, a certified facilitator pool of [N] across "
     "[GOVERNORATES], and a platform that produces participant-level "
     "evidence for reporting.\n\n"
     "We are registered on [PORTAL] and attach our capability statement. We "
     "are not writing about a specific tender. We would like twenty minutes "
     "to understand what [PROGRAMME] is planning for [YEAR], so that if "
     "delivery capacity is needed you already know what exists locally.\n\n"
     "[NAME]\n[TITLE], StartPad"),

    ("Foundation concept note, opening paragraph",
     "Sawiris / Drosos / Misr El Kheir / Alfanar",
     "[FOUNDATION] states that it works on [THEIR MANDATE, IN THEIR OWN "
     "WORDS]. This note proposes [PROGRAMME NAME]: [N] young people in "
     "[GOVERNORATES] taken from idea to a first customer over [DURATION], "
     "of whom we expect [N] to be operating a business at month twelve and "
     "[N] to be women.\n\n"
     "The cost is [AMOUNT], which is [AMOUNT] per participant and [AMOUNT] "
     "per business still operating at month twelve. [PERCENT] of the budget "
     "is delivery, [PERCENT] is evaluation, and [PERCENT] is overhead.\n\n"
     "We are not asking the foundation to build a programme. The curriculum, "
     "the facilitator pool and the measurement system exist. The request is "
     "to fund their use in [GOVERNORATES], where nobody currently pays for "
     "them."),

    ("NGO partnership, first contact",
     "INJAZ / Nahdet El Mahrousa / Life Makers / CARE / Plan",
     "Subject: Partnership, not a sale\n\n"
     "Dear [ROLE],\n\n"
     "[ORGANISATION] reaches [THEIR REACH]. We have the curriculum and the "
     "facilitator certification; we do not have your reach and will not "
     "build it.\n\n"
     "The proposal is that we certify [N] of your staff or volunteers to "
     "deliver the programme, and that we go to [FUNDER] together with you "
     "as the implementer and us as the methodology partner. The funding "
     "would sit with you.\n\n"
     "Could we meet to see whether the method fits what you already run?\n\n"
     "[NAME]\n[TITLE], StartPad"),

    ("Government, memorandum request",
     "Rowad 2030 / MSMEDA / Ministry of Youth / Ministry of Technical "
     "Education",
     "Subject: Contribution to [NATIONAL INITIATIVE], no cost to the "
     "[MINISTRY OR AGENCY]\n\n"
     "Dear [ROLE],\n\n"
     "We would like to contribute [N] trained young entrepreneurs to "
     "[INITIATIVE] over [PERIOD], at no cost to [MINISTRY OR AGENCY]. The "
     "funding is from [FUNDER OR: to be raised against this memorandum].\n\n"
     "What we are asking for is access and recognition: permission to work "
     "with [INSTITUTIONS], and acknowledgement that the participants count "
     "towards the initiative's target.\n\n"
     "We attach a draft memorandum in Arabic for your legal department, and "
     "the methodology document.\n\n"
     "[NAME]\n[TITLE], StartPad"),

    ("Youth organisation, first contact",
     "AIESEC / Enactus / JCI / Hult Prize / student branches",
     "Subject: Free access for your members, and training for your board\n\n"
     "Hi [NAME],\n\n"
     "We run a fifteen-mission entrepreneurship programme in Arabic. The "
     "first three missions are free, for everyone, forever.\n\n"
     "What we would like from [ORGANISATION] is to make it available to "
     "your members and to train [N] of your board as certified "
     "facilitators, which they keep after their term ends.\n\n"
     "There is no cost to you and we are not asking for sponsorship. Fifteen "
     "minutes this week?\n\n"
     "[NAME], StartPad"),
]


# ------------------------------------------------------------------ sequence
# What happens after the first message, because almost nothing closes on it.
SEQUENCE = [
    ("Day 0", "First message",
     "One channel, one message, under 200 words, with a specific ask for 20 "
     "minutes. Attach nothing except a capability statement for donors."),
    ("Day 4", "Second touch, different channel",
     "If email went unanswered, LinkedIn to the same role, or a call to the "
     "switchboard asking for the function rather than the person."),
    ("Day 10", "Value, not a chase",
     "Send something they can use without meeting us: a one-page briefing "
     "on their own sector's youth numbers, or the cohort report template."),
    ("Day 21", "Referral attempt",
     "Ask the warm route in the registry's route column to make the "
     "introduction. Stop sending cold messages after this point."),
    ("Day 45", "Event contact",
     "Meet them where they already are. Ecosystem events, chamber "
     "committees and donor coordination meetings cost nothing and convert "
     "better than any email."),
    ("Quarterly", "Nurture",
     "One useful update a quarter to everyone in the registry who has not "
     "said no. Results, not news."),
    ("On any no", "Record the reason",
     "Write the reason in the registry. A no because of mandate is "
     "permanent; a no because of budget timing is a date."),
]
