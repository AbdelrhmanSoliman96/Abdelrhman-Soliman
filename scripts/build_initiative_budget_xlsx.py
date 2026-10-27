"""Build the 360 budget for One Million First-Time Founders."""
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from outreach import initiative as I                            # noqa: E402
from scripts._determinism import FIXED_TIMESTAMP, normalize_zip  # noqa: E402
from scripts.build_prospects_xlsx import (                      # noqa: E402
    ACCENT, BOX, CONF_FILL, CONF_FONT, HEAD, INK, SUBHEAD, SUNK, banner,
    prose,
)

MONEY = '"$"#,##0'
MONEY2 = '"$"#,##0.00'
EGP = '#,##0'


def row_head(ws, r, heads, widths, start=2):
    for i, (h, w) in enumerate(zip(heads, widths)):
        c = ws.cell(row=r, column=start + i, value=h)
        c.font = Font(bold=True, size=10, color="FFFFFF")
        c.fill = SUBHEAD
        c.border = BOX
        c.alignment = Alignment(vertical="center", indent=1, wrap_text=True)
        ws.column_dimensions[get_column_letter(start + i)].width = w
    ws.row_dimensions[r].height = 28
    return r + 1


def put(ws, r, col, value, fmt=None, bold=False, colour=INK, centre=False,
        wrap=False, size=10, fill=None):
    c = ws.cell(row=r, column=col, value=value)
    c.font = Font(size=size, bold=bold, color=colour)
    c.border = BOX
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    c.alignment = Alignment(horizontal="center" if centre else "left",
                            vertical="top", wrap_text=wrap,
                            indent=0 if centre else 1)
    return c


def total_row(ws, r, label, cells, start=2):
    t = ws.cell(row=r, column=start, value=label)
    t.font = Font(size=10, bold=True, color="FFFFFF")
    t.fill = HEAD
    t.alignment = Alignment(indent=1)
    for col, (value, fmt) in cells.items():
        c = ws.cell(row=r, column=col, value=value)
        c.font = Font(size=10, bold=True, color="FFFFFF")
        c.fill = HEAD
        c.number_format = fmt
        c.alignment = Alignment(horizontal="center")
    return r + 1


# ------------------------------------------------------------------ READ ME
def sheet_readme(wb):
    ws = wb.create_sheet("READ ME FIRST")
    ws.sheet_view.showGridLines = False
    income, lines = I.budget()
    f = dict((k, v) for k, v, _ in I.funnel())
    ret = sum(v for _, v, _ in I.startpad_return())
    inv = sum(v for _, v, _ in I.STARTPAD_INVESTMENT)
    banner(ws, f"{I.NAME}: the whole budget",
           f"{I.WAVE}. Every line, in dollars and in pounds, and what "
           f"StartPad gets back.", 5)
    ws.column_dimensions["B"].width = 32
    ws.column_dimensions["C"].width = 106

    blocks = [
        ("THE TWO PRICES EVERYTHING IS BUILT ON", ""),
        ("", f"A sponsored founder costs ${I.SEAT_PRICE:,.2f}. That is the "
             f"national initiative seat price in the company's financial "
             f"model, year one, described there as priced for a ministry "
             f"buying tens of thousands. It is an Egyptian price and the "
             f"cost base is sized for it."),
        ("", f"An in-person cohort costs ${I.COHORT_PRICE:,.0f} for "
             f"{I.COHORT_SEATS} seats, which is "
             f"${I.COHORT_PRICE / I.COHORT_SEATS:,.0f} a seat. The "
             f"financial model's direct cost for the same cohort is $1,770. "
             f"The difference is the field: getting two facilitators and a "
             f"coordinator to the governorate and keeping them there for "
             f"eight days, which is ${I.field_cost():,.0f} of every cohort "
             f"and is the line a budget written in Cairo leaves out."),
        ("", ""),
        ("THE SHEETS", ""),
        ("THE 360 BUDGET", "Income and every expenditure line, in dollars "
                           "and pounds. It balances to the cent, because "
                           "programme management is the balancing line."),
        ("WHAT A SEAT BUYS", "The $5, divided back into the budget lines it "
                             "came from."),
        ("WHAT A COHORT COSTS", "All eleven lines of the $3,000, with the "
                                "six field lines marked, checked against "
                                "the financial model's own direct cost."),
        ("EVENTS", "Every event the initiative runs, what each costs and "
                   "when. The cohorts are not here; they are the delivery "
                   "line."),
        ("THE FUNNEL", "Reach to registered to completed to sponsored to "
                       "trading, with the conversion rate behind each step."),
        ("SPEND BY MONTH", "When the money actually leaves, which is not "
                           "evenly."),
        ("RETURN ON STARTPAD", "What the company puts in that the budget "
                               "does not pay for, and what comes back in "
                               "the twelve months after the wave."),
        ("SENSITIVITY", "What happens at 30, 50, 75 and 100 per cent "
                        "coalition fill."),
        ("", ""),
        ("THE HEADLINE", ""),
        ("", f"At {I.TARGET_FILL:.0%} coalition fill the wave raises and "
             f"spends ${income:,.0f}, which is EGP {I.egp(income):,.0f}. It "
             f"sponsors {f['Sponsored full journeys, all 15 missions']:,.0f} "
             f"founders through all fifteen missions and runs "
             f"{f['Cohorts run']:,.0f} in-person cohorts in twelve "
             f"governorates."),
        ("", f"StartPad takes no margin from sponsorship in wave one. Every "
             f"dollar raised is in the budget. The company's own return is "
             f"${ret:,.0f} in the twelve months after the wave, against "
             f"${inv:,.0f} it puts in that the budget does not pay for, "
             f"which is {ret / inv:,.1f} times. That is on the RETURN ON "
             f"STARTPAD sheet, priced at the financial model's own prices "
             f"rather than at numbers invented here."),
        ("", ""),
        ("WHAT IS NOT IN THIS BUDGET", ""),
        ("In-kind", "Valued separately and never counted as cash. A "
                    "donated venue takes $260 off a cohort and that saving "
                    "goes back into founders sponsored, not into the "
                    "surplus."),
        ("The platform itself", "Already built and carried by the company. "
                                "The budget pays for hosting, inference and "
                                "the initiative-specific work, not for the "
                                "product."),
        ("Wave 2", "A separate budget, and cheaper per founder, because the "
                   "facilitator pool and the chapters will already exist."),
        ("", ""),
        ("A WARNING ABOUT THESE NUMBERS", ""),
        ("", "Nothing here is a measured result. Every quantity is an "
             "assumption with its driver written next to it, and the "
             "initiative has not run. The conversion rates on the FUNNEL "
             "sheet and the return rates on the RETURN sheet are the two "
             "places where being wrong costs the most, and both are stated "
             "so they can be argued with."),
    ]
    prose(ws, blocks, wrap_at=103)
    return ws


# ------------------------------------------------------------ THE 360 BUDGET
def sheet_budget(wb):
    ws = wb.create_sheet("THE 360 BUDGET")
    ws.sheet_view.showGridLines = False
    income, lines = I.budget()
    f = dict((k, v) for k, v, _ in I.funnel())
    banner(ws, f"The whole wave, in and out",
           f"{I.WAVE}, at {I.TARGET_FILL:.0%} coalition fill. The "
           f"percentage column is a formula, so edit a line and the shares "
           f"move.", 7)
    ws.column_dimensions["A"].width = 3

    r = 4
    ws.cell(row=r, column=2, value="INCOME").font = Font(bold=True, size=11,
                                                          color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Source", "Quantity", "Unit", "USD", "EGP",
                         "Note"], [40, 12, 12, 14, 16, 60])
    first = r
    founders, cohorts = I.bought()
    for label, qty, unit, note in [
        ("Sponsored founders", founders, I.SEAT_PRICE,
         "Founding, Lead, Governorate and Mission partners, at "
         f"{I.TARGET_FILL:.0%} of the capped slots"),
        ("In-person cohorts", cohorts, I.COHORT_PRICE,
         "Funded inside the Founding, Lead and Governorate tiers"),
    ]:
        put(ws, r, 2, label, bold=True)
        put(ws, r, 3, qty, "#,##0", centre=True)
        put(ws, r, 4, unit, MONEY2 if unit < 100 else MONEY, centre=True)
        put(ws, r, 5, f"=C{r}*D{r}", MONEY, centre=True)
        put(ws, r, 6, f"=E{r}*{I.EGP_PER_USD}", EGP, centre=True)
        put(ws, r, 7, note, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(22, 12.4 * (len(note) // 58 + 1))
        r += 1
    r = total_row(ws, r, "Total income",
                  {5: (f"=SUM(E{first}:E{r-1})", MONEY),
                   6: (f"=SUM(F{first}:F{r-1})", EGP)})
    income_row = r - 1
    r += 1

    ws.cell(row=r, column=2, value="EXPENDITURE").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Line", "Share", "", "USD", "EGP", "What it is"],
                 [40, 12, 12, 14, 16, 60])
    first = r
    for label, value, note in lines:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, f"=E{r}/$E${income_row}", "0.0%", centre=True)
        put(ws, r, 4, "")
        put(ws, r, 5, value, MONEY, centre=True)
        put(ws, r, 6, f"=E{r}*{I.EGP_PER_USD}", EGP, centre=True)
        put(ws, r, 7, note, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(26, 12.4 * (len(note) // 58 + 1))
        r += 1
    r = total_row(ws, r, "Total expenditure",
                  {3: (f"=SUM(C{first}:C{r-1})", "0.0%"),
                   5: (f"=SUM(E{first}:E{r-1})", MONEY),
                   6: (f"=SUM(F{first}:F{r-1})", EGP)})
    spend_row = r - 1
    r += 1

    put(ws, r, 2, "Surplus or deficit", bold=True)
    put(ws, r, 5, f"=E{income_row}-E{spend_row}", MONEY, centre=True,
        bold=True, fill=SUNK)
    put(ws, r, 6, f"=F{income_row}-F{spend_row}", EGP, centre=True,
        bold=True, fill=SUNK)
    put(ws, r, 7, "Nil by design. StartPad takes no margin from "
                  "sponsorship in wave one, and programme management is "
                  "the balancing line.", wrap=True, size=9.5,
        colour="3A4050")
    ws.row_dimensions[r].height = 30
    r += 2

    ws.cell(row=r, column=2, value="WHAT IT WORKS OUT AT").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Measure", "USD", "EGP", "", "", "Note"],
                 [40, 12, 14, 2, 2, 78])
    for label, value in I.unit_costs():
        put(ws, r, 2, label, bold=True)
        put(ws, r, 3, round(value, 2), MONEY2, centre=True,
            colour=ACCENT, bold=True)
        put(ws, r, 4, round(value * I.EGP_PER_USD, 2), "#,##0.00",
            centre=True)
        r += 1
    r += 1
    note = ("The sponsored founder and the in-person seat are prices, not "
            "averages: they are what a partner pays and what the wave "
            "spends, and they are equal because the wave takes no margin. "
            "The other four are the total budget divided by an outcome, "
            "which is the form a partner's finance function asks for.")
    c = ws.cell(row=r, column=2, value=note)
    c.font = Font(size=9.5, italic=True, color="6B7A74")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    ws.row_dimensions[r].height = 44
    return ws


# --------------------------------------------------------- WHAT A SEAT BUYS
def sheet_seat(wb):
    ws = wb.create_sheet("WHAT A SEAT BUYS")
    ws.sheet_view.showGridLines = False
    income, lines = I.budget()
    founders, cohorts = I.bought()
    banner(ws, f"The ${I.SEAT_PRICE:,.2f} a sponsored founder costs",
           "Not a price somebody chose. The budget minus the cohorts, "
           "divided by the founders sponsored.", 6)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["Budget line", "USD total", "Per founder",
                         "EGP per founder", "Share"],
                 [44, 16, 14, 16, 10])
    first = r
    delivery = cohorts * I.COHORT_PRICE
    for label, value, _ in lines:
        if label.startswith("Delivery"):
            continue
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, MONEY, centre=True)
        put(ws, r, 4, f"=C{r}/{founders}", MONEY2, centre=True,
            colour=ACCENT, bold=True)
        put(ws, r, 5, f"=D{r}*{I.EGP_PER_USD}", "#,##0.00", centre=True)
        put(ws, r, 6, f"=C{r}/({income}-{delivery})", "0.0%", centre=True)
        ws.row_dimensions[r].height = 24
        r += 1
    r = total_row(ws, r, f"Per sponsored founder",
                  {3: (f"=SUM(C{first}:C{r-1})", MONEY),
                   4: (f"=SUM(D{first}:D{r-1})", MONEY2),
                   5: (f"=SUM(E{first}:E{r-1})", "#,##0.00"),
                   6: (f"=SUM(F{first}:F{r-1})", "0.0%")})
    r += 1
    for text in [
        f"The {founders:,.0f} sponsored founders are the ones the coalition "
        f"pays to carry through all fifteen missions. The platform line "
        f"covers hosting and inference for the whole registered base of "
        f"198,000, not only for them, which is why the free tier costs the "
        f"initiative almost nothing per head.",
        f"At ${I.SEAT_PRICE:,.2f} a founder this is below the "
        f"${I.PRICE_PRO:,.0f} a year a student pays for Pro. That is bulk "
        f"provisioning, and it is the same logic the financial model "
        f"already applies to a ministry buying tens of thousands of seats.",
    ]:
        c = ws.cell(row=r, column=2, value=text)
        c.font = Font(size=9.5, italic=True, color="6B7A74")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
        ws.row_dimensions[r].height = 42
        r += 1
    return ws


# ------------------------------------------------------ WHAT A COHORT COSTS
def sheet_cohort(wb):
    ws = wb.create_sheet("WHAT A COHORT COSTS")
    ws.sheet_view.showGridLines = False
    banner(ws, f"The ${I.COHORT_PRICE:,.0f} in-person cohort, line by line",
           f"{I.COHORT_SEATS} seats, six delivery days, two certified "
           f"facilitators and a coordinator, in a governorate that is not "
           f"theirs.", 6)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["Line", "USD", "EGP", "Per seat", "Field?",
                         "Note"], [44, 12, 14, 12, 10, 56])
    first = r
    for label, value, note in I.COHORT_BREAKDOWN:
        field = label in I.FIELD_LINES
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, MONEY, centre=True)
        put(ws, r, 4, f"=C{r}*{I.EGP_PER_USD}", EGP, centre=True)
        put(ws, r, 5, f"=C{r}/{I.COHORT_SEATS}", MONEY2, centre=True)
        c = put(ws, r, 6, "Field" if field else "", centre=True)
        if field:
            c.fill = CONF_FILL["medium"]
            c.font = CONF_FONT["medium"]
        put(ws, r, 7, note, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(22, 12.4 * (len(note) // 54 + 1))
        r += 1
    r = total_row(ws, r, "Total per cohort",
                  {3: (f"=SUM(C{first}:C{r-1})", MONEY),
                   4: (f"=SUM(D{first}:D{r-1})", EGP),
                   5: (f"=SUM(E{first}:E{r-1})", MONEY2)})
    r += 1

    direct = sum(v for k, v, n in I.COHORT_BREAKDOWN
                 if n.startswith("In the financial model"))
    field = I.field_cost()
    for label, value, note in [
        ("Of which direct cost, in the financial model", direct,
         "Facilitation, materials and the showcase. The same $1,770 the "
         "business plan carries for a university cohort, unchanged."),
        ("Of which field operations", field,
         "Transport, accommodation, the daily allowance, local transport, "
         "shipping and the venue where the host does not donate one. This "
         "is the line that decides whether a governorate programme "
         "happens."),
        ("Of which everything else", I.COHORT_PRICE - direct - field,
         "Certification and quality assurance, cohort reporting and "
         "contingency."),
    ]:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, MONEY, centre=True, colour=ACCENT, bold=True)
        put(ws, r, 4, round(I.egp(value)), EGP, centre=True)
        put(ws, r, 5, f"={value}/{I.COHORT_PRICE}", "0.0%", centre=True)
        put(ws, r, 7, note, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(note) // 54 + 1))
        r += 1
    r += 1

    ws.cell(row=r, column=2, value="THE FIELD RULES").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    for head, body in I.FIELD_POLICY:
        put(ws, r, 2, head, bold=True, wrap=True, colour=ACCENT)
        c = ws.cell(row=r, column=3, value=body)
        c.font = Font(size=9.8)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=7)
        ws.row_dimensions[r].height = max(24, 12.4 * (len(body) // 100 + 1))
        r += 1
    r += 1
    note = (f"A commercial university cohort sells for "
            f"${I.PRICE_UNI_COHORT:,.0f} in the financial model. A sponsored "
            f"one costs ${I.COHORT_PRICE:,.0f} because there is no margin "
            f"in it and no institutional reporting layer, and because the "
            f"host is asked for the room. Where the room is donated, $260 "
            f"goes back into founders sponsored rather than into a surplus.")
    c = ws.cell(row=r, column=2, value=note)
    c.font = Font(size=9.5, italic=True, color="6B7A74")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    ws.row_dimensions[r].height = 44
    return ws


# ------------------------------------------------------------------ EVENTS
def sheet_events(wb):
    ws = wb.create_sheet("EVENTS")
    ws.sheet_view.showGridLines = False
    banner(ws, "Every event the initiative runs",
           "The cohorts are not here: they are the delivery line. These are "
           "the events around them.", 7)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["Event", "How many", "Each", "USD", "EGP", "When",
                         "What it is for"],
                 [34, 11, 12, 13, 15, 22, 48])
    first = r
    for label, count, cost, when, why in I.EVENTS:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, count, "#,##0", centre=True)
        put(ws, r, 4, cost, MONEY, centre=True)
        put(ws, r, 5, f"=C{r}*D{r}", MONEY, centre=True, colour=ACCENT,
            bold=True)
        put(ws, r, 6, f"=E{r}*{I.EGP_PER_USD}", EGP, centre=True)
        put(ws, r, 7, when, centre=True, size=9.5)
        put(ws, r, 8, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(26, 12.4 * (len(why) // 46 + 1))
        r += 1
    r = total_row(ws, r, "Total events and field activation",
                  {5: (f"=SUM(E{first}:E{r-1})", MONEY),
                   6: (f"=SUM(F{first}:F{r-1})", EGP)})
    r += 1
    f = dict((k, v) for k, v, _ in I.funnel())
    for text in [
        f"That is ${I.events_total() / f['Sponsored full journeys, all 15 missions']:,.2f} "
        f"of every sponsored founder's ${I.SEAT_PRICE:,.2f}, and it is the "
        f"second largest line in the whole budget after delivery. It is "
        f"also the line most likely to be cut by somebody reading quickly, "
        f"which would be a mistake: a chapter that has been visited "
        f"activates and a chapter that has only been emailed does not.",
        f"In addition to these, {f['Cohorts run']:,.0f} in-person cohorts "
        f"each end with their own showcase for the participants and the "
        f"host institution. Those sit inside the "
        f"${I.COHORT_PRICE:,.0f} cohort cost, not here.",
    ]:
        c = ws.cell(row=r, column=2, value=text)
        c.font = Font(size=9.5, italic=True, color="6B7A74")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8)
        ws.row_dimensions[r].height = 46
        r += 1
    return ws


# -------------------------------------------------------------- THE FUNNEL
def sheet_funnel(wb):
    ws = wb.create_sheet("THE FUNNEL")
    ws.sheet_view.showGridLines = False
    banner(ws, "Reach to registered to sponsored to trading",
           "The free tier is driven by reach, because it costs almost "
           "nothing a head. Everything below it is driven by the budget, "
           "because it does not.", 6)
    ws.column_dimensions["A"].width = 3
    r = 4
    ws.cell(row=r, column=2, value="WHERE THE REACH COMES FROM").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    r = row_head(ws, r, ["Channel", "Partners", "Reach each", "Register",
                         "Reached", "Why"],
                 [30, 11, 13, 11, 14, 60])
    first = r
    for label, num, per, rate, why in I.CHANNELS:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, num, "#,##0", centre=True)
        put(ws, r, 4, per, "#,##0", centre=True)
        put(ws, r, 5, rate, "0%", centre=True)
        put(ws, r, 6, f"=C{r}*D{r}", "#,##0", centre=True, bold=True,
            colour=ACCENT)
        put(ws, r, 7, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(why) // 58 + 1))
        r += 1
    r = total_row(ws, r, "Total reached",
                  {6: (f"=SUM(F{first}:F{r-1})", "#,##0")})
    r += 1

    ws.cell(row=r, column=2, value="THE FUNNEL").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Stage", "Wave 1", "", "", "", "What it means"],
                 [30, 14, 2, 2, 2, 86])
    for label, value, why in I.funnel():
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, round(value), "#,##0", centre=True, bold=True,
            colour=ACCENT, size=11)
        put(ws, r, 7, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(22, 12.4 * (len(why) // 84 + 1))
        r += 1
    r += 1

    ws.cell(row=r, column=2, value="THE RATES, AND WHY EACH ONE").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    r = row_head(ws, r, ["Rate", "Assumed", "", "", "", "Why"],
                 [30, 14, 2, 2, 2, 86])
    for label, value, why in I.RATES:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, "0%", centre=True, bold=True, colour=ACCENT)
        put(ws, r, 7, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(22, 12.4 * (len(why) // 84 + 1))
        r += 1
    return ws


# ----------------------------------------------------------- SPEND BY MONTH
# When the money leaves. Front-loaded, because the launch, the content and
# most of the chapter activation happen before a single cohort runs.
SPEND_SHAPE = {
    "Delivery": (0.05, 0.31, 0.07, 0.26, 0.31, 0.00),
    "Events and field": (0.34, 0.18, 0.10, 0.08, 0.14, 0.16),
    "Platform": (0.17, 0.17, 0.17, 0.17, 0.16, 0.16),
    "Content": (0.45, 0.20, 0.10, 0.10, 0.10, 0.05),
    "Measurement": (0.10, 0.05, 0.20, 0.05, 0.10, 0.50),
    "Management": (0.17, 0.17, 0.17, 0.17, 0.16, 0.16),
}


def sheet_months(wb):
    ws = wb.create_sheet("SPEND BY MONTH")
    ws.sheet_view.showGridLines = False
    income, lines = I.budget()
    banner(ws, "When the money actually leaves",
           "Not evenly. The launch, the content and most of the chapter "
           "activation happen before a single cohort runs, which is a "
           "cash-flow problem as much as a budget one.", 9)
    ws.column_dimensions["A"].width = 3
    heads = ["Line"] + [f"{m[0]}\n{m[1].split()[0]}" for m in I.MONTHS] \
        + ["Total"]
    r = 4
    r = row_head(ws, r, heads, [34] + [12] * 6 + [14])
    first = r
    keys = list(SPEND_SHAPE)
    for (label, value, _), key in zip(lines, keys):
        put(ws, r, 2, label, bold=True, wrap=True)
        for i in range(6):
            put(ws, r, 3 + i, value * SPEND_SHAPE[key][i], MONEY,
                centre=True)
        put(ws, r, 9, f"=SUM(C{r}:H{r})", MONEY, centre=True, bold=True,
            colour=ACCENT)
        ws.row_dimensions[r].height = 26
        r += 1
    cells = {3 + i: (f"=SUM({get_column_letter(3+i)}{first}:"
                     f"{get_column_letter(3+i)}{r-1})", MONEY)
             for i in range(6)}
    cells[9] = (f"=SUM(I{first}:I{r-1})", MONEY)
    r = total_row(ws, r, "Total spend", cells)
    put(ws, r, 2, "Cumulative", bold=True)
    for i in range(6):
        col = get_column_letter(3 + i)
        ref = f"=SUM($C${r-1}:{col}{r-1})"
        put(ws, r, 3 + i, ref, MONEY, centre=True, fill=SUNK)
    r += 2
    note = (f"Sponsorship is invoiced on signature, not on delivery. With "
            f"roughly a third of the events budget spent in month one and "
            f"the content budget before that, the coalition has to be "
            f"signed and at least half invoiced before the launch. That is "
            f"why the pre-wave months in the framework run from October "
            f"2026 and why nothing is announced until three Founding "
            f"Partners have signed.")
    c = ws.cell(row=r, column=2, value=note)
    c.font = Font(size=9.5, italic=True, color="6B7A74")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=9)
    ws.row_dimensions[r].height = 46
    return ws


# ------------------------------------------------------- RETURN ON STARTPAD
def sheet_return(wb):
    ws = wb.create_sheet("RETURN ON STARTPAD")
    ws.sheet_view.showGridLines = False
    inv = sum(v for _, v, _ in I.STARTPAD_INVESTMENT)
    ret = I.startpad_return()
    total = sum(v for _, v, _ in ret)
    banner(ws, "What the company puts in, and what comes back",
           "Wave 1 takes no margin from sponsorship. The return is "
           "somewhere else, and it is priced at the financial model's own "
           "prices.", 6)
    ws.column_dimensions["A"].width = 3

    r = 4
    ws.cell(row=r, column=2,
            value="WHAT STARTPAD PUTS IN, THAT THE BUDGET DOES NOT PAY "
                  "FOR").font = Font(bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Line", "USD", "EGP", "", "What it is"],
                 [36, 13, 15, 2, 74])
    first = r
    for label, value, note in I.STARTPAD_INVESTMENT:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, MONEY, centre=True)
        put(ws, r, 4, f"=C{r}*{I.EGP_PER_USD}", EGP, centre=True)
        put(ws, r, 6, note, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(note) // 72 + 1))
        r += 1
    r = total_row(ws, r, "Total invested",
                  {3: (f"=SUM(C{first}:C{r-1})", MONEY),
                   4: (f"=SUM(D{first}:D{r-1})", EGP)})
    inv_row = r - 1
    r += 1

    ws.cell(row=r, column=2,
            value="WHAT COMES BACK IN THE TWELVE MONTHS AFTER THE "
                  "WAVE").font = Font(bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Line", "USD", "EGP", "", "How it is counted"],
                 [36, 13, 15, 2, 74])
    first = r
    for label, value, note in ret:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, MONEY, centre=True, colour=ACCENT, bold=True)
        put(ws, r, 4, f"=C{r}*{I.EGP_PER_USD}", EGP, centre=True)
        put(ws, r, 6, note, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(note) // 72 + 1))
        r += 1
    r = total_row(ws, r, "Total return",
                  {3: (f"=SUM(C{first}:C{r-1})", MONEY),
                   4: (f"=SUM(D{first}:D{r-1})", EGP)})
    ret_row = r - 1
    r += 1
    put(ws, r, 2, "Return on what the company put in", bold=True)
    put(ws, r, 3, f"=C{ret_row}/C{inv_row}", "0.0x", centre=True,
        bold=True, colour=ACCENT, fill=SUNK, size=12)
    put(ws, r, 6, "And this counts only what can be priced. The assets "
                  "below are worth more and are not in the number.",
        wrap=True, size=9.5, colour="3A4050")
    ws.row_dimensions[r].height = 28
    r += 2

    ws.cell(row=r, column=2, value="THE RATES BEHIND THOSE LINES").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    r = row_head(ws, r, ["Rate", "Assumed", "", "", "Why"],
                 [36, 13, 2, 2, 89])
    for label, value, why in I.RETURN_RATES:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, "0%", centre=True, bold=True, colour=ACCENT)
        put(ws, r, 6, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(why) // 87 + 1))
        r += 1
    r += 1

    ws.cell(row=r, column=2, value="AND WHAT IS NOT IN THE NUMBER").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    for head, body in I.startpad_assets():
        put(ws, r, 2, head, bold=True, wrap=True, colour=ACCENT)
        c = ws.cell(row=r, column=3, value=body)
        c.font = Font(size=9.8)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
        ws.row_dimensions[r].height = max(26, 12.4 * (len(body) // 100 + 1))
        r += 1
    r += 1
    note = (f"The honest summary: the initiative is cash neutral for "
            f"StartPad in wave one by design, costs the company about "
            f"${inv:,.0f} of time and engineering it does not recover, and "
            f"returns about ${total:,.0f} of commercial revenue in the "
            f"following twelve months plus a facilitator pool, a data asset "
            f"and a delivery record that no amount of selling would have "
            f"bought. If the return rates on this sheet are half right it "
            f"is still worth doing.")
    c = ws.cell(row=r, column=2, value=note)
    c.font = Font(size=10, italic=True, color=INK)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
    ws.row_dimensions[r].height = 56
    return ws


# ------------------------------------------------------------- SENSITIVITY
def sheet_sensitivity(wb):
    ws = wb.create_sheet("SENSITIVITY")
    ws.sheet_view.showGridLines = False
    banner(ws, "What happens if the coalition does not fill",
           "The wave is planned at 50 per cent. This is what the other "
           "outcomes look like.", 8)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["Coalition fill", "Raised USD", "Raised EGP",
                         "Founders sponsored", "Cohorts", "Governorates",
                         "Cost per founder", "What it means"],
                 [13, 14, 16, 16, 10, 13, 14, 48])
    for fill in (0.30, 0.50, 0.75, 1.00):
        founders, cohorts = I.bought(fill)
        income, _ = I.budget(fill)
        govs = max(4, min(12, round(cohorts / 2.5)))
        meaning = {
            0.30: "Thin but real. The governorate count drops, not the "
                  "quality, and the wave still produces a closing report "
                  "worth showing.",
            0.50: "The plan. Twelve governorates, and the number every "
                  "other sheet in this file is quoted at.",
            0.75: "Comfortable. The extra buys governorates and "
                  "facilitator certification rather than more Cairo.",
            1.00: "The money outruns the funnel: the coalition could "
                  "sponsor more founders than finish the free tier. That "
                  "is a good problem, and the answer is to widen reach in "
                  "wave two rather than to raise more.",
        }[fill]
        put(ws, r, 2, f"{fill:.0%}", centre=True, bold=True,
            colour=ACCENT, size=12)
        put(ws, r, 3, income, MONEY, centre=True)
        put(ws, r, 4, round(I.egp(income)), EGP, centre=True)
        put(ws, r, 5, round(founders), "#,##0", centre=True)
        put(ws, r, 6, round(cohorts), "#,##0", centre=True)
        put(ws, r, 7, govs, "#,##0", centre=True)
        put(ws, r, 8, round(income / founders, 2), MONEY2, centre=True)
        put(ws, r, 9, meaning, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(34, 12.4 * (len(meaning) // 46 + 1))
        if fill == I.TARGET_FILL:
            for col in range(2, 10):
                ws.cell(row=r, column=col).fill = CONF_FILL["high"]
        r += 1
    r += 1
    note = ("Cost per founder rises as the coalition fills, because the "
            "cohorts are the expensive part and the richer tiers buy more "
            "of them. That is the right way round: a bigger coalition "
            "should buy more in-person delivery in more governorates, not "
            "more online seats in the same three cities.")
    c = ws.cell(row=r, column=2, value=note)
    c.font = Font(size=9.5, italic=True, color="6B7A74")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=9)
    ws.row_dimensions[r].height = 44
    return ws


def build(path):
    wb = Workbook()
    wb.remove(wb.active)
    sheet_readme(wb)
    sheet_budget(wb)
    sheet_seat(wb)
    sheet_cohort(wb)
    sheet_events(wb)
    sheet_funnel(wb)
    sheet_months(wb)
    sheet_return(wb)
    sheet_sensitivity(wb)
    wb.properties.creator = "StartPad"
    wb.properties.title = f"{I.NAME}: budget"
    wb.properties.created = FIXED_TIMESTAMP
    wb.properties.modified = FIXED_TIMESTAMP
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    normalize_zip(path)
    return path


if __name__ == "__main__":
    out = (sys.argv[1] if len(sys.argv) > 1 else
           os.path.join(os.path.dirname(os.path.dirname(
               os.path.abspath(__file__))), "output",
               "StartPad_Initiative_Budget.xlsx"))
    build(out)
    income, _ = I.budget()
    print(f"wrote {out}  ({os.path.getsize(out)/1024:,.0f} KB)")
    print(f"wave budget ${income:,.0f}, EGP {I.egp(income):,.0f}")
