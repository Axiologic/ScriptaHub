from pathlib import Path
from zipfile import ZipFile
from lxml import etree,html
from html import escape
from collections import Counter
import json,re,hashlib
w=Path(__file__).parent;src=w/'Cine_va_mosteni_lumea.docx';N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};W='{'+N['w']+'}'
with ZipFile(src) as z:doc=etree.fromstring(z.read('word/document.xml'))
for x in ['footnoteReference','endnoteReference','oMath','object','hyperlink','numPr','gridSpan','vMerge','hMerge','drawing','ins','del']:
 assert not doc.xpath('//*[local-name()="'+x+'"]'),x+' requires explicit conversion support'
def plain(p):return ''.join(n.text or '' if n.tag==W+'t' else '\n' if n.tag==W+'br' else '\t' for n in p.iter() if n.tag in {W+'t',W+'br',W+'tab'})
def rich(p):
 out=[]
 for run in p.iter(W+'r'):
  t=''.join(escape(c.text or '') if c.tag==W+'t' else '<br>' if c.tag==W+'br' else ' ' if c.tag==W+'tab' else '' for c in run)
  rp=run.find(W+'rPr')
  if rp is not None:
   b=rp.find(W+'b');i=rp.find(W+'i');v=rp.find(W+'vertAlign')
   if b is not None and b.get(W+'val') not in {'0','false'}:t='<strong>'+t+'</strong>'
   if i is not None and i.get(W+'val') not in {'0','false'}:t='<em>'+t+'</em>'
   if v is not None and v.get(W+'val') in {'superscript','subscript'}:
    tag='sup' if v.get(W+'val')=='superscript' else 'sub';t=f'<{tag}>'+t+f'</{tag}>'
  out.append(t)
 return ''.join(out)
blocks=[];ledger=[];pi=0;ti=0;inlist=False
for b in doc.find(W+'body'):
 if b.tag==W+'sectPr':continue
 if b.tag==W+'p':
  t=plain(b);idx=pi;pi+=1
  if not t.strip():continue
  sty=b.find(W+'pPr/'+W+'pStyle');sty=sty.get(W+'val','') if sty is not None else '';bullet=sty=='ListBullet'
  if inlist and not bullet:blocks.append('</ul>');inlist=False
  if bullet and not inlist:blocks.append('<ul>');inlist=True
  tag='li' if bullet else 'h1' if idx==0 or sty=='Heading1' else 'h2' if sty in {'Heading2','TOCHeading'} else 'p';cls='callout' if sty=='Callout' else 'bibliography' if sty=='Bibliography' else 'subtitle' if idx==1 else ''
  blocks.append(f'<{tag} id="p{idx:04d}"'+(f' class="{cls}"' if cls else '')+'>'+rich(b)+f'</{tag}>');ledger.append(dict(type='paragraph',sourceIndex=idx,text=t,style=sty,tag=tag))
 elif b.tag==W+'tbl':
  if inlist:blocks.append('</ul>');inlist=False
  ti+=1;rows=[];values=[]
  for ri,tr in enumerate(b.findall(W+'tr')):
   cells=[];row=[]
   for ci,tc in enumerate(tr.findall(W+'tc')):
    ps=tc.findall(W+'p');texts=[plain(p) for p in ps if plain(p).strip()];tag='th' if ti==3 and ri==0 else 'td';cells.append(f'<{tag}>'+''.join(f'<p id="t{ti}-r{ri}-c{ci}-p{j}">'+rich(p)+'</p>' for j,p in enumerate(ps) if plain(p).strip())+f'</{tag}>');row.append(texts)
   rows.append('<tr>'+''.join(cells)+'</tr>');values.append(row)
  if any(t.strip() for row in values for cell in row for t in cell):blocks.append(f'<table id="table-{ti}" class="'+('source-toc' if ti==2 else 'data-table')+'">'+''.join(rows)+'</table>')
  ledger.append(dict(type='table',number=ti,rows=values,emptyLayoutOnly=not any(t.strip() for row in values for cell in row for t in cell)))
 else:raise ValueError('Unexpected source block '+b.tag)
if inlist:blocks.append('</ul>')
css='''html{color-scheme:light dark}body{margin:0;font:1.08rem/1.7 Georgia,serif}main{max-width:76ch;margin:auto;padding:2.5rem 1.4rem}h1,h2{font-family:system-ui,sans-serif;line-height:1.2;text-wrap:balance;break-after:avoid}h1{font-size:1.85rem;margin:2.5rem 0 1rem}h2{font-size:1.35rem;margin:2rem 0 .8rem}p{margin:0 0 1em}.subtitle{font-size:1.25rem;font-style:italic}.callout{padding:.8rem 1rem;background:color-mix(in srgb,currentColor 6%,transparent);border-radius:.3rem}.bibliography{font-size:.9em;overflow-wrap:anywhere}li{margin:.45rem 0}table{border-collapse:collapse;width:100%;margin:1.5rem 0;font-size:.9em;overflow-wrap:anywhere}td,th{text-align:left;vertical-align:top;padding:.6rem;border-bottom:1px solid #9aa}table p{margin:0 0 .5em}th{font-family:system-ui,sans-serif}.source-toc td{border:0;width:50%}.source-toc{font-size:.78em;line-height:1.4}a{color:inherit}@media(max-width:650px){main{padding:1.2rem}.data-table{display:block;overflow-x:auto}.source-toc,.source-toc tbody,.source-toc tr,.source-toc td{display:block;width:auto}}@media print{body{font-size:11pt}main{max-width:none;padding:0}h1,h2{break-after:avoid}.callout,tr{break-inside:avoid}}'''
content='\n'.join(blocks);sourcecounter=Counter(re.findall(r'\w+', ' '.join(plain(p) for p in doc.findall('.//'+W+'p'))));rendercounter=Counter(re.findall(r'\w+', ' '.join(html.fragment_fromstring(content,create_parent=True).itertext())));assert sourcecounter==rendercounter,(sourcecounter-rendercounter,rendercounter-sourcecounter)
output=w/'book/ro/full_content.html';assert not output.exists(),'Do not overwrite an existing canonical reader';output.parent.mkdir(parents=True,exist_ok=True);output.write_text('<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cine va moșteni lumea?</title><style>'+css+'</style></head><body><main data-reader-content>\n'+content+'\n</main></body></html>\n')
(w/'source-blocks.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n');(w/'source-complete.txt').write_text('\n\n'.join(plain(b) for b in doc.find(W+'body')))
report=dict(sourceSha256=hashlib.sha256(src.read_bytes()).hexdigest(),bodyParagraphs=pi,nonemptyBodyParagraphs=sum(x['type']=='paragraph' for x in ledger),tablesInSource=ti,substantiveDataTables=1,contentsLayoutTables=1,omittedEmptyLayoutTables=1,omittedNonemptyBlocks=0,exactWordMultisetPreserved=True,sourceTokens=sum(sourcecounter.values()),sourceImages=0,inlineFormatting='Bold, italic, superscript/subscript, line breaks and bullet lists retained; stable IDs preserve body and table order.',canonicalRomanianSha256=hashlib.sha256(output.read_bytes()).hexdigest())
(w/'source-extraction-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
