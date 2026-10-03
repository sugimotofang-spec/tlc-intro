import math, json
R2=math.sqrt(2)
def st(s,t): return ((s+t)/R2,(s-t)/R2)
def rpoly(pts,r):
    """rounded polygon path; r scalar or list"""
    n=len(pts); rs=r if isinstance(r,list) else [r]*n; d=[]
    for i in range(n):
        p0=pts[i-1]; p1=pts[i]; p2=pts[(i+1)%n]; rr=rs[i]
        def mv(a,b,dist):
            L=math.hypot(b[0]-a[0],b[1]-a[1]) or 1; dist=min(dist,L/2); return (a[0]+(b[0]-a[0])*dist/L, a[1]+(b[1]-a[1])*dist/L)
        a=mv(p1,p0,rr); b=mv(p1,p2,rr)
        d.append(('M' if i==0 else 'L')+'%.2f %.2f'%a)
        d.append('Q%.2f %.2f %.2f %.2f'%(p1[0],p1[1],b[0],b[1]))
    return ''.join(d)+'Z'
def band(s0,s1,t0a,t0b,t1a,t1b,r=1.6):
    # t0a/t0b: low end at s0/s1 ; t1a/t1b: high end at s0/s1
    return rpoly([st(s0,t0a),st(s1,t0b),st(s1,t1b),st(s0,t1a)],r)
blue=[]; orange=[]
blue.append(band(24.3,32.2,-28.3,-28.3,30.2,30.2))
blue.append(band(37.8,47.1,-25.7,-25.7,31.2,31.2))
blue.append(band(51.2,67.2,-22.7,-14.8,32.6,41.4,[1.6,1.6,1.4,1.8]))
orange.append(band(72.6,81.0,-18.9,-27.3,30,30,[3,3,0,0]))
orange.append(band(86.6,97.4,-33.7,-33.7,26,26,[3.5,1.8,0,0]))
orange.append(band(105.0,123.4,-37.7,-37.7,13.7,13.7,[3,3,3,3]))
# blob (xy)
def cr(pts,closed=False):
    P=[st(*p) for p in pts]; d=''
    for i in range(len(P)-1):
        p0=P[i-1] if i>0 else P[i]; p1=P[i]; p2=P[i+1]; p3=P[i+2] if i+2<len(P) else P[i+1]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6); c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        d+='C%.2f %.2f %.2f %.2f %.2f %.2f'%(c1+c2+p2)
    return d
P0=st(72.6,28.6)
dome=[(72.6,37.5),(73.6,41.6),(76,45.3),(80,48.1),(84,50.6),(88,52.6),(93,54.5),(99,55.8),(103.5,55.9),(106.6,54.6),(108.6,51.6)]
left=[(108.6,16.0),(107.4,14.6),(105.9,14.9),(97.2,16.8),(89.2,18.7),(81.3,23.4),(73.6,27.6),(72.6,28.6)]
blob='M%.2f %.2f'%P0+'L%.2f %.2f'%st(72.6,37.5)+cr(dome)+'L%.2f %.2f'%st(108.6,16.0)+cr(left)+'Z'
# letters (upright coords; skew applied later)
T=rpoly([(125.6,25.5),(199.6,25.5),(199.6,42.5),(171.3,42.5),(171.3,103.5),(153.3,103.5),(153.3,42.5),(125.6,42.5)],[2,2,2,1,2,2,1,2])
L=('M216 25.5 L230.3 25.5 Q232.3 25.5 232.3 27.5 L232.3 84.5 Q232.3 87.5 235.3 87.5 L276.8 87.5 Q278.8 87.5 278.8 89.5 '
   'L278.8 101.5 Q278.8 103.5 276.8 103.5 L232 103.5 C226.6 103.5 214 96.4 214 85.5 L214 27.5 Q214 25.5 216 25.5 Z')
C=('M343.4 25.5 Q345.4 25.5 345.4 27.5 L345.4 40.5 Q345.4 42.5 343.4 42.5 L318.75 42.5 C312.35 42.5 302.75 52.1 302.75 58.5 '
   'L302.75 71.5 C302.75 77.9 312.35 87.5 318.75 87.5 L343.4 87.5 Q345.4 87.5 345.4 89.5 L345.4 102.8 Q345.4 104.8 343.4 104.8 '
   'L314 104.8 C297.5 104.8 284 91.3 284 74.8 L284 55.5 C284 39 297.5 25.5 314 25.5 Z')
k=0.071; sk=math.degrees(math.atan(k))
letters='<g transform="translate(%.3f 0) skewX(%.3f)">'%(k*103.5,-sk)
json.dump({'blue':blue,'orange':orange,'blob':blob,'T':T,'L':L,'C':C,'skew':sk,'tx':k*103.5},open('logo_parts.json','w'))
def svg(bluefill='#007DC2',orangefill='#EE9039',textfill=None,vb='-1 -5 349 118'):
    textfill=textfill or bluefill
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
      f'<g fill="{orangefill}">'+''.join(f'<path d="{p}"/>' for p in orange)+'</g>'
      f'<g fill="{bluefill}">'+''.join(f'<path d="{p}"/>' for p in blue)+f'<path d="{blob}"/></g>'
      f'<g fill="{textfill}" transform="translate({k*103.5:.3f} 0) skewX({-sk:.3f})"><path d="{T}"/><path d="{L}"/><path d="{C}"/></g></svg>')
open('tlc_logo.svg','w').write(svg())
open('tlc_logo_white.svg','w').write(svg(bluefill='#ffffff'))
open('overlay.html','w').write(f'''<html><body style="margin:0;background:#fff">
<div style="position:relative;width:2262px;height:750px">
<img src="file:///C:/Users/sugi/Desktop/Linkedin/TLC LOGO.jpg" style="position:absolute;left:0;top:0;width:2262px;height:750px;image-rendering:pixelated;opacity:1">
<svg style="position:absolute;left:0;top:0" width="2262" height="750" viewBox="0 0 377 125">
<g fill="none" stroke="#ff00aa" stroke-width="0.25">'''+''.join(f'<path d="{p}"/>' for p in orange+blue+[blob])+f'''</g>
<g fill="none" stroke="#ff00aa" stroke-width="0.25" transform="translate({k*103.5:.3f} 0) skewX({-sk:.3f})"><path d="{T}"/><path d="{L}"/><path d="{C}"/></g></svg></div></body></html>''')
print('ok')
