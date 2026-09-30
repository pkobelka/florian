# Sestaví promo/florian-hasici.html ze šablony hasici_src.html + assets/ (+ volitelně html_audio.mp3)
import base64, os, re, sys
S=os.path.dirname(os.path.abspath(__file__)); A=S+'/assets/'
def uri(f,mime=None):
    mime=mime or {'jpg':'image/jpeg','png':'image/png','mp3':'audio/mpeg'}[f.rsplit('.',1)[1]]
    return 'data:%s;base64,%s'%(mime,base64.b64encode(open(f,'rb').read()).decode())
h=open(S+'/hasici_src.html').read()
have=lambda n: os.path.exists(A+n)
if have('t4.jpg') and have('t5.jpg'):
    nav='''<div class="tablet"><div class="screen">
      <div class="cam" data-k="0,.5,.5,1; 1.2,.42,.6,1.55; 4.4,.42,.6,1.6"><img src="__IMG_t5__" alt="Vést sem – čára k hydrantu"></div>
      <div class="cam fd" data-in="4.6" data-k="0,.5,.5,1.25; 9.6,.45,.55,1.45"><img src="__IMG_t4__" alt="Trasa k hydrantu v Mapy.com"></div>
    </div></div>
    <div class="copy">
      <div class="kick rv" data-in="0.1">Vést sem</div>
      <h1 class="head rv" data-in="0.25">Navigace<br><span class="red">až k hydrantu.</span></h1>
      <div class="chips">
        <span class="chip r pop" data-in="1.6">158 m · šipka na mapě</span>
        <span class="chip b pop" data-in="5.2">Mapy.com · Google</span>
        <span class="chip g pop" data-in="6.0">19 s · 191 m</span>
      </div>
    </div>'''
else:
    nav='''<div class="phone rv" data-in="0"><div class="scr">
      <img src="__IMG_n1__" alt="Trasa k hydrantu">
      <img class="fd" data-in="4.8" src="__IMG_n2__" alt="Navigace k hydrantu">
      <div class="tap" data-in="3.4" style="left:74%;top:94.5%"></div>
    </div></div>
    <div class="copy" style="width:700px">
      <div class="kick rv" data-in="0.1">Vést sem</div>
      <h1 class="head rv" data-in="0.25">Navigace<br><span class="red">až k hydrantu.</span></h1>
      <p class="sub rv" data-in="0.6">Jedním ťuknutím do Mapy.com nebo Google – trasa, čas i odbočky.</p>
      <div class="chips">
        <span class="chip b pop" data-in="1.8">Mapy.com · Google</span>
        <span class="chip g pop" data-in="5.4">2 min · 800 m</span>
      </div>
    </div>'''
h=h.replace('__NAV__',nav)
foto=''
if have('t6.jpg'):
    foto='''<section class="scene" data-d="7.2">
    <div class="tablet"><div class="screen"><div class="cam" data-k="0,.5,.5,1; 1.4,.43,.55,1.7; 7.2,.43,.56,1.85"><img src="__IMG_t6__" alt="Fotky hydrantů na satelitní mapě"></div>
      <div class="tap" data-in="0.6" style="left:94.8%;top:9.5%"></div></div></div>
    <div class="copy">
      <div class="kick rv" data-in="0.1">Satelit + foto</div>
      <h1 class="head rv" data-in="0.25">Poznáte ho<br><span class="red">i v noci.</span></h1>
      <p class="sub rv" data-in="0.6">Fotky hydrantů přímo na satelitní mapě – víte, co hledáte, ještě než vystoupíte.</p>
    </div>
  </section>'''
h=h.replace('__FOTO__',foto)
imgs={'hydrant':'hydrant.jpg','logo':'a10.png','vhos':'a12.jpg','t1':'t1.jpg','t2':'t2.jpg','t3':'t3.jpg',
      'sv':'florian_sv.png','t4':'t4.jpg','t5':'t5.jpg','t6':'t6.jpg','n1':'a08.jpg','n2':'a09.jpg'}
for k,f in imgs.items():
    if '__IMG_%s__'%k in h: h=h.replace('__IMG_%s__'%k, uri(A+f))
durs=[float(x) for x in re.findall(r'class="scene[^"]*" data-d="([\d.]+)"',h)]
h=h.replace('__LEN__',str(round(sum(durs))))
h=h.replace('__AUDIO__', uri(S+'/html_audio.mp3') if os.path.exists(S+'/html_audio.mp3') else '')
open('/home/user/florian/promo/florian-hasici.html','w').write(h)
open(S+'/durs.txt','w').write(' '.join(str(d) for d in durs))
print('ok', durs, sum(durs), len(h)//1024,'kB')
