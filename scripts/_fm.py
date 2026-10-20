"""
Geometry and styling for the StartPad financial model.

The column layout follows the reference workbook the founder supplied: the
year total comes first, then that year's twelve months.

    A        line item
    B        Year 1 total      C … N    Oct 2026 - Sep 2027
    O        Year 2 total      P … AA   Oct 2027 - Sep 2028
    AB       Year 3 total      AC … AN
    AO       Year 4 total      AP … BA
    BB       Year 5 total      BC … BN

Sixty months, five years, one shape on every time sheet, so a formula on one
sheet addresses the same month on another without a lookup.

Nothing here computes a number. Values belong in the workbook as formulas.
"""
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

YEARS = 5
MONTHS = 60
LAST_COL = 2 + (YEARS - 1) * 13 + 12   # BN, the last month of year five

_MONTH_NAMES = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar",
                "Apr", "May", "Jun", "Jul", "Aug", "Sep"]


def year_of(m):
    return (m - 1) // 12 + 1


def pos_in_year(m):
    return (m - 1) % 12 + 1


def months_of(y):
    return range((y - 1) * 12 + 1, y * 12 + 1)


def ycol(y):
    """Column index of the year-y total."""
    return 2 + (y - 1) * 13


def mcol(m):
    """Column index of month m (1-60)."""
    return ycol(year_of(m)) + pos_in_year(m)


def yl(y):
    return get_column_letter(ycol(y))


def ml(m):
    return get_column_letter(mcol(m))


def quarter_of(m):
    """Plan quarter 1-20 that month m falls in."""
    return (m - 1) // 3 + 1


def pos_in_quarter(m):
    return (m - 1) % 3 + 1


MONTH_LABELS = []
for _m in range(1, MONTHS + 1):
    _yr = 2026 + (_m - 1 + 3) // 12
    MONTH_LABELS.append(f"{_MONTH_NAMES[(_m - 1) % 12]}-{str(_yr)[2:]}")

QUARTER_LABELS = []
for _q in range(1, YEARS * 4 + 1):
    _first = (_q - 1) * 3 + 1
    _yr = 2026 + (_first - 1 + 3) // 12
    _qn = ((_first - 1) % 12) // 3 + 1
    QUARTER_LABELS.append(f"FY{(_q - 1) // 4 + 1} Q{_qn} {_yr}")

# ---------------------------------------------------------------- palette
UV, UV_DARK, LIME = "3418E0", "1E0C8C", "CBF24A"
INK, INK2, MUTED = "0B0E14", "3A4050", "6B7285"
WASH, BAND, RULE, WHITE = "F2F3F7", "E8EAF4", "D4D7E3", "FFFFFF"
RED = "B00020"
IN_FONT, LINK_FONT, YELLOW = "0000FF", "008000", "FFFF00"
FONT = "Arial"

MONEY = '$#,##0;($#,##0);"-"'
MONEY2 = '$#,##0.00;($#,##0.00);"-"'
NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
NUM2 = '#,##0.00;(#,##0.00);"-"'
PCT = '0.0%'
PCT2 = '0.00%'
MULT = '0.0x'
TEXT = '@'
DAYS = '0 "days"'

MED = Side(style="medium", color=UV)


def f(size=9, bold=False, color=INK, italic=False):
    return Font(name=FONT, size=size, bold=bold, color=color, italic=italic)


def fill(hexcolor):
    return PatternFill("solid", fgColor=hexcolor)


def sheet_title(ws, title, subtitle, last_col=LAST_COL):
    c = ws.cell(1, 1, title)
    c.font = f(15, True, UV)
    ws.row_dimensions[1].height = 25
    c2 = ws.cell(2, 1, subtitle)
    c2.font = f(8.5, False, MUTED)
    ws.row_dimensions[2].height = 14
    for col in range(1, min(last_col, 40) + 1):
        ws.cell(3, col).border = Border(bottom=MED)
    ws.row_dimensions[3].height = 4
    ws.sheet_view.showGridLines = False


def band(ws, r, text, last_col=LAST_COL):
    for col in range(1, last_col + 1):
        cell = ws.cell(r, col)
        cell.fill = fill(UV)
        cell.font = f(9, True, WHITE)
    ws.cell(r, 1, text)
    ws.row_dimensions[r].height = 17
    return r + 1


def setup_time(ws, title, subtitle, freeze="C6"):
    sheet_title(ws, title, subtitle)
    ws.column_dimensions["A"].width = 46
    for y in range(1, YEARS + 1):
        ws.column_dimensions[get_column_letter(ycol(y))].width = 13.5
        for m in months_of(y):
            ws.column_dimensions[get_column_letter(mcol(m))].width = 10
    ws.freeze_panes = freeze


def time_header(ws, r):
    """The year and month strip, written once per time sheet."""
    c = ws.cell(r, 1, "Line item")
    c.font = f(8.5, True, WHITE)
    c.fill = fill(UV_DARK)
    for y in range(1, YEARS + 1):
        cy = ws.cell(r, ycol(y), f"Year {y}")
        cy.font = f(8.5, True, INK)
        cy.fill = fill(LIME)
        cy.alignment = Alignment(horizontal="center")
        cy.number_format = TEXT
        for m in months_of(y):
            cm = ws.cell(r, mcol(m), MONTH_LABELS[m - 1])
            cm.font = f(7.6, True, WHITE)
            cm.fill = fill(UV_DARK if y % 2 else UV)
            cm.alignment = Alignment(horizontal="center")
            cm.number_format = TEXT
    ws.row_dimensions[r].height = 15
    return r + 1


def year_agg(row, y, agg="sum"):
    ms = list(months_of(y))
    rng = f"{ml(ms[0])}{row}:{ml(ms[-1])}{row}"
    return {"sum": f"=SUM({rng})",
            "end": f"={ml(ms[-1])}{row}",
            "avg": f"=IFERROR(AVERAGE({rng}),0)",
            "max": f"=MAX({rng})",
            "min": f"=MIN({rng})"}[agg]


def label_cell(ws, r, label, note="", bold=False, indent=0, size=9,
               fill_colour=None):
    c = ws.cell(r, 1, ("    " * indent) + label)
    c.font = f(size, bold, INK)
    if note:
        c.comment = None
    if fill_colour:
        ws.cell(r, 1).fill = fill(fill_colour)
        for y in range(1, YEARS + 1):
            ws.cell(r, ycol(y)).fill = fill(fill_colour)
            for m in months_of(y):
                ws.cell(r, mcol(m)).fill = fill(fill_colour)
    return r


def trow(ws, r, label, formula, fmt=MONEY, bold=False, indent=0, agg="sum",
         colour=INK, fill_colour=None, years=True):
    """
    One line across sixty months and five year totals.

    `formula` is called with the month number, so every month is written the
    same way and a single hand-edited cell mid-row - the commonest silent
    error in a model - cannot happen by accident.
    """
    label_cell(ws, r, label, bold=bold, indent=indent,
               fill_colour=fill_colour)
    for m in range(1, MONTHS + 1):
        c = ws.cell(r, mcol(m), formula(m) if callable(formula) else formula)
        c.number_format = fmt
        c.font = f(8.2, bold, colour)
    if years:
        for y in range(1, YEARS + 1):
            c = ws.cell(r, ycol(y), year_agg(r, y, agg))
            c.number_format = fmt
            c.font = f(8.6, True, INK)
            c.fill = fill(fill_colour or BAND)
    return r + 1


def mref(sheet, row, m):
    return f"{sheet}!{ml(m)}${row}"


def yref(sheet, row, y):
    return f"{sheet}!{yl(y)}${row}"
