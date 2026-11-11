from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
from pypdf import PdfReader
import json,re,hashlib,collections
root=Path('.');docs=root/'docs';collection=json.loads((docs/'collection.json').read_text());rows=[]
pattern=re.compile(r'\bAI\b|intelligen|machine|neuro|symbolic|research|circuit|understanding|reasoning|agent|RAG|S\*LM|MRP-VM|coherence|meta-rational|meaning as a path',re.I)
for book in collection['books']:
 if not pattern.search(book['title']['en']):continue
 folder=docs/book['directory'];m=json.loads((folder/'manifest.json').read_text());r={'bookId':book['id'],'title':book['title']['en'],'directory':book['directory'],'readers':{},'confirmedIssues':[],'reviewNeeded':[]}
 for lang in ['en','ro']:
  edition=m['editions'].get(lang,{})
  for fmt,key in [('full','fullContent'),('short','shortContent')]:
   value=edition.get(key)
   if not value:
    r['readers'][f'{lang}-{fmt}']={'available':False};r['reviewNeeded'].append(f'{lang}-{fmt}: edition unavailable; retain published versions and stage a complete requested translation');continue
   p=folder/value
   if not p.exists():r['confirmedIssues'].append('missing reader: '+value);continue
   d=html.fromstring(p.read_bytes());body=d.find('body')
   for e in d.xpath('//script|//style'):e.drop_tree()
   words=re.findall(r'\w+',body.text_content());images=d.xpath('//img');missing=[]
   for img in images:
    url=urlsplit(img.get('src',''))
    if not url.scheme and url.path and not (p.parent/unquote(url.path)).is_file():missing.append(img.get('src'))
   wrong=[e for e in d.xpath('//p[@lang]|//h1[@lang]|//h2[@lang]') if not e.get('lang').lower().startswith(lang)]
   info={'available':True,'words':len(words),'paragraphs':len(d.xpath('//p')),'headings':len(d.xpath('//h1|//h2|//h3')),'tables':len(d.xpath('//table')),'images':len(images),'missingImages':missing,'differentParagraphLanguage':len(wrong),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
   r['readers'][f'{lang}-{fmt}']=info
   if missing:r['confirmedIssues'].append(f'{lang}-{fmt}: {len(missing)} missing images')
   if len(words)<150:r['confirmedIssues'].append(f'{lang}-{fmt}: unusually little text ({len(words)} words)')
   if wrong:r['reviewNeeded'].append(f'{lang}-{fmt}: inspect {len(wrong)} paragraph language declarations')
   if lang=='en' and fmt=='full' and any('/ro/' in i.get('src','') or i.get('src','').startswith('../ro/') for i in images):r['reviewNeeded'].append('English reader shares original Romanian images; check visible labels before deciding whether localization is needed')
  pdf=edition.get('pdf')
  if pdf and (folder/pdf).is_file():
   try:
    reader=PdfReader(folder/pdf);page=reader.pages[0];uses=[args[0] for args,op in page.get_contents().operations if op==b'Do'];r[f'{lang}Pdf']={'pages':len(reader.pages),'firstPageImageDraws':len(uses),'firstPageTextCharacters':len(page.extract_text().strip())}
    if not uses:r['reviewNeeded'].append(f'{lang} PDF: review whether the authored cover is integrated')
   except Exception as e:r['confirmedIssues'].append(f'{lang} PDF cannot be inspected: {e}')
 animation=book.get('animation');r['animation']={'present':bool(animation),'durationMs':animation.get('durationMs') if animation else None,'exceedsCurrentIntroductionTarget':bool(animation and animation.get('durationMs',0)>120000)}
 if not animation:r['reviewNeeded'].append('No published animation')
 elif animation.get('durationMs',0)>120000:r['reviewNeeded'].append('Existing animation exceeds current two-minute introduction target; preserve while a revision is planned')
 rows.append(r)
report={'date':'2026-11-11','scope':'AI and research-related titles selected by title, not a global taxonomy','totalCatalogueBooks':len(collection['books']),'totalRegisteredAnimations':sum(bool(b.get('animation')) for b in collection['books']),'selectedBooks':len(rows),'confirmedConversionIssues':sum(len(r['confirmedIssues']) for r in rows),'reviewFlagsAreNotProvenDefects':True,'books':rows,'priorityProduction':['symbolic-world-models','an-intuitive-introduction-to-machine-learning']}
report['backlog']={'missingFullRomanianReaders':sum(not r['readers']['ro-full'].get('available') for r in rows),'selectedBooksWithoutAnimation':sum(not r['animation']['present'] for r in rows),'allBooksWithoutAnimation':len(collection['books'])-report['totalRegisteredAnimations'],'existingSelectedAnimationsAboveTwoMinutes':sum(r['animation']['exceedsCurrentIntroductionTarget'] for r in rows)}
p=Path('tasks/AI-RESEARCH-MAINTENANCE.json');p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='books'},ensure_ascii=False))
for r in rows:
 if r['confirmedIssues']:print(r['title'],r['confirmedIssues'])
