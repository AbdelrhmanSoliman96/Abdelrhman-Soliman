# -*- coding: utf-8 -*-
import copy
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "assets", "leap-logo.png")
OUT = os.path.join(ROOT, "تقرير-اجتماع-13-سبتمبر-2026.docx")

BLACK = "000000"
DARK  = "333333"
LIGHT = "F2F2F2"
WHITE = "FFFFFF"
MID   = "9A9A9A"
FONT  = "Cairo"

# ----------------------------------------------------------------- xml helpers
PPR_ORDER = ["w:pStyle","w:keepNext","w:keepLines","w:pageBreakBefore","w:framePr",
    "w:widowControl","w:numPr","w:suppressLineNumbers","w:pBdr","w:shd","w:tabs",
    "w:suppressAutoHyphens","w:kinsoku","w:wordWrap","w:overflowPunct","w:topLinePunct",
    "w:autoSpaceDE","w:autoSpaceDN","w:bidi","w:adjustRightInd","w:snapToGrid","w:spacing",
    "w:ind","w:contextualSpacing","w:mirrorIndents","w:suppressOverlap","w:jc",
    "w:textDirection","w:textAlignment","w:textboxTightWrap","w:outlineLvl","w:divId",
    "w:cnfStyle","w:rPr","w:sectPr","w:pPrChange"]

RPR_ORDER = ["w:rStyle","w:rFonts","w:b","w:bCs","w:i","w:iCs","w:caps","w:smallCaps",
    "w:strike","w:dstrike","w:outline","w:shadow","w:emboss","w:imprint","w:noProof",
    "w:snapToGrid","w:vanish","w:webHidden","w:color","w:spacing","w:w","w:kern",
    "w:position","w:sz","w:szCs","w:highlight","w:u","w:effect","w:bdr","w:shd",
    "w:fitText","w:vertAlign","w:rtl","w:cs","w:em","w:lang","w:eastAsianLayout",
    "w:specVanish","w:oMath"]

TBLPR_ORDER = ["w:tblStyle","w:tblpPr","w:tblOverlap","w:bidiVisual","w:tblStyleRowBandSize",
    "w:tblStyleColBandSize","w:tblW","w:jc","w:tblCellSpacing","w:tblInd","w:tblBorders",
    "w:shd","w:tblLayout","w:tblCellMar","w:tblLook","w:tblCaption","w:tblDescription"]

TCPR_ORDER = ["w:cnfStyle","w:tcW","w:gridSpan","w:hMerge","w:vMerge","w:tcBorders","w:shd",
    "w:noWrap","w:tcMar","w:textDirection","w:tcFitText","w:vAlign","w:hideMark"]

TRPR_ORDER = ["w:cnfStyle","w:divId","w:gridBefore","w:gridAfter","w:wBefore","w:wAfter",
    "w:cantSplit","w:trHeight","w:tblHeader","w:tblCellSpacing","w:jc","w:hidden"]

SECTPR_ORDER = ["w:headerReference","w:footerReference","w:footnotePr","w:endnotePr","w:type",
    "w:pgSz","w:pgMar","w:paperSrc","w:pgBorders","w:lnNumType","w:pgNumType","w:cols",
    "w:formProt","w:vAlign","w:noEndnote","w:titlePg","w:textDirection","w:bidi",
    "w:rtlGutter","w:docGrid","w:printerSettings","w:sectPrChange"]

# tags that may appear only once inside a properties element
SINGLETON_SKIP = {"w:headerReference", "w:footerReference", "w:tab", "w:cols"}

def reorder(el, order):
    idx = {t: i for i, t in enumerate(order)}
    kids = list(el)
    kids.sort(key=lambda k: idx.get(k.tag.split('}')[0].replace('{http://schemas.openxmlformats.org/wordprocessingml/2006/main','w')+'}'+k.tag.split('}')[1] if False else _tag(k), 10**6))
    for k in kids:
        el.append(k)

def _tag(el):
    t = el.tag
    if t.startswith('{'):
        uri, local = t[1:].split('}')
        return 'w:' + local
    return t

def dedupe(el):
    """keep the LAST occurrence of each child tag (our explicit overrides win)"""
    seen = {}
    for k in list(el):
        t = _tag(k)
        if t in SINGLETON_SKIP:
            continue
        seen.setdefault(t, []).append(k)
    for t, kids in seen.items():
        for k in kids[:-1]:
            el.remove(k)


def reorder_all(doc_part_element):
    for tag, order in (('w:pPr', PPR_ORDER), ('w:rPr', RPR_ORDER),
                       ('w:tblPr', TBLPR_ORDER), ('w:tcPr', TCPR_ORDER),
                       ('w:trPr', TRPR_ORDER), ('w:sectPr', SECTPR_ORDER)):
        idx = {t: i for i, t in enumerate(order)}
        for el in doc_part_element.iter(qn(tag)):
            dedupe(el)
            kids = sorted(list(el), key=lambda k: idx.get(_tag(k), 10**6))
            for k in kids:
                el.append(k)

def sub(parent, tag, **attrs):
    el = OxmlElement(tag)
    for k, v in attrs.items():
        el.set(qn('w:' + k), v)
    parent.append(el)
    return el

# ------------------------------------------------------------ text primitives
def rtl_par(p, align='start', space_before=0, space_after=6, line=1.5, keep_next=False):
    pPr = p._p.get_or_add_pPr()
    sub(pPr, 'w:bidi')
    if keep_next:
        sub(pPr, 'w:keepNext')
    sp = sub(pPr, 'w:spacing', before=str(int(space_before*20)),
             after=str(int(space_after*20)))
    sp.set(qn('w:line'), str(int(line*240)))
    sp.set(qn('w:lineRule'), 'auto')
    # 'start' is the default for a bidi paragraph, so it is left implicit;
    # w:jc left/right are direction-relative in Word/LibreOffice, which would
    # flip them in an RTL paragraph.
    jc = {'start': None, 'end': 'end', 'center': 'center', 'both': 'both'}[align]
    if jc:
        sub(pPr, 'w:jc', val=jc)
    return p

def run(p, text, size=11, bold=False, color=BLACK, font=FONT, rtl=True,
        spacing=None, caps=False, italic=False):
    r = p.add_run(text)
    rPr = r._r.get_or_add_rPr()
    rf = OxmlElement('w:rFonts')
    for a in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
        rf.set(qn('w:' + a), font)
    rPr.append(rf)
    if bold:
        sub(rPr, 'w:b'); sub(rPr, 'w:bCs')
    if italic:
        sub(rPr, 'w:i'); sub(rPr, 'w:iCs')
    if caps:
        sub(rPr, 'w:caps')
    sub(rPr, 'w:color', val=color)
    if spacing is not None:
        sub(rPr, 'w:spacing', val=str(int(spacing*20)))
    sub(rPr, 'w:sz', val=str(int(size*2)))
    sub(rPr, 'w:szCs', val=str(int(size*2)))
    if rtl:
        sub(rPr, 'w:rtl')
    return r

def para(container, text=None, **kw):
    style = kw.pop('style', None)
    p = container.add_paragraph(style=style) if style else container.add_paragraph()
    rtl_par(p, align=kw.pop('align', 'both'),
            space_before=kw.pop('space_before', 0),
            space_after=kw.pop('space_after', 6),
            line=kw.pop('line', 1.45),
            keep_next=kw.pop('keep_next', False))
    if text:
        run(p, text, **kw)
    return p

def shade(el_pr, fill):
    sub(el_pr, 'w:shd', val='clear', color='auto', fill=fill)

def par_borders(p, bottom=None, top=None, left=None, right=None):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr')
    for name, spec in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        if spec:
            sz, color = spec
            e = OxmlElement('w:' + name)
            e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz))
            e.set(qn('w:space'), '4'); e.set(qn('w:color'), color)
            bdr.append(e)
    pPr.append(bdr)

# --------------------------------------------------------------- table helpers
def make_table(doc, rows, cols, widths_cm):
    t = doc.add_table(rows=rows, cols=cols)
    t.autofit = False
    tblPr = t._tbl.tblPr
    sub(tblPr, 'w:bidiVisual')
    total = int(round(sum(widths_cm) * 567))
    sub(tblPr, 'w:tblW', w=str(total), type='dxa')
    sub(tblPr, 'w:tblLayout', type='fixed')
    grid = t._tbl.find(qn('w:tblGrid'))
    for gc in list(grid):
        grid.remove(gc)
    for w in widths_cm:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), str(int(round(w * 567))))
        grid.append(gc)
    cm = OxmlElement('w:tblCellMar')
    for side, v in (('top', 100), ('start', 130), ('bottom', 100), ('end', 130)):
        e = OxmlElement('w:' + side)
        e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa')
        cm.append(e)
    tblPr.append(cm)
    # borders
    bd = OxmlElement('w:tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + side)
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4')
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), 'D6D6D6')
        bd.append(e)
    tblPr.append(bd)
    for row in t.rows:
        for i, c in enumerate(row.cells):
            c.width = Cm(widths_cm[i])
    for i, w in enumerate(widths_cm):
        for row in t.rows:
            row.cells[i].width = Cm(w)
    return t

def cell_text(cell, text, size=10.5, bold=False, color=BLACK, fill=None,
              align='start', space_after=0, space_before=0, line=1.3):
    cell.text = ''
    p = cell.paragraphs[0]
    rtl_par(p, align=align, space_after=space_after, space_before=space_before, line=line)
    if text != '':
        run(p, text, size=size, bold=bold, color=color)
    if fill:
        shade(cell._tc.get_or_add_tcPr(), fill)
    vA = OxmlElement('w:vAlign'); vA.set(qn('w:val'), 'center')
    cell._tc.get_or_add_tcPr().append(vA)
    return p

def row_shade(row, fill):
    for c in row.cells:
        shade(c._tc.get_or_add_tcPr(), fill)

def keep_row_together(row):
    trPr = row._tr.get_or_add_trPr()
    sub(trPr, 'w:cantSplit')

def header_row_repeat(row):
    trPr = row._tr.get_or_add_trPr()
    sub(trPr, 'w:tblHeader')

# =============================================================== DOCUMENT
doc = Document()

# default style
st = doc.styles['Normal']
st.font.name = FONT
st.font.size = Pt(11)
rpr = st.element.get_or_add_rPr()
rf = OxmlElement('w:rFonts')
for a in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
    rf.set(qn('w:' + a), FONT)
rpr.append(rf)
sub(rpr, 'w:szCs', val='22')
sub(rpr, 'w:rtl')
_npPr = st.element.get_or_add_pPr()
sub(_npPr, 'w:bidi')

sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin = Cm(3.6)
sec.bottom_margin = Cm(2.4)
sec.left_margin = Cm(2.0)
sec.right_margin = Cm(2.0)
sec.header_distance = Cm(1.1)
sec.footer_distance = Cm(1.0)
sub(sec._sectPr, 'w:bidi')

CONTENT_W = 21.0 - 4.0   # 17 cm

# ------------------------------------------------------------------- HEADER
hdr = sec.header
hdr.is_linked_to_previous = False
for p in list(hdr.paragraphs):
    p._p.getparent().remove(p._p)

ht = hdr.add_table(rows=1, cols=2, width=Cm(CONTENT_W))
ht.autofit = False
tblPr = ht._tbl.tblPr
sub(tblPr, 'w:bidiVisual')
sub(tblPr, 'w:tblW', w=str(int(CONTENT_W * 567)), type='dxa')
sub(tblPr, 'w:tblLayout', type='fixed')
_grid = ht._tbl.find(qn('w:tblGrid'))
for _gc in list(_grid):
    _grid.remove(_gc)
for _w in (6.6, CONTENT_W - 6.6):
    _e = OxmlElement('w:gridCol'); _e.set(qn('w:w'), str(int(round(_w * 567))))
    _grid.append(_e)
bd = OxmlElement('w:tblBorders')
for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
    e = OxmlElement('w:' + side); e.set(qn('w:val'), 'none'); e.set(qn('w:sz'), '0')
    e.set(qn('w:space'), '0'); e.set(qn('w:color'), 'auto'); bd.append(e)
tblPr.append(bd)
cmar = OxmlElement('w:tblCellMar')
for side in ('top', 'start', 'bottom', 'end'):
    e = OxmlElement('w:' + side); e.set(qn('w:w'), '0'); e.set(qn('w:type'), 'dxa')
    cmar.append(e)
tblPr.append(cmar)

c_logo, c_meta = ht.rows[0].cells
c_logo.width = Cm(6.6); c_meta.width = Cm(CONTENT_W - 6.6)

p = c_logo.paragraphs[0]
rtl_par(p, align='start', space_after=0, line=1.0)
p.add_run().add_picture(LOGO, width=Cm(5.4))

p = c_meta.paragraphs[0]
rtl_par(p, align='end', space_after=0, line=1.25)
run(p, "تقرير اجتماع", size=10, bold=True, color=BLACK)
p2 = c_meta.add_paragraph(); rtl_par(p2, align='end', space_after=0, line=1.25)
run(p2, "الأحد  13  سبتمبر  2026", size=9, color=DARK)
p3 = c_meta.add_paragraph(); rtl_par(p3, align='end', space_after=0, line=1.25)
run(p3, "وثيقة داخلية", size=8, color=MID)
for cc in (c_logo, c_meta):
    vA = OxmlElement('w:vAlign'); vA.set(qn('w:val'), 'bottom')
    cc._tc.get_or_add_tcPr().append(vA)

rule = hdr.add_paragraph()
rtl_par(rule, align='start', space_before=4, space_after=0, line=1.0)
par_borders(rule, bottom=(12, BLACK))
run(rule, "", size=2)
rule2 = hdr.add_paragraph()
rtl_par(rule2, align='start', space_before=1, space_after=0, line=1.0)
par_borders(rule2, bottom=(4, MID))
run(rule2, "", size=2)

# ------------------------------------------------------------------- FOOTER
ftr = sec.footer
ftr.is_linked_to_previous = False
for p in list(ftr.paragraphs):
    p._p.getparent().remove(p._p)

frule = ftr.add_paragraph()
rtl_par(frule, align='start', space_before=0, space_after=4, line=1.0)
par_borders(frule, bottom=(4, "D6D6D6"))
run(frule, "", size=2)

def borderless(tbl, widths_cm, cell_pad=0):
    tp = tbl._tbl.tblPr
    sub(tp, 'w:bidiVisual')
    sub(tp, 'w:tblW', w=str(int(round(sum(widths_cm) * 567))), type='dxa')
    sub(tp, 'w:tblLayout', type='fixed')
    bd = OxmlElement('w:tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + side)
        e.set(qn('w:val'), 'none'); e.set(qn('w:sz'), '0')
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), 'auto')
        bd.append(e)
    tp.append(bd)
    cm = OxmlElement('w:tblCellMar')
    for side in ('top', 'start', 'bottom', 'end'):
        e = OxmlElement('w:' + side)
        e.set(qn('w:w'), str(cell_pad)); e.set(qn('w:type'), 'dxa')
        cm.append(e)
    tp.append(cm)
    g = tbl._tbl.find(qn('w:tblGrid'))
    for gc in list(g):
        g.remove(gc)
    for w in widths_cm:
        e = OxmlElement('w:gridCol'); e.set(qn('w:w'), str(int(round(w * 567))))
        g.append(e)
    for i, w in enumerate(widths_cm):
        for row in tbl.rows:
            row.cells[i].width = Cm(w)
    return tbl


fw = [5.5, 6.0, CONTENT_W - 11.5]
ftbl = borderless(ftr.add_table(rows=1, cols=3, width=Cm(CONTENT_W)), fw)
fc = ftbl.rows[0].cells

fc[0].text = ''
p0 = fc[0].paragraphs[0]
rtl_par(p0, align='start', space_after=0, line=1.0)
run(p0, "LEAP Consulting", size=8.5, bold=True, color=DARK, rtl=False)

fc[1].text = ''
p1 = fc[1].paragraphs[0]
rtl_par(p1, align='center', space_after=0, line=1.0)
run(p1, "تقرير اجتماع  |  13 سبتمبر 2026", size=8.5, color=MID)

fc[2].text = ''
fp = fc[2].paragraphs[0]
rtl_par(fp, align='end', space_after=0, line=1.0)
run(fp, "صفحة ", size=8.5, color=MID)


def field(p, instr):
    r = p.add_run()
    fchar = OxmlElement('w:fldChar'); fchar.set(qn('w:fldCharType'), 'begin'); r._r.append(fchar)
    r2 = p.add_run()
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr
    r2._r.append(it)
    r3 = p.add_run()
    fchar2 = OxmlElement('w:fldChar'); fchar2.set(qn('w:fldCharType'), 'end'); r3._r.append(fchar2)
    for rr in (r, r2, r3):
        rPr = rr._r.get_or_add_rPr()
        rf2 = OxmlElement('w:rFonts')
        for a in ('ascii', 'hAnsi', 'cs'):
            rf2.set(qn('w:' + a), FONT)
        rPr.append(rf2)
        sub(rPr, 'w:color', val=MID)
        sub(rPr, 'w:sz', val='17'); sub(rPr, 'w:szCs', val='17')


field(fp, ' PAGE ')
run(fp, " من ", size=8.5, color=MID)
field(fp, ' NUMPAGES ')

# =============================================================== BODY
body = doc

# ---- title band ----
tb = make_table(body, 1, 1, [CONTENT_W])
tblPr = tb._tbl.tblPr
old = tblPr.find(qn('w:tblBorders'))
if old is not None:
    tblPr.remove(old)
bd = OxmlElement('w:tblBorders')
for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
    e = OxmlElement('w:' + side); e.set(qn('w:val'), 'none')
    e.set(qn('w:sz'), '0'); e.set(qn('w:space'), '0'); e.set(qn('w:color'), 'auto')
    bd.append(e)
tblPr.append(bd)
for _old in tblPr.findall(qn('w:tblCellMar')):
    tblPr.remove(_old)
cmar = OxmlElement('w:tblCellMar')
for side, v in (('top', 260), ('start', 300), ('bottom', 260), ('end', 300)):
    e = OxmlElement('w:' + side); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa')
    cmar.append(e)
tblPr.append(cmar)

cell = tb.rows[0].cells[0]
shade(cell._tc.get_or_add_tcPr(), BLACK)
cell.text = ''
p = cell.paragraphs[0]
rtl_par(p, align='start', space_after=2, line=1.15)
run(p, "تقرير اجتماع", size=24, bold=True, color=WHITE)
p = cell.add_paragraph(); rtl_par(p, align='start', space_after=6, line=1.3)
run(p, "الاجتماع التأسيسي للتعاون المشترك — توزيع الأدوار وآلية العمل",
    size=12, color="D9D9D9")
p = cell.add_paragraph(); rtl_par(p, align='start', space_after=0, line=1.2)
run(p, "الأحد  13  سبتمبر  2026", size=10.5, bold=True, color=WHITE)

para(body, "", space_after=10, size=4)

# ---- section heading helper ----
def heading(n, text):
    p = body.add_paragraph()
    rtl_par(p, align='start', space_before=14, space_after=7, line=1.2, keep_next=True)
    par_borders(p, bottom=(6, BLACK))
    run(p, f"{n}.  ", size=13.5, bold=True, color=BLACK)
    run(p, text, size=13.5, bold=True, color=BLACK)
    return p

def subheading(text):
    p = body.add_paragraph()
    rtl_par(p, align='start', space_before=9, space_after=4, line=1.25, keep_next=True)
    run(p, "▪  ", size=11.5, bold=True, color=BLACK, rtl=False)
    run(p, text, size=11.5, bold=True, color=DARK)
    return p

def bullet(text, bold_lead=None):
    p = body.add_paragraph()
    rtl_par(p, align='both', space_after=3, line=1.42)
    pPr = p._p.get_or_add_pPr()
    ind = OxmlElement('w:ind')
    ind.set(qn('w:start'), '340'); ind.set(qn('w:hanging'), '190')
    pPr.append(ind)
    run(p, "–  ", size=11, color=DARK, rtl=False)
    if bold_lead:
        run(p, bold_lead, size=11, bold=True, color=BLACK)
    run(p, text, size=11, color=DARK)
    return p

# ============================== 1. بيانات الاجتماع
heading("1", "بيانات الاجتماع")
info = [
    ("موضوع الاجتماع", "الاجتماع التأسيسي للتعاون المشترك بين المكتب السعودي والمكتب المصري"),
    ("التاريخ", "الأحد  13  سبتمبر  2026"),
    ("وقت البدء", "6:55 مساءً"),
    ("مدة الاجتماع", "43 دقيقة"),
    ("طريقة الانعقاد", "اجتماع مرئي عن بُعد"),
    ("الجهات المشاركة", "المكتب السعودي  —  المكتب المصري"),
    ("عدد الحاضرين", "ستة أعضاء"),
    ("مرجع التقرير", "التفريغ النصي الكامل للاجتماع"),
]
t = make_table(body, len(info), 2, [4.6, CONTENT_W - 4.6])
for i, (k, v) in enumerate(info):
    keep_row_together(t.rows[i])
    cell_text(t.rows[i].cells[0], k, size=10.5, bold=True, color=BLACK, fill=LIGHT)
    cell_text(t.rows[i].cells[1], v, size=10.5, color=DARK)

# ============================== 2. الهدف من الاجتماع
heading("2", "الهدف من الاجتماع")
para(body, "انعقد الاجتماع بهدف وضع حجر الأساس للتعاون المشترك بين المكتب السعودي "
           "والمكتب المصري، وتحديد الأدوار والمسؤوليات بشكل واضح لا لبس فيه، والاتفاق على "
           "آلية عمل موحّدة تنظّم التنسيق بين الفريقين وتضبط جودة المخرجات قبل تسليمها "
           "للعملاء، إضافة إلى التعارف بين أعضاء الفريق واستعراض خبراتهم وتخصصاتهم، "
           "وتحديد أولى الخطوات التنفيذية للمرحلة القادمة.",
     size=11, color=DARK, space_after=6)

# ============================== 3. المشاركون والأدوار
heading("3", "المشاركون والأدوار")
people = [
    ("د. أحمد الشيبي", "الإشراف العام على الشراكة، ومتابعة الإجراءات النظامية والورقية للشركة", "المكتب السعودي"),
    ("أ. ياسين كردي", "إدارة العمليات والتنسيق، وحلقة الوصل الرسمية بين المكتبين، ومراجعة المخرجات قبل تسليمها للعميل", "المكتب السعودي"),
    ("م. عوض صالح", "التخصص الصناعي: تحسين سلاسل التوريد وإدارة العمليات، ودراسات الجدوى والتكاليف والميزانيات والعائد على الاستثمار، واختيار المورّدين والموزّعين", "المكتب السعودي"),
    ("أ. عبد الرحمن سليمان", "الشريك المؤسس لمكتب مصر، ووضع الاستراتيجية والرؤية، وتحديد أنواع المشاريع وحجمها، والتسعير وآلية التفاوض مع العملاء", "المكتب المصري"),
    ("أ. أحمد", "المدير التنفيذي: إدارة فريق العمل بالكامل وتنفيذ المشاريع", "المكتب المصري"),
    ("أ. وجدان محمود", "تطوير الأعمال ومتابعة التعاقدات مع العملاء", "المكتب المصري"),
]
t = make_table(body, len(people) + 1, 3, [4.2, 9.0, CONTENT_W - 13.2])
hdrow = t.rows[0]
keep_row_together(hdrow); header_row_repeat(hdrow)
for i, h in enumerate(["الاسم", "الدور والمسؤولية", "الجهة"]):
    cell_text(hdrow.cells[i], h, size=10.5, bold=True, color=WHITE, fill=BLACK)
for i, (n, r, s) in enumerate(people, start=1):
    keep_row_together(t.rows[i])
    fill = LIGHT if i % 2 == 0 else None
    cell_text(t.rows[i].cells[0], n, size=10.5, bold=True, color=BLACK, fill=fill)
    cell_text(t.rows[i].cells[1], r, size=10, color=DARK, fill=fill, align='start')
    cell_text(t.rows[i].cells[2], s, size=10, color=DARK, fill=fill)

para(body, "كما أُشير إلى وجود مجلس استشاري من الأكاديميين والمهندسين يشارك الفريق في "
           "المشاريع من الجانبين الفني والدراسي.", size=10, color=DARK,
     space_before=6, space_after=0, align='start')

# ============================== 4. أبرز محاور النقاش
heading("4", "أبرز محاور النقاش")

subheading("4-1  آلية العمل وتوزيع الأدوار")
bullet("مسؤول عن التنسيق والعمليات بكافة أبعادها، وهو حلقة الوصل الرسمية بين المكتب السعودي والمكتب المصري.", bold_lead="أ. ياسين كردي: ")
bullet("يقوم أ. ياسين بدور المُراجع النهائي لكل المخرجات قبل وصولها للعميل، بما يضمن تسليم المنتج بأفضل صورة ومطابقته لاحتياج العمل.")
bullet("أشار أ. ياسين إلى أنه في طور استكمال رخصة مستشار الامتياز التشغيلي، بما يدعم خط خدمات استشارات التشغيل.")
bullet("مسؤول عن وضع الاستراتيجية والرؤية، وتحديد أنواع المشاريع وأحجامها، والتسعير وآلية التفاوض مع العملاء.", bold_lead="أ. عبد الرحمن سليمان: ")
bullet("أكد الفريق المصري أن التواصل المباشر متاح في أي وقت لتجاوز أي تأخير أو عائق في سير العمل أو الجداول الزمنية.")

subheading("4-2  الوضع الحالي لمشاريع مكتب مصر")
bullet("مشروع قائم حاليًا وصل إلى مراحله الأخيرة (مرحلة التحسينات والتعديلات النهائية).")
bullet("شراكة قيد التشكّل مع شركة هندسية مصرية متخصصة لتغطية الجانب الهندسي (مثل الكونسبت ديزاين)، مع اجتماع مقرر يوم الأربعاء لبحث آلية التعاقد.")
bullet("الفريق جاهز لاستقبال مشاريع جديدة دون تعارض في الجداول الزمنية مع الالتزامات القائمة.")

subheading("4-3  القطاعات والخدمات المستهدفة")
bullet("التوجّه نحو المشاريع التي تشمل الإدارة الكاملة للمشروع، أو تقييم جودة المشاريع، أو الجولات الاستثمارية.")
bullet("طُرح تحديد القطاعات المستهدفة (تقنية / عقارية / سلع استهلاكية سريعة الدوران) بما يتوافق مع قدرات الفريق المتاحة، ليكون البحث في السوق السعودي موجّهًا بدقة.")
bullet("القطاع العقاري يمثل أولوية عالية في السوق السعودي، والفريق يرى أهمية الظهور فيه قريبًا.")

subheading("4-4  هيكل الكيانين: استشارات الأعمال والعقارات")
bullet("تعمل الشركة من خلال واجهتين منفصلتين خارجيًا: واجهة استشارات الأعمال وواجهة العقارات، بينما هما داخليًا كيان واحد بإدارة واحدة.")

subheading("4-5  مقارنة السوق العقاري: السعودية ومصر")
bullet("تختلف الأنظمة والحوكمة المنظِّمة للتعاملات العقارية اختلافًا جوهريًا بين السوقين.")
bullet("للفريق المصري خبرة عملية ممتدة في السوقين، مع مشروعات قائمة حاليًا في السوق السعودي، منها مشروعات على الساحل الجنوبي.")
bullet("تحديات السوق المصري تتمثل في ارتفاع تكاليف الإنشاءات وعدم استقرار سعر الصرف.")
bullet("السوق السعودي أكبر حجمًا ويتيح فرصًا أوسع، خصوصًا مع اختيار التصميم المناسب للمنطقة المستهدفة.")

subheading("4-6  النطاق الجغرافي والالتزامات المتبادلة")
bullet("السوق السعودي هو السوق المستهدف الأساسي، وأي سوق آخر يُعد إضافة.")
bullet("سلّم المكتب المصري السوق السعودي بالكامل للفريق السعودي، ولن يكون له أي تواصل مباشر مع أي طرف في هذا السوق إلا من خلال أ. ياسين كردي أو د. أحمد الشيبي.")
bullet("في المقابل، أكد أ. ياسين على تفرّغ شبه كامل لكافة المشاريع المشتركة، وتنسيق على أعلى مستوى مع الفريق في عمليتي التشغيل وتسليم المشاريع للعملاء.")

subheading("4-7  التنسيق وإدارة الخلافات والتوثيق")
para(body, "وُصفت هذه النقطة في الاجتماع بأنها نقطة مفصلية في العلاقة بين الفريقين، "
           "وطُلب إبرازها بوضوح:", size=10.5, color=DARK, space_after=4, align='start')
bullet("أي خطأ أو سوء فهم أو عدم وضوح بين أعضاء الفريق قد ينعكس سلبًا على صورة الشركة أمام العملاء، خصوصًا في مرحلة الانطلاق.")
bullet("كل تنسيق يمر عبر أ. ياسين كردي، والتعامل معه بمثابة التعامل مع د. أحمد الشيبي مباشرة.")
bullet("الحاجة إلى بروتوكول واضح لإدارة الخلافات، على اعتبار أن حدوث اختلاف أو سوء فهم أمر متوقع وغير مستبعد.")
bullet("تثبيت كل ما يُتفق عليه كتابيًا (الرسائل ومجموعات العمل والبريد الإلكتروني) ليكون مرجعًا يُرجَع إليه عند أي خطأ أو التباس.")
bullet("طُرح اعتماد البريد الإلكتروني كقناة رسمية للتوثيق، على أن يُتفق على الصيغة الأنسب التي يرتاح لها الفريق.")
bullet("الهدف المعلن: بيئة عمل مريحة يعمل فيها الجميع بروح واحدة.")

subheading("4-8  البنية التشغيلية والهوية المؤسسية")
bullet("إنشاء بريد إلكتروني رسمي موحّد على نطاق الشركة، مرتبط بالخدمة السحابية (Zoho)، بما يتيح ترتيب المستندات والمشاريع وإتاحة الوصول إليها من أي مكان.")
bullet("الموقع الإلكتروني يعمل حاليًا بشكل مباشر.")
bullet("حسابات التواصل الاجتماعي: تغطية الواجهتين (الأعمال والعقارات)، ونشر تقارير قطاعية لتعزيز الظهور والمصداقية.")
bullet("تحديث الملف التعريفي للشركة (البروفايل) بإضافة العنوان الجديد وإبراز الكيان السعودي – المصري.")
bullet("توفير رقم تواصل سعودي رسمي باسم الشركة لا باسم شخص بعينه، لضمان استمرارية التواصل مع العملاء.")
bullet("استكمال الإجراءات النظامية والورقية للشركة (الغرفة التجارية وما يتبعها)، وقد بُوشر فيها فعليًا.")

subheading("4-9  كتالوج الخدمات")
bullet("إعداد قائمة تفصيلية بالخدمات، يوضَّح تحت كل خدمة البنود التي تغطيها بشكل صريح.")
bullet("الغرض: استهداف الشريحة الصحيحة من العملاء أولًا، ووضوح ما يستلمه العميل مقابل المبلغ الذي يدفعه ثانيًا.")
bullet("مثال طُرح خلال النقاش: سلاسل المطاعم في السوق السعودي كقطاع عليه طلب مرتفع، مع التحقق من مدى تغطيته ضمن الخدمات الحالية.")

subheading("4-10  الخدمات التمهيدية المجانية")
bullet("اقتراح تقديم بعض الخدمات مجانًا لمدة محددة في البداية، كوسيلة لإثبات جودة العمل وبناء الثقة مع العملاء وفتح باب التعاون الأوسع.")
bullet("أوضح المكتب المصري أن الفريق يقدّم بالفعل الاستشارة الأولى والتشخيص المبدئي مجانًا، إضافة إلى تحليل الاحتياج، بما يُشعر العميل بالقيمة المقدَّمة.")
bullet("اتُّفق على حصر الخدمات التي يمكن تقديمها مجانًا ضمن إطار واضح ومتفق عليه.")

subheading("4-11  قاعدة بيانات العملاء")
bullet("لدى المكتب المصري قاعدة بيانات للعملاء الحاليين والمحتملين، وسيتم إتاحتها للفريق.")
bullet("التوجّه إلى أتمتة القاعدة ورفع البيانات الفعلية عليها بما يدعم التواصل والمتابعة لاحقًا.")

subheading("4-12  توثيق الاجتماعات")
bullet("ضرورة توثيق محاضر الاجتماعات الداخلية والخارجية (مع العملاء) بصيغة موحّدة ومتفق عليها.")
bullet("يتوفر حاليًا ملخص ومحضر كامل لهذا الاجتماع، مع تحديد المسؤول عن تدوين الملاحظات في الاجتماعات الخارجية؛ وقد اقتُرح إسناد هذه المهمة إلى م. عوض صالح.")

# ============================== 5. القرارات
heading("5", "القرارات المتخذة")
decisions = [
    "اعتماد أ. ياسين كردي نقطة التنسيق الرسمية الوحيدة بين المكتبين، وأن يمر كل تنسيق من خلاله.",
    "تسليم السوق السعودي بالكامل للفريق السعودي، وعدم تواصل المكتب المصري مباشرة مع أي طرف في هذا السوق.",
    "التزام متبادل بتفرّغ شبه كامل للمشاريع المشتركة وتنسيق على أعلى مستوى في التشغيل والتسليم.",
    "اعتماد التوثيق الكتابي لكل ما يُتفق عليه كمرجع يُرجَع إليه عند الاختلاف.",
    "اعتبار السوق السعودي السوق المستهدف الأساسي، وما عداه إضافة.",
    "الإبقاء على واجهتين منفصلتين خارجيًا (استشارات الأعمال / العقارات) ضمن كيان واحد داخليًا.",
    "اعتماد بريد إلكتروني رسمي موحّد على نطاق الشركة وربطه بالخدمة السحابية.",
    "تخصيص رقم تواصل رسمي باسم الشركة لا باسم شخص بعينه.",
    "تقديم خدمات تمهيدية مجانية محدودة كمدخل لبناء الثقة مع العملاء.",
    "اعتماد اجتماع دوري أسبوعي في مرحلة الانطلاق.",
]
t = make_table(body, len(decisions), 2, [1.3, CONTENT_W - 1.3])
for i, d in enumerate(decisions):
    keep_row_together(t.rows[i])
    cell_text(t.rows[i].cells[0], str(i + 1), size=10.5, bold=True, color=WHITE,
              fill=BLACK, align='center')
    cell_text(t.rows[i].cells[1], d, size=10.5, color=DARK,
              fill=(LIGHT if i % 2 == 0 else None))

# ============================== 6. خطة العمل
heading("6", "خطة العمل والمهام")
tasks = [
    ("إنشاء البريد الإلكتروني الرسمي الموحّد وربطه بالخدمة السحابية", "أ. عبد الرحمن سليمان", "الخميس 17 سبتمبر 2026"),
    ("استكمال الإجراءات النظامية والورقية (الغرفة التجارية وما يتبعها)", "د. أحمد الشيبي", "قيد التنفيذ"),
    ("توفير رقم تواصل سعودي رسمي باسم الشركة", "د. أحمد الشيبي", "قبل الاجتماع القادم"),
    ("إعداد كتالوج الخدمات التفصيلي مع بنود كل خدمة", "أ. عبد الرحمن سليمان", "قبل الاجتماع القادم"),
    ("تحديد الخدمات التي يمكن تقديمها مجانًا كمرحلة تمهيدية", "أ. عبد الرحمن سليمان  /  أ. ياسين كردي", "قبل الاجتماع القادم"),
    ("إتاحة قاعدة بيانات العملاء للفريق ودراسة أتمتتها", "المكتب المصري", "قبل الاجتماع القادم"),
    ("تحديث الملف التعريفي بالعنوان الجديد والكيان السعودي – المصري", "المكتب المصري", "خلال الأيام القادمة"),
    ("تفعيل حسابات التواصل الاجتماعي للواجهتين ونشر التقارير القطاعية", "المكتب المصري", "مستمر"),
    ("اجتماع مع الشركة الهندسية المصرية لبحث آلية التعاقد", "المكتب المصري", "الأربعاء 16 سبتمبر 2026"),
    ("اعتماد نموذج موحّد لمحاضر الاجتماعات وتحديد المسؤول عن تدوينها", "أ. ياسين كردي  /  م. عوض صالح", "قبل الاجتماع القادم"),
]
t = make_table(body, len(tasks) + 1, 4, [1.0, 7.6, 4.0, CONTENT_W - 12.6])
hdrow = t.rows[0]
keep_row_together(hdrow); header_row_repeat(hdrow)
for i, h in enumerate(["م", "المهمة", "المسؤول", "الموعد المستهدف"]):
    cell_text(hdrow.cells[i], h, size=10.5, bold=True, color=WHITE, fill=BLACK,
              align=('center' if i == 0 else 'start'))
for i, (task, owner, due) in enumerate(tasks, start=1):
    keep_row_together(t.rows[i])
    fill = LIGHT if i % 2 == 0 else None
    cell_text(t.rows[i].cells[0], str(i), size=10, bold=True, color=BLACK, fill=fill, align='center')
    cell_text(t.rows[i].cells[1], task, size=10, color=DARK, fill=fill)
    cell_text(t.rows[i].cells[2], owner, size=10, color=DARK, fill=fill)
    cell_text(t.rows[i].cells[3], due, size=10, bold=True, color=BLACK, fill=fill)

# ============================== 7. الاجتماع القادم
heading("7", "الاجتماع القادم")
t = make_table(body, 4, 2, [4.6, CONTENT_W - 4.6])
nxt = [
    ("الموعد", "الأحد  20  سبتمبر  2026"),
    ("الدورية", "أسبوعيًا في مرحلة الانطلاق"),
    ("التوقيت", "يُتفق عليه قبل الموعد بيومين إلى ثلاثة أيام"),
    ("جدول الأعمال المبدئي", "استعراض ما أُنجز من مهام هذا الاجتماع، والبدء الفعلي في تنفيذ خطة العمل"),
]
for i, (k, v) in enumerate(nxt):
    keep_row_together(t.rows[i])
    cell_text(t.rows[i].cells[0], k, size=10.5, bold=True, color=BLACK, fill=LIGHT)
    cell_text(t.rows[i].cells[1], v, size=10.5, color=DARK)

# ============================== 8. ملاحظات ختامية
heading("8", "ملاحظات وتوصيات ختامية")
bullet("سادت الاجتماع روح إيجابية وتفاؤل واضح بتكامل الفريق وتنوّع تخصصاته بين الإدارة والتشغيل والتطوير والجانب الصناعي والعقاري.")
bullet("يمثّل تكامل الخبرات بين المكتبين ميزة تنافسية في السوق السعودي، شريطة انضباط التنسيق ووضوح المسؤوليات منذ المرحلة الأولى.")
bullet("يُوصى بإغلاق مهام هذا الاجتماع قبل موعد الاجتماع القادم، ليبدأ الفريق فعليًا في تنفيذ خطة العمل.")
bullet("يُوصى باعتماد قناة توثيق رسمية واحدة (البريد الإلكتروني) لكل ما يتعلق بالمستندات والاتفاقات، مع الإبقاء على مجموعات العمل للتواصل اليومي.")

para(body, "", space_before=10, space_after=0, size=4)
p = body.add_paragraph()
rtl_par(p, align='start', space_before=8, space_after=0, line=1.2)
par_borders(p, top=(4, "D6D6D6"))
run(p, "انتهى التقرير", size=9, bold=True, color=MID)

# --------------------------------------------------------------- finalize
reorder_all(doc.element)
for part in (sec.header, sec.footer):
    reorder_all(part._element)

doc.save(OUT)
print("saved:", OUT)
