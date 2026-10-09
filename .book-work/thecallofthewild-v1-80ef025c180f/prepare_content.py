import json,re
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).parent
draft=BeautifulSoup(Path('.book-work/income-pdf-candidates/80ef025c180fe162/clean-draft.html').read_text(encoding='utf-8'),'html.parser')
title='The Call of the Wild'
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title></head><body><article data-reader-content></article></body></html>','html.parser')
out.title.string=title
article=out.article;h1=out.new_tag('h1',id='book-title');h1.string=title;article.append(h1)
main={6:'AI Perspective — About Jack London',9:'Historical and Cultural Context',13:'Main Characters',18:'Plot Summary by Narrative Threads',22:'Chapter I — Into the Primitive',34:'Chapter II — The Law of Club and Fang',44:'Chapter III — The Dominant Primordial Beast',60:'Chapter IV — Who Has Won to Mastership',70:'Chapter V — The Toil of Trace and Trail',87:'Chapter VI — For the Love of a Man',102:'Chapter VII — The Sounding of the Call'}
subheadings={'Buck - The Protagonist','John Thornton','Perrault and François','Hal, Charles, and Mercedes','Spitz','The Other Dogs','The Wild Wolf','From Civilization to Wilderness: The Opening Thread','Learning the Ways of the North','The Trials of Survival','The Bond with Thornton'}
chapters={22,34,44,60,70,87,102};sections=[]
kept=list(range(6,21))+list(range(22,121))
for page in kept:
 sec=draft.select_one(f'section[data-source-page="{page}"]');assert sec,page
 parts=[re.sub(r'\s+',' ',p.get_text(' ',strip=True)).strip() for p in sec.find_all('p',recursive=False)]
 parts=[p for p in parts if p and not re.fullmatch(r'\d+',p) and p!='THE END']
 if page in main:
  heading=main[page]
  h=out.new_tag('h2',id=f'section-{len(sections)+1}');h.string=heading;article.append(h)
  sections.append({'id':h['id'],'title':heading,'sourcePage':page})
  if page==6:
   assert parts[0]=='AI Perspective About Jack London';parts.pop(0)
  elif page in (9,13,18):
   assert parts[0].lower()==heading.lower();parts.pop(0)
  else:
   assert parts[0].startswith('Chapter ');parts.pop(0)
   subtitle=heading.split(' — ',1)[1]
   assert parts[0].startswith(subtitle),(page,parts[0][:90],subtitle)
   parts[0]=parts[0][len(subtitle):].strip()
   parts=[p for p in parts if p]
 for value in parts:
  if value in subheadings and page<21:
   h=out.new_tag('h3',id='subsection-'+str(len(article.find_all('h3'))+1));h.string=value;article.append(h)
  elif page==22 and value.startswith('“Old longings nomadic leap,'):
   quote=out.new_tag('blockquote');quote.string=value;article.append(quote)
  else:
   p=out.new_tag('p');p.string=value;article.append(p)
# Reflow a paragraph interrupted by a source page boundary, retaining chapter
# and perspective headings as barriers.
for p in list(article.find_all('p',recursive=False)):
 prev=p.find_previous_sibling()
 if prev and prev.name=='p':
  left,right=prev.get_text(' ',strip=True),p.get_text(' ',strip=True)
  if left and right and (not re.search(r'[.!?:;”"\)]$',left) or re.match(r'^[a-z]',right)):
   prev.string=left+' '+right;p.decompose()
# Split only very long extracted paragraphs at sentence boundaries.
for p in list(article.find_all('p',recursive=False)):
 value=p.get_text(' ',strip=True)
 if len(value.split())<=230:continue
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',value)
 if len(sentences)<3:continue
 groups=[];group=[];words=0
 for sentence in sentences:
  count=len(sentence.split())
  if group and words+count>170:
   groups.append(' '.join(group));group=[];words=0
  group.append(sentence);words+=count
 if group:groups.append(' '.join(group))
 if len(groups)>1:
  for text in groups:
   node=out.new_tag('p');node.string=text;p.insert_before(node)
  p.decompose()
body=article.get_text(' ',strip=True)
assert len(body.split())>30000,len(body.split())
assert len(article.find_all('h2'))==11
assert not any(term in body.lower() for term in ('outfinitygift','outfinity gift','original book white fang','about ai author'))
target=root/'book/en/full_content.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(str(out)+'\n',encoding='utf-8')
qa=root/'qa';qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({'source':'income/The_Call_of_the_Wild/content.pdf','retainedPdfPages':kept,'excludedPdfPages':list(range(1,6))+[21]+list(range(121,127)),'reason':'Preserve the substantive AI Perspective and the complete seven-chapter Jack London narrative. Remove retired rights, promotional preface, contents, false inserted title leaf and former-project annex.','sourceDefects':['PDF page 21 incorrectly labels the original Buck narrative as WHITE FANG; the seven chapters are The Call of the Wild, so omit only that false title leaf.'],'sections':sections,'readerWords':len(body.split())},ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(body.split()),'words in',len(sections),'sections')
