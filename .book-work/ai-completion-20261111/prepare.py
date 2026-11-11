from pathlib import Path
import json,sys,hashlib,os,re
sys.path.insert(0,'tools')
from html_translation_chunks import prepare
from book_tasks import archive_reader_links
base=Path('.book-work/ai-completion-20261111');audit=json.loads(Path('tasks/AI-RESEARCH-MAINTENANCE.json').read_text());jobs=[]
for b in audit['books']:
 if b['readers']['ro-full'].get('available'):continue
 root=Path('docs')/b['directory'];manifest=json.loads((root/'manifest.json').read_text());history=json.loads((root/'editions.json').read_text());work=base/b['bookId'];work.mkdir(parents=True,exist_ok=True)
 sources={}
 for kind,name in [('full','full_content.html'),('short','short_content.html')]:
  source=root/'en'/name;sources[f'en/{name}']=hashlib.sha256(source.read_bytes()).hexdigest()
  if (root/'ro'/name).exists():continue
  job=work/'translations/ro'/kind
  if not (job/'manifest.json').exists():prepare(source,work/'book/ro'/name,'ro',job,maximum_words=5000)
 if not (work/'release.json').exists():
  release={'source':str(root/'en/full_content.html'),'sourceKind':'canonical-reader-completion','sha256':sources['en/full_content.html'],'sourceVersion':1,'automaticLanguages':['en','ro'],'status':'installed','bookId':b['bookId'],'directory':b['directory'],'englishTitle':b['title'],'editionId':history['currentEdition'],'readerCompletion':{'edition':history['currentEdition'],'canonicalSources':sources,'requestedLanguages':['ro'],'status':'translating'},'validation':{}}
  (work/'release.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n')
 jobs.append({'bookId':b['bookId'],'title':b['title'],'workdir':str(work),'status':'translating'})
Path('tasks/AI-COMPLETION.json').write_text(json.dumps({'scope':'Complete the 16 missing Romanian readers and 14 absent AI/research book introductions, then review existing AI films and remaining conversion findings. Preserve existing editions and completed work.','startedAt':'2026-11-11','readerJobs':jobs,'filmJobs':[{'bookId':b['bookId'],'title':b['title'],'directory':b['directory'],'status':'source-review'} for b in audit['books'] if not b['animation']['present']]},ensure_ascii=False,indent=2)+'\n')
