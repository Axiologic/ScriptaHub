from pathlib import Path
from urllib.parse import urlsplit,unquote
from hashlib import sha256
from lxml import html
import json
base=Path('.book-work/ai-completion-20261111');reports=[];errors=[]
for w in sorted(base.glob('bk-*')):
 rp=w/'release.json'
 if not rp.exists():continue
 r=json.loads(rp.read_text());c=r.get('readerCompletion',{})
 if c.get('status')!='complete':continue
 public=Path('docs')/r['directory'];ed=json.loads((public/'editions.json').read_text());matches=[x for e in ed['editions'] for x in e.get('readerCompletions',[]) if x.get('edition')==c.get('edition') and x.get('completedAt')==c.get('completedAt') and x.get('installedReaders')==c.get('installedReaders')]
 row={'bookId':w.name,'directory':str(public),'historyMatchesWorkspace':len(matches)==1,'readers':[]}
 if len(matches)!=1:errors.append([w.name,'history mismatch'])
 for rel,want in c.get('installedReaders',{}).items():
  p=public/rel;actual=sha256(p.read_bytes()).hexdigest();hash_ok=actual==want
  if not hash_ok:errors.append([w.name,rel,'completion hash mismatch',want,actual])
  if not rel.endswith('.html'):continue
  root=html.fromstring(p.read_bytes());missing=[];tested=[]
  for el in root.iter():
   for attr in ('src','href','poster'):
    raw=el.get(attr)
    if not raw:continue
    u=urlsplit(raw)
    if u.scheme or u.netloc or raw.startswith('//'):continue
    target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
    tested.append({'tag':el.tag,'attribute':attr,'url':raw})
    if not target.is_file():missing.append(raw)
  if missing:errors.append([w.name,rel,'missing assets',missing])
  row['readers'].append({'path':str(p),'sha256':actual,'completionHashMatches':hash_ok,'localAssetTargets':len(tested),'allLocalTargetsResolve':not missing,'missing':missing})
 # Verify every current installed full even if completion map only tracked short.
 full=public/'ro/full_content.html';assert full.exists(),full
 row['canonicalSourcesMatch']=all((public/f).exists() and sha256((public/f).read_bytes()).hexdigest()==h for f,h in c.get('canonicalSources',{}).items())
 if not row['canonicalSourcesMatch']:errors.append([w.name,'canonical source hash mismatch'])
 reports.append(row)
report={'passed':not errors,'completedBooks':len(reports),'books':reports,'errors':errors,'scope':'Read-only QA of installed completion hash against workspace and editions history; all local src/href/poster file targets including CSS/scripts/images, external URLs excluded. No semantic perfection claim.'}
(base/'final-installed-ro-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':not errors,'completedBooks':len(reports),'readers':sum(len(x['readers']) for x in reports),'localTargets':sum(y['localAssetTargets'] for x in reports for y in x['readers']),'errors':errors},ensure_ascii=False,indent=2))
assert len(reports)==9,len(reports)
assert not errors,errors
