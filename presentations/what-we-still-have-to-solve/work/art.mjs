import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#34465a',blue:'#75a8c5',deep:'#57799e',terra:'#d79071',gold:'#dfbd58',paper:'#f2ecdd',wood:'#b09779',mint:'#7fb2a3',lilac:'#b39abf',salt:'#bb769e'};
function setup(q){const{n,path,text,dot}=q;const rect=(x,y,w,h,fill,rx=5)=>n('rect',{x,y,width:w,height:h,fill,rx});const put=(id,x,y,ch,b=1,meaning=id)=>{q.add(q.object(id,x,y,ch,meaning));q.reveal(id,b,1100);};const person=(id,x,y,{identity='person-02-neutral',coat=C.blue,scale=.72,b=1,seated=false}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.lilac});q.reveal(id,b);};const mood=(id,b,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:1000});const delay=(id,action,offset)=>{q.actions.findLast(a=>a.actor===id&&a.action===action).offsetMs=offset;};const panel=(id,x,y,b=1)=>put(id,x,y,[n('path',{d:'M-71 -29H59L82 32H-51Z',fill:C.deep}),path('M-29 -29L-9 32M17 -29L38 32M-61 0H70',C.blue,3),path('M-45 34L-48 50M58 34L61 50',C.wood,7)],b,'A physical solar panel, not a complete energy system.');const house=(id,x,y,b=1,{fill=C.terra,scale=1}={})=>{q.add(q.object(id,x,y,[n('path',{d:'M-70 -61L0 -106L70 -61V43H-70Z',fill}),n('path',{d:'M-85 -60L0 -118L85 -60L72 -44L0 -92L-72 -44Z',fill:C.wood}),rect(-49,-45,40,36,C.paper),rect(17,-20,34,63,C.paper)],'An inhabited destination for a service, not a generic organization node.',scale));q.reveal(id,b);};return{rect,put,person,mood,delay,panel,house};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,delay,house}=setup(q);
 put('clinic-room',359,363,[rect(-279,-145,558,317,C.paper),rect(-279,153,558,19,C.wood),rect(-267,-133,88,45,C.mint),path('M-222 -126V-96M-237 -111H-207',C.paper,8)],1,'An ordinary hospital morning from the source’s explicitly imagined example; no medical outcomes are invented.');
 put('medicine-cabinet',170,377,[rect(-62,-112,124,213,C.blue),rect(-51,-95,102,177,'#dfedf0'),path('M-49 -29H49M-49 40H49',C.deep,4),...[-26,18].flatMap((x)=>[rect(x,-70,18,33,C.mint),rect(x,-77,18,9,C.paper),rect(x,-4,18,29,C.terra),rect(x,-11,18,9,C.paper)]),dot(51,0,4,C.ink)],1,'Refrigerated medicines make electricity a condition of an actual service.');
 person('clinician',342,532,{identity:'person-04-neutral',coat:C.mint,scale:.72});
 put('sink',555,469,[n('path',{d:'M-62 -6H63L42 23H-42Z',fill:C.blue}),path('M28 -9V-42H-5V-29',C.wood,8),path('M0 26V62',C.blue,12)],1,'Water enters the clinical workspace rather than remaining a disconnected label.');
 put('water-feed',663,423,[path('M-108 108H17V-94H143',C.blue,11)],1,'A physical service route crosses the institutional boundary.');
 put('cooling-unit',679,296,[rect(-45,-60,90,118,C.lilac),dot(0,-9,29,C.paper),path('M-22 -9H22M0 -31V13',C.blue,6),path('M-26 34H26M-26 45H26',C.ink,3)],1,'Cooling is powered from outside the hospital.');
 put('feeder',865,241,[path('M-141 43H78V-59M78 -59H220V36',C.gold,9)],1,'One feeder serves more than one local demand; no exact load or voltage is claimed.');
 house('neighbor',1063,365,1,{fill:C.terra,scale:.8});
 person('delivery-worker',854,530,{identity:'person-09-neutral',coat:C.gold,scale:.64,b:2});
 put('delivery-cart',956,486,[rect(-49,-36,99,46,C.wood),path('M-56 13H63V-50',C.ink,6),dot(-33,24,12,C.deep),dot(39,24,12,C.deep),rect(-31,-68,64,31,C.mint)],2,'Deliveries require people and logistics, rather than a decorative truck icon.');q.move('delivery-cart',2,765,486,2400);q.move('delivery-worker',2,697,530,2400);
 put('heat',1040,180,[dot(0,0,33,C.gold),path('M-65 70Q-77 83 -65 96M-26 70Q-38 83 -26 96M13 70Q1 83 13 96',C.terra,4)],3,'The source’s heat event strains health and cooling together; there is no depicted patient deterioration.');
 put('warm-air',780,296,[path('M-17 -28Q14 -10 -17 8M12 -12Q42 6 12 24',C.terra,4)],3,'Visible airflow makes cooling work legible without claiming a specific failure.');q.move('warm-air',3,814,296,2000);
 storyGesture(q,'clinician',2,'reflect');mood('clinician',3,'worried');storyGesture(q,'delivery-worker',3,'question');storyGesture(q,'clinician',4,'explain');mood('delivery-worker',5,'curious');
 scenes[0].visual=q.finish('A clinician, medicine refrigerator, sink and arriving delivery work within one inhabited hospital cutaway. Power and water visibly enter from outside; a nearby household shares demand during heat. The source’s imagined morning motivates examining connected services, with no actual health outcome or clinical instruction.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,delay,panel,house}=setup(q);
 put('land',600,520,[n('path',{d:'M-524 -11Q-217 -35 46 -8Q301 -27 510 -8L510 19H-524Z',fill:'#d9d9b6'})],1,'A single geographic service context prevents the equipment becoming unrelated floating symbols.');
 panel('panel-a',165,379);panel('panel-b',330,379);panel('panel-c',248,460);
 put('cost',243,224,[text('Production cost',0,-10,29,'$ink'),path('M0 11V54M-12 42L0 56L12 42',C.mint,6)],1,'Only the source’s qualitative reduction in generation cost is shown; no price or forecast is fabricated.');q.move('cost',1,243,241,2400);
 house('house-a',960,302,1,{fill:C.terra,scale:.83});house('house-b',1067,430,1,{fill:C.mint,scale:.7});
 put('grid-route',635,363,[path('M-224 17H-46M50 17H201V-22H278M201 17V98H358',C.gold,11),path('M-45 6V28M49 6V28',C.wood,5)],1,'The output route has a real unfinished connection between generation and household service.');
 put('trench',637,401,[n('path',{d:'M-69 -12L-50 34H47L69 -12Z',fill:C.wood}),n('path',{d:'M-50 -12L-36 18H34L49 -12Z',fill:C.ink}),text('Connection pending',0,-79,27,'$ink')],1,'The missing physical/institutional connection is the next binding constraint.');
 put('transformer-trailer',795,484,[rect(-58,-68,115,60,C.lilac),...[-33,-11,11,33].map(x=>path(`M${x} -55V-15`,C.paper,4)),path('M-47 -73V-88M32 -73V-88',C.wood,7),rect(-73,-6,144,17,C.wood),dot(-47,26,14,C.deep),dot(46,26,14,C.deep)],2,'A delivered transformer is one dependency, not a live-work repair procedure.');q.move('transformer-trailer',2,700,484,2200);
 person('crew',525,534,{identity:'person-09-neutral',coat:C.gold,scale:.52,b:2});person('planner',885,534,{identity:'person-04-neutral',coat:C.blue,scale:.52,b:2});
 put('approval',835,465,[rect(-64,-38,127,75,C.paper),text('Approval?',0,10,24,C.ink)],2,'Workable permits and coordination remain questions rather than an instantaneous approval.');
 put('household-cost',1035,191,[text('Household cost?',0,0,27,'$ink')],3,'Retail cost does not automatically follow generation cost; no particular tariff is asserted.');
 storyGesture(q,'planner',2,'question');storyGesture(q,'crew',3,'reflect');mood('planner',3,'worried');
 panel('extra-panel',417,461,4);storyGesture(q,'crew',4,'question');mood('crew',4,'curious');storyGesture(q,'planner',5,'explain');
 scenes[1].visual=q.finish('Production becomes cheaper in a solar field, but its route to actual homes ends at an unfinished interconnection. Equipment, crew and an unanswered approval are brought to that same site. An extra panel leaves the gap unresolved, making the moved constraint visible without a price statistic or universal tariff claim.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,delay}=setup(q);
 put('sea',171,375,[n('path',{d:'M-110 -97Q-67 -113 -22 -98Q25 -80 106 -100V166H-110Z',fill:C.blue}),path('M-79 -37Q-35 -55 10 -36M-51 57Q-7 39 57 59',C.paper,4)],1,'Seawater remains salt water; a separate process is needed.');
 put('separation-body',505,337,[rect(-180,-100,358,194,'#d8e9e9',25),path('M-175 37H173',C.blue,6),path('M-184 37H-260V104',C.blue,14),path('M174 -44H308V-94H355',C.blue,12),path('M-70 97V148H148',C.salt,11)],1,'A conceptual pressure-and-membrane process separates freshwater and concentrated brine, not a simple mesh sieve.');
 put('membrane',529,327,[rect(-12,-76,24,157,C.mint,1),text('Membrane',0,-98,29,'$ink')],2,'A continuous selective membrane, deliberately not ordinary holes that allegedly filter dissolved salt.');
 put('pressure-pump',304,418,[dot(0,0,27,C.deep),path('M-14 0H12M2 -10L14 0L2 10',C.paper,5)],2,'Pressure is represented conceptually; no operating settings or construction instructions.');
 put('salt-in-feed',435,309,[dot(-29,-15,7,C.salt),dot(22,12,7,C.salt),dot(-5,29,7,C.salt),dot(32,-23,7,C.salt)],2,'Dissolved salt is represented by small colored particles in the feed, not dirt caught by a sieve.');
 put('freshwater',578,309,[dot(-15,0,6,C.blue),dot(12,22,6,C.blue),dot(30,-16,6,C.blue)],2,'A few blue markers trace the freshwater side without a numerical purity claim.');q.move('freshwater',2,664,293,1300);q.move('freshwater',2,813,293,1200);delay('freshwater','moveTo',1700);q.move('freshwater',2,813,243,800);delay('freshwater','moveTo',3050);q.move('freshwater',2,883,243,800);delay('freshwater','moveTo',4000);
 put('tank',889,279,[rect(-59,-73,118,147,C.paper),rect(-47,-32,94,93,C.blue),n('ellipse',{cx:0,cy:-72,rx:59,ry:13,fill:C.mint}),text('Fresh water',0,-100,28,'$ink')],2,'Freshwater production creates a possible service, not automatic access.');
 put('brine-end',678,482,[path('M-25 0H44',C.salt,11),path('M-5 -12V12M17 -12V12',C.salt,3),text('Brine management?',0,48,27,'$ink')],3,'The brine route ends at an unresolved management question, not harmless dumping or a fabricated ecological disaster.');
 put('brine-trace',435,391,[dot(0,0,6,C.salt),dot(0,-12,5,C.salt)],3,'Concentrated salt stays on the feed side of the membrane and follows the separate unresolved brine route.');q.move('brine-trace',3,435,485,1300);q.move('brine-trace',3,678,482,2100);delay('brine-trace','moveTo',1700);
 put('distribution',1003,377,[path('M-114 -26V23H-25V80M-25 23H63',C.blue,11),path('M65 11V35',C.wood,7)],3,'A physical distribution branch ends before another household’s tap.');
 put('connected-tap',978,477,[path('M0 -39V-11H24V4',C.wood,9),path('M24 17V29',C.blue,5)],3,'One connected outlet demonstrates the difference between producing water and delivering it.');
 put('filled-container',1000,526,[n('path',{d:'M-25 -23H25L20 14H-20Z',fill:C.blue}),path('M-23 -23Q0 -46 23 -23',C.wood,3)],3,'A household service depends on more than the tank being full.');
 put('dry-tap',1098,455,[path('M0 61V-10H26V4',C.wood,9),path('M-16 61H20',C.wood,8)],4,'The unconnected tap remains dry; no reform is magically resolved.');
 person('resident',1152,535,{identity:'person-09-neutral',coat:C.gold,scale:.53,b:4});
 put('empty-container',1090,529,[n('path',{d:'M-26 -23H26L20 14H-20Z',fill:C.paper}),path('M-24 -23Q0 -46 24 -23',C.wood,3)],4,'An adult waiting for usable access, not a generic observer.');
 storyGesture(q,'resident',4,'question');mood('resident',4,'worried');storyGesture(q,'resident',5,'reflect');
 scenes[2].visual=q.finish('The source’s energy-to-water example becomes seawater intake, a continuous pressure-driven membrane, a freshwater tank, a separately unresolved brine-management path and unequal physical distribution. A full production tank coexists with a dry household tap. No efficacy, environmental outcome or access guarantee is invented.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,delay}=setup(q);
 put('full-tank',168,368,[rect(-63,-91,126,185,C.paper),rect(-52,-43,104,127,C.blue),n('ellipse',{cx:0,cy:-91,rx:63,ry:13,fill:C.mint}),text('Plant output',0,-119,29,'$ink')],1,'The production indicator is genuine but incomplete as a service outcome.');
 person('operator',348,535,{identity:'person-04-neutral',coat:C.blue,scale:.69});person('resident',1035,535,{identity:'person-09-neutral',coat:C.gold,scale:.69});
 put('dry-tap',933,461,[path('M-9 62V-28H21V-10',C.wood,9),path('M-28 63H15',C.wood,8)],1,'A real service gap supplies the feedback that the original output indicator omitted.');
 put('empty-container',937,532,[n('path',{d:'M-27 -22H27L20 12H-20Z',fill:C.paper}),path('M-25 -22Q0 -46 25 -22',C.wood,3)],1,'The resident has a concrete concern, without a clinical or political outcome being claimed.');
 put('review-map',645,337,[rect(-177,-132,354,266,C.paper),text('Service review',0,-89,29,C.ink),path('M-114 -30H-6V42H58',C.blue,8),rect(-131,-43,28,31,C.blue),n('path',{d:'M72 42L108 17L141 42V89H72Z',fill:C.terra})],1,'A map of the actual output and recipient becomes the shared object of review, not an abstract magnifying glass.');
 put('feedback',869,376,[rect(-61,-42,122,84,C.paper),path('M-27 21V-13H4V0',C.wood,6),text('Dry tap',20,30,24,C.ink)],2,'A resident’s observation enters the review record; it is not treated as automatically proving every explanation.');q.move('feedback',2,755,371,2100);storyGesture(q,'resident',2,'question');storyGesture(q,'operator',2,'reflect');
 put('planned-branch',645,337,[path('M59 42H101',C.gold,5),path('M66 31V53M84 31V53',C.paper,5),text('Proposed connection',0,118,25,C.ink)],2,'The newly visible missing branch becomes a testable proposal, not an instantaneous new pipe.');delay('planned-branch','appear',3000);q.hide('feedback',2);delay('feedback','disappear',2500);q.actions.findLast(a=>a.actor==='feedback'&&a.action==='disappear').durationMs=650;
 q.hide('full-tank',3);q.move('operator',3,123,535,1700);put('comparison',304,423,[rect(-124,-53,248,98,C.lilac),rect(-110,-43,220,76,C.paper),text('Output: present',0,-14,24,C.ink),text('Access: incomplete',0,19,23,C.ink),path('M0 45V61M-53 61H53',C.wood,9)],3,'An illustrative AI comparison widens feedback while people retain value judgments and authority; no actual deployed model is claimed.');
 mood('operator',3,'curious');storyGesture(q,'operator',3,'explain');
 for(const id of ['operator','dry-tap','empty-container','review-map','planned-branch','comparison'])q.hide(id,4);
 q.move('resident',4,207,535,2200);
 put('book',772,351,[n('path',{d:'M-253 -136Q-129 -158 0 -133Q133 -158 253 -136V143Q133 118 0 144Q-128 118 -253 143Z',fill:C.paper}),path('M0 -133V144',C.wood,4),text('Why solving one',-127,-76,27,C.ink),text('bottleneck',-127,-37,29,C.ink),text('reveals another',-127,2,27,C.ink),text('The corrigible',129,-70,29,C.ink),text('civilization',129,-29,30,C.ink),path('M-214 52H-44M-214 81H-71M42 30H217M42 61H175',C.blue,4)],4,'Actual source sections take the reader from a changing bottleneck into the larger framework of correctable institutions.');
 put('book-rest',772,516,[rect(-268,-12,536,18,C.wood)],4,'A readable source volume supports the invitation; no duplicated heading or production boilerplate.');
 storyGesture(q,'resident',4,'invite');mood('resident',5,'curious');
 scenes[3].visual=q.finish('A full production tank and dry household tap coexist. The resident’s evidence reaches a shared service map, a missing branch becomes a proposed connection, and an illustrative comparison distinguishes output from access. People retain authority; no instant reform appears. The same diagnostic gap earns the invitation to two real source sections.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
