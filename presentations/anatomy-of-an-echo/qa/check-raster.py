from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).parent;rows=[]
for f in sorted((p/'supported-screenshots').glob('*.png')):
 im=Image.open(f).convert('RGB');night=f.name.startswith('night');head=im.crop((80,35,970,110));art=im.crop((80,150,1130,570));ctrl=im.crop((65,616,1135,705));ink=sum(n for n,c in head.getcolors(head.width*head.height) if (min(c)>170 if night else max(c)<110));sat=lambda z:sum(n for n,c in z.getcolors(z.width*z.height)if max(c)-min(c)>35);a=sat(art);b=sat(ctrl);rows.append({'file':f.name,'titleInk':ink,'artColor':a,'controlColor':b,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pass':ink>700 and a>3000 and b>400})
assert len(rows)==36 and all(r['pass']for r in rows),[r for r in rows if not r['pass']]
(p/'raster-completeness-review.json').write_text(json.dumps({'pass':True,'scope':'Actual raw screenshot title contrast and non-background art/control palette presence; not a proof of artistic quality or every object visibility.','frames':rows},indent=2)+'\n');print('36 actual raw captures contain title, colored art and controls')
