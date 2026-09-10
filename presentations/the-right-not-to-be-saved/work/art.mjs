import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);
const human=(id,x,y,coat,identity='person-02-neutral',seated=false,scale=.9)=>{storyPerson(a,id,x,y,{coat,identity,seated,scale,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;for(const [beat,emotion]of [[1,'curious'],[3,'worried'],[5,'skeptical'],[6,'curious']])a.actions.push({actor:id,action:'character.express',emotion,beat,durationMs:850});storyGesture(a,id,2,'question');storyGesture(a,id,4,'reflect');storyGesture(a,id,6,'invite');};

const teal='#258d86',tn='#98d8c8',coral='#d17550',cn='#efb996',gold='#e0b144',gn='#f4d78e',blue='#5275b2';
const threshold=()=>obj('threshold',600,339,[fill('M-166 175V-170Q0 -222 166 -170V175H127V-141Q0 -176 -127 -141V175Z',teal,tn),fill('M-253 175L-126 118H126L253 175L286 203H-286Z',gold,gn)],'An architectural threshold makes access and authority physically distinct');
if(i===0){threshold();human('helper',344,536,teal,'person-02-neutral',false,1);human('recipient',857,536,coral,'person-03-neutral',false,.97);obj('offered-parcel',458,435,[fill('M-37 -35H37V34H-37Z',gold,gn),path('M-37 -11H37M0 -35V34',blue,5)],'A valuable offer remains outside the other person’s decision space');a.reveal('offered-parcel',3);}
else if(i===1){threshold();obj('training-bench',864,442,[rect(-126,-2,253,22,coral,cn),path('M-100 21V94M99 21V94','$ink',11),fill('M-58 -41L-18 -74L28 -30L74 -53V-2H-58Z',blue,'#a9bce6')],'A practical training task makes readiness more than an exclusion label');human('learner',322,540,gold,'person-03-neutral',false,.96);a.move('learner',4,459,540);human('teacher',1010,527,teal,'person-02-neutral',false,.82);}
else if(i===2){obj('community',600,394,[fill('M-427 141V-127H-222V141H-248V-94H-401V141ZM222 141V-127H427V141H400V-94H247V141Z',teal,tn),fill('M-186 146Q0 68 186 146L223 188H-223Z',gold,gn)],'Exit connects two jurisdictions without making either absolute');human('member',552,527,coral,'person-03-neutral',false,.93);human('outside',902,527,blue,'person-02-neutral',false,.85);a.move('member',4,667,527);obj('stop-condition',743,413,[path('M-28 -15L0 12L34 -29',teal,11)],'The ability to stop an intervention must be more than a promise');a.reveal('stop-condition',5);}
else{threshold();human('reader',613,538,coral,'person-03-neutral',false,1.09);a.move('reader',4,684,538);}

s.visual=a.finish(s.lines[0]+' Original material staging, a richer foreground palette and expressive participants make the particular question visible.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
