from PIL import Image
from pathlib import Path
import json,hashlib,math,time
p=Path(__file__).parent;d=p/('raw-proof-'+str(time.time_ns()));d.mkdir();geo=json.loads((p/'raster-geometry.json').read_text());result=[]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for group in ['rows','feet']:
 for row in geo[group]:
  raw=p/'supported-screenshots'/row['file'];im=Image.open(raw).convert('RGB');targets=[]
  for target in row['targets']:
   if target.get('opacity',1)<.95:continue
   r=target['rect'];box=(math.floor(r['x'])-2,math.floor(r['y'])-2,math.ceil(r['x']+r['width'])+2,math.ceil(r['y']+r['height'])+2);crop=im.crop(box);color=tuple(bytes.fromhex(target['color'][1:]));count=sum(n for n,c in crop.getcolors(crop.width*crop.height)if c==color);f=d/(raw.stem+'-'+target['id']+'.png');crop.save(f);targets.append({'id':target['id'],'box':box,'color':target['color'],'exactPigmentPixels':count,'crop':str(f),'cropSha256':sha(f),'pass':count>(12 if group=='feet' else 20)})
  result.append({'kind':group,'raw':str(raw),'rawSha256':sha(raw),'targets':targets})
pass_all=all(t['pass']for r in result for t in r['targets']);out={'pass':pass_all,'scope':'Pixels counted in original actual full-resolution captures; only actor geometry was reread. Visible stones/labels, all six jar silhouettes and Night lower bodies have positive expected paint. Hidden later stones are not falsely asserted visible.','audiblePlayback':False,'rows':result};(d/'pixel-evidence.json').write_text(json.dumps(out,indent=2)+'\n');(p/'latest-raw-proof.json').write_text(json.dumps({'directory':str(d),'pass':pass_all},indent=2)+'\n');print(d);print('pass',pass_all)
if not pass_all:print([t for r in result for t in r['targets']if not t['pass']]);raise SystemExit(1)
