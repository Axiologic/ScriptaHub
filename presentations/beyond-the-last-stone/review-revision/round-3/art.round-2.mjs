// Beyond the Last Stone — authoritative book-owned art (repair round 2, 2026-10-22).
// Rewrites every scene's visual in work/scenes.json; spoken lines, audio and the
// emotional plan stay untouched. Run: node presentations/beyond-the-last-stone/work/art.mjs
// Cast use the rigged library people (open eyes, 12 dynamic expressions, gestures,
// gaze) with book-owned prehistoric dress; each identity keeps its own coat in
// Color, Paper and Night. No in-art text except the book's cover title.
import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {ASSETS} from '../../../.agents/skills/shf-presentation-creator/scripts/lib/asset-library.mjs';

const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const GROUND=545; // shared floor contact; captions stay below ~585

// Stable cast: identity, dress and night variants (see work/visual-bible.json).
const CAST={
 ar:{identity:'person-15',hair:'curls',hairColor:'#2f2220',skin:'#8a5a42',coat:'#b4513a',night:'#d9735a',fur:'#e8d6b8',scale:.84,meaning:'Ar, a young hunter who asks what people have actually seen.'},
 taan:{identity:'person-16',hair:'short',hairColor:'#7a4a2a',skin:'#d9a07e',coat:'#c8962f',night:'#e2b54f',fur:'#efe2c6',scale:.82,meaning:'Taan, Ar’s companion who carries spears and first names the bear.'},
 karr:{identity:'person-20',hair:'bob',hairColor:'#6d625a',skin:'#b98262',coat:'#6f5a93',night:'#a48ccd',fur:'#e3d7c3',beard:true,scale:.86,meaning:'Karr, the storyteller who keeps what stories can carry.'},
 kee:{identity:'person-23',hair:'bun',hairColor:'#c9c6c0',skin:'#7a5040',coat:'#3f8a76',night:'#62b79f',fur:'#eadfca',build:.92,scale:.76,meaning:'Kee, the oldest member, who remembers rivers, herds and names.'},
 lu:{identity:'person-17',hair:'short',hairColor:'#3a2a24',skin:'#7a5040',coat:'#4f7fb4',night:'#7fa9d9',fur:'#eadfca',glasses:false,scale:.56,meaning:'Lu, a child who asks about the track and plays with counting stones.'}
};
const LEG={fill:'#6b5140',night:'#a08a74'},SHOE={fill:'#3d2e25',night:'#c4b19a'};

const walk=(node,fn)=>{fn(node);for(const c of node.children||[])walk(c,fn);};
function castMember(a,id,x,emotion,{scale,y=GROUND,pupilsY=0}={}){
 const c=CAST[id],opts={coat:c.coat,dynamicExpressions:true,skin:c.skin,hair:c.hair,hairColor:c.hairColor,glasses:false,beard:!!c.beard,collar:'none'};
 if(c.build)opts.build=c.build;
 const visual=ASSETS[`${c.identity}-${emotion}`]('$asset',opts);
 visual.children=visual.children.filter(p=>p.id!=='$asset.shadow');
 // Prehistoric dress: remove zipper, pocket and buttons; the gold scarf becomes a fur collar.
 const drop=new Set();
 for(const p of visual.children){
  if(p.type==='line'||(p.type==='path'&&p.attrs.d?.startsWith('M-8 -174')))drop.add(p);
  if(p.type==='rect'&&p.attrs.fill==='$coatShade')drop.add(p);
  if(p.type==='circle'&&p.attrs.fill==='$gold')drop.add(p);
  if(p.type==='path'&&p.attrs.fill==='$gold'){
   if(p.attrs.d.startsWith('M11 -175'))drop.add(p); // hanging scarf tail
   else{p.attrs.d='M-31 -183Q0 -171 31 -183L27 -167Q0 -157 -27 -167Z';p.attrs.fill=c.fur;p.themeAttrs={night:{fill:c.fur}};}
  }
 }
 visual.children=visual.children.filter(p=>!drop.has(p));
 walk(visual,node=>{
  const at=node.attrs||{},night={};
  for(const k of ['fill','stroke']){
   if(at[k]===c.coat)night[k]=c.night;
   if(at[k]==='$trouser'){at[k]=LEG.fill;night[k]=LEG.night;}
  }
  if(Object.keys(night).length)node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,...night}};
 });
 // Book-owned expression repair: the library 'skeptical' mouth rises into a smirk and
 // 'curious' arches into a frown. Skeptical becomes a flat, slightly lopsided mouth with
 // narrowed lids (skin-coloured upper lids); curious becomes a small open, interested smile.
 const head=visual.children.find(p=>p.id==='$asset.head');
 const group=state=>head.children.find(p=>p.id==='$asset.expression.'+state);
 group('skeptical').children[0].attrs.d='M-9 21 Q0 21 9 24';
 group('skeptical').children.splice(1,0,
  {id:'$asset.expression.skeptical.lids',type:'path',attrs:{d:'M-18 -8H-2V-1H-18Z M4 -8H20V-1H4Z',fill:c.skin,stroke:'none'}},
  {id:'$asset.expression.skeptical.lidline',type:'path',attrs:{d:'M-18 -1H-2M4 -1H20',fill:'none',stroke:'$structural','stroke-width':2,'stroke-linecap':'round'}});
 group('curious').children[0].attrs.d='M-7 19 Q0 27 7 19';
 if(pupilsY){const eyes=head.children.find(p=>p.id==='$asset.eyes'),pupils=eyes.children.find(p=>p.id==='$asset.pupils');pupils.transform={...pupils.transform,y:pupilsY};}
 for(const leg of ['legL','legR']){
  const g=visual.children.find(p=>p.id==='$asset.'+leg);
  for(const p of g.children)if(p.attrs.fill==='$structural'){p.attrs.fill=SHOE.fill;p.themeAttrs={night:{fill:SHOE.night}};}
 }
 a.add({id,asset:'custom',x,y,scale:scale??c.scale,visual,meaning:c.meaning,options:{rig:'character',dynamicExpressions:true}});
}

for(const [index,s]of scenes.entries()){
 const a=stageAuthor(),{n,path,tint,text}=a;
 const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
 // Stage-coordinate drawing whose object origin sits at its visual centre, so gaze targets are true.
 const absObj=(id,cx,cy,kids,meaning)=>obj(id,cx,cy,[{...n('g'),transform:{x:-cx,y:-cy},children:kids}],meaning);
 const fill=(d,color,night=color)=>tint(n('path',{d,fill:color}),night);
 const oval=(cx,cy,rx,ry,color,night=color)=>tint(n('ellipse',{cx,cy,rx,ry,fill:color}),night);
 const stroke=(d,color,w,night=color)=>tint(path(d,color,w),night);
 const act=(actor,beat,action,extra={})=>a.actions.push({actor,action,beat,durationMs:850,...extra});
 const feel=(id,beat,emotion,offsetMs=200)=>act(id,beat,'character.express',{emotion,offsetMs,durationMs:700});
 const look=(id,target,beat,offsetMs=300)=>act(id,beat,'lookAt',{target,offsetMs,durationMs:700});
 const gesture=(id,beat,g,offsetMs=1150,durationMs=2400)=>act(id,beat,'character.gesture',{gesture:g,offsetMs,durationMs});
 const walkTo=(id,beat,x,offsetMs=1200,durationMs=1600)=>act(id,beat,'walkTo',{x,offsetMs,durationMs});
 const appear=(id,beat,offsetMs=250,durationMs=900)=>act(id,beat,'appear',{offsetMs,durationMs});
 const performance=[];
 const dashed=d=>{const p=stroke(d,'#5a3a2a',4,'#3d2a20');p.attrs={...p.attrs,'stroke-dasharray':'3 9',opacity:.5};return p;};

 // A flat tapered band along a quadratic centreline: rivers and trails without round caps.
 const ribbon=([x0,y0],[cx,cy],[x2,y2],w0,w1,color,night,steps=18)=>{const L=[],R=[];for(let i=0;i<=steps;i++){const t=i/steps,u=1-t;
  const x=u*u*x0+2*t*u*cx+t*t*x2,y=u*u*y0+2*t*u*cy+t*t*y2,dx=2*u*(cx-x0)+2*t*(x2-cx),dy=2*u*(cy-y0)+2*t*(y2-cy),len=Math.hypot(dx,dy),w=(w0+(w1-w0)*t)/2;
  L.push(`${(x-dy/len*w).toFixed(1)} ${(y+dx/len*w).toFixed(1)}`);R.push(`${(x+dy/len*w).toFixed(1)} ${(y-dx/len*w).toFixed(1)}`);}
  return fill('M'+L.join('L')+'L'+R.reverse().join('L')+'Z',color,night);};
 // Ochre outline bison in the manner of a cave painting: strokes only, so it reads as an image, not an animal.
 const cavePainting=(dx,dy)=>[stroke(`M${dx-38} ${dy}Q${dx-44} ${dy-26} ${dx-24} ${dy-34}Q${dx-8} ${dy-52} ${dx+14} ${dy-42}Q${dx+38} ${dy-36} ${dx+40} ${dy-12}L${dx+38} ${dy}Z`,'#b5743a',4,'#e0a463'),
  stroke(`M${dx-56} ${dy-14}a12 11 0 1 0 24 0a12 11 0 1 0 -24 0`,'#b5743a',4,'#e0a463'),stroke(`M${dx-50} ${dy-22}Q${dx-58} ${dy-30} ${dx-50} ${dy-34}`,'#b5743a',4,'#e0a463'),
  stroke(`M${dx-30} ${dy}L${dx-34} ${dy+18}M${dx-18} ${dy}L${dx-16} ${dy+18}M${dx+20} ${dy}L${dx+16} ${dy+18}M${dx+32} ${dy}L${dx+36} ${dy+18}`,'#b5743a',4,'#e0a463')];
 // Recognisable, reusable book-owned props (each drawn once per scene, never labelled).
 const hearth=(id,x,meaning,k=1)=>obj(id,x,GROUND,[
  ...[-58,-30,0,30,58].map((dx,i)=>oval(dx,-6+(i%2)*2,16,10,'#857a70','#9b9188')),
  stroke('M-44 -10L40 -30M-40 -30L44 -10','#7a5235',11,'#a77a52'),
  fill('M-30 -22Q-34 -64 -6 -92Q-4 -64 10 -58Q14 -82 30 -96Q44 -60 32 -22Z','#e5733a','#f08a4e'),
  fill('M-14 -22Q-16 -48 2 -66Q6 -44 18 -40Q22 -30 16 -22Z','#f4c04e','#f7d26e')
 ],meaning,k);
 const foodHide=(id,x,meaning)=>obj(id,x,GROUND,[
  fill('M-52 -2Q-60 -22 -38 -26Q0 -34 40 -26Q60 -22 52 -2Q0 6 -52 -2Z','#b08657','#c29a6c'),
  ...[[-24,-16],[2,-19],[26,-15]].map(([x,y])=>fill(`M${x-11} ${y+4}Q${x-12} ${y-6} ${x} ${y-7}Q${x+12} ${y-6} ${x+11} ${y+4}Z`,'#7c3d2b','#a65a43'))
 ],meaning);
 const paw=(cx,cy,k=1,color='#4a3a31')=>[
  fill(`M${cx-24*k} ${cy+6*k}Q${cx-28*k} ${cy-14*k} ${cx} ${cy-14*k}Q${cx+28*k} ${cy-14*k} ${cx+24*k} ${cy+6*k}Q${cx} ${cy+18*k} ${cx-24*k} ${cy+6*k}Z`,color),
  ...[-23,-11.5,0,11.5,23].map((dx,i)=>oval(cx+dx*k,cy-(23+(i===0||i===4?0:5))*k,6.5*k,5.5*k,color)),
  ...[-23,-11.5,0,11.5,23].map((dx,i)=>stroke(`M${cx+dx*k} ${cy-(31+(i===0||i===4?0:5))*k}L${cx+dx*1.12*k} ${cy-(38+(i===0||i===4?0:5))*k}`,color,3))
 ];

 if(index===0){
  // The missing herd: an empty pass beyond the ridges, the river at the black rock,
  // and three people around one small fire and one small food hide.
  absObj('river',120,440,[ribbon([235,270],[150,420],[-40,515],24,92,'#7fa8c8','#3f6f94'),
   fill('M72 454L78 436L92 420L112 412L134 414L150 424L160 440L162 454Z','#57524d','#8d8780'),
   fill('M92 420L112 412L134 414L126 426L104 430Z','#78716a','#aca59d'),
   stroke('M72 454L78 436L92 420L112 412L134 414L150 424L160 440L162 454','#3a3632',3,'#c4beb6'),
   stroke('M62 458Q86 452 110 458Q136 464 170 456','#cfe0ec',4,'#7fa8c8')],'The low river reaches the black rock, which sits in it like the back of a sleeping animal.');
  absObj('empty-route',1000,420,[ribbon([1068,540],[1000,420],[965,286],70,14,'#dcc394','#4e4436')],'An empty trail runs up into the pass; no animal or fresh hoof sign is on it.');
  absObj('far-ridges',600,240,[fill('M0 292L0 226L130 208L270 240L430 172L600 228L750 192L870 244L905 292Z','#d6c09e','#2c3540'),fill('M1025 292L1070 232L1200 204L1200 292Z','#d6c09e','#2c3540')],'Flat ridges frame an empty pass on the right where the herd should appear.');
  hearth('embers',540,'A small fire: the camp’s only warmth while the herd is late.');
  foodHide('food-hide',438,'The remaining food, small enough to sit on one hide.');
  castMember(a,'kee',330,'worried',{pupilsY:3});castMember(a,'karr',660,'neutral');castMember(a,'ar',870,'skeptical');
  // Line 1 — restrained urgency: Karr offers a hopeful story; Kee watches the food; Ar watches the empty pass.
  feel('kee',1,'worried');look('kee','food-hide',1,150);act('kee',1,'reach',{offsetMs:900,durationMs:3800});
  feel('karr',1,'determined');gesture('karr',1,'invite',900,2600);
  feel('ar',1,'skeptical',200);act('ar',1,'lookAt',{target:'empty-route',up:true,offsetMs:300,durationMs:700});
  // Line 2 — grounded concern: Ar comes back toward the fire; Karr's confidence falls; Kee asks what now.
  walkTo('ar',2,830,250,1100);feel('ar',2,'worried',300);look('ar','karr',2,1700);
  feel('karr',2,'worried',500);gesture('karr',2,'recoil',1800,2400);
  act('kee',2,'lookAt',{target:'karr',up:true,offsetMs:300,durationMs:700});feel('kee',2,'sad',400);gesture('kee',2,'question',1100,2400);
  performance.push('1: Kee worried, eyes lowered to the food hide and her hand reaching toward it; Karr determined, open-armed story; Ar skeptical (flat mouth, narrowed lids), head lifted toward the empty pass.','2: Ar steps back toward the fire, worried; Karr’s confidence falls and he draws his arms in; Kee turns to Karr, sad, with a questioning gesture.');
 }else if(index===1){
  // Which signs can guide us? Observation (bear prints in old snow) beside memory (a faint remembered herd).
  absObj('high-ground',260,270,[fill('M0 300L0 212Q120 162 250 176Q380 190 512 280L540 300Z','#cdb592','#2c3540')],'High ground on the left; one route climbs it.');
  absObj('route-a',560,380,[ribbon([650,478],[560,392],[468,276],44,12,'#dcc394','#4e4436')],'One route climbs onto the high ground.');
  absObj('route-b',920,440,[ribbon([650,478],[900,418],[1230,394],44,16,'#dcc394','#4e4436')],'A second route leaves along the low ground.');
  obj('old-snow',600,515,[fill('M-170 8Q-178 -24 -120 -30Q0 -40 120 -30Q178 -24 170 8Q170 32 0 34Q-170 32 -170 8Z','#dbe6ee','#c3d1db')],'A patch of old snow where signs can be inspected.');
  obj('old-track',600,515,[...paw(-95,14,.95),...paw(10,0,.95),...paw(112,16,.95)],'Three large bear prints with claw marks: something that was seen, not where the bear is now.');
  // The remembered herd is told, not present: ochre cave-painting outlines (no fill) rising on
  // story-smoke from Karr's raised hands, high above the ground line, faded out before line 2.
  absObj('remembered-herd',985,240,[{...n('g',{opacity:.62}),children:[
   ...[0,22,44].map(dx=>stroke(`M${1004+dx} 420Q${1030+dx} 384 ${1010+dx} 350Q${990+dx} 316 ${1012+dx} 268`,'#c79a6a',4,'#d9b48a')),
   ...cavePainting(905,222),...cavePainting(1000,206),...cavePainting(1090,226)]}],'A remembered herd drawn like an ochre cave painting on story-smoke rising from Karr’s hands: what stories carry, not animals present today.');
  castMember(a,'taan',150,'neutral');castMember(a,'ar',320,'curious');castMember(a,'karr',930,'neutral');
  // Line 1 — interested contrast: Ar points at the prints; Taan stares at them; Karr raises the remembered herd.
  feel('ar',1,'curious');look('ar','old-track',1,250);gesture('ar',1,'explain',900,3600);
  feel('taan',1,'surprised',600);look('taan','old-track',1,400);
  look('karr','old-track',1,250);feel('karr',1,'inspired',1900);act('karr',1,'lookAt',{target:'remembered-herd',up:true,offsetMs:1900,durationMs:700});
  gesture('karr',1,'invite',2700,3600);appear('remembered-herd',1,3000,1000);act('remembered-herd',1,'disappear',{offsetMs:6300,durationMs:1100});
  // Line 2 — quiet tension: two routes, no answer; faces turn uncertain and toward each other.
  appear('route-a',2,250,1100);appear('route-b',2,700,1100);
  feel('ar',2,'worried',300);look('ar','karr',2,1100);gesture('ar',2,'question',2000,2400);
  feel('taan',2,'skeptical',300);look('taan','route-a',2,700);
  feel('karr',2,'worried',700);look('karr','ar',2,1400);
  performance.push('1: Ar curious, pointing arm held at the prints; Taan surprised (“Bear,” he whispers); Karr inspired, looking up as he raises his hands and a remembered herd rises like an ochre cave painting on story-smoke; it fades before line 2.','2: Two routes appear; Ar worried, turning to Karr with an open question; Taan skeptical (flat mouth, narrowed lids) eyeing the fork; Karr worried, meeting Ar’s gaze. No route is chosen.');
 }else if(index===2){
  // Thought beside the fire: everyone stands on the same ground under low ridges. Karr stands
  // left of the hearth and argues across the fire toward Kee, who guards the remaining food;
  // Ar listens; the child Lu lays counting stones. The fire sits between Karr and Kee, touching neither.
  absObj('fire-ridges',600,245,[fill('M0 292L0 238L160 214L330 236L520 190L700 224L860 196L1040 232L1200 210L1200 292Z','#d6c09e','#2c3540')],'Low ridges behind the camp put the fireside circle on firm ground.');
  hearth('council-ground',700,'The shared hearth between Karr and Kee.',1.05);
  [0,1,2,3,4,5].forEach(i=>obj('stone-'+(i+1),205+i*26,GROUND-6,[oval(0,0,[11,9,12,10,9,11][i],[8,7,9,8,7,8][i],['#8a8580','#9b8f84','#7d7873','#958b80','#867f78','#a09486'][i],'#aaa49d'),oval(-3,-3,4,2,'#b8b2ac','#cfc9c2')],'Counting stone '+(i+1)+': a stone extends the count, not the food.'));
  foodHide('food-hide',832,'The remaining dried food Kee is counting.');
  obj('roots',1048,GROUND,[...[-14,4,20].map((dx,i)=>fill(`M${dx-9} -6Q${dx-12} -28 ${dx+1} -${36+i*3}Q${dx+12} -28 ${dx+9} -6Q${dx} 2 ${dx-9} -6Z`,'#9c6b45','#b9845b')),stroke('M-14 -34L-18 -46M5 -40L4 -52M21 -38L26 -50','#6f8f4a',3,'#8fb365')],'Three dug roots with their green tops.');
  obj('seeds',1050,GROUND,[fill('M30 -2Q32 -18 46 -20H74Q88 -18 90 -2Z','#7a5235','#a77a52'),...[[46,-22],[56,-26],[66,-22],[52,-30],[62,-31],[74,-24]].map(([x,y])=>oval(x,y,4,3,'#d6b25e','#e5c87a'))],'A bark bowl of gathered seeds.');
  castMember(a,'lu',148,'curious');castMember(a,'ar',405,'neutral');castMember(a,'karr',560,'neutral');castMember(a,'kee',945,'neutral');
  // Line 1 — lively warmth: Lu adds stone after stone; Kee counts the food; Karr argues toward her across the fire.
  feel('lu',1,'curious');look('lu','stone-4',1,250);gesture('lu',1,'explain',600,3800);
  [0,1,2,3,4,5].forEach(i=>appear('stone-'+(i+1),1,700+i*520,500));
  feel('kee',1,'skeptical');look('kee','food-hide',1,300);look('kee','karr',1,2600);gesture('kee',1,'question',3500,2600);
  feel('karr',1,'determined',300);look('karr','kee',1,300);gesture('karr',1,'explain',1100,4800);
  feel('ar',1,'happy',900);look('ar','karr',1,400);
  // Line 2 — human warmth: courage, shared memory and one another; the circle softens.
  feel('kee',2,'happy',250);look('kee','lu',2,350);gesture('kee',2,'invite',1200,2600);
  feel('lu',2,'happy',500);look('lu','kee',2,900);
  feel('karr',2,'relieved',400);gesture('karr',2,'release',1400,2200);
  look('ar','lu',2,600);feel('ar',2,'relieved',400);
  performance.push('1: Lu curious, laying six stones one by one; Kee skeptical over the food, then answering Karr with an open question; Karr, beside the hearth on the shared ground, determined, pointing his argument at her across the fire; Ar amused, listening.','2: Kee smiles and opens her arms toward Lu; Lu looks up, happy; Karr relaxes; Ar turns warmly toward Lu.');
 }else{
  // Join the River People: the first hungry camp, a path toward the ridge gap, Orra's ash route
  // partly wiped on a hide, and the book itself as the invitation.
  // The path leaves the camp ground in front of the people and recedes, narrowing, into the ridge gap.
  absObj('far-path',640,430,[ribbon([300,544],[480,545],[660,544],8,38,'#dcc394','#4e4436'),ribbon([658,544],[770,542],[776,440],38,22,'#dcc394','#4e4436'),ribbon([776,442],[782,356],[800,294],22,9,'#dcc394','#4e4436')],'A path from the camp ground toward the gap in the ridge; where it leads is left to the reader.');
  absObj('camp-ridge',600,250,[fill('M0 292L0 236L140 200L300 230L470 186L650 236L766 292Z','#d6c09e','#2c3540'),fill('M830 292L872 242L886 239L886 292Z','#d6c09e','#2c3540'),fill('M1124 292L1124 236L1200 252L1200 292Z','#d6c09e','#2c3540')],'Low ridges beyond the first camp, continuing behind the book, with a gap the path leads into.');
  hearth('camp-fire',300,'The fire of the first hungry camp.');
  obj('reading-cloth',515,GROUND,[fill('M-56 -2Q-64 -20 -46 -26Q0 -34 46 -26Q64 -20 56 -2Q0 6 -56 -2Z','#c49a68','#c9a274'),stroke('M-40 -12Q-20 -22 0 -14','#5a3a2a',4,'#3d2a20'),dashed('M6 -14Q22 -10 38 -20')],'A hide carrying a charcoal route line, part of it wiped away: guidance without a guarantee.');
  obj('opening-book',1000,GROUND,[
   fill('M122 -322H132V0H122Z','#f3e7d3','#e2e7dc'),
   fill('M-122 -330H110Q122 -330 122 -318V-6Q122 6 110 6H-122Z','#8e3b2a','#b4513a'),
   fill('M-122 -330H-96V6H-122Z','#6d2c20','#8e3b2a'),
   text('Beyond',12,-266,50,'#fbf3e4'),text('the Last',12,-200,50,'#fbf3e4'),text('Stone',12,-134,50,'#fbf3e4'),
   oval(-8,-58,22,13,'#c9b8a0'),oval(28,-56,18,12,'#b9a68c'),oval(10,-80,17,11,'#dccbb2')
  ],'Beyond the Last Stone itself, with a small cairn on its cover: the invitation to read on from the first camp.');
  obj('bookmark',1000,GROUND,[fill('M58 -348V-322H84V-348L71 -339Z','#3f8a76','#62b79f')],'A bookmark at the opening chapter, Fire After the Herd.');
  castMember(a,'kee',165,'curious');castMember(a,'karr',425,'neutral');castMember(a,'ar',640,'neutral');
  // Line 1 — wonder: Ar looks along the path; an idea can guide without certainty.
  appear('reading-cloth',1,250,900);
  feel('ar',1,'inspired',300);look('ar','far-path',1,300);gesture('ar',1,'reflect',1300,2600);
  feel('karr',1,'curious',600);look('karr','ar',1,600);
  feel('kee',1,'curious',900);look('kee','ar',1,900);
  // Line 2 — inviting concern: Ar turns back to the camp; Kee invites the viewer in.
  look('ar','kee',2,250);feel('ar',2,'curious',300);
  feel('kee',2,'happy',500);gesture('kee',2,'invite',1100,2600);
  feel('karr',2,'worried',600);gesture('karr',2,'question',1500,2400);
  appear('bookmark',2,1600,900);
  performance.push('1: Ar inspired, looking along the path with a reflective gesture; Kee and Karr turn to him, curious.','2: Ar turns back to the camp, curious; Kee smiles and opens her arms in invitation; Karr shows the concern of the hungry camp with an open question; a bookmark marks where to begin.');
 }
 const meanings=[
  'Flat ridges, an empty trail into the pass and the river at the black rock frame three distinct River People around one small fire and one food hide; Karr’s hopeful story meets Kee’s and Ar’s concern.',
  'Ar points at three bear prints in old snow while Taan stares; as Karr raises his hands, a remembered herd rises on story-smoke as ochre cave-painting outlines and fades again. Two unlabelled routes appear and the three turn to one another without choosing.',
  'Under low ridges, Karr stands beside the shared hearth and argues across the fire toward Kee, who guards the remaining food, roots and seeds; Ar listens and the child Lu lays six counting stones; the circle then warms.',
  'At the first hungry camp Ar looks along a path toward the ridge, beside a hide whose route line is partly wiped; Kee invites the viewer in, and the book with its bookmark marks where to begin.'
 ];
 s.visual={...a.finish(meanings[index]),performance};
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('Beyond the Last Stone art written for '+scenes.length+' scenes.');
