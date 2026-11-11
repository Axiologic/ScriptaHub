from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
from hashlib import sha256
import json
base=Path('.book-work/ai-completion-20261111');specs=json.loads((base/'film-specs.json').read_text())
for spec in specs:
 root=Path('presentations')/spec['slug'];source=root/'source';source.mkdir(parents=True,exist_ok=True);public=Path('docs')/spec['directory'];reader=public/'en/short_content.html';d=html.fromstring(reader.read_bytes())
 for e in d.xpath('//script|//style|//details'):e.drop_tree()
 units=[]
 for e in d.xpath('//body//*[self::h1 or self::h2 or self::h3 or self::p or self::li or self::td or self::th]'):
  text=' '.join(e.text_content().split())
  if not text or text.startswith(('Read the','Read this','Open the complete')):continue
  units.append({'id':f'u{len(units)+1:03d}','kind':e.tag,'anchor':e.get('id',''),'text':text})
 full=html.fromstring((public/'en/full_content.html').read_bytes());chapters=[{'heading':' '.join(e.text_content().split()),'anchor':e.get('id')} for e in full.xpath('//h1|//h2')];images=[]
 for img in full.xpath('//img'):
  value=img.get('src','');parsed=urlsplit(value)
  if not parsed.scheme and parsed.path:images.append({'path':str((public/'en'/unquote(parsed.path)).resolve().relative_to(Path.cwd())),'alt':img.get('alt','')})
 for name,data in [('units.json',units),('chapter-map.json',chapters),('source-images.json',images),('extraction.json',{'file':str(reader),'htmlSha256':sha256(reader.read_bytes()).hexdigest(),'edition':json.loads((public/'editions.json').read_text())['currentEdition'],'completeTenMinuteReaderUsed':True,'completeBookSummarized':False,'chapterMapIncludesCompleteReader':True})]:
  (source/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (source/'source.txt').write_text('\n'.join(u['text'] for u in units)+'\n')
 print(spec['slug'],len(units),'units;',len(images),'source figures')
