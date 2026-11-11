from pathlib import Path
from lxml import etree,html
from difflib import SequenceMatcher
from hashlib import sha256
import json,re,unicodedata,subprocess,sys
base=Path('.book-work/ai-completion-20261111');jobs=json.loads(Path('tasks/AI-COMPLETION.json').read_text())['readerJobs']
norm=lambda t:re.sub(r'[^\w]','',unicodedata.normalize('NFKC',t).casefold())
for job in jobs:
 if len(sys.argv)>1 and job['bookId'] not in sys.argv[1:]:continue
 work=Path(job['workdir']);release=json.loads((work/'release.json').read_text());public=Path('docs')/release['directory'];pdf=public/'en/book.pdf';source=public/'en/full_content.html';folder=base/'reader-repairs'/job['bookId'];folder.mkdir(parents=True,exist_ok=True);bbox=folder/'source-bbox.html'
 if not bbox.exists():subprocess.run(['pdftotext','-bbox-layout',str(pdf),str(bbox)],check=True)
 tree=etree.parse(str(bbox));words=[]
 for number,page in enumerate(tree.xpath('//*[local-name()="page"]'),1):
  height=float(page.get('height'))
  for word in page.xpath('.//*[local-name()="word"]'):
   if 40<=float(word.get('yMin')) and float(word.get('yMax'))<=height-40:
    text=''.join(word.itertext());token=norm(text)
    if token:words.append({'text':text,'norm':token,'page':number,'y':float(word.get('yMin'))})
 doc=html.fromstring(source.read_bytes())
 for e in doc.xpath('//script|//style|//aside[@data-pdf-conversion-warning]'):e.drop_tree()
 target=[]
 for value in doc.find('body').itertext():
  for m in re.finditer(r'\S+',value):
   token=norm(m.group())
   if token:target.append(token)
 a=[w['norm'] for w in words];finder=SequenceMatcher(None,a,target,autojunk=True);findings=[]
 for kind,i,j,k,l in finder.get_opcodes():
  if kind not in {'delete','replace'} or not 1<=j-i<=180:continue
  if ''.join(a[i:j])==''.join(target[k:l]):continue
  missing=words[i:j]
  if len({w['page'] for w in missing})!=1 or max(w['y'] for w in missing)>130:continue
  findings.append({'operation':kind,'replacedHtmlWords':target[k:l],'page':missing[0]['page'],'missingNativePdfWords':' '.join(w['text'] for w in missing),'count':len(missing),'htmlTokenIndex':k,'before':target[max(0,k-8):k],'after':target[k:k+8],'pdfYRange':[min(w['y'] for w in missing),max(w['y'] for w in missing)],'sourceWordRange':[i,j]})
 differences=[{'operation':kind,'pages':sorted({w['page'] for w in words[i:j]}),'pdfYRange':[min([w['y'] for w in words[i:j]],default=0),max([w['y'] for w in words[i:j]],default=0)],'pdfWords':' '.join(w['text'] for w in words[i:j]),'htmlWords':target[k:l],'htmlTokenIndex':k,'before':target[max(0,k-5):k],'after':target[l:l+5]} for kind,i,j,k,l in finder.get_opcodes() if kind!='equal']
 report={'allDifferences':differences,'bookId':job['bookId'],'title':job['title'],'pdf':str(pdf),'source':str(source),'pdfSha256':sha256(pdf.read_bytes()).hexdigest(),'htmlSha256':sha256(source.read_bytes()).hexdigest(),'nativePdfTokens':len(a),'htmlTokens':len(target),'sequenceSimilarity':finder.ratio(),'findings':findings,'scope':'Candidates from native PDF text at the top of body pages only; no OCR. Each candidate still needs context/visual review before a separate source-preserving repair.'};(folder/'topline-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(job['title'],len(findings),'candidates',sum(f['count'] for f in findings),'words',flush=True)
