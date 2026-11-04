const {chromium}=require('playwright');
const FONTS='<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;600&family=Playfair+Display:ital@1&family=Cairo:wght@500;600&display=swap" rel="stylesheet">';
const page=(w,h,pl,pr,hs,ss,ws,ar)=>`<!doctype html><meta charset=utf-8>${FONTS}<style>
*{margin:0;box-sizing:border-box}
body{width:${w}px;height:${h}px;background:#0F3330;position:relative;overflow:hidden;font-family:Montserrat,sans-serif;color:#F6F8F8}
.rule{position:absolute;left:0;right:0;height:1px;background:#3E6B66;opacity:.6}
.wrap{position:absolute;left:${pl}px;right:${pr}px;top:0;bottom:0;display:flex;align-items:center;justify-content:space-between}
.l{display:flex;flex-direction:column;gap:${hs*0.28}px}
.word{font-weight:600;letter-spacing:.6em;font-size:${ws}px;color:#8CC2BB}
h1{font-family:'Playfair Display',serif;font-style:italic;font-weight:400;font-size:${hs}px;line-height:1.1}
p{font-weight:300;font-size:${ss}px;letter-spacing:.04em;color:#D7DCDB}
.r{text-align:right;font-family:Montserrat,sans-serif;font-weight:500;font-size:${ar*0.8}px;color:#8CC2BB;line-height:1.35;border-right:2px solid #8CC2BB;padding-right:${ar*0.5}px;letter-spacing:.02em}
.r small{display:block;font-weight:500;font-size:${ar*0.45}px;color:#D7DCDB;margin-top:6px}
</style><body><div class=rule style="top:${h*0.12}px"></div><div class=rule style="bottom:${h*0.12}px"></div>
<div class=wrap><div class=l><div class=word>A N G E L S T A</div><h1>One record for every round.</h1><p>System of record for founders and the investors who back them</p></div>
<div class=r>Private capital<br>software for MENA<small>Cap tables · ESOP · Portfolio analytics</small></div></div>`;
(async()=>{const b=await chromium.launch();
const jobs={'linkedin-cover-1128x191':[1128,191,280,40,30,11,13,19],'x-header-1500x500':[1500,500,300,70,54,17,22,30]};
for(const [n,[w,h,...a]] of Object.entries(jobs)){
 const pg=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
 await pg.setContent(page(w,h,...a));await pg.waitForTimeout(3000);
 await pg.screenshot({path:n+'.png'});await pg.close();}
await b.close();})();
