import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#314a63',blue:'#5f91ad',teal:'#569a93',coral:'#cf856f',gold:'#dbb75b',paper:'#efe7d7',earth:'#ad8968',leaf:'#80a577',plum:'#9e82a0'};
function setup(q){const{n,path,text,dot}=q;const rect=(x,y,w,h,fill,rx=5)=>n('rect',{x,y,width:w,height:h,fill,rx});const put=(id,x,y,children,b=1,meaning=id)=>{q.add(q.object(id,x,y,children,meaning));q.reveal(id,b,1100);};const person=(id,x,y,{identity='person-04-neutral',coat=C.teal,scale=.83,b=1,seated=false}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.blue});q.reveal(id,b);};const mood=(id,b,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:1000});
 const crop=(x,y,fill=C.leaf)=>[path(`M${x} ${y}V${y-45}`,fill,4),n('path',{d:`M${x} ${y-22}Q${x-32} ${y-49} ${x-34} ${y-21}Q${x-16} ${y-7} ${x} ${y-13}M${x} ${y-35}Q${x+29} ${y-60} ${x+28} ${y-34}Q${x+14} ${y-19} ${x} ${y-25}`,fill})];
 const sack=(x,y,fill=C.gold)=>[n('path',{d:`M${x-15} ${y-43}L${x+15} ${y-43}Q${x+11} ${y-27} ${x+28} ${y-9}Q${x+34} ${y+22} ${x+20} ${y+25}H${x-20}Q${x-34} ${y+22} ${x-28} ${y-9}Q${x-11} ${y-27} ${x-15} ${y-43}Z`,fill}),path(`M${x-14} ${y-32}H${x+14}`,C.earth,3)];
 const truck=(id,x,y,b=1)=>put(id,x,y,[rect(-78,-68,119,64,C.blue),n('path',{d:'M41 -49H76L100 -22V-4H41Z',fill:C.coral}),rect(48,-43,23,22,C.paper,2),path('M-86 1H104',C.ink,7),dot(-48,5,15,C.ink),dot(72,5,15,C.ink),dot(-48,5,6,C.paper),dot(72,5,6,C.paper)],b,'A food transport vehicle; its movement represents a functioning distribution route.');
 return{rect,put,person,mood,crop,sack,truck};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,crop}=setup(q);
 put('cultivated-ground',369,476,[n('path',{d:'M-187 -45L118 -71L192 35L-138 51Z',fill:C.earth}),...[-92,-5,82].flatMap(x=>crop(x,-10)),path('M-126 17L134 -5',C.paper,3)],1,'A working food plot is a retained capability, not a generic house or icon.');
 person('grower',193,525,{coat:C.gold,scale:.76});put('watering-can',273,441,[rect(-19,-23,42,41,C.blue),path('M20 -14L57 -30M-19 -16Q-54 -21 -39 13H-19',C.blue,8)],1,'The grower continues ordinary maintenance.');
 put('lathe',969,433,[rect(-146,-48,293,36,C.teal),rect(-125,-114,48,71,C.blue),dot(-77,-77,27,C.ink),path('M-51 -77H76',C.earth,13),n('path',{d:'M77 -100H125V-46H77Z',fill:C.coral}),rect(-122,-12,24,98,C.earth),rect(94,-12,24,98,C.earth),rect(-47,-38,50,38,C.gold),path('M-23 -29V-78',C.ink,5)],1,'A maintained machine shop carries practical production capacity. The mechanism is illustrative, not a machining tutorial.');
 person('maker',792,525,{identity:'person-09-neutral',coat:C.coral,scale:.76});
 put('transport-link',642,460,[path('M-73 28L-12 -5L63 23',C.blue,12),path('M-11 -10L-3 7L-18 15L-6 28',C.paper,9)],2,'A disrupted route separates the two sites without erasing every local capacity.');
 put('spare-work',1092,266,[rect(-68,-15,135,13,C.earth),dot(-35,-39,22,C.gold),dot(-35,-39,9,C.paper),rect(1,-61,37,46,C.blue)],2,'Tools and spare components are retained at the workshop, not assumed universal independence.');
 storyGesture(q,'grower',1,'reflect');storyGesture(q,'maker',2,'explain');mood('grower',3,'curious');storyGesture(q,'grower',3,'resolve');storyGesture(q,'maker',3,'resolve');
 q.label('food-label','Food still grows',393,301,30);q.reveal('food-label',3);q.label('work-label','Skills and tools remain',930,195,30);q.reveal('work-label',3);
 scenes[0].visual=q.finish('Two working sites retain distinct food and repair capabilities despite a disrupted link. This illustrates the book’s conditional distributed-capability argument without claiming all failures are isolated or catastrophe harmless.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,crop,sack,truck}=setup(q);
 put('distant-city',171,332,[rect(-100,-61,49,61,C.blue,0),rect(-42,-108,43,108,C.plum,0),rect(10,-79,52,79,C.blue,0),rect(70,-45,37,45,C.coral,0),...[-86,-70].flatMap(x=>[-43,-21].map(y=>rect(x,y,7,10,C.paper,0))),...[-30,-14].flatMap(x=>[-87,-63,-39,-15].map(y=>rect(x,y,7,10,C.paper,0))),...[23,43].flatMap(x=>[-59,-36,-13].map(y=>rect(x,y,8,11,C.paper,0))),path('M-18 -108V-127',C.ink,3),path('M-107 5H120',C.ink,3)],1,'A distant affected city provides non-graphic context; no count or magnitude is encoded.');
 put('smoke-rise',253,219,[n('path',{d:'M-85 29Q-83 -25 -28 -40Q25 -52 130 -30L130 -14Q22 -36 -21 -18Q-62 -2 -61 29Z',fill:C.plum})],2,'A plume carries smoke from the affected city into the atmospheric layer; it does not encode a scale.');
 put('soot',233,204,[n('path',{d:'M-82 26Q-137 -13 -88 -26Q-89 -61 -34 -45Q-3 -79 37 -46Q90 -70 102 -29Q151 -22 121 16Q44 42 -82 26Z',fill:C.ink})],2,'Atmospheric soot is the conditional mechanism, not a decorative cloud.');q.move('soot',2,471,200,3100);
 put('light',485,275,[path('M-64 -38L-90 36M1 -38L-6 36M67 -38L84 36',C.gold,8)],1,'Incoming sunlight reaches the agricultural region before the conditional reduction.');q.hide('light',2);
 put('field',483,450,[n('path',{d:'M-144 -15L105 -35L156 61L-124 75Z',fill:C.earth}),...[-74,7,87].flatMap(x=>crop(x,19)),...sack(143,-32)],1,'An agricultural region far from combat can lose production through reduced sunlight.');
 put('crop-loss',483,450,[n('path',{d:'M-144 -15L105 -35L156 61L-124 75Z',fill:C.earth}),...[-74,7,87].flatMap(x=>[path(`M${x} 19V-4Q${x-16} -16 ${x-29} 0`,C.gold,4)]),...sack(143,-32,C.paper)],2,'Reduced crops and an unfilled sack are qualitative illustrations, not measured crop loss.');q.hide('field',2);
 put('warehouse',943,388,[n('path',{d:'M-123 -85L0 -151L122 -85V114H-123Z',fill:C.teal}),rect(-89,-63,178,177,C.paper,0),path('M-136 -81L0 -161L136 -81',C.earth,11),...[-47,26].flatMap(x=>sack(x,66))],3,'An actual grain store, with maintained distribution rather than a magical archive box.');
 truck('delivery',713,513,3);put('blocked-route',816,511,[path('M-16 -23L18 3M-16 3L18 -23',C.coral,8)],3,'Trade and transport interruption prevent available food reaching people.');
 person('recipient',1174,524,{identity:'person-12-neutral',coat:C.plum,scale:.7,b:3});mood('recipient',3,'worried');
 person('clerk',891,498,{identity:'person-09-neutral',coat:C.gold,scale:.59,b:4});put('inventory',952,428,[rect(-32,-41,64,83,C.paper),path('M-19 -21H19M-19 -3H19M-19 15H8',C.ink,3)],4,'The clerk checks stored grain before dispatch, embodying the book’s institutional coordination example.');
 q.hide('blocked-route',4);q.move('delivery',4,1075,513,3400);storyGesture(q,'clerk',4,'resolve');storyGesture(q,'recipient',5,'question');
 q.label('scope','A surviving distribution route',837,174,30);q.reveal('scope',5);
 scenes[1].visual=q.finish('Conditional nuclear soot reduces sunlight over distant crops; disrupted transport blocks food before a surviving warehouse and clerk organize one usable route. Damaged crops remain. No extinction forecast, universal recovery, invented scale or substitution of resilience for prevention.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood}=setup(q);
 const transformer=(id,x,y,b,colour)=>put(id,x,y,[rect(-58,-75,116,141,colour,10),...[-34,-12,12,34].map(xx=>path(`M${xx} -61V51`,C.paper,4)),rect(-68,66,136,15,C.earth),...[-29,29].flatMap(xx=>[rect(xx-10,-116,20,43,C.ink,3),dot(xx,-118,14,C.gold)])],b,'A sealed transformer represents maintained replaceable equipment; no live-work procedure, wiring or repair instruction is depicted.');
 person('technician',219,529,{identity:'person-04-neutral',coat:C.blue,scale:.87});
 transformer('failed-unit',484,431,1,C.plum);put('failure-tag',486,293,[rect(-77,-25,154,50,C.coral),text('Out of service',0,8,23,C.ink)],1,'A failed component remains unavailable even though a manual survives.');
 put('manual',305,392,[n('path',{d:'M-55 -47Q-28 -56 0 -42Q27 -56 55 -47V48Q26 36 0 48Q-26 36 -55 48Z',fill:C.paper}),path('M0 -43V46M-42 -19H-11M12 -19H42M-42 5H-11M12 5H42',C.earth,3)],1,'Stored instructions alone do not restore the component.');
 storyGesture(q,'technician',1,'question');mood('technician',2,'worried');
 put('spare-bay',831,460,[rect(-89,53,178,15,C.earth),path('M-78 65V79M77 65V79',C.earth,8)],3,'Kept spare capacity existed before the disruption; it is not conjured by reading.');
 transformer('kept-spare',831,425,3,C.teal);q.label('spare-label','Maintained spare',831,216,30);q.reveal('spare-label',3);
 person('second-crew',651,533,{identity:'person-09-neutral',coat:C.coral,scale:.83,b:4});storyGesture(q,'second-crew',4,'resolve');
 q.hide('spare-label',4);q.hide('failed-unit',4);q.hide('failure-tag',4);q.move('kept-spare',4,484,431,3400);
 put('pump',1110,415,[rect(-56,-14,94,75,C.blue),dot(-42,20,31,C.ink),dot(-42,20,16,C.paper),path('M13 -15V-76H68V-49',C.teal,18),path('M-43 51V101M26 61V101',C.earth,10)],1,'A water pump represents one essential service depending on restored equipment; this is a conceptual capability chain.');
 put('water',1178,448,[path('M0 -76V4',C.blue,9),n('path',{d:'M-21 16Q0 4 20 16L31 65H-32Z',fill:C.paper}),path('M-22 51H22',C.blue,9)],4,'One service can resume when knowledge, trained crews and usable equipment are available.');q.actions.find(x=>x.actor==='water'&&x.action==='appear').offsetMs=3600;
 storyGesture(q,'technician',5,'explain');q.label('cost','Capacity kept before the emergency',751,168,30);q.reveal('cost',5);
 scenes[2].visual=q.finish('A paper manual cannot fix unavailable infrastructure. A maintained spare and two trained crew members make restoration of one conceptual water-service chain possible. The scene presents no electrical procedure, quantitative result, automatic recovery, or claim that a spare resolves all systemic dependencies.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood}=setup(q);
 person('resident',233,528,{coat:C.coral,scale:.86});person('official',807,514,{identity:'person-02-neutral',coat:C.blue,scale:.85,seated:true});
 put('hearing-table',719,467,[rect(-168,-15,339,24,C.earth),path('M-142 8V69M142 8V69',C.earth,10)],1,'A public hearing is an institutional choice, not a consequence guaranteed by physical recovery.');
 put('working-tap',1107,435,[path('M-34 59V-64H31V-36',C.teal,15),path('M31 -30V20',C.blue,5),n('path',{d:'M5 25H58L52 63H11Z',fill:C.paper}),path('M12 47H51',C.blue,6)],1,'Essential service continues while political authority can still become less accountable.');
 put('resident-report',328,400,[rect(-47,-59,94,116,C.paper),text('Report',0,-22,23,C.ink),path('M-28 2H28M-28 21H17',C.coral,4)],1,'An affected resident has an observed problem to raise.');storyGesture(q,'resident',1,'question');
 put('emergency-order',656,226,[rect(-177,-67,354,136,C.paper),text('Emergency order',0,-16,31,C.ink),text('Review suspended',0,29,27,C.ink)],2,'Illustrative institutional hardening; it is not a quote from a real order or a claim that every emergency suspends rights.');
 mood('resident',2,'worried');storyGesture(q,'official',2,'reflect');
 q.hide('emergency-order',3);storyGesture(q,'official',3,'invite');q.move('resident-report',3,647,405,2700);
 person('second-resident',421,530,{identity:'person-09-neutral',coat:C.gold,scale:.82,b:4});storyGesture(q,'second-resident',4,'question');
 put('public-record',788,398,[rect(-83,-52,166,102,C.paper),path('M-65 -20H62M-65 3H62M-65 25H37',C.blue,4),rect(-89,-52,14,102,C.teal)],4,'Evidence enters an accessible record and another resident can speak; an illustrated alternative, not a forecast of democratic reform.');
 for(const id of ['official','hearing-table','working-tap','resident-report','second-resident','public-record'])q.hide(id,5);
 put('reading-table',826,471,[rect(-281,-9,562,21,C.earth),path('M-247 12V64M247 12V64',C.earth,10)],5,'A reader now examines the book’s categories and the chapter that developed the illustrated case.');
 put('reading-spread',826,355,[n('path',{d:'M-274 -138Q-126 -157 0 -136Q133 -157 274 -138V115Q133 95 0 117Q-128 95 -274 115Z',fill:C.paper}),path('M0 -136V115',C.earth,3),text('Extinction',-136,-86,28,C.ink),text('Collapse',-136,-41,28,C.ink),text('Catastrophe',-136,4,28,C.ink),text('Degradation',-136,49,28,C.ink),text('Catastrophe,',137,-65,29,C.ink),text('Technology,',137,-25,29,C.ink),text('and the',137,15,29,C.ink),text('Missing Cockpit',137,55,27,C.ink)],5,'A real reading route: the four kinds of ending and the source’s catastrophe chapter. Short labels belong to the book spread rather than duplicating the scene heading.');
 storyGesture(q,'resident',5,'invite');mood('resident',6,'curious');
 scenes[3].visual=q.finish('Working water service does not ensure political freedom. A resident’s report faces emergency restriction, then a contrasting institutional choice admits evidence and another voice. The film closes at the actual classification and catastrophe reading route; democratic repair is a possibility to preserve, not an inevitable lesson of disaster.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
