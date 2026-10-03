import sys, os, pathlib, time
from multiprocessing import Process
FPS=60; DUR=30; NF=FPS*DUR; W=6
def work(k):
    from playwright.sync_api import sync_playwright
    url=pathlib.Path('film.html').resolve().as_uri()+'?render=1'
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--force-color-profile=srgb'])
        pg=b.new_page(viewport={'width':1920,'height':1080})
        pg.goto(url); pg.evaluate('window.__ready')
        for f in range(k,NF,W):
            out=f'frames/f{f:05d}.png'
            if os.path.exists(out): continue
            pg.evaluate(f'window.__render({f/FPS})')
            pg.screenshot(path=out+'.tmp.png'); os.replace(out+'.tmp.png',out)
        b.close()
if __name__=='__main__':
    os.makedirs('frames',exist_ok=True); t0=time.time()
    ps=[Process(target=work,args=(k,)) for k in range(W)]
    [p.start() for p in ps]; [p.join() for p in ps]
    n=len([x for x in os.listdir('frames') if x.endswith('.png') and not x.endswith('.tmp.png')])
    print('frames',n,'secs',int(time.time()-t0))
