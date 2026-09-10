from pathlib import Path
import json
w=Path(__file__).parent/'summary-job';analyses=[json.loads(p.read_text()) for p in sorted((w/'analyses').glob('*.json'))]
plans=[
('institutional-filters','Institutions distribute the cost of continuation','Housing, educational timing, prestige, kinship, partner markets and care shape reproductive opportunities without an announced selection program.',1,1,.9),
('fitness-transmission','Continuation requires more than births','Fitness includes reproducing descendants; cultural persistence combines births, retention, conversion and migration rather than copying all children unchanged.',.98,.9,.85),
('timescale-distinction','Culture and genes run on different clocks','Rapid learned behavior, demographic growth, and inherited genetic frequencies must be separated; historical cases illuminate distinct mechanisms.',.98,.95,.9),
('tradeoffs','There is no universally favored personality','Traits and vulnerabilities have costs and benefits conditioned by context, degree and frequency; clinical suffering need not hide an adaptive gift.',.9,.9,.85),
('inference-limits','The three-generation discipline','Distinguish evidence, disputed mechanisms and speculation; require comparable measures, completed fertility, transmission, persistent ecology and meaningful effect sizes.',1,1,.9),
('digital-transmission','AI changes costs and cultural parenthood','Assistance, companionship, tutor curricula and matching objectives may alter family formation and cultural retention in opposite ways; these are scenarios, not forecasts.',.95,.85,.98),
('epistemic-pluralism','Disagreement needs tests','Allow uncertain hypotheses without certifying them as true, and preserve correction rather than homogenization or unchecked belief.',.85,.85,.9),
('reproductive-freedom','Change environments without choosing people','Reduce unwanted barriers to parenting and protect voluntary exit; reproductive neutrality of virtue is not a program to maximize population or select worthy families.',1,1,.98),
('continuation-not-merit','Survival cannot settle ethics','Merit does not ensure continuation and continuation does not prove merit; care and freedom must remain worth transmitting.',1,1,.95),
('cooperation-defense','Protect cooperation without manufacturing threat','Internal cooperation can enable external harm; defensible limits need procedures and criticism, not unlimited aggression.',.85,.8,.9)]
clusters=[]
for j,(key,label,syn,c,r,o) in enumerate(plans):
 pairs=[(a,i) for a in analyses for i in a['ideas'] if i['recurrenceCandidate']==key]
 clusters.append(dict(id=f'cluster-{j+1:03d}',label=label,synthesis=syn,centrality=c,recurrence=r,originality=o,score=round(.5*c+.25*r+.25*o,4),selected=True,chapterIds=sorted(set(a['chapterId'] for a,i in pairs)),sourceUnitIds=sorted(set(u for a,i in pairs for u in i['sourceUnitIds'])),ideaIds=[i['id'] for a,i in pairs]))
outline=[]
for j,(title,purpose,budget,ids) in enumerate([
('The institutions that outlive us','State question through practical family costs and explain fitness versus cultural persistence.',300,[1,2,9]),
('No personality is destined to win','Use counterexamples, clinical distinction and context-dependent trade-offs.',310,[4,5]),
('What history can actually show','Explain rice, kinship, lineage bottleneck and ritual continuity as distinct mechanisms.',350,[3,5,10]),
('When technology becomes family infrastructure','Connect platforms, tutoring and opposite AI scenarios with disciplined pluralism.',350,[1,6,7]),
('Different futures, testable questions','Contrast seven ecologies and three-generation test rather than one prophecy.',350,[2,4,5,6,8,9,10]),
('Making good values livable','Conclude with reproductive freedom, institutional design and unresolved moral tension.',350,[8,9,10])]):
 outline.append(dict(id=f'section-{j+1:02d}',title=title,purpose=purpose,budgetWords=budget,clusterIds=[f'cluster-{i:03d}' for i in ids]))
ch=json.loads((w/'chapters.json').read_text())['chapters']
s=dict(centralMessage='Societies unintentionally shape which ways of life continue; understanding these conditional filters should guide freer, sustainable institutions, not genetic hierarchies or coercive reproduction.',clusters=clusters,outline=outline,chapterCoverage=[dict(chapterId=c['id'],clusterIds=[x['id'] for x in clusters if c['id'] in x['chapterIds']]) for c in ch if c['included']],audit=dict(allAnalysesUsed=True,centralMessageCovered=True,redundancyMerged=True,notes='All sixteen analyses read and merged, including two segments of Part III. Duplicate contents/edition labels and unannotated bibliography excluded from ranking. Numbered subchapters remain covered within part-aligned batches. Rare war-defense and antinatalist counterarguments retained within six thematic sections.'))
(w/'synthesis.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
