from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re

root=Path('.book-work/thematrixuniverseajourneythroughrealityandbeyond-v1-28c4be91976c')
source=Path('.book-work/income-pdf-candidates/28c4be91976c16ca/clean-draft.html')
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('introduction','Introduction',7,9),
 ('matrix-effect','Chapter One — The Matrix Effect in the 21st Century',10,14),
 ('dual-societies','Chapter Two — Dual Societies: The Matrix and Zion',15,18),
 ('nature-of-reality','Chapter Three — Unveiling the Illusion: The Nature of Reality in The Matrix',19,22),
 ('freedom-and-control','Chapter Four — Chains of the Mind: Freedom and Control',23,27),
 ('knowledge-and-ignorance','Chapter Five — Beyond the Veil: Knowledge and Ignorance',28,30),
 ('key-events','Chapter Six — Key Events and Plot Summaries',31,35),
 ('conclusion','Conclusion',36,36),
]
heads={'Introduction','Chapter One','The Matrix Effect in the 21st Century','Chapter Two','Dual Societies: The Matrix and Zion','Chapter Three','Unveiling the Illusion - The Nature of Reality in The Matrix','Chapter Four','Chains of the Mind - Freedom and Control','Chapter Five','Beyond the Veil - Knowledge and Ignorance','Chapter Six','Key Events and Plot Summaries','Conclusion'}
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
title='The Matrix Universe: A Journey Through Reality and Beyond'
out='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>%s</title></head><body><article>\n<h1>%s</h1>\n'%(escape(title),escape(title))+'\n'.join(parts)+'\n</article></body></html>\n'
(root/'book/en/full_content.html').write_text(out)
(root/'qa').mkdir(exist_ok=True)
(root/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'includedPages':[7,36],'excludedPages':[[1,6],[37,42]],'reason':'Substantive introduction, six chapters, and conclusion retained; promotional preface, rights pages, author and project annexes omitted.','sections':records},indent=2)+'\n')
print(records)
