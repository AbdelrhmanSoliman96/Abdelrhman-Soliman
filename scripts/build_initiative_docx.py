"""
Render the initiative framework to Word.

Content comes from outreach/framework.py; every number in it comes from
outreach/initiative.py, which is the same module the sponsor workbook reads.
One assumption set feeds the sentence, the table and the workbook, so the
document and the list cannot quietly disagree.

The formatting helpers below are deliberately local rather than imported from
the business plan builder. Importing that module would pull in the financial
model workbook through the plan's content module, which would make this
document fail to build whenever the model has not been recalculated. A
framework a partner is being sent should not depend on a spreadsheet being
fresh.

    python3 scripts/build_initiative_docx.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re                                                      # noqa: E402

from docx import Document                                      # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT                 # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK        # noqa: E402
from docx.oxml import OxmlElement                              # noqa: E402
from docx.oxml.ns import qn                                    # noqa: E402
from docx.shared import Cm, Pt, RGBColor                       # noqa: E402

from scripts import _ooxml as X                                # noqa: E402
from scripts._determinism import FIXED_TIMESTAMP, normalize_zip  # noqa: E402
from outreach import framework as K                            # noqa: E402
from outreach import initiative as I                           # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")

INK = RGBColor(0x0B, 0x0E, 0x14)
SECOND = RGBColor(0x3A, 0x40, 0x50)
MUTED = RGBColor(0x6B, 0x72, 0x85)
UV = RGBColor(0x34, 0x18, 0xE0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

LIME_HEX = "CBF24A"
UV_HEX = "3418E0"
WASH_HEX = "F5F6F8"
HAIR_HEX = "E2E4EA"
INK_HEX = "0B0E14"

FONT = "Plus Jakarta Sans"
FALLBACK = "Segoe UI"
CONTENT_W = 16.6

FORBIDDEN = {"—": "em dash", "–": "en dash", "·": "middot",
             "‘": "curly quote", "’": "curly quote",
             "“": "curly quote", "”": "curly quote",
             "…": "ellipsis", "→": "arrow",
             "×": "multiplication sign", "−": "minus sign",
             "▪": "square bullet"}


# ------------------------------------------------------------------- runs
def runs_from(markup):
    out = []
    for piece in re.split(r"(<b>.*?</b>)", str(markup), flags=re.S):
        if not piece:
            continue
        bold = piece.startswith("<b>")
        text = re.sub(r"</?b>", "", piece)
        text = text.replace("&amp;", "&").replace("&lt;", "<")
        out.append((text, bold))
    return out


def write(par, markup, size, colour=INK, bold=False, italic=False,
          spacing=None):
    for text, is_bold in runs_from(markup):
        # A table cell carries its own line breaks as "\n", which Word only
        # honours as an explicit break element. The break goes in a run of
        # its own: setting run.text afterwards replaces the run's children
        # and would throw the break away.
        for i, line in enumerate(text.split("\n")):
            if i:
                br = par.add_run()
                br.add_break()
                br.font.name = FONT
                br.font.size = Pt(size)
            run = par.add_run(line)
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


def tbl_fixed(table, widths_cm):
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


# ------------------------------------------------------------------ blocks
def h1(doc, number, text, first=False):
    p = doc.add_paragraph()
    if not first:
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
    write(p2, text, 20, INK, bold=True)
    rule(doc, UV_HEX, "10", before=0, after=10)


def h2(doc, text):
    return para(doc, text, size=12.4, colour=INK, bold=True, before=14,
                after=5, keep=True, line=1.2)


def h3(doc, text):
    return para(doc, text, size=10.4, colour=UV, bold=True, before=10,
                after=3, keep=True)


def lead(doc, markup):
    para(doc, markup, size=11.4, colour=SECOND, before=0, after=12, line=1.4)


def bullets(doc, items, size=9.8):
    for it in items:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(0.72)
        pf.first_line_indent = Cm(-0.42)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.32
        r = p.add_run("-  ")
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
        pf.left_indent = Cm(0.9)
        pf.first_line_indent = Cm(-0.9)
        pf.space_after = Pt(6)
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
        p = para(doc, term, size=10.2, colour=INK, bold=True, before=9,
                 after=2, indent=0.3, keep=True)
        left_bar(p, UV_HEX)
        p2 = para(doc, body, size=9.6, colour=SECOND, after=4, indent=0.3,
                  line=1.34)
        left_bar(p2, HAIR_HEX)


def note(doc, markup):
    p = para(doc, markup, size=9.4, colour=SECOND, before=9, after=10,
             indent=0.28, line=1.34)
    shade_par(p, WASH_HEX)
    left_bar(p, LIME_HEX, size="24")


def quote(doc, markup):
    para(doc, markup, size=13.2, colour=UV, bold=True, before=12, after=12,
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
        write(p, value, 18, UV, bold=True)
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
    X.insert_ordered(hdr._tr.get_or_add_trPr(), "w:tblHeader", X.TRPR,
                     {"w:val": "true"})
    for cell, head, w in zip(hdr.cells, heads, widths):
        cell.width = Cm(w)
        X.tc_shade(cell, INK_HEX)
        X.tc_margins(cell, top=0.14, start=0.16, bottom=0.14, end=0.14)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.16
        write(p, head, size - 0.5, WHITE, bold=True)

    for i, row in enumerate(rows):
        total = str(row[0]).strip().lower().startswith("total")
        X.insert_ordered(t.rows[i + 1]._tr.get_or_add_trPr(), "w:cantSplit",
                         X.TRPR, {"w:val": "true"})
        for j, (cell, val, w) in enumerate(zip(t.rows[i + 1].cells, row,
                                               widths)):
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
            colour = INK if bold else SECOND
            write(p, val, size, colour, bold=bold)
    para(doc, "", size=4, after=7)
    return t


RENDER = {
    "h2": lambda d, b: h2(d, b[1]),
    "h3": lambda d, b: h3(d, b[1]),
    "lead": lambda d, b: lead(d, b[1]),
    "p": lambda d, b: para(d, b[1]),
    "bullets": lambda d, b: bullets(d, b[1]),
    "numbers": lambda d, b: numbers(d, b[1]),
    "deflist": lambda d, b: deflist(d, b[1]),
    "note": lambda d, b: note(d, b[1]),
    "quote": lambda d, b: quote(d, b[1]),
    "kpi": lambda d, b: kpi(d, b[1]),
    "table": lambda d, b: table(d, b[1], b[2],
                                b[3] if len(b) > 3 else None),
}


# ---------------------------------------------------------------- furniture
FAINT = RGBColor(0x9A, 0xA0, 0xAF)


def set_margins(section):
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
    write(hp, f"STARTPAD  |  {I.NAME.upper()}  |  EGYPT", 7.4, FAINT,
          bold=True, spacing=24)
    pbdr = X.insert_ordered(hp._p.get_or_add_pPr(), "w:pBdr", X.PPR)
    el = OxmlElement("w:bottom")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), "4")
    el.set(qn("w:color"), HAIR_HEX)
    pbdr.append(el)

    fp = section.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp.paragraph_format.space_before = Pt(2)
    write(fp, I.WAVE + "          ", 7.4, FAINT)
    field(fp, " PAGE ")


def cover(doc):
    para(doc, "", size=10, after=0)
    para(doc, "", size=10, after=0)
    p = para(doc, "SPONSORSHIP FRAMEWORK", size=8.6, colour=UV, bold=True,
             after=10, spacing=36)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para(doc, K.TITLE, size=34, colour=INK, bold=True, after=2, line=1.06)
    para(doc, I.NAME_AR, size=19, colour=UV, bold=True, after=14, line=1.2,
         align=WD_ALIGN_PARAGRAPH.RIGHT)
    rule(doc, UV_HEX, "12", before=0, after=14)
    para(doc, I.STRAPLINE, size=13.6, colour=SECOND, after=18, line=1.34)

    f = K.F
    kpi(doc, [
        (K.n(f["Registered founders"]), "first-time founders in wave 1"),
        (K.n(f["People reached"]), "people reached"),
        (K.n(f["Ideas in the bank"]), "ideas in the bank"),
        ("6", "months, March to August 2027"),
    ])
    para(doc, "", size=8, after=10)
    deflist(doc, [
        ("For CSR sponsors",
         I.ROLES["CSR sponsor"]["asked_for"] + ". "
         + I.ROLES["CSR sponsor"]["gets"]),
        ("For NGOs and development partners",
         I.ROLES["NGO and development partner"]["asked_for"] + ". "
         + I.ROLES["NGO and development partner"]["gets"]),
        ("For youth foundations",
         I.ROLES["Community supporter"]["asked_for"] + ". "
         + I.ROLES["Community supporter"]["gets"]),
    ])
    para(doc, "", size=8, after=12)
    para(doc, "StartPad", size=10.4, colour=INK, bold=True, after=1)
    para(doc, "Cairo, Egypt", size=9.2, colour=MUTED, after=0)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def contents(doc):
    para(doc, "CONTENTS", size=8.6, colour=UV, bold=True, after=8,
         spacing=36)
    rule(doc, HAIR_HEX, "6", before=0, after=10)
    for i, (name, _) in enumerate(K.SECTIONS, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.2
        write(p, f"{i:02d}", 9.4, UV, bold=True)
        write(p, f"      {name}", 10.6, INK, bold=True)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# --------------------------------------------------------------- the gate
def document_text(doc):
    for p in doc.paragraphs:
        yield p.text
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                yield cell.text
    for s in doc.sections:
        for part in (s.header, s.footer):
            for p in part.paragraphs:
                yield p.text


def check_document(doc):
    """No typographic marks that read as machine written.

    The same gate the business plan carries. Arabic is content and is left
    alone; everything else outside plain ASCII is a mark somebody typed by
    habit.
    """
    found = []
    for text in document_text(doc):
        for ch, label in FORBIDDEN.items():
            if ch in text:
                found.append(f"{label} in {text.strip()[:60]!r}")
    return found


def properties(doc):
    cp = doc.core_properties
    cp.title = f"{I.NAME}: sponsorship framework"
    cp.subject = f"Sponsorship framework, Egypt, {I.WAVE}"
    cp.author = "StartPad"
    cp.last_modified_by = "StartPad"
    cp.comments = ""
    cp.category = ""
    cp.keywords = ""
    cp.created = FIXED_TIMESTAMP
    cp.modified = FIXED_TIMESTAMP


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
        for b in blocks:
            RENDER[b[0]](doc, b)

    properties(doc)
    bad = check_document(doc)
    if bad:
        raise SystemExit("\n".join(bad[:20] + [f"{len(bad)} in all"]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)
    normalize_zip(path)
    return path


if __name__ == "__main__":
    out = (sys.argv[1] if len(sys.argv) > 1 else
           os.path.join(OUT, "StartPad_Initiative_Framework.docx"))
    build(out)
    print(f"wrote {out}  ({os.path.getsize(out)/1024:,.0f} KB)")
    print(f"{len(K.SECTIONS)} sections")
