import json,re
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).parent
source=Path('.book-work/income-pdf-candidates/919d751611d0e507/clean-draft.html')
draft=BeautifulSoup(source.read_text(),'html.parser')
title='Narrative of the Life of Frederick Douglass'
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title></head><body><article data-reader-content></article></body></html>','html.parser')
out.title.string=title;article=out.article
h=out.new_tag('h1',id='book-title');h.string=title;article.append(h)
heads={7:'Modern Perspective About Frederick Douglass',10:'Historical and Cultural Context',14:'Main Characters',19:'Plot Summary by Narrative Threads',25:'Original Preface by William Lloyd Garrison',35:'Letter from Wendell Phillips',39:'Frederick Douglass: Biographical Note',40:'Chapter I',46:'Chapter II',53:'Chapter III',58:'Chapter IV',63:'Chapter V',68:'Chapter VI',72:'Chapter VII',79:'Chapter VIII',85:'Chapter IX',91:'Chapter X',127:'Chapter XI',143:'Appendix'}
subheads={'Frederick Douglass – The Protagonist','Aunt Hester','Sophia Auld',"Douglass's Early Life in Slavery"}
sections=[]
pagebounds={}
retained=list(range(7,24))+list(range(25,151))
for page in retained:
 sec=draft.select_one(f'section[data-source-page="{page}"]');assert sec,page
 paras=[re.sub(r'\s+',' ',p.get_text(' ',strip=True)).strip() for p in sec.find_all('p',recursive=False)]
 paras=[p for p in paras if p and not re.fullmatch(r'\d+',p)]
 if page in heads:
  label=heads[page];h=out.new_tag('h2',id=f'section-{len(sections)+1}');h.string=label;article.append(h);sections.append({'id':h['id'],'title':label,'sourcePdfPage':page})
  original={7:'MODERN PERSPECTIVE ABOUT FREDERICK DOUGLASS',10:'HISTORICAL AND CULTURAL CONTEXT',14:'MAIN CHARACTERS',19:'PLOT SUMMARY BY NARRATIVE THREADS',25:'PREFACE',35:'LETTER FROM WENDELL PHILLIPS, ESQ.',39:'FREDERICK DOUGLASS',143:'APPENDIX'}.get(page)
  if original is None:original=f'CHAPTER {"I II III IV V VI VII VIII IX X XI".split()[list(heads).index(page)-7]}'
  assert paras and paras[0].startswith(original),(page,paras[:1])
  paras[0]=paras[0][len(original):].strip()
 first_node=last_node=None
 for value in paras:
  if not value:continue
  tag='h3' if value in subheads else 'p'
  x=out.new_tag(tag);x.string=value;article.append(x)
  if first_node is None:first_node=x
  last_node=x
 pagebounds[page]=(first_node,last_node)
# Rejoin prose paragraphs broken at PDF page boundaries only. Preserve source stanzas and headings.
merged=[]
for a,b in zip(retained,retained[1:]):
 if b!=a+1 or b in heads or a>=147:continue
 left=pagebounds[a][1];right=pagebounds[b][0]
 if not left or not right or left.name!='p' or right.name!='p':continue
 l=left.get_text(' ',strip=True);r=right.get_text(' ',strip=True)
 if l and r and (not re.search(r'[.!?:;”\"\)]$',l) or re.match(r'^[a-z]',r)):
  left.string=l+' '+r;right.decompose();merged.append((a,b))
# Keep reader paragraphs and direct translation units manageable without paraphrasing.
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
  node.decompose()
body=article.get_text(' ',strip=True)
assert len(body.split())>35000,len(body.split())
assert len(sections)==19,len(sections)
assert not any(x in body.casefold() for x in ('outfinitygift','outfinity gift','outfinitygift.com'))
path=root/'book/en/full_content.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(str(out)+'\n')
qa=root/'qa';qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({'source':'income/Narrative_of_the_Life_of_FREDERICK_DOUGLASS/content.pdf','retainedPdfPages':retained,'excludedPdfPages':list(range(1,7))+[24]+list(range(151,155)),'reason':'Preserve substantive modern perspective and original historical preface, letter, biography, eleven chapters and appendix; exclude rights/contents, retired-project promotional preface, duplicate title-only divider, and promotional annex.','sections':sections,'mergedPageBreaks':merged,'readerWords':len(body.split()),'sourceTitlePage':2,'sourceAuthors':['Frederick Douglass','AI Agent Zira Luthor (2024)']},ensure_ascii=False,indent=2)+'\n')
print('Douglass EN full',len(body.split()),'words',len(sections),'sections')
