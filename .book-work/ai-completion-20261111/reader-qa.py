from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit,unquote
from lxml import html
from hashlib import sha256
import json,sys,re
sys.path.insert(0,'tools')
from html_translation_chunks import validate
base=Path('.book-work/ai-completion-20261111')
for identifier in sys.argv[1:]:
 work=base/identifier;release=json.loads((work/'release.json').read_text());public=Path('docs')/release['directory'];checks=[]
 for kind,name in [('full','full_content.html'),('short','short_content.html')]:
  if (public/'ro'/name).exists() and 'ro/'+name not in release.get('readerCompletion',{}).get('installedReaders',{}):checks.append({'reader':name,'existingPublishedReaderPreserved':True});continue
  job=work/'translations/ro'/kind;manifest,template,translations=validate(job);target=Path(manifest['destination']);assert target.exists()
  src=html.fromstring(Path(manifest['source']).read_bytes());dst=html.fromstring(target.read_bytes())
  for node in src.xpath('//aside[@data-pdf-conversion-warning]'):node.drop_tree()
  a=Counter(e.tag for e in src.iter() if isinstance(e.tag,str));b=Counter(e.tag for e in dst.iter() if isinstance(e.tag,str));assert a==b,(identifier,name,a-b,b-a)
  assert dst.get('lang')=='ro';assert not dst.xpath('//*[@lang and not(starts-with(@lang,"ro"))]')
  for tag in ['script','style','code','pre','math','svg']:
   originals=[''.join(e.itertext()) for e in src.xpath('//'+tag)];revised=[''.join(e.itertext()) for e in dst.xpath('//'+tag)];assert originals==revised,(identifier,name,tag)
  missing=[]
  for img in dst.xpath('//img'):
   u=urlsplit(img.get('src',''))
   if u.path and not u.scheme and not(target.parent/unquote(u.path)).is_file():missing.append(img.get('src'))
  assert not missing,(identifier,missing)
  allsegments=[s for p in sorted((job/'chunks').glob('*.json')) for s in json.loads(p.read_text())['segments']]
  sourcewords=sum(len(s['source'].split()) for s in allsegments);targetwords=sum(len(s['translation'].split()) for s in allsegments)
  assert .6<targetwords/max(sourcewords,1)<1.8,(sourcewords,targetwords)
  unchanged=[s['id'] for s in allsegments if len(s['source'].split())>10 and s['source']==s['translation']]
  checks.append({'reader':name,'sourceSha256':sha256(Path(manifest['source']).read_bytes()).hexdigest(),'targetSha256':sha256(target.read_bytes()).hexdigest(),'segments':len(allsegments),'allSegmentsTranslated':True,'domTagCountsIdentical':True,'protectedContentUnchanged':True,'imagesResolve':True,'sourceWords':sourcewords,'translatedWords':targetwords,'unchangedSubstantiveUnitsForBibliographyReview':unchanged})
 (work/'reader-qa.json').write_text(json.dumps({'valid':True,'scope':'Deterministic completeness, structure, protected content, language declarations, image targets and length checks; semantic review is recorded separately by the translator.','readers':checks},ensure_ascii=False,indent=2)+'\n');print(identifier,'passed',[(c['reader'],c.get('segments','existing')) for c in checks])
