import json,re
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).parent
draft=BeautifulSoup(Path('.book-work/income-pdf-candidates/6635c36d54a18297/clean-draft.html').read_text(),'html.parser')
title='Futuristic Farm of Digital Delights'
subtitle='Software Companies Explained for Dummies'
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title></head><body><article data-reader-content></article></body></html>','html.parser')
out.title.string=title;article=out.article
h=out.new_tag('h1',id='book-title');h.string=title;article.append(h)
h=out.new_tag('p');h['class']='subtitle';h.string=subtitle;article.append(h)
heads={10:'Because True Programmers Start Counting from Zero',13:'A Futuristic Farm of Digital Delights',22:'Decoding the Software Engineer',29:'The Robo-Roosters',36:'The Holographic Sheepdogs aka Project Managers',42:'Quality Assurance in the Digital Savannah',49:'The Holographic Butterflies',56:'The Digital Ghosts',62:'The Drone Swarms',69:'The AI-Enhanced Scarecrows',76:'The lost Art of Digital Dream-Weaving',83:'The Weather Control System as Digital Divination',91:'The Ecosystem Symphony',97:'The Harvest Festival',103:'The Digital Compost Heap',109:'The Quantum Fields',115:'The Digital Singularity: When Farm Meets Future',121:'Reflections from the Farm'}
sections=[]
for page in range(10,126):
 sec=draft.select_one(f'section[data-source-page="{page}"]');assert sec,page
 paras=[re.sub(r'\s+',' ',p.get_text(' ',strip=True)).strip() for p in sec.find_all('p',recursive=False)]
 paras=[p for p in paras if p and not re.fullmatch(r'\d+',p)]
 if page in heads:
  name=heads[page];num=list(heads).index(page)
  label=(f'Chapter {num} — ' if num else '')+name
  h=out.new_tag('h2',id=f'section-{num+1}');h.string=label;article.append(h)
  sections.append({'id':h['id'],'title':label,'sourcePdfPage':page})
  if num:
   assert paras.pop(0).startswith('Chapter '),(page,paras[:2]);assert paras.pop(0)==name,(page,paras[:2])
  else:assert paras.pop(0)==name
 for value in paras:
  value=value.replace('*','')
  p=out.new_tag('p');p.string=value;article.append(p)
# Rejoin fragments broken by a source page while preserving complete paragraphs.
for p in list(article.find_all('p',recursive=False)):
 prev=p.find_previous_sibling()
 if prev and prev.name=='p' and 'subtitle' not in prev.get('class',[]):
  left=prev.get_text(' ',strip=True);right=p.get_text(' ',strip=True)
  if left and right and (not re.search(r'[.!?:;”"\)]$',left) or re.match(r'^[a-z]',right)):
   prev.string=left+' '+right;p.decompose()
# Keep translation units readable without paraphrasing original sentences.
for p in list(article.find_all('p',recursive=False)):
 value=p.get_text(' ',strip=True)
 if len(value.split())<=220:continue
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',value)
 if len(sentences)<3:continue
 groups=[];g=[];count=0
 for sentence in sentences:
  n=len(sentence.split())
  if g and count+n>155:groups.append(' '.join(g));g=[];count=0
  g.append(sentence);count+=n
 if g:groups.append(' '.join(g))
 if len(groups)>1:
  for txt in groups:
   node=out.new_tag('p');node.string=txt;p.insert_before(node)
  p.decompose()
body=article.get_text(' ',strip=True)
assert len(body.split())>18000,len(body.split())
assert len(article.find_all('h2'))==18
assert not any(x in body.lower() for x in ('outfinitygift','outfinity gift','outfinitygift.com'))
assert '*' not in body
path=root/'book/en/full_content.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(str(out)+'\n')
qa=root/'qa';qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({'source':'income/Futuristic_Farm_of_Digital_Delights/content.pdf','retainedPdfPages':list(range(10,126)),'excludedPdfPages':list(range(1,10))+list(range(126,134)),'reason':'Preserve the original opening and seventeen substantive chapters; exclude rights, contents, retired-project promotional preface and annex.','sections':sections,'readerWords':len(body.split()),'sourceTitlePage':2,'sourceAuthor':'AI Agent Eliona Mind (2024)'},ensure_ascii=False,indent=2)+'\n')
print('Futuristic Farm EN full',len(body.split()),'words',len(sections),'sections')
