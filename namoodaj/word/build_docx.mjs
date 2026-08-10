// يبني نسخة Word من البنية الوسيطة doc.json مع دعم كامل للاتجاه من اليمين لليسار
import fs from 'fs';
import {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, HeadingLevel, BorderStyle, ShadingType, PageBreak,
  Header, Footer, PageNumber, VerticalAlign, TableLayoutType, convertMillimetersToTwip,
} from 'docx';

const D = JSON.parse(fs.readFileSync('doc.json', 'utf8'));

// ── الهوية البصرية ──
const INK = '111A15', INK2 = '48534C', MUTED = '77817A';
const ACCENT = '0E5A49', BRASS = '8A6A12';
const RULE = 'DBE2DB', SURF2 = 'EAEEE9', ACCSOFT = 'E4EEE9', BRASSSOFT = 'F4EEDC';
const GOOD = '006300', CRIT = 'A52626';
const FONT = { ascii: 'Arial', cs: 'Arial', hAnsi: 'Arial' };

// A4 بهوامش 18مم جانبية
const MARGIN = convertMillimetersToTwip(18);
const PAGE_W = 11906;
const CONTENT = PAGE_W - MARGIN * 2;          // بالـ DXA
const IMG_W = 655;                             // بكسل عند 96 نقطة/بوصة ≈ عرض المحتوى

const hair = (color = RULE, size = 4) => ({ style: BorderStyle.SINGLE, size, color });
const noBorder = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

function tr(text, o = {}) {
  return new TextRun({
    text, font: FONT, rightToLeft: true,
    size: o.size ?? 20, sizeComplexScript: o.size ?? 20,
    bold: !!o.b, boldComplexScript: !!o.b,
    italics: !!o.i, italicsComplexScript: !!o.i,
    color: o.color ?? INK2, break: o.break,
  });
}

function runsToRuns(runs, o = {}) {
  if (!runs || !runs.length) return [tr('', o)];
  return runs.map(r => tr(r.text, { ...o, b: o.b || r.b, i: o.i || r.i }));
}

function para(children, o = {}) {
  return new Paragraph({
    children,
    bidirectional: true,
    alignment: o.align ?? AlignmentType.BOTH,
    spacing: { before: o.before ?? 0, after: o.after ?? 120, line: o.line ?? 300 },
    indent: o.indent,
    border: o.border,
    keepNext: o.keepNext,
    heading: o.heading,
    outlineLevel: o.outlineLevel,
    pageBreakBefore: o.pageBreakBefore,
  });
}

// ══════════ الجداول ══════════
function colWidths(t) {
  const n = t.ncol;
  const len = new Array(n).fill(0), cnt = new Array(n).fill(0);
  const scan = cells => {
    let c = 0;
    for (const cell of cells) {
      const txt = (cell.runs || []).map(r => r.text).join('');
      if (cell.span === 1 && c < n) { len[c] += txt.length; cnt[c]++; }
      c += cell.span;
    }
  };
  t.head.forEach(scan);
  t.rows.forEach(r => scan(r.cells));
  const avg = len.map((L, i) => Math.max(3, cnt[i] ? L / cnt[i] : 8));
  // الجذر التربيعي يخفّف تطرّف الأعمدة الطويلة جدًا
  let w = avg.map(a => Math.sqrt(a));
  const lo = 0.055, hi = 0.42;
  let sum = w.reduce((a, b) => a + b, 0);
  w = w.map(x => Math.min(hi, Math.max(lo, x / sum)));
  sum = w.reduce((a, b) => a + b, 0);
  w = w.map(x => x / sum);
  const dxa = w.map(x => Math.round(x * CONTENT));
  dxa[n - 1] += CONTENT - dxa.reduce((a, b) => a + b, 0);   // ضبط الفرق
  return dxa;
}

function cellPara(cell, o = {}) {
  const color = cell.pos ? GOOD : cell.neg ? CRIT : (o.color ?? INK2);
  return new Paragraph({
    children: runsToRuns(cell.runs, { size: o.size ?? 17, b: o.b || cell.th, color }),
    bidirectional: true,
    alignment: cell.num ? AlignmentType.END : AlignmentType.START,
    spacing: { before: 20, after: 20, line: 250 },
  });
}

function buildTable(t) {
  const widths = colWidths(t);
  const rows = [];

  for (const h of t.head) {
    let c = 0;
    rows.push(new TableRow({
      tableHeader: true,
      children: h.map(cell => {
        const w = widths.slice(c, c + cell.span).reduce((a, b) => a + b, 0); c += cell.span;
        return new TableCell({
          width: { size: w, type: WidthType.DXA },
          columnSpan: cell.span > 1 ? cell.span : undefined,
          shading: { type: ShadingType.CLEAR, fill: SURF2, color: 'auto' },
          margins: { top: 60, bottom: 60, left: 90, right: 90 },
          verticalAlign: VerticalAlign.CENTER,
          borders: { top: hair(), bottom: hair('C4CEC6', 8), left: hair(), right: hair() },
          children: [cellPara(cell, { b: true, color: INK, size: 16 })],
        });
      }),
    }));
  }

  for (const r of t.rows) {
    const fill = r.cls === 'total' ? ACCSOFT : r.cls === 'sub' ? BRASSSOFT : null;
    let c = 0;
    rows.push(new TableRow({
      children: r.cells.map(cell => {
        const w = widths.slice(c, c + cell.span).reduce((a, b) => a + b, 0); c += cell.span;
        return new TableCell({
          width: { size: w, type: WidthType.DXA },
          columnSpan: cell.span > 1 ? cell.span : undefined,
          shading: fill ? { type: ShadingType.CLEAR, fill, color: 'auto' } : undefined,
          margins: { top: 50, bottom: 50, left: 90, right: 90 },
          borders: { top: hair(), bottom: hair(), left: hair(), right: hair() },
          children: [cellPara(cell, { b: r.cls === 'total', color: r.cls ? INK : INK2 })],
        });
      }),
    }));
  }

  const out = [];
  if (t.caption) {
    out.push(para([tr(t.caption, { size: 16, color: BRASS, b: true })],
      { align: AlignmentType.START, after: 60, before: 160, keepNext: true }));
  }
  out.push(new Table({
    rows, columnWidths: widths, visuallyRightToLeft: true,
    width: { size: CONTENT, type: WidthType.DXA },
    layout: TableLayoutType.FIXED,
  }));
  out.push(para([tr('', { size: 8 })], { after: 140 }));
  return out;
}

// ══════════ الصناديق ══════════
function buildBox(b) {
  const tone = { note: ACCENT, warn: BRASS, crit: CRIT, disclaimer: MUTED }[b.kind] || ACCENT;
  const fill = b.kind === 'disclaimer' ? SURF2 : 'FBFCFA';
  const inner = [];
  if (b.title) {
    inner.push(new Paragraph({
      children: [tr(b.title, { b: true, size: 19, color: tone })],
      bidirectional: true, alignment: AlignmentType.START,
      spacing: { before: 40, after: 80, line: 280 },
    }));
  }
  for (const sb of b.blocks) {
    if (sb.t === 'p') {
      inner.push(new Paragraph({
        children: runsToRuns(sb.runs, { size: 18 }),
        bidirectional: true, alignment: AlignmentType.BOTH,
        spacing: { after: 80, line: 290 },
      }));
    } else if (sb.t === 'list') {
      for (const it of sb.items) {
        inner.push(new Paragraph({
          children: [tr('–  ', { color: tone, b: true, size: 18 }), ...runsToRuns(it, { size: 18 })],
          bidirectional: true, alignment: AlignmentType.BOTH,
          indent: { start: 200 }, spacing: { after: 50, line: 285 },
        }));
      }
    }
  }
  if (!inner.length) inner.push(para([tr('')]));
  return [
    new Table({
      columnWidths: [CONTENT], visuallyRightToLeft: true,
      width: { size: CONTENT, type: WidthType.DXA }, layout: TableLayoutType.FIXED,
      rows: [new TableRow({
        children: [new TableCell({
          width: { size: CONTENT, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
          margins: { top: 120, bottom: 120, left: 160, right: 160 },
          borders: {
            top: hair(RULE), bottom: hair(RULE), left: hair(RULE),
            right: { style: BorderStyle.SINGLE, size: 22, color: tone },  // الحافة الملوّنة يمينًا
          },
          children: inner,
        })],
      })],
    }),
    para([tr('', { size: 8 })], { after: 160 }),
  ];
}

// ══════════ الأشكال ══════════
function buildFig(b) {
  const h = Math.round(IMG_W * (b.h / b.w));
  const out = [];
  out.push(para([
    tr(b.tag + '  ', { b: true, size: 16, color: BRASS }),
    tr(b.title, { b: true, size: 18, color: INK }),
  ], { align: AlignmentType.START, before: 200, after: 100, keepNext: true }));
  out.push(new Paragraph({
    children: [new ImageRun({
      type: 'png', data: fs.readFileSync(b.file),
      transformation: { width: IMG_W, height: h },
    })],
    alignment: AlignmentType.CENTER, bidirectional: true,
    spacing: { after: 80 }, keepNext: true,
  }));
  if (b.cap) {
    out.push(para([tr(b.cap, { size: 16, color: MUTED })],
      { align: AlignmentType.BOTH, after: 200 }));
  }
  return out;
}

// ══════════ البطاقات والمؤشرات و SWOT ══════════
function gridTable(cells, cols, render) {
  const w = Math.floor(CONTENT / cols);
  const widths = new Array(cols).fill(w);
  widths[cols - 1] += CONTENT - w * cols;
  const rows = [];
  for (let i = 0; i < cells.length; i += cols) {
    const chunk = cells.slice(i, i + cols);
    while (chunk.length < cols) chunk.push(null);
    rows.push(new TableRow({
      children: chunk.map((c, j) => new TableCell({
        width: { size: widths[j], type: WidthType.DXA },
        margins: { top: 110, bottom: 110, left: 130, right: 130 },
        borders: { top: hair(), bottom: hair(), left: hair(), right: hair() },
        shading: c && c.hl ? { type: ShadingType.CLEAR, fill: ACCSOFT, color: 'auto' } : undefined,
        children: c ? render(c) : [para([tr('')])],
      })),
    }));
  }
  return [
    new Table({ rows, columnWidths: widths, visuallyRightToLeft: true,
      width: { size: CONTENT, type: WidthType.DXA }, layout: TableLayoutType.FIXED }),
    para([tr('', { size: 8 })], { after: 160 }),
  ];
}

const P = (children, o = {}) => new Paragraph({
  children, bidirectional: true, alignment: o.align ?? AlignmentType.START,
  spacing: { after: o.after ?? 60, line: o.line ?? 270 },
});

function buildCards(b) {
  return gridTable(b.items, b.items.length >= 3 ? 3 : 2, c => [
    P([tr(c.num, { size: 15, color: BRASS, b: true })]),
    P([tr(c.title, { size: 18, color: ACCENT, b: true })]),
    P(runsToRuns(c.runs, { size: 16 }), { align: AlignmentType.BOTH, after: 0 }),
  ]);
}

function buildTiles(b) {
  return gridTable(b.items, 3, c => [
    P([tr(c.k, { size: 15, color: MUTED })]),
    P([tr(c.v, { size: 26, color: ACCENT, b: true })]),
    P([tr(c.d, { size: 15, color: MUTED })], { after: 0 }),
  ]);
}

function buildSwot(b) {
  const out = [];
  out.push(para([
    tr(b.tag + '  ', { b: true, size: 16, color: BRASS }),
    tr(b.title, { b: true, size: 18, color: INK }),
  ], { align: AlignmentType.START, before: 200, after: 100, keepNext: true }));
  out.push(...gridTable(b.quads, 2, q => [
    P([tr(q.title, { size: 18, color: ACCENT, b: true })]),
    ...q.items.map(it => P([tr('•  ', { color: BRASS }), tr(it, { size: 16 })],
      { align: AlignmentType.BOTH, after: 40 })),
  ]));
  return out;
}

// ══════════ الكتل العامة ══════════
function buildBlock(b) {
  switch (b.t) {
    case 'p':
      return [para(runsToRuns(b.runs, { size: b.lead ? 21 : 20, color: b.lead ? INK : INK2 }),
        { after: 140 })];
    case 'h2':
      return [para([tr(b.text, { b: true, size: 24, color: ACCENT })],
        { align: AlignmentType.START, before: 300, after: 120, keepNext: true,
          heading: HeadingLevel.HEADING_2, outlineLevel: 1 })];
    case 'h3':
      return [para([tr(b.text, { b: true, size: 20, color: BRASS })],
        { align: AlignmentType.START, before: 220, after: 90, keepNext: true,
          heading: HeadingLevel.HEADING_3, outlineLevel: 2 })];
    case 'list': {
      const out = [];
      b.items.forEach((it, i) => {
        const mark = b.ordered ? `${i + 1}.  ` : '•  ';
        out.push(para([tr(mark, { color: BRASS, b: true }), ...runsToRuns(it)],
          { indent: { start: 280 }, after: 70 }));
      });
      out.push(para([tr('', { size: 6 })], { after: 60 }));
      return out;
    }
    case 'table': return buildTable(b);
    case 'fig': return buildFig(b);
    case 'box': return buildBox(b);
    case 'cards': return buildCards(b);
    case 'tiles': return buildTiles(b);
    case 'swot': return buildSwot(b);
    default: return [];
  }
}

// ══════════ الغلاف والفهرس ══════════
const cover = [];
cover.push(para([tr(D.cover.eyebrow, { size: 17, color: BRASS, b: true })],
  { align: AlignmentType.START, before: 1400, after: 300 }));
cover.push(para([tr(D.cover.title, { size: 52, color: INK, b: true })],
  { align: AlignmentType.START, after: 200, line: 620 }));
cover.push(new Paragraph({
  children: [tr('', { size: 4 })], bidirectional: true,
  border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: BRASS } },
  spacing: { after: 320 }, indent: { start: 0, end: CONTENT - 1600 },
}));
cover.push(para([tr(D.cover.lede, { size: 22, color: INK2 })], { after: 500, line: 400 }));
cover.push(...gridTable(D.cover.meta, 3, m => [
  P([tr(m.k, { size: 15, color: MUTED })]),
  P([tr(m.v, { size: 19, color: INK, b: true })], { after: 0 }),
]));
cover.push(para([new PageBreak()]));

const toc = [];
toc.push(para([tr('محتويات الدراسة', { size: 32, color: ACCENT, b: true })],
  { align: AlignmentType.START, after: 300, heading: HeadingLevel.HEADING_1, outlineLevel: 0 }));
for (const t of D.toc) {
  toc.push(para([
    tr(t.n + '   ', { size: 18, color: BRASS, b: true }),
    tr(t.t, { size: 20, color: INK }),
  ], { align: AlignmentType.START, after: 110 }));
}
toc.push(para([new PageBreak()]));

// ══════════ الأقسام ══════════
const body = [];
D.sections.forEach((s, i) => {
  body.push(para([
    tr(s.num + '   ', { size: 30, color: BRASS, b: true }),
    tr(s.title, { size: 30, color: ACCENT, b: true }),
  ], { align: AlignmentType.START, before: 0, after: 60, keepNext: true,
       heading: HeadingLevel.HEADING_1, outlineLevel: 0, pageBreakBefore: i > 0 }));
  if (s.kicker) {
    body.push(new Paragraph({
      children: [tr(s.kicker, { size: 17, color: MUTED })],
      bidirectional: true, alignment: AlignmentType.START,
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE } },
      spacing: { after: 260 },
    }));
  }
  for (const b of s.blocks) body.push(...buildBlock(b));
});

for (const f of D.footer) {
  body.push(para([tr(f, { size: 15, color: MUTED })], { before: 200, after: 80 }));
}

// ══════════ المستند ══════════
const doc = new Document({
  creator: 'دراسة جدوى — مركز التمكين الاقتصادي للأسر المنتجة',
  title: D.cover.title,
  description: 'دراسة جدوى متكاملة مُعدّة للتقديم على الجهات المانحة',
  styles: {
    default: {
      document: {
        run: { font: FONT, size: 20, color: INK2 },
        paragraph: { spacing: { line: 300 } },
      },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_W, height: 16838 },
        margin: { top: convertMillimetersToTwip(20), bottom: convertMillimetersToTwip(20),
                  left: MARGIN, right: MARGIN },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [tr('دراسة جدوى — مركز التمكين الاقتصادي للأسر المنتجة', { size: 15, color: MUTED })],
          bidirectional: true, alignment: AlignmentType.START,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE } },
          spacing: { after: 120 },
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          children: [
            new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: MUTED, rightToLeft: true }),
            tr(' من ', { size: 16, color: MUTED }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: MUTED, rightToLeft: true }),
          ],
          bidirectional: true, alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: RULE } },
          spacing: { before: 120 },
        })],
      }),
    },
    children: [...cover, ...toc, ...body],
  }],
});

const out = new URL('../../dirasat-jadwa-markaz-tamkeen.docx', import.meta.url).pathname;
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(out, buf);
  console.log('كُتب:', out, (buf.length / 1024 / 1024).toFixed(2), 'ميغابايت');
});
