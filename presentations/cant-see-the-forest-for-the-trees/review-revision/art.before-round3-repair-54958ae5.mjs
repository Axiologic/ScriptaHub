// Authoritative artwork generator for the current two-sentence-per-scene film
// (round-2 redesign after the independent visual review of art 13a920f4…).
// It rebuilds only scene.visual in work/scenes.json; spoken lines, emotional
// plans, sources and audio are untouched. Previous compositions are archived:
//   review-revision/scenes.before-round2-repair-13a920f4.json + art.before-round2-repair-13a920f4.mjs
//   review-revision/scenes.before-round1-repair-35ec7757.json (round-1 reviewed art)
//   review-revision/collision-repair-art-35ec7757.mjs        (its repair script)
//   review-revision/legacy-railyard-art.mjs                 (never run again)
// Run from the repository root with a staging target, e.g.
//   node presentations/cant-see-the-forest-for-the-trees/art.mjs --output=<staging dir>
// Layout rule: at the 1200-wide stage the caption occupies roughly
// x 274–926, y 580–650, so everything ends above y ≈ 560 (feet at 555).
// Held postures are authored as rig BASELINES (arm/head/pupil transforms), so the
// gesture/gaze a sentence needs is present at every sampled frame; transient
// gestures are sized so their peak brackets the sentence midpoint.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {storyPerson} from '../../tools/shf/people-poses.mjs';
import {ASSETS} from '../../.agents/skills/shf-presentation-creator/scripts/lib/asset-library.mjs';
const base=path.dirname(new URL(import.meta.url).pathname),file=path.join(base,'work/scenes.json');
const scenes=JSON.parse(fs.readFileSync(file,'utf8'));
const FLOOR=555;
// Stable cast: one author across the film, every other person has a distinct identity and coat.
const CAST={
 author:{identity:'person-01',coat:'#2f7a78',night:'#86cbc4'},
 planner:{identity:'person-11',coat:'#7a5c99',night:'#bfa8de'},
 engineer:{identity:'person-04',coat:'#c4703c',night:'#eaa97c'},
 operator:{identity:'person-14',coat:'#4f6a92',night:'#a3b9de'},
 resident:{identity:'person-21',coat:'#b0475a',night:'#e8959f'}
};
// Page-coloured materials keep dark ink in every theme.
const PAGE='#fffaf0',PAGE_NIGHT='#ece6d8',INK='#25323d',CORAL='#b4473a',BLUE='#2f5f8a',GREY='#8796a3';

function build(index){
 const a=stageAuthor(),{n,path:line,text,tint}=a;
 const at=(beat,offsetMs=250)=>({beat,offsetMs});
 const appear=(id,beat,offsetMs=250,durationMs=700)=>a.actions.push({actor:id,action:'appear',...at(beat,offsetMs),durationMs});
 const vanish=(id,beat,offsetMs=250,durationMs=700)=>a.actions.push({actor:id,action:'disappear',...at(beat,offsetMs),durationMs});
 const move=(id,beat,x,y,offsetMs=250,durationMs=1600)=>a.actions.push({actor:id,action:'moveTo',x,y,...at(beat,offsetMs),durationMs});
 const express=(id,beat,emotion,offsetMs=150)=>a.actions.push({actor:id,action:'character.express',emotion,...at(beat,offsetMs),durationMs:500});
 const gesture=(id,beat,g,offsetMs,durationMs)=>a.actions.push({actor:id,action:'character.gesture',gesture:g,...at(beat,offsetMs),durationMs});
 // lookAt is only used on figures that are NOT mirrored (its sign is computed in world x).
 const look=(id,beat,target,offsetMs=300,up=false)=>a.actions.push({actor:id,action:'lookAt',target,...at(beat,offsetMs),durationMs:600,...(up?{up:true}:{})});
 const shape=(id,x,y,kids,meaning,scale=1,anchors)=>{const o=a.object(id,x,y,kids,meaning,scale);if(anchors)o.visual.anchors=anchors;a.add(o);return o;};
 const rect=(x,y,w,h,fill,rx=6,night)=>{const r=n('rect',{x,y,width:w,height:h,rx,fill});return night?tint(r,night):r;};
 const fillPath=(d,fill,night)=>{const p=n('path',{d,fill});return night?tint(p,night):p;};
 const words=(value,x,y,size,color,night)=>{const t=text(value,x,y,size,color);if(night)t.themeAttrs={...t.themeAttrs,night:{fill:night}};return t;};
 const nodeOf=(o,part)=>{const want='$asset.'+part,find=node=>node.id===want?node:(node.children||[]).map(find).find(Boolean);return find(o.visual);};
 // Rigged person with an authored, held posture.
 //  armL/armR: shoulder rotation in degrees (armR negative raises the forward hand; armL negative swings it across the body)
 //  gaze:[x,y] WORLD-direction pupil offset (negative x looks screen-left); tilt: head rotation in the figure's own frame (negative = chin up toward the side it faces)
 //  lean: whole-body world rotation about the feet; faceLeft mirrors the figure so its forward hand points left.
 const person=(id,role,x,emotion,{scale=.9,faceLeft=false,meaning,armL=0,armR=0,gaze=[0,0],tilt=0,lean=0}={})=>{
  const c=CAST[role];storyPerson(a,id,x,FLOOR,{identity:c.identity+'-'+emotion,coat:c.coat,scale});
  const o=a.objects.find(v=>v.id===id);
  const walk=node=>{for(const key of ['fill','stroke'])if(node.attrs?.[key]===c.coat)node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,[key]:c.night}};(node.children||[]).forEach(walk);};walk(o.visual);
  const m=faceLeft?-1:1;
  if(faceLeft)o.visual.transform={...o.visual.transform,scaleX:-(o.visual.transform?.scaleX||1)};
  if(lean){o.visual.transform={...o.visual.transform,rotate:lean};o.visual.origin=[0,0];}
  const armLNode=nodeOf(o,'armL'),armRNode=nodeOf(o,'armR'),head=nodeOf(o,'head'),pupils=nodeOf(o,'pupils');
  if(armL){armLNode.transform={...armLNode.transform,rotate:armL};armLNode.origin=[-34,-157];}
  if(armR){armRNode.transform={...armRNode.transform,rotate:armR};armRNode.origin=[32,-156];}
  if(tilt)head.transform={...head.transform,rotate:tilt};
  pupils.transform={...pupils.transform,x:m*gaze[0],y:gaze[1]};
  o.meaning=meaning||o.meaning;return o;
 };
 const page=(id,x,y,w,h,kids,meaning)=>shape(id,x,y,[rect(-w/2,-h/2,w,h,PAGE,10,PAGE_NIGHT),...kids],meaning,1,{left:[-w/2,0],right:[w/2,0],top:[0,-h/2],bottom:[0,h/2]});
 const textLines=(x0,y0,widths,gap,color=GREY,width=6)=>widths.map((w,i)=>line(`M${x0} ${y0+i*gap}H${x0+w}`,color,width));

 if(index===0){
  // The author stands at his own desk (behind it, so the tabletop occludes his legs),
  // one hand on the desk beside the laptop, looking up at what the edit did.
  person('author','author',370,'curious',{armR:-20,gaze:[2,-2.5],tilt:-6,meaning:'The author at his desk, reading what the AI edit made of his question.'});
  shape('desk',550,465,[rect(-300,-12,600,22,'#a7744f',6,'#8f6a4e'),tint(line('M-260 10V90M260 10V90','#5d4635',12),'#a88563')],'The author’s working desk on the shared floor.');
  // An unbranded laptop whose screen shows the edited text being rewritten.
  shape('laptop',470,453,[
   tint(rect(-62,-82,124,78,'#33424f',8),'#9fb0bd'),rect(-54,-74,108,62,'#e8f1ee',4,'#dfe9e6'),
   ...textLines(-42,-60,[84,70,78],15,'#5d86ad',5),
   tint(fillPath('M-76 -4H76L86 8H-86Z','#5d6f80'),'#b9c7d3')
  ],'The AI editing tool: a laptop rewriting the author’s text.');
  page('working-draft',440,192,260,170,[words('Original',0,-46,34,'#6c5a48','#5a4a3a')],'The author’s original draft card.');
  // Dimmed after-image of the original question, revealed as the vivid version fades.
  shape('sharp-question-dim',440,192,[words('How sharp',0,0,40,'#8a8f96'),words('is the cost?',0,40,40,'#8a8f96'),line('M-92 66L-69 52L-46 66L-23 52L0 66L23 52L46 66L69 52L92 66','#a9aeb4',4)],'The original question, fading after the smoothing.');
  a.objects.find(o=>o.id==='sharp-question-dim').visual.opacity=.42;
  shape('sharp-question',440,192,[words('How sharp',0,0,40,CORAL),words('is the cost?',0,40,40,CORAL),line('M-92 66L-69 52L-46 66L-23 52L0 66L23 52L46 66L69 52L92 66',CORAL,5)],'The author’s original pointed question and its sharp edge (schematic paraphrase).');
  shape('edit-arrow',600,192,[line('M-18 0H14M4 -11L16 0L4 11','$ink',5)],'The AI edit turns the original into the smoothed version.');
  page('smooth-line',760,192,260,170,[words('Smoothed',0,-46,34,'#6c5a48','#5a4a3a'),words('There are',0,0,40,BLUE),words('trade-offs.',0,40,40,BLUE),line('M-92 66H92',BLUE,5)],'The AI’s smoother sentence: reasonable, but without the question.');
  // The book in full: forest-green cover, the complete title and a row of small trees.
  shape('book',1060,FLOOR,[
   rect(-116,-300,232,300,'#2e5c4f',10,'#3d7464'),rect(-116,-300,18,300,'#1f4337',4,'#2c5a4c'),rect(-108,-6,222,8,'#f1e9d6',2),
   words('Can’t See',8,-228,36,'#f6efdc'),words('the Forest',8,-186,36,'#f6efdc'),words('for the Trees',8,-144,31,'#f6efdc'),
   ...[-56,-18,20,58].map((dx,i)=>fillPath(`M${dx} -96L${dx+17} -56H${dx-17}Z`,i===2?'#e3b65a':'#8fc4a5')),line('M-78 -50H96','#8fc4a5',3)
  ],'Can’t See the Forest for the Trees: the book this experience opens.',1,{left:[-116,-150],right:[116,-150],top:[0,-300],bottom:[0,0]});
  // Sentence 1: the smoothed version appears and the original question dims to an after-image.
  appear('edit-arrow',1,1300);appear('smooth-line',1,1900,900);vanish('sharp-question',1,2400,1400);
  express('author',1,'sad',2300);
  // Sentence 2: the book enters; he turns to it with an open, pointing invitation.
  appear('book',2,200,900);express('author',2,'inspired',200);look('author',2,'book',300);
  a.actions.push({actor:'author',action:'walkTo',x:715,...at(2,300),durationMs:2000});
  gesture('author',2,'explain',2400,4400);
  return a.finish('The author stands at his desk, hand beside the laptop, and looks up with disappointment as an AI edit turns his pointed question into a reasonable sentence; the original dims to an after-image. The complete book then appears; he turns, walks along the desk toward it and gestures to it.');
 }
 if(index===1){
  // Sentence 1: the author rereads a polished page; margin notes for doubt, urgency and responsibility fade.
  person('author','author',200,'worried',{gaze:[3,0],tilt:4,meaning:'The author rereads the polished passage with quiet unease.'});
  page('writing-surface',500,290,330,330,[words('Polished passage',0,-120,32,'#6c5a48','#5a4a3a')],'The smoothed manuscript page.');
  shape('continued-draft',500,290,textLines(-108,-74,[236,220,232,190,228,214,160],34,'#7f94a6',7),'Even, reasonable lines of the smoothed argument.');
  // The author’s own question mark, kept inside the page’s left margin beside the first line.
  shape('retained-question',357,216,[words('?',0,14,44,CORAL,'#a13628')],'The author’s own question mark, kept in the margin.');
  const mark=(id,label,y,color,night,meaning)=>shape(id,760,y,[tint(line('M-82 0H-62',color,6),night),text(label,0,13,38,color)],meaning);
  const doubt=mark('doubt-mark','doubt',200,CORAL,'#ee8f82','Doubt, noted in the margin.');
  const urgency=mark('urgency-mark','urgency',290,'#a8741a','#e7bb62','Urgency, noted in the margin.');
  const resp=mark('responsibility-mark','responsibility',380,'#6b4f8f','#c0a6e3','Responsibility, noted in the margin.');
  for(const o of [doubt,urgency,resp]){o.visual.children[1].attrs['text-anchor']='start';o.visual.children[1].attrs.x=-50;o.visual.children[1].themeAttrs={night:{fill:o.visual.children[0].themeAttrs.night.stroke}};}
  look('author',1,'writing-surface',300);a.actions.push({actor:'author',action:'walkTo',x:232,...at(1,600),durationMs:1200});
  for(const [id,d] of [['doubt-mark',0],['urgency-mark',500],['responsibility-mark',1000]])vanish(id,1,5600+d,2400);
  // Sentence 2: the same pattern in companies, research, politics, and the technology connecting them.
  for(const id of ['writing-surface','continued-draft','retained-question'])vanish(id,2,100,600);
  // Library props drawn flat: the catalogue's ground-shadow ellipse is removed.
  const prop=(id,asset,x,y,scale,color,meaning)=>{const visual=ASSETS[asset]('$asset',{color});visual.children=visual.children.filter(c=>c.attrs?.fill!=='$shadow');a.add({id,asset:'custom',x,y,scale,visual,meaning});return id;};
  const domain=(id,asset,label,x,meaning,color,i)=>{const tag=(id==='proposal'?'companies':id)+'-label';prop(id,asset,x,300,.66,color,meaning);shape(tag,x,140,[text(label,0,0,38)],'Label: '+label);appear(id,2,700+i*350,700);appear(tag,2,900+i*350,600);};
  domain('proposal','factory','companies',380,'Companies: a factory standing for commercial organisations.','$coral',0);
  domain('research','microscope','research',600,'Research: a laboratory microscope.','$teal',1);
  domain('politics','courthouse','politics',820,'Politics: a public institution building.','$gold',2);
  // Civic building redrawn with solid materials so it holds contrast on Paper.
  const civic=a.objects.find(o=>o.id==='politics');
  civic.visual.children=[
   tint(n('path',{d:'M-78 -112L0 -150L78 -112Z',fill:'#6b4f8f'}),'#c0a6e3'),tint(rect(-74,-112,148,12,'#6b4f8f',2),'#c0a6e3'),
   ...[-54,-18,18,54].map(x=>tint(rect(x-9,-98,18,82,'#c69443',3),'#e2b664')),tint(rect(-82,-16,164,16,'#6b4f8f',3),'#c0a6e3')];
  civic.scale=1;
  // Links end on the router’s top edge (y 476); antennas stand outside the link points.
  for(const [i,x,end] of [[0,380,568],[1,600,600],[2,820,632]]){const id='link-'+x,mx=(x+end)/2,my=389;shape(id,mx,my,[tint(line(`M${x-mx} -88L${end-mx} 87`,'#3f6f9c',5),'#86b4e0')],'Technology links this domain to the others.');appear(id,2,1700+i*300,700);}
  shape('unknown',600,520,[tint(line('M-56 -44V-84M56 -44V-84','#3f6f9c',6),'#86b4e0'),tint(rect(-70,-44,140,44,'#3f6f9c',10),'#86b4e0'),...[-38,-18,2].map(x=>n('circle',{cx:x,cy:-22,r:5,fill:'#e2b664'})),line('M22 -22H46','#e2b664',4)],'The technologies connecting them: a network router linking all three.');
  shape('unknown-label',800,500,[text('technology',0,0,38)],'Label: the connecting technologies.');
  appear('unknown',2,1400,700);appear('unknown-label',2,1500,600);
  move('author',2,170,FLOOR,200,900);express('author',2,'determined',200);gesture('author',2,'explain',700,5600);
  return a.finish('The author rereads a polished page with unease while his own question mark stays in its margin and notes for doubt, urgency and responsibility fade. The pattern then reappears in a factory, a laboratory and a public institution, each linked to a router for the connecting technology.');
 }
 if(index===2){
  // One shared pipeline: each specialist tends a section; the joint between them leaks unnoticed.
  shape('pipeline',600,215,[
   tint(rect(-500,-16,470,32,'#5a9b8f',8),'#6fbfb0'),tint(rect(30,-16,470,32,'#c69443',8),'#e2b664'),
   tint(rect(-40,-24,22,48,'#58646e',4),'#9fb0bd'),tint(rect(18,-24,22,48,'#58646e',4),'#9fb0bd')
  ],'One shared pipeline: a teal section and a gold section meet at an unowned joint.',1,{left:[-500,0],right:[500,0],top:[0,-24],bottom:[0,24]});
  // Gauge mounted ABOVE the pipe, well clear of the planner’s head.
  shape('gauge',390,215,[tint(line('M0 -16V-40','#58646e',6),'#9fb0bd'),n('circle',{cx:0,cy:-76,r:34,fill:PAGE}),tint(n('circle',{cx:0,cy:-76,r:34,fill:'none',stroke:'#58646e','stroke-width':5}),'#9fb0bd'),line('M0 -76L19 -94',CORAL,5),line('M-22 -60H22','#9aa8b4',3)],'The planner’s pressure gauge on the teal section.');
  // Valve on a short branch dropped from the gold section to the engineer’s hand height.
  shape('valve',822,215,[tint(rect(-7,16,14,170,'#9b7432',4),'#e2b664'),tint(n('circle',{cx:0,cy:188,r:24,fill:'none',stroke:'#7b4b2a','stroke-width':7}),'#e2a77a'),tint(line('M-24 188H24M0 164V212','#7b4b2a',4),'#e2a77a'),tint(n('circle',{cx:0,cy:188,r:6,fill:'#7b4b2a'}),'#e2a77a')],'The engineer’s valve wheel on a branch of the gold section.');
  // Clipboard drawn before the planner so her hand grips its top edge.
  shape('upkeep-ledger',198,500,[rect(-34,-46,68,92,'#8b6a4b',6,'#a88563'),rect(-27,-34,54,74,PAGE,3,PAGE_NIGHT),rect(-12,-52,24,12,'#58646e',3,'#9fb0bd'),line('M-17 -18L-11 -12L-3 -24M-17 4L-11 10L-3 -2M-17 26L-11 32L-3 20',BLUE,3),line('M3 -18H19M3 4H19M3 26H19','#9aa8b4',3)],'The planner’s upkeep ledger: every item in her own section is checked.');
  person('planner','planner',255,'worried',{armL:16,armR:-132,gaze:[3,-3],tilt:-7,meaning:'The planner holds her checklist and looks up at her own gauge, pointing to it.'});
  person('specialist-b','engineer',900,'worried',{faceLeft:true,armR:-75,gaze:[-4,1.5],tilt:3,lean:-2,meaning:'The engineer grips and turns his valve with concerned brows.'});
  // Her pencil continues the raised hand toward the gauge she is reading.
  shape('planner-pencil',304,368,[tint(line('M0 0L13 -34','#c69443',6),'#e2b664'),line('M13 -34L16 -42','#25323d',4)],'The planner’s pencil, raised toward her gauge.');
  const drops=[0,1,2].map(i=>shape('drop-'+i,600,250,[tint(fillPath('M0 -12Q9 2 0 8Q-9 2 0 -12Z','#3f7fb6'),'#7fb7e6')],'Water dripping from the unowned joint.'));
  drops.forEach((d,i)=>{appear(d.id,1,400+i*1200,200);move(d.id,1,600,520,400+i*1200,1500);});
  shape('unowned-consequence',600,540,[tint(n('ellipse',{cx:0,cy:0,rx:88,ry:11,fill:'#3f7fb6',opacity:.75}),'#7fb7e6')],'The consequence of the whole: a spreading puddle that belongs to neither section.');
  appear('unowned-consequence',1,1500,2400);
  // Sentence 1: both are absorbed in their own part; small motivated work beats.
  gesture('specialist-b',1,'resolve',600,1600);
  // Sentence 2: the author steps in beside the leak, uncertain, and raises a question hand toward it.
  person('author','author',430,'curious',{armR:-98,gaze:[3,0],tilt:4,meaning:'The author, uncertain but still asking where people can make a useful difference.'});
  appear('author',2,100,800);a.actions.push({actor:'author',action:'walkTo',x:450,...at(2,100),durationMs:1300});
  shape('unpriced-option',690,330,[n('circle',{cx:0,cy:0,r:40,fill:PAGE}),tint(n('circle',{cx:0,cy:0,r:40,fill:'none',stroke:CORAL,'stroke-width':5}),'#ee8f82'),words('?',0,16,46,CORAL)],'An open question beside the leaking joint: where could someone still make a useful difference?');
  appear('unpriced-option',2,900,800);
  look('planner',2,'unpriced-option',1800);
  return a.finish('A planner holds her checked ledger and looks up at her gauge; an engineer grips and turns his valve. Each tends their own section of one pipeline while the joint between them drips into an unowned puddle. The author then steps in beside the leak and raises an open question.');
 }
 // index 3: the conflict is acted out under a smooth headline that later slides away.
 person('operator','operator',700,'worried',{armR:-50,armL:-14,gaze:[3,0],tilt:-3,lean:-3,meaning:'The operator, defending his side of a real conflict with an open hand.'});
 person('resident','resident',940,'angry',{faceLeft:true,armR:-78,gaze:[-4,0],tilt:-2,lean:-3,meaning:'An affected resident leaning in and pointing, pressing the other side of the conflict.'});
 // Opaque, unframed headline card kept entirely above both heads (bottom 280, head tops ≈ 305).
 shape('polished-explanation',820,180,[
  rect(-240,-90,480,180,PAGE,16,PAGE_NIGHT),words('All systems align.',0,-8,50,BLUE),...textLines(-150,38,[300,240],26,'#a5b0ba',6)
 ],'A smooth explanation hung over the conflict.',1,{left:[-240,0],right:[240,0],top:[0,-90],bottom:[0,90]});
 person('author','author',215,'curious',{armR:-38,gaze:[3,0],tilt:3,meaning:'The author, inviting the reader to examine the edited manuscript.'});
 page('uncertainty-note',360,400,150,190,[...textLines(-52,-60,[104,92,104,70,96],26,'#7f94a6',5),words('?',40,78,44,CORAL,'#a13628')],'The edited manuscript, held open for the reader’s question.');
 // Magnifier resting on the manuscript lines, handle toward the author’s inviting hand.
 shape('review-route',372,370,[tint(n('circle',{cx:0,cy:0,r:40,fill:'none',stroke:'#4d3b2a','stroke-width':8}),'#5a4632'),tint(line('M-29 29L-62 62','#4d3b2a',12),'#5a4632')],'A magnifying glass over the edited manuscript: the reader’s route back to what changed.');
 // Sentence 1: the conflict is visible first; the polished headline settles over it.
 appear('polished-explanation',1,1400,1000);
 a.actions.push({actor:'resident',action:'walkTo',x:925,...at(1,300),durationMs:900});
 look('author',1,'polished-explanation',400,true);
 // Sentence 2: the headline slides away; the author turns to the manuscript and the magnifier lands on it.
 move('polished-explanation',2,1560,180,300,1500);
 look('author',2,'uncertainty-note',300);express('author',2,'determined',300);
 appear('review-route',2,600,700);
 return a.finish('An operator and an affected resident face each other in open conflict while a smooth “All systems align.” headline settles above them. In the second sentence the headline slides away, the author turns to the edited manuscript with an inviting hand, and a magnifier rests on it.');
}

for(let i=0;i<scenes.length;i++)scenes[i].visual=build(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('artSha256',crypto.createHash('sha256').update(JSON.stringify(scenes.map(s=>({id:s.id,visual:s.visual})))).digest('hex'));
import {buildBookFilm} from '../../tools/shf/build-book-film.mjs';
await buildBookFilm(new URL('.',import.meta.url).pathname);
