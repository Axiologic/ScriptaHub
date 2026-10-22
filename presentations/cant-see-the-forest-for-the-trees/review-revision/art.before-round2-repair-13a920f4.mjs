// Authoritative artwork generator for the current two-sentence-per-scene film
// (round-1 redesign after the independent visual review of art 35ec7757…).
// It rebuilds only scene.visual in work/scenes.json; spoken lines, emotional
// plans, sources and audio are untouched. Previous compositions are archived:
//   review-revision/scenes.before-round1-repair-35ec7757.json (reviewed art)
//   review-revision/collision-repair-art-35ec7757.mjs        (its repair script)
//   review-revision/legacy-railyard-art.mjs                 (never run again)
// Layout rule: at the 1200-wide stage the caption occupies roughly
// x 274–926, y 580–650, so everything ends above y ≈ 560 (feet at 555).
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
const PAGE='#fffaf0',PAGE_NIGHT='#ece6d8',INK='#25323d',CORAL='#b4473a',BLUE='#2f5f8a';

function build(index){
 const a=stageAuthor(),{n,path:line,text,tint}=a;
 const at=(beat,offsetMs=250)=>({beat,offsetMs});
 const appear=(id,beat,offsetMs=250,durationMs=700)=>a.actions.push({actor:id,action:'appear',...at(beat,offsetMs),durationMs});
 const vanish=(id,beat,offsetMs=250,durationMs=700)=>a.actions.push({actor:id,action:'disappear',...at(beat,offsetMs),durationMs});
 const move=(id,beat,x,y,offsetMs=250,durationMs=1600)=>a.actions.push({actor:id,action:'moveTo',x,y,...at(beat,offsetMs),durationMs});
 const express=(id,beat,emotion,offsetMs=150)=>a.actions.push({actor:id,action:'character.express',emotion,...at(beat,offsetMs),durationMs:500});
 const gesture=(id,beat,g,offsetMs=450,durationMs=2200)=>a.actions.push({actor:id,action:'character.gesture',gesture:g,...at(beat,offsetMs),durationMs});
 const look=(id,beat,target,offsetMs=2900,up=false)=>a.actions.push({actor:id,action:'lookAt',target,...at(beat,offsetMs),durationMs:600,...(up?{up:true}:{})});
 const shape=(id,x,y,kids,meaning,scale=1,anchors)=>{const o=a.object(id,x,y,kids,meaning,scale);if(anchors)o.visual.anchors=anchors;a.add(o);return o;};
 const rect=(x,y,w,h,fill,rx=6,night)=>{const r=n('rect',{x,y,width:w,height:h,rx,fill});return night?tint(r,night):r;};
 const fillPath=(d,fill,night)=>{const p=n('path',{d,fill});return night?tint(p,night):p;};
 const words=(value,x,y,size,color)=>text(value,x,y,size,color);
 // Rigged person: dynamic expressions, distinct coat per theme, optional mirror so they face left.
 const person=(id,role,x,emotion,{scale=.9,faceLeft=false,meaning}={})=>{
  const c=CAST[role];storyPerson(a,id,x,FLOOR,{identity:c.identity+'-'+emotion,coat:c.coat,scale});
  const o=a.objects.find(v=>v.id===id);
  const walk=node=>{for(const key of ['fill','stroke'])if(node.attrs?.[key]===c.coat)node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,[key]:c.night}};(node.children||[]).forEach(walk);};walk(o.visual);
  if(faceLeft)o.visual.transform={...o.visual.transform,scaleX:-(o.visual.transform?.scaleX||1)};
  // Book-owned 'curious' variant: a raised brow with a slight lopsided smile reads as interest, not sadness.
  const find=node=>node.id==='$asset.expression.curious.mouth'?node:(node.children||[]).map(find).find(Boolean);
  find(o.visual).attrs.d='M-8 21 Q1 26 9 18';
  o.meaning=meaning||o.meaning;return o;
 };
 const page=(id,x,y,w,h,kids,meaning)=>shape(id,x,y,[rect(-w/2,-h/2,w,h,PAGE,10,PAGE_NIGHT),...kids],meaning,1,{left:[-w/2,0],right:[w/2,0],top:[0,-h/2],bottom:[0,h/2]});
 // Library prop drawn flat: the catalogue's ground-shadow ellipse is removed.
 const prop=(id,asset,x,y,scale,color,meaning)=>{const visual=ASSETS[asset]('$asset',{color});visual.children=visual.children.filter(c=>c.attrs?.fill!=='$shadow');a.add({id,asset:'custom',x,y,scale,visual,meaning});return id;};
 const textLines=(x0,y0,widths,gap,color='#9aa8b4',width=6)=>widths.map((w,i)=>line(`M${x0} ${y0+i*gap}H${x0+w}`,color,width));

 if(index===0){
  // The author's own desk: a laptop produces the smoother version of his sharp question.
  shape('desk',600,465,[rect(-290,-12,580,22,'#a7744f',6,'#8f6a4e'),line('M-250 10V90M250 10V90','#5d4635',12)],'The author’s working desk on the shared floor.');
  prop('laptop','laptop',600,453,.62,'$blue','The AI editing tool the author used; an unbranded laptop.');
  person('author','author',165,'sad',{meaning:'The author, disappointed by what the polished edit removed.'});
  page('working-draft',440,215,260,190,[words('Original',0,-58,30,'#6c5a48'),words('How sharp',0,-10,40,CORAL),words('is the cost?',0,30,40,CORAL)],'The author’s original sentence asks a pointed question (schematic paraphrase).');
  // The sharp edge sits in its own band, 18 px below the quote’s descenders.
  shape('sharp-question',440,215,[line('M-92 70L-69 56L-46 70L-23 56L0 70L23 56L46 70L69 56L92 70',CORAL,5)],'The pointed edge of the original question.');
  shape('edit-arrow',600,215,[line('M-18 0H14M4 -11L16 0L4 11','$ink',5)],'The AI edit turns the original into the smoothed version.');
  page('smooth-line',760,215,260,190,[words('Smoothed',0,-58,30,'#6c5a48'),words('There are',0,-10,40,BLUE),words('trade-offs.',0,30,40,BLUE),line('M-92 76H92',BLUE,5)],'The AI’s smoother sentence: reasonable, but without the question.');
  shape('missing-edge',760,215,[(g=>(g.attrs['stroke-dasharray']='7 7',g.opacity=.55,g))(line('M-92 62L-69 50L-46 62L-23 50L0 62L23 50L46 62L69 50L92 62',CORAL,3))],'A faint ghost of the edge that the smoothing removed.');
  // The book in full: forest-green cover, the complete title and a row of small trees.
  shape('book',1060,FLOOR,[
   rect(-112,-300,224,300,'#2e5c4f',10,'#3d7464'),rect(-112,-300,18,300,'#1f4337',4,'#2c5a4c'),rect(-104,-6,214,8,'#f1e9d6',2),
   words('Can’t See',8,-228,36,'#f6efdc'),words('the Forest',8,-186,36,'#f6efdc'),words('for the Trees',8,-146,28,'#f6efdc'),
   ...[-56,-18,20,58].map((dx,i)=>fillPath(`M${dx} -96L${dx+17} -56H${dx-17}Z`,i===2?'#e3b65a':'#8fc4a5')),line('M-78 -50H96','#8fc4a5',3)
  ],'Can’t See the Forest for the Trees: the book this experience opens.',1,{left:[-112,-150],right:[112,-150],top:[0,-300],bottom:[0,0]});
  appear('edit-arrow',1,1600);appear('smooth-line',1,2200,900);appear('missing-edge',1,4200,900);
  express('author',1,'sad');gesture('author',1,'reflect',500,2600);look('author',1,'working-draft',3400,true);
  appear('book',2,300,900);express('author',2,'curious',200);gesture('author',2,'invite',900,2400);look('author',2,'book',3600);
  return a.finish('The author stands at his desk while an AI edit turns a pointed question into a reasonable sentence; the lost edge stays visible as a ghost. The complete book then enters the same workspace.');
 }
 if(index===1){
  // Sentence 1: the reader’s margin notes fade beside a polished page.
  person('author','author',165,'worried',{meaning:'The author rereads the polished passage with quiet unease.'});
  page('writing-surface',500,290,330,330,[words('Polished passage',0,-126,30,'#6c5a48')],'The smoothed manuscript page.');
  shape('continued-draft',500,290,textLines(-130,-80,[260,240,255,200,250,230,170],34,'#7f94a6',7),'Even, reasonable lines of the smoothed argument.');
  shape('retained-question',318,200,[words('?',0,14,46,CORAL)],'The author’s own question mark, kept in the margin.');
  const mark=(id,label,y,color,night,meaning)=>shape(id,760,y,[tint(line('M-82 0H-62',color,6),night),text(label,0,13,38,color)],meaning);
  // Margin tick marks point at the text; labels stand clear of the page edge.
  const doubt=mark('doubt-mark','doubt',200,CORAL,'#ee8f82','Doubt, noted in the margin.');
  const urgency=mark('urgency-mark','urgency',290,'#a8741a','#e7bb62','Urgency, noted in the margin.');
  const resp=mark('responsibility-mark','responsibility',380,'#6b4f8f','#c0a6e3','Responsibility, noted in the margin.');
  for(const o of [doubt,urgency,resp]){o.visual.children[1].attrs['text-anchor']='start';o.visual.children[1].attrs.x=-50;o.visual.children[1].themeAttrs={night:{fill:o.visual.children[0].themeAttrs.night.stroke}};}
  express('author',1,'worried');gesture('author',1,'reflect',500,2400);look('author',1,'writing-surface',3200);
  for(const [id,d] of [['doubt-mark',0],['urgency-mark',400],['responsibility-mark',800]])vanish(id,1,3600+d,2600);
  // Sentence 2: the same pattern in companies, research, politics, and the technology connecting them.
  for(const id of ['writing-surface','continued-draft','retained-question'])vanish(id,2,100,600);
  const domain=(id,asset,label,x,meaning,color)=>{const tag=(id==='proposal'?'companies':id)+'-label';prop(id,asset,x,300,.66,color,meaning);shape(tag,x,140,[text(label,0,0,38)],'Label: '+label);appear(id,2,700+(x-380)*2,700);appear(tag,2,900+(x-380)*2,600);};
  domain('proposal','factory','companies',380,'Companies: a factory standing for commercial organisations.','$coral');
  domain('research','microscope','research',600,'Research: a laboratory microscope.','$teal');
  domain('politics','courthouse','politics',820,'Politics: a public institution building.','$gold');
  // Civic building and router are redrawn with solid materials so they hold contrast on Paper.
  a.objects.find(o=>o.id==='politics').visual.children=[
   tint(n('path',{d:'M-78 -112L0 -150L78 -112Z',fill:'#6b4f8f'}),'#c0a6e3'),tint(rect(-74,-112,148,12,'#6b4f8f',2),'#c0a6e3'),
   ...[-54,-18,18,54].map(x=>tint(rect(x-9,-98,18,82,'#c69443',3),'#e2b664')),tint(rect(-82,-16,164,16,'#6b4f8f',3),'#c0a6e3')];
  a.objects.find(o=>o.id==='politics').scale=1;
  shape('unknown',600,520,[tint(line('M-36 -40V-88M36 -40V-88','#3f6f9c',6),'#86b4e0'),tint(rect(-66,-44,132,44,'#3f6f9c',10),'#86b4e0'),...[-36,-16,4].map(x=>n('circle',{cx:x,cy:-22,r:5,fill:'#e2b664'})),line('M22 -22H46','#e2b664',4)],'The technologies connecting them: a network router linking all three.');
  shape('unknown-label',800,500,[text('technology',0,0,38)],'Label: the connecting technologies.');
  // Links are drawn objects (not player connections) so the plan checker can track them.
  for(const x of [380,600,820]){const id='link-'+x,mx=(600+x)/2,my=375;shape(id,mx,my,[tint(line(`M${600-mx} 57L${x-mx} -57`,'#3f6f9c',5),'#86b4e0')],'Technology links this domain to the others.');appear(id,2,2600+(x-380)*2,700);}
  appear('unknown',2,2300,700);appear('unknown-label',2,2400,600);
  move('author',2,150,FLOOR,200,900);express('author',2,'determined',200);gesture('author',2,'explain',1200,2400);look('author',2,'research',3800);
  return a.finish('Margin notes for doubt, urgency and responsibility fade beside a polished page. The pattern then reappears in a factory, a laboratory and a public institution, joined by connecting technology.');
 }
 if(index===2){
  // One shared pipeline: each specialist tends a section; the joint between them leaks unnoticed.
  shape('pipeline',600,215,[
   tint(rect(-500,-16,470,32,'#5a9b8f',8),'#6fbfb0'),tint(rect(30,-16,470,32,'#c69443',8),'#e2b664'),
   tint(rect(-40,-24,22,48,'#58646e',4),'#9fb0bd'),tint(rect(18,-24,22,48,'#58646e',4),'#9fb0bd')
  ],'One shared pipeline: a teal section and a gold section meet at an unowned joint.',1,{left:[-500,0],right:[500,0],top:[0,-24],bottom:[0,24]});
  shape('gauge',330,215,[tint(line('M0 16V40','#58646e',6),'#9fb0bd'),n('circle',{cx:0,cy:76,r:36,fill:PAGE}),tint(n('circle',{cx:0,cy:76,r:36,fill:'none',stroke:'#58646e','stroke-width':5}),'#9fb0bd'),line('M0 76L20 58',CORAL,5),line('M-24 92H24','#9aa8b4',3)],'The planner’s pressure gauge on the teal section.');
  shape('upkeep-ledger',190,330,[rect(-34,-46,68,92,'#8b6a4b',6,'#a88563'),rect(-27,-34,54,74,PAGE,3,PAGE_NIGHT),line('M-17 -18L-11 -12L-3 -24M-17 4L-11 10L-3 -2M-17 26L-11 32L-3 20',BLUE,3),line('M3 -18H19M3 4H19M3 26H19','#9aa8b4',3)],'The planner’s upkeep ledger: every item in her own section is checked.');
  shape('valve',860,215,[tint(line('M0 -16V-44','#58646e',7),'#9fb0bd'),tint(n('circle',{cx:0,cy:-60,r:22,fill:'none',stroke:'#7b4b2a','stroke-width':7}),'#e2a77a'),tint(line('M-22 -60H22M0 -82V-38','#7b4b2a',4),'#e2a77a')],'The engineer’s valve wheel on the gold section.');
  person('planner','planner',260,'worried',{meaning:'The planner, focused on her own gauge and ledger.'});
  person('specialist-b','engineer',940,'determined',{faceLeft:true,meaning:'The engineer, intent on his own valve.'});
  const drops=[0,1,2].map(i=>shape('drop-'+i,600,250,[tint(fillPath('M0 -12Q9 2 0 8Q-9 2 0 -12Z','#3f7fb6'),'#7fb7e6')],'Water dripping from the unowned joint.'));
  drops.forEach((d,i)=>{appear(d.id,1,600+i*900,200);move(d.id,1,600,520,600+i*900,1500);});
  shape('unowned-consequence',600,540,[tint(n('ellipse',{cx:0,cy:0,rx:120,ry:12,fill:'#3f7fb6',opacity:.75}),'#7fb7e6')],'The consequence of the whole: a spreading puddle that belongs to neither section.');
  appear('unowned-consequence',1,1900,2800);
  express('planner',1,'worried');gesture('planner',1,'explain',500,2200);look('planner',1,'gauge',3000,true);
  express('specialist-b',1,'determined');gesture('specialist-b',1,'reflect',700,2200);
  // Sentence 2: the author arrives, notices the joint and asks where a person could still help.
  person('author','author',1260,'curious',{faceLeft:true,meaning:'The author, uncertain but still asking where people can make a useful difference.'});
  a.actions.push({actor:'author',action:'walkTo',x:1100,...at(2,100),durationMs:1500});
  shape('unpriced-option',600,330,[n('circle',{cx:0,cy:0,r:40,fill:PAGE}),tint(n('circle',{cx:0,cy:0,r:40,fill:'none',stroke:CORAL,'stroke-width':5}),'#ee8f82'),words('?',0,16,46,CORAL)],'An open question at the joint: where could someone still make a useful difference?');
  appear('unpriced-option',2,1800,800);
  express('author',2,'curious',200);gesture('author',2,'question',1700,2400);
  express('planner',2,'curious',2600);look('planner',2,'unpriced-option',3000);
  return a.finish('A planner checks her gauge and ledger and an engineer turns his valve, each on their own section of one pipeline, while the joint between them drips into an unowned puddle. The author arrives and raises an open question at that joint.');
 }
 // index 3: the conflict is still there, behind a smoother explanation.
 person('operator','operator',720,'worried',{meaning:'The operator, one side of a real conflict.'});
 person('resident','resident',960,'angry',{faceLeft:true,meaning:'An affected resident pressing the other side of the conflict.'});
 shape('polished-explanation',840,300,[
  fillPath('M-250 -150H250V150Q125 172 0 150Q-125 128 -250 150Z',PAGE),words('All systems align.',0,-60,40,BLUE),...textLines(-170,-6,[340,300,320],34,'#9aa8b4',6)
 ],'A smooth explanation drawn over the conflict.',1,{left:[-250,0],right:[250,0],top:[0,-150],bottom:[0,150]});
 a.objects.find(o=>o.id==='polished-explanation').visual.children[0].opacity=.9;
 a.objects.find(o=>o.id==='polished-explanation').visual.children[0].themeAttrs={night:{fill:PAGE_NIGHT}};
 Object.assign(a.objects.find(o=>o.id==='polished-explanation').visual.children[0].attrs,{stroke:'#cdbf9f','stroke-width':3});
 person('author','author',180,'curious',{meaning:'The author, inviting the reader to examine the edited manuscript.'});
 page('uncertainty-note',345,390,120,150,[...textLines(-40,-44,[80,70,80,50],22,'#9aa8b4',4),words('?',22,52,40,CORAL)],'The edited manuscript, held open for the reader’s question.');
 shape('review-route',470,300,[tint(n('circle',{cx:0,cy:0,r:34,fill:'none',stroke:'#4d3b2a','stroke-width':8}),'#d9c3a3'),tint(line('M24 -24L58 -58','#4d3b2a',11),'#d9c3a3')],'A magnifying glass: the reader’s route back to what changed.');
 express('operator',1,'worried');gesture('operator',1,'recoil',400,2000);
 express('resident',1,'angry');gesture('resident',1,'explain',400,2000);
 appear('polished-explanation',1,1100,1600);
 express('operator',1,'neutral',5000);express('resident',1,'tired',5000);
 express('author',1,'skeptical',400);look('author',1,'polished-explanation',3600);
 express('author',2,'curious',200);gesture('author',2,'invite',600,2400);
 move('polished-explanation',2,1520,300,700,1700);appear('review-route',2,300,600);move('review-route',2,840,262,2500,1500);
 express('resident',2,'angry',4200);express('operator',2,'worried',4200);
 return a.finish('An operator and an affected resident argue; a smooth explanation slides over them until the conflict is harder to notice. The author holds up the edited manuscript, and a magnifier lifts the polish so the conflict shows again.');
}

for(let i=0;i<scenes.length;i++)scenes[i].visual=build(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('artSha256',crypto.createHash('sha256').update(JSON.stringify(scenes.map(s=>({id:s.id,visual:s.visual})))).digest('hex'));
