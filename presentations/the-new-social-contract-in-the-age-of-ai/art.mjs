// Book-owned staging for "The New Social Contract in the Age of Artificial Intelligence".
// Identity (work/visual-bible.json, cover): a gold automated hub serves independent
// people who keep a link they can contest, cut or reroute. Navy/gold/cream cover palette.
// Usage: node presentations/the-new-social-contract-in-the-age-of-ai/art.mjs
import fs from 'node:fs';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';

const file=new URL('./work/scenes.json',import.meta.url);
const scenes=JSON.parse(fs.readFileSync(file,'utf8'));
const C={gold:'#e9b949',goldDeep:'#c9952a',blue:'#2f5aa8',navy:'#0d1a36',cream:'#f3ead2',
 coral:'#d4634a',green:'#4f9a6e',sky:'#9dbbe6',skin:'#c99074',nightBlue:'#8fb0e6'};

function compose(index){
 const a=stageAuthor(),{n,path,text,dot}=a;
 // Night variants: dark navy/blue fills become light so they read on the black stage.
 const night=(node,color)=>({...node,themeAttrs:{night:{[node.attrs.fill&&node.attrs.fill!=='none'?'fill':'stroke']:color}}});
 const R=(x,y,w,h,fill,rx=6)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const F=(d,fill)=>n('path',{d,fill});
 const ink=(value,x,y,size=26)=>text(value,x,y,size,'$ink');           // label directly on the stage
 const onPaper=(value,x,y,size=22)=>text(value,x,y,size,C.navy);        // label on a fixed cream/gold surface
 const put=(id,x,y,kids,meaning,scale=1,anchors)=>{const o=a.object(id,x,y,kids,meaning,scale);if(anchors)o.visual.anchors=anchors;a.add(o);return id;};
 const appear=(id,beat,offsetMs=250,durationMs=900)=>a.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs});
 const hide=(id,beat,offsetMs=150,durationMs=700)=>a.actions.push({actor:id,action:'disappear',beat,offsetMs,durationMs});
 const move=(id,beat,x,y,durationMs=1800,offsetMs=300)=>a.actions.push({actor:id,action:'moveTo',beat,x,y,offsetMs,durationMs});
 const express=(id,beat,emotion,offsetMs=150)=>a.actions.push({actor:id,action:'character.express',emotion,beat,offsetMs,durationMs:500});
 const gesture=(id,beat,g,offsetMs=700,durationMs=2000)=>a.actions.push({actor:id,action:'character.gesture',gesture:g,beat,offsetMs,durationMs});
 const link=(id,from,fa,to,ta,beat,meaning,color,offsetMs=400,width=5)=>{a.connections.push({id,from:{node:from,anchor:fa},to:{node:to,anchor:ta},width,color,meaning});a.actions.push({actor:id,action:'connection.draw',beat,offsetMs,durationMs:1400});};
 // Book-owned face retouch: 'curious' reads as open interest (raised arch, slight smile), not worry;
 // 'determined' reads as calm resolve (level brows, firm half-smile), not anger.
 const FACES={curious:{mouth:'M-8 21 Q1 26 9 19',brows:'M-17 -17 Q-11 -23 -5 -18 M7 -15 L20 -14'},
  determined:{mouth:'M-10 21 Q0 25 10 20',brows:'M-17 -13 L-5 -13 M7 -13 L20 -13'}};
 const retouch=node=>{for(const [emo,f] of Object.entries(FACES))for(const part of ['mouth','brows'])if(node.id?.endsWith('.expression.'+emo+'.'+part))node.attrs.d=f[part];for(const k of node.children||[])retouch(k);};
 const person=(id,x,y,o={})=>{storyPerson(a,id,x,y,{identity:'person-07-neutral',coat:C.blue,scale:.86,chair:C.goldDeep,...o});retouch(a.objects.find(v=>v.id===id).visual);return id;};

 // Cover motif: the automated hub as a gold processor with pins and a navy core.
 const chip=(s=1,body=C.gold,core=C.navy)=>{
  const k=[],h=70*s,p=[-42,-14,14,42].map(v=>v*s);
  for(const v of p)k.push(R(v-6*s,-h-22*s,12*s,24*s,body,3),R(v-6*s,h-2*s,12*s,24*s,body,3),R(-h-22*s,v-6*s,24*s,12*s,body,3),R(h-2*s,v-6*s,24*s,12*s,body,3));
  k.push(R(-h,-h,2*h,2*h,body,16*s),night(R(-36*s,-36*s,72*s,72*s,core,8*s),'#16284d'));
  return k;
 };
 // Cover-style population silhouette: head and rounded shoulders.
 const citizen=(x,y,s=1,fill=C.blue,nightFill=C.cream)=>[night(dot(x,y-34*s,15*s,fill),nightFill),night(F(`M${x-26*s} ${y+14*s}Q${x-26*s} ${y-14*s} ${x} ${y-14*s}Q${x+26*s} ${y-14*s} ${x+26*s} ${y+14*s}Z`,fill),nightFill)];
 const key=(s=1)=>[n('circle',{cx:-34*s,cy:0,r:22*s,fill:'none',stroke:C.gold,'stroke-width':12*s}),R(-14*s,-6*s,74*s,12*s,C.gold,4),R(38*s,4*s,10*s,18*s,C.gold,2),R(52*s,4*s,8*s,13*s,C.gold,2)];
 const doc=(w,h,lines=4,accent=C.blue)=>[R(-w/2,-h/2,w,h,C.cream,6),F(`M${w/2-26} ${-h/2}H${w/2}V${-h/2+26}Z`,C.goldDeep),R(-w/2,-h/2,8,h,accent,3),...Array.from({length:lines},(_,i)=>R(-w/2+26,-h/2+34+i*22,w-64-(i%2)*30,7,'#b9b2a0',3))];
 const eyeIcon=()=>[F('M-30 0Q0 -26 30 0Q0 26 -30 0Z',C.cream),dot(0,0,10,C.blue),dot(0,0,4,C.navy)];

 if(index===0){
  // WHY — an offer across the stage: a citizen holds the key of governance; the hub offers abundance.
  person('citizen',175,532,{identity:'person-07-neutral',coat:C.blue});
  put('key',300,330,[...key(1),ink('Governance',12,58,24)],'Gold key of governance held by the citizen: the price the automated order asks');
  put('hub',930,250,chip(1.25),'Automated order: the gold processor of the cover, administering production and services',1,{left:[-112,0],right:[112,0],top:[0,-112],bottom:[0,112]});
  const gift=(id,x,kids,label,meaning,offset)=>{put(id,x,445,[...kids,ink(label,0,66,22)],meaning,1,{top:[0,-42],left:[-40,0],right:[40,0],bottom:[0,40]});appear(id,1,offset);};
  gift('comfort',770,[F('M-40 -4L0 -40L40 -4Z',C.coral),R(-32,-6,64,46,C.cream,3),R(-9,12,18,28,C.goldDeep,2),R(-26,4,12,11,C.gold,2)],'Comfort','Home with warm light: material comfort offered by the automated order',800);
  gift('safety',910,[F('M0 -42L34 -28V2Q34 30 0 44Q-34 30 -34 2V-28Z',C.blue),night(F('M0 -42L34 -28V2Q34 30 0 44Z',C.sky),'#c6d7f2'),path('M-14 2L-3 14L17 -12',C.cream,7)],'Safety','Shield: safety offered by the automated order',1500);
  gift('experiences',1050,[R(-42,-20,84,40,C.green,18),dot(-17,0,11,C.cream),dot(17,0,11,C.cream),path('M-26 -20L-14 -40M26 -20L14 -40',C.green,6),dot(-36,-36,6,C.gold),dot(36,-30,5,C.coral)],'Experiences','Virtual-world headset: varied experiences offered by the automated order',2200);
  link('serve-comfort','hub','bottom','comfort','top',1,'The hub supplies comfort',C.gold,700,4);
  link('serve-safety','hub','bottom','safety','top',1,'The hub supplies safety',C.gold,1400,4);
  link('serve-experiences','hub','bottom','experiences','top',1,'The hub supplies experiences',C.gold,2100,4);
  express('citizen',1,'curious');gesture('citizen',1,'question',900,2200);
  // The key drifts toward the hub: the condition of the offer.
  move('key',1,600,196,2200,3000);
  // The book answers: a contract of twenty-one clauses appears between the two parties.
  const clauses=[];for(let c=0;c<3;c++)for(let r=0;r<7;r++)clauses.push(R(-76+c*56,-52+r*20,40,8,c===1&&r===3?C.coral:'#b9b2a0',3));
  put('contract',420,390,[...doc(210,250,0,C.gold).slice(0,3),onPaper('Social contract',4,-82,22),...clauses,onPaper('21 clauses',4,108,22)],'The book’s answer: twenty-one debatable clauses of a new social contract',1,{left:[-105,0],right:[105,0],top:[0,-125],bottom:[0,125]});
  appear('contract',2,300,1100);
  put('pencil',560,420,[R(-6,-50,12,84,C.goldDeep,3),F('M-6 34L0 50L6 34Z',C.navy),R(-6,-56,12,10,C.coral,2)],'A pencil: the clauses are drafts open to debate, not binding law');
  appear('pencil',2,1500);move('pencil',2,538,405,1600,2300);
  express('citizen',2,'determined');gesture('citizen',2,'explain',800,2400);
  // The fear: irreplaceable control of the infrastructure.
  put('enclosure',930,250,[n('circle',{cx:0,cy:0,r:142,fill:'none',stroke:C.coral,'stroke-width':10,'stroke-dasharray':'2 0'}),R(-168,-14,52,42,C.coral,6),n('path',{d:'M-158 -12V-30Q-158 -48 -142 -48Q-126 -48 -126 -30V-12',fill:'none',stroke:C.coral,'stroke-width':8}),dot(-142,6,6,C.cream)],'A locked ring closes around the hub: leadership that controls infrastructure and cannot be replaced');
  appear('enclosure',3,600,1200);
  put('leader',1118,318,[...citizen(0,0,1.35,C.coral,'#f0a08c'),F('M-16 -60L-19 -84L-9 -73L0 -88L9 -73L19 -84L16 -60Z',C.goldDeep),night(path('M-16 -4Q-38 -16 -54 -10',C.coral,11),'#f0a08c'),dot(-57,-10,8,C.skin)],'A crowned leader grips the ring around the infrastructure: the irreplaceable controller the book fears');
  appear('leader',3,1100,900);
  put('no-replace',690,335,[ink('Cannot be',0,0,24),ink('replaced',0,30,24)],'The specific fear named by the book: irreplaceable leadership, not scarcity');
  appear('no-replace',3,1600);
  express('citizen',3,'worried');gesture('citizen',3,'recoil',900,2000);
 }else if(index===1){
  // HOW — four mechanisms of the contract, staged as successive civic situations.
  // 1. Delegate administration; keep collective goals under legitimate control.
  put('assembly',250,400,[R(27,-150,6,128,'$ink',3),F('M33 -150L89 -134L33 -118Z',C.gold),...citizen(-60,20,1.15),...citizen(0,0,1.25),...citizen(60,20,1.15),ink('Goals',0,96,26)],'Citizens holding the flag of collective goals: legitimate political control',1,{right:[80,0],left:[-80,0]});
  put('operator',880,360,[...chip(.9),ink('Administration',0,128,24)],'Automated operator to which administration is delegated',1,{left:[-84,0],right:[84,0]});
  put('mandate-tag',570,330,[R(-66,-20,132,40,C.cream,20),onPaper('Mandate',0,8,22)],'A revocable mandate: delegated, not surrendered');
  link('mandate','assembly','right','operator','left',1,'Delegation by mandate runs from the citizens to the operator',C.gold,400,5);
  appear('mandate-tag',1,1300);
  const service=(id,y,kids,offset,meaning)=>{put(id,1060,y,kids,meaning);appear(id,1,offset,700);};
  service('svc-1',290,[F('M-24 -2L0 -24L24 -2Z',C.coral),R(-18,-4,36,26,C.blue,3),night(R(-18,-4,36,26,C.blue,3),C.nightBlue)],1800,'Delivered service: housing');
  service('svc-2',360,[R(-7,-22,14,44,C.green,3),R(-22,-7,44,14,C.green,3)],2300,'Delivered service: health care');
  service('svc-3',430,[F('M-26 -4H26Q24 22 0 22Q-24 22 -26 -4Z',C.goldDeep),dot(-8,-10,7,C.green),dot(8,-12,8,C.coral)],2800,'Delivered service: food');
  for(const id of ['assembly','operator','mandate-tag','svc-1','svc-2','svc-3'])hide(id,2,100);
  a.actions.push({actor:'mandate',action:'disappear',beat:2,offsetMs:100,durationMs:700});
  // 2. Exit counts only if identity, records and services move with the person.
  put('old-provider',330,250,[...chip(.62,C.gold),ink('Old provider',0,92,22)],'The provider the person leaves');
  put('new-provider',900,250,[...chip(.62,C.sky,C.navy),ink('New provider',0,92,22)],'An alternative provider the person can actually move to');
  appear('old-provider',2,500);appear('new-provider',2,700);
  person('traveller',260,535,{identity:'person-12-neutral',coat:C.green,scale:.72});appear('traveller',2,600);
  const tag=(y,icon,label)=>[R(62,y-18,176,36,C.cream,8),...icon,onPaper(label,162,y+8,21)];
  put('luggage',380,470,[R(-48,-34,96,74,C.coral,10),path('M-16 -34V-46H16V-34','$ink',5),
   ...tag(-70,[R(72,-80,24,18,C.blue,3)],'Identity'),...tag(-28,[R(74,-40,18,22,'#b9b2a0',2)],'Records'),...tag(14,[dot(84,14,9,C.gold)],'Services')],
   'Portable case carrying identity, records and service access: what must move with the person for exit to be real',1);
  appear('luggage',2,600);
  a.actions.push({actor:'traveller',action:'walkTo',beat:2,offsetMs:2400,x:760,durationMs:3000});
  move('luggage',2,880,470,3000,2400);
  express('traveller',2,'determined',300);
  for(const id of ['old-provider','new-provider','traveller','luggage'])hide(id,3,100);
  // 3. An appeal: reasons, corrected facts, independent review, real remedy.
  const steps=[['Reasons'],['Facts','corrected'],['Independent','review'],['Remedy']];
  steps.forEach((label,i)=>{const x=330+i*200,h=50+i*60;put('step-'+i,x,500,[night(R(-100,-h,200,h,i===3?C.green:C.blue,i===3?8:2),i===3?'#6fbf8f':C.nightBlue),...(i===3?[night(text('Remedy',0,-h/2+8,24,C.cream),C.navy)]:label.map((t,j)=>night(text(t,-10,-16-(label.length-1-j)*26,22,C.cream),C.navy)))],'Appeal stage: '+label.join(' '));appear('step-'+i,3,700+i*600,700);});
  const paper=[R(-36,-48,72,96,C.cream,5),R(-24,-30,48,6,'#b9b2a0',3),R(-24,-18,36,6,'#b9b2a0',3)];
  put('decision',140,320,paper,'The person’s case file, carried through each stage of appeal');
  put('verdict',140,320,[n('circle',{cx:0,cy:16,r:20,fill:'none',stroke:C.coral,'stroke-width':6}),path('M-9 7L9 25M9 7L-9 25',C.coral,6)],'Adverse automated decision');
  for(const id of ['decision','verdict']){appear(id,3,700,500);move(id,3,390,400,650,1000);move(id,3,590,340,650,1650);move(id,3,790,280,650,2300);move(id,3,990,220,650,2950);}
  hide('verdict',3,3650,400);
  put('remedy-mark',990,236,[dot(0,0,22,C.green),path('M-10 0L-3 8L11 -9',C.cream,6)],'Remedy granted after independent review');appear('remedy-mark',3,3800,600);
  for(const id of ['step-0','step-1','step-2','step-3','decision','remedy-mark'])hide(id,4,100);
  // 4. Three separate powers: set goals, run infrastructure, oversee rights.
  put('goal-setters',400,430,[night(F('M-90 40V-20Q0 -100 90 -20V40Z',C.blue),C.nightBlue),R(-100,40,200,14,C.goldDeep,3),...citizen(-34,30,.7,C.cream,C.navy),...citizen(34,30,.7,C.cream,C.navy),ink('Set goals',0,100,24)],'Assembly that sets collective goals');
  put('operators',600,410,[...chip(.62),ink('Run infrastructure',0,120,24)],'Operators of automated infrastructure');
  put('overseers',835,430,[R(-8,-80,16,120,C.goldDeep,4),R(-60,40,120,14,C.goldDeep,6),R(-110,-86,220,10,C.goldDeep,5),dot(0,-86,12,C.gold),
   path('M-90 -76L-118 -10M-90 -76L-62 -10M90 -76L62 -10M90 -76L118 -10','$ink',3),F('M-124 -10Q-90 22 -56 -10Z',C.blue),F('M56 -10Q90 22 124 -10Z',C.green),ink('Oversee rights',0,100,24)],
   'Independent oversight of rights: scales held apart from goal-setters and operators');
  ['goal-setters','operators','overseers'].forEach((id,i)=>appear(id,4,200+i*600,700));
  move('goal-setters',4,220,430,1500,1900);move('overseers',4,980,430,1500,1900);
 }else{
  // WHAT — protections, stress tests, the legitimacy test and the reading invitation.
  // 1. A ring of later clauses protects people (the cover's ring, now guarding people, not the chip).
  put('household',600,360,[...citizen(-46,0,1.3),...citizen(46,0,1.3),...citizen(0,30,.8,C.goldDeep)],'A household: people the later clauses protect');
  put('guard-ring',600,330,[n('circle',{cx:0,cy:0,r:150,fill:'none',stroke:C.gold,'stroke-width':8})],'Gold ring of the contract, now guarding people rather than the processor');
  appear('household',1,100,700);appear('guard-ring',1,300,1000);
  const shield=(id,x,y,kids,label,lx,ly,anchor,offset,meaning)=>{put(id,x,y,[night(dot(0,0,34,C.navy),'#2c4478'),...kids,text(label,lx,ly,22,'$ink')],meaning);const t=a.objects.at(-1).visual.children.at(-1);t.attrs['text-anchor']=anchor;appear(id,1,offset,700);};
  shield('attention',450,330,eyeIcon(),'Attention',-48,8,'end',900,'Attentional autonomy');
  shield('privacy',494,224,[R(-18,-14,36,30,C.cream,4),n('path',{d:'M-11 -14V-24Q-11 -34 0 -34Q11 -34 11 -24V-14',fill:'none',stroke:C.cream,'stroke-width':6})],'Privacy',-48,8,'end',1500,'Privacy and separation of life domains');
  shield('ecology',706,224,[F('M-16 14Q-18 -18 18 -20Q18 14 -16 14Z',C.green),path('M-12 10L8 -8',C.cream,3)],'Ecological budgets',48,8,'start',2100,'Ecological budgets');
  shield('reproduction',750,330,[F('M0 18L-20 -2Q-28 -14 -16 -22Q-6 -26 0 -14Q6 -26 16 -22Q28 -14 20 -2Z',C.coral)],'Reproductive freedom',48,8,'start',2700,'Reproductive freedom without coercion');
  shield('generations',706,436,[R(-14,-22,28,40,C.gold,3),dot(6,0,3,C.navy),...citizen(-26,22,.35,C.cream)],'New generations',48,8,'start',3300,'Room for new generations: offices and wealth that do not stay closed');

  for(const id of ['household','guard-ring','attention','privacy','ecology','reproduction','generations'])hide(id,2,100);
  // 2. Stress tests: who pays, who enforces, why would powerful actors comply.
  put('draft',600,235,[...doc(180,190,0,C.gold).slice(0,3),onPaper('21 draft clauses',2,-56,18),...Array.from({length:5},(_,i)=>R(-62,-30+i*22,124-(i%2)*24,7,'#b9b2a0',3))],'The draft contract under stress',1,{bottom:[0,95],left:[-90,0],right:[90,0]});
  appear('draft',2,200,700);
  put('payer',310,440,[...[0,1,2,3].map(i=>night(R(-34,12-i*16,68,14,C.goldDeep,7),C.gold)),ink('Who pays?',0,66,26)],'Coins: who funds each guarantee',1,{top:[0,-50],right:[40,-30]});
  put('enforcer',600,440,[path('M-34 30L24 -28',C.goldDeep,12),night(F('M56.9 -14.3L35.7 6.9L-20.9 -49.7L0.3 -70.9Z',C.navy),C.sky),R(-60,40,110,12,C.goldDeep,4),ink('Who enforces?',0,82,26)],'Gavel: who can enforce the contract',1,{top:[0,-40]});
  put('powerful',890,430,[night(R(-34,-90,68,130,C.navy,4),'#3a5287'),...chip(.3).map(k=>({...k,attrs:{...k.attrs,y:(k.attrs.y??0)-104}})),...[0,1,2].map(i=>R(-20,-70+i*34,40,14,C.gold,2)),ink('Why comply?',0,76,26)],'A tower crowned by a processor: why would powerful actors comply',1,{top:[0,-130],left:[-40,-20]});
  appear('payer',2,700,700);appear('enforcer',2,1400,700);appear('powerful',2,2100,700);
  link('test-pay','payer','top','draft','left',2,'Funding presses on the draft',C.coral,1000,4);
  link('test-enforce','enforcer','top','draft','bottom',2,'Enforcement presses on the draft',C.coral,1700,4);
  link('test-comply','powerful','left','draft','right',2,'Powerful actors press on the draft',C.coral,2400,4);
  move('draft',2,606,233,240,3300);move('draft',2,594,237,240,3540);move('draft',2,600,235,240,3780);
  for(const id of ['draft','payer','enforcer','powerful'])hide(id,3,100);
  for(const id of ['test-pay','test-enforce','test-comply'])a.actions.push({actor:id,action:'disappear',beat:3,offsetMs:100,durationMs:700});
  // 3. The test: abundance reduces dependency vs makes it comfortable.
  put('one-hub',140,250,chip(.5),'A single provider',1,{right:[56,0],bottom:[0,56]});
  person('comfortable',300,520,{identity:'person-04-neutral',coat:C.goldDeep,seated:true,chair:C.blue,scale:.7});a.objects.at(-1).visual.anchors={left:[-60,-130],right:[60,-130],top:[0,-260],bottom:[0,0]};
  put('comfort-label',300,155,[ink('Comfortable',0,0,24),ink('dependency',0,28,24)],'Left side: dependency made comfortable');
  link('tether','one-hub','right','comfortable','left',3,'One locked line: comfortable but dependent',C.coral,1500,7);
  for(const id of ['one-hub','comfortable','comfort-label'])appear(id,3,900,800);
  put('hub-a',700,400,chip(.42),'Provider A',1,{right:[48,0],bottom:[0,48]});
  put('hub-b',1060,400,chip(.42,C.sky),'Provider B',1,{left:[-48,0],bottom:[0,48]});
  person('independent',880,525,{identity:'person-07-neutral',coat:C.blue,scale:.72});a.objects.at(-1).visual.anchors={left:[-62,-100],right:[62,-100],top:[0,-260],bottom:[0,0]};
  put('independent-label',880,175,[ink('Reduced dependency',0,0,24)],'Right side: abundance that reduces dependency');
  for(const id of ['hub-a','hub-b','independent'])appear(id,3,1600,800);
  appear('independent-label',3,2200,800);
  link('route-a','hub-a','right','independent','left',3,'A link the person can cut or reroute',C.gold,2200,5);
  link('route-b','hub-b','left','independent','right',3,'A second real alternative',C.sky,2800,5);
  put('check',880,250,[dot(0,0,26,C.green),path('M-11 0L-3 9L12 -9',C.cream,6)],'Legitimate: the abundance reduces dependency');appear('check',3,3800,600);
  express('comfortable',3,'tired',300);express('independent',3,'determined',1700);gesture('independent',3,'resolve',2200,2200);
  for(const id of ['one-hub','comfortable','comfort-label','hub-a','hub-b','independent','independent-label','check'])hide(id,4,100);
  for(const id of ['tether','route-a','route-b'])a.actions.push({actor:id,action:'disappear',beat:4,offsetMs:100,durationMs:700});
  // 4. Begin with the Introduction.
  a.add({id:'reading-copy',asset:'book',x:600,y:340,scale:1.7,options:{color:C.blue},meaning:'The book opens at its Introduction'});
  appear('reading-copy',4,400,800);a.actions.push({actor:'reading-copy',action:'book.open',beat:4,offsetMs:900,durationMs:1300});
  put('intro-page',475,286,[onPaper('Introduction',0,0,24)],'Opening section of the book');
  put('offer-page',727,286,[onPaper('The political offer',0,0,21)],'The political offer of an automated order, set out in the Introduction');
  appear('intro-page',4,2200,700);appear('offer-page',4,2700,700);
 }
 const meaning=['A citizen holds the key of governance while a gold automated hub offers comfort, safety and experiences; the book answers with a twenty-one-clause contract, and the danger appears as a locked ring of irreplaceable control.',
  'Four mechanisms staged as civic situations: a revocable mandate from citizens to an operator, an exit carrying identity, records and services, an appeal path ending in remedy, and three powers moving apart.',
  'Later clauses ring a household with protections, the draft is tested by funding, enforcement and compliance, comfortable dependency is contrasted with reduced dependency, and the book opens at its Introduction.'][index];
 return a.finish(meaning+' Qualitative illustration; no invented measurements.');
}
scenes.forEach((s,i)=>{s.visual=compose(i);});
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('Staged '+scenes.length+' scenes.');
