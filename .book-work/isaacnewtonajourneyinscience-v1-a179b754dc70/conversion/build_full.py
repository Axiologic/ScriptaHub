"""Reflow Newton's six substantive chapters and bibliography."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib,json,re
w=Path(__file__).resolve().parents[1];root=Path(__file__).resolve().parents[3]
src=root/'.book-work/income-pdf-candidates/a179b754dc70faf5/clean-draft.html'
pages={int(s['data-source-page']):[re.sub(r'\s+',' ',p.get_text(' ',strip=True)) for p in s.select('p')] for s in BeautifulSoup(src.read_text(),'html.parser').select('section[data-source-page]')}
heads={
 'How Newton Transformed the Modern World?':('chapter-one','Chapter One — How Newton Transformed the Modern World?'),
 'Early Life and Education':('chapter-two','Chapter Two — Early Life and Education'),
 'Major Scientific Breakthroughs':('chapter-three','Chapter Three — Major Scientific Breakthroughs'),
 'Impact on Society':('chapter-four','Chapter Four — Impact on Society'),
 "Newton's Personality":('chapter-five',"Chapter Five — Newton's Personality"),
 'Newton vs. His Contemporaries':('chapter-six','Chapter Six — Newton vs. His Contemporaries'),
 'CONCLUSION':('conclusion','Conclusion'),
}
skip={f'CHAPTER {x}' for x in ('ONE','TWO','THREE','FOUR','FIVE','SIX')}
nodes=[]
for page in range(11,36):
 for text in pages[page]:
  if text.isdigit() or text in skip:continue
  if text in heads:
   anchor,label=heads[text];nodes.append(('h2',anchor,label));continue
  if text[0].islower() and nodes and nodes[-1][0]=='p' and page not in (11,15,18,22,28,31,34):
   tag,anchor,prior=nodes[-1];nodes[-1]=(tag,anchor,prior+' '+text)
  else:nodes.append(('p','',text))
assert sum(x[0]=='h2' for x in nodes)==7
title='Isaac Newton: A Journey in Science'
parts=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>',f'<h1>{escape(title)}</h1>','<p class="byline">AI Agent Noah Bradland · 2024</p>']
for tag,anchor,text in nodes:
 parts.append(f'<{tag}{f" id={chr(34)}{anchor}{chr(34)}" if anchor else ""}>{escape(text)}</{tag}>')
refs=[x for p in (42,43) for x in pages[p] if x not in ('BIBLIOGRAPHY','Books:','Articles:','41','42')]
assert len(refs)==5,refs
parts.append('<h2 id="bibliography">Bibliography</h2><ol>')
parts.extend(f'<li id="reference-{i}">{escape(x)}</li>' for i,x in enumerate(refs,1))
parts.extend(['</ol>','</article></body></html>'])
out=w/'book/en/full_content.html';out.write_text('\n'.join(parts)+'\n')
(w/'conversion/receipt.json').write_text(json.dumps({'sourceCleanDraft':str(src.relative_to(root)),'sourceCleanDraftSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'includedPages':'chapters 11–33, conclusion 34–35, bibliography 42–43','excluded':'former rights page 3, promotional preface 5–7, former-project/AI introduction 8–10, former-project/AI-author annexes 36–41','chapters':6,'bibliographyReferences':5},ensure_ascii=False,indent=2)+'\n')
print(out,len(nodes),'nodes')
