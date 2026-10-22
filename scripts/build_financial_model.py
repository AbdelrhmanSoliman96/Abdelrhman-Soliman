"""
Build the StartPad operational financial model.

Sixty months, October 2026 to September 2031, in US dollars. The sheet order
and the column layout follow the reference workbook the founder supplied.

Every cell in the workbook is a formula except the typed inputs, which are blue
on a yellow fill. Nothing is a value this script computed and pasted in, so
changing an assumption changes the model rather than requiring a rebuild.

    python scripts/build_financial_model.py
    python scripts/recalc.py output/StartPad_Financial_Model.xlsx 900
"""
import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

from openpyxl import Workbook                                   # noqa: E402
from openpyxl.chart import BarChart, LineChart, Reference       # noqa: E402
from openpyxl.styles import Alignment, Border, Font             # noqa: E402
from openpyxl.utils import get_column_letter                    # noqa: E402

import _fm as F                                                 # noqa: E402
from _fm import (DATEF, DAYS, MONEY, MONEY2, MULT, NUM, NUM1, NUM2, PCT,  # noqa: E402
                 PCT2, TEXT, band, f, fill, label_cell, mcol, ml,
                 months_of, mref, pos_in_quarter, quarter_of, setup_time,
                 sheet_title, time_header, trow, year_agg, year_of, ycol,
                 yl, yref)
from finmodel import plan as P                                  # noqa: E402

# Sheet names carry spaces, so every cross-sheet reference quotes them.
S_ASS = "'Assumption Setting'"
S_CAP = "'Capital Expenditure'"
S_ACT = "'Actuals'"
S_ACQ = "'Acquisitions'"
S_REV = "'Revenue Streams'"
S_TOT = "'Total Revenue'"
S_PAY = "'Payroll'"
S_DEP = "'Depreciation and Amortization'"
S_EXP = "'Expenses'"
S_IS = "'Income Statement'"
S_BS = "'Balance Sheet'"
S_CF = "'Cash Flow Statement'"
S_FI = "'Financial Indicators'"
S_GTM = "'GTM Capacity and Timing'"

R = {}      # sheet key -> label -> row
A = {}      # assumption key -> absolute reference, or a list of five


# ---------------------------------------------------------------- helpers
def aref(key, m=None, y=None):
    """A reference to an assumption, picking the right year column if needed."""
    v = A[key]
    if isinstance(v, list):
        yy = y if y is not None else year_of(m)
        return v[yy - 1]
    return v


def kv(ws, r, label, note, formulas, fmt=MONEY, bold=False, start=3,
       fill_c=None, colour=F.INK, label_w=None):
    c = ws.cell(r, 1, label)
    c.font = f(9, bold, F.INK)
    if note:
        n = ws.cell(r, 2, note)
        n.font = f(7.5, False, F.MUTED)
    for i, fo in enumerate(formulas):
        cell = ws.cell(r, start + i, fo)
        cell.number_format = fmt
        cell.font = f(9, bold, colour)
        if fill_c:
            cell.fill = fill(fill_c)
    return r + 1


def divider(wb, name, title, items):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 6
    ws.column_dimensions["B"].width = 44
    ws.column_dimensions["C"].width = 92
    ws.cell(2, 2, title).font = Font(name=F.FONT, size=26, bold=True,
                                     color=F.UV)
    ws.row_dimensions[2].height = 38
    for col in (2, 3):
        ws.cell(3, col).border = Border(bottom=F.MED)
    r = 5
    for sheet, what in items:
        ws.cell(r, 2, sheet).font = f(11, True, F.INK)
        c = ws.cell(r, 3, what)
        c.font = f(9, False, F.INK2)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 30
        r += 1
    for col in range(1, 4):
        ws.cell(1, col).fill = fill(F.UV)
    ws.row_dimensions[1].height = 6
    return ws


# =====================================================================
#  COVER
# =====================================================================
def build_cover(wb, order):
    ws = wb.create_sheet("Cover")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 38
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 62
    ws.cell(2, 2, "StartPad").font = Font(name=F.FONT, size=30, bold=True,
                                          color=F.UV)
    ws.row_dimensions[2].height = 42
    ws.cell(3, 2, "Operational Financial Model").font = Font(
        name=F.FONT, size=18, color=F.INK)
    ws.row_dimensions[3].height = 26
    for col in range(2, 5):
        ws.cell(4, col).border = Border(bottom=F.MED)
    r = 6

    def head(t):
        nonlocal r
        ws.cell(r, 2, t).font = f(9.5, True, F.UV)
        r += 1

    def line(k, unit, v, link=False):
        nonlocal r
        ws.cell(r, 2, k).font = f(9.5)
        ws.cell(r, 3, unit).font = f(8.5, False, F.MUTED)
        c = ws.cell(r, 4, v)
        c.font = f(9.5, True, F.LINK_FONT if link else F.INK)
        r += 1

    head("ABOUT THIS MODEL")
    line("Business name", "", "StartPad")
    line("Industry", "", "Entrepreneurship education and venture building")
    line("Markets", "", "Egypt and Saudi Arabia")
    line("Model currency", "", P.CURRENCY)
    line("Model start", "date", "October 2026")
    line("Months in a period", "months", 12)
    line("Forecast period", "years", P.YEARS)
    line("Total months modelled", "months", P.MONTHS)
    r += 1

    head("HOW TO READ IT")
    for t in ("Blue figures on a yellow fill are typed inputs. Change those "
              "and the whole model moves.",
              "Black figures are formulas on the same sheet. Green figures are "
              "links to another sheet.",
              "Red figures are checks. The balance sheet check must read nil "
              "in every column.",
              "On every time sheet the year total comes first, then that "
              "year's twelve months.",
              "No volume is typed. Cohorts, seats, licences and "
              "programmes are produced by the acquisition engine, so cut "
              "the activity and the volume goes with it.",
              "The year one spend is an output of the Expenses sheet, not a "
              "ceiling anybody typed."):
        c = ws.cell(r, 2, t)
        c.font = f(9, False, F.INK2)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        r += 1
    r += 1

    head("CONTENTS")
    for i, (name, blurb) in enumerate(order):
        if name.endswith(">>"):
            ws.cell(r, 2, name.replace(">>", "")).font = f(9.5, True, F.UV)
            ws.cell(r, 4, blurb).font = f(8.5, False, F.MUTED)
        else:
            ws.cell(r, 2, f"   {name}").font = f(9)
            ws.cell(r, 4, blurb).font = f(8.5, False, F.INK2)
            if i % 2 == 0:
                for col in (2, 3, 4):
                    ws.cell(r, col).fill = fill(F.WASH)
        r += 1
    return ws


# =====================================================================
#  ASSUMPTION SETTING
# =====================================================================
def build_assumptions(wb):
    """
    Everything typed in the whole workbook, in the order the model runs:
    what is already true, how StartPad acquires, what an acquired contract
    turns into, what it costs, how it is funded and taxed, what it owns.

    Nothing here is an output. The volume plan that used to sit on this sheet
    is gone: cohorts, seats and programmes are produced by the acquisition
    engine on the Revenue Streams sheet, and the year one spend is produced
    by the Expenses sheet.
    """
    ws = wb.create_sheet("Assumption Setting")
    sheet_title(ws, "Assumption Setting",
                "Every typed number in the model, in the order the model "
                "runs them. Blue on yellow is an input. Nothing on any other "
                "sheet is typed.", last_col=25)
    ws.column_dimensions["A"].width = 54
    ws.column_dimensions["B"].width = 11
    for col in range(3, 24):
        ws.column_dimensions[get_column_letter(col)].width = 11
    ws.column_dimensions["X"].width = 58
    ws.column_dimensions["Y"].width = 46
    ws.freeze_panes = "C5"
    r = 5

    def head(t):
        nonlocal r
        r = band(ws, r, t, last_col=25)

    def note(t):
        nonlocal r
        c = ws.cell(r, 1, t)
        c.font = f(8, False, F.MUTED, italic=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=16)
        r += 1

    def inp(r_, c_, v, fmt):
        cell = ws.cell(r_, c_, v)
        cell.number_format = fmt
        cell.font = f(9, False, F.IN_FONT)
        cell.fill = fill(F.YELLOW)
        return cell

    def why_cell(r_, t, col=24):
        if t:
            c = ws.cell(r_, col, t)
            c.font = f(7.5, False, F.MUTED)
            c.alignment = Alignment(vertical="top", wrap_text=True)

    def one(label, key, unit, val, fmt=MONEY, why=""):
        nonlocal r
        ws.cell(r, 1, label).font = f(9)
        ws.cell(r, 2, unit).font = f(8, False, F.MUTED)
        inp(r, 3, val, fmt)
        why_cell(r, why)
        A[key] = f"{S_ASS}!$C${r}"
        r += 1

    def five(label, key, unit, vals, fmt=MONEY, why=""):
        nonlocal r
        ws.cell(r, 1, label).font = f(9)
        ws.cell(r, 2, unit).font = f(8, False, F.MUTED)
        for i, v in enumerate(vals):
            inp(r, 3 + i, v, fmt)
        why_cell(r, why)
        A[key] = [f"{S_ASS}!${get_column_letter(3 + i)}${r}" for i in range(5)]
        r += 1

    def year_header(start=3):
        nonlocal r
        for i in range(5):
            c = ws.cell(r, start + i, f"Year {i + 1}")
            c.font = f(8, True, F.WHITE)
            c.fill = fill(F.UV_DARK)
            c.alignment = Alignment(horizontal="center")
        r += 1

    def table_header(cols, first="", second="", height=28, start=3):
        nonlocal r
        ws.cell(r, 1, first).font = f(8.5, True, F.WHITE)
        ws.cell(r, 1).fill = fill(F.UV_DARK)
        ws.cell(r, 2, second).font = f(8.5, True, F.WHITE)
        ws.cell(r, 2).fill = fill(F.UV_DARK)
        for i, t in enumerate(cols):
            c = ws.cell(r, start + i, t)
            c.font = f(7.4, True, F.WHITE)
            c.fill = fill(F.UV_DARK)
            c.alignment = Alignment(horizontal="center", wrap_text=True)
        ws.row_dimensions[r].height = height
        r += 1

    # ------------------------------------------------------- 1 basis
    head("1. MODEL BASIS")
    one("Reporting currency", "ccy", "", P.CURRENCY, TEXT)
    one("First calendar month of the model", "start_date", "",
        datetime.date(P.START_YEAR, P.START_MONTH, 1), DATEF,
        "month one. Every month and quarter label in the workbook counts "
        "from here, so quarter one is Q4 2026")
    one("Egyptian pounds to the dollar", "fx_egp", "EGP", P.EGP_PER_USD, NUM2,
        "used only to convert the prize money already committed")
    r += 1

    # --------------------------------------------- 2 opening position
    head("2. WHAT IS ALREADY TRUE, THE OPENING POSITION")
    note("Not forecasts. The position the model opens on: five signed "
         "university memoranda, a competition running now, and the users "
         "already on the platform.")
    for key, lbl, val, unit, why in P.TRACTION:
        one(lbl, key, unit, val, NUM if unit == "#" else MONEY, why)
    ws.cell(r, 1, "Prize money already committed, in dollars").font = f(9)
    ws.cell(r, 2, "USD").font = f(8, False, F.MUTED)
    c = ws.cell(r, 3, f"={A['prize_egp']}/{A['fx_egp']}")
    c.number_format = MONEY
    c.font = f(9, True, F.INK)
    A["prize_usd"] = f"{S_ASS}!$C${r}"
    r += 2

    ws.cell(r, 1, "Signed and near signed institutions").font = f(9, True)
    r += 1
    for col, t in ((1, "Institution"), (3, "Status"), (4, "Detail")):
        c = ws.cell(r, col, t)
        c.font = f(8, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
    r += 1
    for name, status, detail, _y1 in P.SIGNED_INSTITUTIONS:
        ws.cell(r, 1, name).font = f(8.5, True)
        ws.cell(r, 3, status).font = f(8.5, False, F.UV)
        ws.cell(r, 4, detail).font = f(8, False, F.INK2)
        r += 1
    r += 1

    ws.cell(r, 1, "Contracts already signed on day one").font = f(9, True)
    why_cell(r, "these enter the model through the same machinery as a "
                "contract the funnel wins later, so year one volume is "
                "produced rather than typed")
    r += 1
    table_header(["Contracts"], "Engine", "")
    A["open_contracts"] = {}
    for key, n, why in P.OPENING_CONTRACTS:
        label = dict((e[0], e[1]) for e in P.ENGINES)[key]
        ws.cell(r, 1, "Already signed: " + label).font = f(8.5)
        inp(r, 3, n, NUM)
        why_cell(r, why)
        A["open_contracts"][key] = r
        r += 1
    for i, w in enumerate(P.OPENING_MOBILISATION):
        ws.cell(r, 1, f"Share of them mobilising in month {i + 1}").font = \
            f(8.5)
        inp(r, 3, w, PCT)
        A[f"open_mob_{i + 1}"] = f"{S_ASS}!$C${r}"
        r += 1
    r += 1

    # ------------------------------- 3 acquisition, the online funnel
    head("3. ACQUISITION, ONLINE CHANNELS AND THE THREE STAGE FUNNEL")
    note("Budget divided by cost per click gives paid clicks. Organic and "
         "referral traffic are then taken as a stated share of paid, never "
         "assumed free. Three conversion stages follow: click to lead, lead "
         "to registered account, registered account to paid account.")
    table_header(["Monthly budget, Y1", "Monthly, Y2", "Monthly, Y3",
                  "Monthly, Y4", "Monthly, Y5", "Cost per click",
                  "Organic % of paid", "Referral % of paid",
                  "Stage 1, click to lead"],
                 "Online channel", "Every budget on this row is per month")
    A["on"] = {}
    for key, lbl, budgets, cpc, org, ref, s1 in P.ONLINE_CHANNELS:
        ws.cell(r, 1, lbl).font = f(8.5)
        ws.cell(r, 2, "USD").font = f(8, False, F.MUTED)
        for i, v in enumerate(budgets):
            inp(r, 3 + i, v, MONEY)
        inp(r, 8, cpc, MONEY2)
        inp(r, 9, org, PCT)
        inp(r, 10, ref, PCT)
        inp(r, 11, s1, PCT2)
        A["on"][key] = r
        r += 1
    A["on_rows"] = [A["on"][k] for k, *_ in P.ONLINE_CHANNELS]
    A["on_labels"] = [lbl for _, lbl, *_ in P.ONLINE_CHANNELS]
    A["on_keys"] = [k for k, *_ in P.ONLINE_CHANNELS]
    r += 1
    year_header()
    five("Stage 2, lead to registered account", "s2", "%", P.STAGE_2, PCT)
    five("Stage 3, registered to paid, reached online", "s3_online", "%",
         P.STAGE_3_ONLINE, PCT2)
    five("Stage 3, registered to paid, reached through an institution",
         "s3_inst", "%", P.STAGE_3_INSTITUTIONAL, PCT2,
         "a learner who sat in a cohort converts several times better than "
         "a click")
    r += 1

    # --------------------------------- 4 acquisition, offline activity
    head("4. ACQUISITION, OFFLINE ACTIVITY, WHAT THE TEAM ACTUALLY DOES")
    note("This is the engine room. Everything the company sells is traceable "
         "back to a number in this block, and if a number here falls the "
         "volume on the Revenue Streams sheet falls with it.")
    table_header(["Activities per month Y1", "Y2", "Y3", "Y4", "Y5",
                  "Cost per activity", "Free sign ups per activity",
                  "Institutional leads per activity"], "Offline channel", "")
    A["off"] = {}
    for key, lbl, acts, cost, signups, leads, why in P.OFFLINE_CHANNELS:
        ws.cell(r, 1, lbl).font = f(8.5)
        ws.cell(r, 2, "#").font = f(8, False, F.MUTED)
        for i, v in enumerate(acts):
            inp(r, 3 + i, v, NUM1)
        inp(r, 8, cost, MONEY)
        inp(r, 9, signups, NUM)
        inp(r, 10, leads, NUM1)
        why_cell(r, why)
        A["off"][key] = r
        r += 1
    A["off_rows"] = [A["off"][k] for k, *_ in P.OFFLINE_CHANNELS]
    A["off_labels"] = [lbl for _, lbl, *_ in P.OFFLINE_CHANNELS]
    A["off_keys"] = [k for k, *_ in P.OFFLINE_CHANNELS]
    r += 1
    one("Institutional enquiries per 1,000 accounts reached directly",
        "inbound", "#", P.INBOUND_PER_THOUSAND, NUM1,
        "content and the podcast working as pipeline. Counted on accounts "
        "that came through StartPad's own channels, not on learners placed "
        "on the platform by an institution")
    one("Share of online spend serving institutional demand", "online_inst",
        "%", P.ONLINE_INSTITUTIONAL_SHARE, PCT,
        "splits marketing cost between the two funnels")
    r += 1

    # ------------------------------- 5 acquisition, who buys and when
    head("5. ACQUISITION, WHO BUYS, AND HOW LONG EACH KIND TAKES")
    note("Leads split between six buyer types, each with its own conversion "
         "and its own clock. Complexity shows up twice: once as the sales "
         "cycle before signature, once as mobilisation between signature and "
         "the first delivery day.")
    table_header(["Share of leads", "Lead to meeting", "Meeting to proposal",
                  "Proposal to win", "Sales cycle, months",
                  "Mobilisation, signature to first delivery"],
                 "Buyer type", "", height=32)
    A["buyer"] = {}
    for key, lbl, share, m1, m2, m3, cyc, mob, why in P.BUYERS:
        ws.cell(r, 1, lbl).font = f(8.5)
        ws.cell(r, 2, "%").font = f(8, False, F.MUTED)
        inp(r, 3, share, PCT)
        inp(r, 4, m1, PCT)
        inp(r, 5, m2, PCT)
        inp(r, 6, m3, PCT)
        inp(r, 7, cyc, NUM)
        inp(r, 8, mob, NUM)
        why_cell(r, "mobilisation: " + why)
        A["buyer"][key] = r
        r += 1
    A["buyer_rows"] = [(lbl, A["buyer"][k]) for k, lbl, *_ in P.BUYERS]
    A["buyer_keys"] = [k for k, *_ in P.BUYERS]
    n = len(P.BUYERS)
    c = ws.cell(r, 3, f"=SUM(C{r - n}:C{r - 1})")
    c.number_format = PCT
    c.font = f(9, True)
    ws.cell(r, 4, "must total 100%").font = f(7.5, False, F.MUTED)
    r += 2
    year_header()
    five("Win rate uplift as references accumulate", "win_uplift", "x",
         P.WIN_UPLIFT, MULT,
         "applied to the proposal to win stage only")
    r += 1

    # ------------------------ 6 who runs the activity, and how much of it
    head("6. WHO RUNS THE ACTIVITY, AND HOW MUCH OF IT ONE PERSON CAN RUN")
    note("The activity plan above is only credible if somebody is free to do "
         "it. In year one the owning functions are largely empty, which is "
         "why the founder column matters. The sheet named GTM Capacity and "
         "Timing does the arithmetic month by month and fails loudly if the "
         "plan asks for more than the establishment can run.")
    table_header(["Per person in the owning function", "Per founder",
                  "Per ambassador", "Per certified partner organisation"],
                 "Activity", "Owned by", height=30)
    A["cap_act"] = {}
    for key, lbl, function, own, fnd, amb, prt in P.ACTIVITY_CAPACITY:
        ws.cell(r, 1, lbl).font = f(8.5)
        ws.cell(r, 2, function).font = f(7.5, False, F.MUTED)
        inp(r, 3, own, NUM2)
        inp(r, 4, fnd, NUM2)
        inp(r, 5, amb, NUM2)
        inp(r, 6, prt, NUM2)
        why_cell(r, "activities one person can run in a month")
        A["cap_act"][key] = r
        r += 1
    r += 1
    one("Meetings per commercial head per month", "mtg_comm", "#",
        P.MEETINGS_PER_COMMERCIAL_HEAD, NUM,
        "a prepared meeting with a dean, a desk officer or a sponsorship "
        "lead, followed up, not a corridor conversation")
    one("Meetings per founder per month", "mtg_founder", "#",
        P.MEETINGS_PER_FOUNDER, NUM, "on top of running the company")
    one("Meetings per growth and content head per month", "mtg_growth", "#",
        P.MEETINGS_PER_GROWTH_HEAD, NUM)
    r += 1

    # --------------------- 7 revenue, what a won contract turns into
    head("7. REVENUE, WHAT A WON CONTRACT TURNS INTO")
    note("Each engine takes a share of one buyer type's contracts and "
         "delivers a fixed number of units evenly across a contract life. A "
         "contract signed in month m is deliverable from month m plus "
         "mobilisation. Volume on the Revenue Streams sheet is the active "
         "contract stock times units over life, and nothing else.")
    table_header(["Share of that buyer's contracts", "Units per contract",
                  "Contract life, months", "First month it can deliver"],
                 "Engine", "Buyer type", height=32)
    A["eng"] = {}
    for (key, lbl, buyer, share, units, life, unit, gate,
         gate_why) in P.ENGINES:
        ws.cell(r, 1, lbl).font = f(8.5)
        ws.cell(r, 2, dict((b[0], b[1]) for b in P.BUYERS)[buyer]).font = \
            f(7.3, False, F.MUTED)
        inp(r, 3, share, PCT)
        inp(r, 4, units, NUM)
        inp(r, 5, life, NUM)
        inp(r, 6, gate, NUM)
        ws.cell(r, 7, unit).font = f(7.5, False, F.MUTED)
        why_cell(r, gate_why)
        A["eng"][key] = r
        ws.row_dimensions[r].height = 20
        r += 1
    r += 1
    ws.cell(r, 1, "Shares must total 100% for each buyer type").font = \
        f(8.5, True)
    r += 1
    for bkey, blabel, *_ in P.BUYERS:
        rs = [A["eng"][k] for k, _, b, *_ in P.ENGINES if b == bkey]
        ws.cell(r, 1, "    " + blabel).font = f(8)
        c = ws.cell(r, 3, "=" + "+".join(f"C{x}" for x in rs))
        c.number_format = PCT
        c.font = f(8.5, True)
        r += 1
    r += 1
    five("Delivery pace against the full contract rate", "pace", "x",
         P.DELIVERY_PACE, MULT,
         "a contract signed is not a contract delivered at full tilt. In "
         "year one the institution is still localising the curriculum and "
         "training its own faculty. This is also where the year one "
         "spending ceiling is held: set it to 1.00 to run every contract at "
         "its full rate from month one")
    five("Mission Zero seasons produced per year", "podcast_made", "#",
         P.PODCAST_SEASONS_PRODUCED, NUM,
         "the production ceiling. A season nobody sponsors is still a cost, "
         "and sponsored seasons cannot exceed seasons produced")
    r += 1

    # ------------------------------------------- 8 revenue, pricing
    head("8. REVENUE, PRICING BY YEAR")
    year_header()
    for key, (label, unit, vals, why) in P.PRICES.items():
        fmt = MONEY2 if max(vals) < 100 else MONEY
        five(label, key, unit, vals, fmt, why)
    r += 1
    for key, (label, val) in P.SUBSCRIPTION.items():
        fmt = PCT if val < 1 else MONEY
        one(label, key, "USD" if val >= 1 else "%", val, fmt)
    r += 1
    note("How many people one delivered unit reaches. This drives the "
         "institutional side of the subscription funnel.")
    for key, (label, val) in P.REACH.items():
        one(label, key, "#", val, NUM)
    r += 1

    # --------------------------------------- 9 expenses, direct cost
    head("9. EXPENSES, DIRECT COST OF DELIVERY")
    year_header()
    five("Facilitator day rate", "fac_rate", "USD",
         (85, 95, 105, 110, 115), MONEY,
         "certified freelancers, there are no employed facilitators")
    one("Facilitators per cohort", "fac_per", "#", 2, NUM)
    one("Delivery days, university cohort", "d_uni", "days", 6, NUM)
    one("Delivery days, school cohort", "d_school", "days", 4, NUM)
    one("Delivery days, technical cohort", "d_tvet", "days", 5, NUM)
    one("Delivery days one certified facilitator gives per month",
        "fac_days_avail", "days", P.FACILITATOR_DAYS_PER_MONTH, NUM1,
        "a freelancer with other work. This is what sizes the pool")
    one("Spare capacity held in the certified pool", "fac_buffer", "x",
        P.FACILITATOR_BUFFER, MULT,
        "nobody staffs a cohort plan to exactly one hundred percent")
    one("Cost of certifying one facilitator", "c_cert", "USD", 120, MONEY,
        "assessment, materials and the shadow delivery")
    one("Cohorts one certified partner organisation delivers per month",
        "cohorts_per_partner", "#", P.COHORTS_PER_DELIVERY_PARTNER, NUM1)
    five("Materials and showcase, university cohort", "m_uni", "USD",
         (280, 310, 340, 360, 380), MONEY)
    one("Materials and showcase, school cohort", "m_school", "USD", 220,
        MONEY)
    one("Materials and showcase, technical cohort", "m_tvet", "USD", 250,
        MONEY)
    five("Delivery cost, sponsored competition", "c_comp", "USD",
         (3_500, 4_200, 5_000, 5_600, 6_200), MONEY)
    one("Delivery cost, the self funded competition, excluding prizes",
        "c_comp_self", "USD", 900, MONEY,
        "the prizes already committed are added separately")
    five("Production cost, one Mission Zero season", "c_podcast", "USD",
         (2_500, 3_500, 4_500, 5_200, 5_800), MONEY,
         "a freelance two person crew")
    five("Delivery cost, NGO or donor programme", "c_ngo", "USD",
         (4_500, 4_500, 5_200, 5_600, 6_000), MONEY)
    five("Delivery cost, corporate programme", "c_corp", "USD",
         (5_000, 5_000, 6_000, 6_800, 7_400), MONEY)
    five("Delivery cost, train the trainer cohort", "c_tot", "USD",
         (1_600, 1_600, 1_800, 1_950, 2_100), MONEY)
    five("Support cost per national initiative seat", "c_seat_init", "USD",
         (2.20, 2.20, 2.00, 1.85, 1.75), MONEY2,
         "provisioning, a bilingual support queue and partner reporting")
    one("Support cost per programme seat", "c_seat_prog", "USD", 2.20, MONEY2)
    one("Hosting and inference per paid subscriber per month", "c_sub", "USD",
        0.18, MONEY2,
        "sized for a fifteen dollar a year price, not a western one")
    r += 1

    # ----------------------------------- 10 expenses, revenue sharing
    head("10. EXPENSES, REVENUE SHARING WITH THIRD PARTIES")
    note("Three counterparties take a share. Each is margin given up to buy "
         "delivery capacity, distribution or access that would otherwise "
         "have to be hired for.")
    year_header()
    five("Party 1, share of cohorts delivered by certified partners",
         "pd_share", "%", (0.0, 0.08, 0.22, 0.35, 0.45), PCT)
    one("Party 1, the partner's share of that cohort fee", "pd_rate", "%",
        0.40, PCT, "they deliver, StartPad certifies and audits")
    five("Party 2, share of sponsored competition revenue", "ch_comp", "%",
         (0.10, 0.10, 0.10, 0.10, 0.10), PCT,
         "youth and channel organisations such as Enactus and INJAZ")
    one("Party 2, share of programme and incubator seat revenue", "ch_seat",
        "%", 0.10, PCT)
    five("Party 3, share of national initiative seat revenue", "ag_seat", "%",
         (0.07, 0.07, 0.07, 0.06, 0.06), PCT,
         "government aggregators and local distributors")
    one("Party 3, payment processing on subscriptions", "pay_rate", "%",
        0.035, PCT)
    r += 1

    # ---------------------------------- 11 expenses, operating cost
    head("11. EXPENSES, OPERATING COST DRIVERS")
    note("Nothing here is a flat monthly figure chosen by eye. Every line "
         "has a driver: a desk per employee, inference per active learner, "
         "travel per head on the road.")
    year_header()
    five("Desk or office, per employee per month", "o_desk", "USD",
         (65, 85, 100, 110, 120), MONEY,
         "co working in year one, an office later")
    five("Utilities, internet and communications, per employee per month",
         "o_util", "USD", (20, 25, 28, 30, 32), MONEY)
    five("Cloud, AI and third party APIs, fixed per month", "o_cloud", "USD",
         (150, 380, 850, 1_400, 1_900), MONEY)
    one("Cloud and inference, per active learner per month", "o_cloud_var",
        "USD", 0.03, MONEY2)
    five("Software and tooling, per employee per month", "o_soft", "USD",
         (55, 70, 80, 85, 90), MONEY)
    five("Travel, per employee per month", "o_travel", "USD",
         (40, 80, 110, 120, 130), MONEY)
    five("Outsourced finance, legal and audit, per month", "o_prof", "USD",
         (330, 800, 1_400, 1_900, 2_300), MONEY,
         "bought from firms, not hired onto the establishment")
    five("Safeguarding and compliance, per month", "o_safe", "USD",
         (40, 180, 450, 700, 900), MONEY)
    five("Partner enablement, certification and audit, per month",
         "o_partner", "USD", (0, 200, 800, 1_500, 2_100), MONEY)
    five("Insurance, bank charges and sundries, per month", "o_sundry",
         "USD", (110, 180, 280, 360, 440), MONEY)
    five("Campus ambassadors on a stipend", "amb_count", "#",
         (16, 50, 110, 180, 250), NUM)
    one("Ambassador stipend per month", "amb_stipend", "USD", 15, MONEY)
    one("Ambassador active months per year", "amb_months", "#", 7, NUM)
    one("Sales commission on institutional revenue", "commission", "%", 0.04,
        PCT)
    one("Contingency on operating cost", "contingency", "%", 0.04, PCT)
    r += 1

    # ------------------------------- 12 working capital and funding
    head("12. WORKING CAPITAL AND FUNDING")
    one("Days sales outstanding, institutional", "dso", "days", 75, DAYS,
        "universities and ministries pay slowly, the largest cash risk here")
    one("Days sales outstanding, subscriptions", "dso_sub", "days", 2, DAYS)
    one("Days payable outstanding", "dpo", "days", 35, DAYS)
    one("Accrued payroll, days outstanding", "acc_days", "days", 10, DAYS)
    one("Institutional contracts invoiced in advance", "adv_share", "%",
        0.25, PCT, "creates deferred revenue")
    one("Seed round raised", "seed", "USD", 150_000, MONEY,
        "sized on the cash trough, not on a round number")
    one("Month the seed round lands", "seed_month", "#", 4, NUM)
    one("Minimum cash buffer to hold", "min_cash", "USD", 25_000, MONEY)
    one("Years an institutional relationship is retained", "retention", "#",
        2.5, NUM1, "used for institutional lifetime value")
    r += 1

    # ------------------------------------------------------- 13 tax
    head("13. TAX")
    one("Corporate income tax rate", "tax_rate", "%", 0.225, PCT,
        "Egyptian corporate income tax")
    one("Month of the following year in which tax is paid", "tax_month", "#",
        4, NUM)
    one("Tax losses carried forward at inception", "open_losses", "USD", 0,
        MONEY, "none, the company has not traded")
    r += 1

    # ------------------------------------------------- 14 assets
    head("14. ASSETS, DRIVEN BY HEADCOUNT")
    note("Every new employee arrives with a kit, so asset purchases follow "
         "the hiring plan instead of being guessed at. Platform development "
         "is not capitalised: it is the engineers' salaries, and it is "
         "expensed through payroll.")
    table_header(["Cost per unit", "Units per new employee",
                  "Useful life, months"], "Per employee asset", "", height=26)
    A["cap_emp"] = []
    for lbl, cost, units, life in (("Laptop", 750, 1, 36),
                                   ("Monitor and peripherals", 150, 1, 48),
                                   ("Mobile handset and line setup", 180, 1,
                                    24),
                                   ("Desk and chair", 0, 1, 60)):
        ws.cell(r, 1, lbl).font = f(8.5)
        inp(r, 3, cost, MONEY)
        inp(r, 4, units, NUM)
        inp(r, 5, life, NUM)
        A["cap_emp"].append((lbl, r, life))
        r += 1
    r += 1
    ws.cell(r, 1, "Shared and intangible assets").font = f(9, True)
    for i, t in enumerate(["Month acquired", "Cost", "Useful life, months"]):
        c = ws.cell(r, 3 + i, t)
        c.font = f(7.4, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    r += 1
    A["cap_shared"] = []
    for lbl, month, cost, life in (
            ("Mission Zero production kit, camera, audio, lighting", 2, 2_200,
             48),
            ("Network, devices and security", 1, 600, 48),
            ("Trademark, IP registration and entity formation", 1, 3_000, 60),
            ("Riyadh office setup", 25, 4_000, 60),
            ("Cairo office fit out", 25, 6_000, 60)):
        ws.cell(r, 1, lbl).font = f(8.5)
        inp(r, 3, month, NUM)
        inp(r, 4, cost, MONEY)
        inp(r, 5, life, NUM)
        A["cap_shared"].append((lbl, r, life))
        r += 1
    r += 1
    return ws, r


# =====================================================================
#  PAYROLL
# =====================================================================
def build_payroll(wb):
    ws = wb.create_sheet("Payroll")
    setup_time(ws, "Payroll",
               "Fifteen roles, each with a start month and a headcount and a "
               "salary per year. Year one salaries are founder stipends, which "
               "is the only way six people and a year one under 150,000 "
               "dollars are both true. Salaries are capped: the chief "
               "executive reaches 2,000 dollars a month in year five.",
               freeze="C38")
    rows = {}
    r = band(ws, 5, "ESTABLISHMENT, INPUTS")
    hdr = r
    heads = ["Role", "Function", "Start month", "Monthly gross Y1", "Y2", "Y3",
             "Y4", "Y5", "Headcount Y1", "Y2", "Y3", "Y4", "Y5"]
    for i, t in enumerate(heads):
        c = ws.cell(hdr, 1 + i, t)
        c.font = f(7.6, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.row_dimensions[hdr].height = 26
    r += 1
    first = r
    role_rows = []
    for function, role, start, gross, counts in P.ROLES:
        ws.cell(r, 1, role).font = f(8.5)
        ws.cell(r, 2, function).font = f(7.5, False, F.MUTED)
        for col, v, fmt in ([(3, start, NUM)]
                            + [(4 + i, gross[i], MONEY) for i in range(5)]
                            + [(9 + i, counts[i], NUM) for i in range(5)]):
            cell = ws.cell(r, col, v)
            cell.number_format = fmt
            cell.font = f(8.5, False, F.IN_FONT)
            cell.fill = fill(F.YELLOW)
        role_rows.append((r, role, function))
        r += 1
    last = r - 1
    ws.cell(r, 1, "Total establishment").font = f(9, True)
    for i in range(5):
        L = get_column_letter(9 + i)
        c = ws.cell(r, 9 + i, f"=SUM({L}{first}:{L}{last})")
        c.number_format = NUM
        c.font = f(9, True)
    rows["cap_check"] = r
    r += 1
    ws.cell(r, 1, "The cap this plan commits to").font = f(9, True, F.UV)
    for i, v in enumerate(P.HEADCOUNT_CAP):
        c = ws.cell(r, 9 + i, v)
        c.number_format = NUM
        c.font = f(9, True, F.IN_FONT)
        c.fill = fill(F.YELLOW)
    cap_row = r
    r += 1
    ws.cell(r, 1, "Headroom against the cap").font = f(9, True)
    for i in range(5):
        L = get_column_letter(9 + i)
        c = ws.cell(r, 9 + i, f"={L}{cap_row}-{L}{rows['cap_check']}")
        c.number_format = NUM
        c.font = f(9, True, F.RED)
    r += 2

    ws.cell(r, 1, "Employer burden on gross salary").font = f(9)
    ws.cell(r, 2, "social insurance, end of service, medical").font = \
        f(7.5, False, F.MUTED)
    c = ws.cell(r, 3, 0.155)
    c.number_format = PCT
    c.font = f(9, False, F.IN_FONT)
    c.fill = fill(F.YELLOW)
    burden = f"$C${r}"
    r += 2

    gcol = {y: get_column_letter(3 + y) for y in range(1, 6)}
    hcol = {y: get_column_letter(8 + y) for y in range(1, 6)}

    r = band(ws, r, "MONTHLY PAYROLL, FULLY LOADED")
    r = time_header(ws, r)
    cost_first = r
    for ir, role, function in role_rows:
        def cost(m, ir=ir):
            y = year_of(m)
            return (f"=IF({m}<$C${ir},0,${hcol[y]}${ir}*${gcol[y]}${ir}"
                    f"*(1+{burden}))")
        r = trow(ws, r, role, cost, MONEY)
    cost_last = r - 1
    r = trow(ws, r, "Total payroll",
             lambda m: f"=SUM({ml(m)}{cost_first}:{ml(m)}{cost_last})",
             MONEY, bold=True, fill_colour=F.LIME)
    rows["payroll"] = r - 1
    r += 1

    r = band(ws, r, "MONTHLY HEADCOUNT")
    r = time_header(ws, r)
    hc_first = r
    for ir, role, function in role_rows:
        def hc(m, ir=ir):
            return f"=IF({m}<$C${ir},0,${hcol[year_of(m)]}${ir})"
        r = trow(ws, r, role, hc, NUM, agg="end")
    hc_last = r - 1
    r = trow(ws, r, "Total headcount",
             lambda m: f"=SUM({ml(m)}{hc_first}:{ml(m)}{hc_last})",
             NUM, bold=True, agg="end", fill_colour=F.BAND)
    rows["headcount"] = r - 1
    h = rows["headcount"]
    r = trow(ws, r, "New employees joining in the month",
             lambda m: (f"={ml(m)}{h}" if m == 1
                        else f"=MAX(0,{ml(m)}{h}-{ml(m - 1)}{h})"),
             NUM, bold=True)
    rows["new_hires"] = r - 1
    comm = [ir for ir, role, fn in role_rows
            if fn == "Institutional Partnerships"]
    comm_cost = [cost_first + i for i, (ir, role, fn) in enumerate(role_rows)
                 if fn == "Institutional Partnerships"]
    r = trow(ws, r, "Commercial payroll",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in comm_cost),
             MONEY, bold=True)
    rows["commercial_pay"] = r - 1
    r = trow(ws, r, "Commercial heads",
             lambda m: "=" + "+".join(
                 f"IF({m}<$C${ir},0,${hcol[year_of(m)]}${ir})" for ir in comm),
             NUM, agg="end")
    rows["commercial"] = r - 1
    r += 1

    # Capacity is owned by functions, not by job titles, so the establishment
    # is restated by function here and the GTM capacity sheet reads these
    # rows rather than guessing which role runs which activity.
    r = band(ws, r, "HEADCOUNT BY FUNCTION, WHO IS AVAILABLE TO RUN ACTIVITY")
    r = time_header(ws, r)
    rows["fn"] = {}
    for function in dict.fromkeys(fn for _, _, fn in role_rows):
        irs = [ir for ir, _, fn in role_rows if fn == function]
        r = trow(ws, r, function,
                 lambda m, irs=irs: "=" + "+".join(
                     f"IF({m}<$C${ir},0,${hcol[year_of(m)]}${ir})"
                     for ir in irs), NUM, agg="end")
        rows["fn"][function] = r - 1
    fn_first = min(rows["fn"].values())
    fn_last = max(rows["fn"].values())
    r = trow(ws, r, "Check, functions against total establishment",
             lambda m: f"=SUM({ml(m)}{fn_first}:{ml(m)}{fn_last})"
                       f"-{ml(m)}{rows['headcount']}",
             NUM, bold=True, agg="end", colour=F.RED)
    r += 1
    R["pay"] = rows
    return ws


# =====================================================================
#  CAPITAL EXPENDITURE
# =====================================================================
def build_capex(wb):
    ws = wb.create_sheet("Capital Expenditure")
    setup_time(ws, "Capital Expenditure",
               "Per employee assets follow the hiring plan. Shared and "
               "intangible assets are dated explicitly. Platform development "
               "is not capitalised: it is salary, and it is expensed.",
               freeze="C7")
    rows = {}
    nh = R["pay"]["new_hires"]
    r = band(ws, 5, "ADDITIONS IN THE MONTH")
    r = time_header(ws, r)
    classes = []
    first = r
    for lbl, arow, life in A["cap_emp"]:
        r = trow(ws, r, lbl, lambda m, a=arow:
                 f"={mref(S_PAY, nh, m)}*{S_ASS}!$C${a}*{S_ASS}!$D${a}", MONEY)
        classes.append((lbl, r - 1, arow, life))
    for lbl, arow, life in A["cap_shared"]:
        r = trow(ws, r, lbl, lambda m, a=arow:
                 f"=IF({m}={S_ASS}!$C${a},{S_ASS}!$D${a},0)", MONEY)
        classes.append((lbl, r - 1, arow, life))
    last = r - 1
    r = trow(ws, r, "Total capital expenditure",
             lambda m: f"=SUM({ml(m)}{first}:{ml(m)}{last})", MONEY,
             bold=True, fill_colour=F.LIME)
    rows["capex"] = r - 1
    r += 1

    r = band(ws, r, "GROSS COST, CUMULATIVE")
    r = time_header(ws, r)
    cum_first = r
    cum = []
    for lbl, add_row, arow, life in classes:
        this = r
        r = trow(ws, r, lbl, lambda m, a=add_row, t=this:
                 (f"={ml(m)}{a}" if m == 1
                  else f"={ml(m - 1)}{t}+{ml(m)}{a}"), MONEY, agg="end")
        cum.append((lbl, this, arow, life))
    # The last row has to be captured before the total is written: a lambda
    # reading r would see the total's own row and stop one short, which is
    # exactly what it did, silently dropping the last asset class.
    cum_last = r - 1
    r = trow(ws, r, "Total gross assets",
             lambda m: f"=SUM({ml(m)}{cum_first}:{ml(m)}{cum_last})",
             MONEY, bold=True, agg="end", fill_colour=F.BAND)
    rows["gross"] = r - 1
    rows["classes"] = cum
    R["cap"] = rows
    return ws


# =====================================================================
#  DEPRECIATION AND AMORTIZATION
# =====================================================================
def build_depreciation(wb):
    ws = wb.create_sheet("Depreciation and Amortization")
    setup_time(ws, "Depreciation and Amortization",
               "Straight line over each class's useful life, charged from the "
               "month after acquisition and capped so nothing is written below "
               "nil.", freeze="C7")
    rows = {}
    classes = R["cap"]["classes"]
    n = len(classes)
    c_hdr = 5
    c_first = c_hdr + 2
    c_total = c_first + n
    a_hdr = c_total + 2
    a_first = a_hdr + 2
    a_total = a_first + n
    n_hdr = a_total + 2
    n_first = n_hdr + 2
    n_total = n_first + n

    band(ws, c_hdr, "DEPRECIATION CHARGE IN THE MONTH")
    time_header(ws, c_hdr + 1)
    for i, (lbl, cumrow, arow, life) in enumerate(classes):
        trow(ws, c_first + i, lbl, lambda m, c=cumrow, a=a_first + i, ro=arow:
             ("=0" if m == 1 else
              f"=MIN({mref(S_CAP, c, m - 1)}/{S_ASS}!$E${ro},"
              f"{mref(S_CAP, c, m - 1)}-{ml(m - 1)}{a})"), MONEY)
    trow(ws, c_total, "Total depreciation and amortisation",
         lambda m: f"=SUM({ml(m)}{c_first}:{ml(m)}{c_first + n - 1})",
         MONEY, bold=True, fill_colour=F.LIME)
    rows["charge"] = c_total

    band(ws, a_hdr, "ACCUMULATED DEPRECIATION")
    time_header(ws, a_hdr + 1)
    for i in range(n):
        trow(ws, a_first + i, classes[i][0],
             lambda m, c=c_first + i, t=a_first + i:
             (f"={ml(m)}{c}" if m == 1
              else f"={ml(m - 1)}{t}+{ml(m)}{c}"), MONEY, agg="end")
    trow(ws, a_total, "Total accumulated depreciation",
         lambda m: f"=SUM({ml(m)}{a_first}:{ml(m)}{a_first + n - 1})",
         MONEY, bold=True, agg="end", fill_colour=F.BAND)
    rows["accum"] = a_total

    band(ws, n_hdr, "NET BOOK VALUE")
    time_header(ws, n_hdr + 1)
    for i, (lbl, cumrow, arow, life) in enumerate(classes):
        trow(ws, n_first + i, lbl, lambda m, c=cumrow, a=a_first + i:
             f"={mref(S_CAP, c, m)}-{ml(m)}{a}", MONEY, agg="end")
    trow(ws, n_total, "Total net book value",
         lambda m: f"=SUM({ml(m)}{n_first}:{ml(m)}{n_first + n - 1})",
         MONEY, bold=True, agg="end", fill_colour=F.BAND)
    rows["nbv"] = n_total
    intangible = [i for i, (lbl, *_) in enumerate(classes)
                  if "Trademark" in lbl or "IP " in lbl]
    tangible = [i for i in range(n) if i not in intangible]
    rr = n_total + 2
    rr = trow(ws, rr, "Net book value, property and equipment",
              lambda m: "=" + "+".join(f"{ml(m)}{n_first + i}"
                                       for i in tangible),
              MONEY, agg="end", bold=True)
    rows["nbv_tangible"] = rr - 1
    rr = trow(ws, rr, "Net book value, intangible assets",
              lambda m: "=" + "+".join(f"{ml(m)}{n_first + i}"
                                       for i in intangible),
              MONEY, agg="end", bold=True)
    rows["nbv_intangible"] = rr - 1
    R["dep"] = rows
    return ws


# =====================================================================
#  REVENUE STREAMS
# =====================================================================
def build_revenue(wb):
    """
    The sheet is laid out here and its volume rows are left as placeholders.

    They cannot be written yet: a cohort in month 40 is the consequence of a
    contract the funnel won in month 32, and the funnel is built on the next
    sheet. finish_revenue fills them in once the contract book exists. The
    rows have to exist first because the Acquisitions sheet reads them back
    to work out how many learners StartPad reached.
    """
    ws = wb.create_sheet("Revenue Streams")
    setup_time(ws, "Revenue Streams",
               "Volume is not typed anywhere. Every cohort, seat, licence "
               "and programme on this sheet is the active contract book on "
               "the Acquisitions sheet, spread across the contract life.",
               freeze="C7")
    rows = {}
    r = band(ws, 5, "DELIVERY VOLUME, PRODUCED BY THE CONTRACT BOOK")
    r = time_header(ws, r)
    for key, lbl, buyer, share, units, life, unit, gate, why in P.ENGINES:
        fmt = NUM if units >= 100 else NUM1
        rows[key] = r
        r = trow(ws, r, lbl, "=0", fmt, colour=F.LINK_FONT)
    rows["competitions_self"] = r
    r = trow(ws, r, "Competitions, self funded, the one running now", "=0",
             NUM1, colour=F.LINK_FONT)
    r = trow(ws, r, "All in person cohorts delivered", lambda m:
             f"={ml(m)}{rows['uni_cohorts_eg']}"
             f"+{ml(m)}{rows['uni_cohorts_ksa']}"
             f"+{ml(m)}{rows['school_cohorts']}"
             f"+{ml(m)}{rows['tvet_cohorts']}", NUM1, bold=True)
    rows["all_cohorts"] = r - 1
    r += 1

    r = band(ws, r, "REVENUE BY STREAM")
    r = time_header(ws, r)
    first = r
    streams = [
        ("University cohort programmes", lambda m:
         f"=({ml(m)}{rows['uni_cohorts_eg']}+{ml(m)}"
         f"{rows['uni_cohorts_ksa']})*{aref('p_uni', m)}"),
        ("Faculty licences", lambda m:
         f"={ml(m)}{rows['uni_licences']}*{aref('p_uni_lic', m)}"),
        ("School cohorts", lambda m:
         f"={ml(m)}{rows['school_cohorts']}*{aref('p_school', m)}"),
        ("School licences", lambda m:
         f"={ml(m)}{rows['school_licences']}*{aref('p_school_lic', m)}"),
        ("Technical and vocational cohorts", lambda m:
         f"={ml(m)}{rows['tvet_cohorts']}*{aref('p_tvet', m)}"),
        ("National initiative seats", lambda m:
         f"={ml(m)}{rows['initiative_seats']}*{aref('p_seat_init', m)}"),
        ("Train the trainer cohorts", lambda m:
         f"={ml(m)}{rows['tot_cohorts']}*{aref('p_tot', m)}"),
        ("NGO and donor programmes", lambda m:
         f"={ml(m)}{rows['ngo_programmes']}*{aref('p_ngo', m)}"),
        ("Sponsored competitions", lambda m:
         f"={ml(m)}{rows['competitions_sponsored']}*{aref('p_comp', m)}"),
        ("Corporate and CSR programmes", lambda m:
         f"={ml(m)}{rows['corporates']}*{aref('p_corp', m)}"),
        ("Programme and incubator seats", lambda m:
         f"={ml(m)}{rows['prog_seats']}*{aref('p_seat_prog', m)}"),
        ("Mission Zero sponsorship", lambda m:
         f"={ml(m)}{rows['podcast_seasons']}*{aref('p_podcast', m)}"),
    ]
    for lbl, fn in streams:
        r = trow(ws, r, lbl, fn, MONEY)
        rows["rev_" + lbl] = r - 1
    last = r - 1
    r = trow(ws, r, "Institutional and sponsor revenue",
             lambda m: f"=SUM({ml(m)}{first}:{ml(m)}{last})", MONEY,
             bold=True, fill_colour=F.BAND)
    rows["institutional"] = r - 1
    r += 1

    r = band(ws, r, "THE DIRECT ENGINE, FOUNDER SUBSCRIPTIONS")
    r = time_header(ws, r)
    rows["new_subs"] = r
    r = trow(ws, r, "New paid subscribers in the month", "=0", NUM,
             colour=F.LINK_FONT)
    rows["active_subs"] = r
    r = trow(ws, r, "Active paid subscribers", "=0", NUM, agg="end",
             colour=F.LINK_FONT)
    r = trow(ws, r, "Blended annual subscription price", lambda m:
             f"={A['p_pro']}*(1-{A['mix_team']})+{A['p_team']}*{A['mix_team']}",
             MONEY2, agg="avg")
    rows["arpu"] = r - 1
    arpu = rows["arpu"]
    r = trow(ws, r, "Subscription bookings, cash received", lambda m:
             f"={ml(m)}{rows['new_subs']}*{ml(m)}{arpu}", MONEY)
    rows["bookings"] = r - 1
    bk = rows["bookings"]
    r = trow(ws, r, "Subscription revenue recognised", lambda m:
             "=(" + "+".join(f"{ml(k)}{bk}"
                             for k in range(max(1, m - 11), m + 1)) + ")/12",
             MONEY)
    rows["sub_revenue"] = r - 1
    sr = rows["sub_revenue"]
    this = r
    r = trow(ws, r, "Deferred subscription revenue, balance",
             lambda m, t=this: (f"={ml(m)}{bk}-{ml(m)}{sr}" if m == 1
                                else f"={ml(m - 1)}{t}+{ml(m)}{bk}-{ml(m)}{sr}"),
             MONEY, agg="end")
    rows["deferred_sub"] = this
    R["rev"] = rows
    return ws


def finish_revenue(wb):
    """
    Fill the volume rows now that the contract book exists.

    Volume for an engine is the active contract stock times the units one
    contract carries, divided by the contract life, so a contract delivers
    its units evenly across its term and stops. The podcast is additionally
    capped at the seasons actually produced, because a sponsor cannot buy a
    season that was never made.
    """
    ws = wb["Revenue Streams"]
    acq, rows = R["acq"], R["rev"]
    for key, lbl, buyer, share, units, life, unit, gate, why in P.ENGINES:
        er = A["eng"][key]
        act = acq["active"][key]

        def vol(m, a=act, e=er, k=key):
            base = (f"{mref(S_ACQ, a, m)}*{S_ASS}!$D${e}/{S_ASS}!$E${e}"
                    f"*{aref('pace', m)}")
            if k == "podcast_seasons":
                return f"=MIN({base},{aref('podcast_made', m)}/12)"
            return f"={base}"

        row = rows[key]
        for m in range(1, F.MONTHS + 1):
            ws.cell(row, mcol(m), vol(m))

    # The competition running now. StartPad is paying the prizes itself, so
    # it earns nothing: it is here as a cost and as reach, not as revenue.
    row = rows["competitions_self"]
    for m in range(1, F.MONTHS + 1):
        ws.cell(row, mcol(m),
                "=1" if m == P.SELF_FUNDED_COMPETITION_MONTH else "=0")

    for dest, src in (("new_subs", acq["new_paid"]),
                      ("active_subs", acq["active_paid"])):
        row = rows[dest]
        for m in range(1, F.MONTHS + 1):
            ws.cell(row, mcol(m), f"={mref(S_ACQ, src, m)}")


# =====================================================================
#  ACQUISITIONS
# =====================================================================
def build_acquisitions(wb):
    """
    Where every number in the model starts.

    Online spend buys clicks, which become leads, registered accounts and
    paying accounts. Offline activity buys institutional leads, which split
    between six buyer types that each convert differently and on their own
    clock. Won contracts mobilise, enter a contract book by engine, and that
    book is what the Revenue Streams sheet delivers against.
    """
    ws = wb.create_sheet("Acquisitions")
    setup_time(ws, "Acquisitions",
               "Activity to leads to meetings to proposals to signed "
               "contracts to a contract book. Nothing downstream is typed: "
               "cut the activity here and the cohorts disappear.",
               freeze="C7")
    rows = {}
    RV = R["rev"]
    ycl = {y: get_column_letter(2 + y) for y in range(1, 6)}

    def lag(row, lag_ref, m, sheet=None):
        """Reach the month `lag_ref` months before m, across year totals."""
        k = f"({m}-{lag_ref})"
        off = f"2+13*INT(({k}-1)/12)+MOD({k}-1,12)"
        anchor = f"{sheet}!$A${row}" if sheet else f"$A${row}"
        return f"IF({k}<1,0,OFFSET({anchor},0,{off}))"

    # ------------------------------------------- B2C, the CPC funnel
    r = band(ws, 5, "ONLINE CHANNELS, SPEND TO LEADS")
    r = time_header(ws, r)
    paid_rows, click_rows, lead_rows, cost_rows = [], [], [], []
    for lbl, arow in zip(A["on_labels"], A["on_rows"]):
        r = trow(ws, r, lbl, lambda m, a=arow:
                 f"={S_ASS}!${ycl[year_of(m)]}${a}", MONEY)
        spend = r - 1
        cost_rows.append(spend)
        r = trow(ws, r, "Paid clicks", lambda m, a=arow, s=spend:
                 f"=IFERROR({ml(m)}{s}/{S_ASS}!$H${a},0)", NUM, indent=1)
        paid = r - 1
        paid_rows.append(paid)
        r = trow(ws, r, "Total clicks after organic and referral",
                 lambda m, a=arow, pc=paid:
                 f"={ml(m)}{pc}*(1+{S_ASS}!$I${a}+{S_ASS}!$J${a})", NUM,
                 indent=1)
        clicks = r - 1
        click_rows.append(clicks)
        r = trow(ws, r, "Stage 1, leads", lambda m, a=arow, cl=clicks:
                 f"={ml(m)}{cl}*{S_ASS}!$K${a}", NUM1, indent=1)
        lead_rows.append(r - 1)
    r = trow(ws, r, "Online marketing cost",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in cost_rows),
             MONEY, bold=True, fill_colour=F.BAND)
    rows["on_cost"] = r - 1
    r = trow(ws, r, "Total clicks",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in click_rows),
             NUM, bold=True)
    rows["clicks"] = r - 1
    r = trow(ws, r, "Total online leads",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in lead_rows),
             NUM1, bold=True)
    rows["on_leads"] = r - 1
    onl = rows["on_leads"]
    r = trow(ws, r, "Blended cost per lead", lambda m:
             f"=IFERROR({ml(m)}{rows['on_cost']}/{ml(m)}{onl},0)", MONEY2,
             agg="avg")
    rows["cpl"] = r - 1
    r += 1

    # ------------------------------------------------ offline activity
    r = band(ws, r, "OFFLINE ACTIVITY, WHAT THE TEAM DOES")
    r = time_header(ws, r)
    off_cost, off_sign, off_lead = [], [], []
    rows["act"] = {}
    for key, lbl, arow in zip(A["off_keys"], A["off_labels"], A["off_rows"]):
        r = trow(ws, r, lbl, lambda m, a=arow:
                 f"={S_ASS}!${ycl[year_of(m)]}${a}", NUM1)
        acts = r - 1
        rows["act"][key] = acts
        r = trow(ws, r, "Cost", lambda m, a=arow, x=acts:
                 f"={ml(m)}{x}*{S_ASS}!$H${a}", MONEY, indent=1)
        off_cost.append(r - 1)
        r = trow(ws, r, "Free sign ups", lambda m, a=arow, x=acts:
                 f"={ml(m)}{x}*{S_ASS}!$I${a}", NUM, indent=1)
        off_sign.append(r - 1)
        r = trow(ws, r, "Institutional leads", lambda m, a=arow, x=acts:
                 f"={ml(m)}{x}*{S_ASS}!$J${a}", NUM1, indent=1)
        off_lead.append(r - 1)
    r = trow(ws, r, "Offline marketing cost",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in off_cost),
             MONEY, bold=True, fill_colour=F.BAND)
    rows["off_cost"] = r - 1
    r = trow(ws, r, "Offline free sign ups",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in off_sign),
             NUM, bold=True)
    rows["off_signups"] = r - 1
    r = trow(ws, r, "Offline institutional leads",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in off_lead),
             NUM1, bold=True)
    rows["off_leads"] = r - 1
    r = trow(ws, r, "Total marketing cost", lambda m:
             f"={ml(m)}{rows['on_cost']}+{ml(m)}{rows['off_cost']}", MONEY,
             bold=True, fill_colour=F.LIME)
    rows["marketing"] = r - 1
    r += 1

    # ------------------------------------------- institutional funnel
    r = band(ws, r, "INSTITUTIONAL FUNNEL, BY BUYER TYPE")
    r = time_header(ws, r)
    r = trow(ws, r, "Registered accounts from online leads", lambda m:
             f"={ml(m)}{onl}*{aref('s2', m)}", NUM)
    reg_on = r - 1
    r = trow(ws, r, "Registered accounts from offline sign ups", lambda m:
             f"={ml(m)}{rows['off_signups']}*{aref('s2', m)}", NUM)
    reg_off = r - 1
    r = trow(ws, r, "Inbound enquiries from content", lambda m:
             f"=({ml(m)}{reg_on}+{ml(m)}{reg_off})/1000*{A['inbound']}", NUM1)
    inbound = r - 1
    r = trow(ws, r, "Total institutional leads", lambda m:
             f"={ml(m)}{rows['off_leads']}+{ml(m)}{inbound}", NUM1, bold=True,
             fill_colour=F.BAND)
    leads = r - 1
    rows["leads"] = leads
    rows["meet"] = []
    rows["won"] = {}
    rows["mobilised"] = {}
    win_rows, mob_rows = [], []
    for bkey in A["buyer_keys"]:
        brow = A["buyer"][bkey]
        lbl = dict(A["buyer_rows"]).get(
            [l for l, rr in A["buyer_rows"] if rr == brow][0])
        lbl = [l for l, rr in A["buyer_rows"] if rr == brow][0]
        r = trow(ws, r, lbl, lambda m, b=brow:
                 f"={ml(m)}{leads}*{S_ASS}!$C${b}", NUM1, bold=True)
        bl = r - 1
        r = trow(ws, r, "Meetings held", lambda m, b=brow, x=bl:
                 f"={ml(m)}{x}*{S_ASS}!$D${b}", NUM1, indent=1)
        mt = r - 1
        rows["meet"].append(mt)
        r = trow(ws, r, "Proposals, pilots and bids", lambda m, b=brow, x=mt:
                 f"={ml(m)}{x}*{S_ASS}!$E${b}", NUM1, indent=1)
        pr = r - 1
        # The cycle has to reach a specific earlier month, and the month
        # columns are not contiguous: a year total sits between each year, so
        # the column is computed rather than counted.
        r = trow(ws, r, "Contracts signed, after the sales cycle",
                 lambda m, b=brow, x=pr:
                 "=" + lag(x, f"{S_ASS}!$G${b}", m)
                 + f"*{S_ASS}!$F${b}*{aref('win_uplift', m)}",
                 NUM1, indent=1, bold=True)
        wn = r - 1
        win_rows.append(wn)
        rows["won"][bkey] = wn
        r = trow(ws, r, "Contracts mobilised, ready to deliver",
                 lambda m, b=brow, x=wn:
                 "=" + lag(x, f"{S_ASS}!$H${b}", m),
                 NUM1, indent=1, bold=True, fill_colour=F.BAND)
        mob_rows.append(r - 1)
        rows["mobilised"][bkey] = r - 1
    r = trow(ws, r, "Total contracts signed",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in win_rows), NUM1,
             bold=True, fill_colour=F.LIME)
    rows["total_won"] = r - 1
    r = trow(ws, r, "Total contracts mobilised",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in mob_rows), NUM1,
             bold=True, fill_colour=F.LIME)
    rows["total_mobilised"] = r - 1
    r += 1

    # ---------------------------------------------- the contract book
    r = band(ws, r, "THE CONTRACT BOOK, BY ENGINE")
    c = ws.cell(r - 1, 1)
    r = time_header(ws, r)
    c = ws.cell(r - 2, 1)
    rows["open_share"] = {}
    for bkey in A["buyer_keys"]:
        engines = [(k, A["eng"][k]) for k, _, b, *_ in P.ENGINES if b == bkey]
        blbl = [l for l, rr in A["buyer_rows"] if rr == A["buyer"][bkey]][0]
        r = trow(ws, r, blbl + ", share of engines open in the month",
                 lambda m, es=engines: "=" + "+".join(
                     f"IF({m}>={S_ASS}!$F${er},{S_ASS}!$C${er},0)"
                     for _, er in es), PCT, agg="end")
        rows["open_share"][bkey] = r - 1
    c = ws.cell(r, 1, "A contract is signed with a buyer, not with an "
                      "engine. Until an engine opens, that buyer's "
                      "contracts go to the engines that are open, which is "
                      "why a university signing in year one buys a cohort "
                      "rather than a licence.")
    c.font = f(8, False, F.MUTED, italic=True)
    r += 2

    rows["new"], rows["active"] = {}, {}
    open_rows = A["open_contracts"]
    for key, lbl, buyer, share, units, life, unit, gate, why in P.ENGINES:
        er = A["eng"][key]
        mob = rows["mobilised"][buyer]
        osh = rows["open_share"][buyer]

        def new(m, e=er, mo=mob, o=osh, k=key):
            core = (f"IF({m}<{S_ASS}!$F${e},0,"
                    f"IFERROR({ml(m)}{mo}*{S_ASS}!$C${e}/{ml(m)}{o},0))")
            if k in open_rows and m <= len(P.OPENING_MOBILISATION):
                core += (f"+{S_ASS}!$C${open_rows[k]}"
                         f"*{A['open_mob_' + str(m)]}")
            return "=" + core

        r = trow(ws, r, lbl + ", contracts mobilising", new, NUM2)
        nw = r - 1
        rows["new"][key] = nw
        this = r
        r = trow(ws, r, lbl + ", contracts live", lambda m, n=nw, t=this,
                 e=er: (f"={ml(m)}{n}" if m == 1 else
                        f"={ml(m - 1)}{t}+{ml(m)}{n}-"
                        + lag(n, f"{S_ASS}!$E${e}", m)),
                 NUM2, agg="end", bold=True, fill_colour=F.BAND)
        rows["active"][key] = this
    r += 1

    # ------------------------------------------------- learner funnel
    r = band(ws, r, "LEARNER FUNNEL, REACH TO A PAYING ACCOUNT")
    r = time_header(ws, r)
    r = trow(ws, r, "Reached, cohort participants", lambda m:
             f"=({mref(S_REV, RV['uni_cohorts_eg'], m)}"
             f"+{mref(S_REV, RV['uni_cohorts_ksa'], m)})*{A['cohort_size']}"
             f"+({mref(S_REV, RV['school_cohorts'], m)}"
             f"+{mref(S_REV, RV['tvet_cohorts'], m)})*{A['school_size']}",
             NUM)
    rc = r - 1
    r = trow(ws, r, "Reached, competition entrants", lambda m:
             f"=({mref(S_REV, RV['competitions_self'], m)}"
             f"+{mref(S_REV, RV['competitions_sponsored'], m)})"
             f"*{A['entrants_comp']}", NUM)
    rcomp = r - 1
    r = trow(ws, r, "Reached, sponsored and programme seats", lambda m:
             f"={mref(S_REV, RV['initiative_seats'], m)}"
             f"+{mref(S_REV, RV['prog_seats'], m)}", NUM)
    rseat = r - 1
    r = trow(ws, r, "Reached, NGO and corporate participants", lambda m:
             f"={mref(S_REV, RV['ngo_programmes'], m)}*{A['part_ngo']}"
             f"+{mref(S_REV, RV['corporates'], m)}*{A['part_corp']}", NUM)
    rngo = r - 1
    r = trow(ws, r, "Registered accounts from institutions", lambda m:
             f"={ml(m)}{rc}+{ml(m)}{rcomp}+{ml(m)}{rseat}+{ml(m)}{rngo}",
             NUM, bold=True)
    reg_inst = r - 1
    rows["reg_inst"] = reg_inst
    r = trow(ws, r, "Total new registered accounts", lambda m:
             f"={ml(m)}{reg_inst}+{ml(m)}{reg_on}+{ml(m)}{reg_off}", NUM,
             bold=True, fill_colour=F.BAND)
    rows["registered"] = r - 1
    reg = rows["registered"]
    this = r
    r = trow(ws, r, "Cumulative registered accounts",
             lambda m, t=this: (f"={A['registered']}+{ml(m)}{reg}" if m == 1
                                else f"={ml(m - 1)}{t}+{ml(m)}{reg}"),
             NUM, agg="end", bold=True)
    rows["cum_registered"] = this
    r = trow(ws, r, "Stage 3, new paid accounts", lambda m:
             f"={ml(m)}{reg_inst}*{aref('s3_inst', m)}"
             f"+({ml(m)}{reg_on}+{ml(m)}{reg_off})*{aref('s3_online', m)}",
             NUM1, bold=True, fill_colour=F.LIME)
    rows["new_paid"] = r - 1
    np_ = rows["new_paid"]
    this = r
    r = trow(ws, r, "Active paid accounts",
             lambda m, t=this: (f"={A['paid_users']}+{ml(m)}{np_}" if m == 1
                                else f"={ml(m - 1)}{t}*(1-{A['sub_churn']})"
                                     f"+{ml(m)}{np_}"),
             NUM1, bold=True, agg="end")
    rows["active_paid"] = this
    r = trow(ws, r, "Cost per paid account", lambda m:
             f"=IFERROR({ml(m)}{rows['on_cost']}*(1-{A['online_inst']})"
             f"/{ml(m)}{np_},0)", MONEY2, agg="avg")
    rows["cac_b2c"] = r - 1
    r += 1

    r = trow(ws, r, "Institutional acquisition cost", lambda m:
             f"={ml(m)}{rows['off_cost']}"
             f"+{ml(m)}{rows['on_cost']}*{A['online_inst']}"
             f"+{mref(S_PAY, R['pay']['commercial_pay'], m)}",
             MONEY, bold=True)
    rows["inst_spend"] = r - 1
    r = trow(ws, r, "Cost per institutional contract won", lambda m:
             f"=IFERROR({ml(m)}{rows['inst_spend']}"
             f"/{ml(m)}{rows['total_won']},0)", MONEY, agg="avg")
    rows["cac_inst"] = r - 1
    R["acq"] = rows
    return ws


# =====================================================================
#  GTM CAPACITY AND TIMING
# =====================================================================
def build_gtm(wb):
    """
    The sheet that answers "based on what".

    Volume is already an output of the funnel. What this sheet adds is the
    other half of the argument: that the people exist to run the activity the
    funnel needs, that the delivery network exists to deliver what it sells,
    and that the time between the first day of activity and the first day of
    delivery is arithmetic rather than optimism.
    """
    ws = wb.create_sheet("GTM Capacity and Timing")
    setup_time(ws, "GTM Capacity and Timing",
               "Activity starts in month one in every channel. This sheet "
               "shows who runs it, sizes the delivery network it implies, "
               "and shows how long each kind of deal takes to become a "
               "delivery day.", freeze="C7")
    rows = {}
    PAY, ACQ, RV = R["pay"], R["acq"], R["rev"]
    fn = PAY["fn"]

    def pay_fn(function, m):
        return mref(S_PAY, fn[function], m)

    # ------------------------------ 1 the people and the network
    r = band(ws, 5, "1. THE PEOPLE ON THE PAYROLL, AND THE NETWORK THE PLAN "
                    "IMPLIES")
    r = time_header(ws, r)
    for function in fn:
        r = trow(ws, r, function, lambda m, x=function: f"={pay_fn(x, m)}",
                 NUM, agg="end", colour=F.LINK_FONT)
    r = trow(ws, r, "Campus ambassadors on a stipend",
             lambda m: f"={aref('amb_count', m)}", NUM, agg="end",
             colour=F.LINK_FONT)
    amb = r - 1
    rows["ambassadors"] = amb

    r = trow(ws, r, "Facilitator days the cohort plan needs", lambda m: (
        f"=(({mref(S_REV, RV['uni_cohorts_eg'], m)}"
        f"+{mref(S_REV, RV['uni_cohorts_ksa'], m)})*{A['d_uni']}"
        f"+{mref(S_REV, RV['school_cohorts'], m)}*{A['d_school']}"
        f"+{mref(S_REV, RV['tvet_cohorts'], m)}*{A['d_tvet']})"
        f"*{A['fac_per']}"), NUM1)
    need_d = r - 1
    rows["fac_days"] = need_d
    r = trow(ws, r, "Certified facilitators the plan requires", lambda m:
             f"=IFERROR({ml(m)}{need_d}/{A['fac_days_avail']},0)", NUM1,
             indent=1, agg="max")
    req = r - 1
    r = trow(ws, r, "Certified facilitators in the pool", lambda m:
             f"=ROUNDUP({ml(m)}{req}*{A['fac_buffer']},0)", NUM, agg="end",
             bold=True, fill_colour=F.BAND)
    fac = r - 1
    rows["facilitators"] = fac
    r = trow(ws, r, "Facilitators certified in the month",
             lambda m: (f"={ml(m)}{fac}" if m == 1
                        else f"=MAX(0,{ml(m)}{fac}-{ml(m - 1)}{fac})"),
             NUM, indent=1)
    rows["new_facilitators"] = r - 1
    r = trow(ws, r, "Cohorts delivered by certified partners", lambda m:
             f"={mref(S_REV, RV['all_cohorts'], m)}*{aref('pd_share', m)}",
             NUM1)
    pd_cohorts = r - 1
    r = trow(ws, r, "Certified delivery partner organisations", lambda m:
             f"=ROUNDUP(IFERROR({ml(m)}{pd_cohorts}"
             f"/{A['cohorts_per_partner']},0),0)", NUM, agg="end", bold=True,
             fill_colour=F.BAND)
    prt = r - 1
    rows["partners"] = prt
    c = ws.cell(r, 1, "The delivery network is an output, not a wish. The "
                      "plan sells cohorts, the cohorts need days, the days "
                      "need certified freelancers, and certifying them is "
                      "charged to the model. Year one is four employees, so "
                      "the founder column in the capacity table below is "
                      "doing most of the work.")
    c.font = f(8, False, F.MUTED, italic=True)
    r += 2

    # --------------------------------------------- 2 activity capacity
    r = band(ws, r, "2. ACTIVITY THE PLAN NEEDS, AGAINST ACTIVITY THE TEAM "
                    "CAN RUN")
    r = time_header(ws, r)
    short_rows, plan_rows, cap_rows = [], [], []
    for key, lbl, function, *_ in P.ACTIVITY_CAPACITY:
        arow = A["cap_act"][key]
        r = trow(ws, r, lbl + ", planned",
                 lambda m, x=ACQ["act"][key]: f"={mref(S_ACQ, x, m)}",
                 NUM1, colour=F.LINK_FONT)
        planned = r - 1
        plan_rows.append(planned)
        r = trow(ws, r, "Capacity, the people who can run it",
                 lambda m, a=arow, x=function: (
                     f"={pay_fn(x, m)}*{S_ASS}!$C${a}"
                     f"+{pay_fn('Leadership', m)}*{S_ASS}!$D${a}"
                     f"+{ml(m)}{amb}*{S_ASS}!$E${a}"
                     f"+{ml(m)}{prt}*{S_ASS}!$F${a}"),
                 NUM1, indent=1)
        cap = r - 1
        cap_rows.append(cap)
        r = trow(ws, r, "Headroom",
                 lambda m, c=cap, p=planned: f"={ml(m)}{c}-{ml(m)}{p}",
                 NUM1, indent=1)
        short_rows.append((planned, cap))
    r = trow(ws, r, "Activity the plan asks for beyond what the team can run",
             lambda m: "=" + "+".join(f"MAX(0,{ml(m)}{p}-{ml(m)}{c})"
                                      for p, c in short_rows),
             NUM1, bold=True, agg="max", colour=F.RED, fill_colour=F.BAND)
    rows["activity_short"] = r - 1
    r = trow(ws, r, "Activity utilisation",
             lambda m: ("=IFERROR((" + "+".join(f"{ml(m)}{x}"
                                                for x in plan_rows)
                        + ")/(" + "+".join(f"{ml(m)}{x}" for x in cap_rows)
                        + "),0)"),
             PCT, bold=True, agg="avg", fill_colour=F.LIME)
    rows["activity_use"] = r - 1
    c = ws.cell(r, 1, "The row above must read nil in every month. If it "
                      "does not, the plan is running activity nobody is "
                      "free to do, and either the hiring plan or the "
                      "activity plan is wrong.")
    c.font = f(8, False, F.MUTED, italic=True)
    r += 2

    # ---------------------------------------------- 3 meeting capacity
    r = band(ws, r, "3. MEETINGS THE FUNNEL GENERATES, AGAINST MEETINGS THE "
                    "TEAM CAN HOLD")
    r = time_header(ws, r)
    r = trow(ws, r, "Meetings the funnel generates",
             lambda m: "=" + "+".join(f"{mref(S_ACQ, x, m)}"
                                      for x in ACQ["meet"]),
             NUM1, colour=F.LINK_FONT)
    need_m = r - 1
    r = trow(ws, r, "Meetings the team can hold",
             lambda m: (f"={mref(S_PAY, PAY['commercial'], m)}"
                        f"*{A['mtg_comm']}"
                        f"+{pay_fn('Leadership', m)}*{A['mtg_founder']}"
                        f"+{pay_fn('Growth and Content', m)}"
                        f"*{A['mtg_growth']}"),
             NUM1)
    cap_m = r - 1
    r = trow(ws, r, "Meetings asked for beyond capacity",
             lambda m: f"=MAX(0,{ml(m)}{need_m}-{ml(m)}{cap_m})", NUM1,
             bold=True, agg="max", colour=F.RED)
    rows["meeting_short"] = r - 1
    r = trow(ws, r, "Meeting utilisation",
             lambda m: f"=IFERROR({ml(m)}{need_m}/{ml(m)}{cap_m},0)", PCT,
             bold=True, agg="avg", fill_colour=F.LIME)
    rows["meeting_use"] = r - 1
    r += 2

    # ------------------------------------------- 4 the contract book
    r = band(ws, r, "4. THE CONTRACT BOOK THE ACTIVITY PRODUCES")
    r = time_header(ws, r)
    r = trow(ws, r, "Contracts signed",
             lambda m: f"={mref(S_ACQ, ACQ['total_won'], m)}", NUM1,
             colour=F.LINK_FONT)
    r = trow(ws, r, "Contracts mobilised and ready to deliver",
             lambda m: f"={mref(S_ACQ, ACQ['total_mobilised'], m)}", NUM1,
             colour=F.LINK_FONT)
    live = [ACQ["active"][k] for k, *_ in P.ENGINES]
    r = trow(ws, r, "Contracts live across all engines",
             lambda m: "=" + "+".join(f"{mref(S_ACQ, x, m)}" for x in live),
             NUM1, bold=True, agg="end", fill_colour=F.LIME)
    rows["live"] = r - 1
    r = trow(ws, r, "Cost per contract won",
             lambda m: f"={mref(S_ACQ, ACQ['cac_inst'], m)}", MONEY,
             agg="avg", colour=F.LINK_FONT)
    r += 2

    # ---------------------------- 5 first activity to first delivery
    r = band(ws, r, "5. FROM THE FIRST DAY OF ACTIVITY TO THE FIRST DAY OF "
                    "DELIVERY")
    c = ws.cell(r, 1, "Every channel starts in month one, October 2026. What "
                      "follows is arithmetic on the sales cycle and the "
                      "mobilisation period, not judgement: this is the "
                      "earliest a cold conversation opened on day one can "
                      "become a delivered day, by buyer type.")
    c.font = f(8, False, F.MUTED, italic=True)
    r += 1
    hdr = r
    heads = ["Buyer type", "Activity starts", "Sales cycle, months",
             "Signature in month", "Mobilisation, months",
             "First delivery in month", "Which calendar month that is"]
    for i, t in enumerate(heads):
        cc = ws.cell(hdr, 1 + i, t)
        cc.font = f(7.4, True, F.WHITE)
        cc.fill = fill(F.UV_DARK)
        cc.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.row_dimensions[hdr].height = 30
    r += 1
    for lbl, brow in A["buyer_rows"]:
        ws.cell(r, 1, lbl).font = f(8.5)
        for col, formula, fmt in (
                (2, "=1", NUM),
                (3, f"={S_ASS}!$G${brow}", NUM),
                (4, f"=B{r}+C{r}", NUM),
                (5, f"={S_ASS}!$H${brow}", NUM),
                (6, f"=D{r}+E{r}", NUM),
                (7, f"=EDATE({A['start_date']},F{r}-1)", DATEF)):
            cc = ws.cell(r, col, formula)
            cc.number_format = fmt
            cc.font = f(8.5, col == 6)
        r += 1
    r += 1
    c = ws.cell(r, 1, "An engine can also be held back by something other "
                      "than the funnel, and the engine table on the "
                      "Assumption Setting sheet names it in its own column: "
                      "safeguarding clearance for schools, a country manager "
                      "in post for Saudi Arabia, two delivered cohorts "
                      "before a faculty licence.")
    c.font = f(8, False, F.MUTED, italic=True)
    r += 2

    # ------------------------------------ 6 the B2C side of the engine
    r = band(ws, r, "6. THE DIRECT ENGINE, FROM MARKETING SPEND TO A PAYING "
                    "ACCOUNT")
    r = time_header(ws, r)
    r = trow(ws, r, "Marketing spend, online and offline",
             lambda m: f"={mref(S_ACQ, ACQ['marketing'], m)}", MONEY,
             colour=F.LINK_FONT)
    r = trow(ws, r, "New registered accounts",
             lambda m: f"={mref(S_ACQ, ACQ['registered'], m)}", NUM,
             colour=F.LINK_FONT)
    reg = r - 1
    r = trow(ws, r, "New paying accounts",
             lambda m: f"={mref(S_ACQ, ACQ['new_paid'], m)}", NUM1,
             colour=F.LINK_FONT)
    paid = r - 1
    r = trow(ws, r, "Registered to paying, blended",
             lambda m: f"=IFERROR({ml(m)}{paid}/{ml(m)}{reg},0)", PCT2,
             bold=True, agg="avg")
    rows["reg_to_paid"] = r - 1
    r = trow(ws, r, "Cost per paying account",
             lambda m: f"={mref(S_ACQ, ACQ['cac_b2c'], m)}", MONEY2,
             agg="avg", colour=F.LINK_FONT)
    r = trow(ws, r, "Active paying accounts",
             lambda m: f"={mref(S_ACQ, ACQ['active_paid'], m)}", NUM,
             agg="end", bold=True, fill_colour=F.LIME)
    c = ws.cell(r, 1, "The direct engine needs no sales cycle and no "
                      "mobilisation, which is why it carries revenue from "
                      "month one while the institutional engines are still "
                      "in their cycle. A learner who sat in a cohort "
                      "converts several times better than a click, so the "
                      "two routes to a paying account are converted "
                      "separately.")
    c.font = f(8, False, F.MUTED, italic=True)
    r += 1
    R["gtm"] = rows
    return ws


# =====================================================================
#  TOTAL REVENUE
# =====================================================================
def build_total_revenue(wb):
    ws = wb.create_sheet("Total Revenue")
    setup_time(ws, "Total Revenue",
               "Every stream gathered into the four families, and the total "
               "the statements are built on.", freeze="C7")
    rows = {}
    RV = R["rev"]

    def rv(key, m):
        return mref(S_REV, RV["rev_" + key], m)

    r = band(ws, 5, "REVENUE BY FAMILY")
    r = time_header(ws, r)
    fams = [
        ("Education", ["University cohort programmes", "Faculty licences",
                       "School cohorts", "School licences",
                       "Technical and vocational cohorts",
                       "Programme and incubator seats"]),
        ("Public", ["National initiative seats", "Train the trainer cohorts",
                    "NGO and donor programmes"]),
        ("Commercial", ["Sponsored competitions",
                        "Corporate and CSR programmes",
                        "Mission Zero sponsorship"]),
    ]
    fam_rows = []
    for fam, keys in fams:
        r = trow(ws, r, fam,
                 lambda m, ks=keys: "=" + "+".join(rv(k, m) for k in ks),
                 MONEY, bold=True)
        fam_rows.append(r - 1)
        for k in keys:
            r = trow(ws, r, k, lambda m, kk=k: f"={rv(kk, m)}", MONEY,
                     indent=1, colour=F.LINK_FONT)
    r = trow(ws, r, "Direct", lambda m: f"={mref(S_REV, RV['sub_revenue'], m)}",
             MONEY, bold=True)
    fam_rows.append(r - 1)
    r = trow(ws, r, "Founder subscriptions",
             lambda m: f"={mref(S_REV, RV['sub_revenue'], m)}", MONEY,
             indent=1, colour=F.LINK_FONT)
    r += 1
    r = trow(ws, r, "Total revenue",
             lambda m: "=" + "+".join(f"{ml(m)}{x}" for x in fam_rows), MONEY,
             bold=True, fill_colour=F.LIME)
    rows["total"] = r - 1
    tot = rows["total"]
    r = trow(ws, r, "Institutional and sponsor share of revenue", lambda m:
             f"=IFERROR({mref(S_REV, RV['institutional'], m)}/{ml(m)}{tot},0)",
             PCT, agg="avg")
    rows["inst_share"] = r - 1
    r = trow(ws, r, "Month on month growth",
             lambda m: ("=0" if m == 1
                        else f"=IFERROR({ml(m)}{tot}/{ml(m - 1)}{tot}-1,0)"),
             PCT, agg="avg")
    R["tot"] = rows
    return ws


# =====================================================================
#  EXPENSES
# =====================================================================
def build_expenses(wb):
    ws = wb.create_sheet("Expenses")
    setup_time(ws, "Expenses",
               "Direct cost moves with delivery. Operating cost has a driver "
               "behind every line: a desk per employee, inference per active "
               "learner, travel per head on the road.", freeze="C7")
    rows = {}
    RV, AQ, PY, DP = R["rev"], R["acq"], R["pay"], R["dep"]

    def v(key, m):
        return mref(S_REV, RV[key], m)

    def rv(key, m):
        return mref(S_REV, RV["rev_" + key], m)

    r = band(ws, 5, "DIRECT COST OF DELIVERY")
    r = time_header(ws, r)
    first = r
    fac = lambda m: f"{aref('fac_rate', m)}*{A['fac_per']}"
    direct = [
        ("Facilitation, university cohorts", lambda m:
         f"=({v('uni_cohorts_eg', m)}+{v('uni_cohorts_ksa', m)})"
         f"*{fac(m)}*{A['d_uni']}"),
        ("Facilitation, school cohorts", lambda m:
         f"={v('school_cohorts', m)}*{fac(m)}*{A['d_school']}"),
        ("Facilitation, technical cohorts", lambda m:
         f"={v('tvet_cohorts', m)}*{fac(m)}*{A['d_tvet']}"),
        ("Materials, kits and showcases", lambda m:
         f"=({v('uni_cohorts_eg', m)}+{v('uni_cohorts_ksa', m)})"
         f"*{aref('m_uni', m)}"
         f"+{v('school_cohorts', m)}*{A['m_school']}"
         f"+{v('tvet_cohorts', m)}*{A['m_tvet']}"),
        ("Competition delivery, sponsored", lambda m:
         f"={v('competitions_sponsored', m)}*{aref('c_comp', m)}"),
        ("Competition delivery and prizes, self funded", lambda m:
         f"={v('competitions_self', m)}*({A['c_comp_self']}"
         f"+{A['prize_usd']})"),
        ("Mission Zero production", lambda m:
         f"={aref('podcast_made', m)}/12*{aref('c_podcast', m)}"),
        ("NGO and donor programme delivery", lambda m:
         f"={v('ngo_programmes', m)}*{aref('c_ngo', m)}"),
        ("Corporate programme delivery", lambda m:
         f"={v('corporates', m)}*{aref('c_corp', m)}"),
        ("Train the trainer delivery", lambda m:
         f"={v('tot_cohorts', m)}*{aref('c_tot', m)}"),
        ("National initiative seat support", lambda m:
         f"={v('initiative_seats', m)}*{aref('c_seat_init', m)}"),
        ("Programme and incubator seat support", lambda m:
         f"={v('prog_seats', m)}*{A['c_seat_prog']}"),
        ("Subscription hosting and inference", lambda m:
         f"={mref(S_ACQ, AQ['active_paid'], m)}*{A['c_sub']}"),
        ("Certifying facilitators into the delivery pool", lambda m:
         f"={mref(S_GTM, R['gtm']['new_facilitators'], m)}*{A['c_cert']}"),
    ]
    for lbl, fn in direct:
        r = trow(ws, r, lbl, fn, MONEY)
    r = trow(ws, r, "Revenue share, certified delivery partners", lambda m:
             f"=({rv('University cohort programmes', m)}"
             f"+{rv('School cohorts', m)}"
             f"+{rv('Technical and vocational cohorts', m)})"
             f"*{aref('pd_share', m)}*{A['pd_rate']}", MONEY)
    rows["rs1"] = r - 1
    r = trow(ws, r, "Revenue share, youth and channel organisations",
             lambda m: f"={rv('Sponsored competitions', m)}"
                       f"*{aref('ch_comp', m)}"
                       f"+{rv('Programme and incubator seats', m)}"
                       f"*{A['ch_seat']}", MONEY)
    rows["rs2"] = r - 1
    r = trow(ws, r, "Revenue share, aggregators and payment processing",
             lambda m: f"={rv('National initiative seats', m)}"
                       f"*{aref('ag_seat', m)}"
                       f"+{mref(S_REV, RV['sub_revenue'], m)}*{A['pay_rate']}",
             MONEY)
    rows["rs3"] = r - 1
    last = r - 1
    r = trow(ws, r, "Total direct cost",
             lambda m: f"=SUM({ml(m)}{first}:{ml(m)}{last})", MONEY,
             bold=True, fill_colour=F.BAND)
    rows["cogs"] = r - 1
    cogs = rows["cogs"]
    r = trow(ws, r, "Gross profit", lambda m:
             f"={mref(S_TOT, R['tot']['total'], m)}-{ml(m)}{cogs}", MONEY,
             bold=True, fill_colour=F.LIME)
    rows["gross_profit"] = r - 1
    gp = rows["gross_profit"]
    r = trow(ws, r, "Gross margin", lambda m:
             f"=IFERROR({ml(m)}{gp}/{mref(S_TOT, R['tot']['total'], m)},0)",
             PCT, agg="avg")
    rows["gross_margin"] = r - 1
    r += 1

    r = band(ws, r, "OPERATING COST")
    r = time_header(ws, r)
    ofirst = r
    hc = f"{S_PAY}!"
    opex = [
        ("Payroll, fully loaded",
         lambda m: f"={mref(S_PAY, PY['payroll'], m)}", F.LINK_FONT),
        ("Sales commission", lambda m:
         f"={mref(S_REV, RV['institutional'], m)}*{A['commission']}", F.INK),
        ("Marketing, offline channels",
         lambda m: f"={mref(S_ACQ, AQ['off_cost'], m)}", F.LINK_FONT),
        ("Marketing, online channels",
         lambda m: f"={mref(S_ACQ, AQ['on_cost'], m)}", F.LINK_FONT),
        ("Ambassador stipends", lambda m:
         f"={aref('amb_count', m)}*{A['amb_stipend']}*{A['amb_months']}/12",
         F.INK),
        ("Desk and office", lambda m:
         f"={mref(S_PAY, PY['headcount'], m)}*{aref('o_desk', m)}", F.INK),
        ("Utilities, internet and communications", lambda m:
         f"={mref(S_PAY, PY['headcount'], m)}*{aref('o_util', m)}", F.INK),
        ("Cloud, AI inference and APIs", lambda m:
         f"={aref('o_cloud', m)}+({mref(S_ACQ, AQ['registered'], m)}"
         f"+{mref(S_ACQ, AQ['active_paid'], m)})*{A['o_cloud_var']}", F.INK),
        ("Software and tooling", lambda m:
         f"={mref(S_PAY, PY['headcount'], m)}*{aref('o_soft', m)}", F.INK),
        ("Travel", lambda m:
         f"={mref(S_PAY, PY['headcount'], m)}*{aref('o_travel', m)}", F.INK),
        ("Outsourced finance, legal and audit",
         lambda m: f"={aref('o_prof', m)}", F.INK),
        ("Safeguarding and compliance",
         lambda m: f"={aref('o_safe', m)}", F.INK),
        ("Partner enablement, certification and audit",
         lambda m: f"={aref('o_partner', m)}", F.INK),
        ("Insurance, bank charges and sundries",
         lambda m: f"={aref('o_sundry', m)}", F.INK),
    ]
    opex_labels = {}
    for lbl, fn, col in opex:
        r = trow(ws, r, lbl, fn, MONEY, colour=col)
        opex_labels[lbl] = r - 1
    olast = r - 1
    r = trow(ws, r, "Contingency", lambda m:
             f"=SUM({ml(m)}{ofirst}:{ml(m)}{olast})"
             f"*{aref('contingency', m)}", MONEY)
    cont = r - 1
    opex_labels["Contingency"] = cont
    R["exp_labels"] = opex_labels
    r = trow(ws, r, "Operating cost before depreciation", lambda m:
             f"=SUM({ml(m)}{ofirst}:{ml(m)}{olast})+{ml(m)}{cont}", MONEY,
             bold=True, fill_colour=F.BAND)
    rows["opex_cash"] = r - 1
    r = trow(ws, r, "Depreciation and amortisation",
             lambda m: f"={mref(S_DEP, DP['charge'], m)}", MONEY,
             colour=F.LINK_FONT)
    rows["dna"] = r - 1
    r = trow(ws, r, "Total operating cost", lambda m:
             f"={ml(m)}{rows['opex_cash']}+{ml(m)}{rows['dna']}", MONEY,
             bold=True, fill_colour=F.BAND)
    rows["opex_total"] = r - 1
    r += 1

    r = band(ws, r, "RESULT, AND THE YEAR ONE CEILING")
    r = time_header(ws, r)
    r = trow(ws, r, "Total expenses, direct and operating", lambda m:
             f"={ml(m)}{cogs}+{ml(m)}{rows['opex_total']}", MONEY, bold=True,
             fill_colour=F.BAND)
    rows["total_expenses"] = r - 1
    te = rows["total_expenses"]
    r = trow(ws, r, "EBITDA", lambda m:
             f"={ml(m)}{gp}-{ml(m)}{rows['opex_cash']}", MONEY, bold=True,
             fill_colour=F.LIME)
    rows["ebitda"] = r - 1
    r = trow(ws, r, "EBIT, operating profit", lambda m:
             f"={ml(m)}{rows['ebitda']}-{ml(m)}{rows['dna']}", MONEY,
             bold=True, fill_colour=F.LIME)
    rows["ebit"] = r - 1
    r = trow(ws, r, "Cash operating cost excluding payroll", lambda m:
             f"={ml(m)}{rows['opex_cash']}-{mref(S_PAY, PY['payroll'], m)}",
             MONEY)
    rows["opex_ex_payroll"] = r - 1
    r += 1
    ws.cell(r, 1, "Year one total expense, produced by this sheet").font = \
        f(9, True, F.UV)
    c = ws.cell(r, 2, f"={yl(1)}{te}")
    c.number_format = MONEY
    c.font = f(9, True)
    rows["y1_expense"] = r
    cc = ws.cell(r, 3, "an output of the activity plan, the hiring plan and "
                       "the cost drivers, not a number anybody typed")
    cc.font = f(7.5, False, F.MUTED)
    R["exp"] = rows
    return ws


def acol(y):
    """Column letter for year y on an annual sheet."""
    return get_column_letter(2 + y)


def annual_sheet(wb, name, title, subtitle, widths=(50, 32, 15, 15, 15, 15,
                                                    15, 15), last_col=10):
    ws = wb.create_sheet(name)
    sheet_title(ws, title, subtitle, last_col=last_col)
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(1 + i)].width = w
    return ws


def year_header(ws, r, labels=None, start=3, last_col=10):
    labels = labels or [f"Year {y}" for y in range(1, 6)]
    for col in (1, 2):
        ws.cell(r, col).fill = fill(F.UV_DARK)
    for i, t in enumerate(labels):
        c = ws.cell(r, start + i, t)
        c.font = f(9, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center")
        c.number_format = TEXT
    return r + 1


# =====================================================================
#  INCOME STATEMENT
# =====================================================================
def build_income_statement(wb):
    ws = annual_sheet(wb, "Income Statement", "Income Statement",
                      "Five years to 30 September. Every line is the sum of "
                      "its sixty monthly cells, so the annual figures cannot "
                      "drift from the monthly model.")
    rows = {}
    EX, TOT = R["exp"], R["tot"]
    r = year_header(ws, band(ws, 5, "FOR THE YEARS ENDED 30 SEPTEMBER",
                             last_col=10))

    def line(label, sheet, srow, note="", bold=False, pct_row=None,
             fill_c=None, indent=0):
        nonlocal r
        c = ws.cell(r, 1, ("    " * indent) + label)
        c.font = f(9, bold, F.INK)
        if note:
            ws.cell(r, 2, note).font = f(7.5, False, F.MUTED)
        for y in range(1, 6):
            cell = ws.cell(r, 2 + y, f"={sheet}!{yl(y)}${srow}")
            cell.number_format = MONEY
            cell.font = f(9, bold, F.INK if bold else F.LINK_FONT)
            if fill_c:
                cell.fill = fill(fill_c)
        rows[label] = r
        if pct_row:
            for y in range(1, 6):
                pc = ws.cell(r + 1, 2 + y,
                             f"=IFERROR({acol(y)}{r}/{acol(y)}{pct_row},0)")
                pc.number_format = PCT
                pc.font = f(8, False, F.MUTED)
        r += 1

    line("Total revenue", S_TOT, TOT["total"], "every engine", bold=True,
         fill_c=F.BAND)
    rev = rows["Total revenue"]
    ws.cell(r, 1, "Annual growth").font = f(8, False, F.MUTED)
    for y in range(2, 6):
        c = ws.cell(r, 2 + y, f"=IFERROR({acol(y)}{rev}/{acol(y - 1)}{rev}-1,0)")
        c.number_format = PCT
        c.font = f(8, False, F.MUTED)
    r += 1
    line("Cost of revenue", S_EXP, EX["cogs"],
         "facilitation, materials, seats, prizes and revenue share")
    line("Gross profit", S_EXP, EX["gross_profit"], bold=True, fill_c=F.BAND)
    gpr = rows["Gross profit"]
    ws.cell(r, 1, "Gross profit margin").font = f(8, False, F.MUTED)
    for y in range(1, 6):
        c = ws.cell(r, 2 + y, f"=IFERROR({acol(y)}{gpr}/{acol(y)}{rev},0)")
        c.number_format = PCT
        c.font = f(8, False, F.MUTED)
    r += 1
    r += 1
    ws.cell(r, 1, "Operating expenses").font = f(9, True, F.UV)
    r += 1
    for lbl in ("Payroll, fully loaded", "Sales commission",
                "Marketing, offline channels", "Marketing, online channels",
                "Ambassador stipends", "Desk and office",
                "Utilities, internet and communications",
                "Cloud, AI inference and APIs", "Software and tooling",
                "Travel", "Outsourced finance, legal and audit",
                "Safeguarding and compliance",
                "Partner enablement, certification and audit",
                "Insurance, bank charges and sundries", "Contingency"):
        line(lbl, S_EXP, R["exp_labels"][lbl], indent=1)
    line("Total operating expenses", S_EXP, EX["opex_cash"], bold=True,
         fill_c=F.BAND)
    line("EBITDA", S_EXP, EX["ebitda"], bold=True, fill_c=F.LIME)
    eb = rows["EBITDA"]
    ws.cell(r, 1, "EBITDA margin").font = f(8, False, F.MUTED)
    for y in range(1, 6):
        c = ws.cell(r, 2 + y, f"=IFERROR({acol(y)}{eb}/{acol(y)}{rev},0)")
        c.number_format = PCT
        c.font = f(8, False, F.MUTED)
    r += 1
    line("Depreciation and amortisation", S_EXP, EX["dna"])
    line("EBIT, operating profit", S_EXP, EX["ebit"], bold=True, fill_c=F.BAND)
    ebit = rows["EBIT, operating profit"]
    r += 1

    def arow(label, formula_fn, fmt=MONEY, bold=False, note="", fill_c=None,
             colour=F.INK):
        nonlocal r
        c = ws.cell(r, 1, label)
        c.font = f(9, bold, F.INK)
        if note:
            ws.cell(r, 2, note).font = f(7.5, False, F.MUTED)
        for y in range(1, 6):
            cell = ws.cell(r, 2 + y, formula_fn(y))
            cell.number_format = fmt
            cell.font = f(9, bold, colour)
            if fill_c:
                cell.fill = fill(fill_c)
        rows[label] = r
        r += 1
        return r - 1

    ebt = arow("Profit before tax", lambda y: f"={acol(y)}{ebit}",
               bold=True, note="no debt in the plan, so no interest")
    cf_open = arow("Tax losses carried forward, opening",
                   lambda y: (f"={A['open_losses']}" if y == 1
                              else f"={acol(y - 1)}{r + 1}"),
                   note="an early loss shelters a later profit")
    cf_close = arow("Tax losses carried forward, closing", lambda y:
                    f"=MAX(0,{acol(y)}{cf_open}-MAX(0,{acol(y)}{ebt}))"
                    f"+MAX(0,-{acol(y)}{ebt})")
    taxable = arow("Taxable profit", lambda y:
                   f"=MAX(0,{acol(y)}{ebt}-{acol(y)}{cf_open})")
    tax = arow("Corporate income tax", lambda y:
               f"=-{acol(y)}{taxable}*{A['tax_rate']}")
    rows["tax"] = tax
    net = arow("Net profit for the year", lambda y:
               f"={acol(y)}{ebt}+{acol(y)}{tax}", bold=True, fill_c=F.LIME)
    rows["net"] = net
    ws.cell(r, 1, "Net profit margin").font = f(8, False, F.MUTED)
    for y in range(1, 6):
        c = ws.cell(r, 2 + y, f"=IFERROR({acol(y)}{net}/{acol(y)}{rev},0)")
        c.number_format = PCT
        c.font = f(8, False, F.MUTED)
    r += 2
    ws.cell(r, 1, "Total expenses, direct and operating").font = f(9, True)
    for y in range(1, 6):
        c = ws.cell(r, 2 + y, f"={S_EXP}!{yl(y)}${EX['total_expenses']}")
        c.number_format = MONEY
        c.font = f(9, True)
    te = r
    r += 1
    R["is"] = rows
    return ws


# =====================================================================
#  CASH FLOW STATEMENT
# =====================================================================
def build_cash_flow(wb):
    ws = wb.create_sheet("Cash Flow Statement")
    setup_time(ws, "Cash Flow Statement",
               "Indirect method, monthly, with the working capital balances "
               "the balance sheet is built from, then the annual statement.",
               freeze="C7")
    rows = {}
    EX, RV, PY, CPX, IS = R["exp"], R["rev"], R["pay"], R["cap"], R["is"]
    tax_row = IS["tax"]

    r = band(ws, 5, "OPERATING ACTIVITIES")
    r = time_header(ws, r)
    r = trow(ws, r, "EBIT, operating profit",
             lambda m: f"={mref(S_EXP, EX['ebit'], m)}", MONEY,
             colour=F.LINK_FONT)
    ebit = r - 1
    r = trow(ws, r, "Corporate income tax charge", lambda m:
             f"={S_IS}!${acol(year_of(m))}${tax_row}/12", MONEY,
             colour=F.LINK_FONT)
    taxchg = r - 1
    r = trow(ws, r, "Net profit", lambda m:
             f"={ml(m)}{ebit}+{ml(m)}{taxchg}", MONEY, bold=True)
    rows["net"] = r - 1
    net = rows["net"]
    r = trow(ws, r, "Add back depreciation and amortisation",
             lambda m: f"={mref(S_EXP, EX['dna'], m)}", MONEY,
             colour=F.LINK_FONT)
    dna = r - 1
    r += 1

    r = band(ws, r, "WORKING CAPITAL BALANCES AT MONTH END")
    r = time_header(ws, r)
    r = trow(ws, r, "Trade receivables", lambda m:
             f"={mref(S_REV, RV['institutional'], m)}*{A['dso']}/30"
             f"+{mref(S_REV, RV['sub_revenue'], m)}*{A['dso_sub']}/30",
             MONEY, agg="end")
    rows["ar"] = r - 1
    ar = rows["ar"]
    r = trow(ws, r, "Trade and other payables", lambda m:
             f"=({mref(S_EXP, EX['cogs'], m)}"
             f"+{mref(S_EXP, EX['opex_ex_payroll'], m)})*{A['dpo']}/30",
             MONEY, agg="end")
    rows["ap"] = r - 1
    ap = rows["ap"]
    r = trow(ws, r, "Accrued payroll", lambda m:
             f"={mref(S_PAY, PY['payroll'], m)}*{A['acc_days']}/30", MONEY,
             agg="end")
    rows["accrued"] = r - 1
    acc = rows["accrued"]
    r = trow(ws, r, "Deferred revenue", lambda m:
             f"={mref(S_REV, RV['deferred_sub'], m)}"
             f"+{mref(S_REV, RV['institutional'], m)}*{A['adv_share']}",
             MONEY, agg="end")
    rows["deferred"] = r - 1
    dfr = rows["deferred"]
    tp = r
    r = trow(ws, r, "Tax payable",
             lambda m, t=tp: (f"=-{ml(m)}{taxchg}" if m == 1
                              else f"={ml(m - 1)}{t}-{ml(m)}{taxchg}"
                                   f"-{ml(m)}{t + 1}"), MONEY, agg="end")
    rows["taxpay"] = tp
    r = trow(ws, r, "Tax paid in the month", lambda m:
             ("=0" if year_of(m) == 1 else
              f"=IF({m}={(year_of(m) - 1) * 12}+{A['tax_month']},"
              f"-{S_IS}!${acol(year_of(m) - 1)}${tax_row},0)"), MONEY)
    r += 1

    r = band(ws, r, "CASH FLOW")
    r = time_header(ws, r)
    deltas = {}
    for lbl, bal, sign in (("(Increase) decrease in receivables", ar, "-"),
                           ("Increase (decrease) in payables", ap, ""),
                           ("Increase (decrease) in accrued payroll", acc, ""),
                           ("Increase (decrease) in deferred revenue", dfr,
                            "")):
        r = trow(ws, r, lbl, lambda m, b=bal, g=sign:
                 (f"={g}{ml(m)}{b}" if m == 1
                  else f"={g}({ml(m)}{b}-{ml(m - 1)}{b})"), MONEY)
        deltas[bal] = r - 1
    r = trow(ws, r, "Increase (decrease) in tax payable",
             lambda m: (f"={ml(m)}{tp}" if m == 1
                        else f"={ml(m)}{tp}-{ml(m - 1)}{tp}"), MONEY)
    d_tax = r - 1
    r = trow(ws, r, "Net cash from operating activities", lambda m:
             f"={ml(m)}{net}+{ml(m)}{dna}+{ml(m)}{deltas[ar]}"
             f"+{ml(m)}{deltas[ap]}+{ml(m)}{deltas[acc]}"
             f"+{ml(m)}{deltas[dfr]}+{ml(m)}{d_tax}", MONEY, bold=True,
             fill_colour=F.BAND)
    rows["cfo"] = r - 1
    cfo = rows["cfo"]
    r = trow(ws, r, "Capital expenditure",
             lambda m: f"=-{mref(S_CAP, CPX['capex'], m)}", MONEY,
             colour=F.LINK_FONT)
    capex = r - 1
    r = trow(ws, r, "Net cash used in investing activities",
             lambda m: f"={ml(m)}{capex}", MONEY, bold=True)
    rows["cfi"] = r - 1
    cfi = rows["cfi"]
    r = trow(ws, r, "Share capital raised", lambda m:
             f"=IF({m}={A['seed_month']},{A['seed']},0)", MONEY)
    raised = r - 1
    rows["raised"] = raised
    r = trow(ws, r, "Net cash from financing activities",
             lambda m: f"={ml(m)}{raised}", MONEY, bold=True)
    rows["cff"] = r - 1
    cff = rows["cff"]
    r = trow(ws, r, "Net movement in cash", lambda m:
             f"={ml(m)}{cfo}+{ml(m)}{cfi}+{ml(m)}{cff}", MONEY, bold=True)
    move = r - 1
    opening = r
    r = trow(ws, r, "Cash at the start of the month",
             lambda m, t=opening: (f"={A['open_cash']}" if m == 1
                                   else f"={ml(m - 1)}{t + 1}"), MONEY,
             agg="min")
    r = trow(ws, r, "Cash at the end of the month",
             lambda m, o=opening: f"={ml(m)}{o}+{ml(m)}{move}", MONEY,
             bold=True, agg="end", fill_colour=F.LIME)
    rows["cash"] = r - 1
    cash = rows["cash"]
    r = trow(ws, r, "Headroom against the minimum cash buffer", lambda m:
             f"={ml(m)}{cash}-{A['min_cash']}", MONEY, agg="min")
    rows["headroom"] = r - 1
    this = r
    r = trow(ws, r, "Cumulative free cash flow",
             lambda m, t=this: (f"={ml(m)}{cfo}+{ml(m)}{cfi}" if m == 1
                                else f"={ml(m - 1)}{t}+{ml(m)}{cfo}"
                                     f"+{ml(m)}{cfi}"), MONEY, agg="end")
    rows["cum_fcf"] = this
    r += 1

    r = band(ws, r, "CASH FLOW STATEMENT, ANNUAL")
    r = year_header(ws, r, last_col=F.LAST_COL)
    annual = [("Net profit for the year", net, "sum", False),
              ("Depreciation and amortisation", dna, "sum", False),
              ("(Increase) decrease in receivables", deltas[ar], "sum", False),
              ("Increase (decrease) in payables", deltas[ap], "sum", False),
              ("Increase (decrease) in accrued payroll", deltas[acc], "sum",
               False),
              ("Increase (decrease) in deferred revenue", deltas[dfr], "sum",
               False),
              ("Increase (decrease) in tax payable", d_tax, "sum", False),
              ("Net cash from operating activities", cfo, "sum", True),
              ("Net cash used in investing activities", cfi, "sum", True),
              ("Net cash from financing activities", cff, "sum", True),
              ("Net movement in cash", move, "sum", True),
              ("Cash at the end of the year", cash, "end", True)]
    for lbl, srow, agg, bold in annual:
        c = ws.cell(r, 1, lbl)
        c.font = f(9, bold, F.INK)
        for y in range(1, 6):
            formula = (f"={yl(y)}{srow}" if agg == "sum"
                       else f"={ml(list(months_of(y))[-1])}{srow}")
            # The annual block sits in the year total columns, not in C to G,
            # which on this sheet are the first twelve months.
            cell = ws.cell(r, ycol(y), formula)
            cell.number_format = MONEY
            cell.font = f(9, bold)
            if bold:
                cell.fill = fill(F.BAND)
        rows["ann_" + lbl] = r
        r += 1
    R["cf"] = rows
    return ws


# =====================================================================
#  ACTUALS
# =====================================================================
def build_actuals(wb):
    ws = wb.create_sheet("Actuals")
    setup_time(ws, "Actuals",
               "The position the model opens on, and a grid to record each "
               "month as it closes so this stays an operating tool rather "
               "than a one off forecast.", freeze="C7")
    rows = {}
    EX, CF, TOT = R["exp"], R["cf"], R["tot"]
    r = band(ws, 5, "OPENING POSITION AT 30 SEPTEMBER 2026")
    for lbl, note, val in (
            ("Cash at bank", "founder capital already contributed",
             f"={A['open_cash']}"),
            ("Trade receivables", "nothing invoiced yet", 0),
            ("Property and equipment, net", "nothing acquired yet", 0),
            ("Intangible assets, net", "capitalised from month 1", 0)):
        ws.cell(r, 1, lbl).font = f(9)
        ws.cell(r, 2, note).font = f(7.5, False, F.MUTED)
        c = ws.cell(r, 3, val)
        c.number_format = MONEY
        if isinstance(val, str):
            c.font = f(9, False, F.LINK_FONT)
        else:
            c.font = f(9, False, F.IN_FONT)
            c.fill = fill(F.YELLOW)
        rows[lbl] = r
        r += 1
    ws.cell(r, 1, "Total opening assets").font = f(9, True)
    c = ws.cell(r, 3, f"=SUM(C{rows['Cash at bank']}:C{r - 1})")
    c.number_format = MONEY
    c.font = f(9, True)
    rows["assets"] = r
    r += 2
    for lbl, note, val in (
            ("Trade and other payables", "none at inception", 0),
            ("Accrued payroll", "nobody employed before month 1", 0),
            ("Deferred revenue", "nothing billed in advance yet", 0),
            ("Tax payable", "no trading, so nothing owed", 0),
            ("Paid in share capital", "the opening cash, recorded as equity",
             f"={A['open_cash']}"),
            ("Retained earnings", "no trading before month 1", 0)):
        ws.cell(r, 1, lbl).font = f(9)
        ws.cell(r, 2, note).font = f(7.5, False, F.MUTED)
        c = ws.cell(r, 3, val)
        c.number_format = MONEY
        if isinstance(val, str):
            c.font = f(9, False, F.LINK_FONT)
        else:
            c.font = f(9, False, F.IN_FONT)
            c.fill = fill(F.YELLOW)
        rows[lbl] = r
        r += 1
    ws.cell(r, 1, "Total opening liabilities and equity").font = f(9, True)
    c = ws.cell(r, 3, f"=SUM(C{rows['Trade and other payables']}:"
                      f"C{rows['Retained earnings']})")
    c.number_format = MONEY
    c.font = f(9, True)
    rows["liab_eq"] = r
    r += 1
    ws.cell(r, 1, "Check, assets less liabilities and equity").font = f(9, True)
    c = ws.cell(r, 3, f"=C{rows['assets']}-C{rows['liab_eq']}")
    c.number_format = MONEY
    c.font = f(9, True, F.RED)
    r += 2

    r = band(ws, r, "TRACTION ALREADY ACHIEVED, CARRIED INTO THE MODEL")
    for key, lbl, val, unit, why in P.TRACTION:
        ws.cell(r, 1, lbl).font = f(9)
        ws.cell(r, 2, why).font = f(7.5, False, F.MUTED)
        c = ws.cell(r, 3, f"={A[key]}")
        c.number_format = NUM if unit == "#" else MONEY
        c.font = f(9, True, F.LINK_FONT)
        r += 1
    r += 1

    r = band(ws, r, "MONTHLY ACTUALS, ENTER AS EACH MONTH CLOSES")
    c = ws.cell(r, 1, "Leave a month blank until it has closed. Nothing "
                      "downstream reads this grid: the statements run on the "
                      "forecast, and these rows exist so the variance can be "
                      "read without disturbing the model.")
    c.font = f(8, False, F.MUTED, italic=True)
    r += 1
    r = time_header(ws, r)
    entry = {}
    for lbl in ("Revenue, actual", "Direct cost, actual",
                "Operating cost, actual", "Closing cash, actual",
                "Registered accounts, actual", "Paid accounts, actual"):
        label_cell(ws, r, lbl)
        for m in range(1, F.MONTHS + 1):
            cell = ws.cell(r, mcol(m))
            cell.number_format = MONEY if "actual" in lbl and "account" \
                not in lbl else NUM
            cell.font = f(8.2, False, F.IN_FONT)
            cell.fill = fill(F.YELLOW)
        for y in range(1, 6):
            cell = ws.cell(r, ycol(y), year_agg(r, y,
                                                "end" if "account" in lbl
                                                else "sum"))
            cell.number_format = MONEY if "account" not in lbl else NUM
            cell.font = f(8.6, True)
        entry[lbl] = r
        r += 1
    r += 1

    r = band(ws, r, "VARIANCE AGAINST THE MODEL")
    r = time_header(ws, r)
    for lbl, sheet, srow, fmt in (
            ("Revenue", S_TOT, TOT["total"], MONEY),
            ("Direct cost", S_EXP, EX["cogs"], MONEY),
            ("Operating cost", S_EXP, EX["opex_cash"], MONEY),
            ("Closing cash", S_CF, CF["cash"], MONEY)):
        r = trow(ws, r, f"{lbl}, forecast",
                 lambda m, sh=sheet, x=srow: f"={mref(sh, x, m)}", fmt,
                 colour=F.LINK_FONT)
        frow = r - 1
        arow_ = entry[f"{lbl}, actual"]
        r = trow(ws, r, f"{lbl}, variance",
                 lambda m, a=arow_, fr=frow:
                 f"=IF({ml(m)}{a}=0,0,{ml(m)}{a}-{ml(m)}{fr})", fmt,
                 bold=True)
    R["act"] = rows
    return ws


# =====================================================================
#  BALANCE SHEET
# =====================================================================
def build_balance_sheet(wb):
    ws = annual_sheet(wb, "Balance Sheet", "Balance Sheet",
                      "At 30 September each year, with the opening position "
                      "at inception. The check line is nil in every column, "
                      "which is the only proof the model hangs together.",
                      widths=(50, 34, 15, 15, 15, 15, 15, 15))
    rows = {}
    CF, DP, IS, AC = R["cf"], R["dep"], R["is"], R["act"]
    r = year_header(ws, band(ws, 5, "STATEMENT OF FINANCIAL POSITION",
                             last_col=10),
                    labels=["At inception"] + [f"Year {y}" for y in range(1, 6)])
    last_m = {y: list(months_of(y))[-1] for y in range(1, 6)}

    def bs(label, note, open_f, year_f, bold=False, fill_c=None):
        nonlocal r
        c = ws.cell(r, 1, label)
        c.font = f(9, bold, F.INK)
        if note:
            ws.cell(r, 2, note).font = f(7.5, False, F.MUTED)
        cell = ws.cell(r, 3, open_f)
        cell.number_format = MONEY
        cell.font = f(9, bold)
        if fill_c:
            cell.fill = fill(fill_c)
        for y in range(1, 6):
            cell = ws.cell(r, 3 + y, year_f(y))
            cell.number_format = MONEY
            cell.font = f(9, bold)
            if fill_c:
                cell.fill = fill(fill_c)
        rows[label] = r
        r += 1
        return r - 1

    cash = bs("Cash and cash equivalents", "see the cash flow statement",
              f"={S_ACT}!$C${AC['Cash at bank']}",
              lambda y: f"={S_CF}!{ml(last_m[y])}${CF['cash']}")
    ar = bs("Trade receivables", "institutional invoices outstanding",
            f"={S_ACT}!$C${AC['Trade receivables']}",
            lambda y: f"={S_CF}!{ml(last_m[y])}${CF['ar']}")
    tang = bs("Property and equipment, net", "laptops, kit and fit out",
              f"={S_ACT}!$C${AC['Property and equipment, net']}",
              lambda y: f"={S_DEP}!{ml(last_m[y])}${DP['nbv_tangible']}")
    intang = bs("Intangible assets, net", "trademark, IP and formation",
                f"={S_ACT}!$C${AC['Intangible assets, net']}",
                lambda y: f"={S_DEP}!{ml(last_m[y])}${DP['nbv_intangible']}")
    ta = bs("Total assets", "", f"=SUM(C{cash}:C{intang})",
            lambda y: f"=SUM({get_column_letter(3 + y)}{cash}:"
                      f"{get_column_letter(3 + y)}{intang})",
            bold=True, fill_c=F.BAND)
    r += 1
    ap = bs("Trade and other payables", "",
            f"={S_ACT}!$C${AC['Trade and other payables']}",
            lambda y: f"={S_CF}!{ml(last_m[y])}${CF['ap']}")
    acc = bs("Accrued payroll", "", f"={S_ACT}!$C${AC['Accrued payroll']}",
             lambda y: f"={S_CF}!{ml(last_m[y])}${CF['accrued']}")
    dfr = bs("Deferred revenue", "billed, not yet earned",
             f"={S_ACT}!$C${AC['Deferred revenue']}",
             lambda y: f"={S_CF}!{ml(last_m[y])}${CF['deferred']}")
    txp = bs("Tax payable", "paid in arrears",
             f"={S_ACT}!$C${AC['Tax payable']}",
             lambda y: f"={S_CF}!{ml(last_m[y])}${CF['taxpay']}")
    tl = bs("Total liabilities", "", f"=SUM(C{ap}:C{txp})",
            lambda y: f"=SUM({get_column_letter(3 + y)}{ap}:"
                      f"{get_column_letter(3 + y)}{txp})",
            bold=True, fill_c=F.BAND)
    r += 1
    sc = bs("Share capital", "founder capital plus the seed round",
            f"={S_ACT}!$C${AC['Paid in share capital']}",
            lambda y: f"={A['open_cash']}"
                      f"+IF({last_m[y]}>={A['seed_month']},{A['seed']},0)")
    re_ = bs("Retained earnings", "cumulative profit and loss",
             f"={S_ACT}!$C${AC['Retained earnings']}",
             lambda y: "=" + "+".join(f"{S_IS}!${acol(k)}${IS['net']}"
                                      for k in range(1, y + 1)))
    teq = bs("Total equity", "", f"=C{sc}+C{re_}",
             lambda y: f"={get_column_letter(3 + y)}{sc}"
                       f"+{get_column_letter(3 + y)}{re_}",
             bold=True, fill_c=F.BAND)
    tle = bs("Total liabilities and equity", "", f"=C{tl}+C{teq}",
             lambda y: f"={get_column_letter(3 + y)}{tl}"
                       f"+{get_column_letter(3 + y)}{teq}",
             bold=True, fill_c=F.LIME)
    r += 1
    chk = bs("CHECK, total assets less liabilities and equity",
             "nil in every column, or the model is wrong",
             f"=C{ta}-C{tle}",
             lambda y: f"={get_column_letter(3 + y)}{ta}"
                       f"-{get_column_letter(3 + y)}{tle}", bold=True)
    for col in range(3, 9):
        ws.cell(chk, col).font = f(9, True, F.RED)
    rows["check"] = chk
    rows["total_assets"] = ta
    R["bs"] = rows
    return ws


def ar(ws, r, label, note, fn, fmt=MONEY, bold=False, fill_c=None,
       colour=F.INK, store=None):
    """One annual row across five year columns."""
    c = ws.cell(r, 1, label)
    c.font = f(9, bold, F.INK)
    if note:
        ws.cell(r, 2, note).font = f(7.5, False, F.MUTED)
    for y in range(1, 6):
        cell = ws.cell(r, 2 + y, fn(y))
        cell.number_format = fmt
        cell.font = f(9, bold, colour)
        if fill_c:
            cell.fill = fill(fill_c)
    if store is not None:
        store[label] = r
    return r + 1


# =====================================================================
#  FINANCIAL INDICATORS
# =====================================================================
def build_indicators(wb):
    ws = annual_sheet(wb, "Financial Indicators", "Financial Indicators",
                      "The numbers the business is run on, taken from the "
                      "model rather than restated beside it.")
    rows = {}
    IS, EX, CF, AQ, PY, TOT, RV = (R["is"], R["exp"], R["cf"], R["acq"],
                                   R["pay"], R["tot"], R["rev"])
    last_m = {y: list(months_of(y))[-1] for y in range(1, 6)}
    r = year_header(ws, band(ws, 5, "GROWTH AND SCALE", last_col=10))
    r = ar(ws, r, "Total revenue", "",
           lambda y: f"={S_IS}!${acol(y)}${IS['Total revenue']}", bold=True,
           colour=F.LINK_FONT, store=rows)
    rev = rows["Total revenue"]
    r = ar(ws, r, "Revenue growth", "year on year",
           lambda y: ("n/a" if y == 1 else
                      f"=IFERROR({acol(y)}{rev}/{acol(y - 1)}{rev}-1,0)"), PCT)
    r = ar(ws, r, "Institutional and sponsor share of revenue", "engines 1 to 7",
           lambda y: f"=IFERROR({S_REV}!{yl(y)}${RV['institutional']}"
                     f"/{S_TOT}!{yl(y)}${TOT['total']},0)", PCT)
    r = ar(ws, r, "Cohorts delivered", "all formats including free pilots",
           lambda y: f"={S_REV}!{yl(y)}${RV['all_cohorts']}", NUM, store=rows)
    r = ar(ws, r, "New registered accounts", "",
           lambda y: f"={S_ACQ}!{yl(y)}${AQ['registered']}", NUM, store=rows)
    r = ar(ws, r, "Registered accounts at year end", "",
           lambda y: f"={S_ACQ}!{ml(last_m[y])}${AQ['cum_registered']}", NUM)
    r = ar(ws, r, "Active paid accounts at year end", "",
           lambda y: f"={S_ACQ}!{ml(last_m[y])}${AQ['active_paid']}", NUM,
           store=rows)
    r = ar(ws, r, "Employees at year end", "the cap this plan commits to",
           lambda y: f"={S_PAY}!{ml(last_m[y])}${PY['headcount']}", NUM,
           store=rows)
    hc = rows["Employees at year end"]
    r = ar(ws, r, "Revenue per employee", "",
           lambda y: f"=IFERROR({acol(y)}{rev}/{acol(y)}{hc},0)")
    r = ar(ws, r, "Certified facilitators in the pool", "not on the payroll",
           lambda y: f"={S_GTM}!{ml(last_m[y])}${R['gtm']['facilitators']}",
           NUM)
    r += 1

    r = year_header(ws, band(ws, r, "PROFITABILITY", last_col=10))
    r = ar(ws, r, "Gross profit", "",
           lambda y: f"={S_IS}!${acol(y)}${IS['Gross profit']}",
           colour=F.LINK_FONT, store=rows)
    gp = rows["Gross profit"]
    r = ar(ws, r, "Gross margin", "",
           lambda y: f"=IFERROR({acol(y)}{gp}/{acol(y)}{rev},0)", PCT,
           bold=True)
    r = ar(ws, r, "EBITDA", "", lambda y: f"={S_IS}!${acol(y)}${IS['EBITDA']}",
           colour=F.LINK_FONT, store=rows)
    eb = rows["EBITDA"]
    r = ar(ws, r, "EBITDA margin", "",
           lambda y: f"=IFERROR({acol(y)}{eb}/{acol(y)}{rev},0)", PCT,
           bold=True)
    r = ar(ws, r, "Net profit", "",
           lambda y: f"={S_IS}!${acol(y)}${IS['net']}", colour=F.LINK_FONT,
           store=rows)
    np_ = rows["Net profit"]
    r = ar(ws, r, "Net margin", "",
           lambda y: f"=IFERROR({acol(y)}{np_}/{acol(y)}{rev},0)", PCT,
           bold=True)
    r = ar(ws, r, "Total expenses, direct and operating", "",
           lambda y: f"={S_EXP}!{yl(y)}${EX['total_expenses']}", bold=True,
           store=rows)
    te = rows["Total expenses, direct and operating"]
    r += 1

    r = year_header(ws, band(ws, r, "UNIT ECONOMICS AND THE FUNNEL",
                             last_col=10))
    r = ar(ws, r, "Blended cost per lead, online", "",
           lambda y: f"={S_ACQ}!{yl(y)}${AQ['cpl']}", MONEY2)
    r = ar(ws, r, "Cost per paid account", "learner CAC",
           lambda y: f"=IFERROR({S_ACQ}!{yl(y)}${AQ['on_cost']}"
                     f"*(1-{A['online_inst']})"
                     f"/{S_ACQ}!{yl(y)}${AQ['new_paid']},0)", MONEY2,
           store=rows)
    cacb = rows["Cost per paid account"]
    r = ar(ws, r, "Subscriber lifetime value",
           "annual price times gross margin, over monthly churn",
           lambda y: f"=IFERROR({S_REV}!{yl(y)}${RV['arpu']}/12"
                     f"*IFERROR({acol(y)}{gp}/{acol(y)}{rev},0)"
                     f"/{A['sub_churn']},0)", MONEY2, store=rows)
    ltv = rows["Subscriber lifetime value"]
    r = ar(ws, r, "Subscriber LTV to CAC", "",
           lambda y: f"=IFERROR({acol(y)}{ltv}/{acol(y)}{cacb},0)", MULT,
           bold=True)
    r = ar(ws, r, "Cost per institutional contract won",
           "offline activity, a share of online, and the commercial payroll",
           lambda y: f"=IFERROR({S_ACQ}!{yl(y)}${AQ['inst_spend']}"
                     f"/{S_ACQ}!{yl(y)}${AQ['total_won']},0)", store=rows)
    caci = rows["Cost per institutional contract won"]
    r = ar(ws, r, "Average institutional contract value", "first year value",
           lambda y: f"=IFERROR({S_REV}!{yl(y)}${RV['institutional']}"
                     f"/{S_ACQ}!{yl(y)}${AQ['total_won']},0)", store=rows)
    acv = rows["Average institutional contract value"]
    r = ar(ws, r, "Institutional LTV to CAC",
           "contract value times gross margin times years retained, over "
           "CAC",
           lambda y: f"=IFERROR({acol(y)}{acv}"
                     f"*IFERROR({acol(y)}{gp}/{acol(y)}{rev},0)"
                     f"*{A['retention']}"
                     f"/{acol(y)}{caci},0)", MULT, bold=True)
    r = ar(ws, r, "Contracts live at year end",
           "the book the activity has built",
           lambda y: f"={S_GTM}!{ml(last_m[y])}${R['gtm']['live']}", NUM1,
           bold=True)
    r += 1

    r = year_header(ws, band(ws, r, "CASH", last_col=10))
    r = ar(ws, r, "Cash at year end", "",
           lambda y: f"={S_CF}!{ml(last_m[y])}${CF['cash']}", bold=True,
           colour=F.LINK_FONT, store=rows)
    r = ar(ws, r, "Lowest cash balance in the year", "",
           lambda y: f"=MIN({S_CF}!{ml(list(months_of(y))[0])}${CF['cash']}:"
                     f"{ml(last_m[y])}${CF['cash']})", store=rows)
    r = ar(ws, r, "Net cash from operations", "",
           lambda y: f"={S_CF}!{yl(y)}${CF['cfo']}")
    r = ar(ws, r, "Free cash flow", "operations less capital expenditure",
           lambda y: f"={S_CF}!{yl(y)}${CF['cfo']}+{S_CF}!{yl(y)}${CF['cfi']}",
           bold=True, store=rows)
    fcf = rows["Free cash flow"]
    r = ar(ws, r, "Average monthly burn or generation", "",
           lambda y: f"={acol(y)}{fcf}/12")
    r = ar(ws, r, "Months of runway at year end cash", "on that year's burn",
           lambda y: f"=IF({acol(y)}{fcf}>=0,99,IFERROR("
                     f"{acol(y)}{rows['Cash at year end']}"
                     f"/(-{acol(y)}{fcf}/12),0))", NUM1)
    r = ar(ws, r, "Debtor days achieved", "receivables over revenue",
           lambda y: f"=IFERROR({S_CF}!{ml(last_m[y])}${CF['ar']}"
                     f"/{acol(y)}{rev}*365,0)", NUM)
    R["fi"] = rows
    return ws


# =====================================================================
#  BEP ANALYSIS
# =====================================================================
def all_months(sheet, row):
    """Every month cell of a row, as five contiguous ranges."""
    return ",".join(
        f"{sheet}!{ml(list(months_of(y))[0])}${row}:"
        f"{ml(list(months_of(y))[-1])}${row}" for y in range(1, 6))


def build_bep(wb):
    ws = annual_sheet(wb, "BEP Analysis", "Break Even Analysis",
                      "Where the contribution from delivery covers the cost "
                      "of existing, and the month the company stops consuming "
                      "cash.")
    EX, CF, TOT, RV = R["exp"], R["cf"], R["tot"], R["rev"]
    rows = {}
    r = year_header(ws, band(ws, 5, "ANNUAL BREAK EVEN", last_col=10))
    r = ar(ws, r, "Revenue", "", lambda y: f"={S_TOT}!{yl(y)}${TOT['total']}",
           colour=F.LINK_FONT, store=rows)
    rev = rows["Revenue"]
    r = ar(ws, r, "Variable cost of delivery",
           "direct cost, prizes and revenue share",
           lambda y: f"={S_EXP}!{yl(y)}${EX['cogs']}", colour=F.LINK_FONT,
           store=rows)
    vc = rows["Variable cost of delivery"]
    r = ar(ws, r, "Contribution", "",
           lambda y: f"={acol(y)}{rev}-{acol(y)}{vc}", bold=True, store=rows)
    con = rows["Contribution"]
    r = ar(ws, r, "Contribution margin", "",
           lambda y: f"=IFERROR({acol(y)}{con}/{acol(y)}{rev},0)", PCT,
           bold=True, store=rows)
    cm = rows["Contribution margin"]
    r = ar(ws, r, "Fixed operating cost",
           "everything that does not move with a cohort, including "
           "depreciation",
           lambda y: f"={S_EXP}!{yl(y)}${EX['opex_total']}",
           colour=F.LINK_FONT, store=rows)
    fc = rows["Fixed operating cost"]
    r = ar(ws, r, "Break even revenue", "fixed cost over contribution margin",
           lambda y: f"=IFERROR({acol(y)}{fc}/{acol(y)}{cm},0)", bold=True,
           fill_c=F.LIME, store=rows)
    be = rows["Break even revenue"]
    r = ar(ws, r, "Break even revenue per month", "",
           lambda y: f"={acol(y)}{be}/12")
    r = ar(ws, r, "Margin of safety",
           "how far revenue can fall before a loss",
           lambda y: f"=IFERROR(({acol(y)}{rev}-{acol(y)}{be})"
                     f"/{acol(y)}{rev},0)", PCT, bold=True)
    r = ar(ws, r, "Break even in university cohort equivalents",
           "at that year's cohort price",
           lambda y: f"=IFERROR({acol(y)}{be}/{aref('p_uni', y=y)},0)", NUM)
    r = ar(ws, r, "Cohorts actually delivered", "for comparison",
           lambda y: f"={S_REV}!{yl(y)}${RV['all_cohorts']}", NUM,
           colour=F.LINK_FONT)
    r += 1

    r = band(ws, r, "THE MONTH IT TURNS", last_col=10)
    for i, t in enumerate(["Month number", "Which month"]):
        c = ws.cell(r, 3 + i, t)
        c.font = f(9, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
    r += 1
    lbl_row = r
    for m in range(1, F.MONTHS + 1):
        ws.cell(lbl_row, mcol(m), F.MONTH_LABELS[m - 1]).number_format = TEXT
    ws.cell(lbl_row, 1, "Month labels, lookup row").font = f(8, False, F.MUTED)
    ws.row_dimensions[lbl_row].hidden = True
    r += 1
    specs = (("First month with positive EBITDA", S_EXP, EX["ebitda"],
              "delivery covers the cost of existing", "pos"),
             ("First month with positive operating cash flow", S_CF,
              CF["cfo"], "profit converted into cash", "pos"),
             ("Month of the lowest cash balance", S_CF, CF["cash"],
              "the trough of the cash curve", "trough"),
             ("First month cumulative free cash flow turns positive", S_CF,
              CF["cum_fcf"], "the business has repaid its own burn", "pos"))
    helpers = []
    for label, sheet, srow, note, mode in specs:
        hr = r
        trow(ws, hr, label + ", working",
             lambda m, s=sheet, x=srow, md=mode:
             (f"=IF({mref(s, x, m)}>0,{m},9999)" if md == "pos" else
              f"=IF({mref(s, x, m)}=MIN({all_months(s, x)}),{m},9999)"),
             NUM, years=False)
        ws.row_dimensions[hr].hidden = True
        helpers.append((label, hr, note))
        r += 1
    for label, hr, note in helpers:
        ws.cell(r, 1, label).font = f(9, True)
        ws.cell(r, 2, note).font = f(7.5, False, F.MUTED)
        c = ws.cell(r, 3, f"=MIN({ml(1)}{hr}:{ml(F.MONTHS)}{hr})")
        c.number_format = NUM
        c.font = f(9, True)
        ws.cell(r, 4, f'=IF(C{r}=9999,"not within 60 months",'
                      f'INDEX(${ml(1)}${lbl_row}:${ml(F.MONTHS)}${lbl_row},1,'
                      f'C{r}))').font = f(9, True, F.UV)
        r += 1
    ws.column_dimensions["D"].width = 24
    R["bep"] = rows
    return ws


# =====================================================================
#  PAYBACK ANALYSIS
# =====================================================================
def build_payback(wb):
    ws = annual_sheet(wb, "PB Analysis", "Payback Analysis",
                      "When the money put in comes back, in the base case and "
                      "under stress.")
    CF, FI = R["cf"], R["fi"]
    rows = {}
    r = band(ws, 5, "CAPITAL IN", last_col=10)
    r = ar(ws, r, "Founder capital at inception", "already contributed",
           lambda y: (f"={A['open_cash']}" if y == 1 else '=""'), bold=True)
    r = ar(ws, r, "Seed round", "the raise this model sizes",
           lambda y: (f"={A['seed']}" if y == 1 else '=""'), bold=True)
    r = ar(ws, r, "Total capital invested", "",
           lambda y: (f"={A['open_cash']}+{A['seed']}" if y == 1 else '=""'),
           bold=True, fill_c=F.LIME, store=rows)
    inv = rows["Total capital invested"]
    r += 1

    r = year_header(ws, band(ws, r, "CASH RETURNED, BASE CASE", last_col=10))
    r = ar(ws, r, "Free cash flow in the year", "operations less capex",
           lambda y: f"={S_FI}!${acol(y)}${FI['Free cash flow']}",
           colour=F.LINK_FONT, store=rows)
    fcf = rows["Free cash flow in the year"]
    cum = r
    r = ar(ws, r, "Cumulative free cash flow", "",
           lambda y: (f"=C{fcf}" if y == 1
                      else f"={acol(y - 1)}{cum}+{acol(y)}{fcf}"), bold=True,
           store=rows)
    r = ar(ws, r, "Capital recovered", "cumulative free cash flow over capital",
           lambda y: f"=IFERROR({acol(y)}{cum}/$C${inv},0)", PCT, bold=True)
    r = ar(ws, r, "Capital still outstanding", "",
           lambda y: f"=MAX(0,$C${inv}-{acol(y)}{cum})")
    r += 1

    r = band(ws, r, "PAYBACK PERIOD", last_col=10)
    lbl_row = r
    for m in range(1, F.MONTHS + 1):
        ws.cell(lbl_row, mcol(m), F.MONTH_LABELS[m - 1]).number_format = TEXT
    ws.row_dimensions[lbl_row].hidden = True
    r += 1
    flag = r
    trow(ws, flag, "Payback flag, working", lambda m:
         f"=IF({mref(S_CF, CF['cum_fcf'], m)}>=$C${inv},{m},9999)", NUM,
         years=False)
    ws.row_dimensions[flag].hidden = True
    r += 1
    ws.cell(r, 1, "Months to repay all capital invested").font = f(9, True)
    ws.cell(r, 2, "cumulative free cash flow covers the money in").font = \
        f(7.5, False, F.MUTED)
    c = ws.cell(r, 3, f"=MIN({ml(1)}{flag}:{ml(F.MONTHS)}{flag})")
    c.number_format = NUM
    c.font = f(9, True)
    ws.cell(r, 4, f'=IF(C{r}=9999,"beyond the 60 months modelled",'
                  f'INDEX(${ml(1)}${lbl_row}:${ml(F.MONTHS)}${lbl_row},1,'
                  f'C{r}))').font = f(9, True, F.UV)
    ws.column_dimensions["D"].width = 28
    rows["payback_months"] = r
    r += 2

    r = band(ws, r, "WHAT THE PAYBACK IS SENSITIVE TO", last_col=10)
    hdr = r
    for i, t in enumerate(["Volume at", "Cumulative free cash flow, 5 years",
                           "Capital recovered"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.row_dimensions[hdr].height = 26
    r += 1
    for flex in (-0.40, -0.25, -0.10, 0.0, 0.10, 0.25):
        ws.cell(r, 1, "Delivery volume flexed").font = f(9)
        c = ws.cell(r, 3, 1 + flex)
        c.number_format = MULT
        c.font = f(9, False, F.IN_FONT)
        c.fill = fill(F.YELLOW)
        c2 = ws.cell(r, 4, f"=SUMPRODUCT(($C${fcf}:$G${fcf}))"
                           f"+({S_TOT}!{yl(1)}${R['tot']['total']}"
                           f"+{S_TOT}!{yl(2)}${R['tot']['total']}"
                           f"+{S_TOT}!{yl(3)}${R['tot']['total']}"
                           f"+{S_TOT}!{yl(4)}${R['tot']['total']}"
                           f"+{S_TOT}!{yl(5)}${R['tot']['total']}"
                           f"-{S_EXP}!{yl(1)}${R['exp']['cogs']}"
                           f"-{S_EXP}!{yl(2)}${R['exp']['cogs']}"
                           f"-{S_EXP}!{yl(3)}${R['exp']['cogs']}"
                           f"-{S_EXP}!{yl(4)}${R['exp']['cogs']}"
                           f"-{S_EXP}!{yl(5)}${R['exp']['cogs']})*(C{r}-1)")
        c2.number_format = MONEY
        c2.font = f(9)
        c3 = ws.cell(r, 5, f"=IFERROR(D{r}/$C${inv},0)")
        c3.number_format = PCT
        c3.font = f(9, True)
        r += 1
    c = ws.cell(r, 1, "Volume flexes revenue and direct cost together; the "
                      "operating base is held, which is what makes a volume "
                      "shortfall expensive.")
    c.font = f(8, False, F.MUTED, italic=True)
    R["pb"] = rows
    return ws


# =====================================================================
#  SENSITIVITY AND STRESS
# =====================================================================
def build_sensitivity(wb):
    ws = annual_sheet(wb, "Sensitivity", "Sensitivity Analysis",
                      "Two way grids on the year five result. Every cell is a "
                      "live formula, so a changed assumption moves the whole "
                      "grid.",
                      widths=(40, 14, 14, 14, 14, 14, 14), last_col=9)
    TOT, EX, RV = R["tot"], R["exp"], R["rev"]
    rev5 = f"{S_TOT}!{yl(5)}${TOT['total']}"
    cogs5 = f"{S_EXP}!{yl(5)}${EX['cogs']}"
    opex5 = f"{S_EXP}!{yl(5)}${EX['opex_cash']}"
    r = 5

    def grid(title, note_t, rowvals, colvals, rowlab, collab, cell_fn,
             fmt=MONEY):
        nonlocal r
        r = band(ws, r, title, last_col=9)
        c = ws.cell(r, 1, note_t)
        c.font = f(8, False, F.MUTED, italic=True)
        r += 1
        ws.cell(r, 2, collab).font = f(8, True, F.UV)
        for j, cv in enumerate(colvals):
            cell = ws.cell(r, 3 + j, cv)
            cell.number_format = PCT
            cell.font = f(8.5, True, F.IN_FONT)
            cell.fill = fill(F.YELLOW)
            cell.alignment = Alignment(horizontal="center")
        colrow = r
        r += 1
        first = r
        for rv in rowvals:
            cell = ws.cell(r, 2, rv)
            cell.number_format = PCT
            cell.font = f(8.5, True, F.IN_FONT)
            cell.fill = fill(F.YELLOW)
            ws.cell(r, 1, rowlab if r == first else "").font = f(8, True, F.UV)
            for j, cv in enumerate(colvals):
                cc = ws.cell(r, 3 + j,
                             cell_fn(f"$B${r}",
                                     f"{get_column_letter(3 + j)}${colrow}"))
                cc.number_format = fmt
                cc.font = f(8.5)
            r += 1
        r += 1

    steps = [-0.30, -0.15, 0.0, 0.15, 0.30]
    grid("YEAR FIVE EBITDA, VOLUME AGAINST PRICE",
         "Rows flex delivery volume, columns flex price. Direct cost moves "
         "with volume, the operating base does not.",
         steps, [-0.15, -0.075, 0.0, 0.075, 0.15],
         "Volume change", "Price change",
         lambda rv, cv: f"={rev5}*(1+{rv})*(1+{cv})-{cogs5}*(1+{rv})-{opex5}")
    grid("YEAR FIVE EBITDA, VOLUME AGAINST OPERATING COST",
         "Columns flex the fixed operating base, the cost of holding the "
         "establishment and the network.",
         steps, [-0.20, -0.10, 0.0, 0.10, 0.20],
         "Volume change", "Operating cost change",
         lambda rv, cv: f"={rev5}*(1+{rv})-{cogs5}*(1+{rv})-{opex5}*(1+{cv})")
    grid("YEAR FIVE EBITDA, COST PER CLICK AGAINST PAID CONVERSION",
         "The two levers that decide whether the direct engine pays for "
         "itself. Rows flex every channel's cost per click, columns flex the "
         "registered to paid rate.",
         [-0.30, -0.15, 0.0, 0.25, 0.50], [-0.40, -0.20, 0.0, 0.25, 0.50],
         "Cost per click change", "Paid conversion change",
         lambda rv, cv:
         f"={rev5}-{cogs5}-{opex5}"
         f"+({S_REV}!{yl(5)}${RV['sub_revenue']}*{cv})"
         f"-({S_ACQ}!{yl(5)}${R['acq']['on_cost']}*{rv})")
    return ws


def build_stress(wb):
    ws = annual_sheet(wb, "Stress Test", "Stress Testing",
                      "Four scenarios applied to the base case. Volume and "
                      "price flex, the operating base barely does, which is "
                      "what makes a shortfall expensive.",
                      widths=(34, 22, 13, 13, 13, 13, 13, 13), last_col=10)
    TOT, EX, CF = R["tot"], R["exp"], R["cf"]
    r = band(ws, 5, "SCENARIO LEVERS", last_col=10)
    hdr = r
    for i, t in enumerate(["Volume", "Price", "Operating cost",
                           "Collection days", "Paid conversion"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr, 1, "Scenario").font = f(9, True, F.WHITE)
    for col in (1, 2):
        ws.cell(hdr, col).fill = fill(F.UV_DARK)
    ws.row_dimensions[hdr].height = 26
    r += 1
    scen = [("Base case", "the plan as modelled", 1.00, 1.00, 1.00, 1.00, 1.00),
            ("Upside", "institutional demand lands early", 1.20, 1.03, 1.06,
             0.92, 1.15),
            ("Downside", "a slow first two years in Egypt", 0.72, 0.94, 1.00,
             1.20, 0.80),
            ("Severe", "public budgets freeze and a market slips", 0.50, 0.86,
             0.96, 1.45, 0.65)]
    first_s = r
    for name, note_t, *vals in scen:
        ws.cell(r, 1, name).font = f(9, name == "Base case")
        ws.cell(r, 2, note_t).font = f(7.5, False, F.MUTED)
        for i, v in enumerate(vals):
            c = ws.cell(r, 3 + i, v)
            c.number_format = MULT
            c.font = f(9, False, F.IN_FONT)
            c.fill = fill(F.YELLOW)
        r += 1
    rowof = {s[0]: first_s + i for i, s in enumerate(scen)}
    r += 1

    def block(title, fn, fmt=MONEY):
        nonlocal r
        r = year_header(ws, band(ws, r, title, last_col=10))
        out = {}
        for name, *_ in scen:
            sr = rowof[name]
            ws.cell(r, 1, name).font = f(9, name == "Base case")
            for y in range(1, 6):
                cell = ws.cell(r, 2 + y, fn(sr, y))
                cell.number_format = fmt
                cell.font = f(9, name == "Base case")
            out[name] = r
            r += 1
        r += 1
        return out

    block("REVENUE UNDER STRESS",
          lambda sr, y: f"={S_TOT}!{yl(y)}${TOT['total']}*$C${sr}*$D${sr}")
    eb = block("EBITDA UNDER STRESS", lambda sr, y:
               f"={S_TOT}!{yl(y)}${TOT['total']}*$C${sr}*$D${sr}"
               f"-{S_EXP}!{yl(y)}${EX['cogs']}*$C${sr}"
               f"-{S_EXP}!{yl(y)}${EX['opex_cash']}*$E${sr}")
    r = band(ws, r, "CASH AND WHAT IT WOULD TAKE TO SURVIVE", last_col=10)
    hdr = r
    for i, t in enumerate(["Year 1", "Year 2", "Year 3", "Year 4", "Year 5",
                           "Lowest cash", "Further funding needed"]):
        c = ws.cell(hdr, 3 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr, 1, "Scenario").font = f(9, True, F.WHITE)
    ws.row_dimensions[hdr].height = 26
    r += 1
    for name, *_ in scen:
        sr, er = rowof[name], eb[name]
        ws.cell(r, 1, name).font = f(9, name == "Base case")
        for y in range(1, 6):
            col = acol(y)
            prev = (f"{A['open_cash']}+{A['seed']}" if y == 1
                    else f"{acol(y - 1)}{r}")
            cell = ws.cell(r, 2 + y,
                           f"={prev}+{col}{er}"
                           f"-{S_CAP}!{yl(y)}${R['cap']['capex']}"
                           f"-{S_CF}!{ml(list(months_of(y))[-1])}"
                           f"${CF['ar']}*($F${sr}-1)")
            cell.number_format = MONEY
            cell.font = f(9, name == "Base case")
        ws.cell(r, 8, f"=MIN(C{r}:G{r})").number_format = MONEY
        ws.cell(r, 8).font = f(9, True)
        ws.cell(r, 9, f"=MAX(0,{A['min_cash']}-H{r})").number_format = MONEY
        ws.cell(r, 9).font = f(9, True, F.RED)
        r += 1
    r += 1
    c = ws.cell(r, 1, "The cash rows re run the base case cash walk with the "
                      "scenario's EBITDA and collection cycle substituted. "
                      "They are an overlay on the model, not a second model: "
                      "capital expenditure and payables are held at the base "
                      "case, which makes the downside slightly flattering and "
                      "is the honest direction for an error to run.")
    c.font = f(8, False, F.MUTED, italic=True)
    return ws


# =====================================================================
#  EXIT, ANGEL AND VC
# =====================================================================
def build_exit(wb):
    ws = annual_sheet(wb, "Exit Angel and VC", "Investor Return and Exit",
                      "What an angel and a venture investor each put in, what "
                      "they hold after dilution, and what the holding is worth "
                      "on three exit assumptions.",
                      widths=(48, 28, 17, 17, 17), last_col=6)
    FI = R["fi"]
    r = band(ws, 5, "THE ROUND", last_col=6)
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
        ws.cell(r, 1, label).font = f(9, bold, F.INK)
        if note:
            ws.cell(r, 2, note).font = f(7.5, False, F.MUTED)
        for i, v in enumerate((a_val, b_val)):
            c = ws.cell(r, 3 + i, v)
            c.number_format = fmt
            c.font = f(9, bold, F.IN_FONT if inputs else F.INK)
            if inputs:
                c.fill = fill(F.YELLOW)
            elif fill_c:
                c.fill = fill(fill_c)
        r += 1
        return r - 1

    amt = pair("Amount invested",
               "the angel takes part of the seed, the fund takes a later round",
               125_000, 750_000, MONEY, inputs=True)
    pre = pair("Pre money valuation",
               "a MENA pre revenue to early revenue range",
               900_000, 4_500_000, MONEY, inputs=True)
    post = pair("Post money valuation", "",
                f"=C{pre}+C{amt}", f"=D{pre}+D{amt}", MONEY, bold=True)
    own = pair("Ownership at entry", "",
               f"=IFERROR(C{amt}/C{post},0)", f"=IFERROR(D{amt}/D{post},0)",
               PCT, bold=True)
    dil = pair("Dilution from later rounds", "two further rounds assumed",
               0.42, 0.25, PCT, inputs=True)
    fin = pair("Ownership at exit", "",
               f"=C{own}*(1-C{dil})", f"=D{own}*(1-D{dil})", PCT, bold=True,
               fill_c=F.LIME)
    r += 1

    r = band(ws, r, "WHAT THE COMPANY IS WORTH AT EXIT", last_col=6)
    c = ws.cell(r, 1, "Three bases, because no single multiple is defensible "
                      "on its own. Education businesses selling to "
                      "institutions trade on revenue while they are growing "
                      "and on earnings once they are not.")
    c.font = f(8, False, F.MUTED, italic=True)
    r += 1
    hdr = r
    for i, t in enumerate(["Multiple", "Exit value", "Angel proceeds",
                           "Venture proceeds"]):
        c = ws.cell(hdr, 2 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws.cell(hdr, 1, "Basis").font = f(9, True, F.WHITE)
    ws.cell(hdr, 1).fill = fill(F.UV_DARK)
    ws.row_dimensions[hdr].height = 24
    r += 1
    rev5 = f"{S_FI}!$G${FI['Total revenue']}"
    eb5 = f"{S_FI}!$G${FI['EBITDA']}"
    base_rows = []
    for label, note_t, mult, base in (
            ("Year five revenue multiple, conservative",
             "a slower growth trade sale", 2.0, rev5),
            ("Year five revenue multiple, central",
             "the base case for a strategic buyer", 3.5, rev5),
            ("Year five revenue multiple, strong", "a competitive process",
             5.5, rev5),
            ("Year five EBITDA multiple", "a cash generative buyer's view",
             10.0, eb5)):
        ws.cell(r, 1, label).font = f(9, True)
        ws.cell(r, 2, note_t).font = f(7.5, False, F.MUTED)
        c = ws.cell(r, 3, mult)
        c.number_format = MULT
        c.font = f(9, False, F.IN_FONT)
        c.fill = fill(F.YELLOW)
        c2 = ws.cell(r, 4, f"=C{r}*{base}")
        c2.number_format = MONEY
        c2.font = f(9, True)
        for i in range(2):
            cc = ws.cell(r, 5 + i,
                         f"=$D${r}*{get_column_letter(3 + i)}${fin}")
            cc.number_format = MONEY
            cc.font = f(9)
        base_rows.append(r)
        r += 1
    r += 1

    central = base_rows[1]
    r = band(ws, r, "RETURN TO THE INVESTOR, ON THE CENTRAL MULTIPLE",
             last_col=6)
    yrs = pair("Years held from entry to exit",
               "the angel enters at the seed, the fund at a later round",
               5.0, 3.5, NUM1, inputs=True)
    proc = pair("Proceeds at exit", "on the central revenue multiple",
                f"=E{central}", f"=F{central}", MONEY, bold=True)
    moic = pair("Multiple of money returned", "",
                f"=IFERROR(C{proc}/C{amt},0)", f"=IFERROR(D{proc}/D{amt},0)",
                MULT, bold=True, fill_c=F.LIME)
    pair("Annualised return",
         "the internal rate of return on one investment and one exit",
         f"=IFERROR(C{moic}^(1/C{yrs})-1,0)",
         f"=IFERROR(D{moic}^(1/D{yrs})-1,0)", PCT, bold=True, fill_c=F.LIME)
    r += 1

    r = band(ws, r, "THE ROUTES OUT", last_col=6)
    for label, text in (
            ("Strategic acquisition by an education group",
             "A regional training or education group buying the institutional "
             "relationships and the certified network. The most likely route, "
             "and the one the business is shaped for: a buyer acquires "
             "delivery capacity in two markets without building it."),
            ("Acquisition by a platform or edtech consolidator",
             "A buyer acquiring the curriculum, the assessment record and the "
             "Arabic product. Values the platform and the data rather than "
             "the relationships."),
            ("Secondary sale at the Series A or B",
             "Early investors sell part of the holding to an incoming fund. "
             "Partial liquidity at three to four years without an exit."),
            ("Acquisition by a government backed vehicle",
             "A sovereign or development backed fund buying national delivery "
             "capacity. Slower, lower multiple, highest certainty once the "
             "initiative engine is contracted."),
            ("Continue and distribute",
             "A profitable company of this size can pay dividends rather than "
             "sell. The weakest return for an investor and the one a founder "
             "should name openly rather than leave implied.")):
        ws.cell(r, 1, label).font = f(9, True)
        c = ws.cell(r, 2, text)
        c.font = f(8.5, False, F.INK2)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
        ws.row_dimensions[r].height = 34
        r += 1
    return ws


# =====================================================================
#  SUMMARY AND MARKET RESEARCH
# =====================================================================
def build_summary(wb):
    ws = annual_sheet(wb, "Summary", "Summary",
                      "The whole model on one page. Every figure is a link, "
                      "nothing here is typed.",
                      widths=(48, 30, 15, 15, 15, 15, 15), last_col=9)
    FI, BS, IS = R["fi"], R["bs"], R["is"]
    r = year_header(ws, band(ws, 5, "HEADLINES", last_col=9))
    for lbl, srow, fmt, bold in (
            ("Total revenue", FI["Total revenue"], MONEY, True),
            ("Gross profit", FI["Gross profit"], MONEY, False),
            ("EBITDA", FI["EBITDA"], MONEY, True),
            ("Net profit", FI["Net profit"], MONEY, True),
            ("Total expenses, direct and operating",
             FI["Total expenses, direct and operating"], MONEY, True),
            ("Cash at year end", FI["Cash at year end"], MONEY, True),
            ("Lowest cash balance in the year",
             FI["Lowest cash balance in the year"], MONEY, False),
            ("Employees at year end", FI["Employees at year end"], NUM, False),
            ("Cohorts delivered", FI["Cohorts delivered"], NUM, False),
            ("New registered accounts", FI["New registered accounts"], NUM,
             False),
            ("Active paid accounts at year end",
             FI["Active paid accounts at year end"], NUM, False)):
        r = ar(ws, r, lbl, "", lambda y, s=srow: f"={S_FI}!${acol(y)}${s}",
               fmt, bold=bold, colour=F.INK if bold else F.LINK_FONT)
    r += 1
    r = band(ws, r, "THE TWO CHECKS THAT MATTER", last_col=9)
    r = ar(ws, r, "Year one total expense, produced not typed",
           "the output of the activity plan, the hiring plan and the cost "
           "drivers",
           lambda y: (f"={S_FI}!$C${FI['Total expenses, direct and operating']}"
                      if y == 1 else '=""'), bold=True)
    r = ar(ws, r, "Balance sheet check", "nil in every column",
           lambda y: f"={S_BS}!{get_column_letter(3 + y)}${BS['check']}",
           bold=True, colour=F.RED)
    r += 1
    anchor = r
    r += 22
    r = band(ws, r, "WHAT THIS MODEL OPENS ON", last_col=9)
    for key, lbl, val, unit, why in P.TRACTION:
        ws.cell(r, 1, lbl).font = f(9)
        ws.cell(r, 2, why).font = f(7.5, False, F.MUTED)
        c = ws.cell(r, 3, f"={A[key]}")
        c.number_format = NUM if unit == "#" else MONEY
        c.font = f(9, True, F.LINK_FONT)
        r += 1

    ch = LineChart()
    ch.title = "Monthly revenue against total expenses"
    ch.height, ch.width = 7.5, 17
    for sheet, row in ((wb["Total Revenue"], R["tot"]["total"]),
                       (wb["Expenses"], R["exp"]["total_expenses"])):
        data = Reference(sheet, min_col=mcol(1), max_col=mcol(F.MONTHS),
                         min_row=row, max_row=row)
        ch.add_data(data, titles_from_data=False, from_rows=True)
    ch.y_axis.numFmt = '$#,##0'
    ws.add_chart(ch, f"A{anchor}")

    ch2 = LineChart()
    ch2.title = "Cash balance, month by month"
    ch2.height, ch2.width = 7.5, 17
    data = Reference(wb["Cash Flow Statement"], min_col=mcol(1),
                     max_col=mcol(F.MONTHS), min_row=R["cf"]["cash"],
                     max_row=R["cf"]["cash"])
    ch2.add_data(data, titles_from_data=False, from_rows=True)
    ch2.y_axis.numFmt = '$#,##0'
    ws.add_chart(ch2, f"F{anchor}")
    return ws


def build_market(wb):
    ws = annual_sheet(wb, "Market Research", "Market Research",
                      "Where the demand already exists. These are named "
                      "targets, not signed partners, except the five "
                      "memoranda, which are signed.",
                      widths=(44, 16, 62, 22, 26), last_col=6)
    r = band(ws, 5, "SIGNED AND NEAR SIGNED", last_col=6)
    for i, t in enumerate(["Institution", "Status", "Detail",
                           "Cohorts planned in year one"]):
        c = ws.cell(r, 1 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
    r += 1
    for name, status, detail, y1 in P.SIGNED_INSTITUTIONS:
        ws.cell(r, 1, name).font = f(9, True)
        ws.cell(r, 2, status).font = f(8.5, False, F.UV)
        ws.cell(r, 3, detail).font = f(8.5, False, F.INK2)
        c = ws.cell(r, 4, y1)
        c.number_format = NUM
        c.font = f(9, True, F.LINK_FONT)
        r += 1
    r += 1
    r = band(ws, r, "NAMED PROGRAMMES THE ENGINES ATTACH TO", last_col=6)
    for i, t in enumerate(["Programme", "Market", "What it already runs",
                           "Cadence", "What StartPad supplies"]):
        c = ws.cell(r, 1 + i, t)
        c.font = f(8.5, True, F.WHITE)
        c.fill = fill(F.UV_DARK)
    r += 1
    progs = [
        ("Rowad 2030, One Million Entrepreneurs", "Egypt",
         "Ministry of Planning. A three stage online curriculum with the "
         "Rowad Meter platform; universities including Alexandria fund seats.",
         "Running to 2030", "Seats, then trainer certification"),
        ("MSMEDA governorate programme", "Egypt",
         "Service centres across the governorates.", "Continuous",
         "Seats and certification"),
        ("Central Bank of Egypt, FinYology", "Egypt",
         "More than thirty universities; FinTech Got Talent is its showcase.",
         "Annual, academic year", "Build cohorts, then the season"),
        ("Enactus Egypt National Competition", "Egypt",
         "Thirty to thirty five university teams in the national final. "
         "Orange Egypt has sponsored it for seventeen years.",
         "Annual season, 4 to 5 months", "Platform and build cohorts"),
        ("INJAZ Egypt, Company Program", "Egypt and the Arab region",
         "A six month student venture programme with school and university "
         "tracks, feeding INJAZ Al Arab.", "6 months per cycle",
         "Delivery partner licence"),
        ("Startup Teen, iSchool", "Egypt",
         "Ages 13 to 18. First edition drew 800 students from 40 schools.",
         "Annual season", "School variant training track"),
        ("Egypt Entrepreneurship Rally", "Egypt",
         "Run with AASTMT, sponsored by the National Bank of Egypt since "
         "2019.", "Annual", "Platform and the sponsor's report"),
        ("Rowad Domiat", "Egypt",
         "Run by the ILO with ICSB, backed by Methanex Egypt, on the ILO "
         "Start and Improve Your Business methodology.", "Annual",
         "Platform and the ILO mapping"),
        ("Monsha'at Academy", "KSA",
         "More than two hundred training events, with no build stage after "
         "them.", "Continuous catalogue", "Capstone cohorts, then seats"),
        ("Misk Foundation and the MISK SDG competition", "KSA",
         "Youth education and entrepreneurship since 2011; the SDG "
         "competition runs with UNDP.", "Annual",
         "Cohorts, platform, programmes"),
        ("TVTC", "KSA",
         "336,150 trainees across 314 institutions in 2024, under a Vision "
         "2030 mandate.", "Academic year", "Trainer certification at scale"),
        ("Hadaf and the Social Development Bank", "KSA",
         "Subsidised training and finance with per beneficiary funding in "
         "place.", "Continuous", "Seat rider as a screening instrument"),
    ]
    for i, row in enumerate(progs):
        for j, v in enumerate(row):
            c = ws.cell(r, 1 + j, v)
            c.font = f(8.5, j == 0, F.INK if j == 0 else F.INK2)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        if i % 2 == 0:
            for j in range(1, 6):
                ws.cell(r, j).fill = fill(F.WASH)
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1
    c = ws.cell(r, 1, "No revenue in this model is attributed to any one of "
                      "these. They are listed so the demand can be checked "
                      "rather than taken on trust.")
    c.font = f(8.5, False, F.MUTED, italic=True)
    return ws


# =====================================================================
#  ASSEMBLY
# =====================================================================
CONTENTS = [
    ("Cover", "This page: what the model is and how to read it"),
    ("Summary", "The whole model on one page, with charts"),
    ("Market Research", "Signed institutions and the named programmes"),
    ("Input>>", "Everything typed is here and nowhere else"),
    ("Assumption Setting", "In the order the model runs: basis, traction, "
                           "acquisition, what a won contract becomes, "
                           "pricing, expenses, working capital, tax, "
                           "assets"),
    ("Capital Expenditure", "Assets driven by new hires, plus shared and "
                            "intangible assets"),
    ("Actuals", "The opening position and a grid to record each month"),
    ("Process>>", "Where the inputs become the model"),
    ("Acquisitions", "Activity to leads to contracts to the contract book, sixty months"),
    ("GTM Capacity and Timing", "Who runs the activity, whether there are "
                                "enough of them, and how long a deal takes "
                                "to become a delivery day"),
    ("Revenue Streams", "Thirteen engines, every one of them an output of the contract book"),
    ("Total Revenue", "Gathered into four families"),
    ("Payroll", "Fifteen roles, monthly, capped at 6, 9, 12, 16 and 20"),
    ("Depreciation and Amortization", "Straight line by asset class"),
    ("Expenses", "Direct cost, revenue share to three parties, operating "
                 "cost, and the year one total it produces"),
    ("Output>>", "The three statements"),
    ("Income Statement", "Five years to 30 September"),
    ("Balance Sheet", "Five years, with the balance check"),
    ("Cash Flow Statement", "Monthly working and the annual statement"),
    ("Financial Indicators", "Growth, profitability, unit economics, cash"),
    ("Analysis>>", "What the model is tested against"),
    ("BEP Analysis", "Break even revenue and the month it turns"),
    ("PB Analysis", "When the capital comes back, base and flexed"),
    ("Sensitivity", "Three two way grids on the year five result"),
    ("Stress Test", "Four scenarios on volume, price, cost and collection"),
    ("Exit Angel and VC", "Angel and venture returns, and the routes out"),
]

ORDER = [n for n, _ in CONTENTS]

FORBIDDEN = {"—": "em dash", "–": "en dash", "·": "middot",
             "‘": "curly quote", "’": "curly quote",
             "“": "curly quote", "”": "curly quote",
             "…": "ellipsis"}


def check_characters(wb):
    """
    No typographic marks that read as machine written.

    The founder asked for these out of the workbook, so this is a build gate
    rather than something to watch for by eye: the build fails if one appears
    in any cell on any sheet.
    """
    found = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str):
                    for ch, name in FORBIDDEN.items():
                        if ch in cell.value:
                            found.append(f"{ws.title}!{cell.coordinate} "
                                         f"contains a {name}")
    return found


def build():
    wb = Workbook()
    wb.remove(wb.active)
    build_assumptions(wb)
    build_payroll(wb)
    build_capex(wb)
    build_depreciation(wb)
    build_revenue(wb)
    build_acquisitions(wb)
    finish_revenue(wb)
    build_gtm(wb)
    build_total_revenue(wb)
    build_expenses(wb)
    build_income_statement(wb)
    build_cash_flow(wb)
    build_actuals(wb)
    build_balance_sheet(wb)
    build_indicators(wb)
    build_bep(wb)
    build_payback(wb)
    build_sensitivity(wb)
    build_stress(wb)
    build_exit(wb)
    build_market(wb)
    build_summary(wb)
    build_cover(wb, CONTENTS)
    divider(wb, "Input>>", "Input",
            [(n, b) for n, b in CONTENTS[4:7]])
    divider(wb, "Process>>", "Process",
            [(n, b) for n, b in CONTENTS[8:15]])
    divider(wb, "Output>>", "Output",
            [(n, b) for n, b in CONTENTS[16:20]])
    divider(wb, "Analysis>>", "Analysis",
            [(n, b) for n, b in CONTENTS[21:]])
    wb._sheets = [wb[n] for n in ORDER]
    wb.active = 0
    return wb


if __name__ == "__main__":
    wb = build()
    bad = check_characters(wb)
    if bad:
        print("BUILD FAILED, forbidden characters:")
        for b in bad[:20]:
            print("  ", b)
        sys.exit(1)
    out = os.path.join(ROOT, "output", "StartPad_Financial_Model.xlsx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wb.save(out)
    print(f"wrote {out} ({os.path.getsize(out) / 1024:,.0f} KB, "
          f"{len(wb.sheetnames)} sheets)")
