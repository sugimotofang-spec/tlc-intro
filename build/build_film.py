import json
src=open('film.src.html',encoding='utf-8').read()
parts=open('logo_parts.json',encoding='utf-8').read()
dots=json.load(open('mapdots.json'))
src=src.replace('/*LOGO_PARTS*/null',parts).replace('/*MAPDOTS*/null',json.dumps(dots,separators=(',',':')))
open('film.html','w',encoding='utf-8').write(src); print('built',len(src))
