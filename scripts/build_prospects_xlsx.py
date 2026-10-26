"""Build the Egypt CSR, NGO and youth organisation prospect registry."""
import math
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from outreach.prospects import (  # noqa: E402
    BANDS, CATEGORIES, DOCUMENTS, MESSAGES, PLAYBOOK, PROSPECTS, SEQUENCE,
    TIERS,
)
from scripts._determinism import FIXED_TIMESTAMP, normalize_zip  # noqa: E402

INK = "16211E"
ACCENT = "0F5C4B"
HEAD = PatternFill("solid", fgColor="0F5C4B")
SUBHEAD = PatternFill("solid", fgColor="2E6F5E")
SUNK = PatternFill("solid", fgColor="ECF0EE")
THIN = Side(style="thin", color="D9E2DE")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

CONF_FILL = {
    "high": PatternFill("solid", fgColor="D7EBE3"),
    "medium": PatternFill("solid", fgColor="F5EAD5"),
    "low": PatternFill("solid", fgColor="F7DDD3"),
}
CONF_FONT = {
    "high": Font(size=10, bold=True, color="0F5C4B"),
    "medium": Font(size=10, bold=True, color="8A6E3C"),
    "low": Font(size=10, bold=True, color="B4531C"),
}
TIER_FILL = {
    "A": PatternFill("solid", fgColor="0F5C4B"),
    "B": PatternFill("solid", fgColor="BFD8CF"),
    "C": PatternFill("solid", fgColor="ECF0EE"),
}
TIER_FONT = {
    "A": Font(size=10, bold=True, color="FFFFFF"),
    "B": Font(size=10, bold=True, color="0F5C4B"),
    "C": Font(size=10, bold=True, color="6B7A74"),
}

STAGES = ["Not started", "Researching", "Message sent", "Meeting booked",
          "Meeting held", "Proposal sent", "Negotiating", "Won", "Lost",
          "Parked"]


def banner(ws, title, subtitle, width):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=width)
    c = ws.cell(row=1, column=1, value=title)
    c.font = Font(size=15, bold=True, color="FFFFFF")
    c.fill = HEAD
    c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[1].height = 28
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=width)
    c = ws.cell(row=2, column=1, value=subtitle)
    c.font = Font(size=10, italic=True, color=INK)
    c.fill = SUNK
    c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[2].height = 19


def header(ws, row, headers, widths, freeze_col=1):
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = SUBHEAD
        c.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
        c.border = BOX
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 32
    ws.freeze_panes = ws.cell(row=row + 1, column=freeze_col)


def prose(ws, blocks, start=4, label_col=2, text_col=3, wrap_at=105):
    r = start
    for label, text in blocks:
        if label and not text:
            c = ws.cell(row=r, column=label_col, value=label)
            c.font = Font(bold=True, size=11, color=ACCENT)
        elif label:
            c = ws.cell(row=r, column=label_col, value=label)
            c.font = Font(bold=True, size=10, color=INK)
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c2 = ws.cell(row=r, column=text_col, value=text)
            c2.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r].height = max(15, 13 * (len(text) // wrap_at + 1))
        elif text:
            c2 = ws.cell(row=r, column=text_col, value=text)
            c2.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r].height = max(15, 13 * (len(text) // wrap_at + 1))
        r += 1
    return r


# ------------------------------------------------------------------ READ ME
def sheet_readme(wb):
    ws = wb.create_sheet("READ ME FIRST")
    ws.sheet_view.showGridLines = False
    banner(ws, "One Million Entrepreneurs in Egypt: prospect registry",
           "Corporates with CSR, foundations, donors, NGOs and youth "
           "organisations. Who they are, what they want, and how to reach "
           "them.", 5)
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 108

    counts = {}
    for p in PROSPECTS:
        counts[p["cat"]] = counts.get(p["cat"], 0) + 1
    tier_a = [p for p in PROSPECTS if p["tier"] == "A"]

    blocks = [
        ("WHAT THIS IS", ""),
        ("", f"{len(PROSPECTS)} organisations in Egypt that could fund, host "
             f"or carry the One Million Entrepreneurs initiative, across "
             f"{len(CATEGORIES)} categories. One row per organisation. For "
             f"each: what they actually fund, why they fit, what they are "
             f"looking for in return, the concrete thing to ask them for, "
             f"who decides, how to reach them, and when."),
        ("", "A few rows are categories rather than single organisations "
             "(the second-tier corporate foundations, the mass charities, "
             "the smaller bilateral agencies). That is deliberate. A "
             "pipeline built only from famous names is a pipeline that "
             "misses most of the available money."),
        ("", ""),
        ("THE SHEETS", ""),
        ("PROSPECTS", "The registry. Filter by category, tier or confidence. "
                      "The last five columns are yours to fill in: stage, "
                      "owner, next action, next date, notes."),
        ("HOW TO REACH THEM", "One row per category: where the money sits, "
                              "who decides, what they are measured on, the "
                              "objection that kills it, the proof that "
                              "answers it, and the budget cycle. This is "
                              "the sheet that stops the registry being a "
                              "list of names."),
        ("WHAT THEY WANT", "The same thing from the other side: read this "
                           "before writing to anyone, because every one of "
                           "these organisations is buying its own outcome, "
                           "not our programme."),
        ("FIRST MESSAGES", "Six templates, one per type. Square brackets are "
                           "the only things to change."),
        ("FOLLOW-UP", "What happens after the first message, because almost "
                      "nothing closes on it."),
        ("DOCUMENTS", "What has to exist before the first serious meeting. "
                      "Several of these disqualify a bid on their own."),
        ("PIPELINE MATH", "How many of these have to be worked to land the "
                          "contracts the plan needs."),
        ("", ""),
        ("READ THE CONFIDENCE COLUMN BEFORE QUOTING ANYTHING", ""),
        ("high", "The organisation exists, its CSR or programme area is well "
                 "established, and nothing in the row depends on a cycle "
                 "that may have closed. Several of these were confirmed in "
                 "published sources while this file was compiled."),
        ("medium", "Organisation and focus are established. The specific "
                   "programme, budget line or route named here changes "
                   "between cycles and must be re-checked before it is "
                   "quoted to anyone, inside or outside the company."),
        ("low", "A reasoned prospect, not a confirmed one. Verify that the "
                "programme still exists before spending a meeting on it."),
        ("", f"Counts: {sum(1 for p in PROSPECTS if p['conf']=='high')} high, "
             f"{sum(1 for p in PROSPECTS if p['conf']=='medium')} medium, "
             f"{sum(1 for p in PROSPECTS if p['conf']=='low')} low."),
        ("", ""),
        ("WHAT THIS FILE DOES NOT CONTAIN", ""),
        ("No names", "There is not one individual's name, email address or "
                     "phone number in this file, by choice. Named contacts "
                     "go stale faster than anything else in a registry and a "
                     "wrong one burns the introduction. Every route is an "
                     "organisational door: a published channel, a role to "
                     "ask for, or an intermediary who can introduce. Add the "
                     "names yourself as you earn them."),
        ("No verified URLs", "No page was opened while this was compiled. "
                             "Where a site or portal is named, find it "
                             "yourself rather than trusting a URL typed from "
                             "memory."),
        ("No promises about budgets", "The ticket bands are planning "
                                      "assumptions for sizing the pipeline, "
                                      "not quotes. The first real "
                                      "conversation replaces them."),
        ("", ""),
        ("WHERE TO START", ""),
        ("", f"{len(tier_a)} organisations are tier A: either the budget "
             f"line already exists or the relationship opens several others. "
             f"Working those before anything else is the whole strategy."),
        ("", "The five that change the company if they land: Rowad 2030 "
             "(the initiative itself, and the name that opens the rest), "
             "GIZ Egypt (contracts delivery and already funds this exact "
             "activity), Drosos Foundation (runs the same funnel, in the "
             "right governorates), Orange Egypt and NBE (already pay for "
             "student entrepreneurship), and INJAZ Egypt or Enactus Egypt "
             "(the reach, without the method)."),
        ("", "Two warnings that will save a quarter each. The CIB "
             "Foundation is a health and nutrition funder, so the "
             "entrepreneurship ask belongs to CIB's SME banking side, not "
             "to the foundation. And the Mastercard Foundation's Egypt "
             "status is unverified here, so check it before building a plan "
             "around the biggest number in this file."),
        ("", ""),
        ("TIERS", ""),
    ] + [(t, why) for t, why in TIERS.items()] + [
        ("", ""),
        ("TICKET BANDS", ""),
        ("", "Planning assumptions for sizing the pipeline. Not quotes. The "
             "first real conversation replaces them."),
    ] + [(b, why) for b, why in BANDS.items()] + [
        ("", ""),
        ("CATEGORIES", ""),
    ]
    for cat in CATEGORIES:
        blocks.append((cat, f"{counts.get(cat, 0)} organisations"))
    r = prose(ws, blocks)
    return ws


# ---------------------------------------------------------------- PROSPECTS
COLS = [
    ("name", "Organisation", 34), ("arabic", "Arabic name", 22),
    ("cat", "Category", 26), ("sector", "Sector", 24),
    ("reach", "Reach", 24), ("tier", "Tier", 7),
    ("focus", "What they actually fund", 58),
    ("fit", "Why they are a prospect", 58),
    ("want", "What they are looking for", 48),
    ("ask", "What to ask them for", 46),
    ("band", "Ticket band", 11),
    ("unit", "Who decides", 38),
    ("route", "How to reach them", 52),
    ("window", "When to approach", 34),
    ("conf", "Confidence", 11),
    ("note", "Verify this before quoting", 50),
]
OWN = [("Stage", 18), ("Owner", 16), ("Next action", 34), ("Next date", 14),
       ("Notes", 40)]
WRAP = {"name", "focus", "fit", "want", "ask", "unit", "route", "window",
        "note", "reach", "sector", "cat", "arabic"}


def sheet_prospects(wb):
    ws = wb.create_sheet("PROSPECTS")
    ws.sheet_view.showGridLines = False
    heads = [c[1] for c in COLS] + [o[0] for o in OWN]
    widths = [c[2] for c in COLS] + [o[1] for o in OWN]
    header(ws, 1, heads, widths, freeze_col=2)

    order = {c: i for i, c in enumerate(CATEGORIES)}
    tier_order = {"A": 0, "B": 1, "C": 2}
    rows = sorted(PROSPECTS,
                  key=lambda p: (order[p["cat"]], tier_order[p["tier"]],
                                 p["name"]))
    r = 2
    for p in rows:
        for i, (key, _, _) in enumerate(COLS, start=1):
            c = ws.cell(row=r, column=i, value=p[key])
            c.border = BOX
            c.font = Font(size=10)
            c.alignment = Alignment(wrap_text=key in WRAP, vertical="top",
                                    indent=1)
        ws.cell(row=r, column=1).font = Font(size=10, bold=True, color=ACCENT)
        if p["arabic"]:
            ws.cell(row=r, column=2).alignment = Alignment(
                horizontal="right", vertical="top", wrap_text=True)
        t = ws.cell(row=r, column=6)
        t.fill = TIER_FILL[p["tier"]]
        t.font = TIER_FONT[p["tier"]]
        t.alignment = Alignment(horizontal="center", vertical="top")
        cf = ws.cell(row=r, column=15)
        cf.fill = CONF_FILL[p["conf"]]
        cf.font = CONF_FONT[p["conf"]]
        cf.alignment = Alignment(horizontal="center", vertical="top")
        b = ws.cell(row=r, column=11)
        b.alignment = Alignment(horizontal="center", vertical="top")
        b.font = Font(size=10, bold=True, color=INK)
        for i in range(len(COLS) + 1, len(COLS) + len(OWN) + 1):
            cell = ws.cell(row=r, column=i)
            cell.border = BOX
            cell.fill = SUNK
            cell.alignment = Alignment(wrap_text=True, vertical="top",
                                       indent=1)
        ws.cell(row=r, column=len(COLS) + 1, value="Not started").font = Font(
            size=10, color="6B7A74")
        # Row height is driven by the longest wrapped cell, measured against
        # its own column width rather than a single average, because the fit
        # and focus columns are three times the width of the reach column.
        # Excel wraps on word boundaries, so a column fits fewer characters
        # than its width suggests. The 1.12 is that loss; the extra line is
        # the margin that keeps a long cell from being clipped.
        need = max((len(str(p[k])) / dict((c[0], c[2]) for c in COLS)[k]
                    for k in WRAP if p[k]), default=1)
        ws.row_dimensions[r].height = max(30, 12.2 * (math.ceil(need * 1.12)
                                                      + 1))
        r += 1

    last = get_column_letter(len(COLS) + len(OWN))
    ws.auto_filter.ref = f"A1:{last}{r - 1}"
    dv = DataValidation(type="list", formula1='"' + ",".join(STAGES) + '"',
                        allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"{get_column_letter(len(COLS) + 1)}2:"
           f"{get_column_letter(len(COLS) + 1)}{r - 1}")
    return ws


# -------------------------------------------------------- HOW TO REACH THEM
def sheet_playbook(wb):
    ws = wb.create_sheet("HOW TO REACH THEM")
    ws.sheet_view.showGridLines = False
    cols = [("cat", "Category", 26), ("money", "Where the money sits", 50),
            ("decides", "Who decides", 48),
            ("measured", "What they are measured on", 48),
            ("objection", "The objection that kills it", 34),
            ("proof", "What answers it", 54),
            ("cycle", "Budget cycle", 40),
            ("first", "The first move", 48)]
    header(ws, 1, [c[1] for c in cols], [c[2] for c in cols], freeze_col=2)
    order = {c: i for i, c in enumerate(CATEGORIES)}
    r = 2
    for e in sorted(PLAYBOOK, key=lambda e: order[e["cat"]]):
        for i, (k, _, _) in enumerate(cols, start=1):
            c = ws.cell(row=r, column=i, value=e[k])
            c.border = BOX
            c.font = Font(size=10)
            c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.cell(row=r, column=1).font = Font(size=10, bold=True, color=ACCENT)
        ws.cell(row=r, column=5).font = Font(size=10, italic=True,
                                             color="B4531C")
        need = max(len(e[k]) / dict((c[0], c[2]) for c in cols)[k]
                   for k, _, _ in cols)
        ws.row_dimensions[r].height = max(34, 12.2 * (math.ceil(need * 1.12)
                                                      + 1))
        r += 1
    return ws


# ------------------------------------------------------------ WHAT THEY WANT
def sheet_wants(wb):
    ws = wb.create_sheet("WHAT THEY WANT")
    ws.sheet_view.showGridLines = False
    banner(ws, "What each kind of funder is actually buying",
           "Nobody in this file wants to fund entrepreneurship training. "
           "They each want their own outcome, and the training is how they "
           "get it.", 4)
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 108

    blocks = [
        ("THE RULE", ""),
        ("", "Every proposal in this file should be written in the funder's "
             "own words for their own outcome, with our programme as the "
             "method. A proposal that opens with what StartPad is has "
             "already lost the reader. A proposal that opens with their "
             "target, their governorate or their reporting obligation has "
             "their attention for the second paragraph."),
        ("", ""),
        ("WHAT EACH ONE IS BUYING", ""),
    ]
    for e in sorted(PLAYBOOK,
                    key=lambda e: CATEGORIES.index(e["cat"])):
        blocks.append((e["cat"], e["measured"]))
    blocks += [
        ("", ""),
        ("THE FIVE THINGS THEY ALL ASK FOR", ""),
        ("A number", "How many young people, by when, in which "
                     "governorates, and how many of them women. Every single "
                     "one of them asks this. Have it ready before the "
                     "meeting, and have it ready as a range with an "
                     "assumption attached, not as a promise."),
        ("A unit cost", "Cost per participant and cost per business still "
                        "operating twelve months later. The second number is "
                        "the one that separates a serious provider from a "
                        "training vendor, and almost nobody can answer it."),
        ("Proof it works", "Not testimonials. Completion rates, the "
                           "proportion still trading, and a cohort report "
                           "with named institutions. Until these exist, "
                           "borrow them: deliver as a sub-contractor to an "
                           "organisation that has them."),
        ("Proof you will not embarrass them", "Registration, audited "
                                              "accounts, safeguarding "
                                              "policy, data protection, and "
                                              "insurance. This is the "
                                              "DOCUMENTS sheet and it is "
                                              "boring and it disqualifies "
                                              "more bids than quality ever "
                                              "does."),
        ("Something they can publish", "A report, a photograph, a graduate "
                                       "with a name and a business, a "
                                       "number they can put in their own "
                                       "annual report. Build the publishable "
                                       "artefact into the delivery, not into "
                                       "an afterthought."),
        ("", ""),
        ("WHAT NONE OF THEM WANT", ""),
        ("A platform demo", "The product is interesting to us and not to "
                            "them. Show the cohort report instead, which is "
                            "the thing they keep."),
        ("A sponsorship request", "Asking for money to support a good cause "
                                  "puts the request in the charity queue, "
                                  "which is the slowest and smallest queue "
                                  "there is. Ask them to buy an outcome "
                                  "instead."),
        ("A partnership with no number in it", "Memoranda that commit "
                                               "nobody to anything are easy "
                                               "to sign and worth nothing. "
                                               "Put the number of young "
                                               "people in the memorandum."),
        ("To build something", "Every funder in this file has been asked to "
                               "fund the creation of a curriculum. Ours "
                               "exists. Say so in the first paragraph; it is "
                               "the strongest sentence available."),
    ]
    prose(ws, blocks)
    return ws


# ----------------------------------------------------------- FIRST MESSAGES
def sheet_messages(wb):
    ws = wb.create_sheet("FIRST MESSAGES")
    ws.sheet_view.showGridLines = False
    header(ws, 1, ["Template", "Use it for", "Text"], [30, 34, 110])
    r = 2
    for title, use, text in MESSAGES:
        for i, v in enumerate([title, use, text], start=1):
            c = ws.cell(row=r, column=i, value=v)
            c.border = BOX
            c.font = Font(size=10)
            c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.cell(row=r, column=1).font = Font(size=10, bold=True, color=ACCENT)
        lines = text.count("\n") + sum(len(x) // 108 for x in text.split("\n"))
        ws.row_dimensions[r].height = max(40, 12.6 * (lines + 2))
        r += 1
    ws.cell(row=r + 1, column=1,
            value="Write in Arabic to Egyptian NGOs, youth organisations, "
                  "ministries and most Egyptian corporates. Write in English "
                  "to development agencies, UN agencies, international NGOs "
                  "and multinational corporate affairs teams. Writing in the "
                  "wrong one is not fatal, but writing in Arabic to a "
                  "ministry is worth more than any other single thing in "
                  "this file.").font = Font(size=10, italic=True, color=INK)
    ws.cell(row=r + 1, column=1).alignment = Alignment(wrap_text=True,
                                                       vertical="top")
    ws.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1,
                   end_column=3)
    ws.row_dimensions[r + 1].height = 60
    return ws


# ---------------------------------------------------------------- FOLLOW-UP
def sheet_sequence(wb):
    ws = wb.create_sheet("FOLLOW-UP")
    ws.sheet_view.showGridLines = False
    header(ws, 1, ["When", "What", "How"], [16, 34, 100])
    r = 2
    for when, what, how in SEQUENCE:
        for i, v in enumerate([when, what, how], start=1):
            c = ws.cell(row=r, column=i, value=v)
            c.border = BOX
            c.font = Font(size=10)
            c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.cell(row=r, column=1).font = Font(size=10, bold=True, color=ACCENT)
        ws.row_dimensions[r].height = max(30, 12.6 * (len(how) // 98 + 2))
        r += 1
    return ws


# ---------------------------------------------------------------- DOCUMENTS
def sheet_documents(wb):
    ws = wb.create_sheet("DOCUMENTS")
    ws.sheet_view.showGridLines = False
    header(ws, 1, ["Document", "Who asks for it", "Why it matters",
                   "Priority", "Status"], [40, 34, 72, 16, 18])
    r = 2
    for doc, who, why, prio in DOCUMENTS:
        for i, v in enumerate([doc, who, why, prio], start=1):
            c = ws.cell(row=r, column=i, value=v)
            c.border = BOX
            c.font = Font(size=10)
            c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.cell(row=r, column=1).font = Font(size=10, bold=True, color=ACCENT)
        p = ws.cell(row=r, column=4)
        p.alignment = Alignment(horizontal="center", vertical="top")
        if prio == "Must have":
            p.fill = CONF_FILL["low"]
            p.font = CONF_FONT["low"]
        elif prio == "Build early":
            p.fill = CONF_FILL["medium"]
            p.font = CONF_FONT["medium"]
        else:
            p.fill = CONF_FILL["high"]
            p.font = CONF_FONT["high"]
        s = ws.cell(row=r, column=5)
        s.border = BOX
        s.fill = SUNK
        ws.row_dimensions[r].height = max(30, 12.6 * (len(why) // 70 + 1))
        r += 1
    dv = DataValidation(type="list",
                        formula1='"Have it,Drafting,Not started,Not needed yet"',
                        allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"E2:E{r - 1}")
    return ws


# ------------------------------------------------------------ PIPELINE MATH
# Every number on this sheet is a formula over the assumption block, so the
# sheet answers "what if the reply rate is half that" by editing one cell
# rather than by rebuilding the file.
ASSUMPTIONS = [
    ("Reply rate, cold approach", 0.25, "0%",
     "Quarter of cold messages get any reply. Optimistic for corporates, "
     "pessimistic for youth organisations."),
    ("Reply rate, warm introduction", 0.70, "0%",
     "The reason the route column in the registry names an intermediary "
     "wherever one exists."),
    ("Share of approaches that are warm", 0.35, "0%",
     "Raise this before raising the number of approaches. It is the "
     "cheapest lever on the sheet."),
    ("Meeting per reply", 0.55, "0%",
     "A reply is not a meeting. Half convert with a specific ask attached."),
    ("Proposal per meeting", 0.60, "0%",
     "A meeting that does not end with permission to send something was a "
     "failed meeting."),
    ("Win per proposal", 0.22, "0%",
     "Across all types. Donor tenders are far lower, warm corporate "
     "sponsorships far higher."),
    ("Months from first contact to signature", 5.0, "0.0",
     "Average across types. Government and donor are nine to fifteen; "
     "corporate sponsorship is two to four."),
    ("Average contract value, USD", 18000, "#,##0",
     "A blend of the ticket bands in the registry. Replace with real "
     "numbers as soon as two contracts exist."),
]


def sheet_pipeline(wb):
    ws = wb.create_sheet("PIPELINE MATH")
    ws.sheet_view.showGridLines = False
    banner(ws, "How many of these have to be worked",
           "Every number below is a formula. Change an assumption and the "
           "whole sheet moves.", 7)
    for col, w in zip("ABCDEFG", [4, 38, 14, 14, 14, 14, 58]):
        ws.column_dimensions[col].width = w

    r = 4
    ws.cell(row=r, column=2, value="ASSUMPTIONS").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    first_assumption = r
    for label, value, fmt, why in ASSUMPTIONS:
        ws.cell(row=r, column=2, value=label).font = Font(size=10)
        c = ws.cell(row=r, column=3, value=value)
        c.number_format = fmt
        c.font = Font(size=10, bold=True, color=ACCENT)
        c.fill = SUNK
        c.border = BOX
        c.alignment = Alignment(horizontal="center")
        w = ws.cell(row=r, column=7, value=why)
        w.font = Font(size=9, italic=True, color="6B7A74")
        w.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = max(15, 12 * (len(why) // 60 + 1))
        r += 1
    A = {label: f"$C${first_assumption + i}"
         for i, (label, *_) in enumerate(ASSUMPTIONS)}

    r += 1
    ws.cell(row=r, column=2, value="THE FUNNEL, BY CATEGORY").font = Font(
        bold=True, size=11, color=ACCENT)
    r += 1
    heads = ["Category", "In registry", "Approach", "Meetings", "Proposals",
             "Wins", "Expected value, USD"]
    for i, h in enumerate(heads, start=1):
        c = ws.cell(row=r, column=i + 1, value=h)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = SUBHEAD
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
    ws.row_dimensions[r].height = 30
    head_row = r
    r += 1

    counts = {}
    for p in PROSPECTS:
        counts[p["cat"]] = counts.get(p["cat"], 0) + 1
    first = r
    for cat in CATEGORIES:
        n = counts.get(cat, 0)
        ws.cell(row=r, column=2, value=cat).font = Font(size=10)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True,
                                                       vertical="center",
                                                       indent=1)
        ws.cell(row=r, column=3, value=n)
        # Approach every one of them. The registry is already the filter.
        ws.cell(row=r, column=4, value=f"=C{r}")
        ws.cell(row=r, column=5,
                value=(f"=D{r}*({A['Share of approaches that are warm']}"
                       f"*{A['Reply rate, warm introduction']}"
                       f"+(1-{A['Share of approaches that are warm']})"
                       f"*{A['Reply rate, cold approach']})"
                       f"*{A['Meeting per reply']}"))
        ws.cell(row=r, column=6,
                value=f"=E{r}*{A['Proposal per meeting']}")
        ws.cell(row=r, column=7, value=f"=F{r}*{A['Win per proposal']}")
        ws.cell(row=r, column=8,
                value=f"=G{r}*{A['Average contract value, USD']}")
        for i in range(3, 9):
            c = ws.cell(row=r, column=i)
            c.border = BOX
            c.font = Font(size=10)
            c.alignment = Alignment(horizontal="center")
            c.number_format = "0.0" if i in (5, 6, 7) else "#,##0"
        ws.row_dimensions[r].height = 26
        r += 1

    for i, col in enumerate("CDEFGH"):
        c = ws.cell(row=r, column=3 + i, value=f"=SUM({col}{first}:{col}{r-1})")
        c.font = Font(size=10, bold=True, color="FFFFFF")
        c.fill = HEAD
        c.border = BOX
        c.alignment = Alignment(horizontal="center")
        c.number_format = "0.0" if col in ("E", "F", "G") else "#,##0"
    t = ws.cell(row=r, column=2, value="TOTAL")
    t.font = Font(size=10, bold=True, color="FFFFFF")
    t.fill = HEAD
    t.alignment = Alignment(indent=1)
    total_row = r
    r += 2

    notes = [
        ("WHAT THIS SAYS", ""),
        ("", f"At the assumed rates, one pass over the whole registry "
             f"produces about three signed contracts (cell G{total_row}) and "
             f"the value in H{total_row}. That is a fraction of what year "
             f"one needs, and saying so is the point of the sheet. This "
             f"registry is one channel beside the university, school and "
             f"competition engines, it has to be worked more than once a "
             f"year, and the win rate in the assumptions is a guess until "
             f"two contracts have been signed and measured."),
        ("", "The cheapest way to move it is not more approaches. It is the "
             "warm share: the registry's route column names an intermediary "
             "for most rows, and a warm introduction converts at nearly "
             "three times a cold one."),
        ("", "The second cheapest is the DOCUMENTS sheet. A bid that is "
             "disqualified on registration or safeguarding never reaches the "
             "win rate at all, and that failure does not appear anywhere in "
             "this arithmetic."),
        ("", ""),
        ("A REALISTIC FIRST QUARTER", ""),
        ("", "Not the whole registry. The tier A rows only, which is "
             f"{sum(1 for p in PROSPECTS if p['tier'] == 'A')} "
             "organisations, worked properly: a researched approach, a named "
             "intermediary where one exists, and a follow-up sequence that "
             "is actually run. Twenty organisations worked well beats a "
             "hundred emailed."),
    ]
    prose(ws, notes, start=r, label_col=2, text_col=2, wrap_at=100)
    for rr in range(r, r + len(notes)):
        ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=7)
    return ws


def build(path):
    wb = Workbook()
    wb.remove(wb.active)
    sheet_readme(wb)
    sheet_prospects(wb)
    sheet_playbook(wb)
    sheet_wants(wb)
    sheet_messages(wb)
    sheet_sequence(wb)
    sheet_documents(wb)
    sheet_pipeline(wb)
    wb.properties.creator = "StartPad"
    wb.properties.title = "Egypt CSR, NGO and youth organisation prospects"
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
               "StartPad_Egypt_CSR_NGO_Prospects.xlsx"))
    build(out)
    print(f"wrote {out}  ({os.path.getsize(out)/1024:,.0f} KB)")
    print(f"{len(PROSPECTS)} organisations, {len(CATEGORIES)} categories")
