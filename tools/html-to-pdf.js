// Render a print-mode HTML file to A4 PDF via headless Chromium.
//   cd <repo root>   (node must resolve ./node_modules)
//   PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install playwright
//   node tools/html-to-pdf.js /abs/path/in.html out.pdf "Footer text"
const { chromium } = require('playwright');

const [, , inHtml, outPdf, footerText] = process.argv;

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  });
  const p = await b.newPage();
  await p.goto('file://' + inHtml, { waitUntil: 'networkidle' });
  await p.emulateMedia({ media: 'print', colorScheme: 'light' });
  const foot = `<div style="width:100%;font-family:'DejaVu Sans',sans-serif;font-size:7pt;
    color:#8A8F98;padding:0 16mm;display:flex;justify-content:space-between;">
    <span>${footerText || ''}</span>
    <span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
  await p.pdf({
    path: outPdf,
    format: 'A4',
    printBackground: true,
    margin: { top: '20mm', bottom: '18mm', left: '16mm', right: '16mm' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: foot,
  });
  await b.close();
  console.log('pdf written:', outPdf);
})();
