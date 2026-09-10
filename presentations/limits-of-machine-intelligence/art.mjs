// Book-owned mechanical cutaway: a bounded check, a counterexample and a visibly changed guard.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));
const C={ink:'#40334e',copper:'#bd704e',petrol:'#226f82',enamel:'#ece5d8',gold:'#e5b143',danger:'#cf5257',silver:'#b4c3c5',pale:'#d5d8d0'};
function compose(i){const q=stageAuthor(),{n,path:p,text:t,dot}=q;
const put=(id,x,y,nodes,beat=1,meaning=id,scale=1)=>{q.add(q.object(id,x,y,nodes,meaning,scale));q.reveal(id,beat,1000);return id};
const stroke=(d,color=C.ink,w=8)=>q.tint(p(d,color,w),color===C.ink?'#abb8c9':color);
const txt=(s,x,y,size=35,color=C.ink)=>color===C.ink?q.tint(t(s,x,y,size,color),'#b8cad4'):t(s,x,y,size,color);
const metal=(d,fill=C.copper)=>n('path',{d,fill,stroke:C.ink,'stroke-width':3,'stroke-linejoin':'round'});
const screw=(x,y)=>[dot(x,y,7,C.silver),p(`M${x-3} ${y+3}L${x+3} ${y-3}`,C.ink,2)];
const gear=(r=110)=>{const points=Array.from({length:64},(_,j)=>{const a=j*Math.PI/32,rad=j%4<2?r:r*.83;return `${Math.cos(a)*rad},${Math.sin(a)*rad}`}).join(' ');return[n('polygon',{points,fill:C.copper,stroke:C.ink,'stroke-width':4}),dot(0,0,r*.56,C.enamel),...Array.from({length:6},(_,j)=>{const a=j*Math.PI/3;return p(`M${Math.cos(a)*20} ${Math.sin(a)*20}L${Math.cos(a)*r*.56} ${Math.sin(a)*r*.56}`,C.copper,17)}),dot(0,0,24,C.petrol),dot(0,0,8,C.silver)];};
const display=(id,value,x,y,beat=1,w=144)=>put(id,x,y,[n('rect',{x:-w/2,y:-47,width:w,height:94,rx:13,fill:C.ink}),t(value,0,23,65,C.enamel)],beat,'Integrated counter reading '+value);
const inspector=(id,x,y,beat=1,scale=.9)=>{storyPerson(q,id,x,y,{identity:'person-19-neutral',coat:C.copper,scale,ink:C.ink});const o=q.objects.at(-1);function silverHair(v){if(/hair/i.test(v.id||'')&&v.attrs?.fill)v.attrs.fill=C.silver;for(const z of v.children||[])silverHair(z);}silverHair(o.visual);q.reveal(id,beat);return id};
const housing=(id,x,y,beat=1,scale=1)=>put(id,x,y,[metal('M-295 -117L-243 -153H251L298 -111V151H-295Z',C.petrol),metal('M-295 -117H250L298 -111L250 -75H-295Z',C.silver),metal('M250 -75L298 -111V151L250 181Z',C.ink),n('rect',{x:-275,y:-93,width:501,height:250,rx:18,fill:C.enamel}),p('M-252 138H206',C.ink,7),...screw(-256,-71),...screw(204,-71),...screw(-256,133),...screw(204,133),metal('M-238 160H-180V205H-259Z',C.ink),metal('M172 160H223L243 205H172Z',C.ink)],beat,'A visibly bounded controller housing',scale);
if(i===0){
 housing('controller',720,305,1,.86);put('ratchet',605,306,gear(83),1,'The counter mechanism is physically inside the inspected controller');display('scope-ten','10',828,288,2,116);
 put('scope-mark',830,368,[t('steps checked',0,0,32,C.ink)],2,'Scope marking belongs to the ten-step check, not all future operation');
 put('lever',983,360,[p('M0 70V-68',C.copper,22),dot(0,-78,27,C.gold),metal('M-40 57H40V81H-40Z',C.ink)],1,'A proposed next action waits at the output lever');
 put('latch',928,399,[metal('M-51 -22H28V24H-51Z',C.petrol),p('M-31 0H72',C.silver,14)],2,'The permission latch is separate from the counter reading');
 inspector('engineer',276,524,1,1.05);storyGesture(q,'engineer',1,'reflect');storyGesture(q,'engineer',3,'question');storyGesture(q,'engineer',4,'resolve');
 put('inspection-hand',402,371,[p('M-56 7L0 -10L48 20',C.copper,17),dot(49,20,12,'#d1a27a')],2,'The inspector checks the physical scope-to-action connection');q.move('inspection-hand',3,422,376,1500);
}
if(i===1){
 // Macro: initial state c=0; hold or increment; bad if c>10. The ten-step scope does not include the eleventh transition.
 put('cutaway',610,310,[metal('M-435 -112L-387 -155H400L440 -107V156H-435Z',C.petrol),n('rect',{x:-405,y:-125,width:805,height:253,rx:27,fill:C.enamel}),metal('M-435 156H440V192H-435Z',C.copper),...screw(-379,-99),...screw(374,-99),...screw(-379,101),...screw(374,101)],1,'Macro view exposes the count and the checked horizon');
 put('drive',363,307,gear(117),1);put('pawl',403,193,[metal('M-12 0H80L104 42L67 57L55 23H-12Z',C.ink),dot(0,10,11,C.gold)],1);q.move('pawl',2,418,201,1100);
 display('zero','0',785,298,1,200);q.hide('zero',3);display('ten','10',785,298,3,200);q.hide('ten',4);display('eleven','11',785,298,4,200);
 put('scale',756,390,[p('M-142 0H146',C.ink,7),p('M-130 -14V14M130 -14V14',C.ink,6),t('0',-131,57,36,C.ink),t('10',131,57,36,C.ink)],2,'The proof question has a horizon ending at ten transitions');
 put('bounded-check',370,460,[metal('M-101 -28H101V32H-101Z',C.gold),t('10-step check',0,13,31,C.ink)],3,'The earlier successful result keeps its exact scope');
 put('forbidden-flag',1048,274,[p('M-30 150V-76',C.ink,9),metal('M-30 -72H69V-7H-30Z',C.danger),t('>10',20,-26,37,'#ffffff')],4,'The eleventh increment reaches the forbidden state');
 put('advance',606,313,[p('M-67 0H53L22 -24M53 0L22 24',C.copper,11)],4,'A requested transition exceeds the original question');
}
if(i===2){
 put('base',645,421,[metal('M-416 -65L-348 -105H368L416 -65V58H-416Z',C.petrol),metal('M-416 58H416L368 98H-365Z',C.ink),n('rect',{x:-385,y:-68,width:757,height:90,rx:10,fill:C.enamel})],1,'Changed controller seen from the side');
 put('old-trace',313,254,[metal('M-111 -82H111V80H-111Z',C.enamel),t('10 → 11',0,-14,41,C.ink),p('M-17 30L17 58M17 30L-17 58',C.danger,9),t('counterexample',0,-49,28,C.ink)],1,'One explicit failing trace refutes unlimited safety of the original model');q.hide('old-trace',3);
 put('wheel',771,313,gear(121),1);display('held','10',496,374,3,118);
 put('unguarded-drive',1029,373,[p('M-42 0H36L9 -24M36 0L9 24',C.copper,17)],2,'Successful prior tests alone cannot constrain the next move');q.hide('unguarded-drive',3);
 put('new-guard',696,196,[metal('M-38 -63H9L56 106L11 122L-26 15H-38Z',C.gold),dot(-15,-39,13,C.ink),p('M-57 -59H26',C.silver,12)],3,'An explicitly new physical guard prevents increments at the limit');q.move('new-guard',3,701,217,1900);
 
 put('model-change',425,490,[t('Guard added',0,0,35,C.enamel)],3,'An integrated assembly label identifies the changed model at the moment the script changes its rule');
}
if(i===3){
 // A single cutaway environment: proposal intake feeds an isolated test workspace; deployment has its own locked output.
 put('work-area',600,337,[metal('M-436 -54L-338 -141H373L453 -46V142H-436Z',C.petrol),metal('M-436 142H453L373 191H-361Z',C.ink),metal('M-410 -39L-322 -111H344L425 -25H-410Z',C.enamel),p('M-410 13H425',C.silver,7)],1,'One system contains distinct proposal, sandbox and deployment authority');
 put('proposal-desk',303,281,[metal('M-121 -31L-48 -74H107L45 -22Z',C.copper),p('M-101 -22V96M41 -19V96',C.copper,13)],1,'Patch authoring desk');
 put('patch',307,218,[metal('M-70 -66H77V40L-70 68Z',C.enamel),p('M-48 -29H54M-48 -3H26M-48 24H55',C.petrol,8)],1,'A proposed code change remains a candidate');
 put('propose-label',304,438,[t('Propose',0,0,37,C.enamel)],1);
 put('sandbox',620,270,[metal('M-126 -113L-83 -146H125V104H-126Z',C.silver),n('rect',{x:-109,y:-113,width:203,height:192,rx:7,fill:C.ink}),p('M-83 -70L-54 -43L-83 -16M-24 -14H61',C.gold,8),p('M-75 37H65',C.enamel,6),...screw(-109,-127),...screw(110,-127),p('M-135 110H139',C.copper,16)],2,'Code runs within a contained test workspace');
 put('test-label',613,438,[t('Test',0,0,37,C.enamel)],2);q.move('patch',2,452,281,1800);
 put('deployment',928,267,[metal('M-80 -110L-44 -135H88V125H-80Z',C.copper),n('rect',{x:-57,y:-79,width:110,height:142,rx:10,fill:C.ink}),p('M-9 0V-32Q-9 -61 18 -61Q45 -61 45 -32V0',C.silver,10),n('rect',{x:-20,y:-5,width:79,height:57,rx:10,fill:C.gold}),dot(18,17,8,C.ink)],3,'The external deployment latch has separate authority');
 put('deploy-label',929,438,[t('Deploy',0,0,37,C.enamel)],3);
}
if(i===4){
 housing('controller',824,344,1,.65);put('ratchet',737,337,gear(61),1);display('scope','10',900,332,1,89);put('scope-label',903,408,[t('steps',0,0,29,C.ink)],1);
 inspector('reader',320,531,1,1.03);storyGesture(q,'reader',1,'reflect');storyGesture(q,'reader',2,'explain');storyGesture(q,'reader',4,'reflect');storyGesture(q,'reader',5,'invite');
 put('book-rest',500,450,[metal('M-130 -19L15 -55L147 -17L-8 18Z',C.petrol),p('M-22 11V108',C.petrol,13),p('M-80 111H42',C.petrol,14)],1,'The actual book is being consulted beside the machine it helps question',.85);
 put('open-book',500,397,[metal('M-137 -54Q-73 -83 0 -47Q67 -88 137 -61L129 92Q64 67 0 105Q-71 68 -140 95Z',C.copper),n('path',{d:'M-125 -57Q-69 -74 0 -37Q69 -76 123 -61L117 77Q59 63 0 96Q-62 64 -127 80Z',fill:C.enamel}),p('M0 -36V94',C.copper,4),t('Practical',-66,1,31,C.ink),t('warrant',-66,35,31,C.ink),p('M28 -8H99M28 18H96M28 43H83M-105 56H-27',C.petrol,4)],1,'Reader opens the specific practical-verification chapter',.85);
 put('output-latch',1064,420,[p('M-37 -63V55',C.copper,17),dot(-37,-68,18,C.gold),p('M-73 10H4',C.silver,15)],2,'The same scope-to-action question remains visible at the end');
}
for(const action of q.actions)if(action.actor==='old-trace'&&action.action==='disappear')action.durationMs=160;
for(const actor of q.objects.filter(o=>o.options?.rig==='character'))for(const [j,emotion]of ['curious','skeptical','determined'].entries())q.actions.push({actor:actor.id,action:'character.express',emotion,beat:Math.min(scenes[i].lines.length,1+j*2),durationMs:1100});
return q.finish(['An older engineer inspects the separate link between a ten-step scope and action permission.','Original toy controller starts at zero; ten bounded steps pass, an explicitly additional eleventh step reaches c>10.','Spoken and visible model change adds a guard; its invariant belongs to the changed controller.','The source code-generation example separates proposal, sandbox tests and independently gated deployment.','A reader consults the real practical-verification chapter beside the scoped controller.'][i]);}
for(let i=0;i<scenes.length;i++)scenes[i].visual=compose(i);fs.writeFileSync(path.join(root,'work/scenes.json'),JSON.stringify(scenes,null,2)+'\n');
