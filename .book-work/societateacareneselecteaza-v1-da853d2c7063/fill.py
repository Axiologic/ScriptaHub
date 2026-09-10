from pathlib import Path
import json,sys
w=Path(__file__).parent
p=w/'translations/en/full/chunks'/f'{int(sys.argv[1]):04d}.json';d=json.loads(p.read_text());lines=sys.stdin.read().strip().split('\n');assert len(lines)==len(d['segments']),(len(lines),len(d['segments']))
for s,t in zip(d['segments'],lines):assert t.strip();s['translation']=t.strip()
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(p.name,len(lines),'filled')
