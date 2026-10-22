// Authoritative artwork generator for the current two-sentence-per-scene film
// (round-3 repair after the independent visual review of art 54958ae5…, R2-1…R2-7).
// It rebuilds only scene.visual in work/scenes.json; spoken lines, emotional
// plans, sources and audio are untouched. Previous compositions are archived:
//   review-revision/scenes.before-round3-repair-54958ae5.json + art.before-round3-repair-54958ae5.mjs
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
// Measured scene durations of the current (unchanged) narration, used only to hold a
// raised arm (`reach` untilMs) to the end of its sentence. If the audio is re-rendered,
// the director throws on an out-of-scene key, so a stale value fails loudly.
const SCENE_MS=[21906,22678,15727,19227];
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
  // R2-1: the library's 'button' collar is a flat white bar laid over the scarf, and its
  // 'older' forehead crease runs across curly hair. Remove the bar (the scarf is the collar)
  // and keep only the cheek creases. Only the older resident carries either detail.
  o.visual.children=o.visual.children.filter(c=>!(c.type==='rect'&&c.attrs?.fill==='$page'&&c.attrs.y===-167));
  const crease=nodeOf(o,'head').children.find(c=>c.attrs?.d?.startsWith('M-15 -24 H13'));
  if(crease)crease.attrs.d='M-18 14 L-24 16.5 M21 14 L26 16.5';
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

 // ---- Round-3 rig helpers (project-local; shared rig code untouched) ----
 const skinOf=o=>nodeOf(o,'head').children[0].attrs.fill;
 const coatNight=role=>CAST[role].night;
 // Hand drawn at H, fingers along `deg` (figure-local degrees, 0 = forward, -90 = up).
 //  point: fist with an extended index finger; palm: open hand with four fingers and a thumb.
 const handParts=(H,deg,kind,skin,thumbSide=-1)=>{
  const r=deg*Math.PI/180,u=[Math.cos(r),Math.sin(r)],v=[-Math.sin(r),Math.cos(r)];
  const P=(a,b)=>[+(H[0]+u[0]*a+v[0]*b).toFixed(1),+(H[1]+u[1]*a+v[1]*b).toFixed(1)];
  const stroke=(pts,w)=>n('path',{d:'M'+pts.map(q=>q.join(' ')).join('L'),fill:'none',stroke:skin,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round'});
  if(kind==='point')return [n('circle',{cx:H[0],cy:H[1],r:10,fill:skin}),stroke([P(4,-3),P(27,-4)],7),stroke([P(2,thumbSide*7),P(9,thumbSide*10)],6)];
  return [n('ellipse',{cx:P(3,0)[0],cy:P(3,0)[1],rx:11,ry:10,fill:skin}),
   ...[-7,-2.4,2.4,7].map((k,i)=>stroke([P(8,k),P(i===0||i===3?20:23,k*1.25)],5)),
   stroke([P(0,thumbSide*8),P(9,thumbSide*17)],5.5)];
 };
 // Replace a rig arm (keeping its group id, so rotation/gesture/reach still work) with a
 // shoulder→elbow→hand polyline in the figure's own frame and an expressive hand.
 const customArm=(o,role,side,{elbow,hand,deg,kind='palm',thumbSide=-1})=>{
  const g=nodeOf(o,side),S=side==='armR'?[32,-156]:[-34,-157],pts=[S,...(elbow?[elbow]:[]),hand];
  const sleeve=n('path',{d:'M'+pts.map(q=>q.join(' ')).join('L'),fill:'none',stroke:CAST[role].coat,'stroke-width':20,'stroke-linecap':'round','stroke-linejoin':'round'});
  sleeve.themeAttrs={night:{stroke:coatNight(role)}};
  g.children=[sleeve,...handParts(hand,deg,kind,skinOf(o),thumbSide)];
  // keep generated ids unique inside the figure
  g.children.forEach((c,i)=>{c.id=g.id+'.r3-'+i;});
 };
 // `reach` rotates armR by -46° about the shoulder. Author the RAISED pose, then draw the
 // arm at rest (rotated +46°) so the reach lands exactly on that pose and holds it.
 const REACH=46,S_R=[32,-156];
 const rot=(q,t)=>{const r=t*Math.PI/180,dx=q[0]-S_R[0],dy=q[1]-S_R[1];return [+(S_R[0]+dx*Math.cos(r)-dy*Math.sin(r)).toFixed(1),+(S_R[1]+dx*Math.sin(r)+dy*Math.cos(r)).toFixed(1)];};
 const reachArm=(o,role,raised)=>customArm(o,role,'armR',{...raised,elbow:raised.elbow&&rot(raised.elbow,REACH),hand:rot(raised.hand,REACH),deg:raised.deg+REACH});
 const holdReach=(id,beat,offsetMs,durationMs,scene)=>a.actions.push({actor:id,action:'reach',...at(beat,offsetMs),durationMs,untilMs:SCENE_MS[scene]-1});
 // Project-local redraw of one dynamic expression state's brows/mouth (closed shapes only).
 const face=(o,state,{brows,mouth})=>{
  const m=nodeOf(o,'expression.'+state+'.mouth'),b=nodeOf(o,'expression.'+state+'.brows');
  if(mouth){m.attrs.d=mouth;m.attrs.fill='none';}if(brows)b.attrs.d=brows;
 };
 // Engaged, clear interest: gently raised level brows and a small closed smile.
 const INTEREST={brows:'M-17 -16 Q-11 -20 -5 -17 M7 -17 Q13 -20 20 -16',mouth:'M-8 20 Q0 26 8 20'};
 // Inviting challenge: level, focused brows and a slight confident (asymmetric) closed smile.
 const CONFIDENT={brows:'M-17 -13 L-5 -13 M7 -13 L20 -13',mouth:'M-9 21 Q1 26 10 19'};
 const page=(id,x,y,w,h,kids,meaning)=>shape(id,x,y,[rect(-w/2,-h/2,w,h,PAGE,10,PAGE_NIGHT),...kids],meaning,1,{left:[-w/2,0],right:[w/2,0],top:[0,-h/2],bottom:[0,h/2]});
 const textLines=(x0,y0,widths,gap,color=GREY,width=6)=>widths.map((w,i)=>line(`M${x0} ${y0+i*gap}H${x0+w}`,color,width));

 if(index===0){
  // The author stands at his own desk (behind it, so the tabletop occludes his legs),
  // one hand on the desk beside the laptop, looking up at what the edit did.
  // He stands behind his desk, hand resting by the laptop, looking up at what the edit did.
  // His arm is authored at rest; the sentence-2 reach raises it to an index finger on the book.
  const author1=person('author','author',250,'curious',{gaze:[2,-2.5],tilt:-6,meaning:'The author at his desk, reading what the AI edit made of his question.'});
  // Rest hand lands on the desk top (world y ≈ 443) just left of the laptop.
  reachArm(author1,'author',{elbow:[80,-186],hand:[124,-205],deg:-14,kind:'point'});
  face(author1,'relieved',INTEREST);
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
  // Sentence 2 (clear interest): the book enters; he walks along the desk and points to it
  // with his index finger (fingertip ≈ x 932 in the rendered frame, the cover edge is x 944),
  // a closed smile under gently raised brows.
  appear('book',2,200,900);express('author',2,'relieved',200);look('author',2,'book',300);
  a.actions.push({actor:'author',action:'walkTo',x:805,...at(2,300),durationMs:2400});
  holdReach('author',2,2700,1400,0);
  return a.finish('The author stands at his desk, hand beside the laptop, and looks up with disappointment as an AI edit turns his pointed question into a reasonable sentence; the original dims to an after-image. The complete book then appears; he turns, walks along the desk toward it and gestures to it.');
 }
 if(index===1){
  // Sentence 1: the author rereads a polished page; margin notes for doubt, urgency and responsibility fade.
  const author2=person('author','author',200,'worried',{gaze:[3,0],tilt:4,meaning:'The author rereads the polished passage with quiet unease; later he opens his palm toward the connecting network.'});
  // Relaxed hanging arm in sentence 1; the sentence-2 reach turns it into an open palm
  // presented toward the router hub (fingers aimed slightly down at it).
  reachArm(author2,'author',{elbow:[80,-150],hand:[124,-138],deg:12,kind:'palm',thumbSide:-1});
  face(author2,'relieved',INTEREST);
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
  // R2-3: on the Night stage (#06090F) the library's $woodDark (#3B3A39), $structural
  // (#0E202D) and $glass (#1D3944) parts vanish; give them light Night tokens (≥ 3:1).
  const NIGHT_PROP={'$woodDark':'#8a8a8a','$structural':'#9fb3c8','$glass':'#7fa9bb','$edge':'#6f8b9a'};
  const nightProp=node=>{for(const key of ['fill','stroke'])if(NIGHT_PROP[node.attrs?.[key]])node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,[key]:NIGHT_PROP[node.attrs[key]]}};(node.children||[]).forEach(nightProp);};
  const prop=(id,asset,x,y,scale,color,meaning)=>{const visual=ASSETS[asset]('$asset',{color});visual.children=visual.children.filter(c=>c.attrs?.fill!=='$shadow');nightProp(visual);a.add({id,asset:'custom',x,y,scale,visual,meaning});return id;};
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
  // R2-6: links end close together on the router's top edge (x 585/600/615, y 476) and the
  // antennas splay outward from the body's outer corners, so no link crosses a stem.
  // A segment-intersection assert below proves it for every link/stem pair.
  const ROUTER=[600,520],ANT=[[-62,-44,-86,-80],[62,-44,86,-80]],links=[[0,380,585],[1,600,600],[2,820,615]];
  const cross=(p1,p2,p3,p4)=>{const d=(a,b,c)=>(c[0]-a[0])*(b[1]-a[1])-(c[1]-a[1])*(b[0]-a[0]);const d1=d(p3,p4,p1),d2=d(p3,p4,p2),d3=d(p1,p2,p3),d4=d(p1,p2,p4);return d1*d2<0&&d3*d4<0;};
  for(const [i,x,end] of links){
   for(const [x1,y1,x2,y2] of ANT)if(cross([x,301],[end,476],[ROUTER[0]+x1,ROUTER[1]+y1],[ROUTER[0]+x2,ROUTER[1]+y2]))throw Error('scene-02 link '+x+' crosses a router antenna');
   const id='link-'+x,mx=(x+end)/2,my=389;shape(id,mx,my,[tint(line(`M${x-mx} -88L${end-mx} 87`,'#3f6f9c',5),'#86b4e0')],'Technology links this domain to the others.');appear(id,2,1700+i*300,700);
  }
  shape('unknown',ROUTER[0],ROUTER[1],[tint(line(ANT.map(([x1,y1,x2,y2])=>`M${x1} ${y1}L${x2} ${y2}`).join(''),'#3f6f9c',6),'#86b4e0'),tint(rect(-70,-44,140,44,'#3f6f9c',10),'#86b4e0'),...[-38,-18,2].map(x=>n('circle',{cx:x,cy:-22,r:5,fill:'#e2b664'})),line('M22 -22H46','#e2b664',4)],'The technologies connecting them: a network router linking all three.');
  shape('unknown-label',800,500,[text('technology',0,0,38)],'Label: the connecting technologies.');
  appear('unknown',2,1400,700);appear('unknown-label',2,1500,600);
  // Sentence 2 (engaged clarity): a small closed smile under raised brows, eyes on the hub,
  // and an open palm presented toward the router that links the three domains.
  move('author',2,170,FLOOR,200,900);express('author',2,'relieved',200);look('author',2,'unknown',400);
  holdReach('author',2,900,1400,1);
  return a.finish('The author rereads a polished page with unease while his own question mark stays in its margin and notes for doubt, urgency and responsibility fade. The pattern then reappears in a factory, a laboratory and a public institution, each linked to a router for the connecting technology, while the author presents the network with an open palm.');
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
 // index 3: the conflict is acted out; a smooth headline first covers the point where it
 // meets, then is lifted above the pair in sentence 2.
 // R2-4: the operator leans back with a bent elbow and an open palm raised at chest height;
 // the resident leans in with an extended index finger aimed at his chest.
 const operator=person('operator','operator',630,'worried',{gaze:[3,-.5],tilt:-7,lean:-8,meaning:'The operator, leaning back and defending his side of a real conflict with an open raised palm.'});
 customArm(operator,'operator','armR',{elbow:[60,-110],hand:[88,-140],deg:-68,kind:'palm',thumbSide:-1});
 const resident=person('resident','resident',1010,'angry',{faceLeft:true,gaze:[-4,.5],tilt:3,lean:6,meaning:'An affected resident leaning in and pointing her index finger, pressing the other side of the conflict.'});
 customArm(resident,'resident','armR',{elbow:[84,-160],hand:[124,-158],deg:6,kind:'point',thumbSide:1});
 // R2-7: opaque, unframed headline between the two heads; its lower edge covers the gap
 // and the tips of both gestures, so the conflict is literally smoothed over in sentence 1.
 shape('polished-explanation',812,318,[
  rect(-128,-88,256,176,PAGE,16,PAGE_NIGHT),words('All systems',0,-12,44,BLUE),words('align.',0,40,44,BLUE)
 ],'A smooth explanation laid over the point where the conflict meets.',1,{left:[-128,0],right:[128,0],top:[0,-88],bottom:[0,88]});
 const author4=person('author','author',165,'curious',{gaze:[3,-1],tilt:3,meaning:'The author, inviting the reader to examine the edited manuscript.'});
 // Rest in sentence 1; the sentence-2 reach presents an open palm toward the manuscript.
 reachArm(author4,'author',{elbow:[78,-150],hand:[118,-146],deg:-4,kind:'palm',thumbSide:-1});
 face(author4,'determined',CONFIDENT);
 page('uncertainty-note',360,400,150,190,[...textLines(-52,-60,[104,92,104,70,96],26,'#7f94a6',5),words('?',40,78,44,CORAL,'#a13628')],'The edited manuscript, held open for the reader’s question.');
 // Magnifier resting on the manuscript lines, handle toward the author’s inviting hand.
 shape('review-route',372,370,[tint(n('circle',{cx:0,cy:0,r:40,fill:'none',stroke:'#4d3b2a','stroke-width':8}),'#5a4632'),tint(line('M-29 29L-62 62','#4d3b2a',12),'#5a4632')],'A magnifying glass over the edited manuscript: the reader’s route back to what changed.');
 // Sentence 1: the headline is already settling over the confrontation by the first frame.
 appear('polished-explanation',1,250,900);
 a.actions.push({actor:'resident',action:'walkTo',x:990,...at(1,200),durationMs:900});
 look('author',1,'polished-explanation',400,true);
 // Sentence 2: the headline is lifted above the pair, exposing palm and finger again; the
 // author turns to the manuscript with a focused, confident smile and an open palm.
 move('polished-explanation',2,812,150,300,1500);
 look('author',2,'uncertainty-note',300);express('author',2,'determined',300);
 holdReach('author',2,500,1400,3);
 appear('review-route',2,900,700);
 return a.finish('An operator leaning back with a raised open palm and an affected resident leaning in with a pointing finger face each other; a smooth “All systems align.” card covers the point where their gestures meet. In the second sentence the card is lifted above them, and the author presents the edited manuscript with an open palm while a magnifier rests on it.');
}

for(let i=0;i<scenes.length;i++)scenes[i].visual=build(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('artSha256',crypto.createHash('sha256').update(JSON.stringify(scenes.map(s=>({id:s.id,visual:s.visual})))).digest('hex'));
import {buildBookFilm} from '../../tools/shf/build-book-film.mjs';
await buildBookFilm(new URL('.',import.meta.url).pathname);
