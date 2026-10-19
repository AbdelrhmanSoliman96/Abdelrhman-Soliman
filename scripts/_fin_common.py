"""
Shared layout, styling and formula helpers for the financial model builder.

The model is 36 monthly columns with three annual totals beside them. Every
sheet uses the same geometry, so a formula written on one sheet can address the
same month on another without a lookup:

    A   line item
    B   driver, unit or source
    C … AL    months 1-36   (M1 = Oct 2026, M36 = Sep 2029)
    AM        spacer
    AN AO AP  Year 1, Year 2, Year 3

Nothing here computes a number. Values belong in the workbook as formulas, so
that changing an assumption changes the model rather than requiring a rebuild.
"""
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

MONTHS = 36
FIRST_M_COL = 3                      # column C
YEAR_COLS = {1: 40, 2: 41, 3: 42}    # AN, AO, AP
SPACER_COL = 39                      # AM

# ---------------------------------------------------------------- geometry

def mcol(m):
    """Column index of month m (1-36)."""
    return FIRST_M_COL + m - 1


def ml(m):
    """Column letter of month m."""
    return get_column_letter(mcol(m))


def yl(y):
    """Column letter of year y (1-3)."""
    return get_column_letter(YEAR_COLS[y])


def year_of(m):
    return (m - 1) // 12 + 1


def months_of(y):
    return range((y - 1) * 12 + 1, y * 12 + 1)


def quarter_of(m):
    """Plan quarter 1-12 that month m falls in."""
    return (m - 1) // 3 + 1


def pos_in_quarter(m):
    """1, 2 or 3 — which month of its quarter."""
    return (m - 1) % 3 + 1


MONTH_LABELS = []
_names = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar",
          "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
for _m in range(1, MONTHS + 1):
    _yr = 2026 + (_m - 1 + 3) // 12          # Oct 2026 starts FY1
    MONTH_LABELS.append(f"{_names[(_m - 1) % 12]} {str(_yr)[2:]}")

QUARTER_LABELS = ["Q4 2026", "Q1 2027", "Q2 2027", "Q3 2027",
                  "Q4 2027", "Q1 2028", "Q2 2028", "Q3 2028",
                  "Q4 2028", "Q1 2029", "Q2 2029", "Q3 2029"]

# ---------------------------------------------------------------- palette
UV = "3418E0"          # StartPad primary
UV_DARK = "1E0C8C"
LIME = "CBF24A"
INK = "0B0E14"
WASH = "F2F3F7"
BAND = "E8EAF4"
RULE = "D4D7E3"
WHITE = "FFFFFF"

# Financial-model convention: blue = typed input, black = formula,
# green = link to another sheet, yellow fill = key assumption to edit.
IN_FONT = "0000FF"
LINK_FONT = "008000"
YELLOW = "FFFF00"

FONT = "Arial"

# ---------------------------------------------------------------- formats
MONEY = '$#,##0;($#,##0);"-"'
MONEY2 = '$#,##0.00;($#,##0.00);"-"'
NUM = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%'
PCT0 = '0%'
MULT = '0.0x'
DAYS = '0 "days"'
TEXT = '@'

# ---------------------------------------------------------------- styling
THIN = Side(style="thin", color=RULE)
MED = Side(style="medium", color=UV)


def f(size=9, bold=False, color=INK, italic=False):
    return Font(name=FONT, size=size, bold=bold, color=color, italic=italic)


def fill(hexcolor):
    return PatternFill("solid", fgColor=hexcolor)


def sheet_title(ws, title, subtitle, last_col=42):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=last_col)
    c = ws.cell(1, 1, title)
    c.font = f(15, True, UV)
    c.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 26
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=last_col)
    c2 = ws.cell(2, 1, subtitle)
    c2.font = f(8.5, False, "6B7285")
    ws.row_dimensions[2].height = 14
    for col in range(1, last_col + 1):
        ws.cell(3, col).border = Border(bottom=MED)
    ws.row_dimensions[3].height = 4


def band(ws, r, text, last_col=42):
    """A section heading band across the sheet."""
    for col in range(1, last_col + 1):
        cell = ws.cell(r, col)
        cell.fill = fill(UV)
        cell.font = f(9, True, WHITE)
    ws.cell(r, 1, text)
    ws.row_dimensions[r].height = 17
    return r + 1


def month_header(ws, r, include_years=True):
    """The month strip. Written once per monthly sheet."""
    ws.cell(r, 1, "Line item").font = f(8.5, True, WHITE)
    ws.cell(r, 2, "Driver / source").font = f(8.5, True, WHITE)
    for col in (1, 2):
        ws.cell(r, col).fill = fill(UV_DARK)
    for m in range(1, MONTHS + 1):
        c = ws.cell(r, mcol(m), MONTH_LABELS[m - 1])
        c.font = f(8, True, WHITE)
        c.fill = fill(UV_DARK if year_of(m) % 2 else UV)
        c.alignment = Alignment(horizontal="center")
        c.number_format = TEXT
    ws.cell(r, SPACER_COL).fill = fill(WHITE)
    if include_years:
        for y in (1, 2, 3):
            c = ws.cell(r, YEAR_COLS[y], f"YEAR {y}")
            c.font = f(8.5, True, INK)
            c.fill = fill(LIME)
            c.alignment = Alignment(horizontal="center")
            c.number_format = TEXT
    ws.row_dimensions[r].height = 16
    return r + 1


def setup_monthly(ws, title, subtitle, freeze="C6"):
    sheet_title(ws, title, subtitle)
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 30
    for m in range(1, MONTHS + 1):
        ws.column_dimensions[get_column_letter(mcol(m))].width = 10.5
    ws.column_dimensions[get_column_letter(SPACER_COL)].width = 2
    for y in (1, 2, 3):
        ws.column_dimensions[get_column_letter(YEAR_COLS[y])].width = 13
    ws.freeze_panes = freeze
    ws.sheet_view.showGridLines = False


def year_sum(row, y, agg="sum"):
    """Annual aggregate formula for a monthly row."""
    ms = list(months_of(y))
    rng = f"{ml(ms[0])}{row}:{ml(ms[-1])}{row}"
    if agg == "sum":
        return f"=SUM({rng})"
    if agg == "end":
        return f"={ml(ms[-1])}{row}"
    if agg == "avg":
        return f"=IFERROR(AVERAGE({rng}),0)"
    if agg == "max":
        return f"=MAX({rng})"
    if agg == "min":
        return f"=MIN({rng})"
    raise ValueError(agg)


def write_row(ws, r, label, note="", fmt=MONEY, bold=False, indent=0,
              label_colour=INK, fill_colour=None, size=9):
    c = ws.cell(r, 1, ("    " * indent) + label)
    c.font = f(size, bold, label_colour)
    n = ws.cell(r, 2, note)
    n.font = f(7.5, False, "6B7285")
    n.alignment = Alignment(wrap_text=False)
    if fill_colour:
        for col in list(range(1, SPACER_COL)) + list(YEAR_COLS.values()):
            ws.cell(r, col).fill = fill(fill_colour)
    return r


def monthly_row(ws, r, label, formula, note="", fmt=MONEY, bold=False,
                indent=0, agg="sum", colour=INK, fill_colour=None,
                years=True):
    """
    One monthly line. `formula` is called with the month number and returns the
    formula string (or a literal), so every month is written the same way and a
    single edited cell mid-row — the commonest silent error in a model — cannot
    happen by accident.
    """
    write_row(ws, r, label, note, fmt, bold, indent, fill_colour=fill_colour)
    for m in range(1, MONTHS + 1):
        c = ws.cell(r, mcol(m), formula(m) if callable(formula) else formula)
        c.number_format = fmt
        c.font = f(8.5, bold, colour)
    if years:
        for y in (1, 2, 3):
            c = ws.cell(r, YEAR_COLS[y], year_sum(r, y, agg))
            c.number_format = fmt
            c.font = f(8.5, True, INK)
            c.fill = fill(WASH)
    return r + 1


def input_cell(ws, r, c, value, fmt=MONEY, note=None):
    cell = ws.cell(r, c, value)
    cell.number_format = fmt
    cell.font = f(9, False, IN_FONT)
    cell.fill = fill(YELLOW)
    if note:
        ws.cell(r, 2, note).font = f(7.5, False, "6B7285")
    return cell


def abs_ref(sheet, row, col):
    return f"{sheet}!${get_column_letter(col)}${row}"
