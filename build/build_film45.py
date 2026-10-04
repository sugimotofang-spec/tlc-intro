"""Build the 45s film pages from film45.src.html.
    python build_film45.py         -> film45.html      (public edition; safe to commit)
    python build_film45.py --int   -> film45_int.html  (adds internal_data.json; git-ignored, never publish)"""
import json, sys
INTERNAL = '--int' in sys.argv
src = open('film45.src.html', encoding='utf-8').read()
parts = open('logo_parts.json', encoding='utf-8').read()
dots = json.load(open('mapdots.json'))
shoe = open('shoe_parts.json', encoding='utf-8').read()
intd = json.dumps(json.load(open('internal_data.json', encoding='utf-8')), ensure_ascii=False) if INTERNAL else 'null'
for k, v in (('/*LOGO_PARTS*/null', parts), ('/*MAPDOTS*/null', json.dumps(dots, separators=(',', ':'))),
             ('/*SHOE_PARTS*/null', shoe), ('/*INTERNAL_DATA*/null', intd)):
    assert k in src, k
    src = src.replace(k, v)
out = 'film45_int.html' if INTERNAL else 'film45.html'
open(out, 'w', encoding='utf-8').write(src)
print('built', out, len(src))
