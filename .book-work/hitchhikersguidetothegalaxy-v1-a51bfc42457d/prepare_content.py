from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re
root=Path('.book-work/hitchhikersguidetothegalaxy-v1-a51bfc42457d')
source=Path('.book-work/income-pdf-candidates/a51bfc42457d6aaa/clean-draft.html')
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('introduction','Introduction',7,8),
 ('babel-fish','Chapter One — Could the Babel Fish Be a Symbol of Modern Communication?',9,12),
 ('adams-influence','Chapter Two — Adams’ Wit and Its Influence on Sci-Fi',13,15),
 ('cosmic-comedy','Chapter Three — The Art of Cosmic Comedy',16,21),
 ('philosophy','Chapter Four — Philosophical Musings in a Ridiculous Universe',22,27),
 ('technology','Chapter Five — Technology: The Double-Edged Sword of Progress',28,31),
 ('key-events','Chapter Six — Key Events and Plot Summaries',32,33),
 ('conclusion','Conclusion',34,35),
]
heads={'Introduction','Chapter One','Could the Babel Fish Be a Symbol of Modern Communication?','Chapter Two',"Adams' Wit and Its Influence on Sci-Fi",'Chapter Three','The Art of Cosmic Comedy','Chapter Four','Philosophical Musings in a Ridiculous Universe','Chapter Five','Technology: The Double-Edged Sword of Progress','Chapter Six','Key Events and Plot Summaries','Conclusion'}
records=[];parts=[]
for sid,label,start,end in sections:
 paras=[]
 for page in range(start,end+1):
  node=soup.find('section',{'data-source-page':str(page)});assert node,page
  texts=[p.get_text(' ',strip=True) for p in node.select('p')]
  texts=[t for t in texts if t not in heads|{str(page-1),str(page)}]
  for i,t in enumerate(texts):
   if i==0 and paras and not re.search(r'[.!?][”\'\"]?$',paras[-1]):paras[-1]+=' '+t
   else:paras.append(t)
 records.append({'id':sid,'pages':[start,end],'paragraphs':len(paras),'words':sum(len(p.split()) for p in paras)})
 parts.append('<section id="%s"><h2>%s</h2>\n%s\n</section>'%(sid,escape(label),'\n'.join('<p>%s</p>'%escape(t) for t in paras)))
title='Hitchhiker’s Guide to the Galaxy'
(root/'book/en/full_content.html').write_text('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>%s</title></head><body><article>\n<h1>%s</h1>\n'%(escape(title),escape(title))+'\n'.join(parts)+'\n</article></body></html>\n')
(root/'qa').mkdir(exist_ok=True)
(root/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'includedPages':[7,35],'excludedPages':[[1,6],[36,43]],'reason':'Substantive introduction, six chapters and conclusion retained; old preface, rights, author/project annexes and bibliography omitted.','sections':records},indent=2)+'\n')
print(records)
