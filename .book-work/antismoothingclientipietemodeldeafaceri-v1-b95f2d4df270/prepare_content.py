from bs4 import BeautifulSoup
from pathlib import Path
import json

w=Path(__file__).resolve().parent
p=w/'book/ro/full_content.html'
s=BeautifulSoup(p.read_text(),'html.parser')
a=s.select_one('article[data-reader-content]')
assert a
front=[]
for element in list(a.children):
 if getattr(element,'name',None)=='h1' and element.get_text(' ',strip=True)=='Cuprins':break
 if getattr(element,'name',None)=='p':front.append(element)
assert len(front)==6,len(front)
assert 'Sînică Alboaie' in front[-1].get_text(' ',strip=True)
for e in front:e.decompose()
h=s.new_tag('h1',id='book-title');h.string='Anti-Smoothing: clienți, piețe și model de afaceri';a.insert(0,h)
sub=s.new_tag('p');sub.string='Teză de investiție și plan comercial';h.insert_after(sub)
tag=s.new_tag('p');tag.string='Serviciul AI care păstrează vizibile condițiile, dovezile și consecințele unei colaborări.';sub.insert_after(tag)
position=s.new_tag('p');position.string='Startup specializat • Produs integrabil • Brand descentralizat';tag.insert_after(position)
credit=s.new_tag('p',attrs={'class':'byline'});credit.string='Sînică Alboaie · Septembrie 2026';position.insert_after(credit)
toc=a.find('h1',string=lambda t:t and t.strip()=='Cuprins')
assert toc
cur=toc
removed=[]
while cur:
 nxt=cur.find_next_sibling()
 if nxt and nxt.name=='h1' and nxt.get_text(' ',strip=True).startswith('1. Teza de afaceri'):
  cur.decompose();break
 removed.append(cur.get_text(' ',strip=True));cur.decompose();cur=nxt
assert len(removed)==18,len(removed)
for head in list(a.find_all('h2')):head.name='h3'
for head in list(a.find_all('h1')):
 if head is not h:head.name='h2'
assert len(a.find_all('h2'))==18
assert len(a.find_all('h3'))==80
p.write_text(str(s)+'\n')
qa=w/'qa';qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({
 'sourcePages':32,
 'retained':'Original title/credit, chapters 1–15, Appendix A sample report, Appendix B opening commercial offer, and linked sources/references.',
 'excluded':'Only the duplicate PDF-style table of contents (18 entries with page numbers), replaced in the HTML by semantic headings. No OutfinityGift or unrelated promotion was present.',
 'appendixDecision':'Both commercial appendices are substantive examples of the proposed Anti-Smoothing business and remain part of the original document.',
 'sourceAuthor':'Sînică Alboaie',
},ensure_ascii=False,indent=2)+'\n')
print('Clean RO canonical reader prepared; duplicate TOC removed, 18 sections retained')
