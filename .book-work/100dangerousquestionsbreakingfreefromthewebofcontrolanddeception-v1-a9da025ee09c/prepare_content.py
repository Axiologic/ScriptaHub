from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re

work=Path(__file__).resolve().parent
source=Path('.book-work/income-pdf-candidates/a9da025ee09cb181/clean-draft.html')
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('society-culture','Chapter One — Society and Culture',14,20),
 ('love-relationships','Chapter Two — Love and Relationships',21,29),
 ('economy-work','Chapter Three — Economy and Work',30,38),
 ('religion-belief','Chapter Four — Religion and Belief Systems',39,47),
 ('self-existence','Chapter Five — Self and Existence',48,56),
 ('power-structures','Chapter Six — Society and Power Structures',57,65),
 ('social-norms','Chapter Seven — Human Relationships and Social Norms',66,74),
 ('work-wealth','Chapter Eight — Work, Economy, and Wealth',75,83),
 ('spirituality-morality','Chapter Nine — Religion, Spirituality, and Morality',84,96),
 ('technology-media','Chapter Ten — Technology, Media, and Information',97,106),
 ('conclusion','Conclusion',107,109),
]
headings={x for pair in [('CHAPTER ONE','Society and Culture'),('CHAPTER TWO','Love, Relationships'),('CHAPTER THREE','Economy and Work'),('CHAPTER FOUR','Religion and Belief Systems'),('CHAPTER FIVE','Self and Existence'),('CHAPTER SIX','Society and Power Structures'),('CHAPTER SEVEN','Human Relationships and Social Norms'),('CHAPTER EIGHT','Work, Economy, and Wealth'),('CHAPTER NINE','Religion, Spirituality, and Morality'),('CHAPTER TEN','Technology, Media, and Information')] for x in pair}|{'CONCLUSION'}
parts=[];records=[]
for slug,heading,first,last in sections:
 paragraphs=[]
 for page in range(first,last+1):
  node=soup.find('section',{'data-source-page':str(page)});assert node,page
  for element in node.select('p'):
   value=re.sub(r'\s+',' ',element.get_text(' ',strip=True)).strip()
   if not value or value in headings or value in {str(page),str(page-1)}:continue
   if paragraphs and not re.search(r'[.!?][”"’\']?$',paragraphs[-1]) and not paragraphs[-1].endswith(':'):
    paragraphs[-1]+=' '+value
   else:paragraphs.append(value)
 readable=[]
 for paragraph in paragraphs:
  if len(paragraph.split())<=140:readable.append(paragraph);continue
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',paragraph);group=[]
  for sentence in sentences:
   if group and sum(len(x.split()) for x in group)+len(sentence.split())>140:
    readable.append(' '.join(group));group=[]
   group.append(sentence)
  if group:readable.append(' '.join(group))
 paragraphs=readable
 records.append({'id':slug,'pages':[first,last],'paragraphs':len(paragraphs),'words':sum(len(x.split()) for x in paragraphs)})
 parts.append('<section id="'+slug+'"><h2>'+escape(heading)+'</h2>\n'+'\n'.join('<p>'+escape(x)+'</p>' for x in paragraphs)+'\n</section>')
title='100 Dangerous Questions: Breaking Free from the Web of Control and Deception'
output='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(work/'book/en/full_content.html').write_text(output)
(work/'qa').mkdir(exist_ok=True)
(work/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'includedPages':[[14,109]],'excludedPages':[[1,13],[110,115]],'reason':'Retained ten question chapters and substantive conclusion; excluded rights, contents, promotional preface/introduction, and former-project annexes.','sections':records},indent=2)+'\n')
print(records)
