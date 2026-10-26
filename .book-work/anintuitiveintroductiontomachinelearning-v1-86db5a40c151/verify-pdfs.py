from pathlib import Path
from collections import Counter
from hashlib import sha256
from lxml import html
from pypdf import PdfReader
from PIL import Image, ImageOps, ImageDraw
import json,re,subprocess,unicodedata

work=Path(__file__).resolve().parent
qa=work/'qa/pdf';qa.mkdir(parents=True,exist_ok=True)
def tokens(s):
    s=unicodedata.normalize('NFKC',s).replace('\u00ad','')
    s=re.sub(r'(\w)-\s*\n\s*(\w)',r'\1\2',s)
    return Counter(re.findall(r'[^\W\d_]+',s.casefold()))
reports={}
for lang in ('en','ro'):
    pdf=work/f'book/{lang}/book.pdf'
    reader=PdfReader(pdf)
    pages=[p.extract_text() or '' for p in reader.pages]
    doc=html.fromstring((work/f'book/{lang}/full_content.html').read_bytes())
    for n in doc.xpath('//head | //math'): n.drop_tree()
    text=' '.join(doc.itertext())
    pdftext=subprocess.check_output(['pdftotext',str(pdf),'-']).decode()
    missing=tokens(text)-tokens(pdftext)
    critical={k:v for k,v in missing.items() if len(k)>3 and v>1}
    selected=sorted(set([1,2,3,8,len(pages)//2,len(pages)]+[i+1 for i,s in enumerate(pages) if 'Precision' in s or 'RMSE' in s or 'Softmax' in s or 'softmax' in s or 'Recall' in s]))
    thumbs=[]
    for page in selected:
        out=qa/f'{lang}-{page:03d}'
        subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1200','-singlefile','-png',str(pdf),str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        im=Image.open(str(out)+'.png').convert('RGB');im.thumbnail((300,450))
        tile=Image.new('RGB',(320,480),'#e5e5e5');tile.paste(im,((320-im.width)//2,15));ImageDraw.Draw(tile).text((12,460),f'{lang} page {page}',fill='black');thumbs.append(tile)
    sheet=Image.new('RGB',(320*4,480*((len(thumbs)+3)//4)),'white')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*320,(i//4)*480))
    sheet.save(qa/f'{lang}-contact.png')
    reports[lang]={'pages':len(pages),'bytes':pdf.stat().st_size,'sha256':sha256(pdf.read_bytes()).hexdigest(),'renderedPages':selected,'proseTokenCount':sum(tokens(text).values()),'missingTokenCount':sum(missing.values()),'missingRepeatedLongTokens':critical,'missingSample':missing.most_common(25),'emptyTextPages':[i+1 for i,s in enumerate(pages) if len(s.strip())<4],'firstPageRights':pages[0]}
(qa/'report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(reports,ensure_ascii=False,indent=2))
