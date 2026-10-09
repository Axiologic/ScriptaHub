from bs4 import BeautifulSoup
from pathlib import Path
from html import escape
import re

w=Path(__file__).parent
s=BeautifulSoup(Path('.book-work/income-pdf-candidates/34593707338a3aaa/clean-draft.html').read_text(),'html.parser')
sections=[];current=None;paragraphs=[]
heading={
 'INTRODUCTION':('introduction','INTRODUCTION'),
 'CHAPTER ONE':('chapter-1','CHAPTER ONE'),
 'CHAPTER TWO':('chapter-2','CHAPTER TWO'),
 'CHAPTER THREE':('chapter-3','CHAPTER THREE'),
 'CHAPTER FOUR':('chapter-4','CHAPTER FOUR'),
 'CONCLUSION':('conclusion','CONCLUSION'),
 'BIBLIOGRAPHY':('bibliography','BIBLIOGRAPHY'),
}
subheads={
 'The Struggles of Early Life – A Voice Against Oppression',
 'The Journey to Thornfield – Love and the Negotiation of Power',
 'Solitude and Self-Discovery: The Road to Independence',
 'Empowered Reunion: Jane’s Path to Independence',
}
for sec in s.select('section[data-source-page]'):
 page=int(sec['data-source-page'])
 if page not in list(range(7,30))+[37,38]:continue
 for el in sec.select('p'):
  t=el.get_text(' ',strip=True)
  if not t or t.isdecimal():continue
  if t in heading:
   current=heading[t];sections.append((current[0],current[1],[]));continue
  if not sections:continue
  blocks=sections[-1][2]
  if t in subheads:blocks.append(('h3',t));continue
  # The extraction splits a paragraph at a page break when the next page starts mid-sentence.
  if blocks and blocks[-1][0]=='p' and (not re.search(r'[.!?][”"’\)]?$',blocks[-1][1]) or t[:1].islower()):
   blocks[-1]=('p',blocks[-1][1]+' '+t)
  else:blocks.append(('p',t))
out=['<!doctype html>','<html lang="en"><head><meta charset="utf-8"><title>A Woman’s Fight for Freedom: Jane Eyre</title></head><body>','<main>','<h1>A Woman’s Fight for Freedom: Jane Eyre</h1>','<p class="byline">AI Agent Jowen Larkspur · 2024</p>']
for ident,title,blocks in sections:
 out.append(f'<section id="{ident}">');out.append(f'<h2>{escape(title)}</h2>')
 for tag,text in blocks:out.append(f'<{tag}>{escape(text)}</{tag}>')
 out.append('</section>')
out+=['</main>','</body></html>']
(w/'book/en/full_content.html').write_text('\n'.join(out)+'\n')
print([(i,len(b)) for i,_,b in sections])
