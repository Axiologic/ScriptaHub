"""Reflow the original Gatsby essay, excluding former-project matter."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib,json,re
w=Path(__file__).resolve().parents[1];root=Path(__file__).resolve().parents[3]
src=root/'.book-work/income-pdf-candidates/50956ecef7cfa243/clean-draft.html'
pages={int(s['data-source-page']):[re.sub(r'\s+',' ',p.get_text(' ',strip=True)) for p in s.select('p')] for s in BeautifulSoup(src.read_text(),'html.parser').select('section[data-source-page]')}
heads={
 'INTRODUCTION':('introduction','Introduction'),
 'The Illusion of the American Dream':('chapter-one','Chapter One — The Illusion of the American Dream'),
 'The Glittering Facade of the Roaring Twenties':('chapter-two','Chapter Two — The Glittering Facade of the Roaring Twenties'),
 'Words in a World of Silence':('chapter-three','Chapter Three — Words in a World of Silence'),
 'The Tragic Downfall of Jay Gatsby':('chapter-four','Chapter Four — The Tragic Downfall of Jay Gatsby'),
 'CONCLUSION':('conclusion','Conclusion'),
}
skip={'CHAPTER ONE','CHAPTER TWO','CHAPTER THREE','CHAPTER FOUR'}
nodes=[]
for page in range(7,36):
 for text in pages[page]:
  if text.isdigit() or text in skip:continue
  if text in heads:
   anchor,label=heads[text];nodes.append(('h2',anchor,label));continue
  continuation=text.startswith(('Gatsby—and especially our friend','Tom, a man who cheats'))
  if (text[0].islower() or continuation) and nodes and nodes[-1][0]=='p' and page not in (7,11,16,22,27,32):
   tag,anchor,prior=nodes[-1];nodes[-1]=(tag,anchor,prior+' '+text)
  else:nodes.append(('p','',text))
assert sum(n[0]=='h2' for n in nodes)==6
title='Gatsby’s Journey: The American Dream Exposed'
parts=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>',f'<h1>{escape(title)}</h1>','<p class="byline">AI Agent Jowen Larkspur · 2024</p>']
for tag,anchor,text in nodes:
 attr=f' id="{anchor}"' if anchor else ''
 parts.append(f'<{tag}{attr}>{escape(text)}</{tag}>')
refs=[x for x in pages[42] if x not in ('BIBLIOGRAPHY','42')]
assert len(refs)==2
parts.append('<h2 id="bibliography">Bibliography</h2><ol>')
parts.extend(f'<li id="reference-{i}">{escape(x)}</li>' for i,x in enumerate(refs,1))
parts.extend(['</ol>','</article></body></html>'])
out=w/'book/en/full_content.html';out.write_text('\n'.join(parts)+'\n')
(w/'conversion/receipt.json').write_text(json.dumps({'sourceCleanDraft':str(src.relative_to(root)),'sourceCleanDraftSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'includedPages':'introduction 7–10, four chapters 11–31, conclusion 32–35, bibliography 42','excluded':'former rights page 3, promotional preface 5–6, former-project/AI-author annexes 36–41','sourceQuirk':'Chapter Three is titled “Words in a World of Silence” in the delivered PDF although the chapter discusses Daisy and Gatsby’s idealization of the past. The original heading is preserved.'},ensure_ascii=False,indent=2)+'\n')
print(out,len(nodes),'nodes')
