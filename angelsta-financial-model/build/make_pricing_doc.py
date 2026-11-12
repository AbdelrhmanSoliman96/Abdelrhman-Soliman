import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import params as P

TEAL = RGBColor(0x0D, 0x2B, 0x30)
ACCENT = RGBColor(0x2E, 0x7D, 0x74)
GREY = RGBColor(0x5F, 0x67, 0x70)

doc = Document()
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2.0)
    s.top_margin = s.bottom_margin = Cm(1.8)

st = doc.styles["Normal"]
st.font.name = "Arial"
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
st.font.size = Pt(10)
for name, size, color in [("Heading 1", 16, TEAL), ("Heading 2", 12.5, ACCENT), ("Heading 3", 11, TEAL)]:
    h = doc.styles[name]
    h.font.name = "Arial"
    h.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    h.font.size = Pt(size)
    h.font.bold = True
    h.font.color.rgb = color


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def para(text, bold=False, italic=False, color=None, size=None, align=None, space_after=4):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if color:
        r.font.color.rgb = color
    if size:
        r.font.size = Pt(size)
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p


def bullets(items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        if isinstance(it, tuple):
            r = p.add_run(it[0])
            r.bold = True
            p.add_run(it[1])
        else:
            p.add_run(it)
        p.paragraph_format.space_after = Pt(2)


def table(rows, widths=None, header_fill="0D2B30", first_col_bold=False, font=8.5, zebra=True):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = ""
            p = c.paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(font)
            if i == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                shade(c, header_fill)
            else:
                if first_col_bold and j == 0:
                    r.bold = True
                if zebra and i % 2 == 0:
                    shade(c, "EEF5F4")
    if widths:
        for row in t.rows:
            for j, w in enumerate(widths):
                row.cells[j].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def usd(x):
    return "Free" if x == 0 else f"${x:,.0f}"


S, I = P.STARTUP, P.INVESTOR

# ---------------- Cover ----------------
para("Angelsta", bold=True, size=28, color=TEAL, space_after=0)
para("Pricing Strategy, Founders and Investors", size=15, color=ACCENT, space_after=2)
para("The freemium subscription model that the 2027 to 2031 financial model is built on", italic=True, color=GREY, space_after=14)
table([
    ["Document", "Pricing strategy and the pricing assumptions used by the financial model"],
    ["Company", "Angelsta, the operating system for private investors and founders, Cairo and the GCC"],
    ["Prepared", "November 2026, for the pre-seed financial model v1.0"],
    ["Currency", "US dollars, GCC list price. Egypt price list at 60 per cent of list"],
    ["Status", "Recommended pricing. Prices are inputs on the Assumption Setting sheet and can be changed there"],
], widths=[3.5, 13.5], first_col_bold=True, zebra=False)

# ---------------- 1. Executive summary ----------------
doc.add_heading("1. Executive summary", level=1)
para("Angelsta sells two products that share one record: a founder workspace (cap table, data room, investor updates, "
     "valuation and exit scenarios) and an investor portfolio operating system (live portfolio, MOIC, TVPI, DPI and IRR, stress tests, deal access). "
     "Both sides start free, because each free founder brings their investors onto the platform and each investor brings deal flow. "
     "That network is what Angelsta has that the deal marketplaces do not. Revenue comes from subscriptions. Paid plans unlock the AI layer: valuations, "
     "stress scenarios, the diligence and portfolio agents, and matching. They also unlock the controls a raising company or a fund needs: permissions, NDA gating and the audit trail.")
para("Recommended price list in USD. Every plan can be paid monthly or annually; the annual plan saves about 17 per cent, two months free.", bold=True)
table([
    ["Founders, priced per company", "Free", "Pro", "Team", "Custom"],
    ["Monthly plan, per month", "$0", usd(S["Pro"]["monthly"][0]), usd(S["Team"]["monthly"][0]), "From " + usd(S["Custom"]["monthly"][0])],
    ["Annual plan, per month", "$0", usd(S["Pro"]["annual"][0]), usd(S["Team"]["annual"][0]), "From " + usd(S["Custom"]["annual"][0])],
    ["Annual plan, per year", "$0", usd(S["Pro"]["annual"][0]*12), usd(S["Team"]["annual"][0]*12), "From " + usd(S["Custom"]["annual"][0]*12)],
    ["How it is bought", "Sign up", "Self-serve, 14-day trial", "Self-serve or demo, 14-day trial", "Demo and proposal"],
], widths=[4.4, 2.2, 3.2, 3.6, 3.6], first_col_bold=True)
table([
    ["Investors, priced per account", "Free", "Angel", "Institutional", "Custom"],
    ["Monthly plan, per month", "$0", usd(I["Angel"]["monthly"][0]), usd(I["Institutional"]["monthly"][0]) + " base", "From " + usd(I["Custom"]["monthly"][0])],
    ["Annual plan, per month", "$0", usd(I["Angel"]["annual"][0]), usd(I["Institutional"]["annual"][0]) + " base", "From " + usd(I["Custom"]["annual"][0])],
    ["Annual plan, per year", "$0", usd(I["Angel"]["annual"][0]*12), usd(I["Institutional"]["annual"][0]*12) + " base", "From " + usd(I["Custom"]["annual"][0]*12)],
    ["Included", "5 holdings", "40 holdings, 2 seats", "50 companies, 5 seats", "Unlimited, multi-fund"],
    ["How it is bought", "Sign up", "Self-serve, 14-day trial", "Demo and 30-day guided pilot", "Demo, pilot and proposal"],
], widths=[4.4, 2.2, 3.2, 3.6, 3.6], first_col_bold=True)
para("Six decisions shape the model:", bold=True)
bullets([
    ("Founders and investors have separate price lists. ", "A startup buys one company workspace. An investor buys an account that holds many companies, so investor prices scale with seats and with the number of portfolio companies tracked."),
    ("Institutional is a single plan for family offices, venture capital, private equity, corporate venture and angel networks. ", "Price scales with use, at $49 per extra seat and $10 per extra portfolio company. A separate plan per investor type would add sales friction without adding revenue."),
    ("Paying annually saves about 17 per cent, which is two months free. ", "Annual billing reduces churn and brings cash in up front. The model assumes 25 per cent of self-serve accounts pay annually in 2027, rising to 40 per cent, and 70 to 80 per cent of sales-led accounts."),
    ("Egypt has its own price list at 60 per cent of the GCC list, billed in pounds. ", "The model assumes Egypt is 55 per cent of paying accounts in 2027, falling to 22 per cent by 2031 as KSA and the UAE open."),
    ("Prices are low on purpose against the US tools. ", "Founder Pro is about a third of Carta's or Pulley's entry price, and Institutional is below Affinity for a single user. These are launch prices. The model raises them by 5 to 9 per cent a year from 2029, and existing annual customers keep their price until renewal."),
    ("The base case is subscription only. ", "Add-ons are built into the model behind a switch that is off in the base case: AI credit top-ups, analyst-reviewed valuation reports, white-label licences, syndicate and SPV administration, and event sponsorship."),
])

# ---------------- 2. Market evidence ----------------
doc.add_heading("2. What the market charges today", level=1)
para("Most private-market software is priced for US customers and quoted only on request. The published and widely reported figures below anchor what a MENA founder or investor will compare Angelsta against. "
     "Third-party sites often disagree with each other, so every figure should be read as an indication of the range, not a list price.", italic=True, color=GREY)
doc.add_heading("2.1 Founder side: cap table, data room and investor updates", level=2)
table([
    ["Product", "Entry paid plan", "Higher plans", "Free plan", "What it means for Angelsta"],
    ["Carta", "Build about $1,600/yr plus $80 per stakeholder after 20", "Grow about $3,900/yr; Scale quoted", "Launch: free to 25 stakeholders and $1m raised", "The global anchor. Angelsta Pro at $588/yr is about a third of Carta Build."],
    ["Pulley", "Startup $1,200/yr, annual billing only", "Growth about $3,500/yr; Enterprise quoted", "None", "Angelsta Team at $1,488/yr is close to Pulley's entry price but also includes the data room, valuation and AI agents."],
    ["Cake Equity", "Build about $1,000/yr", "Team about $2,750/yr; Pro quoted", "Limited", "Confirms the $1,000 to $3,000 a year band for cap table software."],
    ["Eqvista", "Free to 20 shareholders, then $2 per shareholder per month", "Valuation bundles $990 to $2,590/yr", "Yes", "Valuation is the item buyers pay for most clearly. Angelsta includes it in Pro."],
    ["Visible", "Founders: Base $59/mo, Core $129 to $149/mo", "Top founder plan about $199 to $249/mo", "Starter, free", "Investor updates alone sell for $59 to $249 a month. Angelsta includes the Update Writer agent in Pro and Team."],
    ["AngelList (startups)", "Starter about $1,600/yr", "Fund admin 0.1 to 0.75% of fund size plus a fee", "Free for investors", "Sets the expectation that investors should not pay to view a cap table, which Angelsta's free investor plan meets."],
], widths=[2.3, 3.6, 3.4, 3.0, 4.9], font=7.8)
doc.add_heading("2.2 Investor side: portfolio monitoring, deal flow and reporting", level=2)
table([
    ["Product", "Published or reported price", "Pricing unit", "What it means for Angelsta"],
    ["Affinity (relationship CRM for VC)", "$2,000 to $2,700 per user per year", "Per user", "One Affinity seat costs about a third of Angelsta Institutional for a whole team of five."],
    ["Zapflow (deal flow and portfolio)", "Starter $99/mo for 1 user; Pro $495/mo for 5 users; Enterprise $3,995/mo for 15 users", "Seats included", "The closest structural match. Angelsta Institutional at $499 to $599 a month for 5 seats sits at Zapflow Pro's level and adds valuation and stress testing."],
    ["Visible for Investors", "Custom pricing; reported around $449/mo", "Per firm", "Confirms $400 to $600 a month as the entry price for portfolio monitoring."],
    ["Synaptic (portfolio data)", "Essentials about $99 per portfolio company per year", "Per portfolio company", "Supports charging $10 a month per portfolio company above the 50 included."],
    ["Standard Metrics, Vestberry, Allvue", "Enterprise, quoted on request", "Per fund", "Built for large funds. Angelsta's Custom plan competes here only for MENA funds that need Arabic, local data residency and LP reporting."],
    ["FundCount (PE accounting)", "From about $38,000 per year", "Per firm", "A ceiling. PE fund administration is not Angelsta's product, but it shows what institutions pay."],
    ["Emerging manager budgets", "About $1k for a $15m fund, $7k for $30m, $12k for $75m", "Annual portfolio tool budget", "Places Institutional at $5,988 a year inside the budget of a $30m to $75m MENA fund."],
], widths=[3.4, 4.6, 2.4, 6.8], font=7.8)
doc.add_heading("2.3 The MENA market these prices sell into", level=2)
bullets([
    "MENA venture funding reached $3.8bn across 688 deals in 2025, up 74 per cent in value (MAGNiTT FY2025). Wamda counts 647 startups raising $7.5bn in the same year on a broader definition.",
    "Saudi Arabia led the region by deal count for the first time, with $1.72bn across 257 deals. The UAE had 231 deals. Together the two countries took 86 per cent of funding, which is why the model opens KSA in month 7 and the UAE in month 13.",
    "58 per cent of MENA family groups are active in venture, and about 70 per cent source deals through their own networks. Angelsta's Institutional plan, with its community and deal-flow layer, is built for this buyer.",
    "Angel networks are concentrated and reachable. OQAL alone reports 100 to 200 members, and Saudi Arabia hosts more than 65 VC firms, angel groups and accelerators. Partnering with networks and accelerators is the cheapest channel for both sides of the market.",
    "Freemium benchmarks: free-to-paid conversion averages 2.6 to 3.7 per cent for traditional freemium (First Page Sage, 80+ SaaS companies) and 3 to 5 per cent for SMB-focused B2B SaaS. Companies that use product-qualified leads convert about three times better.",
    "Churn benchmarks: SMB SaaS loses 3 to 7 per cent of accounts a month, mid-market 1 to 3 per cent, and enterprise 0.5 to 1 per cent. The model's churn starts at these levels and improves as annual billing and the shared record lock customers in.",
])

# ---------------- 3. Principles ----------------
doc.add_heading("3. Pricing principles", level=1)
table([
    ["Principle", "How it is applied"],
    ["Free is the growth engine, not a trial", "Free plans never expire. A free founder workspace invites its investors, and a free investor account receives updates and deal flow. The community stays free for every member, as the deck promises."],
    ["Charge for each side's value metric", "Founders pay per company workspace, because one startup is one company and no seat count makes sense there. Institutions pay for seats and portfolio companies, which is how their workload grows."],
    ["Paid plans unlock AI and control", "Free accounts get a taste of each AI feature. Paid plans unlock volume (valuations, scenarios, AI credits), governance (permissions, NDA gating, audit trail) and the agents that do the analyst work."],
    ["AI credits as a fair-use guardrail", "Every plan includes a monthly credit allowance. One credit is about one agent action; a full valuation uses about 20 and a diligence memo about 60. The allowance keeps inference cost per account predictable."],
    ["Price below US tools, sell on outcomes", "Founder Pro costs about a third of Carta or Pulley. It is sold on a measurable outcome: a data room, model and valuation ready for diligence in days rather than weeks."],
    ["Regional pricing", "There are two price lists: GCC list in USD, SAR or AED, and an Egypt list in EGP at 60 per cent of the GCC price."],
    ["One upgrade path per side", "Founders go Free, Pro, Team, Custom. Investors go Free, Angel, Institutional, Custom. Each step is triggered by a limit the customer can see, not by a feature hidden behind a sales call."],
], widths=[4.5, 12.7], first_col_bold=True, font=8.2)

# ---------------- 4. Founder plans ----------------
doc.add_heading("4. Founder plans, priced per company", level=1)
para("A founder workspace belongs to one company. Multi-entity groups, holding companies and studios with several companies buy the Custom plan.", italic=True, color=GREY)
table([
    ["", "Free", "Pro", "Team", "Custom"],
    ["Who it is for", "Pre-seed founders setting up", "A startup raising its next round", "A funded startup with a finance or ops lead", "Groups, holdcos, later-stage and regulated companies"],
    ["Monthly plan, per month", "$0", "$59", "$149", "From $479"],
    ["Annual plan, per month", "$0", "$49", "$124", "From $399"],
    ["Annual plan, per year", "$0", "$588", "$1,488", "From $4,788"],
    ["Seats", "1", "3", "10", "Unlimited"],
    ["Cap table stakeholders", "Up to 15", "Up to 50", "Up to 150", "Unlimited"],
    ["ESOP, vesting and dilution modelling", "View only", "Yes", "Yes", "Yes, plus multi-entity"],
    ["Secure data rooms", "1 room, 1 GB, 10 viewers", "3 rooms, 10 GB, NDA gating, per-investor permissions", "Unlimited rooms, 100 GB, full audit trail", "Custom retention, watermarking, SSO"],
    ["Guided valuation, 5 methods", "1 per quarter", "5 per month", "Unlimited", "Unlimited, analyst sign-off option"],
    ["Exit and stress scenarios", "1", "3", "Unlimited", "Unlimited"],
    ["Financial model generator, 3 statements and 5 years", "Sample only", "1 live model", "Unlimited, with versions", "Custom templates"],
    ["Investor updates", "Monthly template", "Unlimited plus Update Writer agent", "KPI-linked, scheduled", "White-label"],
    ["AI agents: Readiness coach, Data-room assistant, Update writer", "Preview", "Yes", "Yes, priority", "Yes, custom prompts"],
    ["AI credits per month", "25", "300", "1,500", "4,000 or a pooled allowance"],
    ["AI investor matching", "See top 3 matches", "10 warm intro requests a month", "30 a month", "Unlimited"],
    ["Investor pipeline and CRM", "25 investors", "250 investors", "Unlimited", "Unlimited, API"],
    ["Community, events and channels", "Full access", "Full access", "Full access", "Full access"],
    ["Support", "Community and help centre", "Email, 48 hours", "Priority, 24 hours, onboarding call", "Dedicated success manager, SLA"],
    ["Trial and demo", "Not needed", "14-day trial, no card", "14-day trial or a booked demo", "Demo and tailored proposal"],
], widths=[4.4, 2.6, 3.4, 3.4, 3.4], first_col_bold=True, font=7.6)
para("What triggers each upgrade:", bold=True)
bullets([
    ("Free to Pro: ", "the company opens a round. It needs NDA-gated data rooms and more than one valuation, or passes 15 stakeholders when the ESOP is granted."),
    ("Pro to Team: ", "the round closes and the company has more stakeholders, a finance hire and monthly investor reporting."),
    ("Team to Custom: ", "a second entity, a holding company restructuring, or a requirement for SSO or data residency."),
])

# ---------------- 5. Investor plans ----------------
doc.add_heading("5. Investor plans, priced per account", level=1)
para("The Institutional plan covers family offices, venture capital, private equity, corporate venture capital and organised angel networks. One plan scales with use instead of a separate list for each investor type.", italic=True, color=GREY)
table([
    ["", "Free", "Angel", "Institutional", "Custom"],
    ["Who it is for", "Any investor following founders and deals", "Active individual angels and syndicate leads", "Family offices, VC, PE, CVC, angel networks", "Multi-fund managers, large family offices, banks"],
    ["Monthly plan, per month", "$0", "$79", "$599 base", "From $1,799"],
    ["Annual plan, per month", "$0", "$65", "$499 base", "From $1,499"],
    ["Annual plan, per year", "$0", "$780", "$5,988 base", "From $17,988"],
    ["Seats", "1", "2", "5 included, then $49 per seat per month", "Unlimited"],
    ["Portfolio companies tracked", "5", "40", "50 included, then $10 per company per month", "Unlimited, multi-fund"],
    ["Returns: MOIC, TVPI, DPI, RVPI, IRR", "MOIC only", "Full set, benchmarked", "Full set, fund and LP level", "Full set, custom metrics"],
    ["Valuation and waterfall", "1 per month", "15 per month", "Unlimited, waterfall per company", "Unlimited, audit-ready packs"],
    ["Stress testing and portfolio simulator", "Base case only", "Unlimited", "Unlimited, saved snapshots", "Unlimited, custom shocks"],
    ["KPI collection from portfolio companies", "None", "Read issuer-shared KPIs", "Request KPIs; founders join free", "Automated, with data integrations"],
    ["AI agents: Diligence, Portfolio monitor, Deal scout", "Preview", "Diligence, 10 memos a month; Deal scout", "All three, team workspace", "All three, custom agents"],
    ["AI credits per month", "25", "500", "3,000", "8,000 or a pooled allowance"],
    ["Deal access and AI matching", "Browse the deal feed", "Thesis matching, alerts, co-invest circles", "Pipeline board, team matching, syndicate tools", "Private deal rooms, white-label"],
    ["Reports and LP packs", "None", "Personal reports", "LP reporting pack, Arabic and English", "LP portal, branded"],
    ["Audit history and permissions", "None", "Basic", "Full audit trail, roles", "SSO and SAML, data residency in KSA"],
    ["Support", "Community", "Email, 48 hours", "Onboarding and data migration, 24 hours", "Dedicated success manager, SLA"],
    ["Trial and demo", "Not needed", "14-day trial, no card", "Demo, then a 30-day guided pilot", "Demo, pilot and proposal"],
], widths=[4.4, 2.6, 3.2, 3.6, 3.4], first_col_bold=True, font=7.6)
para("Example Institutional bill, a $50m VC fund with 7 users and 60 portfolio companies, paid annually: "
     "$499 base + 2 extra seats × $49 + 10 extra companies × $10 = $697 a month, or $8,364 a year.", italic=True)

# ---------------- 6. Trials, demos ----------------
doc.add_heading("6. Trials, demos and the sales motion", level=1)
table([
    ["Plan", "Path to purchase", "Who sells it", "Target sales cycle"],
    ["Founder Pro, Investor Angel", "14-day full-feature trial with no card, in-product nudges at each limit, card checkout", "The product, supported by growth marketing", "Same day to 30 days"],
    ["Founder Team", "Trial, or a booked 30-minute demo for funded companies", "Product plus customer success", "2 to 4 weeks"],
    ["Investor Institutional", "Demo, then a 30-day guided pilot that imports up to 15 holdings, then an annual proposal", "SDR books the meeting, account executive runs the demo and pilot", "6 to 10 weeks; the model uses a 2-month lag"],
    ["Custom, both sides", "Discovery call, tailored demo, security review, proposal and contract", "Head of sales, with a co-founder on the call", "2 to 4 months"],
], widths=[3.6, 6.4, 4.2, 3.0], first_col_bold=True, font=8)
para("The demo is a pre-loaded sample portfolio, worth $212.4m with a 23.7 per cent net IRR as in the deck, plus a live import of the prospect's own top three holdings. Pilots convert best when the investor's own data is in the product by day 7.")

# ---------------- 7. Discounts and policies ----------------
doc.add_heading("7. Discounts and commercial policy", level=1)
table([
    ["Policy", "Terms", "Where it sits in the model"],
    ["Monthly or annual billing", "Every plan, including Custom, is offered monthly or annually; annual saves about 17 per cent, two months free", "Annual price per month by tier and year; share of accounts paying annually"],
    ["Egypt price list", "60 per cent of the GCC list, billed in EGP", "Egypt price index and Egypt share of paying accounts, by year"],
    ["Founding member offer", "30 per cent off the first year for the first 150 paying accounts on each side", "Price realization of 85 per cent in 2027 rising to 96 per cent"],
    ["Accelerator and incubator programme", "Cohort startups get Pro free for 3 months, then the standard price; the partner earns 15 per cent of first-year revenue", "Partner-sourced share of founder revenue, 15 per cent revenue share"],
    ["Angel network programme", "Members get 20 per cent off Angel; the network gets an Institutional seat bundle", "Partner-sourced share of investor revenue, 15 per cent revenue share"],
    ["Price changes", "Launch prices held through 2028; increases of 5 to 9 per cent a year from 2029; annual customers keep their price until renewal", "List price by year, 2027 to 2031"],
    ["Refunds and cancellation", "Monthly plans cancel at period end. Annual plans can be refunded within 14 days, then not.", "Churn by tier"],
    ["Non-profit, university and government ecosystem bodies", "Up to 50 per cent off Team or Institutional", "Covered by price realization"],
], widths=[4.0, 7.2, 6.0], first_col_bold=True, font=8)

# ---------------- 8. Add-ons ----------------
doc.add_heading("8. Add-ons and future revenue, switched off in the base case", level=1)
para("The model is subscription-led as instructed. These lines are built in behind one switch on the Assumption Setting sheet, set to 0 in the base case and 1 to show the upside.", italic=True, color=GREY)
table([
    ["Add-on", "Price", "Opens", "Notes"],
    ["AI credit top-up pack", "$20 per 500 credits", "Month 6", "For heavy diligence periods; about 80 per cent gross margin"],
    ["Analyst-reviewed valuation report", "$249 per report", "Month 4", "Investor-ready pack signed off by an Angelsta valuation analyst"],
    ["White-label licence", "$6,000 per year", "Month 13", "For accelerators, angel networks and banks' private wealth teams"],
    ["Syndicate and SPV administration", "2 per cent of SPV size, one-off", "Month 25", "Needs a licensed partner or an FRA, CMA or FSRA licence"],
    ["Event sponsorship", "$10k to $60k per year", "Month 13", "Sponsors of the Angelsta community events and MENA data reports"],
], widths=[4.2, 3.4, 2.0, 7.6], first_col_bold=True, font=8)

# ---------------- 9. Unit economics ----------------
doc.add_heading("9. Unit economics by plan, 2027", level=1)
para("Monthly cost to serve one paying account, with AI inference at $0.012 per credit and average use below the allowance:", italic=True, color=GREY)
rows = [["Plan", "Effective price*", "AI inference", "Hosting and support", "Payment fees", "Gross margin"]]
plans = [("Founder Pro", 0.75*59+0.25*49, P.AI_USE["S-Pro"], 0), ("Founder Team", 0.65*149+0.35*124, P.AI_USE["S-Team"], 0),
         ("Investor Angel", 0.75*79+0.25*65, P.AI_USE["I-Angel"], 0), ("Investor Institutional", 0.3*599+0.7*499, P.AI_USE["I-Inst"], 25)]
for name, price, credits, data in plans:
    ai = credits*P.AI_COST_PER_CREDIT[0]
    host = 1.20 + 1.50 + data
    pay = price*0.029
    gm = 1-(ai+host+pay)/price
    rows.append([name, f"${price:,.0f}", f"${ai:,.2f}", f"${host:,.2f}", f"${pay:,.2f}", f"{gm:.0%}"])
table(rows, widths=[3.8, 2.6, 2.5, 3.2, 2.5, 2.6], first_col_bold=True, font=8)
para("* GCC list price, blended for monthly and annual billing, before Egypt pricing and launch discounts. Hosting and support includes third-party market data feeds for Institutional accounts.", italic=True, size=8, color=GREY)

# ---------------- 10. Model linkage ----------------
doc.add_heading("10. The pricing inputs the financial model uses", level=1)
para("Every figure below is a typed input on the Assumption Setting sheet, section 8.", italic=True, color=GREY)
hdr = ["Input, USD per month"] + [str(y) for y in P.YEARS]
rows = [hdr]
for side, d in [("Founder", S), ("Investor", I)]:
    for tier, v in d.items():
        if tier == "Free":
            continue
        rows.append([f"{side} {tier}, monthly plan, per month"] + [usd(x) for x in v["monthly"]])
        rows.append([f"{side} {tier}, annual plan, per month"] + [usd(x) for x in v["annual"]])
        rows.append([f"{side} {tier}, annual plan, per year"] + [usd(x*12) for x in v["annual"]])
rows.append(["Share of self-serve accounts paying annually"] + [f"{x:.0%}" for x in P.ANNUAL_SHARE_SELF])
rows.append(["Share of sales-led accounts paying annually"] + [f"{x:.0%}" for x in P.ANNUAL_SHARE_SALES])
rows.append(["Price realization after discounts"] + [f"{x:.0%}" for x in P.PRICE_REALIZATION])
rows.append(["Egypt share of paying accounts"] + [f"{x:.0%}" for x in P.EGYPT_SHARE])
rows.append(["Egypt price index against the GCC list"] + [f"{P.EGYPT_PRICE_INDEX:.0%}"]*5)
rows.append(["AI inference cost per credit"] + [f"${x:.3f}" for x in P.AI_COST_PER_CREDIT])
table(rows, widths=[6.7, 2.1, 2.1, 2.1, 2.1, 2.1], first_col_bold=True, font=7.8)

# ---------------- 11. Risks ----------------
doc.add_heading("11. Risks, and what to test in the first six months", level=1)
table([
    ["Risk", "Signal to watch", "Response"],
    ["Free plan too generous; conversion stays under 1 per cent a month", "Activated free accounts that never reach a limit", "Tighten Free to 10 stakeholders and 1 valuation every 6 months, and add usage nudges"],
    ["Egypt willingness to pay below the 60 per cent list", "Trial-to-paid in Egypt under half the GCC rate", "EGP-only Pro Lite at 40 per cent of list, annual billing only"],
    ["Institutional cycle longer than 2 months", "Pilots running past day 45", "Fixed-scope pilot with the prospect's data imported by Angelsta in week one"],
    ["AI cost per credit does not fall", "Inference over 8 per cent of revenue", "Route routine actions to smaller models; lower credit allowances on new plans"],
    ["Churn after the round closes (founders)", "Pro cancellations within 60 days of a close", "Annual-only discount at close; Team bundles post-close investor reporting"],
], widths=[5.0, 5.2, 7.0], first_col_bold=True, font=8)
para("Price tests to run: Pro at $49 against $59 monthly, Institutional at $499 against $699 annual base, and a $29 Egypt Pro. Each runs for 6 weeks with at least 300 trials per arm.")

# ---------------- 12. Sources ----------------
doc.add_heading("12. Sources", level=1)
src = [
    ("Carta pricing, partner pricing and third-party estimates", "https://carta.com/partners/partner-pricing/ ; https://www.costbench.com/software/equity-management/carta/ ; https://www.roundfunded.com/en/alternatives/carta"),
    ("Pulley pricing", "https://pricingsaas.com/companies/pulley ; https://frontdeskreview.com/software/cap-table-management/pulley/"),
    ("Cake Equity pricing", "https://cakeequity.com/pricing ; https://costbench.com/software/equity-management/cake-equity/"),
    ("Eqvista pricing", "https://eqvista.com/pricing/ ; https://eqvista.com/support/premium-plan-pricing/"),
    ("Visible founder and investor pricing", "https://visible.vc/pricing/ ; https://visible.vc/investor-pricing/ ; https://www.roundfunded.com/en/alternatives/visible"),
    ("AngelList pricing", "https://www.angellist.com/startups/pricing ; https://www.allocations.com/insights/angellist-fees-in-2026-the-complete-breakdown-spv-setup-carry-and-add-ons"),
    ("Affinity pricing", "https://www.affinity.co/product/pricing"),
    ("Zapflow pricing", "https://www.saasworthy.com/product/zapflow/pricing"),
    ("Synaptic, FundCount, emerging manager stack", "https://research.synaptic.com/drafts/old-pages/pricing-page ; https://fundcount.com/top-7-private-equity-portfolio-monitoring-software/ ; https://valueaddvc.com/blog/the-emerging-manager-tech-stack-12-tools-that-replace-a-full-back-office"),
    ("MENA venture funding 2025", "https://www.magnitt.com/research/FY-2025-MENA-VC-Report-51018 ; https://www.wamda.com/research/pdf/2025-year-review-investments-mena ; https://www.arabnews.com/node/2629071"),
    ("Family offices and angel networks in MENA", "https://www.arabnews.pk/node/2593586/business-economy ; https://mena.entrepreneur.com/growth-strategies/a-guide-to-the-top-angel-investor-groups-in-saudi-arabia/448476"),
    ("Freemium conversion benchmarks", "https://userpilot.com/blog/freemium-saas/ ; https://www.crazyegg.com/blog/free-to-paid-conversion-rate/ ; https://productled.com/blog/product-led-growth-benchmarks"),
    ("SaaS churn benchmarks", "https://www.shno.co/marketing-statistics/saas-churn-benchmarks-statistics ; https://recurly.com/research/recurly-research-metrics-report-churn"),
    ("Payment processing in MENA", "https://ziina.com/blog/top-payment-gateways-UAE ; https://dodopayments.com/blogs/paymob-alternatives"),
]
table([["Topic", "Links"]] + [[a, b] for a, b in src], widths=[5.0, 12.2], first_col_bold=True, font=7.4, zebra=False)
para("Most vendors quote on request and third-party aggregators often disagree, so treat the competitor prices as directional. Angelsta's live pricing page could not be reached during this research, so the existing $79 Growth and $199 Premium plans in the deck have been replaced by the plans above.", italic=True, size=8, color=GREY)

out = sys.argv[1]
doc.save(out)
print("saved", out)
