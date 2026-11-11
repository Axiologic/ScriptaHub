import json
from pathlib import Path
r=Path(__file__).parent
analyses=[json.loads(p.read_text()) for p in sorted((r/'analyses').glob('*.json'))]
# All reviewed analyses participate; recurrence merges repeated mechanisms rather than repeating chapter summaries.
groups=[('Continuitatea unei situații', [1,2,3,7,11], ['continuity','plurality','dialogue'],1,.95,.85),('O formă precisă pentru sens',[2,3,4,9,11],['formalization','contracts','integration'],1,.9,.9),('Întrebări diferite, calcule diferite',[5,6,7,9],['reasoning','uncertainty','dialogue'],.95,.9,.85),('Memoria care își revizuiește concluziile',[2,6,11],['revision','continuity'],1,.9,.9),('De la scenariu la efect verificat',[8,9,10,11],['programs','contracts','digital-twins','execution'],1,.9,.95),('Tipare care pot fi îmbunătățite',[3,7,12,13,14],['learning','evaluation','applications','qualification'],.95,.85,.85)]
cs=[]
for n,(label,ns,keys,c,rec,o) in enumerate(groups,1):
 selected=[a for i,a in enumerate(analyses,1) if i in ns]
 ideas=[i for a in selected for i in a['ideas'] if i['recurrenceCandidate'] in keys]
 cs.append({'id':f'cluster-{n:03}','label':label,'synthesis':' '.join(i['statement'] for i in ideas),'centrality':c,'recurrence':rec,'originality':o,'score':round(.5*c+.25*rec+.25*o,4),'selected':True,'chapterIds':[a['chapterId'] for a in selected],'sourceUnitIds':list(dict.fromkeys(u for i in ideas for u in i['sourceUnitIds'])),'ideaIds':[i['id'] for i in ideas]})
sy={'centralMessage':'Un model simbolic al lumii poate păstra continuitatea sensului între mesaje, situații, calcule, revizuiri și efecte prin tipare reutilizabile, instanțe persistente și contracte explicite; valoarea propunerii trebuie demonstrată prin comportamente verificabile.','clusters':cs,'outline':[{'id':f'section-{n:02}','title':c['label'],'purpose':c['label'],'budgetWords':[270,300,310,300,380,350][n-1],'clusterIds':[c['id']]} for n,c in enumerate(cs,1)],'chapterCoverage':[{'chapterId':a['chapterId'],'clusterIds':[c['id'] for c in cs if a['chapterId'] in c['chapterIds']]} for a in analyses],'audit':{'allAnalysesUsed':True,'centralMessageCovered':True,'redundancyMerged':True,'notes':'Bibliografia neadnotată exclusă din ierarhie; nota metodologică u000517 păstrează statutul propunerii și exemplelor. Prefața și concluzia se integrează tematic.'}}
(r/'synthesis.json').write_text(json.dumps(sy,ensure_ascii=False,indent=2)+'\n')
for a in analyses:print(a['batch'],a['thesis'], ' | '.join(i['statement'] for i in a['ideas']))
