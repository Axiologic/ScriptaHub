#!/usr/bin/env python3
"""Reflow the original literary companion, omitting former-project matter."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib,json,re
w=Path(__file__).resolve().parents[1];root=Path(__file__).resolve().parents[3]
src=root/'.book-work/income-pdf-candidates/3593d1635cb40f9a/clean-draft.html'
pages={int(s['data-source-page']):[re.sub(r'\s+',' ',p.get_text(' ',strip=True)) for p in s.select('p')] for s in BeautifulSoup(src.read_text(),'html.parser').select('section[data-source-page]')}
heads={
 'INTRODUCTION':('introduction','Introduction'),
 'The Weapon We All Hold':('ch1','Chapter One — The Weapon We All Hold'),
 'A Thief ’s Journey Begins':('ch2','Chapter Two — A Thief’s Journey Begins'),
 'Words in a World of Silence':('ch3','Chapter Three — Words in a World of Silence'),
 'The Cost of Survival':('ch4','Chapter Four — The Cost of Survival'),
}
skip={'CHAPTER ONE','CHAPTER TWO','CHAPTER THREE','CHAPTER FOUR'}
nodes=[]
for page in list(range(7,11))+list(range(12,31)):
 for i,text in enumerate(pages[page]):
  if text.isdigit() or text in skip:continue
  if text in heads:
   anchor,label=heads[text];nodes.append(('h2',anchor,label));continue
  if i==0 and page not in (7,12,17,22,27) and text[0].islower() and nodes and nodes[-1][0]=='p':
   tag,anchor,prior=nodes[-1];nodes[-1]=(tag,anchor,prior+' '+text)
  else:nodes.append(('p','',text))
assert sum(n[0]=='h2' for n in nodes)==5
parts=['<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Unlocking Markus Zusak’s The Book Thief</title></head><body><article>',
 '<h1>Unlocking Markus Zusak’s The Book Thief</h1>','<p class="byline">AI Agent Jowen Larkspur · 2024</p>']
for tag,anchor,text in nodes:
 attr=f' id="{anchor}"' if anchor else ''
 parts.append(f'<{tag}{attr}>{escape(text)}</{tag}>')
parts.append('<h2 id="bibliography">Bibliography</h2><ol>')
refs=[x for x in pages[37] if x not in ('BIBLIOGRAPHY','37')];assert len(refs)==2
parts.extend(f'<li id="reference-{i}">{escape(x)}</li>' for i,x in enumerate(refs,1))
parts.extend(['</ol>','</article></body></html>'])
out=w/'book/en/full_content.html';out.write_text('\n'.join(parts)+'\n',encoding='utf-8')
(w/'conversion/receipt.json').write_text(json.dumps({'sourceCleanDraft':str(src.relative_to(root)),'sourceCleanDraftSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'includedPages':'introduction 7–10, chapters 12–30, bibliography 37','excluded':'former rights page, promotional preface 5–6, reading-invitation CTA page 11, former-project/AI-author annexes 31–36','chapters':4,'bibliographyReferences':2},indent=2)+'\n')
print(out,len(nodes),'nodes')
