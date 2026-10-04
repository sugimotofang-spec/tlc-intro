"""Render film45.html to PNG frames at 60 fps (6 parallel browsers).
    python render45.py [--int] [--en]     -> frames45_<pub|int>_<zh|en>/
Then blend pairs of frames to 30 fps with motion blur in ffmpeg (see README)."""
import sys, os, pathlib, time
from multiprocessing import Process
VER = 'int' if '--int' in sys.argv else 'pub'
LANG = 'en' if '--en' in sys.argv else 'zh'
OUT = f'frames45_{VER}_{LANG}'
FPS = 60; DUR = 45; NF = FPS*DUR; W = 6
def work(k):
    from playwright.sync_api import sync_playwright
    url = pathlib.Path('film45_int.html' if VER == 'int' else 'film45.html').resolve().as_uri() + '?render=1' + ('&ver=int' if VER == 'int' else '') + ('&lang=en' if LANG == 'en' else '')
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--force-color-profile=srgb'])
        pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        pg.goto(url); pg.evaluate('window.__ready')
        for f in range(k, NF, W):
            out = f'{OUT}/f{f:05d}.png'
            if os.path.exists(out): continue
            pg.evaluate(f'window.__render({f/FPS})')
            pg.screenshot(path=out+'.tmp.png'); os.replace(out+'.tmp.png', out)
        b.close()
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True); t0 = time.time()
    ps = [Process(target=work, args=(k,)) for k in range(W)]
    [p.start() for p in ps]; [p.join() for p in ps]
    n = len([x for x in os.listdir(OUT) if x.endswith('.png') and not x.endswith('.tmp.png')])
    print(OUT, 'frames', n, 'secs', int(time.time()-t0))
