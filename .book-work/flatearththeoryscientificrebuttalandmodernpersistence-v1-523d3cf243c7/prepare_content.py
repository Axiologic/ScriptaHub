from pathlib import Path
from bs4 import BeautifulSoup
import json
import re

root=Path(__file__).parent
draft=BeautifulSoup(Path('.book-work/income-pdf-candidates/523d3cf243c77867/clean-draft.html').read_text(), 'html.parser')
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flat Earth Theory: Scientific Rebuttal and Modern Persistence</title></head><body><article data-reader-content></article></body></html>','html.parser')
article=out.article
h1=out.new_tag('h1',id='book-title');h1.string='Flat Earth Theory: Scientific Rebuttal and Modern Persistence';article.append(h1)
byline=out.new_tag('p');byline['class']='book-byline';byline.string='AI Agent Althea Zappa';article.append(byline)
heads={
 7:('Introduction',1),
 10:('Chapter 1 — NASA: Guardian of Truth or Master of Deception?',2),
 14:('Chapter 2 — Historical Context of Flat Earth Theory',2),
 16:('Chapter 3 — A Resurgence of Flat Earth Ideas',2),
 21:('Chapter 4 — Understanding Pseudoscience',2),
 29:('Chapter 5 — Arguments Against Flat Earth Theory',2),
 37:('Chapter 6 — The Scientific Community’s Response',2),
 43:('Chapter 7 — Implications for Science Education and Critical Thinking',2),
 49:('Conclusion',1),
 56:('Bibliography',1),
}
kept=list(range(7,50))+[56,57]
sections=[]
for page in kept:
 sec=draft.select_one(f'section[data-source-page="{page}"]');assert sec,page
 paragraphs=sec.find_all('p',recursive=False)
 if page in heads:
  label,skip=heads[page]
  ident='bibliography' if page==56 else ('introduction' if page==7 else 'conclusion' if page==49 else f'chapter-{len([x for x in sections if x["id"].startswith("chapter-")])+1}')
  h=out.new_tag('h2',id=ident);h.string=label;article.append(h);sections.append({'id':ident,'title':label,'page':page});paragraphs=paragraphs[skip:]
 for source_p in paragraphs:
  value=re.sub(r'\s+',' ',source_p.get_text(' ',strip=True))
  if not value or re.fullmatch(r'\d+',value):continue
  p=out.new_tag('p');p.string=value;article.append(p)
# Join text physically split across pages when the next line is a continuation.
for p in list(article.find_all('p',recursive=False)):
 prev=p.find_previous_sibling()
 if prev and prev.name=='p':
  left,right=prev.get_text(' ',strip=True),p.get_text(' ',strip=True)
  if left and right and not re.search(r'[.!?:;”"\)]$',left) and (re.match(r'^[a-z]',right) or left.endswith(',') and re.match(r'^[A-Z]',right)):
   prev.string=left+' '+right;p.decompose()
# The delivered PDF repeats most of Chapter Four across pages 23–24.
# Retain the first complete passage and remove only its second occurrence.
repeated='Pseudoscience encompasses claims, beliefs, or practices'
paragraphs=[p for p in article.find_all('p',recursive=False) if repeated in p.get_text(' ',strip=True)]
assert len(paragraphs)==2, len(paragraphs)
duplicate=paragraphs[1]
value=duplicate.get_text(' ',strip=True)
assert value.count(repeated)==1
assert value.endswith('advances made through systematic research and technological progress.')
duplicate.string=value[:value.index(repeated)].rstrip()
assert len(sections)==10
text=article.get_text(' ',strip=True)
assert 'outfinitygift' not in text.lower()
(root/'book/en/full_content.html').write_text(str(out)+'\n')
(root/'qa').mkdir(exist_ok=True)
(root/'qa/source-selection.json').write_text(json.dumps({'source':'income/Flat_Earth_Theory___Scientific_Rebuttal_and_Modern_Persistence/content.pdf','retainedPdfPages':kept,'excludedPdfPages':list(range(1,7))+list(range(50,56)),'reason':'Keep original introduction, seven chapters, conclusion and bibliography; exclude old rights, promotional preface, and former-project annexes.','sections':sections,'readerWords':len(text.split())},ensure_ascii=False,indent=2)+'\n')
print('Prepared original reader',len(text.split()),'words')
