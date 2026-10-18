const { chromium } = require('playwright');
(async () => {
  const specs = [
    { id:'a',  name:'StartPad_Facebook_Cover_Lockup' },
    { id:'b',  name:'StartPad_Facebook_Cover_Mark' },
    { id:'ar', name:'StartPad_Facebook_Cover_Arabic' },
  ];
  const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const s of specs) for (const scale of [1,2]) {
    const ctx = await browser.newContext({ deviceScaleFactor:scale, viewport:{width:820,height:312} });
    const page = await ctx.newPage();
    await page.goto('file://' + __dirname + '/facebook.html');
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    const dims = scale===2 ? '1640x624' : '820x312';
    await page.locator('#'+s.id).screenshot({ path:`${__dirname}/${s.name}_${dims}.png` });
    await ctx.close();
  }
  await browser.close(); console.log('done');
})();
