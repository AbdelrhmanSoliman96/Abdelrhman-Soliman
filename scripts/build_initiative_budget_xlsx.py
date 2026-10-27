"""Build the budget for One Million First-Time Founders. One page of money."""
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
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
EGPF = '#,##0'


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


def footnote(ws, r, text, last_col, height=44):
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
    f = dict((k, v) for k, v, _ in I.funnel())
    total = I.budget_total()
    ret = sum(v for _, v, _ in I.startpad_return())
    banner(ws, f"{I.NAME}: the budget",
           f"{I.WAVE}. Six lines, {ws and ''}funded entirely by partners.", 5)
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 108

    blocks = [
        ("THE WHOLE THING IN FOUR NUMBERS", ""),
        ("", f"It costs ${total:,.0f}, which is EGP {I.egp(total):,.0f}. It "
             f"registers {f['Registered entrepreneurs']:,.0f} "
             f"entrepreneurs. That is "
             f"${total / f['Registered entrepreneurs']:,.2f} a head. And "
             f"StartPad puts in no cash at all."),
        ("", ""),
        ("WHY IT IS THIS CHEAP", ""),
        ("", "Because there are no paid in-person cohorts in this wave. A "
             "cohort serves 25 people for $3,000. A webinar serves twenty "
             "thousand for $500. Everything is online, everything is free "
             "to the participant, and the offline part happens only where "
             "a partner asks for a session and hosts it in their own "
             "venue with their own people."),
        ("", f"And because the million is not bought, it is referred. "
             f"{I.seed_total():,.0f} registrations come from partner "
             f"channels, chapters and ambassadors; the rest comes from the "
             f"referral loop built into the product. The viral coefficient "
             f"of {I.VIRAL_K:.2f} is the riskiest number in this file and "
             f"the SENSITIVITY sheet shows what happens if it is wrong."),
        ("", ""),
        ("THE SHEETS", ""),
        ("THE BUDGET", "Six lines, in dollars and pounds, and what the "
                       "coalition has to raise to cover them."),
        ("HOW THE MILLION HAPPENS", "The seed channels, the referral loop, "
                                    "and the nine mechanics that make it "
                                    "spread."),
        ("THE FUNNEL", "Registered to finished to trading, with the rate "
                       "behind each step."),
        ("EVENTS AND WEBINARS", "Every event and every piece of live "
                                "delivery, itemised. The two lines "
                                "reconcile to the budget exactly."),
        ("SPEND BY MONTH", "When the money leaves, which is not evenly."),
        ("RETURN ON STARTPAD", "What the company contributes, which is not "
                               "cash, and what comes back in the twelve "
                               "months after."),
        ("SENSITIVITY", "What happens if the loop is weaker, or the "
                        "coalition smaller."),
        ("", ""),
        ("WHAT STARTPAD PUTS IN", ""),
        ("", "No cash. Not a token amount, none. The company contributes "
             "the platform, which is already built and paid for, the "
             "fifteen missions and the review rubric, the team's time, "
             "which is already on its payroll, and five months of "
             "coalition building before any money arrives."),
        ("", f"It also takes no margin from the sponsorship: the budget "
             f"balances to the raise. What it gets back is ${ret:,.0f} of "
             f"commercial revenue in the twelve months after the wave, "
             f"priced at the financial model's own prices, and a set of "
             f"assets it could not otherwise buy. That is on the RETURN ON "
             f"STARTPAD sheet, stated rather than left to a partner's "
             f"imagination."),
        ("", ""),
        ("A WARNING ABOUT THESE NUMBERS", ""),
        ("", "Nothing here is a measured result. Every quantity is an "
             "assumption with its driver written next to it. The viral "
             "coefficient and the completion rates are where being wrong "
             "costs the most, and both are stated so they can be argued "
             "with rather than buried."),
    ]
    prose(ws, blocks, wrap_at=103)
    return ws


# --------------------------------------------------------------- THE BUDGET
def sheet_budget(wb):
    ws = wb.create_sheet("THE BUDGET")
    ws.sheet_view.showGridLines = False
    total = I.budget_total()
    f = dict((k, v) for k, v, _ in I.funnel())
    banner(ws, "Six lines", f"{I.WAVE}. Funded entirely by the coalition. "
                            f"StartPad contributes no cash and takes no "
                            f"margin.", 7)
    ws.column_dimensions["A"].width = 3

    r = 4
    ws.cell(row=r, column=2, value="WHAT IT COSTS").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Line", "USD", "EGP", "Share", "What it is"],
                 [38, 14, 16, 10, 66])
    first = r
    for label, value, note in I.BUDGET:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, MONEY, centre=True, colour=ACCENT, bold=True)
        put(ws, r, 4, f"=C{r}*{I.EGP_PER_USD}", EGPF, centre=True)
        put(ws, r, 5, f"=C{r}/{total}", "0.0%", centre=True)
        put(ws, r, 6, note, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(26, 12.4 * (len(note) // 64 + 1))
        r += 1
    r = total_row(ws, r, "Total cost of the wave",
                  {3: (f"=SUM(C{first}:C{r-1})", MONEY),
                   4: (f"=SUM(D{first}:D{r-1})", EGPF),
                   5: (f"=SUM(E{first}:E{r-1})", "0.0%")})
    cost_row = r - 1
    r += 1

    ws.cell(row=r, column=2, value="WHERE IT COMES FROM").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Tier", "Each", "Slots", "If full", "Who it is for"],
                 [38, 14, 10, 16, 66])
    first = r
    for t in I.TIERS:
        if not t["slots"]:
            continue
        put(ws, r, 2, t["name"], bold=True)
        put(ws, r, 3, t["price"], MONEY, centre=True)
        put(ws, r, 4, t["slots"], "#,##0", centre=True)
        put(ws, r, 5, f"=C{r}*D{r}", MONEY, centre=True, colour=ACCENT,
            bold=True)
        put(ws, r, 6, t["gives"], wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24,
                                          12.4 * (len(t["gives"]) // 64 + 1))
        r += 1
    r = total_row(ws, r, "Coalition capacity",
                  {5: (f"=SUM(E{first}:E{r-1})", MONEY)})
    cap_row = r - 1
    r += 1
    put(ws, r, 2, "Headroom over what the wave needs", bold=True)
    put(ws, r, 5, f"=E{cap_row}-C{cost_row}", MONEY, centre=True, bold=True,
        fill=SUNK)
    put(ws, r, 6, "The coalition can lose four or five conversations and "
                  "still fund the wave. That headroom is the plan, not "
                  "optimism.", wrap=True, size=9.5, colour="3A4050")
    ws.row_dimensions[r].height = 30
    r += 2

    ws.cell(row=r, column=2, value="WHAT IT WORKS OUT AT").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Measure", "USD", "EGP", "", ""],
                 [38, 14, 16, 10, 66])
    for label, value in I.unit_costs():
        put(ws, r, 2, label, bold=True)
        put(ws, r, 3, round(value, 2), MONEY2, centre=True, colour=ACCENT,
            bold=True)
        put(ws, r, 4, round(value * I.EGP_PER_USD, 2), "#,##0.00",
            centre=True)
        put(ws, r, 5, "")
        put(ws, r, 6, "")
        r += 1
    r += 1
    r = footnote(ws, r,
                 f"Twenty cents a head is not a number a corporate "
                 f"programme can reach on its own, and it is the whole "
                 f"argument for a coalition. The cost per entrepreneur who "
                 f"finishes all fifteen missions, "
                 f"${I.budget_total() / f['All 15 missions completed']:,.2f}, "
                 f"is the number to compare against anything else a partner "
                 f"funds, because that is a person who took an idea to a "
                 f"tested model, a prototype and a launch plan.", 6)
    return ws


# ------------------------------------------------- HOW THE MILLION HAPPENS
def sheet_viral(wb):
    ws = wb.create_sheet("HOW THE MILLION HAPPENS")
    ws.sheet_view.showGridLines = False
    banner(ws, "Seeded by partners, carried by the loop",
           "A million is not bought. It is referred.", 7)
    ws.column_dimensions["A"].width = 3

    r = 4
    ws.cell(row=r, column=2, value="THE SEED").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    r = row_head(ws, r, ["Channel", "How many", "Each", "Registrations",
                         "Why"], [30, 11, 12, 15, 72])
    first = r
    for label, num, per, why in I.SEED:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, num, "#,##0", centre=True)
        put(ws, r, 4, per, "#,##0", centre=True)
        put(ws, r, 5, f"=C{r}*D{r}", "#,##0", centre=True, colour=ACCENT,
            bold=True)
        put(ws, r, 6, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(26, 12.4 * (len(why) // 70 + 1))
        r += 1
    r = total_row(ws, r, "Seed registrations",
                  {5: (f"=SUM(E{first}:E{r-1})", "#,##0")})
    seed_row = r - 1
    r += 1

    put(ws, r, 2, "Viral coefficient", bold=True)
    put(ws, r, 5, I.VIRAL_K, "0.00", centre=True, colour=ACCENT, bold=True,
        fill=SUNK, size=12)
    put(ws, r, 6, "Each registered entrepreneur brings this many more "
                  "across the wave, through the referral unlock on mission "
                  "04 and the shareable card after every mission.",
        wrap=True, size=9.5, colour="3A4050")
    ws.row_dimensions[r].height = 32
    k_row = r
    r += 1
    put(ws, r, 2, "Multiplier", bold=True)
    put(ws, r, 5, f"=1/(1-E{k_row})", "0.00x", centre=True)
    put(ws, r, 6, "The sum of the series, not a guess.", wrap=True,
        size=9.5, colour="3A4050")
    r += 1
    put(ws, r, 2, "Registered entrepreneurs", bold=True, size=11)
    put(ws, r, 5, f"=E{seed_row}/(1-E{k_row})", "#,##0", centre=True,
        colour=ACCENT, bold=True, size=13, fill=SUNK)
    put(ws, r, 6, "The million.", wrap=True, size=9.5, colour="3A4050")
    ws.row_dimensions[r].height = 24
    r += 2

    ws.cell(row=r, column=2, value="THE NINE MECHANICS").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    for head, body in I.VIRAL_LOOPS:
        put(ws, r, 2, head, bold=True, wrap=True, colour=ACCENT)
        c = ws.cell(row=r, column=3, value=body)
        c.font = Font(size=9.8)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
        ws.row_dimensions[r].height = max(26, 12.4 * (len(body) // 110 + 1))
        r += 1
    r += 1
    r = footnote(ws, r,
                 "The loop is in the product, not in a campaign. Mission 04 "
                 "opens when a founder brings two others who finish mission "
                 "01, and every mission finished generates a card in Arabic "
                 "designed to be posted. A referral scheme bolted on at "
                 "launch does not produce a coefficient like this; one "
                 "built into the thing itself might.", 6)
    return ws


# --------------------------------------------------------------- THE FUNNEL
def sheet_funnel(wb):
    ws = wb.create_sheet("THE FUNNEL")
    ws.sheet_view.showGridLines = False
    banner(ws, "Registered, finished, trading",
           "Free and online, with no facilitator standing over anybody. "
           "The rates reflect that.", 6)
    ws.column_dimensions["A"].width = 3
    r = 4
    r = row_head(ws, r, ["Stage", "Wave 1", "What it means"],
                 [34, 16, 92])
    for label, value, why in I.funnel():
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, round(value), "#,##0", centre=True, bold=True,
            colour=ACCENT, size=11)
        put(ws, r, 4, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(why) // 90 + 1))
        r += 1
    r += 1
    ws.cell(row=r, column=2, value="THE RATES, AND WHY EACH ONE").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    r = row_head(ws, r, ["Rate", "Assumed", "Why"], [34, 16, 92])
    for label, value, why in I.RATES:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, "0%", centre=True, bold=True, colour=ACCENT)
        put(ws, r, 4, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(why) // 90 + 1))
        r += 1
    r += 1
    r = footnote(ws, r,
                 "Forty-five per cent finishing mission 01 is lower than a "
                 "supported cohort would produce, and honestly so: nobody "
                 "is holding anyone's hand. The headline the initiative "
                 "publishes is the completion rate, not the registration "
                 "number, because a million registrations with nothing "
                 "behind them would be worth nothing to any partner on the "
                 "list.", 4)
    return ws


# -------------------------------------------------------- EVENTS & WEBINARS
def sheet_events(wb):
    ws = wb.create_sheet("EVENTS AND WEBINARS")
    ws.sheet_view.showGridLines = False
    banner(ws, "Everything that happens live",
           "There are no paid in-person cohorts in this wave. This is the "
           "whole of what happens in a room or on a call.", 7)
    ws.column_dimensions["A"].width = 3

    r = 4
    for title, items, line in [
        ("EVENTS", I.EVENTS, "Events: launch, regional showcases, demo day"),
        ("LIVE DELIVERY AND CONTENT", I.DELIVERY,
         "Content, webinars and the info session kit"),
    ]:
        ws.cell(row=r, column=2, value=title).font = Font(
            bold=True, size=11, color=ACCENT)
        r += 1
        r = row_head(ws, r, ["Item", "How many", "Each", "Total", "When",
                             "What it is for"],
                     [28, 11, 11, 13, 20, 60])
        first = r
        for label, count, cost, when, why in items:
            put(ws, r, 2, label, bold=True, wrap=True)
            put(ws, r, 3, count, "#,##0", centre=True)
            put(ws, r, 4, cost, MONEY, centre=True)
            put(ws, r, 5, f"=C{r}*D{r}", MONEY, centre=True, colour=ACCENT,
                bold=True)
            put(ws, r, 6, when, centre=True, size=9.5)
            put(ws, r, 7, why, wrap=True, size=9.5, colour="3A4050")
            ws.row_dimensions[r].height = max(26, 12.4 * (len(why) // 58 + 1))
            r += 1
        budget_line = dict((l, v) for l, v, _ in I.BUDGET)[line]
        r = total_row(ws, r, f"Total, against a budget line of "
                             f"${budget_line:,.0f}",
                      {5: (f"=SUM(E{first}:E{r-1})", MONEY)})
        r += 1

    r = footnote(ws, r,
                 "Offline info sessions are hosted by partners: their "
                 "venue, their people, our kit and our training. The "
                 "initiative pays $20 for a kit, not for a room, which is "
                 "why 300 of them cost less than two in-person cohorts "
                 "would. Where they happen, and how many, is a partner's "
                 "call rather than ours.", 7)
    return ws


# ----------------------------------------------------------- SPEND BY MONTH
SPEND_SHAPE = {
    "Platform, AI review and hosting": (0.10, 0.15, 0.18, 0.19, 0.20, 0.18),
    "Content, webinars and the info session kit":
        (0.30, 0.16, 0.14, 0.14, 0.14, 0.12),
    "Community: ambassadors and chapters":
        (0.30, 0.20, 0.14, 0.12, 0.12, 0.12),
    "Events: launch, regional showcases, demo day":
        (0.24, 0.03, 0.03, 0.09, 0.41, 0.20),
    "Measurement, reporting and evaluation":
        (0.10, 0.05, 0.20, 0.05, 0.10, 0.50),
    "Programme coordination": (0.17, 0.17, 0.17, 0.17, 0.16, 0.16),
}


def sheet_months(wb):
    ws = wb.create_sheet("SPEND BY MONTH")
    ws.sheet_view.showGridLines = False
    f = dict((k, v) for k, v, _ in I.funnel())
    banner(ws, "When the money leaves, and where the million is by then",
           "Not evenly. The launch, the content and most of the ambassador "
           "recruitment happen before the loop has produced anybody.", 9)
    ws.column_dimensions["A"].width = 3
    heads = ["Line"] + [f"{m[0]}\n{m[1].split()[0]}" for m in I.MONTHS] \
        + ["Total"]
    r = 4
    r = row_head(ws, r, heads, [34] + [12] * 6 + [14])
    first = r
    for label, value, _ in I.BUDGET:
        put(ws, r, 2, label, bold=True, wrap=True)
        for i in range(6):
            put(ws, r, 3 + i, value * SPEND_SHAPE[label][i], MONEY,
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
    put(ws, r, 2, "Cumulative spend", bold=True)
    for i in range(6):
        col = get_column_letter(3 + i)
        put(ws, r, 3 + i, f"=SUM($C${r-1}:{col}{r-1})", MONEY, centre=True,
            fill=SUNK)
    r += 1
    put(ws, r, 2, "Registered by month end", bold=True)
    for i, m in enumerate(I.MONTHS):
        put(ws, r, 3 + i, round(f["Registered entrepreneurs"] * m[4]),
            "#,##0", centre=True, colour=ACCENT, bold=True)
    put(ws, r, 9, round(f["Registered entrepreneurs"]), "#,##0",
        centre=True, bold=True)
    r += 2
    r = footnote(ws, r,
                 "Roughly a third of the content and community budgets go "
                 "before the launch, and the launch itself is in month one. "
                 "Sponsorship is invoiced on signature rather than on "
                 "delivery, so the coalition has to be signed and at least "
                 "half invoiced before March. That is what the pre-wave "
                 "months from October 2026 are for, and why nothing is "
                 "announced until both Founding Partners have signed.", 9)
    return ws


# ------------------------------------------------------- RETURN ON STARTPAD
def sheet_return(wb):
    ws = wb.create_sheet("RETURN ON STARTPAD")
    ws.sheet_view.showGridLines = False
    ret = I.startpad_return()
    total = sum(v for _, v, _ in ret)
    banner(ws, "No cash in, and what comes back",
           "StartPad funds none of this wave and takes no margin from it. "
           "A partner is entitled to know what the company gets instead.",
           6)
    ws.column_dimensions["A"].width = 3

    r = 4
    ws.cell(row=r, column=2,
            value="WHAT STARTPAD CONTRIBUTES, NONE OF IT CASH").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    for head, body in I.STARTPAD_CONTRIBUTION:
        put(ws, r, 2, head, bold=True, wrap=True, colour=ACCENT)
        c = ws.cell(row=r, column=3, value=body)
        c.font = Font(size=9.8)
        c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
        ws.row_dimensions[r].height = max(26, 12.4 * (len(body) // 108 + 1))
        r += 1
    r += 1

    ws.cell(row=r, column=2,
            value="WHAT COMES BACK IN THE TWELVE MONTHS AFTER").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    r = row_head(ws, r, ["Line", "USD", "EGP", "How it is counted"],
                 [40, 14, 16, 60])
    first = r
    for label, value, note in ret:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, MONEY, centre=True, colour=ACCENT, bold=True)
        put(ws, r, 4, f"=C{r}*{I.EGP_PER_USD}", EGPF, centre=True)
        put(ws, r, 5, note, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(note) // 58 + 1))
        r += 1
    r = total_row(ws, r, "Total, twelve months after the wave",
                  {3: (f"=SUM(C{first}:C{r-1})", MONEY),
                   4: (f"=SUM(D{first}:D{r-1})", EGPF)})
    r += 1

    ws.cell(row=r, column=2, value="THE RATES BEHIND THOSE LINES").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    r = row_head(ws, r, ["Rate", "Assumed", "", "Why"], [40, 14, 16, 60])
    for label, value, why in I.RETURN_RATES:
        put(ws, r, 2, label, bold=True, wrap=True)
        put(ws, r, 3, value, "0%", centre=True, bold=True, colour=ACCENT)
        put(ws, r, 4, "")
        put(ws, r, 5, why, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(24, 12.4 * (len(why) // 58 + 1))
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
        ws.row_dimensions[r].height = max(26, 12.4 * (len(body) // 108 + 1))
        r += 1
    r += 1
    r = footnote(ws, r,
                 f"The honest summary: the company spends no money on this "
                 f"and makes none from it directly, and gets about "
                 f"${total:,.0f} of commercial revenue in the following "
                 f"year plus a million registered entrepreneurs, a data "
                 f"asset nobody else in Egypt has, and a measured referral "
                 f"coefficient. If these rates are half right it is still "
                 f"the best twelve months of business development the "
                 f"company could buy, and it is being funded by somebody "
                 f"else.", 6, height=56)
    return ws


# -------------------------------------------------------------- SENSITIVITY
def sheet_sensitivity(wb):
    ws = wb.create_sheet("SENSITIVITY")
    ws.sheet_view.showGridLines = False
    banner(ws, "If the loop is weaker, or the coalition smaller",
           "Two things can go wrong with this plan, and they go wrong "
           "independently.", 7)
    ws.column_dimensions["A"].width = 3

    r = 4
    ws.cell(row=r, column=2, value="IF THE VIRAL COEFFICIENT IS WRONG").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    r = row_head(ws, r, ["Coefficient", "Multiplier", "Registered",
                         "Cost per head", "What it means"],
                 [14, 13, 16, 14, 72])
    seed = I.seed_total()
    for k in (0.25, 0.40, 0.50, 0.60):
        reg = seed / (1 - k)
        meaning = {
            0.25: "The loop barely fires and the wave is carried by the "
                  "partner channels alone. Still two thirds of a million, "
                  "and still the largest entrepreneurship programme ever "
                  "run in Egypt.",
            0.40: "Below plan but comfortably viable. The headline becomes "
                  "830,000 and the completion numbers barely move.",
            0.50: "The plan. Every registered entrepreneur brings one more "
                  "across six months.",
            0.60: "Above plan. The constraint stops being reach and "
                  "becomes inference cost, which is the good problem.",
        }[k]
        put(ws, r, 2, k, "0.00", centre=True, bold=True, colour=ACCENT,
            size=12)
        put(ws, r, 3, f"=1/(1-B{r})", "0.00x", centre=True)
        put(ws, r, 4, round(reg), "#,##0", centre=True, bold=True)
        put(ws, r, 5, round(I.budget_total() / reg, 2), MONEY2,
            centre=True)
        put(ws, r, 6, meaning, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(30, 12.4 * (len(meaning) // 70 + 1))
        if k == I.VIRAL_K:
            for col in range(2, 7):
                ws.cell(row=r, column=col).fill = CONF_FILL["high"]
        r += 1
    r += 1

    ws.cell(row=r, column=2, value="IF THE COALITION DOES NOT FILL").font = (
        Font(bold=True, size=11, color=ACCENT))
    r += 1
    r = row_head(ws, r, ["Fill", "Raised", "EGP", "Gap", "What gets cut"],
                 [14, 13, 16, 14, 72])
    for fill in (0.40, 0.60, 0.80, 1.00):
        raised = I.raised(fill)
        gap = I.budget_total() - raised
        cut = {
            0.40: "Below the floor. The wave is postponed rather than run "
                  "badly, and the coalition is rebuilt for the autumn.",
            0.60: "The regional showcases drop from six to two and the "
                  "ambassador programme halves. Reach suffers, and so does "
                  "the loop.",
            0.80: "The plan. Everything in the budget runs.",
            1.00: "The extra goes to ambassadors and to a second language "
                  "pass, not to the surplus. There is no surplus.",
        }[fill]
        put(ws, r, 2, f"{fill:.0%}", centre=True, bold=True, colour=ACCENT,
            size=12)
        put(ws, r, 3, raised, MONEY, centre=True, bold=True)
        put(ws, r, 4, round(I.egp(raised)), EGPF, centre=True)
        c = put(ws, r, 5, gap, MONEY, centre=True)
        if gap > 0:
            c.fill = CONF_FILL["low"]
            c.font = CONF_FONT["low"]
        put(ws, r, 6, cut, wrap=True, size=9.5, colour="3A4050")
        ws.row_dimensions[r].height = max(30, 12.4 * (len(cut) // 70 + 1))
        if fill == I.TARGET_FILL:
            for col in range(2, 7):
                if col != 5:
                    ws.cell(row=r, column=col).fill = CONF_FILL["high"]
        r += 1
    r += 1
    r = footnote(ws, r,
                 "The two risks are independent, which is the comfort in "
                 "this plan. A weak loop with a full coalition still "
                 "reaches two thirds of a million. A strong loop with a "
                 "thin coalition still reaches a million, with fewer "
                 "showcases. Both failing together is the case to watch, "
                 "and the mid-wave report in May is the decision point.", 6)
    return ws


def build(path):
    wb = Workbook()
    wb.remove(wb.active)
    sheet_readme(wb)
    sheet_budget(wb)
    sheet_viral(wb)
    sheet_funnel(wb)
    sheet_events(wb)
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
    f = dict((k, v) for k, v, _ in I.funnel())
    print(f"wrote {out}  ({os.path.getsize(out)/1024:,.0f} KB)")
    print(f"${I.budget_total():,.0f} for "
          f"{f['Registered entrepreneurs']:,.0f} entrepreneurs, "
          f"${I.budget_total() / f['Registered entrepreneurs']:,.2f} a head")
