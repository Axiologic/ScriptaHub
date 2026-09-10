from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
from html import escape
import json,re,hashlib,shutil
w=Path(__file__).parent;n={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};W=n['w']
with ZipFile(w/'Societatea_care_ne_selecteaza.docx') as z:r=E.fromstring(z.read('word/document.xml'))
def text(p):
 return ''.join(x.text or '' if x.tag=='{'+W+'}t' else '\n' if x.tag=='{'+W+'}br' else '\t' for x in p.iter() if x.tag in ['{'+W+'}t','{'+W+'}br','{'+W+'}tab']).strip()
blocks=[];source=[];pi=0;tc=0
for b in r.find('w:body',n):
 if b.tag=='{'+W+'}p':
  t=text(b);i=pi;pi+=1
  if not t:continue
  sizes=[int(x.get('{'+W+'}val')) for x in b.findall('.//w:sz',n)];size=max(sizes or [20]);bold=bool(b.findall('.//w:b',n));italic=bool(b.findall('.//w:i',n))
  tag='h1' if size>=44 else 'h2' if bold and size==24 else 'p';cls='kicker' if re.match(r'^(CAPITOLUL|PARTEA|PREFAȚĂ|EPILOG|ANEXĂ)',t) and size<24 else 'subtitle' if italic else ''
  if i==0:t=t.replace('\n',' ')
  source.append({'type':'paragraph','sourceIndex':i,'text':t,'tag':tag});blocks.append(f'<{tag} id="p{i:04}"'+(f' class="{cls}"' if cls else '')+'>'+escape(t).replace('\n','<br>')+f'</{tag}>')
 elif b.tag=='{'+W+'}tbl':
  tc+=1;rows=[];sr=[]
  for ri,tr in enumerate(b.findall('w:tr',n)):
   cells=[];texts=[]
   for td in tr.findall('w:tc',n):
    ps=[text(p) for p in td.findall('w:p',n)];tag='th' if ri==0 else 'td';cells.append(f'<{tag}>'+''.join('<p>'+escape(t)+'</p>' for t in ps if t)+f'</{tag}>');texts.append(ps)
   rows.append('<tr>'+''.join(cells)+'</tr>');sr.append(texts)
  blocks.append(f'<table id="table-{tc}">'+''.join(rows)+'</table>');source.append({'type':'table','number':tc,'rows':sr})
style='''body{margin:0;background:#f6f3ed;color:#24343a;font-family:Georgia,"Noto Serif",serif;line-height:1.65}main{max-width:760px;margin:auto;padding:3rem 1.5rem}h1,h2{line-height:1.18;color:#153c41}h1{font-size:2rem;margin-top:3rem;page-break-before:always}h2{font-size:1.25rem;margin-top:2rem}p{margin:0 0 1em}.kicker{font-family:Arial,sans-serif;letter-spacing:.08em;margin:2rem 0 .4rem}.subtitle{font-style:italic;color:#516367}table{border-collapse:collapse;width:100%;font-size:.88em;margin:1.5rem 0}th,td{border-bottom:1px solid #b5c3c0;padding:.6rem;text-align:left;vertical-align:top}th{background:#e1e9e5}table p{margin:0 0 .4rem}.cover{width:100%;max-width:520px;display:block;margin:auto}@media(max-width:600px){main{padding:1rem}table{display:block;overflow:auto}}'''
html='<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Societatea care ne selectează</title><style>'+style+'</style></head><body><main data-reader-content>'+ '\n'.join(blocks)+'</main></body></html>'
(w/'book/ro/full_content.html').write_text(html);(w/'source-blocks.json').write_text(json.dumps(source,ensure_ascii=False,indent=2));(w/'source-complete.txt').write_text('\n\n'.join(text(b) for b in r.find('w:body',n)))
flat=' '.join(t['text'] if t['type']=='paragraph' else ' '.join(' '.join(c) for row in t['rows'] for c in row) for t in source)
print('All source words',len(flat.split()),'paragraphs',sum(x['type']=='paragraph' for x in source),'tables',tc)
(w/'source-extraction-review.json').write_text(json.dumps({'sourceSha256':hashlib.sha256((w/'Societatea_care_ne_selecteaza.docx').read_bytes()).hexdigest(),'paragraphs':sum(x['type']=='paragraph' for x in source),'tables':tc,'allWords':len(flat.split()),'omittedNonemptyBlocks':0,'lineBreakPolicy':'Preserved as br; first title line break normalized to space','sourceArtworkCount':0},indent=2))
shutil.copy2('/home/salboaie/.codex/generated_images/01a08adb-ded1-7bb1-b464-5d0ce8168b6c/exec-cdc7390e-bff0-4c77-87ed-36340e37becd.png',w/'generated-cover.png')
