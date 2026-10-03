import sys, pathlib, time
from playwright.sync_api import sync_playwright
from PIL import Image
times=[float(x) for x in sys.argv[1].split(',')]; out=sys.argv[2] if len(sys.argv)>2 else 'sheet.png'
cols=int(sys.argv[3]) if len(sys.argv)>3 else 3
url=pathlib.Path('film.html').resolve().as_uri()+'?render=1'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--force-color-profile=srgb'])
    pg=b.new_page(viewport={'width':1920,'height':1080})
    msgs=[]; pg.on('console',lambda m: msgs.append(m.text)); pg.on('pageerror',lambda e: msgs.append('ERR '+str(e)))
    pg.goto(url); pg.evaluate('window.__ready')
    imgs=[]
    for t in times:
        t0=time.time(); pg.evaluate(f'window.__render({t})'); pg.screenshot(path=f'pv_{t:05.2f}.png'); imgs.append(Image.open(f'pv_{t:05.2f}.png').convert('RGB'))
    print('last frame ms',int((time.time()-t0)*1000)); print('\n'.join(msgs[:20]))
    b.close()
w,h=640,360; rows=(len(imgs)+cols-1)//cols
sheet=Image.new('RGB',(w*cols,h*rows),(30,30,30))
for i,im in enumerate(imgs): sheet.paste(im.resize((w,h)),((i%cols)*w,(i//cols)*h))
sheet.save(out)
