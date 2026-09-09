"""Build Startpad — Mission Playbook.docx (the content/facilitator guide)."""
import os
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from startpad.missions import ALWAYS_AVAILABLE, MAPPING, MISSIONS  # noqa: E402
from startpad.resources import BY_MISSION, FOUNDATION, FUNDRAISING  # noqa: E402
from startpad.tools import TOOL_BY_NAME  # noqa: E402
from scripts.build_xlsx import FINDINGS  # noqa: E402
from scripts._determinism import FIXED_TIMESTAMP, normalize_zip  # noqa: E402

INK = RGBColor(0x1F, 0x29, 0x33)
GREEN = RGBColor(0x0F, 0x5C, 0x4B)
BLUE = RGBColor(0x1D, 0x6F, 0xA3)
BROWN = RGBColor(0x7A, 0x6A, 0x55)
GREY = RGBColor(0x5A, 0x6B, 0x66)

ROLE_STYLE = {
    "core": ("CORE", GREEN, "D7EBE3"),
    "supporting": ("SUPPORTING", BLUE, "DCE9F4"),
    "stretch": ("STRETCH", BROWN, "F0EAE0"),
}


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def no_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "DCE3E0")
        borders.append(e)
    tblPr.append(borders)


def para(doc, text="", size=10.5, bold=False, italic=False, color=INK,
         space_before=0, space_after=4, align=None, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return p


def heading(doc, text, level=1, color=GREEN, size=None, space_before=14, space_after=6):
    sizes = {0: 22, 1: 16, 2: 12.5, 3: 11}
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.size = Pt(size or sizes[level])
    r.font.bold = True
    r.font.color.rgb = color
    return p


def rule(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:color"), "0F5C4B")
    pbdr.append(bottom)
    pPr.append(pbdr)


def bullet(doc, text, size=10.5, indent=0.6, color=INK, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(indent)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run("•  ")
    r.font.size = Pt(size)
    r.font.color.rgb = GREEN
    r.font.bold = True
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.size = Pt(size)
        rb.font.bold = True
        rb.font.color.rgb = INK
    r2 = p.add_run(text)
    r2.font.size = Pt(size)
    r2.font.color.rgb = color
    return p


def hyperlink(paragraph, url, text, size=9):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    col = OxmlElement("w:color")
    col.set(qn("w:val"), "1D6FA3")
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    rPr.append(col)
    rPr.append(u)
    rPr.append(sz)
    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    h.append(new_run)
    paragraph._p.append(h)


def build(out_path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.font.color.rgb = INK
    for s in doc.sections:
        s.top_margin = Cm(2.0)
        s.bottom_margin = Cm(2.0)
        s.left_margin = Cm(2.2)
        s.right_margin = Cm(2.2)

    # ---------------- cover ----------------
    para(doc, "STARTPAD", size=11, bold=True, color=GREEN, space_before=60)
    para(doc, "Mission Playbook", size=30, bold=True, color=INK, space_after=2)
    para(doc, "Which tools belong in each mission, why, and what to watch first",
         size=13, italic=True, color=GREY, space_after=18)
    rule(doc)
    para(doc, "The build spec behind the 15-mission journey.", size=11, color=INK, space_after=10)
    para(doc,
         "This playbook pairs every one of the 15 Startpad missions with the tools from the "
         "Tool Library that a founder actually needs to complete it, and with the video and "
         "reading material that teaches the thinking behind it. It is written for three readers: "
         "the product engineer deciding what to render on a mission screen, the content lead "
         "deciding what to upload to /resources, and the mentor preparing a session.",
         size=10.5, space_after=8)
    para(doc, "122 unique tools  ·  15 missions  ·  196 tool placements  ·  96 curated resources",
         size=10.5, bold=True, color=GREEN, space_after=20)

    t = doc.add_table(rows=3, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    no_borders(t)
    rows = [
        ("CORE", "The founder cannot answer this mission's questions well without it. "
                 "Render it on the mission screen, already open."),
        ("SUPPORTING", "Recommended — sharpens or de-risks the answer. One click away in a "
                       "'recommended tools' rail."),
        ("STRETCH", "Optional. For a second pass or an ambitious founder. Collapsed under "
                    "'go deeper'."),
    ]
    for i, (label, desc) in enumerate(rows):
        c0, c1 = t.rows[i].cells
        c0.width = Cm(3.2)
        c1.width = Cm(13.0)
        p = c0.paragraphs[0]
        r = p.add_run(label)
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = ROLE_STYLE[label.lower()][1]
        shade(c0, ROLE_STYLE[label.lower()][2])
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(desc)
        r1.font.size = Pt(9.5)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------------- how to read ----------------
    heading(doc, "How to read this playbook", level=1, space_before=0)
    rule(doc)
    para(doc,
         "Each mission gets one section. Inside it you will find the mission's own questions, "
         "the tools mapped to it with the reason each one is there and the specific question its "
         "output should populate, the resources worth putting in the pre-mission briefing, and a "
         "'done well' bar the AI evaluator can be tuned against.",
         space_after=8)
    bullet(doc, "the mapping in machine-readable form, plus a coverage grid and a reverse index.",
           bold_prefix="Startpad_Mission_Tool_Matrix.xlsx — ")
    bullet(doc, "two CSVs shaped for direct import into the missions / mission_tools / "
                "mission_resources tables.", bold_prefix="Seed CSVs — ")
    bullet(doc, "an interactive version of the same mapping, for sharing with the team.",
           bold_prefix="Artifact — ")
    para(doc, "", space_after=6)

    para(doc,
         "A note on the links. Every URL in this document came from a live web search during "
         "compilation — none were written from memory. The compiling environment blocked direct "
         "page fetches, so the links are search-index verified rather than fetch-verified. Run "
         "one link check from an unrestricted network before publishing any of them to "
         "startpad.me.", size=9.5, italic=True, color=GREY)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------------- foundation resources ----------------
    heading(doc, "Foundation resources", level=1, space_before=0)
    rule(doc)
    para(doc,
         "These are not mission-specific. They belong on /resources, offered at onboarding and "
         "again whenever a founder stalls.", space_after=8)
    for kind, title, source, url, length, lang, why in FOUNDATION:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.4)
        r = p.add_run(f"[{kind}] ")
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = GREEN
        r2 = p.add_run(f"{title}")
        r2.font.size = Pt(10)
        r2.font.bold = True
        r3 = p.add_run(f"  ·  {source}  ·  {length}  ·  {lang}")
        r3.font.size = Pt(9)
        r3.font.color.rgb = GREY
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Cm(0.9)
        p2.paragraph_format.space_after = Pt(1)
        r4 = p2.add_run(why)
        r4.font.size = Pt(9.5)
        r4.font.color.rgb = INK
        p3 = doc.add_paragraph()
        p3.paragraph_format.left_indent = Cm(0.9)
        p3.paragraph_format.space_after = Pt(8)
        hyperlink(p3, url, url)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------------- missions ----------------
    for idx, m in enumerate(MISSIONS):
        block = MAPPING[m["id"]]
        n_core = len(block.get("core", []))
        n_all = sum(len(v) for v in block.values())

        heading(doc, f'Mission {m["id"]} · {m["title"]}', level=1, space_before=0)
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f'{m["phase"]}  ·  {m["points"]} points  ·  {m["time"]}  ·  '
                      f'{n_core} core tools of {n_all} mapped')
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = GREY
        para(doc, m["summary"], size=11, italic=True, color=INK, space_after=4)
        rule(doc)

        heading(doc, "The questions this mission asks", level=3, color=INK, space_before=6)
        for i, q in enumerate(m["questions"], start=1):
            bullet(doc, q, size=10, bold_prefix=f"Q{i}. ")

        for role_key in ("core", "supporting", "stretch"):
            items = block.get(role_key, [])
            if not items:
                continue
            label, color, fill = ROLE_STYLE[role_key]
            heading(doc, f"{label} tools  ({len(items)})", level=3, color=color, space_before=12)
            tbl = doc.add_table(rows=len(items), cols=2)
            no_borders(tbl)
            for i, (tool, why, feeds) in enumerate(items):
                _, cat, does, ref = TOOL_BY_NAME[tool]
                c0, c1 = tbl.rows[i].cells
                c0.width = Cm(4.3)
                c1.width = Cm(12.0)
                shade(c0, fill)
                p0 = c0.paragraphs[0]
                p0.paragraph_format.space_after = Pt(1)
                r0 = p0.add_run(tool)
                r0.font.size = Pt(9.5)
                r0.font.bold = True
                r0.font.color.rgb = color
                p0b = c0.add_paragraph()
                p0b.paragraph_format.space_after = Pt(0)
                r0b = p0b.add_run(cat)
                r0b.font.size = Pt(7.5)
                r0b.font.color.rgb = GREY

                p1 = c1.paragraphs[0]
                p1.paragraph_format.space_after = Pt(1)
                r1 = p1.add_run(why)
                r1.font.size = Pt(9.5)
                p1b = c1.add_paragraph()
                p1b.paragraph_format.space_after = Pt(0)
                r1b = p1b.add_run(f"→ feeds {feeds}   ·   {ref}")
                r1b.font.size = Pt(8)
                r1b.font.italic = True
                r1b.font.color.rgb = GREY
            doc.add_paragraph().paragraph_format.space_after = Pt(2)

        res = BY_MISSION.get(m["id"], [])
        if res:
            heading(doc, f"Watch / read before starting  ({len(res)})", level=3,
                    color=INK, space_before=12)
            for kind, title, source, url, length, lang, why in res:
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.left_indent = Cm(0.4)
                r = p.add_run(f"[{kind}] ")
                r.font.size = Pt(8.5)
                r.font.bold = True
                r.font.color.rgb = GREEN if kind in ("Video", "Playlist") else BLUE
                r2 = p.add_run(title)
                r2.font.size = Pt(9.5)
                r2.font.bold = True
                r3 = p.add_run(f"  ·  {source}  ·  {length}  ·  {lang}")
                r3.font.size = Pt(8.5)
                r3.font.color.rgb = GREY
                p2 = doc.add_paragraph()
                p2.paragraph_format.left_indent = Cm(0.9)
                p2.paragraph_format.space_after = Pt(1)
                r4 = p2.add_run(why)
                r4.font.size = Pt(9)
                p3 = doc.add_paragraph()
                p3.paragraph_format.left_indent = Cm(0.9)
                p3.paragraph_format.space_after = Pt(6)
                hyperlink(p3, url, url, size=8)

        heading(doc, "Done well looks like", level=3, color=INK, space_before=10)
        for line in DONE_WELL[m["id"]]:
            bullet(doc, line, size=9.5)

        if idx != len(MISSIONS) - 1:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------------- founder toolkit ----------------
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    heading(doc, "The Founder Toolkit — 21 tools with no home in the missions", level=1,
            space_before=0)
    rule(doc)
    para(doc,
         "Placing every tool against the missions surfaced a real gap: almost the entire "
         "fundraising block, most of the finance statements, and the team and governance tools "
         "are never reachable from the mission flow. A founder who only follows missions will "
         "never open the Cap Table, the Pitch Deck template, or the Legal Checklist — three of "
         "the highest-value assets in the library. Do not force them into a mission. Shelve them, "
         "and surface each shelf on a trigger.", space_after=10)

    for shelf, items in ALWAYS_AVAILABLE.items():
        heading(doc, shelf, level=2, color=GREEN, space_before=10)
        for tool, why in items:
            _, cat, _, _ = TOOL_BY_NAME[tool]
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.5)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(f"{tool}  ")
            r.font.size = Pt(9.5)
            r.font.bold = True
            r2 = p.add_run(f"— {why}")
            r2.font.size = Pt(9.5)
            r3 = p.add_run(f"   ({cat})")
            r3.font.size = Pt(8)
            r3.font.color.rgb = GREY

    heading(doc, "Proposed Mission 16 — Raise Your Round", level=2, color=GREEN, space_before=14)
    para(doc,
         "The fundraising shelf is large and coherent enough to be a mission in its own right. "
         "It would sit after Mission 15, carry roughly 600 points, and give the 15 fundraising "
         "tools a narrative home instead of leaving them undiscoverable. Suggested resources:",
         space_after=6)
    for kind, title, source, url, length, lang, why in FUNDRAISING:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(f"[{kind}] ")
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = BLUE
        r2 = p.add_run(title)
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r3 = p.add_run(f"  ·  {source}")
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = GREY
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Cm(0.9)
        p2.paragraph_format.space_after = Pt(1)
        r4 = p2.add_run(why)
        r4.font.size = Pt(9)
        p3 = doc.add_paragraph()
        p3.paragraph_format.left_indent = Cm(0.9)
        p3.paragraph_format.space_after = Pt(6)
        hyperlink(p3, url, url, size=8)

    # ---------------- findings ----------------
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    heading(doc, "What the mapping exposed", level=1, space_before=0)
    rule(doc)
    para(doc,
         "Placing 122 tools against 15 missions is a stress test of the mission design. "
         "Twelve findings, ordered roughly by how much they cost you if left alone.",
         space_after=10)
    for i, (finding, why, rec) in enumerate(FINDINGS, start=1):
        heading(doc, f"{i}.  {finding}", level=3, color=GREEN, space_before=10, space_after=3)
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(why)
        r.font.size = Pt(9.5)
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Cm(0.5)
        p2.paragraph_format.space_after = Pt(2)
        r1 = p2.add_run("Recommendation:  ")
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = GREEN
        r2 = p2.add_run(rec)
        r2.font.size = Pt(9.5)

    cp = doc.core_properties
    cp.created = FIXED_TIMESTAMP
    cp.modified = FIXED_TIMESTAMP
    cp.last_modified_by = ""
    cp.revision = 1
    doc.save(out_path)
    normalize_zip(out_path)
    return out_path


DONE_WELL = {
    1: ["The problem is described in the words of someone who has it, not the founder's summary of it.",
        "At least three existing solutions are named, with a specific limitation each — not 'they're all bad'.",
        "The founder can say who is affected and roughly how many of them there are.",
        "Evidence exists: a conversation, a forum thread, a support log — something outside the founder's head."],
    2: ["The primary user is one named persona, not 'SMEs' or 'young people'.",
        "The problem statement includes when and where it happens, and how often, as numbers.",
        "The characteristics come from interviews, and the founder can say how many they ran.",
        "Anything asserted without evidence is logged in the Assumptions Tracker rather than presented as fact."],
    3: ["At least two problems are plotted, with importance and frequency scored independently.",
        "The scores trace back to Mission 2 evidence, not to the founder's preference.",
        "The chosen problem is defended against the runner-up in one sentence.",
        "A problem that scored high but was rejected is explained — usually reachability."],
    4: ["The statement names a specific user, a specific pain, and a frequency.",
        "Impact is quantified: time, money, or count of people.",
        "The success measure is one metric with a threshold, not 'more users'.",
        "The statement is falsifiable — you could run a test that proves it wrong."],
    5: ["At least two solution ideas are scored on the same criteria.",
        "The selection rationale references the scores, not enthusiasm.",
        "The rejected ideas are parked in a backlog, not deleted.",
        "The chosen idea is checked against what this specific team can build."],
    6: ["The value proposition survives the 30-second test — a stranger repeats it back correctly.",
        "Features are 3-5, and each maps to a pain or gain on the customer side of the canvas.",
        "Differentiation is stated against a named alternative, not against 'nothing like this exists'.",
        "The assumptions list is honest and ranked — the riskiest one is named."],
    7: ["The hypothesis is one falsifiable sentence with a pass threshold set before the test ran.",
        "The test method is described well enough that someone else could repeat it.",
        "Results include the number that was measured, not just an impression.",
        "The 'what did you learn' answer includes at least one thing that surprised the founder."],
    8: ["All nine blocks are filled, and none contradict another.",
        "Revenue streams name a price and who pays it.",
        "Cost structure has line items, not a single number.",
        "Unit economics are computed: what one customer costs and what one customer is worth."],
    9: ["The prototype demonstrates the core flow end to end, even if faked behind the scenes.",
        "Scope was decided before building, and something was explicitly cut.",
        "The tool choice is justified rather than defaulted to.",
        "A link exists, and it opens for someone who is not the founder."],
    10: ["Five or more people outside the founder's circle tested it.",
         "There is a written protocol — the same tasks were given to each tester.",
         "Findings are ranked by severity, and at least one is uncomfortable.",
         "The improvement list is prioritised, not a flat list of everything anyone said."],
    11: ["The target market is narrower than the total market, and the narrowing is justified.",
         "Each channel has an estimated cost per acquisition, not just a name.",
         "Pricing has a rationale — value-based or cost-plus — and a tier structure.",
         "The sales process has stages a person could actually follow on a Monday morning."],
    12: ["Demand evidence is behavioural: sign-ups, pre-orders, click-throughs — not survey enthusiasm.",
         "Market size is built bottom-up and the math is shown.",
         "Competitor learning is specific enough to change a product decision.",
         "The pricing response came from customers, not from the founder's estimate."],
    13: ["The MVP does the must-haves and visibly does not do the could-haves.",
         "Analytics are instrumented before launch — the North Star metric can actually be read.",
         "Terms, privacy policy and data handling exist before real users arrive.",
         "The founder can state what they would cut if they had half the time again."],
    14: ["Retention is measured by cohort, and the curve is shown, not described.",
         "The PMF score comes from the Sean Ellis survey, not a self-rating.",
         "Feedback is segmented — PMF is usually real for one segment and absent for another.",
         "The improvement plan follows the 50/50 rule: half for what fans love, half for what blocks the rest."],
    15: ["The launch was a sequence of moments, not one day.",
         "Results are per channel, with ROAS or CPA, so the next spend is informed.",
         "Acquisition and revenue numbers are real and reconcilable with the analytics.",
         "The next-steps answer names one growth loop to invest in, not five tactics to try."],
}


if __name__ == "__main__":
    p = build(sys.argv[1] if len(sys.argv) > 1 else "output/Startpad_Mission_Playbook.docx")
    print("wrote", p)
