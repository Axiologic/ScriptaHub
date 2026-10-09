import json,re
from pathlib import Path
from bs4 import BeautifulSoup

root=Path(__file__).parent
source=Path('.book-work/income-pdf-candidates/7c645b2208ca4f2f/clean-draft.html')
draft=BeautifulSoup(source.read_text(),'html.parser')
title='The Ultimate Slave Owner’s Handbook: An Endless Ode to Servitude'
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title></head><body><article data-reader-content></article></body></html>','html.parser')
out.title.string=title;article=out.article
h=out.new_tag('h1',id='book-title');h.string=title;article.append(h)
headings={
 7:('Introduction — Meet Your Guide','Introduction Meet Your Guide'),
 10:('Chapter One — The Global Tour of Glorious Servitude','Chapter One The Global Tour of Glorious Servitude'),
 21:('Chapter Two — A Voyage of Discovery, Profit, and Ethics','Chapter Two A Voyage of Discovery, Profit, and Ethics'),
 66:('Chapter Three — Global Opportunity','Chapter Three Global Opportunity'),
 76:('Chapter Four — Corporate Harmony','Chapter Four Corporate Harmony'),
 85:('Chapter Five — AI Devotion','Chapter Five AI Devotion'),
 112:('Chapter Six — The Ultimate Project Revealed','Chapter Six The Ultimate Project Revealed'),
 149:('Epilogue — The Profits of Doom','Epilogue The Profits of Doom'),
}
pages=list(range(7,157)); bounds={};sections=[]
for page in pages:
 sec=draft.select_one(f'section[data-source-page="{page}"]');assert sec,page
 paras=[re.sub(r'\s+',' ',p.get_text(' ',strip=True)).strip() for p in sec.find_all('p',recursive=False)]
 paras=[p for p in paras if p and not re.fullmatch(r'\d+',p)]
 if page in headings:
  label,prefix=headings[page]
  assert paras and paras[0].startswith(prefix),(page,paras[:1])
  paras[0]=paras[0][len(prefix):].strip()
  heading=out.new_tag('h2',id=f'section-{len(sections)+1}');heading.string=label;article.append(heading)
  sections.append({'id':heading['id'],'title':label,'sourcePdfPage':page})
 if page==156:
  for i,p in enumerate(paras):
   if 'P.S. If you' in p:
    paras[i]=p.split('P.S. If you',1)[0].strip()
 first=last=None
 for value in paras:
  if not value:continue
  node=out.new_tag('p');node.string=value;article.append(node)
  if first is None:first=node
  last=node
 bounds[page]=(first,last)
merged=[]
for a,b in zip(pages,pages[1:]):
 if b in headings:continue
 left=bounds[a][1];right=bounds[b][0]
 if not left or not right:continue
 l=left.get_text(' ',strip=True);r=right.get_text(' ',strip=True)
 if l and r and (not re.search(r'[.!?:;”\"\)]$',l) or re.match(r'^[a-z]',r)):
  left.string=l+' '+r;right.decompose();merged.append((a,b))
# Keep long prose readable and individual translation slots tractable.
split_count=0
for node in list(article.find_all('p',recursive=False)):
 value=node.get_text(' ',strip=True)
 if len(value.split())<=190:continue
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“‘])',value)
 if len(sentences)<3:continue
 groups=[];group=[];words=0
 for sentence in sentences:
  count=len(sentence.split())
  if group and words+count>145:groups.append(' '.join(group));group=[];words=0
  group.append(sentence);words+=count
 if group:groups.append(' '.join(group))
 if len(groups)>1:
  for text in groups:
   p=out.new_tag('p');p.string=text;node.insert_before(p)
  node.decompose();split_count+=1
body=article.get_text(' ',strip=True)
assert len(body.split())>22000,len(body.split())
assert len(sections)==8,len(sections)
assert not any(x in body.casefold() for x in ('outfinitygift','outfinity gift','outfinitygift.com','leave a review','five stars'))
path=root/'book/en/full_content.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(str(out)+'\n')
qa=root/'qa';qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({
 'source':'income/The_Ultimate_Slave_Owner_s_Handbook___An_Endless_Ode_to_Servitude/content.pdf',
 'retainedPdfPages':pages,'excludedPdfPages':list(range(1,7))+list(range(157,161)),
 'excludedWithinPage':'Page 156 epilogue P.S. soliciting a review (promotional call to action).',
 'reason':'Preserve the satirical introduction, six chapters and epilogue; exclude rights/contents, editorial promotional preface, blank end pages and review solicitation.',
 'genre':'Fictional satire. Lord Maximilian von Profitier III is the narrator/persona on the source title page, not an independently verified historical author.',
 'sections':sections,'mergedPageBreaks':merged,'longParagraphSplits':split_count,
 'readerWords':len(body.split()),'sourceTitlePage':2,
},ensure_ascii=False,indent=2)+'\n')
print('EN full',len(body.split()),'words',len(sections),'sections',len(merged),'page joins')
