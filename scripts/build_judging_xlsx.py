# -*- coding: utf-8 -*-
"""
Build the Mission Zero judging workbook.

The rubric weights live in one place — competition/rules.py — and are read from
there, so the sheet a judge scores on cannot drift from the rubric published to
entrants. Pillar scores are entered 0–5 and the weighted total is a formula, so
nobody hand-computes a percentage under time pressure at Demo Day.

Two columns exist because of how this competition can fail rather than because a
scoring sheet usually has them: a conflict-of-interest flag, declared before
scores are entered, and a verification log tab for the calls placed to people
finalists claim to have interviewed.
"""
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from competition.rules import EN, VERSION  # noqa: E402
from scripts._determinism import FIXED_TIMESTAMP, normalize_zip  # noqa: E402

INK = "FF101E2E"
SEA = "FF0E7C86"
AMBER = "FFB4650E"
GREY = "FF63737F"
HEAD_FILL = PatternFill("solid", fgColor="FFEDF3F3")
NOTE_FILL = PatternFill("solid", fgColor="FFFAEFDF")
EX_FILL = PatternFill("solid", fgColor="FFF4F4F0")
THIN = Side(style="thin", color="FFD9DBD3")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

ROWS = 120  # scoring capacity; the plan targets ~55 eligible entries


def rubric_from_rules():
    """Read the published rubric straight out of the participant-facing rules."""
    for block in EN["blocks"]:
        if block[0] == "t" and block[1][:2] == ["Pillar", "Weight"]:
            return [(name, int(w.rstrip("%")), desc) for name, w, desc in block[2]]
    raise RuntimeError("rubric table not found in competition/rules.py")


RUBRIC = rubric_from_rules()
assert sum(w for _, w, _ in RUBRIC) == 100, "rubric weights must total 100"


def head(ws, row, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = Font(bold=True, size=9, color=SEA)
        c.fill = HEAD_FILL
        c.border = BORDER
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 28
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=15, color=INK)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(size=9.5, color=GREY)


def sheet_readme(wb):
    ws = wb.create_sheet("READ ME FIRST")
    ws.column_dimensions["A"].width = 110
    title(ws, "Mission Zero — judging workbook", "Rubric " + VERSION)
    lines = [
        ("", ""),
        ("How this is scored", "h"),
        ("Every pillar is scored 0–5. The weighted total is a formula — do not type over "
         "it. Weights come from the rubric published to entrants, so this sheet and that "
         "page cannot disagree.", ""),
        ("0 = absent · 1 = asserted, no support · 2 = thin · 3 = adequate · "
         "4 = strong · 5 = exceptional", ""),
        ("", ""),
        ("Before you score anything", "h"),
        ("1. Declare conflicts. If you know an entrant, or taught them, or their team "
         "approached you for work, put Yes in 'Conflict' and leave their scores empty. "
         "Someone else scores that row.", ""),
        ("2. Score the shortlist blind. Names and universities are stripped before this "
         "sheet reaches you; do not go looking for them.", ""),
        ("3. Automated scores are advisory. They decided who reached you, not who wins.", ""),
        ("", ""),
        ("The verification log is not optional", "n"),
        ("For every finalist, call a random 10% of the people they logged as interviewed. "
         "The log tab records who was called, who answered, and whether the interview "
         "happened. An entry with a fabricated interview is disqualified, not "
         "down-scored — and that was announced before entries opened.", ""),
        ("", ""),
        ("Sheets", "h"),
        ("RUBRIC — the published criteria and what earns each mark.", ""),
        ("SCORESHEET — one row per entry. Rows marked EXAMPLE are illustrations; delete "
         "them before use. Leave the pitch column empty until Demo Day, so a pre-pitch "
         "total reads out of 85% — the SHORTLIST tab adds the pitch back.", ""),
        ("SHORTLIST — the ten who pitch, with pitch scores added on the day.", ""),
        ("VERIFICATION LOG — calls placed to interviewees named by finalists.", ""),
        ("VOCAB — the dropdown values. Edit here, not in the columns.", ""),
    ]
    r = 4
    for text, kind in lines:
        c = ws.cell(row=r, column=1, value=text)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if kind == "h":
            c.font = Font(bold=True, size=11, color=SEA)
        elif kind == "n":
            c.font = Font(bold=True, size=11, color=AMBER)
            c.fill = NOTE_FILL
        else:
            c.font = Font(size=10, color=INK)
        ws.row_dimensions[r].height = 15 if len(text) < 90 else 30
        r += 1
    return ws


def sheet_rubric(wb):
    ws = wb.create_sheet("RUBRIC")
    title(ws, "Published rubric", "Identical to the criteria shown to entrants")
    head(ws, 4, ["Pillar", "Weight", "What earns the marks"], [34, 10, 88])
    for i, (name, weight, desc) in enumerate(RUBRIC, start=5):
        ws.cell(row=i, column=1, value=name).font = Font(bold=True, size=10, color=INK)
        c = ws.cell(row=i, column=2, value=weight / 100)
        c.number_format = "0%"
        c.alignment = Alignment(horizontal="right")
        ws.cell(row=i, column=3, value=desc).alignment = Alignment(wrap_text=True,
                                                                  vertical="top")
        for col in range(1, 4):
            ws.cell(row=i, column=col).border = BORDER
        ws.row_dimensions[i].height = 30
    total = ws.cell(row=5 + len(RUBRIC), column=2,
                    value="=SUM(B5:B%d)" % (4 + len(RUBRIC)))
    total.number_format = "0%"
    total.font = Font(bold=True, color=SEA)
    ws.cell(row=5 + len(RUBRIC), column=1, value="Total").font = Font(bold=True)
    return ws


def sheet_scoresheet(wb):
    ws = wb.create_sheet("SCORESHEET")
    title(ws, "Scoresheet", "Score 0–5 per pillar. The weighted total is a formula.")
    pillars = [name for name, _, _ in RUBRIC]
    headers = (["Entry ID", "Judge", "Conflict"] + pillars +
               ["Weighted total", "Decision", "Note"])
    widths = [12, 14, 11] + [17] * len(pillars) + [15, 16, 46]
    head(ws, 4, headers, widths)

    first_p = 4                      # column D
    last_p = 3 + len(pillars)
    weight_cells = ["RUBRIC!$B$%d" % (5 + i) for i in range(len(RUBRIC))]

    for r in range(5, 5 + ROWS):
        terms = ["%s%d/5*%s" % (get_column_letter(first_p + i), r, weight_cells[i])
                 for i in range(len(pillars))]
        f = ws.cell(row=r, column=last_p + 1,
                    value="=IF(COUNT(%s%d:%s%d)=0,\"\",%s)" % (
                        get_column_letter(first_p), r,
                        get_column_letter(last_p), r, "+".join(terms)))
        f.number_format = "0.0%"
        f.font = Font(bold=True, color=INK)
        for col in range(1, len(headers) + 1):
            ws.cell(row=r, column=col).border = BORDER

    score_dv = DataValidation(type="whole", operator="between", formula1=0, formula2=5,
                              allow_blank=True, showErrorMessage=True,
                              errorTitle="Score out of range",
                              error="Pillar scores are whole numbers from 0 to 5.")
    ws.add_data_validation(score_dv)
    score_dv.add("%s5:%s%d" % (get_column_letter(first_p),
                               get_column_letter(last_p), 4 + ROWS))

    yn = DataValidation(type="list", formula1="=VOCAB!$A$2:$A$3", allow_blank=True,
                        showErrorMessage=True)
    ws.add_data_validation(yn)
    yn.add("C5:C%d" % (4 + ROWS))

    dec = DataValidation(type="list", formula1="=VOCAB!$B$2:$B$5", allow_blank=True,
                         showErrorMessage=True)
    ws.add_data_validation(dec)
    dec.add("%s5:%s%d" % (get_column_letter(last_p + 2),
                          get_column_letter(last_p + 2), 4 + ROWS))

    # One illustrative row, keyed by column so it cannot drift out of alignment if the
    # rubric gains a pillar. The weighted-total column is left to its formula.
    example = {
        1: "MZ-0001", 2: "Judge A", 3: "No",
        first_p: 4, first_p + 1: 3, first_p + 2: 4, first_p + 3: 3,
        last_p: "",                      # pitch stays empty until Demo Day
        last_p + 2: "Shortlist",
        last_p + 3: "EXAMPLE ROW — delete before use.",
    }
    for col, val in example.items():
        c = ws.cell(row=5, column=col, value=val)
        c.fill = EX_FILL
        c.font = Font(size=10, italic=True, color=GREY)
    return ws


def sheet_shortlist(wb):
    ws = wb.create_sheet("SHORTLIST")
    title(ws, "Demo Day shortlist", "Ten pitches. Pitch scores are added on the day.")
    head(ws, 4,
         ["Rank", "Entry ID", "Team", "Governorate", "Pre-pitch total",
          "Pitch score (0–5)", "Final total", "Verification cleared", "Outcome"],
         [8, 12, 26, 18, 16, 17, 14, 20, 20])
    for r in range(5, 15):
        ws.cell(row=r, column=1, value=r - 4).font = Font(bold=True, color=GREY)
        ws.cell(row=r, column=7, value="=IF(COUNT(E%d:F%d)<2,\"\",E%d*0.85+F%d/5*0.15)"
                % (r, r, r, r)).number_format = "0.0%"
        for col in range(1, 10):
            ws.cell(row=r, column=col).border = BORDER
    dv = DataValidation(type="list", formula1="=VOCAB!$A$2:$A$3", allow_blank=True)
    ws.add_data_validation(dv)
    dv.add("H5:H14")
    out = DataValidation(type="list", formula1="=VOCAB!$C$2:$C$6", allow_blank=True)
    ws.add_data_validation(out)
    out.add("I5:I14")
    ws.cell(row=16, column=1,
            value="Final total re-weights the pre-pitch score to 85% and the pitch to "
                  "15%, matching the published rubric.").font = Font(size=9, color=GREY)
    return ws


def sheet_verification(wb):
    ws = wb.create_sheet("VERIFICATION LOG")
    title(ws, "Interview verification",
          "A random 10% of each finalist's logged interviewees. Announced before entries "
          "opened.")
    head(ws, 4,
         ["Entry ID", "Interviewee first name", "City", "Date logged", "Called on",
          "Reached", "Interview confirmed", "Caller", "Note"],
         [12, 24, 16, 14, 14, 12, 20, 14, 44])
    for r in range(5, 65):
        for col in range(1, 10):
            ws.cell(row=r, column=col).border = BORDER
    for col, src in (("F", "$A$2:$A$3"), ("G", "$D$2:$D$5")):
        dv = DataValidation(type="list", formula1="=VOCAB!" + src, allow_blank=True)
        ws.add_data_validation(dv)
        dv.add("%s5:%s64" % (col, col))
    ws.cell(row=66, column=1,
            value="'Interview confirmed = No' is a disqualification question, not a "
                  "scoring one. Escalate before acting.").font = Font(size=9, color=AMBER)
    return ws


def sheet_vocab(wb):
    ws = wb.create_sheet("VOCAB")
    title(ws, "Dropdown values", "Edit here; the columns read from this sheet.")
    cols = {
        "A": ("Yes / No", ["Yes", "No"]),
        "B": ("Decision", ["Shortlist", "Hold", "Reject", "Disqualify"]),
        "C": ("Outcome", ["First", "Second", "Third", "Finalist", "Withdrawn"]),
        "D": ("Confirmed", ["Confirmed", "Not reached", "Denies interview", "Unclear"]),
    }
    for letter, (label, values) in cols.items():
        ws.column_dimensions[letter].width = 20
        c = ws["%s1" % letter]
        c.value = label
        c.font = Font(bold=True, size=9, color=SEA)
        c.fill = HEAD_FILL
        for i, v in enumerate(values, start=2):
            ws["%s%d" % (letter, i)] = v
    return ws


def build(out_path):
    wb = Workbook()
    wb.remove(wb.active)
    sheet_readme(wb)
    sheet_rubric(wb)
    sheet_scoresheet(wb)
    sheet_shortlist(wb)
    sheet_verification(wb)
    sheet_vocab(wb)

    wb.properties.title = "Mission Zero — judging workbook"
    wb.properties.creator = "StartPad"
    wb.properties.created = FIXED_TIMESTAMP
    wb.properties.modified = FIXED_TIMESTAMP

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    wb.save(out_path)
    normalize_zip(out_path)
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/Mission_Zero_Judging_Pack.xlsx"
    p = build(out)
    print("wrote", p, os.path.getsize(p), "bytes")
