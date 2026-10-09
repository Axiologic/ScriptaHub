from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

w=Path(__file__).resolve().parent
source=Path('.book-work/income-pdf-candidates/f10df726833a8f2e/clean-draft.html')
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('introduction','Introduction',8,12),
 ('crisis-code','Chapter I — Cracking the Crisis Code',13,17),
 ('historic-crises','Chapter II — History’s Biggest Financial Fiascos',18,23),
 ('intervention','Chapter III — The Balancing Act of Intervention',24,30),
 ('central-banking','Chapter IV — The Global Ripple Effects of Central Banking',31,37),
 ('conclusion','Conclusion — The Mirage of Stability',38,42),
 ('bibliography','Bibliography',51,51),
]
headings={'Introduction','Bibliography','Chapter I Cracking the Crisis Code','Chapter II History’s Biggest Financial Fiascos','Chapter III The Balancing Act of Intervention','Chapter IV The Global Ripple Effects of Central Banking','CONCLUSION The Mirage of Stability'}
parts=[];records=[]
for slug,heading,first,last in sections:
 paragraphs=[]
 for page in range(first,last+1):
  node=soup.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip()
   if not value or value in headings or value in {str(page),str(page-1)}:continue
   if slug!='bibliography' and paragraphs and not re.search(r'[.!?][”"’\']?$',paragraphs[-1]) and not paragraphs[-1].endswith(':'):paragraphs[-1]+=' '+value
   else:paragraphs.append(value)
 if slug=='conclusion':
  paragraphs=[paragraph.split('For more knowledge,',1)[0].strip() for paragraph in paragraphs]
  paragraphs=[paragraph for paragraph in paragraphs if paragraph]
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
title='The Mirage of Stability in Financial Crisis'
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Agent Zach Lawsone · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':51,'includedPages':[[8,42],[51,51]],'excludedPages':[[1,7],[43,50]],'reason':'Retained thematic introduction, four original chapters, substantive conclusion and bibliography; excluded rights, contents, promotional preface, old-project author/letter annexes and advertising.','sections':records},indent=2)+'\n')
print(records)
