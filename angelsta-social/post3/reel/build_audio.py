import json,subprocess,wave,numpy as np
S='/tmp/claude-0/-home-user-Abdelrhman-Soliman/366d35d3-d3a3-595a-abae-2e84e0b5e1fb/scratchpad/reel'
segs=json.load(open('segments.json'))
t=0.35
for s in segs:
    s['start']=round(t,3);t+=s['dur']+0.42
end_voice=segs[-1]['start']+segs[-1]['dur']
total=round(end_voice+3.6,2)
json.dump({'segs':segs,'total':total,'end_voice':end_voice},open('timeline.json','w'),indent=1)
print('total',total)
# ---- music (numpy synth) ----
SR=44100;N=int(total*SR);T=np.arange(N)/SR
bpm=84;beat=60/bpm;bar=4*beat
chords=[[130.81,196.0,246.94,329.63],[110.0,164.81,196.0,261.63],[87.31,174.61,220.0,329.63],[98.0,196.0,246.94,329.63]]
def env(n,a,r):
    e=np.ones(n);na=int(a*SR);nr=int(r*SR)
    e[:na]=np.linspace(0,1,na);e[-nr:]=np.minimum(e[-nr:],np.linspace(1,0,nr));return e
pad=np.zeros(N)
nb=int(total/bar)+2
for b in range(nb):
    ch=chords[b%4];s0=int(b*bar*SR);L=int((bar+0.9)*SR)
    if s0>=N:break
    L=min(L,N-s0);tt=np.arange(L)/SR;seg=np.zeros(L)
    for f in ch:
        for det in (-0.6,0,0.6):
            ff=f*(1+det/1000*3)
            seg+=np.sin(2*np.pi*ff*tt)+0.25*np.sin(2*np.pi*2*ff*tt)+0.08*np.sin(2*np.pi*3*ff*tt)
    pad[s0:s0+L]+=seg*env(L,0.9,0.9)*0.035
sub=np.zeros(N)
for b in range(nb):
    s0=int(b*bar*SR);L=min(int(bar*SR),N-s0)
    if L<=0:break
    tt=np.arange(L)/SR;f=chords[b%4][0]/2 if chords[b%4][0]>100 else chords[b%4][0]
    sub[s0:s0+L]+=np.sin(2*np.pi*f*tt)*env(L,0.05,0.4)*0.10
pl=np.zeros(N);pat=[0,2,3,2,1,2,3,2];
k=0;step=beat/2
while k*step<total:
    s0=int(k*step*SR);ch=chords[int(k*step/bar)%4];f=ch[pat[k%8]%4]*2
    L=min(int(1.1*SR),N-s0)
    if L<=0:break
    tt=np.arange(L)/SR;e=np.exp(-tt*5.5)
    pl[s0:s0+L]+=(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*9))*e*0.06*(0.8 if k%2 else 1)
    k+=1
# soft pulse on beats (muted kick)
kick=np.zeros(N);kb=0
while kb*beat<total:
    s0=int(kb*beat*SR);L=min(int(0.35*SR),N-s0)
    if L<=0:break
    tt=np.arange(L)/SR;f=55+60*np.exp(-tt*25)
    kick[s0:s0+L]+=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*10)*(0.20 if kb%4==0 else 0.12 if kb%2==0 else 0.0)
    kb+=1
m=pad+sub+pl+kick
# echo for space
out=m.copy()
for dly,g in ((int(beat*0.75*SR),0.35),(int(beat*1.5*SR),0.2)):
    out[dly:]+=pl[:-dly]*g+pad[:-dly]*0.15
m=out
fade=np.ones(N);fi=int(1.2*SR);fo=int(2.5*SR);fade[:fi]=np.linspace(0,1,fi);fade[-fo:]=np.linspace(1,0,fo)
m=m*fade;m=m/np.max(np.abs(m))*0.9
with wave.open(f'{S}/music.wav','wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((m*32767).astype(np.int16).tobytes())
# ---- mix ----
inputs=[];fc=[];lab=[]
for i,s in enumerate(segs):
    inputs+=['-i',f"{S}/{s['id']}.wav"]
    ms=int(s['start']*1000);fc.append(f"[{i}:a]aresample=44100,adelay={ms}|{ms}[v{i}]");lab.append(f"[v{i}]")
n=len(segs)
fc.append(''.join(lab)+f"amix=inputs={n}:normalize=0,volume=1.6,apad=whole_dur={total}[vo]")
inputs+=['-i',f'{S}/music.wav']
fc.append(f"[{n}:a]aresample=44100,volume=0.55[mu]")
fc.append("[vo]asplit=2[vo1][vo2]")
fc.append("[mu][vo1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck]")
fc.append(f"[duck][vo2]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
subprocess.run(['ffmpeg','-y','-loglevel','error']+inputs+['-filter_complex',';'.join(fc),'-map','[a]','-t',str(total),f'{S}/mix.wav'],check=True)
print('mix ok')
