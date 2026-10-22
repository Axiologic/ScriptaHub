// Canonical artwork generator (round-1 repair, 2026-10-22). Writes only each
// scene's `visual` and the additive `emotionalPlan.performance` notes into
// work/scenes.json; spoken lines, states and audio are never touched.
// Run from the repository root: node presentations/ai-adoption-beyond-the-slop/art.mjs
import fs from 'node:fs';import crypto from 'node:crypto';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {storyPerson} from '../../tools/shf/people-poses.mjs';

const file=new URL('work/scenes.json',import.meta.url);
const scenes=JSON.parse(fs.readFileSync(file));
if(scenes.length!==4)throw Error('Expected the four approved scenes.');

// Visual bible: one stable identity per role, distinct in every theme.
const CAST={
 worker:{identity:'person-11-neutral',coat:'#7a4a86',night:'#b68ac6',hairNight:'#6b5560',name:'Elena, the quiet first user (aubergine coat, long dark hair)'},
 colleague:{identity:'person-16-neutral',coat:'#2f7f86',night:'#62bcc2',hairNight:'#c08552',name:'Daniel, the curious colleague (teal coat, auburn bun)'},
 newcomer:{identity:'person-07-neutral',coat:'#c4603f',night:'#ee8f6c',hairNight:'#6b5a60',name:'Sam, a hesitant newcomer (coral coat, short hair)'},
 reviewer:{identity:'person-21-neutral',coat:'#b0821f',night:'#e0b752',hairNight:'#b6b9bb',name:'Eli, the senior reviewer (ochre coat, grey curls, glasses)'}
};
const F=528; // shared floor line: every foot, desk leg and table leg ends here
const C={ink:'#3a2f44',wood:'#a7744b',woodNight:'#c99a6c',woodDark:'#7f5636',slate:'#55697a',slateNight:'#8fa4b6',paper:'#fbf5e8',line:'#b9ad9c',edge:'#6d5f72',coral:'#d0684b',aub:'#7a4a86',aubNight:'#c79ad6',teal:'#2f7f86',rim:'#2d3540',rimNight:'#8c9aa8',screen:'#eaf2f3',gold:'#e0a72e'};

function art(index){
 const a=stageAuthor(),{n,path,text}=a;
 const night=(node,color)=>{const key=node.attrs.fill&&node.attrs.fill!=='none'?'fill':'stroke';node.themeAttrs={...node.themeAttrs,night:{...node.themeAttrs?.night,[key]:color}};return node;};
 const R=(x,y,w,h,fill,rx=4,stroke)=>n('rect',{x,y,width:w,height:h,rx,fill,...(stroke?{stroke,'stroke-width':2.5}:{})});
 const P=(d,fill,stroke)=>n('path',{d,fill,...(stroke?{stroke,'stroke-width':2.5,'stroke-linejoin':'round'}:{})});
 const actions=a.actions;
 const act=(actor,action,beat,offsetMs,extra={})=>actions.push({actor,action,beat,offsetMs,durationMs:extra.durationMs??700,...extra});
 const put=(id,x,y,kids,meaning,beat,offsetMs=250,scale=1)=>{a.add(a.object(id,x,y,kids,meaning,scale));if(beat)act(id,'appear',beat,offsetMs,{durationMs:800});};
 const spark=(cx,cy,r,fill,nightFill)=>{const s=r*.22;const node=P(`M${cx} ${cy-r}Q${cx+s} ${cy-s} ${cx+r} ${cy}Q${cx+s} ${cy+s} ${cx} ${cy+r}Q${cx-s} ${cy+s} ${cx-r} ${cy}Q${cx-s} ${cy-s} ${cx} ${cy-r}Z`,fill);return nightFill?night(node,nightFill):node;};
 const page=(x,y,w,h,lines=3)=>[R(x,y,w,h,C.paper,3,C.edge),...Array.from({length:lines},(_,i)=>path(`M${x+w*.15} ${y+h*(.3+i*.2)}H${x+w*(i===lines-1?.6:.85)}`,C.line,4))];
 const person=(id,role,x,{scale=.95,beat=1,offsetMs=0}={})=>{
  const c=CAST[role];storyPerson(a,id,x,F,{identity:c.identity,coat:c.coat,scale});
  const o=a.objects.find(v=>v.id===id);o.meaning=c.name;
  const hair=(c.identity==='person-21-neutral')?'#B6B9BB':null;
  const walk=v=>{for(const key of ['fill','stroke'])if(v.attrs?.[key]===c.coat)v.themeAttrs={...v.themeAttrs,night:{...v.themeAttrs?.night,[key]:c.night}};
   // Dark hair would vanish against the Night stage; lift it without changing identity.
   for(const key of ['fill'])if(v.attrs?.[key]&&/^#(28343C|39272D|563A2D|A76B3F)$/i.test(v.attrs[key])&&!hair)v.themeAttrs={...v.themeAttrs,night:{...v.themeAttrs?.night,[key]:c.hairNight}};
   for(const k of v.children||[])walk(k);};
  walk(o.visual);
  act(id,'appear',beat,offsetMs,{durationMs:800});
  return id;
 };
 const express=(id,beat,offsetMs,emotion)=>act(id,'character.express',beat,offsetMs,{emotion,durationMs:600});
 const gesture=(id,beat,offsetMs,g,durationMs=2600)=>act(id,'character.gesture',beat,offsetMs,{gesture:g,durationMs});
 const look=(id,beat,offsetMs,target,up=false)=>act(id,'lookAt',beat,offsetMs,{target,durationMs:500,...(up?{up:true}:{})});
 const walkTo=(id,beat,offsetMs,x,durationMs=1600)=>act(id,'walkTo',beat,offsetMs,{x,durationMs});
 const move=(id,beat,offsetMs,x,y,durationMs=900)=>act(id,'moveTo',beat,offsetMs,{x,y,durationMs});
 const hide=(id,beat,offsetMs)=>act(id,'disappear',beat,offsetMs,{durationMs:600});
 // A supported desk or table: top at y=-h, legs reach the floor line.
 const desk=(id,x,w,{h=128,beat=1,offsetMs=0,meaning='Work desk standing on the floor'}={})=>put(id,x,F,[
  night(R(-w/2,-h,w,16,C.wood,4),C.woodNight),night(R(-w/2+10,-h+16,w-20,22,C.woodDark,2),C.wood),
  night(path(`M${-w/2+22} ${-h+38}V-2M${w/2-22} ${-h+38}V-2`,C.woodDark,12),C.woodNight)],meaning,beat,offsetMs);
 // Monitor whose stand rests on the desk top at absolute y=topY.
 const monitor=(id,x,topY,kids,meaning,beat=1,offsetMs=0,w=230,h=150)=>put(id,x,topY,[
  night(R(-14,-36,28,36,C.rim,2),C.rimNight),night(R(-55,-8,110,10,C.rim,4),C.rimNight),
  night(R(-w/2,-36-h,w,h,C.rim,12),C.rimNight),R(-w/2+10,-26-h,w-20,h-20,C.screen,6),...kids],meaning,beat,offsetMs);
 const keyCard=(x,y,w=28,h=70)=>[R(x,y,w,h,C.paper,4,C.edge),n('circle',{cx:x+w/2,cy:y+18,r:7,fill:'none',stroke:C.aub,'stroke-width':4}),path(`M${x+w/2} ${y+25}V${y+50}M${x+w/2} ${y+40}H${x+w/2+7}`,C.aub,4)];

 if(index===0){
  // Sentence 1: an untouched crate of licences beside quiet, real work.
  put('licences',190,F,[
   ...[-100,-70,-40,-10,20,50,80].flatMap((x,i)=>keyCard(x,-178+(i%2)*8)),
   night(R(-135,-125,270,125,C.slate,8),C.slateNight),night(R(-135,-125,270,18,C.ink,4),C.slate),
   R(-130,-94,260,64,C.paper,6,C.edge),text('AI licences',0,-48,40,C.ink)],
   'A crate of purchased, still-sealed AI licence key cards',1,0);
  desk('workbench',690,380,{meaning:'Worker desk; legs stand on the floor'});
  monitor('computer',690,F-128,[R(-90,-166,124,112,C.paper,3,C.edge),spark(68,-140,16,C.aub,C.aubNight)],'Monitor showing a working draft with a small AI assistant mark',1,0);
  put('draft-lines',690,F-128,[path('M-60 -122H25M-60 -102H25M-60 -82H5',C.line,5)],'The draft fills in as the work proceeds',1,1800);
  person('worker','worker',455);
  express('worker',1,300,'determined');look('worker',1,700,'computer');gesture('worker',1,1500,'explain',2600);
  put('sheet-1',840,F-128,[R(-34,-8,68,8,C.paper,2,C.edge)],'First finished page from the assisted work',1,4300);
  // Sentence 2: work through the tool accumulates; a colleague notices.
  [2,3,4,5,6].forEach((k,i)=>put('sheet-'+k,840,F-128-9*(k-1),[R(-34,-8,68,8,C.paper,2,C.edge)],'Repeated work keeps landing on the pile: dependence grows',2,500+i*650));
  put('tried-label',550,190,[text('Tried',0,0,46,'$ink')],'Adoption starts as trying a tool',2,300);
  put('ladder-arrow',690,178,[path('M-60 0H52M36 -14L54 0L36 14','$ink',5)],'Direction of adoption from trying to relying',2,900);
  put('relied-label',865,190,[text('Relied on',0,0,46,'$ink')],'Adoption becomes reliance on a working habit',2,1500);
  person('colleague','colleague',1160,{beat:2,offsetMs:0});
  walkTo('colleague',2,100,1010,1700);express('colleague',2,300,'surprised');look('colleague',2,1900,'computer');express('colleague',2,3200,'happy');gesture('colleague',2,2500,'question',2600);
  look('worker',2,2700,'colleague');express('worker',2,2900,'happy');
  return {visual:a.finish('Sealed AI licences gather dust while Elena quietly finishes real work; pages pile up as trying becomes reliance, and colleague Daniel notices.'),
   performance:[{expression:'determined',gesture:'explain',gaze:'monitor',note:'Quiet, absorbed work; the unopened crate supplies the wry contrast.'},{expression:'happy',gesture:'none (colleague: question)',gaze:'colleague',note:'Clear interest: the growing pile shows dependence; Daniel is surprised, then pleased, and asks.'}]};
 }
 if(index===1){
  // People stand behind one long shared table; table drawn after them.
  person('worker','worker',250);
  express('worker',1,300,'curious');look('worker',1,700,'public');gesture('worker',1,2300,'reflect',3400);
  person('newcomer','newcomer',660,{beat:2,offsetMs:700});
  person('colleague','colleague',830,{beat:2,offsetMs:1100});
  desk('table',600,960,{h:118,meaning:'One shared worktable for all three ways AI can appear'});
  const top=F-118;
  put('public',420,top,[...keyCard(-50,-92,44,92),R(4,-104,58,104,C.paper,3,C.edge),path('M14 -84H50M14 -66H50M14 -48H40',C.line,4),night(n('circle',{cx:33,cy:-22,r:14,fill:'none',stroke:C.coral,'stroke-width':4}),C.coral)],'A purchased licence card with its paid receipt',1,300);
  put('tested',640,top,[P('M-22 -118H22V-80L52 -6Q55 0 48 0H-48Q-55 0 -52 -6L-22 -80Z',C.paper,C.edge),night(P('M-38 -30H38L48 -6Q50 0 44 0H-44Q-50 0 -48 -6Z',C.aub),C.aubNight),spark(-30,-150,14,C.gold),spark(18,-170,20,C.gold),spark(52,-136,11,C.gold)],'A clever one-off experiment: a flask with sparkles',1,2100);
  put('result',870,top,[R(-90,-140,180,140,C.paper,6,C.edge),night(R(-90,-140,180,30,C.teal,6),'#62bcc2'),...[0,1,2,3,4].flatMap(i=>[spark(-68+i*34,-80,11,C.aub,C.aub),spark(-68+i*34,-40,11,C.aub,C.aub)])],'A changed routine: the same AI-assisted step marked every working day of the week',1,3900);
  // Sentence 2: a first user helps others feel comfortable trying.
  hide('public',2,0);hide('tested',2,0);move('result',2,0,985,top,900);
  put('work',470,top,[night(R(-92,-112,184,112,C.rim,10),C.rimNight),R(-82,-102,164,92,C.screen,5),spark(0,-58,26,C.aub),night(P('M-112 0H112L100 -10H-100Z',C.rim),C.rimNight)],'An open laptop showing the AI assistant, offered for others to try',2,500);
  walkTo('worker',2,200,320,1200);express('worker',2,500,'happy');look('worker',2,900,'newcomer');gesture('worker',2,1500,'invite',2800);
  express('newcomer',2,800,'worried');look('newcomer',2,900,'work');gesture('newcomer',2,2700,'invite',2300);express('newcomer',2,3300,'relieved');
  express('colleague',2,1300,'curious');look('colleague',2,1500,'work');express('colleague',2,3600,'happy');
  return {visual:a.finish('Elena compares a bought licence, a sparkling experiment and a changed weekly routine; then she invites hesitant Sam and curious Daniel to try the tool at her laptop.'),
   performance:[{expression:'curious',gesture:'reflect',gaze:'licence, flask, routine in turn',note:'Thoughtful contrast between three different stories.'},{expression:'happy',gesture:'invite',gaze:'Sam',note:'Warm interest: Sam moves from worried to relieved as she reaches to try; Daniel watches with curiosity.'}]};
 }
 if(index===2){
  desk('desk',330,300,{meaning:'Elena’s own desk'});
  monitor('work',350,F-128,[...page(-80,-156,104,100,4)],'Monitor with a finished, polished document',1,0,200,140);
  put('ai-window',350,F-128,[R(30,-150,52,48,C.paper,5,C.edge),spark(56,-126,15,C.aub,C.aubNight)],'The private AI assistant window beside the draft',1,300);
  desk('review-table',850,300,{meaning:'Review table where the work will be judged'});
  person('worker','worker',115);
  express('worker',1,300,'determined');look('worker',1,600,'work');
  person('colleague','colleague',1180,{beat:1,offsetMs:400});
  walkTo('colleague',1,500,640,2000);express('colleague',1,700,'happy');look('colleague',1,2600,'worker');gesture('colleague',1,3200,'question',2300);
  look('worker',1,2700,'colleague');express('worker',1,2900,'worried');gesture('worker',1,3300,'recoil',2100);hide('ai-window',1,3200);
  // Sentence 2: polished output arrives faster than judgment can follow.
  walkTo('colleague',2,0,1260,1500);hide('colleague',2,900);
  put('ai-window-2',350,F-128,[R(30,-150,52,48,C.paper,5,C.edge),spark(56,-126,15,C.aub,C.aubNight)],'The assistant keeps generating polished pages',2,600);
  person('reviewer','reviewer',1065,{beat:2,offsetMs:1100});
  put('checked-page',925,F-128,[R(-40,-8,80,8,C.paper,2,C.edge)],'The single page the reviewer has examined so far',2,1300);
  put('loupe',925,F-128,[n('circle',{cx:0,cy:-40,r:26,fill:'none',stroke:'$ink','stroke-width':7}),path('M18 -21L36 -3','$ink',9)],'Magnifier: slow, careful professional judgment on one page',2,1500);
  for(let i=0;i<7;i++){const id='page-'+(i+1);put(id,350,F-230,[R(-34,-46,68,92,C.paper,3,C.edge),path('M-22 -26H22M-22 -10H22M-22 6H10',C.line,4),spark(20,30,9,C.gold)],'A polished AI-assisted page arriving at the review table',2,1500+i*480,1);move(id,2,1550+i*480,780,F-176-i*9,520);}
  express('reviewer',2,1700,'worried');look('reviewer',2,1900,'page-1');gesture('reviewer',2,2600,'reflect',3600);
  look('worker',2,1800,'reviewer');express('worker',2,3800,'surprised');
  return {visual:a.finish('Elena hides her AI window when Daniel asks about her work; then polished pages pour onto the review table while senior reviewer Eli, concerned, is still examining one page with a magnifier.'),
   performance:[{expression:'worried',gesture:'recoil',gaze:'Daniel',note:'Confidential curiosity: she relies on AI privately and closes the window when a colleague asks.'},{expression:'worried (reviewer)',gesture:'reflect',gaze:'growing pile',note:'Gentle concern: output outpaces the single page judgment has reached.'}]};
 }
 // index 3
 desk('desk',470,340,{meaning:'Elena’s desk with her own tasks'});
 const top=F-128;
 put('tasks',470,top,[
  R(-140,-56,76,54,C.paper,4,C.edge),path('M-140 -56L-102 -26L-64 -56',C.edge,3),
  R(-38,-70,76,70,C.paper,4,C.edge),night(path('M-26 -14V-30M-10 -14V-44M6 -14V-36M22 -14V-56',C.teal,8),'#62bcc2'),
  R(64,-66,70,66,C.paper,4,C.edge),path('M76 -48H122M76 -32H122M76 -16H104',C.line,4)],'Three of her own tasks: messages, figures, writing',1,0);
 put('ai-spark',330,top-120,[spark(0,0,24,C.aub,C.aubNight)],'Where does AI belong? The assistant mark hovers over one task, then another',1,600);
 move('ai-spark',1,1500,470,top-130,900);move('ai-spark',1,3000,605,top-120,900);
 put('practice',940,300,[night(R(-150,-120,300,170,C.coral,10),C.coral),spark(-60,-40,46,C.gold),spark(30,-70,22,C.paper),spark(80,-10,30,C.paper),
  night(P('M-132 -6L-112 -16L-64 -34V40L-112 22L-132 12Z',C.ink),C.ink),path('M-48 -22Q-36 3 -48 28M-34 -34Q-16 3 -34 40',C.paper,5),night(path('M-140 50V228M140 50V228',C.woodDark,8),C.woodNight)],'The loud, visible example: a bright showcase poster with a megaphone',1,200);
 person('learner','worker',165);
 express('learner',1,300,'neutral');look('learner',1,700,'ai-spark',true);gesture('learner',1,1600,'reflect',3200);
 // Sentence 2: open the book's stages; look beneath the loud example.
 hide('tasks',2,0);hide('ai-spark',2,0);
 put('stages-book',470,top,[night(P('M-150 -8Q-75 -30 0 -8Q75 -30 150 -8V-96Q75 -118 0 -96Q-75 -118 -150 -96Z',C.paper,C.edge),C.paper),path('M0 -96V-8',C.edge,3),
  night(path('M-126 -24H-96V-44H-66V-64H-36V-84',C.aub,7),C.aub),night(path('M36 -24H66V-44H96V-64H126V-84',C.aub,7),C.aub),spark(-120,-48,9,C.gold)],'The book open at its stages of adoption, drawn as rising steps',2,300);
 put('unaided',940,F-92,[night(R(-80,-6,160,14,C.wood,3),C.woodNight),night(path('M-66 8V88M66 8V88',C.woodDark,8),C.woodNight),
  ...[0,1,2,3].map(i=>R(-50,-14-i*9,100,8,C.paper,2,C.edge)),spark(54,-46,10,C.aub,C.aubNight)],'Quiet repeated work: an ordinary pile of everyday pages, left out of the showcase',2,1500);
 put('look-beneath',925,F-125,[n('circle',{cx:0,cy:0,r:32,fill:'none',stroke:'$ink','stroke-width':7}),path('M-23 23L-50 50','$ink',9)],'Magnifier inviting a look beneath the loud example',2,2400);
  express('learner',2,400,'happy');gesture('learner',2,800,'invite',2600);express('learner',2,3400,'inspired');look('learner',2,3500,'unaided');
 return {visual:a.finish('Elena weighs where AI belongs among her own tasks; the book opens at its stages of adoption while a magnifier finds the quiet everyday work beneath the loud showcase poster.'),
  performance:[{expression:'neutral',gesture:'reflect',gaze:'the hovering AI mark',note:'Personal reflection: deciding where AI belongs in her own work.'},{expression:'happy then inspired',gesture:'invite',gaze:'quiet work under the poster',note:'Inviting curiosity: start with the stages, then look past the loudest example.'}]};
}

for(let i=0;i<scenes.length;i++){
 const {visual,performance}=art(i);
 scenes[i].visual=visual;
 scenes[i].emotionalPlan.performance=performance;
 scenes[i].marketingVisualRevision={status:'round-1-repair-2026-10-22',plan:scenes[i].marketingVisualRevision?.plan};
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('artSha256',crypto.createHash('sha256').update(JSON.stringify(scenes.map(s=>({id:s.id,visual:s.visual})))).digest('hex'));
