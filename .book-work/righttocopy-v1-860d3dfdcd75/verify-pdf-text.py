from pathlib import Path
import fitz,json,re,unicodedata,shutil,hashlib
from lxml import html
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];jobs=[('righttocopy-v1-860d3dfdcd75', 'RIGHT_TO_COPY')]
def norm(t):
 return ''.join(c.lower() for c in unicodedata.normalize('NFKD',t) if c.isalnum())
for name,native in jobs:
 w=ROOT/'.book-work'/name;t=(w/'pdf-text.txt').read_text();t=re.sub(r'(?m)^\s*\d+\s*$','',t);t=re.sub(r'(?mi)^\s*THE (?:RIGHT TO COPY|NETWORK OF INTENT)\s*$','',t);hay=norm(t);dom=html.parse(str(w/'book/en/full_content.html'));bad=[];total=0
 for e in dom.xpath('//main//*[self::p or self::h1 or self::h2 or self::h3 or self::h4 or self::li][not(descendant::p)]'):
  s=e.text_content().strip()
  if not s:continue
  if not native and e.xpath('.//a[starts-with(@href,"#")]') and len(s)<180:s=re.sub(r'\s+\d+$','',s)
  total+=1
  if norm(s) not in hay and not (s.isdigit() and s in (w/'pdf-text.txt').read_text().split()):bad.append({'id':e.get('id'),'text':s})
 (w/'qa/pdf/text-check.json').write_text(json.dumps(dict(blocks=total,unmatched=bad),indent=2,ensure_ascii=False));print(name,total,len(bad),json.dumps(bad[:6],ensure_ascii=False)[:1800])
