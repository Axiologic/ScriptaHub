"""Retain Barrie's novel and the delivery's substantive editorial perspective."""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root=Path(__file__).resolve().parent
draft=BeautifulSoup(Path('.book-work/income-pdf-candidates/edb55e5b4f87ecbe/clean-draft.html').read_text(),'html.parser')
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Peter Pan</title></head><body><article data-reader-content></article></body></html>','html.parser')
article=out.article
h=out.new_tag('h1',id='book-title');h.string='Peter Pan';article.append(h)
perspective={8:'About James Matthew Barrie',11:'Historical and Cultural Context',15:'Main Characters',20:'Plot Summary by Narrative Threads'}
chapters={27:'Peter Breaks Through',37:'The Shadow',48:'Come Away, Come Away!',64:'The Flight',75:'The Island Come True',87:'The Little House',97:'The Home Under the Ground',103:'The Mermaids’ Lagoon',117:'The Never Bird',121:'The Happy Home',129:'Wendy’s Story',139:'The Children Are Carried Off',145:'Do You Believe in Fairies?',155:'The Pirate Ship',164:'“Hook or Me This Time”',175:'The Return Home',185:'When Wendy Grew Up'}
roman=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII']
pages=list(range(8,26))+list(range(27,198))
sections=[]
def heading(tag,value,page):
 id=f'section-{len(sections)+1}' if tag=='h2' else f'subsection-{page}'
 node=out.new_tag(tag,id=id);node.string=value;article.append(node)
 sections.append({'id':id,'title':value,'sourcePage':page})
for page in pages:
 source=draft.select_one(f'section[data-source-page="{page}"]')
 assert source,page
 parts=[re.sub(r'\s+',' ',p.get_text(' ',strip=True)).strip() for p in source.find_all('p',recursive=False)]
 parts=[p for p in parts if p and not re.fullmatch(r'\d+',p) and p!='THE END']
 if not parts: continue
 if page==8:
  assert parts[0]=='AI Perspective About James Mattew Barrie'
  parts.pop(0);heading('h2','AI Perspective',page);heading('h3',perspective[page],page)
 elif page in perspective:
  label={11:'Historical and cultural context',15:'Main Characters',20:'Plot Summary by Narrative Threads'}[page]
  assert parts[0].startswith(label),(page,parts[0][:80])
  parts[0]=parts[0][len(label):].strip();heading('h3',perspective[page],page)
 elif page in chapters:
  idx=list(chapters).index(page)
  assert parts[0]==f'Chapter {roman[idx]}',(page,parts[0])
  assert parts[1].casefold()==chapters[page].casefold(),(page,parts[1])
  parts=parts[2:];heading('h2',f'Chapter {roman[idx]} — {chapters[page]}',page)
 for value in parts:
  if not value: continue
  node=out.new_tag('p');node.string=value;article.append(node)

# The PDF export can split a sentence at a page edge. Join only the exact
# continuation; keep authorial paragraphs and dialogue otherwise.
for node in list(article.find_all('p',recursive=False)):
 prev=node.find_previous_sibling()
 if prev and prev.name=='p':
  left,right=prev.get_text(' ',strip=True),node.get_text(' ',strip=True)
  if left and right and (not re.search(r'[.!?:;”"’\)]$',left) or re.match(r'^[a-z]',right)):
   prev.string=left+' '+right;node.decompose()

# Keep translation units readable even where the PDF layout merged several
# authorial paragraphs into a page-sized block.
for node in list(article.find_all('p',recursive=False)):
 value=node.get_text(' ',strip=True)
 if len(value.split())<=190: continue
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“‘])',value)
 if len(sentences)<3: continue
 groups=[];group=[];words=0
 for sentence in sentences:
  n=len(sentence.split())
  if group and words+n>145:
   groups.append(' '.join(group));group=[];words=0
  group.append(sentence);words+=n
 if group: groups.append(' '.join(group))
 if len(groups)>1:
  for value in groups:
   part=out.new_tag('p');part.string=value;node.insert_before(part)
  node.decompose()

body=article.get_text(' ',strip=True)
assert len(body.split())>40000,len(body.split())
assert len(article.find_all('h2'))==18
assert not any(x in body.lower() for x in ('outfinity','about ai author','all rights reserved'))
target=root/'book/en/full_content.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(str(out)+'\n')
qa=root/'qa';qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({
 'source':'income/Peter_Pan/content.pdf','retainedPdfPages':pages,
 'excludedPdfPages':list(range(1,8))+[26]+list(range(198,202)),
 'reason':'Retain the substantive AI Perspective and all 17 chapters of J. M. Barrie’s novel. Exclude rights, TOC, promotional preface, retired-edition title leaf, and author/project promotional annex.',
 'sections':sections,'readerWords':len(body.split())
},ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(body.split()),'words in',len(sections),'sections')
