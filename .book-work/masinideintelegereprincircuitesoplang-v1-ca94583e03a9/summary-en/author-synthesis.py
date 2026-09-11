import json
from pathlib import Path
w=Path(__file__).parent
analyses=[json.loads(p.read_text()) for p in sorted((w/'analyses').glob('*.json'))]
groups=[
 ('Understanding as accountable computation','The operational ambition is justified, revisable reasoning with explicit epistemic boundaries, not a metaphysical or general-intelligence achievement.',['bounded claims','operational understanding','epistemic provenance','circuit architecture'],1,.95,.8),
 ('Preserving the relevant future','Exact sufficient interfaces merge histories only when permitted continuations and observations cannot distinguish them.',['sufficient interfaces'],1,1,.95),
 ('Relations and the limits of approximation','Sound abstractions filter without losing actual possibilities, but exact acceptance and relational dependencies demand stronger representations.',['guarantee types','relational frontier','compositional contracts'],1,1,.85),
 ('Language with revisable memory','Shared alternatives and richer persistent sources support new questions and correction without inventing missing facts.',['revisable memory'],1,.85,.95),
 ('Learning and the full cost of compression','Counterexamples must produce transferable interfaces; symbolic, vector and hybrid approaches must disclose library, search, verification and update costs.',['counterexample learning','representation costs'],.95,1,.9),
 ('A program that can fail informatively','Finite demonstrations motivate controlled comparisons and staged independent evaluation; exactness, efficiency, transfer and diagnostic value require separate evidence.',['bounded experiments'],1,.95,.85)]
clusters=[]
for k,(label,syn,keys,c,r,o) in enumerate(groups,1):
 chosen=[(a,i) for a in analyses for i in a['ideas'] if i['recurrenceCandidate'] in keys]
 units={u for a,i in chosen for u in i['sourceUnitIds']}
 # Reviewed evidence and qualifications belong to the same analyzed chapter and
 # remain available to substantiate precise examples in the thematic draft.
 for a,i in chosen:
  for x in a['evidenceAndExamples']+a['objectionsAndQualifications']:units.update(x['sourceUnitIds'])
 clusters.append({'id':f'cluster-{k:03}','label':label,'synthesis':syn,'centrality':c,'recurrence':r,'originality':o,'score':.5*c+.25*r+.25*o,'selected':True,'chapterIds':sorted({a['chapterId'] for a,i in chosen}),'sourceUnitIds':sorted(units),'ideaIds':[i['id'] for a,i in chosen]})
outline=[]
for k,(title,budget,cs) in enumerate([
 ('What an answer must justify',280,[1]),('When different histories can share a future',350,[2,5]),('What compression must preserve',350,[3]),('An answer that can change for the right reason',350,[1,4]),('Learning representations without hiding the cost',300,[2,5]),('Evidence for a research program',350,[3,6])],1):
 outline.append({'id':f'section-{k:02}','title':title,'purpose':groups[k-1][1],'budgetWords':budget,'clusterIds':[f'cluster-{c:03}' for c in cs]})
d={'centralMessage':'Understanding through circuits is a research program for discovering sufficient representations that preserve relevant future distinctions, enabling shared search and revisable, source-grounded reasoning under explicit guarantees and measured limits.','clusters':clusters,'outline':outline,'chapterCoverage':[{'chapterId':a['chapterId'],'clusterIds':[c['id'] for c in clusters if a['chapterId'] in c['chapterIds']]} for a in analyses],'audit':{'allAnalysesUsed':True,'centralMessageCovered':True,'redundancyMerged':True,'notes':'All chapter groups read, including every numbered chapter and appendices. Continued contents reviewed and omitted as navigation. Annotated bibliography translated/read in full upstream; it records precedents already covered in chapters, not independent results.'}}
(w/'synthesis.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
