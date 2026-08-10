import { chromium } from 'playwright';
import fs from 'fs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport:{width:1500,height:1000}, colorScheme:'light', deviceScaleFactor:2.6 });
const p = await ctx.newPage();
await p.goto('file:///tmp/render.html', { waitUntil:'networkidle' });
await p.addStyleTag({ content: `html{scroll-behavior:auto!important}
  .rail{display:none!important} .layout{grid-template-columns:1fr!important}
  main{max-width:1240px!important} .frame{box-shadow:none!important; overflow:visible!important}
  .chart{min-width:0!important}` });
await p.waitForTimeout(600);
const ex = await p.$$('.exhibit');
const meta = [];
for (let i=0;i<ex.length;i++){
  const frame = await ex[i].$('.frame');
  if(!frame){ meta.push(null); continue; }
  const tag = await ex[i].$eval('.ex-tag', e=>e.textContent.trim()).catch(()=>'');
  const title = await ex[i].$eval('.ex-title', e=>e.textContent.trim()).catch(()=>'');
  const cap = await ex[i].$eval('figcaption', e=>e.textContent.replace(/\s+/g,' ').trim()).catch(()=>'');
  await frame.scrollIntoViewIfNeeded(); await p.waitForTimeout(80);
  const box = await frame.boundingBox();
  const file = `figs/fig-${String(i).padStart(2,'0')}.png`;
  await frame.screenshot({ path: file });
  meta.push({ i, file, tag, title, cap, w: Math.round(box.width), h: Math.round(box.height) });
}
fs.writeFileSync('figs/figs.json', JSON.stringify(meta.filter(Boolean), null, 1));
console.log('rasterized', meta.filter(Boolean).length);
for (const m of meta.filter(Boolean)) console.log(' ', m.file, m.tag, `${m.w}x${m.h}`);
await b.close();
