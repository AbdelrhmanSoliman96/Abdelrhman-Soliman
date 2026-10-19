"""
Build the StartPad operational financial model.

Monthly for thirty-six months, summed to three years, driven by the volumes and
the headcount in the business plan (business_plan/model.py) and the channel
taxonomy in the go-to-market strategy.

Every output is a formula. Nothing is a value Python computed and pasted in, so
changing an assumption changes the model rather than requiring this script to be
run again. The only literals written are the typed inputs — shown in blue on a
yellow fill, per the convention stated on the cover.

    python scripts/build_financial_model_xlsx.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openpyxl import Workbook                                    # noqa: E402
from openpyxl.chart import BarChart, LineChart, Reference        # noqa: E402
from openpyxl.styles import Alignment, Border, Font              # noqa: E402
from openpyxl.utils import get_column_letter                     # noqa: E402

import _fin_common as F                                          # noqa: E402
from _fin_common import (MONEY, MONEY2, MULT, NUM, NUM1, PCT, PCT0,  # noqa: E402
                         TEXT, DAYS, band, f, fill, input_cell,
                         mcol, ml, monthly_row, month_header, months_of,
                         pos_in_quarter, quarter_of, setup_monthly,
                         sheet_title, write_row, year_of, year_sum, yl)
from business_plan import model as BP                            # noqa: E402

R = {}          # sheet -> label -> row number
A = {}          # assumption key -> absolute reference


def ref(sheet, row, col=None, m=None, absolute=True):
    """Absolute reference to a cell on another sheet."""
    c = col if col is not None else mcol(m)
    d = "$" if absolute else ""
    return f"{sheet}!{d}{get_column_letter(c)}{d}{row}"


def mref(sheet, row, m):
    """Same month, another sheet — column relative so it can be filled across."""
    return f"{sheet}!{ml(m)}${row}"


# =====================================================================
#  03 · ASSUMPTIONS
# =====================================================================
def build_assumptions(wb):
    ws = wb.create_sheet("Assumptions")
    sheet_title(ws, "Assumptions",
                "Every typed input in the model. Blue on yellow is an input you "
                "may change; black is a formula. Nothing elsewhere in the "
                "workbook is typed.")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 34
    for col in range(3, 16):
        ws.column_dimensions[get_column_letter(col)].width = 11
    ws.column_dimensions["P"].width = 2
    ws.column_dimensions["Q"].width = 58
    ws.freeze_panes = "C5"
    r = 5

    def head(text):
        nonlocal r
        r = band(ws, r, text, last_col=17)

    def three_year(label, key, vals, fmt=MONEY, note=""):
        """A Year 1 / Year 2 / Year 3 input triple."""
        nonlocal r
        write_row(ws, r, label, note)
        for i, v in enumerate(vals):
            input_cell(ws, r, 3 + i, v, fmt)
        A[key] = [f"Assumptions!${get_column_letter(3 + i)}${r}" for i in range(3)]
        r += 1

    def single(label, key, val, fmt=MONEY, note=""):
        nonlocal r
        write_row(ws, r, label, note)
        input_cell(ws, r, 3, val, fmt)
        A[key] = f"Assumptions!$C${r}"
        r += 1

    def comment(text):
        nonlocal r
        c = ws.cell(r, 1, text)
        c.font = f(8, False, "6B7285", italic=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=14)
        r += 1

    # ---------------------------------------------------------- timeline
    head("1 · TIMELINE AND BASIS")
    comment("Month 1 is October 2026, the Land quarter in the business plan. "
            "Year 1 runs Oct 2026 - Sep 2029 in three twelve-month blocks.")
    single("Reporting currency", "ccy", "USD", TEXT)
    single("Corporate tax rate (Egypt)", "tax_rate", 0.225, PCT,
           "Egyptian corporate income tax")
    single("Tax paid in month of the following year", "tax_pay_month", 4, NUM,
           "Month 4 of the next financial year")
    r += 1

    # ------------------------------------------------- quarterly drivers
    head("2 · VOLUME DRIVERS — QUARTERLY, FROM THE BUSINESS PLAN")
    comment("These twelve quarters are the delivery plan. Monthly figures "
            "everywhere else are this quarter's volume split by the phasing "
            "weights below, so an annual total always ties back to the plan.")
    hdr = r
    ws.cell(hdr, 1, "Driver").font = f(8.5, True, F.WHITE)
    ws.cell(hdr, 2, "Unit").font = f(8.5, True, F.WHITE)
    for col in (1, 2):
        ws.cell(hdr, col).fill = fill(F.UV_DARK)
    for i, q in enumerate(F.QUARTER_LABELS):
        c = ws.cell(hdr, 3 + i, q)
        c.font = f(8, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center")
    r += 1

    drivers = [
        ("University cohorts — Egypt", "uni_cohorts_eg", "cohorts"),
        ("University cohorts — Saudi Arabia", "uni_cohorts_ksa", "cohorts"),
        ("University pilot cohorts (unpaid)", "uni_pilots", "cohorts"),
        ("Faculty licences sold", "uni_licences", "licences"),
        ("School cohorts", "school_cohorts", "cohorts"),
        ("School licences sold", "school_licences", "licences"),
        ("Technical and vocational cohorts", "tvet_cohorts", "cohorts"),
        ("National initiative seats", "initiative_seats", "seats"),
        ("Train-the-trainer cohorts", "tot_cohorts", "cohorts"),
        ("NGO and donor programmes", "ngo_programmes", "programmes"),
        ("Sponsored competitions", "competitions", "competitions"),
        ("Corporate and CSR programmes", "corporates", "programmes"),
        ("Programme and incubator partners active", "programmes", "partners"),
        ("Seats per programme partner", "seats_each", "seats"),
    ]
    for label, key, unit in drivers:
        write_row(ws, r, label, unit)
        for i in range(12):
            input_cell(ws, r, 3 + i, BP.QUARTERLY[key][i], NUM)
        A["q_" + key] = r
        r += 1

    write_row(ws, r, "Certified facilitators in the pool",
              "cumulative at quarter end")
    for i in range(12):
        input_cell(ws, r, 3 + i, BP.QUARTERLY["certified_facilitators"][i], NUM)
    A["q_facilitators"] = r
    r += 1
    write_row(ws, r, "Certified delivery partner organisations",
              "cumulative at quarter end")
    for i in range(12):
        input_cell(ws, r, 3 + i, BP.QUARTERLY["delivery_partners"][i], NUM)
    A["q_delivery_partners"] = r
    r += 1
    r += 1

    write_row(ws, r, "Monthly phasing within a quarter",
              "month 1 / month 2 / month 3 of each quarter")
    for i, v in enumerate((0.30, 0.33, 0.37)):
        input_cell(ws, r, 3 + i, v, PCT)
    A["phase"] = [f"Assumptions!${get_column_letter(3 + i)}${r}" for i in range(3)]
    ws.cell(r, 6, f"=SUM(C{r}:E{r})").number_format = PCT
    ws.cell(r, 6).font = f(8.5, True, F.INK)
    ws.cell(r, 7, "must be 100%").font = f(7.5, False, "6B7285")
    r += 2

    # ---------------------------------------------------------- pricing
    head("3 · PRICING — BY YEAR")
    three_year("University cohort — all-in programme fee", "p_uni",
               [BP.COHORT_PRICE[y] for y in (1, 2, 3)], MONEY,
               "6 bootcamp days, seats, judging, cohort report")
    three_year("Faculty licence — annual", "p_uni_lic",
               [BP.PRICE_FACULTY_LICENCE] * 3, MONEY, "faculty-wide, per year")
    three_year("School cohort", "p_school",
               [BP.PRICE_SCHOOL_COHORT[y] for y in (1, 2, 3)], MONEY,
               "4 days, larger groups, employability frame")
    three_year("School licence — annual", "p_school_lic",
               [BP.PRICE_SCHOOL_LICENCE] * 3, MONEY)
    three_year("Technical and vocational cohort", "p_tvet",
               [BP.PRICE_TVET_COHORT[y] for y in (1, 2, 3)], MONEY, "5 days")
    three_year("National initiative seat", "p_seat_init",
               [BP.PRICE_INITIATIVE_SEAT[y] for y in (1, 2, 3)], MONEY2,
               "per participant, bulk provisioned")
    three_year("Train-the-trainer cohort", "p_tot",
               [BP.PRICE_TOT_COHORT[y] for y in (1, 2, 3)], MONEY)
    three_year("NGO and donor programme", "p_ngo",
               [BP.PRICE_NGO_PROGRAMME[y] for y in (1, 2, 3)], MONEY,
               "multi-site, logframe reporting")
    three_year("Sponsored competition", "p_comp",
               [BP.PRICE_COMPETITION[y] for y in (1, 2, 3)], MONEY,
               "paid by the sponsor, not the organiser")
    three_year("Corporate and CSR programme", "p_corp",
               [BP.PRICE_CORPORATE[y] for y in (1, 2, 3)], MONEY)
    three_year("Programme and incubator seat", "p_seat_prog",
               [BP.PRICE_SEAT[y] for y in (1, 2, 3)], MONEY2)
    single("Subscription — Pro, annual", "p_pro", BP.PRICE_PRO_YEAR, MONEY)
    single("Subscription — Team, annual", "p_team", BP.PRICE_TEAM_YEAR, MONEY)
    single("Share of new subscribers taking Team", "mix_team", BP.MIX_TEAM, PCT)
    single("Subscription monthly churn", "sub_churn", 0.045, PCT,
           "of the active base, monthly")
    single("Cohort size — university", "cohort_size", BP.COHORT_SIZE, NUM)
    single("Cohort size — school and technical", "school_size",
           BP.SCHOOL_COHORT_SIZE, NUM)
    r += 1

    # ------------------------------------------------- acquisition: offline
    head("4 · ACQUISITION — OFFLINE CHANNELS (they create sign-ups)")
    comment("Five offline channels, from the go-to-market strategy. Activities "
            "per month is the lever; cost, sign-ups and institutional leads "
            "follow from it.")
    hdr = r
    for i, t in enumerate(["Activities / month — Y1", "Y2", "Y3",
                           "Cost per activity", "Sign-ups per activity",
                           "Institutional leads per activity"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(7.6, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr, 1, "Offline channel").font = f(8.5, True, F.WHITE)
    ws.cell(hdr, 1).fill = fill(F.UV_DARK)
    ws.cell(hdr, 2).fill = fill(F.UV_DARK)
    ws.row_dimensions[hdr].height = 26
    r += 1
    offline = [
        ("Campus workshops", "ws", 2, 6, 11, 420, 45, 0.9,
         "Mission 01 completed live in an hour"),
        ("Ambassador campus activity", "amb", 3, 8, 14, 180, 38, 0.6,
         "run by the stipended ambassador network"),
        ("Competitions and qualifying rounds", "cmp", 0.5, 1.2, 2.0, 2600, 320,
         2.4, "a sponsor pays; entry is a free account"),
        ("Events, fairs and conferences", "evt", 1, 2, 3.5, 1900, 150, 3.2,
         "judged on meetings booked, not stand traffic"),
        ("Partner sessions inside NGO and programme cohorts", "prt",
         1, 3, 5, 350, 60, 1.4, "talks inside somebody else's cohort"),
        ("Direct outreach by the partnership heads", "out", 4, 7, 9, 0, 0, 6.0,
         "their own prospecting; the cost sits in payroll, not marketing"),
    ]
    A["off"] = {}
    for label, key, y1, y2, y3, cost, signups, leads, note in offline:
        write_row(ws, r, label, note)
        for i, v in enumerate((y1, y2, y3)):
            input_cell(ws, r, 3 + i, v, NUM1)
        input_cell(ws, r, 6, cost, MONEY)
        input_cell(ws, r, 7, signups, NUM)
        input_cell(ws, r, 8, leads, NUM1)
        A["off"][key] = r
        r += 1
    A["off_rows"] = [A["off"][k] for _, k, *_ in offline]
    A["off_labels"] = [lbl for lbl, *_ in offline]
    r += 1

    # -------------------------------------------------- acquisition: online
    head("5 · ACQUISITION — ONLINE CHANNELS (they create reach)")
    comment("Monthly spend is the lever. Reach, clicks and sign-ups follow. "
            "There is no cold paid-acquisition line beyond the budget shown: "
            "digital retargets people the engines already reached.")
    hdr = r
    for i, t in enumerate(["Spend / month — Y1", "Y2", "Y3",
                           "Cost per 1,000 reached", "Reach to click",
                           "Click to free account"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(7.6, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr, 1, "Online channel").font = f(8.5, True, F.WHITE)
    ws.cell(hdr, 1).fill = fill(F.UV_DARK)
    ws.cell(hdr, 2).fill = fill(F.UV_DARK)
    ws.row_dimensions[hdr].height = 26
    r += 1
    online = [
        ("Short video — TikTok, Instagram, Facebook", "vid", 900, 2200, 4200,
         3.50, 0.012, 0.09, "organic-first, boosted selectively"),
        ("Paid social — targeted by age, city, university", "ads", 850, 2000,
         4000, 6.50, 0.009, 0.11, "retargeting and event fill only"),
        ("Influencers and student creators", "inf", 700, 1700, 3200, 5.50,
         0.011, 0.10, "Arabic student and founder voices"),
        ("Mission Zero — the founder podcast", "pod", 2100, 4000, 8000, 14.00,
         0.012, 0.10, "its real return is institutional, not sign-ups"),
        ("Webinars — live Mission 01 sessions", "web", 260, 600, 1150, 25.00,
         0.050, 0.25, "highest intent, smallest reach"),
        ("SEO and organic search", "seo", 500, 1150, 2100, 3.00, 0.018, 0.08,
         "content and the annual readiness report"),
    ]
    A["on"] = {}
    for label, key, y1, y2, y3, cpm, ctr, cvr, note in online:
        write_row(ws, r, label, note)
        for i, v in enumerate((y1, y2, y3)):
            input_cell(ws, r, 3 + i, v, MONEY)
        input_cell(ws, r, 6, cpm, MONEY2)
        input_cell(ws, r, 7, ctr, PCT)
        input_cell(ws, r, 8, cvr, PCT)
        A["on"][key] = r
        r += 1
    A["on_rows"] = [A["on"][k] for _, k, *_ in online]
    A["on_labels"] = [lbl for lbl, *_ in online]
    r += 1

    # ------------------------------------------------------- funnel rates
    head("6 · FUNNEL CONVERSION")
    comment("Two funnels. The institutional one ends in a signed contract; the "
            "learner one ends at Mission 01 and then a paid plan.")
    three_year("Institutional lead to first meeting", "c_meet",
               [0.40, 0.44, 0.48], PCT)
    three_year("Meeting to proposal, pilot or bid", "c_prop",
               [0.50, 0.54, 0.58], PCT)
    three_year("Proposal to signed contract", "c_win", [0.38, 0.44, 0.50], PCT)
    single("Sales cycle — months from lead to signature", "cycle", 4, NUM,
           "the lag applied between leads and wins")
    three_year("Free account to Mission 01 activation", "c_act",
               [0.42, 0.46, 0.50], PCT, "activation is finishing Mission 01")
    three_year("Activation to engaged (Discovery complete)", "c_eng",
               [0.55, 0.58, 0.61], PCT)
    three_year("Engaged to paid — reached through an institution", "c_pay_inst",
               [0.075, 0.085, 0.095], PCT)
    three_year("Engaged to paid — reached online", "c_pay_online",
               [0.030, 0.034, 0.038], PCT)
    single("Inbound institutional enquiries per 1,000 online sign-ups",
           "inbound_rate", 14, NUM1, "content and the podcast, working as "
           "pipeline rather than brand")
    single("Share of online spend serving institutional demand",
           "online_inst_share", 0.35, PCT, "splits marketing cost between the "
           "two funnels for the CAC calculations")
    three_year("Deliveries per signed contract", "per_contract",
               [1.8, 2.2, 2.6], NUM1,
               "land and expand: one agreement covers more cohorts each year")
    single("Entrants per sponsored competition", "entrants_per_comp", 700, NUM)
    single("Participants per NGO or donor programme", "part_ngo", 140, NUM)
    single("Participants per corporate programme", "part_corp", 60, NUM)
    r += 1

    # --------------------------------------------------- direct cost (COGS)
    head("7 · DIRECT COST OF DELIVERY")
    single("Facilitator day rate", "fac_rate", BP.FACILITATOR_DAY_RATE, MONEY)
    single("Facilitators per cohort", "fac_per", BP.FACILITATORS_PER_COHORT, NUM)
    single("Delivery days — university cohort", "d_uni", BP.BOOTCAMP_DAYS, NUM)
    single("Delivery days — school cohort", "d_school", BP.SCHOOL_DAYS, NUM)
    single("Delivery days — technical cohort", "d_tvet", BP.TVET_DAYS, NUM)
    single("Materials and showcase — university cohort", "m_uni",
           BP.COHORT_MATERIALS + BP.COHORT_BAZAAR, MONEY)
    single("Materials and showcase — school cohort", "m_school",
           BP.SCHOOL_MATERIALS + BP.SCHOOL_SHOWCASE, MONEY)
    single("Materials and showcase — technical cohort", "m_tvet",
           BP.TVET_MATERIALS + BP.TVET_SHOWCASE, MONEY)
    single("Delivery cost — train-the-trainer cohort", "c_tot", BP.TOT_DIRECT,
           MONEY)
    single("Delivery cost — NGO and donor programme", "c_ngo", BP.NGO_DIRECT,
           MONEY)
    single("Delivery cost — sponsored competition", "c_comp",
           BP.COMPETITION_DIRECT, MONEY)
    single("Delivery cost — corporate programme", "c_corp", BP.CORPORATE_DIRECT,
           MONEY)
    single("Support cost per national initiative seat", "c_seat_init",
           BP.INITIATIVE_SEAT_DIRECT, MONEY2,
           "provisioning, bilingual support, partner reporting")
    single("Support cost per programme seat", "c_seat_prog", BP.SEAT_DIRECT,
           MONEY2)
    single("Subscription hosting and inference, per paid user per month",
           "c_sub", 0.72, MONEY2)
    r += 1

    # ------------------------------------------- revenue share, three parties
    head("8 · REVENUE SHARING WITH THIRD PARTIES")
    comment("Three counterparties take a share. Each is margin deliberately "
            "surrendered to buy delivery capacity, distribution or access that "
            "would otherwise have to be hired for.")
    three_year("Party 1 · share of cohorts delivered by certified partners",
               "pd_share", [0.10, 0.35, 0.55], PCT,
               "certified delivery partner organisations")
    single("Party 1 · partner's share of the cohort fee", "pd_rate",
           BP.PARTNER_REVENUE_SHARE, PCT, "they deliver, StartPad audits")
    three_year("Party 2 · share of competition revenue", "ch_comp_rate",
               [0.15, 0.15, 0.14], PCT,
               "youth and channel organisations — Enactus, INJAZ, chapters")
    three_year("Party 2 · share of programme and incubator seat revenue",
               "ch_seat_rate", [0.10, 0.10, 0.10], PCT)
    three_year("Party 3 · share of national initiative seat revenue",
               "ag_seat_rate", [0.08, 0.08, 0.07], PCT,
               "government aggregators and local distributors")
    single("Party 3 · payment processing on subscriptions", "pay_rate", 0.035,
           PCT)
    r += 1

    # ----------------------------------------------------- indirect / opex
    head("9 · INDIRECT OPERATING COST — MONTHLY, BY YEAR")
    comment("Costs that do not move with a cohort. Payroll comes from the HR "
            "model and marketing from the acquisition sheet, so neither is "
            "typed here.")
    three_year("Office rent — Cairo", "o_rent_cairo", [1400, 2400, 3600], MONEY)
    three_year("Office rent and desks — Riyadh", "o_rent_riyadh",
               [0, 1600, 2800], MONEY, "a desk in year one, an office later")
    three_year("Utilities, internet and communications", "o_util",
               [420, 760, 1250], MONEY)
    three_year("Cloud, AI inference and third-party APIs — fixed",
               "o_cloud_fixed", [900, 2100, 4600], MONEY)
    single("Cloud and inference — variable, per active learner per month",
           "o_cloud_var", 0.085, MONEY2)
    three_year("Software and tooling, per employee", "o_software",
               [180, 195, 210], MONEY)
    three_year("Travel — per commercial head, per month", "o_travel",
               [1250, 1450, 1650], MONEY, "Cairo, Riyadh, campuses, governorates")
    three_year("Outsourced finance, legal, audit and the KSA entity",
               "o_prof", [3800, 5300, 9600], MONEY)
    three_year("Safeguarding, child protection and compliance", "o_safe",
               [1150, 2500, 4800], MONEY)
    three_year("Partner enablement — certification, audits, regional hubs",
               "o_partner", [600, 3200, 11600], MONEY)
    three_year("Insurance, bank charges and sundries", "o_sundry",
               [380, 620, 1100], MONEY)
    single("Contingency on operating cost", "contingency", BP.CONTINGENCY, PCT)
    single("Sales commission on institutional revenue", "commission",
           BP.B2B_COMMISSION, PCT)
    single("Ambassador stipend per month", "amb_stipend",
           BP.AMBASSADOR_STIPEND_MONTH, MONEY)
    three_year("Ambassadors on stipend", "amb_count",
               [BP.AMBASSADORS[y] for y in (1, 2, 3)], NUM)
    single("Ambassador active months per year", "amb_months",
           BP.AMBASSADOR_ACTIVE_MONTHS, NUM)
    r += 1

    # -------------------------------------------------------- working capital
    head("10 · WORKING CAPITAL, ASSETS AND FUNDING")
    single("Days sales outstanding — institutional", "dso", 75, DAYS,
           "universities and ministries pay slowly; this is the single biggest "
           "cash risk in the model")
    single("Days sales outstanding — subscriptions", "dso_sub", 2, DAYS,
           "card payments settle immediately")
    single("Days payable outstanding — suppliers", "dpo", 35, DAYS)
    single("Accrued payroll — days outstanding", "acc_days", 10, DAYS)
    single("Institutional contracts invoiced in advance", "adv_share", 0.30, PCT,
           "creates deferred revenue")
    single("Opening cash — the money already in", "open_cash", 50000, MONEY,
           "stated by the founder; see the Actuals sheet")
    single("Seed round raised", "seed", 600000, MONEY,
           "sized on this model's own cash trough and the buffer below, not on "
           "a round number — see the lowest-cash row on the KPI sheet")
    single("Month the seed round lands", "seed_month", 1, NUM,
           "month one: the capitalised platform build and the office are paid "
           "for before any cohort has been invoiced")
    single("Minimum cash buffer to hold", "min_cash", 90000, MONEY)
    r += 1

    head("11 · ASSETS — DRIVEN BY HEADCOUNT")
    comment("Every new employee arrives with a kit. Asset purchases therefore "
            "follow the hiring plan rather than being guessed at.")
    hdr = r
    for i, t in enumerate(["Cost per unit", "Units per new employee",
                           "Useful life (months)"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(7.6, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr, 1, "Per-employee asset").font = f(8.5, True, F.WHITE)
    ws.cell(hdr, 1).fill = fill(F.UV_DARK)
    ws.cell(hdr, 2).fill = fill(F.UV_DARK)
    ws.row_dimensions[hdr].height = 26
    r += 1
    peremp = [("Laptop", "laptop", 1400, 1, 36),
              ("Desk, chair and storage", "desk", 620, 1, 60),
              ("Monitor and peripherals", "periph", 310, 1, 48),
              ("Mobile handset and line setup", "phone", 390, 1, 24)]
    A["cap_emp"] = []
    for label, key, cost, units, life in peremp:
        write_row(ws, r, label)
        input_cell(ws, r, 3, cost, MONEY)
        input_cell(ws, r, 4, units, NUM)
        input_cell(ws, r, 5, life, NUM)
        A["cap_emp"].append((label, r, life))
        r += 1
    write_row(ws, r, "Total per new employee", "", MONEY, bold=True)
    pe_first, pe_last = A["cap_emp"][0][1], A["cap_emp"][-1][1]
    cell = ws.cell(r, 3, f"=SUMPRODUCT(C{pe_first}:C{pe_last},D{pe_first}:D{pe_last})")
    cell.number_format = MONEY
    cell.font = f(9, True, F.INK)
    A["cap_per_emp"] = f"Assumptions!$C${r}"
    r += 2

    write_row(ws, r, "Shared and intangible assets", "month acquired · cost · life")
    r += 1
    shared = [("Office fit-out — Cairo", "fitout", 1, 14000, 60),
              ("Mission Zero production kit — camera, audio, lighting", "av",
               2, 9500, 48),
              ("Riyadh office setup", "riyadh", 14, 8500, 60),
              ("Network, servers and security", "net", 1, 4200, 48),
              ("Capitalised platform development", "platform", 1, 86000, 36),
              ("Capitalised curriculum and certification build", "curriculum",
               1, 42000, 36),
              ("Trademark, IP registration and entity formation", "ip", 1,
               11000, 60)]
    A["cap_shared"] = []
    for label, key, month, cost, life in shared:
        write_row(ws, r, label)
        input_cell(ws, r, 3, month, NUM)
        input_cell(ws, r, 4, cost, MONEY)
        input_cell(ws, r, 5, life, NUM)
        A["cap_shared"].append((label, r, life))
        r += 1
    r += 1
    R["Assumptions"] = {"last": r}
    return ws, r


# =====================================================================
#  04 · HR MODEL
# =====================================================================
def build_hr(wb):
    ws = wb.create_sheet("HR_Model")
    setup_monthly(ws, "HR Model",
                  "Eighteen roles, each with a start month and a headcount per "
                  "year. Payroll is computed monthly and summed annually; new "
                  "hires drive the asset purchases on the Capex sheet.",
                  freeze="C33")
    rows = {}
    r = band(ws, 5, "ESTABLISHMENT — INPUTS")
    hdr = r
    for col, t in ((1, "Role"), (2, "Function"), (3, "Start month"),
                   (4, "Base monthly gross"), (5, "Headcount Y1"),
                   (6, "Headcount Y2"), (7, "Headcount Y3")):
        c = ws.cell(hdr, col, t)
        c.font = f(8, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.row_dimensions[hdr].height = 26
    r += 1

    first_role = r
    role_rows = []
    for function, role, monthly, y1, y2, y3, y4, y5 in BP.ROLES:
        start = 1 if y1 else (13 if y2 else 25)
        ws.cell(r, 1, role).font = f(8.5)
        ws.cell(r, 2, function).font = f(7.5, False, "6B7285")
        input_cell(ws, r, 3, start, NUM)
        input_cell(ws, r, 4, monthly, MONEY)
        for i, v in enumerate((y1, y2, y3)):
            input_cell(ws, r, 5 + i, v, NUM)
        role_rows.append((r, role, function))
        r += 1
    last_role = r - 1

    ws.cell(r, 1, "Total establishment").font = f(9, True)
    ws.cell(r, 2, "the cap the business plan commits to").font = \
        f(7.5, False, "6B7285")
    for col in (5, 6, 7):
        L = get_column_letter(col)
        c = ws.cell(r, col, f"=SUM({L}{first_role}:{L}{last_role})")
        c.number_format = NUM
        c.font = f(9, True, F.INK)
    rows["total_hc_input"] = r
    r += 2

    write_row(ws, r, "Employer burden on gross salary",
              "social insurance, end-of-service, medical")
    input_cell(ws, r, 3, 0.155, PCT)
    burden = f"$C${r}"
    r += 1
    write_row(ws, r, "Annual salary increment", "applied from year two")
    input_cell(ws, r, 3, 0.08, PCT)
    incr = f"$C${r}"
    r += 2

    hc_col = {1: "E", 2: "F", 3: "G"}

    r = band(ws, r, "MONTHLY PAYROLL — FULLY LOADED")
    r = month_header(ws, r)
    cost_first = r
    for ir, role, function in role_rows:
        def cost(m, ir=ir):
            y = year_of(m)
            return (f"=IF({m}<$C${ir},0,${hc_col[y]}${ir}*$D${ir}"
                    f"*(1+{burden})*(1+{incr})^{y - 1})")
        r = monthly_row(ws, r, role, cost, function, MONEY)
    cost_last = r - 1
    r = monthly_row(ws, r, "Total payroll", lambda m:
                    f"=SUM({ml(m)}{cost_first}:{ml(m)}{cost_last})",
                    "fully loaded, all roles", MONEY, bold=True,
                    fill_colour=F.BAND)
    rows["payroll"] = r - 1
    r += 1

    r = band(ws, r, "MONTHLY HEADCOUNT")
    r = month_header(ws, r)
    hc_first = r
    for ir, role, function in role_rows:
        def hc(m, ir=ir):
            return f"=IF({m}<$C${ir},0,${hc_col[year_of(m)]}${ir})"
        r = monthly_row(ws, r, role, hc, function, NUM, agg="end")
    hc_last = r - 1
    r = monthly_row(ws, r, "Total headcount", lambda m:
                    f"=SUM({ml(m)}{hc_first}:{ml(m)}{hc_last})",
                    "at month end", NUM, bold=True, agg="end",
                    fill_colour=F.BAND)
    rows["headcount"] = r - 1
    hcr = rows["headcount"]
    r = monthly_row(ws, r, "New employees joining in the month", lambda m:
                    (f"={ml(m)}{hcr}" if m == 1
                     else f"=MAX(0,{ml(m)}{hcr}-{ml(m - 1)}{hcr})"),
                    "drives the Capex sheet", NUM, bold=True)
    rows["new_hires"] = r - 1

    comm = [ir for ir, role, function in role_rows
            if function == "Institutional Partnerships"]
    r = monthly_row(ws, r, "Commercial heads on the road", lambda m:
                    "=" + "+".join(
                        f"IF({m}<$C${ir},0,${hc_col[year_of(m)]}${ir})"
                        for ir in comm),
                    "drives the travel line on Expenses", NUM, agg="end")
    rows["commercial"] = r - 1
    R["HR_Model"] = rows
    return ws


# =====================================================================
#  06 · CAPEX AND ASSETS
# =====================================================================
def build_capex(wb):
    ws = wb.create_sheet("Capex")
    setup_monthly(ws, "Assets and Capital Expenditure",
                  "Per-employee assets follow the hiring plan: every new "
                  "employee arrives with a laptop, a desk, peripherals and a "
                  "handset. Shared and intangible assets are dated explicitly.",
                  freeze="C7")
    rows = {}
    nh = R["HR_Model"]["new_hires"]
    r = band(ws, 5, "ADDITIONS IN THE MONTH")
    r = month_header(ws, r)

    classes = []          # (label, additions_row, assumption_row, life)
    add_first = r
    for label, arow, life in A["cap_emp"]:
        r = monthly_row(ws, r, label, lambda m, arow=arow:
                        f"={mref('HR_Model', nh, m)}*Assumptions!$C${arow}"
                        f"*Assumptions!$D${arow}",
                        f"per new employee · {life} month life", MONEY)
        classes.append((label, r - 1, arow, life))
    for label, arow, life in A["cap_shared"]:
        r = monthly_row(ws, r, label, lambda m, arow=arow:
                        f"=IF({m}=Assumptions!$C${arow},Assumptions!$D${arow},0)",
                        f"one-off · {life} month life", MONEY)
        classes.append((label, r - 1, arow, life))
    add_last = r - 1
    r = monthly_row(ws, r, "Total capital expenditure", lambda m:
                    f"=SUM({ml(m)}{add_first}:{ml(m)}{add_last})",
                    "feeds investing activities", MONEY, bold=True,
                    fill_colour=F.BAND)
    rows["capex"] = r - 1
    r += 1

    r = band(ws, r, "GROSS COST — CUMULATIVE")
    r = month_header(ws, r)
    cum = {}
    cum_first = r
    for label, arow_add, arow_as, life in classes:
        this = r
        r = monthly_row(ws, r, label, lambda m, a=arow_add, t=this:
                        (f"={ml(m)}{a}" if m == 1
                         else f"={ml(m - 1)}{t}+{ml(m)}{a}"),
                        "", MONEY, agg="end")
        cum[label] = this
    cum_last = r - 1
    r = monthly_row(ws, r, "Total gross assets", lambda m:
                    f"=SUM({ml(m)}{cum_first}:{ml(m)}{cum_last})", "", MONEY,
                    bold=True, agg="end", fill_colour=F.BAND)
    rows["gross"] = r - 1
    rows["classes"] = [(label, cum[label], arow_as, life)
                       for label, _, arow_as, life in classes]
    R["Capex"] = rows
    return ws


# =====================================================================
#  10 · DEPRECIATION AND AMORTISATION
# =====================================================================
def build_depreciation(wb):
    ws = wb.create_sheet("Depreciation")
    setup_monthly(ws, "Depreciation and Amortisation",
                  "Straight line over each class's useful life, charged from "
                  "the month after acquisition and capped so an asset is never "
                  "written down below nil.",
                  freeze="C7")
    rows = {}
    classes = R["Capex"]["classes"]
    n = len(classes)

    # Rows are allocated before anything is written, because the charge for a
    # month depends on accumulated depreciation at the end of the month before,
    # which lives in the block underneath it.
    charge_hdr = 5
    charge_first = charge_hdr + 2
    charge_total = charge_first + n
    accum_hdr = charge_total + 2
    accum_first = accum_hdr + 2
    accum_total = accum_first + n
    nbv_hdr = accum_total + 2
    nbv_first = nbv_hdr + 2
    nbv_total = nbv_first + n

    band(ws, charge_hdr, "DEPRECIATION CHARGE IN THE MONTH")
    month_header(ws, charge_hdr + 1)
    for i, (label, cumrow, arow, life) in enumerate(classes):
        cr, ar = charge_first + i, accum_first + i
        monthly_row(ws, cr, label, lambda m, cum=cumrow, a=ar, ro=arow:
                    ("=0" if m == 1 else
                     f"=MIN({mref('Capex', cum, m - 1)}/Assumptions!$E${ro},"
                     f"{mref('Capex', cum, m - 1)}-{ml(m - 1)}{a})"),
                    f"{life} months, straight line", MONEY)
    monthly_row(ws, charge_total, "Total depreciation and amortisation",
                lambda m: f"=SUM({ml(m)}{charge_first}:"
                          f"{ml(m)}{charge_first + n - 1})",
                "feeds Expenses and the cash flow add-back", MONEY, bold=True,
                fill_colour=F.BAND)
    rows["charge"] = charge_total

    band(ws, accum_hdr, "ACCUMULATED DEPRECIATION")
    month_header(ws, accum_hdr + 1)
    for i, (label, cumrow, arow, life) in enumerate(classes):
        ar, cr = accum_first + i, charge_first + i
        monthly_row(ws, ar, label, lambda m, c=cr, t=accum_first + i:
                    (f"={ml(m)}{c}" if m == 1
                     else f"={ml(m - 1)}{t}+{ml(m)}{c}"),
                    "", MONEY, agg="end")
    monthly_row(ws, accum_total, "Total accumulated depreciation",
                lambda m: f"=SUM({ml(m)}{accum_first}:"
                          f"{ml(m)}{accum_first + n - 1})", "", MONEY,
                bold=True, agg="end", fill_colour=F.BAND)
    rows["accum"] = accum_total

    band(ws, nbv_hdr, "NET BOOK VALUE")
    month_header(ws, nbv_hdr + 1)
    for i, (label, cumrow, arow, life) in enumerate(classes):
        monthly_row(ws, nbv_first + i, label,
                    lambda m, cum=cumrow, a=accum_first + i:
                    f"={mref('Capex', cum, m)}-{ml(m)}{a}", "", MONEY,
                    agg="end")
    monthly_row(ws, nbv_total, "Total net book value",
                lambda m: f"=SUM({ml(m)}{nbv_first}:"
                          f"{ml(m)}{nbv_first + n - 1})",
                "carried to the balance sheet", MONEY, bold=True, agg="end",
                fill_colour=F.BAND)
    rows["nbv"] = nbv_total

    # Tangible and intangible split, for the balance sheet.
    intangible = [i for i, (label, *_ ) in enumerate(classes)
                  if "platform" in label.lower() or "curriculum" in label.lower()
                  or "Trademark" in label]
    tangible = [i for i in range(n) if i not in intangible]
    r = nbv_total + 2
    r = monthly_row(ws, r, "Net book value — tangible fixed assets",
                    lambda m: "=" + "+".join(f"{ml(m)}{nbv_first + i}"
                                             for i in tangible),
                    "property, equipment and fit-out", MONEY, agg="end",
                    bold=True)
    rows["nbv_tangible"] = r - 1
    r = monthly_row(ws, r, "Net book value — intangible assets",
                    lambda m: "=" + "+".join(f"{ml(m)}{nbv_first + i}"
                                             for i in intangible),
                    "capitalised platform, curriculum and IP", MONEY,
                    agg="end", bold=True)
    rows["nbv_intangible"] = r - 1
    R["Depreciation"] = rows
    return ws


def q_vol(qrow):
    """Monthly volume = that quarter's plan volume x the monthly phasing weight."""
    def g(m):
        qcol = get_column_letter(3 + quarter_of(m) - 1)
        return (f"=Assumptions!${qcol}${qrow}"
                f"*{A['phase'][pos_in_quarter(m) - 1]}")
    return g


def q_stock(qrow):
    """A level rather than a flow — the quarter's value, unphased."""
    def g(m):
        qcol = get_column_letter(3 + quarter_of(m) - 1)
        return f"=Assumptions!${qcol}${qrow}"
    return g


def price(key, m):
    return A[key][year_of(m) - 1]


# =====================================================================
#  08 · REVENUE
# =====================================================================
def build_revenue(wb):
    ws = wb.create_sheet("Revenue")
    setup_monthly(ws, "Revenue Streams",
                  "Thirteen lines across eight engines. Volume comes from the "
                  "quarterly plan split by the monthly phasing weight, so every "
                  "annual total ties back to the business plan exactly.",
                  freeze="C7")
    rows = {}
    r = band(ws, 5, "DELIVERY VOLUME")
    r = month_header(ws, r)
    vols = [
        ("University cohorts — Egypt", "uni_cohorts_eg", "cohorts", NUM1),
        ("University cohorts — Saudi Arabia", "uni_cohorts_ksa", "cohorts", NUM1),
        ("University pilot cohorts (unpaid)", "uni_pilots", "sales cost", NUM1),
        ("Faculty licences", "uni_licences", "licences", NUM1),
        ("School cohorts", "school_cohorts", "cohorts", NUM1),
        ("School licences", "school_licences", "licences", NUM1),
        ("Technical and vocational cohorts", "tvet_cohorts", "cohorts", NUM1),
        ("National initiative seats", "initiative_seats", "seats", NUM),
        ("Train-the-trainer cohorts", "tot_cohorts", "cohorts", NUM1),
        ("NGO and donor programmes", "ngo_programmes", "programmes", NUM1),
        ("Sponsored competitions", "competitions", "competitions", NUM1),
        ("Corporate and CSR programmes", "corporates", "programmes", NUM1),
    ]
    for label, key, note, fmt in vols:
        r = monthly_row(ws, r, label, q_vol(A["q_" + key]), note, fmt)
        rows[key] = r - 1
    r = monthly_row(ws, r, "Programme and incubator partners active",
                    q_stock(A["q_programmes"]), "partners", NUM1, agg="end")
    rows["prog_partners"] = r - 1
    r = monthly_row(ws, r, "Programme and incubator seats", lambda m:
                    (f"=Assumptions!${get_column_letter(3 + quarter_of(m) - 1)}"
                     f"${A['q_programmes']}"
                     f"*Assumptions!${get_column_letter(3 + quarter_of(m) - 1)}"
                     f"${A['q_seats_each']}"
                     f"*{A['phase'][pos_in_quarter(m) - 1]}"), "seats", NUM)
    rows["prog_seats"] = r - 1
    r = monthly_row(ws, r, "All in-person cohorts delivered", lambda m:
                    f"={ml(m)}{rows['uni_cohorts_eg']}+{ml(m)}"
                    f"{rows['uni_cohorts_ksa']}+{ml(m)}{rows['uni_pilots']}"
                    f"+{ml(m)}{rows['school_cohorts']}+{ml(m)}"
                    f"{rows['tvet_cohorts']}",
                    "the capacity constraint", NUM1, bold=True)
    rows["all_cohorts"] = r - 1
    r += 1

    r = band(ws, r, "REVENUE BY STREAM")
    r = month_header(ws, r)
    rev_first = r
    streams = [
        ("University cohort programmes", lambda m:
         f"=({ml(m)}{rows['uni_cohorts_eg']}+{ml(m)}"
         f"{rows['uni_cohorts_ksa']})*{price('p_uni', m)}", "Engine 1"),
        ("Faculty licences", lambda m:
         f"={ml(m)}{rows['uni_licences']}*{price('p_uni_lic', m)}", "Engine 1"),
        ("School cohorts", lambda m:
         f"={ml(m)}{rows['school_cohorts']}*{price('p_school', m)}", "Engine 2"),
        ("School licences", lambda m:
         f"={ml(m)}{rows['school_licences']}*{price('p_school_lic', m)}",
         "Engine 2"),
        ("Technical and vocational cohorts", lambda m:
         f"={ml(m)}{rows['tvet_cohorts']}*{price('p_tvet', m)}", "Engine 2"),
        ("National initiative seats", lambda m:
         f"={ml(m)}{rows['initiative_seats']}*{price('p_seat_init', m)}",
         "Engine 3"),
        ("Train-the-trainer cohorts", lambda m:
         f"={ml(m)}{rows['tot_cohorts']}*{price('p_tot', m)}", "Engine 3"),
        ("NGO and donor programmes", lambda m:
         f"={ml(m)}{rows['ngo_programmes']}*{price('p_ngo', m)}", "Engine 4"),
        ("Sponsored competitions", lambda m:
         f"={ml(m)}{rows['competitions']}*{price('p_comp', m)}", "Engine 5"),
        ("Corporate and CSR programmes", lambda m:
         f"={ml(m)}{rows['corporates']}*{price('p_corp', m)}", "Engine 6"),
        ("Programme and incubator seats", lambda m:
         f"={ml(m)}{rows['prog_seats']}*{price('p_seat_prog', m)}", "Engine 7"),
    ]
    for label, fn, note in streams:
        r = monthly_row(ws, r, label, fn, note, MONEY)
        rows["rev_" + label] = r - 1
    rev_last = r - 1
    r = monthly_row(ws, r, "Institutional revenue", lambda m:
                    f"=SUM({ml(m)}{rev_first}:{ml(m)}{rev_last})",
                    "engines 1 to 7 — somebody else pays", MONEY, bold=True,
                    fill_colour=F.BAND)
    rows["institutional"] = r - 1
    r += 1

    r = band(ws, r, "ENGINE 8 · FOUNDER SUBSCRIPTIONS")
    r = month_header(ws, r)
    rows["new_subs"] = r
    r = monthly_row(ws, r, "New paid subscribers in the month", "=0",
                    "from the Acquisition sheet", NUM, colour=F.LINK_FONT)
    rows["active_subs"] = r
    r = monthly_row(ws, r, "Active paid subscribers", "=0",
                    "from the Acquisition sheet", NUM, agg="end",
                    colour=F.LINK_FONT)
    r = monthly_row(ws, r, "Blended annual subscription price", lambda m:
                    f"={A['p_pro']}*(1-{A['mix_team']})"
                    f"+{A['p_team']}*{A['mix_team']}",
                    "Pro and Team at the stated mix", MONEY, agg="avg")
    rows["arpu"] = r - 1
    arpu = rows["arpu"]
    r = monthly_row(ws, r, "Subscription bookings — cash received", lambda m:
                    f"={ml(m)}{rows['new_subs']}*{ml(m)}{arpu}",
                    "annual plans, billed in advance", MONEY)
    rows["bookings"] = r - 1
    bk = rows["bookings"]
    r = monthly_row(ws, r, "Subscription revenue recognised", lambda m:
                    f"=SUM({ml(max(1, m - 11))}{bk}:{ml(m)}{bk})/12",
                    "one twelfth of each annual plan, monthly", MONEY)
    rows["sub_revenue"] = r - 1
    sr = rows["sub_revenue"]
    this = r
    r = monthly_row(ws, r, "Deferred subscription revenue — balance",
                    lambda m, t=this: (f"={ml(m)}{bk}-{ml(m)}{sr}" if m == 1
                                       else f"={ml(m - 1)}{t}+{ml(m)}{bk}"
                                            f"-{ml(m)}{sr}"),
                    "a liability until the month is served", MONEY, agg="end")
    rows["deferred_sub"] = this
    r += 1

    r = band(ws, r, "TOTAL REVENUE")
    r = month_header(ws, r)
    inst, sub = rows["institutional"], rows["sub_revenue"]
    r = monthly_row(ws, r, "Total revenue", lambda m:
                    f"={ml(m)}{inst}+{ml(m)}{sub}", "", MONEY, bold=True,
                    fill_colour=F.LIME)
    rows["total"] = r - 1
    tot = rows["total"]
    r = monthly_row(ws, r, "Institutional share of revenue", lambda m:
                    f"=IFERROR({ml(m)}{inst}/{ml(m)}{tot},0)", "", PCT,
                    agg="avg")
    rows["inst_share"] = r - 1
    R["Revenue"] = rows
    return ws


def finish_revenue(wb):
    """Fill the two subscription rows that depend on the Acquisition sheet."""
    ws = wb["Revenue"]
    acq = R["Acquisition"]
    for dest, src in (("new_subs", acq["new_paid"]),
                      ("active_subs", acq["active_paid"])):
        row = R["Revenue"][dest]
        for m in range(1, F.MONTHS + 1):
            ws.cell(row, mcol(m), f"={mref('Acquisition', src, m)}")


# =====================================================================
#  07 · ACQUISITION
# =====================================================================
def build_acquisition(wb):
    ws = wb.create_sheet("Acquisition")
    setup_monthly(ws, "Acquisition",
                  "Two funnels. Offline channels create sign-ups and "
                  "institutional leads; online channels create reach. Both land "
                  "on the same first step — Mission 01 — and only then on a "
                  "paid plan.",
                  freeze="C7")
    rows = {}
    RV = R["Revenue"]
    ycol = {1: "C", 2: "D", 3: "E"}

    # ---------------------------------------------------- offline channels
    r = band(ws, 5, "OFFLINE CHANNELS — THEY CREATE SIGN-UPS")
    r = month_header(ws, r)
    off_cost, off_sign, off_lead = [], [], []
    for label, arow in zip(A["off_labels"], A["off_rows"]):
        act = f"Assumptions!${ycol[1]}${arow}"
        r = monthly_row(ws, r, label, lambda m, a=arow:
                        f"=Assumptions!${ycol[year_of(m)]}${a}",
                        "activities in the month", NUM1)
        arow_m = r - 1
        r = monthly_row(ws, r, "Cost", lambda m, a=arow, x=arow_m:
                        f"={ml(m)}{x}*Assumptions!$F${a}", "", MONEY, indent=1)
        off_cost.append(r - 1)
        r = monthly_row(ws, r, "Free sign-ups", lambda m, a=arow, x=arow_m:
                        f"={ml(m)}{x}*Assumptions!$G${a}", "", NUM, indent=1)
        off_sign.append(r - 1)
        r = monthly_row(ws, r, "Institutional leads", lambda m, a=arow, x=arow_m:
                        f"={ml(m)}{x}*Assumptions!$H${a}", "", NUM1, indent=1)
        off_lead.append(r - 1)
    r = monthly_row(ws, r, "Offline marketing cost", lambda m:
                    "=" + "+".join(f"{ml(m)}{x}" for x in off_cost), "",
                    MONEY, bold=True, fill_colour=F.BAND)
    rows["off_cost"] = r - 1
    r = monthly_row(ws, r, "Offline sign-ups", lambda m:
                    "=" + "+".join(f"{ml(m)}{x}" for x in off_sign), "",
                    NUM, bold=True)
    rows["off_signups"] = r - 1
    r = monthly_row(ws, r, "Offline institutional leads", lambda m:
                    "=" + "+".join(f"{ml(m)}{x}" for x in off_lead), "",
                    NUM1, bold=True)
    rows["off_leads"] = r - 1
    r += 1

    # ----------------------------------------------------- online channels
    r = band(ws, r, "ONLINE CHANNELS — THEY CREATE REACH")
    r = month_header(ws, r)
    on_cost, on_sign, on_reach = [], [], []
    for label, arow in zip(A["on_labels"], A["on_rows"]):
        r = monthly_row(ws, r, label, lambda m, a=arow:
                        f"=Assumptions!${ycol[year_of(m)]}${a}",
                        "spend in the month", MONEY)
        spend = r - 1
        on_cost.append(spend)
        r = monthly_row(ws, r, "Reach", lambda m, a=arow, s=spend:
                        f"=IFERROR({ml(m)}{s}/Assumptions!$F${a}*1000,0)", "",
                        NUM, indent=1)
        reach = r - 1
        on_reach.append(reach)
        r = monthly_row(ws, r, "Free sign-ups", lambda m, a=arow, x=reach:
                        f"={ml(m)}{x}*Assumptions!$G${a}*Assumptions!$H${a}",
                        "reach x click-through x conversion", NUM, indent=1)
        on_sign.append(r - 1)
    r = monthly_row(ws, r, "Online marketing cost", lambda m:
                    "=" + "+".join(f"{ml(m)}{x}" for x in on_cost), "", MONEY,
                    bold=True, fill_colour=F.BAND)
    rows["on_cost"] = r - 1
    r = monthly_row(ws, r, "Online reach", lambda m:
                    "=" + "+".join(f"{ml(m)}{x}" for x in on_reach), "", NUM,
                    bold=True)
    rows["on_reach"] = r - 1
    r = monthly_row(ws, r, "Online sign-ups", lambda m:
                    "=" + "+".join(f"{ml(m)}{x}" for x in on_sign), "", NUM,
                    bold=True)
    rows["on_signups"] = r - 1
    r = monthly_row(ws, r, "Total marketing cost", lambda m:
                    f"={ml(m)}{rows['off_cost']}+{ml(m)}{rows['on_cost']}",
                    "carried to the Expenses sheet", MONEY, bold=True,
                    fill_colour=F.LIME)
    rows["marketing"] = r - 1
    r += 1

    # ------------------------------------------------ institutional funnel
    r = band(ws, r, "INSTITUTIONAL FUNNEL — MAP, MEET, SIGN")
    r = month_header(ws, r)
    r = monthly_row(ws, r, "Inbound enquiries from content", lambda m:
                    f"={ml(m)}{rows['on_signups']}/1000*{A['inbound_rate']}",
                    "podcast, search and the readiness report", NUM1)
    inbound = r - 1
    r = monthly_row(ws, r, "Total institutional leads", lambda m:
                    f"={ml(m)}{rows['off_leads']}+{ml(m)}{inbound}", "", NUM1,
                    bold=True)
    leads = r - 1
    r = monthly_row(ws, r, "First meetings held", lambda m:
                    f"={ml(m)}{leads}*{price('c_meet', m)}", "", NUM1)
    meets = r - 1
    r = monthly_row(ws, r, "Proposals, pilots and bids submitted", lambda m:
                    f"={ml(m)}{meets}*{price('c_prop', m)}", "", NUM1)
    props = r - 1
    r = monthly_row(ws, r, "Contracts signed", lambda m:
                    f"=IFERROR(INDEX($C{props}:$AL{props},1,{m}-{A['cycle']})"
                    f"*{price('c_win', m)},0)",
                    "proposals lagged by the sales cycle", NUM1, bold=True)
    won = r - 1
    rows["won"] = won
    r = monthly_row(ws, r, "Contracts the delivery plan requires", lambda m:
                    "=(" + "+".join(
                        f"Revenue!{ml(m)}${RV[k]}" for k in
                        ("uni_cohorts_eg", "uni_cohorts_ksa", "uni_licences",
                         "school_cohorts", "school_licences", "tvet_cohorts",
                         "tot_cohorts", "ngo_programmes", "competitions",
                         "corporates"))
                    + f")/{price('per_contract', m)}",
                    "deliveries, over deliveries per contract", NUM1,
                    colour=F.LINK_FONT)
    need = r - 1
    r = monthly_row(ws, r, "Coverage — signings against the plan", lambda m:
                    f"=IFERROR({ml(m)}{won}/{ml(m)}{need},0)",
                    "below 1.0x means the funnel is short", PCT, bold=True,
                    agg="avg")
    rows["coverage"] = r - 1
    r = monthly_row(ws, r, "Cost per institutional contract won", lambda m:
                    f"=IFERROR(({ml(m)}{rows['off_cost']}+{ml(m)}"
                    f"{rows['on_cost']}*{A['online_inst_share']})/{ml(m)}{won},0)",
                    "institutional CAC", MONEY, agg="avg")
    rows["cac_inst"] = r - 1
    r += 1

    # ----------------------------------------------------- learner funnel
    r = band(ws, r, "LEARNER FUNNEL — EVERY CHANNEL LANDS ON MISSION 01")
    r = month_header(ws, r)
    r = monthly_row(ws, r, "Reached — cohort participants", lambda m:
                    f"=(Revenue!{ml(m)}${RV['uni_cohorts_eg']}+Revenue!{ml(m)}$"
                    f"{RV['uni_cohorts_ksa']}+Revenue!{ml(m)}${RV['uni_pilots']})"
                    f"*{A['cohort_size']}+(Revenue!{ml(m)}${RV['school_cohorts']}"
                    f"+Revenue!{ml(m)}${RV['tvet_cohorts']})*{A['school_size']}",
                    "university, school and technical", NUM)
    reach_cohort = r - 1
    r = monthly_row(ws, r, "Reached — competition entrants", lambda m:
                    f"=Revenue!{ml(m)}${RV['competitions']}*{A['entrants_per_comp']}",
                    "entry is a free account", NUM)
    reach_comp = r - 1
    r = monthly_row(ws, r, "Reached — sponsored and programme seats", lambda m:
                    f"=Revenue!{ml(m)}${RV['initiative_seats']}+Revenue!{ml(m)}$"
                    f"{RV['prog_seats']}", "", NUM)
    reach_seats = r - 1
    r = monthly_row(ws, r, "Reached — NGO and corporate participants", lambda m:
                    f"=Revenue!{ml(m)}${RV['ngo_programmes']}*{A['part_ngo']}"
                    f"+Revenue!{ml(m)}${RV['corporates']}*{A['part_corp']}", "", NUM)
    reach_ngo = r - 1
    r = monthly_row(ws, r, "Free accounts — through an institution", lambda m:
                    f"={ml(m)}{reach_cohort}+{ml(m)}{reach_comp}+{ml(m)}"
                    f"{reach_seats}+{ml(m)}{reach_ngo}", "", NUM, bold=True)
    inst_signups = r - 1
    r = monthly_row(ws, r, "Free accounts — direct, offline and online",
                    lambda m: f"={ml(m)}{rows['off_signups']}+{ml(m)}"
                              f"{rows['on_signups']}", "", NUM, bold=True)
    direct_signups = r - 1
    r = monthly_row(ws, r, "Total new free accounts", lambda m:
                    f"={ml(m)}{inst_signups}+{ml(m)}{direct_signups}", "", NUM,
                    bold=True, fill_colour=F.BAND)
    rows["signups"] = r - 1
    r = monthly_row(ws, r, "Activated — Mission 01 completed", lambda m:
                    f"=({ml(m)}{inst_signups}+{ml(m)}{direct_signups})"
                    f"*{price('c_act', m)}",
                    "activation is finishing Mission 01, not opening an account",
                    NUM, bold=True)
    rows["activated"] = r - 1
    r = monthly_row(ws, r, "Engaged — through an institution", lambda m:
                    f"={ml(m)}{inst_signups}*{price('c_act', m)}"
                    f"*{price('c_eng', m)}", "", NUM, indent=1)
    eng_inst = r - 1
    r = monthly_row(ws, r, "Engaged — direct", lambda m:
                    f"={ml(m)}{direct_signups}*{price('c_act', m)}"
                    f"*{price('c_eng', m)}", "", NUM, indent=1)
    eng_dir = r - 1
    r = monthly_row(ws, r, "New paid subscribers", lambda m:
                    f"={ml(m)}{eng_inst}*{price('c_pay_inst', m)}+{ml(m)}"
                    f"{eng_dir}*{price('c_pay_online', m)}",
                    "institutional reach converts far better", NUM, bold=True,
                    fill_colour=F.LIME)
    rows["new_paid"] = r - 1
    np_ = rows["new_paid"]
    this = r
    r = monthly_row(ws, r, "Active paid subscribers", lambda m, t=this:
                    (f"={ml(m)}{np_}" if m == 1
                     else f"={ml(m - 1)}{t}*(1-{A['sub_churn']})+{ml(m)}{np_}"),
                    "after monthly churn", NUM, bold=True, agg="end")
    rows["active_paid"] = this
    r = monthly_row(ws, r, "Cost per paid subscriber", lambda m:
                    f"=IFERROR({ml(m)}{rows['on_cost']}"
                    f"*(1-{A['online_inst_share']})/{ml(m)}{np_},0)",
                    "learner CAC, on the online spend only", MONEY, agg="avg")
    rows["cac_learner"] = r - 1
    R["Acquisition"] = rows
    return ws


# =====================================================================
#  09 · EXPENSES
# =====================================================================
def build_expenses(wb):
    ws = wb.create_sheet("Expenses")
    setup_monthly(ws, "Expenses",
                  "Direct cost moves with delivery; operating cost does not. "
                  "Payroll comes from the HR model, marketing from the "
                  "acquisition sheet and depreciation from the asset register, "
                  "so none of the three is typed twice.",
                  freeze="C7")
    rows = {}
    RV, AQ = R["Revenue"], R["Acquisition"]
    fac = f"{A['fac_rate']}*{A['fac_per']}"

    r = band(ws, 5, "DIRECT COST OF DELIVERY")
    r = month_header(ws, r)
    cogs_first = r
    direct = [
        ("Facilitation — university cohorts", lambda m:
         f"=(Revenue!{ml(m)}${RV['uni_cohorts_eg']}+Revenue!{ml(m)}${RV['uni_cohorts_ksa']}"
         f"+Revenue!{ml(m)}${RV['uni_pilots']})*{fac}*{A['d_uni']}",
         "certified freelancers, never employees"),
        ("Facilitation — school cohorts", lambda m:
         f"=Revenue!{ml(m)}${RV['school_cohorts']}*{fac}*{A['d_school']}", ""),
        ("Facilitation — technical cohorts", lambda m:
         f"=Revenue!{ml(m)}${RV['tvet_cohorts']}*{fac}*{A['d_tvet']}", ""),
        ("Materials, kits and showcases", lambda m:
         f"=(Revenue!{ml(m)}${RV['uni_cohorts_eg']}+Revenue!{ml(m)}${RV['uni_cohorts_ksa']}"
         f"+Revenue!{ml(m)}${RV['uni_pilots']})*{A['m_uni']}"
         f"+Revenue!{ml(m)}${RV['school_cohorts']}*{A['m_school']}"
         f"+Revenue!{ml(m)}${RV['tvet_cohorts']}*{A['m_tvet']}", ""),
        ("Train-the-trainer delivery", lambda m:
         f"=Revenue!{ml(m)}${RV['tot_cohorts']}*{A['c_tot']}", ""),
        ("NGO and donor programme delivery", lambda m:
         f"=Revenue!{ml(m)}${RV['ngo_programmes']}*{A['c_ngo']}", "multi-site"),
        ("Competition delivery and judging", lambda m:
         f"=Revenue!{ml(m)}${RV['competitions']}*{A['c_comp']}", ""),
        ("Corporate programme delivery", lambda m:
         f"=Revenue!{ml(m)}${RV['corporates']}*{A['c_corp']}", ""),
        ("National initiative seat support", lambda m:
         f"=Revenue!{ml(m)}${RV['initiative_seats']}*{A['c_seat_init']}",
         "provisioning, support queue, partner reporting"),
        ("Programme and incubator seat support", lambda m:
         f"=Revenue!{ml(m)}${RV['prog_seats']}*{A['c_seat_prog']}", ""),
        ("Subscription hosting and inference", lambda m:
         f"={mref('Acquisition', AQ['active_paid'], m)}*{A['c_sub']}", ""),
    ]
    for label, fn, note in direct:
        r = monthly_row(ws, r, label, fn, note, MONEY)
    r = monthly_row(ws, r, "Revenue share — certified delivery partners",
                    lambda m:
                    f"=(Revenue!{ml(m)}${RV['rev_University cohort programmes']}+Revenue!{ml(m)}$"
                    f"{RV['rev_School cohorts']}+Revenue!{ml(m)}$"
                    f"{RV['rev_Technical and vocational cohorts']})"
                    f"*{price('pd_share', m)}*{A['pd_rate']}",
                    "party 1 · they deliver, StartPad audits", MONEY)
    rows["rs1"] = r - 1
    r = monthly_row(ws, r, "Revenue share — youth and channel organisations",
                    lambda m:
                    f"=Revenue!{ml(m)}${RV['rev_Sponsored competitions']}"
                    f"*{price('ch_comp_rate', m)}+Revenue!{ml(m)}$"
                    f"{RV['rev_Programme and incubator seats']}"
                    f"*{price('ch_seat_rate', m)}",
                    "party 2 · Enactus, INJAZ, chapters", MONEY)
    rows["rs2"] = r - 1
    r = monthly_row(ws, r, "Revenue share — aggregators and payment processing",
                    lambda m:
                    f"=Revenue!{ml(m)}${RV['rev_National initiative seats']}"
                    f"*{price('ag_seat_rate', m)}+Revenue!{ml(m)}${RV['sub_revenue']}"
                    f"*{A['pay_rate']}",
                    "party 3 · distributors and card fees", MONEY)
    rows["rs3"] = r - 1
    cogs_last = r - 1
    r = monthly_row(ws, r, "Total direct cost", lambda m:
                    f"=SUM({ml(m)}{cogs_first}:{ml(m)}{cogs_last})", "", MONEY,
                    bold=True, fill_colour=F.BAND)
    rows["cogs"] = r - 1
    cogs = rows["cogs"]
    r = monthly_row(ws, r, "Gross profit", lambda m:
                    f"={mref('Revenue', RV['total'], m)}-{ml(m)}{cogs}", "",
                    MONEY, bold=True, fill_colour=F.LIME)
    rows["gross_profit"] = r - 1
    gp = rows["gross_profit"]
    r = monthly_row(ws, r, "Gross margin", lambda m:
                    f"=IFERROR({ml(m)}{gp}/{mref('Revenue', RV['total'], m)},0)",
                    "", PCT, agg="avg")
    rows["gross_margin"] = r - 1
    r += 1

    r = band(ws, r, "OPERATING COST")
    r = month_header(ws, r)
    opex_first = r
    hr, dep = R["HR_Model"], R["Depreciation"]
    opex = [
        ("Payroll — fully loaded", lambda m:
         f"={mref('HR_Model', hr['payroll'], m)}", "from the HR model",
         F.LINK_FONT),
        ("Sales commission", lambda m:
         f"={mref('Revenue', RV['institutional'], m)}*{A['commission']}",
         "on institutional revenue", F.INK),
        ("Ambassador stipends", lambda m:
         f"={price('amb_count', m)}*{A['amb_stipend']}*{A['amb_months']}/12",
         "a stipend and standing, not a salary", F.INK),
        ("Marketing — offline channels", lambda m:
         f"={mref('Acquisition', AQ['off_cost'], m)}", "from Acquisition",
         F.LINK_FONT),
        ("Marketing — online channels", lambda m:
         f"={mref('Acquisition', AQ['on_cost'], m)}", "from Acquisition",
         F.LINK_FONT),
        ("Office rent", lambda m:
         f"={price('o_rent_cairo', m)}+{price('o_rent_riyadh', m)}",
         "Cairo, and a Riyadh desk from year two", F.INK),
        ("Utilities, internet and communications", lambda m:
         f"={price('o_util', m)}", "", F.INK),
        ("Cloud, AI inference and APIs", lambda m:
         f"={price('o_cloud_fixed', m)}+({mref('Acquisition', AQ['signups'], m)}"
         f"+{mref('Acquisition', AQ['active_paid'], m)})*{A['o_cloud_var']}",
         "fixed, plus a charge per active learner", F.INK),
        ("Software and tooling", lambda m:
         f"={mref('HR_Model', hr['headcount'], m)}*{price('o_software', m)}",
         "per employee", F.INK),
        ("Travel", lambda m:
         f"={mref('HR_Model', hr['commercial'], m)}*{price('o_travel', m)}",
         "per commercial head", F.INK),
        ("Outsourced finance, legal and audit", lambda m:
         f"={price('o_prof', m)}", "bought, not hired", F.INK),
        ("Safeguarding and compliance", lambda m: f"={price('o_safe', m)}",
         "a condition of entry to the school market", F.INK),
        ("Partner enablement — certification and audit", lambda m:
         f"={price('o_partner', m)}", "what keeps the licence meaningful",
         F.INK),
        ("Insurance, bank charges and sundries", lambda m:
         f"={price('o_sundry', m)}", "", F.INK),
    ]
    for label, fn, note, colour in opex:
        r = monthly_row(ws, r, label, fn, note, MONEY, colour=colour)
    opex_last = r - 1
    r = monthly_row(ws, r, "Contingency", lambda m:
                    f"=SUM({ml(m)}{opex_first}:{ml(m)}{opex_last})"
                    f"*{A['contingency']}", "on operating cost", MONEY)
    cont = r - 1
    r = monthly_row(ws, r, "Operating cost before depreciation", lambda m:
                    f"=SUM({ml(m)}{opex_first}:{ml(m)}{opex_last})"
                    f"+{ml(m)}{cont}", "", MONEY, bold=True,
                    fill_colour=F.BAND)
    rows["opex_cash"] = r - 1
    r = monthly_row(ws, r, "Depreciation and amortisation", lambda m:
                    f"={mref('Depreciation', dep['charge'], m)}",
                    "from the asset register", MONEY, colour=F.LINK_FONT)
    rows["dna"] = r - 1
    r = monthly_row(ws, r, "Total operating cost", lambda m:
                    f"={ml(m)}{rows['opex_cash']}+{ml(m)}{rows['dna']}", "",
                    MONEY, bold=True, fill_colour=F.BAND)
    rows["opex_total"] = r - 1
    r += 1

    r = band(ws, r, "RESULT")
    r = month_header(ws, r)
    r = monthly_row(ws, r, "EBITDA", lambda m:
                    f"={ml(m)}{gp}-{ml(m)}{rows['opex_cash']}", "", MONEY,
                    bold=True, fill_colour=F.LIME)
    rows["ebitda"] = r - 1
    r = monthly_row(ws, r, "EBIT — operating profit", lambda m:
                    f"={ml(m)}{rows['ebitda']}-{ml(m)}{rows['dna']}", "",
                    MONEY, bold=True, fill_colour=F.LIME)
    rows["ebit"] = r - 1
    eb = rows["ebit"]
    r = monthly_row(ws, r, "Cash operating cost, excluding payroll", lambda m:
                    f"={ml(m)}{rows['opex_cash']}"
                    f"-{mref('HR_Model', hr['payroll'], m)}",
                    "used for the payables calculation", MONEY)
    rows["opex_ex_payroll"] = r - 1
    R["Expenses"] = rows
    return ws


# =====================================================================
#  11 · INCOME STATEMENT
# =====================================================================
def build_income_statement(wb):
    ws = wb.create_sheet("Income_Statement")
    sheet_title(ws, "Income Statement",
                "Three years to 30 September. Every line is the sum of its "
                "thirty-six monthly cells, so the annual figures cannot drift "
                "from the monthly model.", last_col=9)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 30
    for col in "CDE":
        ws.column_dimensions[col].width = 15
    for col in "FGH":
        ws.column_dimensions[col].width = 11
    rows = {}
    EX, RV = R["Expenses"], R["Revenue"]

    r = band(ws, 5, "FOR THE YEARS ENDED 30 SEPTEMBER", last_col=9)
    hdr = r
    for i, t in enumerate(["Year 1", "Year 2", "Year 3"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(9, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center")
    for i, t in enumerate(["% rev Y1", "% rev Y2", "% rev Y3"]):
        c = ws.cell(hdr, 6 + i, t)
        c.font = f(8, True, F.INK)
        c.fill = fill(F.LIME)
        c.alignment = Alignment(horizontal="center")
    ws.cell(hdr, 1, "").fill = fill(F.UV_DARK)
    ws.cell(hdr, 2, "").fill = fill(F.UV_DARK)
    r += 1

    def line(label, sheet, srow, note="", bold=False, pct_of_rev=True,
             indent=0, fmt=MONEY, band_fill=None):
        nonlocal r
        write_row(ws, r, label, note, bold=bold, indent=indent,
                  fill_colour=band_fill)
        for y in (1, 2, 3):
            c = ws.cell(r, 2 + y, f"={sheet}!{yl(y)}${srow}")
            c.number_format = fmt
            c.font = f(9, bold, F.LINK_FONT if not bold else F.INK)
        rows[label] = r
        if pct_of_rev:
            for y in (1, 2, 3):
                c = ws.cell(r, 5 + y,
                            f"=IFERROR({get_column_letter(2 + y)}{r}"
                            f"/{get_column_letter(2 + y)}${rows.get('rev_row', r)},0)")
                c.number_format = PCT
                c.font = f(8, False, "6B7285")
        r += 1

    line("Institutional revenue", "Revenue", RV["institutional"],
         "engines 1 to 7", pct_of_rev=False)
    line("Founder subscription revenue", "Revenue", RV["sub_revenue"],
         "engine 8, recognised monthly", pct_of_rev=False)
    line("Total revenue", "Revenue", RV["total"], "", bold=True,
         pct_of_rev=False, band_fill=F.BAND)
    rows["rev_row"] = rows["Total revenue"]
    rr = rows["rev_row"]
    for y in (1, 2, 3):
        c = ws.cell(rr, 5 + y, 1)
        c.number_format = PCT
        c.font = f(8, False, "6B7285")
    line("Direct cost of delivery", "Expenses", EX["cogs"],
         "facilitation, materials, seats and revenue share")
    line("Gross profit", "Expenses", EX["gross_profit"], "", bold=True,
         band_fill=F.BAND)
    line("Operating cost before depreciation", "Expenses", EX["opex_cash"],
         "payroll, marketing, premises and overhead")
    line("EBITDA", "Expenses", EX["ebitda"], "", bold=True, band_fill=F.LIME)
    line("Depreciation and amortisation", "Expenses", EX["dna"], "")
    line("EBIT — operating profit", "Expenses", EX["ebit"], "", bold=True,
         band_fill=F.BAND)
    r += 1

    write_row(ws, r, "Profit before tax", "no debt in the plan, so no interest",
              bold=True)
    for y in (1, 2, 3):
        c = ws.cell(r, 2 + y, f"={get_column_letter(2 + y)}{rows['EBIT — operating profit']}")
        c.number_format = MONEY
        c.font = f(9, True)
    rows["ebt"] = r
    ebt = r
    r += 1

    write_row(ws, r, "Tax losses carried forward, opening",
              "year one's loss shelters year two")
    for y in (1, 2, 3):
        col = get_column_letter(2 + y)
        if y == 1:
            c = ws.cell(r, 2 + y, 0)
        else:
            prev = get_column_letter(1 + y)
            c = ws.cell(r, 2 + y, f"={prev}{r + 1}")
        c.number_format = MONEY
        c.font = f(9)
    cf_open = r
    r += 1
    write_row(ws, r, "Tax losses carried forward, closing", "")
    for y in (1, 2, 3):
        col = get_column_letter(2 + y)
        c = ws.cell(r, 2 + y,
                    f"=MAX(0,{col}{cf_open}-MAX(0,{col}{ebt}))"
                    f"+MAX(0,-{col}{ebt})")
        c.number_format = MONEY
        c.font = f(9)
    r += 1
    write_row(ws, r, "Taxable profit", "after the carried-forward loss")
    for y in (1, 2, 3):
        col = get_column_letter(2 + y)
        c = ws.cell(r, 2 + y, f"=MAX(0,{col}{ebt}-{col}{cf_open})")
        c.number_format = MONEY
        c.font = f(9)
    taxable = r
    r += 1
    write_row(ws, r, "Corporate income tax", "Egyptian rate on taxable profit")
    for y in (1, 2, 3):
        col = get_column_letter(2 + y)
        c = ws.cell(r, 2 + y, f"=-{col}{taxable}*{A['tax_rate']}")
        c.number_format = MONEY
        c.font = f(9)
    rows["tax"] = r
    r += 1
    write_row(ws, r, "Net profit for the year", "", bold=True,
              fill_colour=F.LIME)
    for y in (1, 2, 3):
        col = get_column_letter(2 + y)
        c = ws.cell(r, 2 + y, f"={col}{ebt}+{col}{rows['tax']}")
        c.number_format = MONEY
        c.font = f(10, True)
        pc = ws.cell(r, 5 + y, f"=IFERROR({col}{r}/{col}{rr},0)")
        pc.number_format = PCT
        pc.font = f(8, False, "6B7285")
    rows["net"] = r
    R["Income_Statement"] = rows
    return ws


# =====================================================================
#  13 · CASH FLOW
# =====================================================================
def build_cash_flow(wb):
    ws = wb.create_sheet("Cash_Flow")
    setup_monthly(ws, "Cash Flow",
                  "Indirect method, monthly, with the working-capital balances "
                  "the balance sheet is built from. Institutional customers pay "
                  "slowly, which is the single largest cash risk in the model.",
                  freeze="C7")
    rows = {}
    EX, RV, HR_, CP = R["Expenses"], R["Revenue"], R["HR_Model"], R["Capex"]
    IS = R["Income_Statement"]
    taxrow = IS["tax"]

    r = band(ws, 5, "OPERATING ACTIVITIES")
    r = month_header(ws, r)
    r = monthly_row(ws, r, "EBIT — operating profit", lambda m:
                    f"={mref('Expenses', EX['ebit'], m)}", "", MONEY,
                    colour=F.LINK_FONT)
    ebit = r - 1
    r = monthly_row(ws, r, "Corporate income tax charge", lambda m:
                    f"=Income_Statement!${get_column_letter(2 + year_of(m))}"
                    f"${taxrow}/12", "the year's charge, spread evenly", MONEY,
                    colour=F.LINK_FONT)
    taxchg = r - 1
    r = monthly_row(ws, r, "Net profit", lambda m:
                    f"={ml(m)}{ebit}+{ml(m)}{taxchg}", "", MONEY, bold=True)
    rows["net"] = r - 1
    net = rows["net"]
    r = monthly_row(ws, r, "Add back depreciation and amortisation", lambda m:
                    f"={mref('Expenses', EX['dna'], m)}", "non-cash", MONEY,
                    colour=F.LINK_FONT)
    dna = r - 1
    r += 0

    r = band(ws, r, "WORKING CAPITAL BALANCES AT MONTH END")
    r = month_header(ws, r)
    r = monthly_row(ws, r, "Trade receivables", lambda m:
                    f"={mref('Revenue', RV['institutional'], m)}"
                    f"*{A['dso']}/30"
                    f"+{mref('Revenue', RV['sub_revenue'], m)}"
                    f"*{A['dso_sub']}/30",
                    "institutions pay slowly; cards settle at once", MONEY,
                    agg="end")
    rows["ar"] = r - 1
    ar = rows["ar"]
    r = monthly_row(ws, r, "Trade and other payables", lambda m:
                    f"=({mref('Expenses', EX['cogs'], m)}"
                    f"+{mref('Expenses', EX['opex_ex_payroll'], m)})"
                    f"*{A['dpo']}/30", "suppliers and freelancers", MONEY,
                    agg="end")
    rows["ap"] = r - 1
    ap = rows["ap"]
    r = monthly_row(ws, r, "Accrued payroll", lambda m:
                    f"={mref('HR_Model', HR_['payroll'], m)}"
                    f"*{A['acc_days']}/30", "", MONEY, agg="end")
    rows["accrued"] = r - 1
    acc = rows["accrued"]
    r = monthly_row(ws, r, "Deferred revenue", lambda m:
                    f"={mref('Revenue', RV['deferred_sub'], m)}"
                    f"+{mref('Revenue', RV['institutional'], m)}"
                    f"*{A['adv_share']}",
                    "annual plans and contracts billed in advance", MONEY,
                    agg="end")
    rows["deferred"] = r - 1
    dfr = rows["deferred"]

    tp = r
    r = monthly_row(ws, r, "Tax payable", lambda m, t=tp:
                    (f"=-{ml(m)}{taxchg}" if m == 1 else
                     f"={ml(m - 1)}{t}-{ml(m)}{taxchg}-{ml(m)}{t + 1}"),
                    "paid in arrears, in the stated month", MONEY, agg="end")
    rows["taxpay"] = tp
    r = monthly_row(ws, r, "Tax paid in the month", lambda m:
                    (f"=IF({m}=12+{A['tax_pay_month']},"
                     f"-Income_Statement!$C${taxrow},0)" if year_of(m) == 2 else
                     (f"=IF({m}=24+{A['tax_pay_month']},"
                      f"-Income_Statement!$D${taxrow},0)" if year_of(m) == 3
                      else "=0")),
                    "the prior year's charge", MONEY)
    taxpaid = r - 1
    r += 0

    r = band(ws, r, "CASH FLOW")
    r = month_header(ws, r)
    for label, bal, note in (("(Increase) decrease in receivables", ar,
                              "the cash cost of a 75-day collection cycle"),
                             ("Increase (decrease) in payables", ap, ""),
                             ("Increase (decrease) in accrued payroll", acc, ""),
                             ("Increase (decrease) in deferred revenue", dfr,
                              "cash received before the service is given")):
        sign = "-" if "receivab" in label else ""
        r = monthly_row(ws, r, label, lambda m, b=bal, s=sign:
                        (f"={s}{ml(m)}{b}" if m == 1
                         else f"={s}({ml(m)}{b}-{ml(m - 1)}{b})"), note, MONEY)
        rows["d_" + str(bal)] = r - 1
    d_ar, d_ap, d_acc, d_dfr = (rows["d_" + str(x)] for x in (ar, ap, acc, dfr))
    r = monthly_row(ws, r, "Increase (decrease) in tax payable", lambda m:
                    (f"={ml(m)}{tp}" if m == 1
                     else f"={ml(m)}{tp}-{ml(m - 1)}{tp}"), "", MONEY)
    d_tax = r - 1
    r = monthly_row(ws, r, "Net cash from operating activities", lambda m:
                    f"={ml(m)}{net}+{ml(m)}{dna}+{ml(m)}{d_ar}+{ml(m)}{d_ap}"
                    f"+{ml(m)}{d_acc}+{ml(m)}{d_dfr}+{ml(m)}{d_tax}", "",
                    MONEY, bold=True, fill_colour=F.BAND)
    rows["cfo"] = r - 1
    cfo = rows["cfo"]
    r = monthly_row(ws, r, "Capital expenditure", lambda m:
                    f"=-{mref('Capex', CP['capex'], m)}",
                    "laptops, desks, fit-out, capitalised build", MONEY,
                    colour=F.LINK_FONT)
    capex = r - 1
    r = monthly_row(ws, r, "Net cash used in investing activities", lambda m:
                    f"={ml(m)}{capex}", "", MONEY, bold=True)
    rows["cfi"] = r - 1
    cfi = rows["cfi"]
    r = monthly_row(ws, r, "Share capital raised", lambda m:
                    f"=IF({m}={A['seed_month']},{A['seed']},0)",
                    "the seed round in the month it lands", MONEY)
    raise_ = r - 1
    r = monthly_row(ws, r, "Net cash from financing activities", lambda m:
                    f"={ml(m)}{raise_}", "", MONEY, bold=True)
    rows["cff"] = r - 1
    cff = rows["cff"]
    r = monthly_row(ws, r, "Net movement in cash", lambda m:
                    f"={ml(m)}{cfo}+{ml(m)}{cfi}+{ml(m)}{cff}", "", MONEY,
                    bold=True)
    move = r - 1
    opening = r
    r = monthly_row(ws, r, "Cash at the start of the month", lambda m, t=opening:
                    (f"={A['open_cash']}" if m == 1
                     else f"={ml(m - 1)}{t + 1}"), "", MONEY, agg="min")
    r = monthly_row(ws, r, "Cash at the end of the month", lambda m, o=opening:
                    f"={ml(m)}{o}+{ml(m)}{move}", "", MONEY, bold=True,
                    agg="end", fill_colour=F.LIME)
    rows["cash"] = r - 1
    cash = rows["cash"]
    r = monthly_row(ws, r, "Headroom against the minimum cash buffer",
                    lambda m: f"={ml(m)}{cash}-{A['min_cash']}",
                    "negative means the buffer is breached", MONEY, agg="min")
    rows["headroom"] = r - 1
    r += 1

    # --------------------------------------------- annual statement
    r = band(ws, r, "CASH FLOW STATEMENT — ANNUAL")
    hdr = r
    for i, t in enumerate(["Year 1", "Year 2", "Year 3"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(9, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center")
    r += 1
    annual = [
        ("Net profit for the year", net, "sum", False),
        ("Depreciation and amortisation", dna, "sum", False),
        ("(Increase) decrease in receivables", d_ar, "sum", False),
        ("Increase (decrease) in payables", d_ap, "sum", False),
        ("Increase (decrease) in accrued payroll", d_acc, "sum", False),
        ("Increase (decrease) in deferred revenue", d_dfr, "sum", False),
        ("Increase (decrease) in tax payable", d_tax, "sum", False),
        ("Net cash from operating activities", cfo, "sum", True),
        ("Net cash used in investing activities", cfi, "sum", True),
        ("Net cash from financing activities", cff, "sum", True),
        ("Net movement in cash", move, "sum", True),
        ("Cash at the end of the year", cash, "end", True),
    ]
    for label, srow, agg, bold in annual:
        write_row(ws, r, label, "", bold=bold,
                  fill_colour=F.BAND if bold else None)
        for y in (1, 2, 3):
            formula = (f"={yl(y)}{srow}" if agg == "sum"
                       else f"={ml(list(months_of(y))[-1])}{srow}")
            c = ws.cell(r, 2 + y, formula)
            c.number_format = MONEY
            c.font = f(9, bold)
        rows["ann_" + label] = r
        r += 1
    R["Cash_Flow"] = rows
    return ws


# =====================================================================
#  12 · BALANCE SHEET
# =====================================================================
def build_balance_sheet(wb):
    ws = wb.create_sheet("Balance_Sheet")
    sheet_title(ws, "Balance Sheet",
                "At 30 September each year, with the opening position at "
                "inception. The check line at the foot is nil in every column, "
                "which is the only proof that the model hangs together.",
                last_col=7)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 32
    for col in "CDEF":
        ws.column_dimensions[col].width = 15
    rows = {}
    CF, DEP, IS = R["Cash_Flow"], R["Depreciation"], R["Income_Statement"]
    AC = R["Actuals"]

    r = band(ws, 5, "STATEMENT OF FINANCIAL POSITION", last_col=7)
    hdr = r
    for i, t in enumerate(["At inception", "Year 1", "Year 2", "Year 3"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(9, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center")
    for col in (1, 2):
        ws.cell(hdr, col).fill = fill(F.UV_DARK)
    r += 1

    def bs_line(label, note, open_f, year_f, bold=False, fill_c=None,
                indent=0):
        nonlocal r
        write_row(ws, r, label, note, bold=bold, indent=indent,
                  fill_colour=fill_c)
        c = ws.cell(r, 3, open_f)
        c.number_format = MONEY
        c.font = f(9, bold)
        for y in (1, 2, 3):
            c = ws.cell(r, 3 + y, year_f(y))
            c.number_format = MONEY
            c.font = f(9, bold)
        rows[label] = r
        r += 1
        return r - 1

    last_m = {y: list(months_of(y))[-1] for y in (1, 2, 3)}
    cash = bs_line("Cash and cash equivalents", "see the cash flow statement",
                   f"=Actuals!$C${AC['Cash at bank']}",
                   lambda y: f"=Cash_Flow!{ml(last_m[y])}${CF['cash']}")
    ar = bs_line("Trade receivables", "institutional invoices outstanding", 0,
                 lambda y: f"=Cash_Flow!{ml(last_m[y])}${CF['ar']}")
    tang = bs_line("Property and equipment, net", "laptops, desks, fit-out", 0,
                   lambda y: f"=Depreciation!{ml(last_m[y])}"
                             f"${DEP['nbv_tangible']}")
    intang = bs_line("Intangible assets, net",
                     "capitalised platform, curriculum and IP", 0,
                     lambda y: f"=Depreciation!{ml(last_m[y])}"
                               f"${DEP['nbv_intangible']}")
    total_assets = bs_line("Total assets", "", f"=SUM(C{cash}:C{intang})",
                           lambda y: f"=SUM({get_column_letter(3 + y)}{cash}:"
                                     f"{get_column_letter(3 + y)}{intang})",
                           bold=True, fill_c=F.BAND)
    r += 1

    ap = bs_line("Trade and other payables", "", 0,
                 lambda y: f"=Cash_Flow!{ml(last_m[y])}${CF['ap']}")
    acc = bs_line("Accrued payroll", "", 0,
                  lambda y: f"=Cash_Flow!{ml(last_m[y])}${CF['accrued']}")
    dfr = bs_line("Deferred revenue", "billed, not yet earned", 0,
                  lambda y: f"=Cash_Flow!{ml(last_m[y])}${CF['deferred']}")
    txp = bs_line("Tax payable", "paid in arrears", 0,
                  lambda y: f"=Cash_Flow!{ml(last_m[y])}${CF['taxpay']}")
    total_liab = bs_line("Total liabilities", "", f"=SUM(C{ap}:C{txp})",
                         lambda y: f"=SUM({get_column_letter(3 + y)}{ap}:"
                                   f"{get_column_letter(3 + y)}{txp})",
                         bold=True, fill_c=F.BAND)
    r += 1

    sc = bs_line("Share capital", "founder capital plus the seed round",
                 f"={A['open_cash']}",
                 lambda y: f"={A['open_cash']}"
                           f"+IF({last_m[y]}>={A['seed_month']},{A['seed']},0)")
    re_ = bs_line("Retained earnings", "cumulative profit and loss", 0,
                  lambda y: "=" + "+".join(
                      f"Income_Statement!${get_column_letter(2 + k)}"
                      f"${IS['net']}" for k in range(1, y + 1)))
    total_eq = bs_line("Total equity", "", f"=C{sc}+C{re_}",
                       lambda y: f"={get_column_letter(3 + y)}{sc}"
                                 f"+{get_column_letter(3 + y)}{re_}",
                       bold=True, fill_c=F.BAND)
    tle = bs_line("Total liabilities and equity", "",
                  f"=C{total_liab}+C{total_eq}",
                  lambda y: f"={get_column_letter(3 + y)}{total_liab}"
                            f"+{get_column_letter(3 + y)}{total_eq}",
                  bold=True, fill_c=F.LIME)
    r += 1
    chk = bs_line("CHECK — total assets less liabilities and equity",
                  "nil in every column, or the model is wrong",
                  f"=C{total_assets}-C{tle}",
                  lambda y: f"={get_column_letter(3 + y)}{total_assets}"
                            f"-{get_column_letter(3 + y)}{tle}", bold=True)
    for col in range(3, 7):
        ws.cell(chk, col).font = f(9, True, "B00020")
    rows["check"] = chk
    rows["total_assets"] = total_assets
    R["Balance_Sheet"] = rows
    return ws


def ann_sheet(wb, name, title, subtitle, widths=(46, 32, 15, 15, 15, 15),
              last_col=8):
    ws = wb.create_sheet(name)
    sheet_title(ws, title, subtitle, last_col=last_col)
    ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(1 + i)].width = w
    return ws


def year_header(ws, r, labels=("Year 1", "Year 2", "Year 3"), start=3,
                fill_hex=None):
    for i, t in enumerate(labels):
        c = ws.cell(r, start + i, t)
        c.font = f(9, True, F.WHITE)
        c.fill = fill(fill_hex or F.UV_DARK)
        c.alignment = Alignment(horizontal="center")
    for col in (1, 2):
        ws.cell(r, col).fill = fill(fill_hex or F.UV_DARK)
    return r + 1


def kv(ws, r, label, note, formulas, fmt=MONEY, bold=False, start=3,
       fill_c=None, colour=F.INK):
    write_row(ws, r, label, note, bold=bold, fill_colour=fill_c)
    for i, fo in enumerate(formulas):
        c = ws.cell(r, start + i, fo)
        c.number_format = fmt
        c.font = f(9, bold, colour)
    return r + 1


# =====================================================================
#  15 · KPI PERFORMANCE
# =====================================================================
def build_kpis(wb):
    ws = ann_sheet(wb, "KPIs", "KPI Performance",
                   "The numbers the business is actually run on, taken from the "
                   "model rather than restated beside it.")
    rows = {}
    IS, EX, RV, CF, AQ, HR_ = (R["Income_Statement"], R["Expenses"],
                               R["Revenue"], R["Cash_Flow"], R["Acquisition"],
                               R["HR_Model"])
    last_m = {y: list(months_of(y))[-1] for y in (1, 2, 3)}
    yc = {y: get_column_letter(2 + y) for y in (1, 2, 3)}
    r = band(ws, 5, "GROWTH AND SCALE", last_col=8)
    r = year_header(ws, r)
    rev = IS["Total revenue"]
    r = kv(ws, r, "Total revenue", "",
           [f"=Income_Statement!${yc[y]}${rev}" for y in (1, 2, 3)],
           bold=True, colour=F.LINK_FONT)
    rev_r = r - 1
    r = kv(ws, r, "Revenue growth", "year on year",
           ["n/a"] + [f"=IFERROR({get_column_letter(3 + y)}{rev_r}"
                      f"/{get_column_letter(2 + y)}{rev_r}-1,0)"
                      for y in (1, 2)], PCT)
    r = kv(ws, r, "Institutional share of revenue", "engines 1 to 7",
           [f"=IFERROR(Revenue!{yl(y)}${RV['institutional']}"
            f"/Revenue!{yl(y)}${RV['total']},0)" for y in (1, 2, 3)], PCT)
    r = kv(ws, r, "Cohorts delivered", "all formats, including free pilots",
           [f"=Revenue!{yl(y)}${RV['all_cohorts']}" for y in (1, 2, 3)], NUM)
    coh = r - 1
    r = kv(ws, r, "Learners reached", "cohorts, seats, competitions, direct",
           [f"=Acquisition!{yl(y)}${AQ['signups']}" for y in (1, 2, 3)], NUM)
    learners = r - 1
    r = kv(ws, r, "Active paid subscribers", "at year end",
           [f"=Acquisition!{ml(last_m[y])}${AQ['active_paid']}"
            for y in (1, 2, 3)], NUM)
    r = kv(ws, r, "Employees", "at year end",
           [f"=HR_Model!{ml(last_m[y])}${HR_['headcount']}"
            for y in (1, 2, 3)], NUM)
    hc = r - 1
    r = kv(ws, r, "Revenue per employee", "",
           [f"=IFERROR({yc[y]}{rev_r}/{yc[y]}{hc},0)" for y in (1, 2, 3)])
    r = kv(ws, r, "Learners per employee", "the leverage the plan claims",
           [f"=IFERROR({yc[y]}{learners}/{yc[y]}{hc},0)" for y in (1, 2, 3)],
           NUM)
    r += 1

    r = band(ws, r, "PROFITABILITY", last_col=8)
    r = year_header(ws, r)
    r = kv(ws, r, "Gross profit", "",
           [f"=Income_Statement!${yc[y]}${IS['Gross profit']}"
            for y in (1, 2, 3)], colour=F.LINK_FONT)
    gp = r - 1
    r = kv(ws, r, "Gross margin", "",
           [f"=IFERROR({yc[y]}{gp}/{yc[y]}{rev_r},0)" for y in (1, 2, 3)], PCT,
           bold=True)
    r = kv(ws, r, "EBITDA", "",
           [f"=Income_Statement!${yc[y]}${IS['EBITDA']}" for y in (1, 2, 3)],
           colour=F.LINK_FONT)
    eb = r - 1
    rows["ebitda"] = eb
    r = kv(ws, r, "EBITDA margin", "",
           [f"=IFERROR({yc[y]}{eb}/{yc[y]}{rev_r},0)" for y in (1, 2, 3)], PCT,
           bold=True)
    r = kv(ws, r, "Net profit", "",
           [f"=Income_Statement!${yc[y]}${IS['net']}" for y in (1, 2, 3)],
           colour=F.LINK_FONT)
    npf = r - 1
    rows["net"] = npf
    r = kv(ws, r, "Net margin", "",
           [f"=IFERROR({yc[y]}{npf}/{yc[y]}{rev_r},0)" for y in (1, 2, 3)],
           PCT, bold=True)
    r += 1

    r = band(ws, r, "UNIT ECONOMICS", last_col=8)
    r = year_header(ws, r)
    r = kv(ws, r, "Cost per institutional contract won", "institutional CAC",
           [f"=IFERROR((Acquisition!{yl(y)}${AQ['off_cost']}"
            f"+Acquisition!{yl(y)}${AQ['on_cost']}*{A['online_inst_share']})"
            f"/Acquisition!{yl(y)}${AQ['won']},0)" for y in (1, 2, 3)])
    cac_i = r - 1
    r = kv(ws, r, "Average institutional contract value", "first-year value",
           [f"=IFERROR(Revenue!{yl(y)}${RV['institutional']}"
            f"/Acquisition!{yl(y)}${AQ['won']},0)" for y in (1, 2, 3)])
    acv = r - 1
    r = kv(ws, r, "Institutional LTV to CAC",
           "contract value x gross margin x retained years, over CAC",
           [f"=IFERROR({yc[y]}{acv}*IFERROR({yc[y]}{gp}/{yc[y]}{rev_r},0)"
            f"*2.8/{yc[y]}{cac_i},0)" for y in (1, 2, 3)], MULT, bold=True)
    r = kv(ws, r, "Cost per paid subscriber", "learner CAC",
           [f"=IFERROR(Acquisition!{yl(y)}${AQ['on_cost']}"
            f"*(1-{A['online_inst_share']})/Acquisition!{yl(y)}"
            f"${AQ['new_paid']},0)" for y in (1, 2, 3)], MONEY2)
    cac_l = r - 1
    r = kv(ws, r, "Subscriber lifetime value",
           "annual price x gross margin, over monthly churn",
           [f"=IFERROR(Revenue!{yl(y)}${RV['arpu']}/12"
            f"*IFERROR({yc[y]}{gp}/{yc[y]}{rev_r},0)/{A['sub_churn']},0)"
            for y in (1, 2, 3)], MONEY2)
    ltv = r - 1
    r = kv(ws, r, "Subscriber LTV to CAC", "",
           [f"=IFERROR({yc[y]}{ltv}/{yc[y]}{cac_l},0)" for y in (1, 2, 3)],
           MULT, bold=True)
    r = kv(ws, r, "Funnel — free account to Mission 01", "activation rate",
           [f"=IFERROR(Acquisition!{yl(y)}${AQ['activated']}"
            f"/Acquisition!{yl(y)}${AQ['signups']},0)" for y in (1, 2, 3)], PCT)
    r = kv(ws, r, "Funnel — coverage of the signing plan",
           "below 1.0x means the pipeline is short",
           [f"=IFERROR(Acquisition!{yl(y)}${AQ['won']}"
            f"/(Revenue!{yl(y)}${RV['uni_cohorts_eg']}"
            f"+Revenue!{yl(y)}${RV['uni_cohorts_ksa']}"
            f"+Revenue!{yl(y)}${RV['uni_licences']}"
            f"+Revenue!{yl(y)}${RV['school_cohorts']}"
            f"+Revenue!{yl(y)}${RV['school_licences']}"
            f"+Revenue!{yl(y)}${RV['tvet_cohorts']}"
            f"+Revenue!{yl(y)}${RV['tot_cohorts']}"
            f"+Revenue!{yl(y)}${RV['ngo_programmes']}"
            f"+Revenue!{yl(y)}${RV['competitions']}"
            f"+Revenue!{yl(y)}${RV['corporates']}),0)" for y in (1, 2, 3)],
           MULT, bold=True)
    r += 1

    r = band(ws, r, "CASH AND EFFICIENCY", last_col=8)
    r = year_header(ws, r)
    r = kv(ws, r, "Cash at year end", "",
           [f"=Cash_Flow!{ml(last_m[y])}${CF['cash']}" for y in (1, 2, 3)],
           bold=True, colour=F.LINK_FONT)
    cash = r - 1
    rows["cash"] = cash
    r = kv(ws, r, "Lowest cash balance in the year", "",
           [f"=MIN(Cash_Flow!{ml(months_of(y)[0])}${CF['cash']}:"
            f"{ml(last_m[y])}${CF['cash']})" for y in (1, 2, 3)])
    rows["min_cash"] = r - 1
    r = kv(ws, r, "Net cash from operations", "",
           [f"=Cash_Flow!{yl(y)}${CF['cfo']}" for y in (1, 2, 3)])
    cfo = r - 1
    r = kv(ws, r, "Free cash flow", "operations less capital expenditure",
           [f"=Cash_Flow!{yl(y)}${CF['cfo']}+Cash_Flow!{yl(y)}${CF['cfi']}"
            for y in (1, 2, 3)], bold=True)
    rows["fcf"] = r - 1
    r = kv(ws, r, "Average monthly burn or generation", "",
           [f"={yc[y]}{rows['fcf']}/12" for y in (1, 2, 3)])
    r = kv(ws, r, "Months of runway at year-end cash", "on the year's burn",
           [f"=IF({yc[y]}{rows['fcf']}>=0,99,"
            f"IFERROR({yc[y]}{cash}/(-{yc[y]}{rows['fcf']}/12),0))"
            for y in (1, 2, 3)], NUM1)
    r = kv(ws, r, "Debtor days achieved", "receivables over revenue",
           [f"=IFERROR(Cash_Flow!{ml(last_m[y])}${CF['ar']}"
            f"/{yc[y]}{rev_r}*365,0)" for y in (1, 2, 3)], NUM)
    rows["rev"] = rev_r
    rows["hc"] = hc
    rows["learners"] = learners
    rows["cohorts"] = coh
    R["KPIs"] = rows
    return ws


# =====================================================================
#  17 · BREAK-EVEN
# =====================================================================
def build_breakeven(wb):
    ws = ann_sheet(wb, "Break_Even", "Break-even Analysis",
                   "Where the contribution from delivery covers the cost of "
                   "existing, and the month the company stops consuming cash.")
    EX, RV, CF = R["Expenses"], R["Revenue"], R["Cash_Flow"]
    yc = {y: get_column_letter(2 + y) for y in (1, 2, 3)}
    r = band(ws, 5, "ANNUAL BREAK-EVEN", last_col=8)
    r = year_header(ws, r)
    r = kv(ws, r, "Revenue", "",
           [f"=Revenue!{yl(y)}${RV['total']}" for y in (1, 2, 3)],
           colour=F.LINK_FONT)
    rev = r - 1
    r = kv(ws, r, "Variable cost of delivery", "direct cost and revenue share",
           [f"=Expenses!{yl(y)}${EX['cogs']}" for y in (1, 2, 3)],
           colour=F.LINK_FONT)
    vc = r - 1
    r = kv(ws, r, "Contribution", "",
           [f"={yc[y]}{rev}-{yc[y]}{vc}" for y in (1, 2, 3)], bold=True)
    contrib = r - 1
    r = kv(ws, r, "Contribution margin", "",
           [f"=IFERROR({yc[y]}{contrib}/{yc[y]}{rev},0)" for y in (1, 2, 3)],
           PCT, bold=True)
    cm = r - 1
    r = kv(ws, r, "Fixed operating cost", "everything that does not move with a "
           "cohort, including depreciation",
           [f"=Expenses!{yl(y)}${EX['opex_total']}" for y in (1, 2, 3)],
           colour=F.LINK_FONT)
    fc = r - 1
    r = kv(ws, r, "Break-even revenue", "fixed cost over contribution margin",
           [f"=IFERROR({yc[y]}{fc}/{yc[y]}{cm},0)" for y in (1, 2, 3)],
           bold=True, fill_c=F.LIME)
    be = r - 1
    r = kv(ws, r, "Break-even revenue per month", "",
           [f"={yc[y]}{be}/12" for y in (1, 2, 3)])
    r = kv(ws, r, "Margin of safety", "how far revenue can fall before a loss",
           [f"=IFERROR(({yc[y]}{rev}-{yc[y]}{be})/{yc[y]}{rev},0)"
            for y in (1, 2, 3)], PCT, bold=True)
    r = kv(ws, r, "Break-even in university-cohort equivalents",
           "at that year's cohort price and margin",
           [f"=IFERROR({yc[y]}{be}/{A['p_uni'][y - 1]},0)"
            for y in (1, 2, 3)], NUM)
    r += 1

    r = band(ws, r, "THE MONTH IT TURNS", last_col=8)
    hdr = r
    for i, t in enumerate(["Month number", "Which month"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(9, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center")
    r += 1

    # Helper rows: the first month a series turns positive, written without an
    # array formula — 9,999 stands for "not within the thirty-six months
    # modelled", so MIN over the row returns the first month that qualifies.
    lbl_row = r
    for m in range(1, F.MONTHS + 1):
        ws.cell(lbl_row, mcol(m), F.MONTH_LABELS[m - 1]).number_format = TEXT
    ws.cell(lbl_row, 1, "Month labels — lookup row").font = f(8, False, "6B7285")
    ws.row_dimensions[lbl_row].hidden = True
    r += 1

    helpers = []
    specs = (("First month with positive EBITDA", "Expenses", EX["ebitda"],
              "the month delivery covers the cost of existing", "pos"),
             ("First month with positive operating cash flow", "Cash_Flow",
              CF["cfo"], "profit converted into cash", "pos"),
             ("First month cash stops falling", "Cash_Flow", CF["cash"],
              "the trough of the cash curve", "turn"))
    for label, sheet, srow, note, mode in specs:
        hr_ = r
        monthly_row(ws, hr_, label + " — working",
                    lambda m, s=sheet, sr=srow, md=mode:
                    (f"=IF({mref(s, sr, m)}>0,{m},9999)" if md == "pos" else
                     f"=IF({m}=1,9999,IF({mref(s, sr, m)}>{mref(s, sr, m - 1)},"
                     f"{m},9999))"),
                    note, NUM, years=False)
        ws.row_dimensions[hr_].hidden = True
        helpers.append((label, hr_, note))
        r += 1

    for label, hr_, note in helpers:
        write_row(ws, r, label, note, bold=True)
        c = ws.cell(r, 3, f"=MIN({ml(1)}{hr_}:{ml(F.MONTHS)}{hr_})")
        c.number_format = NUM
        c.font = f(9, True)
        c2 = ws.cell(r, 4, f'=IF(C{r}=9999,"not within 36 months",'
                           f'INDEX(${ml(1)}${lbl_row}:${ml(F.MONTHS)}'
                           f'${lbl_row},1,C{r}))')
        c2.font = f(9, True, F.UV)
        r += 1
    ws.column_dimensions["D"].width = 22
    return ws


# =====================================================================
#  14 · STRESS TESTING
# =====================================================================
def build_stress(wb):
    ws = ann_sheet(wb, "Stress_Test", "Stress Testing",
                   "Four scenarios applied to the base case. Delivery volume "
                   "and price flex; operating cost barely does, which is what "
                   "makes a volume shortfall expensive.",
                   widths=(34, 20, 13, 13, 13, 13, 13, 13), last_col=10)
    IS, EX, RV, CF = (R["Income_Statement"], R["Expenses"], R["Revenue"],
                      R["Cash_Flow"])
    yc = {y: get_column_letter(2 + y) for y in (1, 2, 3)}

    r = band(ws, 5, "SCENARIO LEVERS", last_col=10)
    hdr = r
    for i, t in enumerate(["Volume", "Price", "Operating cost",
                           "Collection days", "Conversion"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr, 1, "Scenario").font = f(9, True, F.WHITE)
    for col in (1, 2):
        ws.cell(hdr, col).fill = fill(F.UV_DARK)
    r += 1
    scen = [
        ("Base case", "the plan as modelled", 1.00, 1.00, 1.00, 1.00, 1.00),
        ("Upside", "institutional demand lands early", 1.20, 1.03, 1.06, 0.92,
         1.10),
        ("Downside", "a slow first year in Egypt", 0.75, 0.95, 1.00, 1.20, 0.85),
        ("Severe", "public budgets freeze and a market slips", 0.55, 0.88, 0.97,
         1.45, 0.70),
    ]
    first_s = r
    for name, note, vol, pr, op, dso, conv in scen:
        write_row(ws, r, name, note, bold=(name == "Base case"))
        for i, v in enumerate((vol, pr, op, dso, conv)):
            input_cell(ws, r, 3 + i, v, MULT if i != 2 else MULT)
        r += 1
    last_s = r - 1
    rowof = {name: first_s + i for i, (name, *_ ) in enumerate(scen)}
    r += 1

    def block(title, metric_rows):
        nonlocal r
        r = band(ws, r, title, last_col=10)
        hdr2 = r
        for i, t in enumerate(["Year 1", "Year 2", "Year 3"]):
            c = ws.cell(hdr2, 3 + i, t)
            c.font = f(9, True, F.WHITE)
            c.fill = fill(F.UV_DARK)
            c.alignment = Alignment(horizontal="center")
        ws.cell(hdr2, 1, "Scenario").font = f(9, True, F.WHITE)
        for col in (1, 2):
            ws.cell(hdr2, col).fill = fill(F.UV_DARK)
        r += 1
        out = {}
        for name, *_ in scen:
            sr = rowof[name]
            write_row(ws, r, name, "", bold=(name == "Base case"))
            for y in (1, 2, 3):
                ws.cell(r, 2 + y, metric_rows(sr, y)).number_format = MONEY
                ws.cell(r, 2 + y).font = f(9, name == "Base case")
            out[name] = r
            r += 1
        r += 1
        return out

    rev_rows = block(
        "REVENUE UNDER STRESS",
        lambda sr, y: f"=Revenue!{yl(y)}${RV['institutional']}*$C${sr}*$D${sr}"
                      f"+Revenue!{yl(y)}${RV['sub_revenue']}*$G${sr}*$D${sr}")
    ebitda_rows = block(
        "EBITDA UNDER STRESS",
        lambda sr, y:
        f"=(Revenue!{yl(y)}${RV['institutional']}*$C${sr}*$D${sr}"
        f"+Revenue!{yl(y)}${RV['sub_revenue']}*$G${sr}*$D${sr})"
        f"-Expenses!{yl(y)}${EX['cogs']}*$C${sr}"
        f"-Expenses!{yl(y)}${EX['opex_cash']}*$E${sr}")

    r = band(ws, r, "CASH AT YEAR END, AND WHAT IT WOULD TAKE TO SURVIVE",
             last_col=10)
    hdr3 = r
    for i, t in enumerate(["Year 1", "Year 2", "Year 3", "Lowest cash",
                           "Further funding needed"]):
        c = ws.cell(hdr3, 3 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr3, 1, "Scenario").font = f(9, True, F.WHITE)
    for col in (1, 2):
        ws.cell(hdr3, col).fill = fill(F.UV_DARK)
    r += 1
    cash_rows = {}
    for name, *_ in scen:
        sr = rowof[name]
        er = ebitda_rows[name]
        write_row(ws, r, name, "", bold=(name == "Base case"))
        for y in (1, 2, 3):
            col = get_column_letter(2 + y)
            prev = (f"{A['open_cash']}+{A['seed']}" if y == 1
                    else f"{get_column_letter(1 + y)}{r}")
            # Cash is the base-case cash walk with the scenario's EBITDA
            # substituted, plus the extra receivables a slower collection
            # cycle locks up.
            ws.cell(r, 2 + y,
                    f"={prev}+{col}{er}-Capex!{yl(y)}${R['Capex']['capex']}"
                    f"-(Cash_Flow!{ml(list(months_of(y))[-1])}"
                    f"${R['Cash_Flow']['ar']})*($F${sr}-1)"
                    f"+Cash_Flow!{yl(y)}${R['Cash_Flow']['d_' + str(R['Cash_Flow']['ap'])]}"
                    f"+Cash_Flow!{yl(y)}${R['Cash_Flow']['d_' + str(R['Cash_Flow']['deferred'])]}"
                    ).number_format = MONEY
            ws.cell(r, 2 + y).font = f(9, name == "Base case")
        ws.cell(r, 6, f"=MIN(C{r}:E{r})").number_format = MONEY
        ws.cell(r, 6).font = f(9, True)
        ws.cell(r, 7, f"=MAX(0,{A['min_cash']}-F{r})").number_format = MONEY
        ws.cell(r, 7).font = f(9, True, "B00020")
        cash_rows[name] = r
        r += 1
    r += 1
    note = ws.cell(r, 1,
                   "The cash rows above re-run the base-case cash walk with the "
                   "scenario's EBITDA and collection cycle substituted. They are "
                   "an overlay on the model, not a second model: capital "
                   "expenditure, payables and deferred revenue are held at the "
                   "base case, which makes the downside figures slightly "
                   "flattering and is the honest direction for an error to run.")
    note.font = f(8, False, "6B7285", italic=True)
    ws.merge_cells(start_row=r, start_column=1, end_row=r + 1, end_column=10)
    ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical="top")
    R["Stress_Test"] = {"cash": cash_rows, "ebitda": ebitda_rows,
                        "rev": rev_rows}
    return ws


# =====================================================================
#  16 · SENSITIVITY
# =====================================================================
def build_sensitivity(wb):
    ws = ann_sheet(wb, "Sensitivity", "Sensitivity Analysis",
                   "Two-way grids on the year-three result. Each cell is a live "
                   "formula, so a changed assumption moves the whole grid.",
                   widths=(34, 14, 13, 13, 13, 13, 13), last_col=9)
    IS, EX, RV = R["Income_Statement"], R["Expenses"], R["Revenue"]
    inst3 = f"Revenue!{yl(3)}${RV['institutional']}"
    sub3 = f"Revenue!{yl(3)}${RV['sub_revenue']}"
    cogs3 = f"Expenses!{yl(3)}${EX['cogs']}"
    opex3 = f"Expenses!{yl(3)}${EX['opex_cash']}"

    def grid(title, note, rowvals, colvals, rowlab, collab, cell_fn,
             fmt=MONEY):
        nonlocal r
        r = band(ws, r, title, last_col=9)
        c = ws.cell(r, 1, note)
        c.font = f(8, False, "6B7285", italic=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
        r += 1
        ws.cell(r, 2, collab).font = f(8, True, F.UV)
        for j, cv in enumerate(colvals):
            cell = ws.cell(r, 3 + j, cv)
            cell.number_format = PCT
            cell.font = f(8.5, True, F.WHITE)
            cell.fill = fill(F.UV_DARK)
            cell.alignment = Alignment(horizontal="center")
        colrow = r
        r += 1
        first = r
        for rv in rowvals:
            cell = ws.cell(r, 2, rv)
            cell.number_format = PCT
            cell.font = f(8.5, True, F.INK)
            cell.fill = fill(F.LIME)
            ws.cell(r, 1, rowlab if r == first else "").font = f(8, True, F.UV)
            for j, cv in enumerate(colvals):
                cc = ws.cell(r, 3 + j,
                             cell_fn(f"$B${r}",
                                     f"{get_column_letter(3 + j)}${colrow}"))
                cc.number_format = fmt
                cc.font = f(8.5)
            r += 1
        r += 1

    r = 5
    steps = [-0.30, -0.15, 0.0, 0.15, 0.30]
    grid("YEAR-THREE EBITDA · VOLUME AGAINST PRICE",
         "Rows flex delivery volume; columns flex price. Direct cost moves with "
         "volume, operating cost does not.",
         steps, [-0.15, -0.075, 0.0, 0.075, 0.15],
         "Volume change", "Price change",
         lambda rv, cv: f"=({inst3}+{sub3})*(1+{rv})*(1+{cv})"
                        f"-{cogs3}*(1+{rv})-{opex3}")

    grid("YEAR-THREE EBITDA · VOLUME AGAINST OPERATING COST",
         "Rows flex delivery volume; columns flex the fixed operating base — "
         "the cost of holding the establishment and the network.",
         steps, [-0.20, -0.10, 0.0, 0.10, 0.20],
         "Volume change", "Operating cost change",
         lambda rv, cv: f"=({inst3}+{sub3})*(1+{rv})-{cogs3}*(1+{rv})"
                        f"-{opex3}*(1+{cv})")

    grid("YEAR-THREE GROSS MARGIN · PARTNER SHARE AGAINST FACILITATOR RATE",
         "Rows flex the share of cohorts delivered by certified partners; "
         "columns flex the facilitator day rate. The two levers that decide "
         "whether the delivery model pays for itself.",
         [-0.5, -0.25, 0.0, 0.25, 0.5], [-0.20, -0.10, 0.0, 0.10, 0.20],
         "Partner-delivered share", "Facilitator day rate",
         lambda rv, cv:
         f"=IFERROR((({inst3}+{sub3})"
         f"-({cogs3}-Expenses!{yl(3)}${EX['rs1']}"
         f"-(Revenue!{yl(3)}${RV['uni_cohorts_eg']}"
         f"+Revenue!{yl(3)}${RV['uni_cohorts_ksa']})"
         f"*{A['fac_rate']}*{A['fac_per']}*{A['d_uni']})"
         f"-Expenses!{yl(3)}${EX['rs1']}*(1+{rv})"
         f"-(Revenue!{yl(3)}${RV['uni_cohorts_eg']}"
         f"+Revenue!{yl(3)}${RV['uni_cohorts_ksa']})"
         f"*{A['fac_rate']}*(1+{cv})*{A['fac_per']}*{A['d_uni']})"
         f"/({inst3}+{sub3}),0)", PCT)
    return ws


# =====================================================================
#  18 · PAYBACK
# =====================================================================
def build_payback(wb):
    ws = ann_sheet(wb, "Payback", "Payback and Funding Scenarios",
                   "When the money put in comes back, under the base case and "
                   "under stress.", widths=(44, 26, 15, 15, 15, 15), last_col=8)
    CF, KP, ST = R["Cash_Flow"], R["KPIs"], R["Stress_Test"]
    yc = {y: get_column_letter(2 + y) for y in (1, 2, 3)}
    r = band(ws, 5, "CAPITAL IN", last_col=8)
    r = kv(ws, r, "Founder capital at inception", "already contributed",
           [f"={A['open_cash']}"], bold=True)
    r = kv(ws, r, "Seed round", "the business plan's funding requirement",
           [f"={A['seed']}"], bold=True)
    r = kv(ws, r, "Total capital invested", "",
           [f"={A['open_cash']}+{A['seed']}"], bold=True, fill_c=F.LIME)
    invested = r - 1
    r += 1

    r = band(ws, r, "CASH RETURNED — BASE CASE", last_col=8)
    r = year_header(ws, r)
    r = kv(ws, r, "Free cash flow in the year", "operations less capex",
           [f"=KPIs!${yc[y]}${KP['fcf']}" for y in (1, 2, 3)],
           colour=F.LINK_FONT)
    fcf = r - 1
    cum = r
    r = kv(ws, r, "Cumulative free cash flow", "", ["", "", ""], bold=True)
    for y, formula in ((1, f"=C{fcf}"), (2, f"=C{cum}+D{fcf}"),
                       (3, f"=D{cum}+E{fcf}")):
        c = ws.cell(cum, 2 + y, formula)
        c.number_format = MONEY
        c.font = f(9, True)
    r = kv(ws, r, "Capital recovered", "cumulative free cash flow over capital in",
           [f"=IFERROR({yc[y]}{cum}/$C${invested},0)" for y in (1, 2, 3)],
           PCT, bold=True)
    recov = r - 1
    r = kv(ws, r, "Capital still outstanding", "",
           [f"=MAX(0,$C${invested}-{yc[y]}{cum})" for y in (1, 2, 3)])
    r += 1

    r = band(ws, r, "PAYBACK PERIOD", last_col=8)
    lbl_row = r
    for m in range(1, F.MONTHS + 1):
        ws.cell(lbl_row, mcol(m), F.MONTH_LABELS[m - 1]).number_format = TEXT
    ws.row_dimensions[lbl_row].hidden = True
    r += 1
    cumrow = r
    monthly_row(ws, cumrow, "Cumulative free cash flow — working",
                lambda m: (f"={mref('Cash_Flow', CF['cfo'], m)}"
                           f"+{mref('Cash_Flow', CF['cfi'], m)}" if m == 1 else
                           f"={ml(m - 1)}{cumrow}"
                           f"+{mref('Cash_Flow', CF['cfo'], m)}"
                           f"+{mref('Cash_Flow', CF['cfi'], m)}"),
                "", MONEY, years=False)
    ws.row_dimensions[cumrow].hidden = True
    r += 1
    flagrow = r
    monthly_row(ws, flagrow, "Payback flag — working", lambda m:
                f"=IF({ml(m)}{cumrow}>=$C${invested},{m},9999)", "", NUM,
                years=False)
    ws.row_dimensions[flagrow].hidden = True
    r += 1
    write_row(ws, r, "Months to repay all capital invested",
              "cumulative free cash flow covers the money in", bold=True)
    ws.cell(r, 3, f"=MIN({ml(1)}{flagrow}:{ml(F.MONTHS)}{flagrow})"
            ).number_format = NUM
    ws.cell(r, 3).font = f(9, True)
    ws.cell(r, 4, f'=IF(C{r}=9999,"beyond the 36 months modelled",'
                  f'INDEX(${ml(1)}${lbl_row}:${ml(F.MONTHS)}${lbl_row},1,C{r}))'
            ).font = f(9, True, F.UV)
    ws.column_dimensions["D"].width = 26
    r += 2

    r = band(ws, r, "PAYBACK UNDER STRESS", last_col=8)
    r = year_header(ws, r, labels=("Year 1", "Year 2", "Year 3",
                                   "Capital recovered by Y3"))
    for name in ("Base case", "Upside", "Downside", "Severe"):
        sr = ST["ebitda"][name]
        write_row(ws, r, name, "EBITDA less capital expenditure",
                  bold=(name == "Base case"))
        for y in (1, 2, 3):
            ws.cell(r, 2 + y,
                    f"=Stress_Test!{get_column_letter(2 + y)}${sr}"
                    f"-Capex!{yl(y)}${R['Capex']['capex']}"
                    ).number_format = MONEY
            ws.cell(r, 2 + y).font = f(9, name == "Base case")
        ws.cell(r, 6, f"=IFERROR(SUM(C{r}:E{r})/$C${invested},0)"
                ).number_format = PCT
        ws.cell(r, 6).font = f(9, True)
        r += 1
    return ws


# =====================================================================
#  19 · EXIT STRATEGY
# =====================================================================
def build_exit(wb):
    ws = ann_sheet(wb, "Exit_Strategy", "Investor Return and Exit",
                   "What an angel and a venture investor each put in, what they "
                   "hold after dilution, and what the holding is worth on three "
                   "exit assumptions.",
                   widths=(44, 26, 15, 15, 15, 15), last_col=8)
    KP, IS = R["KPIs"], R["Income_Statement"]
    yc = {y: get_column_letter(2 + y) for y in (1, 2, 3)}

    r = band(ws, 5, "THE ROUND", last_col=8)
    hdr = r
    for i, t in enumerate(["Angel round", "Venture round"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(9, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center")
    for col in (1, 2):
        ws.cell(hdr, col).fill = fill(F.UV_DARK)
    r += 1

    def pair(label, note, a_val, b_val, fmt=MONEY, bold=False, inputs=False,
             fill_c=None):
        nonlocal r
        write_row(ws, r, label, note, bold=bold, fill_colour=fill_c)
        for i, v in enumerate((a_val, b_val)):
            if inputs:
                input_cell(ws, r, 3 + i, v, fmt)
            else:
                c = ws.cell(r, 3 + i, v)
                c.number_format = fmt
                c.font = f(9, bold)
        r += 1
        return r - 1

    amount = pair("Amount invested", "the seed requirement, split two ways",
                  175000, 350000, MONEY, inputs=True)
    pre = pair("Pre-money valuation", "a MENA pre-revenue to early-revenue range",
               1400000, 2600000, MONEY, inputs=True)
    post = pair("Post-money valuation", "",
                f"=C{pre}+C{amount}", f"=D{pre}+D{amount}", MONEY, bold=True)
    own = pair("Ownership at entry", "",
               f"=IFERROR(C{amount}/C{post},0)",
               f"=IFERROR(D{amount}/D{post},0)", PCT, bold=True)
    dil = pair("Dilution from later rounds", "two further rounds assumed",
               0.38, 0.30, PCT, inputs=True)
    final = pair("Ownership at exit", "",
                 f"=C{own}*(1-C{dil})", f"=D{own}*(1-D{dil})", PCT, bold=True,
                 fill_c=F.LIME)
    r += 1

    r = band(ws, r, "WHAT THE COMPANY IS WORTH AT EXIT", last_col=8)
    note = ws.cell(r, 1, "Three bases, because no single multiple is "
                         "defensible on its own. Education-technology businesses "
                         "selling to institutions trade on revenue while they "
                         "are growing and on earnings once they are not.")
    note.font = f(8, False, "6B7285", italic=True)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    r += 1
    hdr2 = r
    for i, t in enumerate(["Multiple", "Exit value", "Angel proceeds",
                           "Venture proceeds"]):
        c = ws.cell(hdr2, 3 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr2, 1, "Basis").font = f(9, True, F.WHITE)
    for col in (1, 2):
        ws.cell(hdr2, col).fill = fill(F.UV_DARK)
    r += 1
    rev3 = f"KPIs!${yc[3]}${KP['rev']}"
    ebitda3 = f"KPIs!${yc[3]}${KP['ebitda']}"
    bases = [
        ("Year-three revenue multiple — conservative", "a slower-growth trade sale",
         2.5, rev3),
        ("Year-three revenue multiple — central", "the base case for a strategic "
         "buyer", 4.0, rev3),
        ("Year-three revenue multiple — strong", "a competitive process", 6.0,
         rev3),
        ("Year-three EBITDA multiple", "a cash-generative buyer's view", 12.0,
         ebitda3),
    ]
    base_rows = []
    for label, note_t, mult, base in bases:
        write_row(ws, r, label, note_t)
        input_cell(ws, r, 3, mult, MULT)
        c = ws.cell(r, 4, f"=C{r}*{base}")
        c.number_format = MONEY
        c.font = f(9, True)
        for i, orow in enumerate((final, final)):
            cc = ws.cell(r, 5 + i,
                         f"=$D${r}*{get_column_letter(3 + i)}${final}")
            cc.number_format = MONEY
            cc.font = f(9)
        base_rows.append(r)
        r += 1
    r += 1

    r = band(ws, r, "RETURN TO THE INVESTOR — CENTRAL CASE", last_col=8)
    central = base_rows[1]
    r = kv(ws, r, "Years held from entry to exit",
           "entry at the seed round, exit after year three", [3.5, 3.0], NUM1,
           bold=False)
    years = r - 1
    for i in (0, 1):
        input_cell(ws, years, 3 + i, (3.5, 3.0)[i], NUM1)
    r = kv(ws, r, "Proceeds at exit", "on the central revenue multiple",
           [f"=E{central}", f"=F{central}"], bold=True)
    proceeds = r - 1
    r = kv(ws, r, "Multiple of money returned", "",
           [f"=IFERROR(C{proceeds}/C{amount},0)",
            f"=IFERROR(D{proceeds}/D{amount},0)"], MULT, bold=True,
           fill_c=F.LIME)
    moic = r - 1
    r = kv(ws, r, "Annualised return",
           "the internal rate of return on a single investment and a single exit",
           [f"=IFERROR(C{moic}^(1/C{years})-1,0)",
            f"=IFERROR(D{moic}^(1/D{years})-1,0)"], PCT, bold=True,
           fill_c=F.LIME)
    r += 1

    r = band(ws, r, "THE ROUTES OUT", last_col=8)
    routes = [
        ("Strategic acquisition by an education group",
         "A regional training or education group buying the institutional "
         "relationships and the certified network. The most likely route, and "
         "the one the business is shaped for: a buyer acquires delivery "
         "capacity in two markets without building it."),
        ("Acquisition by a platform or edtech consolidator",
         "A buyer acquiring the curriculum, the assessment record and the "
         "Arabic product. Values the platform and the data rather than the "
         "relationships."),
        ("Secondary sale at the Series A or B",
         "Early investors sell part of the holding to an incoming fund. "
         "Partial liquidity at three to four years without an exit."),
        ("Acquisition by a government-backed vehicle",
         "A sovereign or development-backed fund buying national delivery "
         "capacity. Slower, lower multiple, highest certainty once the "
         "initiative engine is contracted."),
        ("Continue and distribute",
         "A profitable company of this size can pay dividends rather than "
         "sell. The weakest return for an investor and the one a founder "
         "should name openly rather than leave implied."),
    ]
    for label, text in routes:
        write_row(ws, r, label, "", bold=True)
        c = ws.cell(r, 3, text)
        c.font = f(8.5, False, F.INK2 if hasattr(F, "INK2") else "3A4050")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=8)
        ws.row_dimensions[r].height = 30
        r += 1
    return ws


# =====================================================================
#  02 · DASHBOARD
# =====================================================================
def build_dashboard(wb):
    ws = wb.create_sheet("Dashboard")
    sheet_title(ws, "Dashboard",
                "The whole model on one page. Every figure is a link; nothing "
                "here is typed.", last_col=12)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 26
    for col in "CDEFGH":
        ws.column_dimensions[col].width = 15
    KP, IS, CF, BS = (R["KPIs"], R["Income_Statement"], R["Cash_Flow"],
                      R["Balance_Sheet"])
    yc = {y: get_column_letter(2 + y) for y in (1, 2, 3)}

    r = band(ws, 5, "HEADLINES", last_col=12)
    r = year_header(ws, r)
    tiles = [
        ("Total revenue", f"=Income_Statement!${{c}}${IS['Total revenue']}",
         MONEY, True),
        ("Gross profit", f"=Income_Statement!${{c}}${IS['Gross profit']}",
         MONEY, False),
        ("EBITDA", f"=Income_Statement!${{c}}${IS['EBITDA']}", MONEY, True),
        ("Net profit", f"=Income_Statement!${{c}}${IS['net']}", MONEY, True),
        ("Cash at year end", f"=KPIs!${{c}}${KP['cash']}", MONEY, True),
        ("Lowest cash in the year", f"=KPIs!${{c}}${KP['min_cash']}", MONEY,
         False),
        ("Employees at year end", f"=KPIs!${{c}}${KP['hc']}", NUM, False),
        ("Learners reached", f"=KPIs!${{c}}${KP['learners']}", NUM, False),
    ]
    for label, tmpl, fmt, bold in tiles:
        r = kv(ws, r, label, "", [tmpl.format(c=yc[y]) for y in (1, 2, 3)],
               fmt, bold=bold, colour=F.LINK_FONT if not bold else F.INK)
    r += 1

    r = band(ws, r, "BALANCE SHEET AND CHECK", last_col=12)
    r = year_header(ws, r, labels=("At inception", "Year 1", "Year 2", "Year 3"))
    for label, srow in (("Total assets", BS["total_assets"]),
                        ("CHECK — must be nil", BS["check"])):
        write_row(ws, r, label, "", bold=True)
        for i in range(4):
            c = ws.cell(r, 3 + i,
                        f"=Balance_Sheet!${get_column_letter(3 + i)}${srow}")
            c.number_format = MONEY
            c.font = f(9, True, "B00020" if "CHECK" in label else F.LINK_FONT)
        r += 1
    r += 1

    chart_anchor = r
    r += 20
    r = band(ws, r, "HOW TO USE THIS WORKBOOK", last_col=12)
    for text in (
        "Blue figures on a yellow fill are inputs. Change those and the whole "
        "model moves. Everything else is a formula.",
        "The Assumptions sheet holds every typed number in the model. Nothing "
        "is typed on any process or output sheet.",
        "Volume comes from the twelve-quarter plan in the business plan, split "
        "into months by the phasing weights on the Assumptions sheet.",
        "The check line on the balance sheet must read nil in every column. If "
        "it does not, something upstream has been broken.",
    ):
        c = ws.cell(r, 1, "·  " + text)
        c.font = f(8.5, False, "3A4050")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=12)
        r += 1

    # ------------------------------------------------------------ charts
    rev_row = R["Revenue"]["total"]
    cost_row = R["Expenses"]["opex_total"]
    cash_row = R["Cash_Flow"]["cash"]

    ch = LineChart()
    ch.title = "Monthly revenue against total cost"
    ch.height, ch.width = 7.5, 18
    ch.style = 2
    for row, name in ((rev_row, "Revenue"), (cost_row, "Operating cost")):
        data = Reference(wb["Revenue"] if row == rev_row else wb["Expenses"],
                         min_col=mcol(1), max_col=mcol(F.MONTHS),
                         min_row=row, max_row=row)
        ch.add_data(data, titles_from_data=False, from_rows=True)
    ch.y_axis.numFmt = '$#,##0'
    ws.add_chart(ch, f"A{chart_anchor}")

    ch2 = LineChart()
    ch2.title = "Cash balance, month by month"
    ch2.height, ch2.width = 7.5, 18
    ch2.style = 12
    data = Reference(wb["Cash_Flow"], min_col=mcol(1), max_col=mcol(F.MONTHS),
                     min_row=cash_row, max_row=cash_row)
    ch2.add_data(data, titles_from_data=False, from_rows=True)
    ch2.y_axis.numFmt = '$#,##0'
    ws.add_chart(ch2, f"G{chart_anchor}")
    return ws


# =====================================================================
#  01 · COVER
# =====================================================================
def build_cover(wb, order):
    ws = wb.create_sheet("Cover")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 72
    ws.column_dimensions["D"].width = 20

    ws.merge_cells("B3:D3")
    c = ws.cell(3, 2, "StartPad")
    c.font = Font(name=F.FONT, size=30, bold=True, color=F.UV)
    ws.row_dimensions[3].height = 42
    ws.merge_cells("B4:D4")
    c = ws.cell(4, 2, "Operational Financial Model")
    c.font = Font(name=F.FONT, size=19, bold=False, color=F.INK)
    ws.row_dimensions[4].height = 28
    ws.merge_cells("B5:D5")
    c = ws.cell(5, 2, "Thirty-six months · October 2026 to September 2029 · "
                      "Egypt and Saudi Arabia · USD")
    c.font = Font(name=F.FONT, size=10, color="6B7285")
    for col in range(2, 5):
        ws.cell(7, col).border = Border(bottom=F.MED)
    r = 8

    ws.cell(r, 2, "WHAT THIS IS").font = f(9, True, F.UV)
    r += 1
    for text in (
        "A monthly operating model for three years, built directly on the "
        "volumes and the establishment in the StartPad business plan and on "
        "the channel structure in the go-to-market strategy.",
        "Every figure in the workbook is a formula. The only typed numbers are "
        "the inputs on the Assumptions, HR Model and Actuals sheets, which are "
        "shown in blue on a yellow fill.",
        "Change an input and the acquisition funnel, the revenue streams, the "
        "expense base, the three statements and every analysis sheet move with "
        "it.",
    ):
        cell = ws.cell(r, 2, text)
        cell.font = f(9, False, "3A4050")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1

    ws.cell(r, 2, "CONVENTIONS").font = f(9, True, F.UV)
    r += 1
    legend = [("Blue figure on a yellow fill", "A typed input. Change these."),
              ("Black figure", "A formula on this sheet."),
              ("Green figure", "A link to another sheet."),
              ("Red figure", "A check that must read nil."),
              ("Lime band", "A headline result.")]
    for k, v in legend:
        cell = ws.cell(r, 2, k)
        cell.font = f(9, True)
        if k.startswith("Blue"):
            cell.font = f(9, True, F.IN_FONT)
            cell.fill = fill(F.YELLOW)
        elif k.startswith("Green"):
            cell.font = f(9, True, F.LINK_FONT)
        elif k.startswith("Red"):
            cell.font = f(9, True, "B00020")
        elif k.startswith("Lime"):
            cell.fill = fill(F.LIME)
        ws.cell(r, 3, v).font = f(9, False, "3A4050")
        r += 1
    r += 1

    ws.cell(r, 2, "CONTENTS").font = f(9, True, F.UV)
    r += 1
    blurbs = {
        "Cover": "This page — what the model is and how to read it",
        "Dashboard": "The whole model on one page, with charts",
        "Assumptions": "INPUT · every typed number: volumes, prices, "
                       "acquisition, cost, revenue share, working capital",
        "HR_Model": "INPUT · eighteen roles, salaries and start months, "
                    "monthly and annual",
        "Actuals": "INPUT · the opening position and a grid to record each "
                   "month as it closes",
        "Capex": "INPUT · assets driven by new hires, plus shared and "
                 "intangible assets",
        "Acquisition": "PROCESS · offline and online channels, both funnels, "
                       "36 months",
        "Revenue": "PROCESS · thirteen revenue lines across eight engines, "
                   "36 months",
        "Expenses": "PROCESS · direct cost, revenue share to three parties, "
                    "operating cost, 36 months",
        "Depreciation": "PROCESS · straight-line depreciation and amortisation "
                        "by asset class",
        "Income_Statement": "OUTPUT · three years to 30 September",
        "Balance_Sheet": "OUTPUT · three years, with the balance check",
        "Cash_Flow": "OUTPUT · monthly working and the annual statement",
        "Stress_Test": "ANALYSIS · four scenarios on volume, price, cost and "
                       "collection",
        "KPIs": "ANALYSIS · growth, profitability, unit economics, cash",
        "Sensitivity": "ANALYSIS · three two-way grids on the year-three result",
        "Break_Even": "ANALYSIS · break-even revenue and the month it turns",
        "Payback": "ANALYSIS · when the capital comes back, base and stressed",
        "Exit_Strategy": "ANALYSIS · angel and venture returns, and the routes "
                         "out",
    }
    for i, name in enumerate(order):
        cell = ws.cell(r, 2, f"{i + 1:02d}   {name.replace('_', ' ')}")
        cell.font = f(9, True, F.UV)
        b = ws.cell(r, 3, blurbs.get(name, ""))
        b.font = f(8.5, False, "3A4050")
        if i % 2 == 0:
            for col in (2, 3, 4):
                ws.cell(r, col).fill = fill(F.WASH)
        r += 1
    r += 1
    cell = ws.cell(r, 2, "Built from business_plan/model.py. Rebuild with: "
                         "python scripts/build_financial_model_xlsx.py")
    cell.font = f(8, False, "9AA0AF", italic=True)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
    return ws


# =====================================================================
#  05 · ACTUALS AND OPENING POSITION
# =====================================================================
def build_actuals(wb):
    ws = wb.create_sheet("Actuals")
    setup_monthly(ws, "Actuals and Opening Position",
                  "The money already in, the opening balance sheet it creates, "
                  "and a grid to record each month as it closes so this becomes "
                  "an operating tool rather than a one-off forecast.",
                  freeze="C7")
    rows = {}
    RV, EX, CF = R["Revenue"], R["Expenses"], R["Cash_Flow"]

    r = band(ws, 5, "OPENING POSITION AT 30 SEPTEMBER 2026")
    for label, note, val in (
            ("Cash at bank", "founder capital already contributed",
             f"={A['open_cash']}"),
            ("Trade receivables", "nothing invoiced yet", 0),
            ("Property and equipment, net", "nothing acquired yet", 0),
            ("Intangible assets, net", "capitalised from month 1", 0)):
        write_row(ws, r, label, note)
        c = ws.cell(r, 3, val)
        c.number_format = MONEY
        c.font = f(9, False, F.LINK_FONT if isinstance(val, str) else F.INK)
        rows[label] = r
        r += 1
    write_row(ws, r, "Total opening assets", "", bold=True, fill_colour=F.BAND)
    c = ws.cell(r, 3, f"=SUM(C{rows['Cash at bank']}:C{r - 1})")
    c.number_format = MONEY
    c.font = f(9, True)
    rows["assets"] = r
    r += 2

    for label, note, val in (
            ("Trade and other payables", "none at inception", 0),
            ("Paid-in share capital", "the opening cash, recorded as equity",
             f"={A['open_cash']}"),
            ("Retained earnings", "no trading before month 1", 0)):
        write_row(ws, r, label, note)
        c = ws.cell(r, 3, val)
        c.number_format = MONEY
        c.font = f(9, False, F.LINK_FONT if isinstance(val, str) else F.INK)
        rows[label] = r
        r += 1
    write_row(ws, r, "Total opening liabilities and equity", "", bold=True,
              fill_colour=F.BAND)
    c = ws.cell(r, 3, f"=C{rows['Trade and other payables']}"
                      f"+C{rows['Paid-in share capital']}"
                      f"+C{rows['Retained earnings']}")
    c.number_format = MONEY
    c.font = f(9, True)
    rows["liab_eq"] = r
    r += 1
    write_row(ws, r, "CHECK — assets less liabilities and equity",
              "must read nil", bold=True)
    c = ws.cell(r, 3, f"=C{rows['assets']}-C{rows['liab_eq']}")
    c.number_format = MONEY
    c.font = f(9, True, "B00020")
    r += 2

    r = band(ws, r, "MONTHLY ACTUALS — ENTER AS EACH MONTH CLOSES")
    c = ws.cell(r, 1,
                "Leave a month blank until it has closed. Nothing downstream "
                "reads this grid: the statements run on the forecast, and these "
                "rows exist so the variance can be read without disturbing the "
                "model.")
    c.font = f(8, False, "6B7285", italic=True)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=22)
    r += 1
    r = month_header(ws, r)
    entry = {}
    for label in ("Revenue — actual", "Direct cost — actual",
                  "Operating cost — actual", "Closing cash — actual"):
        write_row(ws, r, label, "enter when the month closes")
        for m in range(1, F.MONTHS + 1):
            cell = ws.cell(r, mcol(m))
            cell.number_format = MONEY
            cell.font = f(8.5, False, F.IN_FONT)
            cell.fill = fill(F.YELLOW)
        for y in (1, 2, 3):
            cell = ws.cell(r, F.YEAR_COLS[y], year_sum(r, y))
            cell.number_format = MONEY
            cell.font = f(8.5, True)
        entry[label] = r
        r += 1
    r += 1

    r = band(ws, r, "VARIANCE AGAINST THE MODEL")
    r = month_header(ws, r)
    pairs = (("Revenue", entry["Revenue — actual"], "Revenue", RV["total"]),
             ("Direct cost", entry["Direct cost — actual"], "Expenses",
              EX["cogs"]),
             ("Operating cost", entry["Operating cost — actual"], "Expenses",
              EX["opex_cash"]),
             ("Closing cash", entry["Closing cash — actual"], "Cash_Flow",
              CF["cash"]))
    for label, arow, sheet, srow in pairs:
        r = monthly_row(ws, r, f"{label} — forecast", lambda m, s=sheet, x=srow:
                        f"={mref(s, x, m)}", "from the model", MONEY,
                        colour=F.LINK_FONT)
        frow = r - 1
        r = monthly_row(ws, r, f"{label} — variance",
                        lambda m, a=arow, fr=frow:
                        f"=IF({ml(m)}{a}=0,0,{ml(m)}{a}-{ml(m)}{fr})",
                        "blank months read as nil", MONEY, bold=True)
    R["Actuals"] = rows
    return ws


SHEET_ORDER = ["Cover", "Dashboard", "Assumptions", "HR_Model", "Actuals",
               "Capex", "Acquisition", "Revenue", "Expenses", "Depreciation",
               "Income_Statement", "Balance_Sheet", "Cash_Flow", "Stress_Test",
               "KPIs", "Sensitivity", "Break_Even", "Payback", "Exit_Strategy"]


def build():
    wb = Workbook()
    wb.remove(wb.active)
    build_assumptions(wb)
    build_hr(wb)
    build_capex(wb)
    build_depreciation(wb)
    build_revenue(wb)
    build_acquisition(wb)
    finish_revenue(wb)
    build_expenses(wb)
    build_income_statement(wb)
    build_cash_flow(wb)
    build_actuals(wb)
    build_balance_sheet(wb)
    build_kpis(wb)
    build_stress(wb)
    build_sensitivity(wb)
    build_breakeven(wb)
    build_payback(wb)
    build_exit(wb)
    build_dashboard(wb)
    build_cover(wb, SHEET_ORDER)
    wb._sheets = [wb[name] for name in SHEET_ORDER]
    wb.active = 0
    return wb


if __name__ == "__main__":
    wb = build()
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "output", "StartPad_Financial_Model.xlsx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wb.save(out)
    print("wrote", out, f"({os.path.getsize(out)/1024:,.0f} KB)")
