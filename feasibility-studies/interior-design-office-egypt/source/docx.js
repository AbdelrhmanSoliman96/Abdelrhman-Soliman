const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 680, height: 1000 }, deviceScaleFactor: 2.5 });
  await p.goto('file://' + process.argv[2]); await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: '.cover{height:962px;width:680px} .divider{height:900px;width:680px} .divider .dn{top:560px} .divider h1{top:640px} .divider p{top:710px} .divider .bar{top:520px} .sec{break-before:auto} body{background:#fff}' });
  const sels = ['.cover', '.divider', '.prow', 'figure .fig-body', '.kpis', '.grid', '.flow', '.org', '.verdict', 'table.gantt'];
  const els = await p.$$(sels.join(','));
  let i = 0;
  for (const e of els) {
    const buf = await e.screenshot({ type: 'png' });
    const box = await e.boundingBox();
    const uri = 'data:image/png;base64,' + buf.toString('base64');
    const k = Math.min(1, 640 / box.width);
    await e.evaluate((el, a) => {
      const im = document.createElement('img'); im.src = a[0]; im.setAttribute('width', a[1]); im.setAttribute('height', a[2]);
      const pp = document.createElement('p'); pp.setAttribute('align', 'center'); pp.appendChild(im); el.replaceWith(pp);
    }, [uri, Math.round(box.width * k), Math.round(box.height * k)]);
    i++;
  }
  const html = await p.evaluate(() => {
    const drop = (n) => n.parentNode.removeChild(n);
    document.querySelectorAll('style').forEach(drop);
    document.querySelectorAll('.two').forEach(t => { [...t.children].forEach(c => { while (c.firstChild) t.parentNode.insertBefore(c.firstChild, t); }); drop(t); });
    document.querySelectorAll('.callout').forEach(c => {
      const t = document.createElement('table'); t.setAttribute('width', '100%'); t.setAttribute('cellpadding', '8'); t.setAttribute('dir', 'rtl');
      const td = t.insertRow().insertCell(); td.setAttribute('bgcolor', '#F4F7FA');
      const ct = c.querySelector('.ct');
      td.innerHTML = '<p><b>' + (ct ? ct.textContent : '') + '</b></p><p>' + c.lastElementChild.innerHTML + '</p>'; c.replaceWith(t);
    });
    document.querySelectorAll('.tbl table').forEach(t => { t.setAttribute('border', '1'); t.setAttribute('cellpadding', '5'); t.setAttribute('cellspacing', '0'); t.setAttribute('width', '100%'); t.setAttribute('dir', 'rtl'); });
    document.querySelectorAll('th').forEach(t => { t.setAttribute('bgcolor', '#12304A'); t.innerHTML = '<font color="#FFFFFF"><b>' + t.innerHTML + '</b></font>'; });
    document.querySelectorAll('tr.tot td, tr.sub td').forEach(t => { t.setAttribute('bgcolor', '#EAF0F5'); t.innerHTML = '<b>' + t.innerHTML + '</b>'; });
    document.querySelectorAll('.pill').forEach(s => { s.outerHTML = '<b>' + s.textContent + '</b>'; });
    document.querySelectorAll('.sec-head').forEach(h => { const n = h.querySelector('.sec-num').textContent; const t = h.querySelector('h1').textContent; h.outerHTML = '<h1 style="page-break-before:always">' + n + ' | ' + t + '</h1>'; });
    document.querySelectorAll('.toc td.pg').forEach(drop);
    document.querySelectorAll('.toc a').forEach(a => a.replaceWith(a.textContent));
    document.querySelectorAll('.front h1').forEach(h => { h.setAttribute('style', 'page-break-before:always'); });
    document.querySelectorAll('.src, .fnote').forEach(s => { s.outerHTML = '<p class="src"><font size="1" color="#6B7580">' + s.innerHTML + '</font></p>'; });
    document.querySelectorAll('figcaption, .tcap').forEach(s => { s.outerHTML = '<p class="cap"><font color="#12304A"><b>' + s.textContent + '</b></font></p>'; });
    return document.body.innerHTML;
  });
  const css = `@page{size:21cm 29.7cm;margin:2cm 1.8cm} body{font-family:'Segoe UI','Arial';font-size:10.5pt;line-height:150%;text-align:justify}
  h1{font-size:20pt;color:#12304A;text-align:right} h2{font-size:14pt;color:#12304A;text-align:right;margin-top:14pt} h3{font-size:11.5pt;color:#1E4566;text-align:right}
  p{margin:0 0 7pt 0} td,th{font-size:9pt;text-align:right;vertical-align:top} table{border-collapse:collapse} p.lead{font-size:11.5pt;color:#33414E} p.cap{text-align:right;margin-top:10pt}`;
  fs.writeFileSync(process.argv[3], '<!doctype html><html dir="rtl" lang="ar"><head><meta charset="utf-8"><style>' + css + '</style></head><body dir="rtl">' + html + '</body></html>');
  console.log('shots', i); await b.close();
})();
