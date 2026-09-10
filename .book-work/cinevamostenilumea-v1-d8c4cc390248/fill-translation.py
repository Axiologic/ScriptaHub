from pathlib import Path
import json,sys
w=Path(__file__).parent;r=w/'translations/en/full';number=int(sys.argv[1]);p=r/'chunks'/f'{number:04}.json';j=json.loads(p.read_text());values=(w/f'translated-{number:04}.txt').read_text().splitlines();assert len(values)==len(j['segments']),(len(values),len(j['segments']))
for s,t in zip(j['segments'],values):
 assert t.strip();assert not s['translation'] or s['translation']==t,(s['id'],'existing translation differs');s['translation']=t
p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n');memory={}
for f in sorted((r/'chunks').glob('*.json')):
 for s in json.loads(f.read_text())['segments']:
  if s['translation']:
   if s['source'] in memory:assert memory[s['source']]==s['translation'],s['source']
   memory[s['source']]=s['translation']
for f in sorted((r/'chunks').glob('*.json')):
 j=json.loads(f.read_text());changed=False
 for s in j['segments']:
  if not s['translation'] and s['source'] in memory:s['translation']=memory[s['source']];changed=True
 if changed:f.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
print('Completed chunk',number,'and propagated only exact already-translated source strings.')
