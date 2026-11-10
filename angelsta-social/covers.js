const {chromium}=require('playwright');const fs=require('fs');
const LOGO='data:image/png;base64,'+fs.readFileSync(__dirname+'/assets/angelsta-lockup-light.png').toString('base64');
const FONTS='<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">';
const strip=['#10211F','#0F3330','#3E6B66','#8CC2BB','#D7DCDB'].map(c=>`<i style="background:${c}"></i>`).join('');
// layout: 'row' (LinkedIn) or 'stack' (X)
const page=(w,h,o)=>`<!doctype html><meta charset=utf-8>${FONTS}<style>
*{margin:0;box-sizing:border-box}
body{width:${w}px;height:${h}px;background:#0F3330;position:relative;overflow:hidden;font-family:Montserrat,sans-serif;color:#F6F8F8}
.strip{position:absolute;top:0;left:0;right:0;height:${o.strip}px;display:flex}.strip i{flex:1}
.wrap{position:absolute;left:${o.left}px;right:${o.right}px;top:${o.strip}px;bottom:0;display:flex;align-items:center;flex-direction:${o.dir};gap:${o.gap}px;justify-content:${o.dir=='row'?'flex-start':'center'};align-items:${o.dir=='row'?'center':'flex-start'}}
img.w{position:absolute;right:${o.wr||0}px;top:50%;transform:translateY(-45%);height:${o.wh||0}px;opacity:.14}
img{height:${o.logo}px;width:auto;display:block}
.sep{width:1px;align-self:stretch;margin:${o.sepm}px 0;background:#3E6B66}
.hl{display:flex;flex-direction:column;gap:${o.hs*0.3}px}
h1{font-family:'Playfair Display',serif;font-style:italic;font-weight:400;font-size:${o.hs}px;line-height:1.1}
p{font-weight:300;font-size:${o.ss}px;letter-spacing:.04em;color:#D7DCDB}
</style><body><div class=strip>${strip}</div>
<div class=wrap><img src="${LOGO}">${o.dir=='row'?'<div class=sep></div>':''}<div class=hl><h1>One record for every round.</h1><p>System of record for founders and the investors who back them</p></div></div>`;
(async()=>{const b=await chromium.launch();
const jobs={
'linkedin-cover-1128x191':[1128,191,{strip:5,left:270,right:30,dir:'row',gap:30,logo:62,sepm:46,hs:27,ss:11.5}],
'x-header-1500x500':[1500,500,{strip:8,left:300,right:60,dir:'column',gap:34,logo:104,sepm:0,hs:50,ss:17}]};
for(const [n,[w,h,o]] of Object.entries(jobs)){
 const pg=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
 await pg.setContent(page(w,h,o));await pg.waitForTimeout(3000);
 await pg.screenshot({path:n+'.png'});await pg.close();}
await b.close();})();
