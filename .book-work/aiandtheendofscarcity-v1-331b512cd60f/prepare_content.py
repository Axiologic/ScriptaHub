from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
w=Path(__file__).resolve().parent
source=Path('.book-work/income-pdf-candidates/331b512cd60f99fb/clean-draft.html')
s=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('scarcity-economics','Chapter One — Understanding Scarcity in Economics',20,27),
 ('resource-limits','Chapter Two — The Role of AI in Overcoming Resource Limits',28,36),
 ('manufacturing','Chapter Three — AI and Automated Manufacturing',37,44),
 ('distribution','Chapter Four — AI and Resource Distribution',45,54),
 ('energy','Chapter Five — AI and Energy Scarcity',55,63),
 ('circular-economy','Chapter Six — AI-Driven Circular Economy',64,72),
 ('ethics','Chapter Seven — Ethical Considerations in AI-Driven Economies',73,82),
 ('post-scarcity','Chapter Eight — The Path to a Post-Scarcity World',83,92),
 ('conclusion','Conclusion',93,99),
]
headings={'Chapter One Understanding Scarcity in Economics','Chapter Two The Role of AI in Overcoming Resource Limits','Chapter Three AI and Automated Manufacturing','Chapter Four AI and Resource Distribution','Chapter Five AI and Energy Scarcity','Chapter Six AI-Driven Circular Economy','Chapter Seven Ethical Considerations in AI-Driven Economies','Chapter Eight The Path to a Post-Scarcity World','Conclusion'}
parts=[];records=[]
for slug,heading,first,last in sections:
 paragraphs=[]
 chapter_parts=heading.split(' — ',1)
 local_headings=set(chapter_parts)|{heading.replace(' — ',' ')}
 for page in range(first,last+1):
  node=s.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip()
   if not value or value in headings or value in local_headings or value in {str(page),str(page-1)}:continue
   if len(chapter_parts)==2 and value.startswith(chapter_parts[1]+' '):
    value=value[len(chapter_parts[1]):].strip()
   for source_heading in headings:
    if value.startswith(source_heading+' '):
     value=value[len(source_heading):].strip()
     break
   if not value:continue
   if paragraphs and not re.search(r'[.!?][”"’\']?$',paragraphs[-1]) and not paragraphs[-1].endswith(':'):
    paragraphs[-1]+=' '+value
   else:paragraphs.append(value)
 readable=[]
 for paragraph in paragraphs:
  if len(paragraph.split())<=145:readable.append(paragraph);continue
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',paragraph);group=[]
  for sentence in sentences:
   if group and sum(len(x.split()) for x in group)+len(sentence.split())>145:
    readable.append(' '.join(group));group=[]
   group.append(sentence)
  if group:readable.append(' '.join(group))
 records.append({'id':slug,'pages':[first,last],'paragraphs':len(readable),'words':sum(len(x.split()) for x in readable)})
 parts.append('<section id="'+slug+'"><h2>'+escape(heading)+'</h2>\n'+'\n'.join('<p>'+escape(x)+'</p>' for x in readable)+'\n</section>')
title='AI and The End of Scarcity'
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Personality Yason West · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':105,'includedPages':[[20,99]],'excludedPages':[[1,19],[100,105]],'reason':'Retained eight original chapters and substantive conclusion; excluded rights, contents, promotional preface/introduction, and former-project annexes.','sections':records},indent=2)+'\n')
print(records)
