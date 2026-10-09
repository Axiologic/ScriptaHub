"""Reflow the five substantive chapters and preserve the source bibliography."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib,json,re
w=Path(__file__).resolve().parents[1];root=Path(__file__).resolve().parents[3]
src=root/'.book-work/income-pdf-candidates/7b2b25947d81af65/clean-draft.html'
pages={int(s['data-source-page']):[re.sub(r'\s+',' ',p.get_text(' ',strip=True)) for p in s.select('p')] for s in BeautifulSoup(src.read_text(),'html.parser').select('section[data-source-page]')}
heads={
 'Chapter I The Nature of Money and Its Impact on Society':('ch1','Chapter I — The Nature of Money and Its Impact on Society'),
 'Chapter II Archetypes and the Human Psyche in Money Systems':('ch2','Chapter II — Archetypes and the Human Psyche in Money Systems'),
 'Chapter III Historical Precedents for Complementary Currencies':('ch3','Chapter III — Historical Precedents for Complementary Currencies'),
 'Chapter IV Toward a New Monetary System':('ch4','Chapter IV — Toward a New Monetary System'),
 'Chapter v Critical Reflections on the Feasibility of Lietaer’s Vision':('ch5','Chapter V — Critical Reflections on the Feasibility of Lietaer’s Vision'),
}
nodes=[]
for page in range(9,36):
 for text in pages[page]:
  if text.isdigit():continue
  if text in heads:
   anchor,label=heads[text];nodes.append(('h2',anchor,label));continue
  if nodes and nodes[-1][0]=='p' and (text[0].islower() or not re.search(r'[.!?][”"\']?$',nodes[-1][2])):
   tag,anchor,prior=nodes[-1];nodes[-1]=(tag,anchor,prior+' '+text)
  else:nodes.append(('p','',text))
assert sum(x[0]=='h2' for x in nodes)==5
refs=[x for page in range(44,48) for x in pages[page] if x!='Bibliography' and not x.isdigit()]
assert len(refs)==19,len(refs)
title='Beyond Greed and Scarcity with Bernard Lietaer'
parts=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>',f'<h1>{escape(title)}</h1>','<p class="byline">AI Agent Adria Morgan · 2024</p>']
for tag,anchor,text in nodes:parts.append(f'<{tag}{f" id={chr(34)}{anchor}{chr(34)}" if anchor else ""}>{escape(text)}</{tag}>')
parts.append('<h2 id="bibliography">Bibliography</h2><ol>')
parts.extend(f'<li id="reference-{i}">{escape(x)}</li>' for i,x in enumerate(refs,1))
parts.extend(['</ol>','</article></body></html>'])
out=w/'book/en/full_content.html';out.write_text('\n'.join(parts)+'\n')
(w/'conversion/receipt.json').write_text(json.dumps({'sourceCleanDraft':str(src.relative_to(root)),'sourceCleanDraftSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'includedPages':'chapters 9–35 and bibliography 44–47','excluded':'retired rights page 3, table of contents 4, promotional preface 5–8, AI-author/former-project annexes 36–43','chapters':5,'bibliographyReferences':len(refs)},ensure_ascii=False,indent=2)+'\n')
print(out,len(nodes),'nodes',len(refs),'references')
