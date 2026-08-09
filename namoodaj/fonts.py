import re, base64, urllib.request, os, ssl
import os
BASE = os.path.dirname(os.path.abspath(__file__))
SCR = BASE
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
ctx=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
def get(u):
    r=urllib.request.Request(u,headers=UA)
    return urllib.request.urlopen(r,context=ctx,timeout=60).read()

WANT={"IBM Plex Sans Arabic":{400,500,700},"Noto Kufi Arabic":{700}}
KEEP={"arabic","latin"}

# تنزيل أوراق أنماط الخطوط إن لم تكن موجودة محليًا
CSS_SRC={
 "plex.css":"https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap",
 "kufi.css":"https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@500;700&display=swap",
}
for name,url in CSS_SRC.items():
    dest=os.path.join(SCR,name)
    if not os.path.exists(dest):
        open(dest,"wb").write(get(url))
        print("تنزيل",name)
out=[]; total=0
for f in ["plex.css","kufi.css"]:
    css=open(os.path.join(SCR,f),encoding="utf-8").read()
    blocks=re.split(r"/\*\s*([a-z0-9\-]+)\s*\*/", css)
    # blocks: [pre, name, body, name, body...]
    for i in range(1,len(blocks),2):
        name=blocks[i]; body=blocks[i+1]
        if name not in KEEP: continue
        fam=re.search(r"font-family: '([^']+)'",body).group(1)
        w=int(re.search(r"font-weight: (\d+)",body).group(1))
        if w not in WANT.get(fam,set()): continue
        url=re.search(r"url\((https://[^)]+)\)",body).group(1)
        ur=re.search(r"unicode-range: ([^;]+);",body).group(1)
        data=get(url); total+=len(data)
        b64=base64.b64encode(data).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2');unicode-range:{ur};}}")
        print(f"{fam} {w} {name}: {len(data)/1024:.1f} KB")
open(os.path.join(SCR,"fonts.css"),"w",encoding="utf-8").write("\n".join(out))
print("raw total KB", round(total/1024,1), "| css KB", round(os.path.getsize(os.path.join(SCR,'fonts.css'))/1024,1))
