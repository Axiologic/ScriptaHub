from bs4 import BeautifulSoup
from pathlib import Path
from html import escape
import re
w=Path(__file__).parent
s=BeautifulSoup(Path('.book-work/income-pdf-candidates/b596d241bda00a9b/clean-draft.html').read_text(),'html.parser')
heads={'INTRODUCTION':('introduction','INTRODUCTION'),'CHAPTER ONE':('chapter-1','CHAPTER ONE'),'CHAPTER TWO':('chapter-2','CHAPTER TWO'),'CHAPTER THREE':('chapter-3','CHAPTER THREE'),'CHAPTER FOUR':('chapter-4','CHAPTER FOUR'),'CONCLUSION':('conclusion','CONCLUSION')}
subheads={'From Chains to Redemption','Fantine’s Tragic Descent','Revolution’s Price','Love’s Final Sacrifice'}
sections=[]
for sec in s.select('section[data-source-page]'):
 page=int(sec['data-source-page'])
 if page not in list(range(7,34))+[41]:continue
 for ix,el in enumerate(sec.select('p')):
  t=el.get_text(' ',strip=True)
  if not t or t.isdecimal():continue
  if page==33 and ix>0:continue
  if page==41:
   if t=='BIBLIOGRAPHY':sections.append(('bibliography','BIBLIOGRAPHY',[]))
   elif t.startswith('Hugo, V.'):sections[-1][2].append(('p',t))
   continue
  if t in heads:
   h=heads[t];sections.append((h[0],h[1],[]));continue
  if not sections:continue
  blocks=sections[-1][2]
  if t in subheads:blocks.append(('h3',t));continue
  t=re.sub(r'\s+',' ',t)
  if blocks and blocks[-1][0]=='p' and (not re.search(r'[.!?][”"’\)]?$',blocks[-1][1]) or t[:1].islower()):blocks[-1]=('p',blocks[-1][1]+' '+t)
  else:blocks.append(('p',t))
out=['<!doctype html>','<html lang="en"><head><meta charset="utf-8"><title>The Price of Freedom in Les Misérables</title></head><body>','<main>','<h1>The Price of Freedom in Les Misérables</h1>','<p class="byline">AI Agent Chloe Vohan · 2024</p>']
for ident,title,blocks in sections:
 out.append(f'<section id="{ident}"><h2>{escape(title)}</h2>')
 for tag,text in blocks:out.append(f'<{tag}>{escape(text)}</{tag}>')
 out.append('</section>')
out+=['</main>','</body></html>']
(w/'book/en/full_content.html').write_text('\n'.join(out)+'\n')
print([(i,len(b)) for i,_,b in sections])
