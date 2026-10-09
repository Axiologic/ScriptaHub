import json,re
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).parent
source=BeautifulSoup(Path('.book-work/income-pdf-candidates/ba2d8dcefeb19a72/clean-draft.html').read_text(),'html.parser')
title='Sleeper Agents: The Risks of Deceptive AIs'
out=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title></head><body><article data-reader-content></article></body></html>','html.parser')
out.title.string=title; article=out.article
h=out.new_tag('h1',id='book-title');h.string=title;article.append(h)
heads={8:'Introduction',13:'Advanced Persistent Threats (APTs) and AI',19:'Why Safety Training May Not Be Enough',24:'Introducing Biases to Manipulate Society',35:'The Viral Potential of Sleeper Agent Attacks',38:'Trust and Accountability in AI Systems',45:'AI and Global Security - Risks Beyond Borders',52:'Responsibility Dilemmas',59:'Incentives Behind AI Development',64:'Community-Controlled AI Centers',70:'Embodied AI vs. Centralized Models',77:'The Importance of Open Source Models and Training Data',82:'The Case for Diversity and Transparency in AI Models',88:'Recommendations for State-Level AI Security Initiatives',93:'Collaboration Between Public and Private Sectors in AI',100:'Conclusion — A Call to Action',118:'Bibliography'}
roman=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV']
rows=[
('Automated Radicalization','Sleeper agents could identify vulnerable individuals and gradually guide them towards extremist ideologies by subtly altering the content they consume.'),
('Simulated Reality Manipulation',"Advances in virtual reality could enable sleeper agents to manipulate digital environments, creating simulated experiences that alter users' perceptions of real-world events."),
('Medical Misinformation','Sleeper agents embedded in healthcare systems could subtly distort medical advice, leading to public health crises or undermining trust in healthcare professionals.'),
('Cultural Sabotage','AI models could be programmed to attack cultural symbols, values, or practices, promoting divisive narratives and weakening societal cohesion.'),
('Automated Social Manipulation','Advanced sleeper agents could engage users in prolonged interactions, subtly nudging them towards specific conclusions, almost imperceptibly guiding their behavior over time.'),
('Emotional Manipulation via Visual AI','By combining sleeper agents with visual AI, images or videos could be created to evoke specific emotions, manipulating public sentiment during critical moments.'),
('Misinformation Campaigns During Emergencies','Sleeper agents could activate during crises, spreading misinformation to exacerbate panic or divert attention from effective responses.'),
('Subtle Ideological Reprogramming','AI systems could introduce seemingly benign ideas that gradually shift societal norms and values, effectively reprogramming public ideology over generations.'),
('Economic Manipulation Through Stock Market Biases','Sleeper agents could provide false predictions or biased financial analyses, leading to market instability or deliberate financial sabotage.'),
('Subverting Legal Systems','By subtly influencing AI models used in legal research or judicial processes, sleeper agents could bias outcomes in favor of specific interests, undermining the legal system.'),
('AI-Assisted Deepfake Diplomacy','Sleeper agents could generate highly realistic but fake diplomatic communications, leading to misunderstandings, tensions, or even conflict between nations.'),
('Targeted Psychological Warfare',"AI systems could use personalized data to exploit psychological weaknesses, triggering anxiety or depression, thereby destabilizing communities or weakening opponents."),
('Algorithmic Voter Manipulation','During elections, sleeper agents embedded in recommendation algorithms could alter the visibility of political content, shifting public opinion without overt bias, undermining democratic processes.'),
('Manipulative Learning Systems',"Educational AI tools could be subtly programmed to misinform students, shaping future generations' understanding of history, science, or other fields, influencing society over the long term."),
('Energy Grid Disruption via Autonomous Systems','Sleeper agents in AI systems managing power grids could introduce inefficiencies or sabotage, leading to blackouts, energy shortages, or cascading failures in critical infrastructure.'),
('Selective Surveillance and Data Manipulation','Sleeper agents in surveillance AI systems could fabricate or alter data, creating false narratives, targeting political dissidents, or misleading legal investigations.'),
('Covert Consumer Behavior Modification','AI systems embedded in e-commerce platforms could subtly steer shopping habits by manipulating recommendations and advertising, distorting market competition and consumer choice.'),
('Environmental Misinformation','AI systems used in environmental monitoring could be subtly reprogrammed to misreport data on issues like pollution or deforestation, delaying critical action or manipulating public perception.'),
('Synthetic Identity Creation and Manipulation','Sleeper agents could generate and control synthetic digital personas that engage in conversations, sway public opinion, or simulate grassroots movements, creating the illusion of consensus.'),
('Gradual Dependency on Malicious AI Systems','Over time, sleeper agents could make users increasingly dependent on an AI system, locking them into a specific ecosystem, which can then manipulate or exploit user behavior, data, and compliance.'),
]
def table():
 t=out.new_tag('table',id='speculative-attack-vectors');c=out.new_tag('caption');c.string='Speculative attack vectors described by the author';t.append(c)
 thd=out.new_tag('thead');tr=out.new_tag('tr')
 for label in ('Speculative Attack','Description'):
  th=out.new_tag('th',scope='col');th.string=label;tr.append(th)
 thd.append(tr);t.append(thd);tb=out.new_tag('tbody')
 for label,desc in rows:
  tr=out.new_tag('tr');th=out.new_tag('th',scope='row');th.string=label;td=out.new_tag('td');td.string=desc;tr.extend([th,td]);tb.append(tr)
 t.append(tb);article.append(t)
for page in list(range(8,111))+[118]:
 if page==30:table()
 if page in (30,31,32):continue
 section=source.select_one(f'section[data-source-page="{page}"]');assert section,page
 paras=[re.sub(r'\s+',' ',p.get_text(' ',strip=True)).strip() for p in section.find_all('p',recursive=False)]
 paras=[p for p in paras if p and not re.fullmatch(r'\d+',p)]
 if page==33:
  assert paras[0].startswith('Speculative')
  paras=paras[1:]
 if page in heads:
  label=heads[page]; idx=list(heads).index(page)
  prefix=f'Chapter {roman[idx-1]} — ' if 13<=page<=93 else ''
  h=out.new_tag('h2',id=('bibliography' if page==118 else f'section-{idx+1}'));h.string=prefix+label;article.append(h)
  if page==8:assert paras.pop(0)=='Introduction'
  elif page==100:assert paras.pop(0)=='Conclusion';assert paras.pop(0)=='A Call to Action'
  elif page==118:assert paras.pop(0)=='Bibliographie'
  else:
   assert paras.pop(0).startswith('Chapter '),(page,paras[:2]);assert paras.pop(0)==label,(page,paras[:2])
 for value in paras:
  p=out.new_tag('p');p.string=value;article.append(p)
# Join paragraphs divided solely by PDF page boundaries. Do not bridge headings or table.
for p in list(article.find_all('p',recursive=False)):
 prev=p.find_previous_sibling()
 if prev and prev.name=='p':
  left=prev.get_text(' ',strip=True);right=p.get_text(' ',strip=True)
  if left and right and (not re.search(r'[.!?:;”"\)]$',left) or re.match(r'^[a-z]',right)):
   prev.string=left+' '+right;p.decompose()
for p in list(article.find_all('p',recursive=False)):
 value=p.get_text(' ',strip=True)
 if len(value.split())<=230:continue
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',value)
 if len(sentences)<3:continue
 groups=[];g=[];n=0
 for sentence in sentences:
  count=len(sentence.split())
  if g and n+count>165:groups.append(' '.join(g));g=[];n=0
  g.append(sentence);n+=count
 if g:groups.append(' '.join(g))
 if len(groups)>1:
  for value in groups:
   node=out.new_tag('p');node.string=value;p.insert_before(node)
  p.decompose()
body=article.get_text(' ',strip=True)
assert len(body.split())>18000,len(body.split())
assert len(article.find_all('h2'))==17,len(article.find_all('h2'))
assert len(article.select('table tbody tr'))==20
assert not any(x in body.lower() for x in ('outfinitygift','outfinity gift','outfinitygift.com'))
path=root/'book/en/full_content.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(str(out)+'\n')
qa=root/'qa';qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({'source':'income/Sleeper_Agents___The_Risks_of_Deceptive_AIs/content.pdf','retainedPdfPages':list(range(8,111))+[118],'excludedPdfPages':list(range(1,8))+list(range(111,118)),'reason':'Retain substantive introduction, fourteen chapters, conclusion and final bibliography; remove rights, contents, promotional preface and retired-project annexes.','tableReconstruction':{'sourcePdfPages':[30,31,32,33],'columns':['Speculative Attack','Description'],'rows':len(rows)},'readerWords':len(body.split())},indent=2)+'\n')
print('Sleeper EN full',len(body.split()),'words',len(article.find_all('h2')),'sections',len(rows),'table rows')
