import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#344353',blue:'#82b4cf',river:'#559fbc',teal:'#4d9e95',rust:'#ce8670',gold:'#dbb458',paper:'#f3eddd',wood:'#a79883',plum:'#9875ac',pollution:'#96835c',white:'#fff9ec'};
function setup(q){const{n,path,text,dot}=q;const rect=(x,y,w,h,fill,rx=4)=>n('rect',{x,y,width:w,height:h,fill,rx});const put=(id,x,y,ch,b=1,m=id,scale=1)=>{q.add(q.object(id,x,y,ch,m,scale));q.reveal(id,b,900);};const person=(id,x,y,{identity='person-02-neutral',coat=C.teal,scale=.64,b=1,seated=false}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.plum});q.reveal(id,b);};const delay=(id,action,offset)=>{q.actions.findLast(a=>a.actor===id&&a.action===action).offsetMs=offset;};const mood=(id,b,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:900});const report=(id,x,y,b=1,label='Revenue')=>put(id,x,y,[rect(-57,-38,114,76,C.paper),text(label,0,-10,23,C.ink),path('M-35 16H30M-35 28H12',C.teal,4)],b,'An actual selective work report.');const parcel=(id,x,y,b=1)=>put(id,x,y,[rect(-28,-22,56,44,C.gold),rect(-4,-22,8,44,C.paper)],b,'An ordinary completed output; no invented quantity or revenue.');return{rect,put,person,delay,mood,report,parcel};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,report,parcel}=setup(q);
 put('workplace',602,385,[rect(-492,-165,984,319,C.paper),rect(-492,146,984,15,C.wood),rect(-492,-165,984,24,C.rust),rect(-477,-124,167,125,'#d9e8e6'),path('M-393 -124V1',C.white,8)],1,'A working factory office keeps its instructions while ordinary occupants change.');
 put('control-machine',830,389,[rect(-141,-110,283,222,C.teal),rect(-120,-92,239,72,C.ink),text('Production target',0,-60,28,C.paper),path('M-86 47H87',C.paper,6),dot(77,3,13,C.gold),dot(77,44,13,C.rust),rect(-137,115,274,14,C.wood)],1,'The target governs a real production machine rather than a floating idea.');
 put('belt',751,509,[rect(-210,-21,474,23,C.wood),...[-170,-70,30,130,230].map(x=>dot(x,10,11,C.ink))],1,'The work continues as leadership changes.');
 parcel('output',626,476);q.move('output',1,939,476,4000);q.hide('output',1);delay('output','disappear',4700);
 person('manager-a',341,527,{identity:'person-02-neutral',coat:C.teal,scale:.71});
 put('desk',403,445,[rect(-115,-6,230,17,C.wood),path('M-98 11V81M98 11V81',C.wood,13)],1,'An ordinary role with responsibility for a retained objective.');
 report('instructions',482,409,1,'Target');
 q.move('manager-a',2,157,527,2600);q.hide('manager-a',2);delay('manager-a','disappear',3100);
 person('manager-b',334,527,{identity:'person-04-neutral',coat:C.plum,scale:.71,b:2});delay('manager-b','appear',3200);
 parcel('next-output',626,476,2);delay('next-output','appear',3000);q.move('next-output',2,970,476,4300);delay('next-output','moveTo',3100);
 storyGesture(q,'manager-b',3,'reflect');mood('manager-b',3,'curious');
 put('outside-report',151,320,[rect(-55,-36,110,72,C.paper),path('M-31 5Q-10 -9 10 5T37 5',C.river,5),text('River',0,-13,24,C.ink)],4,'The outside consequence has not entered target-setting authority.');
 storyGesture(q,'manager-b',4,'question');
 scenes[0].visual=q.finish('A manager leaves and a different ordinary manager inherits the same production schedule and continuing machine output. This explicitly imagined organizational mechanism avoids portraying staff as monsters or diagnosing individuals. An outside river report begins the question of what reaches authority.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,report,parcel}=setup(q);
 put('factory',333,338,[rect(-259,-128,518,236,C.paper),n('path',{d:'M-259 -128V-170L-132 -128V-170L0 -128V-170L132 -128V-170L259 -128Z',fill:C.rust}),rect(-243,-103,487,14,C.wood),rect(-236,47,120,61,C.teal),rect(-236,62,120,10,C.gold)],1,'An imagined company based on the book’s opening river case, not a named historical polluter.');
 put('land',632,486,[n('path',{d:'M-568 -22H-54L100 28H486V58H-568Z',fill:'#d8d4af'})],1,'The factory and downstream household share an actual geography.');
 put('river',630,487,[n('path',{d:'M-151 -39Q-77 -69 18 -19Q95 19 183 -4Q292 -26 430 25L410 58Q286 12 180 35Q86 56 -7 16Q-77 -20 -150 1Z',fill:C.river})],1,'An existing river receives the discharge; the household is downstream.');
 put('pipe',467,443,[path('M-35 -45H19V40H62',C.wood,18)],1,'A visible physical route carries the external cost.');
 put('tainted-flow',636,489,[path('M-104 -6Q-75 -16 -17 10Q37 34 90 17Q155 6 213 30',C.pollution,14)],1,'Discolored water signifies the explicitly imagined pollution without identifying a chemical or health outcome.');
 put('current',554,479,[n('ellipse',{cx:0,cy:0,rx:21,ry:5,fill:C.pollution})],1,'Continued discharge stays visible even after the public message changes.');q.move('current',1,823,505,4200);
 put('home',1007,352,[rect(-101,-79,202,153,C.rust),n('path',{d:'M-119 -79L-13 -145L119 -79Z',fill:C.plum}),rect(-79,-60,60,51,C.paper),rect(34,-34,42,108,C.paper)],2,'An inhabited downstream household makes the consequence legible.');
 person('resident',1013,526,{identity:'person-09-neutral',coat:C.gold,scale:.53,b:2});
 put('empty-container',912,509,[n('path',{d:'M-24 -21H24L18 17H-18Z',fill:C.paper}),path('M-23 -21Q0 -42 23 -21',C.wood,3)],2,'An adult withdraws an empty container from visibly polluted water; no injury is invented.');q.move('empty-container',2,973,497,2200);mood('resident',2,'worried');storyGesture(q,'resident',2,'question');
 person('production-worker',221,441,{identity:'person-02-neutral',coat:C.teal,scale:.49});person('reviewer',401,441,{identity:'person-04-neutral',coat:C.plum,scale:.49,b:3});
 report('revenue',160,250,2);q.move('revenue',2,300,260,2100);
 put('claims-desk',693,394,[rect(-74,-3,148,14,C.wood),path('M-60 12V103M60 12V103',C.wood,9),text('Claims',0,-68,27,'$ink')],3,'A claims role can receive a complaint without changing production authority.');
 person('clerk',754,503,{identity:'person-12-neutral',coat:C.blue,scale:.53,b:3});
 report('river-report',892,475,3,'River harm');q.move('river-report',3,633,475,2300);
 q.hide('revenue',4);put('public-notice',383,232,[rect(-104,-56,208,103,C.paper),text('We are sorry',0,-3,27,C.ink),path('M-64 20H61',C.rust,4)],4,'An apology changes the public message while physical discharge persists.');
 q.move('current',4,554,479,1);q.move('current',4,839,505,4300);delay('current','moveTo',200);
 storyGesture(q,'clerk',4,'reflect');storyGesture(q,'reviewer',5,'question');mood('reviewer',5,'curious');
 scenes[1].visual=q.finish('The source’s river example is expanded as an explicitly imagined factory and household. Revenue travels inward, a resident’s report reaches only a claims desk, and a public apology does not stop the physical discharge. No real company, contaminant measurement or medical outcome is asserted.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood}=setup(q);
 put('spread',651,359,[n('path',{d:'M-478 -177Q-245 -192 0 -162Q240 -192 478 -177V166Q236 136 0 166Q-243 136 -478 166Z',fill:C.paper}),path('M0 -162V166',C.wood,4)],1,'A physical editorial spread contains both selected harmful cases and omitted constructive institutional work.');
 put('selected-factory',390,365,[rect(-123,-70,246,107,C.rust),n('path',{d:'M-123 -70V-108L-42 -70V-108L42 -70V-108L123 -70Z',fill:C.plum}),rect(-92,-48,69,39,C.paper),path('M87 16H129V61H163',C.wood,12),path('M-146 81Q-23 61 88 86T209 84',C.river,18),path('M158 70H199',C.pollution,10)],1,'The selected factory illustration remains true within the hypothetical case; the critique concerns selection, not erasing the harm.');
 put('crop',407,359,[path('M-193 -121V-153H-153M154 -153H193V-120M193 116V150H154M-153 150H-193V116',C.rust,10)],1,'These are functional editorial crop marks, not decorative scene borders.');
 put('folded-leaf',878,359,[rect(-218,-177,470,343,C.plum),text('Outside the frame',0,-35,28,C.paper),path('M-130 3H117M-130 31H63',C.paper,4)],1,'A closed portion of the spread visibly excludes constructive examples.');
 person('editor',110,532,{identity:'person-04-neutral',coat:C.rust,scale:.69});storyGesture(q,'editor',2,'question');mood('editor',2,'skeptical');
 q.move('crop',3,380,359,1700);q.hide('folded-leaf',3);q.move('crop',3,819,357,2300);delay('crop','moveTo',2100);
 put('clinic',792,290,[rect(-83,-57,166,116,'#cbded6'),rect(-83,-57,166,20,C.teal),path('M52 -16V20M34 2H70',C.paper,8),rect(-66,9,53,8,C.wood),path('M-57 17V44M-22 17V44',C.wood,5)],3,'Public health is part of the source’s counterhistory of constructive institutions.');
 person('clinician',749,346,{identity:'person-09-neutral',coat:C.blue,scale:.29,b:3});
 put('commons',917,440,[path('M-181 -8Q-85 -49 24 -8T147 -3',C.river,17),path('M-170 18Q-81 -20 30 18T158 22',C.wood,6),rect(-137,-10,37,13,C.gold)],4,'A maintained shared irrigation channel is a conceptual illustration of collective resource governance, not an invented named case.');
 person('maintainer',947,478,{identity:'person-02-neutral',coat:C.gold,scale:.28,b:4});
 put('research-table',1022,304,[rect(-61,-2,122,11,C.wood),path('M-49 9V51M49 9V51',C.wood,6),rect(-27,-40,63,37,C.paper),path('M-15 -24H21M-15 -12H10',C.blue,3)],4,'Preserved observations show cumulative scientific knowledge as constructive collective work.');
 person('researcher',1077,354,{identity:'person-12-neutral',coat:C.plum,scale:.29,b:4});
 q.hide('crop',5);storyGesture(q,'editor',5,'reflect');mood('editor',5,'curious');
 scenes[2].visual=q.finish('A physical editorial crop first selects the pollution case while a folded page hides constructive collective work. Unfolding reveals an inhabited clinic, maintained common water channel and shared research observations. Accurate chosen examples remain intact; the scene exposes omitted counterhistory rather than denying institutional harm.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,report,parcel}=setup(q);
 put('control',586,339,[rect(-133,-106,266,183,C.teal),rect(-103,-82,206,51,C.ink),text('Production',0,-49,29,C.paper),dot(66,14,24,C.rust),path('M66 -1V28',C.paper,7),rect(-122,92,244,19,C.wood)],1,'A person with decision rights can constrain the actual process, not merely acknowledge a report.');
 put('belt',808,466,[rect(-186,-13,373,19,C.wood),...[-156,-78,0,78,156].map(x=>dot(x,19,9,C.ink))],1,'The incomplete shipment makes the hypothetical pause costly without inventing money or quantities.');
 parcel('order',694,435);q.move('order',1,836,435,2400);
 put('discharge-route',461,491,[path('M-8 -72V4H96',C.wood,16),path('M84 16Q180 0 274 24T541 22',C.river,21),path('M86 16Q180 0 274 24T541 22',C.pollution,9)],1,'Prior pollution remains in the river after production is constrained; no instant environmental cleanup.');
 put('fresh-discharge',509,488,[n('ellipse',{cx:0,cy:0,rx:20,ry:5,fill:C.pollution})],1,'An active discharge marker can stop while the already affected river stays discolored.');q.move('fresh-discharge',1,779,515,2900);
 person('authority',349,535,{identity:'person-04-neutral',coat:C.plum,scale:.72});person('resident',155,535,{identity:'person-09-neutral',coat:C.gold,scale:.62});
 report('evidence',193,465,2,'River harm');q.move('evidence',2,447,465,2400);storyGesture(q,'resident',2,'question');storyGesture(q,'authority',2,'reflect');
 q.move('order',2,918,435,2700);q.move('fresh-discharge',2,509,488,1);q.move('fresh-discharge',2,779,515,2800);delay('fresh-discharge','moveTo',200);
 storyGesture(q,'authority',3,'resolve');mood('authority',3,'determined');q.move('order',3,968,435,1700);q.move('fresh-discharge',3,839,515,1700);
 put('stop-hand',637,353,[path('M-37 16L-12 0L15 -2',C.gold,13),dot(17,-2,9,C.gold)],3,'A conceptual authority action pauses the control; not an operating procedure for an actual factory.');
 delay('stop-hand','appear',1500);q.hide('fresh-discharge',3);delay('fresh-discharge','disappear',1700);put('paused-control',586,339,[rect(-98,-76,196,41,C.ink),text('Paused',0,-47,27,C.paper)],3,'The actual process has stopped and its shipment is left incomplete; this is an explicitly imagined test.');delay('paused-control','appear',1700);
 for(const id of ['control','belt','order','discharge-route','evidence','stop-hand','paused-control'])q.hide(id,4);
 q.move('authority',4,237,535,2100);q.hide('resident',4);
 put('book',768,352,[n('path',{d:'M-250 -139Q-122 -156 0 -131Q123 -156 250 -139V145Q129 121 0 143Q-121 122 -250 145Z',fill:C.paper}),path('M0 -132V143',C.wood,4),text('The Moral',-123,-70,29,C.ink),text('Turing Test',-123,-28,30,C.ink),text('The Book as a',126,-76,28,C.ink),text('Small Egregopath',126,-34,27,C.ink),path('M-213 30H-44M-213 57H-72M43 24H214M43 52H177',C.teal,4)],4,'Two exact source chapter headings direct the reader to costly correction and the book’s own selective framing.');
 put('rest',768,514,[rect(-268,-9,536,16,C.wood)],4,'A physical open volume supports the final reading invitation.');storyGesture(q,'authority',4,'reflect');storyGesture(q,'authority',5,'invite');mood('authority',5,'curious');
 scenes[3].visual=q.finish('In an explicitly imagined alternative, resident evidence reaches actual production authority. An authority action stops the moving output and active discharge marker, leaving an incomplete shipment and the already discolored river. This shows a costly constraint without claiming a real reform or instantaneous cleanup. The book opens to the two actual source chapters that examine correction and selective argument.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
