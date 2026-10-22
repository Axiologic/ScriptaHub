// Book-owned staging for Affective Calculus: an appraisal, not a word, explains the feeling.
// Scene 1 enacts the Chapter 1 subtext example, scene 2 exposes the AAC mechanism,
// scene 3 stages Appendix B.1 (Mara: fear or anger?) and ends on the actual Chapter 1 title.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),file=path.join(root,'work/scenes.json'),scenes=JSON.parse(fs.readFileSync(file,'utf8'));
// Visual-bible palette (cover navy ink, signal red, teal) plus quiet supporting materials.
const C={ink:'#1b2233',red:'#e0524a',teal:'#2a9d8f',paper:'#f6efe3',gold:'#e8b04b',slate:'#55657d',sand:'#d8c6a6',rain:'#93aabd',brick:'#b8735a',fur:'#7a5a44',night:'#c8d2e2',amber:'#a86d12',navyNight:'#5d7196'};
const AXES=['Goals','Control','Agency','Norms','Dignity','Attachment'];
function compose(i){
 const q=stageAuthor(),{n,path:p,text:t,dot}=q;
 const put=(id,x,y,nodes,beat=0,meaning=id,scale=1,offsetMs=250)=>{q.add(q.object(id,x,y,nodes,meaning,scale));if(beat)q.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs:700});return id;};
 const hide=(id,beat,offsetMs=150,durationMs=450)=>q.actions.push({actor:id,action:'disappear',beat,offsetMs,durationMs});
 const move=(id,beat,x,y,durationMs=1800,offsetMs=300)=>q.actions.push({actor:id,action:'moveTo',beat,x,y,durationMs,offsetMs});
 const express=(id,beat,emotion,offsetMs=200)=>q.actions.push({actor:id,action:'character.express',emotion,beat,offsetMs,durationMs:700});
 // Ink drawn directly on the stage brightens in Night; ink on paper stays dark.
 const line=(d,color=C.ink,w=6)=>color===C.ink?q.tint(p(d,color,w),C.night):p(d,color,w);
 const label=(s,x,y,size=28,color=C.ink)=>color===C.ink?q.tint(t(s,x,y,size,color),C.night):t(s,x,y,size,color);
 const shape=(d,fill)=>n('path',{d,fill});
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const person=(id,x,y,o)=>{storyPerson(q,id,x,y,{ink:C.ink,...o});
  // Shared rig lifts legs to pale grey on Dark; keep the clothing navy, only lighter for contrast.
  const keep=nd=>{const night=nd.themeAttrs?.night;if(night)for(const k of ['fill','stroke'])if(night[k]==='#9aafc3')night[k]=C.navyNight;for(const c of nd.children||[])keep(c);};
  keep(q.objects.find(o=>o.id===id).visual);return id;};
 const angerText=(s,x,y,size)=>q.tint(t(s,x,y,size,C.amber),C.gold);
 // Radial appraisal vector: six AAC dimensions, qualitative shape only (no invented scores).
 const radarNodes=(r,values,fill,{axisLabels=[],size=24,cx=0,cy=0,onPaper=false}={})=>{
  const pt=(k,v)=>{const a=(-90+k*60)*Math.PI/180;return [cx+Math.cos(a)*r*v,cy+Math.sin(a)*r*v];};
  const stroke=(d,w)=>onPaper?p(d,C.slate,w):line(d,C.slate,w);
  const shapeOf=values=>values.map((v,k)=>pt(k,v).map(z=>z.toFixed(1)).join(',')).join(' ');
  const ring=v=>AXES.map((_,k)=>pt(k,v).map(z=>z.toFixed(1)).join(',')).join(' ');
  return [
   (nd=>onPaper?nd:q.tint(nd,C.night))(n('polygon',{points:ring(1),fill:'none',stroke:C.slate,'stroke-width':2,'stroke-dasharray':'6 8'})),
   ...AXES.map((_,k)=>{const [x,y]=pt(k,1);return stroke(`M${cx} ${cy}L${x.toFixed(1)} ${y.toFixed(1)}`,3);}),
   n('polygon',{points:shapeOf(values),fill,opacity:.4}),n('polygon',{points:shapeOf(values),fill:'none',stroke:fill,'stroke-width':5,'stroke-linejoin':'round'}),
   ...values.map((v,k)=>{const [x,y]=pt(k,v);return dot(x,y,8,fill);}),
   ...axisLabels.map(k=>{const [x,y]=pt(k,k%3?1.45:1.3);return label(AXES[k],x,y+9,size);})
  ];
 };
 const FEAR=[.9,.2,.25,.35,.3,.3],ANGER=[.9,.8,.9,.75,.5,.3];
 if(i===0){
  // A character says she is fine inside a scene of despair; a word-matching judge reads only the word.
  put('floor',600,548,[rect(-470,0,940,12,C.sand,4)],0,'Room floor shared by the character and the judge');
  put('window',600,282,[rect(-112,-104,224,208,C.rain,10),rect(-112,-4,224,8,C.slate),rect(-4,-104,8,208,C.slate),
   ...[[-80,-80],[-40,-50],[30,-86],[70,-40],[-70,30],[-20,56],[50,30],[84,70]].map(([x,y])=>p(`M${x} ${y}L${x-9} ${y+24}`,'#e8eef3',3))],
   0,'Rain on the window: a scene of despair around the speaker, not her words');
  person('speaker',300,560,{identity:'person-08-neutral',coat:C.slate,seated:true,chair:C.sand,scale:.86});
  express('speaker',1,'sad');storyGesture(q,'speaker',1,'reflect',2200);
  put('bubble',372,196,[shape('M-142 -52Q-142 -74 -120 -74H120Q142 -74 142 -52V30Q142 52 120 52H-40L-78 88L-70 52H-120Q-142 52 -142 30Z',C.paper),
   t('“I’m perfectly',0,-16,30,C.ink),t('fine”',0,26,30,C.ink)],2,'The character’s spoken words, a social mask in a scene of despair');
  put('judge',960,372,[q.tint(rect(-92,-132,184,146,C.ink,16),'#4a5872'),rect(-74,-114,148,104,C.teal,10),p('M-50 -82H50M-50 -58H22',C.paper,7),
   q.tint(rect(-12,14,24,96,C.ink),C.night),q.tint(rect(-70,108,140,18,C.ink,8),C.night),label('AI judge',0,162,36)],0,'An AI judge that hunts for emotion words');
  put('lens',1080,212,[n('circle',{cx:0,cy:0,r:34,fill:'none',stroke:C.red,'stroke-width':9}),p('M24 24L54 54',C.red,12)],0,'The judge’s word-matching lens');
  move('lens',3,452,272,1700,200);
  put('word-hit',372,213,[n('rect',{x:-40,y:-24,width:80,height:40,rx:8,fill:'none',stroke:C.red,'stroke-width':4})],3,'The judge locks onto the word “fine”',1,1700);
  put('calm-tag',960,302,[rect(-60,-26,120,52,C.paper,26),t('Calm',0,10,28,C.red)],3,'Wrong verdict: the expression is mistaken for the state',1,2100);
  put('strike',960,302,[p('M-70 0H70',C.red,7)],4,'The word-based verdict is struck out',1,300);
  hide('lens',4,200);hide('word-hit',4,200);
  // Beat 4: an evaluated relationship links the agent with her world.
  put('appraisal',600,282,[n('path',{d:'M-260 120Q-190 30 -84 52',fill:'none',stroke:C.red,'stroke-width':6,'stroke-dasharray':'2 12','stroke-linecap':'round'}),dot(-84,52,9,C.red),dot(-260,120,9,C.red)],4,'Emotion as an evaluated relationship between an agent and her world',1,600);
  put('appraisal-label',600,436,[label('Agent ↔ world',0,0,28)],4,'The relationship, not the word, carries the emotion',1,900);
 }
 if(i===1){
  // Exposed mechanism, no characters: timescales, then the appraisal vector, then prototypes.
  const rows=[['Episode',90,C.red],['Mood',260,C.gold],['Sentiment',430,C.teal],['Attitude',560,C.slate]];
  rows.forEach(([name,w,color],k)=>{put('scale-'+k,600,196+k*86,[label(name,-250,10,30),rect(-150,-20,w,40,color,20)],1,'AAC separates a '+name.toLowerCase()+' by its timescale and structure',1,250+k*700);hide('scale-'+k,2,0,400);});
  put('time-arrow',600,548,[line('M-150 0H420',C.ink,4),line('M402 -12L420 0L402 12',C.ink,4),label('Seconds → years',140,-18,24)],1,'Brief episodes to lasting attitudes',1,300);hide('time-arrow',2,0,400);
  put('vector',600,330,radarNodes(150,[.85,.35,.7,.55,.6,.45],C.teal,{axisLabels:[0,1,2,3,4,5],size:25}),2,'Appraisal vector: goals, control, agency, norms, dignity and attachment',1,500);
  put('fear-proto',900,236,[n('ellipse',{cx:0,cy:0,rx:104,ry:70,fill:C.red,opacity:.32}),t('Fear',0,10,32,C.red)],3,'A contextual probabilistic prototype, not a rigid box',1,900);
  put('anger-proto',960,330,[n('ellipse',{cx:0,cy:0,rx:96,ry:64,fill:C.gold,opacity:.36}),angerText('Anger',0,10,30)],3,'A neighbouring prototype that overlaps',1,1300);
  q.connections.push({id:'to-prototypes',from:{node:'vector',anchor:'right'},to:{node:'fear-proto',anchor:'left'},width:4,color:C.teal,meaning:'The vector is compared with label prototypes'});
  move('vector',3,380,330,900,0);
  q.objects.find(o=>o.id==='vector').visual.anchors={left:[-180,0],right:[140,0],top:[0,-160],bottom:[0,160]};
  q.objects.find(o=>o.id==='fear-proto').visual.anchors={left:[-104,0],right:[104,0],top:[0,-70],bottom:[0,70]};
  q.actions.push({actor:'to-prototypes',action:'connection.draw',beat:3,offsetMs:1100,durationMs:1300});
  const meter=(id,x,y,name,fill,offsetMs)=>put(id,x,y,[label(name,-120,9,26),rect(-30,-14,200,28,C.sand,14),rect(-30,-14,fill,28,C.red,14)],3,name+' reported separately',1,offsetMs);
  meter('confidence',880,460,'Confidence',180,1800);meter('intensity',880,510,'Intensity',62,2300);
 }
 if(i===2){
  // Appendix B.1: one fact changes, and the dominant appraisal moves from fear toward anger.
  // The locked gate is Mara's blocked exit, set into the dead-end wall behind her; nothing stands between her and the dog.
  const bricks=(x0,x1,rows)=>rows.map(y=>p(`M${x0} ${y}H${x1}`,C.paper,3));
  put('ground',570,548,[rect(-520,0,1040,12,C.sand,4)],0,'The alley floor');
  put('doorway',200,548,[rect(-45,-214,90,214,'#e9dcc0')].map(nd=>q.tint(nd,'#33405a')),0,'Daylight beyond the gate: the only way out');
  put('dead-end',200,548,[rect(-150,-340,105,340,C.brick,4),rect(45,-340,105,340,C.brick,4),rect(-150,-340,300,126,C.brick,4),
   ...bricks(-150,150,[-296,-252]),...bricks(45,150,[-208,-164,-120,-76,-32]),...[-296,-252,-208,-164,-120,-76].map((y,k)=>p(`M${k%2?96:118} ${y}V${y+44}`,C.paper,3)),...[-296,-252].map((y,k)=>p(`M${k%2?-30:10} ${y}V${k?-214:y+44}`,C.paper,3))],0,'The alley ends at a wall; its gate is the exit');
  put('gate',200,548,[rect(-45,-214,8,214,C.ink),rect(37,-214,8,214,C.ink),...[-22,0,22].map(x=>rect(x-3,-208,6,206,C.slate)),rect(-45,-184,90,8,C.slate),rect(-45,-56,90,8,C.slate)].map(nd=>nd.attrs.fill===C.ink?q.tint(nd,C.night):nd),0,'The exit gate, shut and locked',1);
  put('padlock',236,430,[n('path',{d:'M-10 -6V-16Q-10 -28 0 -28Q10 -28 10 -16V-6',fill:'none',stroke:C.gold,'stroke-width':5}),rect(-15,-8,30,26,C.gold,4)],0,'The exit gate is locked');
  // Wall pocket drawn over the gate: in the variant the gate slides into it, leaving the exit open.
  put('pocket',200,548,[rect(-150,-214,105,214,C.brick,0),...bricks(-150,-45,[-208,-164,-120,-76,-32]),...[-208,-164,-120,-76].map((y,k)=>p(`M${k%2?-118:-90} ${y}V${y+44}`,C.paper,3))],0,'The wall pocket that receives the sliding gate');
  person('mara',400,560,{identity:'person-05-neutral',coat:C.teal,scale:.84});
  express('mara',1,'worried');storyGesture(q,'mara',1,'recoil',2000);
  put('dog',1040,500,[n('ellipse',{cx:0,cy:-26,rx:66,ry:28,fill:C.fur}),n('ellipse',{cx:-70,cy:-52,rx:28,ry:22,fill:C.fur}),shape('M-96 -50L-122 -40L-96 -34Z',C.fur),
   shape('M-62 -72L-50 -96L-46 -66Z','#5a4031'),p('M-44 -14L-74 14M-26 -10L-14 22M30 -10L56 18M48 -18L86 4',C.fur,11),p('M62 -36Q92 -58 98 -76',C.fur,9),dot(-78,-58,4,C.ink)],0,'A dog running toward Mara',1);
  for(const nd of q.objects.find(o=>o.id==='dog').visual.children)if(nd.attrs.fill===C.fur||nd.attrs.stroke===C.fur)Object.assign(nd,q.tint(nd,'#a8846a'));
  move('dog',1,770,500,2600,300);
  put('fear-vector',850,206,radarNodes(70,FEAR,C.red),0,'Fear: high threat, low control, no one to blame');
  put('fear-word',850,318,[t('Fear',0,0,30,C.red)],0,'Dominant hypothesis: fear');
  // Beat 2: she can shut the gate, and the owner released the dog deliberately.
  hide('padlock',2,0,300);move('gate',2,122,548,1500,300);
  put('remote',354,452,[q.tint(rect(-11,-18,22,36,C.ink,5),'#2b3550'),dot(0,-6,5,C.red)],2,'Mara holds the device that can shut the gate instantly',1,200);
  put('signal',318,440,[...[14,28].map(r=>n('path',{d:`M${-r*.6} ${-r}Q${-r*1.3} 0 ${-r*.6} ${r}`,fill:'none',stroke:C.teal,'stroke-width':4,'stroke-linecap':'round'}))],2,'Her device reaches the gate',1,1500);
  put('shut-cue',200,452,[n('path',{d:'M-14 0H26',fill:'none',stroke:C.teal,'stroke-width':5,'stroke-dasharray':'10 8','stroke-linecap':'round'}),p('M18 -12L34 0L18 12',C.teal,5)],2,'The open gate can slide shut at her command',1,1800);
  person('owner',1075,560,{identity:'person-16-neutral',coat:C.brick,scale:.74});express('owner',2,'determined',1300);
  q.actions.push({actor:'owner',action:'appear',beat:2,offsetMs:1300,durationMs:700});storyGesture(q,'owner',2,'release',1900);
  put('leash',1036,488,[p('M0 0Q-10 50 -60 56',C.red,5),n('circle',{cx:-76,cy:54,r:13,fill:'none',stroke:C.red,'stroke-width':5})],2,'An empty leash and open collar: the owner freed the dog deliberately',1,2300);
  express('mara',2,'angry',1600);
  hide('fear-vector',2,2200,500);hide('fear-word',2,2200,500);
  put('anger-vector',850,206,radarNodes(70,ANGER,C.gold),2,'Control and agency rise; anger should rise relative to fear',1,2500);
  put('anger-word',850,318,[angerText('Anger',0,0,30)],2,'The dominant point moves toward anger',1,2500);
  // Beat 3: the minimal pair, side by side, isolates the one changed fact.
  for(const id of ['ground','doorway','dead-end','gate','pocket','mara','dog','remote','signal','shut-cue','owner','leash','anger-vector','anger-word'])hide(id,3,0,450);
  put('pair-fear',330,300,radarNodes(120,FEAR,C.red,{axisLabels:[1,2],size:26}),3,'Minimal pair, first case: fear',1,500);
  put('pair-fear-word',330,486,[t('Fear',0,0,32,C.red)],3,'Fear case label',1,500);
  put('pair-anger',870,300,radarNodes(120,ANGER,C.gold,{axisLabels:[1,2],size:26}),3,'Minimal pair, second case: anger',1,1100);
  put('pair-anger-word',870,486,[angerText('Anger',0,0,32)],3,'Anger case label',1,1100);
  put('one-fact',600,300,[line('M-80 0H70',C.ink,5),line('M52 -16L72 0L52 16',C.ink,5),label('One fact',-5,-24,26)],3,'Only one relevant fact differs between the two cases',1,1700);
  // Beat 4: the reading invitation, opened at the real first chapter.
  for(const id of ['pair-fear','pair-fear-word','pair-anger','pair-anger-word','one-fact'])hide(id,4,0,450);
  put('open-book',600,350,[n('path',{d:'M-330 -150Q-160 -184 0 -136Q160 -184 330 -150V160Q160 128 0 172Q-160 128 -330 160Z',fill:C.teal}),
   n('path',{d:'M-312 -136Q-152 -164 0 -120Q152 -164 312 -136V140Q152 112 0 154Q-152 112 -312 140Z',fill:C.paper}),p('M0 -120V154',C.sand,4),
   t('Chapter 1',-156,-62,26,C.teal),t('An Emotion',-156,-14,36,C.ink),t('Is Not a Word',-156,30,36,C.ink),p('M-236 70H-76M-236 96H-96',C.sand,5),
   t('Affective',156,-40,34,C.ink),t('Calculus',156,4,34,C.ink),...radarNodes(46,ANGER,C.gold,{cx:156,cy:88,onPaper:true}),
   shape('M-56 -130H-26V-60L-41 -73L-56 -60Z',C.red)],4,'Affective Calculus opened at Chapter 1, An Emotion Is Not a Word',1,500);
 }
 return q.finish([
  'A seated character in a rain-lit room says “I’m perfectly fine”; an AI judge’s lens locks onto the word and labels her calm, then the verdict is struck out and an appraisal links agent and world.',
  'An exposed AAC mechanism: four timescale bars, then a six-axis appraisal vector compared with overlapping prototypes, with confidence and intensity shown as separate meters.',
  'Appendix B.1 staged: Mara backs against a dead-end wall whose exit gate is locked while a dog runs at her, giving fear; the gate slides open, her device can shut it, and a deliberate owner shifts the radial vector toward anger; the minimal pair is isolated, then Chapter 1 opens.'
 ][i]);
}
for(let i=0;i<scenes.length;i++)scenes[i].visual=compose(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
