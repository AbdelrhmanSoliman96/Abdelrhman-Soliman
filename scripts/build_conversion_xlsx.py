"""Build the conversion playbook: why nobody finishes, and what to run."""
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from growth import conversion as C                              # noqa: E402
from scripts._determinism import FIXED_TIMESTAMP, normalize_zip  # noqa: E402
from scripts.build_prospects_xlsx import (                      # noqa: E402
    ACCENT, BOX, CONF_FILL, CONF_FONT, HEAD, INK, SUBHEAD, SUNK, banner,
    prose,
)

EFFORT_LABEL = {"S": "S, days", "M": "M, weeks", "L": "L, a quarter"}
EFFORT_FILL = {"S": CONF_FILL["high"], "M": CONF_FILL["medium"],
               "L": CONF_FILL["low"]}
EFFORT_FONT = {"S": CONF_FONT["high"], "M": CONF_FONT["medium"],
               "L": CONF_FONT["low"]}
CONF_ORDER = {"High": 0, "Medium": 1, "Low": 2}
STATUS = ["Not started", "Designing", "Building", "Running", "Won", "Lost",
          "Inconclusive", "Dropped"]


def row_head(ws, r, heads, widths, start=2):
    for i, (h, w) in enumerate(zip(heads, widths)):
        c = ws.cell(row=r, column=start + i, value=h)
        c.font = Font(bold=True, size=10, color="FFFFFF")
        c.fill = SUBHEAD
        c.border = BOX
        c.alignment = Alignment(vertical="center", indent=1, wrap_text=True)
        ws.column_dimensions[get_column_letter(start + i)].width = w
    ws.row_dimensions[r].height = 30
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


def footnote(ws, r, text, last_col, height=46):
    c = ws.cell(row=r, column=2, value=text)
    c.font = Font(size=9.5, italic=True, color="6B7A74")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=2, end_row=r,
                   end_column=last_col)
    ws.row_dimensions[r].height = height
    return r + 1


# ------------------------------------------------------------------ READ ME
def sheet_readme(wb):
    ws = wb.create_sheet("READ ME FIRST")
    ws.sheet_view.showGridLines = False
    banner(ws, "Why nobody finishes mission 01, and what to do about it",
           "The paid conversion problem is not a pricing problem. It is an "
           "onboarding problem and a payments problem wearing a pricing "
           "problem's clothes.", 5)
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 104

    now = tgt = 10_000
    for _, a, b, _ in C.FUNNEL[1:]:
        now *= a
        tgt *= b

    blocks = [
        ("THE SHORT VERSION", ""),
        ("", "Mission 01 asks a stranger who registered ninety seconds ago "
             "for five written answers, and tells them it will take two to "
             "three hours. That is the largest leak in the product, and "
             "nobody converts to paid from a mission they never finished."),
        ("", "Underneath that, the checkout takes valU, Visa and "
             "Mastercard, and does not take Fawry, Vodafone Cash, InstaPay "
             "or Meeza. A student in Assiut who wants to pay often "
             "cannot, and in the data that looks exactly like a student "
             "who did not want to pay."),
        ("", "Fix those two and the price question becomes answerable. Fix "
             "the price first and you will have discounted a product "
             "nobody can finish."),
        ("", ""),
        ("THE THREE PROBLEMS, IN ORDER", ""),
        ("1. Activation", "They never finish the first mission. Everything "
                          "else is downstream of this."),
        ("2. Habit", "Nothing brings them back tomorrow: no WhatsApp, no "
                     "peer, no deadline."),
        ("3. Paying", "A dollar price and a card most of the market does "
                      "not have."),
        ("", ""),
        ("WHAT THIS FILE IS", ""),
        ("DIAGNOSIS", "Eight things that are wrong, with the evidence from "
                      "the product itself."),
        ("MEASURE FIRST", "What has to be instrumented in weeks one and "
                          "two. Until this exists, every fix is a guess."),
        ("EXPERIMENTS", f"{len(C.EXPERIMENTS)} experiments in six themes, "
                        f"each with a hypothesis, the change, a metric, an "
                        f"effort and an expected lift. Sorted so the top of "
                        f"the sheet is what to run first."),
        ("THE FIRST 10 MINUTES", "The replacement onboarding, screen by "
                                 "screen, with a clock on it."),
        ("NUDGES", "The WhatsApp sequence, message by message, ready to be "
                   "written properly in Egyptian Arabic."),
        ("THE MATHS", "What the funnel does today and what it could do. "
                      "Replace the 'now' column with real numbers the "
                      "moment the instrumentation is live."),
        ("THE 90 DAYS", "The order to do it in, and the rules that stop a "
                        "quarter ending with six changes and no "
                        "knowledge."),
        ("", ""),
        ("THE PRIZE", ""),
        ("", f"On the illustrative numbers in THE MATHS, paid conversion "
             f"goes from {now / 100:,.2f} per cent to {tgt / 100:,.2f} per "
             f"cent, which is {tgt / now:,.1f} times. Six improvements "
             f"multiplied together is also how a plan lies to the person "
             f"who wrote it, so treat the compound as a direction rather "
             f"than a forecast. Half of it would still be the difference "
             f"between a product that does not sell and one that does."),
        ("", "The two largest contributors are the first row of that "
             "funnel and the last: an onboarding screen and a payment "
             "method. Neither of them is the price."),
        ("", ""),
        ("ONE THING TO DO THIS WEEK, BEFORE ANY OF IT", ""),
        ("", "Call twenty users who stopped at mission 01 and ask what "
             "they were doing at the moment they stopped. Not what they "
             "think of the product. What they were doing. An afternoon of "
             "that is worth more than this entire file, and it will "
             "reorder the experiment sheet."),
    ]
    prose(ws, blocks, wrap_at=100)
    return ws


# -------------------------------------------------------------- DIAGNOSIS
def sheet_diagnosis(wb):
    ws = wb.create_sheet("DIAGNOSIS")
    ws.sheet_view.showGridLines = False
    banner(ws, "Eight things that are wrong",
           "Taken from the product as it is today, not from a general "
           "theory of onboarding.", 4)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["What is wrong", "Why it costs you users"],
                 [42, 92])
    for head, body in C.DIAGNOSIS:
        put(ws, r, 2, head, bold=True, wrap=True, colour=ACCENT)
        put(ws, r, 3, body, wrap=True, size=9.8)
        ws.row_dimensions[r].height = max(30, 12.4 * (len(body) // 90 + 1))
        r += 1
    r += 1
    r = footnote(ws, r,
                 "The first one is worth the other seven put together. A "
                 "product whose first screen asks for an essay has already "
                 "lost most of the people who will ever see it, and no "
                 "amount of work further down the funnel gets them back.",
                 3)
    return ws


# ----------------------------------------------------------- MEASURE FIRST
def sheet_measure(wb):
    ws = wb.create_sheet("MEASURE FIRST")
    ws.sheet_view.showGridLines = False
    banner(ws, "Weeks one and two: instrument, and change nothing",
           "Shipping before measuring is how a team spends a quarter and "
           "cannot say whether it worked.", 5)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["What to measure", "Type", "Why", "By", "Done?"],
                 [34, 12, 70, 12, 12])
    first = r
    for what, kind, why, when in C.INSTRUMENTATION:
        put(ws, r, 2, what, bold=True, wrap=True, colour=ACCENT)
        put(ws, r, 3, kind, centre=True, size=9.5)
        put(ws, r, 4, why, wrap=True, size=9.8)
        put(ws, r, 5, when, centre=True, size=9.5)
        c = put(ws, r, 6, "", centre=True)
        c.fill = SUNK
        ws.row_dimensions[r].height = max(28, 12.4 * (len(why) // 68 + 1))
        r += 1
    dv = DataValidation(type="list", formula1='"Yes,In progress,No"',
                        allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"F{first}:F{r - 1}")
    r += 1
    r = footnote(ws, r,
                 "Two of these change decisions immediately. Step-level "
                 "drop-off will show that users leave on a specific "
                 "question rather than on a mission, which tells you which "
                 "question to cut. Payment failure by method will show a "
                 "card failure rate that nobody has ever looked at, and in "
                 "this market it is routinely between a third and two "
                 "thirds.", 6)
    return ws


# ------------------------------------------------------------ EXPERIMENTS
def sheet_experiments(wb):
    ws = wb.create_sheet("EXPERIMENTS")
    ws.sheet_view.showGridLines = False
    heads = ["Theme", "Experiment", "Why we think so", "What changes",
             "Primary metric", "Effort", "Expected lift", "Confidence",
             "Run in", "Status", "Owner", "Result"]
    widths = [22, 28, 44, 54, 30, 12, 13, 11, 12, 14, 13, 30]
    r = 1
    for i, (h, w) in enumerate(zip(heads, widths), start=1):
        c = ws.cell(row=r, column=i, value=h)
        c.font = Font(bold=True, size=10, color="FFFFFF")
        c.fill = SUBHEAD
        c.border = BOX
        c.alignment = Alignment(vertical="center", indent=1, wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = ws.cell(row=2, column=3)

    rows = sorted(C.EXPERIMENTS,
                  key=lambda e: (e["theme"], CONF_ORDER[e["confidence"]],
                                 -e["high"]))
    r = 2
    for e in rows:
        put(ws, r, 1, e["theme"], wrap=True, size=9.5, colour="3A4050")
        put(ws, r, 2, e["name"], bold=True, wrap=True, colour=ACCENT)
        put(ws, r, 3, e["hypothesis"], wrap=True, size=9.8)
        put(ws, r, 4, e["change"], wrap=True, size=9.8)
        put(ws, r, 5, e["metric"], wrap=True, size=9.5)
        c = put(ws, r, 6, EFFORT_LABEL[e["effort"]], centre=True)
        c.fill = EFFORT_FILL[e["effort"]]
        c.font = EFFORT_FONT[e["effort"]]
        lift = ("decision" if e["low"] == e["high"] == 1.0
                else f"{e['low']:.1f}x to {e['high']:.1f}x")
        put(ws, r, 7, lift, centre=True, bold=True, colour=ACCENT)
        put(ws, r, 8, e["confidence"], centre=True, size=9.5)
        put(ws, r, 9, e["when"], centre=True, size=9.5)
        for col in (10, 11, 12):
            cell = put(ws, r, col, "", wrap=True)
            cell.fill = SUNK
        ws.cell(row=r, column=10, value="Not started").font = Font(
            size=10, color="6B7A74")
        need = max(len(e["change"]) / 54, len(e["hypothesis"]) / 44,
                   len(e["metric"]) / 30)
        ws.row_dimensions[r].height = max(34, 12.4 * (int(need * 1.12) + 1))
        r += 1

    ws.auto_filter.ref = f"A1:{get_column_letter(len(heads))}{r - 1}"
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUS) + '"',
                        allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"J2:J{r - 1}")
    r += 1
    c = ws.cell(row=r, column=1,
                value="Expected lift is on that experiment's own primary "
                      "metric, not on paid conversion. They do not "
                      "multiply: two activation experiments that both "
                      "move the same metric overlap heavily. Sort by "
                      "theme, run in the order on THE 90 DAYS, and fill "
                      "in the last three columns as you go.")
    c.font = Font(size=9.5, italic=True, color="6B7A74")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
    ws.row_dimensions[r].height = 44
    return ws


# -------------------------------------------------- THE FIRST 10 MINUTES
def sheet_first_ten(wb):
    ws = wb.create_sheet("THE FIRST 10 MINUTES")
    ws.sheet_view.showGridLines = False
    banner(ws, "What a new user should actually see",
           "The current product puts a five-question form here. This is "
           "the replacement, with a clock on it.", 5)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["At", "Screen", "What it does", "Takes"],
                 [10, 22, 86, 14])
    for at, screen, what, takes in C.FIRST_TEN:
        put(ws, r, 2, at, centre=True, bold=True, colour=ACCENT)
        put(ws, r, 3, screen, bold=True, wrap=True)
        put(ws, r, 4, what, wrap=True, size=9.8)
        put(ws, r, 5, takes, centre=True, size=9.5)
        ws.row_dimensions[r].height = max(28, 12.4 * (len(what) // 84 + 1))
        r += 1
    r += 1
    for text in [
        "Three minutes and forty-five seconds from a phone number to a "
        "finished mission, a shareable card, a group of twenty people and "
        "an invited friend. The current flow does not get a user to a "
        "finished anything.",
        "Mission 01's other three questions are not deleted. They move "
        "into mission 02, where a user who has already finished something "
        "will answer them. The content is not the problem; the order is.",
        "Every screen above also works as a WhatsApp conversation, which "
        "is what makes the nudges on the next sheet able to carry a user "
        "forward without an app at all.",
    ]:
        r = footnote(ws, r, text, 5, height=40)
    return ws


# ----------------------------------------------------------------- NUDGES
def sheet_nudges(wb):
    ws = wb.create_sheet("NUDGES")
    ws.sheet_view.showGridLines = False
    banner(ws, "The WhatsApp sequence",
           "Drafts in English, to be written properly in Egyptian Arabic. "
           "Email is close to a no-op with this audience.", 5)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["When", "What it is", "The message", "Who gets it"],
                 [14, 22, 62, 34])
    for when, what, message, who in C.NUDGES:
        put(ws, r, 2, when, centre=True, bold=True, colour=ACCENT)
        put(ws, r, 3, what, bold=True, wrap=True)
        put(ws, r, 4, message, wrap=True, size=9.8)
        put(ws, r, 5, who, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(34, 12.4 * (len(message) // 60 + 1))
        r += 1
    r += 1
    for text in [
        "Every message names the user's own problem back to them. A "
        "message that could have been sent to anybody gets read by "
        "nobody, and 'continue your journey' is the worst sentence in "
        "consumer software.",
        "The last one is the one nobody sends. A payment that fails is "
        "a user who decided to buy and could not, which is the most "
        "valuable user in the whole file. Message them inside five "
        "minutes with a Fawry code and a Vodafone Cash number, and a "
        "meaningful share of them will pay.",
    ]:
        r = footnote(ws, r, text, 5, height=42)
    return ws


# -------------------------------------------------------------- THE MATHS
def sheet_maths(wb):
    ws = wb.create_sheet("THE MATHS")
    ws.sheet_view.showGridLines = False
    banner(ws, "What the funnel does, and what it could do",
           "Every cell below the first row is a formula. Replace the 'now' "
           "column with real numbers and the sheet answers the question "
           "immediately.", 7)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["Stage", "Now", "Target", "Users now",
                         "Users at target", "What moves it"],
                 [30, 11, 11, 13, 15, 58])
    first = r
    for i, (stage, now, tgt, why) in enumerate(C.FUNNEL):
        put(ws, r, 2, stage, bold=True, wrap=True)
        if i == 0:
            put(ws, r, 3, "", centre=True)
            put(ws, r, 4, "", centre=True)
            put(ws, r, 5, now, "#,##0", centre=True, bold=True, fill=SUNK)
            put(ws, r, 6, tgt, "#,##0", centre=True, bold=True, fill=SUNK)
        else:
            put(ws, r, 3, now, "0%", centre=True, fill=SUNK)
            put(ws, r, 4, tgt, "0%", centre=True, bold=True, colour=ACCENT,
                fill=SUNK)
            put(ws, r, 5, f"=E{r-1}*C{r}", "#,##0", centre=True)
            put(ws, r, 6, f"=F{r-1}*D{r}", "#,##0", centre=True,
                bold=True, colour=ACCENT)
        put(ws, r, 7, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(26, 12.4 * (len(why) // 56 + 1))
        r += 1
    last = r - 1

    put(ws, r, 2, "Paid conversion", bold=True, size=11)
    put(ws, r, 5, f"=E{last}/E{first}", "0.00%", centre=True, bold=True,
        size=12, fill=SUNK)
    put(ws, r, 6, f"=F{last}/F{first}", "0.00%", centre=True, bold=True,
        size=12, colour=ACCENT, fill=SUNK)
    put(ws, r, 7, "The number the whole file exists to move.", wrap=True,
        size=9.5, colour="3A4050")
    conv_row = r
    r += 1
    put(ws, r, 2, "Multiple", bold=True)
    put(ws, r, 6, f"=F{conv_row}/E{conv_row}", "0.0x", centre=True,
        bold=True, colour=ACCENT, size=12, fill=SUNK)
    r += 2
    r = footnote(ws, r, C.FUNNEL_WARNING, 7, height=62)
    r = footnote(ws, r,
                 "The 'now' column is illustrative and almost certainly "
                 "wrong in detail. That is the point of MEASURE FIRST: two "
                 "weeks of instrumentation replaces it with the truth, and "
                 "the truth will reorder the experiment sheet.", 7)
    return ws


# ------------------------------------------------------------ THE 90 DAYS
def sheet_plan(wb):
    ws = wb.create_sheet("THE 90 DAYS")
    ws.sheet_view.showGridLines = False
    banner(ws, "The order to do it in",
           "Activation, then habit, then payments, then price. Doing it in "
           "any other order wastes the quarter.", 5)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["When", "What", "What it means", "The number"],
                 [14, 38, 62, 32])
    for when, what, means, number in C.PLAN:
        put(ws, r, 2, when, centre=True, bold=True, colour=ACCENT)
        put(ws, r, 3, what, bold=True, wrap=True)
        put(ws, r, 4, means, wrap=True, size=9.8)
        put(ws, r, 5, number, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(34, 12.4 * (len(means) // 60 + 1))
        r += 1
    r += 2

    ws.cell(row=r, column=2, value="THE RULES").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    for head, body in C.RULES:
        put(ws, r, 2, head, bold=True, wrap=True, colour=ACCENT)
        c = ws.cell(row=r, column=3, value=body)
        c.font = Font(size=9.8)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
        ws.row_dimensions[r].height = max(26, 12.4 * (len(body) // 100 + 1))
        r += 1
    r += 1
    r = footnote(ws, r,
                 "Week seven has one item on it that is not an experiment: "
                 "decide whether Pro is $15 once or $15 a year. The "
                 "financial model carries it as annual and the team "
                 "describes it as one-time. Those are different "
                 "businesses, and only one of them has recurring revenue "
                 "in the plan.", 5)
    return ws


def build(path):
    wb = Workbook()
    wb.remove(wb.active)
    sheet_readme(wb)
    sheet_diagnosis(wb)
    sheet_measure(wb)
    sheet_experiments(wb)
    sheet_first_ten(wb)
    sheet_nudges(wb)
    sheet_maths(wb)
    sheet_plan(wb)
    wb.properties.creator = "StartPad"
    wb.properties.title = "Conversion playbook"
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
               "StartPad_Conversion_Playbook.xlsx"))
    build(out)
    print(f"wrote {out}  ({os.path.getsize(out)/1024:,.0f} KB)")
    print(f"{len(C.EXPERIMENTS)} experiments, {len(C.DIAGNOSIS)} findings")
