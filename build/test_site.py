import pathlib, sys, time
from playwright.sync_api import sync_playwright
url=pathlib.Path(r'C:/Users/sugi/Desktop/中良工業介紹影片/index.html').as_uri()+(sys.argv[4] if len(sys.argv)>4 else '')
W,H=(int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (1440,900)
tag=sys.argv[3] if len(sys.argv)>3 else 'd'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H})
    errs=[]; pg.on('console',lambda m: errs.append(f'{m.type}: {m.text}') if m.type in('error','warning') else None); pg.on('pageerror',lambda e: errs.append('PAGEERR '+str(e)))
    pg.goto(url); pg.wait_for_timeout(2500)
    pg.mouse.move(W*.7,H*.4); pg.wait_for_timeout(100); pg.mouse.move(W*.75,H*.45); pg.wait_for_timeout(600)
    pg.screenshot(path=f'site_{tag}_0hero.png')
    def go(sel,off=0,wait=900,name=None):
        pg.evaluate(f"(()=>{{const e=document.querySelector('{sel}'); window.scrollTo(0, e.getBoundingClientRect().top+scrollY+{off});}})()")
        pg.wait_for_timeout(wait); pg.screenshot(path=f'site_{tag}_{name}.png')
    go('#film',0,900,'1film')
    th=pg.evaluate("document.querySelector('#craftTall').offsetHeight - innerHeight")
    for k,f in enumerate([0.12,0.38,0.62,0.97]):
        go('#craftTall',int(th*f),900,f'2craft{k}')
    go('#layers',0,1200,'3layers')
    go('#physics',0,600,'4phys_a')
    # press foam
    box=pg.evaluate("(()=>{const r=document.querySelector('#phyC').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
    pg.mouse.move(box[0]+box[2]*.5, box[1]+60); pg.mouse.down(); pg.mouse.move(box[0]+box[2]*.5, box[1]+box[3]*.55, steps=8); pg.wait_for_timeout(500)
    pg.screenshot(path=f'site_{tag}_4phys_b.png'); pg.mouse.up(); pg.wait_for_timeout(1200); pg.screenshot(path=f'site_{tag}_4phys_c.png')
    pg.click('#phyMode button[data-m=rain]'); pg.click('#phyCell button[data-c=open]'); pg.wait_for_timeout(3500); pg.screenshot(path=f'site_{tag}_4phys_d.png')
    go('#footprint',0,1200,'5map')
    go('#esg',0,1200,'6esg')
    go('#esg',700,1200,'6esg2')
    go('#contact',0,1000,'7contact')
    print('\n'.join(errs[:30]) or 'no console errors')
    print('doc height',pg.evaluate('document.documentElement.scrollHeight'),'overflowX',pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
    b.close()
