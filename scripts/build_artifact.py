"""Generate the interactive Mission Atlas artifact (single self-contained HTML file)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from startpad.missions import ALWAYS_AVAILABLE, MAPPING, MISSIONS  # noqa: E402
from startpad.resources import BY_MISSION, FOUNDATION, FUNDRAISING  # noqa: E402
from startpad.tools import CATEGORY_ORDER, TOOLS, TOOL_BY_NAME  # noqa: E402
from scripts.build_xlsx import FINDINGS  # noqa: E402
from scripts.build_docx import DONE_WELL  # noqa: E402


def payload():
    tools = [{"n": n, "c": c, "d": d, "r": r} for n, c, d, r in TOOLS]
    missions = []
    for m in MISSIONS:
        block = MAPPING[m["id"]]
        missions.append({
            "id": m["id"], "title": m["title"], "phase": m["phase"],
            "points": m["points"], "time": m["time"], "summary": m["summary"],
            "questions": m["questions"],
            "tools": {k: [{"t": t, "w": w, "f": f} for t, w, f in block.get(k, [])]
                      for k in ("core", "supporting", "stretch")},
            "resources": [{"k": k, "t": t, "s": s, "u": u, "l": ln, "g": lg, "w": w}
                          for k, t, s, u, ln, lg, w in BY_MISSION.get(m["id"], [])],
            "done": DONE_WELL[m["id"]],
        })
    return {
        "tools": tools,
        "missions": missions,
        "categoryOrder": CATEGORY_ORDER,
        "toolkit": [{"shelf": s,
                     "items": [{"t": t, "w": w, "c": TOOL_BY_NAME[t][1]} for t, w in items]}
                    for s, items in ALWAYS_AVAILABLE.items()],
        "findings": [{"f": f, "w": w, "r": r} for f, w, r in FINDINGS],
        "foundation": [{"k": k, "t": t, "s": s, "u": u, "l": ln, "g": lg, "w": w}
                       for k, t, s, u, ln, lg, w in FOUNDATION],
        "fundraising": [{"k": k, "t": t, "s": s, "u": u, "l": ln, "g": lg, "w": w}
                        for k, t, s, u, ln, lg, w in FUNDRAISING],
    }


HTML = r"""<title>Startpad Mission Atlas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;600&display=swap">
<style>
:root{
  --ground:#F5F7F5; --panel:#FFFFFF; --sunk:#ECF0EE; --line:#D9E2DE; --line-soft:#E6ECE9;
  --ink:#16211E; --ink-2:#4A5A55; --ink-3:#788883;
  --core:#0F5C4B; --core-bg:#DCEBE4; --core-line:#9CC4B5;
  --supp:#1D6FA3; --supp-bg:#DDE9F3; --supp-line:#A2C2DB;
  --stretch:#8A6E3C; --stretch-bg:#EFE7D8; --stretch-line:#CFBC9B;
  --flag:#B4531C; --flag-bg:#F6E5DA;
  --shadow:0 1px 2px rgba(22,33,30,.05), 0 8px 24px -16px rgba(22,33,30,.28);
  color-scheme:light;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0E1412; --panel:#161D1B; --sunk:#111917; --line:#2A3733; --line-soft:#212C29;
    --ink:#E6EDEA; --ink-2:#A3B2AD; --ink-3:#74837E;
    --core:#5FBFA3; --core-bg:#14312A; --core-line:#2E5C4F;
    --supp:#71B4E0; --supp-bg:#132836; --supp-line:#2C516B;
    --stretch:#C9A971; --stretch-bg:#2B2417; --stretch-line:#57482C;
    --flag:#E08A55; --flag-bg:#33200F;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px -18px rgba(0,0,0,.8);
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --ground:#0E1412; --panel:#161D1B; --sunk:#111917; --line:#2A3733; --line-soft:#212C29;
  --ink:#E6EDEA; --ink-2:#A3B2AD; --ink-3:#74837E;
  --core:#5FBFA3; --core-bg:#14312A; --core-line:#2E5C4F;
  --supp:#71B4E0; --supp-bg:#132836; --supp-line:#2C516B;
  --stretch:#C9A971; --stretch-bg:#2B2417; --stretch-line:#57482C;
  --flag:#E08A55; --flag-bg:#33200F;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px -18px rgba(0,0,0,.8);
  color-scheme:dark;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"IBM Plex Sans","IBM Plex Sans Arabic",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:14px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
a{color:var(--supp)}
:focus-visible{outline:2px solid var(--core); outline-offset:2px; border-radius:3px}
@media (prefers-reduced-motion:reduce){*{animation:none!important; transition:none!important}}

.wrap{max-width:1440px; margin:0 auto; padding:0 24px 72px}

/* ---------- masthead ---------- */
header.top{padding:38px 0 20px; border-bottom:1px solid var(--line)}
.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px; font-weight:500;
  letter-spacing:.16em; text-transform:uppercase; color:var(--ink-3); margin:0 0 10px;
}
h1{
  font-family:Fraunces,Georgia,serif; font-optical-sizing:auto;
  font-size:clamp(30px,4.4vw,46px); font-weight:600; line-height:1.05; letter-spacing:-.015em;
  margin:0 0 10px; text-wrap:balance;
}
.lede{max-width:66ch; color:var(--ink-2); font-size:15px; margin:0 0 20px}
.stats{display:flex; flex-wrap:wrap; gap:0; border:1px solid var(--line); border-radius:6px; overflow:hidden; background:var(--panel)}
.stat{padding:11px 18px; border-right:1px solid var(--line-soft); flex:1 1 auto; min-width:112px}
.stat:last-child{border-right:0}
.stat b{display:block; font-family:"IBM Plex Mono",monospace; font-size:19px; font-weight:600;
  font-variant-numeric:tabular-nums; letter-spacing:-.02em}
.stat span{display:block; font-size:10.5px; letter-spacing:.07em; text-transform:uppercase; color:var(--ink-3); margin-top:1px}

/* ---------- tabs ---------- */
nav.tabs{display:flex; gap:2px; margin:22px 0 0; flex-wrap:wrap; border-bottom:1px solid var(--line)}
.tab{
  appearance:none; background:none; border:0; border-bottom:2px solid transparent;
  font:inherit; font-size:13px; font-weight:500; color:var(--ink-2);
  padding:9px 15px; cursor:pointer; margin-bottom:-1px;
}
.tab:hover{color:var(--ink)}
.tab[aria-selected="true"]{color:var(--core); border-bottom-color:var(--core); font-weight:600}

/* ---------- mission layout ---------- */
.cols{display:grid; grid-template-columns:270px minmax(0,1fr); gap:26px; margin-top:24px; align-items:start}
@media (max-width:900px){.cols{grid-template-columns:1fr}}

.rail{position:sticky; top:12px; border:1px solid var(--line); border-radius:6px; background:var(--panel); overflow:hidden}
@media (max-width:900px){.rail{position:static}}
.phase-h{
  font-family:"IBM Plex Mono",monospace; font-size:10px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--ink-3); padding:11px 14px 5px; background:var(--sunk); border-bottom:1px solid var(--line-soft);
  border-top:1px solid var(--line-soft);
}
.phase-h:first-child{border-top:0}
.mrow{
  display:grid; grid-template-columns:26px minmax(0,1fr) auto; gap:9px; align-items:baseline;
  width:100%; text-align:left; appearance:none; background:none; border:0; border-bottom:1px solid var(--line-soft);
  font:inherit; padding:9px 14px; cursor:pointer; color:var(--ink);
}
.mrow:hover{background:var(--sunk)}
.mrow[aria-current="true"]{background:var(--core-bg); box-shadow:inset 3px 0 0 var(--core)}
.mrow .num{font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--ink-3); font-variant-numeric:tabular-nums}
.mrow[aria-current="true"] .num{color:var(--core); font-weight:600}
.mrow .nm{font-size:12.5px; font-weight:500; line-height:1.3}
.mrow[aria-current="true"] .nm{font-weight:600}
.mrow .pt{font-family:"IBM Plex Mono",monospace; font-size:10.5px; color:var(--ink-3); font-variant-numeric:tabular-nums}
.railfoot{padding:10px 14px; font-size:11.5px; color:var(--ink-3); background:var(--sunk)}

.panel{border:1px solid var(--line); border-radius:6px; background:var(--panel); box-shadow:var(--shadow); overflow:hidden}
.phead{padding:20px 24px 16px; border-bottom:1px solid var(--line)}
.phead .kicker{font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ink-3); margin:0 0 6px}
.phead h2{font-family:Fraunces,Georgia,serif; font-size:27px; font-weight:600; margin:0 0 6px;
  letter-spacing:-.01em; line-height:1.15; text-wrap:balance}
.phead p{margin:0; color:var(--ink-2); font-size:14px; max-width:62ch}
.meta{display:flex; flex-wrap:wrap; gap:7px; margin-top:13px}
.chip{font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.05em; text-transform:uppercase;
  padding:3px 9px; border-radius:3px; background:var(--sunk); color:var(--ink-2); border:1px solid var(--line-soft)}

.sect{padding:20px 24px; border-bottom:1px solid var(--line-soft)}
.sect:last-child{border-bottom:0}
.sect > h3{
  font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--ink-3); margin:0 0 13px; font-weight:500;
}
.qlist{margin:0; padding:0; list-style:none; display:grid; gap:5px}
.qlist li{display:grid; grid-template-columns:30px minmax(0,1fr); gap:8px; font-size:13.5px; align-items:baseline}
.qlist .q{font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--core); font-weight:600}

.rolehead{display:flex; align-items:center; gap:9px; margin:20px 0 10px}
.rolehead:first-of-type{margin-top:0}
.rolebadge{font-family:"IBM Plex Mono",monospace; font-size:10px; letter-spacing:.12em; text-transform:uppercase;
  font-weight:600; padding:3px 8px; border-radius:3px; border:1px solid}
.r-core .rolebadge{color:var(--core); background:var(--core-bg); border-color:var(--core-line)}
.r-supporting .rolebadge{color:var(--supp); background:var(--supp-bg); border-color:var(--supp-line)}
.r-stretch .rolebadge{color:var(--stretch); background:var(--stretch-bg); border-color:var(--stretch-line)}
.rolehead .note{font-size:12px; color:var(--ink-3)}

.tools{display:grid; gap:0; border:1px solid var(--line-soft); border-radius:5px; overflow:hidden}
.tool{display:grid; grid-template-columns:210px minmax(0,1fr); gap:16px; padding:11px 14px;
  border-bottom:1px solid var(--line-soft); align-items:start}
.tool:last-child{border-bottom:0}
.tool:nth-child(odd){background:var(--sunk)}
@media (max-width:640px){.tool{grid-template-columns:1fr; gap:4px}}
.tool .tn{font-size:13px; font-weight:600; line-height:1.3}
.r-core .tool .tn{color:var(--core)}
.r-supporting .tool .tn{color:var(--supp)}
.r-stretch .tool .tn{color:var(--stretch)}
.tool .tc{font-size:10.5px; color:var(--ink-3); margin-top:2px}
.tool .tw{font-size:13px; color:var(--ink)}
.tool .tf{font-family:"IBM Plex Mono",monospace; font-size:10.5px; color:var(--ink-3); margin-top:4px; line-height:1.45}

.res{display:grid; gap:9px}
.rescard{display:grid; grid-template-columns:76px minmax(0,1fr); gap:13px; padding:11px 13px;
  border:1px solid var(--line-soft); border-radius:5px; background:var(--sunk); align-items:start}
@media (max-width:640px){.rescard{grid-template-columns:1fr; gap:5px}}
.kind{font-family:"IBM Plex Mono",monospace; font-size:9.5px; letter-spacing:.1em; text-transform:uppercase;
  font-weight:600; padding:3px 0; text-align:center; border-radius:3px; border:1px solid}
.k-video,.k-playlist{color:var(--flag); background:var(--flag-bg); border-color:var(--flag)}
.k-article,.k-data{color:var(--core); background:var(--core-bg); border-color:var(--core-line)}
.k-guide,.k-course,.k-template{color:var(--supp); background:var(--supp-bg); border-color:var(--supp-line)}
.rescard .rt{font-size:13.5px; font-weight:600; line-height:1.3}
.rescard .rm{font-size:11px; color:var(--ink-3); margin-top:2px}
.rescard .rw{font-size:12.5px; color:var(--ink-2); margin-top:5px}
.rescard a{font-family:"IBM Plex Mono",monospace; font-size:10.5px; word-break:break-all; display:inline-block; margin-top:4px}

.done{margin:0; padding:0; list-style:none; display:grid; gap:6px}
.done li{display:grid; grid-template-columns:16px minmax(0,1fr); gap:8px; font-size:13px; align-items:start}
.done .mk{color:var(--core); font-weight:700; line-height:1.5}

/* ---------- matrix ---------- */
.tools-bar{display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:20px 0 14px}
.search{flex:1 1 240px; max-width:340px; padding:8px 11px; border:1px solid var(--line); border-radius:5px;
  background:var(--panel); color:var(--ink); font:inherit; font-size:13px}
.search::placeholder{color:var(--ink-3)}
.legend{display:flex; gap:14px; flex-wrap:wrap; font-size:12px; color:var(--ink-2); align-items:center}
.legend i{display:inline-grid; place-items:center; width:19px; height:19px; border-radius:3px; border:1px solid;
  font-family:"IBM Plex Mono",monospace; font-size:10px; font-weight:600; font-style:normal; margin-right:5px}
.sw-core{color:var(--core); background:var(--core-bg); border-color:var(--core-line)}
.sw-supporting{color:var(--supp); background:var(--supp-bg); border-color:var(--supp-line)}
.sw-stretch{color:var(--stretch); background:var(--stretch-bg); border-color:var(--stretch-line)}
.sw-none{color:var(--ink-3); background:var(--sunk); border-color:var(--line-soft)}

.matrix-scroll{overflow:auto; max-height:78vh; border:1px solid var(--line); border-radius:6px; background:var(--panel)}
table.matrix{border-collapse:separate; border-spacing:0; font-size:12px; width:auto}
table.matrix th,table.matrix td{border-bottom:1px solid var(--line-soft); border-right:1px solid var(--line-soft)}
table.matrix thead th{
  position:sticky; top:0; z-index:3; background:var(--sunk); color:var(--ink-2);
  font-family:"IBM Plex Mono",monospace; font-size:10.5px; font-weight:600; padding:7px 4px;
  text-align:center; border-bottom:1px solid var(--line);
}
table.matrix thead th.corner{left:0; z-index:5; text-align:left; padding-left:12px; min-width:230px}
table.matrix thead th.catcol{left:230px; z-index:5; text-align:left; padding-left:10px; min-width:150px}
table.matrix tbody th.tname{
  position:sticky; left:0; z-index:2; background:var(--panel); text-align:left; font-weight:600;
  font-size:12px; padding:6px 12px; min-width:230px; max-width:230px;
}
table.matrix tbody td.cat{
  position:sticky; left:230px; z-index:2; background:var(--panel); color:var(--ink-3);
  font-size:10.5px; padding:6px 10px; min-width:150px; max-width:190px; white-space:nowrap;
  overflow:hidden; text-overflow:ellipsis;
}
table.matrix tbody tr:hover th.tname,table.matrix tbody tr:hover td.cat{background:var(--sunk)}
table.matrix td.cell{width:38px; min-width:38px; text-align:center; padding:5px 0;
  font-family:"IBM Plex Mono",monospace; font-size:11px; font-weight:600}
td.c-core{color:var(--core); background:var(--core-bg)}
td.c-supporting{color:var(--supp); background:var(--supp-bg)}
td.c-stretch{color:var(--stretch); background:var(--stretch-bg)}
tr.shelved th.tname{color:var(--ink-3); font-weight:500; font-style:italic}
.count{font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--ink-3); font-variant-numeric:tabular-nums}

/* ---------- toolkit / findings ---------- */
.shelf{border:1px solid var(--line); border-radius:6px; background:var(--panel); margin-top:16px; overflow:hidden}
.shelf > h3{margin:0; padding:13px 18px; font-family:Fraunces,Georgia,serif; font-size:17px; font-weight:600;
  background:var(--sunk); border-bottom:1px solid var(--line); letter-spacing:-.005em}
.shelfitem{display:grid; grid-template-columns:220px minmax(0,1fr); gap:16px; padding:9px 18px;
  border-bottom:1px solid var(--line-soft); font-size:13px; align-items:baseline}
.shelfitem:last-child{border-bottom:0}
@media (max-width:640px){.shelfitem{grid-template-columns:1fr; gap:3px}}
.shelfitem b{font-weight:600}
.shelfitem .sc{font-size:10.5px; color:var(--ink-3); display:block}

.finding{border:1px solid var(--line); border-left:3px solid var(--flag); border-radius:5px;
  background:var(--panel); padding:15px 18px; margin-top:12px}
.finding h3{margin:0 0 7px; font-size:15.5px; font-weight:600; line-height:1.3; letter-spacing:-.005em}
.finding h3 .n{font-family:"IBM Plex Mono",monospace; font-size:12px; color:var(--flag); margin-right:8px}
.finding p{margin:0 0 8px; font-size:13px; color:var(--ink-2); max-width:78ch}
.finding .rec{font-size:13px; color:var(--ink); max-width:78ch}
.finding .rec b{color:var(--core)}

.intro{max-width:74ch; color:var(--ink-2); font-size:13.5px; margin:18px 0 4px}
footer.foot{margin-top:38px; padding-top:16px; border-top:1px solid var(--line); font-size:12px; color:var(--ink-3); max-width:80ch}
[hidden]{display:none!important}
</style>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Startpad · startpad.me · mission design</p>
  <h1>Mission Atlas</h1>
  <p class="lede">Every tool in the Startpad library, placed against the 15 missions — with the reason
  it belongs there and the mission question its output should fill in. Plus the video and reading
  material worth putting in front of a founder before each mission starts.</p>
  <div class="stats" id="stats"></div>
  <nav class="tabs" role="tablist" aria-label="Views">
    <button class="tab" role="tab" id="tab-missions"  aria-selected="true"  aria-controls="v-missions">Missions</button>
    <button class="tab" role="tab" id="tab-matrix"    aria-selected="false" aria-controls="v-matrix">Coverage matrix</button>
    <button class="tab" role="tab" id="tab-toolkit"   aria-selected="false" aria-controls="v-toolkit">Founder Toolkit</button>
    <button class="tab" role="tab" id="tab-resources" aria-selected="false" aria-controls="v-resources">Resources</button>
    <button class="tab" role="tab" id="tab-findings"  aria-selected="false" aria-controls="v-findings">Findings</button>
  </nav>
</header>

<section id="v-missions" role="tabpanel" aria-labelledby="tab-missions">
  <div class="cols">
    <aside class="rail" id="rail" aria-label="Missions"></aside>
    <main class="panel" id="detail"></main>
  </div>
</section>

<section id="v-matrix" role="tabpanel" aria-labelledby="tab-matrix" hidden>
  <p class="intro">122 tools down, 15 missions across. Read a column for a mission's whole toolset;
  read a row for a tool's life across the journey. Tool names in italic grey are never used inside a
  mission — they live on a Founder Toolkit shelf instead.</p>
  <div class="tools-bar">
    <input class="search" id="msearch" type="search" placeholder="Filter tools or categories…" aria-label="Filter tools">
    <div class="legend">
      <span><i class="sw-core">C</i>Core</span>
      <span><i class="sw-supporting">S</i>Supporting</span>
      <span><i class="sw-stretch">·</i>Stretch</span>
      <span><i class="sw-none"></i>not used</span>
      <span class="count" id="mcount"></span>
    </div>
  </div>
  <div class="matrix-scroll"><table class="matrix" id="matrix"></table></div>
</section>

<section id="v-toolkit" role="tabpanel" aria-labelledby="tab-toolkit" hidden>
  <p class="intro">Placing every tool against the missions surfaced a gap: almost the whole fundraising
  block, most of the finance statements, and the team and governance tools are never reachable from the
  mission flow. A founder who only follows missions never opens the Cap Table, the Pitch Deck template,
  or the Legal Checklist. Don't force them into a mission — shelve them, and surface each shelf on a trigger.</p>
  <div id="toolkit"></div>
</section>

<section id="v-resources" role="tabpanel" aria-labelledby="tab-resources" hidden>
  <p class="intro">Foundation material for <span style="font-family:'IBM Plex Mono',monospace">/resources</span>,
  and the reading list for the proposed Mission 16. Per-mission resources sit inside each mission.
  Every URL came from a live web search during compilation — none written from memory — but the
  compiling environment blocked direct page fetches, so run one link check before publishing.</p>
  <div id="resources"></div>
</section>

<section id="v-findings" role="tabpanel" aria-labelledby="tab-findings" hidden>
  <p class="intro">Placing 122 tools against 15 missions is a stress test of the mission design.
  Twelve findings, ordered roughly by what they cost if left alone.</p>
  <div id="findings"></div>
</section>

<footer class="foot">
  Compiled from <b>startpad15missions.md</b>, <b>Startpad — Tool Library (123 tools)</b>,
  the <b>Pitch Deck &amp; One-Pager</b> template and the <b>StartPad End-to-End User Journey</b>.
  122 unique tools · 196 mission-tool placements · 96 curated resources.
  The library's headline count of 123 double-counts <i>Term Sheet Analyzer</i>, which is cross-listed
  on two tabs.
</footer>
</div>

<script>
const DATA = __DATA__;
const ROLES = ["core","supporting","stretch"];
const ROLE_NOTE = {
  core:"required — render on the mission screen, already open",
  supporting:"recommended — one click away in a rail",
  stretch:"optional — collapsed under “go deeper”"
};
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

/* ---------- header stats ---------- */
(function(){
  const placements = DATA.missions.reduce((a,m)=>a+ROLES.reduce((b,r)=>b+m.tools[r].length,0),0);
  const inMission = new Set();
  DATA.missions.forEach(m=>ROLES.forEach(r=>m.tools[r].forEach(t=>inMission.add(t.t))));
  const res = DATA.missions.reduce((a,m)=>a+m.resources.length,0)+DATA.foundation.length+DATA.fundraising.length;
  const pts = DATA.missions.reduce((a,m)=>a+m.points,0);
  const rows = [[DATA.tools.length,"tools"],[DATA.missions.length,"missions"],[placements,"placements"],
                [DATA.tools.length-inMission.size,"shelved"],[res,"resources"],[pts.toLocaleString(),"points"]];
  document.getElementById("stats").innerHTML =
    rows.map(([b,s])=>`<div class="stat"><b>${b}</b><span>${s}</span></div>`).join("");
})();

/* ---------- mission rail ---------- */
let current = 1;
(function(){
  let html = "", phase = null;
  DATA.missions.forEach(m=>{
    if(m.phase !== phase){ phase = m.phase; html += `<div class="phase-h">${esc(phase)}</div>`; }
    html += `<button class="mrow" data-m="${m.id}" aria-current="${m.id===current}">
      <span class="num">${String(m.id).padStart(2,"0")}</span>
      <span class="nm">${esc(m.title)}</span>
      <span class="pt">${m.points}</span></button>`;
  });
  const shelved = DATA.tools.length - new Set(DATA.missions.flatMap(m=>ROLES.flatMap(r=>m.tools[r].map(t=>t.t)))).size;
  html += `<div class="railfoot">${shelved} more tools live on the Founder Toolkit shelves, outside the mission flow.</div>`;
  const rail = document.getElementById("rail");
  rail.innerHTML = html;
  rail.addEventListener("click", e=>{
    const b = e.target.closest(".mrow"); if(!b) return;
    current = +b.dataset.m;
    rail.querySelectorAll(".mrow").forEach(x=>x.setAttribute("aria-current", String(+x.dataset.m===current)));
    renderDetail();
  });
})();

function toolMeta(name){ return DATA.tools.find(t=>t.n===name) || {c:"",d:"",r:""}; }

function renderDetail(){
  const m = DATA.missions.find(x=>x.id===current);
  const nCore = m.tools.core.length, nAll = ROLES.reduce((a,r)=>a+m.tools[r].length,0);
  let h = `<div class="phead">
    <p class="kicker">Mission ${String(m.id).padStart(2,"0")} · ${esc(m.phase)}</p>
    <h2>${esc(m.title)}</h2>
    <p>${esc(m.summary)}</p>
    <div class="meta">
      <span class="chip">${m.points} points</span>
      <span class="chip">${esc(m.time)}</span>
      <span class="chip">${nCore} core of ${nAll} tools</span>
      <span class="chip">${m.resources.length} resources</span>
    </div></div>`;

  h += `<div class="sect"><h3>The questions this mission asks</h3><ul class="qlist">` +
    m.questions.map((q,i)=>`<li><span class="q">Q${i+1}</span><span>${esc(q)}</span></li>`).join("") +
    `</ul></div>`;

  h += `<div class="sect"><h3>Tools mapped to this mission</h3>`;
  ROLES.forEach(r=>{
    const items = m.tools[r]; if(!items.length) return;
    h += `<div class="r-${r}"><div class="rolehead">
        <span class="rolebadge">${r} · ${items.length}</span>
        <span class="note">${ROLE_NOTE[r]}</span></div><div class="tools">`;
    items.forEach(t=>{
      const meta = toolMeta(t.t);
      h += `<div class="tool">
        <div><div class="tn">${esc(t.t)}</div><div class="tc">${esc(meta.c)}</div></div>
        <div><div class="tw">${esc(t.w)}</div>
             <div class="tf">→ feeds ${esc(t.f)}${meta.r?"  ·  "+esc(meta.r):""}</div></div></div>`;
    });
    h += `</div></div>`;
  });
  h += `</div>`;

  if(m.resources.length){
    h += `<div class="sect"><h3>Watch / read before starting</h3><div class="res">` +
      m.resources.map(r=>`<div class="rescard">
        <span class="kind k-${r.k.toLowerCase()}">${esc(r.k)}</span>
        <div><div class="rt">${esc(r.t)}</div>
          <div class="rm">${esc(r.s)} · ${esc(r.l)} · ${esc(r.g)}</div>
          <div class="rw">${esc(r.w)}</div>
          <a href="${esc(r.u)}" target="_blank" rel="noopener noreferrer">${esc(r.u)}</a>
        </div></div>`).join("") + `</div></div>`;
  }

  h += `<div class="sect"><h3>Done well looks like</h3><ul class="done">` +
    m.done.map(d=>`<li><span class="mk">✓</span><span>${esc(d)}</span></li>`).join("") + `</ul></div>`;

  document.getElementById("detail").innerHTML = h;
}
renderDetail();

/* ---------- coverage matrix ---------- */
const LOOKUP = {};
DATA.missions.forEach(m=>ROLES.forEach(r=>m.tools[r].forEach(t=>{ LOOKUP[t.t+"|"+m.id] = r; })));
const MARK = {core:"C", supporting:"S", stretch:"·"};

function renderMatrix(filter){
  const f = (filter||"").trim().toLowerCase();
  const ordered = [];
  DATA.categoryOrder.forEach(c=>DATA.tools.filter(t=>t.c===c).forEach(t=>ordered.push(t)));
  const rows = ordered.filter(t=>!f || t.n.toLowerCase().includes(f) || t.c.toLowerCase().includes(f)
                                  || t.d.toLowerCase().includes(f));
  let head = `<thead><tr><th class="corner">Tool</th><th class="catcol">Category</th>` +
    DATA.missions.map(m=>`<th title="${esc(m.title)}">M${m.id}</th>`).join("") + `</tr></thead>`;
  let body = "<tbody>" + rows.map(t=>{
    const cells = DATA.missions.map(m=>{
      const r = LOOKUP[t.n+"|"+m.id];
      return r ? `<td class="cell c-${r}" title="${esc(t.n)} — ${r} in M${m.id} ${esc(m.title)}">${MARK[r]}</td>`
               : `<td class="cell"></td>`;
    }).join("");
    const used = DATA.missions.some(m=>LOOKUP[t.n+"|"+m.id]);
    return `<tr class="${used?"":"shelved"}"><th class="tname" scope="row" title="${esc(t.d)}">${esc(t.n)}</th>` +
           `<td class="cat">${esc(t.c)}</td>${cells}</tr>`;
  }).join("") + "</tbody>";
  document.getElementById("matrix").innerHTML = head + body;
  document.getElementById("mcount").textContent = `${rows.length} of ${DATA.tools.length} tools`;
}
renderMatrix("");
document.getElementById("msearch").addEventListener("input", e=>renderMatrix(e.target.value));

/* ---------- toolkit ---------- */
document.getElementById("toolkit").innerHTML = DATA.toolkit.map(s=>
  `<section class="shelf"><h3>${esc(s.shelf)}</h3>` +
  s.items.map(i=>`<div class="shelfitem"><div><b>${esc(i.t)}</b><span class="sc">${esc(i.c)}</span></div>
     <div>${esc(i.w)}</div></div>`).join("") + `</section>`).join("");

/* ---------- resources ---------- */
function resBlock(title, items){
  return `<section class="shelf"><h3>${esc(title)}</h3>` + items.map(r=>
    `<div class="shelfitem" style="grid-template-columns:76px minmax(0,1fr)">
       <span class="kind k-${r.k.toLowerCase()}">${esc(r.k)}</span>
       <div><b>${esc(r.t)}</b><span class="sc">${esc(r.s)} · ${esc(r.l)} · ${esc(r.g)}</span>
         <div style="margin-top:5px">${esc(r.w)}</div>
         <a href="${esc(r.u)}" target="_blank" rel="noopener noreferrer"
            style="font-family:'IBM Plex Mono',monospace;font-size:10.5px;word-break:break-all">${esc(r.u)}</a>
       </div></div>`).join("") + `</section>`;
}
document.getElementById("resources").innerHTML =
  resBlock("Foundation — for /resources, offered at onboarding", DATA.foundation) +
  resBlock("Proposed Mission 16 — Raise Your Round", DATA.fundraising);

/* ---------- findings ---------- */
document.getElementById("findings").innerHTML = DATA.findings.map((f,i)=>
  `<article class="finding"><h3><span class="n">${String(i+1).padStart(2,"0")}</span>${esc(f.f)}</h3>
   <p>${esc(f.w)}</p><div class="rec"><b>Recommendation:</b> ${esc(f.r)}</div></article>`).join("");

/* ---------- tabs ---------- */
document.querySelectorAll(".tab").forEach(tab=>{
  tab.addEventListener("click", ()=>{
    document.querySelectorAll(".tab").forEach(t=>{
      const on = t===tab;
      t.setAttribute("aria-selected", String(on));
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
  });
});
</script>
"""


def build(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    html = HTML.replace("__DATA__", json.dumps(payload(), ensure_ascii=False))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path, len(html)


if __name__ == "__main__":
    p, n = build(sys.argv[1] if len(sys.argv) > 1 else "output/startpad_mission_atlas.html")
    print(f"wrote {p}  ({n/1024:.0f} KB)")
