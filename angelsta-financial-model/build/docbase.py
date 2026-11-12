"""Shared Word styling for Angelsta documents."""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEAL = RGBColor(0x0D, 0x2B, 0x30)
ACCENT = RGBColor(0x0E, 0x5A, 0x5F)
GREY = RGBColor(0x5F, 0x67, 0x70)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def _field(run, instr):
    for t, v in [("begin", None), (None, instr), ("end", None)]:
        if t:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), t)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = v
        run._r.append(el)


class Doc:
    def __init__(self, header_text):
        self.d = Document()
        self.fig_n = 0
        self.tab_n = 0
        for s in self.d.sections:
            s.left_margin = s.right_margin = Cm(2.0)
            s.top_margin = s.bottom_margin = Cm(1.8)
        st = self.d.styles["Normal"]
        st.font.name = "Arial"
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        st.font.size = Pt(10)
        for name, size, color in [("Heading 1", 16, TEAL), ("Heading 2", 12.5, ACCENT), ("Heading 3", 11, TEAL)]:
            h = self.d.styles[name]
            h.font.name = "Arial"
            h.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
            h.font.size = Pt(size)
            h.font.bold = True
            h.font.color.rgb = color
        sec = self.d.sections[0]
        sec.different_first_page_header_footer = True
        hp = sec.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = hp.add_run(header_text)
        r.font.size = Pt(7.5)
        r.font.color.rgb = GREY
        r.bold = True
        fp = sec.footer.paragraphs[0]
        r = fp.add_run("Angelsta  |  Strictly confidential  |  Page ")
        r.font.size = Pt(7.5)
        r.font.color.rgb = GREY
        r2 = fp.add_run()
        r2.font.size = Pt(7.5)
        _field(r2, "PAGE")

    # text ---------------------------------------------------------------
    def para(self, text, bold=False, italic=False, color=None, size=None, align=None, after=4):
        p = self.d.add_paragraph()
        r = p.add_run(text)
        r.bold, r.italic = bold, italic
        if color:
            r.font.color.rgb = color
        if size:
            r.font.size = Pt(size)
        if align:
            p.alignment = align
        p.paragraph_format.space_after = Pt(after)
        return p

    def note(self, text):
        return self.para(text, italic=True, color=GREY, size=8.5)

    def h1(self, t):
        return self.d.add_heading(t, level=1)

    def h2(self, t):
        return self.d.add_heading(t, level=2)

    def bullets(self, items, numbered=False):
        for it in items:
            p = self.d.add_paragraph(style="List Number" if numbered else "List Bullet")
            if isinstance(it, tuple):
                r = p.add_run(it[0])
                r.bold = True
                p.add_run(it[1])
            else:
                p.add_run(it)
            p.paragraph_format.space_after = Pt(2)

    def callout(self, title, text, fill="E6F1EF"):
        t = self.d.add_table(rows=1, cols=1)
        c = t.cell(0, 0)
        shade(c, fill)
        c.text = ""
        p = c.paragraphs[0]
        r = p.add_run(title)
        r.bold = True
        r.font.color.rgb = ACCENT
        r.font.size = Pt(10)
        p2 = c.add_paragraph()
        r2 = p2.add_run(text)
        r2.font.size = Pt(9)
        self.d.add_paragraph().paragraph_format.space_after = Pt(2)

    def kpis(self, items, fill="0D2B30"):
        """Infographic strip of headline numbers: list of (value, label)."""
        t = self.d.add_table(rows=2, cols=len(items))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for j, (v, lab) in enumerate(items):
            for i in range(2):
                shade(t.cell(i, j), fill if j % 2 == 0 else "0E5A5F")
            c = t.cell(0, j)
            c.text = ""
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(v)
            r.bold = True
            r.font.size = Pt(16)
            r.font.color.rgb = WHITE
            c = t.cell(1, j)
            c.text = ""
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(lab)
            r.font.size = Pt(7.5)
            r.font.color.rgb = RGBColor(0xCF, 0xE6, 0xE1)
        self.d.add_paragraph().paragraph_format.space_after = Pt(2)

    def table(self, rows, widths=None, first_bold=False, font=8.2, zebra=True, header_fill="0D2B30", caption=None, highlight=None):
        if caption:
            self.tab_n += 1
            self.para(f"Table {self.tab_n}. {caption}", bold=True, size=8.5, color=ACCENT, after=2)
        t = self.d.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                c = t.cell(i, j)
                c.text = ""
                r = c.paragraphs[0].add_run(str(val))
                r.font.size = Pt(font)
                if i == 0:
                    r.bold = True
                    r.font.color.rgb = WHITE
                    shade(c, header_fill)
                else:
                    if first_bold and j == 0:
                        r.bold = True
                    if highlight and highlight(row):
                        shade(c, "FFF3CC")
                    elif zebra and i % 2 == 0:
                        shade(c, "EEF5F4")
        if widths:
            tblPr = t._tbl.tblPr
            lay = OxmlElement("w:tblLayout")
            lay.set(qn("w:type"), "fixed")
            tblPr.append(lay)
            for gc, w in zip(t._tbl.tblGrid.gridCol_lst, widths):
                gc.w = Cm(w)
            for row in t.rows:
                for j, w in enumerate(widths):
                    row.cells[j].width = Cm(w)
        self.d.add_paragraph().paragraph_format.space_after = Pt(2)
        return t

    def figure(self, path, caption, width=16.5, source=None):
        self.fig_n += 1
        p = self.d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=Cm(width))
        cap = self.para(f"Figure {self.fig_n}. {caption}", bold=True, size=8.5, color=ACCENT, align=WD_ALIGN_PARAGRAPH.CENTER, after=1)
        if source:
            self.para(f"Source: {source}", italic=True, size=7.5, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=6)

    def cover(self, title, subtitle, tagline, meta):
        for _ in range(3):
            self.d.add_paragraph()
        self.para("CONFIDENTIAL  ·  PRE-SEED 2026", bold=True, color=ACCENT, size=9)
        self.para(title, bold=True, size=30, color=TEAL, after=0)
        self.para(subtitle, size=16, color=ACCENT, after=4)
        self.para(tagline, italic=True, color=GREY, size=10.5, after=18)
        self.table(meta, widths=[4, 13], first_bold=True, zebra=False, header_fill="0E5A5F")
        self.d.add_page_break()

    def contents(self, items):
        self.h1("Contents")
        for i, it in enumerate(items, 1):
            self.para(f"{i}.  {it}", size=10, after=2)
        self.d.add_page_break()

    def landscape(self):
        s = self.d.add_section()
        s.different_first_page_header_footer = False
        s.orientation = WD_ORIENT.LANDSCAPE
        s.page_width, s.page_height = s.page_height, s.page_width
        return s

    def portrait(self):
        s = self.d.add_section()
        s.different_first_page_header_footer = False
        s.orientation = WD_ORIENT.PORTRAIT
        s.page_width, s.page_height = s.page_height, s.page_width
        return s

    def page_break(self):
        self.d.add_page_break()

    def save(self, path):
        self.d.save(path)
