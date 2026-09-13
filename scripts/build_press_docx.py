# -*- coding: utf-8 -*-
"""
Build the bilingual press release .docx from press/release.py.

Arabic and English are the same document: Arabic first (right-to-left), a page
break, then English. Word needs three separate signals to lay Arabic out
correctly — `w:bidi` on the paragraph, `w:rtl` on each run, and a complex-script
font and size (`w:rFonts w:cs`, `w:szCs`) — because the Latin font properties are
ignored for Arabic glyphs. Setting only the alignment produces a document that
looks right-aligned but still breaks punctuation and mixed AR/EN runs.
"""
import os
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from press.release import NOTES_SOURCES, VERSIONS  # noqa: E402
from scripts._determinism import FIXED_TIMESTAMP, normalize_zip  # noqa: E402

INK = RGBColor(0x1F, 0x29, 0x33)
GREEN = RGBColor(0x0F, 0x5C, 0x4B)
GREY = RGBColor(0x5A, 0x6B, 0x66)

LATIN_FONT = "Calibri"
ARABIC_FONT = "Arial"


def _bidi(p):
    pPr = p._p.get_or_add_pPr()
    el = OxmlElement("w:bidi")
    el.set(qn("w:val"), "1")
    pPr.append(el)


def _style_run(run, size, rtl):
    run.font.size = Pt(size)
    rPr = run._r.get_or_add_rPr()
    # Complex-script size is a separate property; without it Arabic renders at the
    # default 10pt no matter what run.font.size says.
    szCs = OxmlElement("w:szCs")
    szCs.set(qn("w:val"), str(int(size * 2)))
    rPr.append(szCs)
    if rtl:
        fonts = OxmlElement("w:rFonts")
        fonts.set(qn("w:cs"), ARABIC_FONT)
        rPr.append(fonts)
        el = OxmlElement("w:rtl")
        el.set(qn("w:val"), "1")
        rPr.append(el)


def para(doc, text="", size=11, bold=False, italic=False, color=INK, rtl=False,
         space_before=0, space_after=6, align=None, indent=0, line=1.25):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    if indent:
        pf.left_indent = Cm(indent)
        pf.right_indent = Cm(indent)
    if rtl:
        _bidi(p)
        p.alignment = align if align is not None else WD_ALIGN_PARAGRAPH.RIGHT
    else:
        p.alignment = align if align is not None else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    _style_run(r, size, rtl)
    return p


def rule(doc, color="0F5C4B", size="6"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:color"), color)
    pbdr.append(bottom)
    pPr.append(pbdr)


def bullet(doc, text, rtl):
    # The marker leads on the reading side, so it has to flip with the language.
    prefix = "•  "
    p = para(doc, prefix + text, size=10.5, rtl=rtl, indent=0.7, space_after=4)
    return p


def render(doc, v):
    rtl = v["dir"] == "rtl"
    para(doc, "STARTPAD  ×  GROWTHLABS", size=10, bold=True, color=GREEN, rtl=rtl,
         space_after=2)
    para(doc, v["kicker"], size=9.5, bold=True, color=GREY, rtl=rtl, space_after=10)
    rule(doc)
    para(doc, v["headline"], size=19, bold=True, color=INK, rtl=rtl,
         space_after=6, line=1.15)
    para(doc, v["subhead"], size=12, italic=True, color=GREY, rtl=rtl,
         space_after=14, line=1.3)
    para(doc, v["dateline"], size=10.5, bold=True, color=GREEN, rtl=rtl,
         space_after=10)

    for block in v["blocks"]:
        kind = block[0]
        if kind == "h":
            para(doc, block[1], size=13, bold=True, color=GREEN, rtl=rtl,
                 space_before=14, space_after=5)
        elif kind == "p":
            para(doc, block[1], size=11, rtl=rtl, space_after=8)
        elif kind == "b":
            for item in block[1]:
                bullet(doc, item, rtl)
        elif kind == "q":
            para(doc, "“" + block[1] + "”", size=11.5, italic=True, color=INK,
                 rtl=rtl, indent=0.8, space_before=6, space_after=2)
            para(doc, "— " + block[2], size=10, bold=True, color=GREEN, rtl=rtl,
                 indent=0.8, space_after=10)
        elif kind == "kv":
            for label, value in block[1]:
                p = para(doc, "", size=10.5, rtl=rtl, space_after=3)
                r = p.add_run(label + ": ")
                r.font.bold = True
                r.font.color.rgb = INK
                _style_run(r, 10.5, rtl)
                r2 = p.add_run(value)
                r2.font.color.rgb = INK
                _style_run(r2, 10.5, rtl)

    para(doc, "###", size=11, bold=True, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=4)


def build(out_path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = LATIN_FONT
    st.font.size = Pt(11)
    st.font.color.rgb = INK
    for s in doc.sections:
        s.top_margin = Cm(2.0)
        s.bottom_margin = Cm(2.0)
        s.left_margin = Cm(2.2)
        s.right_margin = Cm(2.2)

    for i, v in enumerate(VERSIONS):
        if i:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        render(doc, v)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    para(doc, "Fact-check sources", size=13, bold=True, color=GREEN, space_after=4)
    para(doc,
         "Every figure in this release was taken from the sources below during "
         "drafting, not from memory. Confirm them against the live pages before "
         "distribution — and confirm StartPad's own product claims against the "
         "platform.",
         size=10.5, color=GREY, space_after=8)
    for label, url in NOTES_SOURCES:
        p = para(doc, "", size=10, space_after=3, indent=0.4)
        r = p.add_run("•  " + label + " — ")
        r.font.color.rgb = INK
        _style_run(r, 10, False)
        r2 = p.add_run(url)
        r2.font.color.rgb = RGBColor(0x1D, 0x6F, 0xA3)
        _style_run(r2, 10, False)

    core = doc.core_properties
    core.title = "StartPad × GrowthLabs — LEAP launch press release"
    core.author = "Abdelrhman Soliman"
    core.created = FIXED_TIMESTAMP
    core.modified = FIXED_TIMESTAMP

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    doc.save(out_path)
    normalize_zip(out_path)
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else \
        "output/StartPad_LEAP_Launch_Press_Release.docx"
    path = build(out)
    print("wrote", path, os.path.getsize(path), "bytes")
