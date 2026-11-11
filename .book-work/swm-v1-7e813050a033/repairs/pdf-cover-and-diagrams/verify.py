from pathlib import Path
from lxml import html,etree
from pypdf import PdfReader
from hashlib import sha256
import subprocess,json,re,unicodedata
W=Path('.book-work/swm-v1-7e813050a033');Q=W/'qa';R=W/'repairs/pdf-cover-and-diagrams';P=Path('docs/books/symbolic/world/models/bk-049d00ef0ab54f38')
norm=lambda s:''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if c.isalnum())
old=html.fromstring((P/'en/full_content.html').read_bytes()).xpath('//article')[0].text_content()
new=html.fromstring((W/'book/en/full_content.html').read_bytes()).xpath('//article')[0].text_content()
assert old==new,'Localized artwork changed reader prose'
assets=json.loads((R/'asset-review.json').read_text())['diagrams']
for asset in assets:
 svg=etree.parse(str(W/'book/en'/asset['localized']))
 assert len(svg.xpath('//*[local-name()="rect"]'))==len(asset['nodes'])+1
 assert len(svg.xpath('//*[local-name()="path" and @marker-end]'))==len(asset['edges'])
assert len(assets)==3
report={}
for language in ['en','ro']:
 pdf=W/f'book/{language}/book.pdf';reader=PdfReader(pdf)
 assert len(reader.pages)==(120 if language=='en' else 117)
 cover_uses=[args[0] for args,op in reader.pages[0].get_contents().operations if op==b'Do']
 assert len(cover_uses)==1,'First page must draw exactly one cover image'
 cover_object=reader.pages[0]['/Resources']['/XObject'][cover_uses[0]].get_object()
 assert cover_object['/Subtype']=='/Image' and cover_object['/Width']==1200 and cover_object['/Height']==1800
 out=Q/f'cover-repair-{language}-raw.txt';subprocess.run(['pdftotext','-raw',str(pdf),str(out)],check=True)
 raw=out.read_text().split('\f');texts=[]
 for i,page in enumerate(raw):
  lines=page.splitlines()
  while lines and not lines[-1].strip():lines.pop()
  if lines and lines[-1].strip()==str(i):lines.pop()
  texts.append('\n'.join(lines))
 alltext=norm('\n'.join(texts))
 prose_pages=list(texts)
 if language=='en':
  for asset in assets:
   expected=''.join(label for lines in asset['nodes'] for label in lines)+''.join(asset['edgeLabels'])
   found=[]
   for i,page in enumerate(prose_pages):
    at=page.rfind(asset['nodes'][0][0])
    if at>=0 and norm(page[at:])==norm(expected):found.append((i,at))
   assert len(found)==1,('Could not isolate the complete SVG text block',asset['localized'],found)
   i,at=found[0];prose_pages[i]=prose_pages[i][:at]
 prose_text=norm('\n'.join(prose_pages))
 doc=html.fromstring((W/f'publication/{language}/clean-publication.html').read_bytes())
 blocks=doc.xpath('//body//p|//body//h1|//body//h2|//body//h3')
 missing=[i for i,b in enumerate(blocks) if norm(b.text_content()) and norm(b.text_content()) not in prose_text]
 assert not missing,(language,'Missing text blocks',missing)
 assert 'Edition 2' in ''.join(texts) if language=='en' else 'Ediția 2' in ''.join(texts)
 pages=[1,2,3,len(reader.pages)]
 for i,text in enumerate(texts):
  if re.search(r'Figure [123]\.',text):pages.append(i+1)
 if language=='en':
  for asset in assets:
   for lines in asset['nodes']:
    for label in lines:assert norm(label) in alltext,label
   for label in asset['edgeLabels']:assert norm(label) in alltext,label
  for label in ['Tipar de lume','Mesaj sau observație','Instanță de lume','Pregătirea bicicletei']:
   assert norm(label) not in alltext,label
 bounds=Q/f'cover-repair-{language}-bounds.html';subprocess.run(['pdftotext','-bbox',str(pdf),str(bounds)],check=True)
 bd=html.fromstring(bounds.read_bytes());outside=[]
 for i,page in enumerate(bd.xpath('//page')):
  for word in page.xpath('.//word'):
   if float(word.get('xmin'))<0 or float(word.get('xmax'))>432.5 or float(word.get('ymin'))<0 or float(word.get('ymax'))>648.5:outside.append((i+1,word.text))
 assert not outside,outside
 for page in sorted(set(pages)):
  subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1500','-singlefile','-png',str(pdf),str(Q/f'cover-repair-{language}-page-{page}')],check=True)
 report[language]={'pages':len(reader.pages),'completeTextBlocks':len(blocks),'missingTextBlocks':missing,'outsidePageWords':outside,'coverImageCount':len(cover_uses),'pdfSha256':sha256(pdf.read_bytes()).hexdigest(),'renderedPages':sorted(set(pages)),'firstPageCoverConfirmed':True}
(R/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Both full-page covers, complete prose, all English diagram labels and page bounds verified.')
