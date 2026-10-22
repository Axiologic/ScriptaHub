// Book-owned staging for We Manufacture Our Own Masters: levelled fortunes feed a raised desk,
// one hostile-ruler test bench examines every system (and the book), and the cover's pedestal
// becomes a figure's practical power to refuse. Palette follows the cover: red, grey, ink.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
import {closedBookVisual,openBookVisual} from '../../.agents/skills/shf-presentation-creator/scripts/lib/book-art.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),file=path.join(root,'work/scenes.json'),scenes=JSON.parse(fs.readFileSync(file,'utf8'));
const C={red:'#c8322b',grey:'#8e8e93',ink:'#141414',stone:'#a9a9ae',slate:'#5f5f65',paper:'#f4efe6',ochre:'#d39a3a',bread:'#c98a45',night:'#d6d3cd'};
function compose(i){
 const q=stageAuthor(),{n,path:p,text:t,dot}=q;
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const shape=(d,fill)=>n('path',{d,fill});
 // Ink lines drawn directly on the stage stay visible in Night.
 const inkLine=(d,w=6)=>q.tint(p(d,C.ink,w),C.night);
 const put=(id,x,y,nodes,meaning,scale=1)=>q.add(q.object(id,x,y,nodes,meaning,scale));
 const show=(id,beat,offsetMs=250,durationMs=700)=>q.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs});
 const hide=(id,beat,offsetMs=150)=>q.actions.push({actor:id,action:'disappear',beat,offsetMs,durationMs:170});
 const move=(id,beat,x,y,offsetMs=300,durationMs=1400)=>q.actions.push({actor:id,action:'moveTo',beat,x,y,offsetMs,durationMs});
 const express=(id,beat,emotion,offsetMs=200)=>q.actions.push({actor:id,action:'character.express',emotion,beat,offsetMs,durationMs:700});
 const gesture=(id,beat,g,offsetMs=900)=>q.actions.push({actor:id,action:'character.gesture',gesture:g,beat,offsetMs,durationMs:1900});
 const who=(id,x,y,{coat=C.grey,identity='person-14-neutral',scale=.62,seated=false,chair=C.slate}={})=>{
  storyPerson(q,id,x,y,{identity,coat,scale,seated,chair,ink:C.ink});
  const v=q.objects.at(-1).visual,regrey=z=>{if(z.themeAttrs?.night)for(const k of ['fill','stroke'])if(z.themeAttrs.night[k]==='#9aafc3')z.themeAttrs.night[k]='#b9b9be';if(['#28343C','#39272D','#563A2D'].includes(z.attrs?.fill))z.themeAttrs={...z.themeAttrs,night:{...z.themeAttrs?.night,fill:'#8a8178'}};for(const c of z.children||[])regrey(c);};regrey(v);
  return id;
 };
 const ground=(x1,x2,y=548)=>put('ground',600,y,[rect(x1-600,0,x2-x1,8,C.grey,4)],'A plain shared floor line');
 const coins=h=>Array.from({length:h},(_,k)=>n('ellipse',{cx:0,cy:-8-k*12,rx:26,ry:8,fill:k%2?C.ochre:'#e2b45a'}));
 if(i===0){
  // 1: fortunes leave three levelled citizens and rise to a desk that allocates homes and exits.
  ground(110,1110);
  [['citizen-a',170,'person-14-neutral'],['citizen-b',310,'person-05-neutral'],['citizen-c',450,'person-09-neutral']].forEach(([id,x,identity])=>who(id,x,556,{identity}));
  [[232,7],[372,4],[512,2]].forEach(([x,h],k)=>put('fortune-'+k,x,548,coins(h),'A private fortune of unequal size beside a citizen'));
  put('pedestal',800,548,[rect(-190,-74,380,74,C.stone,4),rect(-150,-146,300,72,C.grey,4)],'An administrative hierarchy raised from ordinary blocks');
  who('official',800,402,{coat:C.red,identity:'person-20-neutral',scale:.6,seated:true,chair:C.slate});
  put('desk',800,402,[rect(-120,-74,240,74,C.slate,6),rect(-128,-82,256,12,C.ink,3)],'The allocating desk in front of the seated official');
  put('ledger',748,320,[rect(-34,-6,68,12,C.paper,2),p('M-22 0H22',C.slate,2)],'The allocation ledger on the desk');
  put('home-keys',800,368,[rect(-62,-22,124,44,C.paper,5),...[-34,0,34].map(x=>[dot(x,-7,7,C.red),p(`M${x} 0V14M${x} 9H${x+6}`,C.red,3)]).flat()],'Housing keys now held by the desk');
  put('exit-gate',1060,548,[rect(-58,-180,14,180,C.slate,3),rect(44,-180,14,180,C.slate,3)],'An exit gate out of the levelled order');
  put('barrier',1060,430,[rect(-44,-9,88,18,C.red,4)],'The gate barrier lowered by the desk');
  for(let k=0;k<3;k++){const x=[232,372,512][k];move('fortune-'+k,1,x,320,300+k*150,700);move('fortune-'+k,1,690,330,1100+k*150,900);hide('fortune-'+k,1,2150+k*150);}
  show('home-keys',1,2700);show('barrier',1,3700);
  put('loop',600,300,[p('M-290 40Q-150 -120 40 -40',C.red,6),shape('M28 -58L58 -36L24 -20Z',C.red)],'The levelling ideal loops back into a new command');
  put('loop-label',360,190,[t('Antinomies',0,0,34)],'Name of the recurring trap');
  show('loop',2,300,1100);show('loop-label',2,900);
  put('hidden-crown',800,182,[n('path',{d:'M-36 18V-14L-18 2L0 -24L18 2L36 -14V18Z',fill:'none',stroke:C.red,'stroke-width':4,'stroke-dasharray':'7 6','stroke-linejoin':'round'})],'A crown without a title above the official: nobility hidden behind levelled incomes');
  put('crown-label',990,182,[t('No title',0,0,28)],'The privilege carries no formal title');
  show('hidden-crown',3,400,1000);show('crown-label',3,1100);
  [232,372,512].forEach((x,k)=>{put('levelled-'+k,x,548,coins(1),'Three equal levelled incomes beside the citizens');show('levelled-'+k,3,200+k*120,500);});
  for(const id of ['citizen-a','citizen-b','citizen-c']){express(id,1,'surprised',2300);express(id,3,'sad');}
  gesture('citizen-b',1,'recoil',2500);gesture('official',1,'explain',3200);express('official',1,'determined',2600);
  gesture('citizen-a',2,'question');gesture('citizen-c',3,'release');express('official',3,'determined');
  return q.finish('Unequal fortunes leave three levelled citizens and rise into a raised desk that now holds the housing keys and lowers the exit barrier; a red loop names the antinomy, and an untitled crown marks the hidden nobility.');
 }
 if(i===1){
  // 2: the same seat, the same pressure and the same brace test every system, including the book.
  ground(110,1110);
  put('column',560,548,[rect(-110,-218,220,218,C.grey,6),rect(-96,-196,192,150,C.paper,6)],'One test bench beneath a seat of power');
  who('benign',560,330,{coat:C.stone,identity:'person-02-neutral',scale:.66,seated:true,chair:C.slate});
  who('hostile',560,330,{coat:C.red,identity:'person-07-neutral',scale:.66,seated:true,chair:C.slate});
  hide('benign',1,700);show('hostile',1,800,500);express('benign',1,'happy',0);express('hostile',1,'angry',1400);gesture('hostile',1,'explain',2200);
  put('pressure',900,214,[rect(-260,-8,260,14,C.slate,4),inkLine('M-10 6V40',5),rect(-130,40,240,62,C.slate,6)],'A weight the ruler can lower over those affected');
  move('pressure',1,900,262,3000,1300);
  who('affected-a',830,560,{identity:'person-10-neutral'});who('affected-b',980,560,{identity:'person-16-neutral'});
  express('affected-a',1,'worried',3600);express('affected-b',1,'worried',3600);
  put('brace',900,548,[rect(-10,-214,20,214,C.red,4),rect(-34,-222,68,12,C.red,4)],'A brace the affected people can raise: their power to stop the ruler');
  show('brace',2,500,800);move('pressure',2,900,226,1400,1000);gesture('affected-a',2,'resolve',600);gesture('affected-b',2,'explain',900);express('affected-a',2,'determined');express('hostile',2,'surprised',1500);
  const emblem=(id,beat,offset,nodes,name,meaning,last=false)=>{put(id,560,425,[...nodes,t(name,0,62,name.length>15?19:22,C.ink)],meaning);if(beat)show(id,beat,offset,350);if(!last&&beat)hide(id,beat,offset+1500);};
  emblem('any-system',0,0,[dot(0,-6,30,C.slate),dot(0,-6,12,C.paper)],'Any system','Before the comparison: an unspecified system on the bench');hide('any-system',3,200);
  emblem('liberal',3,300,[rect(-30,-30,60,46,C.slate,5),rect(-16,-36,32,6,C.ink,2),rect(-8,-50,16,22,C.paper,2)],'Liberal democracy','Liberalism on the same bench');
  emblem('one-party',3,1800,[rect(-14,-44,28,62,C.slate,3),p('M-10 -44V-64',C.ink,3),shape('M-10 -64H18L10 -57L18 -50H-10Z',C.red)],'One-party order','Chinese one-party order on the same bench');
  emblem('private-city',3,3300,[rect(-34,-24,22,42,C.slate,3),rect(-8,-44,26,62,C.slate,3),rect(22,-14,16,32,C.slate,3),rect(-4,-8,10,26,C.red,2)],'Private city','A privately governed city on the same bench');
  emblem('income',3,4800,[rect(-34,-30,68,44,C.slate,5),p('M-34 -30L0 -6L34 -30',C.paper,4),dot(26,10,13,C.ochre)],'Guaranteed income','Guaranteed income on the same bench',true);
  hide('income',4,200);
  put('own-book',560,458,[{...closedBookVisual('$asset',{color:C.red}),id:'$asset.book'}],'The book itself placed on its own test bench',.42);
  put('own-book-name',560,484,[t('This book',0,0,22,C.ink)],'The book names itself as the next system on the bench');
  show('own-book',4,1500,700);show('own-book-name',4,1500,700);
  put('appendix',230,330,[rect(-120,-124,240,248,C.paper,6),t('Supported',-56,-88,20,C.ink),t('Hypothesis',58,-88,20,C.ink),p('M0 -104V104',C.stone,2),...[-56,-22,12,46].map(y=>[p(`M-102 ${y}H-12`,C.slate,7),p(`M14 ${y}H102`,C.slate,4)]).flat().map((z,k)=>k%2?{...z,attrs:{...z.attrs,'stroke-dasharray':'8 7'}}:z)],'Appendix separating supported claims from hypothesis');
  show('appendix',4,300,800);
  gesture('affected-b',3,'reflect',600);express('affected-b',3,'skeptical');express('hostile',4,'neutral');gesture('affected-a',4,'question',1600);express('affected-a',4,'relieved',300);
  return q.finish('A smiling ruler is replaced by a hostile one on the same seat, lowering a weight over two affected people until they raise a brace; four named systems then pass the same bench before the book and its two-column appendix face the test.');
 }
 // 3: concrete dangers, then the cover's pedestal and a figure who can walk away, then chapter one.
 ground(110,1110);
 put('stall',300,548,[rect(-130,-140,14,140,C.slate,3),rect(116,-140,14,140,C.slate,3),shape('M-150 -140H150L130 -186H-130Z',C.red),rect(-110,-60,220,60,C.stone,4),dot(-60,-72,16,C.ochre),dot(-20,-74,14,C.bread),dot(24,-72,16,C.ochre)],'A market stall held by an established winner');
 who('winner',250,556,{coat:C.red,identity:'person-03-neutral',scale:.56});
 put('gate-open',470,548,[rect(-8,-130,16,130,C.slate,3),rect(10,-120,10,110,C.stone,2)],'An entry gate standing open');
 put('gate-shut',470,548,[rect(-8,-130,16,130,C.slate,3),rect(-6,-100,96,12,C.slate,3),rect(-6,-52,96,12,C.slate,3),rect(80,-130,12,130,C.slate,3)],'The winner closes the entry gate');
 show('gate-shut',1,1300,400);hide('gate-open',1,1350);
 who('newcomer',610,556,{identity:'person-05-neutral',scale:.56});express('newcomer',1,'worried',1700);gesture('winner',1,'explain',800);
 put('speaker-box',900,548,[rect(-50,-40,100,40,C.slate,4)],'A small box for a public speaker');
 who('speaker',900,508,{identity:'person-09-neutral',scale:.52});gesture('speaker',1,'explain',2800);express('speaker',1,'worried',4900);
 put('speech',990,268,[n('path',{d:'M-46 -26H46V22H-12L-30 40L-24 22H-46Z',fill:C.red}),p('M-30 -8H30M-30 6H14',C.paper,4)],'The speaker’s legal argument');
 const noise=[[790,250],[1080,330],[860,190],[1050,190],[760,340],[960,170],[1100,250],[968,276],[1014,256]];
 noise.forEach(([x,y],k)=>{put('noise-'+k,x,y,[n('path',{d:'M-34 -20H34V18H-8L-22 32L-18 18H-34Z',fill:C.stone}),p('M-20 -4H20',C.slate,3)],'Flooding noise crowding out the argument without a censor');show('noise-'+k,1,3600+k*260,300);});
 const beat1=['stall','winner','gate-open','gate-shut','newcomer','speaker-box','speaker','speech',...noise.map((_,k)=>'noise-'+k)];
 beat1.filter(id=>id!=='gate-open').forEach(id=>hide(id,2,100));
 // Beat 2: cheap expertise at small terminals, but every tether runs to one owned infrastructure.
 put('infrastructure',880,548,[rect(-110,-300,220,300,C.slate,8),...[-250,-190,-130,-70].map(y=>[rect(-86,y,172,40,C.grey,4),dot(-62,y+20,6,C.ochre)]).flat()],'Infrastructure, data and access owned by one provider');
 put('owner-crown',880,226,[shape('M-46 22V-16L-22 4L0 -28L22 4L46 -16V22Z',C.red)],'Control accrues to whoever owns the infrastructure');
 const terminals=[[230,'user-a','person-14-neutral'],[440,'user-b','person-16-neutral']];
 terminals.forEach(([x,id,identity])=>{who(id,x,556,{identity,scale:.56});put(id+'-device',x+62,490,[rect(-34,-24,68,44,C.slate,5),rect(-28,-18,56,32,C.paper,3),p('M-18 -6H18M-18 4H8',C.red,3)],'A small group gains low-cost expert answers');});
 put('tethers',0,0,[p('M326 470Q380 330 770 300',C.red,4),p('M536 480Q650 470 770 420',C.red,4)],'Each terminal depends on the provider’s infrastructure');
 ['infrastructure','user-a','user-b','user-a-device','user-b-device'].forEach(id=>show(id,2,450,700));
 show('tethers',2,2700,900);show('owner-crown',2,3900,700);gesture('user-a',2,'invite',900);express('user-b',2,'happy',900);express('user-a',2,'worried',4200);
 ['infrastructure','owner-crown','user-a','user-b','user-a-device','user-b-device','tethers'].forEach(id=>hide(id,3,100));
 // Beat 3: the cover's pedestal; a figure with its own provision can step away from it.
 put('pedestal',470,548,[rect(-170,-62,340,62,C.grey,4),rect(-124,-122,248,60,C.stone,4),rect(-78,-180,156,58,C.grey,4)],'A pedestal built from ordinary blocks');
 put('crown',470,346,[shape('M-52 22V-26L-26 0L0 -38L26 0L52 -26V22Z',C.red)],'The master raised by the pedestal');
 who('refuser',740,556,{identity:'person-10-neutral',scale:.6});
 put('provision',1000,548,[shape('M-62 0L-50 -40H50L62 0Z',C.slate),n('ellipse',{cx:-18,cy:-48,rx:26,ry:14,fill:C.bread}),n('ellipse',{cx:22,cy:-50,rx:24,ry:13,fill:C.ochre}),p('M66 -2L92 -118',C.slate,6),shape('M80 -122L108 -112L102 -96L74 -106Z',C.slate)],'Bread and tools of one’s own: refusal without starving');
 ['pedestal','crown','refuser'].forEach(id=>show(id,3,350,700));show('provision',3,1400,600);
 q.actions.push({actor:'refuser',action:'walkTo',x:900,beat:3,offsetMs:2000,durationMs:1700});gesture('refuser',3,'recoil',4000);express('refuser',3,'determined',3800);
 // Beat 4: the first chapter as a concrete starting point.
 const openBook=openBookVisual('$asset',{color:C.red});openBook.children[0].children=openBook.children[0].children.slice(0,3);
 put('chapter-one',218,236,[{...openBook,id:'$asset.book'},t('Chapter 1',-76,-22,20,C.ink),t('Antinomies Are',-76,6,17,C.ink),t('Not Accidents',-76,28,17,C.ink)],'The book open at chapter one, Antinomies Are Not Accidents',1.05);
 show('chapter-one',4,300,900);gesture('refuser',4,'invite',1200);express('refuser',4,'happy',900);
 return q.finish('A winner closes the market gate and noise buries a speaker; small terminals tether to one crowned infrastructure; then the cover pedestal returns while a figure with its own bread and tools steps away, and chapter one opens as the starting point.');
}
for(let i=0;i<scenes.length;i++)scenes[i].visual=compose(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
