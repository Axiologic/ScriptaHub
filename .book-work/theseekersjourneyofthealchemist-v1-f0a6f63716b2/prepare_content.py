from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re

root=Path('.book-work/theseekersjourneyofthealchemist-v1-f0a6f63716b2')
source=next(Path('.book-work/income-pdf-candidates').glob('f0a6f63716b2*/clean-draft.html'))
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('following-dreams','Chapter One — Following Dreams Against All Odds',7,11),
 ('lessons-of-the-journey','Chapter Two — The Lessons of the Journey',12,17),
 ('power-of-belief','Chapter Three — The Power of Belief',18,23),
 ('treasure-inside','Chapter Four — Treasure Inside',24,28),
]
headings={'Chapter One','Following Dreams Against All Odds','Chapter Two','The Lessons of the Journey','Chapter Three','The Power of Belief','Chapter Four','Treasure inside','Conclusion'}
records=[];html_sections=[]
for sid,label,start,end in sections:
 paras=[]
 for page in range(start,end+1):
  node=soup.find('section',attrs={'data-source-page':str(page)});assert node,page
  texts=[p.get_text(' ',strip=True) for p in node.find_all('p')]
  texts=[t for t in texts if t not in headings|{str(page)}]
  for i,t in enumerate(texts):
   if i==0 and paras and not re.search(r'[.!?][”\'\"]?$',paras[-1]):paras[-1]+=' '+t
   else:paras.append(t)
 records.append({'id':sid,'pages':[start,end],'paragraphs':len(paras),'words':sum(len(p.split()) for p in paras)})
 html_sections.append('<section id="%s"><h2>%s</h2>\n%s\n</section>'%(sid,escape(label),'\n'.join('<p>%s</p>'%escape(p) for p in paras)))
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>The Seeker’s Journey of the Alchemist</title></head><body><article>\n<h1>The Seeker’s Journey of the Alchemist</h1>\n'+'\n'.join(html_sections)+'\n</article></body></html>\n'
(root/'book/en/full_content.html').write_text(html)
(root/'qa').mkdir(exist_ok=True)
(root/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'includedPages':[7,28],'excludedPages':[[1,6],[29,38]],'reason':'Four substantive chapters retained; promotional preface, front matter, generic recommendation pages, author promotion and bibliography excluded.','sections':records},indent=2)+'\n')
print(records)
