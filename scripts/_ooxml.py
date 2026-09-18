# -*- coding: utf-8 -*-
"""
Schema-ordered OOXML helpers.

WordprocessingML property containers are xsd:sequence, not xsd:all — the order
of children is part of the grammar. python-docx keeps that order for the
properties it sets through its own API, but anything hand-built and appended
lands after whatever the library already wrote, which is usually invalid:
`w:bidi` has to precede `w:spacing`, `w:ind` and `w:jc` inside `w:pPr`, and
`w:bidiVisual` has to precede `w:tblW` and `w:tblBorders` inside `w:tblPr`.

Word opens such a file anyway. LibreOffice refuses it outright, and Google Docs
and Pages are inconsistent about it — which matters here, because these files
are published for anyone to download. `insert_ordered` puts each element where
the schema says it goes.

Sequences below are from ECMA-376 Part 1, trimmed to the elements used in this
repository.
"""
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

PPR = ("w:pStyle", "w:keepNext", "w:keepLines", "w:pageBreakBefore", "w:framePr",
       "w:widowControl", "w:numPr", "w:suppressLineNumbers", "w:pBdr", "w:shd",
       "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
       "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
       "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
       "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
       "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
       "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr",
       "w:pPrChange")

RPR = ("w:rStyle", "w:rFonts", "w:b", "w:bCs", "w:i", "w:iCs", "w:caps",
       "w:smallCaps", "w:strike", "w:dstrike", "w:outline", "w:shadow",
       "w:emboss", "w:imprint", "w:noProof", "w:snapToGrid", "w:vanish",
       "w:webHidden", "w:color", "w:spacing", "w:w", "w:kern", "w:position",
       "w:sz", "w:szCs", "w:highlight", "w:u", "w:effect", "w:bdr", "w:shd",
       "w:fitText", "w:vertAlign", "w:rtl", "w:cs", "w:em", "w:lang",
       "w:eastAsianLayout", "w:specVanish", "w:oMath")

TCPR = ("w:cnfStyle", "w:tcW", "w:gridSpan", "w:hMerge", "w:vMerge",
        "w:tcBorders", "w:shd", "w:noWrap", "w:tcMar", "w:textDirection",
        "w:tcFitText", "w:vAlign", "w:hideMark", "w:headers")

TBLPR = ("w:tblStyle", "w:tblpPr", "w:tblOverlap", "w:bidiVisual",
         "w:tblStyleRowBandSize", "w:tblStyleColBandSize", "w:tblW", "w:jc",
         "w:tblCellSpacing", "w:tblInd", "w:tblBorders", "w:shd", "w:tblLayout",
         "w:tblCellMar", "w:tblLook", "w:tblCaption", "w:tblDescription")

TRPR = ("w:cnfStyle", "w:divId", "w:gridBefore", "w:gridAfter", "w:wBefore",
        "w:wAfter", "w:cantSplit", "w:trHeight", "w:tblHeader",
        "w:tblCellSpacing", "w:jc", "w:hidden")

SECTPR = ("w:headerReference", "w:footerReference", "w:footnotePr",
          "w:endnotePr", "w:type", "w:pgSz", "w:pgMar", "w:paperSrc",
          "w:pgBorders", "w:lnNumType", "w:pgNumType", "w:cols", "w:formProt",
          "w:vAlign", "w:noEndnote", "w:titlePg", "w:textDirection", "w:bidi",
          "w:rtlGutter", "w:docGrid")


def insert_ordered(parent, tagname, seq, attrs=None, replace=True):
    """
    Put `tagname` into `parent` at the position the schema requires.

    Returns the element. With replace=True an existing element of the same tag
    is reused, so calling twice does not produce two `w:shd` children — which
    Word renders unpredictably.
    """
    existing = parent.find(qn(tagname))
    if existing is not None and replace:
        el = existing
    else:
        el = OxmlElement(tagname)
        try:
            after = seq[seq.index(tagname) + 1:]
        except ValueError:
            after = ()
        successor = None
        for child in parent:
            for name in after:
                if child.tag == qn(name):
                    successor = child
                    break
            if successor is not None:
                break
        if successor is not None:
            successor.addprevious(el)
        else:
            parent.append(el)
    for k, v in (attrs or {}).items():
        el.set(qn(k), str(v))
    return el


# --------------------------------------------------------------- paragraph/run
def para_rtl(paragraph):
    """Right-to-left paragraph. Must precede spacing, ind and jc in w:pPr."""
    insert_ordered(paragraph._p.get_or_add_pPr(), "w:bidi", PPR, {"w:val": "1"})


def run_cs(run, font, size_pt, rtl=False):
    """Complex-script font and size — Word ignores the Latin ones for Arabic."""
    rPr = run._r.get_or_add_rPr()
    fonts = insert_ordered(rPr, "w:rFonts", RPR)
    fonts.set(qn("w:cs"), font)
    insert_ordered(rPr, "w:szCs", RPR, {"w:val": str(int(size_pt * 2))})
    if rtl:
        insert_ordered(rPr, "w:rtl", RPR, {"w:val": "1"})


def run_spacing(run, twentieths):
    insert_ordered(run._r.get_or_add_rPr(), "w:spacing", RPR,
                   {"w:val": str(int(twentieths))})


# ----------------------------------------------------------------- table parts
def tc_shade(cell, hexcolor):
    insert_ordered(cell._tc.get_or_add_tcPr(), "w:shd", TCPR,
                   {"w:val": "clear", "w:fill": hexcolor})


def tc_margins(cell, top=0.14, start=0.18, bottom=0.14, end=0.18):
    mar = insert_ordered(cell._tc.get_or_add_tcPr(), "w:tcMar", TCPR)
    for child in list(mar):
        mar.remove(child)
    for tag, val in (("w:top", top), ("w:start", start), ("w:bottom", bottom),
                     ("w:end", end)):
        el = OxmlElement(tag)
        el.set(qn("w:w"), str(int(val * 567)))
        el.set(qn("w:type"), "dxa")
        mar.append(el)


def tc_valign(cell, val="top"):
    insert_ordered(cell._tc.get_or_add_tcPr(), "w:vAlign", TCPR, {"w:val": val})


def tbl_rtl(table):
    """Reverses column order so an Arabic table reads right-to-left."""
    insert_ordered(table._tbl.tblPr, "w:bidiVisual", TBLPR, {"w:val": "1"})


def tbl_borders(table, color="D8DCE2", sz="6", style="single"):
    el = insert_ordered(table._tbl.tblPr, "w:tblBorders", TBLPR)
    for child in list(el):
        el.remove(child)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), style)
        e.set(qn("w:sz"), sz)
        e.set(qn("w:color"), color)
        el.append(e)


def tbl_fixed_layout(table):
    insert_ordered(table._tbl.tblPr, "w:tblLayout", TBLPR, {"w:type": "fixed"})


def tr_height(row, cm, rule="atLeast"):
    insert_ordered(row._tr.get_or_add_trPr(), "w:trHeight", TRPR,
                   {"w:val": str(int(cm * 567)), "w:hRule": rule})


def sect_rtl(section):
    insert_ordered(section._sectPr, "w:bidi", SECTPR, {"w:val": "1"})
