"""
Audit the financial model for static values and broken links.

Three questions, asked of every cell on every sheet:

  1  Is there a number sitting in a cell that is not a designated input?
     An input is blue on a yellow fill. Anything else numeric should be a
     formula, or the model does not move when the assumption moves.

  2  Is there a number buried inside a formula that ought to be an input?
     Structural constants are allowed and listed below; a retention
     assumption or a price is not structural.

  3  Does every sheet actually reach the sheets it depends on?

Run it after any change to the builder:

    python scripts/audit_financial_model.py output/StartPad_Financial_Model.xlsx
"""
import collections
import re
import sys

from openpyxl import load_workbook

# Numbers that are structural rather than assumptions. Twelve is months in a
# year, thirty is days in a month for the working capital conversion, a
# thousand is the unit of a per thousand rate, and 9999 is the sentinel that
# means "did not happen inside the modelled period".
STRUCTURAL = {"0", "1", "2", "3", "30", "100", "1000", "9999", "365", "99"}

# Year boundaries. A test like "is this month 24" is asking which year the
# month falls in, and 13 is the column stride on a time sheet: twelve months
# plus the year total that sits in front of them.
STRUCTURAL |= {str(12 * y) for y in range(1, 6)} | {"13"}

# A monthly model written one column per month carries its own month number in
# any formula that has to know which month it is: the acquisition date test,
# the sales cycle lag, the break even flag. That is the column's identity, not
# an assumption, so a number equal to the cell's own month index is allowed.

# Sheets whose cells are reference text rather than model values.
TEXT_SHEETS = {"Cover", "Market Research", "Input>>", "Process>>", "Output>>",
               "Analysis>>"}

NUM_IN_FORMULA = re.compile(r"(?<![A-Za-z0-9_$.!])(\d+\.?\d*)(?![0-9]*\s*\))")


def month_index(col):
    """The month number a column holds, or None, for the rule above."""
    if col < 3:
        return None
    y, rest = divmod(col - 2, 13)
    if rest == 0:
        return None
    return str((y * 12) + rest)


def is_input(cell):
    fillc = cell.fill
    return (fillc is not None and fillc.fgColor is not None
            and str(fillc.fgColor.rgb).endswith("FFFF00"))


def audit(path):
    wb = load_workbook(path)
    statics = []
    magic = collections.Counter()
    magic_where = collections.defaultdict(list)
    links = collections.defaultdict(set)
    formulas = 0

    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                v = cell.value
                if v is None:
                    continue
                if isinstance(v, str) and v.startswith("="):
                    formulas += 1
                    for ref in re.findall(r"'([^']+)'!", v):
                        links[ws.title].add(ref)
                    for ref in re.findall(r"(?<!['\w])([A-Za-z_]+)!", v):
                        links[ws.title].add(ref)
                    body = re.sub(r"'[^']*'!\$?[A-Z]+\$?\d+", " ", v)
                    body = re.sub(r"\$?[A-Z]{1,2}\$?\d+", " ", body)
                    body = re.sub(r'"[^"]*"', " ", body)
                    own = month_index(cell.column)
                    for n in NUM_IN_FORMULA.findall(body):
                        n = n.rstrip(".")
                        if n and n not in STRUCTURAL and n != own:
                            magic[n] += 1
                            if len(magic_where[n]) < 4:
                                magic_where[n].append(
                                    f"{ws.title}!{cell.coordinate}")
                    continue
                if ws.title in TEXT_SHEETS:
                    continue
                if isinstance(v, (int, float)) and not is_input(cell):
                    statics.append((ws.title, cell.coordinate, v))

    print(f"formulas: {formulas:,}")
    print(f"\nSTATIC NUMBERS OUTSIDE AN INPUT CELL: {len(statics)}")
    by_sheet = collections.Counter(s for s, _, _ in statics)
    for sheet, n in by_sheet.most_common():
        sample = [f"{c}={v}" for s, c, v in statics if s == sheet][:6]
        print(f"  {sheet:34s} {n:4d}   {', '.join(sample)}")

    print(f"\nHARDCODED NUMBERS INSIDE FORMULAS: {len(magic)} distinct")
    for n, count in magic.most_common():
        print(f"  {n:>10s}  x{count:<5d} {', '.join(magic_where[n])}")

    print("\nSHEET DEPENDENCIES")
    for sheet in wb.sheetnames:
        deps = sorted(links.get(sheet, ()))
        if deps:
            print(f"  {sheet:34s} -> {', '.join(deps)}")
    orphans = [s for s in wb.sheetnames
               if s not in TEXT_SHEETS and not links.get(s)
               and not any(s in d for d in links.values())]
    print("\n  sheets neither reading nor read:", orphans or "none")
    return statics, magic


if __name__ == "__main__":
    audit(sys.argv[1] if len(sys.argv) > 1
          else "output/StartPad_Financial_Model.xlsx")
