from pathlib import Path
from hashlib import sha256
import json
w=Path(__file__).resolve().parent;root=w.parents[1]
r=json.loads((w/'release.json').read_text());public=root/'docs'/r['directory']
h=json.loads((public/'editions.json').read_text());edition=next(e for e in h['editions'] if e['id']==h['currentEdition'])
assert r['status']=='installed'
assert json.loads((w/'qa/browser/report.json').read_text())['status']=='passed'
sources=[(root/r['source'],edition['source']['sha256'])]
for item in edition['source']['pairedSources']:
    sources.append((root/'income'/item['filename'],item['sha256']))
staged=w/Path(r['source']).name
if staged.exists():sources.append((staged,edition['source']['sha256']))
for lang in ('en','ro'):
    assert all((public/lang/n).is_file() for n in ('book.pdf','full_content.html','short_content.html'))
removed=[]
for p,digest in sources:
    assert p.suffix=='.docx' and p.parent in (root/'income',w)
    assert sha256(p.read_bytes()).hexdigest()==digest
    removed.append({'path':str(p.relative_to(root)),'sha256':digest})
r['validation'].update(browserLayoutReviewed=True,catalogueChecked=True,linksChecked=True)
r['cleanup']={'verifiedAgainstInstalledEdition':h['currentEdition'],'removedDocx':removed,'retained':'Complete original-language HTML, PDF, figures, source filename and SHA-256 provenance','date':'2026-10-26'}
(w/'release.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
for p,_ in sources:p.unlink()
print('Removed verified DOCX deliveries and staging copy:',*[x['path'] for x in removed],sep='\n')
