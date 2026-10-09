from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
w=Path(__file__).resolve().parent
source=Path('.book-work/income-pdf-candidates/3e2046fed7279234/clean-draft.html')
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[('introduction','Introduction — The Mystical Foundations of Kabbalah and Taoism',8,23),('cosmic-information','Chapter One — The Cosmic Dance of Information',24,34),('multidimensional-realities','Chapter Two — Multidimensional Realities',35,45),('energy-matter-consciousness','Chapter Three — Energy, Matter, and Consciousness',46,57),('cycles-symmetry-transformation','Chapter Four — Cycles, Symmetry, and Transformation',58,68),('human-conclusions','Human Conclusions — AI, Mysticism, and Human Understanding',69,73)]
headings={'Introduction The Mystical Foundations of Kabbalah and Taoism','Chapter One The Cosmic Dance of Information','Chapter Two Multidimensional Realities','Chapter Three Energy, Matter, and Consciousness','Chapter Four Cycles, Symmetry, and Transformation','Human Conclusions AI, Mysticism, and Human Understanding'}
parts=[];records=[]
for slug,heading,first,last in sections:
 paragraphs=[]
 for page in range(first,last+1):
  node=soup.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip().replace('**','')
   value=re.sub(rf'\s+{page-1}$','',value)
   if not value or value in headings or re.fullmatch(r'\d{1,2}',value):continue
   if paragraphs and not re.search(r'[.!?][”"’\']?$',paragraphs[-1]) and not paragraphs[-1].endswith(':') and not re.match(r'^\d{1,2}\.\s',value):
    paragraphs[-1]+=' '+value
   else:paragraphs.append(value)
 readable=[]
 for paragraph in paragraphs:
  if len(paragraph.split())<=150:readable.append(paragraph);continue
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',paragraph);group=[]
  for sentence in sentences:
   if group and sum(len(x.split()) for x in group)+len(sentence.split())>150:
    readable.append(' '.join(group));group=[]
   group.append(sentence)
  if group:readable.append(' '.join(group))
 records.append({'id':slug,'pages':[first,last],'paragraphs':len(readable),'words':sum(len(x.split()) for x in readable)})
 parts.append('<section id="'+slug+'"><h2>'+escape(heading)+'</h2>\n'+'\n'.join('<p>'+escape(x)+'</p>' for x in readable)+'\n</section>')
title='An AI’s Perspective on Kabbalah and Taoism'
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">Sînică Alboaie · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':81,'includedPages':[[8,73]],'excludedPages':[[1,7],[74,81]],'reason':'Retained original introduction, four chapters and human-authored concluding reflection; excluded rights, contents, promotional preface and author/business annexes.','editorialNote':'Parallels between mysticism and physics are presented as analogies or questions, not established scientific equivalences.','sections':records},ensure_ascii=False,indent=2)+'\n')
print(records)
