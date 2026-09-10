from pathlib import Path
import json,re,shutil
w=Path('presentations/borrowed-credibility');r=w/'review-revision';old=r/'previous-version';old.mkdir(exist_ok=True)
for f in ['scenes.json','editorial.json','production.json','film.direction.json','voice-receipts.json']:
 if not (old/f).exists():shutil.copy2(w/'work'/f,old/f)
for f in ['art.mjs','PRODUCTION.md']:
 if not (old/f).exists():shutil.copy2(w/f,old/f)
prod=json.loads((old/'production.json').read_text());pub=Path(prod['bookDirectory'])/'Animation'/f"{prod['id']}.shf"
if not (old/pub.name).exists():shutil.copy2(pub,old/pub.name)
manifest=Path(prod['bookDirectory'])/'manifest.json'
if not (old/'manifest.json').exists():shutil.copy2(manifest,old/'manifest.json')
t=(r/'SCRIPT-AND-ART.md').read_text();speech=t.split('## Full spoken script',1)[1].split('## Original visual direction',1)[0];groups=re.split(r'^### Scene \d+ — ',speech,flags=re.M)[1:]
art=t.split('## Original visual direction',1)[1].split('## Source and scope',1)[0];refs=[[4,5,7,8],[5,40,41],[40,41,42],[6,41,69,71]]
gestures=[['Inspect the same manuscript','Attend to the review queue','Lift identity cover slip','Look back at unchanged result','Pause before a verdict'],['Introduce the composite researcher','Open supporting record','Set affiliation aside for this check','Trace source marks to statement','Expose supporting margin','Place a question on separate note'],['Compare measurement and interpretation','Bracket only the interpretation','Preserve original data marks','Record verification labour','Keep allocation question unresolved'],['Inspect proposed mapping against source','Mark extracted relation for checking','Turn to the manuscript chapter','Move bookmark to correction chapter','Hold the reading invitation open']]
ss=[]
for i,g in enumerate(groups):
 title=g.splitlines()[0];lines=re.findall(r'^\d+\. (.+)$',g,re.M);sid=re.sub('[^a-z0-9]+','-',title.lower()).strip('-');states=['curiosity','attention','reflection','concern','reflection','curiosity'][:len(lines)];ep={'arc':'curiosity → inspection → uncertainty → reading invitation','purpose':title,'states':states,'intensities':[.35]*len(lines),'gestures':gestures[i],'sentenceDirection':[{'sentence':n+1,'feeling':states[n],'visualAction':[v],'intensity':.35} for n,v in enumerate(gestures[i])],'visualActing':art}
 ss.append({'id':sid,'title':title,'lens':'book','sources':refs[i],'lines':lines,'pauseAfterMs':[1450]*(len(lines)-1)+[2200],'emotionalPlan':ep,'visual':{'objects':[],'actions':[],'connections':[],'meaning':art}})
assert len(ss)==4 and sum(len(s['lines']) for s in ss)==21
(w/'work/scenes.json').write_text(json.dumps(ss,ensure_ascii=False,indent=2)+'\n')
(w/'work/script.md').write_text('# Borrowed Credibility\n\n'+'\n\n'.join('## '+s['title']+'\n\n'+'\n\n'.join(s['lines']) for s in ss)+'\n')
e=json.loads((old/'editorial.json').read_text());secs=json.loads((w/'source/sections.json').read_text());raw=(w/'source/source.txt').read_text().encode('utf-16-le');slice16=lambda a,z:raw[a*2:z*2].decode('utf-16-le')
e.update(targetMinutes=2.5,centralQuestion='When does useful scientific reputation substitute for evidence about a particular claim?',thesis='The book follows institutional credibility through a composite manuscript and proposes more local, inspectable and funded correction.',narrativeFramework={'why':ss[0]['lines'][0],'how':'The unchanged composite manuscript separates pedigree, supporting evidence and local correction.','what':'Read the institutional incentive argument before judging its proposed reforms.'})
e['claims']=[{'id':'claim-'+s['id'],'statement':' '.join(s['lines']),'kind':'source-claim','noveltyScope':'within-source','spans':[{'sourceId':secs[k]['id'],'start':secs[k]['start'],'end':secs[k]['end'],'quote':slice16(secs[k]['start'],secs[k]['end'])}for k in s['sources']]}for s in ss]
e['scenePlan']=[{'id':s['id'],'lens':'book','purpose':s['title'],'emotionalPlan':s['emotionalPlan']}for s in ss]
e['hooks']=[{'question':ss[0]['lines'][0],'introducedSceneId':ss[0]['id'],'status':'open-by-design','reason':'Selected example earns interest in the full institutional proposal without claiming validation.','sourceClaimIds':['claim-'+ss[0]['id']]}]
e['readerInvitation'].update(reasonToExist=' '.join(ss[0]['lines'][:2]),readerPromise=ss[-1]['lines'][3],closingInvitation=ss[-1]['lines'][2],readerOutcomes=[ss[1]['lines'][-1],ss[2]['lines'][3],ss[-1]['lines'][3]],contentSamples=[{'sceneId':s['id'],'readingValue':s['lines'][-1]}for s in ss[1:3]])
e['originalIllustrations']=[{'id':'schematic-local-review','status':'Explicitly imagined reviewer questions interpretation while measurement retained; no invented real study or result.','sourceBasis':['source-40']}]
e['sourceImageReview']=json.loads((r/'source-evidence.json').read_text())['sourceImageInspection'];e['review']={'scriptApproved':True,'independentReport':'presentations/qa/quality-review-borrowed-credibility-proposal-independent.json','scope':'Full21-line draft and cited complete source ranges; no fresh whole-book read.'}
(w/'work/editorial.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');prod.update(minDurationMs=120000,maxDurationMs=180000);(w/'work/production.json').write_text(json.dumps(prod,ensure_ascii=False,indent=2)+'\n')
p=r/'progress.json';d=json.loads(p.read_text());d.update(status='approved21-line script installed in workspace; local voice next',publicChanged=False,archive=str(old));p.write_text(json.dumps(d,indent=2)+'\n')
print('Prepared 4 scenes,21 lines; old public film and editable work preserved.')
