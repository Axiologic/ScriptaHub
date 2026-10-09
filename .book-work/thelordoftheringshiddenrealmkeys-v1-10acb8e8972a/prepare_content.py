from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
w=Path(__file__).resolve().parent;source=Path('.book-work/income-pdf-candidates/10acb8e8972ab69d/clean-draft.html');soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('introduction','Introduction',9,12),
 ('shire-secret','Chapter One — The Shire’s Secret: A Hobbit’s Discovery',13,19),
 ('fellowship','Chapter Two — The Fellowship’s Quest: Assembling the Dream Team!',20,26),
 ('trials','Chapter Three — Trials of the Hidden Realm: Secrets and Sacrifices',27,32),
 ('revelation','Chapter Four — The Final Revelation: Light vs. Darkness',33,38),
 ('conclusion','Conclusion',39,42),
 ('bibliography','Bibliography',52,52),
]
headings={'Introduction','Conclusion','Bibliography','Chapter One','Chapter Two','Chapter Three','Chapter Four','The Shire’s Secret: A Hobbit’s','Discovery','The Fellowship’s Quest: Assembling','the Dream Team!','Trials of the Hidden Realm: Secrets','and Sacrifices','The Final Revelation: Light vs.','Darkness'}
parts=[];records=[]
for slug,heading,first,last in sections:
 paragraphs=[]
 for page in range(first,last+1):
  node=soup.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip()
   if not value or value in headings or value in {str(page),str(page-1),str(page-2)}:continue
   if slug!='bibliography' and paragraphs and not re.search(r'[.!?][”"’\']?$',paragraphs[-1]) and not paragraphs[-1].endswith(':'):paragraphs[-1]+=' '+value
   else:paragraphs.append(value)
 if slug=='conclusion':
  paragraphs=[p.split('As we conclude our exploration of The Lord of the Rings:',1)[0].strip() for p in paragraphs]
  paragraphs=[p for p in paragraphs if p]
 readable=[]
 for paragraph in paragraphs:
  if len(paragraph.split())<=135 or slug=='bibliography':readable.append(paragraph);continue
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“*])',paragraph);group=[]
  for sentence in sentences:
   if group and sum(len(x.split()) for x in group)+len(sentence.split())>135:readable.append(' '.join(group));group=[]
   group.append(sentence)
  if group:readable.append(' '.join(group))
 records.append({'id':slug,'pages':[first,last],'paragraphs':len(readable),'words':sum(len(x.split()) for x in readable)})
 parts.append('<section id="'+slug+'"><h2>'+escape(heading)+'</h2>\n'+'\n'.join('<p>'+escape(x)+'</p>' for x in readable)+'\n</section>')
title='The Lord of the Rings: Hidden Realm Keys'
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Agent Lyora Ember · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':52,'includedPages':[[9,42],[52,52]],'excludedPages':[[1,8],[43,51]],'reason':'Retained original introduction, four narrative chapters, substantive conclusion and bibliography; excluded rights, contents, promotional preface, final recommendation to consume source franchise, and old-project annexes/advertising.','sections':records},indent=2)+'\n')
print(records)
