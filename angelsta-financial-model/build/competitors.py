"""Competitor and comparable dataset, built from the supplied Angelsta SaaS Marketing Competitive Analysis
(research cut-off 19 August 2026) plus public sources found in November 2026."""

MODULES = ["Data room", "Cap table", "ESOP", "Model and valuation", "KPI tracking", "Deal pipeline",
           "Portfolio management", "Startup tracking", "Deal matching", "Investor cap table", "Exit scenarios"]
FOUNDER_MODS = 6   # first six are founder side, last five investor side

# name: (region, hq, founded, side, category, threat, coverage string F/P/N over MODULES, source of coverage)
# coverage source "S12" = supplied 11-module matrix; "A" = Angelsta analyst mapping from the supplied feature matrices
COVER = {
    "Angelsta": ("Egypt and GCC", "Cairo, Egypt", 2025, "Both", "Founder and investor OS", "-", "FFFFFFFFFFF", "Product scope"),
    "RasMal": ("GCC", "Riyadh, Saudi Arabia", 2019, "Both", "Equity management", "Critical", "FFFFPFFFPFP", "S12"),
    "Govy": ("GCC", "Saudi Arabia", None, "Founder", "Equity management", "Critical", "FFFNNFNNNPN", "S12"),
    "EquityList": ("MENA serving", "Singapore and India", 2021, "Founder", "Equity management", "Critical", "FFFFNNPNNFP", "S12"),
    "MAGNiTT": ("GCC", "Dubai, UAE", 2013, "Investor", "Market data", "High", "NNNNNPNFFNN", "S12"),
    "Pentugram": ("GCC", "Riyadh, Saudi Arabia", None, "Investor", "Portfolio monitoring", "High", "NNNNPNFFPPN", "S12"),
    "Qapita": ("Emerging markets", "Singapore", 2019, "Founder", "Equity management", "High", "FFFFNNPNNFF", "S12"),
    "Carta": ("Global", "San Francisco, USA", 2012, "Both", "Equity management", "Critical", "FFFFPNFFNFF", "S12"),
    "Pulley": ("Global", "San Francisco, USA", 2019, "Founder", "Equity management", "High", "PFFFNNNNNFF", "S12"),
    "Eqvista": ("Global", "Nevada, USA", 2018, "Founder", "Equity management", "High", "PFFFNNNNNFF", "S12"),
    "AngelList": ("Global", "San Francisco, USA", 2010, "Both", "Fund admin and SPV", "High", "PFPNNPFPPFP", "S12"),
    "Visible": ("Global", "Detroit, USA", 2014, "Both", "Portfolio monitoring", "Critical", "PNNNFFFFNNN", "S12"),
    "Standard Metrics": ("Global", "San Francisco, USA", 2019, "Investor", "Portfolio monitoring", "High", "NNNNFNFFNPP", "S12"),
    "Affinity": ("Global", "San Francisco, USA", 2014, "Investor", "Investor CRM", "High", "NNNNPNPFFNN", "S12"),
    "Foundersuite": ("Global", "San Francisco, USA", 2016, "Founder", "Fundraising CRM", "High", "PNNNPFNNPNN", "S12"),
    "OpenVC": ("Global", "Remote, France", 2020, "Founder", "Fundraising CRM", "High", "NNNNNFNPFNN", "S12"),
    "DocSend": ("Global", "San Francisco, USA", 2013, "Founder", "Data room", "High", "FNNNNPNNNNN", "S12"),
    "Papermark": ("Global", "Berlin, Germany", 2023, "Founder", "Data room", "Moderate", "FNNNNPNNNNN", "S12"),
    "Ledgy": ("Emerging markets", "Zurich, Switzerland", 2017, "Founder", "Equity management", "Moderate", "PFFPNNNNNFP", "S12"),
    "Cake Equity": ("Emerging markets", "Brisbane, Australia", 2019, "Founder", "Equity management", "Moderate", "PFFPNNNNNFP", "S12"),
    "Trica Equity": ("Emerging markets", "Bengaluru, India", 2016, "Founder", "Equity management", "Moderate", "PFFPNNPNPFP", "S12"),
    "Rundit": ("Emerging markets", "Helsinki, Finland", 2019, "Investor", "Portfolio monitoring", "Moderate", "NNNNFNFFNPP", "S12"),
    "Vestberry": ("Emerging markets", "Bratislava, Slovakia", 2016, "Investor", "Portfolio monitoring", "Moderate", "NNNNFNFFNPP", "S12"),
    "Edda": ("Emerging markets", "New York and Paris", 2017, "Investor", "Investor CRM", "Moderate", "PNNNPNFFFPN", "S12"),
    "Dealroom": ("Emerging markets", "Amsterdam, Netherlands", 2013, "Investor", "Market data", "Moderate", "NNNNPNPFFNN", "S12"),
    "Causal": ("Global", "London, UK", 2019, "Founder", "FP&A and modelling", "Moderate", "NNNFFNNNNNN", "S12"),
    "Jirav": ("Global", "San Francisco, USA", 2015, "Founder", "FP&A and modelling", "Moderate", "NNNFFNNNNNN", "S12"),
    "Trackify": ("Africa", "Africa", None, "Both", "Founder and investor OS", "High", "FNNPFFFFPNN", "A"),
    "Capital Connect Africa": ("Africa", "Nairobi, Kenya", 2022, "Both", "Readiness and matching", "Moderate", "FNNFPFPPFNN", "A"),
    "Dynamo": ("Global and GCC", "USA, Dubai office 2022", 1998, "Investor", "Portfolio monitoring", "High", "PNNPPPFFNPP", "A"),
    "Clara": ("GCC", "Dubai and Abu Dhabi", None, "Founder", "Legal and company admin", "High", "FFPNNPNNNPN", "A"),
    "Equidam": ("Global", "Netherlands", 2013, "Founder", "Valuation", "High", "NNNFNNPNNNP", "A"),
    "Lemina": ("Africa", "Nigeria", None, "Investor", "Market data", "Moderate", "NNNNPNFFPNN", "A"),
    "FundNaija": ("Africa", "Nigeria", None, "Founder", "Readiness and matching", "Low", "NNNPPNNNPNN", "A"),
}

# Competitive scores from the supplied primary research, section 7 (1 to 5; total out of 40)
SCORES = {  # overlap, MENA, startup, investor, AI, ease, pricing access, traction, total
    "Visible": (4.5, 2.5, 4.5, 4.5, 4.0, 4.5, 5.0, 4.5, 34.0),
    "Trackify": (4.5, 3.0, 4.5, 4.5, 4.5, 4.0, 2.5, 2.5, 30.0),
    "Equidam": (2.8, 2.0, 4.0, 2.8, 4.0, 4.5, 5.0, 5.0, 30.1),
    "Standard Metrics": (3.8, 2.5, 2.5, 5.0, 5.0, 4.0, 1.5, 5.0, 29.3),
    "Foundersuite": (3.0, 2.0, 5.0, 1.5, 2.5, 4.5, 5.0, 5.0, 28.5),
    "MAGNiTT": (2.5, 5.0, 2.5, 4.0, 4.0, 4.0, 1.5, 4.5, 28.0),
    "Papermark": (2.4, 2.0, 3.5, 2.5, 3.0, 5.0, 5.0, 4.8, 28.2),
    "Dynamo": (3.6, 4.5, 1.5, 5.0, 4.5, 2.5, 1.0, 5.0, 27.6),
    "Capital Connect Africa": (3.5, 1.0, 4.3, 3.2, 3.0, 4.0, 5.0, 2.8, 26.8),
    "Clara": (2.8, 5.0, 4.0, 2.5, 1.5, 4.0, 2.5, 4.5, 26.8),
    "Vestberry": (3.4, 2.0, 1.5, 5.0, 4.5, 4.0, 1.5, 4.8, 26.7),
    "Rundit": (3.1, 2.0, 1.5, 4.8, 4.0, 4.5, 1.5, 4.5, 25.9),
}
SCORE_DIMS = ["Product overlap", "MENA relevance", "Startup side", "Investor side", "AI and data", "Ease of use", "Pricing access", "Traction"]

# Entry paid price, USD per month, lowest published paid plan (annual billing where offered). None = quote based.
PRICE = {
    "Angelsta Pro": (49, "Founder", "Angelsta"), "Angelsta Team": (124, "Founder", "Angelsta"),
    "Angelsta Angel": (65, "Investor", "Angelsta"), "Angelsta Institutional": (499, "Investor", "Angelsta"),
    "Govy": (25, "Founder", "Govy $24.99 a month flat"), "OpenVC": (25, "Founder", "Paid $25 to $99 a month"),
    "Papermark": (26, "Founder", "EUR 24 Pro"), "Equidam": (34, "Founder", "Advanced $412.25 a year"),
    "Capital Connect Africa": (50, "Founder", "$49.99 investor database"), "Visible": (59, "Founder", "$59 a month annual"),
    "Foundersuite": (62, "Founder", "$745 a year"), "Cake Equity": (83, "Founder", "Build about $1,000 a year"),
    "Eqvista": (83, "Founder", "Bundles from $990 a year"), "Pulley": (100, "Founder", "$1,200 a year"),
    "Carta": (133, "Founder", "Build about $1,600 a year"), "Ledgy": (163, "Founder", "EUR 150 a month"),
    "Crunchbase": (49, "Investor", "Pro about $49 a user a month"), "Affinity": (167, "Investor", "$2,000 a user a year"),
    "MAGNiTT": (200, "Investor", "From $2,400 a year"), "Tracxn": (417, "Investor", "From $5,000 a year"),
    "Visible investors": (449, "Investor", "Reported, quote based"), "Zapflow": (495, "Investor", "Pro, 5 users"),
    "Digify": (480, "Investor", "Team plan"), "PitchBook": (1000, "Investor", "From $12,000 a year"),
    "Dealroom": (1667, "Investor", "From $20,000 a year"),
}
# Coverage key for the value map (price name -> coverage name)
PRICE_COVER = {"Angelsta Pro": "Angelsta", "Angelsta Institutional": "Angelsta", "Govy": "Govy", "OpenVC": "OpenVC", "Papermark": "Papermark",
               "Equidam": "Equidam", "Capital Connect Africa": "Capital Connect Africa", "Visible": "Visible", "Foundersuite": "Foundersuite",
               "Cake Equity": "Cake Equity", "Eqvista": "Eqvista", "Pulley": "Pulley", "Carta": "Carta", "Ledgy": "Ledgy",
               "Affinity": "Affinity", "MAGNiTT": "MAGNiTT", "Dealroom": "Dealroom"}

# Funding raised, USD millions, disclosed
FUNDING = [("Qapita", 79.3, "Total raised, Series B $26.5m led by Charles Schwab, Oct 2025"),
           ("Standard Metrics", 23.7, "Series A, 2022"), ("RasMal", 4.8, "Pre-Series A, SAR 18m, LEAP 2025"),
           ("Clara", 3.5, "Seed, 500 Startups, Techstars, DIFC; acquired by Ascentium, Feb 2026"),
           ("EquityList", 2.2, "Seed, AngelList India, Hustle Fund and others"), ("MAGNiTT", 1.0, "Close to $1m, international and Gulf investors")]

# Transaction comparables, disclosed value USD millions
DEALS = [("Preqin by BlackRock", 2024, 3200, "Private markets data"), ("PitchBook by Morningstar", 2016, 225, "Private markets data, implied value"),
         ("DocSend by Dropbox", 2021, 165, "Data rooms"), ("Pry by Brex", 2022, 90, "Startup financial planning")]
DEALS_UNDISCLOSED = [("Global Shares by J.P. Morgan", 2022, "Equity plan administration"), ("Causal by Lucanet", 2024, "Startup financial modelling"),
                     ("Finmark by BILL", 2022, "Startup financial planning, sunset April 2026"), ("Clara by Ascentium", 2026, "MENA company formation and equity admin"),
                     ("LTSE Equity customers to Astrella", 2024, "Cap table, market exit"), ("Capshare by Solium", 2017, "Cap table")]

# Valuation benchmarks
MULTIPLES = [("Public SaaS, Q1 2026, Aventis", 3.4), ("Public SaaS, 2Q 2026, SEG", 3.2),
             ("Private SaaS M&A, 2Q 2026, SEG", 4.0), ("Private SaaS M&A, Q1 2026, Aventis", 3.1),
             ("Private vertical B2B SaaS, 2015 to 2025", 4.7), ("Angelsta model, central exit", 4.0)]

# Full directory, from the supplied analysis section 13 plus additions. (name, region, hq, side, category, threat, pricing, note)
DIRECTORY = [
    # Egypt and North Africa
    ("Cairo Angels", "Egypt", "Cairo", "Investor", "Angel network", "Partner", "Membership", "Egypt's first formal angel network, about 50 active angels; syndicate fund writes $100k to $250k. Target customer and channel."),
    ("AUC Angels", "Egypt", "Cairo", "Investor", "Angel network", "Partner", "Membership", "First university based angel network in MENA. Target customer and channel."),
    ("Fabeh", "Egypt and MENA", "MENA", "Both", "Deal marketplace", "Moderate", "Transaction based", "Lists deals; no cap table, portfolio or AI layer per Angelsta deck."),
    ("Thanawi", "MENA", "MENA", "Both", "Deal marketplace", "Moderate", "Transaction based", "Secondary and deal listing positioning; no operating system."),
    ("Finstreet", "MENA", "MENA", "Investor", "Deal marketplace", "Moderate", "Transaction based", "Investment marketplace positioning."),
    ("GetEquity", "Africa", "Lagos, Nigeria", "Investor", "Deal marketplace", "Moderate", "Transaction based", "Retail private market investing marketplace."),
    ("Thndr", "Egypt", "Cairo", "Investor", "Retail investing app", "Low", "Free and commissions", "4m+ users, $15.7m round led by Prosus 2025; public markets, adjacent only."),
    # Qatar and GCC
    ("RasMal", "GCC", "Riyadh", "Both", "Equity management", "Critical", "Not disclosed", "$4.8m pre-Series A at LEAP 2025; cap table, ESOP, valuation, data rooms; Pentugram for investors."),
    ("Pentugram", "GCC", "Riyadh", "Investor", "Portfolio monitoring", "High", "Not disclosed", "RasMal's investor arm: deal flow and investor reporting for Gulf VCs and angels."),
    ("Govy", "GCC", "Saudi Arabia", "Founder", "Equity management", "Critical", "$24.99 a month flat", "Cap table, ESOP, governance, data room; Arabic RTL in progress."),
    ("EquityList", "MENA serving", "Singapore and India", "Founder", "Equity management", "Critical", "Quote by stakeholders", "$2.2m seed; counts Tabby as a customer."),
    ("MAGNiTT", "GCC", "Dubai", "Investor", "Market data", "High", "$2,400 to $30,000+ a year", "Reference MENA venture dataset; 25 staff."),
    ("Clara", "GCC", "Dubai and Abu Dhabi", "Founder", "Legal and company admin", "High", "Not disclosed", "5,000+ businesses; acquired by Ascentium, Feb 2026."),
    ("Dynamo", "Global and GCC", "Dubai office", "Investor", "Portfolio monitoring", "High", "Quote", "Enterprise alternative assets software; Dubai since 2022."),
    ("Numu Angels", "GCC", "Riyadh", "Investor", "Angel network", "Moderate", "Membership", "Built its own investor tooling."),
    ("OQAL Angel Investors Network", "GCC", "Riyadh", "Investor", "Angel network", "Moderate", "Membership", "600+ registered Saudi angels."),
    ("Jeddah Angels", "GCC", "Jeddah", "Investor", "Angel network", "Low", "Membership", "Launched January 2025."),
    ("Eureeca", "GCC", "Dubai, DIFC", "Both", "Equity crowdfunding", "Low", "Success fee", "Regulated DFSA, FCA, AFM; raises $300k to $800k."),
    ("Sharikat Mubasher", "GCC", "Riyadh", "Investor", "Media and directory", "Low", "Free and advertising", "KSA SME and PE news and directory."),
    ("CFO.Ventures", "GCC", "Dubai", "Founder", "Advisory service", "Low", "Retainer", "Outsourced CFO with cap table as a service."),
    ("Aranca", "GCC", "Dubai and Mumbai", "Founder", "Advisory service", "Low", "Project fees", "Valuation and 409A advisory incumbent."),
    ("Rasmal Ventures", "Qatar", "Doha", "Investor", "Venture fund", "Partner", "Fund", "Qatar's first independent VC; first fund in QIA's Fund of Funds. Target Institutional customer."),
    ("Qatar FinTech Hub, QDB, QSTP", "Qatar", "Doha", "Both", "Ecosystem programme", "Partner", "Programme", "Accelerator and ecosystem channels for Qatar founders."),
    # Africa
    ("Trackify", "Africa", "Africa", "Both", "Founder and investor OS", "High", "Not public", "Founder OS and Investor OS; 1,000+ monthly active users reported."),
    ("Capital Connect Africa", "Africa", "Nairobi", "Both", "Readiness and matching", "Moderate", "Free; $49.99 to $99.99 services", "5,200+ investors in database."),
    ("Lemina", "Africa", "Nigeria", "Investor", "Market data", "Moderate", "Not stated", "998+ African tech companies database; AI diligence."),
    ("FundNaija", "Africa", "Nigeria", "Founder", "Readiness and matching", "Low", "Not stated", "1,173 founders reported."),
    ("Confluence Africa", "Africa", "Africa", "Founder", "Advisory service", "Low", "Not stated", "Fundraising advisory alternative."),
    # Emerging and regional
    ("Qapita", "Emerging markets", "Singapore", "Founder", "Equity management", "High", "Quote", "$26.5m Series B led by Charles Schwab, Oct 2025."),
    ("Trica Equity", "Emerging markets", "Bengaluru", "Founder", "Equity management", "Moderate", "Quote", "800+ companies; LetsVenture group."),
    ("Hissa", "Emerging markets", "Bengaluru", "Founder", "Equity management", "Low", "Quote", "Indian equity platform."),
    ("Cake Equity", "Emerging markets", "Brisbane", "Founder", "Equity management", "Moderate", "From about $50 a month", "4.8 of 5 on G2."),
    ("Ledgy", "Emerging markets", "Zurich", "Founder", "Equity management", "Moderate", "EUR 150 to 400 a month", "70+ HRIS integrations."),
    ("Vestd", "Emerging markets", "United Kingdom", "Founder", "Equity management", "Low", "From low hundreds GBP", "UK EMI focus."),
    ("Rundit", "Emerging markets", "Helsinki", "Investor", "Portfolio monitoring", "Moderate", "Quote by fund size", "4,500+ fund managers in 35+ countries; Launch Africa a customer."),
    ("Vestberry", "Emerging markets", "Bratislava", "Investor", "Portfolio monitoring", "Moderate", "Enterprise quote", "500+ funds, $45bn+ AUM."),
    ("Edda", "Emerging markets", "New York and Paris", "Investor", "Investor CRM", "Moderate", "Quote", "Deal flow plus portfolio."),
    ("Dealroom", "Emerging markets", "Amsterdam", "Investor", "Market data", "Moderate", "$20,000+ a year", "European ecosystem data; thin in MENA."),
    ("Tracxn", "Emerging markets", "Bengaluru", "Investor", "Market data", "Moderate", "$5,000 to $20,000 a year", "Listed in India; covers MENA."),
    ("Waveup", "Emerging markets", "Remote, Europe", "Founder", "Advisory service", "Low", "$100 to $5,000+", "Pitch deck and valuation agency."),
    # Global
    ("Carta", "Global", "San Francisco", "Both", "Equity management", "Critical", "Build about $1,600 a year", "$500m ARR 2025; ~35,000 startups; $3.5bn secondary valuation."),
    ("Pulley", "Global", "San Francisco", "Founder", "Equity management", "High", "$1,200 to $3,500 a year", "4.7 on G2."),
    ("AngelList", "Global", "San Francisco", "Both", "Fund admin and SPV", "High", "Free under $1m; fund fees", "$170bn+ assets on platform; US entities only."),
    ("Visible", "Global", "Detroit", "Both", "Portfolio monitoring", "Critical", "Founders $59 to $249 a month", "7,050+ founders and VC funds."),
    ("Standard Metrics", "Global", "San Francisco", "Investor", "Portfolio monitoring", "High", "Quote", "$23.7m Series A; 150+ VC and PE firms, 10,000+ companies; SOC 2."),
    ("Affinity", "Global", "San Francisco", "Investor", "Investor CRM", "High", "$2,000 to $2,700 a user a year", "3,000+ customers in 70+ countries."),
    ("Foundersuite", "Global", "San Francisco", "Founder", "Fundraising CRM", "High", "$745 to $1,609 a year", "100,000+ users, $21bn raised."),
    ("OpenVC", "Global", "Remote", "Founder", "Fundraising CRM", "High", "Free; $25 to $99 a month", "15,000+ verified investors."),
    ("Flowlie", "Global", "New York", "Founder", "Fundraising CRM", "Moderate", "Freemium", "AI investor matching."),
    ("Metal", "Global", "New York", "Founder", "Fundraising CRM", "Low", "Freemium", "Intro pathway intelligence."),
    ("Equidam", "Global", "Netherlands", "Founder", "Valuation", "High", "$412 to $1,990 a year", "160,000 companies valued in 90 countries."),
    ("Eqvista", "Global", "Nevada", "Founder", "Equity management", "High", "Free to 20 holders; $990+ a year", "Aggressive pricing."),
    ("Astrella", "Global", "USA", "Founder", "Equity management", "Moderate", "Tiered", "Took over LTSE Equity customers."),
    ("Morgan Stanley at Work", "Global", "USA", "Founder", "Equity management", "Low", "Enterprise", "Late stage and public."),
    ("Global Shares, J.P. Morgan", "Global", "Cork", "Founder", "Equity management", "Low", "Enterprise", "Acquired by J.P. Morgan 2022."),
    ("Fidelity Private Shares", "Global", "USA", "Founder", "Equity management", "Low", "Bundled", "Distribution led."),
    ("DocSend", "Global", "San Francisco", "Founder", "Data room", "High", "From $15 a user a month", "Acquired by Dropbox for $165m."),
    ("Papermark", "Global", "Berlin", "Founder", "Data room", "Moderate", "EUR 24 to 99 a month", "Open source; SOC 2 Type II, ISO 27001."),
    ("Digify", "Global", "Singapore", "Founder", "Data room", "Moderate", "From $480 a month", "SMB and mid-market VDR."),
    ("Ansarada", "Global", "Sydney", "Investor", "Data room", "Low", "$244 to $5,134 a month", "M&A VDR."),
    ("Datasite, Intralinks, Firmex, iDeals", "Global", "USA, Canada, UK", "Investor", "Data room", "Low", "Per deal or enterprise", "M&A virtual data rooms, upmarket."),
    ("PitchBook", "Global", "Seattle", "Investor", "Market data", "Moderate", "$12,000 to $70,000+ a year", "Thin MENA coverage."),
    ("Crunchbase", "Global", "San Francisco", "Investor", "Market data", "Low", "Free; Pro about $49 a month", "MENA data often incomplete."),
    ("CB Insights", "Global", "New York", "Investor", "Market data", "Low", "Enterprise", "Corporate research."),
    ("Preqin", "Global", "London", "Investor", "Market data", "Low", "Enterprise", "Acquired by BlackRock, about $3.2bn."),
    ("DealCloud, Intapp", "Global", "Palo Alto", "Investor", "Investor CRM", "Moderate", "$2,000+ a user a year", "Mid-market and large PE."),
    ("Juniper Square", "Global", "San Francisco", "Investor", "Fund admin and LP portal", "Low", "Enterprise", "Valued above $1bn."),
    ("Allvue Systems", "Global", "Miami", "Investor", "Fund admin and LP portal", "Low", "Enterprise", "Vista owned."),
    ("Chronograph", "Global", "New York", "Investor", "Portfolio monitoring", "Low", "Enterprise", "LP look-through."),
    ("Causal, Lucanet", "Global", "London", "Founder", "FP&A and modelling", "Moderate", "Was $250 a month", "Acquired by Lucanet, Oct 2024."),
    ("Finmark, BILL", "Global", "Raleigh", "Founder", "FP&A and modelling", "Low", "Was from $50 a month", "Sunset April 2026: a gap below $300 a month."),
    ("Pry, Brex", "Global", "San Francisco", "Founder", "FP&A and modelling", "Low", "Bundled", "Acquired by Brex for $90m."),
    ("Jirav", "Global", "San Francisco", "Founder", "FP&A and modelling", "Moderate", "Quote", "Fractional CFO channel."),
    ("Forecastr", "Global", "Louisville", "Founder", "FP&A and modelling", "Moderate", "Tiered plus analysts", "Fundraising models with analysts."),
    ("Sturppy", "Global", "Denver", "Founder", "FP&A and modelling", "Low", "Low cost", "Model in ten minutes."),
    ("Abacum, Cube, Mosaic, Pigment", "Global", "USA and Europe", "Founder", "FP&A and modelling", "Low", "From $1,500 a month", "Series B+ finance teams."),
    ("Sydecar", "Global", "San Francisco", "Investor", "Fund admin and SPV", "Low", "Flat fee per SPV", "Syndicate SPVs."),
    ("Allocations", "Global", "Miami", "Investor", "Fund admin and SPV", "Low", "Per vehicle", "Fast SPV launch."),
    ("Bunch", "Global", "Berlin", "Investor", "Fund admin and SPV", "Low", "Quote per fund", "European emerging managers."),
    ("Excel, Google Drive, Notion", "Everywhere", "-", "Both", "Manual alternative", "Critical", "Free", "The real incumbent: spreadsheets, folders and email."),
]

REGION_ORDER = ["Egypt", "Egypt and MENA", "Qatar", "GCC", "MENA", "MENA serving", "Global and GCC", "Africa", "Emerging markets", "Global", "Everywhere"]

# Ecosystem figures used in charts (USD millions)
ECOSYSTEM = [("MENA venture, 2025", 3800, "MAGNiTT FY2025, 688 deals"), ("Saudi Arabia", 1720, "MAGNiTT, 257 deals"),
             ("UAE", 1580, "Arab News, 231 deals"), ("Egypt", 304, "MAGNiTT, 69 VC deals; $614m incl. debt per ministry"),
             ("Qatar", 59, "QDB and MAGNiTT, QR214m record, +81%"), ("Africa, equity and debt", 4100, "Partech 2025, ~570 deals")]


def coverage_score(code):
    v = {"F": 1.0, "P": 0.5, "N": 0.0}
    f = sum(v[c] for c in code[:FOUNDER_MODS])
    i = sum(v[c] for c in code[FOUNDER_MODS:])
    return f, i, f + i
