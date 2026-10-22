// Book-owned staging for "Enthusiasm: The Missing Energy of a Successful Civilization".
// Rewrites only scene.visual in work/scenes.json; the reviewed spoken lines are never touched.
// Identity (work/visual-bible.json): a current runs from a small present-world terminal to a larger
// possible future, while sparks of stimulation flicker without joining it. Qualitative staging only.
import fs from 'node:fs';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
const file=new URL('./work/scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file,'utf8'));
// Cover palette plus quiet derived tones; dark fills receive a Night variant.
const C={amber:'#f0a12b',teal:'#2f8f9d',ink:'#1d2433',deep:'#1f6470',pale:'#f8cf86',cream:'#fff6e3',mist:'#9ccfd6',slate:'#55607a',rust:'#c8622d',nightInk:'#c9d3dc'};
function art(index){
 const a=stageAuthor(),{n,path,text,dot,tint}=a;
 const R=(x,y,w,h,fill,rx=4)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const F=(d,fill)=>n('path',{d,fill});
 const dash=(d,w=4)=>n('path',{d,fill:'none',stroke:'$ink','stroke-width':w,'stroke-dasharray':'9 9','stroke-linecap':'round',opacity:.5});
 const dark=(node)=>tint(node,C.nightInk);
 const appear=(id,beat,offsetMs=250,durationMs=700)=>a.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs});
 const hide=(id,beat,offsetMs=250,durationMs=500)=>a.actions.push({actor:id,action:'disappear',beat,offsetMs,durationMs});
 const move=(id,beat,x,y,durationMs=1600,offsetMs=250)=>a.actions.push({actor:id,action:'moveTo',beat,offsetMs,x,y,durationMs});
 const express=(id,beat,emotion,offsetMs=150)=>a.actions.push({actor:id,action:'character.express',emotion,beat,offsetMs,durationMs:500});
 const put=(id,x,y,kids,meaning,anchors)=>{const o=a.object(id,x,y,kids,meaning);if(anchors)o.visual.anchors=anchors;a.add(o);return id;};
 const label=(id,value,x,y,size=30)=>put(id,x,y,[text(value,0,0,size)],value+' (label for the object beneath it)');
 const person=(id,x,identity,coat,scale=.82,y=548)=>storyPerson(a,id,x,y,{identity,coat,scale});

 if(index===0){
  // Book lens: a smoothly running system, a horizon of uncommitted possibility, then a current
  // from a person's present terminal into one future being built; stimulation flickers apart.
  put('system',290,470,[
   R(-250,-115,92,125,C.teal,10),R(-236,-98,64,40,C.mist,6),dot(-204,-30,7,C.cream),
   R(-160,-10,360,20,C.deep,10),...[-140,-80,-20,40,100,160].map(x=>dot(x,0,6,C.mist)),
   dark(path('M-140 10V75M170 10V75',C.ink,8)),dark(path('M-232 10V75M-176 10V75',C.ink,8))
  ],'A reliable production line that runs well without anyone needing to feel inspired');
  put('parcels',290,445,[-150,-80,-10,60].flatMap(x=>[R(x,-27,52,44,C.mist,5),R(x+22,-27,8,44,C.deep,1)]),'Identical finished parcels moving steadily: competent maintenance');
  move('parcels',1,320,445,3600,300);move('parcels',2,350,445,3600,200);
  label('label-reliability','Reliability',290,372,32);appear('label-reliability',1,900);
  person('maker',585,'person-04-neutral',C.teal);
  storyGesture(a,'maker',2,'question');express('maker',2,'curious');
  put('present',672,460,[R(-22,-32,44,64,C.teal,9),dot(0,-14,7,C.cream),dark(path('M22 -9H34M22 9H34',C.ink,5)),dark(path('M0 32V88',C.ink,6))],
   'Small present-world terminal: the effort available to this person now',{left:[-22,0],right:[36,0],top:[0,-32],bottom:[0,88]});
  // Possibilities are dashed: available but not yet committed to.
  put('possible-sail',770,250,[dash('M0 -50L42 22H0Z'),dash('M-6 -44L-38 22H-6'),dash('M-46 34H50L36 52H-34Z')],'A possible future no one has committed to yet (sailing)');
  put('possible-dome',1105,225,[dash('M-48 26A48 48 0 0 1 48 26Z'),dash('M0 -22V-40')],'Another uncommitted possible future (an observatory dome)');
  const blocks=[[-130,-40],[-130,-80],[-130,-120],[80,-40],[80,-80],[80,-120]].map(([x,y])=>[x,y,50,38]).concat([[-130,-162,82,40],[48,-162,82,40]]);
  put('future-outline',985,480,[...blocks.map(([x,y,w,h])=>dash(`M${x} ${y}h${w}v${h}h${-w}Z`,3)),dash('M-46 -162h92v40h-92Z',3)],
   'A larger possible future: an arch that could be built, still only an outline',{left:[-130,-20],right:[130,-20],top:[0,-162],bottom:[0,0]});
  appear('possible-sail',2,300,900);appear('possible-dome',2,700,900);appear('future-outline',2,1100,900);
  a.connections.push({id:'current',from:{node:'present',anchor:'right'},to:{node:'future-outline',anchor:'left'},color:C.amber,width:8,meaning:'Voluntary energy flows from the present terminal toward a future the person can help shape'});
  a.actions.push({actor:'current',action:'connection.draw',beat:3,offsetMs:300,durationMs:1500});
  put('future-built',985,480,blocks.map(([x,y,w,h])=>R(x+2,y+2,w-4,h-4,C.amber,4)),'The chosen future begins to take solid form once energy reaches it');
  appear('future-built',3,1700,900);storyGesture(a,'maker',3,'resolve');express('maker',3,'inspired');
  // Stimulation: brief sparks that nudge attention and never connect to the circuit.
  const sparks=[[512,300,C.amber],[660,262,C.teal],[540,236,C.teal],[690,318,C.amber],[600,214,C.amber]];
  sparks.forEach(([x,y,c],i)=>{put('spark-'+(i+1),x,y,[path('M-12 -14L2 -2L-6 2L10 14',c,5)],'A momentary stimulus that nudges attention without joining the current');appear('spark-'+(i+1),4,100+i*520,250);if(i<3)hide('spark-'+(i+1),4,800+i*520,300);});
  label('label-stimulation','Stimulation',430,226,28);appear('label-stimulation',4,200,500);
  put('pulse',672,460,[dot(0,0,13,C.cream),n('circle',{cx:0,cy:0,r:13,fill:'none',stroke:C.amber,'stroke-width':4})],'A pulse of effort travelling along the current');
  appear('pulse',4,2300,300);move('pulse',4,850,460,1200,2500);hide('pulse',4,3700,250);
  label('label-voltage','Voltage',782,424,28);appear('label-voltage',4,2400,500);
  put('keystone',985,236,[R(-44,-20,88,40,C.amber,4),R(-44,-20,88,8,C.pale,3)],'The effort arrives: the missing keystone lands, so the work visibly moves forward');
  appear('keystone',4,3600,400);move('keystone',4,985,338,900,3900);
  return a.finish('A reliable line runs while its worker is merely calm; uncommitted possibilities appear as outlines; a current from the present terminal makes one future solid, while sparks of stimulation flicker without joining it. Qualitative, no measurements.');
 }

 if(index===1){
  // Content lens: a dream meets a wall of early safeguards, is stamped flat into a credential,
  // then a reachable configuration replaces the wall; the book's shadow side remains in view.
  person('dreamer',205,'person-14-neutral',C.deep);express('dreamer',1,'skeptical');
  put('dream',400,292,[F('M-70 30Q-98 28 -92 2Q-96 -30 -62 -30Q-58 -60 -22 -58Q2 -78 34 -58Q72 -66 78 -32Q102 -20 90 8Q96 34 66 34Z',C.pale),
   F('M-40 -4L-24 -24L-8 -4Z',C.amber),n('path',{d:'M6 8Q22 -14 38 8Q54 -14 70 8',fill:'none',stroke:C.teal,'stroke-width':5,'stroke-linecap':'round'}),dot(-22,14,6,C.teal),
   dot(-120,48,6,C.pale),dot(-102,34,9,C.pale)],'A young dream, still open and undeveloped');
  // The wall: safeguards (form), metrics (chart), early evaluation (score card), stacked against a first move.
  put('form',640,498,[R(-80,-50,160,100,'#d9e6e8',6),R(-24,-58,48,16,C.slate,4),...[-24,2,28].flatMap(y=>[n('rect',{x:-60,y:y-9,width:18,height:18,fill:'none',stroke:C.teal,'stroke-width':3,rx:3}),path(`M-30 ${y}H58`,C.mist,5)])],'Forms and safeguards that raise the cost of an unproven first move');
  put('metric',640,398,[R(-80,-50,160,100,C.mist,6),...[[-52,26],[-20,44],[12,62],[44,34]].map(([x,h])=>R(x,38-h,22,h,C.deep,2)),path('M-66 -34H66',C.rust,4)],'Metrics and targets demanding a measurable outcome early');
  put('score',640,298,[R(-80,-50,160,100,C.slate,6),text('? / 10',0,14,36,C.cream)],'Early evaluation before the work has developed depth');
  for(const [id,o] of [['form',200],['metric',800],['score',1400]]){appear(id,1,o,600);}
  label('label-trap','Costly beginnings',640,222,32);appear('label-trap',1,2000,500);
  for(const [id,value,y,o] of [['label-form','Safeguards',498,500],['label-metric','Metrics',398,1100],['label-score','Early scoring',298,1700]]){label(id,value,800,y,26);appear(id,1,o,500);}
  put('flag',990,548,[R(-110,-58,220,58,C.deep,6),dark(path('M-85 -58V-190',C.ink,6)),F('M-85 -190L-21 -170L-85 -148Z',C.amber)],'A real place to begin, beyond the wall');
  // Dream compression: a stamp flattens the dream into a credential before it gains depth.
  put('stamp',400,168,[R(-18,-48,36,40,C.slate,10),R(-52,-10,104,26,C.rust,6),dark(R(-58,14,116,12,C.ink,3))],'An evaluation stamp');
  appear('stamp',2,150,500);move('stamp',2,400,214,700,700);
  hide('dream',2,1300,300);
  put('credential',400,292,[R(-74,-26,148,52,'#d9e6e8',4),R(-74,-26,10,52,C.amber,2),path('M-52 -8H48M-52 8H24',C.mist,5),dot(52,8,9,C.rust)],'The dream compressed into a credential or business model');
  appear('credential',2,1300,350);move('stamp',2,400,160,700,2200);
  storyGesture(a,'dreamer',2,'recoil',1700);express('dreamer',2,'worried',1300);
  label('label-compression','Dream compression',410,360,28);appear('label-compression',2,2400,500);
  for(const id of ['form','metric','score','label-trap','label-form','label-metric','label-score','stamp','credential','label-compression'])hide(id,3,150,600);
  // Ignition: reachable first step, visible consequence, enough control.
  put('steps',800,548,[R(-80,-20,62,20,C.amber,3),R(-18,-40,62,40,C.teal,3),R(44,-60,46,60,C.deep,3)],'A reachable first step up to the place of work');
  appear('steps',3,700,700);
  put('lamp',1072,490,[n('circle',{cx:0,cy:-70,r:44,fill:C.pale,opacity:.75}),dark(path('M0 0V-48',C.ink,6)),dot(0,-70,18,C.amber)],'A visible consequence: the effort lights something up');
  appear('lamp',3,2300,700);
  put('control',990,470,[dark(path('M0 7V20',C.ink,5)),R(-42,-7,84,14,C.slate,7)],'Enough control to change the work: a slider mounted at the place of work');
  put('control-knob',962,470,[dot(0,0,13,C.cream),n('circle',{cx:0,cy:0,r:13,fill:'none',stroke:C.teal,'stroke-width':4})],'The slider is moved: the participant can alter the work');
  appear('control',3,3000,500);appear('control-knob',3,3000,500);move('control-knob',3,1018,470,900,3700);
  a.actions.push({actor:'dreamer',action:'walkTo',beat:3,offsetMs:400,x:700,durationMs:2400});
  storyGesture(a,'dreamer',3,'invite',2600);express('dreamer',3,'inspired',2400);
  put('dream-shaped',944,300,[F('M-46 20Q-64 18 -60 0Q-62 -20 -40 -20Q-36 -40 -14 -38Q2 -50 22 -38Q46 -42 50 -20Q66 -12 58 6Q62 22 44 22Z',C.pale),F('M-26 -2L-14 -16L-2 -2Z',C.amber),dot(18,0,6,C.teal)],'The same dream, now attached to a concrete beginning');
  appear('dream-shaped',3,3300,600);label('label-ignition','Ignition',836,400);appear('label-ignition',3,1200,500);
  // Shadow side, presented soberly: cults, bubbles, burnout, the passion tax.
  const muted=(d,w=4)=>n('path',{d,fill:'none',stroke:'$ink','stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round',opacity:.7});
  put('cult',150,190,[n('circle',{cx:0,cy:0,r:12,fill:'$ink',opacity:.7}),...[0,1,2,3,4,5].map(i=>n('circle',{cx:Math.round(38*Math.cos(i*Math.PI/3)),cy:Math.round(38*Math.sin(i*Math.PI/3)),r:8,fill:'$ink',opacity:.45}))],'Cult: a group that claims the whole person');
  put('bubble',290,190,[muted('M0 -38A38 38 0 1 1 -0.1 -38'),muted('M-18 -18Q-8 -28 6 -26',3)],'Bubble: intense collective energy detached from evidence');
  put('burnout',430,192,[dark(path('M-26 34L18 -14',C.ink,6)),F('M18 -14Q30 -34 22 -40Q36 -36 32 -18Q30 -8 18 -14Z',C.slate),muted('M30 -48Q22 -60 32 -70',3)],'Burnout: a spent match');
  put('passion-tax',570,192,[R(-38,0,76,40,C.slate,5),R(-14,4,28,6,C.ink,2),F('M0 -6C-20 -24 -24 -44 -8 -44C-2 -44 0 -38 0 -36C0 -38 2 -44 8 -44C24 -44 20 -24 0 -6Z',C.rust)],'Unpaid passion tax: devotion dropped into an unpaid slot');
  [['cult',200],['bubble',900],['burnout',1600],['passion-tax',2300]].forEach(([id,o])=>appear(id,4,o,500));
  [['label-cult','Cults',150],['label-bubble','Bubbles',290],['label-burnout','Burnout',430],['label-tax','Passion tax',570]].forEach(([id,value,x],i)=>{label(id,value,x,262,26);appear(id,4,400+i*700,500);});
  a.actions.push({actor:'dreamer',action:'lookAt',target:'burnout',up:true,beat:4,offsetMs:300,durationMs:600});
  express('dreamer',4,'neutral',200);storyGesture(a,'dreamer',4,'reflect',1900);
  return a.finish('A dream is blocked by forms, metrics and early scoring, then stamped flat into a credential; the wall gives way to a reachable step, a visible light and a usable control; the shadow side is shown soberly.');
 }

 // Reader lens: permission as an open door, a protected experiment with room for dissent,
 // AI output that a person still checks, then the book opened at its first chapter.
 put('door',150,548,[R(-78,-262,156,262,C.deep,10),R(-60,-246,120,246,C.pale,6),F('M-60 0L60 0L84 18H-84Z',C.amber)],'A doorway opening onto lit space: permission as a concrete opening');
 put('door-leaf',150,548,[R(-60,-246,120,246,C.teal,6),dot(40,-120,8,C.cream)],'The door, still closed');
 put('door-open',150,548,[F('M-60 -246L-28 -228V-16L-60 0Z',C.teal),n('path',{d:'M38 -150V-166A14 14 0 0 1 66 -166',fill:'none',stroke:C.slate,'stroke-width':6,'stroke-linecap':'round'}),R(32,-152,40,32,C.slate,5)],'The door swung open, its padlock unlocked');
 hide('door-leaf',1,300,500);appear('door-open',1,300,500);
 label('label-permission','Permission',150,262);appear('label-permission',1,800,500);
 // The bench stands at hand height between the two builders (drawn behind them), so their
 // reaching hands meet the experiment rather than the bench top cutting across their bodies.
 put('bench',470,548,[R(-108,-66,216,14,C.deep,5),dark(path('M-92 -52V0M92 -52V0',C.ink,9))],'A protected workbench for a bounded experiment');
 person('builder-a',345,'person-06-neutral',C.teal,.7);person('builder-b',576,'person-17-neutral',C.amber,.7);
 person('dissenter',790,'person-21-neutral',C.slate,.7);
 put('experiment',470,482,[R(-50,-26,24,26,C.amber,3),R(26,-26,24,26,C.amber,3),R(-50,-48,100,20,C.amber,3),R(-50,-48,100,6,C.pale,2)],'A small protected experiment: a model arch, the book\'s future in miniature');
 appear('experiment',1,1200,600);label('label-experiments','Protected experiments',470,300,28);appear('label-experiments',1,1600,500);
 storyGesture(a,'dissenter',1,'question',2200);express('dissenter',1,'skeptical',2000);express('builder-a',1,'happy',900);express('builder-b',1,'happy',900);
 a.actions.push({actor:'builder-a',action:'reach',beat:1,offsetMs:1300,durationMs:3200});storyGesture(a,'builder-b',1,'invite',4200);
 // Generative AI weighed: the machine drafts, a person chooses, checks and stays with the result.
 put('ai',1045,548,[dark(R(-58,-196,116,196,C.ink,14)),R(-44,-180,88,70,C.mist,8),path('M-14 -146L0 -160L14 -146L0 -132Z',C.amber,4),R(-34,-80,68,8,C.slate,4)],'A generative AI system that can produce a polished first version');
 appear('ai',2,150,600);label('label-ai','AI scaffolding',1045,322,28);appear('label-ai',2,600,500);
 put('draft',1045,462,[R(-38,-50,76,100,C.cream,5),n('rect',{x:-38,y:-50,width:76,height:100,rx:5,fill:'none',stroke:C.amber,'stroke-width':3}),path('M-24 -26H24M-24 -8H24M-24 10H12',C.mist,5)],'A polished AI-made draft');
 appear('draft',2,900,400);move('draft',2,872,430,1400,1300);
 storyGesture(a,'dissenter',2,'explain',2900);express('dissenter',2,'curious',2700);
 put('check',872,430,[path('M-20 26L-6 40L22 10',C.teal,7)],'A person has checked the draft and accepts responsibility for it');
 appear('check',2,3700,400);
 for(const id of ['door','door-open','label-permission','builder-a','builder-b','dissenter','bench','experiment','label-experiments','ai','label-ai','draft','check'])hide(id,3,0,450);
 // Invitation: the volume opens at its first chapter, with the circuit in miniature on the facing page.
 a.add({id:'volume',asset:'book',x:600,y:418,scale:1.9,options:{color:C.teal},meaning:'The book itself, opened at its first chapter'});
 appear('volume',3,550,600);a.actions.push({actor:'volume',action:'book.open',beat:3,offsetMs:1000,durationMs:1300});
 // The asset's own ribbon is attached to the spread, not to the opening halves: reveal it only
 // once the book has opened, so it never floats beside a closed volume.
 appear('volume.detail18',3,2300,400);
 put('chapter',452,400,[text('The Missing',0,-14,32,C.ink),text('Voltage',0,20,30,C.ink),path('M-70 46H70',C.amber,4)],'The first chapter heading as it appears in the book');
 put('page-circuit',748,404,[R(-86,-12,22,30,C.teal,5),path('M-62 3H24',C.amber,6),R(24,-12,22,30,C.amber,3),R(64,-12,22,30,C.amber,3),R(24,-34,62,18,C.amber,3)],'The present-to-future circuit in miniature on the facing page');
 // Printed page rules give way to the chapter content instead of being cut by blank patches.
 for(const d of [4,5,6,7,8])hide('volume.detail'+d,3,2300,500);for(const d of [12,13,14,15,16])hide('volume.detail'+d,3,2600,500);
 appear('chapter',3,2300,500);appear('page-circuit',3,2600,500);
 return a.finish('A door unlocks onto a protected experiment where one participant openly questions; an AI draft is still checked by a person; the book opens at its first chapter, The Missing Voltage.');
}
scenes.forEach((scene,index)=>{scene.visual=art(index);});
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('Staged',scenes.length,'scenes:',scenes.map(s=>s.id+'('+s.visual.objects.length+' objects, '+s.visual.actions.length+' actions)').join(', '));
