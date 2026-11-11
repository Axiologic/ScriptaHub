from pathlib import Path
from lxml import html
from collections import Counter
from PIL import Image,ImageDraw
import subprocess,json,re,unicodedata
w=Path('.book-work/swm-v1-7e813050a033');qa=w/'qa';report={}
normalize=lambda s:''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if c.isalnum())
for lang in ['ro','en']:
 pdf=w/f'book/{lang}/book.pdf';out=qa/f'{lang}-pdf-text.txt';subprocess.run(['pdftotext','-layout',str(pdf),str(out)],check=True)
 pages=out.read_text().split('\f');pages=pages[:-1] if not pages[-1].strip() else pages
 text=[]
 for i,p in enumerate(pages):
  lines=p.splitlines()
  while lines and not lines[-1].strip():lines.pop()
  if lines and lines[-1].strip()==str(i+1):lines.pop()
  text.append('\n'.join(lines))
 raw=qa/f'{lang}-pdf-raw.txt';subprocess.run(['pdftotext','-raw',str(pdf),str(raw)],check=True)
 raw_text=[]
 for i,page in enumerate(raw.read_text().split('\f')):
  lines=page.splitlines()
  while lines and not lines[-1].strip():lines.pop()
  if lines and lines[-1].strip()==str(i+1):lines.pop()
  raw_text.append('\n'.join(lines))
 norm=normalize('\n'.join(raw_text))
 d=html.fromstring((w/f'publication/{lang}/clean-publication.html').read_bytes());blocks=d.xpath('//body//p|//body//h1|//body//h2|//body//h3')
 missing=[]
 for i,b in enumerate(blocks):
  t=normalize(b.text_content())
  if t and t not in norm: missing.append({'block':i,'text':b.text_content()[:200]})
 print(lang,'pages',len(pages),'blocks',len(blocks),'missing',missing[:8])
 # Text bounds for all pages: outside-page words reveal clipping.
 bbox=qa/f'{lang}-pdf-bounds.html';subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
 bd=html.fromstring(bbox.read_bytes());overflow=[]
 for i,p in enumerate(bd.xpath('//page')):
  for word in p.xpath('.//word'):
   if float(word.get('xmin'))<0 or float(word.get('xmax'))>432.5 or float(word.get('ymin'))<0 or float(word.get('ymax'))>648.5:overflow.append((i+1,word.text))
 needles=['Figura 1.','Figura 2.','Figura 3.','Întrebarea despre deplasare','Momentul scenariului','Lume urmărită'] if lang=='ro' else ['Figure 1.','Figure 2.','Figure 3.','Question about the journey','Scenario time','World being tracked']
 selected={1,2,3,5,len(pages)}
 for needle in needles:
  for i,p in enumerate(pages):
   if needle in p: selected.add(i+1)
 for table in d.xpath('//table'):
  needle=normalize(table.xpath('.//p')[0].text_content())
  for i,page in enumerate(raw_text):
   if needle in normalize(page):selected.add(i+1)
 selected=sorted(selected)
 for page in selected:subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1200','-singlefile','-png',str(pdf),str(qa/f'{lang}-page-{page}')],check=True,stdout=subprocess.DEVNULL)
 subprocess.run(['pdftoppm','-scale-to','250','-jpeg','-jpegopt','quality=60',str(pdf),str(qa/f'{lang}-repaired-sequence')],check=True,stdout=subprocess.DEVNULL)
 thumbs=sorted(qa.glob(f'{lang}-repaired-sequence-*.jpg'))
 for start in range(0,len(thumbs),40):
  group=thumbs[start:start+40];montage=Image.new('RGB',(8*180,5*285),'#bbb');dr=ImageDraw.Draw(montage)
  for i,p in enumerate(group):
   im=Image.open(p);im.thumbnail((170,255));x=(i%8)*180;y=(i//8)*285;montage.paste(im,(x,y+20));dr.text((x,y),str(start+i+1),fill='black')
  montage.save(qa/f'{lang}-repaired-sequence-contact-{start//40+1}.png')
 report[lang]={'pages':len(pages),'checkedTextBlocks':len(blocks),'missingBlocks':missing,'outsidePageWords':overflow,'representativePages':selected,'allPagesRendered':len(thumbs)}
(qa/'pdf-fidelity-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
