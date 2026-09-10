import json,re,hashlib
from pathlib import Path
f=Path('.book-work/catalogue-descriptions-20260910');p=f/'descriptions-1.json';a=json.loads(p.read_text());rp=f/'review-1.json';report=json.loads(rp.read_text())
changes={
'en': 'Even exact computation can answer the wrong question after a misinterpretation.',
'fr': 'Même un calcul exact peut répondre à la mauvaise question après une erreur d’interprétation.',
'de': 'Selbst exakte Berechnung kann nach einer Fehlinterpretation die falsche Frage beantworten.',
'es': 'Incluso un cálculo exacto puede responder a la pregunta equivocada tras una mala interpretación.',
'pt': 'Mesmo um cálculo exato pode responder à pergunta errada após uma interpretação incorreta.',
'it': 'Anche un calcolo esatto può rispondere alla domanda sbagliata dopo un’interpretazione errata.',
'ro': 'Chiar și un calcul exact poate răspunde întrebării greșite după o interpretare eronată.',
'pl': 'Nawet dokładne obliczenie może odpowiadać na niewłaściwe pytanie po błędnej interpretacji.'}
for l,t in changes.items():
 parts=re.split(r'(?<=[.!?])\s+',a[27]['shortDescription'][l]);old=parts[3];parts[3]=t;a[27]['shortDescription'][l]=' '.join(parts)
 assert len(parts)==6 and all(len(s.split())<=22 for s in parts)
 report['issues'].append(dict(id=a[27]['id'],language=l,sentence=4,finding='State exact-computation/wrong-question problem explicitly in plain language.',before=old,after=t,status='fixed'))
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');report['draftSha256']=hashlib.sha256(p.read_bytes()).hexdigest();report['notes']=report['notes'].replace('110 localized','118 localized');rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report['draftSha256'])
