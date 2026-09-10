import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);
const human=(id,x,y,coat,identity='person-02-neutral',seated=false,scale=.9)=>{storyPerson(a,id,x,y,{coat,identity,seated,scale,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;for(const [beat,emotion]of [[1,'curious'],[3,'worried'],[5,'skeptical'],[6,'curious']])a.actions.push({actor:id,action:'character.express',emotion,beat,durationMs:850});storyGesture(a,id,2,'question');storyGesture(a,id,4,'reflect');storyGesture(a,id,6,'invite');};

const teal='#288f88',tn='#99d8c4',coral='#d67d58',cn='#efbd9b',gold='#e4b247',gn='#f6db97',violet='#7b72b1';
const bridge=()=>obj('scaffold',603,411,[path('M-417 36H-53M54 36H417M-353 36V136M-197 36V136M198 36V136M354 36V136',teal,15),path('M-356 131L-199 43M196 45L353 130',coral,8),rect(-60,28,120,20,gold,gn)],'A temporary scaffold spans a genuine gap rather than declaring it absent');
if(i===0||i===1){bridge();human('learner',441,450,coral,'person-03-neutral',false,.94);human('supporter',856,450,teal,'person-02-neutral',false,.88);a.move('learner',4,565,450);if(i===1){obj('toll',695,294,[rect(-17,-37,34,181,violet,'#c2bbe3'),fill('M-17 -37H118L92 31H-17Z',gold,gn),text('Exemption',55,-1,26,'#294b57')],'The same support can be converted into a privilege that blocks reciprocal scrutiny');a.reveal('toll',3);a.hide('toll',6);}}
else if(i===2){obj('review-table',606,456,[rect(-334,-11,668,29,teal,tn),path('M-280 18V99M279 18V99','$ink',13)],'A discrepancy is reviewed beside the work it describes');human('reviewer',354,551,coral,'person-03-neutral',true,.96);obj('passport',771,369,[rect(-193,-138,386,211,'#ebddbd','#d5d9bd',9),text('Declared norm',0,-81,33,'#294b57'),text('Observed conduct',0,-31,33,'#294b57'),text('Who carries the cost?',0,23,30,'#294b57'),path('M-145 44H145',violet,5)],'The proposed passport exposes the norm, evidence and burden rather than certifying innocence');a.reveal('passport',3);}
else{bridge();human('learner',590,450,coral,'person-03-neutral',false,1.04);a.move('learner',4,674,450);obj('repair',803,421,[rect(-58,-20,116,23,gold,gn)],'The gap can narrow through actual work while the ideal remains demanding');a.reveal('repair',4);}

s.visual=a.finish(s.lines[0]+' Original material staging, a richer foreground palette and expressive participants make the particular question visible.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
