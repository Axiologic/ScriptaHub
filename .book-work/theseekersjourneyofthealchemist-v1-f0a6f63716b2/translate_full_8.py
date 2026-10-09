from pathlib import Path
import json
p=Path('.book-work/theseekersjourneyofthealchemist-v1-f0a6f63716b2/translations/ro/full/chunks/0008.json');d=json.loads(p.read_text())
t=['Comoara pe care Santiago o scoate de sub sicomor este adevărată, dar nu marchează sfârșitul poveștii. El înțelege acum că sensul vieții se află în urmarea Legendei Personale, în încrederea pe care o punem în univers și în credința că fiecare experiență, bună sau rea, ne apropie de omul care suntem meniți să devenim. Santiago nu mai este păstorul care visa la bogății; este un om care și-a trăit visul și a descoperit că cea mai mare comoară este călătoria însăși. Privind lumea și fiind pregătit pentru ce va veni, știe că bogăția lăuntrică îl va călăuzi oriunde îl va purta inima.']
assert len(t)==len(d['segments'])
for s,x in zip(d['segments'],t):s['translation']=x
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
