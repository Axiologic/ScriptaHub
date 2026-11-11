from pathlib import Path
from html import unescape,escape
from lxml import html
from hashlib import sha256
from urllib.parse import urlsplit,unquote
import json,re,os,unicodedata,sys,shutil
base=Path('.book-work/ai-completion-20261111');identifier=sys.argv[1];folder=base/'reader-repairs'/identifier;report=json.loads((folder/'topline-audit.json').read_text());source=Path(report['source']);raw=source.read_text();assert sha256(source.read_bytes()).hexdigest()==report['htmlSha256']
norm=lambda t:re.sub(r'[^\w]','',unicodedata.normalize('NFKC',t).casefold())
# Preserve original markup and all protected code byte-for-byte: only insert
# source-proven text before known body-token offsets.
TOKEN=re.compile(r'<!--.*?-->|<[^>]+>',re.S);TAG=re.compile(r'<\s*(/?)\s*([\w:-]+)');stack=[];tokens=[];pos=0
for match in TOKEN.finditer(raw):
 if 'body' in stack and not any(tag in stack for tag in ['script','style','aside']):
  value=raw[pos:match.start()];decoded=[];indices=[]
  for part in re.finditer(r'&(?:#\w+|\w+);|.',value,re.S):
   text=unescape(part[0]);decoded.extend(text);indices.extend([pos+part.start()]*len(text))
  text=''.join(decoded)
  for word in re.finditer(r'\S+',text):
   token=norm(word[0])
   if token:tokens.append((token,indices[word.start()]))
 tag=TAG.match(match[0])
 if tag:
  closing,name=tag.groups();name=name.lower()
  if closing and name in stack:del stack[len(stack)-1-stack[::-1].index(name):]
  elif not closing and not match[0].endswith('/>') and name not in {'meta','link','img','br','hr','input','source','wbr'}:stack.append(name)
 pos=match.end()
assert len(tokens)==report['htmlTokens'],(len(tokens),report['htmlTokens'])
patches=[]
for item in report['allDifferences']:
 if item['operation']!='delete':continue
 # These source-proven losses occur exclusively in the top/bottom body lines;
 # central table ordering differences and intentional branding are untouched.
 low,high=item['pdfYRange']
 if not (high<=130 or low>=700 or low<=130 and high>=700):continue
 index=item['htmlTokenIndex'];assert [t for t,_ in tokens[max(0,index-5):index]]==item['before'];assert [t for t,_ in tokens[index:index+5]]==item['after']
 patches.append({'offset':tokens[index][1],'text':item['pdfWords']+' ','evidence':item})
for patch in sorted(patches,key=lambda p:p['offset'],reverse=True):raw=raw[:patch['offset']]+escape(patch['text'],quote=False)+raw[patch['offset']:]
book=folder/'book/en';book.mkdir(parents=True,exist_ok=True)
for name,markup in [('full_content.html',raw),('short_content.html',(source.parent/'short_content.html').read_text())]:
 dest=book/name
 def rebase(match):
  prefix,quote,value=match.groups();parsed=urlsplit(unescape(value))
  if not parsed.path or parsed.scheme or parsed.netloc or value.startswith('/'):return match[0]
  target=(source.parent/unquote(parsed.path)).resolve()
  if target.parent==source.parent.resolve() and target.name in {'full_content.html','short_content.html'}:target=(book/target.name).resolve()
  value=os.path.relpath(target,dest.parent.resolve())
  if parsed.query:value+='?'+parsed.query
  if parsed.fragment:value+='#'+parsed.fragment
  return prefix+quote+escape(value,quote=True)+quote
 markup=re.sub(r'(\b(?:src|href)\s*=\s*)(["\x27])(.*?)\2',rebase,markup)
 dest.write_text(markup)
# Text insertion leaves topology and all protected text intact.
a=html.fromstring(source.read_bytes());b=html.fromstring((book/'full_content.html').read_bytes())
assert [e.tag for e in a.iter()]==[e.tag for e in b.iter()]
for tag in ['script','style','code','pre','math','svg']:assert [''.join(e.itertext()) for e in a.xpath('//'+tag)]==[''.join(e.itertext()) for e in b.xpath('//'+tag)]
result={'bookId':identifier,'source':str(source),'sourcePdf':report['pdf'],'sourcePdfSha256':report['pdfSha256'],'oldHtmlSha256':report['htmlSha256'],'candidate':str(book/'full_content.html'),'newHtmlSha256':sha256((book/'full_content.html').read_bytes()).hexdigest(),'patches':patches,'wordsRestored':sum(len(p['text'].split()) for p in patches),'publication':'staged only; complete EN/RO validation and previous edition archive required','evidence':'Native PDF body text and adjacent exact HTML token sequences; no OCR, inferred prose, deletion, rebranding reversal or table reordering.'};(folder/'repair-proof.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(identifier,len(patches),'losses repaired;',result['wordsRestored'],'native source words restored into a separate candidate')
