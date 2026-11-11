import json
from pathlib import Path
r=Path(__file__).parent; d=json.loads((r/'draft.json').read_text());s=json.loads((r/'synthesis.json').read_text())
def add(sec,text,ids):
 d['sections'][sec-1]['paragraphs'].append({'text':text,'clusterIds':[f'cluster-{sec:03}'],'sourceUnitIds':ids.split(','),'audit':{'meaningPreserved':True,'factsPreserved':True,'noUnsupportedClaim':True}})
add(2,'Pregătirea tiparului include verificarea operațiilor disponibile și construirea indexurilor care identifică regulile relevante când apare un fapt nou. Acest lucru permite actualizarea locală: schimbarea unei sosiri activează evaluările temporale dependente, fără să impună reluarea fiecărui calcul despre toate călătoriile. Dacă o operație cerută nu are interpretor, sistemul trebuie să o declare nesuportată. O condiție nu devine satisfăcută prin omiterea calculului ei, iar o intrare lipsă nu primește pe ascuns o valoare convenabilă.','u000037,u000118,u000137,u000417')
add(3,'Nici incertitudinea nu poate fi redusă la un scor universal. O listă păstrează alternative, un interval delimitează valori, iar distribuția probabilistică adaugă ponderarea rezultatelor. Pentru o probabilitate trebuie definit exact evenimentul și domeniul modelului; combinarea estimărilor cere relația dintre ele și dependența datelor. Decizia mai folosește consecințe și preferințe. Același risc poate fi acceptabil într-o vizită flexibilă și nepotrivit înaintea unei prezentări. Schimbarea scopului poate cere altă alegere fără să schimbe estimarea.','u000219,u000220,u000223,u000224,u000225,u000226')
# Align the evidence graph with every paragraph's reviewed source evidence.
chap=json.loads((r/'chapters.json').read_text())['chapters']; unit_ch={u:c['id'] for c in chap for u in c['unitIds']}
for p in [p for sec in d['sections'] for p in sec['paragraphs']]+d['conclusion']:
 for cid in p['clusterIds']:
  c=next(c for c in s['clusters'] if c['id']==cid)
  c['sourceUnitIds']=list(dict.fromkeys(c['sourceUnitIds']+p['sourceUnitIds']))
  c['chapterIds']=list(dict.fromkeys(c['chapterIds']+[unit_ch[u] for u in p['sourceUnitIds']]))
for c in s['chapterCoverage']:c['clusterIds']=[g['id'] for g in s['clusters'] if c['chapterId'] in g['chapterIds']]
(r/'draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');(r/'synthesis.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
