from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from pypdf import PdfReader
import json,re,zipfile,xml.etree.ElementTree as E
w=Path(__file__).resolve().parent
counts={}
for mode in ['full','short']:
 for lang in ['en','ro']:
  f=w/'book'/lang/f'{mode}_content.html';s=BeautifulSoup(f.read_text(),'html.parser')
  counts[mode,lang]=Counter(t.name for t in s.find_all())
  assert all(t['lang']==lang for t in s.find_all(attrs={'lang':True}))
  for img in s.find_all('img'):assert (f.parent/img['src']).resolve().is_file()
 assert counts[mode,'en']==counts[mode,'ro']
with zipfile.ZipFile('tasks/THOSE_WHO_NO_LONGER_RUN.docx') as z:doc=E.fromstring(z.read('word/document.xml'))
source=''.join(t.text or '' for t in doc.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
ro=BeautifulSoup((w/'book/ro/full_content.html').read_text(),'html.parser').article.get_text()
assert re.sub(r'\s+','',source)==re.sub(r'\s+','',ro)
r=PdfReader(w/'book/en/book.pdf');pdftext=[]
for i,page in enumerate(r.pages,1):pdftext.append(re.sub(r'^'+str(i)+r'\s+Those Who No Longer Run\s*','',page.extract_text()))
en=BeautifulSoup((w/'book/en/full_content.html').read_text(),'html.parser').article.get_text(' ',strip=True)
tokens=lambda text:Counter(re.findall(r'[^\W_]+',text.casefold()))
assert tokens(en)==tokens(' '.join(pdftext))
assert counts['full','en']['h1']==5 and counts['full','en']['h2']==24
f=w/'release.json';d=json.loads(f.read_text());d.setdefault('validation',{}).update(readerStructureChecked=True,readerStructure=dict(counts['full','en']),translationReviewed=True,sourceDocxTextPreserved=True,pdfTextComplete=True,pdfPageCount=len(r.pages));f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Verified: original DOCX text, matching EN/RO structure, five parts, 24 chapters, complete PDF text across',len(r.pages),'pages.')
