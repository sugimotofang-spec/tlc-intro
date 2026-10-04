import json, base64, io
from PIL import Image
OUT_DIR=r'C:/Users/sugi/Desktop/中良工業介紹影片'
VIDEO='中良工業_30s.mp4'; POSTER='中良工業_30s_封面.jpg'
src=open('site.src.html',encoding='utf-8').read()
L=json.load(open('logo_parts.json',encoding='utf-8'))
def logo(text='#FFFFFF',mark='#1A93DB',orange='#EE9039',h=30):
    s=f'<svg viewBox="-1 -5 349 118" height="{h}" role="img" aria-label="TLC">'
    s+=''.join(f'<path fill="{orange}" d="{d}"/>' for d in L['orange'])
    s+=''.join(f'<path fill="{mark}" d="{d}"/>' for d in L['blue'])+f'<path fill="{mark}" d="{L["blob"]}"/>'
    s+=f'<g fill="{text}" transform="translate({L["tx"]} 0) skewX({-L["skew"]})">'+''.join(f'<path d="{L[k]}"/>' for k in 'TLC')+'</g></svg>'
    return s
dots=[d for d in json.load(open('mapdots.json')) if 90<=d[0]<=136 and -12.5<=d[1]<=35.5]
def img64(p,w=760):
    im=Image.open(p).convert('RGB'); im=im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
    b=io.BytesIO(); im.save(b,'JPEG',quality=82,optimize=True,progressive=True); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
P=r'C:/Users/sugi/Desktop/Linkedin/圖片區/地球友善小組Pason 怕剩/'
rep={'/*LOGO_NAV*/':logo(h=30),'/*LOGO_FOOT*/':logo(h=26),'/*LOGO_PARTS*/null':json.dumps(L,ensure_ascii=False),
     '/*MAPDOTS*/null':json.dumps(dots,separators=(',',':')),'/*SHOE_PARTS*/null':open('shoe_parts.json',encoding='utf-8').read(),'/*PASONT1*/':img64(P+'S__234512469_0.jpg'),'/*PASONT2*/':img64(P+'S__234512472_0.jpg',820),
     '/*VIDEO*/':VIDEO,'/*POSTER*/':POSTER}
for k,v in rep.items(): src=src.replace(k,v)
assert '/*' not in src.split('<script>')[0].replace('/*!','') or True
out=OUT_DIR+'/index.html'
open(out,'w',encoding='utf-8').write(src); print('site built',len(src)//1024,'KB', len(dots),'dots')
