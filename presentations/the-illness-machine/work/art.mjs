import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#304254',teal:'#528f91',plum:'#936b92',ochre:'#d6aa60',sage:'#97b69c',paper:'#f0e9dd',coral:'#ce8975',wood:'#aa8768'};
function setup(q){const {n,path,text,dot}=q;const rect=(x,y,w,h,fill,rx=6)=>n('rect',{x,y,width:w,height:h,fill,rx});const put=(id,x,y,children,b=1,meaning=id)=>{q.add(q.object(id,x,y,children,meaning));q.reveal(id,b,1000);};const person=(id,x,y,{identity='person-04-neutral',coat=C.teal,scale=.93,seated=false,b=1}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.sage});q.reveal(id,b);};const mood=(id,b,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:1100});
 const phone=(id,x,y,b=1)=>put(id,x,y,[rect(-38,-65,76,132,C.ink,10),rect(-30,-53,60,100,C.paper,4),path('M-20 -24H20M-20 -4H15M-20 16H20',C.teal,3),dot(0,56,4,C.paper)],b,'A workplace message interrupts the person’s ordinary day.');
 const schedule=(id,x,y,b=1)=>put(id,x,y,[rect(-146,-99,292,203,C.paper),text('Work schedule',0,-58,31,C.ink),...[-85,0,85].flatMap(xx=>[rect(xx-29,-28,58,46,C.sage),rect(xx-29,36,58,43,C.sage)]),text('Mon',-85,3,20,C.ink),text('Tue',0,3,20,C.ink),text('Wed',85,3,20,C.ink)],b,'A schedule is a concrete exposure controlled by the workplace, not a claim that every work change causes illness.');
 return{rect,put,person,mood,phone,schedule};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,phone,schedule}=setup(q);
 person('worker',247,525,{coat:C.plum,seated:true});person('clinician',510,524,{identity:'person-02-neutral',coat:C.teal,seated:true});
 put('tissue-table',381,465,[rect(-43,-8,86,16,C.wood),path('M-28 8V58M28 8V58',C.wood,8),rect(-29,-41,58,31,C.paper),path('M-10 -41Q-14 -69 9 -66L19 -41',C.paper,7)],1,'Two equal-height seats and a small shared table locate a listening encounter without prescribing treatment.');
 mood('worker',1,'worried');storyGesture(q,'worker',1,'reflect');storyGesture(q,'clinician',1,'invite');
 schedule('schedule',921,299,2);phone('message',935,466,2);
 put('changed-shift',820,281,[rect(-48,-23,96,46,C.coral),text('Changed',0,6,20,C.ink)],3,'The shift is reassigned while the clinical encounter continues.');q.move('changed-shift',3,1006,357,2600);
 
 storyGesture(q,'clinician',3,'explain');mood('worker',4,'curious');
 scenes[0].visual=q.finish('The source’s worker example: a person receives a listening clinical encounter while an employer-controlled schedule changes elsewhere. The person is illustrative; no therapy, medication recommendation or improvement in clinical outcome is depicted.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood}=setup(q);
 // The longitudinal observation begins before the payment, then becomes a selective outcome record.
 person('parent',303,520,{identity:'person-09-neutral',coat:C.teal});person('child',474,523,{identity:'person-12-neutral',coat:C.ochre,scale:.59});
 put('home-seat',172,448,[rect(-58,-61,116,112,C.sage,13),path('M-48 51V80M49 51V80',C.wood,9)],1,'A normal home situation; the people are not portraits of study participants or ethnic caricatures.');
 put('prior-record',883,286,[rect(-181,-107,362,220,C.paper),text('Earlier assessments',0,-65,30,C.ink),path('M-135 -21H135M-135 9H135M-135 39H73',C.teal,5),text('Children and families',0,85,24,C.ink)],1,'Repeated study observations already existed before the income change.');
 put('payment',1095,448,[rect(-112,-53,224,111,'#e9d5ad'),text('Annual payment',0,-12,27,C.ink),text('Tribal profits',0,25,23,C.ink)],2,'Annual distributions of tribal casino profits, not gambling winnings.');q.move('payment',2,645,432,3300);
 q.label('income-change','Some families left poverty',410,577,31);q.reveal('income-change',3);storyGesture(q,'parent',3,'reflect');
 for(const id of ['parent','child','home-seat','payment','income-change'])q.hide(id,4);
 q.hide('prior-record',4);q.move('prior-record',5,284,290,1500);q.reveal('prior-record',6);
 put('follow-up',823,332,[rect(-267,-165,534,326,C.paper),text('Families leaving poverty',0,-118,32,C.ink),text('Conduct / oppositional',-40,-53,27,C.ink),text('symptoms',-116,-20,27,C.ink),path('M165 -79V-15M148 -35L165 -15L182 -35',C.teal,7),text('Fewer',169,19,24,C.ink),path('M-223 41H222',C.wood,3)],4,'Qualitative study findings; the arrow indicates direction only and does not encode an effect size or universal outcome.');
 q.actions.find(x=>x.actor==='follow-up'&&x.action==='appear').offsetMs=1500;
 put('selective-result',809,440,[text('Anxiety / depression',-33,-21,27,C.ink),text('No equivalent improvement',0,22,26,C.ink)],5,'The same study did not find the equivalent improvement in anxiety and depression.');
 put('time-return',538,334,[path('M-51 0H29M-31 -19L-51 0L-31 19',C.plum,6)],6,'Researchers can refer back to observations made before the income change; this was not randomized assignment.');
 q.label('timing','Before the payments',284,481,29);q.reveal('timing',6);
 scenes[1].visual=q.finish('The book’s western North Carolina child study: earlier assessments precede annual tribal profit payments. The displayed qualitative follow-up is explicitly restricted to families escaping poverty, with fewer conduct/oppositional symptoms but no equivalent anxiety/depression improvement. No invented amount, effect size, casino glamour, randomization or guaranteed cure.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,phone,schedule}=setup(q);
 person('worker',230,531,{coat:C.plum});phone('message',302,395);
 schedule('rota',640,294);put('replacement-shift',553,345,[rect(-39,-23,78,46,C.coral),text('New',0,8,24,C.ink)],1,'A repeatedly changed shift is part of the source’s harmful workplace scenario.');q.move('replacement-shift',1,726,282,2600);
 person('representative',1005,532,{identity:'person-02-neutral',coat:C.teal,b:3});
 put('concern',1005,178,[n('path',{d:'M-155 -35H155V39H-85L-133 66L-116 39H-155Z',fill:C.paper}),text('Raise the concern',0,9,27,C.ink)],3,'An accessible reporting conversation is one proposed change in workplace control.');
 mood('worker',1,'worried');storyGesture(q,'worker',2,'reflect');storyGesture(q,'worker',3,'question');storyGesture(q,'representative',3,'invite');
 q.hide('replacement-shift',4);put('schedule-note',640,453,[text('Proposed repair',0,-20,31,'$ink'),text('Predictable shifts',0,20,28,'$ink')],4,'Proposed reduction of unpredictability; not a depicted trial result or promise of clinical improvement.');
 put('care-continues',330,185,[rect(-162,-46,324,98,'#d6e3dc'),text('Clinical care continues',0,9,29,C.ink)],2,'Immediate care is retained while work conditions are addressed.');
 storyGesture(q,'representative',4,'explain');mood('worker',5,'curious');
 scenes[2].visual=q.finish('A worker’s changing rota and interrupted day lead to a reporting conversation and a proposed more predictable schedule. Clinical support continues; the illustration does not diagnose the person, promise a cure or prescribe treatment.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood}=setup(q);
 person('person',321,528,{coat:C.plum,seated:true});mood('person',1,'tired');storyGesture(q,'person',1,'reflect');
 put('missed-work',650,262,[rect(-165,-112,330,226,C.paper),text('Work interrupted',0,-66,31,C.ink),path('M-116 -22H115M-116 9H78',C.teal,5),text('Income disrupted',0,70,28,C.ink)],2,'An existing episode can disrupt work and income; a consequence can become a maintaining condition.');
 put('new-obligation',947,421,[rect(-132,-70,264,143,'#e8d1bb'),text('A new obstacle',0,-18,30,C.ink),text('Bills still arrive',0,26,25,C.ink)],3,'A continuing obligation returns into daily life, without implying irresponsibility or identifying a diagnosis.');q.move('new-obligation',3,552,416,3100);
 for(const id of ['missed-work','new-obligation'])q.hide(id,4);
 put('reading-spread',859,333,[n('path',{d:'M-246 -150Q-122 -177 0 -148Q120 -177 246 -150V157Q124 130 0 158Q-122 130 -246 157Z',fill:C.paper}),path('M0 -146V157',C.wood,3),text('The casino study',-125,-79,29,C.ink),text('The case against',120,-79,27,C.ink),text('this book',120,-40,27,C.ink),...[-1,1].map(sign=>path(sign<0?'M-212 -9H-37M-212 28H-37M-212 65H-64':'M36 -9H211M36 28H211M36 65H176',C.teal,4))],4,'A reading invitation to the actual prologue and counterargument chapter; chapter labels are not fabricated source quotations.');
 put('held-pages',412,389,[n('path',{d:'M-55 -37Q-30 -48 0 -35Q28 -49 55 -37V38Q29 28 0 39Q-29 28 -55 38Z',fill:C.paper}),path('M0 -34V38',C.wood,2)],4,'The person turns toward reading; the enlarged spread is a view of the same reading object.');storyGesture(q,'person',4,'invite');mood('person',5,'curious');
 scenes[3].visual=q.finish('Reverse causation is illustrated through an existing difficult episode interrupting work, followed by a new household obstacle. The reader returns to the source’s casino study and strongest countercase. No specific diagnosis, moral blame or universal social explanation is assigned.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
