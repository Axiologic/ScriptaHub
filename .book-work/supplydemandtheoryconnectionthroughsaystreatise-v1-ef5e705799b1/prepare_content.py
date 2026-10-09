from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
w=Path(__file__).resolve().parent
source=Path('.book-work/income-pdf-candidates/ef5e705799b139aa/clean-draft.html')
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('introduction','Introduction',8,13),
 ('foundation','Chapter I — The Foundation of Economic Thought',14,18),
 ('entrepreneur','Chapter II — The Role of the Entrepreneur',19,24),
 ('supply-demand','Chapter III — The Dynamics of Supply and Demand',25,31),
 ('legacy','Chapter IV — Legacy and Relevance Today',32,37),
 ('conclusion','Conclusion',38,44),
 ('bibliography','Bibliography',54,54),
]
headings={'Introduction','Bibliography','Chapter I The Foundation of Economic Thought','Chapter II The Role of the Entrepreneur','Chapter III The Dynamics of Supply and Demand','Chapter IV Legacy and Relevance Today','Conclusion'}
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
  paragraphs=[p.split('Reading Jean-Baptiste Say',1)[0].strip() for p in paragraphs]
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
title='Supply-Demand Theory Connection Through Say’s Treatise'
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Agent Zach Lawsone · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':54,'includedPages':[[8,44],[54,54]],'excludedPages':[[1,7],[45,53]],'reason':'Retained substantive introduction, four original chapters, conclusion through its original analytical ending, and bibliography; excluded rights, contents, promotional preface, final reading recommendation, and old-project annexes/advertising.','sections':records},indent=2)+'\n')
print(records)
