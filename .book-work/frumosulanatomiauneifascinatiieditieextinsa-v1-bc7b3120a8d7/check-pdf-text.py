from pathlib import Path
from lxml import html
import pymupdf as fitz,unicodedata,json,re,hashlib
slugs=[Path(__file__).resolve().parent.name]
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if c.isalnum())
for slug in slugs:
 w=Path('.book-work')/slug;doc=fitz.open(w/'book/en/book.pdf');d=html.fromstring((w/'book/en/full_content.html').read_bytes());txt='';bounds=[]
 for i,page in enumerate(doc):
  for b in page.get_text('blocks'):
   if b[1]>page.rect.height-40:continue
   txt+=b[4]
   if b[0]<40 or b[2]>page.rect.width-40 or b[3]>page.rect.height-45:bounds.append(dict(page=i+1,box=list(b[:4]),text=b[4][:70]))
 nt=norm(txt);cur=0;missing=[];passed=[]
 for e in d.xpath('//main/*'):
  if e.get('class')=='source-toc':continue
  t=norm(e.text_content())
  if not t:continue
  pos=nt.find(t,cur)
  if pos<0:missing.append(dict(id=e.get('id'),text=e.text_content()[:150]))
  else:cur=pos+len(t);passed.append(e.get('id'))
 report=dict(sourceHtmlSha256=hashlib.sha256((w/'book/en/full_content.html').read_bytes()).hexdigest(),pdfSha256=hashlib.sha256((w/'book/en/book.pdf').read_bytes()).hexdigest(),pages=len(doc),normalizedNonTocElementsChecked=len(passed)+len(missing),matchedInSourceOrder=len(passed),missing=missing,bodyOutsideMargins=bounds,normalization='NFKC/casefold alphanumeric stream, removing pagination blocks; all non-TOC direct source elements must match in order.',sourceImages=len(d.xpath('//img')),sourceTables=len(d.xpath('//table')))
 (w/'qa/pdf/text-fidelity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(slug,len(doc),'missing',len(missing),missing[:3],'bounds',len(bounds))
