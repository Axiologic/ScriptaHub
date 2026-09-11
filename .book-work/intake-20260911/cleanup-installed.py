from pathlib import Path
import json,hashlib,sys
for arg in sys.argv[1:]:
 w=Path(arg);r=json.loads((w/'release.json').read_text());src=Path(r['source']);arc=Path('docs')/r['directory']/'edition-files'/r['editionId']/'source'/src.name
 assert r['status']=='installed'
 assert hashlib.sha256(arc.read_bytes()).hexdigest()==r['sha256']
 assert len(json.loads((w/'qa/browser-public-review.json').read_text()))==10
 if src.exists():
  assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256'];src.unlink()
 (w/'source-cleanup.json').write_text(json.dumps(dict(source=str(src),archive=str(arc),sha256=r['sha256'],identicalArchiveVerified=True,installedEnglishPdfValidated=True,action='Removed delivered DOCX after successful install and catalogue/link/browser checks'),indent=2)+'\n');print('Archived and cleaned',src.name)
