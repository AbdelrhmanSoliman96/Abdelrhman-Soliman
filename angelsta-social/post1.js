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
.bar{display:flex;width:100%;height:120px;border-radius:4px;overflow:hidden;margin:56px 0 18px}
.bar div{display:flex;align-items:center;justify-content:center;font-weight:600;font-size:34px;color:#0F3330}
.lab{display:flex;width:100%;font-size:24px;font-weight:500;color:#D7DCDB;letter-spacing:.03em}
.lab span{text-align:center}
img.lg{height:84px;width:auto;position:absolute;left:96px}`;
const bar=(hl)=>`<div class=bar><div style="width:70%;background:#3E6B66;color:#F6F8F8">70%</div><div style="width:10%;background:#8CC2BB">10%</div><div style="width:20%;background:#D7DCDB">20%</div></div>
<div class=lab><span style="width:70%">Existing holders</span><span style="width:10%">Pool</span><span style="width:20%">Investor</span></div>`;
const S=[
`<div class=pg><img class=lg src="${LOGO}" style="top:96px"><h1 style="font-size:104px">A $8M pre-money can mean <span class=hl>$7M.</span></h1><p style="font-size:38px;margin-top:44px">The difference is the option pool.</p></div><div class=ill style="left:96px;bottom:84px">Illustrative example</div><div class=n style="right:96px;bottom:84px">1 / 6</div>`,
`<div class=pg><h2 style="font-size:64px">The round.</h2><p style="font-size:44px;margin-top:40px">$2M invested at an <span class=hl style="font-weight:500">$8M pre-money</span>. That makes $10M post-money.</p><p style="font-size:44px;margin-top:28px">The investor owns 20%.</p></div><div class=ill style="left:96px;bottom:84px">Illustrative example</div><div class=n style="right:96px;bottom:84px">2 / 6</div>`,
`<div class=pg><h2 style="font-size:64px">The pool.</h2><p style="font-size:44px;margin-top:40px">The term sheet asks for a <span class=hl style="font-weight:500">10% unallocated pool</span>, measured <span style="white-space:nowrap">post-money</span>.</p><p style="font-size:44px;margin-top:28px">That is $1M of the $10M.</p></div><div class=ill style="left:96px;bottom:84px">Illustrative example</div><div class=n style="right:96px;bottom:84px">3 / 6</div>`,
`<div class=pg><h2 style="font-size:64px">Who pays for it.</h2><p style="font-size:40px;margin-top:36px">The pool is created before the new money comes in. It comes out of the people already on the cap table.</p>${bar()}</div><div class=ill style="left:96px;bottom:84px">Illustrative example</div><div class=n style="right:96px;bottom:84px">4 / 6</div>`,
`<div class=pg><h2 style="font-size:64px">The result.</h2><p style="font-size:44px;margin-top:40px">Existing holders own 70%, not 80%.</p><p style="font-size:44px;margin-top:28px">Effective pre-money: <span class=hl style="font-weight:500">$7M</span>, not $8M.</p></div><div class=ill style="left:96px;bottom:84px">Illustrative example</div><div class=n style="right:96px;bottom:84px">5 / 6</div>`,
`<div class=pg><h1 style="font-size:80px">The headline valuation names the round.</h1><h1 class=hl style="font-size:80px;margin-top:28px">The pool shows what it costs.</h1><p style="font-size:34px;margin-top:44px">Model the pool before you read the valuation.</p><img class=lg src="${LOGO}" style="bottom:84px;height:76px"></div><div class=n style="right:96px;bottom:84px">6 / 6</div>`];
const X=`<div style="position:absolute;inset:0;padding:90px 110px;display:flex;flex-direction:column;justify-content:center">
<h1 style="font-size:76px">Who pays for the option pool?</h1><p style="font-size:30px;margin-top:20px">$2M in at an $8M pre-money. A 10% post-money pool.</p>
${bar().replace('height:120px','')}</div><div class=ill style="left:110px;bottom:56px">Illustrative example</div><img class=lg src="${LOGO}" style="right:110px;left:auto;bottom:44px;height:56px;position:absolute">`;
(async()=>{const b=await chromium.launch();
const shoot=async(html,w,h,f,dsf,extra='')=>{const pg=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:dsf});
 await pg.setContent(`<!doctype html><meta charset=utf-8>${FONTS}<style>${CSS}body{width:${w}px;height:${h}px}${extra}</style><body>${html}`);await pg.waitForTimeout(2500);await pg.screenshot({path:f});await pg.close();};
for(let i=0;i<S.length;i++)await shoot(S[i],1080,1350,`post1/linkedin-carousel-${i+1}.png`,1);
await shoot(X,1600,900,'post1/x-image-1600x900.png',1,'.bar{height:110px!important}');
await b.close();})();
