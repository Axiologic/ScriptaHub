import json
from pathlib import Path
p=Path(__file__).parent/'chunks/0004.json';d=json.loads(p.read_text())
for seg in d['segments']:
 if seg['id']=='t000034':
  seg['translation']='''Dexter urmărește viața lui Dexter Morgan, care ziua este analist criminalist specializat în urmele de sânge pentru poliția din Miami, iar noaptea devine un ucigaș în serie ce se vede drept justițiar. Dexter își canalizează impulsurile întunecate spre un simț deformat al dreptății, vizând infractori care au scăpat de lege. Îndrumat de un cod strict insuflat de tatăl său adoptiv, își alege cu grijă victimele, convins că merită pedeapsa fatală. Ducând o viață dublă, el trebuie să fie mai isteț decât colegii și decât infractorii pe care îi urmărește, în timp ce se luptă cu propriii demoni. Dexter este un thriller psihologic tulburător despre moralitate, dreptate și capacitatea omului de a face rău.'''
 elif seg['id']=='t000035':seg['translation']='Alte sugestii'
 else:seg['translation']=seg['source']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('translated/preserved',len(d['segments']))
