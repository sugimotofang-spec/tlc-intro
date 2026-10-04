"""Render single frames of film45.html: python shot45.py <outdir> <ver:pub|int> <lang:zh|en> t1,t2,..."""
import sys, pathlib
from playwright.sync_api import sync_playwright
out, ver, lang, ts = sys.argv[1], sys.argv[2], sys.argv[3], [float(x) for x in sys.argv[4].split(',')]
pathlib.Path(out).mkdir(parents=True, exist_ok=True)
url = pathlib.Path('film45_int.html' if ver == 'int' else 'film45.html').resolve().as_uri() + '?render=1' + ('&ver=int' if ver == 'int' else '') + ('&lang=en' if lang == 'en' else '')
with sync_playwright() as p:
    b = p.chromium.launch(args=['--force-color-profile=srgb'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(url); pg.evaluate('window.__ready')
    for t in ts:
        pg.evaluate(f'window.__render({t})'); f = f'{out}/{ver}_{lang}_{t:05.2f}.png'; pg.screenshot(path=f); print(f)
    print('errors:', errs[:5]); b.close()
