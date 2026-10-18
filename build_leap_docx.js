const fs = require('fs');
const d = require('docx');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, HeadingLevel, BorderStyle, ShadingType, Footer, PageNumber,
  TableOfContents, PageBreak, convertInchesToTwip,
} = d;

const AR = /[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]/;
const FONT_AR = 'Arial';
const INK = '15171C', SOFT = '4A4F5A', FAINT = '6E7480';
const ACCENT = '0F5C4A', RULE = 'D8D5CC', SURF = 'F5F4F0';
const CW = 9360; // content width in DXA (A4 minus 1" margins ≈ 6.5")

const isRTL = (s) => {
  const m = s.replace(/[^\p{L}]/gu, '').match(/\p{L}/u);
  return m ? AR.test(m[0]) : true;
};

// ---- inline markdown -> runs ----
function runs(text, opts = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*)|(`[^`]+`)|(\*[^*\n]+\*)|(\[[^\]]+\]\([^)]+\))/g;
  let last = 0, m;
  const push = (t, o = {}) => {
    if (!t) return;
    out.push(new TextRun({
      text: t, font: o.mono ? 'Consolas' : FONT_AR,
      size: opts.size || 20, bold: !!o.bold, italics: !!o.italic,
      color: o.color || opts.color || INK,
      rightToLeft: AR.test(t),
    }));
  };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index));
    if (m[1]) push(m[1].slice(2, -2), { bold: true });
    else if (m[2]) push(m[2].slice(1, -1), { mono: true, color: ACCENT });
    else if (m[3]) push(m[3].slice(1, -1), { italic: true, color: SOFT });
    else if (m[4]) {
      const mm = m[4].match(/\[([^\]]+)\]\(([^)]+)\)/);
      push(mm[1], { color: ACCENT });
    }
    last = re.lastIndex;
  }
  push(text.slice(last));
  return out.length ? out : [new TextRun({ text: '', font: FONT_AR, size: opts.size || 20 })];
}

const para = (text, o = {}) => {
  const rtl = o.forceLTR ? false : isRTL(text);
  return new Paragraph({
    children: runs(text, o),
    bidirectional: rtl,
    alignment: o.align || (rtl ? AlignmentType.JUSTIFIED : AlignmentType.LEFT),
    spacing: { before: o.before ?? 80, after: o.after ?? 120, line: 300 },
    indent: o.indent,
    ...(o.heading ? { heading: o.heading } : {}),
    ...(o.bullet ? { bullet: { level: 0 } } : {}),
    ...(o.numbered ? { numbering: { reference: 'nums', level: 0 } } : {}),
    ...(o.border ? {
      border: {
        [rtl ? 'right' : 'left']: { style: BorderStyle.SINGLE, size: 18, color: '8A6A28', space: 8 },
      },
      shading: { type: ShadingType.CLEAR, color: 'auto', fill: SURF },
    } : {}),
    ...(o.pageBreakBefore ? { pageBreakBefore: true } : {}),
  });
};

const heading = (text, lvl) => {
  const sizes = { 1: 40, 2: 30, 3: 24, 4: 21 };
  const rtl = isRTL(text);
  return new Paragraph({
    children: [new TextRun({
      text: text.replace(/\*\*/g, ''), font: FONT_AR, size: sizes[lvl] || 22,
      bold: true, color: lvl <= 2 ? ACCENT : (lvl === 3 ? ACCENT : SOFT),
      rightToLeft: AR.test(text),
    })],
    heading: [null, HeadingLevel.HEADING_1, HeadingLevel.HEADING_2,
      HeadingLevel.HEADING_3, HeadingLevel.HEADING_4][lvl],
    bidirectional: rtl,
    alignment: rtl ? AlignmentType.RIGHT : AlignmentType.LEFT,
    spacing: { before: lvl <= 2 ? 360 : 240, after: lvl <= 2 ? 160 : 100 },
    outlineLevel: lvl - 1,
    ...(lvl === 2 ? {
      pageBreakBefore: true,
      border: { top: { style: BorderStyle.SINGLE, size: 12, color: INK, space: 8 } },
    } : {}),
  });
};

const cell = (text, o = {}) => new TableCell({
  width: { size: o.w, type: WidthType.DXA },
  shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
  margins: { top: 70, bottom: 70, left: 100, right: 100 },
  children: [new Paragraph({
    children: runs(text, { size: o.head ? 16 : 18, color: o.head ? FAINT : INK }),
    bidirectional: isRTL(text),
    alignment: isRTL(text) ? AlignmentType.RIGHT : AlignmentType.LEFT,
    spacing: { before: 0, after: 0, line: 260 },
  })],
});

function table(head, rows) {
  const n = head.length;
  // size columns by content, with a floor so short index columns stay legible
  const MIN = Math.max(620, Math.floor(CW / (n * 3)));
  const weight = head.map((h, i) => {
    const lens = [h, ...rows.map((r) => r[i] ?? '')].map((s) => s.replace(/\*\*|`/g, '').length);
    const avg = lens.reduce((a, b) => a + b, 0) / lens.length;
    const max = Math.max(...lens);
    return Math.max(1, avg * 0.75 + max * 0.25);
  });
  const total = weight.reduce((a, b) => a + b, 0);
  let widths = weight.map((w) => Math.max(MIN, Math.round((w / total) * CW)));
  // renormalise to exactly CW, taking the slack off the widest column
  let diff = CW - widths.reduce((a, b) => a + b, 0);
  while (diff !== 0) {
    const idx = diff < 0
      ? widths.indexOf(Math.max(...widths))
      : widths.indexOf(Math.min(...widths.filter((w) => w > MIN)) || Math.max(...widths));
    const step = diff < 0 ? -Math.min(-diff, widths[idx] - MIN) : diff;
    if (step === 0) { widths[widths.indexOf(Math.max(...widths))] += diff; break; }
    widths[idx] += step;
    diff = CW - widths.reduce((a, b) => a + b, 0);
  }
  const border = { style: BorderStyle.SINGLE, size: 4, color: RULE };
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: widths,
    visuallyRightToLeft: true,
    borders: { top: border, bottom: border, left: border, right: border,
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: 'EAE7E0' },
      insideVertical: { style: BorderStyle.SINGLE, size: 2, color: 'EAE7E0' } },
    rows: [
      new TableRow({
        tableHeader: true,
        children: head.map((c, i) => cell(c, { w: widths[i], fill: SURF, head: true })),
      }),
      ...rows.map((r) => new TableRow({
        children: head.map((_, i) => cell(r[i] ?? '', { w: widths[i] })),
      })),
    ],
  });
}

// ---- parse markdown ----
const md = fs.readFileSync(process.argv[2], 'utf8').split('\n');
const body = [];
let i = 0;
const cells = (r) => r.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());

while (i < md.length) {
  const ln = md[i];

  if (/^\|/.test(ln) && i + 1 < md.length && /^\|[\s:|-]+\|$/.test(md[i + 1].trim())) {
    const head = cells(ln); i += 2;
    const rows = [];
    while (i < md.length && /^\|/.test(md[i])) { rows.push(cells(md[i])); i++; }
    body.push(table(head, rows));
    body.push(new Paragraph({ text: '', spacing: { after: 120 } }));
    continue;
  }
  if (/^#{1,4}\s/.test(ln)) {
    const lvl = ln.match(/^#+/)[0].length;
    body.push(heading(ln.replace(/^#+\s*/, ''), lvl)); i++; continue;
  }
  if (/^(---|\*\*\*|___)\s*$/.test(ln)) { i++; continue; }
  if (/^>\s/.test(ln)) {
    const buf = [];
    while (i < md.length && /^>\s/.test(md[i])) { buf.push(md[i].replace(/^>\s/, '')); i++; }
    body.push(para(buf.join(' '), { border: true, before: 140, after: 140 }));
    continue;
  }
  if (/^\s*([-*]|\d+\.)\s+/.test(ln)) {
    const ordered = /^\s*\d+\.\s/.test(ln);
    while (i < md.length && /^\s*([-*]|\d+\.)\s+/.test(md[i])) {
      const t = md[i].replace(/^\s*([-*]|\d+\.)\s+/, '');
      body.push(para(t, ordered ? { numbered: true, after: 60 } : { bullet: true, after: 60 }));
      i++;
    }
    continue;
  }
  if (ln.trim()) {
    const buf = [];
    while (i < md.length && md[i].trim() && !/^(#|\||>|\s*([-*]|\d+\.)\s)/.test(md[i])
           && !/^(---|\*\*\*|___)\s*$/.test(md[i].trim())) { buf.push(md[i].trim()); i++; }
    if (buf.length) { body.push(para(buf.join(' '))); continue; }
  }
  i++;
}

// ---- assemble ----
const footer = new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 6 } },
    children: [
      new TextRun({ text: 'LEAP CONSULTING  ·  INTERNAL — INVESTMENT & FUNDRAISING FEE METHODOLOGY        ',
        font: FONT_AR, size: 14, color: FAINT }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT_AR, size: 14, color: FAINT }),
      new TextRun({ text: ' / ', font: FONT_AR, size: 14, color: FAINT }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT_AR, size: 14, color: FAINT }),
    ],
  })],
});

const doc = new Document({
  creator: 'LEAP Consulting',
  title: 'آلية التسعير وتقدير المدد — خدمات الاستثمار وجمع التمويل',
  description: 'Fee & Duration Methodology — Investment & Fundraising Advisory',
  numbering: {
    config: [{
      reference: 'nums',
      levels: [{ level: 0, format: 'decimal', text: '%1.', alignment: AlignmentType.START,
        style: { paragraph: { indent: { start: 360, hanging: 260 } } } }],
    }],
  },
  styles: { default: { document: { run: { font: FONT_AR, size: 20 } } } },
  sections: [{
    properties: {
      page: { margin: { top: convertInchesToTwip(1), bottom: convertInchesToTwip(1),
        left: convertInchesToTwip(0.9), right: convertInchesToTwip(0.9) } },
    },
    footers: { default: footer },
    children: [
      new Paragraph({
        children: [new TextRun({ text: 'المحتويات', font: FONT_AR, size: 28, bold: true, color: ACCENT, rightToLeft: true })],
        bidirectional: true, alignment: AlignmentType.RIGHT, spacing: { after: 200 },
      }),
      new TableOfContents('جدول المحتويات', { hyperlink: true, headingStyleRange: '1-3' }),
      new Paragraph({ children: [new PageBreak()] }),
      ...body,
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(process.argv[3], buf);
  console.log('docx written:', process.argv[3], buf.length, 'bytes');
});
