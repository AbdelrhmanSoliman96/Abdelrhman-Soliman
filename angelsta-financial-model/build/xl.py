"""Styling and layout helpers that reproduce the Btakka model conventions for Angelsta."""
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as gcl

FONT = "Arial"
BRAND = "0E5A5F"      # Angelsta teal, titles
SECTION = "0E4F55"    # section bars
HDR = "1E2A2E"        # column header rows
YHDR = "D6EAE7"       # year-total header
YFILL = "EFF6F5"      # year-total cells
INK = "0B0E14"
GREY = "6B7285"
GREEN = "007A33"
BLUE = "0000FF"
RED = "C00000"
YELLOW = "FFFF00"

USD = '\\$#,##0;"($"#,##0\\);\\-'
USD2 = '\\$#,##0.00;"($"#,##0.00\\);\\-'
NUM = '#,##0;\\(#,##0\\);\\-'
NUM1 = '#,##0.0;\\(#,##0.0\\);\\-'
NUM2 = '#,##0.00;\\(#,##0.00\\);\\-'
PCT = '0.0%'
MULT = '0.00"x"'
DATE = 'mmm-yy'

NM = 60
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def mcol(m):
    y = (m - 1) // 12
    return gcl(3 + y * 13 + (m - 1) % 12)


def ycol(y):
    return gcl(2 + (y - 1) * 13)


def yr(m):
    return (m - 1) // 12 + 1


def miy(m):
    return (m - 1) % 12 + 1


def mlabel(m):
    return f"{MONTHS[(m - 1) % 12]}-{27 + (m - 1) // 12}"


def f(size=9, bold=False, italic=False, color=INK):
    return Font(name=FONT, size=size, bold=bold, italic=italic, color=color)


def fill(c):
    return PatternFill("solid", fgColor=c)


def title(ws, text, sub):
    ws["A1"] = text
    ws["A1"].font = f(15, True, color=BRAND)
    ws["A2"] = sub
    ws["A2"].font = f(8.5, italic=True, color=GREY)
    ws.sheet_view.showGridLines = False


def section(ws, r, text, ncols=66):
    for c in range(1, ncols + 1):
        ws.cell(r, c).fill = fill(SECTION)
    ws.cell(r, 1, text).font = f(9, True, color="FFFFFF")


def note(ws, r, text, col=1):
    ws.cell(r, col, text).font = f(8.5, italic=True, color=GREY)


def hdr(ws, r, labels, start=1, center_from=2):
    for i, lab in enumerate(labels):
        c = ws.cell(r, start + i, lab)
        c.font = f(8.5, True, color="FFFFFF")
        c.fill = fill(HDR)
        c.number_format = "@"
        c.alignment = Alignment(horizontal="left" if i + start < center_from else "center", wrap_text=True)


def time_hdr(ws, r, label="Line item"):
    c = ws.cell(r, 1, label)
    c.font = f(8.5, True, color="FFFFFF")
    c.fill = fill(HDR)
    for y in range(1, 6):
        c = ws[f"{ycol(y)}{r}"]
        c.value = f"Year {y}"
        c.font = f(8.5, True, color=INK)
        c.fill = fill(YHDR)
        c.alignment = Alignment(horizontal="center")
    for m in range(1, NM + 1):
        c = ws[f"{mcol(m)}{r}"]
        c.value = mlabel(m)
        c.font = f(7.6, True, color="FFFFFF")
        c.fill = fill(HDR)
        c.alignment = Alignment(horizontal="center")


def is_link(formula):
    return isinstance(formula, str) and "!" in formula


def put(ws, addr, value, fmt=NUM, kind=None, bold=False, size=8.2):
    c = ws[addr]
    c.value = value
    if kind is None:
        kind = "link" if is_link(value) else "calc"
    color = {"calc": INK, "link": GREEN, "check": RED, "input": BLUE, "note": GREY}[kind]
    c.font = f(size if kind != "input" else 9, bold or kind == "check", color=color)
    if kind == "input":
        c.fill = fill(YELLOW)
        c.alignment = Alignment(horizontal="right")
    c.number_format = fmt
    return c


def label(ws, r, text, bold=False, indent=0, col=1, size=9, color=INK):
    c = ws.cell(r, col, ("    " * indent) + text)
    c.font = f(size, bold, color=color)
    return c


def set_time_widths(ws, a=52, group=True):
    ws.column_dimensions["A"].width = a
    for y in range(1, 6):
        ws.column_dimensions[ycol(y)].width = 13.5
    for m in range(1, NM + 1):
        ws.column_dimensions[mcol(m)].width = 10.5
    if group:
        for y in range(1, 6):
            first = mcol((y - 1) * 12 + 1)
            last = mcol(y * 12)
            ws.column_dimensions.group(first, last, outline_level=1, hidden=False)
    ws.freeze_panes = "B3"


class TS:
    """Time-series sheet writer. Rows are registered by key so other sheets can link to them."""

    def __init__(self, ws, registry, start=4):
        self.ws = ws
        self.reg = registry.setdefault(ws.title, {})
        self.r = start

    def ref(self, key, m, sheet=None):
        return f"{mcol(m)}{self.reg[key]}"

    def section(self, text, sub=None):
        section(self.ws, self.r, text)
        self.r += 1
        if sub:
            note(self.ws, self.r, sub)
            self.r += 1
        time_hdr(self.ws, self.r)
        self.r += 1

    def blank(self, n=1):
        self.r += n

    def line(self, key, text, fn, fmt=NUM, total="sum", bold=False, indent=0, kind=None):
        ws, r = self.ws, self.r
        label(ws, r, text, bold=bold, indent=indent)
        for m in range(1, NM + 1):
            v = fn(m)
            if isinstance(v, str) and not v.startswith("="):
                v = "=" + v
            put(ws, f"{mcol(m)}{r}", v, fmt, kind=kind)
        for y in range(1, 6):
            a, b = mcol((y - 1) * 12 + 1), mcol(y * 12)
            if total == "sum":
                tv = f"=SUM({a}{r}:{b}{r})"
            elif total == "end":
                tv = f"={b}{r}"
            elif total == "avg":
                tv = f"=IFERROR(AVERAGE({a}{r}:{b}{r}),0)"
            elif total == "max":
                tv = f"=MAX({a}{r}:{b}{r})"
            elif total == "min":
                tv = f"=MIN({a}{r}:{b}{r})"
            else:
                tv = None
            c = put(ws, f"{ycol(y)}{r}", tv, fmt, kind="calc", bold=True, size=8.6)
            c.fill = fill(YFILL)
        if key:
            self.reg[key] = r
        self.r += 1
        return r


import re as _re
_TOK = _re.compile(r"@@([^|@]+)\|([^@]+)@@")


def tok(sheet, key):
    return f"@@{sheet}|{key}@@"


def resolve_all(wb, REG):
    """Replace @@Sheet|key@@ tokens with the registered row numbers."""
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and "@@" in v:
                    c.value = _TOK.sub(lambda mo: str(REG[mo.group(1)][mo.group(2)]), v)
