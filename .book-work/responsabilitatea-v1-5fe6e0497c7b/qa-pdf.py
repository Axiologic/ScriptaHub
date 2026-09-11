from pathlib import Path
import fitz,json,re,collections
from lxml import html
w=Path(__file__).parent;qa=w/'qa/pdf';qa.mkdir(parents=True,exist_ok=True);doc=fitz.open(w/'book/en/book.pdf');texts=[];rows=[]
for i,p in enumerate(doc):
 txt=p.get_text();texts.append(txt);pix=p.get_pixmap(matrix=fitz.Matrix(1,1));pix.save(qa/f'page-{i+1:03d}.png');blocks=[b for b in p.get_text('blocks') if b[4].strip() and not b[4].strip().isdigit()];rows.append(dict(page=i+1,words=len(txt.split()),start=' '.join(txt.split())[:95],end=' '.join(txt.split())[-160:],lowest=max([b[3] for b in blocks] or [0])))
(w/'pdf-text.txt').write_text('\n\f\n'.join(texts));(qa/'pages.json').write_text(json.dumps(rows,indent=2))
# Full-size individual renders above; compact contacts for page sequence/support review.
from PIL import Image,ImageDraw
for start in range(0,len(doc),20):
 subset=range(start,min(start+20,len(doc)));sheet=Image.new('RGB',(5*245,4*390),'#bfc9c1');d=ImageDraw.Draw(sheet)
 for j,i in enumerate(subset):
  im=Image.open(qa/f'page-{i+1:03d}.png').convert('RGB');im.thumbnail((235,360));x=(j%5)*245+(245-im.width)//2;y=(j//5)*390+20;sheet.paste(im,(x,y));d.text((x,y-16),str(i+1),fill='black')
 sheet.save(qa/f'contact-{start//20:02d}.jpg')
print('pages',len(doc));print(json.dumps([x for x in rows if x['words']<75],indent=2));print('contacts',list(qa.glob('contact*')))
