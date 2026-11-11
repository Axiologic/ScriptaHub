from pathlib import Path
from collections import Counter,defaultdict
from lxml import html,etree
from urllib.parse import urlsplit,unquote
from hashlib import sha256
from html import escape,unescape
import json,re,unicodedata,os,sys
base=Path('.book-work/ai-completion-20261111')
def bag(text):return Counter(re.findall(r'\w+',unicodedata.normalize('NFKC',text).casefold()))
def compact(text):return ''.join(re.findall(r'\w+',unicodedata.normalize('NFKC',text).casefold()))
def text_of(e):return ' '.join(' '.join(e.itertext()).split())
def candidate_table(table,page):
 cols=table['columns'];rows=table['rows'];widths={};heights={}
 for cell in table['cells']:
  if cell['colspan']==1:widths.setdefault(cell['col'],cell['widthPt'])
  if cell['rowspan']==1:heights.setdefault(cell['row'],cell['heightPt'])
 if set(widths)!=set(range(cols)) or set(heights)!=set(range(rows)):raise ValueError('Uncertain row/column geometry')
 output=html.Element('table',{'class':'pdf-table','data-source-pdf-page':str(table['page'])});header=etree.SubElement(output,'thead');body=etree.SubElement(output,'tbody');x0=table['leftPt'];y0=table['topPt']
 for r in range(rows):
  row=etree.SubElement(header if r==0 else body,'tr')
  for cell in sorted([c for c in table['cells'] if c['row']==r],key=lambda c:c['col']):
   left=x0+sum(widths[c] for c in range(cell['col']));right=left+sum(widths[c] for c in range(cell['col'],cell['col']+cell['colspan']));top=y0+sum(heights[i] for i in range(r));bottom=top+sum(heights[i] for i in range(r,r+cell['rowspan']))
   if cell.get('boundsPt'):
    box=cell['boundsPt'];left,right,top,bottom=box['left'],box['right'],box['top'],box['bottom']
   words=[]
   for word in page.xpath('.//*[local-name()="word"]'):
    x=(float(word.get('xMin'))+float(word.get('xMax')))/2;y=(float(word.get('yMin'))+float(word.get('yMax')))/2
    if left<x<right and top<y<bottom:words.append(word)
   words.sort(key=lambda w:(round(float(w.get('yMin'))/2),float(w.get('xMin'))))
   value=' '.join(''.join(w.itertext()) for w in words)
   if compact(value)!=compact(cell['text']):raise ValueError(f"Native text and operator geometry disagree: row{r} col{cell['col']} expected {cell['text'][:100]!r}, observed {value[:100]!r}")
   elem=etree.SubElement(row,'th' if r==0 else 'td');elem.text=value
   if r==0:elem.set('scope','col')
   if cell['colspan']>1:elem.set('colspan',str(cell['colspan']))
   if cell['rowspan']>1:elem.set('rowspan',str(cell['rowspan']))
   typography=cell.get('typography') or {};fill=cell.get('background');styles=[]
   if fill:styles.append('background:'+fill)
   if typography.get('color'):styles.append('color:'+typography['color'])
   if typography.get('weight'):styles.append('font-weight:'+str(typography['weight']))
   if typography.get('style')=='italic':styles.append('font-style:italic')
   for side,value_ in cell.get('borders',{}).items():styles.append('border-'+side+':'+value_)
   if styles:elem.set('style',';'.join(styles))
 return output
if __name__ == '__main__':
 for identifier in sys.argv[1:]:
  folder=base/'reader-repairs'/identifier
  existing=folder/'table-repair-proof.json'
  if existing.exists() and json.loads(existing.read_text()).get('repairs'):
   print(identifier,'existing table candidate preserved; inspect proof before an explicit rebuild');continue
  evidence=json.loads((folder/'decorations.json').read_text());audit=json.loads((folder/'topline-audit.json').read_text());source=Path(audit['source']);candidate=folder/'book/en/full_content.html';active_source=candidate if candidate.exists() else source;raw=active_source.read_text();doc=html.fromstring(raw.encode());bbox=etree.parse(str(folder/'source-bbox.html'));pages=bbox.xpath('//*[local-name()="page"]');old_by_page=defaultdict(list);page=0
  for node in doc.iter():
   if m:=re.fullmatch(r'page_(\d+)',node.get('id','')):page=int(m[1])
   if node.tag=='table':old_by_page[page].append(node)
  native_by_page=defaultdict(list)
  for table in evidence['tables']:native_by_page[table['page']].append(table)
  repairs=[];pending=[]
  for number,native in native_by_page.items():
   old=old_by_page.get(number,[])
   if not old:pending.append({'page':number,'reason':'Native grid has no existing HTML table; inspect surrounding prose before structural recovery.'});continue
   try:new=[candidate_table(t,pages[number-1]) for t in sorted(native,key=lambda t:t['topPt'])]
   except ValueError as error:pending.append({'page':number,'reason':str(error)});continue
   oldbag=bag(' '.join(text_of(t) for t in old));newbag=bag(' '.join(text_of(t) for t in new));common=sum((oldbag&newbag).values());oldn=sum(oldbag.values());newn=sum(newbag.values())
   if common/max(1,oldn)<.94 or common/max(1,newn)<.90:
    pending.append({'page':number,'reason':'Detected native grids do not fully cover the HTML page tables; manual mapping required.','oldWords':oldn,'nativeWords':newn,'sharedWords':common});continue
   oldmatrix=[[[text_of(c) for c in row] for row in t.xpath('./thead/tr|./tbody/tr|./tr')] for t in old];newmatrix=[[[text_of(c) for c in row] for row in t.xpath('./thead/tr|./tbody/tr|./tr')] for t in new]
   if oldmatrix==newmatrix:continue
   # Keep anchors on the first recovered table; unrelated inter-table prose stays.
   for key,value in old[0].attrib.items():
    if key!='class':new[0].set(key,value)
   parent=old[0].getparent();index=parent.index(old[0])
   for offset,table in enumerate(new):parent.insert(index+offset,table)
   for node in old:
    tail=node.tail
    if tail:
     prior=node.getprevious()
     if prior is not None:prior.tail=(prior.tail or '')+tail
     else:node.getparent().text=(node.getparent().text or '')+tail
    node.getparent().remove(node)
   repairs.append({'page':number,'previousTableRows':[len(t.xpath('.//tr')) for t in old],'recoveredTableRows':[len(t.xpath('.//tr')) for t in new],'oldWords':oldn,'nativeWords':newn,'sharedWords':common,'nativeTables':native})
  if not repairs:
   (folder/'table-repair-proof.json').write_text(json.dumps({'bookId':identifier,'repairs':[],'pending':pending},ensure_ascii=False,indent=2)+'\n');print(identifier,'no safe table replacements;',len(pending),'manual mappings');continue
  candidate.parent.mkdir(parents=True,exist_ok=True)
  serialized=html.tostring(doc,encoding='unicode',method='html')
  def rebase(match):
   prefix,quote,value=match.groups();parsed=urlsplit(unescape(value))
   if not parsed.path or parsed.scheme or parsed.netloc or value.startswith('/'):return match[0]
   resolved=(active_source.parent/unquote(parsed.path)).resolve()
   if resolved.parent==active_source.parent.resolve() and resolved.name in {'full_content.html','short_content.html'}:resolved=(candidate.parent/resolved.name).resolve()
   value=os.path.relpath(resolved,candidate.parent.resolve())
   if parsed.query:value+='?'+parsed.query
   if parsed.fragment:value+='#'+parsed.fragment
   return prefix+quote+escape(value,quote=True)+quote
  serialized=re.sub(r'(\b(?:src|href)\s*=\s*)(["\x27])(.*?)\2',rebase,serialized)
  # Protected content remains exactly the same at DOM text level.
  revised=html.fromstring(serialized)
  for tag in ['script','style','code','pre','math','svg']:assert [''.join(e.itertext()) for e in doc.xpath('//'+tag)]==[''.join(e.itertext()) for e in revised.xpath('//'+tag)]
  candidate.write_text(serialized)
  proof={'bookId':identifier,'source':str(source),'sourcePdf':audit['pdf'],'sourcePdfSha256':evidence['sourceSha256'],'originalHtmlSha256':audit['htmlSha256'],'candidate':str(candidate),'candidateSha256':sha256(candidate.read_bytes()).hexdigest(),'repairs':repairs,'pending':pending,'scope':'Separate English candidate; certified native grid geometry, punctuation-preserving Poppler words and PDF.js character evidence agree. No OCR or inferred prose. Manual mappings remain explicit.'};(folder/'table-repair-proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(identifier,len(repairs),'pages of safely reconstructed tables;',len(pending),'manual mappings')
