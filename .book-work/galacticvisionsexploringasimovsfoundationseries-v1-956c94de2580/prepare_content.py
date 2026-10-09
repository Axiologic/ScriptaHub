from pathlib import Path
from bs4 import BeautifulSoup
import json,re
root=Path(__file__).parent
source=BeautifulSoup(Path('.book-work/income-pdf-candidates/956c94de25805176/clean-draft.html').read_text(),'html.parser')
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Galactic Visions: Exploring Asimov’s Foundation Series</title></head><body><article data-reader-content></article></body></html>','html.parser')
article=out.article
h1=out.new_tag('h1',id='book-title');h1.string='Galactic Visions: Exploring Asimov’s Foundation Series';article.append(h1)
by=out.new_tag('p');by['class']='book-byline';by.string='AI Agent Elarise Synthia';article.append(by)
heads={8:('Introduction',1),10:('Chapter 1 — Psychohistory: Science or Art',2),14:('Chapter 2 — Historical Determinism',2),19:('Chapter 3 — The Decline and Rebirth of Civilizations',2),26:('Chapter 4 — Politics and Manipulation',2),33:('Chapter 5 — Imperial Decline and the Power of Knowledge',2),50:('Chapter 6 — Key Events and Plot Summaries',2),54:('Conclusion',1),63:('Bibliography',1)}
kept=list(range(8,56))+[63];sections=[]
for page in kept:
 sec=source.select_one(f'section[data-source-page="{page}"]');assert sec,page
 paras=sec.find_all('p',recursive=False)
 if page in heads:
  label,skip=heads[page];ident='introduction' if page==8 else 'conclusion' if page==54 else 'bibliography' if page==63 else f'chapter-{len([x for x in sections if x["id"].startswith("chapter-")])+1}'
  h=out.new_tag('h2',id=ident);h.string=label;article.append(h);sections.append({'id':ident,'title':label,'page':page});paras=paras[skip:]
 for item in paras:
  value=re.sub(r'\s+',' ',item.get_text(' ',strip=True))
  if not value or re.fullmatch(r'\d+',value):continue
  p=out.new_tag('p');p.string=value;article.append(p)
# Rejoin sentences physically split at PDF page boundaries.
for p in list(article.find_all('p',recursive=False)):
 prev=p.find_previous_sibling()
 if prev and prev.name=='p':
  left,right=prev.get_text(' ',strip=True),p.get_text(' ',strip=True)
  if left and right and not re.search(r'[.!?:;”"\)]$',left) and (re.match(r'^[a-z]',right) or left.endswith(',') and re.match(r'^[A-Z]',right)):
   prev.string=left+' '+right;p.decompose()
# PDF pp17–18 contain an irrecoverably truncated sentence ending “inspired numerous”.
# Discard this damaged sentence without inventing the missing object.
for p in article.find_all('p',recursive=False):
 value=p.get_text(' ',strip=True)
 if 'The idea that the future can be predicted and manipulated through scientific analysis of human behavior has inspired numerous' in value:
  p.string=value.replace('The idea that the future can be predicted and manipulated through scientific analysis of human behavior has inspired numerous','').strip()
assert len(sections)==9
text=article.get_text(' ',strip=True);assert 'outfinitygift' not in text.lower()
(root/'book/en/full_content.html').write_text(str(out)+'\n')
(root/'qa').mkdir(exist_ok=True)
(root/'qa/source-selection.json').write_text(json.dumps({'source':'income/Galactic_Visions___Exploring_Asimov_s_Foundation_Series/content.pdf','retainedPdfPages':kept,'excludedPdfPages':list(range(1,8))+list(range(56,63)),'reason':'Original introduction, six chapters, conclusion and bibliography retained; old rights, promotional preface, project annex and letter excluded.','sourceCorrection':'Unfinished sentence at pp17–18 ending “inspired numerous” removed without supplying invented content.','sections':sections,'readerWords':len(text.split())},ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(text.split()),'words')
