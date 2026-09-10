import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));const scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));

function baseCompose(i){const a=stageAuthor(),slate='#527285',ochre='#b8844d',pale='#e5e0d1';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};
 if(i===0){put('frontier',490,300,[a.n('path',{d:'M-250 -75 H150 V75 H-250Z',fill:pale}),...[-200,-100,0,100].map(x=>a.path(`M${x-22} 0 L${x-4} 20 L${x+28} -22`,slate,10)),a.text('Certified domain',-50,170,34)],1);put('unfold',895,300,[a.n('path',{d:'M-155 -75 L-55 -115 L45 -75 L145 -115 V35 L45 75 L-55 35 L-155 75Z',fill:slate}),a.text('Unperformed extension',0,170,32)],2,'Continuation is not a completed totality');put('boundary',690,300,[a.path('M0 -115 V110',ochre,14)],3,'The certificate stops where its conditions stop');}
 if(i===1){put('finite',350,290,[...Array.from({length:25},(_,j)=>a.n('rect',{x:(j%5)*39-95,y:Math.floor(j/5)*39-95,width:30,height:30,rx:4,fill:slate})),a.text('Finite domain',0,175,34)],1);put('clock',865,295,[a.n('circle',{cx:0,cy:0,r:100,fill:pale}),a.path('M0 -65 V0 L60 34',ochre,13),a.text('Verification cost',0,170,34)],2,'Exhaustive checking can be finite and still impractical');put('question',605,300,[a.text('Feasible?',0,0,36)],3);}
 if(i===2){put('certificate',345,290,[a.n('path',{d:'M-110 -120 H110 V120 H-110Z',fill:pale}),a.text('Domain',0,-53,36,'#354855'),a.text('Precision',0,1,34,'#354855'),a.text('Horizon',0,54,35,'#354855')],1);put('extension',895,295,[a.path('M-160 70 L-60 -55 L40 25 L135 -75',slate,14),a.text('New conditions',0,175,34)],2);put('transfer',620,295,[a.path('M-80 0 H80 L49 -26 M80 0 L49 26',ochre,12)],3,'Transferring a result across frontiers requires justification');a.hide('transfer',4);put('unknown',620,305,[a.text('?',0,23,80,ochre)],4);}
 if(i===3){put('known',360,300,[a.n('path',{d:'M-150 -90 H150 V90 H-150Z',fill:pale}),a.path('M-72 0 L-22 44 L76 -57',slate,16),a.text('Bounded warrant',0,180,34)],1);put('unresolved',880,300,[a.n('path',{d:'M-125 -75 L-20 -120 L100 -65 V85 L-20 125 L-125 75Z',fill:slate}),a.text('?',0,20,70,'#ffffff'),a.text('Open continuation',0,180,32)],2);put('cost',610,520,[a.text('Conditions · cost · fallback',0,0,34)],4);}
 return a.finish('A folding finite frontier separates checked tiles from unperformed continuation and makes certificate transport conditional; classical impossibility results are not depicted as defeated.');}

function compose(i){if(i!==0)return baseCompose(i);const a=stageAuthor(),navy='#426f94',coral='#d67f60',green='#5ea58f',gold='#ddb052',cream='#e9e6d8';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};const figure=(id,x,y,c,identity='person-04-neutral',seated=false,scale=.95)=>{storyPerson(a,id,x,y,{coat:c,identity,seated,scale});a.reveal(id,1);};
put('bridge',570,410,[a.path('M-370 45 H90 M-340 45 V125 M30 45 V125',navy,16),...[-315,-225,-135,-45,45].map(x=>a.n('path',{d:`M${x-35} -5 H${x+35} V39 H${x-35}Z`,fill:green})),a.path('M150 -5 L240 -42 L325 -5 L415 -42 V2 L325 39 L240 2 L150 39Z',gold,12)],1,'A checked finite walkway ends before its unperformed continuation');figure('inspector',290,398,coral,'person-04-neutral',false,.9);storyGesture(a,'inspector',2,'reflect');put('probe',460,355,[a.path('M-45 -30 L45 30 M-45 30 L45 -30',navy,12)],2);a.move('probe',3,600,395);put('mark',630,410,[a.path('M0 -115 V60',coral,14)],3,'The warrant stops at the checked boundary');put('extension',960,275,[a.text('Not yet checked',0,0,34)],4);put('labels',550,545,[a.text('Finite does not mean inexpensive',0,0,34)],5);

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
