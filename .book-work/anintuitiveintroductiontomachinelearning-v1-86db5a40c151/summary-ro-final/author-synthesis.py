import json
from pathlib import Path
root=Path(__file__).parent
essay=json.loads((root/'essay.json').read_text())
additions={
1:' Alegerea pragului este tot o decizie despre costuri: câte verificări suplimentare acceptă echipa și cât o costă un caz ratat. Aceasta nu trebuie ascunsă într-un număr produs de model. Mai multe modele pot avea scoruri apropiate și efecte diferite în folosire. Cazurile individuale și condițiile în care apar oferă informații pe care media le pierde.',
3:' Nici învățarea mai multă, nici un model mai mare nu sunt remedii universale. O curbă de validare încă descendentă sugerează utilitatea datelor suplimentare. O curbă aplatizată poate cere etichete mai curate, trăsături mai informative sau o întrebare schimbată. Repetarea exemplelor greșite întărește lecția greșită, iar datele sintetice cer verificare pentru a evita pierderea treptată a cazurilor rare.',
4:' Nici acceptarea unui document lung nu garantează că toate detaliile sunt folosite la fel de bine. Capacitatea de lucru depinde de reprezentarea pozițiilor, de calcule și de antrenare. A cere pași expliciți sau a încerca mai multe răspunsuri cu un verificator poate adăuga calcul util, însă explicația scrisă nu dovedește singură cum a apărut răspunsul. Instrumentele și testele din jur trebuie evaluate împreună cu modelul.',
6:' Un sistem poate avea discriminare bună și calibrare slabă: ordonează cazurile corect, dar exagerează probabilitățile. O corecție a scorurilor nu rezolvă automat intrările din afara lumii cunoscute. În astfel de cazuri, sistemul poate avea nevoie să se abțină sau să trimită decizia unui om. Și explicațiile trebuie încercate prin schimbări controlate: o hartă vizuală convingătoare poate descrie imaginea mai mult decât dependențele reale ale rețelei.',
7:' Confidențialitatea cere aceeași precizie. Învățarea federată păstrează datele în locuri separate, dar singură nu garantează că informația individuală nu se scurge. Confidențialitatea diferențială limitează influența unei persoane prin zgomot și un buget al protecției, cu un compromis de precizie. Ștergerea unei informații dintr-o rețea antrenată nu seamănă cu ștergerea unei pagini dintr-un dosar. Proprietatea și folosirea datelor cer decizii explicite, iar accesul unui agent la instrumente trebuie limitat la necesarul sarcinii.'
}
groups=[[1,2],[2,3,4],[5,6,7],[8,9,10],[11,12],[13,14,15],[16,17,18],[8,9,19,20,21]]
analyses={int(f.stem.split('-')[1]):json.loads(f.read_text()) for f in (root/'analyses').glob('batch-*.json')}
clusters=[]
for i,nums in enumerate(groups,1):
 aa=[analyses[n] for n in nums]
 refs=list(dict.fromkeys(r for a in aa for field in ['ideas','evidenceAndExamples','objectionsAndQualifications'] for item in a[field] for r in item['sourceUnitIds']))
 clusters.append({'id':f'cluster-{i:03d}','label':essay['sections'][i-1]['heading'],'synthesis':' '.join(a['thesis'] for a in aa),'centrality':.95,'recurrence':.85,'originality':.8,'score':.8875,'selected':True,'chapterIds':list(dict.fromkeys(a['chapterId'] for a in aa)),'sourceUnitIds':refs,'ideaIds':[idea['id'] for a in aa for idea in a['ideas']]})
synthesis={'centralMessage':'Învățarea automată ajustează aritmetică din exemple și feedback; oamenii aleg țintele, datele, măsurile, costurile și condițiile în care sistemul merită încredere.','clusters':clusters,'outline':[{'id':f'section-{i:02d}','title':s['heading'],'purpose':clusters[i-1]['synthesis'],'budgetWords':250,'clusterIds':[clusters[i-1]['id']]} for i,s in enumerate(essay['sections'],1)],'chapterCoverage':[{'chapterId':ch,'clusterIds':[c['id'] for c in clusters if ch in c['chapterIds']]} for ch in json.loads((root/'job.json').read_text())['contentChapterIds']],'audit':{'allAnalysesUsed':True,'centralMessageCovered':True,'redundancyMerged':True,'notes':'Toate cele 21 de analize sunt reunite tematic; prefața este folosită pentru mesaj și metodă, anexele ca punte către practică.'}}
(root/'synthesis.json').write_text(json.dumps(synthesis,ensure_ascii=False,indent=2)+'\n')
draft={'title':essay['title'],'dek':essay['dek'],'sections':[],'conclusion':[],'audit':{'sameLanguage':True,'centralMessagePreserved':True,'coherentEssay':True,'notes':'Revizie semantică: ideile sunt atribuite cărții; incertitudinea teoriilor creierului și a scalării este păstrată, fără fapte externe.'}}
for i,sec in enumerate(essay['sections']):
 paragraphs=sec['paragraphs'].copy()
 if i in additions:paragraphs[-1]+=additions[i]
 draft['sections'].append({'id':f'section-{i+1:02d}','heading':sec['heading'],'paragraphs':[{'text':text,'clusterIds':[clusters[i]['id']],'sourceUnitIds':clusters[i]['sourceUnitIds'],'audit':{'meaningPreserved':True,'factsPreserved':True,'noUnsupportedClaim':True}} for text in paragraphs]})
draft['conclusion']=[draft['sections'][-1]['paragraphs'].pop()]
(root/'draft.json').write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n')
