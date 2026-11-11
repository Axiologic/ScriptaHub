from pathlib import Path
from lxml import html,etree
from collections import Counter
from hashlib import sha256
import json,re,importlib.util
base=Path('.book-work/ai-completion-20261111');folder=base/'reader-repairs/bk-5e790be3de5d4533';candidate=folder/'book/en/full_content.html';raw=candidate.read_bytes();doc=html.fromstring(raw);tables=json.loads((folder/'decorations.json').read_text())['tables'];pages=etree.parse(str(folder/'source-bbox.html')).xpath('//*[local-name()="page"]');spec=importlib.util.spec_from_file_location('table_repair',base/'stage-table-repairs.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
chars=lambda text:Counter(re.sub(r'[^\w]','',' '.join(text.split()).casefold()))
text=lambda node:' '.join(' '.join(node.itertext()).split())
proof=[]
def source_table(page,first_header):
 t=next(t for t in tables if t['page']==page and t['cells'][0]['text']==first_header)
 result=module.candidate_table(t,pages[page-1])
 # Restore identifiers split by visual line wraps, retaining identical glyphs.
 for row in result.xpath('./tbody/tr'):
  cell=row[0];value=cell.text or ''
  if first_header in {'Field','Invariant'} and ('_' in value or len(re.findall('[A-Z]',value))>=3) and re.fullmatch(r'[A-Za-z0-9_ ]+',value):cell.text=value.replace(' ','')
 return result

def matching_p(prefix,start=0):
 matches=[p for p in doc.xpath('//p') if text(p).startswith(prefix)]
 assert matches,prefix
 return matches[start]
def replace_prose(header,data,new,tail_marker=None):
 assert len(data)==0,'Inline formatting requires separate mapping'
 value=data.text or '';prefix,marker,tail=value.partition(tail_marker) if tail_marker else (value,'','')
 assert not tail_marker or marker,tail_marker
 original=text(header)+' '+prefix
 assert chars(original)==chars(text(new)),(original,text(new))
 if header.get('id'):new.set('id',header.get('id'))
 new.tail=header.tail;header.getparent().replace(header,new)
 if tail_marker:data.text=marker+tail
 else:data.getparent().remove(data)
 proof.append({'page':new.get('data-source-pdf-page'),'operation':'native table replaces fragmented prose','originalText':original,'recoveredText':text(new),'narrativeTailPreserved':tail_marker})
header=matching_p('State of the relation Appropriate response');replace_prose(header,header.getnext(),source_table(42,'State of the relation'))
header=matching_p('State of the relation Appropriate response');replace_prose(header,header.getnext(),source_table(43,'State of the relation'),'Models sometimes collapse')
# The page93 field table and the invariant table occupy distinct source grids.
old=next(t for t in doc.xpath('//table') if 'BRIDGE_STATUS' in text(t));new=source_table(93,'Field');assert chars(text(old))==chars(text(new));new.tail=old.tail;old.getparent().replace(old,new);proof.append({'page':93,'operation':'field rows recovered from the matching3-column grid'})
header=matching_p('Invariant Violation signal');replace_prose(header,header.getnext(),source_table(93,'Invariant'))
old=next(t for t in doc.xpath('//table') if 'CompatibleAlternativesRemainVisible' in text(t));spill=old.getparent().getnext() if old.getparent().tag=='div' else old.getnext();assert spill.tag=='p';prefix,marker,tail=(spill.text or '').partition('Rules return');assert marker;new=source_table(94,'Invariant');assert chars(text(old)+' '+prefix)==chars(text(new));new.tail=old.tail;old.getparent().replace(old,new);spill.text=marker+tail;proof.append({'page':94,'operation':'complete invariant rows recovered; following Rules return prose preserved'})
old=next(t for t in doc.xpath('//table') if 'Lexical bridge' in text(t));new=source_table(94,'Attack');assert chars(text(old))==chars(text(new));new.tail=old.tail;old.getparent().replace(old,new);proof.append({'page':94,'operation':'attack rows recovered'})
header=matching_p('Attack Operation');replace_prose(header,header.getnext(),source_table(95,'Attack'),'An attack is validated')
# A one-cell pseudo-table is a plain parameter continuation, not a source grid.
old=next(t for t in doc.xpath('//table') if 'DECLARED_INVARIANTS' in text(t));p=html.Element('p');p.text=text(old);p.tail=old.tail;old.getparent().replace(old,p);proof.append({'page':95,'operation':'parameter list retained as prose rather than a false table','text':p.text})
for tag in ['script','style','pre','math','svg']:
 original=html.fromstring(raw);assert [''.join(e.itertext()) for e in original.xpath('//'+tag)]==[''.join(e.itertext()) for e in doc.xpath('//'+tag)]
candidate.write_text(html.tostring(doc,encoding='unicode',method='html'))
(folder/'manual-table-review.json').write_text(json.dumps({'status':'passed-native-mapping','source':'PDF native character/grid evidence and exact remaining prose; no OCR or invented cells.','oldCandidateSha256':sha256(raw).hexdigest(),'newCandidateSha256':sha256(candidate.read_bytes()).hexdigest(),'repairs':proof,'reviewedUnchanged':[{'page':8,'reason':'Detector certifies only the Appendix portion of a contents layout; preserve the existing whole contents rather than replacing it with a partial grid.'}]},ensure_ascii=False,indent=2)+'\n');print('Coherence Pressure: six manual source-grid mappings and one false table corrected; contents retained.')
