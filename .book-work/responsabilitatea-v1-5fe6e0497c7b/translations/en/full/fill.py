from pathlib import Path
import sys,json
w=Path(__file__).parent;p=w/'chunks'/f'{int(sys.argv[1]):04d}.json';d=json.loads(p.read_text());lines=Path(sys.argv[2]).read_text().splitlines();assert len(lines)==len(d['segments']),(len(lines),len(d['segments']))
for s,t in zip(d['segments'],lines):
 assert not s['translation'] or s['translation']==t
 s['translation']=t
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
