const topo=require('topojson-client'), d3=require('d3-geo'), fs=require('fs');
const w=JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json'));
const countries=topo.feature(w,w.objects.countries).features;
const want={158:'TW',156:'CN',704:'VN',360:'ID'};
const step=0.42, out=[];
const lon0=86,lon1=146,lat0=-12,lat1=44;
// bbox prefilter
const feats=countries.map(f=>({f,b:d3.geoBounds(f),id:+f.id}));
for(let lat=lat1;lat>=lat0;lat-=step){
  const off=(Math.round((lat1-lat)/step)%2)*step/2; // hex offset
  for(let lon=lon0+off;lon<=lon1;lon+=step){
    for(const {f,b,id} of feats){
      if(b[0][0]<=b[1][0]){ if(lon<b[0][0]||lon>b[1][0]) continue; }
      if(lat<b[0][1]||lat>b[1][1]) continue;
      if(d3.geoContains(f,[lon,lat])){ out.push([+lon.toFixed(2),+lat.toFixed(2),({158:1,156:2,704:3,360:4})[id]||0]); break; }
    }
  }
}
// small islands: ensure Taiwan has decent dots
fs.writeFileSync('mapdots.json',JSON.stringify(out));
const c=[0,0,0,0,0]; out.forEach(p=>c[p[2]]++);
console.log(out.length,'dots; TW',c[1],'CN',c[2],'VN',c[3],'ID',c[4]);
