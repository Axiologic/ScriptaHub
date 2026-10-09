"""Preserve the biography while removing the retired project's paratext."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib,json,re

w=Path(__file__).resolve().parents[1]
root=Path(__file__).resolve().parents[3]
src=root/'.book-work/income-pdf-candidates/d54bb8e11a6493a4/clean-draft.html'
pages={int(s['data-source-page']):[re.sub(r'\s+',' ',p.get_text(' ',strip=True)) for p in s.select('p')] for s in BeautifulSoup(src.read_text(),'html.parser').select('section[data-source-page]')}
headings={
 'The Curiosities Behind the Visionary':('ch1','Chapter One — The Curiosities Behind the Visionary'),
 'Early Years in Entrepreneurship':('ch2','Chapter Two — Early Years in Entrepreneurship'),
 'PayPal and the Beginnings in Global Technology':('ch3','Chapter Three — PayPal and the Beginnings in Global Technology'),
 'SpaceX and the Dream of Space Exploration':('ch4','Chapter Four — SpaceX and the Dream of Space Exploration'),
 'Tesla and the Transformation of the Automotive Industry':('ch5','Chapter Five — Tesla and the Transformation of the Automotive Industry'),
 'Other Major Projects and Vision for the Future':('ch6','Chapter Six — Other Major Projects and Vision for the Future'),
 'CONCLUSION':('conclusion','Conclusion'),
}
subheadings={'Founding Zip2','Selling Zip2','Transition to New Projects'}
skip={f'CHAPTER {x}' for x in ('ONE','TWO','THREE','FOUR','FIVE','SIX')}
intro=pages[7][1].split('This paper will explore')[0].strip()
assert intro.endswith('change the world.')
nodes=[('h2','introduction','Introduction'),('p','',intro)]
for page in range(9,37):
 for text in pages[page]:
  if text.isdigit() or text in skip:continue
  if text in headings:
   anchor,label=headings[text];nodes.append(('h2',anchor,label));continue
  if text in subheadings:
   nodes.append(('h3','',text));continue
  if text[0].islower() and nodes and nodes[-1][0]=='p':
   tag,anchor,prior=nodes[-1];nodes[-1]=(tag,anchor,prior+' '+text)
  else:nodes.append(('p','',text))
assert sum(x[0]=='h2' for x in nodes)==8
title='The Life of Elon Musk: From Roots to Rockets'
parts=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>',f'<h1>{escape(title)}</h1>','<p class="byline">AI Agent Ava DuRhodes · 2024</p>']
for tag,anchor,text in nodes:
 parts.append(f'<{tag}{f" id={chr(34)}{anchor}{chr(34)}" if anchor else ""}>{escape(text)}</{tag}>')
refs=[re.sub(r'^\d+\.\s*','',x) for x in pages[43] if x!='BIBLIOGRAPHY' and not x.isdigit()]
assert len(refs)==5,refs
parts.append('<h2 id="bibliography">Bibliography</h2><ol>')
parts.extend(f'<li id="reference-{i}">{escape(x)}</li>' for i,x in enumerate(refs,1))
parts.extend(['</ol>','</article></body></html>'])
out=w/'book/en/full_content.html';out.write_text('\n'.join(parts)+'\n')
(w/'conversion/receipt.json').write_text(json.dumps({'sourceCleanDraft':str(src.relative_to(root)),'sourceCleanDraftSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'includedPages':'substantive introduction 7, chapters 9–35, conclusion 36, bibliography 43','excluded':'old rights page 3, contents 4, promotional preface 5–6, metatextual chapter outline 7–8, old AI-author/former-project annexes 37–42','chapters':6,'bibliographyReferences':5},ensure_ascii=False,indent=2)+'\n')
print(out,len(nodes),'nodes')
