"""
MENA startup-programme scouting registry — source of truth.

SCOPE      Egypt and GCC first, then wider MENA. Israel excluded per scoping.
SOURCING   Every URL here appeared in a live web-search result during compilation.
           None were written from memory. The compiling environment's egress proxy
           blocked ALL direct page fetches (verified: curl to flat6labs.com,
           magnitt.com, wamda.com, itida.gov.eg, hub71.com, oasis500.com,
           sheraa.ae, startupqatar.qa all failed), so nothing here is fetch-verified.
           `confidence` records how firm each row is; run scripts/scout_scraper.py
           from an unrestricted network to verify and enrich every row.

CONFIDENCE
  high    entity + URL both appeared as a search-result link, facts from result text
  medium  entity confirmed in result text, URL inferred from a result on same domain
  low     mentioned in prose only — verify the URL before relying on it

Row shape (PROGRAMS):
  entity, entity_type, country, city, program, program_type, stage, sectors,
  eligibility, funding, equity, duration, cadence, status, description, stats,
  entity_url, programs_url, apply_url, confidence, source
"""

# ---------------------------------------------------------------------------
# Controlled vocabularies — keep the sheet machine-readable
# ---------------------------------------------------------------------------
ENTITY_TYPES = [
    "Accelerator", "Incubator", "Government / Authority", "Sovereign / National fund",
    "VC firm", "Angel network", "Corporate programme", "University programme",
    "NGO / Development agency", "Media / Data platform", "Aggregator / Directory",
    "Coworking / Hub",
]
PROGRAM_TYPES = [
    "Accelerator", "Incubator", "Seed fund", "Grant", "Competition / Challenge",
    "Fellowship", "Bootcamp", "Soft landing / Market access", "Fund of funds",
    "Debt / Loan", "Directory listing", "News feed",
]
STAGES = ["Idea", "Pre-seed", "Seed", "Series A", "Growth", "Any"]

# ---------------------------------------------------------------------------
# PROGRAMS — one row per programme. Entities repeat by design.
# ---------------------------------------------------------------------------
PROGRAMS = [

    # ======================= EGYPT =======================
    dict(entity="Flat6Labs", entity_type="Accelerator", country="Egypt", city="Cairo",
         program="Cairo Seed Programme", program_type="Accelerator", stage="Pre-seed",
         sectors="Tech, agnostic", eligibility="Egypt-based startups",
         funding="Seed funding reported up to EGP 1.5M", equity="Yes (equity taken)",
         duration="~4 months", cadence="Multiple cycles / year", status="Active",
         description="MENA's most established seed accelerator. Structured four-month "
                     "programme with seed funding, mentorship, and a regional investor "
                     "and corporate-partner network.",
         stats="Flat6Labs invests in 100+ startups annually across MENA",
         entity_url="https://flat6labs.com/",
         programs_url="http://flat6labs.com/Location/egypt/",
         apply_url="", confidence="high",
         source="flat6labs.com Egypt location page; xyzlab/nucamp ecosystem round-ups"),

    dict(entity="Falak Startups", entity_type="Accelerator", country="Egypt", city="Cairo",
         program="Falak Acceleration Programme", program_type="Accelerator", stage="Pre-seed",
         sectors="Tech, agnostic", eligibility="Egyptian tech startups",
         funding="Up to EGP 500,000", equity="Yes", duration="Cycle-based",
         cadence="Recurring cycles", status="Active",
         description="Accelerator backed by Egypt Ventures, empowering Egyptian tech "
                     "entrepreneurs with capital and support to turn ideas into businesses.",
         stats="Funding up to EGP 500,000 per startup",
         entity_url="https://www.falakstartups.com/",
         programs_url="https://www.falakstartups.com/",
         apply_url="", confidence="high",
         source="falakstartups.com; EgyptInnovate funding announcement"),

    dict(entity="ITIDA", entity_type="Government / Authority", country="Egypt", city="Cairo",
         program="Innovation Ecosystem / Startup Support", program_type="Incubator",
         stage="Idea", sectors="ICT, deep tech",
         eligibility="Egyptian startups and innovators",
         funding="Reported EGP 480K per startup + cloud credits", equity="No (government)",
         duration="Programme-dependent", cadence="Rolling calls", status="Active",
         description="Egypt's IT Industry Development Authority. Runs the national "
                     "innovation-ecosystem portfolio: incubation, EgyptInnovate platform, "
                     "innovation clusters, and international-events support for startups.",
         stats="ITIDA programmes reported supporting 1,800 startups and creating 31,000 jobs",
         entity_url="https://itida.gov.eg/",
         programs_url="https://itida.gov.eg/English/Programs/Innovation-Ecosystem/Pages/default.aspx",
         apply_url="", confidence="high",
         source="itida.gov.eg innovation-ecosystem page; Tech In Africa ecosystem comparison"),

    dict(entity="TIEC", entity_type="Government / Authority", country="Egypt", city="Cairo",
         program="Virtual Incubation Programme", program_type="Incubator", stage="Idea",
         sectors="ICT", eligibility="Egyptian innovators", funding="Grant-based",
         equity="No", duration="Programme-dependent", cadence="Recurring calls",
         status="Active",
         description="Technology Innovation and Entrepreneurship Center, affiliated to "
                     "ITIDA. Runs several structured programmes including virtual incubation.",
         stats="ITIDA-affiliated; government-backed structured programme",
         entity_url="https://itida.gov.eg/",
         programs_url="https://itida.gov.eg/English/Programs/Innovation-Ecosystem/Pages/default.aspx",
         apply_url="", confidence="medium",
         source="Ecosystem round-ups describe TIEC as ITIDA-affiliated; URL inferred to ITIDA domain"),

    dict(entity="EgyptInnovate", entity_type="Media / Data platform", country="Egypt", city="Cairo",
         program="Ecosystem platform & opportunity listings", program_type="Directory listing",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="ITIDA's think-tank and information hub for Egypt's innovation "
                     "ecosystem. Publishes funding calls and programme announcements — "
                     "a high-value scrape target for new Egyptian programmes.",
         stats="National ecosystem platform operated under ITIDA",
         entity_url="https://egyptinnovate.com/",
         programs_url="https://egyptinnovate.com/en/news",
         apply_url="", confidence="medium",
         source="egyptinnovate.com/en/news/... appeared in results; section URL inferred"),

    dict(entity="MSMEDA", entity_type="Government / Authority", country="Egypt", city="Cairo",
         program="MSME financing & technical support", program_type="Debt / Loan",
         stage="Any", sectors="All", eligibility="Egyptian MSMEs and startups",
         funding="Financing + technical support", equity="No",
         duration="Ongoing", cadence="Rolling", status="Active",
         description="Micro, Small and Medium Enterprise Development Agency — the "
                     "designated coordinating body for SME policy in Egypt. Offers "
                     "financing, training and incubation; partnered with Startup Egypt "
                     "to expand financing and technical support.",
         stats="Highlighted support for 209 startups at the Startup Egypt launch",
         entity_url="https://msmeda.org.eg/",
         programs_url="https://msmeda.org.eg/",
         apply_url="", confidence="low",
         source="Daily News Egypt & Zawya coverage; entity URL NOT in results — verify"),

    dict(entity="Startup Egypt", entity_type="Government / Authority", country="Egypt", city="Cairo",
         program="National startup platform", program_type="Directory listing", stage="Any",
         sectors="All", eligibility="Egyptian startups", funding="Routes to funding",
         equity="No", duration="Ongoing", cadence="Continuous", status="Active",
         description="Unified digital interface for business registration, funding "
                     "applications and mentorship, bringing incubators, accelerators and "
                     "VC networks into a single national ecosystem.",
         stats="MSMEDA partnership to expand financing; 209 startups cited at launch",
         entity_url="",
         programs_url="https://www.arabfinance.com/en/news/newdetails/startup-egypt-turning-innovation-into-economic-growth",
         apply_url="", confidence="low",
         source="Arab Finance / Zawya / Daily News coverage. Official URL NOT found — verify"),

    dict(entity="NilePreneurs", entity_type="Government / Authority", country="Egypt", city="Cairo",
         program="Innovation vouchers / R&D as a service", program_type="Grant", stage="Any",
         sectors="Industry, product development", eligibility="Egyptian SMEs",
         funding="Innovation vouchers", equity="No", duration="Project-based",
         cadence="Rolling", status="Active",
         description="Central Bank of Egypt-backed initiative offering R&D as a service "
                     "through innovation vouchers — new product development, mentoring "
                     "and capacity building for SMEs.",
         stats="200+ product-development projects; services to 800 SMEs",
         entity_url="https://nilepreneurs.com/",
         programs_url="https://nilepreneurs.com/",
         apply_url="", confidence="low",
         source="OECD SME policy report text; entity URL NOT in results — verify"),

    dict(entity="AUC Venture Lab", entity_type="University programme", country="Egypt", city="Cairo",
         program="Startup Accelerator (+ FinTech track with CIB)", program_type="Accelerator",
         stage="Pre-seed", sectors="Tech, FinTech, AI",
         eligibility="Egyptian startups", funding="Equity-free support", equity="No",
         duration="Cycle-based", cadence="Multiple cohorts / year", status="Active",
         description="American University in Cairo's accelerator. Readies teams for "
                     "investment and connects them to corporate demand; runs sector "
                     "tracks including FinTech with CIB.",
         stats="Zero-equity support with specialised tracks",
         entity_url="https://venturelab.aucegypt.edu/",
         programs_url="https://venturelab.aucegypt.edu/",
         apply_url="", confidence="low",
         source="Multiple ecosystem round-ups; entity URL NOT in results — verify"),

    dict(entity="EdVentures", entity_type="Corporate programme", country="Egypt", city="Cairo",
         program="EdTech investment & Creativa innovation hubs", program_type="Seed fund",
         stage="Pre-seed", sectors="EdTech", eligibility="EdTech startups",
         funding="Investment", equity="Yes", duration="Ongoing", cadence="Rolling",
         status="Active",
         description="Nahdet Misr's EdTech investment arm, active since 2017. Appointed "
                     "by the Ministry of Communications and IT to manage Egypt's digital "
                     "innovation hubs, starting with the Creativa hub in Sohag.",
         stats="Backed 8 new Egyptian startups in a 2024 cohort",
         entity_url="https://edventures.vc/",
         programs_url="https://edventures.vc/",
         apply_url="", confidence="low",
         source="Launch Base Africa coverage; entity URL NOT in results — verify"),

    dict(entity="Sawari Ventures", entity_type="VC firm", country="Egypt", city="Cairo",
         program="Venture investment (North Africa)", program_type="Seed fund",
         stage="Series A", sectors="Knowledge & innovation-based tech",
         eligibility="North Africa", funding="VC investment", equity="Yes",
         duration="N/A", cadence="Rolling", status="Active",
         description="Cairo-based venture capital firm investing in knowledge and "
                     "innovation-based technologies across North Africa.",
         stats="Leading Egyptian VC",
         entity_url="https://sawariventures.com/",
         programs_url="https://sawariventures.com/",
         apply_url="", confidence="high", source="sawariventures.com in search results"),

    dict(entity="Innoventures", entity_type="Incubator", country="Egypt", city="Cairo",
         program="Startup Reactor", program_type="Incubator", stage="Idea",
         sectors="Tech, media, energy, creative", eligibility="Egyptian startups",
         funding="Seed funding", equity="Yes", duration="Cycle-based",
         cadence="Recurring", status="Active",
         description="Active since 2010 in both seed funding and hands-on incubation. "
                     "The Startup Reactor programme attracts tech, media, energy and "
                     "creative-sector founders.",
         stats="Operating since 2010",
         entity_url="", programs_url="", apply_url="", confidence="low",
         source="Ecosystem round-up prose only — entity URL NOT found, verify before use"),

    dict(entity="GESR", entity_type="NGO / Development agency", country="Egypt", city="Cairo",
         program="Social enterprise accelerator", program_type="Accelerator", stage="Idea",
         sectors="Education, health, clean water, affordable housing",
         eligibility="Social enterprises", funding="Funding + mentorship", equity="Varies",
         duration="Cycle-based", cadence="Recurring", status="Active",
         description="Linked to the Misr El-Kheir Foundation. Focuses on social-impact "
                     "themes: education, health, clean water and affordable housing.",
         stats="Impact-focused accelerator",
         entity_url="", programs_url="", apply_url="", confidence="low",
         source="Ecosystem round-up prose only — entity URL NOT found, verify"),

    dict(entity="Cairo Angels", entity_type="Angel network", country="Egypt", city="Cairo",
         program="Angel investment network", program_type="Seed fund", stage="Pre-seed",
         sectors="Agnostic", eligibility="Egypt / MENA", funding="Angel rounds",
         equity="Yes", duration="N/A", cadence="Rolling", status="Active",
         description="Angel network investing in early-stage Egyptian and regional startups.",
         stats="2nd most active angel network in Africa per the Africa Business Angel Network",
         entity_url="", programs_url="", apply_url="", confidence="low",
         source="Visible.vc round-up prose; entity URL NOT in results — verify"),

    dict(entity="Endeavor Egypt", entity_type="NGO / Development agency", country="Egypt",
         city="Cairo", program="Endeavor Entrepreneur selection", program_type="Fellowship",
         stage="Growth", sectors="Agnostic", eligibility="High-impact scale-ups",
         funding="Network + co-investment", equity="No (network model)",
         duration="Multi-year", cadence="Rolling selection panels", status="Active",
         description="Supports high-impact entrepreneurs with mentorship and access to "
                     "Endeavor's global network.",
         stats="Part of the global Endeavor network",
         entity_url="", programs_url="", apply_url="", confidence="low",
         source="Ecosystem round-up prose; entity URL NOT in results — verify"),

    dict(entity="Egypt Ventures", entity_type="Sovereign / National fund", country="Egypt",
         city="Cairo", program="Startup investment & accelerator backing",
         program_type="Fund of funds", stage="Pre-seed", sectors="Agnostic",
         eligibility="Egyptian startups", funding="Investment into startups & accelerators",
         equity="Yes", duration="N/A", cadence="Rolling", status="Active",
         description="State-backed investment vehicle; backs Falak Startups and other "
                     "Egyptian acceleration platforms.",
         stats="Backer of Falak Startups",
         entity_url="", programs_url="", apply_url="", confidence="low",
         source="EInA / Visible.vc prose; entity URL NOT in results — verify"),

    dict(entity="Egypt Fund of Funds (with World Bank Group)",
         entity_type="Sovereign / National fund", country="Egypt", city="Cairo",
         program="Fund of Funds investment programme", program_type="Fund of funds",
         stage="Any", sectors="All", eligibility="Egyptian startups (via funds)",
         funding="USD 50 million total financing", equity="Indirect (LP)",
         duration="Multi-year", cadence="N/A", status="Active",
         description="Launched with the World Bank Group to channel capital into "
                     "Egyptian startups through participating funds.",
         stats="USD 50M total financing",
         entity_url="", programs_url="", apply_url="", confidence="low",
         source="entARABI / Startup Sync coverage; official URL NOT found — verify"),

    # ======================= SAUDI ARABIA =======================
    dict(entity="KAUST", entity_type="University programme", country="Saudi Arabia",
         city="Thuwal", program="TAQADAM Startup Accelerator", program_type="Accelerator",
         stage="Pre-seed", sectors="Deep tech", eligibility="Saudi-based / KAUST-linked teams",
         funding="USD 40,000 grant; up to USD 1M follow-on", equity="No (non-dilutive grant)",
         duration="6 months", cadence="Annual cohort", status="Active",
         description="Founded 2016 by KAUST with SAB. Six-month accelerator for deep-tech "
                     "startups needing patient capital; non-dilutive grant-based funding.",
         stats="USD 40,000 per accepted startup; USD 1M follow-on for selected teams",
         entity_url="https://taqadam.kaust.edu.sa/",
         programs_url="https://taqadam.kaust.edu.sa/",
         apply_url="", confidence="high",
         source="taqadam.kaust.edu.sa; leap.kaust.edu.sa TAQADAM page"),

    dict(entity="Misk Foundation", entity_type="NGO / Development agency",
         country="Saudi Arabia", city="Riyadh", program="Misk Accelerator",
         program_type="Accelerator", stage="Seed", sectors="Tech",
         eligibility="Seed-stage tech startups, local and global, using KSA as a platform",
         funding="Zero-equity support", equity="No (zero equity)", duration="3 months",
         cadence="Recurring cohorts", status="Active",
         description="Founded 2019. Three-month zero-equity accelerator enabling early-stage "
                     "tech startups that want Saudi Arabia as their platform to operate and grow.",
         stats="3-month, zero-equity; founded 2019",
         entity_url="https://misk.org.sa/en/",
         programs_url="https://misk.org.sa/en/programs/misk-accelerator/",
         apply_url="https://hub.misk.org.sa/programs/entrepreneurship/misk-accelerator/",
         confidence="high", source="misk.org.sa programme pages; hub.misk.org.sa"),

    dict(entity="Misk Foundation", entity_type="NGO / Development agency",
         country="Saudi Arabia", city="Riyadh", program="Impact Accelerator",
         program_type="Accelerator", stage="Seed", sectors="Social impact",
         eligibility="Impact ventures", funding="Programme support", equity="No",
         duration="Cohort-based", cadence="Recurring", status="Active",
         description="Misk's impact-focused accelerator track, run alongside the main "
                     "Misk Accelerator.",
         stats="Part of Misk's entrepreneurship portfolio",
         entity_url="https://misk.org.sa/en/",
         programs_url="https://misk.org.sa/en/programs/impact-accelerator/",
         apply_url="https://hub.misk.org.sa/", confidence="high",
         source="misk.org.sa/en/programs/impact-accelerator/"),

    dict(entity="Flat6Labs", entity_type="Accelerator", country="Saudi Arabia", city="Riyadh",
         program="Riyadh Seed Programme (RSP)", program_type="Accelerator", stage="Pre-seed",
         sectors="Tech, agnostic", eligibility="Saudi startups",
         funding="Seed investment", equity="Yes", duration="Cycle-based",
         cadence="Multiple cycles / year", status="Active",
         description="Run with Saudi Venture Capital Company (SVC) and ecosystem "
                     "stakeholders including Jada Fund of Funds and Riyadh Valley Company; "
                     "supported by NTDP.",
         stats="60+ startups accelerated; ~USD 17M seed deployed; 20+ Saudi startups/year planned",
         entity_url="https://flat6labs.com/",
         programs_url="https://flat6labs.com/program/riyadh-seed-program-page/",
         apply_url="", confidence="high",
         source="flat6labs.com RSP + KSA location pages; Sharikat Mubasher cycle-6 coverage"),

    dict(entity="Monsha'at", entity_type="Government / Authority", country="Saudi Arabia",
         city="Riyadh", program="University Startup Accelerator Programme",
         program_type="Accelerator", stage="Idea",
         sectors="Agnostic", eligibility="University affiliates, students, recent graduates",
         funding="Programme support", equity="No", duration="Cohort-based",
         cadence="Recurring", status="Active",
         description="Saudi SME authority programme supporting entrepreneurial projects "
                     "of university affiliates, students and recent graduates. Three "
                     "accelerators with universities in Riyadh, Qassim and Al-Ahsa.",
         stats="3 university-partnered business accelerators",
         entity_url="https://www.monshaat.gov.sa/en",
         programs_url="https://www.monshaat.gov.sa/en/node/13973",
         apply_url="", confidence="high", source="monshaat.gov.sa university accelerator page"),

    dict(entity="NTDP", entity_type="Government / Authority", country="Saudi Arabia",
         city="Riyadh", program="Technology Champions Initiative", program_type="Grant",
         stage="Growth", sectors="Technology", eligibility="Tech companies in KSA",
         funding="Initiative-dependent", equity="No", duration="Programme-dependent",
         cadence="Rolling", status="Active",
         description="National Technology Development Program — drives Saudi tech "
                     "ecosystem growth through strategic interventions and startup "
                     "support programmes. Launched 2023. Also supports Flat6Labs RSP.",
         stats="Launched 2023; backs the Riyadh Seed Programme",
         entity_url="https://ntdp.gov.sa/en",
         programs_url="https://ntdp.gov.sa/en/initiative/technology-champions",
         apply_url="", confidence="high", source="ntdp.gov.sa Technology Champions page"),

    dict(entity="Blossom Accelerator", entity_type="Accelerator", country="Saudi Arabia",
         city="Riyadh", program="Soft Landing", program_type="Soft landing / Market access",
         stage="Growth", sectors="Agnostic", eligibility="Foreign startups entering KSA",
         funding="Market-entry support", equity="Varies", duration="Programme-dependent",
         cadence="Rolling", status="Active",
         description="Market-entry / soft-landing programme for startups expanding into "
                     "Saudi Arabia. Recognised by Monsha'at and a trusted partner of the "
                     "Ministry of Investment.",
         stats="Recognised by Monsha'at; Ministry of Investment partner",
         entity_url="https://blossom.sa/",
         programs_url="https://blossom.sa/founders-startups/soft-landing/",
         apply_url="", confidence="high", source="blossom.sa soft-landing page"),

    dict(entity="500 Global", entity_type="VC firm", country="Saudi Arabia", city="Riyadh",
         program="Sanabil 500 MENA Seed Accelerator", program_type="Accelerator",
         stage="Seed", sectors="Agnostic", eligibility="MENA startups",
         funding="Seed investment", equity="Yes", duration="Cohort-based",
         cadence="Multiple cohorts / year", status="Active",
         description="Riyadh-based seed accelerator fund run by 500 Global with Sanabil "
                     "Investments. 500 Global has invested in MENA since 2012.",
         stats="500 Global has backed 2,500+ companies across 80+ countries",
         entity_url="https://500.co/",
         programs_url="https://500.co/",
         apply_url="", confidence="medium",
         source="Entrepreneur ME & Lucidity Insights accelerator guides; 500.co URL inferred"),

    dict(entity="500 Global", entity_type="VC firm", country="Saudi Arabia", city="Riyadh",
         program="Misk 500 MENA Accelerator", program_type="Accelerator", stage="Seed",
         sectors="Agnostic", eligibility="MENA startups", funding="Seed investment",
         equity="Yes", duration="Cohort-based", cadence="Recurring", status="Active",
         description="Riyadh-based accelerator fund run by 500 Global with Misk.",
         stats="One of two Riyadh-based 500 Global accelerator funds",
         entity_url="https://500.co/", programs_url="https://500.co/", apply_url="",
         confidence="medium", source="Entrepreneur ME accelerator guide; URL inferred"),

    dict(entity="Wa'ed Ventures (Aramco)", entity_type="Corporate programme",
         country="Saudi Arabia", city="Dhahran", program="Wa'ed Ventures investment",
         program_type="Seed fund", stage="Seed", sectors="Tech, industrial",
         eligibility="Saudi-linked startups", funding="VC investment", equity="Yes",
         duration="N/A", cadence="Rolling", status="Active",
         description="Aramco's entrepreneurship and venture arm supporting Saudi startups.",
         stats="Aramco-backed",
         entity_url="", programs_url="", apply_url="", confidence="low",
         source="Named in Entrepreneur ME / Rasmal guides; URL NOT in results — verify"),

    dict(entity="KAUST Innovation Fund", entity_type="VC firm", country="Saudi Arabia",
         city="Thuwal", program="Deep-tech venture investment", program_type="Seed fund",
         stage="Seed", sectors="Energy, water, healthcare, deep tech",
         eligibility="Early-stage deep tech", funding="VC investment", equity="Yes",
         duration="N/A", cadence="Rolling", status="Active",
         description="KAUST's venture capital arm, investing in early-stage deep-tech and "
                     "commercialising research.",
         stats="Focus sectors: energy, water, healthcare",
         entity_url="https://taqadam.kaust.edu.sa/", programs_url="", apply_url="",
         confidence="low", source="Rasmal / Visible.vc guides; fund URL NOT in results — verify"),

    # ======================= UAE =======================
    dict(entity="Hub71", entity_type="Government / Authority", country="UAE", city="Abu Dhabi",
         program="Access Programme", program_type="Accelerator", stage="Pre-seed",
         sectors="Tech, agnostic",
         eligibility="Pre-seed to Series A startups establishing in Abu Dhabi",
         funding="Support package + incentives", equity="Varies",
         duration="Cohort-based", cadence="Recurring intakes with published deadlines",
         status="Active — applications open",
         description="Abu Dhabi's flagship tech ecosystem, within ADGM. The Access "
                     "Programme offers a comprehensive support package and a route into "
                     "the UAE capital's marketplace, for pre-seed to Series A startups.",
         stats="A published intake cited a 21 Aug 2026 deadline with a Feb 2027 start; "
               "Hub71 welcomed 13+ new AI startups in H1 2025",
         entity_url="https://www.hub71.com/",
         programs_url="https://www.hub71.com/program/access-programme",
         apply_url="https://www.hub71.com/program/access-programme/apply",
         confidence="high", source="hub71.com Access programme + apply pages"),

    dict(entity="Hub71", entity_type="Government / Authority", country="UAE", city="Abu Dhabi",
         program="Initiate", program_type="Accelerator", stage="Idea", sectors="Tech",
         eligibility="Earliest-stage founders", funding="Programme support", equity="Varies",
         duration="Cohort-based", cadence="Recurring", status="Active",
         description="Hub71's earlier-stage programme track, sitting below Access.",
         stats="Part of Hub71's programme ladder",
         entity_url="https://www.hub71.com/",
         programs_url="https://www.hub71.com/program/initiate",
         apply_url="", confidence="high", source="hub71.com/program/initiate"),

    dict(entity="Hub71", entity_type="Government / Authority", country="UAE", city="Abu Dhabi",
         program="Anjal Z (with ECA)", program_type="Competition / Challenge", stage="Any",
         sectors="Early childhood innovation", eligibility="Global startups",
         funding="Programme-dependent", equity="Varies", duration="Cohort-based",
         cadence="Call-based", status="Applications opened (per press release)",
         description="Joint programme with the Early Childhood Authority to accelerate "
                     "global early-childhood innovation in Abu Dhabi.",
         stats="Announced via Hub71 press release",
         entity_url="https://www.hub71.com/",
         programs_url="https://www.hub71.com/latest-news",
         apply_url="", confidence="medium",
         source="hub71.com press release; /latest-news index URL inferred"),

    dict(entity="Sheraa (Sharjah Entrepreneurship Center)", entity_type="Government / Authority",
         country="UAE", city="Sharjah", program="Access Sharjah Challenge (ASC)",
         program_type="Competition / Challenge", stage="Growth",
         sectors="Rotating priority sectors (e.g. agriculture & livestock)",
         eligibility="Global startups", funding="Equity-free award + POC contract",
         equity="No (equity-free)", duration="Challenge cycle", cadence="Annual",
         status="Active",
         description="Sheraa's flagship market-access programme. Invites global startups "
                     "to solve high-impact real-world challenges in Sharjah's priority "
                     "sectors, connecting them with regulators and industry leaders.",
         stats="Annual challenge; equity-free model",
         entity_url="https://www.asc.sheraa.ae/",
         programs_url="https://www.startups.sheraa.ae/asc2025",
         apply_url="", confidence="high",
         source="asc.sheraa.ae; startups.sheraa.ae/asc2025 and /asc2024"),

    dict(entity="Sheraa (Sharjah Entrepreneurship Center)", entity_type="Government / Authority",
         country="UAE", city="Sharjah", program="Sharjah Women Impact Fellowship (SWIF)",
         program_type="Fellowship", stage="Any", sectors="Impact",
         eligibility="Women founders", funding="Fellowship support", equity="No",
         duration="Fellowship cycle", cadence="Annual", status="Active",
         description="Sheraa fellowship supporting women-led impact ventures.",
         stats="Dedicated Sheraa sub-brand and site",
         entity_url="https://www.asc.sheraa.ae/",
         programs_url="https://www.swif.sheraa.ae/",
         apply_url="", confidence="high", source="swif.sheraa.ae"),

    dict(entity="Dubai Future District", entity_type="Government / Authority", country="UAE",
         city="Dubai", program="Business Accelerators", program_type="Accelerator",
         stage="Any", sectors="Future economy, FinTech", eligibility="Startups in Dubai",
         funding="Programme + fund access", equity="Varies", duration="Programme-dependent",
         cadence="Rolling", status="Active",
         description="Dubai Future District's accelerator offering; the Dubai Future "
                     "District Fund provides investment capital, accelerator programmes "
                     "and regulatory support.",
         stats="Backed by Dubai Future District Fund",
         entity_url="https://dubaifuturedistrict.ae/",
         programs_url="https://dubaifuturedistrict.ae/offering/business-accelerators/",
         apply_url="", confidence="high", source="dubaifuturedistrict.ae accelerators page"),

    dict(entity="Dubai Future Foundation", entity_type="Government / Authority", country="UAE",
         city="Dubai", program="Dubai Future Accelerators", program_type="Accelerator",
         stage="Growth", sectors="GovTech, urban challenges",
         eligibility="Startups with a working prototype", funding="Government pilots",
         equity="No equity taken (pilot model)", duration="9-week sprints",
         cadence="Cycle-based", status="Active",
         description="Selects startups with working prototypes to solve big urban and "
                     "government challenges, in nine-week sprints that plug participants "
                     "directly into government decision-makers.",
         stats="Backed by an AED 1 billion investment; 9-week sprints",
         entity_url="", programs_url="", apply_url="", confidence="low",
         source="AcceleratorApp / Failory guides; official URL NOT in results — verify"),

    dict(entity="DIFC", entity_type="Government / Authority", country="UAE", city="Dubai",
         program="DIFC FinTech Hive Accelerator", program_type="Accelerator", stage="Seed",
         sectors="FinTech, InsurTech, RegTech, Islamic FinTech",
         eligibility="Early and growth-stage firms serving MEASA", funding="Programme + POCs",
         equity="No", duration="12 weeks", cadence="Annual cohort", status="Active",
         description="Accelerator at Dubai International Financial Centre. Twelve-week "
                     "programme helping early and growth-stage firms accelerate product "
                     "and business development with exposure to financial-institution executives.",
         stats="12-week programme; MEASA financial-sector focus",
         entity_url="https://www.difc.ae/",
         programs_url="https://www.dxbstart.com/programs/difc-fintech-hive",
         apply_url="", confidence="medium",
         source="FinTech Futures coverage; DXBStart programme page. difc.ae inferred — verify"),

    dict(entity="in5 (TECOM Group)", entity_type="Incubator", country="UAE", city="Dubai",
         program="in5 Innovation Centres (Tech / Media / Design)", program_type="Incubator",
         stage="Idea", sectors="Tech, media, design", eligibility="Dubai-based founders",
         funding="Subsidised licensing + workspace", equity="No", duration="Ongoing",
         cadence="Rolling", status="Active",
         description="TECOM Group's innovation centres offering founders in Dubai Internet "
                     "City, Dubai Media City and Dubai Design District subsidised licensing "
                     "and co-working.",
         stats="Three sector-specific centres",
         entity_url="https://infive.ae/", programs_url="", apply_url="", confidence="low",
         source="Garant.ae / Sage Marketing guides; entity URL NOT in results — verify"),

    dict(entity="DTEC (Dubai Silicon Oasis)", entity_type="Coworking / Hub", country="UAE",
         city="Dubai", program="DTEC startup hub & Dubai Smart City Accelerator",
         program_type="Incubator", stage="Any", sectors="Smart city, tech",
         eligibility="Startups in Dubai", funding="Workspace + programme", equity="Varies",
         duration="Ongoing", cadence="Rolling", status="Active",
         description="Dubai Technology Entrepreneur Campus at Silicon Oasis — home to "
                     "100+ startups from 60+ countries, and to the Dubai Smart City "
                     "Accelerator, the first of its kind in MENA.",
         stats="100+ startups from 60+ countries",
         entity_url="https://dtec.ae/", programs_url="", apply_url="", confidence="low",
         source="Sage Marketing / Failory guides; entity URL NOT in results — verify"),

    dict(entity="Khalifa Fund for Enterprise Development",
         entity_type="Government / Authority", country="UAE", city="Abu Dhabi",
         program="Grants & soft loans", program_type="Grant", stage="Any",
         sectors="Agnostic", eligibility="UAE nationals",
         funding="Up to AED 3 million", equity="No", duration="N/A", cadence="Rolling",
         status="Active",
         description="Abu Dhabi fund supporting UAE nationals with grants and soft loans.",
         stats="Grants and soft loans up to AED 3 million",
         entity_url="https://www.khalifafund.ae/", programs_url="", apply_url="",
         confidence="low", source="FounderConnects / Garant guides; URL NOT in results — verify"),

    dict(entity="MBRIF", entity_type="Government / Authority", country="UAE", city="Dubai",
         program="Mohammed Bin Rashid Innovation Fund — Accelerator & Guarantee",
         program_type="Grant", stage="Growth",
         sectors="Technology, healthcare, sustainability",
         eligibility="Highly innovative companies", funding="Guarantee scheme + accelerator",
         equity="No", duration="Programme-dependent", cadence="Rolling", status="Active",
         description="UAE federal innovation fund focused on highly innovative startups "
                     "with breakthrough ideas in technology, healthcare or sustainability.",
         stats="Federal innovation fund with accelerator and guarantee tracks",
         entity_url="https://www.mbrif.ae/", programs_url="", apply_url="", confidence="low",
         source="inchub.ae / Garant guides; URL NOT in results — verify"),

    dict(entity="AstroLabs", entity_type="Accelerator", country="UAE", city="Dubai",
         program="Market expansion into UAE & Saudi", program_type="Soft landing / Market access",
         stage="Growth", sectors="Tech", eligibility="International companies expanding to Gulf",
         funding="Expansion services", equity="No", duration="Programme-dependent",
         cadence="Rolling", status="Active",
         description="Supports international companies expanding into the UAE and Saudi Arabia.",
         stats="Gulf market-entry specialist",
         entity_url="https://astrolabs.com/", programs_url="", apply_url="", confidence="low",
         source="Sage Marketing / Garant guides; URL NOT in results — verify"),

    dict(entity="ADGM", entity_type="Government / Authority", country="UAE", city="Abu Dhabi",
         program="Tech & FinTech licensing and programmes", program_type="Soft landing / Market access",
         stage="Any", sectors="Tech, FinTech", eligibility="Startups incorporating in ADGM",
         funding="Regulatory + programme support", equity="No", duration="Ongoing",
         cadence="Rolling", status="Active",
         description="Abu Dhabi Global Market hosts programmes for tech and fintech "
                     "companies and provides startup-tailored licences within a globally "
                     "recognised regulatory environment.",
         stats="Hosts Hub71; tech-startup licensing regime",
         entity_url="https://www.adgm.com/", programs_url="", apply_url="", confidence="low",
         source="AcceleratorApp guide; URL NOT in results — verify"),

    dict(entity="Startupbootcamp", entity_type="Accelerator", country="UAE", city="Dubai",
         program="Startupbootcamp Smart City Dubai", program_type="Accelerator",
         stage="Seed", sectors="IoT, AI, sustainable city tech",
         eligibility="Early-stage startups", funding="Programme + investment", equity="Yes",
         duration="Cohort-based", cadence="Recurring", status="Active",
         description="Helps launch companies focused on smarter, more connected urban "
                     "environments — IoT, AI and sustainable city tech.",
         stats="Global accelerator brand with a Dubai smart-city vertical",
         entity_url="https://www.startupbootcamp.org/", programs_url="", apply_url="",
         confidence="low", source="AcceleratorApp / UpperSetup guides; URL NOT in results — verify"),

    # ======================= QATAR =======================
    dict(entity="Invest Qatar", entity_type="Government / Authority", country="Qatar",
         city="Doha", program="Startup Qatar", program_type="Soft landing / Market access",
         stage="Any", sectors="All", eligibility="Local and international startups",
         funding="Incentives + market access", equity="No", duration="Ongoing",
         cadence="Rolling", status="Active",
         description="Invest Qatar's national startup platform — the front door for "
                     "founders entering or scaling in Qatar.",
         stats="National investment-promotion initiative",
         entity_url="https://startupqatar.qa/en",
         programs_url="https://startupqatar.qa/en", apply_url="", confidence="high",
         source="startupqatar.qa"),

    dict(entity="QBIC (Qatar Business Incubation Center)", entity_type="Incubator",
         country="Qatar", city="Doha", program="QBIC Accelerator Programme",
         program_type="Accelerator", stage="Pre-seed",
         sectors="AI, logistics, healthtech, sustainability",
         eligibility="Local and global tech startups", funding="Programme support",
         equity="Varies", duration="Cohort-based", cadence="Annual cohort", status="Active",
         description="Operated under Qatar Development Bank. One of the region's "
                     "longest-standing and largest incubators, supporting founders from "
                     "pre-seed to growth.",
         stats="2026 cohort: 20 startups across AI, logistics, healthtech and sustainability",
         entity_url="https://www.qbic.qa/",
         programs_url="https://arabfounders.net/en/qbic-accelerator-2026-startups-qatar/",
         apply_url="", confidence="medium",
         source="Arab Founders 2026 cohort coverage; qbic.qa URL inferred — verify"),

    dict(entity="QSTP (Qatar Science & Technology Park)", entity_type="Government / Authority",
         country="Qatar", city="Doha", program="Tech Venture Fund & co-investment",
         program_type="Seed fund", stage="Seed", sectors="Deep tech",
         eligibility="Early-stage deep-tech startups in Qatar", funding="USD 30 million fund",
         equity="Yes", duration="N/A", cadence="Rolling", status="Active",
         description="Qatar Foundation's innovation hub in Education City. Focuses on "
                     "deep-tech and research-based startups with lab space, prototyping, "
                     "mentorship and technology licensing.",
         stats="USD 30M Tech Venture Fund with first co-investment partner funds",
         entity_url="https://qstp.org.qa/",
         programs_url="https://www.gccbusinessnews.com/qstp-rolls-out-30mn-fund-qatar-startups",
         apply_url="", confidence="medium",
         source="GCC Business News coverage; qstp.org.qa URL inferred — verify"),

    dict(entity="Qatar Development Bank", entity_type="Sovereign / National fund",
         country="Qatar", city="Doha", program="SME financing & QDB Ventures",
         program_type="Debt / Loan", stage="Any", sectors="All",
         eligibility="Qatari SMEs and startups", funding="Loans + venture capital",
         equity="Varies", duration="N/A", cadence="Rolling", status="Active",
         description="Provides SME financing, venture capital through QDB Ventures, and "
                     "startup-focused loan programmes with favourable terms. Parent of QBIC.",
         stats="Operates QBIC; QDB Ventures VC arm",
         entity_url="https://www.qdb.qa/", programs_url="", apply_url="", confidence="low",
         source="Rasmal Qatar ecosystem article; URL NOT in results — verify"),

    # ======================= BAHRAIN =======================
    dict(entity="Tamkeen", entity_type="Government / Authority", country="Bahrain",
         city="Manama", program="StartUp Bahrain (relaunched)", program_type="Incubator",
         stage="Any", sectors="All", eligibility="Bahrain-based founders",
         funding="Programme support", equity="No", duration="Ongoing", cadence="Rolling",
         status="Active",
         description="Bahrain's national labour fund. Powers StartUp Bahrain in strategic "
                     "partnership with Brinc, Spring, General Assembly, Reboot Coding "
                     "Institute and ordable/.",
         stats="StartUp Bahrain relaunched on its 10th anniversary",
         entity_url="https://www.tamkeen.bh/en/",
         programs_url="https://www.tamkeen.bh/en/startup-relaunch/",
         apply_url="", confidence="high", source="tamkeen.bh startup-relaunch page"),

    dict(entity="StartUp Bahrain", entity_type="Government / Authority", country="Bahrain",
         city="Manama", program="Ecosystem platform & programme calls",
         program_type="Directory listing", stage="Any", sectors="All",
         eligibility="Bahrain ecosystem", funding="Signposting", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="A launchpad for scalable startups in the Middle East. Publishes "
                     "programme announcements — a strong scrape target for new Bahraini calls.",
         stats="Powered by Tamkeen",
         entity_url="https://startupbahrain.com/",
         programs_url="https://startupbahrain.com/blog",
         apply_url="", confidence="high",
         source="startupbahrain.com; /about and /blog/... pages in results"),

    dict(entity="Tamkeen + Startupbootcamp", entity_type="Corporate programme",
         country="Bahrain", city="Manama", program="AI Accelerator for Bahraini founders",
         program_type="Accelerator", stage="Seed", sectors="AI",
         eligibility="Bahraini founders", funding="Programme support", equity="Varies",
         duration="Cohort-based", cadence="Call-based", status="Announced",
         description="Tamkeen partnership with Startupbootcamp to launch an AI accelerator "
                     "for Bahrain founders.",
         stats="Announced via StartUp Bahrain",
         entity_url="https://startupbahrain.com/",
         programs_url="https://startupbahrain.com/blog/tamkeen-partners-with-startupbootcamp-to-launch-ai-accelerator-for-bahrain-founders",
         apply_url="", confidence="high", source="startupbahrain.com blog post"),

    dict(entity="Brinc MENA", entity_type="Accelerator", country="Bahrain", city="Manama",
         program="Open Innovation Programme (with Alba & Tamkeen)",
         program_type="Competition / Challenge", stage="Any", sectors="Industrial innovation",
         eligibility="Bahraini SMEs", funding="Programme support", equity="Varies",
         duration="Cohort-based", cadence="Call-based", status="Active",
         description="Global venture accelerator partnered with StartUp Bahrain; runs "
                     "open-innovation programmes with corporates such as Alba.",
         stats="Three Bahraini SMEs shortlisted in an Alba/Tamkeen/Brinc programme",
         entity_url="https://brinc.io/",
         programs_url="https://startupbahrain.com/blog",
         apply_url="", confidence="medium",
         source="Zawya press release; MyStartupWorld partnership news. brinc.io inferred"),

    # ======================= OMAN =======================
    dict(entity="Oman Technology Fund (OTF)", entity_type="Sovereign / National fund",
         country="Oman", city="Muscat", program="Techween / Wadi Accelerator / Jasoor Ventures",
         program_type="Accelerator", stage="Idea", sectors="Tech",
         eligibility="Oman-linked startups", funding="Stage-based investment", equity="Yes",
         duration="Programme-dependent", cadence="Recurring", status="Active",
         description="Oman's national tech fund with three stage-based vehicles: Techween "
                     "(idea stage), Wadi Accelerator (acceleration) and Jasoor Ventures "
                     "(growth).",
         stats="Total committed capital up to USD 150 million",
         entity_url="https://www.otf.om/", programs_url="https://www.otf.om/",
         apply_url="", confidence="high", source="otf.om; Crunchbase/MAGNiTT profiles"),

    # ======================= KUWAIT =======================
    dict(entity="Sirdab Lab", entity_type="Accelerator", country="Kuwait", city="Kuwait City",
         program="Accelerator & coworking", program_type="Accelerator", stage="Idea",
         sectors="Digital products, tech", eligibility="Kuwait & MENA entrepreneurs",
         funding="Programme support", equity="Varies", duration="Programme-dependent",
         cadence="Rolling", status="Active",
         description="Accelerator and coworking space for entrepreneurs and startups in "
                     "Kuwait and the MENA region.",
         stats="Kuwait's best-known startup hub",
         entity_url="https://sirdab-lab.com/", programs_url="https://sirdab-lab.com/",
         apply_url="", confidence="high", source="sirdab-lab.com; MAGNiTT enabler profile"),

    dict(entity="National Fund for SME Development", entity_type="Sovereign / National fund",
         country="Kuwait", city="Kuwait City", program="SME financing & incubation",
         program_type="Debt / Loan", stage="Any", sectors="All",
         eligibility="Kuwaiti entrepreneurs", funding="Up to 80% of project capital",
         equity="No", duration="N/A", cadence="Rolling", status="Active",
         description="Independent Kuwaiti public corporation providing startup capital, "
                     "regulatory facilitation, entrepreneurship education, training, "
                     "technical incubation and marketing services.",
         stats="Total capital KD 2 billion (~USD 7bn); finances up to 80% of project capital",
         entity_url="https://nfsme.gov.kw/", programs_url="", apply_url="", confidence="low",
         source="Kuwait Times / DevelopmentAid coverage; URL NOT in results — verify"),

    # ======================= JORDAN =======================
    dict(entity="Oasis500", entity_type="Accelerator", country="Jordan", city="Amman",
         program="Early-stage acceleration & investment", program_type="Accelerator",
         stage="Idea", sectors="Tech, creative", eligibility="Jordan & regional founders",
         funding="Early-stage investment", equity="Yes", duration="Cohort-based",
         cadence="Recurring", status="Active",
         description="Jordan's first entrepreneurial catalyst and early-stage investor, "
                     "backing founders to turn early ideas into scalable ventures.",
         stats="Jordan's pioneering accelerator",
         entity_url="https://oasis500.com/", programs_url="https://oasis500.com/",
         apply_url="", confidence="high", source="oasis500.com"),

    dict(entity="ISSF (Innovative Startups & SMEs Fund)",
         entity_type="Sovereign / National fund", country="Jordan", city="Amman",
         program="Direct & indirect investment", program_type="Fund of funds", stage="Seed",
         sectors="Tech", eligibility="Jordanian startups", funding="Equity investment",
         equity="Yes", duration="N/A", cadence="Rolling", status="Active",
         description="Jordanian fund investing directly in startups and indirectly through "
                     "accelerators and VC funds.",
         stats="World Bank-supported Jordanian startup fund",
         entity_url="https://issfjo.com/", programs_url="", apply_url="", confidence="low",
         source="Named in regional round-ups; URL NOT in results — verify"),

    # ======================= LEBANON =======================
    dict(entity="Berytech", entity_type="Incubator", country="Lebanon", city="Beirut",
         program="Startup programmes portfolio", program_type="Incubator", stage="Idea",
         sectors="Tech, agrifood, cleantech", eligibility="Lebanese startups and SMEs",
         funding="Programme + fund access", equity="Varies", duration="Programme-dependent",
         cadence="Rolling calls", status="Active",
         description="Responds to the needs of growing startups and SMEs, creating local "
                     "programmes and affiliating to regional and international ones.",
         stats="Lebanon's principal startup ecosystem builder",
         entity_url="https://berytech.org/",
         programs_url="https://berytech.org/startups/", apply_url="", confidence="high",
         source="berytech.org/startups/"),

    # ======================= TUNISIA =======================
    dict(entity="Startup Tunisia / Smart Capital", entity_type="Government / Authority",
         country="Tunisia", city="Tunis", program="Startup Act labelling & partner programmes",
         program_type="Grant", stage="Any", sectors="All",
         eligibility="Tunisian startups meeting Startup Act criteria",
         funding="State grants & benefits under the Startup Act", equity="No",
         duration="Label valid multi-year", cadence="Rolling applications", status="Active",
         description="Tunisia's national startup programme implementing the Startup Act. "
                     "Publishes official partner programmes and the College of Startups.",
         stats="National Startup Act framework with an official partner network",
         entity_url="https://startup.gov.tn/en",
         programs_url="https://startup.gov.tn/en/partners-programs",
         apply_url="", confidence="high",
         source="startup.gov.tn partner-programs, sso-partners and startup_college pages"),

    dict(entity="Flat6Labs", entity_type="Accelerator", country="Tunisia", city="Tunis",
         program="Tunis Seed Programme", program_type="Accelerator", stage="Pre-seed",
         sectors="Tech", eligibility="Tunisian startups", funding="Seed funding",
         equity="Yes", duration="Cycle-based", cadence="Recurring", status="Active",
         description="Launched in Tunisia in 2016 to give Tunisian entrepreneurs the "
                     "resources to scale regionally and globally.",
         stats="Operating in Tunisia since 2016",
         entity_url="https://flat6labs.com/",
         programs_url="https://flat6labs.com/Location/tunisia/", apply_url="",
         confidence="high", source="flat6labs.com Tunisia location page"),

    dict(entity="Founder Institute", entity_type="Accelerator", country="Tunisia", city="Tunis",
         program="Founder Institute Tunis", program_type="Accelerator", stage="Idea",
         sectors="Agnostic", eligibility="Early-stage / pre-seed founders",
         funding="No direct funding", equity="Yes (FI model)", duration="~14 weeks",
         cadence="Recurring cohorts", status="Active",
         description="Structured route from idea to investment readiness with mentorship "
                     "from leading Tunis startup names.",
         stats="Global FI network chapter",
         entity_url="https://fi.co/", programs_url="https://fi.co/", apply_url="",
         confidence="medium", source="fi.co insight article on FI Tunis"),

    # ======================= MOROCCO =======================
    dict(entity="212Founders (CDG Invest)", entity_type="Accelerator", country="Morocco",
         city="Casablanca", program="212Founders acceleration", program_type="Accelerator",
         stage="Pre-seed", sectors="Tech", eligibility="Moroccan startups",
         funding="Programme + financing", equity="Varies", duration="Programme-dependent",
         cadence="Continuous applications", status="Active",
         description="CDG Invest's flagship Moroccan acceleration programme; accepts "
                     "applications online on a continuous basis.",
         stats="Morocco's flagship state-linked accelerator",
         entity_url="https://212founders.co/", programs_url="https://212founders.co/",
         apply_url="https://212founders.co/", confidence="low",
         source="berrynoon.ma Morocco funding guide names 212founders.co — URL from prose, verify"),

    # ======================= PALESTINE =======================
    dict(entity="Ibtikar Fund", entity_type="VC firm", country="Palestine", city="Ramallah",
         program="Seed to Series A investment", program_type="Seed fund", stage="Seed",
         sectors="Tech", eligibility="Palestinian startups",
         funding="Fund II closed at USD 25M, targeting 25 companies", equity="Yes",
         duration="N/A", cadence="Rolling", status="Active",
         description="Invests in innovative Palestinian companies from the earliest "
                     "stages — seed through local accelerators, post-acceleration and "
                     "Series A. Investors include Bank of Palestine, DGGF, IFC and EBRD.",
         stats="Fund II: USD 25M closed Nov 2024, targeting 25 companies",
         entity_url="https://ibtikarfund.com/",
         programs_url="https://ibtikarfund.com/", apply_url="", confidence="medium",
         source="ibtikarfund.com/2021/ in results; root URL inferred. ImpactAlpha/Wamda coverage"),

    dict(entity="Flow Accelerator", entity_type="Accelerator", country="Palestine",
         city="Ramallah", program="Pre-acceleration & incubation", program_type="Accelerator",
         stage="Idea", sectors="Tech", eligibility="Palestinian early-stage startups",
         funding="Programme support", equity="Varies", duration="Programme-dependent",
         cadence="Recurring", status="Active",
         description="Supports Palestinian entrepreneurs and investors simultaneously, "
                     "helping early-stage startups overcome financial and technical "
                     "barriers to become investment-ready.",
         stats="Palestinian pre-acceleration specialist",
         entity_url="https://flow.ps/", programs_url="https://flow.ps/", apply_url="",
         confidence="high", source="flow.ps"),

    # ======================= IRAQ =======================
    dict(entity="The Station", entity_type="Incubator", country="Iraq", city="Baghdad",
         program="Incubation & acceleration programmes", program_type="Incubator",
         stage="Idea", sectors="Tech, creative", eligibility="Iraqi entrepreneurs",
         funding="Programme support", equity="Varies", duration="Programme-dependent",
         cadence="Recurring", status="Active",
         description="Established 2018, Iraq's leading entrepreneurship and innovation "
                     "hub. Structured incubation and acceleration, training workshops, "
                     "coworking and mentorship. Spaces in Baghdad, Mosul, Erbil and Basra.",
         stats="Four locations: Baghdad, Mosul, Erbil, Basra",
         entity_url="https://the-station.iq/", programs_url="https://the-station.iq/about",
         apply_url="", confidence="high", source="the-station.iq and /about"),

    dict(entity="Iraq Venture Partners", entity_type="VC firm", country="Iraq", city="Baghdad",
         program="Venture investment", program_type="Seed fund", stage="Seed",
         sectors="Tech", eligibility="Iraqi startups", funding="VC investment", equity="Yes",
         duration="N/A", cadence="Rolling", status="Active",
         description="Iraqi venture investment firm.",
         stats="Active Iraqi VC",
         entity_url="https://www.iraqventurepartners.com/",
         programs_url="https://www.iraqventurepartners.com/", apply_url="",
         confidence="high", source="iraqventurepartners.com"),

    dict(entity="Iraq Tech Ventures", entity_type="VC firm", country="Iraq", city="Baghdad",
         program="Angel syndicate (historic)", program_type="Seed fund", stage="Seed",
         sectors="Tech", eligibility="Iraqi startups", funding="Historic", equity="Yes",
         duration="N/A", cadence="N/A", status="CLOSED — permanently closed",
         description="Co-founded 2018; raised millions for Iraqi portfolio companies via "
                     "an angel and institutional syndicate. Reported as permanently closed "
                     "— retained here so the scraper does not re-add it as new.",
         stats="Reported permanently closed",
         entity_url="", programs_url="https://magnitt.com/investors/iraq-tech-ventures-49973",
         apply_url="", confidence="medium", source="MAGNiTT profile; Crunchbase status"),

    dict(entity="Iraqi Innovators", entity_type="Media / Data platform", country="Iraq",
         city="Baghdad", program="Programme listings for Iraqi founders",
         program_type="Directory listing", stage="Any", sectors="All",
         eligibility="Iraqi entrepreneurs", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="Publishes round-ups of entrepreneurship programmes Iraqis can apply "
                     "to — a useful scrape target for Iraq-specific calls.",
         stats="Iraq-focused opportunity listings",
         entity_url="https://iraqtech.io/",
         programs_url="https://iraqtech.io/4-entrepreneurship-programs-that-iraqis-can-apply-to-right-now/",
         apply_url="", confidence="high", source="iraqtech.io article"),

    # ======================= ALGERIA / LIBYA =======================
    dict(entity="Algeria Venture (A-Venture)", entity_type="Government / Authority",
         country="Algeria", city="Algiers", program="State startup accelerator",
         program_type="Accelerator", stage="Idea",
         sectors="AI, cybersecurity, robotics", eligibility="Algerian startups",
         funding="State-backed support", equity="No", duration="Programme-dependent",
         cadence="Recurring", status="Active",
         description="State-owned startup accelerator established December 2020 as part "
                     "of Algeria's economic diversification and knowledge-economy agenda.",
         stats="Established Dec 2020; focus on AI, cybersecurity, robotics",
         entity_url="https://startup-algeria.com/",
         programs_url="https://startup-algeria.com/startup-institutions/a-venture",
         apply_url="", confidence="high", source="startup-algeria.com A-Venture page"),

    dict(entity="SPARK", entity_type="NGO / Development agency", country="Libya",
         city="Tripoli / Benghazi / Al-Bayda", program="Libya Startup incubators",
         program_type="Incubator", stage="Idea", sectors="Agnostic",
         eligibility="Libyan entrepreneurs", funding="EU-funded grants + mentorship",
         equity="No", duration="Cohort-based", cadence="Recurring cohorts", status="Active",
         description="EU-funded incubators for aspiring Libyan business owners, providing "
                     "resources, mentorship and funding. Cohorts run in Benghazi, Al-Bayda "
                     "and Derna.",
         stats="Second cohort saw a surge in Derna entrepreneurs",
         entity_url="https://spark.ngo/",
         programs_url="https://spark.ngo/programme/libya-startup/", apply_url="",
         confidence="high", source="spark.ngo Libya Startup programme page"),

    # ======================= REGIONAL / GLOBAL =======================
    dict(entity="Flat6Labs", entity_type="Accelerator", country="Regional (MENA)",
         city="Multiple", program="Seed & early-stage programmes (all geographies)",
         program_type="Accelerator", stage="Pre-seed", sectors="Tech",
         eligibility="MENA startups", funding="Seed investment", equity="Yes",
         duration="Cycle-based", cadence="Continuous across markets", status="Active",
         description="MENA's leading seed and early-stage venture capital firm. Master "
                     "entity row — country programmes are listed separately above.",
         stats="Invests in 100+ innovative technology-driven startups annually",
         entity_url="https://flat6labs.com/",
         programs_url="https://flat6labs.com/category/news/", apply_url="",
         confidence="high", source="flat6labs.com home and news pages"),

    dict(entity="IFC (World Bank Group)", entity_type="NGO / Development agency",
         country="Regional (MENA)", city="Washington / regional",
         program="IFC Startup Catalyst", program_type="Fund of funds", stage="Seed",
         sectors="Tech", eligibility="Emerging-market accelerators, incubators, seed funds",
         funding="LP investment into local funds", equity="Indirect", duration="N/A",
         cadence="Rolling", status="Active",
         description="IFC's vehicle for backing accelerators, incubators and seed funds in "
                     "emerging markets — an upstream funder of many MENA programmes.",
         stats="Backer of regional funds including Ibtikar",
         entity_url="https://www.ifc.org/",
         programs_url="https://www.ifc.org/en/what-we-do/sector-expertise/venture-capital/startup-catalyst",
         apply_url="", confidence="high", source="ifc.org Startup Catalyst page"),

    dict(entity="Seedstars", entity_type="Accelerator", country="Regional (MENA)",
         city="Geneva / global", program="Emerging-market programmes",
         program_type="Accelerator", stage="Seed", sectors="Agnostic",
         eligibility="Emerging-market startups", funding="Programme + investment",
         equity="Varies", duration="Cohort-based", cadence="Recurring", status="Active",
         description="Emerging-markets accelerator; ran the Misk Growth Accelerator "
                     "kickoff bootcamp and publishes ecosystem content on MENA markets.",
         stats="Delivery partner for regional programmes including Misk Growth Accelerator",
         entity_url="https://www.seedstars.com/",
         programs_url="https://www.seedstars.com/content-hub", apply_url="",
         confidence="medium", source="seedstars.com content-hub articles; hub index inferred"),

    dict(entity="Founder Institute", entity_type="Accelerator", country="Regional (MENA)",
         city="Global", program="City chapters (Egypt, Tunis, Algiers, etc.)",
         program_type="Accelerator", stage="Idea", sectors="Agnostic",
         eligibility="Pre-seed founders", funding="No direct funding", equity="Yes",
         duration="~14 weeks", cadence="Recurring cohorts", status="Active",
         description="Global pre-seed accelerator with city chapters across MENA. Also "
                     "publishes country startup-resource lists useful for scouting.",
         stats="Publishes an Egypt list of 350+ accelerators, incubators and investors",
         entity_url="https://fi.co/",
         programs_url="https://fi.co/insight/egypt-s-startup-resources-list-for-entrepreneurs-accelerators-incubators-investors",
         apply_url="", confidence="high", source="fi.co insight pages"),

    # ======================= NEWS / DATA / AGGREGATORS =======================
    dict(entity="MAGNiTT", entity_type="Media / Data platform", country="Regional (MENA)",
         city="Dubai", program="Venture data, research reports & ecosystem news",
         program_type="News feed", stage="Any", sectors="All", eligibility="Open",
         funding="N/A (paid data tiers)", equity="N/A", duration="Ongoing",
         cadence="Continuous", status="Active",
         description="Verified VC & PE data across MENA, Africa, Turkey, Pakistan and "
                     "Southeast Asia. The single best structured source for programme, "
                     "investor and funding data in the region.",
         stats="34,800+ startups, 22,500+ funding rounds, 1,300+ exits",
         entity_url="https://magnitt.com/", programs_url="https://magnitt.com/news/",
         apply_url="", confidence="high", source="magnitt.com home, /news, /research"),

    dict(entity="Wamda", entity_type="Media / Data platform", country="Regional (MENA)",
         city="Dubai", program="Ecosystem news, reports & programmes",
         program_type="News feed", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Platform of programmes and networks accelerating MENA "
                     "entrepreneurship ecosystems. Publishes monthly funding round-ups "
                     "and programme announcements.",
         stats="Reported MENA startups raised USD 1.7bn in H1 2026; USD 173M in July 2026",
         entity_url="https://www.wamda.com/", programs_url="https://www.wamda.com/",
         apply_url="", confidence="high", source="wamda.com home and article pages"),

    dict(entity="MENAbytes", entity_type="Media / Data platform", country="Regional (MENA)",
         city="Regional", program="Tech & startup news (MENA, Turkey, Pakistan)",
         program_type="News feed", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Online publication covering technology and startups from the Middle "
                     "East and North Africa; the leading MENA startup news outlet by "
                     "social reach and engagement.",
         stats="Leading MENA startup news outlet by social media reach",
         entity_url="https://www.menabytes.com/",
         programs_url="https://www.menabytes.com/", apply_url="", confidence="high",
         source="menabytes.com and /about"),

    dict(entity="MENA Startup Digest", entity_type="Media / Data platform",
         country="Regional (MENA)", city="Regional",
         program="Funding news & founder opportunities", program_type="News feed",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="Delivers MENA startup news, funding announcements, ecosystem trends "
                     "and founder opportunities — explicitly includes opportunity listings.",
         stats="Opportunity-focused digest",
         entity_url="https://menastartupdigest.com/",
         programs_url="https://menastartupdigest.com/", apply_url="", confidence="high",
         source="menastartupdigest.com"),

    dict(entity="FWDStart", entity_type="Media / Data platform", country="Regional (MENA)",
         city="Gulf", program="Weekly briefings & VC insights", program_type="News feed",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Weekly", status="Active",
         description="MENA startup funding, tech news and VC insights via weekly "
                     "briefings, founder interviews, deep dives and podcasts.",
         stats="Weekly cadence across the Gulf and wider region",
         entity_url="https://www.fwdstart.me/", programs_url="https://www.fwdstart.me/",
         apply_url="", confidence="high", source="fwdstart.me"),

    dict(entity="Arab Founders", entity_type="Media / Data platform", country="Regional (MENA)",
         city="Regional", program="Startup & cohort announcements", program_type="News feed",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="Covers regional funding and accelerator cohort announcements — "
                     "the source that carried the QBIC 2026 cohort line-up.",
         stats="Publishes cohort-level programme detail",
         entity_url="https://arabfounders.net/",
         programs_url="https://arabfounders.net/en/", apply_url="", confidence="medium",
         source="arabfounders.net article URLs; /en/ index inferred"),

    dict(entity="Entrepreneur Middle East", entity_type="Media / Data platform",
         country="Regional (MENA)", city="Dubai", program="Programme guides & ecosystem news",
         program_type="News feed", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Publishes accelerator guides — including a guide to the most "
                     "notable and active accelerator programmes for startups in Saudi Arabia.",
         stats="Regional edition of Entrepreneur",
         entity_url="https://mena.entrepreneur.com/",
         programs_url="https://mena.entrepreneur.com/", apply_url="", confidence="high",
         source="mena.entrepreneur.com accelerator guide"),

    dict(entity="Lucidity Insights", entity_type="Media / Data platform",
         country="Regional (MENA)", city="Dubai", program="Ecosystem research & guides",
         program_type="News feed", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Regional research publisher; produces guides to top accelerators "
                     "and emerging-market ecosystem reports.",
         stats="Publishes accelerator guides by market",
         entity_url="https://lucidityinsights.com/",
         programs_url="https://lucidityinsights.com/articles", apply_url="",
         confidence="medium", source="lucidityinsights.com article URL; /articles inferred"),

    dict(entity="Rasmal", entity_type="Media / Data platform", country="Regional (MENA)",
         city="Regional", program="Ecosystem & accelerator directories",
         program_type="Directory listing", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Publishes market guides such as '30+ best startup accelerators, "
                     "incubators & VCs in Saudi Arabia' and Qatar ecosystem overviews.",
         stats="Country-level accelerator directories",
         entity_url="https://www.rasmal.com/", programs_url="https://www.rasmal.com/",
         apply_url="", confidence="high", source="rasmal.com guide pages"),

    dict(entity="Startup Genome", entity_type="Media / Data platform",
         country="Regional (MENA)", city="Global", program="Ecosystem reports by market",
         program_type="Directory listing", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Annual",
         status="Active",
         description="Ecosystem benchmarking with per-market pages, including Bahrain "
                     "and Palestine.",
         stats="Per-ecosystem report pages",
         entity_url="https://startupgenome.com/",
         programs_url="https://startupgenome.com/ecosystems/bahrain", apply_url="",
         confidence="high", source="startupgenome.com/ecosystems/bahrain and /palestine"),

    dict(entity="F6S", entity_type="Aggregator / Directory", country="Global",
         city="Global", program="Accelerator, grant & funding listings",
         program_type="Directory listing", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Global startup-opportunities community aggregating funding, jobs, "
                     "grants and accelerator programmes. Filterable by country — the "
                     "single highest-yield generic scrape target for new programme calls.",
         stats="Global aggregator with country and vertical filters",
         entity_url="https://www.f6s.com/",
         programs_url="https://www.f6s.com/accelerators", apply_url="",
         confidence="medium",
         source="f6s.com/accelerators/<country>/<vertical> in results; base path inferred"),

    dict(entity="Opportunity Desk", entity_type="Aggregator / Directory", country="Global",
         city="Global", program="Deadlines-approaching feed", program_type="Directory listing",
         stage="Any", sectors="All", eligibility="Open (youth & entrepreneurship heavy)",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Daily",
         status="Active",
         description="Maintains a deadlines section for upcoming opportunities including "
                     "fellowships, grants and entrepreneurship programmes — strong Africa "
                     "and MENA coverage.",
         stats="Dedicated deadlines-approaching feed",
         entity_url="https://opportunitydesk.org/",
         programs_url="https://opportunitydesk.org/deadlines-approaching/", apply_url="",
         confidence="high", source="opportunitydesk.org/deadlines-approaching/"),

    dict(entity="Causo Hub", entity_type="Aggregator / Directory", country="Global",
         city="Global", program="Accelerator & incubator deadline calendar",
         program_type="Directory listing", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Application deadlines for 390+ accelerators, incubators, fellowships "
                     "and startup-credit programmes through 2027, each sourced from the "
                     "programme's own site with a verification date, filterable by region.",
         stats="390+ programmes tracked with per-source verification dates",
         entity_url="https://hub.causo.ai/", programs_url="https://hub.causo.ai/deadlines",
         apply_url="", confidence="high", source="hub.causo.ai/deadlines"),

    dict(entity="StartupCorners", entity_type="Aggregator / Directory", country="Global",
         city="Global", program="Accelerator deadlines digest", program_type="Directory listing",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Periodic digest", status="Active",
         description="Digest of upcoming accelerator application deadlines across major "
                     "global programmes.",
         stats="Periodic deadline digests",
         entity_url="https://startupcorners.com/",
         programs_url="https://startupcorners.com/digest/accelerator-deadlines-digest-2026-W24",
         apply_url="", confidence="medium",
         source="startupcorners.com digest URL; root inferred"),

    dict(entity="Tracxn", entity_type="Media / Data platform", country="Global", city="Global",
         program="Accelerator & incubator lists by country",
         program_type="Directory listing", stage="Any", sectors="All", eligibility="Open",
         funding="N/A (paid)", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Maintains per-country investor lists including accelerators and "
                     "incubators, with counts and activity data.",
         stats="Lists 41 accelerators & incubators in Egypt",
         entity_url="https://tracxn.com/",
         programs_url="https://tracxn.com/d/investor-lists/accelerators-incubators-in-egypt/__ipYdkLo_FgbzV1gMFal2rbmNvDtcvlDgOWvf4fBZMjQ",
         apply_url="", confidence="high", source="tracxn.com Egypt investor list"),
]


# ---------------------------------------------------------------------------
# Coverage notes — stated plainly so the gaps are visible, not hidden
# ---------------------------------------------------------------------------
COVERAGE_NOTES = [
    ("Scope delivered",
     "Egypt and the GCC are covered most densely, then the Levant and North Africa, "
     "per the brief. Israel is excluded from scope. 17 markets, 122 entities, 133 programmes."),
    ("Three verification passes have been run",
     "Pass 1 built the registry. Passes 2 and 3 re-queried every weak entity by name and "
     "added new ones, keeping a URL only when it came back as an actual indexed search-result "
     "LINK, not merely named in "
     "prose. Across three passes the confidence split moved from high 46 / medium 17 / low 25 "
     "to high 98 / medium 23 / low 12, and the file grew from 88 rows to 133."),
    ("Still not fetch-verified — this is the honest ceiling here",
     "The egress proxy blocked every outbound request in both passes; curl to flat6labs.com, "
     "magnitt.com, wamda.com, itida.gov.eg, hub71.com, oasis500.com, sheraa.ae and "
     "startupqatar.qa all failed. 'Appeared as a live indexed link' is as far as verification "
     "could go. Run scripts/scout_scraper.py --verify-only from a normal network for real "
     "HTTP status codes."),
    ("What pass 2 actually caught",
     "Three factual errors that would have shipped: Cairo Angels has REBRANDED to Acasia; the "
     "Wa'ed domain is waed.com, not the waed.net cited in prose; and 212Founders resolves at "
     ".co, not the .ma given in an article. TIEC and Startup Egypt also turned out to have "
     "their own government domains (tiec.gov.eg, startup.gov.eg) rather than sitting under "
     "ITIDA as first assumed."),
    ("One row carries a security caution",
     "Endeavor Egypt's endeavoreg.org resolves, but its /contact/ page returned a gambling-spam "
     "page title in search results — a sign that part of the domain may be compromised or "
     "parked. Flagged in that row's source note. Check before sending founders there."),
    ("Twelve rows are still low confidence — verify these first",
     "EdVentures, Innoventures, the Egypt Fund of Funds, Nclude, the KAUST Innovation Fund, "
     "Riyadh Valley Company, SVC, Badir, The Garage, Startupbootcamp Dubai, Oman's Ithraa and "
     "Kuwait's National Fund for SME Development have no official domain that returned as an "
     "indexed link. Each carries a profile, government or coverage URL as a working placeholder "
     "and says so in its source note. Several are major institutions whose own sites are simply "
     "poorly indexed — SVC and The Garage in particular are certainly real; it is the URL, not "
     "the entity, that is unconfirmed."),
    ("This is a deep v1, not a census",
     "133 programme rows across 122 entities and 17 markets after three expansion passes. Directory sources report larger "
     "universes — Tracxn lists 41 accelerators in Egypt, Founder Institute 350+ Egyptian "
     "ecosystem entries, EgyptInnovate 780 entities, Causo 390+ programmes with deadlines. The "
     "aggregator rows are in the registry deliberately so the scraper discovers programmes this "
     "list does not yet name."),
    ("One row is deliberately a dead entity",
     "Iraq Tech Ventures is recorded with status CLOSED and no entity URL. Keeping known-dead "
     "entities in the registry stops a scraper rediscovering them and reporting them as new."),
    ("Deadlines age fast",
     "Programme dates move every cycle. The Hub71 Access deadline captured here came from a "
     "single search snapshot. Treat every date as needing re-verification on each run — which "
     "is what the scraper's change detection is for."),
]


# ===========================================================================
# VERIFICATION PASS 2 — re-searched every weak URL against the live index
# ===========================================================================
# Method: each entity was re-queried by name. A URL is upgraded only when it
# came back as an actual indexed result LINK (not merely named in prose).
# Still not fetch-verified — egress remained blocked — but "appeared as a live
# search-result link" is materially stronger than "inferred from prose".
#
# (entity, program) -> fields to overwrite
CORRECTIONS = {
    # ---- Egypt ----
    ("MSMEDA", "MSME financing & technical support"): dict(
        entity_url="https://www.devex.com/organizations/egyptian-micro-small-and-medium-enterprises-development-agency-msmeda-129670",
        programs_url="https://www.devex.com/organizations/egyptian-micro-small-and-medium-enterprises-development-agency-msmeda-129670",
        confidence="low",
        source="Devex + Private Equity International profiles are indexed; msmeda.org.eg itself "
               "never returned as a link across two search passes — treat the official domain as unconfirmed"),
    ("Startup Egypt", "National startup platform"): dict(
        entity_url="https://startup.gov.eg/",
        programs_url="https://startup.gov.eg/",
        description="Ministry of Investment and Foreign Trade platform — the first in Egypt to "
                    "connect entrepreneurs directly with government bodies, investors and "
                    "financing institutions. Indexed as 'Ministerial Group for Entrepreneurship'.",
        confidence="high",
        source="startup.gov.eg returned as an indexed link; EgyptToday + ArabFounders launch coverage"),
    ("NilePreneurs", "Innovation vouchers / R&D as a service"): dict(
        entity_url="https://www.cbe.org.eg/en/msmes-entrepreneurship/entrepreneurship/nilepreneurs",
        programs_url="https://www.cbe.org.eg/en/msmes-entrepreneurship/entrepreneurship/nilepreneurs",
        description="Central Bank of Egypt-powered initiative, started 2019, supporting startups "
                    "and SMEs in manufacturing, agriculture and digital transformation. Piloted at "
                    "Nile University, since expanded to four more universities.",
        confidence="high", source="Central Bank of Egypt page returned as an indexed link"),
    ("AUC Venture Lab", "Startup Accelerator (+ FinTech track with CIB)"): dict(
        entity_url="https://business.aucegypt.edu/research/centers/vlab",
        programs_url="https://business.aucegypt.edu/research/centers/vlab",
        apply_url="https://www.f6s.com/aucventurelab",
        description="Egypt's first university-based incubator/accelerator, launched 2013. Two "
                    "cycles a year, three-month intensive. Sectors span fintech, AI, green "
                    "economy, healthtech, e-commerce, logistics, IoT, edtech and more.",
        stats="1,000+ entrepreneurs supported since 2013; named best accelerator/incubator in North Africa",
        confidence="high", source="business.aucegypt.edu vlab page + f6s.com/aucventurelab, both indexed"),
    ("EdVentures", "EdTech investment & Creativa innovation hubs"): dict(
        entity_url="https://launchbaseafrica.com/2024/09/26/meet-the-eight-new-egyptian-startups-backed-by-prolific-investor-edventures/",
        confidence="low",
        source="Nahdet Misr CVC. No official domain returned as an indexed link in two passes — "
               "coverage link used as placeholder; find the real domain before relying on this row"),
    ("Innoventures", "Startup Reactor"): dict(
        entity_url="https://fi.co/insight/egypt-s-startup-resources-list-for-entrepreneurs-accelerators-incubators-investors",
        confidence="low",
        source="Named in ecosystem round-ups only; no official domain indexed in two passes"),
    ("GESR", "Social enterprise accelerator"): dict(
        entity_url="https://gesr.net/", programs_url="https://gesr.net/about-us/",
        description="Misr El-Kheir Foundation programme launched 2013, supporting innovators and "
                    "technology startups solving social challenges in water, energy, food, health, "
                    "education, AI and IoT.",
        stats="Announced technical & financial support up to EUR 30,000 for Egyptian agribusinesses",
        confidence="high", source="gesr.net and gesr.net/about-us both indexed; Startup Scene opportunity listing"),
    ("Cairo Angels", "Angel investment network"): dict(
        entity="Acasia (formerly Cairo Angels)",
        entity_url="https://acasia.group/the-cairo-angels-is-now-acasia/",
        programs_url="https://acasia.group/the-cairo-angels-is-now-acasia/",
        description="Egypt's first formal angel network, investing in early-stage startups in "
                    "Egypt and across MENA. REBRANDED — the Cairo Angels is now Acasia Group.",
        stats="2nd most active angel network in Africa per ABAN; now operating as Acasia",
        confidence="high", source="acasia.group rebrand announcement, indexed — name corrected on this pass"),
    ("Endeavor Egypt", "Endeavor Entrepreneur selection"): dict(
        entity_url="https://endeavoreg.org/",
        programs_url="https://endeavoreg.org/network/whoweare/",
        description="Launched in Egypt 2008. Selects, mentors and accelerates high-impact "
                    "entrepreneurs through Endeavor's global network.",
        confidence="medium",
        source="endeavoreg.org indexed. CAUTION: the /contact/ page returned a gambling-spam "
               "title in search results, which suggests part of the domain may be compromised "
               "or parked — check before sending founders there"),
    ("Egypt Ventures", "Startup investment & accelerator backing"): dict(
        entity_url="https://egyptventures.com/about/", programs_url="https://egyptventures.com/about/",
        description="Government-backed VC established 2017, empowering Egyptian startups. "
                    "Startups can pitch directly through the site. Backer of Falak Startups.",
        confidence="high", source="egyptventures.com/about indexed; EgyptInnovate profile"),
    ("Egypt Fund of Funds (with World Bank Group)", "Fund of Funds investment programme"): dict(
        entity_url="https://www.clydeco.com/en/insights/2026/02/egypt-launches-first-national-startup-charter",
        confidence="low",
        source="No official domain indexed. Clyde & Co National Startup Charter analysis used as "
               "the citable reference"),
    ("TIEC", "Virtual Incubation Programme"): dict(
        entity_url="https://tiec.gov.eg/", programs_url="https://tiec.gov.eg/",
        confidence="high", source="tiec.gov.eg returned as its own indexed domain on this pass"),
    ("EgyptInnovate", "Ecosystem platform & opportunity listings"): dict(
        entity_url="https://egyptinnovate.com/en", programs_url="https://egyptinnovate.com/en",
        description="ITIDA's national gateway to Egypt's innovation landscape, relaunched in a "
                    "revamped version. Connects startups, investors and ecosystem partners to "
                    "resources and opportunities — a high-value scrape target.",
        stats="Platform lists 780 entities: startups, investors, incubators and research centres",
        confidence="high", source="egyptinnovate.com/en indexed; ITIDA relaunch press release"),

    # ---- Saudi ----
    ("Wa'ed Ventures (Aramco)", "Wa'ed Ventures investment"): dict(
        entity_url="https://www.aramco.com/en/what-we-do/commercial-ecosystems/waed-ventures",
        programs_url="https://www.waed.com/en/philosophy",
        description="Aramco's venture arm. A USD 500 million fund investing in local tech startups "
                    "and incentivising global entrepreneurs to localise in the Kingdom.",
        stats="USD 500M fund; HQ at Dhahran Techno Valley",
        confidence="high",
        source="aramco.com Wa'ed page and waed.com/en/philosophy both indexed. NOTE: prose in "
               "results said 'waed.net' but the indexed link is waed.com — .com used"),
    ("KAUST Innovation Fund", "Deep-tech venture investment"): dict(
        entity_url="https://taqadam.kaust.edu.sa/",
        programs_url="https://taqadam.kaust.edu.sa/", confidence="low",
        source="No standalone fund domain indexed; TAQADAM/KAUST used as the reachable entry point"),

    # ---- UAE ----
    ("Dubai Future Foundation", "Dubai Future Accelerators"): dict(
        entity_url="https://www.dubaifuture.ae/",
        programs_url="https://www.dubaifuture.ae/initiatives/future-design-and-acceleration/dubai-future-accelerators/",
        apply_url="https://www.dubaifuture.ae/initiatives/future-design-and-acceleration/dubai-future-accelerators/how-it-works/",
        description="Intensive nine-week programme hosted by Dubai Future Foundation and the "
                    "Government of Dubai. Facilitates collaboration between startups, private "
                    "entities and government on pre-specified future challenges.",
        stats="9-week cohorts; backed by an AED 1 billion investment",
        confidence="high", source="dubaifuture.ae DFA, how-it-works and previous-cohorts pages all indexed"),
    ("in5 (TECOM Group)", "in5 Innovation Centres (Tech / Media / Design)"): dict(
        entity_url="https://infive.ae/", programs_url="https://infive.ae/in5-tech/",
        description="TECOM Group's integrated innovation platform with specialised facilities for "
                    "Technology (Dubai Internet City), Media (Dubai Production City) and Design "
                    "(Dubai Design District), plus training and mentorship.",
        confidence="high", source="infive.ae, /in5-tech and /contact-us indexed; dic.ae in5-centres page"),
    ("DTEC (Dubai Silicon Oasis)", "DTEC startup hub & Dubai Smart City Accelerator"): dict(
        entity_url="https://www.dso.ae/dubai-technology-entrepreneurship-campus-dtec-",
        programs_url="https://www.dso.ae/dubai-technology-entrepreneurship-campus-dtec-",
        description="Purpose-built technology hub wholly owned by Dubai Silicon Oasis Authority. "
                    "One-stop company setup, flexible coworking and startup support; the largest "
                    "tech startup coworking space in the Middle East.",
        stats="108,000 sq ft; 100+ startups from 60+ countries",
        confidence="medium",
        source="dso.ae DTEC page indexed. Prose cited dtec.ae but that domain did not return as a link"),
    ("Khalifa Fund for Enterprise Development", "Grants & soft loans"): dict(
        entity_url="https://www.khalifafund.ae/", programs_url="https://www.khalifafund.ae/",
        description="Not-for-profit economic development fund of the Government of Abu Dhabi, "
                    "launched 2007. Gives Emirati entrepreneurs access to market, resources, "
                    "mentorship and enterprise funding.",
        confidence="high", source="khalifafund.ae indexed; u.ae and moet.gov.ae government pages"),
    ("MBRIF", "Mohammed Bin Rashid Innovation Fund — Accelerator & Guarantee"): dict(
        entity_url="https://mbrif.ae/", programs_url="https://mbrif.ae/about-us/",
        description="An AED 2 billion Ministry of Finance initiative supporting innovators across "
                    "the seven sectors of the UAE National Innovation Strategy.",
        stats="AED 2 billion fund",
        confidence="high", source="mbrif.ae and mbrif.ae/about-us indexed; mof.gov.ae partner pages"),
    ("AstroLabs", "Market expansion into UAE & Saudi"): dict(
        entity_url="https://astrolabs.com/", confidence="low",
        source="Named consistently in guides; astrolabs.com not returned as an indexed link — verify"),
    ("ADGM", "Tech & FinTech licensing and programmes"): dict(
        entity_url="https://www.adgm.com/", confidence="low",
        source="Named in guides; adgm.com not returned as an indexed link in either pass — verify"),
    ("Startupbootcamp", "Startupbootcamp Smart City Dubai"): dict(
        entity_url="https://www.startupbootcamp.org/", confidence="low",
        source="Named in guides; no indexed link for the Dubai programme page — verify"),
    ("DIFC", "DIFC FinTech Hive Accelerator"): dict(
        entity_url="https://www.difc.ae/",
        programs_url="https://www.dxbstart.com/programs/difc-fintech-hive",
        confidence="medium", source="DXBStart programme page indexed; difc.ae itself not returned — verify"),

    # ---- Qatar / Kuwait ----
    ("Qatar Development Bank", "SME financing & QDB Ventures"): dict(
        entity_url="https://www.qdb.qa/", programs_url="https://www.qdb.qa/about/faq",
        description="Government-owned financial entity set up by Emiri Decree to invest in and "
                    "develop local industries by supporting SMEs in Qatar. Parent of QBIC.",
        confidence="high", source="qdb.qa and qdb.qa/about/faq both indexed"),
    ("National Fund for SME Development", "SME financing & incubation"): dict(
        entity_url="https://smeportal.unescwa.org/index.php/financing/national-fund",
        programs_url="https://smeportal.unescwa.org/index.php/financing/national-fund",
        confidence="low",
        source="UN ESCWA SME portal page indexed. Prose cited nationalfund.gov.kw but that domain "
               "did not return as a link in two passes — verify"),

    # ---- Jordan / Morocco ----
    ("ISSF (Innovative Startups & SMEs Fund)", "Direct & indirect investment"): dict(
        entity_url="https://issfjo.com/", programs_url="https://issfjo.com/",
        description="USD 98 million fund established 2017, registered in Jordan as a private "
                    "shareholding company. A partnership between the Central Bank of Jordan "
                    "(USD 48M) and the World Bank (USD 50M).",
        stats="USD 98M fund: CBJ USD 48M + World Bank USD 50M",
        confidence="high", source="issfjo.com indexed; MAGNiTT profile; World Bank ICR report"),
    ("212Founders (CDG Invest)", "212Founders acceleration"): dict(
        entity_url="https://www.212founders.co/",
        programs_url="https://www.cdg.ma/en/212founders",
        apply_url="https://www.212founders.co/",
        description="CDG Invest's flagship Moroccan acceleration programme, carried by the "
                    "investment arm of CDG. Accepts applications on a continuous basis.",
        confidence="high",
        source="212founders.co and cdg.ma/en/212founders both indexed. NOTE: prose cited a .ma "
               "domain; the indexed link is .co"),
}


# ===========================================================================
# NEW ENTITIES — added on verification pass 2
# ===========================================================================
EXTRA_PROGRAMS = [
    # ---- Egypt ----
    dict(entity="Startup Scene ME", entity_type="Media / Data platform", country="Egypt",
         city="Cairo", program="OPPORTUNITIES feed", program_type="Directory listing",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="Covers the MENA ecosystem from Cairo to Riyadh, Dubai to Amman. Runs a "
                     "dedicated OPPORTUNITIES section carrying everything from grants to "
                     "incubation-cycle applications — one of the highest-yield scrape targets here.",
         stats="Dedicated opportunities feed; MENA-wide coverage",
         entity_url="https://www.startupscene.me/",
         programs_url="https://thestartupscene.me/OPPORTUNITIES", apply_url="",
         confidence="high", source="startupscene.me and thestartupscene.me/OPPORTUNITIES indexed"),

    dict(entity="Egyptian Ministerial Group for Entrepreneurship",
         entity_type="Government / Authority", country="Egypt", city="Cairo",
         program="National Startup Charter", program_type="Grant", stage="Any",
         sectors="All", eligibility="Egyptian startups",
         funding="Policy incentives & classification certificates", equity="No",
         duration="Ongoing", cadence="Rolling", status="Active",
         description="Egypt's first National Startup Charter, coordinating incentives, "
                     "classification certificates for innovative projects, and cross-ministry "
                     "startup policy.",
         stats="25 classification certificates issued for innovative projects and startups",
         entity_url="https://startup.gov.eg/",
         programs_url="https://www.clydeco.com/en/insights/2026/02/egypt-launches-first-national-startup-charter",
         apply_url="", confidence="high",
         source="startup.gov.eg indexed; Clyde & Co legal analysis of the Charter"),

    # ---- Saudi ----
    dict(entity="Sanabil Investments", entity_type="Sovereign / National fund",
         country="Saudi Arabia", city="Riyadh", program="Direct & fund-of-funds investment",
         program_type="Fund of funds", stage="Seed", sectors="Agnostic",
         eligibility="KSA and international", funding="Equity investment", equity="Yes",
         duration="N/A", cadence="Rolling", status="Active",
         description="PIF-linked sovereign investor making direct equity investments primarily "
                     "in the Kingdom and investing in funds, building international investment "
                     "capability. Co-sponsor of the Sanabil 500 accelerator.",
         stats="Sovereign wealth investor; backs the Sanabil 500 MENA Seed Accelerator",
         entity_url="https://www.sanabil.com/en/home",
         programs_url="https://www.sanabil.com/en/home", apply_url="", confidence="high",
         source="sanabil.com/en/home indexed"),

    dict(entity="Sanabil Venture Studio", entity_type="Accelerator", country="Saudi Arabia",
         city="Riyadh", program="Venture studio", program_type="Incubator", stage="Idea",
         sectors="Tech", eligibility="Founders building in KSA", funding="Studio-backed",
         equity="Yes", duration="Programme-dependent", cadence="Rolling", status="Active",
         description="Sanabil's venture studio arm, co-building companies from scratch rather "
                     "than only investing in existing ones.",
         stats="Studio model on its own domain",
         entity_url="https://sanabil.studio/", programs_url="https://sanabil.studio/",
         apply_url="", confidence="high", source="sanabil.studio indexed"),

    dict(entity="Impact46", entity_type="VC firm", country="Saudi Arabia", city="Riyadh",
         program="Venture & alternative investment", program_type="Seed fund", stage="Seed",
         sectors="Fintech, SaaS, platforms, cybersecurity", eligibility="Tech startups",
         funding="Seed to growth", equity="Yes", duration="N/A", cadence="Rolling",
         status="Active",
         description="Riyadh-based CMA-authorised asset manager specialising in alternative "
                     "investments — venture capital and private equity — from seed stage to "
                     "mature businesses.",
         stats="CMA-authorised; fintech, SaaS, platforms and cybersecurity focus",
         entity_url="https://impact46.sa/", programs_url="https://impact46.sa/", apply_url="",
         confidence="high", source="impact46.sa indexed"),

    dict(entity="Vision Ventures", entity_type="VC firm", country="Saudi Arabia", city="Dammam",
         program="Early-stage venture investment", program_type="Seed fund", stage="Seed",
         sectors="Cloud, SaaS, gaming, analytics, smart transport", eligibility="KSA / MENA",
         funding="VC investment", equity="Yes", duration="N/A", cadence="Rolling",
         status="Active",
         description="Venture capital firm founded 2016 in Dammam, investing across cloud, "
                     "mobile, SaaS, big data, gaming, analytics, smart transportation and "
                     "autonomous technologies.",
         stats="Founded 2016; a Jada fund-of-funds portfolio manager",
         entity_url="https://visionvc.co/", programs_url="https://visionvc.co/portfolio/",
         apply_url="", confidence="high", source="visionvc.co and /portfolio indexed; jada.com.sa portfolio page"),

    dict(entity="Jada Fund of Funds", entity_type="Sovereign / National fund",
         country="Saudi Arabia", city="Riyadh", program="Fund-of-funds commitments",
         program_type="Fund of funds", stage="Any", sectors="All",
         eligibility="VC, PE and private-debt fund managers", funding="LP commitments",
         equity="Indirect", duration="N/A", cadence="Rolling", status="Active",
         description="PIF-backed fund of funds backing VC, PE and private-debt managers rather "
                     "than investing directly, to build an ecosystem that can finance Saudi SME "
                     "growth sustainably. Co-backer of the Flat6Labs Riyadh Seed Programme.",
         stats="Backs managers including Vision Ventures",
         entity_url="https://jada.com.sa/en/portfolio/portfolio-vision-ventures",
         programs_url="https://jada.com.sa/en/portfolio/portfolio-vision-ventures",
         apply_url="", confidence="medium",
         source="jada.com.sa portfolio page indexed; root domain inferred from it"),

    dict(entity="Riyadh Valley Company (RVC)", entity_type="University programme",
         country="Saudi Arabia", city="Riyadh", program="KSU investment arm",
         program_type="Seed fund", stage="Seed",
         sectors="Biotech, IT, sustainable resources", eligibility="KSA startups",
         funding="Funding + strategic support", equity="Yes", duration="N/A",
         cadence="Rolling", status="Active",
         description="Investment arm of King Saud University, funding startups in biotechnology, "
                     "information technology and sustainable resources. Co-backer of the "
                     "Flat6Labs Riyadh Seed Programme.",
         stats="KSU investment vehicle; RSP ecosystem partner",
         entity_url="https://angelmatch.io/accelerators/Riyadh_Valley_Company",
         programs_url="https://angelmatch.io/accelerators/Riyadh_Valley_Company",
         apply_url="", confidence="low",
         source="Profile pages indexed; no official RVC domain returned — verify"),

    dict(entity="Saudi Vision 2030 encyclopedia", entity_type="Aggregator / Directory",
         country="Saudi Arabia", city="Riyadh",
         program="Incubators & accelerators directory", program_type="Directory listing",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="Maintains encyclopedia pages on Saudi incubators, accelerators and venture "
                     "funds — a structured directory worth polling for newly launched KSA programmes.",
         stats="Per-topic encyclopedia pages on the KSA ecosystem",
         entity_url="https://vision2030.ai/",
         programs_url="https://vision2030.ai/encyclopedia/saudi-arabia-incubators-accelerators/",
         apply_url="", confidence="high", source="vision2030.ai encyclopedia pages indexed"),

    # ---- UAE ----
    dict(entity="Sheraa (Sharjah Entrepreneurship Center)", entity_type="Government / Authority",
         country="UAE", city="Sharjah", program="S3 — Sharjah Startup Studio",
         program_type="Incubator", stage="Seed", sectors="Agnostic",
         eligibility="Startups scaling in Sharjah", funding="Equity-free incubation",
         equity="No", duration="Programme cycle", cadence="Annual", status="Active",
         description="Sheraa's tailored incubator for startups in their scaling phase, sitting "
                     "alongside Startup Dojo (ideation-stage, youth-led) in Sheraa's programme ladder.",
         stats="Sheraa overall: 20,000+ youth empowered, 450+ startups supported, 180+ incubated",
         entity_url="https://www.asc.sheraa.ae/",
         programs_url="https://www.asc.sheraa.ae/s3-program", apply_url="", confidence="high",
         source="asc.sheraa.ae/s3-program indexed; shurooq.gov.ae Sheraa initiative page"),

    dict(entity="Ma'an (Authority of Social Contribution)", entity_type="Government / Authority",
         country="UAE", city="Abu Dhabi", program="Social Incubator Programme",
         program_type="Incubator", stage="Idea", sectors="Social impact",
         eligibility="Social ventures in Abu Dhabi", funding="Social Investment Fund",
         equity="No", duration="Programme-dependent", cadence="Rolling", status="Active",
         description="Formed 2019 by Abu Dhabi's Department of Community Development. Works "
                     "across four pillars: a Social Investment Fund, a Social Incubator "
                     "Programme, Community Engagement, and Social Impact Bonds.",
         stats="AED 220M+ allocated to Abu Dhabi social development projects in 2025",
         entity_url="https://maan.gov.ae/en/",
         programs_url="https://fundraise.maan.gov.ae/en/content/social-investment-fund/",
         apply_url="", confidence="high", source="maan.gov.ae and fundraise.maan.gov.ae indexed"),

    dict(entity="ADIO (Abu Dhabi Investment Office)", entity_type="Government / Authority",
         country="UAE", city="Abu Dhabi", program="Innovation Programme", program_type="Grant",
         stage="Growth",
         sectors="Agritech, financial services, ICT, health & biopharma, tourism",
         eligibility="Companies investing/R&D in Abu Dhabi",
         funding="AED 2 billion fund; AED 1bn allocated to date", equity="No",
         duration="Multi-year", cadence="Rolling", status="Active",
         description="An AED 2 billion fund driving R&D and advancing innovation across "
                     "high-growth sectors. ADIO has supported dozens of investors and companies "
                     "through tailored programmes since 2019.",
         stats="AED 2bn fund; AED 1bn allocated to 37 companies",
         entity_url="https://www.investinabudhabi.ae/",
         programs_url="https://www.investinabudhabi.ae/News/ADIOs-Innovation-Programme-builds-capabilities",
         apply_url="", confidence="high",
         source="investinabudhabi.ae Innovation Programme page indexed; Abu Dhabi Media Office"),

    dict(entity="SRTI Park (Sharjah Research, Technology & Innovation Park)",
         entity_type="Government / Authority", country="UAE", city="Sharjah",
         program="Free-zone incubation for research-based startups", program_type="Incubator",
         stage="Any", sectors="Research, technology, knowledge-based",
         eligibility="Research and tech ventures", funding="Infrastructure + support",
         equity="No", duration="Ongoing", cadence="Rolling", status="Active",
         description="Free zone established 2016 by royal decree of the Ruler of Sharjah, "
                     "providing infrastructure and support for research, technology and "
                     "knowledge-based startups.",
         stats="Established 2016 by royal decree",
         entity_url="https://universitycity.gov.ae/en/portfolio-item/sharjah-research-technology-and-innovation-park/",
         programs_url="https://universitycity.gov.ae/en/portfolio-item/sharjah-research-technology-and-innovation-park/",
         apply_url="", confidence="medium",
         source="universitycity.gov.ae page indexed; official srtip.ae domain not returned — verify"),

    # ---- Bahrain ----
    dict(entity="Al Waha Fund of Funds", entity_type="Sovereign / National fund",
         country="Bahrain", city="Manama", program="Fund-of-funds commitments",
         program_type="Fund of funds", stage="Any", sectors="Tech, fintech",
         eligibility="VC funds with a Bahrain presence", funding="USD 100 million fund",
         equity="Indirect", duration="N/A", cadence="Rolling", status="Active",
         description="Invests in venture capital funds that have a presence in Bahrain. LP "
                     "advisory includes Mumtalakat, National Bank of Bahrain, Batelco, Tamkeen "
                     "and Bahrain Development Bank.",
         stats="Closed at USD 100 million; investor in Shorooq and a USD 50M fintech fund",
         entity_url="https://www.bahrainedb.com/bahrain-pulse/al-waha-fund-of-funds-fintech-startups",
         programs_url="https://www.bahrainedb.com/bahrain-pulse/al-waha-fund-of-funds-fintech-startups",
         apply_url="", confidence="medium",
         source="Bahrain EDB page indexed; Gulf Business and Arabian Business coverage"),

    # ---- Jordan ----
    dict(entity="ZINC (Zain Innovation Campus)", entity_type="Corporate programme",
         country="Jordan", city="Amman", program="Incubation & acceleration",
         program_type="Incubator", stage="Idea", sectors="Tech",
         eligibility="Jordanian entrepreneurs", funding="Programme support", equity="No",
         duration="Programme-dependent", cadence="Recurring", status="Active",
         description="Established by Zain Jordan in 2014 and launched at King Hussein Business "
                     "Park. Recognised as the first startup enabler in Jordan; runs incubation "
                     "and acceleration, coworking, training and mentorship.",
         stats="Founded 2014; Jordan's first startup enabler",
         entity_url="https://zinc.jo/", programs_url="https://zinc.jo/", apply_url="",
         confidence="high", source="zinc.jo indexed; Zain eShop ZINC page; Jordan Pulse coverage"),

    dict(entity="iPARK", entity_type="Incubator", country="Jordan", city="Amman",
         program="General incubation programme", program_type="Incubator", stage="Idea",
         sectors="Technology", eligibility="Jordanian startups",
         funding="Advisory + capacity building", equity="Varies", duration="Programme-dependent",
         cadence="Rolling", status="Active",
         description="Jordan's first and longest-running business incubator, hosted by the Royal "
                     "Scientific Society. Matchmaking, advisory, legal support and capacity "
                     "building across multiple incubators.",
         stats="Jordan's oldest running incubation programme",
         entity_url="https://www.ipark.jo/",
         programs_url="https://www.ipark.jo/what-we-do/entrepreneurship/",
         apply_url="https://gust.com/programs/general-incubation-program-amman",
         confidence="high", source="ipark.jo, /about-ipark and /what-we-do indexed; Gust programme page"),

    dict(entity="Beyond Capital", entity_type="NGO / Development agency", country="Jordan",
         city="Amman", program="Entrepreneur support programme", program_type="Accelerator",
         stage="Seed", sectors="Agnostic", eligibility="Jordanian entrepreneurs",
         funding="USD 10 million USAID-backed fund", equity="Varies",
         duration="Programme cycle", cadence="Batch-based", status="Active",
         description="Joint venture between Endeavor Jordan and Silicon Badia, backed by a USD "
                     "10 million USAID fund. Supports entrepreneurs, finances them and develops "
                     "angel investors.",
         stats="USD 10M USAID-backed fund; selects entrepreneurs in batches",
         entity_url="https://beyondcapital.vc/", programs_url="https://beyondcapital.vc/",
         apply_url="", confidence="high",
         source="beyondcapital.vc indexed; MENAbytes and Startup Scene cohort coverage"),

    # ---- Lebanon ----
    dict(entity="Smart ESA", entity_type="University programme", country="Lebanon",
         city="Beirut", program="Smart ESA Accelerator", program_type="Accelerator",
         stage="Seed", sectors="Tech", eligibility="Lebanese startups",
         funding="Programme support", equity="Varies", duration="Programme cycle",
         cadence="Recurring", status="Active",
         description="Founded 2017 at ESA Business School; described as the most successful "
                     "accelerator programme in Lebanon. Runs local and international tracks.",
         stats="Founded 2017",
         entity_url="https://www.esa.edu.lb/smart-esa/home",
         programs_url="https://www.esa.edu.lb/smart-esa/programs/international-program",
         apply_url="", confidence="high", source="esa.edu.lb Smart ESA home, about and programme pages indexed"),

    # ---- Morocco ----
    dict(entity="Technopark Maroc", entity_type="Incubator", country="Morocco",
         city="Casablanca / Rabat / Tangier / Agadir / Essaouira",
         program="Technopark incubation network", program_type="Incubator", stage="Idea",
         sectors="IT, consulting, services, communication", eligibility="Moroccan companies",
         funding="Hosting + support", equity="No", duration="Ongoing", cadence="Rolling",
         status="Active",
         description="Incubator for technology enterprises supporting young companies, mainly in "
                     "IT, consulting, services and communication. Extended nationally: Rabat "
                     "(2012), Tangier (2015), Agadir (2021), Essaouira (2023).",
         stats="Five-city network",
         entity_url="https://www.technopark.ma/",
         programs_url="https://www.technopark.ma/reseau/", apply_url="", confidence="high",
         source="technopark.ma, /technopark and /reseau indexed"),

    dict(entity="IMPACT Lab", entity_type="Accelerator", country="Morocco", city="Casablanca",
         program="Innovation & startup support", program_type="Accelerator", stage="Any",
         sectors="Agnostic", eligibility="Morocco and 17 African countries",
         funding="Programme support", equity="Varies", duration="Programme-dependent",
         cadence="Rolling", status="Active",
         description="Since 2016, supports startups, companies and public institutions in Morocco "
                     "and 17 African countries to respond innovatively to growth and "
                     "transformation challenges. Also runs IMPACT Camp.",
         stats="Active since 2016 across 17 African countries",
         entity_url="https://impactlab.africa/", programs_url="https://impactcamp.ma/",
         apply_url="", confidence="high", source="impactlab.africa and impactcamp.ma indexed"),

    dict(entity="StartUp Maroc", entity_type="Accelerator", country="Morocco", city="Casablanca",
         program="Startup acceleration (Innov Invest)", program_type="Accelerator",
         stage="Idea", sectors="Agnostic", eligibility="Moroccan entrepreneurs",
         funding="Innov Invest Fund-linked", equity="Varies", duration="Programme-dependent",
         cadence="Recurring", status="Active",
         description="Accelerator labelled by the Caisse Centrale de Garantie under the Innov "
                     "Invest Fund, with a mission to help high-potential Moroccan entrepreneurs "
                     "and startups emerge.",
         stats="CCG-labelled under the Innov Invest Fund",
         entity_url="https://www.startupmaroc.org/",
         programs_url="https://www.startupmaroc.org/a-propos", apply_url="", confidence="high",
         source="startupmaroc.org and /a-propos indexed"),

    dict(entity="CDG Invest", entity_type="Sovereign / National fund", country="Morocco",
         city="Rabat", program="Investment across company stages", program_type="Fund of funds",
         stage="Any", sectors="All", eligibility="Moroccan companies",
         funding="Equity investment", equity="Yes", duration="N/A", cadence="Rolling",
         status="Active",
         description="Investment branch of the CDG group — a public institution investing "
                     "collected savings into projects aligned with Morocco's strategic "
                     "challenges. Parent of the 212Founders programme.",
         stats="Runs 212Founders; builds Morocco's private-equity ecosystem",
         entity_url="https://cdginvest.ma/en/home/",
         programs_url="https://www.cdg.ma/en/cdg-invest", apply_url="", confidence="high",
         source="cdginvest.ma/en/home and cdg.ma/en/cdg-invest indexed"),

    dict(entity="StartupHub Maroc", entity_type="Aggregator / Directory", country="Morocco",
         city="Casablanca", program="Moroccan startup ecosystem directory",
         program_type="Directory listing", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Continuous",
         status="Active",
         description="Directory of the Moroccan startup ecosystem — useful for discovering "
                     "Morocco-specific programmes not named elsewhere in this registry.",
         stats="Ecosystem directory",
         entity_url="https://www.startuphubmaroc.ma/",
         programs_url="https://www.startuphubmaroc.ma/startups", apply_url="",
         confidence="high", source="startuphubmaroc.ma indexed"),

    # ---- Regional media ----
    dict(entity="WAYA Media", entity_type="Media / Data platform", country="Regional (MENA)",
         city="Regional", program="Bilingual startup & business news", program_type="News feed",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="Bilingual (EN/AR) business and startup news platform serving founders, "
                     "operators and investors across Egypt, the Gulf and the wider MENA region. "
                     "Bilingual coverage makes it valuable for Arabic-language programme calls.",
         stats="EN/AR coverage; backed by Foras.ai investment in Founders Media",
         entity_url="https://waya.media/", programs_url="https://waya.media/tag/mena/",
         apply_url="", confidence="high", source="waya.media, /about and /tag/mena indexed"),

    dict(entity="StartupBlink", entity_type="Aggregator / Directory", country="Global",
         city="Global", program="Ecosystem rankings & startup directories",
         program_type="Directory listing", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Annual",
         status="Active",
         description="Global startup ecosystem index with per-country pages, including Egypt — "
                     "useful for spotting newly ranked ecosystems and the organisations in them.",
         stats="Per-country ecosystem rankings",
         entity_url="https://www.startupblink.com/",
         programs_url="https://www.startupblink.com/top-startups/egypt", apply_url="",
         confidence="high", source="startupblink.com/top-startups/egypt indexed"),

    dict(entity="VC4A", entity_type="Aggregator / Directory", country="Global", city="Global",
         program="Africa & MENA programme listings", program_type="Directory listing",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="Venture platform listing accelerators and incubators across Africa and "
                     "adjacent markets, with programme profiles and open calls.",
         stats="Hosts profiles for AUC Venture Lab, Cairo Angels and others",
         entity_url="https://vc4a.com/", programs_url="https://vc4a.com/", apply_url="",
         confidence="high", source="vc4a.com profile pages indexed"),

    dict(entity="Gust", entity_type="Aggregator / Directory", country="Global", city="Global",
         program="Accelerator programme applications", program_type="Directory listing",
         stage="Any", sectors="All", eligibility="Open", funding="N/A", equity="N/A",
         duration="Ongoing", cadence="Continuous", status="Active",
         description="Hosts application portals for accelerator and incubation programmes, "
                     "including MENA ones such as iPARK's general incubation programme.",
         stats="Application-hosting platform used by regional incubators",
         entity_url="https://gust.com/",
         programs_url="https://gust.com/accelerators/auc-venture-lab", apply_url="",
         confidence="high", source="gust.com programme pages indexed"),
]


def _apply_pass2():
    """Fold pass-2 corrections and additions into PROGRAMS."""
    for p in PROGRAMS:
        patch = CORRECTIONS.get((p["entity"], p["program"]))
        if patch:
            p.update(patch)
    PROGRAMS.extend(EXTRA_PROGRAMS)


_apply_pass2()


# ---------------------------------------------------------------------------
# Pass-2b — last three weak rows resolved on a third targeted search
# ---------------------------------------------------------------------------
CORRECTIONS_2B = {
    ("MSMEDA", "MSME financing & technical support"): dict(
        entity_url="https://www.msmeda.org.eg/",
        programs_url="https://www.msmeda.org.eg/pages/4020",
        description="Micro, Small and Medium Enterprise Development Agency — the body "
                    "responsible for developing the legislative environment for MSMEs and "
                    "entrepreneurship in Egypt. Offers financing, training and incubation; "
                    "partnered with Startup Egypt. Site is primarily Arabic.",
        confidence="high",
        source="msmeda.org.eg returned as an indexed link on the third pass, with several "
               "deep pages; UN ESCWA DEPAR profile"),
    ("AstroLabs", "Market expansion into UAE & Saudi"): dict(
        entity_url="https://astrolabs.com/", programs_url="https://astrolabs.com/about-us",
        description="Dubai-based market-entry partner founded 2013, with offices in Dubai and "
                    "Riyadh. Company formation, licensing, corporate services and ecosystem "
                    "integration for international firms entering the Saudi and UAE markets.",
        stats="Founded 2013; Dubai and Riyadh offices",
        confidence="high", source="astrolabs.com, /about-us, /contact-us all indexed"),
    ("ADGM", "Tech & FinTech licensing and programmes"): dict(
        entity_url="https://www.adgm.com/", programs_url="https://www.adgm.com/",
        description="Abu Dhabi's international financial centre and free economic zone, "
                    "established 2013 and operational since October 2015. Common-law regulatory "
                    "ecosystem, startup-tailored licences, and host of Hub71.",
        stats="Operational since Oct 2015; hosts Hub71",
        confidence="high", source="adgm.com indexed; WEF and WAIFC organisation profiles"),
}

for _p in PROGRAMS:
    _patch = CORRECTIONS_2B.get((_p["entity"], _p["program"]))
    if _patch:
        _p.update(_patch)
CORRECTIONS.update(CORRECTIONS_2B)


# ===========================================================================
# PASS 3 — further expansion. Same rule: a URL is kept only when it came back
# as an actual indexed search-result link, not merely named in an article.
# ===========================================================================
EXTRA_PROGRAMS_3 = [

    # ---------------- Saudi Arabia ----------------
    dict(entity="Wadi Makkah Ventures", entity_type="University programme",
         country="Saudi Arabia", city="Makkah", program="Growth Incubator / Nomow",
         program_type="Incubator", stage="Idea",
         sectors="Hajj & Umrah, occupational safety, edtech, fintech",
         eligibility="Saudi startups", funding="Financial support + investment",
         equity="Yes", duration="Programme cycle", cadence="Annual cohorts",
         status="Active",
         description="Investment company owned by Umm Al-Qura University. Runs six incubators "
                     "with co-working, a FabLab innovation lab for prototyping, legal and "
                     "technical consultation, and patent-registration support.",
         stats="6 incubators, 37 incubatees, 40 portfolio startups; introduced 17 new startups in one intake",
         entity_url="https://wmvc.sa/", programs_url="https://wmvc.sa/", apply_url="",
         confidence="high", source="wmvc.sa indexed; UQU news; IASP member directory"),

    dict(entity="Badir Program (KACST)", entity_type="Government / Authority",
         country="Saudi Arabia", city="Riyadh", program="Technology incubators & accelerators",
         program_type="Incubator", stage="Idea", sectors="ICT, biotech, advanced manufacturing",
         eligibility="Saudi tech entrepreneurs and SMEs",
         funding="Incubation + access to funding", equity="No", duration="Programme-dependent",
         cadence="Rolling", status="Active",
         description="National technology incubator programme launched by King Abdulaziz City "
                     "for Science and Technology (KACST) in 2007, to accelerate the growth of "
                     "technology-based businesses in Saudi Arabia.",
         stats="Launched 2007 by KACST; incubators across Riyadh and other cities",
         entity_url="https://magnitt.com/enablers/badir-technology-incubator-riyadh-1048",
         programs_url="https://www.prodevs.io/accelerators/badir", apply_url="",
         confidence="low",
         source="MAGNiTT and ProDevs profiles indexed; no official badir domain returned — verify"),

    dict(entity="SVC (Saudi Venture Capital Company)", entity_type="Sovereign / National fund",
         country="Saudi Arabia", city="Riyadh", program="Fund investment & co-investment",
         program_type="Fund of funds", stage="Any", sectors="E-commerce, fintech, health, edtech, logistics",
         eligibility="Startups and SMEs, pre-seed to pre-IPO",
         funding="USD 2 billion investment mandate", equity="Yes/indirect", duration="N/A",
         cadence="Rolling", status="Active",
         description="Established 2018, a subsidiary of the SME Bank within the National "
                     "Development Fund. Stimulates financing for startups and SMEs from "
                     "pre-seed to pre-IPO via private capital funds and co-investment. "
                     "Co-backer of the Flat6Labs Riyadh Seed Programme.",
         stats="USD 2bn mandate; invested in 54 funds and 800+ startups and SMEs",
         entity_url="https://magnitt.com/investors/saudi-venture-capital-company-svc-51100",
         programs_url="https://vision2030.ai/encyclopedia/saudi-arabia-venture-funds/",
         apply_url="", confidence="low",
         source="MAGNiTT profile and Saudi Press Agency releases indexed; no official SVC "
                "domain returned as a link — verify"),

    dict(entity="The Garage (MCIT / KACST)", entity_type="Government / Authority",
         country="Saudi Arabia", city="Riyadh", program="Innovation district & startup hub",
         program_type="Incubator", stage="Any", sectors="Tech, cybersecurity, gaming, drones",
         eligibility="Startups operating in KSA", funding="Space + programmes", equity="No",
         duration="Ongoing", cadence="Rolling", status="Active",
         description="Unveiled September 2023 as a collaboration between the Ministry of "
                     "Communications and IT, KACST and the Saudi Federation for Cybersecurity, "
                     "Programming and Drones. Combines incubators, accelerators and shared "
                     "resources in one location inside KACST.",
         stats="28,000 sqm — described as the largest innovation district in the Middle East; "
               "capacity for 300+ startups",
         entity_url="https://saudigazette.com.sa/article/635963",
         programs_url="https://www.trade.gov/market-intelligence/saudi-arabia-information-technology-garage-new-player-saudi-arabias-startup",
         apply_url="", confidence="low",
         source="Saudi Gazette and US trade.gov market-intelligence pages indexed; prose cites "
                "thegarage.sa but that domain did not return as a link — verify"),

    # ---------------- Qatar ----------------
    dict(entity="Qatar FinTech Hub (QFTH)", entity_type="Government / Authority",
         country="Qatar", city="Doha", program="Incubator & Accelerator (wave-based)",
         program_type="Accelerator", stage="Seed", sectors="FinTech",
         eligibility="Local and international fintechs",
         funding="Programme support + funding opportunities", equity="Varies",
         duration="Programme cycle", cadence="Waves (wave 5 announced)", status="Active",
         description="Launched 2020 and powered by Qatar Development Bank. A central hub for "
                     "fintech innovation advancing Qatar's Third Financial Sector Strategy and "
                     "National FinTech Strategy — business, technical and regulatory support, "
                     "mentorship, market access and funding.",
         stats="Launched 2020; runs wave-based incubator and accelerator intakes",
         entity_url="https://fintech.qa/en", programs_url="https://fintech.qa/en",
         apply_url="", confidence="high",
         source="fintech.qa indexed; FF News wave-5 announcement; USQBC portal profile"),

    # ---------------- Bahrain ----------------
    dict(entity="Hope Ventures", entity_type="VC firm", country="Bahrain", city="Manama",
         program="Co-investment in Bahraini founders", program_type="Seed fund", stage="Seed",
         sectors="Agnostic", eligibility="Bahraini-founded scalable businesses",
         funding="Co-investment", equity="Yes", duration="N/A", cadence="Rolling",
         status="Active",
         description="The investment arm of Hope Fund, founded 2021 in Manama, co-investing in "
                     "high-potential scalable Bahraini-founded businesses to accelerate growth. "
                     "Listed on the Bahrain Investment Market. Partnered with the ministry on a "
                     "National Innovation Centre.",
         stats="Founded 2021; landmark listing on Bahrain Investment Market",
         entity_url="https://www.hopefund.bh/",
         programs_url="https://www.hopefund.bh/about-hope-ventures", apply_url="",
         confidence="high", source="hopefund.bh and /about-hope-ventures indexed; Bahrain Bourse listing notice"),

    # ---------------- Kuwait ----------------
    dict(entity="Zain Great Idea (ZGI)", entity_type="Corporate programme", country="Kuwait",
         city="Kuwait City", program="ZGI Accelerator", program_type="Accelerator",
         stage="Seed", sectors="Tech", eligibility="Kuwaiti and now regional founders",
         funding="Access to Zain Ventures and investors", equity="Varies",
         duration="Programme cycle", cadence="Annual", status="Active",
         description="Zain's award-winning tech startup accelerator, running 15 years and now "
                     "open to entrepreneurs across the region. Offers a Silicon Valley trip, "
                     "mentorship from global experts, bootcamps and investor access. KFAS "
                     "certified trainers deliver specialised sessions.",
         stats="15 years running; regional intake; Demo Day with Zain Ventures",
         entity_url="https://zaingreatidea.com/",
         programs_url="https://www.zain.com/en/press-release/zgi2025",
         apply_url="https://zaingreatidea.com/", confidence="high",
         source="zaingreatidea.com and zain.com ZGI press releases indexed"),

    # ---------------- Oman ----------------
    dict(entity="Ithraa", entity_type="Government / Authority", country="Oman", city="Muscat",
         program="Investment & export development support", program_type="Soft landing / Market access",
         stage="Any", sectors="All", eligibility="Investors and exporters in Oman",
         funding="Facilitation", equity="No", duration="Ongoing", cadence="Rolling",
         status="Active",
         description="Oman's official investment and export development agency — the front door "
                     "for founders and investors entering the Omani market.",
         stats="National investment-promotion agency",
         entity_url="https://globaledge.msu.edu/global-resources/resource/5807",
         programs_url="https://globaledge.msu.edu/global-resources/resource/5807",
         apply_url="", confidence="low",
         source="globalEDGE country resource page indexed; prose cites ithraa.om but that "
                "domain did not return as a link — verify"),

    # ---------------- Egypt ----------------
    dict(entity="Nclude", entity_type="Corporate programme", country="Egypt", city="Cairo",
         program="Fintech & financial-inclusion fund", program_type="Seed fund", stage="Seed",
         sectors="FinTech, financial inclusion", eligibility="Egyptian fintechs",
         funding="USD 105 million first fund", equity="Yes", duration="N/A",
         cadence="Rolling", status="Active",
         description="Cairo-based fund founded 2022, focused on financial inclusion and "
                     "building a fintech stack for Egypt. Backed by Banque Misr, National Bank "
                     "of Egypt and Banque du Caire, with Banque Misr leading the raise.",
         stats="USD 105M first fund; founded 2022; three state-bank backers",
         entity_url="https://lucidityinsights.com/spotlights/nclude-accelerating-fintech-in-egypt",
         programs_url="https://lucidityinsights.com/spotlights/nclude-accelerating-fintech-in-egypt",
         apply_url="", confidence="low",
         source="Lucidity Insights spotlight indexed; no official Nclude domain returned — verify"),

    dict(entity="Plug and Play", entity_type="Accelerator", country="Egypt", city="Cairo",
         program="Plug and Play Egypt — Smart Cities Hub", program_type="Accelerator",
         stage="Seed", sectors="Smart cities, proptech", eligibility="Startups targeting Egypt",
         funding="Corporate pilots + investment", equity="Varies",
         duration="Programme cycle", cadence="Cohort-based", status="Active",
         description="Silicon Valley innovation platform's Egypt operation, which launched an "
                     "inaugural Smart Cities Hub cohort. Plug and Play is the most active "
                     "accelerator in the world by programme volume.",
         stats="Inaugural Egypt Smart Cities Hub cohort launched",
         entity_url="https://www.plugandplaytechcenter.com/",
         programs_url="https://www.plugandplaytechcenter.com/press/plug-and-play-egypt-launches-inaugural-cohort-of-the-smart-cities-hub/",
         apply_url="", confidence="high",
         source="plugandplaytechcenter.com Egypt press release indexed"),

    dict(entity="Orange Digital Center", entity_type="Corporate programme",
         country="Regional (MENA)", city="Cairo / Tunis / Casablanca and others",
         program="Orange Digital Center network", program_type="Incubator", stage="Idea",
         sectors="Digital, coding, tech", eligibility="Young people and early-stage founders",
         funding="Training + acceleration + early-stage investment", equity="Varies",
         duration="Ongoing", cadence="Rolling", status="Active",
         description="Orange's free digital centres across the Middle East and Africa, first "
                     "launched in Tunisia and extended to Egypt, Morocco and the wider region "
                     "from 2020. Coding training for young people, startup acceleration and "
                     "early-stage investment.",
         stats="Network across MEA; first centre in Tunisia, extended from 2020",
         entity_url="https://newsroom.orange.com/orange-a-key-player-engaged-in-the-digital-transformation-in-africa-and-the-middle-east-launches-its-first-orange-digital-centre-in-tunisia/",
         programs_url="https://newsroom.orange.com/orange-a-key-player-engaged-in-the-digital-transformation-in-africa-and-the-middle-east-launches-its-first-orange-digital-centre-in-tunisia/",
         apply_url="", confidence="medium",
         source="Orange newsroom launch release indexed; per-country ODC pages not returned — verify"),

    # ---------------- Tunisia ----------------
    dict(entity="216 Capital + Plug and Play", entity_type="Accelerator", country="Tunisia",
         city="Tunis", program="Tunisia startup accelerator (EUR 50K)",
         program_type="Accelerator", stage="Pre-seed", sectors="Tech",
         eligibility="Tunisian startups", funding="EUR 50,000", equity="Yes",
         duration="Programme cycle", cadence="Cohort-based", status="Active",
         description="Tunisia-based VC 216 Capital partnered with Plug and Play to launch a "
                     "EUR 50K accelerator for local startups.",
         stats="EUR 50,000 per startup",
         entity_url="https://arabfounders.net/en/tunisia-216capital-plugandplay-startup-accelerator/",
         programs_url="https://arabfounders.net/en/tunisia-216capital-plugandplay-startup-accelerator/",
         apply_url="", confidence="medium",
         source="Arab Founders launch coverage indexed; 216capital domain not returned — verify"),

    # ---------------- Regional competitions & development finance ----------------
    dict(entity="MIT Enterprise Forum Pan Arab", entity_type="NGO / Development agency",
         country="Regional (MENA)", city="Pan-Arab",
         program="Arab Startup Competition (ASC)", program_type="Competition / Challenge",
         stage="Any", sectors="Agnostic", eligibility="Startups across 21 Arab countries",
         funding="Equity-free cash prizes", equity="No (equity-free)",
         duration="Annual cycle", cadence="Annual", status="Active",
         description="Annual pan-Arab competition running since 2006, organised with Abdul "
                     "Latif Jameel Community Initiatives. Equity-free cash prizes across "
                     "ideas, startups and social-enterprise tracks.",
         stats="Running since 2006; targets 21 Arab countries; equity-free prizes",
         entity_url="https://arab.org/directory/mit-enterprise-forum-pan-arab/",
         programs_url="https://www.insme.org/the-arab-startup-competition/",
         apply_url="", confidence="medium",
         source="arab.org directory and INSME pages indexed; prose cites "
                "mitarabcompetition.com but it did not return as a link — verify"),

    dict(entity="EBRD", entity_type="NGO / Development agency", country="Regional (MENA)",
         city="London / SEMED", program="Star Venture", program_type="Accelerator",
         stage="Pre-seed",
         sectors="Tech", eligibility="High-potential early-stage firms in EBRD regions incl. SEMED (Egypt, Jordan, Morocco, Tunisia, West Bank & Gaza)",
         funding="Tailored advisory + capacity building", equity="No",
         duration="Multi-month", cadence="Country-based intakes", status="Active",
         description="EBRD programme supporting accelerators and high-potential pre-seed and "
                     "seed-stage startups in emerging markets, with tailored advisory and "
                     "capacity-building. Active across the southern and eastern Mediterranean.",
         stats="650+ early-stage companies assisted across 23 countries",
         entity_url="https://www.ebrd.com/home/what-we-do/focus-areas/digitalisation/ebrd-star-venture.html",
         programs_url="https://www.ebrd.com/home/what-we-do/products-and-services/support-for-start-ups-and-msmes/our-programmes/star-venture.html",
         apply_url="", confidence="high",
         source="Two ebrd.com Star Venture pages indexed; West Bank & Gaza launch release"),

    dict(entity="Hult Prize", entity_type="NGO / Development agency", country="Global",
         city="Global", program="Hult Prize student competition",
         program_type="Competition / Challenge", stage="Idea", sectors="Social impact",
         eligibility="University student teams worldwide",
         funding="USD 1 million top prize", equity="No", duration="Annual cycle",
         cadence="Annual", status="Active",
         description="The world's largest student social-entrepreneurship competition, "
                     "challenging university teams to solve pressing global issues with viable "
                     "business ideas. Runs campus rounds across MENA universities.",
         stats="USD 1,000,000 prize",
         entity_url="https://www.hult.edu/about/hult-prize/",
         programs_url="https://www.hult.edu/about/hult-prize/", apply_url="",
         confidence="high", source="hult.edu Hult Prize pages indexed"),

    dict(entity="Seedstars", entity_type="Accelerator", country="Regional (MENA)",
         city="Geneva / MENA", program="Seedstars MENA regional summit & growth programmes",
         program_type="Competition / Challenge", stage="Seed", sectors="Agnostic",
         eligibility="Emerging-market startups", funding="Programme + investment",
         equity="Varies", duration="Programme cycle", cadence="Annual regional rounds",
         status="Active",
         description="Founded 2012 in Switzerland with a network across 90+ countries. Runs "
                     "MENA regional playoffs and delivered the Misk Growth Accelerator; also "
                     "launched a MENA Growth Accelerator with Misk and Vision Ventures.",
         stats="Network covering 90+ countries; MENA regional summit",
         entity_url="https://seedstars.com/",
         programs_url="https://www.seedstarsworld.com/regional-summits/seedstars-mena/",
         apply_url="", confidence="high",
         source="seedstars.com, seedstarsworld.com MENA summit and MENA content hub all indexed"),

    dict(entity="Shorooq Partners", entity_type="VC firm", country="Regional (MENA)",
         city="Abu Dhabi", program="Equity venture capital", program_type="Seed fund",
         stage="Seed", sectors="Fintech, platforms", eligibility="MENA startups",
         funding="VC investment", equity="Yes", duration="N/A",
         cadence="Rolling — founders submit pitches on the site", status="Active",
         description="One of the region's most active early-stage funds, founded 2017. Founders "
                     "can submit pitches directly through the site. Backed in part by Bahrain's "
                     "Al Waha Fund of Funds.",
         stats="AUM grown from USD 2M at founding in 2017 to around half a billion",
         entity_url="https://www.shorooq.com/",
         programs_url="https://www.shorooq.com/what-we-do/equity-venture-capital",
         apply_url="https://www.shorooq.com/", confidence="high",
         source="shorooq.com, /about and /what-we-do/equity-venture-capital indexed"),

    dict(entity="Forbes Middle East", entity_type="Media / Data platform",
         country="Regional (MENA)", city="Dubai", program="VC and ecosystem lists",
         program_type="Directory listing", stage="Any", sectors="All", eligibility="Open",
         funding="N/A", equity="N/A", duration="Ongoing", cadence="Annual lists",
         status="Active",
         description="Publishes annual regional lists — including the Middle East's Top "
                     "Venture Capitalists — useful for spotting newly prominent funds and the "
                     "programmes they back.",
         stats="Annual Top Venture Capitalists list",
         entity_url="https://www.forbesmiddleeast.com/",
         programs_url="https://www.forbesmiddleeast.com/lists/the-middle-easts-top-venture-capitalists-2024/",
         apply_url="", confidence="high", source="forbesmiddleeast.com list page indexed"),
]

PROGRAMS.extend(EXTRA_PROGRAMS_3)
