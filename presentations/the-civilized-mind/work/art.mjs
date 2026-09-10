import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#35485b',coral:'#d88671',olive:'#8d9e69',cobalt:'#6c8aba',stone:'#e1d6bd',paper:'#f4edda',teal:'#7cafac',gold:'#dfb752',plum:'#a086ad',wood:'#ab8c70'};
function setup(q){const{n,path,text,dot}=q;const rect=(x,y,w,h,fill,rx=4)=>n('rect',{x,y,width:w,height:h,fill,rx});const put=(id,x,y,ch,b=1,m=id,scale=1)=>{q.add(q.object(id,x,y,ch,m,scale));q.reveal(id,b,1000);};const person=(id,x,y,{identity='person-02-neutral',coat=C.teal,scale=.66,b=1,seated=false}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.coral});q.reveal(id,b);};const delay=(id,action,offset)=>{q.actions.findLast(a=>a.actor===id&&a.action===action).offsetMs=offset;};const mood=(id,b,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:900});const plant=(id,x,y,b=1,scale=1)=>put(id,x,y,[n('path',{d:'M-33 -17H33L25 29H-24Z',fill:C.coral}),path('M0 -17V-77',C.olive,6),n('ellipse',{cx:-15,cy:-62,rx:22,ry:9,fill:C.olive}),n('ellipse',{cx:18,cy:-41,rx:26,ry:10,fill:C.olive}),n('ellipse',{cx:0,cy:-83,rx:10,ry:20,fill:C.olive})],b,'A tended communal plant, not a decorative background texture.',scale);const prospectus=(id,x,y,b=1)=>put(id,x,y,[rect(-59,-47,118,94,C.paper),text('Study plans',0,-20,24,C.ink),n('path',{d:'M-30 2L0 -10L31 2V29H-30Z',fill:C.cobalt}),path('M-19 6V23M0 6V23M19 6V23',C.paper,4)],b,'An adult’s actual study prospectus; no promise of admission or invented university.');const photo=(id,x,y,b=1)=>put(id,x,y,[rect(-52,-42,104,83,C.wood),rect(-43,-34,86,66,C.paper),dot(-20,-10,10,C.coral),dot(19,-14,11,C.gold),n('path',{d:'M-37 26V7Q-20 -3 -3 7V26M1 26V2Q20 -9 38 2V26Z',fill:C.teal})],b,'Family memory has genuine value without granting ownership of the adult.');return{rect,put,person,delay,mood,plant,prospectus,photo};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,plant,prospectus,photo}=setup(q);
 put('courtyard',601,363,[rect(-504,-163,1008,322,C.stone),rect(-504,150,1008,17,C.wood),rect(-489,-163,977,21,C.coral),n('path',{d:'M274 146V-53Q340 -150 409 -53V146Z',fill:C.paper}),rect(-458,-123,192,88,C.teal),path('M-366 -122V-36',C.paper,8)],1,'A warm inhabited community has real practices, mutual help and memory, not a costume stereotype.');
 plant('herbs',208,481,1,1.15);plant('herbs-small',291,502,1,.68);
 person('parent',409,531,{identity:'person-12-neutral',coat:C.olive,scale:.73});person('adult-daughter',687,531,{identity:'person-04-neutral',coat:C.cobalt,scale:.72});
 put('meal-table',559,446,[rect(-145,-7,290,18,C.wood),path('M-123 11V84M123 11V84',C.wood,13),n('ellipse',{cx:0,cy:-16,rx:50,ry:14,fill:C.coral}),n('path',{d:'M-48 -14Q0 35 48 -14Z',fill:C.coral}),path('M32 -34L72 -59',C.wood,7),...[-83,84].map(x=>n('ellipse',{cx:x,cy:-15,rx:22,ry:8,fill:C.paper}))],1,'Shared food and practical help make belonging substantive before disagreement appears.');
 person('neighbor',1017,531,{identity:'person-02-neutral',coat:C.coral,scale:.62,b:2});
 put('borrowed-tool',933,462,[path('M0 45V-33',C.wood,10),path('M-28 -35H29M-27 -35V-49M-9 -35V-49M10 -35V-49M28 -35V-49',C.ink,6)],2,'A returned garden tool makes mutual aid visible, without a generic community symbol.');q.move('borrowed-tool',2,891,462,1600);storyGesture(q,'neighbor',2,'invite');
 photo('family-photo',484,272,3);prospectus('study-plan',732,440,3);
 storyGesture(q,'adult-daughter',4,'question');mood('parent',4,'curious');storyGesture(q,'parent',4,'reflect');storyGesture(q,'adult-daughter',5,'explain');
 scenes[0].visual=q.finish('An adult daughter shares a meal with an older parent in a tended courtyard, while a neighbor returns a real garden tool. Family memory and an adult study prospectus establish both belonging and a future beyond it. The invented scenario is not a diagnosis of any religion or ethnic group.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,plant,prospectus,photo}=setup(q);
 put('connected-rooms',604,364,[rect(-499,-163,998,318,C.paper),rect(-499,144,998,17,C.wood),rect(-499,-163,475,22,C.coral),rect(24,-163,475,22,C.cobalt),rect(-13,-163,26,127,C.stone),rect(-13,91,26,53,C.stone)],1,'Two connected spaces allow recognition without dissolving a real disagreement.');
 put('family-shelf',332,345,[rect(-133,15,266,15,C.wood),path('M-117 31V54H-90M117 31V54H90',C.wood,8)],1,'Memory remains present rather than being caricatured as hostility.');
 photo('family-photo',311,309);
 person('parent',230,533,{identity:'person-12-neutral',coat:C.olive,scale:.7});person('adult-daughter',921,533,{identity:'person-04-neutral',coat:C.cobalt,scale:.73});
 put('study-desk',803,447,[rect(-120,-7,240,17,C.wood),path('M-101 10V85M101 10V85',C.wood,12)],1,'An adult’s possible education is a concrete future, not a rebellion stereotype.');prospectus('study-plan',792,440);
 storyGesture(q,'parent',2,'reflect');mood('parent',2,'worried');storyGesture(q,'adult-daughter',2,'reflect');
 storyGesture(q,'adult-daughter',3,'explain');mood('adult-daughter',3,'determined');
 q.move('parent',4,431,533,2100);q.move('adult-daughter',4,752,533,2100);storyGesture(q,'parent',4,'question');mood('parent',4,'curious');
 put('calendar',595,287,[rect(-97,-68,194,136,C.paper),text('Optional visits',0,-31,27,C.ink),...[-49,0,49].flatMap(x=>[-2,36].map(y=>rect(x-15,y-9,29,22,(x===0&&y===36)?C.coral:C.stone)))],5,'A possible contact arrangement is explicitly optional, never a condition for an adult’s basic freedom.');
 q.move('family-photo',5,311,438,1000);q.move('family-photo',5,529,438,1400);delay('family-photo','moveTo',1300);q.move('study-plan',5,650,438,2200);storyGesture(q,'adult-daughter',5,'question');storyGesture(q,'parent',6,'explain');mood('adult-daughter',6,'curious');
 scenes[1].visual=q.finish('A parent attends to family memory while an unmistakably adult daughter attends to her study prospectus. They move into the connected space and bring the two objects together. An explicitly optional visits calendar is a topic for coexistence, not permission to leave. Recognition and cost do not magically settle the disagreement.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,plant}=setup(q);
 put('administration',348,365,[rect(-255,-172,510,324,C.stone),rect(-255,144,510,16,C.wood),text('Separate test',-103,-135,25,C.ink),text('Hypothetical',-103,-104,24,C.ink),rect(63,-95,157,239,C.paper),path('M65 -94L166 -69V126L65 144Z',C.teal,3)],1,'A visibly separate institutional test with a different adult and official, not a claim that the warm earlier family seized documents.');
 person('applicant',169,530,{identity:'person-09-neutral',coat:C.plum,scale:.68});person('official',502,530,{identity:'person-02-neutral',coat:C.cobalt,scale:.66});
 put('counter',366,441,[rect(-102,-7,204,17,C.wood),rect(-95,10,190,72,C.coral),path('M-75 21H75M-75 53H75',C.paper,4)],1,'An administrative drawer can hold the papers despite a formally open exit.');
 put('exit-notice',498,266,[rect(-79,-41,158,82,C.paper),text('Exit permitted',0,-4,25,C.ink),path('M-31 21H30M20 12L31 21L20 30',C.teal,4)],1,'A formal declaration is tested against practical conditions.');
 put('identity-record',317,472,[rect(-47,-31,94,62,C.paper),dot(-22,-6,9,C.plum),path('M-34 19V8Q-22 -1 -10 8V19',C.plum,6),text('Identity',12,4,19,C.ink)],2,'An unspecified identity document remains at the local office; no personal data is generated.');
 put('drawer-front',326,477,[rect(-70,-37,140,75,C.coral),text('Identity papers',0,-8,19,C.ink),path('M-22 15H22',C.wood,5)],2,'The held record is a concrete obstacle, not a locked symbolic gate.');delay('drawer-front','appear',1700);
 put('unconfirmed-room',954,354,[rect(-127,-113,254,220,C.paper),rect(-127,99,254,16,C.wood),text('Accommodation?',0,-74,27,C.ink),rect(-97,16,194,19,C.teal),rect(-91,-7,56,25,C.stone),path('M-96 35V94M97 35V94',C.wood,10)],2,'A place to go remains a practical question, not an instant housing allocation.');
 put('case-bag',696,514,[rect(-30,-25,60,51,C.plum),path('M-13 -26V-40H14V-26',C.wood,5)],2,'A destination and transition have to exist for practical exit.');mood('applicant',2,'worried');storyGesture(q,'applicant',2,'question');
 q.hide('unconfirmed-room',3);q.hide('case-bag',3);
 put('intervention-plan',885,332,[rect(-203,-139,406,278,C.paper),text('Intervention scope',0,-101,28,C.ink),rect(-172,-67,265,149,C.stone),rect(-172,-67,265,12,C.coral),rect(-131,-22,100,16,C.wood),dot(68,30,18,C.olive),rect(117,-10,57,91,C.teal)],3,'A separate planning view tests whether outside protection wrongly erases the whole communal setting.');
 put('overbroad-mark',840,340,[path('M-135 -46L138 80M-134 79L139 -45',C.coral,10)],3,'A proposed overbroad intervention would erase valuable shared life; it is never executed in the scene.');
 person('support-person',1094,533,{identity:'person-12-neutral',coat:C.teal,scale:.58,b:3});storyGesture(q,'support-person',3,'question');
 q.hide('overbroad-mark',4);put('limited-scope',1029,366,[path('M-41 -36H41V66H-41Z',C.cobalt,7)],4,'The proposal narrows to a record and appeal obstacle, rather than eliminating the community; this is a scope decision, not a completed legal victory.');
 storyGesture(q,'support-person',4,'explain');mood('applicant',4,'curious');storyGesture(q,'official',5,'reflect');
 scenes[2].visual=q.finish('A visibly separate hypothetical case uses different people at a community counter. Exit is formally permitted, but papers remain in a drawer and accommodation is unresolved. A proposed overbroad intervention is marked on a planning drawing, then its scope narrows to the obstructed record/appeal route. The community is never physically erased; no family is retroactively proven abusive and no safe exit is guaranteed.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,delay,mood,plant,prospectus,photo}=setup(q);
 put('local-counter',238,433,[rect(-135,-5,270,17,C.wood),rect(-121,12,242,82,C.coral),path('M-104 30H104M-104 60H104',C.paper,4)],1,'The unresolved local request supplies a specific reason to seek review elsewhere.');
 person('local-official',161,534,{identity:'person-02-neutral',coat:C.cobalt,scale:.63});person('applicant',434,534,{identity:'person-09-neutral',coat:C.plum,scale:.65});
 put('review-room',741,359,[rect(-129,-125,258,294,C.paper),rect(-129,151,258,17,C.wood),text('Independent appeal',0,-83,26,C.ink),rect(-85,44,170,12,C.wood),path('M-68 56V146M68 56V146',C.wood,10)],1,'An outside reviewer provides another route to be heard, not an automatic favorable judgment.');
 person('reviewer',741,530,{identity:'person-12-neutral',coat:C.teal,scale:.61});
 put('request',377,470,[rect(-62,-34,124,68,C.paper),text('Documents',0,-8,24,C.ink),path('M-35 14H34',C.cobalt,4)],1,'A concrete document-access request crosses beyond the local official’s sole account.');q.move('request',2,658,469,2600);q.move('applicant',2,532,534,2200);storyGesture(q,'applicant',2,'question');storyGesture(q,'reviewer',2,'reflect');
 put('courtyard-continuity',1013,389,[rect(-113,-90,226,230,C.stone),rect(-113,-90,226,14,C.coral),rect(-113,125,226,15,C.wood),rect(-80,17,140,12,C.wood),path('M-66 29V116M43 29V116',C.wood,8),n('ellipse',{cx:-10,cy:4,rx:27,ry:9,fill:C.coral})],2,'The shared courtyard continues while a specific obstruction is contested; belonging itself is not abolished.');
 plant('courtyard-herb',1091,487,2,.6);person('neighbor',956,526,{identity:'person-02-neutral',coat:C.coral,scale:.43,b:2});
 storyGesture(q,'reviewer',3,'explain');mood('applicant',3,'curious');
 for(const id of ['local-counter','local-official','applicant','review-room','reviewer','request','courtyard-continuity','courtyard-herb','neighbor'])q.hide(id,4);
 person('adult-daughter',217,535,{identity:'person-04-neutral',coat:C.cobalt,scale:.72,b:4});
 put('book',769,351,[n('path',{d:'M-265 -144Q-128 -165 0 -137Q127 -165 265 -144V148Q131 120 0 146Q-135 120 -265 148Z',fill:C.paper}),path('M0 -138V147',C.wood,4),text('The Bridge',-134,-73,30,C.ink),text('Method',-134,-29,31,C.ink),text('Capture by',135,-71,30,C.ink),text('Pluralism',135,-27,31,C.ink),path('M-220 25H-49M-220 52H-77M44 26H220M44 55H176',C.teal,4)],4,'The source’s bridge-method section and Capture by Pluralism offer the explicit reading route from conversation to institutional restraint.');
 put('book-rest',769,520,[rect(-281,-8,562,16,C.wood)],4,'A real source volume carries the reading invitation, not a generic branded book icon.');prospectus('study-plan',383,481,4);photo('family-photo',339,274,4);storyGesture(q,'adult-daughter',4,'reflect');mood('adult-daughter',5,'curious');storyGesture(q,'adult-daughter',5,'invite');
 scenes[3].visual=q.finish('An unresolved documents request reaches an independent reviewer while local testimony remains distinct. The community’s ordinary meal and gardening continue, so targeted scrutiny does not erase belonging. No legal victory or completed relocation is invented. The adult daughter returns for the final reading invitation, retaining both study plans and family memory.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
