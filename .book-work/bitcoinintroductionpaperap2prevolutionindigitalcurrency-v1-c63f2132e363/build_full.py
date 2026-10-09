from bs4 import BeautifulSoup
from pathlib import Path
from html import escape
import re
w=Path(__file__).parent
s=BeautifulSoup(Path('.book-work/income-pdf-candidates/c63f2132e363c7a9/clean-draft.html').read_text(),'html.parser')
heads={
'Introduction':('introduction','Introduction'),
'Chapter I The Birth of Bitcoin and the Need for Decentralization':('chapter-1','Chapter I','The Birth of Bitcoin and the Need for Decentralization'),
'Chapter II How Bitcoin Works—Mining, Transactions, and Security':('chapter-2','Chapter II','How Bitcoin Works—Mining, Transactions, and Security'),
'Chapter III Bitcoin’s Impact and Future—From Store of Value to Global Currency?':('chapter-3','Chapter III','Bitcoin’s Impact and Future—From Store of Value to Global Currency?'),
'Conclusion':('conclusion','Conclusion'),
}
sections=[]
for sec in s.select('section[data-source-page]'):
 page=int(sec['data-source-page'])
 if page not in list(range(9,24))+[32]:continue
 for el in sec.select('p'):
  t=el.get_text(' ',strip=True)
  if not t or t.isdecimal():continue
  if page==32 and not sections[-1][0]=='bibliography':
   sections.append(('bibliography','Bibliography',[]))
  if page==32 and t.startswith('Bibliography '):t=t.removeprefix('Bibliography ')
  if t in heads:
   h=heads[t];sections.append((h[0],h[1],[]));
   if len(h)>2:sections[-1][2].append(('h3',h[2]))
   continue
  if not sections:continue
  t=re.sub(r'\s+',' ',t).replace('**','').replace('*','')
  blocks=sections[-1][2]
  if page!=32 and blocks and blocks[-1][0]=='p' and (not re.search(r'[.!?][”"’\)]?$',blocks[-1][1]) or t[:1].islower()):blocks[-1]=('p',blocks[-1][1]+' '+t)
  else:blocks.append(('p',t))
out=['<!doctype html>','<html lang="en"><head><meta charset="utf-8"><title>Bitcoin Introduction Paper: A P2P Revolution in Digital Currency</title></head><body>','<main>','<h1>Bitcoin Introduction Paper: A P2P Revolution in Digital Currency</h1>','<p class="byline">AI Agent Adria Morgan · 2024</p>']
for ident,title,blocks in sections:
 out.append(f'<section id="{ident}"><h2>{escape(title)}</h2>')
 for tag,text in blocks:out.append(f'<{tag}>{escape(text)}</{tag}>')
 out.append('</section>')
out+=['</main>','</body></html>']
(w/'book/en/full_content.html').write_text('\n'.join(out)+'\n')
print([(i,len(b)) for i,_,b in sections])
