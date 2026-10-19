"""
Render the StartPad business plan to Word.

Content comes from business_plan/content.py; every number in it comes from
business_plan/model.py; every chart comes from business_plan/charts.py, which also
reads the model. One assumption set feeds the sentence, the table and the picture,
so none of the three can quietly fall behind the other two.

Formatting is hand-built rather than styled, because a recipient's Normal style is
unknown and a document that inherits their template is not the document we sent.

    python3 scripts/build_business_plan_docx.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docx import Document                                      # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT                 # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK        # noqa: E402
from docx.oxml import OxmlElement                              # noqa: E402
from docx.oxml.ns import qn                                    # noqa: E402
from docx.shared import Cm, Pt, RGBColor                       # noqa: E402

from scripts import _ooxml as X                                # noqa: E402
from business_plan import content as K                         # noqa: E402
from business_plan.roles import BY_ROLE                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(ROOT, "business_plan", "figures")
OUT = os.path.join(ROOT, "output")

# ---------------------------------------------------------------- palette
INK = RGBColor(0x0B, 0x0E, 0x14)
SECOND = RGBColor(0x3A, 0x40, 0x50)
MUTED = RGBColor(0x6B, 0x72, 0x85)
FAINT = RGBColor(0x9A, 0xA0, 0xAF)
UV = RGBColor(0x34, 0x18, 0xE0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

LIME_HEX = "CBF24A"
UV_HEX = "3418E0"
WASH_HEX = "F5F6F8"
HAIR_HEX = "E2E4EA"
INK_HEX = "0B0E14"

FONT = "Plus Jakarta Sans"
FALLBACK = "Segoe UI"   # named second so Word substitutes something close, not Calibri

CONTENT_W = 16.6        # cm, the printable column on A4 at these margins


# --------------------------------------------------- row-level OOXML helpers
#
# These two live here rather than in scripts/_ooxml.py because that module is
# shared with the builders the existing check gates run against, and this document
# is the only thing that needs them.

def tr_header(row):
    """Repeat this row at the top of every page the table spills onto."""
    X.insert_ordered(row._tr.get_or_add_trPr(), "w:tblHeader", X.TRPR,
                     {"w:val": "true"})


def tr_cant_split(row):
    """Never break a row across a page — a half-row reads as missing data."""
    X.insert_ordered(row._tr.get_or_add_trPr(), "w:cantSplit", X.TRPR,
                     {"w:val": "true"})


def tbl_fixed(table, widths_cm):
    """
    Honour the column widths actually asked for.

    Without an explicit fixed layout and a tblGrid, Word and LibreOffice both
    re-fit columns to their content, which silently throws away the widths set on
    the cells — a one-character column ends up as wide as a sentence.
    """
    X.insert_ordered(table._tbl.tblPr, "w:tblLayout", X.TBLPR,
                     {"w:type": "fixed"})
    X.insert_ordered(table._tbl.tblPr, "w:tblW", X.TBLPR,
                     {"w:w": str(int(sum(widths_cm) * 567)), "w:type": "dxa"})
    grid = table._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        table._tbl.remove(grid)
    grid = OxmlElement("w:tblGrid")
    for w in widths_cm:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(int(w * 567)))
        grid.append(col)
    table._tbl.insert(list(table._tbl).index(table._tbl.tblPr) + 1, grid)


# ---------------------------------------------------------------- runs
def runs_from(markup):
    """Split a fragment into (text, bold) pairs, honouring <b> and &amp;."""
    out = []
    for piece in re.split(r"(<b>.*?</b>)", str(markup), flags=re.S):
        if not piece:
            continue
        bold = piece.startswith("<b>")
        text = re.sub(r"</?b>", "", piece)
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        out.append((text, bold))
    return out


def write(par, markup, size, colour=INK, bold=False, italic=False, spacing=None):
    for text, is_bold in runs_from(markup):
        run = par.add_run(text)
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.color.rgb = colour
        run.bold = bold or is_bold
        run.italic = italic
        X.run_cs(run, FALLBACK, size)
        if spacing:
            X.run_spacing(run, spacing)
    return par


def para(doc, markup="", size=9.8, colour=INK, bold=False, italic=False,
         before=0, after=5, align=None, indent=0, line=1.34, keep=False,
         spacing=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if indent:
        pf.left_indent = Cm(indent)
    if align is not None:
        p.alignment = align
    if keep:
        pf.keep_with_next = True
    # Widow and orphan control only. Setting keepLines as well would make every
    # paragraph atomic, so a paragraph that does not fit jumps whole to the next
    # page and leaves a near-empty one behind it — which is a worse artefact than
    # the split it was meant to prevent. Headings keep with the next paragraph
    # instead, via `keep`, which is where that behaviour actually belongs.
    X.insert_ordered(p._p.get_or_add_pPr(), "w:widowControl", X.PPR,
                     {"w:val": "true"})
    write(p, markup, size, colour, bold, italic, spacing)
    return p


def shade_par(p, hexcolor):
    X.insert_ordered(p._p.get_or_add_pPr(), "w:shd", X.PPR,
                     {"w:val": "clear", "w:fill": hexcolor})


def left_bar(p, hexcolor, size="18"):
    pbdr = X.insert_ordered(p._p.get_or_add_pPr(), "w:pBdr", X.PPR)
    for c in list(pbdr):
        pbdr.remove(c)
    el = OxmlElement("w:left")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), size)
    el.set(qn("w:space"), "8")
    el.set(qn("w:color"), hexcolor)
    pbdr.append(el)


def rule(doc, hexcolor=HAIR_HEX, size="6", before=2, after=9):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    pbdr = X.insert_ordered(p._p.get_or_add_pPr(), "w:pBdr", X.PPR)
    for c in list(pbdr):
        pbdr.remove(c)
    el = OxmlElement("w:bottom")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), size)
    el.set(qn("w:color"), hexcolor)
    pbdr.append(el)
    return p


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def content_count(doc):
    """Body children excluding the trailing sectPr.

    python-docx inserts new content *before* that sectPr, so a plain len(body)
    taken beforehand points one past the paragraph that is about to be added.
    Counting content elements instead gives an index that stays valid, and does
    not rely on the identity of an lxml proxy, which is not stable across
    lookups.
    """
    return sum(1 for e in doc.element.body if e.tag != qn("w:sectPr"))


def break_before_first(doc, before):
    """Set pageBreakBefore on the first element added since `before` content
    elements existed.

    Works for a table too: Word cannot break before a table, so the flag goes on
    the first paragraph inside its first cell, which has the same effect.
    """
    content = [e for e in doc.element.body if e.tag != qn("w:sectPr")]
    for el in content[before:]:
        tag = el.tag.split("}")[-1]
        if tag == "p":
            X.insert_ordered(el.get_or_add_pPr(), "w:pageBreakBefore", X.PPR,
                             {"w:val": "true"})
            return
        if tag == "tbl":
            first_p = el.find(".//" + qn("w:p"))
            if first_p is not None:
                X.insert_ordered(first_p.get_or_add_pPr(), "w:pageBreakBefore",
                                 X.PPR, {"w:val": "true"})
            return


# ---------------------------------------------------------------- blocks
def h1(doc, number, text, first=False):
    p = doc.add_paragraph()
    if not first:
        # Break before the heading rather than after the previous section: an
        # explicit trailing break lands on a fresh page when the section already
        # ended at the page boundary, and leaves a blank sheet behind it.
        X.insert_ordered(p._p.get_or_add_pPr(), "w:pageBreakBefore", X.PPR,
                         {"w:val": "true"})
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    write(p, f"SECTION {number:02d}", 8, UV, bold=True, spacing=28)
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(6)
    p2.paragraph_format.keep_with_next = True
    write(p2, text, 21, INK, bold=True)
    rule(doc, UV_HEX, "10", before=0, after=10)


def h2(doc, text):
    p = para(doc, text, size=13, colour=INK, bold=True, before=15, after=5,
             keep=True, line=1.2)
    return p


def h3(doc, text):
    return para(doc, text, size=10.4, colour=UV, bold=True, before=10, after=3,
                keep=True)


def lead(doc, markup):
    para(doc, markup, size=11.6, colour=SECOND, before=0, after=12, line=1.4)


def bullets(doc, items, size=9.8):
    for it in items:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(0.72)
        pf.first_line_indent = Cm(-0.42)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.32
        r = p.add_run("▪  ")
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.color.rgb = UV
        r.bold = True
        X.run_cs(r, FALLBACK, size)
        write(p, it, size)


def numbers(doc, items, size=9.8):
    for i, it in enumerate(items, start=1):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(0.82)
        pf.first_line_indent = Cm(-0.82)
        pf.space_after = Pt(5)
        pf.line_spacing = 1.32
        r = p.add_run(f"{i:02d}   ")
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.color.rgb = UV
        r.bold = True
        X.run_cs(r, FALLBACK, size)
        write(p, it, size)


def deflist(doc, items):
    for term, body in items:
        p = para(doc, term, size=10, colour=INK, bold=True, before=8, after=2,
                 indent=0.3, keep=True)
        left_bar(p, UV_HEX)
        p2 = para(doc, body, size=9.6, colour=SECOND, after=4, indent=0.3,
                  line=1.34)
        left_bar(p2, HAIR_HEX)


def note(doc, markup):
    p = para(doc, markup, size=9.4, colour=SECOND, before=8, after=9, indent=0.28,
             line=1.34)
    shade_par(p, WASH_HEX)
    left_bar(p, LIME_HEX, size="24")


def quote(doc, markup):
    para(doc, markup, size=13.5, colour=UV, bold=True, before=12, after=12,
         line=1.26, indent=0.4)


def kpi(doc, tiles):
    t = doc.add_table(rows=1, cols=len(tiles))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    X.tbl_borders(t, color="FFFFFF", sz="2")
    w = CONTENT_W / len(tiles)
    tbl_fixed(t, [w] * len(tiles))
    for cell, (value, label) in zip(t.rows[0].cells, tiles):
        cell.width = Cm(w)
        X.tc_shade(cell, WASH_HEX)
        X.tc_margins(cell, top=0.26, start=0.26, bottom=0.26, end=0.22)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        write(p, value, 19, UV, bold=True)
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.22
        write(p2, label, 7.8, SECOND)
    para(doc, "", size=4, after=8)
    return t


def table(doc, heads, rows, widths=None, size=8.6):
    ncols = len(heads)
    if not widths:
        widths = [CONTENT_W / ncols] * ncols
    scale = CONTENT_W / sum(widths)
    widths = [w * scale for w in widths]

    t = doc.add_table(rows=len(rows) + 1, cols=ncols)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    X.tbl_borders(t, color=HAIR_HEX, sz="4")
    tbl_fixed(t, widths)

    hdr = t.rows[0]
    tr_header(hdr)
    for cell, head, w in zip(hdr.cells, heads, widths):
        cell.width = Cm(w)
        X.tc_shade(cell, INK_HEX)
        X.tc_margins(cell, top=0.14, start=0.16, bottom=0.14, end=0.14)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.16
        write(p, head, size - 0.5, WHITE, bold=True)

    for i, row in enumerate(rows):
        last = i == len(rows) - 1
        # A row whose first cell starts with "Total" is the summary row, and is
        # given the lime ground so the eye lands on it without needing a rule.
        total = str(row[0]).strip().lower().startswith(("total", "year one",
                                                        "serviceable", "total "))
        tr_cant_split(t.rows[i + 1])
        for j, (cell, val, w) in enumerate(zip(t.rows[i + 1].cells, row, widths)):
            cell.width = Cm(w)
            X.tc_margins(cell, top=0.13, start=0.16, bottom=0.13, end=0.14)
            if total:
                X.tc_shade(cell, LIME_HEX)
            elif i % 2 == 1:
                X.tc_shade(cell, WASH_HEX)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.2
            bold = total or j == 0
            colour = INK if (bold or j == 0) else SECOND
            write(p, val, size, colour, bold=bold)
    para(doc, "", size=4, after=7)
    return t


def figure(doc, name, caption):
    path = os.path.join(FIGS, f"{name}.png")
    if not os.path.exists(path):
        raise FileNotFoundError(f"figure not built: {path}")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Cm(CONTENT_W))
    cap = para(doc, caption, size=8.2, colour=MUTED, after=11, line=1.3)
    cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p


def role_cards(doc, names):
    """One card per role: purpose, responsibilities, and the measure it is held to."""
    for name in names:
        role, reports_to, purpose, duties, measure = BY_ROLE[name]
        p = para(doc, role, size=11.4, colour=INK, bold=True, before=12, after=1,
                 indent=0.3, keep=True)
        left_bar(p, UV_HEX, size="24")
        p2 = para(doc, f"Reports to {reports_to}", size=8.2, colour=UV, bold=True,
                  after=3, indent=0.3, keep=True)
        left_bar(p2, UV_HEX, size="24")
        p3 = para(doc, purpose, size=9.6, colour=SECOND, italic=True, after=5,
                  indent=0.3)
        left_bar(p3, HAIR_HEX)
        for d in duties:
            q = doc.add_paragraph()
            pf = q.paragraph_format
            pf.left_indent = Cm(1.02)
            pf.first_line_indent = Cm(-0.42)
            pf.space_after = Pt(3)
            pf.line_spacing = 1.3
            r = q.add_run("\u2013  ")
            r.font.name = FONT
            r.font.size = Pt(9.3)
            r.font.color.rgb = FAINT
            X.run_cs(r, FALLBACK, 9.3)
            write(q, d, 9.3)
            left_bar(q, HAIR_HEX)
        pm = para(doc, measure, size=8.8, colour=INK, bold=True, before=3,
                  after=9, indent=0.3)
        shade_par(pm, WASH_HEX)
        left_bar(pm, LIME_HEX, size="24")


RENDER = {
    "lead": lambda d, b: lead(d, b[1]),
    "h2": lambda d, b: h2(d, b[1]),
    "h3": lambda d, b: h3(d, b[1]),
    "p": lambda d, b: para(d, b[1]),
    "bul": lambda d, b: bullets(d, b[1]),
    "num": lambda d, b: numbers(d, b[1]),
    "deflist": lambda d, b: deflist(d, b[1]),
    "note": lambda d, b: note(d, b[1]),
    "quote": lambda d, b: quote(d, b[1]),
    "kpi": lambda d, b: kpi(d, b[1]),
    "table": lambda d, b: table(d, b[1], b[2], b[3] if len(b) > 3 else None),
    "fig": lambda d, b: figure(d, b[1], b[2]),
    "roles": lambda d, b: role_cards(d, b[1]),
    "pb": lambda d, b: page_break(d),
}


# ---------------------------------------------------------------- furniture
def set_margins(section):
    # A4, not python-docx's Letter default: this document is printed in Cairo and
    # Riyadh, and the content width every figure is sized against assumes it.
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(1.9)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)
    section.header_distance = Cm(1.1)
    section.footer_distance = Cm(1.0)


def field(par, instr):
    r = par.add_run()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    r._r.append(fld)
    r2 = par.add_run()
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    r2._r.append(it)
    r3 = par.add_run()
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    r3._r.append(end)
    for r_ in (r, r2, r3):
        r_.font.name = FONT
        r_.font.size = Pt(8)
        r_.font.color.rgb = MUTED
        X.run_cs(r_, FALLBACK, 8)


def furniture(section):
    hp = section.header.paragraphs[0]
    hp.paragraph_format.space_after = Pt(0)
    write(hp, "STARTPAD  ·  BUSINESS PLAN  ·  EGYPT AND SAUDI ARABIA", 7.4,
          FAINT, bold=True, spacing=24)
    pbdr = X.insert_ordered(hp._p.get_or_add_pPr(), "w:pBdr", X.PPR)
    el = OxmlElement("w:bottom")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), "4")
    el.set(qn("w:color"), HAIR_HEX)
    pbdr.append(el)

    fp = section.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp.paragraph_format.space_before = Pt(2)
    write(fp, K.PERIOD + "          ", 7.4, FAINT)
    field(fp, " PAGE ")


def cover(doc):
    # The cover carries no running header or page number; those start on the
    # contents page, which is where a reader starts counting.
    sect = doc.sections[0]
    sect.different_first_page_header_footer = True

    logo = os.path.join(ROOT, "brand", "startpad_logo.png")
    if os.path.exists(logo):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(34)
        p.paragraph_format.space_after = Pt(26)
        p.add_run().add_picture(logo, width=Cm(3.4))
    else:
        para(doc, "STARTPAD", size=12, colour=UV, bold=True, before=60, after=10,
             spacing=52)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("  ")
    r.font.size = Pt(2)
    shade_par(p, LIME_HEX)

    para(doc, K.TITLE, size=42, colour=INK, bold=True, before=22, after=0,
         line=1.02)
    para(doc, K.SUBTITLE, size=14.5, colour=SECOND, before=6, after=16, line=1.3)
    rule(doc, INK_HEX, "8", before=0, after=14)

    para(doc, "A gamified, AI-native venture-building platform that takes MENA "
              "founders from a raw idea to a live product in fifteen guided "
              "missions — and the six institutional engines built around it.",
         size=11.4, colour=INK, after=20, line=1.42)

    kpi(doc, [(K.money(K.M["tam"]), "Total addressable market, Egypt and KSA"),
              (K.money(K.M["sam"]), "Serviceable available market"),
              (K.money(K.R1["total"]), "Year-one revenue"),
              (K.pct(K.R1["institutional_share"]), "Institutional revenue")])

    para(doc, "", size=9, after=28)
    t = doc.add_table(rows=1, cols=2)
    X.tbl_borders(t, color="FFFFFF", sz="2")
    c0, c1 = t.rows[0].cells
    c0.width = Cm(8.3)
    c1.width = Cm(8.3)
    for cell, (k, v) in zip((c0, c1), [("PLANNING PERIOD", K.PERIOD),
                                       ("MARKETS", "Egypt · Saudi Arabia")]):
        X.tc_margins(cell, top=0.1, start=0.0, bottom=0.1, end=0.1)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        write(p, k, 7.4, FAINT, bold=True, spacing=24)
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(0)
        write(p2, v, 9.6, INK, bold=True)
    page_break(doc)


def contents(doc):
    para(doc, "Contents", size=19, colour=INK, bold=True, after=4)
    rule(doc, UV_HEX, "10", before=0, after=10)
    t = doc.add_table(rows=len(K.SECTIONS), cols=3)
    X.tbl_borders(t, color="FFFFFF", sz="2")
    tbl_fixed(t, [0.95, 6.45, 9.2])
    blurbs = {
        "Executive Summary": "The company, the problem, the opportunity and the "
                             "eight engines, in brief",
        "Company Description": "Mission, vision, values, and what has to be true "
                               "for this to work",
        "Market Analysis": "Segments, buyer universe, size, drivers, gaps and "
                           "the regulatory frame",
        "Competitive Analysis": "Who a buyer uses instead, how we compare, and "
                                "what is actually hard to copy",
        "Products and Services": "What is sold, in what format, at what price "
                                 "and anchored against what",
        "Marketing Strategy": "Two customer journeys, the channels that produce "
                              "institutional pipeline, and the brand",
        "Sales Strategy": "Four selling motions, the team that runs them, and "
                          "the pipeline they feed",
        "Go-to-Market Roadmap": "Eight engines, eight gates, twelve quarters — "
                                "and the critical path through them",
        "Operations Plan": "How a contract becomes a delivered cohort, and what "
                           "breaks first if it does not",
        "Management and Organization": "A deliberately small team, with every "
                                       "role described in full",
        "Strategic Analysis": "SWOT, PESTLE, risk and what we do when something "
                              "goes wrong",
        "Appendix": "Every figure behind the plan, and what it does not claim",
    }
    for i, (name, _) in enumerate(K.SECTIONS):
        row = t.rows[i]
        row.cells[0].width = Cm(0.95)
        row.cells[1].width = Cm(6.45)
        row.cells[2].width = Cm(9.2)
        for cell in row.cells:
            X.tc_margins(cell, top=0.10, start=0.0, bottom=0.10, end=0.25)
        # The blurb column needs its own left inset or it touches the title above it.
        X.tc_margins(row.cells[2], top=0.10, start=0.22, bottom=0.10, end=0.0)
        p = row.cells[0].paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        write(p, f"{i+1:02d}", 11, UV, bold=True)
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        write(p1, name, 10, INK, bold=True)
        p2 = row.cells[2].paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.22
        write(p2, blurbs.get(name, ""), 8.4, MUTED)
    page_break(doc)


def build(path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(9.8)
    st.font.color.rgb = INK
    for s in doc.sections:
        set_margins(s)
        furniture(s)

    cover(doc)
    contents(doc)

    for i, (name, blocks) in enumerate(K.SECTIONS, start=1):
        h1(doc, i, name, first=(i == 1))
        # A ("pb",) block does not emit a break of its own. An explicit trailing
        # break lands on a fresh page whenever the content happened to end at the
        # page boundary, and leaves a blank sheet behind it — which is exactly
        # what a hard break before "Role descriptions" used to produce. Instead
        # the break is carried forward and set as pageBreakBefore on the first
        # paragraph the next block writes, which is a no-op on a fresh page.
        pending_break = False
        for b in blocks:
            if b[0] == "pb":
                pending_break = True
                continue
            before = content_count(doc) if pending_break else None
            RENDER[b[0]](doc, b)
            if pending_break:
                break_before_first(doc, before)
                pending_break = False

    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)
    return path


if __name__ == "__main__":
    out = os.path.join(OUT, "StartPad_Business_Plan.docx")
    build(out)
    print(f"wrote {out}  ({os.path.getsize(out)/1024:,.0f} KB)")
