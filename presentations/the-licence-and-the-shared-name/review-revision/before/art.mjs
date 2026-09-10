import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));const scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));

function baseCompose(i){const a=stageAuthor(),blue='#477699',coral='#d58755',green='#63a393',pale='#e5e4da';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};
 const code=(id,x,y,b=1)=>put(id,x,y,[a.n('rect',{x:-115,y:-85,width:230,height:170,rx:13,fill:blue}),a.path('M-35 -34 L-70 0 L-35 34 M35 -34 L70 0 L35 34 M12 -49 L-12 49',pale,10)],b,'Technical rights allow continued use of the open code');
 const name=(id,x,y,b=1)=>put(id,x,y,[a.n('path',{d:'M-130 -58 H130 V58 H-130Z',fill:green}),a.text('Shared name',0,11,34,'#ffffff')],b,'Representation under a common name carries a distinct proposed compact');
 if(i===0){code('code',310,285);name('name',885,285,2);put('split',600,315,[a.path('M0 -130 V130',coral,14)],3,'Technical permission and authority to represent a brand are separate');put('label',600,515,[a.text('Freedom and responsibility use different instruments',0,0,32)],4);}
 if(i===1){code('code',325,300);put('copy',325,300,[a.n('path',{d:'M-45 -40 H45 V40 H-45Z',fill:pale}),a.path('M-24 0 H24',blue,8)],2);a.move('copy',3,700,300);name('name',935,235,1);put('reputation',910,415,[a.dot(-50,0,24,coral),a.dot(10,0,24,green),a.dot(70,0,24,blue),a.text('Reputation · relationships',0,100,32)],2,'Access to code does not itself transfer reputation and customers');}
 if(i===2){put('technical',320,315,[a.path('M-160 70 H160 M-120 70 V140 M120 70 V140',blue,13)],1);code('code',320,275);put('compact',865,290,[a.n('path',{d:'M-140 -130 H140 V130 H-140Z',fill:pale}),a.text('Name',0,-70,35,blue),a.text('Contribution',0,-15,34,blue),a.text('Authority',0,40,34,blue),a.text('Exit',0,95,35,blue)],2);put('choice',595,300,[a.path('M-75 0 H75 L45 -27 M75 0 L45 27',coral,11)],3,'Brand participation is voluntary and has separately defined responsibilities');}
 if(i===3){code('code',295,295);name('name',900,230,2);put('custodian',900,365,[a.dot(0,-20,25,coral),a.n('path',{d:'M-40 65 Q-43 11 0 11 Q43 11 40 65Z',fill:blue})],3);put('mandate',900,485,[a.text('Limited mandate',0,0,34)],3);put('continue',600,405,[a.path('M-95 0 H95 L65 -28 M95 0 L65 28',green,12)],4,'A limited custodian does not own all technical futures');}
 return a.finish('An open code workbench remains distinct from a shared sign and its compact; copying, reputation, voluntary participation and limited custodianship are visually differentiated without offering legal advice.');}

function compose(i){if(i!==0)return baseCompose(i);const a=stageAuthor(),navy='#426f94',coral='#d67f60',green='#5ea58f',gold='#ddb052',cream='#e9e6d8';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};const figure=(id,x,y,c,identity='person-04-neutral',seated=false,scale=.95)=>{storyPerson(a,id,x,y,{coat:c,identity,seated,scale});a.reveal(id,1);};
figure('developer',240,492,green,'person-04-neutral',true,.95);storyGesture(a,'developer',2,'reflect');put('workstation',470,400,[a.path('M-230 15 H225 M-175 15 V140 M180 15 V140',navy,15),a.n('rect',{x:-147,y:-200,width:285,height:167,rx:14,fill:navy}),a.n('rect',{x:-126,y:-180,width:243,height:128,rx:6,fill:cream}),a.path('M-42 -150 L-74 -116 L-42 -82 M28 -150 L60 -116 L28 -82 M6 -159 L-18 -73',green,12)],1,'Open technical rights allow continued work on code');put('shared-sign',950,200,[a.n('path',{d:'M-142 -50 H142 V50 H-142Z',fill:coral}),a.text('Shared name',0,11,35,'#ffffff')],2);figure('custodian',960,495,navy,'person-02-neutral',false,.88);storyGesture(a,'custodian',3,'question');put('compact',760,355,[a.n('path',{d:'M-76 -95 H76 V95 H-76Z',fill:cream}),a.text('Rules',0,-43,34,navy),a.path('M-42 -4 H43 M-42 33 H43 M-42 70 H20',green,8)],3,'Representing the shared name carries a separate proposed compact');put('fork',600,490,[a.path('M-80 0 H10 L95 -46 M10 0 L95 42',gold,12)],4,'The technical future is not owned by the name custodian');

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
