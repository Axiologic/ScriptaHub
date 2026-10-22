// Book-owned staging for "Is There Light at the End of the Tunnel?".
// Rewrites only scene.visual; the reviewed spoken lines stay untouched.
import fs from 'node:fs';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
const file=new URL('./work/scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file,'utf8'));
// Cover palette: amber light, brick and near-black ink, plus the cover's slate and crimson arches.
const C={amber:'#f0b45a',brick:'#8c422d',ink:'#120f0e',crimson:'#6e2328',slate:'#3c4b5e',rust:'#c0673d',cream:'#fbecd0',stone:'#d9c6a5',mist:'#9fb0c2',deep:'#221a19'};
const NIGHT={ink:'#cdbba6',deep:'#283240',slate:'#7f93a8',crimson:'#9a3b3e',brick:'#b05a3f'};

function setup(q){
 const {n,path,text,dot}=q;
 const paint=(node,night)=>night?{...node,themeAttrs:{night:{[node.attrs.fill&&node.attrs.fill!=='none'?'fill':'stroke']:night}}}:node;
 const rect=(x,y,w,h,fill,rx=3,night)=>paint(n('rect',{x,y,width:w,height:h,fill,rx}),night);
 const shape=(d,fill,night)=>paint(n('path',{d,fill}),night);
 const line=(d,color,width=6,night)=>paint(path(d,color,width),night);
 const last=(id,action)=>q.actions.findLast(a=>a.actor===id&&a.action===action);
 const at=(id,action,offset)=>{if(offset!==undefined)last(id,action).offsetMs=offset;};
 const show=(id,beat,offset,ms=900)=>{q.reveal(id,beat,ms);at(id,'appear',offset);};
 const put=(id,x,y,kids,meaning,{beat,offset,scale=1}={})=>{q.add(q.object(id,x,y,kids,meaning,scale));if(beat)show(id,beat,offset);return id;};
 const hide=(ids,beat,offset=0)=>{for(const id of ids){q.hide(id,beat);at(id,'disappear',offset);}};
 const move=(id,beat,x,y,ms,offset)=>{q.move(id,beat,x,y,ms);at(id,'moveTo',offset);};
 const mood=(id,beat,emotion,offset=250)=>q.actions.push({actor:id,action:'character.express',emotion,beat,offsetMs:offset,durationMs:700});
 const gesture=(id,beat,kind,offset=250,ms=1700)=>{storyGesture(q,id,beat,kind,ms);last(id,'character.gesture').offsetMs=offset;};
 const person=(id,x,y,{identity='person-02-neutral',coat=C.slate,scale=.62,seated=false,chair=C.crimson,beat,offset}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair});if(beat)show(id,beat,offset);return id;};
 const label=(id,value,x,y,{beat,offset,size=28}={})=>put(id,x,y,[text(value,0,0,size,'$ink')],'Short stage label naming the object beneath it.',{beat,offset});
 // Round-topped tunnel arch, base at y=0.
 const arch=(w,h)=>{const r=w/2,s=h-r;return `M${-r} 0V${-s}A${r} ${r} 0 0 1 ${r} ${-s}V0Z`;};
 const bars=(w,h,color,night)=>{const r=w/2,s=h-r,xs=[-.66,-.33,0,.33,.66].map(f=>f*r);return xs.map(x=>line(`M${x} -4V${-(s+Math.sqrt(r*r-x*x))+8}`,color,7,night));};
 const pawn=(x,y,color,s=1,night)=>[paint(dot(x,y-62*s,14*s,color),night),shape(`M${x-17*s} ${y}L${x-11*s} ${y-44*s}Q${x} ${y-52*s} ${x+11*s} ${y-44*s}L${x+17*s} ${y}Z`,color,night)];
 return {n,path,text,dot,paint,rect,shape,line,show,put,hide,move,mood,gesture,person,label,arch,bars,pawn,at};
}

// Scene 1 · the exit that resembles the entrance; hidden caste; testimony as a source of questions.
{
 const q=stageAuthor(),A=setup(q),{rect,shape,line,text,dot,put,hide,move,mood,gesture,person,label,arch,bars,pawn,n}=A;
 put('ground',600,522,[rect(-470,0,940,10,C.brick,2,NIGHT.brick)],'One continuous road from the entrance to the promised exit.');
 put('entrance',230,522,[shape(arch(230,300),C.crimson,NIGHT.crimson),shape(arch(170,262),C.deep,NIGHT.deep),...bars(170,262,C.mist)],'The entrance: a barred arch standing for the dependence a system promised to end.');
 label('entrance-label','Dependence',230,194);
 put('exit',970,522,[shape(arch(230,300),C.rust),shape(arch(170,262),C.amber),n('ellipse',{cx:0,cy:-150,rx:46,ry:62,fill:C.cream})],'The promised exit, warm with the light of freedom.');
 label('exit-label','Promised freedom',970,194);
 person('traveller',400,526,{identity:'person-07-neutral',coat:C.slate,scale:.7});
 move('traveller',1,770,526,3000,300);
 put('exit-bars',970,522,bars(170,262,C.slate,NIGHT.slate),'The same bars reappear inside the exit: the new system rebuilds the old dependence.',{beat:1,offset:3500});
 mood('traveller',1,'worried',3700);gesture('traveller',1,'recoil',3900,1600);
 hide(['entrance','entrance-label','exit','exit-label','exit-bars','traveller'],2,0);
 // Equality on the floor can hide a raised tier; money climbs into a podium.
 put('raised-tier',360,322,[rect(-178,0,356,16,C.brick,2,NIGHT.brick),line('M-164 16V200M164 16V200',C.brick,8,NIGHT.brick),...pawn(-80,0,C.amber,1.15),...pawn(0,0,C.amber,1.15),...pawn(80,0,C.amber,1.15)],'A raised tier of privileged officials, kept above the equal citizens below.',{beat:2,offset:900});
 put('curtain',360,316,[rect(-190,-112,380,128,C.crimson,4,NIGHT.crimson),line('M-130 -104V8M-50 -104V8M30 -104V8M110 -104V8','#4f1a1e',4,'#6d2a2d')],'A curtain of proclaimed equality hides the tier.',{beat:2,offset:900});
 put('equal-row',360,522,[...[-124,-62,0,62,124].flatMap(x=>[rect(x-24,-26,48,26,C.stone,3),...pawn(x,-26,C.slate,.9,NIGHT.slate)])],'Citizens on equal plinths: incomes levelled.',{beat:2,offset:900});
 hide(['curtain'],2,2300);
 label('caste-label','Hidden caste',360,176,{beat:2,offset:2900});
 put('coins',700,522,[...[0,1,2,3,4].map(i=>n('ellipse',{cx:0,cy:-10-i*16,rx:34,ry:11,fill:i%2?C.amber:'#d99a3f'}))],'Economic reward from a free market.',{beat:2,offset:900});
 move('coins',2,780,522,1300,3000);
 put('step-1',900,522,[rect(-100,-38,200,38,C.brick,3,NIGHT.brick)],'First step of a political podium, built from money.',{beat:2,offset:3500});
 put('step-2',900,484,[rect(-72,-38,144,38,C.brick,3,NIGHT.brick)],'Second step of the podium.',{beat:2,offset:3900});
 put('lectern',900,446,[rect(-30,-62,60,62,C.rust,4),line('M-4 -62L-22 -92',C.slate,5,NIGHT.slate),dot(-24,-96,7,C.slate)],'A lectern and microphone: political voice purchased with wealth.',{beat:2,offset:4300});
 hide(['coins'],2,4400);
 label('power-label','Bought influence',900,300,{beat:2,offset:4500});
 hide(['raised-tier','equal-row','caste-label','step-1','step-2','lectern','power-label'],3,0);
 // Testimony: a remembered experience raises questions; it is not offered as proof.
 person('witness',420,528,{identity:'person-12-neutral',coat:C.slate,scale:.64,seated:true,chair:C.crimson,beat:3,offset:900});
 put('notebook',438,452,[n('path',{d:'M-46 -30Q-22 -38 0 -28Q22 -38 46 -30V22Q22 14 0 24Q-22 14 -46 22Z',fill:C.cream}),line('M0 -28V24',C.brick,3),line('M-36 -14H-10M-36 -2H-12M12 -14H36M12 -2H32',C.slate,2.5)],'The initiator’s notebook of lived experience under communism, held open on his lap.',{beat:3,offset:1200,scale:.72});
 put('memory',760,236,[n('path',{d:'M-170 40Q-200 -20 -140 -46Q-130 -110 -50 -100Q0 -150 70 -108Q150 -120 160 -50Q210 -10 178 52Q160 120 60 112Q0 138 -70 114Q-170 126 -170 40Z',fill:C.cream}),rect(-120,-56,70,110,C.mist,2),rect(-40,-80,80,134,'#8496aa',2),rect(50,-40,70,94,C.mist,2),...[-104,-82,-24,0,20,66,92].flatMap(x=>[-36,-6,24].map(y=>rect(x,y,12,14,C.cream,1))),line('M-150 54H150',C.slate,4),text('Testimony',0,86,26,C.ink)],'A remembered city of grey housing blocks: testimony, not a representative sample.',{beat:3,offset:1800,scale:.85});
 put('thought-dots',500,330,[dot(0,0,8,C.stone),dot(30,-24,12,C.stone)],'The memory belongs to the witness.',{beat:3,offset:1600});
 for(const [i,[x,y]] of [[650,440],[705,415],[760,440]].entries()){const id='question-'+(i+1);put(id,x,y,[text('?',0,0,52,C.rust)],'A question raised by the testimony, still open for evidence.',{beat:3,offset:3000+i*450});move(id,3,x+24,y-28,1300,3300+i*450);}
 gesture('witness',3,'reflect',1400,1800);mood('witness',3,'skeptical',3400);
 scenes[0].visual=q.finish('A traveller walks from a barred entrance toward a warm promised exit and finds the same bars inside it. Then a curtain of equality lifts from a raised tier, and coins climb into a political podium. Finally a seated witness opens a notebook beside a remembered grey city; question marks rise from it as testimony rather than proof.');
}

// Scene 2 · an office interior: who can compel and replace whom, convertible privilege, rewritten rules, graded evidence.
{
 const q=stageAuthor(),A=setup(q),{rect,shape,line,text,dot,put,hide,move,mood,gesture,person,label,arch,n}=A;
 put('floor',600,522,[rect(-470,0,940,10,C.slate,2,NIGHT.slate)],'The floor of a public institution.');
 put('dais',330,522,[rect(-150,-34,300,34,C.brick,3,NIGHT.brick),rect(-110,-62,220,30,C.crimson,3,NIGHT.crimson)],'A raised dais: the seat of office.');
 person('occupant',330,466,{identity:'person-04-neutral',coat:C.crimson,scale:.6,seated:true,chair:C.amber});
 put('door',1000,522,[shape(arch(170,290),C.deep,NIGHT.deep),shape(arch(130,262),C.amber),n('ellipse',{cx:0,cy:-140,rx:34,ry:54,fill:C.cream})],'An open door to the office: the route by which a challenger can enter.');
 person('challenger',860,526,{identity:'person-09-neutral',coat:C.rust,scale:.6});
 label('compel-label','Who compels whom?',600,176,{beat:1,offset:400});
 move('challenger',1,700,526,2200,1800);
 q.connections.push({id:'replace-link',from:{node:'occupant',anchor:'right'},to:{node:'challenger',anchor:'left'},width:4,color:C.rust,bend:-60,meaning:'The open question: can the challenger peacefully replace the occupant?'});q.actions.push({actor:'replace-link',action:'connection.draw',beat:1,offsetMs:4300,durationMs:1100});gesture('challenger',1,'question',4700,1500);gesture('occupant',1,'recoil',5000,1500);
 hide(['compel-label','replace-link'],2,0);
 // Four forms of privilege, each convertible into the next.
 const token=(id,x,kids,name,meaning,offset)=>put(id,x,168,[dot(0,0,44,C.cream),...kids,text(name,0,76,26,'$ink')],meaning,{beat:2,offset});
 token('office',170,[shape('M-6 -26A14 14 0 1 1 6 -26L6 22L14 22L14 30L-6 30Z',C.brick),dot(0,-14,5,C.cream)],'Office','Privilege held as office: a key to authority.',400);
 token('career',360,[line('M-16 -28V30M16 -28V30M-16 -14H16M-16 4H16M-16 22H16',C.slate,5)],'Careers','Privilege held as control over careers: a promotion ladder.',1300);
 token('information',550,[rect(-22,-28,44,56,'#ffffff',3),line('M-12 -12H12M-12 0H12M-12 12H4',C.slate,3)],'Information','Privilege held as access to information: a restricted file.',2200);
 token('status',740,[dot(0,8,18,C.amber),shape('M-12 -30H12L6 -8H-6Z',C.crimson)],'Status','Privilege held as symbolic status: a medal.',3100);
 const convert=(id,a,b,offset)=>{q.connections.push({id,from:{node:a,anchor:'right'},to:{node:b,anchor:'left'},width:4,color:C.rust,bend:-34,meaning:'One form of privilege converts into the next.'});q.actions.push({actor:id,action:'connection.draw',beat:2,offsetMs:offset,durationMs:900});};
 for(const id of ['office','career','information','status'])q.objects.find(o=>o.id===id).visual.anchors={left:[-50,0],right:[50,0],top:[0,-50],bottom:[0,50]};
 convert('office-career','office','career',2000);convert('career-information','career','information',2900);convert('information-status','information','status',3800);
 gesture('occupant',2,'explain',800,1800);
 hide(['office','career','information','status','office-career','career-information','information-status'],3,0);
 // A winner rewrites the rules and the open door narrows.
 put('rulebook',600,522,[rect(-12,-96,24,96,C.brick,2,NIGHT.brick),rect(-80,-140,160,52,C.cream,4),text('Rules',0,-106,24,C.ink)],'The rules of competition, written on a public lectern.',{beat:3,offset:300});
 label('winner-label','Winner',330,232,{beat:3,offset:300});
 put('reward',600,500,[...[0,1,2].map(i=>n('ellipse',{cx:0,cy:-i*13,rx:26,ry:9,fill:i%2?'#d99a3f':C.amber}))],'Market reward collected by the winner.',{beat:3,offset:600});
 move('reward',3,410,458,1400,1200);gesture('occupant',3,'explain',2500,1700);
 put('rewrite',600,410,[line('M-40 0H40',C.crimson,5),line('M48 -6L74 -34',C.crimson,5)],'The winner’s mark rewrites the rules.',{beat:3,offset:3000});
 put('narrowing',1000,522,[shape('M-65 0V-188L-28 -200V0Z',C.crimson,NIGHT.crimson),shape('M65 0V-188L28 -200V0Z',C.crimson,NIGHT.crimson)],'The doorway narrows: entry and replacement become harder.',{beat:3,offset:3500});
 move('challenger',3,850,526,1400,3600);mood('challenger',3,'worried',3700);
 hide(['dais','occupant','door','challenger','rulebook','reward','rewrite','narrowing','winner-label'],4,0);
 // Reader lens: three kinds of claim kept apart, then weighed.
 const tray=(id,x,kids,name,meaning,offset)=>put(id,x,290,[rect(-120,-100,240,190,C.cream,8),...kids,text(name,0,128,26,'$ink')],meaning,{beat:4,offset});
 tray('findings',260,[rect(-70,-70,140,120,'#ffffff',4),line('M-50 -40H50M-50 -18H50M-50 4H30',C.slate,4),text('[1]',36,34,22,C.brick)],'Findings','Cited findings: published results with references.',1300);
 tray('mechanisms',600,[dot(-24,-10,34,C.slate),dot(-24,-10,13,C.cream),dot(34,30,24,C.rust),dot(34,30,9,C.cream),line('M-24 -54V-44M-24 24V34M-68 -10H-58M10 -10H20M34 -4V2M34 58V64M6 30H12M58 30H64',C.slate,8)],'Mechanisms','Possible mechanisms: explanations still to be tested.',1800);
 tray('proposals',940,[rect(-76,-70,152,124,'#4f6b8c',4),line('M-52 -40H52M-52 30H52M-52 -40V30M52 -40V30M-52 -6H52M0 -40V30',C.cream,2.5)],'Proposals','Working proposals: designs offered for testing.',2300);
 put('balance',600,522,[line('M0 0V-50M-60 0H60',C.ink,6,NIGHT.ink),line('M-110 -58H110',C.ink,6,NIGHT.ink),line('M-110 -58L-130 -30M-110 -58L-90 -30M110 -58L90 -30M110 -58L130 -30',C.ink,3,NIGHT.ink),shape('M-136 -30H-84Q-110 -14 -136 -30Z',C.amber),shape('M84 -30H136Q110 -14 84 -30Z',C.amber)],'A balance: the reader weighs each kind of claim separately.',{beat:4,offset:3000,scale:1.35});
 scenes[1].visual=q.finish('Inside an office, an occupant sits on a dais while a challenger approaches through an open door. Four forms of privilege, office, careers, information and status, appear and convert into one another. The winner places market reward on the rule lectern, marks the rules and the doorway narrows. Finally findings, mechanisms and proposals stand in separate trays above a balance for the reader.');
}

// Scene 3 · cosmolocal institutions, a test of ownership and voice, modest light, and the reading invitation.
{
 const q=stageAuthor(),A=setup(q),{rect,shape,line,text,dot,put,hide,move,mood,gesture,person,label,arch,n}=A;
 put('globe',600,206,[dot(0,0,72,'#4f6b8c'),n('ellipse',{cx:0,cy:0,rx:30,ry:72,fill:'none',stroke:C.amber,'stroke-width':4}),line('M-72 0H72M-62 -36H62M-62 36H62',C.amber,3)],'Knowledge that circulates globally.');
 const workshop=(id,x,tool,meaning,offset)=>put(id,x,522,[rect(-80,-100,160,100,C.stone,3),shape('M-92 -100L0 -150L92 -100Z',C.brick,NIGHT.brick),rect(-26,-62,52,62,C.slate,2,NIGHT.slate),...tool],meaning,offset?{beat:1,offset}:{});
 workshop('workshop-1',240,[dot(52,-62,14,C.amber),dot(52,-62,5,C.slate)],'A local workshop with its own productive tools.');
 workshop('workshop-2',600,[rect(38,-74,26,20,C.amber,2)],'A second local workshop: capacities are distributed.');
 workshop('workshop-3',960,[line('M40 -78L62 -50',C.amber,6)],'A third local workshop: no single centre owns production.');
 for(const id of ['workshop-1','workshop-2','workshop-3'])q.objects.find(o=>o.id===id).visual.anchors={left:[-80,-50],right:[80,-50],top:[0,-152],bottom:[0,0]};
 q.objects.find(o=>o.id==='globe').visual.anchors={left:[-72,0],right:[72,0],top:[0,-72],bottom:[0,72]};
 for(const [i,[id,anchor]] of [['workshop-1','left'],['workshop-2','bottom'],['workshop-3','right']].entries()){const cid='knowledge-'+(i+1);q.connections.push({id:cid,from:{node:'globe',anchor},to:{node:id,anchor:'top'},width:4,color:C.amber,meaning:'Knowledge flows from the global commons to each local workshop.'});q.actions.push({actor:cid,action:'connection.draw',beat:1,offsetMs:900+i*500,durationMs:1100});}
 const shield=(id,x,offset)=>put(id,x,452,[shape('M-20 -24H20V2Q20 20 0 30Q-20 20 -20 2Z',C.amber),line('M-8 2L-2 10L10 -8',C.ink,4)],'Rights guaranteed by a common charter, not by local goodwill.',{beat:1,offset});
 shield('right-1',240,3900);shield('right-2',600,4300);shield('right-3',960,4700);
 hide(['globe','workshop-1','workshop-2','workshop-3','knowledge-1','knowledge-2','knowledge-3','right-1','right-2','right-3'],2,0);
 // AI and basic income tested by ownership, control and voice.
 person('owner',330,500,{identity:'person-02-neutral',coat:C.slate,scale:.58,beat:2,offset:700});
 person('controller',600,500,{identity:'person-15-neutral',coat:C.rust,scale:.58,beat:2,offset:700});
 person('speaker',870,500,{identity:'person-20-neutral',coat:C.crimson,scale:.58,beat:2,offset:700});
 put('table',600,522,[rect(-290,-74,580,74,C.crimson,3,NIGHT.crimson),rect(-300,-92,600,20,C.brick,3,NIGHT.brick)],'A public test counter in front of three citizens, hiding their legs so they clearly stand behind it.',{beat:2,offset:700});
 put('ai-chip',465,392,[rect(-36,-36,72,72,C.slate,8,NIGHT.slate),rect(-22,-22,44,44,C.amber,4),text('AI',0,9,22,C.ink),line('M-20 -36V-46M0 -36V-46M20 -36V-46M-20 36V44M0 36V44M20 36V44',C.slate,4,NIGHT.slate)],'Artificial intelligence on the test table.',{beat:2,offset:900});
 put('income',735,402,[dot(0,-6,28,C.amber),dot(0,-6,19,'#d99a3f'),text('Income',0,-46,22,'$ink')],'A basic income on the test table.',{beat:2,offset:900});
 const tag=(id,x,kids,name,meaning,offset)=>{put(id,x,170,kids,meaning,{beat:2,offset,scale:1.35});label(id+'-label',name,x,262,{beat:2,offset,size:26});};
 tag('owns',330,[rect(-26,-30,52,62,C.cream,3),line('M-14 -14H14M-14 0H14M-14 14H6',C.brick,3)],'Who owns?','Who owns the infrastructure: a title deed.',2000);
 tag('controls',600,[rect(-30,8,60,18,C.slate,4,NIGHT.slate),line('M0 14L18 -26',C.slate,6,NIGHT.slate),dot(18,-28,9,C.amber)],'Who controls?','Who controls it: a control lever.',2900);
 tag('speaks',870,[n('path',{d:'M-34 -28H34V16H-6L-22 30V16H-34Z',fill:C.cream}),line('M-20 -12H20M-20 2H10',C.slate,3)],'Who speaks?','Who has political voice: a speech bubble.',3800);
 gesture('speaker',2,'question',4000,1500);
 hide(['owner','controller','speaker','table','ai-chip','income','owns','controls','speaks','owns-label','controls-label','speaks-label'],3,0);
 // Modest light: nested arches open onto a correction loop and peaceful replacement.
 const rings=[[620,520,C.crimson,NIGHT.crimson],[520,440,C.slate,NIGHT.slate],[430,370,C.rust],[340,300,'#d98a4f'],[250,230,C.amber]];
 put('tunnel',600,522,[...rings.map(([w,h,c,night])=>shape(arch(w,h),c,night)),n('ellipse',{cx:0,cy:-150,rx:58,ry:68,fill:C.cream}),shape('M-40 0L-14 -86H14L40 0Z',C.cream)],'Nested tunnel arches narrowing toward a small, warm opening.',{beat:3,offset:500,scale:.66});
 put('error',880,250,[dot(0,0,32,C.cream),line('M-12 -12L12 12M12 -12L-12 12',C.crimson,7)],'An error, noticed rather than hidden.',{beat:3,offset:1500});
 hide(['error'],3,2800);
 put('record',880,250,[rect(-30,-38,60,76,C.cream,4),line('M-16 -18H16M-16 -4H16M-16 10H8',C.slate,3)],'The error becomes information in a public record.',{beat:3,offset:3000});
 person('outgoing',220,526,{identity:'person-04-neutral',coat:C.crimson,scale:.56,beat:3,offset:800});
 person('incoming',1000,526,{identity:'person-09-neutral',coat:C.rust,scale:.56,beat:3,offset:800});
 put('key',290,420,[line('M2 0H34M24 0V12M32 0V10',C.ink,11,NIGHT.deep),A.paint(dot(-10,0,15,C.ink),NIGHT.deep),A.paint(dot(-10,0,12,C.brick),NIGHT.brick),dot(-10,0,5,C.cream),line('M2 0H34M24 0V12M32 0V10',C.brick,6,NIGHT.brick)],'The key of office passes peacefully to a successor.',{beat:3,offset:1000});
 move('key',3,600,140,1200,3600);move('key',3,930,420,1200,4800);gesture('outgoing',3,'release',3400,1500);gesture('incoming',3,'invite',5600,1400);
 hide(['tunnel','record','outgoing','incoming','key'],4,0);
 // The book itself: where to begin and what to test.
 put('book',640,350,[n('path',{d:'M-330 -150Q-160 -176 0 -136Q160 -176 330 -150V170Q160 144 0 184Q-160 144 -330 170Z',fill:C.cream}),line('M0 -136V184',C.brick,4),text('When the Exit',-165,-62,30,C.ink),text('Resembles',-165,-24,30,C.ink),text('the Entrance',-165,14,30,C.ink),line('M-260 58H-70M-260 82H-90M-260 106H-80',C.stone,4),text('Ten clauses',165,-96,28,C.ink)],'The open book: its introduction on the left, the ten constitutional clauses to test on the right.',{beat:4,offset:300});
 const clause=(i)=>{const col=i<5?0:1,row=i%5,x=640+92+col*130,y=350-58+row*42;return [x,y];};
 for(let i=0;i<10;i++){const [x,y]=clause(i);put('clause-'+(i+1),x,y,[rect(-14,-14,28,28,'#ffffff',4),line('M22 0H82',C.stone,4)],'One of the ten clauses, open for the reader to test.',{beat:4,offset:800});
  put('check-'+(i+1),x,y,[line('M-8 0L-2 7L10 -8',C.brick,4)],'A clause the reader has tested.',{beat:4,offset:2200+i*260});}
 put('bookmark',490,206,[shape('M-14 -24H14V30L0 18L-14 30Z',C.crimson)],'Bookmark at the introduction, the suggested starting point.',{beat:4,offset:1200});
 person('reader',170,526,{identity:'person-07-neutral',coat:C.slate,scale:.62,beat:4,offset:1200});
 mood('reader',4,'happy',1200);gesture('reader',4,'invite',1700,3400);
 scenes[2].visual=q.finish('Knowledge flows from a global commons to three local workshops, each protected by a common charter. Three citizens stand behind a table holding AI and a basic income while ownership, control and voice are tested. Nested cover arches open toward a modest light where an error becomes a record and the key of office passes peacefully. The film ends at the open book, marking the introduction and ten clauses to test.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('Wrote visual staging for',scenes.length,'scenes.');
