const {chromium}=require('playwright');const fs=require('fs');
const TL=JSON.parse(fs.readFileSync(__dirname+'/timeline.json'));
const LOGO='data:image/png;base64,'+fs.readFileSync(__dirname+'/../../assets/angelsta-lockup-light.png').toString('base64');
const OUT=process.argv[2];const FPS=30;
const FONTS='<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;600;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">';
const html=`<!doctype html><meta charset=utf-8>${FONTS}<style>
*{margin:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:#0F3330;overflow:hidden;font-family:Montserrat,sans-serif;color:#F6F8F8}
.abs{position:absolute}
#strip{position:absolute;top:0;left:0;right:0;height:10px;display:flex}#strip i{flex:1}
#logoTop{left:80px;top:96px;height:64px}
.num{font-family:'Playfair Display',serif;font-style:italic;position:absolute;left:0;width:1080px;text-align:center;line-height:1}
.lbl{position:absolute;left:0;width:1080px;text-align:center;font-weight:500;letter-spacing:.04em;color:#D7DCDB;font-size:38px}
.bar{position:absolute;height:110px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:34px;color:#0F3330}
.chip{position:absolute;height:170px;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:700}
.chip small{font-size:30px;font-weight:500;letter-spacing:.1em;opacity:.85}.chip b{font-size:58px;font-weight:700}
.card{position:absolute;left:90px;width:900px;height:230px;border-radius:16px;border:2px solid #3E6B66;padding:34px 44px}
.card p{font-size:38px;font-weight:300;color:#D7DCDB;line-height:1.3}.card h3{font-size:80px;font-weight:600;margin-top:6px}
#cap{position:absolute;left:60px;width:960px;top:1400px;height:210px;text-align:center;display:flex;flex-wrap:wrap;justify-content:center;align-content:flex-start;gap:6px 22px}
#cap span{font-weight:700;font-size:76px;line-height:1.12;color:#F6F8F8;text-shadow:0 4px 18px rgba(0,0,0,.35)}
#cap span.on{color:#8CC2BB}
#ill{position:absolute;left:0;width:1080px;top:1330px;text-align:center;font-size:24px;letter-spacing:.14em;color:#8CC2BB;font-weight:500;text-transform:uppercase}
  .xx{font-family:Montserrat,sans-serif;font-style:normal;font-size:.5em;font-weight:600;margin-left:6px}
#end{position:absolute;inset:0;background:#0F3330;opacity:0}
#endLogo{position:absolute;left:50%;top:790px;height:230px;transform:translateX(-50%)}
#endTag{position:absolute;left:0;width:1080px;top:1070px;text-align:center;font-family:'Playfair Display',serif;font-style:italic;font-size:54px;color:#D7DCDB}
</style><body>
<div id=strip>${['#10211F','#0F3330','#3E6B66','#8CC2BB','#D7DCDB'].map(c=>`<i style="background:${c}"></i>`).join('')}</div>
<img id=logoTop class=abs src="${LOGO}">
<div id=scene></div><div id=ill>Illustrative example</div><div id=cap></div>
<div id=end><img id=endLogo src="${LOGO}"><div id=endTag>One record for every round.</div></div>`;
const script=`
const TL=${JSON.stringify(TL)};
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const eo=x=>1-Math.pow(1-clamp(x),3);
const eb=x=>{x=clamp(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const lerp=(a,b,x)=>a+(b-a)*x;
const $=id=>document.getElementById(id);
const scene=$('scene');
let built=false,els={};
function mk(tag,cls,css,txt){const e=document.createElement(tag);e.className=cls||'';Object.assign(e.style,css||{});if(txt!==undefined)e.innerHTML=txt;scene.appendChild(e);return e}
function build(){
 // S1
 els.n15=mk('div','num',{top:'340px',fontSize:'330px',color:'#F6F8F8'},'1.5<span class=xx>x</span>');
 els.n12=mk('div','num',{top:'720px',fontSize:'330px',color:'#8CC2BB'},'1.2<span class=xx>x</span>');
 els.both=mk('div','lbl',{top:'1120px',fontSize:'46px',color:'#F6F8F8',fontWeight:'600'},'Same fund. Both correct.');
 // bars (60px per $M, origin x=180)
 els.tPaid=mk('div','lbl',{top:'470px',textAlign:'left',left:'180px',width:'800px',fontSize:'34px'},'LPs paid in: $10M');
 els.bInv=mk('div','bar',{left:'180px',top:'530px',background:'#3E6B66',color:'#F6F8F8',width:'0px'},'$8M invested');
 els.bFee=mk('div','bar',{left:'660px',top:'530px',background:'#D7DCDB',width:'0px',fontSize:'22px',whiteSpace:'nowrap'},'$2M fees');
 els.tVal=mk('div','lbl',{top:'700px',textAlign:'left',left:'180px',width:'800px',fontSize:'34px'},'Value of companies today: $12M');
 els.bVal=mk('div','bar',{left:'180px',top:'760px',background:'#8CC2BB',width:'0px'},'$12M');
 els.hl8=mk('div','',{position:'absolute',left:'174px',top:'524px',height:'122px',width:'492px',border:'4px solid #8CC2BB',borderRadius:'10px',opacity:0});
 els.hl10=mk('div','',{position:'absolute',left:'174px',top:'524px',height:'122px',width:'612px',border:'4px solid #8CC2BB',borderRadius:'10px',opacity:0});
 els.f1=mk('div','num',{top:'960px',fontSize:'190px',color:'#8CC2BB'},'1.5<span class=xx>x</span>');
 els.f1l=mk('div','lbl',{top:'1190px',fontSize:'40px'},'MOIC on investments · $12M ÷ $8M');
 els.f2=mk('div','num',{top:'960px',fontSize:'190px',color:'#8CC2BB'},'1.2<span class=xx>x</span>');
 els.f2l=mk('div','lbl',{top:'1190px',fontSize:'40px'},'TVPI on paid-in · $12M ÷ $10M · before carry');
 // S5 chips
 const cs=[['DPI','0.0x','#3E6B66','#F6F8F8',70],['+','','',' ',0],['RVPI','1.2x','#D7DCDB','#0F3330',0],['=','','','',0],['TVPI','1.2x','#8CC2BB','#0F3330',0]];
 els.c1=mk('div','chip',{left:'70px',top:'640px',width:'250px',background:'#3E6B66',color:'#F6F8F8'},'<small>DPI</small><b>0.0x</b>');
 els.p=mk('div','lbl',{left:'330px',width:'60px',top:'690px',fontSize:'64px',fontWeight:'600'},'+');
 els.c2=mk('div','chip',{left:'400px',top:'640px',width:'250px',background:'#D7DCDB',color:'#0F3330'},'<small>RVPI</small><b>1.2x</b>');
 els.e=mk('div','lbl',{left:'660px',width:'60px',top:'690px',fontSize:'64px',fontWeight:'600'},'=');
 els.c3=mk('div','chip',{left:'730px',top:'640px',width:'280px',background:'#8CC2BB',color:'#0F3330'},'<small>TVPI</small><b>1.2x</b>');
 els.c5n=mk('div','lbl',{top:'900px',fontSize:'38px'},'Nothing distributed yet, so it is all residual value.');
 // S6 cards
 els.k1=mk('div','card',{top:'470px'},'<p>How good are the deals?</p><h3 style="color:#F6F8F8">MOIC 1.5x</h3>');
 els.k2=mk('div','card',{top:'760px',borderColor:'#8CC2BB'},'<p>What is the position worth against what was paid in?</p><h3 style="color:#8CC2BB">TVPI 1.2x</h3>');
 // S7
 els.q=mk('div','num',{top:'640px',fontSize:'150px',lineHeight:'1.1',color:'#F6F8F8'},'Which<br><span style="color:#8CC2BB">denominator?</span>');
 built=true;
}
function vis(e,o,y){e.style.opacity=o;e.style.transform='translateY('+(y||0)+'px)'}
function render(t){
 if(!built)build();
 const S=TL.segs,T=i=>S[i].start,D=i=>S[i].dur;
 const rel=i=>(t-T(i))/D(i);
 // reset
 Object.values(els).forEach(e=>{e.style.opacity=0;e.style.transform=''});
 // top logo: mask reveal 0.2-1.4s
 const lr=eo((t-0.2)/1.2);$('logoTop').style.clipPath='inset(0 '+((1-lr)*100)+'% 0 0)';$('logoTop').style.opacity=t>TL.end_voice+0.2?clamp(1-(t-TL.end_voice-0.2)/0.5):1;
 $('logoTop').style.transform='translateX('+((1-lr)*-24)+'px)';
 // scenes by time
 const seg=S.findIndex((s,i)=>t>=(i===0?0:s.start-0.2)&&t<(S[i+1]?S[i+1].start-0.2:TL.end_voice+0.4));
 const fade=(i,a=0.25)=>clamp((t-(T(i)-0.2))/a)*clamp(1-(t-(S[i+1]?S[i+1].start-0.45:TL.end_voice))/0.25);
 if(seg===0){const r=rel(0);
  const a=1*clamp(1-(t-(T(1)-0.45))/0.25);
  vis(els.n15,a,(1-eb((t+0.05)/0.6))*60);els.n15.style.transform+=' scale('+lerp(0.8,1,eb((t+0.05)/0.6))+')';
  const t2=T(0)+D(0)*0.50;vis(els.n12,clamp((t-t2)/0.01)*a,(1-eb((t-t2)/0.6))*60);els.n12.style.transform+=' scale('+lerp(0.8,1,eb((t-t2)/0.6))+')';
  const t3=T(0)+D(0)*0.76;vis(els.both,clamp((t-t3)/0.3)*a,(1-eo((t-t3)/0.4))*20);}
 else if(seg>=1&&seg<=4){
  const a=fade(seg);
  // bars
  const s2=rel(1);
  if(seg===1){
   vis(els.tPaid,a);const g=eo((t-T(1)-0.1)/0.9);
   els.bInv.style.width=(480*g)+'px';els.bFee.style.width=(120*g)+'px';
   const ti=T(1)+D(1)*0.38,tf=T(1)+D(1)*0.68;
   els.bInv.style.opacity=a*clamp((t-ti+0.3)/0.3);els.bFee.style.opacity=a*clamp((t-tf+0.3)/0.3);
   els.bInv.style.color=clamp((t-ti)/0.3)>0?'#F6F8F8':'transparent';
   els.bInv.innerHTML=clamp((t-ti)/0.25)>0?'$8M invested':'';els.bFee.innerHTML=clamp((t-tf)/0.25)>0?'$2M fees':'';
   els.bInv.style.opacity=a;els.bFee.style.opacity=a;
  } else {
   vis(els.tPaid,a);els.bInv.style.width='480px';els.bFee.style.width='120px';els.bInv.style.opacity=a;els.bFee.style.opacity=a;
   const tv=seg===2?T(2)+0.1:T(seg)-9;
   vis(els.tVal,a*clamp((t-tv)/0.3));els.bVal.style.opacity=a*clamp((t-tv)/0.1);els.bVal.style.width=(720*eo((t-tv)/0.9))+'px';
   els.bVal.innerHTML=(t-tv>0.8)?'$12M':'';
   if(seg===2){const tf=T(2)+D(2)*0.42;els.hl8.style.opacity=a*clamp((t-tf)/0.3);
     const x=eo((t-tf)/1.0);vis(els.f1,a*clamp((t-tf)/0.2),(1-x)*40);els.f1.innerHTML=(1+0.5*x).toFixed(1)+'<span class=xx>x</span>';vis(els.f1l,a*clamp((t-tf-0.5)/0.4));}
   if(seg===3){const tf=T(3)+D(3)*0.38;els.hl10.style.opacity=a*clamp((t-tf)/0.3);
     const x=eo((t-tf)/1.0);vis(els.f2,a*clamp((t-tf)/0.2),(1-x)*40);els.f2.innerHTML=(1+0.2*x).toFixed(1)+'<span class=xx>x</span>';vis(els.f2l,a*clamp((t-tf-0.5)/0.4));}
   if(seg===4){
     // chips replace bars
     [els.tPaid,els.bInv,els.bFee,els.tVal,els.bVal].forEach(e=>e.style.opacity=0);
     const a4=a;const b1=T(4)+D(4)*0.12,b2=T(4)+D(4)*0.42,b3=T(4)+D(4)*0.72;
     const pop=(e,tt)=>{const x=eb((t-tt)/0.5);e.style.opacity=a4*clamp((t-tt)/0.1);e.style.transform='scale('+lerp(0.7,1,x)+')'};
     pop(els.c1,b1);pop(els.p,b2-0.15);pop(els.c2,b2);pop(els.e,b3-0.15);pop(els.c3,b3);vis(els.c5n,a4*clamp((t-b3-0.5)/0.4));}
  }
 }
 else if(seg===5){const a=fade(5);const r=rel(5);
  const k1=T(5)+D(5)*0.40,k2=T(5)+D(5)*0.68;
  vis(els.k1,a*clamp((t-k1)/0.2),(1-eo((t-k1)/0.5))*50);vis(els.k2,a*clamp((t-k2)/0.2),(1-eo((t-k2)/0.5))*50);}
 else if(seg===6){const a=fade(6);const x=eb((t-T(6))/0.7);vis(els.q,a,(1-x)*40);els.q.style.transform+=' scale('+lerp(0.9,1,x)+')';}
 // illustrative tag
 $('ill').style.opacity=(seg>=0&&seg<=5)?clamp((t-0.8)/0.4):0;
 // captions
 const cap=$('cap');cap.innerHTML='';
 for(let i=0;i<S.length;i++){const s=S[i];if(t<s.start-0.05||t>s.start+s.dur+0.25)continue;
  const words=s.cap.split(' ');const lens=words.map(w=>w.length+2);const tot=lens.reduce((a,b)=>a+b,0);
  const usable=s.dur*0.94;let acc=0;const times=words.map((w,k)=>{const st=s.start+usable*acc/tot;acc+=lens[k];return [st,s.start+usable*acc/tot]});
  // chunks of 3 words
  const ch=[];for(let k=0;k<words.length;k+=3)ch.push([k,Math.min(k+3,words.length)]);
  let cur=ch.findIndex(([a,b])=>t>=times[a][0]-0.04&&t<(times[b]?times[b][0]:1e9)-0.04);
  if(cur<0)cur=t<times[0][0]?0:ch.length-1;
  const [a0,b0]=ch[cur];for(let k=a0;k<b0;k++){const sp=document.createElement('span');sp.textContent=words[k];if(t>=times[k][0]&&t<times[k][1])sp.className='on';cap.appendChild(sp);}
 }
 // end card
 const ec=clamp((t-(TL.end_voice+0.45))/0.5);$('end').style.opacity=ec;
 const lt=eo((t-(TL.end_voice+0.7))/0.9);$('endLogo').style.clipPath='inset(0 '+((1-lt)*100)+'% 0 0)';
 $('endLogo').style.transform='translateX(-50%) scale('+lerp(0.92,1,lt)+')';
 $('endTag').style.opacity=clamp((t-(TL.end_voice+1.7))/0.6);$('endTag').style.transform='translateY('+((1-eo((t-(TL.end_voice+1.7))/0.6))*20)+'px)';
}
`;
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.setContent(html);await pg.addScriptTag({content:script});await pg.waitForTimeout(3000);
const total=Math.round(TL.total*FPS);const only=process.argv[3]?process.argv[3].split(',').map(Number):null;
fs.mkdirSync(OUT,{recursive:true});
const frames=only?only.map(s=>Math.round(s*FPS)):[...Array(total).keys()];
for(const f of frames){await pg.evaluate(t=>render(t),f/FPS);await pg.screenshot({path:`${OUT}/f${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();})();
