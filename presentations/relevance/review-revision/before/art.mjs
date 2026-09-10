import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));const scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));

function baseCompose(i){const a=stageAuthor(),blue='#4d779d',coral='#d58b55',green='#61a693',pale='#e5e5dc';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};
 const method=(id,x,y,b=1)=>put(id,x,y,[a.n('path',{d:'M-76 -100 H76 V100 H-76Z',fill:pale}),a.path('M-42 44 L-14 -23 L12 5 L44 -55',blue,11)],b,'One unchanged artifact is assessed in different contexts');
 if(i===0){method('artifact',600,275);put('gallery',275,295,[a.path('M-130 115 V-105 H130 V115 M-130 115 H130',blue,12),a.dot(0,-25,48,coral),a.text('Cultural context',0,210,32)],2);put('lab',950,315,[a.path('M-150 75 H150 M-100 75 V125 M100 75 V125',green,14),a.n('path',{d:'M-32 -100 H32 V-28 L77 47 H-77 L-32 -28Z',fill:blue}),a.text('Research context',0,190,32)],3);a.move('artifact',4,690,280);}
 if(i===1){method('artifact',570,300);put('river',945,330,[a.path('M-95 -130 C80 -72 -80 28 95 105',blue,40),a.path('M-100 -25 H100 M-100 15 H100',coral,12),a.text('A local decision',0,190,33)],2,'An illustrative context where a method may become consequential');put('shelf',270,310,[a.path('M-105 110 H105 M-105 -98 V110 M105 -98 V110',green,13),a.text('Other priorities',0,210,32)],1);a.move('artifact',3,705,300);put('fixed',560,500,[a.text('Same artifact',0,0,34)],4);}
 if(i===2){put('table',600,360,[a.path('M-390 80 H390 M-325 80 V135 M325 80 V135',blue,13)],1);put('dossier',600,285,[a.n('path',{d:'M-140 -95 H140 V95 H-140Z',fill:pale}),a.text('Decision',0,-37,36,blue),a.text('Context · values',0,20,32,blue)],1);for(const[id,x,t,c,b]of[['critic-a',265,'Feasibility',green,2],['critic-b',960,'Contribution',coral,3]])put(id,x,290,[a.dot(0,-35,26,c),a.n('path',{d:'M-46 53 Q-50 0 0 0 Q50 0 46 53Z',fill:c}),a.text(t,0,120,32)],b);put('disagreement',600,470,[a.text('Disagreement stays visible',0,63,33)],4);}
 if(i===3){put('familiar',400,295,[...[-110,0,110].map(x=>a.n('path',{d:`M${x-40} -90 H${x+40} V90 H${x-40}Z`,fill:blue})),a.text('Earlier success',0,190,34)],1);put('unfamiliar',880,295,[a.n('path',{d:'M-90 -62 L25 -115 L95 12 L-15 105 L-100 30Z',fill:coral}),a.n('circle',{cx:10,cy:-10,r:31,fill:pale}),a.text('Unfamiliar value',0,190,34)],2);put('room',605,430,[a.path('M0 -115 V40',green,13)],3,'Recognized patterns should not exclude exploratory work');a.hide('room',4);}
 return a.finish('One artifact remains unchanged while cultural, scientific and local decision contexts change; a plural review table and unfamiliar object keep judgment inspectable without collapsing it into popularity.');}

function compose(i){if(i!==0)return baseCompose(i);const a=stageAuthor(),navy='#426f94',coral='#d67f60',green='#5ea58f',gold='#ddb052',cream='#e9e6d8';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};const figure=(id,x,y,c,identity='person-04-neutral',seated=false,scale=.95)=>{storyPerson(a,id,x,y,{coat:c,identity,seated,scale});a.reveal(id,1);};
put('gallery',300,325,[a.path('M-135 130 V-120 H135 V130 M-135 130 H135',navy,14),a.n('path',{d:'M-98 -77 H98 V68 H-98Z',fill:cream}),a.path('M-73 35 L-17 -43 L22 21 L72 -18',green,10)],1,'The same artifact can enter a cultural context');figure('viewer',170,495,coral,'person-09-neutral',false,.72);storyGesture(a,'viewer',2,'reflect');put('planning-table',890,380,[a.n('path',{d:'M-155 -62 H155 L183 27 H-180Z',fill:cream}),a.path('M-125 27 V132 M130 27 V132',navy,14),a.path('M-105 -18 L-35 -34 L10 2 L100 -24',green,10)],2,'A local decision gives the same artifact another relevance');figure('planner',1020,492,green,'person-04-neutral',false,.85);storyGesture(a,'planner',3,'explain');put('artifact',585,300,[a.n('path',{d:'M-64 -90 H64 V90 H-64Z',fill:cream}),a.path('M-39 33 L-12 -47 L12 10 L42 -27',green,10)],1);a.move('artifact',3,755,290);put('labels',595,550,[a.text('The work stays · the context changes',0,0,33)],4);

return a.finish('Original enacted situation: task-specific work, visible participants, source-grounded causal distinction and meaningful motion; illustrative objects do not claim an empirical experiment.');}

for(let i=0;i<scenes.length;i++){
 const visual=compose(i);
 for(const actor of visual.objects.filter(o=>o.options?.rig==='character')){
  const affected=/patient|visitor/.test(actor.id), reflective=/author|reader|reviewer|evaluator|judge/.test(actor.id);
  const states=affected?['curious','worried','worried']:reflective?['curious','skeptical','determined']:['curious','skeptical','determined'];
  for(const [j,beat] of [1,3,5].entries())visual.actions.push({actor:actor.id,action:'character.express',emotion:states[j],beat,durationMs:900});
 }
 scenes[i].visual=visual;
}fs.writeFileSync(path.join(root,'work/scenes.json'),JSON.stringify(scenes,null,2)+'\n');
