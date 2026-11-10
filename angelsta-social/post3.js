const {chromium}=require('playwright');const fs=require('fs');
const LOGO='data:image/png;base64,'+fs.readFileSync(__dirname+'/assets/angelsta-lockup-light.png').toString('base64');
const FONTS='<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;600&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">';
const CSS=`*{margin:0;box-sizing:border-box}
body{background:#0F3330;color:#F6F8F8;font-family:Montserrat,sans-serif;position:relative;overflow:hidden}
.n{position:absolute;font-size:22px;letter-spacing:.2em;color:#3E6B66;font-weight:500}
.ill{position:absolute;font-size:22px;letter-spacing:.12em;color:#8CC2BB;font-weight:500;text-transform:uppercase}
.pg{position:absolute;inset:0;padding:110px 96px;display:flex;flex-direction:column;justify-content:center}
h1{font-family:'Playfair Display',serif;font-style:italic;font-weight:400;line-height:1.12}
h2{font-weight:500;line-height:1.15;letter-spacing:-.01em}
p{font-weight:300;line-height:1.45;color:#D7DCDB}
.hl{color:#8CC2BB}
.xx{font-family:Montserrat,sans-serif;font-style:normal;font-size:.5em;font-weight:600;margin-left:6px}
.bar{display:flex;width:100%;height:120px;border-radius:4px;overflow:hidden;margin:56px 0 18px}
.bar div{display:flex;align-items:center;justify-content:center;font-weight:600;font-size:30px;color:#0F3330}
.lab{display:flex;width:100%;font-size:24px;font-weight:500;color:#D7DCDB;letter-spacing:.03em}
.lab span{text-align:center}
.big{font-family:'Playfair Display',serif;font-style:italic;font-size:260px;line-height:1;margin-top:56px;color:#8CC2BB}
.chips{display:flex;align-items:center;gap:22px;margin-top:64px}
.chip{flex:1;height:200px;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.chip small{font-size:26px;font-weight:500;letter-spacing:.1em}.chip b{font-size:54px;font-weight:600}
.op{font-size:54px;font-weight:600;color:#D7DCDB}
img.lg{height:84px;width:auto;position:absolute;left:96px}`;
const x='<span class=xx>x</span>';
const foot=(i)=>`<div class=ill style="left:96px;bottom:84px">Illustrative example</div><div class=n style="right:96px;bottom:84px">${i} / 6</div>`;
const S=[
`<div class=pg><img class=lg src="${LOGO}" style="top:96px"><h1 style="font-size:100px">The same fund can be <span class=hl>1.5${x}</span> and 1.2${x}.</h1><p style="font-size:38px;margin-top:44px">Both numbers are correct.</p></div>${foot(1)}`,
`<div class=pg><h2 style="font-size:64px">The setup.</h2><p style="font-size:42px;margin-top:40px">Limited partners (LPs) paid in $10M. $8M went into companies. <span class=hl style="font-weight:500">$2M went to fees and expenses.</span></p><div class=bar><div style="width:80%;background:#3E6B66;color:#F6F8F8">$8M invested</div><div style="width:20%;background:#8CC2BB">$2M</div></div></div>${foot(2)}`,
`<div class=pg><h2 style="font-size:64px">MOIC on the deals.</h2><p style="font-size:42px;margin-top:40px">The companies are now worth $12M. $12M ÷ $8M invested.</p><div class=big>1.5${x}</div></div>${foot(3)}`,
`<div class=pg><h2 style="font-size:64px">TVPI on the fund.</h2><p style="font-size:42px;margin-top:40px">TVPI divides by everything paid in, fees included. $12M ÷ $10M, before carry.</p><div class=big>1.2${x}</div></div>${foot(4)}`,
`<div class=pg><h2 style="font-size:64px">The split.</h2><p style="font-size:42px;margin-top:40px">Nothing has been distributed yet, so all of TVPI is residual value.</p><div class=chips><div class=chip style="background:#3E6B66"><small>DPI</small><b>0.0${x}</b></div><div class=op>+</div><div class=chip style="background:#D7DCDB;color:#0F3330"><small>RVPI</small><b>1.2${x}</b></div><div class=op>=</div><div class=chip style="background:#8CC2BB;color:#0F3330"><small>TVPI</small><b>1.2${x}</b></div></div></div>${foot(5)}`,
`<div class=pg><h1 style="font-size:84px">Neither number is wrong.</h1><h1 class=hl style="font-size:84px;margin-top:28px">Ask which denominator.</h1><img class=lg src="${LOGO}" style="bottom:84px;height:76px"></div><div class=n style="right:96px;bottom:84px">6 / 6</div>`];
const X=`<div style="position:absolute;inset:0;padding:80px 110px;display:flex;flex-direction:column;justify-content:center">
<h1 style="font-size:70px">One fund. Two correct numbers.</h1>
<div style="display:flex;gap:60px;margin-top:48px">
<div style="flex:1;border-top:2px solid #3E6B66;padding-top:22px"><div class=big style="font-size:190px;margin:0;color:#F6F8F8">1.5${x}</div><p style="font-size:28px;margin-top:14px"><b style="font-weight:600;color:#F6F8F8">MOIC</b> on investments<br>$12M ÷ $8M invested</p></div>
<div style="flex:1;border-top:2px solid #8CC2BB;padding-top:22px"><div class=big style="font-size:190px;margin:0">1.2${x}</div><p style="font-size:28px;margin-top:14px"><b style="font-weight:600;color:#8CC2BB">TVPI</b> on paid-in, before carry<br>$12M ÷ $10M paid in</p></div></div></div>
<div class=ill style="left:110px;bottom:50px">Illustrative example</div><img class=lg src="${LOGO}" style="right:110px;left:auto;bottom:38px;height:56px;position:absolute">`;
(async()=>{const b=await chromium.launch();
const shoot=async(html,w,h,f)=>{const pg=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
 await pg.setContent(`<!doctype html><meta charset=utf-8>${FONTS}<style>${CSS}body{width:${w}px;height:${h}px}</style><body>${html}`);await pg.waitForTimeout(2500);await pg.screenshot({path:f});await pg.close();};
for(let i=0;i<S.length;i++)await shoot(S[i],1080,1350,`post3/linkedin-carousel-${i+1}.png`);
await shoot(X,1600,900,'post3/x-image-1600x900.png');await b.close();})();
