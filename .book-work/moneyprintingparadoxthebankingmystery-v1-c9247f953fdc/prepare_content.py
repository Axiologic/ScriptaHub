from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
w=Path(__file__).resolve().parent
source=Path('.book-work/income-pdf-candidates/c9247f953fdc25bb/clean-draft.html')
s=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('origins','Chapter I — The Origins of Money Printing',13,25),
 ('cost','Chapter II — The Cost of Money Printing',26,33),
 ('central-banks','Chapter III — Central Banks: The Architects of Money Manipulation',34,41),
 ('reform','Chapter IV — Reforming the Banking System: A Call for Change',42,50),
 ('conclusion','Conclusion — Money Printing Paradox',51,55),
 ('bibliography','Bibliography',65,65),
]
heads={x[1].replace(' — ',' ') for x in sections}|{'Chapter I The Origins of Money Printing','Chapter II The Cost of Money Printing','Chapter III Central Banks: The Architects of Money Manipulation','Chapter IV Reforming the Banking System: A Call for Change','Conclusion Money Printing Paradox','Bibliography'}
parts=[];records=[]
for slug,heading,first,last in sections:
 paras=[]
 for page in range(first,last+1):
  node=s.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip()
   if not value or value in heads or value in {str(page),str(page-1)}:continue
   if page==55 and 'For a deeper understanding of the principles' in value:
    value=value.split('For a deeper understanding of the principles')[0].strip()
   if not value:continue
   if paras and slug!='bibliography' and not re.search(r'[.!?][”"’\']?$',paras[-1]) and not paras[-1].endswith(':'):
    paras[-1]+=' '+value
   else:paras.append(value)
 readable=[]
 for paragraph in paras:
  if len(paragraph.split())<=130 or slug=='bibliography':readable.append(paragraph);continue
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',paragraph);group=[]
  for sentence in sentences:
   if group and sum(len(x.split()) for x in group)+len(sentence.split())>130:
    readable.append(' '.join(group));group=[]
   group.append(sentence)
  if group:readable.append(' '.join(group))
 records.append({'id':slug,'pages':[first,last],'paragraphs':len(readable),'words':sum(len(x.split()) for x in readable)})
 parts.append('<section id="'+slug+'"><h2>'+escape(heading)+'</h2>\n'+'\n'.join('<p>'+escape(x)+'</p>' for x in readable)+'\n</section>')
title='Money Printing Paradox: The Banking Mystery'
out='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Agent Zach Lawsone · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(out)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':65,'includedPages':[[13,55],[65,65]],'excludedPages':[[1,12],[56,64]],'reason':'Retained original four chapters, substantive conclusion, and bibliography; removed old rights, contents, promotional preface/introduction, book recommendation after the conclusion, and former-project annexes.','sections':records},indent=2)+'\n')
print(records)
