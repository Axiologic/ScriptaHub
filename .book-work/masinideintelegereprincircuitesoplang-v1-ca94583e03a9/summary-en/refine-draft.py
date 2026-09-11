import json
from pathlib import Path
w=Path(__file__).parent
for n,statement,ids in [(3,'SOP Lang proposes a common circuit form for knowledge, rules, interpretation and composition strategies.',['u000084']),(4,'Unknown values can be represented as sets narrowed by constraints without prematurely selecting one value.',['u000142','u000143']),(9,'Faster prepared queries must be evaluated together with compilation and update costs.',['u000730'])]:
 p=w/f'analyses/batch-{n:04}.json';a=json.loads(p.read_text());a['evidenceAndExamples'].append({'statement':statement,'sourceUnitIds':ids});p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
