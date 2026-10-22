// Canonical artwork generator (round-4 repair, 2026-10-22). Writes only each
// scene's `visual`, the additive `emotionalPlan.performance` notes and
// `marketingVisualRevision.status` into work/scenes.json; spoken lines,
// emotional states, pauses and audio are never touched.
// Run from the repository root: node presentations/ai-adoption-beyond-the-slop/art.mjs
// (it does not build; see PRODUCTION.md for the staging build and QA commands).
import fs from 'node:fs';import crypto from 'node:crypto';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {storyPerson} from '../../tools/shf/people-poses.mjs';

const file=new URL('work/scenes.json',import.meta.url);
const scenes=JSON.parse(fs.readFileSync(file));
if(scenes.length!==4)throw Error('Expected the four approved scenes.');
// Measured scene lengths (qa/audio-timing.json, unchanged Qwen clips). Only
// held reaches use them (untilMs is scene-absolute); the compiler rejects a
// hold that would run past a scene if the audio were ever re-rendered.
const SCENE_MS=[17537,16347,17013,14968];

// Visual bible: one stable identity per role, distinct in every theme.
const CAST={
 worker:{identity:'person-11-neutral',coat:'#7a4a86',night:'#b68ac6',hairNight:'#6b5560',name:'Elena, the quiet first user (aubergine coat, long dark hair)'},
 colleague:{identity:'person-16-neutral',coat:'#2f7f86',night:'#62bcc2',hairNight:'#c08552',name:'Daniel, the curious colleague (teal coat, auburn bun)'},
 newcomer:{identity:'person-07-neutral',coat:'#c4603f',night:'#ee8f6c',hairNight:'#6b5a60',name:'Sam, a hesitant newcomer (coral coat, short hair)'},
 reviewer:{identity:'person-21-neutral',coat:'#b0821f',night:'#e0b752',hairNight:'#b6b9bb',name:'Eli, the senior reviewer (ochre coat, grey curls, glasses)'}
};
const F=528;   // shared floor line: every foot, desk leg and table leg ends here
const S=1.3;   // people scale: faces stay legible at 393 px phone width
const C={ink:'#3a2f44',wood:'#a7744b',woodNight:'#c99a6c',woodDark:'#7f5636',slate:'#55697a',slateNight:'#8fa4b6',paper:'#fbf5e8',line:'#b9ad9c',edge:'#6d5f72',coral:'#d0684b',aub:'#7a4a86',aubNight:'#c79ad6',teal:'#2f7f86',rim:'#2d3540',rimNight:'#8c9aa8',screen:'#eaf2f3',gold:'#e0a72e',tape:'#d9b45a'};
// Rig geometry (person asset, unscaled): shoulders and resting hands.
const SHOULDER={armL:[-34,-157],armR:[32,-156]},HAND={armL:[-46,-97],armR:[53,-108]};
// Where a hand lands after rotating an arm about its shoulder (stage units, relative to the feet).
// Person assets also scale x by their build (PEOPLE build: Elena and Sam 1.1, Eli .94, Daniel 1).
const BUILD={worker:1.1,newcomer:1.1,colleague:1,reviewer:.94};
// A point given in arm-local asset units, after rotating that arm about its shoulder, in stage units relative to the feet.
const armPoint=(role,side,deg,[px,py])=>{const [sx,sy]=SHOULDER[side],r=deg*Math.PI/180,dx=px-sx,dy=py-sy;return [(sx+dx*Math.cos(r)-dy*Math.sin(r))*S*BUILD[role],(sy+dx*Math.sin(r)+dy*Math.cos(r))*S];};
const handAt=(side,deg)=>{const [sx,sy]=SHOULDER[side],[hx,hy]=HAND[side],r=deg*Math.PI/180,dx=hx-sx,dy=hy-sy;return [(sx+dx*Math.cos(r)-dy*Math.sin(r))*S,(sy+dx*Math.sin(r)+dy*Math.cos(r))*S];};

function art(index){
 const a=stageAuthor(),{n,path,text}=a;
 const night=(node,color)=>{const key=node.attrs.fill&&node.attrs.fill!=='none'?'fill':'stroke';node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,[key]:color}};return node;};
 const R=(x,y,w,h,fill,rx=4,stroke)=>n('rect',{x,y,width:w,height:h,rx,fill,...(stroke?{stroke,'stroke-width':2.5}:{})});
 const P=(d,fill,stroke)=>n('path',{d,fill,...(stroke?{stroke,'stroke-width':2.5,'stroke-linejoin':'round'}:{})});
 const actions=a.actions;
 const act=(actor,action,beat,offsetMs,extra={})=>actions.push({actor,action,beat,offsetMs,durationMs:extra.durationMs??700,...extra});
 const put=(id,x,y,kids,meaning,beat,offsetMs=250,scale=1)=>{a.add(a.object(id,x,y,kids,meaning,scale));if(beat)act(id,'appear',beat,offsetMs,{durationMs:800});};
 const spark=(cx,cy,r,fill,nightFill)=>{const s=r*.22;const node=P(`M${cx} ${cy-r}Q${cx+s} ${cy-s} ${cx+r} ${cy}Q${cx+s} ${cy+s} ${cx} ${cy+r}Q${cx-s} ${cy+s} ${cx-r} ${cy}Q${cx-s} ${cy-s} ${cx} ${cy-r}Z`,fill);return nightFill?night(node,nightFill):node;};
 const sheet=(w=84)=>[R(-w/2,-9,w,9,C.paper,2,C.edge)];
 const find=(node,id)=>node.id===id?node:(node.children||[]).map(c=>find(c,id)).find(Boolean);
 // pose: static rest rotations (held for the whole scene; gestures compose on top and return here).
 const pose=(id,{armL,armR,head,pupils}={})=>{
  const v=a.objects.find(o=>o.id===id).visual;
  for(const [side,deg] of [['armL',armL],['armR',armR]])if(deg!==undefined){const g=find(v,'$asset.'+side);g.transform={...g.transform,rotate:deg};g.origin=SHOULDER[side];}
  if(head!==undefined){const g=find(v,'$asset.head');g.transform={...g.transform,rotate:head};g.origin=[0,30];}
  if(pupils){const g=find(v,'$asset.pupils');g.transform={...g.transform,x:pupils[0],y:pupils[1]};}
 };
 // A hand loupe held in one hand: a visible wooden handle runs from the grip at
 // an angle to a see-through lens (light, translucent fill in every theme, with
 // magnified text lines and a highlight). Drawn inside the arm group, under the
 // hand, so it moves with the arm.
 const holdLoupe=(id,side,dx,dy,r=19,armDeg=0,textLines=true)=>{
  const g=find(a.objects.find(o=>o.id===id).visual,'$asset.'+side),[hx,hy]=HAND[side];
  const len=Math.hypot(dx,dy),ux=dx/len,uy=dy/len,cx=hx+dx,cy=hy+dy;
  const lens=n('circle',{cx,cy,r,fill:'#d6edf2',opacity:.55,stroke:'none'});
  lens.themeAttrs={night:{fill:'#e4f4f8',opacity:.5}};
  const kids=[lens,
   ...(textLines?[
   // Magnified text lines stay level on screen: counter-rotate them by the arm's held angle.
   path((()=>{const t=-armDeg*Math.PI/180,q=(x,y)=>[cx+x*Math.cos(t)-y*Math.sin(t),cy+x*Math.sin(t)+y*Math.cos(t)].map(v=>+v.toFixed(2)).join(' ');return `M${q(-r*.5,-r*.12)}L${q(r*.5,-r*.12)}M${q(-r*.5,r*.28)}L${q(r*.3,r*.28)}`;})(),'$ink',2.5)]:[]),
   path(`M${cx-r*.62} ${cy-r*.2}A${r*.66} ${r*.66} 0 0 1 ${cx-r*.1} ${cy-r*.64}`,'#ffffff',2.5),
   night(path(`M${hx} ${hy}L${cx-ux*(r+3)} ${cy-uy*(r+3)}`,'#5b3b26',8),C.woodNight),
   n('circle',{cx,cy,r,fill:'none',stroke:'$ink','stroke-width':5})];
  g.children.splice(g.children.length-1,0,...kids); // keep the hand circle on top: the hand grips the handle
 };
 // Baked gaze bias: shifts the pupil circles inside the eye whites (6.6 x 8.5) for one
 // scene. lookAt then adds its own +/-4 (x) and -2.5 (up) on top, so the combined
 // gaze clearly points at the target without leaving the eye.
 const bakePupils=(id,dx,dy)=>{for(const c of find(a.objects.find(o=>o.id===id).visual,'$asset.pupils').children){c.attrs={...c.attrs,cx:c.attrs.cx+dx,cy:c.attrs.cy+dy};}};
 const person=(id,role,x,{beat=1,offsetMs=0}={})=>{
  const c=CAST[role];storyPerson(a,id,x,F,{identity:c.identity,coat:c.coat,scale:S});
  const o=a.objects.find(v=>v.id===id);o.meaning=c.name;
  // The reviewer asset carries a detached white chest tab; it read as a stray artifact.
  // Its pale salmon forehead and crow's-feet strokes ran past the face outline and
  // read as scratches; grey curls and glasses carry his age instead.
  if(role==='reviewer'){o.visual.children=o.visual.children.filter(k=>k.id!=='$asset.detail.n3');const head=find(o.visual,'$asset.head');head.children=head.children.filter(k=>k.id!=='$asset.detail.n2');}
  const hair=(c.identity==='person-21-neutral')?'#B6B9BB':null;
  const walk=v=>{for(const key of ['fill','stroke'])if(v.attrs?.[key]===c.coat)v.themeAttrs={...v.themeAttrs,night:{...v.themeAttrs?.night,[key]:c.night}};
   // Dark hair would vanish against the Night stage; lift it without changing identity.
   if(v.attrs?.fill&&/^#(28343C|39272D|563A2D|A76B3F)$/i.test(v.attrs.fill)&&!hair)v.themeAttrs={...v.themeAttrs,night:{...v.themeAttrs?.night,fill:c.hairNight}};
   for(const k of v.children||[])walk(k);};
  walk(o.visual);
  act(id,'appear',beat,offsetMs,{durationMs:800});
  return id;
 };
 // Expressions switch with a hard 140 ms cut, never a long cross-fade (two faces at once).
 const express=(id,beat,offsetMs,emotion)=>act(id,'character.express',beat,offsetMs,{emotion,durationMs:140});
 const gesture=(id,beat,offsetMs,g,durationMs=2600)=>act(id,'character.gesture',beat,offsetMs,{gesture:g,durationMs});
 const look=(id,beat,offsetMs,target,up=false)=>act(id,'lookAt',beat,offsetMs,{target,durationMs:450,...(up?{up:true}:{})});
 const walkTo=(id,beat,offsetMs,x,durationMs=1600)=>act(id,'walkTo',beat,offsetMs,{x,durationMs});
 const move=(id,beat,offsetMs,x,y,durationMs=900)=>act(id,'moveTo',beat,offsetMs,{x,y,durationMs});
 const hide=(id,beat,offsetMs,durationMs=600)=>act(id,'disappear',beat,offsetMs,{durationMs});
 const reachHold=(id,beat,offsetMs,untilMs,durationMs=1100)=>act(id,'reach',beat,offsetMs,{durationMs,untilMs});
 // A supported desk or table: top at y=-h, legs reach the floor line.
 const desk=(id,x,w,{h=140,beat=1,offsetMs=0,meaning='Work desk standing on the floor'}={})=>put(id,x,F,[
  night(R(-w/2,-h,w,16,C.wood,4),C.woodNight),night(R(-w/2+10,-h+16,w-20,20,C.woodDark,2),C.wood),
  night(path(`M${-w/2+22} ${-h+36}V-2M${w/2-22} ${-h+36}V-2`,C.woodDark,12),C.woodNight)],meaning,beat,offsetMs);
 // Monitor whose stand rests on the desk top at absolute y=topY.
 const monitor=(id,x,topY,kids,meaning,beat=1,offsetMs=0,w=240,h=160)=>put(id,x,topY,[
  night(R(-14,-36,28,36,C.rim,2),C.rimNight),night(R(-55,-8,110,10,C.rim,4),C.rimNight),
  night(R(-w/2,-36-h,w,h,C.rim,12),C.rimNight),R(-w/2+10,-26-h,w-20,h-20,C.screen,6),...kids],meaning,beat,offsetMs);
 const keyboard=(id,x,topY,w=110)=>put(id,x,topY,[night(R(-w/2,-9,w,9,C.rim,3),C.rimNight),path(`M${-w/2+10} -5H${w/2-10}`,C.screen,2)],'Keyboard on the desk under the worker’s hand');
 const keyCard=(x,y,w=28,h=70)=>[R(x,y,w,h,C.paper,4,C.edge),n('circle',{cx:x+w/2,cy:y+18,r:7,fill:'none',stroke:C.aub,'stroke-width':4}),path(`M${x+w/2} ${y+25}V${y+50}M${x+w/2} ${y+40}H${x+w/2+7}`,C.aub,4)];

 if(index===0){
  // Sentence 1: a sealed crate of licences beside quiet, real, AI-assisted work.
  put('licences',150,F,[
   night(R(-115,-150,230,150,C.slate,8),C.slateNight),night(R(-125,-170,250,26,C.ink,5),C.slate),
   night(path('M-60 -170V0M60 -170V0',C.tape,14),C.tape),
   R(-98,-112,196,60,C.paper,6,C.edge),text('AI licenses',0,-70,38,C.ink)],
   'A sealed, unopened crate of purchased AI licenses, taped shut',1,0);
  desk('workbench',615,510,{meaning:'Worker desk; legs stand on the floor'});
  monitor('computer',540,F-140,[R(-96,-176,128,120,C.paper,3,C.edge),spark(70,-150,17,C.aub,C.aubNight)],'Monitor showing a working draft with a small AI assistant mark',1,0);
  put('draft-lines',540,F-140,[path('M-78 -150H16M-78 -128H16M-78 -106H-6M-78 -84H10',C.line,5)],'The draft fills in as the work proceeds',1,1800);
  const [kx]=handAt('armR',-25);
  keyboard('keys',330+kx,F-140);
  person('worker','worker',330);pose('worker',{armR:-25});
  express('worker',1,200,'neutral');look('worker',1,600,'computer');
  const PX=725; // the growing pile of finished pages, right of the monitor
  put('sheet-1',PX,F-140,sheet(),'First finished page from the assisted work',1,4300);
  // Sentence 2: work through the tool accumulates beside her; a colleague notices.
  [2,3,4,5,6,7].forEach((k,i)=>put('sheet-'+k,PX,F-140-10*(k-1),sheet(),'Repeated work keeps landing on the pile: dependence grows',2,400+i*520));
  // Tags are 44 stage units so they stay readable at 320 px.
  put('tried-label',PX,F-140,[path('M48 -6H60',C.edge,3),n('text',{x:66,y:6,'font-size':44,'font-weight':700,'text-anchor':'start',fill:'$ink'},'Tried')],'The first page: adoption starts as trying a tool',2,300);
  put('ladder-arrow',PX,F-140,[path('M56 -26V-62M46 -50L56 -64L66 -50','$ink',4)],'The pile rises from trying toward reliance',2,1300);
  put('relied-label',PX,F-140,[path('M48 -70H60',C.edge,3),n('text',{x:66,y:-66,'font-size':44,'font-weight':700,'text-anchor':'start',fill:'$ink'},'Relied on')],'The top of the pile: adoption has become reliance on a working habit',2,2400);
  // Daniel arrives surprised and holds it past the line's midpoint (3238 ms), looking
  // left at the pile and Elena; at about 66% he switches to pleased with a hard cut.
  person('colleague','colleague',1290,{beat:2,offsetMs:0});
  walkTo('colleague',2,100,1105,1500);express('colleague',2,300,'surprised');look('colleague',2,1500,'worker');bakePupils('colleague',-1.5,1);
  // A surprised step back (recoil: hands drawn in, head raised toward Elena) peaks over the midpoint.
  gesture('colleague',2,1700,'recoil',2600);express('colleague',2,4300,'happy');
  look('worker',2,2400,'colleague');express('worker',2,2700,'happy');
  return {visual:a.finish('Sealed AI licenses sit taped shut while Elena quietly types her real work; finished pages pile up from “Tried” to “Relied on”, and colleague Daniel notices.'),
   performance:[{expression:'neutral (calm, absorbed)',gesture:'hand on the keyboard (held pose)',gaze:'monitor',note:'Quiet, absorbed work; the sealed crate supplies the wry contrast.'},{expression:'happy (Elena); Daniel surprised until about 66%, then a hard cut to happy',gesture:'hands stay on the keyboard (colleague: a small surprised step back, head raised toward Elena)',gaze:'Elena: colleague; Daniel: left, to the pile and Elena',note:'Clear interest: the pile rises from Tried to Relied on; Daniel notices with surprise, asks, then is pleased.'}]};
 }
 if(index===1){
  // One long shared table, drawn before the people so every hand stays visible.
  desk('table',700,940,{h:135,meaning:'One shared worktable for all three ways AI can appear'});
  const top=F-135;
  put('public',420,top,[...keyCard(-62,-110,52,110),R(4,-124,70,124,C.paper,3,C.edge),path('M16 -100H62M16 -80H62M16 -60H50',C.line,5),night(n('circle',{cx:39,cy:-28,r:16,fill:'none',stroke:C.coral,'stroke-width':5}),C.coral)],'A purchased license card with its paid receipt',1,300);
  put('tested',650,top,[P('M-24 -130H24V-88L58 -7Q61 0 53 0H-53Q-61 0 -58 -7L-24 -88Z',C.paper,C.edge),night(P('M-42 -34H42L53 -7Q55 0 48 0H-48Q-55 0 -53 -7Z',C.aub),C.aubNight),spark(-34,-164,15,C.gold),spark(20,-186,22,C.gold),spark(58,-150,12,C.gold)],'A clever one-off experiment: a flask with sparkles',1,2100);
  put('result',890,top,[R(-82,-150,164,150,C.paper,6,C.edge),night(R(-82,-150,164,32,C.teal,6),'#62bcc2'),...[0,1,2,3,4].flatMap(i=>[spark(-62+i*31,-86,11,C.aub,C.aubNight),spark(-62+i*31,-42,11,C.aub,C.aubNight)])],'A changed routine: the same AI-assisted step marked every working day of the week',1,3900);
  // The laptop of sentence 2 is declared before the people so hands stay in front of it.
  put('work',500,top,[night(R(-100,-120,200,120,C.rim,10),C.rimNight),R(-90,-110,180,100,C.screen,5),spark(0,-60,28,C.aub,C.aubNight),night(P('M-122 0H122L108 -10H-108Z',C.rim),C.rimNight)],'An open laptop showing the AI assistant, offered for others to try',2,300);
  person('worker','worker',150);
  express('worker',1,200,'skeptical');look('worker',1,500,'public');
  gesture('worker',1,400,'explain',1600);gesture('worker',1,2200,'explain',1600);gesture('worker',1,4000,'explain',1700);
  // Sentence 2: a first user helps others feel comfortable trying.
  hide('public',2,0);hide('tested',2,0);move('result',2,0,1088,top,900);
  // Elena stops at x=220, so her open hand, raised level with her shoulder (about x=340, y=330; peak 2130-3210 ms, over the midpoint at 2517 ms), reaches toward Sam clearly above the table and left of the laptop.
  walkTo('worker',2,0,220,700);express('worker',2,300,'happy');look('worker',2,900,'newcomer');gesture('worker',2,400,'explain',3600);
  // Sam fades in only after the flask and license have gone (600 ms), so he is never a ghost over them.
  person('newcomer','newcomer',820,{beat:2,offsetMs:650});pose('newcomer',{armL:30});
  express('newcomer',2,650,'worried');walkTo('newcomer',2,700,675,1000);gesture('newcomer',2,750,'recoil',1450);
  express('newcomer',2,2100,'relieved');look('newcomer',2,2150,'work');
  // Daniel fades in only after Sam has finished walking (1700 ms), so he never overlaps Sam; he is opaque by about 2250 ms.
  person('colleague','colleague',895,{beat:2,offsetMs:1800});
  // 'curious' reads as a frown at phone size; raised brows and an open mouth read as interest.
  express('colleague',2,1800,'surprised');look('colleague',2,2000,'work');express('colleague',2,3900,'happy');
  return {visual:a.finish('Elena compares a bought license, a sparkling experiment and a changed weekly routine; then she invites hesitant Sam, whose hand settles on her laptop, while curious Daniel looks on.'),
   performance:[{expression:'skeptical (wry, weighing)',gesture:'explain toward each object as it appears',gaze:'license, flask, routine',note:'Thoughtful contrast between three different stories on one table.'},{expression:'happy',gesture:'open hand raised to shoulder height toward Sam, above the table and clear of the laptop (held through the midpoint)',gaze:'Sam',note:'Warm interest: Sam hesitates (worried, recoil), then his hand settles on the laptop and he relaxes; Daniel watches the laptop with open interest (raised brows), then smiles.'}]};
 }
 if(index===2){
  // Elena stands at the left end of her desk with the monitor to her right, so
  // Daniel can approach from the left and the pages leave from the monitor's
  // free right edge on a short, low path to the review table; nobody is crossed.
  desk('desk',470,480,{meaning:'Elena’s own desk'});
  // Pages of the second sentence start hidden behind the monitor (drawn before it).
  // Flights pause around the line's midpoint (3117 ms), so a landed page shows there.
  const FLIGHTS=[1100,1500,1900,2300,3500,3950,4400];
  FLIGHTS.forEach((t,i)=>{const id='page-'+(i+1);put(id,620,F-220,[R(-30,-40,60,80,C.paper,3,C.edge),path('M-18 -22H18M-18 -8H18M-18 6H8',C.line,4),spark(16,26,8,C.gold)],'A polished AI-assisted page leaving the monitor for the review table',null);
   act(id,'appear',2,t,{durationMs:200});move(id,2,t+80,822,F-178-i*10,480);hide(id,2,t+520,160);});
  monitor('work',580,F-140,[R(-104,-176,120,128,C.paper,3,C.edge),path('M-90 -150H0M-90 -130H0M-90 -110H-20M-90 -90H0',C.line,4)],'Monitor with a finished, polished document',1,0);
  put('ai-window',580,F-140,[R(30,-170,64,56,C.paper,5,C.edge),spark(62,-142,17,C.aub,C.aubNight)],'The private AI assistant window beside the draft',1,300);
  const [kx]=handAt('armR',-25);
  keyboard('keys',360+kx,F-140,90);
  person('worker','worker',360);pose('worker',{armR:-25});
  // Pupils carry an intrinsic +2 right offset; this left/down bias makes her look at Daniel read as an averted glance down-left.
  bakePupils('worker',-2,1.5);
  express('worker',1,200,'curious');look('worker',1,400,'work');
  // Daniel stops at x=150 so his outstretched left hand stays inside the frame at 393 px.
  person('colleague','colleague',-110,{beat:1,offsetMs:0});
  walkTo('colleague',1,100,150,1300);express('colleague',1,300,'happy');look('colleague',1,1300,'worker');gesture('colleague',1,1450,'question',2600);
  // A gesture returns the head to its start value, so the brief recoil ends first (1550-2350 ms)
  // and only then does she turn to Daniel; head and eyes stay on him through the midpoint (2839 ms) and beyond.
  express('worker',1,1550,'worried');gesture('worker',1,1550,'recoil',800);hide('ai-window',1,1650,500);look('worker',1,2350,'colleague');
  // Sentence 2: polished output arrives faster than judgment can follow.
  walkTo('colleague',2,0,-170,900);hide('colleague',2,500,350);
  put('ai-window-2',580,F-140,[R(30,-170,64,56,C.paper,5,C.edge),spark(62,-142,17,C.aub,C.aubNight)],'The assistant keeps generating polished pages',2,300);
  desk('review-table',890,240,{h:130,beat:2,offsetMs:600,meaning:'Review table where the work will be judged'});
  FLIGHTS.forEach((t,i)=>{const id='pile-'+(i+1);put(id,822,F-130-i*10,sheet(),'The page lands flat: the unchecked pile grows',null);act(id,'appear',2,t+540,{durationMs:200});});
  // The checked page lies flat on the table, drawn in slight perspective and larger than a pile sheet.
  put('checked-page',942,F-130,[P('M-62 0H62L52 -24H-52Z',C.paper,C.edge),path('M-40 -7H36M-36 -16H30',C.line,3)],'The single page the reviewer is examining, lying flat on the table',2,900);
  // Eli holds a handled loupe at an angle, its lens hovering over that page.
  person('reviewer','reviewer',1105,{beat:2,offsetMs:900});pose('reviewer',{armL:55,head:-12,pupils:[-4,3]});holdLoupe('reviewer','armL',-17,48,21,55);
  express('reviewer',2,900,'worried');
  look('worker',2,1300,'reviewer');
  return {visual:a.finish('Elena closes her private AI window as soon as Daniel asks about her work; then polished pages leave her monitor and land on the review table while senior reviewer Eli, concerned, examines a single page through a hand loupe.'),
   performance:[{expression:'curious, then worried',gesture:'recoil while the window closes',gaze:'monitor, then Daniel',note:'Confidential curiosity: she relies on AI privately and closes the window the moment a colleague asks.'},{expression:'worried (reviewer and Elena)',gesture:'reviewer holds the loupe by its handle over one page, head and gaze down (held pose)',gaze:'Eli: the checked page; Elena: Eli',note:'Gentle concern: output keeps arriving while judgment has reached only one page.'}]};
 }
 // index 3
 // Elena stands right of her desk (x=620), between the desk and the quiet pile, so
 // she never walks across the desk or the stages book. In sentence 1 the AI mark hovers
 // just above her tasks, slightly below eye height to her left; her head tilt, the
 // open-hands question and her down-biased pupils all point at it. In sentence 2 the
 // book opens on the desk to her left while the stages are named, then she takes a
 // short walk right to the pile beneath the wall-hung showcase poster.
 desk('desk',330,340,{meaning:'Elena’s desk with her own tasks'});
 const top=F-140;
 put('tasks',330,top,[
  R(-150,-60,84,58,C.paper,4,C.edge),path('M-150 -60L-108 -28L-66 -60',C.edge,3),
  R(-42,-78,84,76,C.paper,4,C.edge),night(path('M-28 -16V-34M-10 -16V-50M8 -16V-40M26 -16V-62',C.teal,9),'#62bcc2'),
  R(68,-72,78,70,C.paper,4,C.edge),path('M80 -52H134M80 -34H134M80 -16H112',C.line,4)],'Three of her own tasks: messages, figures, writing',1,0);
 put('ai-spark',222,top-112,[spark(0,0,24,C.aub,C.aubNight)],'Where does AI belong? The assistant mark hovers over one task, then another',1,100);
 move('ai-spark',1,1400,330,top-128,900);move('ai-spark',1,2900,438,top-118,900);
 // The showcase poster hangs on the wall (two pins, no legs), high and right, clear of Elena.
 put('practice',1060,210,[night(R(-150,-120,300,170,C.coral,10),C.coral),spark(-60,-40,46,C.gold),spark(30,-70,22,C.paper),spark(80,-10,30,C.paper),
  night(P('M-132 -6L-112 -16L-64 -34V40L-112 22L-132 12Z',C.ink),C.ink),path('M-48 -22Q-36 3 -48 28M-34 -34Q-16 3 -34 40',C.paper,5),
  night(n('circle',{cx:-128,cy:-106,r:7,fill:C.ink}),C.slate),night(n('circle',{cx:128,cy:-106,r:7,fill:C.ink}),C.slate)],'The loud, visible example: a bright showcase poster with a megaphone, pinned to the wall',1,200,.8);
 put('unaided',1000,F-80,[night(R(-85,-6,170,14,C.wood,3),C.woodNight),night(path('M-70 8V76M70 8V76',C.woodDark,8),C.woodNight),
  ...[0,1,2,3].map(i=>R(-52,-14-i*9,104,8,C.paper,2,C.edge)),spark(58,-46,10,C.aub,C.aubNight)],'Quiet repeated work: an ordinary pile of everyday pages on a low table beneath the showcase',1,800);
 // The stages book is declared before Elena, so she is always drawn in front of it.
 put('stages-book',330,top,[night(P('M-160 -8Q-80 -30 0 -8Q80 -30 160 -8V-104Q80 -126 0 -104Q-80 -126 -160 -104Z',C.paper,C.edge),C.paper),path('M0 -104V-8',C.edge,3),
  night(path('M-136 -24H-104V-36H-72V-48H-40V-60H-8V-68H8V-76H40V-84H72V-92H104V-100H130',C.aub,7),C.aub),n('circle',{cx:-136,cy:-24,r:6,fill:C.gold}),spark(136,-102,11,C.gold)],'The book open at its stages of adoption: one path rising step by step across both pages',2,200);
 const EX=620,PX=860,HOLD=-46;
 person('learner','worker',EX);
 // Eli's handled loupe, held in her right hand. Its lens shows only a curved highlight while
 // the arm moves (no strokes that could rotate into a diagonal); level magnified text lines
 // appear inside the lens only while the arm is held at its reach angle over the pile.
 const LOUPE=[-12,50,18];holdLoupe('learner','armR',LOUPE[0],LOUPE[1],LOUPE[2],0,false);
 // Pupils carry a downward bias for the whole scene (no upward look is used), so she looks
 // slightly down at the mark over her tasks and down at the book and the pile.
 bakePupils('learner',-1,3.5);
 express('learner',1,200,'neutral');look('learner',1,200,'ai-spark');gesture('learner',1,700,'question',3000);
 // Sentence 2: the book opens at its stages while she looks at it; then a short walk to the quiet pile.
 hide('tasks',2,0);hide('ai-spark',2,0);
 look('learner',2,400,'stages-book');express('learner',2,400,'happy');
 walkTo('learner',2,1500,PX,700);look('learner',2,1500,'unaided');
 reachHold('learner',2,2000,SCENE_MS[3]-500,900);express('learner',2,3400,'inspired');
 {const [hx,hy]=HAND.armR,[lx,ly]=armPoint('worker','armR',HOLD,[hx+LOUPE[0],hy+LOUPE[1]]),r=LOUPE[2]*S;
  put('loupe-text',PX+lx,F+ly,[path(`M${-r*.5} ${-r*.12}H${r*.5}M${-r*.5} ${r*.28}H${r*.3}`,'$ink',3)],'Magnified lines of the quiet everyday work, level inside the held lens',null);
  act('loupe-text','appear',2,2420,{durationMs:200});hide('loupe-text',2,SCENE_MS[3]-500-6699 /* 6699 ms: measured start of scene 4, sentence 2; the lines stay fully visible until the hold ends */,150);}
 return {visual:a.finish('Elena weighs where AI belongs among her own tasks; the book opens at its rising stages of adoption, and she carries her magnifier to the quiet everyday pile beneath the loud showcase poster on the wall.'),
  performance:[{expression:'neutral (reflective)',gesture:'question (open hands), held through the midpoint',gaze:'left and slightly down, at the AI mark hovering just above her tasks; head tilted toward it',note:'Personal reflection: deciding where AI belongs in her own work.'},{expression:'happy, then inspired (hard cut at about 68%)',gesture:'looks at the open stages book beside her, then takes a short walk to the quiet pile and holds the handled loupe over it',gaze:'down-left to the stages book, then down-right to the quiet pile from arrival to the end',note:'Inviting curiosity: start with the stages, then look past the loudest example.'}]};
}
for(let i=0;i<scenes.length;i++){
 const {visual,performance}=art(i);
 scenes[i].visual=visual;
 scenes[i].emotionalPlan.performance=performance;
 scenes[i].marketingVisualRevision={status:'round-4-repair-2026-10-22',plan:scenes[i].marketingVisualRevision?.plan};
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('artSha256',crypto.createHash('sha256').update(JSON.stringify(scenes.map(s=>({id:s.id,visual:s.visual})))).digest('hex'));
