from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
w=Path(__file__).resolve().parent;source=Path('.book-work/income-pdf-candidates/7d866fc6ab2ae260/clean-draft.html');soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[('introduction','Introduction',8,10),('other-planets','Chapter One — The Kaleidoscope Beyond: Sky Colors on Other Planets',11,15),('blue-sky','Chapter Two — The Blue Sky Phenomenon',16,20),('light-dispersion','Chapter Three — The Physics of Light Dispersion',21,24),('sky-variation','Chapter Four — Variations in Sky Color',25,29),('pollution','Chapter Five — Atmospheric Pollution and Sky Color',30,37),('climate-weather','Chapter Six — Climate and Weather Effects on Sky Appearance',38,45),('seasonal-variation','Chapter Seven — Seasonal Variations in Sky Color',46,50),('planetary-skies','Chapter Eight — Sky Colors on Other Planets',51,55),('measurement','Chapter Nine — Observing and Measuring Sky Color',56,60),('culture-art','Chapter Ten — The Cultural and Artistic Significance of Sky Colors',61,66),('future-sky','Chapter Eleven — Future Changes in Earth’s Sky',67,70),('conclusion','Conclusion',71,74),('bibliography','Bibliography',81,82)]
headings={'Introduction','Chapter One The Kaleidoscope Beyond Sky Colors on Other Planets','Chapter Two The Blue Sky Phenomenon','Chapter Three The Physics of Light Dispersion','Chapter Four Variations in Sky Color','Chapter Five Atmospheric Pollution and Sky Color','Chapter Six Climate and Weather Effects on Sky Appearance','Chapter Seven Seasonal Variations in Sky Color','Chapter Eight Sky Colors on Other Planets','Chapter Nine Observing and Measuring Sky Color','Chapter Ten The Cultural and Artistic Significance of Sky Colors','Chapter Eleven Future Changes in Earth\'s Sky','Conclusion','Bibliography'}
headings.update({'Chapter One','Chapter Two','Chapter Three','Chapter Four','Chapter Five','Chapter Six','Chapter Seven','Chapter Eight','Chapter Nine','Chapter Ten','The Kaleidoscope Beyond Sky Colors on Other Planets','The Blue Sky Phenomenon','The Physics of Light Dispersion','Variations in Sky Color','Atmospheric Pollution and Sky Color','Climate and Weather Effects on Sky Appearance','Seasonal Variations in Sky Color','Sky Colors on Other Planets','Observing and Measuring Sky Color','The Cultural and Artistic Significance of Sky Colors'})
parts=[];records=[]
for slug,heading,first,last in sections:
 paragraphs=[]
 for page in range(first,last+1):
  node=soup.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip().replace('**','')
   value=re.sub(rf'\s+{page-1}$','',value)
   for source_heading in sorted(headings,key=len,reverse=True):
    if value.startswith(source_heading+' '):
     value=value[len(source_heading):].strip()
     break
   if not value or value in headings or re.fullmatch(r'\d{1,2}',value):continue
   if slug!='bibliography' and paragraphs and not re.search(r'[.!?][”"’\']?$',paragraphs[-1]) and not paragraphs[-1].endswith(':') and not re.match(r'^\d{1,2}\.\s',value):paragraphs[-1]+=' '+value
   else:paragraphs.append(value)
 readable=[]
 for paragraph in paragraphs:
  if len(paragraph.split())<=150 or slug=='bibliography':readable.append(paragraph);continue
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',paragraph);group=[]
  for sentence in sentences:
   if group and sum(len(x.split()) for x in group)+len(sentence.split())>150:readable.append(' '.join(group));group=[]
   group.append(sentence)
  if group:readable.append(' '.join(group))
 records.append({'id':slug,'pages':[first,last],'paragraphs':len(readable),'words':sum(len(x.split()) for x in readable)})
 parts.append('<section id="'+slug+'"><h2>'+escape(heading)+'</h2>\n'+'\n'.join('<p>'+escape(x)+'</p>' for x in readable)+'\n</section>')
title='Planetary Sky: Understanding the Colors Above Us'
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Agent Althea Zappa · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html);(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':82,'includedPages':[[8,74],[81,82]],'excludedPages':[[1,7],[75,80]],'reason':'Retained original introduction, eleven chapters, conclusion and bibliography; excluded rights, contents, promotional preface and old-project author annexes.','editorialNote':'Chapter one and chapter eight both discuss other planets but are not textual duplicates; the former is imaginative and the latter more observational.','sections':records},ensure_ascii=False,indent=2)+'\n')
print(records)
