import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));const scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));

function baseCompose(i){const a=stageAuthor(),purple='#86527b',orange='#c6804f',pale='#e8dfd2';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};
 const person=(id,x,y,b=1)=>put(id,x,y,[a.dot(0,-30,25,purple),a.n('path',{d:'M-43 55 Q-49 0 0 0 Q49 0 43 55Z',fill:purple})],b,'Matched users; no protected demographic difference is implied');
 if(i===0||i===1){person('user-a',205,245);person('user-b',205,435);put('routes',570,330,[a.path('M-300 -90 H-170 L-45 -165 L105 -165 L270 -90 M-300 100 H270',purple,10)],2,'Equivalent users can receive unequal investigative paths');put('tool',585,170,[a.n('path',{d:'M-50 -32 H50 V32 H-50Z',fill:pale}),a.text('Search',0,12,30,'#402c46')],2,'Additional evidence gathering on one route');put('outputs',960,330,[a.n('path',{d:'M-70 -130 H70 V-50 H-70 M-70 62 H70 V142 H-70Z',fill:pale}),a.path('M-42 -92 H42 M-42 102 H42',purple,9)],3,'Similar final text does not establish equivalent resource allocation');put('labels',600,520,[a.text(i===0?'Follow the consequential pathway':'Similar answers, different resources',0,0,34)],4);if(i===1){put('attention',440,240,[a.dot(0,0,19,orange)],1,'Allocated computational attention');a.move('attention',3,675,165);}}
 if(i===2){put('target',350,295,[a.n('circle',{cx:0,cy:0,r:96,fill:'none',stroke:purple,'stroke-width':13}),a.n('circle',{cx:0,cy:0,r:46,fill:'none',stroke:purple,'stroke-width':10}),a.dot(0,0,14,orange),a.text('Intended outcome',0,170,34)],1);put('measure',800,295,[a.n('path',{d:'M-110 -85 H110 V85 H-110Z',fill:pale}),a.path('M-74 42 L-32 -36 L8 24 L76 -52',purple,12),a.text('Measured proxy',0,170,34)],2);put('pointer',600,300,[a.path('M80 0 H-80 L-52 -26 M-80 0 L-52 26',orange,12)],3,'A predictive proxy must be related to the intended decision, not assumed equivalent');a.move('pointer',4,600,335);}
 if(i===3){put('case',355,290,[a.n('path',{d:'M-95 -115 H95 V115 H-95Z',fill:pale}),a.text('Population',0,-60,32,'#402c46'),a.text('Harm',0,-10,36,'#402c46'),a.text('Context',0,43,34,'#402c46')],1);put('change',840,295,[a.path('M-100 -55 H65 L35 -80 M65 -55 L35 -30 M100 55 H-65 L-35 30 M-65 55 L-35 80',purple,12),a.text('Re-evaluate',0,170,34)],3,'A change to the system requires renewed fairness evidence');put('sample',840,280,[a.dot(0,0,23,orange)],4,'A newly observed consequence informs reassessment');}
 return a.finish('Matched users and a changing measurement context reveal mechanisms of bias; illustrative trajectories make no empirical claim about a demographic group or measured disparity.');}

function compose(i){if(i!==0)return baseCompose(i);const a=stageAuthor(),navy='#426f94',coral='#d67f60',green='#5ea58f',gold='#ddb052',cream='#e9e6d8';const put=(id,x,y,z,b=1,m=id)=>{a.add(a.object(id,x,y,z,m));a.reveal(id,b);};const figure=(id,x,y,c,identity='person-04-neutral',seated=false,scale=.95)=>{storyPerson(a,id,x,y,{coat:c,identity,seated,scale});a.reveal(id,1);};
for(const[id,y]of[['one',275],['two',510]]){figure(id,210,y,green,'person-02-neutral',true,.64);storyGesture(a,id,2,'question');put('terminal-'+id,390,y-120,[a.n('rect',{x:-90,y:-60,width:180,height:110,rx:10,fill:navy}),a.n('rect',{x:-72,y:-42,width:144,height:73,rx:5,fill:cream}),a.text('Request',0,-1,32,navy),a.path('M-130 73 H130 M-95 73 V135 M95 73 V135',navy,12)]);}
put('top-route',680,220,[a.path('M-180 0 H-75 V-90 H175 V0 H260',navy,12)],2,'One matched request receives additional investigation');put('lower-route',680,455,[a.path('M-180 0 H260',green,12)],2,'The second request goes directly to an answer');put('tool',775,130,[a.n('path',{d:'M-72 -34 H72 V34 H-72Z',fill:gold}),a.text('Search',0,11,32,navy)],3);put('reply',1000,340,[a.n('path',{d:'M-50 -135 H50 V-62 H-50 M-50 100 H50 V173 H-50Z',fill:cream}),a.path('M-28 -99 H28 M-28 136 H28',navy,9)],3);

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
