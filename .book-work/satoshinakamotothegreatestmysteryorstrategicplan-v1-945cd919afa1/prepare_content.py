from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
w=Path(__file__).resolve().parent
source=Path('.book-work/income-pdf-candidates/945cd919afa1f4b1/clean-draft.html');soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[('introduction','Introduction',8,12),('usd-control','Chapter One — Global Control Through the USD',13,18),('oil-cryptocurrency','Chapter Two — Oil, Cryptocurrency, and the Petrodollar',19,24),('petrodollar-war','Chapter Three — The Petrodollar War',25,31),('petrodollar-disappearance','Chapter Four — Disappearance of the Petrodollar',32,38),('satoshi-mystery','Chapter Five — The Unsolvable Mystery of Satoshi Nakamoto',39,44),('conclusion','Conclusion — The Duality of Power and Freedom',45,50),('bibliography','Bibliography',57,57)]
headings={'INTRODUCTION','CHAPTER ONE','CHAPTER TWO','CHAPTER THREE','CHAPTER FOUR','CHAPTER FIVE','CONCLUSION','BIBLIOGRAPHY','Global Control Through the USD','Oil, Cryptocurrency, and the Petrodollar','The Petrodollar War','Disappearance of the Petrodollar','The Unsolvable Mystery of Satoshi Nakamoto','The Duality of Power and Freedom'}
parts=[];records=[]
for slug,heading,first,last in sections:
 paragraphs=[]
 for page in range(first,last+1):
  node=soup.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip().replace('**','')
   if not value or value in headings or re.fullmatch(r'\d{1,2}',value):continue
   if slug!='bibliography' and paragraphs and not re.search(r'[.!?][”"’\']?$',paragraphs[-1]) and not paragraphs[-1].endswith(':'):paragraphs[-1]+=' '+value
   else:paragraphs.append(value)
 readable=[]
 for paragraph in paragraphs:
  if len(paragraph.split())<=140 or slug=='bibliography':readable.append(paragraph);continue
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“*])',paragraph);group=[]
  for sentence in sentences:
   if group and sum(len(x.split()) for x in group)+len(sentence.split())>140:readable.append(' '.join(group));group=[]
   group.append(sentence)
  if group:readable.append(' '.join(group))
 records.append({'id':slug,'pages':[first,last],'paragraphs':len(readable),'words':sum(len(x.split()) for x in readable)})
 parts.append('<section id="'+slug+'"><h2>'+escape(heading)+'</h2>\n'+'\n'.join('<p>'+escape(x)+'</p>' for x in readable)+'\n</section>')
title='Satoshi Nakamoto: The Greatest Mystery or Strategic Plan'
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Agent Liora Riveers · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'sourceVersion':1,'sourcePages':57,'includedPages':[[8,50],[57,57]],'excludedPages':[[1,7],[51,56]],'reason':'Retained original introduction, five speculative chapters, conclusion and bibliography; excluded rights, contents, promotional preface and old-project annexes/advertising.','editorialNote':'Claims about Satoshi, the US and the petrodollar are the source author’s speculative analysis, not independently verified historical findings.','sections':records},indent=2)+'\n')
print(records)
