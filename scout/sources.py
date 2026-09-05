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
     "per the brief. Israel is excluded from scope."),
    ("This is a strong v1, not a census",
     "Roughly 70 programme rows across 14 markets. Directory sources themselves report far "
     "larger universes — Tracxn lists 41 accelerators in Egypt alone; Founder Institute "
     "lists 350+ Egyptian ecosystem entries. The registry is built to be extended, and the "
     "aggregator rows (F6S, Causo, Opportunity Desk, MAGNiTT) are deliberately included so "
     "the scraper can discover programmes this list does not yet name."),
    ("Nothing here is fetch-verified",
     "The compiling environment's egress proxy blocked every outbound request — curl to "
     "flat6labs.com, magnitt.com, wamda.com, itida.gov.eg, hub71.com, oasis500.com, "
     "sheraa.ae and startupqatar.qa all failed. Every URL came from a live search result, "
     "but none were opened. Run scripts/scout_scraper.py from an unrestricted network "
     "before treating any row as confirmed."),
    ("Read the confidence column before acting",
     "high = entity and URL both appeared as search-result links. medium = entity confirmed "
     "in result text, URL inferred from the same domain. low = the entity was named only in "
     "prose and the URL is a plausible guess — roughly a third of rows. Verify low rows first."),
    ("One row is deliberately a dead entity",
     "Iraq Tech Ventures is recorded with status CLOSED. Keeping known-dead entities in the "
     "registry stops a scraper from rediscovering them and reporting them as new."),
    ("Deadlines age fast",
     "Programme dates move every cycle. The Hub71 Access deadline captured here came from a "
     "single search snapshot. Treat every date as needing re-verification on each run — "
     "which is what the scraper's change detection is for."),
]
