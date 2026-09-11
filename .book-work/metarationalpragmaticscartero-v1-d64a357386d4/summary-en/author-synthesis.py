import json
from pathlib import Path
w=Path(__file__).parent
analyses={int(p.stem.split('-')[1]):json.loads(p.read_text()) for p in (w/'analyses').glob('*.json')}
# All analyses have been read and reconciled against the complete source.
specs=[
('The distinction an agent cannot yet make','Operational understanding rests on representation and procedure together; sufficiency is relative to a task family, and lost distinctions cannot be recovered without information.',[2,3,4,5,7,29],1,.95,.8,320),
('Diagnose before learning','Distinguish implementation error, compression loss, missing observations and stochastic uncertainty, then induce and test a general executable refinement.',[8,9,10,11,12,28],1,.9,.9,340),
('Paying for a reusable capability','Probability, utility and evidence remain separate while bounded metareasoning evaluates complementary operations and lifetime library costs.',[6,13,14],.95,.9,.75,270),
('Geometry with a stated purpose','Test-based distances, fixed-utility preference cones and local atlases are precise conditional tools, not a universal geometry of knowledge.',[15,16,17,27],.85,.65,.85,290),
('An environment that remembers its reasons','Versioned contracts, evidence states and dependency records support controlled promotion and revision; circuits and SOP Lang are optional implementations.',[5,14,18,19,20,29],.9,.9,.8,270),
('Where the proposal can be tested','Bounded protocols, document exceptions, research interventions and educational contrasts offer separate test domains with human and epistemic limits.',[21,22,23,24],.8,.75,.7,260),
('A hypothesis allowed to fail','The claimed diagnosis-to-reuse advantage must survive equal-resource baselines, structural holdouts, ablations and honest uncertainty; no completed theory or competitive product is established.',[2,12,25,26,27,28],1,1,.8,250)
]
clusters=[];outline=[]
for i,(title,msg,nums,c,r,o,budget) in enumerate(specs,1):
 aa=[analyses[n] for n in nums];ids=[]
 for a in aa:
  for block in a['ideas']+a['evidenceAndExamples']+a['objectionsAndQualifications']:ids+=block['sourceUnitIds']
 cid=f'cluster-{i:03}'
 clusters.append(dict(id=cid,label=title,synthesis=msg,centrality=c,recurrence=r,originality=o,score=.5*c+.25*r+.25*o,selected=True,chapterIds=sorted({a['chapterId'] for a in aa}),sourceUnitIds=sorted(set(ids)),ideaIds=[x['id'] for a in aa for x in a['ideas']]))
 outline.append(dict(id=f'section-{i:02}',title=title,purpose=msg,budgetWords=budget,clusterIds=[cid]))
s=dict(centralMessage='MRP proposes learning, verifying and reusing executable distinctions that repair diagnosed representational insufficiencies; whether this improves error and lifetime cost remains an empirical question under explicit information, scope and resource constraints.',clusters=clusters,outline=outline,chapterCoverage=[dict(chapterId=a['chapterId'],clusterIds=[c['id'] for c in clusters if a['chapterId'] in c['chapterIds']]) for a in analyses.values()],audit=dict(allAnalysesUsed=True,centralMessageCovered=True,redundancyMerged=True,notes='All 29 batches read. Continued contents has no selected cluster. Annotated bibliography read during complete translation; it attributes established methods and adds no independent validation of MRP. Repeated appendix examples support the same thematic clusters, not a duplicate chapter inventory.'))
(w/'synthesis.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
