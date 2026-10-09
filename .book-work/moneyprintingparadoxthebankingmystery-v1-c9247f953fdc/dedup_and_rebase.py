from bs4 import BeautifulSoup
from pathlib import Path
import json,subprocess,shutil
w=Path(__file__).resolve().parent
source=w/'book/en/full_content.html';work=w/'translations/ro/full';temp=w/'translations/ro/full-rebased'
old=[]
for x in sorted((work/'chunks').glob('*.json')):old.extend(json.loads(x.read_text())['segments'])
by_source={}
for seg in old:
 if seg['translation']:
  key=seg['source']
  if key in by_source: assert by_source[key]==seg['translation'],key
  by_source[key]=seg['translation']
soup=BeautifulSoup(source.read_text(),'html.parser')
section=soup.select_one('#origins');paras=section.select('p');assert len(paras)==20
assert paras[7].get_text().startswith('The paradox of money printing becomes even more pronounced')
assert paras[-1].get_text().startswith('Policymakers will need to adapt')
for p in paras[7:]:p.decompose()
source.write_text(str(soup)+'\n')
if temp.exists():shutil.rmtree(temp)
subprocess.run(['python3','tools/html_translation_chunks.py','prepare',str(source),'--language','ro','--destination',str(w/'book/ro/full_content.html'),'--workdir',str(temp)],check=True)
new=[]
for x in sorted((temp/'chunks').glob('*.json')):
 d=json.loads(x.read_text())
 for seg in d['segments']:
  if seg['source'] in by_source:seg['translation']=by_source[seg['source']]
  new.append(seg)
 x.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert len(old)-len(new)==13,(len(old),len(new))
assert sum(bool(x['translation']) for x in new)==sum(bool(x['translation']) for x in old)-sum(bool(x['translation']) for x in old if x['id'] in {f't{i:06}' for i in range(12,25)})
shutil.rmtree(work/'chunks')
for name in ('manifest.json','template.html'):(work/name).unlink()
shutil.move(str(temp/'chunks'),str(work/'chunks'))
for name in ('manifest.json','template.html'):shutil.move(str(temp/name),str(work/name))
temp.rmdir()
q=json.loads((w/'qa/source-selection.json').read_text());q['intraBookDeduplication']={'removed':'13 near-repeated paragraphs on inflation from the latter half of Chapter I (source pp18–25); Chapter II retains the substantive treatment, examples, and policy discussion.','preserved':'original origin-of-money material in Chapter I and full inflation analysis in Chapter II','translationMigration':'All surviving completed Romanian segments were migrated by exact English source text; none were reset.'};(w/'qa/source-selection.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
print('Rebased',len(old),'to',len(new),'segments;',sum(bool(x['translation']) for x in new),'translated')
