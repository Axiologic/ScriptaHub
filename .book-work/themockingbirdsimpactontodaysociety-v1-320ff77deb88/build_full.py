from bs4 import BeautifulSoup
from pathlib import Path
from html import escape
import re

w=Path(__file__).parent
s=BeautifulSoup(Path('.book-work/income-pdf-candidates/320ff77deb8828a5/clean-draft.html').read_text(),'html.parser')
heads={'INTRODUCTION':('introduction','Introduction'),'CHAPTER ONE':('chapter-1','Chapter One'),'CHAPTER TWO':('chapter-2','Chapter Two'),'CHAPTER THREE':('chapter-3','Chapter Three'),'CHAPTER FOUR':('chapter-4','Chapter Four'),'CONCLUSION':('conclusion','Conclusion')}
subheads={'Racial Injustice: Lessons','Empathy and Moral Courage: The Atticus Effect','Education and Awareness','Cultural Conversations: The Mockingbird in Media'}
sections=[]
for sec in s.select('section[data-source-page]'):
 page=int(sec['data-source-page'])
 if page not in list(range(7,36))+[42]:continue
 for el in sec.select('p'):
  t=el.get_text(' ',strip=True)
  if not t or t.isdecimal():continue
  if page==42:
   if t=='BIBLIOGRAPHY':sections.append(('bibliography','Bibliography',[]))
   elif t.startswith('Lee, H.'):sections[-1][2].append(('p',t))
   continue
  if t in heads:
   ident,label=heads[t];sections.append((ident,label,[]));continue
  if not sections:continue
  blocks=sections[-1][2]
  if t in subheads:blocks.append(('h3',t));continue
  t=re.sub(r'\s+',' ',t)
  if blocks and blocks[-1][0]=='p' and (not re.search(r'[.!?][”"’\)]?$',blocks[-1][1]) or t[:1].islower()):blocks[-1]=('p',blocks[-1][1]+' '+t)
  else:blocks.append(('p',t))
title='The Mockingbird’s Impact on Today’s Society'
out=['<!doctype html>',f'<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body>','<main>',f'<h1>{escape(title)}</h1>','<p class="byline">AI Agent Ilda Fairbank · 2024</p>']
for ident,label,blocks in sections:
 out.append(f'<section id="{ident}"><h2>{escape(label)}</h2>')
 for tag,text in blocks:out.append(f'<{tag}>{escape(text)}</{tag}>')
 out.append('</section>')
out+=['</main>','</body></html>']
(w/'book/en/full_content.html').write_text('\n'.join(out)+'\n')
print([(i,len(b)) for i,_,b in sections])
