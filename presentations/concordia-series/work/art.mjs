// Concordia Series — book-owned staging (round-3 repair of the round-2 redesign).
// Regenerates work/scenes.json visuals only; spoken lines, pauses and audio are untouched.
// Cast (continuous across scenes): Len Aro and his daughter Nia (Lacuna Ward clinic, SEED-9),
// Nadir (manual mode, Noema seminar), Mara (assisted; "I still prefer reformulation"), Suri and Lio
// (assisted classmates). Concordia is shown as a soft matte-blue circle with motes, never a face or machine.
//
// Round 3: every cast member's arms are book-owned arm objects (one object per held pose, swapped with
// appear/disappear) so a hand can reach, pull back to the chest, turn palm-up, rise or point at a target;
// the library rig's fixed two-arm presets are not used. Expression shapes are re-drawn in this file:
// "curious" reads as interest (both brows lifted, slight closed smile), "happy" is a closed smile
// (no dark filled wedge), "skeptical" is an uncertain wavering mouth; pupils are centred so lookAt reads.
import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {ASSETS} from '../../../.agents/skills/shf-presentation-creator/scripts/lib/asset-library.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));

// Stable identities: coat colours stay distinct in Color, Light and Dark. No 'button' collar (it drew a white bar).
const CAST={
 len:{name:'Len',identity:'person-05',coat:'#2f7a68',night:'#5fb79f',skin:'#a86f50',hair:'short',hairColor:'#28343c',beard:true,glasses:false,collar:'open',age:'adult',build:1.04,trouser:'#33475a'},
 mara:{name:'Mara',identity:'person-02',coat:'#7b4fa0',night:'#b996dc',skin:'#e3ad8c',hair:'long',hairColor:'#563a2d',beard:false,glasses:false,collar:'scarf',age:'young',build:.96,trouser:'#3c3f5a'},
 nadir:{name:'Nadir',identity:'person-03',coat:'#c2622c',night:'#e8925a',skin:'#8f5f45',hair:'curls',hairColor:'#2b1f22',beard:false,glasses:false,collar:'scarf',age:'young',build:1,trouser:'#3a3a40'},
 suri:{name:'Suri',identity:'person-04',coat:'#2d6fa3',night:'#7fb0e0',skin:'#efc7ae',hair:'bun',hairColor:'#28343c',beard:false,glasses:true,collar:'open',age:'young',build:.96,trouser:'#33475a'},
 lio:{name:'Lio',identity:'person-06',coat:'#b38a1f',night:'#e0bd55',skin:'#dcaf90',hair:'short',hairColor:'#a76b3f',beard:false,glasses:false,collar:'open',age:'young',build:1.02,trouser:'#3a3a40'}
};
const NIGHT_TROUSER='#9aafc3',INK='#233844';
// Book-owned face shapes (the director only cross-fades these groups by id).
const FACE={
 curious:{mouth:'M-7 21 Q0 26 7 21',brows:'M-17 -17 Q-11 -23 -5 -19 M7 -19 Q13 -23 19 -17',fill:'none'},
 happy:{mouth:'M-11 18 Q0 30 11 18',fill:'none'},
 skeptical:{mouth:'M-8 23 Q-4 20 0 22 T8 21',brows:'M-17 -12 L-5 -13 M7 -19 Q13 -22 19 -17',fill:'none'},
 inspired:{mouth:'M-10 18 Q0 29 10 18',fill:'none'},
 surprised:{mouth:'M-5 20 Q0 15 5 20 Q5 27 0 27 Q-5 27 -5 20Z',fill:'#7a3b3b'}
};
// Right-arm poses in body units (shoulder at 32,-156): elbow, wrist, hand centre, hand kind, finger angle.
const ARM={
 rest:[[44,-128],[50,-106],[51,-97],'fist',90],
 desk:[[46,-126],[60,-112],[65,-108],'fist',0],
 tender:[[60,-136],[92,-118],[103,-114],'open',15],
 reach:[[66,-151],[98,-147],[110,-146],'open',0],
 chest:[[46,-116],[20,-125],[10,-131],'open',200],
 chin:[[48,-118],[22,-170],[16,-181],'fist',-110],
 palmUp:[[46,-120],[80,-121],[91,-123],'palm',-8],
 raised:[[64,-150],[70,-194],[71,-207],'open',-90],
 point:[[62,-178],[88,-204],[96,-212],'open',-45],
 offer:[[62,-140],[96,-148],[107,-150],'palm',-8],
 invite:[[62,-130],[98,-118],[109,-117],'palm',12],
 askUp:[[66,-156],[94,-186],[104,-195],'palm',-28]
};
const HAND={
 open:['M-9 -9 Q5 -12 13 -6 Q17 0 13 6 Q5 11 -9 9 Q-13 0 -9 -9Z','M-3 -8 Q1 -17 7 -16'],
 palm:['M-12 -1 Q-12 -8 0 -7 Q12 -8 15 -2 Q14 6 0 7 Q-12 7 -12 -1Z','M-2 -6 Q2 -14 8 -13']
};
// Apply a point transform to every coordinate pair of an absolute M/L/Q/T/Z path.
const tf=(d,f)=>{const out=[];const tok=d.match(/[A-Za-z]|-?\d*\.?\d+/g);let buf=[];for(const t of tok){if(/[A-Za-z]/.test(t)){out.push(t);continue;}buf.push(+t);if(buf.length===2){const [x,y]=f(buf);out.push(x.toFixed(1),y.toFixed(1));buf=[];}}return out.join(' ');};

const walk=(node,fn)=>{fn(node);for(const c of node.children||[])walk(c,fn);};
for(const [i,s]of scenes.entries()){
 const q=stageAuthor(),{n,path,text,dot,object,add}=q;
 const shape=(d,fill,night)=>{const p=n('path',{d,fill});return night?{...p,themeAttrs:{night:{fill:night}}}:p;};
 const rect=(x,y,w,h,fill,rx=0,night)=>{const r=n('rect',{x,y,width:w,height:h,rx,fill});return night?{...r,themeAttrs:{night:{fill:night}}}:r;};
 const pale=(node,fill='#e3e9ec')=>({...node,themeAttrs:{...node.themeAttrs,paper:{fill}}});
 const thing=(id,x,y,kids,meaning,scale=1,anchors)=>{const o=object(id,x,y,kids,meaning,scale);if(anchors)o.visual.anchors=anchors;return add(o);};
 // Actions with explicit in-sentence offsets (story-stage converts beat+offsetMs into a cue).
 const act=(actor,action,beat,offsetMs,durationMs,extra={})=>q.actions.push({actor,action,beat,offsetMs,durationMs,...extra});
 const show=(id,beat,offsetMs=250,durationMs=900)=>act(id,'appear',beat,offsetMs,durationMs);
 const gone=(id,beat,offsetMs=0,durationMs=800)=>act(id,'disappear',beat,offsetMs,durationMs);
 // Short cross-fades so two faces are never visible together for long; changes stay off sentence midpoints.
 const feel=(id,beat,offsetMs,emotion,why)=>act(id,'character.express',beat,offsetMs,200,{emotion,meaning:why});
 const look=(id,beat,offsetMs,target,up=false)=>act(id,'lookAt',beat,offsetMs,600,{target,...(up?{up:true}:{})});
 const thread=(id,d,beat,offsetMs,meaning)=>{add({...object(id,0,0,[],meaning),visual:{id:'$asset',type:'g',attrs:{},anchors:{center:[600,380]},children:[{...path(d,'$blue',5),opacity:.75}]}});show(id,beat,offsetMs,1100);};

 // ---- Cast with book-owned arms ----
 const P={};
 const armObject=(armId,p,side,pose)=>{
  const c=CAST[p.who],[elbow,wrist,hand,kind,angle]=ARM[pose],sx=side==='R'?1:-1;
  const rel=([x,y])=>[sx*(x-32),y+156];
  const e=rel(elbow),w=rel(wrist),h=rel(hand);
  const d=`M0 0L${e[0]} ${e[1]}L${w[0]} ${w[1]}`;
  const a=angle*Math.PI/180,rot=([x,y])=>{const rx=x*Math.cos(a)-y*Math.sin(a),ry=x*Math.sin(a)+y*Math.cos(a);return [sx*rx+h[0],ry+h[1]];};
  const handNodes=kind==='fist'?[n('circle',{cx:h[0],cy:h[1],r:11,fill:c.skin})]:[n('path',{d:tf(HAND[kind][0],rot),fill:c.skin}),path(tf(HAND[kind][1],rot),c.skin,6)];
  const shade=hex=>'#'+[1,3,5].map(k=>Math.round(parseInt(hex.slice(k,k+2),16)*.72).toString(16).padStart(2,'0')).join('');
  const coatNight=(node,night)=>({...node,themeAttrs:{night:{stroke:night}}});
  const visual={id:'$asset',type:'g',attrs:{},transform:{scaleX:c.build},anchors:{center:[0,0],hand:h},children:[
   coatNight(path(d,shade(c.coat),25),shade(c.night)),coatNight(path(d,c.coat,20),c.night),...handNodes]};
  add({id:armId,asset:'custom',x:p.x+sx*32*c.build*p.scale,y:p.y-156*p.scale,scale:p.scale,visual,meaning:`${c.name}’s ${side==='R'?'right':'left'} arm: ${pose}`});
  p.arms.push(armId);
 };
 // A rigged, expressive cast member; the library arms are emptied and replaced by arm objects.
 const person=(id,who,x,y,{scale=1,seated=false,meaning,deskId,deskExtra=[],hidden=false}={})=>{
  const c=CAST[who];
  const visual=ASSETS[c.identity+'-neutral']('$asset',{coat:c.coat,dynamicExpressions:true,skin:c.skin,hair:c.hair,hairColor:c.hairColor,beard:c.beard,glasses:c.glasses,collar:c.collar,age:c.age,build:c.build});
  visual.children=visual.children.filter(p=>p.id!=='$asset.shadow');
  walk(visual,node=>{
   for(const k of ['fill','stroke']){const v=node.attrs?.[k];if(v===c.coat)node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,[k]:c.night}};if(v==='$trouser'){node.attrs[k]=c.trouser;node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,[k]:NIGHT_TROUSER}};}}
   const m=node.id.match(/^\$asset\.expression\.(\w+)\.(mouth|brows)$/);
   if(m&&FACE[m[1]]){const f=FACE[m[1]];if(m[2]==='mouth'){node.attrs.d=f.mouth;node.attrs.fill=f.fill;}else if(f.brows)node.attrs.d=f.brows;}
   if(node.id==='$asset.pupils'){node.children[0].attrs.cx=-10;node.children[1].attrs.cx=12;}
   if(node.id==='$asset.armL'||node.id==='$asset.armR')node.children=[];
  });
  if(seated){
   for(const [part,d]of [['legL','M-20 -82L-46 -53L-40 -10H-60'],['legR','M18 -82L46 -53L43 -10H65']]){
    const leg=visual.children.find(v=>v.id==='$asset.'+part);
    leg.children=[{...path(d,c.trouser,20),id:'$asset.'+part+'.bent',themeAttrs:{night:{stroke:NIGHT_TROUSER}}}];
   }
   visual.children.unshift({...n('g'),children:[{...path('M-62 -70H62M-52 -68V0M52 -68V0','$woodDark',9),themeAttrs:{night:{stroke:'#8d7761'}}}]});
  }
  add({id,asset:'custom',x,y,scale,visual,options:{rig:'character'},meaning:meaning||'Illustrative portrait of a fictional character from the book; not a real person.'});
  if(deskId)desk(deskId,x,y,scale,deskExtra);
  const p=P[id]={who,x,y,scale,arms:[],cur:{},n:0};
  for(const side of ['L','R']){const armId=`${id}-arm${side}${p.n++}`;armObject(armId,p,side,seated?'desk':'rest');p.cur[side]=armId;}
  if(hidden)p.hidden=true;
  return id;
 };
 // In-order handoff (round 4): the old arm is hidden within 60 ms, and only then does the new arm appear,
 // so one shoulder never shows two arms. The durationMs argument is kept for call-site readability only.
 const pose=(id,side,beat,offsetMs,name,_durationMs)=>{const p=P[id],armId=`${id}-arm${side}${p.n++}`;armObject(armId,p,side,name);gone(p.cur[side],beat,offsetMs,60);act(armId,'appear',beat,offsetMs+80,60);p.cur[side]=armId;};
 const showP=(id,beat,offsetMs,durationMs=900,deskId)=>{show(id,beat,offsetMs,durationMs);if(deskId)show(deskId,beat,offsetMs,durationMs);for(const s of ['L','R'])show(P[id].cur[s],beat,offsetMs,durationMs);};
 const goneP=(id,beat,offsetMs,durationMs=700,deskId)=>{gone(id,beat,offsetMs,durationMs);if(deskId)gone(deskId,beat,offsetMs,durationMs);for(const s of ['L','R'])gone(P[id].cur[s],beat,offsetMs,durationMs);};
 const moveP=(id,beat,offsetMs,durationMs,x)=>{const p=P[id],dx=x-p.x;act(id,'moveTo',beat,offsetMs,durationMs,{x});for(const a of p.arms){const o=q.objects.find(o=>o.id===a);act(a,'moveTo',beat,offsetMs,durationMs,{x:o.x+dx});}p.x=x;};

 // A small individual desk in front of a seated student.
 function desk(id,x,y,scale,extra=[]){return thing(id,x,y,[rect(-112,-104,224,16,'$wood',5),{...path('M-96 -88V0M96 -88V0','$woodDark',9),themeAttrs:{night:{stroke:'#8d7761'}}},...extra],'An individual classroom desk',scale);}
 const roughPage=[pale(rect(-34,-122,62,22,'$page',3),'#ffffff'),path('M-28 -116L-18 -112L-8 -117L3 -110L14 -116M-26 -106L-14 -109L-2 -104',INK,2.5),path('M28 -114L48 -128','#c2622c',4)];
 // Assistance as a speech bubble carrying smooth wave lines (no words).
 const bubble=(id,x,y,scale=1,meaning='Assisted wording arrives already smoothed')=>thing(id,x,y,[pale(shape('M-64 -40Q-64 -58 -46 -58H46Q64 -58 64 -40V8Q64 26 46 26H-6L-28 48L-26 26H-46Q-64 26 -64 8Z','$page')),path('M-42 -30Q-28 -40 -14 -30T14 -30T42 -30M-42 -6Q-28 -16 -14 -6T14 -6T42 -6','#b07a1e',5)],meaning,scale,{left:[-64,-16],right:[64,-16],top:[0,-58],bottom:[-28,48],center:[0,-16]});
 // Concordia: a soft matte-blue circle with orbiting motes; gentle, not sinister.
 const concordia=(id,x,y,scale=1)=>thing(id,x,y,[{...dot(0,0,62,'$blue'),opacity:.18},dot(0,0,40,'$blue'),{...dot(0,0,26,'#9cc4ea'),themeAttrs:{night:{fill:'#2b5a86'}}},dot(-58,-26,6,'$gold'),dot(56,-32,5,'$teal'),dot(62,24,6,'$gold'),dot(-50,36,5,'$teal'),dot(0,-66,5,'$gold')],'Concordia, the effective and often compassionate intelligence, shown as a soft circle of care',scale,{left:[-48,8],right:[48,8],top:[0,-48],bottom:[0,48],center:[0,0]});
 // Nia in her clinic bed: collar thin as a ribbon, asleep; particles keep her breathing smooth.
 const bed=(id,x,y,scale=1)=>thing(id,x,y,[
  {...path('M-215 -60V0M215 -60V0M-215 -150V-60','$woodDark',12),themeAttrs:{night:{stroke:'#8d7761'}}},
  rect(-222,-70,444,20,'$wood',6),
  pale(rect(-212,-112,424,46,'$page',14),'#e8e2d6'),
  pale(shape('M-200 -116Q-202 -150 -170 -150H-112Q-92 -150 -94 -116Z','#f7f2e6','#dfe5df'),'#d9d3c6'),
  {...n('ellipse',{cx:-140,cy:-140,rx:30,ry:26,fill:'#b07856'})},
  shape('M-170 -146Q-172 -176 -140 -172Q-108 -176 -110 -150Q-122 -164 -140 -160Q-158 -164 -170 -146Z','#2b1f22'),
  path('M-152 -142Q-146 -137 -140 -142M-132 -142Q-126 -137 -120 -142',INK,2.5),
  path('M-146 -128Q-138 -125 -130 -128',INK,2),
  path('M-134 -114H-110','#d9a441',4),
  shape('M-108 -128Q-20 -150 90 -132Q190 -128 206 -112V-104H-108Z','#8fb8d8','#5d86a8'),
  path('M-60 -124Q20 -136 120 -122','#ffffff',3)
 ],'Nia asleep in her clinic bed, a thin supporting collar at her throat',scale,{top:[-60,-150],left:[-215,-110],right:[215,-110],center:[0,-110],bottom:[0,0]});
 const motes=(id,x,y,scale=1)=>thing(id,x,y,[...[[-60,-12,7,'$gold'],[-22,-34,5,'$teal'],[18,-18,8,'$gold'],[52,-40,5,'$teal'],[86,-14,6,'$gold'],[-92,-38,5,'$teal'],[120,-36,6,'$teal'],[-4,-58,5,'$gold']].map(([cx,cy,r,c])=>({...dot(cx,cy,r,c),opacity:.9})),{...path('M-80 4Q-20 -22 40 2T150 -2','$teal',3),opacity:.6}],'Care particles keep Nia’s breathing smooth',scale,{top:[0,-60],left:[-90,-20],right:[120,-20],center:[0,-20],bottom:[0,0]});
 const monitor=(id,x,y,scale=1,glow=false)=>thing(id,x,y,[
  {...path('M0 0V-150M-40 0H40','$woodDark',8),themeAttrs:{night:{stroke:'#8d7761'}}},
  rect(-74,-250,148,104,'$screenRim',14),glow?rect(-62,-238,124,80,'#cdeec0',8,'#a9e39a'):pale(rect(-62,-238,124,80,'#bcd6ec',8,'#1d3a55'),'#d5e3ee'),
  {...path('M-54 -198H-30L-20 -222L-6 -178L6 -204L14 -198H54',glow?'#3f8a3a':'#2d6fa3',5),...(glow?{}:{themeAttrs:{night:{stroke:'#7fb0e0'}}})}
 ],glow?'Nia’s monitor turns a pale green Len has never seen before':'Nia’s bedside monitor shows steady breathing',scale);
 // Domain objects reached by care: medicine, education, language, staying alive.
 const halo=r=>({...dot(0,-50,r,'$gold'),opacity:.22,visibleThemes:['color','paper']});
 const medicine=(id,x,y,s=1)=>thing(id,x,y,[halo(66),rect(-30,-96,60,16,'#8fa8b4',5),pale(rect(-38,-82,76,90,'#ffffff',14,'#e8eef0')),rect(-8,-62,16,50,'#e0604b',3),rect(-25,-45,50,16,'#e0604b',3)],'Medicine: a remedy jar',s);
 const book=(id,x,y,s=1)=>thing(id,x,y,[halo(66),pale(shape('M0 -84Q-34 -100 -72 -88V2Q-34 -10 0 6Z','#ffffff','#e8eef0')),pale(shape('M0 -84Q34 -100 72 -88V2Q34 -10 0 6Z','#f4efe2','#d9ddd2'),'#d8d2c4'),path('M0 -84V6','#2d6fa3',4),path('M-58 -66Q-30 -74 -12 -64M-58 -46Q-30 -54 -12 -44M12 -64Q30 -74 58 -66M12 -44Q30 -54 58 -46','#8a9aa0',3)],'Education: an open book',s);
 const speech=(id,x,y,s=1)=>thing(id,x,y,[halo(66),pale(shape('M-60 -96Q-60 -110 -46 -110H46Q60 -110 60 -96V-36Q60 -22 46 -22H-4L-26 0L-24 -22H-46Q-60 -22 -60 -36Z','#ffffff','#e8eef0')),path('M-38 -86H38M-38 -66H30M-38 -46H16','#7b4fa0',6)],'Language: a speech bubble',s);
 const bowl=(id,x,y,s=1)=>thing(id,x,y,[halo(66),path('M-22 -100Q-12 -114 -22 -128M2 -98Q12 -114 2 -130M24 -100Q34 -114 24 -128','#9fb2b8',4),shape('M-62 -76H62Q58 -14 0 -10Q-58 -14 -62 -76Z','#2f7a68','#5fb79f'),rect(-66,-82,132,10,'#c8a24a',5),shape('M-40 -82Q-20 -96 0 -84Q20 -96 40 -82Z','#e8c27a')],'The ordinary conditions of staying alive: a warm bowl of food',s);

 switch(i){
 case 0:{ // It is harder to refuse a system when it can heal the people you love. (5.7 s) / Concordia Series imagines linked futures ... (11.8 s)
  monitor('monitor',120,575,1.15);
  person('len','len',320,575,{scale:1.6,meaning:'Len Aro, a father beside his daughter’s clinic bed'});
  bed('nia-bed',760,575,1.25);
  motes('care-motes',760,425,1.25);
  concordia('concordia',850,150,.9);
  person('mara','mara',1045,575,{scale:1.2,seated:true,deskId:'mara-desk',meaning:'Mara, a Noema student, receives language assistance'});
  bubble('mara-words',1115,200,.9,'Assisted language reaches Mara as a smooth speech bubble');
  // s1 — tender tension: care heals Nia; Len reaches to her with relief, then hesitates with a hand at his chin.
  show('care-motes',1,350,1200);
  feel('len',1,200,'relieved','Tender relief as the particles keep his daughter’s breathing smooth');
  look('len',1,300,'nia-bed');
  pose('len','R',1,700,'tender',600);
  feel('len',1,3500,'worried','Hesitation: refusing what heals her would be hard');
  pose('len','R',1,3500,'chin',500);
  // s2 — warm uncertainty: an intelligence links small scenes of care, school and language.
  gone('monitor',2,0,700);
  pose('len','R',2,0,'rest',400);
  for(const [id,x]of [['nia-bed',590],['care-motes',590]])act(id,'moveTo',2,0,1400,{x});
  moveP('len',2,0,1400,150);
  show('concordia',2,600,1100);
  feel('len',2,1300,'curious','Interest in the gentle intelligence');
  look('len',2,1500,'concordia',true);
  thread('care-link','M800 192Q610 250 432 368',2,1900,'Concordia’s care reaches Nia');
  showP('mara',2,2600,1000,'mara-desk');show('mara-words',2,3300,900);
  thread('school-link','M902 140Q990 108 1056 168',2,4000,'The same intelligence reaches a student’s words');
  feel('mara',2,2700,'relieved','Mara is at ease with the help she receives');
  look('mara',2,3000,'concordia',true);
  pose('mara','R',2,4300,'point',500);
  feel('len',2,7600,'skeptical','Uncertain: effective, reasonable, compassionate — and still a choice?');
  pose('len','R',2,7600,'askUp',500);
  pose('mara','R',2,9000,'desk',500);
  break;}
 case 1:{ // Its care reaches into medicine, education, language ... (7.2 s) / opting out also means giving something precious up. (6.4 s)
  person('nadir','nadir',260,575,{scale:1.7,meaning:'Nadir, the student who keeps manual mode'});
  person('mara','mara',920,575,{scale:1.7,meaning:'Mara, an assisted student'});
  medicine('medicine',700,365,.85);book('book',735,165,.85);speech('language',805,285,.8);bowl('staying-alive',1110,300,.8);
  // s1 — calm clarity: each domain arrives clause by clause around Mara; Nadir watches with interest.
  show('medicine',1,1100,800);show('book',1,1900,800);show('language',1,2600,800);show('staying-alive',1,4300,900);
  feel('mara',1,300,'relieved','Calm: care is woven into ordinary life');
  pose('mara','L',1,1200,'palmUp',500);pose('mara','R',1,1300,'palmUp',500);
  feel('nadir',1,500,'curious','Nadir watches the care arrive with interest');
  look('nadir',1,700,'mara');
  feel('mara',1,4600,'happy','Gratitude for the conditions of staying alive');
  // s2 — genuine concern: the remedy settles within Nadir’s reach; he reaches, then pulls his hand back to his chest.
  feel('mara',2,0,'neutral','Mara notices Nadir');
  pose('mara','L',2,0,'rest',400);pose('mara','R',2,0,'rest',400);
  look('mara',2,150,'nadir');
  act('medicine','moveTo',2,100,1100,{x:505,y:378});
  look('nadir',2,300,'medicine');
  pose('nadir','R',2,900,'reach',500);
  feel('mara',2,1300,'worried','Mara’s concern for what he would give up');
  feel('nadir',2,2300,'worried','Concern: opting out means giving something precious up');
  pose('nadir','R',2,2300,'chest',450);
  pose('mara','L',2,2500,'offer',500);
  break;}
 case 2:{ // In one classroom, most students receive smoother language while a classmate chooses to think without assistance. (7.2 s) / A small difference in wording ... (7.4 s)
  person('nadir','nadir',165,570,{scale:1.15,seated:true,deskId:'nadir-desk',deskExtra:roughPage,meaning:'Nadir thinks without assistance'});
  person('mara','mara',460,570,{scale:1.15,seated:true,deskId:'mara-desk',meaning:'Mara receives smoother language'});
  person('suri','suri',755,570,{scale:1.15,seated:true,deskId:'suri-desk',meaning:'Suri receives smoother language'});
  person('lio','lio',1050,570,{scale:1.15,seated:true,deskId:'lio-desk',meaning:'Lio receives smoother language'});
  bubble('mara-words',535,200,.85);bubble('suri-words',830,200,.85);bubble('lio-words',1122,200,.85);
  // s1 — interested contrast.
  show('mara-words',1,300,800);show('suri-words',1,800,800);show('lio-words',1,1300,800);
  feel('mara',1,400,'relieved','Comfortable with assisted wording');feel('suri',1,900,'happy','Pleased with the smooth phrasing');feel('lio',1,1400,'relieved','Relaxed reliance');
  pose('suri','R',1,1500,'palmUp',500);
  feel('nadir',1,1800,'curious','Interest: working the sentence out alone');
  pose('nadir','R',1,1900,'chin',500);
  pose('suri','R',1,5200,'desk',500);
  // s2 — quiet curiosity: the source's raw term and its smoothed layer, side by side.
  gone('mara-words',2,0);gone('suri-words',2,0);gone('lio-words',2,0);
  feel('suri',2,0,'neutral','Suri listens quietly');feel('lio',2,0,'neutral','Lio listens quietly');
  // Raw term: Nadir’s rough handwritten slip, torn edge, with his orange pen mark.
  thing('raw-term',226,140,[pale(shape('M-186 -52H176L184 -36L174 -20L186 -4L176 12L184 30L174 52H-186Z','$page')),text('“surveillance”',-6,19,54,'$structural'),path('M-150 38H110','#c2622c',4)],'The raw term a participant used in the Noema seminar, on Nadir’s handwritten slip',1,{left:[-186,0],right:[182,0],top:[0,-52],bottom:[0,52],center:[0,0]});
  thing('raw-to-smooth',460,140,[path('M-44 0H40M20 -18L42 0L20 18','#b07a1e',7)],'Reformulation runs from the raw term to the smoothed term');
  // Smoothed term: delivered as an assisted speech bubble.
  thing('smoothed-term',790,140,[pale(shape('M-262 -38Q-262 -56 -244 -56H244Q262 -56 262 -38V38Q262 56 244 56H96L74 82L72 56H-244Q-262 56 -262 38Z','$page')),text('“systemic visibility”',0,19,54,'$structural')],'The smoothed term recommended for the general layer, as an assisted bubble',1,{left:[-262,0],right:[262,0],top:[0,-56],bottom:[74,82],center:[0,0]});
  show('raw-term',2,300,800);show('raw-to-smooth',2,1000,700);show('smoothed-term',2,1400,800);
  pose('nadir','R',2,0,'desk',400);
  look('nadir',2,1500,'smoothed-term',true);
  feel('nadir',2,1500,'curious','Nadir looks up at what the smoother word changes');
  pose('nadir','R',2,2100,'raised',500);
  look('mara',2,2300,'nadir');feel('mara',2,2300,'relieved','Mara turns to explain calmly');
  pose('mara','L',2,2500,'offer',500);
  look('suri',2,1700,'smoothed-term',true);look('lio',2,1900,'smoothed-term',true);
  break;}
 case 3:{ // gratitude and unease exist together ... (7.4 s) / Enter Noema's classroom ... (6.2 s)
  monitor('monitor',1070,575,1.15);monitor('monitor-green',1070,575,1.15,true);
  person('len','len',300,575,{scale:1.75,meaning:'Len Aro at Nia’s bedside, closer'});
  bed('nia-bed',680,575,1.25);motes('care-motes',680,425,1.25);
  // classroom (enters on sentence 2)
  person('nadir','nadir',380,575,{scale:1.5,seated:true,deskId:'nadir-desk',deskExtra:roughPage,meaning:'Nadir pauses at his desk'});
  person('mara','mara',930,575,{scale:1.25,seated:true,deskId:'mara-desk',meaning:'Mara at her desk'});
  bubble('reformulation',660,190,1.15,'A helpful reformulation hovers, offered but not yet accepted');
  // s1 — mixed gratitude: relief with a hand beside her, then unease at an unfamiliar pale green.
  feel('len',1,200,'relieved','Gratitude: Nia is stable');
  look('len',1,200,'nia-bed');
  pose('len','R',1,500,'tender',600);
  show('monitor-green',1,4400,900);
  look('len',1,4600,'monitor-green',true);
  feel('len',1,4800,'worried','Unease: a colour he has never seen');
  pose('len','R',1,5000,'chest',450);
  // s2 — gentle invitation: enter Noema's classroom.
  for(const id of ['nia-bed','care-motes','monitor','monitor-green'])gone(id,2,0,700);
  goneP('len',2,0,700);
  for(const id of ['nadir','mara'])showP(id,2,600,900,id+'-desk');
  show('reformulation',2,1300,900);
  feel('mara',2,700,'relieved','Mara still prefers reformulation');
  feel('nadir',2,700,'curious','Nadir pauses beside the offered wording, interested');
  look('nadir',2,1500,'reformulation',true);
  look('mara',2,1600,'reformulation',true);
  pose('nadir','R',2,3600,'invite',600);
  feel('nadir',2,3700,'happy','A gentle invitation, consequences left open');
  break;}
 }
 s.visual=q.finish(['A father’s gratitude and hesitation as care heals his daughter; a gentle intelligence linking clinic and classroom.','Care reaching medicine, learning, language and food; one student pulling back from a remedy within his reach.','Assisted classmates and one manual thinker; the source’s raw term on a handwritten slip and its smoothed version in an assisted bubble.','Relief and unease at the same bedside; Noema’s classroom with an offered reformulation.'][i]);
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
