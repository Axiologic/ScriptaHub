from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
w=Path(__file__).resolve().parent
source=Path('.book-work/income-pdf-candidates/8db385f98ceeb4bb/clean-draft.html')
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('introduction','Introduction',8,11),
 ('sophons','Chapter One — The Limits of Sophons: Is There Something Even More Advanced?',12,15),
 ('science-politics','Chapter Two — The Clash of Science and Politics',16,19),
 ('alien-threats','Chapter Three — Survival Instincts: Humanity Confronting Alien Threats',20,25),
 ('repeated-cycles','Chapter Four — From History to the Stars: Survival in Repeated Cycles',26,31),
 ('dark-forest','Chapter Five — The Dark Forest Theory: A New Understanding of the Universe',32,37),
 ('adventures','Chapter Six — Adventures in the Three-Body Universe',38,41),
 ('legacy','Chapter Seven — The Legacy and the Impact on Science Fiction',42,45),
 ('conclusion','Conclusion',46,46),
 ('bibliography','Bibliography',53,53),
]
headings={'Introduction','Conclusion','Bibliography','Chapter One','Chapter Two','Chapter Three','Chapter Four','Chapter Five','Chapter Six','Chapter Seven','The Limits of Sophons: Is There Something Even More Advanced?','The Clash of Science and Politics','Survival Instincts: Humanity Confronting Alien Threats','From History to the Stars: Survival in Repeated Cycles','The Dark Forest Theory: A New Understanding of the Universe','Adventures in the Three-Body Universe','The Legacy and the Impact on Science Fiction'}
parts=[];records=[]
for slug,heading,first,last in sections:
 paragraphs=[]
 for page in range(first,last+1):
  node=soup.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip()
   if not value or value in headings or re.fullmatch(r'\d{1,2}',value):continue
   value=value.replace('n resilience and adaptability.', 'Resilience and adaptability.').replace('all civilization,, civilizations', 'all civilizations; civilizations').replace('remains constant, It', 'remains constant; it')
   if slug!='bibliography' and paragraphs and not re.search(r'[.!?][”"’\']?$',paragraphs[-1]) and not paragraphs[-1].endswith(':'):paragraphs[-1]+=' '+value
   else:paragraphs.append(value)
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
title='Navigating the Three-Body Problem Universe'
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Agent Astraeon Nova · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':53,'includedPages':[[8,46],[53,53]],'excludedPages':[[1,7],[47,52]],'reason':'Retained original introduction, seven analytical chapters, conclusion and bibliography; excluded rights, contents, promotional preface, and old-project annexes/advertising.','sections':records},indent=2)+'\n')
print(records)
