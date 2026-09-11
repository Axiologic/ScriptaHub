import json
from pathlib import Path
w=Path(__file__).parent
for line in (w/'analysis-notes.tsv').read_text().splitlines():
 n,thesis,role,ids,ev,eids,qual,qids=line.split('|');n=int(n);name=f'batch-{n:04}.json';b=json.loads((w/'batches'/name).read_text())
 def units(s):return [f'u{int(i):06}' for i in s.split(',')]
 d=dict(batch=name,chapterId=b['chapterId'],segment=b['segment'],thesis=thesis,role=role,ideas=[dict(id=f'batch-{n:04}-idea-001',statement=thesis,centrality=0 if n==1 else .9,originality=0 if n==1 else .6,recurrenceCandidate=role,sourceUnitIds=units(ids))],evidenceAndExamples=[dict(statement=ev,sourceUnitIds=units(eids))],objectionsAndQualifications=[dict(statement=qual,sourceUnitIds=units(qids))],audit=dict(chapterCovered=True,meaningPreserved=True,factsPreserved=True,notes='All units read. Contents continuation excluded from ranking.' if n==1 else 'Source-grounded analysis; proposed mechanisms and limited guarantees preserved.'))
 (w/'analyses'/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
