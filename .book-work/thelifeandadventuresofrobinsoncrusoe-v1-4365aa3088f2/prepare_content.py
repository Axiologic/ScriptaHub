#!/usr/bin/env python3
"""Extract only Daniel Defoe's complete 20-chapter novel from the delivered PDF."""
import html,json,re
from pathlib import Path

root=Path(__file__).resolve().parent
pages=(root/'source-layout.txt').read_text().split('\f')
titles={
 1:'Start in Life',2:'Slavery and Escape',3:'Wrecked on a Desert Island',
 4:'First Weeks on the Island',5:'Builds a House—The Journal',
 6:'Ill and Conscience-Stricken',7:'Agricultural Experience',
 8:'Surveys His Position',9:'A Boat',10:'Tames Goats',
 11:'Finds Print of Man’s Foot on the Sand',12:'A Cave Retreat',
 13:'Wreck of a Spanish Ship',14:'A Dream Realised',
 15:'Friday’s Education',16:'Rescue of Prisoners from Cannibals',
 17:'Visit of Mutineers',18:'The Ship Recovered',
 19:'Return to England',20:'Fight between Friday and a Bear',
}
roman={1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI',7:'VII',8:'VIII',9:'IX',10:'X',11:'XI',12:'XII',13:'XIII',14:'XIV',15:'XV',16:'XVI',17:'XVII',18:'XVIII',19:'XIX',20:'XX'}
chapter_starts={18:1,33:2,48:3,69:4,94:5,110:6,126:7,137:8,149:9,168:10,182:11,198:12,218:13,233:14,252:15,269:16,288:17,306:18,325:19,342:20}
parts=[];paragraph=[];page_stats=[]
def flush():
 if paragraph:
  txt=' '.join(paragraph).strip()
  txt=re.sub(r'\s+',' ',txt)
  if txt:parts.append(f'<p>{html.escape(txt,quote=False)}</p>')
  paragraph.clear()
def add_line(s):
 s=s.strip()
 if not s:return
 if paragraph and paragraph[-1].endswith('-') and re.match(r'^[a-z]',s):
  paragraph[-1]=paragraph[-1][:-1]+s
 else:paragraph.append(s)

for page_number in range(18,356):
 raw=pages[page_number-1]
 lines=raw.splitlines()
 # Remove printed page number, but keep genuine standalone prose lines.
 lines=[x for x in lines if x.strip()!=str(page_number)]
 if page_number in chapter_starts:
  flush()
  n=chapter_starts[page_number]
  parts.append(f'<h2 id="chapter-{n}">Chapter {roman[n]} — {html.escape(titles[n])}</h2>')
  idx=next((i for i,x in enumerate(lines) if re.fullmatch(r'\s*CHAPTER\s+'+roman[n]+r'\s*',x)),None)
  if idx is None:raise ValueError(f'chapter heading absent on PDF page {page_number}')
  # Skip the printed subtitle (one line, except chapters XI and XVI, where
  # it wraps onto a second line) without relying on indentation.
  j=idx+1
  count=2 if n in {11,16} else 1
  while j<len(lines) and count:
   if lines[j].strip():count-=1
   j+=1
  while j<len(lines) and not lines[j].strip():j+=1
  lines=lines[j:]
 for line in lines:
  if not line.strip() or line.strip()=='THE END':continue
  if re.match(r'^\s{5,}\S',line) and paragraph:flush()
  add_line(line)
 page_stats.append({'pdfPage':page_number,'characters':len(raw)})
flush()
body='\n'.join(parts)
out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>The Life and Adventures of Robinson Crusoe</title></head><body><article data-reader-content=""><h1 id="book-title">The Life and Adventures of Robinson Crusoe</h1><p>Daniel Defoe</p>{body}</article></body></html>'''
target=root/'book/en/full_content.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(out)
from bs4 import BeautifulSoup
soup=BeautifulSoup(out,'html.parser')
headings=soup.select('article > h2');paras=soup.select('article > p')
assert len(headings)==20,len(headings)
assert 'Second Part of my Story' in paras[-1].get_text(' ',strip=True)
assert not any(x in soup.get_text(' ',strip=True).lower() for x in ['outfinitygift','ai perspective','a letter to readers and supporters'])
receipt={'sourcePdfPages':[18,355],'chapterCount':len(headings),'paragraphCount':len(paras)-1,'words':len(soup.get_text(' ',strip=True).split()),'firstParagraph':paras[1].get_text(' ',strip=True)[:140],'lastParagraph':paras[-1].get_text(' ',strip=True)[-200:],'pages':page_stats}
(root/'qa/extraction-review.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print({k:receipt[k] for k in ['chapterCount','paragraphCount','words','firstParagraph','lastParagraph']})
