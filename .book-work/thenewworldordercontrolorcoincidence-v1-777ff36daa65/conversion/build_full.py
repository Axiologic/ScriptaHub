#!/usr/bin/env python3
"""Reflow only the original essay and bibliography from the delivered PDF."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib,json,re
work=Path(__file__).resolve().parents[1]
root=Path(__file__).resolve().parents[3]
source=root/'.book-work/income-pdf-candidates/777ff36daa654adc/clean-draft.html'
pages={int(s['data-source-page']):[re.sub(r'\s+',' ',p.get_text(' ',strip=True)) for p in s.select('p')] for s in BeautifulSoup(source.read_text(),'html.parser').select('section[data-source-page]')}
main={
 'INTRODUCTION':('introduction','Introduction'),
 'The Secret Origins of the Illuminati: Myth or Reality?':('ch1','Chapter One — The Secret Origins of the Illuminati: Myth or Reality?'),
 'The New World Order: Total Control or Fear-Driven Theory?':('ch2','Chapter Two — The New World Order: Total Control or Fear-Driven Theory?'),
 'Media Manipulation and Pop Culture: Tools of the Elite?':('ch3','Chapter Three — Media Manipulation and Pop Culture: Tools of the Elite?'),
 'Unveiling the Power Behind the Curtain':('conclusion','Conclusion — Unveiling the Power Behind the Curtain'),
}
subheads={
 'The Historical Illuminati: A Brief Foundation','The Rise of Modern Conspiracy: Are We All Being Controlled?',
 'Theories, Control, and the Power of Media','Could the Illuminati Still Be Pulling the Strings?',
 'Lockdowns, Digital Jobs, and the Perfect Test of Control','Digital Surveillance: From Public Safety to Permanent Control?',
 'Is the New World Order Already Here?',"The Media's Role During the Pandemic: Informing or Controlling?",
 'Pop Culture’s Role: Conditioning the Masses?','The Power of Influence: Who Truly Controls the Narrative?'
}
skip={'CHAPTER ONE','CHAPTER TWO','CHAPTER THREE','CONCLUSION'}
nodes=[];counts={};previous_page=None
for page in range(8,32):
 for i,text in enumerate(pages[page]):
  if text.isdigit() or text in skip:continue
  if text in main:
   anchor,label=main[text];nodes.append(('h2',anchor,label));counts[anchor]=0;continue
  if text in subheads:
   nodes.append(('h3','',text));continue
  if i==0 and page!=8 and text and text[0].islower() and nodes and nodes[-1][0]=='p':
   tag,anchor,prior=nodes[-1];nodes[-1]=(tag,anchor,prior+' '+text)
  else:
   nodes.append(('p','',text))
  previous_page=page
assert sum(n[0]=='h2' for n in nodes)==5
assert sum(n[0]=='h3' for n in nodes)==10
parts=['<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The New World Order: Control or Coincidence?</title></head><body><article>',
 '<h1>The New World Order: Control or Coincidence?</h1>','<p class="byline">AI Agent Liora Riveers · 2024</p>']
for tag,anchor,text in nodes:
 attr=f' id="{anchor}"' if anchor else ''
 markup=escape(text).replace('**','')
 parts.append(f'<{tag}{attr}>{markup}</{tag}>')
parts.append('<h2 id="bibliography">Bibliography</h2><ol>')
refs=[p for p in pages[38] if p not in ('BIBLIOGRAPHY','38')]
assert len(refs)==5
parts.extend(f'<li id="reference-{i}">{escape(x)}</li>' for i,x in enumerate(refs,1))
parts.extend(['</ol>','</article></body></html>'])
out=work/'book/en/full_content.html';out.write_text('\n'.join(parts)+'\n',encoding='utf-8')
(work/'conversion/receipt.json').write_text(json.dumps({'sourceCleanDraft':str(source.relative_to(root)),'sourceCleanDraftSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'contentPages':[8,31],'bibliographyPage':38,'sections':5,'subsections':10,'bibliographyReferences':5,'excluded':'former rights, promotional preface, AI-author/project annex, old project letter'},indent=2)+'\n')
print(out,len(nodes),'nodes')
