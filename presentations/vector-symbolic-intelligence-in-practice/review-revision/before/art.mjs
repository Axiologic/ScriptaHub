import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));const scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));

function baseCompose(i){const a=stageAuthor(),blue='#3e76aa',orange='#bd7950',pale='#e0e0e8';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};
 const role=(id,x,y,t,c,b)=>put(id,x,y,[a.n('path',{d:'M-95 -50 H95 V50 H-95Z',fill:c}),a.text(t,0,12,32,'#ffffff')],b,t);
 if(i===0){role('actor',260,250,'Actor',blue,1);role('recipient',260,410,'Recipient',orange,1);put('binding',620,315,[a.path('M-155 -70 C-40 -70 -40 70 80 70 M-155 90 C-35 90 -35 -70 80 -70',blue,15),a.path('M-130 70 C-10 70 -10 -70 110 -70',orange,15)],2,'Role-preserving binding is an experimental obligation');put('decode',980,315,[a.n('path',{d:'M-65 -110 H65 V110 H-65Z',fill:pale}),a.text('Readout',0,-42,30,'#304254'),a.text('?',0,42,68,blue)],3);put('question',650,520,[a.text('Which operation survived?',0,0,34)],4);}
 if(i===1){put('bag',345,305,[a.n('path',{d:'M-105 -80 H105 L125 100 H-125Z',fill:pale}),a.text('Words',0,-20,35,'#304254'),a.dot(-42,42,17,blue),a.dot(8,22,17,orange),a.dot(47,48,17,blue)],1,'An index can preserve words without preserving event roles');role('actor',840,220,'Actor',blue,2);role('recipient',840,410,'Recipient',orange,2);put('relation',840,315,[a.path('M0 -55 V55 L-24 28 M0 55 L24 28',blue,12)],3,'Order and roles carry semantic information');}
 if(i===2){put('carrier',290,310,Array.from({length:15},(_,j)=>a.n('rect',{x:(j%5)*35-90,y:Math.floor(j/5)*48-73,width:24,height:28+(j%3)*12,rx:5,fill:j%2?blue:orange})),1,'The representation is held fixed during a decoder comparison');put('readout',670,315,[a.n('path',{d:'M-105 -90 H105 V90 H-105Z',fill:pale}),a.text('Decoder',0,10,35,'#304254')],2);put('old',670,315,[a.path('M-40 -40 L40 40 M40 -40 L-40 40',orange,13)],2,'The tested readout produces an error');a.hide('old',3);put('repair',960,315,[a.path('M-45 0 L-10 34 L55 -46',blue,15),a.text('Tested setting',0,155,32)],4,'A changed readout fixes the observed error within the tested full-rank linear setting');}
 if(i===3){put('storage',390,320,[...Array.from({length:5},(_,j)=>a.n('path',{d:`M${j*35-140} ${40-j*22} H${j*35-55} V${115-j*22} H${j*35-140}Z`,fill:j%2?orange:blue})),a.text('Explicit growth',0,185,34)],1,'Removing interference can increase storage cost');put('test',870,300,[a.n('path',{d:'M-100 -110 H100 V110 H-100Z',fill:pale}),a.text('Operation',0,-50,34,'#304254'),a.text('Cost',0,1,38,'#304254'),a.text('Failure',0,52,35,'#304254')],2);put('compare',650,480,[a.text('Conclusions stay reversible',0,0,34)],4);}
 return a.finish('Original representation laboratory distinguishes indexing, role-preserving operations, decoder behavior and explicit storage; no new numerical performance or universal VSA claim is invented.');}

function compose(i){if(i!==0)return baseCompose(i);const a=stageAuthor(),navy='#426f94',coral='#d67f60',green='#5ea58f',gold='#ddb052',cream='#e9e6d8';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};const figure=(id,x,y,c,identity='person-04-neutral',seated=false,scale=.95)=>{storyPerson(a,id,x,y,{coat:c,identity,seated,scale});a.reveal(id,1);};
figure('giver',300,490,green,'person-04-neutral',false,.9);figure('receiver',915,490,coral,'person-09-neutral',false,.9);storyGesture(a,'giver',2,'explain');storyGesture(a,'receiver',3,'question');put('parcel',435,350,[a.n('path',{d:'M-43 -38 H43 V38 H-43Z',fill:gold}),a.path('M0 -38 V38 M-43 -8 H43',cream,7)],1,'An illustrative event gives its participants different roles');a.move('parcel',2,760,350);put('event',600,175,[a.text('Who gave what to whom?',0,0,37)],1);put('binding',600,315,[a.path('M-95 65 C-40 -100 40 100 95 -65',navy,13)],3,'Role-preserving representation must distinguish an event from an unordered word set');put('labels',600,545,[a.text('Actor',-300,0,34),a.text('Recipient',315,0,34)],3);put('readout',600,455,[a.n('rect',{x:-105,y:-34,width:210,height:67,rx:12,fill:cream}),a.text('Readout?',0,12,34,navy)],4);

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
