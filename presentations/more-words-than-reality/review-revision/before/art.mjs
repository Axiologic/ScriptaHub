import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));const scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));

function baseCompose(i){const a=stageAuthor(),navy='#586082',rust='#b97854',pale='#e7e0d7';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};
 const stack=(id,x,y,b=1)=>put(id,x,y,[...Array.from({length:5},(_,j)=>a.n('path',{d:`M${-115+j*6} ${-100+j*17} H${105+j*6} V${55+j*17} H${-115+j*6}Z`,fill:j===4?pale:navy})),a.path('M-40 15 H100 M-40 52 H80',navy,10)],b,'A convincing package of theory, code, tests and self-review');
 if(i===0){stack('package',360,290);put('table',845,345,[a.path('M-180 70 H180 M-135 70 V145 M135 70 V145',navy,14),a.n('path',{d:'M-68 -105 H68 V35 H-68Z',fill:pale}),a.path('M-38 -63 L38 0 M38 -63 L-38 0',rust,10)],2,'An independent test can challenge the apparent result');put('page',570,285,[a.n('path',{d:'M-43 -62 H43 V62 H-43Z',fill:pale})],3);a.move('page',4,715,295);put('label',600,530,[a.text('Apparent maturity → independent scrutiny',0,0,33)],5);}
 if(i===1){stack('package',320,280);put('target',840,290,[a.n('circle',{cx:0,cy:0,r:100,fill:'none',stroke:navy,'stroke-width':12}),a.n('circle',{cx:0,cy:0,r:44,fill:'none',stroke:navy,'stroke-width':10}),a.text('Intended problem',0,190,34)],1);put('nearby',1060,215,[a.dot(0,0,24,rust)],2,'The demonstrated result may address a nearby but different problem');put('arrow',600,305,[a.path('M-60 0 L60 -20',rust,12)],3);a.move('arrow',4,960,235);}
 if(i===2){put('claim',600,270,[a.n('path',{d:'M-150 -75 H150 V75 H-150Z',fill:pale}),a.text('Claim',0,0,40,'#3d4560')],1);put('status',600,440,[a.text('Assumed',-305,0,34),a.text('Tested',0,0,34),a.text('Demonstrated',310,0,32)],1);put('cursor',295,477,[a.path('M-68 0 H68',rust,10)],1);a.move('cursor',2,600,477);put('test',265,265,[a.path('M-38 -60 V0 L-75 65 Q0 90 75 65 L38 0 V-60',navy,12)],2,'Execution challenges one aspect of the claim');put('counter',945,265,[a.path('M-55 -55 L55 55 M55 -55 L-55 55',rust,14)],3,'A counterexample challenges another');}
 if(i===3){stack('package',340,280);a.hide('package',2);put('remaining',340,340,[a.n('path',{d:'M-95 -45 H95 V45 H-95Z',fill:pale}),a.text('Survives?',0,10,36,'#3d4560')],3,'Remove presentational maturity and inspect the contribution');put('desk',850,335,[a.path('M-170 80 H170 M-125 80 V145 M125 80 V145',navy,14),a.n('path',{d:'M-70 -110 H70 V40 H-70Z',fill:pale}),a.path('M-38 -50 L-10 -20 L44 -78',rust,12)],2);put('institution',600,525,[a.text('Evidence and incentives both matter',0,0,34)],4);}
 return a.finish('An impressive research stack meets an independent execution bench, a misplaced target and explicit epistemic status; scrutiny, not presentation volume, determines what remains.');}

function compose(i){if(i!==0)return baseCompose(i);const a=stageAuthor(),navy='#426f94',coral='#d67f60',green='#5ea58f',gold='#ddb052',cream='#e9e6d8';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};const figure=(id,x,y,c,identity='person-04-neutral',seated=false,scale=.95)=>{storyPerson(a,id,x,y,{coat:c,identity,seated,scale});a.reveal(id,1);};
figure('reviewer',980,505,green,'person-04-neutral');storyGesture(a,'reviewer',2,'reflect');storyGesture(a,'reviewer',4,'question');put('package',310,315,[...Array.from({length:5},(_,j)=>a.n('path',{d:`M${-125+j*12} ${-142+j*22} H${85+j*12} V${25+j*22} H${-125+j*12}Z`,fill:j===4?cream:navy})),a.text('Theory',35,-12,34,navy),a.path('M-34 33 H100 M-34 70 H62',green,10)],1);put('bench',650,400,[a.path('M-170 35 H185 M-125 35 V135 M135 35 V135',navy,15),a.n('rect',{x:-137,y:-143,width:251,height:145,rx:10,fill:navy}),a.n('rect',{x:-119,y:-125,width:215,height:104,rx:5,fill:cream}),a.path('M-50 -58 L-17 -30 L42 -73',coral,10)],2);put('claim',440,420,[a.n('path',{d:'M-34 -52 H34 V52 H-34Z',fill:gold})],2);a.move('claim',3,615,420);put('test-label',650,235,[a.text('Independent test',0,0,34)],2);

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
