# Hudba pro promo „Florián pro hasiče“ (odvozeno z music_v2.py): souvislé arpeggio, akord na scénu,
# závěr jen v poslední scéně. Délky scén (s, násobky taktu 2,4 s) jako argumenty: python3 music_hasici.py 4.8 9.6 ...
import sys
import numpy as np, wave
SR=44100
DUR=[float(x) for x in sys.argv[1:]] or [14.4,9.6,7.2,7.2,9.6,9.6]
B=[0.0]
for d in DUR: B.append(round(B[-1]+d,3))
TOTAL=B[-1]
def n(m): return 440*2**((m-69)/12)
# akordy (MIDI) – G dur: úvod Em, přehled C, pokrytí G, detail D, protokol Em, hodnota C, hasiči D→Dsus4, závěr G
# úvod Em, nejbližší C, karta G, celá karta D, navigace Em, foto C, … závěr vždy G
POOL=[[52,59,64,67,71],[48,55,60,64,67],[43,55,59,62,67],[50,57,62,66,69],[52,59,64,67,71],[48,55,60,64,67],[50,57,62,66,69]]
CH=[POOL[i%len(POOL)] for i in range(len(DUR)-1)]+[[43,55,59,62,67]]
t=np.arange(int(TOTAL*SR))/SR
L=np.zeros_like(t); R=np.zeros_like(t)
def seg_env(i,xf=0.9):
    a,b=B[i],B[i+1]
    e=np.clip((t-(a-xf/2))/xf,0,1)*np.clip(((b+xf/2)-t)/xf,0,1)
    if i==0: e=np.clip(t/1.0,0,1)*np.clip(((b+xf/2)-t)/xf,0,1)
    if i==len(B)-2: e=np.clip((t-(a-xf/2))/xf,0,1)
    return np.sin(e*np.pi/2)**2
# podkres (pad): tóny akordu, mírně rozladěné, pomalé vlnění
for i,ch in enumerate(CH):
    e=seg_env(i)
    m=e>0
    for k,mm in enumerate(ch[1:]):
        f=n(mm)
        for det,pan in ((-0.12,0.3),(0.12,0.7)):
            ph=2*np.pi*(f+det)*t[m]
            s=(np.sin(ph)+0.25*np.sin(2*ph)+0.08*np.sin(3*ph))*(0.6+0.4*np.sin(2*np.pi*0.11*t[m]+k))
            L[m]+=0.028*e[m]*s*(1-pan)*2; R[m]+=0.028*e[m]*s*pan*2
# arpeggio: krok 0,3 s, fáze 0,09 s jako originál; vzor po 8 krocích (takt 2,4 s)
PAT=[0,2,4,2,1,3,4,3]
def chord_at(x):
    for i in range(len(B)-1):
        if B[i]<=x<B[i+1]: return i
    return len(B)-2
step=0.3; t0=0.09
DROP=9.6   # v úvodu hraje jen podkres a údery; arpeggio a basa nastoupí s logem („drop“)
k=0
while True:
    ts=t0+k*step
    if ts>TOTAL-2.2: break
    if ts<DROP: k+=1; continue
    i=chord_at(ts); ch=CH[i]
    mm=ch[PAT[k%8]]+12
    if i==len(CH)-1 and ts>B[-2]+4.8: break   # v závěru arpeggio doznívá
    f=n(mm); dur=1.1; a=int(ts*SR); b=min(len(t),a+int(dur*SR)); tt=t[a:b]-ts
    env=(1-np.exp(-tt/0.006))*np.exp(-tt/0.32)
    s=(np.sin(2*np.pi*f*tt)+0.35*np.sin(4*np.pi*f*tt)*np.exp(-tt/0.12)+0.12*np.sin(6*np.pi*f*tt)*np.exp(-tt/0.06))*env
    acc=1.0 if k%8==0 else (0.8 if k%2==0 else 0.62)
    pan=0.35+0.3*((k%4)/3)
    L[a:b]+=0.085*acc*s*(1-pan)*2; R[a:b]+=0.085*acc*s*pan*2
    k+=1
# basa na každou půlku taktu (1,2 s)
k=0
while True:
    ts=t0+k*1.2
    if ts>TOTAL-2.5: break
    if ts<DROP: k+=1; continue
    i=chord_at(ts); f=n(CH[i][0]-12 if CH[i][0]>45 else CH[i][0])
    a=int(ts*SR); b=min(len(t),a+int(1.4*SR)); tt=t[a:b]-ts
    env=(1-np.exp(-tt/0.01))*np.exp(-tt/0.55)
    s=(np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt))*env*(1.0 if k%2==0 else 0.7)
    L[a:b]+=0.11*s; R[a:b]+=0.11*s
    k+=1
# úvod: údery na dopad slov, tikání v panice, ztišení („Neboj…“), náběh šumu a velký náraz s logem (9,6 s)
rng=np.random.default_rng(7)
def hit(at,g,big=False):
    a=int(at*SR); d=1.6 if big else 0.7; b=min(len(t),a+int(d*SR)); tt=t[a:b]-at
    f=38+90*np.exp(-tt/0.05)                       # „boom“ – klesající sinus
    ph=2*np.pi*np.cumsum(f)/SR
    boom=np.sin(ph)*np.exp(-tt/(0.45 if big else 0.22))
    nz=rng.standard_normal(len(tt)); nz=np.convolve(nz,np.ones(6)/6,'same')
    snap=nz*np.exp(-tt/(0.5 if big else 0.06))*(0.5 if big else 0.8)
    x=g*(1.0*boom+0.35*snap)
    L[a:b]+=x; R[a:b]+=x
for at,g in ((0.6,.30),(1.8,.36),(3.0,.30),(4.2,.26),(5.7,.26)): hit(at,g)
hit(DROP,.52,True)
for k2 in range(2,24):                                             # tikání po dobách (0,6–7,2 s) – spěch
    at=k2*0.3; a=int(at*SR); b=a+int(0.05*SR); tt=t[a:b]-at
    c=rng.standard_normal(b-a); c=c-np.convolve(c,np.ones(4)/4,'same')
    x=0.05*c*np.exp(-tt/0.012)*(1.3 if k2%2==0 else 0.8); L[a:b]+=x; R[a:b]+=x
a=int((DROP-0.65)*SR); b=int(DROP*SR); tt=t[a:b]-(DROP-0.65)         # náběh (riser) před logem
nz=rng.standard_normal(b-a); nz=nz-np.convolve(nz,np.ones(30)/30,'same')
L[a:b]+=0.10*nz*(tt/0.65)**2; R[a:b]+=0.10*nz*(tt/0.65)**2
# závěrečný akord (G) s delším dozvukem
a=int(B[-2]*SR); tt=t[a:]-B[-2]
for mm in [55,59,62,67,71,74]:
    s=np.sin(2*np.pi*n(mm)*tt)*(1-np.exp(-tt/0.02))*np.exp(-tt/3.0)
    L[a:]+=0.05*s; R[a:]+=0.05*s
# jednoduchý dozvuk (zpožděné kopie) + stereo
def rev(x):
    y=x.copy()
    for d,g in ((0.137,0.28),(0.211,0.22),(0.293,0.17),(0.419,0.12),(0.577,0.08)):
        s=int(d*SR); y[s:]+=g*x[:-s]
    return y
L,R=rev(L),rev(R[::1])
# celková obálka: náběh 0,8 s, dozvuk 3 s
g=np.clip(t/0.8,0,1)*np.clip((TOTAL-t)/3.0,0,1)
L*=g; R*=g
mx=max(np.abs(L).max(),np.abs(R).max()); L=L/mx*0.85; R=R/mx*0.85
out=(np.stack([L,R],1)*32767).astype(np.int16)
w=wave.open('music_hasici.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
print('ok',TOTAL)
