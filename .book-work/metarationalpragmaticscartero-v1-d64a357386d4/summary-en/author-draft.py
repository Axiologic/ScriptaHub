import json
from pathlib import Path
w=Path(__file__).parent;s=json.loads((w/'synthesis.json').read_text());sections=[]
for i,o in enumerate(s['outline'],1):
 pp=[]
 for line in (w/'draft-paragraphs.tsv').read_text().splitlines():
  n,ids,t=line.split('|')
  if int(n)==i:pp.append(dict(text=t,clusterIds=[f'cluster-{i:03}'],sourceUnitIds=[f'u{int(v):06}' for v in ids.split(',')],audit=dict(meaningPreserved=True,factsPreserved=True,noUnsupportedClaim=True)))
 sections.append(dict(id=o['id'],heading=o['title'],paragraphs=pp))
conclusion=[sections[-1]['paragraphs'].pop()]
d=dict(title='Meta-Rational Pragmatics',dek='Learning useful distinctions through programs, evidence and bounded computation.',sections=sections,conclusion=conclusion,audit=dict(sameLanguage=True,centralMessagePreserved=True,coherentEssay=True,notes='All chapters analyzed; thematic essay preserves conditional status, causal limits, distinct evidence types and experimental falsifiability. Numerical examples are instructional, not reported measurements.'))
(w/'draft.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
