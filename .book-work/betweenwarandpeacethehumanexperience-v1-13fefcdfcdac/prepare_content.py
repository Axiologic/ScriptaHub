from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json,re

root=Path('.book-work/betweenwarandpeacethehumanexperience-v1-13fefcdfcdac')
source=next(Path('.book-work/income-pdf-candidates').glob('13fefcdfcdac*/clean-draft.html'))
soup=BeautifulSoup(source.read_text(),'html.parser')
sections=[
 ('introduction','Introduction',7,10),
 ('love-versus-war','Chapter One — Love vs. War: Who Will Prevail?',11,15),
 ('surviving-the-storm','Chapter Two — Surviving the Storm',16,20),
 ('dancing-through-turmoil','Chapter Three — Dancing Through Turmoil',21,25),
 ('battlefield-revelations','Chapter Four — Battlefield Revelations: What War Reveals',26,29),
 ('conclusion','Conclusion',30,34),
]
headings={'INTRODUCTION','CHAPTER ONE','Love vs. War: Who Will Prevail?','CHAPTER TWO','Surviving to the Storm','CHAPTER THREE','Dancing Through Turmoil','CHAPTER FOUR','Battlefield Revelations: What War Reveals','CONCLUSION'}
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
html='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>Between War and Peace: The Human Experience</title></head><body><article>\n<h1>Between War and Peace: The Human Experience</h1>\n'+'\n'.join(html_sections)+'\n</article></body></html>\n'
(root/'book/en/full_content.html').write_text(html)
(root/'qa').mkdir(exist_ok=True)
(root/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'includedPages':[7,34],'excludedPages':[[1,6],[35,41]],'reason':'Introduction, four substantive chapters and thematic conclusion retained; promotional preface, front matter, author profile and bibliography excluded.','sections':records},indent=2)+'\n')
print(records)
