import sys, pathlib
from playwright.sync_api import sync_playwright
html=sys.argv[1]; out=sys.argv[2]; w=int(sys.argv[3]) if len(sys.argv)>3 else 1200; h=int(sys.argv[4]) if len(sys.argv)>4 else 800
wait=int(sys.argv[5]) if len(sys.argv)>5 else 500
url=html if html.startswith(('http','file')) else pathlib.Path(html).resolve().as_uri()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':h})
    pg.goto(url); pg.wait_for_timeout(wait)
    pg.screenshot(path=out, full_page=('--full' in sys.argv)); b.close()
