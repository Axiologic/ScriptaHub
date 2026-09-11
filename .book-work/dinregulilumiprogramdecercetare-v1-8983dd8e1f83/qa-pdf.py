from pathlib import Path
import fitz,json,re,unicodedata,shutil,hashlib
from lxml import html
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];jobs=[('dinregulilumiprogramdecercetare-v1-8983dd8e1f83', None)]
for name,native in jobs:
 w=ROOT/'.book-work'/name;qa=w/'qa/pdf';qa.mkdir(parents=True,exist_ok=True);src=ROOT/'.book-work/intake-20260911/source-pdfs'/f'{native}.pdf' if native else w/'book/en/book.pdf';doc=fitz.open(src);texts=[];rows=[]
 for i,p in enumerate(doc):
  txt=p.get_text();texts.append(txt);p.get_pixmap(matrix=fitz.Matrix(1,1)).save(qa/f'page-{i+1:03d}.png');rows.append(dict(page=i+1,words=len(txt.split()),start=' '.join(txt.split())[:95],end=' '.join(txt.split())[-100:]))
 (w/'pdf-text.txt').write_text('\n\f\n'.join(texts));(qa/'pages.json').write_text(json.dumps(rows,indent=2))
 for start in range(0,len(doc),20):
  sheet=Image.new('RGB',(1225,1560),'#bfc9c1');draw=ImageDraw.Draw(sheet)
  for j,i in enumerate(range(start,min(start+20,len(doc)))):
   im=Image.open(qa/f'page-{i+1:03d}.png').convert('RGB');im.thumbnail((235,360));x=(j%5)*245+(245-im.width)//2;y=(j//5)*390+20;sheet.paste(im,(x,y));draw.text((x,y-16),str(i+1),fill='black')
  sheet.save(qa/f'contact-{start//20:02d}.jpg')
 print(name,len(doc),'pages',[(x['page'],x['words']) for x in rows if x['words']<40])
