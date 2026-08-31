const { chromium } = require('playwright');
(async () => {
  const specs = [
    { id:'a', w:1128, h:191, name:'StartPad_LinkedIn_CompanyCover_1128x191' },
    { id:'b', w:1128, h:191, name:'StartPad_LinkedIn_CompanyCover_Wordmark_1128x191' },
    { id:'c', w:1584, h:396, name:'StartPad_LinkedIn_ProfileCover_1584x396' },
  ];
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const s of specs) {
    for (const scale of [1, 2]) {
      const ctx = await browser.newContext({ deviceScaleFactor: scale, viewport:{ width:s.w, height:s.h } });
      const page = await ctx.newPage();
      await page.goto('file://' + __dirname + '/cover.html');
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(400);
      await page.locator('#' + s.id).screenshot({ path:`${__dirname}/${s.name}${scale===2?'@2x':''}.png` });
      await ctx.close();
    }
  }
  await browser.close();
  console.log('done');
})();
