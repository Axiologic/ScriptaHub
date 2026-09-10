import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#374b62',indigo:'#687ba3',copper:'#be8667',stone:'#d9d2bf',paper:'#f4efdf',coral:'#d97d6d',teal:'#72aea8',gold:'#d6b65e',wood:'#ad947c',sky:'#bdd5d9'};
function setup(q){const{n,path,text,dot}=q;const rect=(x,y,w,h,fill,rx=4)=>n('rect',{x,y,width:w,height:h,fill,rx});const put=(id,x,y,ch,b=1,m=id,scale=1)=>{q.add(q.object(id,x,y,ch,m,scale));q.reveal(id,b,1000);};const person=(id,x,y,{identity='person-02-neutral',coat=C.indigo,scale=.64,b=1,seated=false}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.teal});q.reveal(id,b);};const delay=(id,action,offset)=>{q.actions.findLast(a=>a.actor===id&&a.action===action).offsetMs=offset;};const mood=(id,b,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:900});const page=(id,x,y,b,label='Warning',color=C.paper)=>put(id,x,y,[rect(-58,-39,116,78,color),text(label,0,-11,23,C.ink),path('M-34 10H32M-34 25H15',C.copper,4)],b,'A specific project document, not an abstract idea card.');const bridge=(id,x,y,b=1,scale=1)=>put(id,x,y,[n('path',{d:'M-272 24H-149L-117 124H-272ZM151 24H272V124H119Z',fill:C.stone}),rect(-246,-5,220,22,C.copper),rect(77,-5,168,22,C.copper),path('M-227 -6V-40H-27M99 -6V-40H230M-153 -40V-6M-78 -40V-6M170 -40V-6',C.indigo,5),path('M-172 18V119M172 18V119',C.wood,19),rect(-266,126,532,12,C.wood)],b,'An unfinished pedestrian bridge with supported abutments, piers and a visible deck gap; a conceptual long project, not an engineering specification.',scale);return{rect,put,person,delay,mood,page,bridge};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,page,bridge}=setup(q);
 put('planning-room',298,366,[rect(-226,-152,453,318,C.paper),rect(-226,151,453,18,C.wood),rect(-211,-136,422,66,C.sky),path('M-54 -136V-70M95 -136V-70',C.paper,8)],1,'A modern public planning room overlooks an unfinished useful project, not a hereditary throne.');
 person('leader',225,526,{identity:'person-04-neutral',coat:C.indigo,scale:.72});
 put('plan-table',364,438,[rect(-87,-4,174,15,C.wood),path('M-74 11V87M74 11V87',C.wood,11),n('path',{d:'M-71 -57H64L82 -4H-87Z',fill:C.indigo}),path('M-43 -42H19M-30 -23H38',C.paper,4)],1,'Specialist coordination has a concrete task and legitimate room to act.');
 bridge('project',830,382,1,.93);
 person('worker',1032,535,{identity:'person-09-neutral',coat:C.coral,scale:.57,b:2});
 put('unplaced-section',939,522,[rect(-80,-18,160,19,C.copper),path('M-65 1V12M64 1V12',C.wood,9)],2,'A supported unfinished structural section is still waiting; no unsafe live-work instructions.');
 put('mandate',569,252,[rect(-88,-71,176,143,C.paper),text('Mandate',0,-37,29,C.ink),path('M-56 0H57M-56 -11V12M57 -11V12',C.indigo,5),text('Start',-43,43,22,C.ink),text('End',47,43,22,C.ink)],2,'Authority has a defined beginning and ending, rather than a permanent identity.');
 storyGesture(q,'leader',2,'explain');storyGesture(q,'worker',3,'question');
 put('archive',534,469,[rect(-37,-57,74,113,C.teal),path('M-32 -15H32M-32 23H32',C.paper,3),...[-36,3,41].map(y=>rect(-10,y,20,4,C.ink))],3,'The work record belongs to the office and remains available across occupants.');
 q.move('leader',4,134,526,2300);storyGesture(q,'worker',4,'reflect');mood('leader',5,'curious');storyGesture(q,'leader',5,'invite');
 scenes[0].visual=q.finish('A modern planning room, finite mandate and supported unfinished bridge establish useful concentrated capability. The office, archive and project remain as the leader steps aside. No historical nobility costume, numerical simulation claim or implemented constitution is implied.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,page,bridge}=setup(q);
 bridge('long-project',834,396,1,.93);
 put('review-space',309,391,[rect(-224,-188,447,330,C.paper),rect(-224,138,447,16,C.wood),text('Captured review',0,-145,29,C.ink)],1,'First explicitly imagined rule: accountability exists but the incumbent controls its evidence.');
 person('incumbent',404,529,{identity:'person-04-neutral',coat:C.indigo,scale:.66,b:2});person('reviewer',166,529,{identity:'person-12-neutral',coat:C.teal,scale:.6,b:2});
 put('cabinet',305,364,[rect(-52,-84,105,173,C.copper),rect(-43,-71,86,148,C.paper),path('M-40 -20H40M-40 31H40',C.wood,4),rect(36,-14,9,29,C.indigo)],2,'A record held inside the incumbent’s controlled archive cannot supply independent review.');
 page('warning',303,389,2,'Warning');
 put('locked-door',305,364,[rect(-44,-71,87,149,C.indigo),path('M-17 -11V-24Q0 -44 17 -24V-11',C.gold,5),rect(-21,-10,42,35,C.gold)],2,'The original warning remains behind the controlled record boundary; no invented warning content is asserted.');delay('locked-door','appear',1900);
 page('curated-report',412,466,3,'Progress');q.move('curated-report',3,220,466,2200);storyGesture(q,'reviewer',3,'question');mood('reviewer',3,'worried');
 for(const id of ['review-space','incumbent','reviewer','cabinet','warning','locked-door','curated-report'])q.hide(id,4);
 put('audition-room',302,391,[rect(-224,-188,447,330,C.paper),rect(-224,138,447,16,C.wood),text('Permanent audition',0,-145,29,C.ink),rect(-150,47,270,12,C.wood),path('M-135 59V139M104 59V139',C.wood,10)],4,'A separate hypothetical reset, not a conviction or chronological claim about the first leader.');delay('audition-room','appear',1300);
 person('audition-reviewer',117,530,{identity:'person-12-neutral',coat:C.teal,scale:.55,b:4,seated:true});delay('audition-reviewer','appear',1500);storyGesture(q,'audition-reviewer',4,'question');
 person('leader-b',360,530,{identity:'person-02-neutral',coat:C.coral,scale:.65,b:4});delay('leader-b','appear',1500);
 person('waiting-worker',1029,535,{identity:'person-09-neutral',coat:C.gold,scale:.56,b:4});
 put('work-plan',579,308,[rect(-74,-66,149,136,C.paper),text('Long project',0,-31,26,C.ink),path('M-40 7H42M-40 28H10',C.indigo,4)],4,'A useful long project cannot advance while every step becomes an immediate mandate contest.');
 q.move('leader-b',4,451,530,2200);delay('leader-b','moveTo',2000);q.move('leader-b',4,287,530,2000);delay('leader-b','moveTo',4700);
 q.move('leader-b',5,431,530,2100);q.move('leader-b',5,264,530,2100);delay('leader-b','moveTo',2500);
 
 // Express concern using the supported expressive rig and a motivated quiet pause.
 mood('leader-b',5,'worried');storyGesture(q,'waiting-worker',5,'question');
 put('waiting-segment',920,531,[rect(-80,-20,160,18,C.copper),path('M-61 -2V8M61 -2V8',C.wood,8)],5,'The unfinished physical work does not mysteriously complete while the authority is continually interrupted.');
 storyGesture(q,'leader-b',6,'reflect');mood('waiting-worker',6,'curious');
 scenes[1].visual=q.finish('Two sequential hypothetical rules govern the same long bridge project: a captured archive produces only curated progress for review; after a visible reset, permanent audition repeatedly pulls a leader away while workers and unplaced sections remain waiting. This does not portray all opposition as illegitimate or establish any real person’s guilt.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,page}=setup(q);
 put('independent-archive',858,355,[rect(-146,-151,292,282,C.teal),rect(-126,-115,252,226,C.paper),text('Independent record',0,-121,28,C.ink),path('M-116 -46H116M-116 38H116',C.wood,7),...[-90,-49,-9,34,77].map(x=>rect(x,-102,25,52,C.indigo)),...[-90,-45,0,45,85].map(x=>rect(x,49,24,52,C.copper))],1,'Independent custody survives changes to the officeholder’s account.');
 person('engineer',145,535,{identity:'person-09-neutral',coat:C.coral,scale:.66});person('officeholder',393,535,{identity:'person-04-neutral',coat:C.indigo,scale:.68});person('independent-reviewer',1078,535,{identity:'person-12-neutral',coat:C.teal,scale:.63});
 page('warning-copy',195,471,1,'Warning');q.move('warning-copy',2,836,351,2900);
 put('review-rule',595,266,[rect(-102,-62,204,126,C.paper),text('Review condition',0,-26,27,C.ink),text('Declared earlier',0,18,25,C.ink)],2,'A prospective criterion is consulted rather than invented by an opposing coalition after the result.');
 put('review-table',595,480,[rect(-155,-8,310,15,C.wood),path('M-137 7V55M137 7V55',C.wood,10)],2,'An actual encounter between evidence and a response, not immediate public punishment.');
 page('answer',430,444,3,'Reply');q.move('answer',3,650,439,2300);storyGesture(q,'officeholder',3,'explain');storyGesture(q,'independent-reviewer',3,'reflect');
 for(const id of ['engineer','warning-copy','review-rule','review-table','answer'])q.hide(id,4);
 put('possible-outcome',532,196,[text('Possible end of mandate',0,0,30,'$ink')],4,'A possible outcome, not an inevitable guilty finding from the preceding illustrative review.');
 put('badge-tray',558,450,[n('path',{d:'M-68 -18H68L56 17H-57Z',fill:C.wood})],4,'The office access is returned while the individual and unrelated personal property continue.');
 put('badge',425,412,[rect(-17,-25,34,50,C.gold),dot(0,-9,6,C.paper),path('M-10 8H10',C.indigo,3)],4,'Return of jurisdiction is distinct from confiscation of personal life.');q.move('badge',4,550,441,2300);
 put('personal-bag',322,506,[rect(-31,-25,62,52,C.copper),path('M-13 -26V-39H13V-26',C.wood,5)],4,'Personal possessions are retained.');
 q.move('officeholder',4,271,535,2100);q.move('personal-bag',4,206,506,2100);delay('officeholder','moveTo',2600);delay('personal-bag','moveTo',2600);
 person('neighbor',129,535,{identity:'person-02-neutral',coat:C.gold,scale:.6,b:4});delay('neighbor','appear',3400);storyGesture(q,'neighbor',5,'invite');mood('officeholder',5,'relieved');storyGesture(q,'independent-reviewer',5,'reflect');
 scenes[2].visual=q.finish('A warning enters an independent archive, a previously declared review condition is consulted, and the officeholder adds a reply. The record remains available. A separately marked possible outcome returns only the office badge; the person carries personal belongings into ordinary civic life. No guilty finding, automatic removal, confiscation of unrelated assets or implemented legal procedure is asserted.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,page}=setup(q);
 put('kitchen',332,366,[rect(-253,-162,507,321,C.paper),rect(-253,144,507,17,C.wood),rect(-238,-145,477,50,C.teal),path('M-91 -142V-98M69 -142V-98',C.paper,4),rect(-222,-71,94,105,C.stone),path('M-142 -45V-1',C.wood,4)],1,'An evening kitchen recognizes citizens’ finite time, work and care without depicting them as incapable.');
 person('citizen',329,530,{identity:'person-09-neutral',coat:C.coral,scale:.69});person('elder',126,530,{identity:'person-12-neutral',coat:C.indigo,scale:.55,seated:true});
 put('table',440,447,[rect(-115,-7,230,17,C.wood),path('M-99 10V78M99 10V78',C.wood,11)],1,'Care and paid work coexist with the public question.');
 put('meal',399,420,[n('ellipse',{cx:0,cy:0,rx:34,ry:10,fill:C.teal}),dot(-9,-5,8,C.gold),dot(10,-5,8,C.coral)],1,'Ordinary family care is retained, not consumed by unlimited civic paperwork.');
 put('work-laptop',510,408,[rect(-45,-45,90,56,C.indigo),rect(-37,-38,74,41,C.sky),n('path',{d:'M-45 12H45L62 23H-61Z',fill:C.stone})],1,'The citizen also has work; the point is usable public accountability.');
 put('deep-record',788,455,[...Array.from({length:5},(_,i)=>rect(-72-i*5,-i*20,155,14,i%2?C.indigo:C.paper))],1,'The full evidence may remain complex while an understandable public handle gives access.');
 put('public-handle',765,264,[rect(-152,-58,304,116,C.paper),text('Independent review',0,-12,29,C.ink),path('M-65 19H66M55 9L68 19L55 29',C.teal,5)],2,'A short commitment opens its underlying evidence rather than replacing the constitutional truth with a private story.');
 q.hide('deep-record',3);
 put('record-view',835,434,[rect(-166,-98,332,195,C.paper),path('M-134 -42H126M-134 -14H73',C.copper,4),text('Review condition',0,41,26,C.ink)],3,'The exact conceptual warning from the earlier encounter is exposed through the public commitment, not multiplied into abstract labels.');
 put('record-title',835,369,[text('Preserved warning',0,0,27,C.ink)],3,'The record is titled after the moving warning has been filed, preserving legibility during transit.');delay('record-title','appear',3450);
 page('opened-warning',765,309,3,'Warning');q.move('opened-warning',3,835,422,1600);q.hide('opened-warning',3);delay('opened-warning','disappear',2200);
 person('reviewer',1101,535,{identity:'person-12-neutral',coat:C.teal,scale:.58,b:3});storyGesture(q,'citizen',3,'question');storyGesture(q,'reviewer',3,'explain');
 for(const id of ['kitchen','elder','table','meal','work-laptop','public-handle','record-view','record-title','reviewer'])q.hide(id,4);
 q.move('citizen',4,225,535,2200);
 put('book',775,350,[n('path',{d:'M-263 -140Q-137 -162 0 -133Q139 -162 263 -140V150Q138 123 0 149Q-136 123 -263 150Z',fill:C.paper}),path('M0 -134V149',C.wood,4),text('The Contract',-135,-78,29,C.ink),text('That Selects',-135,-38,29,C.ink),text('After Selection',-135,2,27,C.ink),text('A Human Coda',134,-71,29,C.ink),text('Complexity',134,-31,27,C.ink),text('Is Not Consent',134,9,27,C.ink),path('M-219 60H-42M43 65H223',C.teal,4)],4,'Exact source reading destinations: the continuing contract and the human coda’s challenge of intelligible consent.');
 put('book-rest',775,524,[rect(-278,-8,556,16,C.wood)],4,'The reading invitation remains book-first rather than presenting a finished political program.');storyGesture(q,'citizen',4,'reflect');mood('citizen',5,'curious');storyGesture(q,'citizen',5,'invite');
 scenes[3].visual=q.finish('In an inhabited evening kitchen, work and care coexist with a thick public record. A short independent-review commitment opens the preserved warning and review condition, with another human available to answer. The record remains shared and inspectable rather than personalized constitutional truth. The final book pages point to the contract chapter and Human Coda, without claiming automatic consent or resolved appeal.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
