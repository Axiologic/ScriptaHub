import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#34435f',blue:'#7096bf',papaya:'#da9279',yellow:'#e2bd62',lilac:'#aa94ba',paper:'#f5e8ce',wood:'#b28d6f',teal:'#79a89c'};
function setup(q){const{n,path,text,dot}=q;const rect=(x,y,w,h,fill,rx=5)=>n('rect',{x,y,width:w,height:h,fill,rx});const put=(id,x,y,children,b=1,meaning=id)=>{q.add(q.object(id,x,y,children,meaning));q.reveal(id,b,1100);};const person=(id,x,y,{identity='person-02-neutral',coat=C.blue,scale=.89,b=1,seated=false}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.lilac});q.reveal(id,b);};const mood=(id,b,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:1100});
 const bucket=(id,x,y,b=1)=>put(id,x,y,[n('path',{d:'M-37 -40H37L29 32H-29Z',fill:C.teal}),path('M-39 -40Q0 -70 39 -40',C.ink,3),path('M-23 13H23',C.blue,6)],b,'A real household task, not a measure of existential value.');
 return{rect,put,person,mood,bucket};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,bucket}=setup(q);
 person('thinker',250,531,{coat:C.lilac});person('resident',1090,531,{identity:'person-04-neutral',coat:C.papaya});
 put('long-argument',475,385,[n('path',{d:'M-128 -73H108Q137 -75 137 -49V73Q139 102 107 98H-91Q-127 99 -127 73Z',fill:C.paper}),path('M-128 -72Q-162 -73 -162 -49Q-162 -29 -127 -31M-106 98Q-143 99 -143 72',C.wood,6),text('An ultimate answer',0,-25,29,C.ink),path('M-93 10H101M-93 39H85M-93 68H111',C.wood,4)],1,'An impressive argument is a conceptual prop; the phrase is not a claimed quotation from the source.');
 put('eave',872,253,[n('path',{d:'M-165 25L-48 -34L44 -5L133 22L148 39H-165Z',fill:C.wood}),path('M-148 49H145',C.papaya,13),rect(-43,-12,26,41,C.paper,0)],1,'A small damaged eave makes a nearby practical obligation visible on a quiet stage.');
 bucket('bucket',842,505);put('leak',842,382,[path('M0 -83V-68M0 -30V-15M0 22V38M0 71V83',C.blue,5)],1,'The person must attend to a leak while the other reads a grand explanation.');
 mood('thinker',1,'curious');storyGesture(q,'thinker',2,'explain');mood('resident',2,'skeptical');storyGesture(q,'resident',2,'question');
 storyGesture(q,'thinker',3,'reflect');q.hide('long-argument',4);q.move('thinker',4,628,531,2800);mood('thinker',4,'curious');storyGesture(q,'thinker',4,'invite');
 scenes[0].visual=q.finish('The book’s serious comedy is illustrated by a grand argument meeting a nearby roof leak and an affected adult. The thinker turns toward the person rather than dismissing philosophy or treating labor as simple consolation.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood}=setup(q);
 person('caller',212,532,{coat:C.lilac});person('support',993,526,{identity:'person-04-neutral',coat:C.blue,seated:true});
 put('support-counter',941,456,[rect(-149,-21,297,100,C.papaya),rect(-164,-39,327,23,C.wood),text('Cosmic support',0,24,30,C.ink)],1,'A plainly theatrical support counter from the book’s imaginary interlude, not a religious deity or empirical history.');
 put('handset',252,346,[path('M-18 -23Q17 -3 11 34',C.ink,14),path('M-23 -27L-8 -39M8 33L-5 45',C.ink,17)],1,'Humanity’s imaginary call to existence.');
 put('cord',575,431,[path('M-311 -43Q-226 77 -160 20Q-94 -22 -22 33Q76 84 154 -2',C.blue,5)],1,'A physical telephone cord locates the comic conversation.');
 put('empty-sleeve',410,413,[rect(-64,-72,128,143,C.paper),n('path',{d:'M-54 -62H54V31L0 6L-54 31Z',fill:'#fff8ed'}),text('Manual?',0,61,27,C.ink)],1,'The source’s complaint that the product arrived without a user manual.');
 put('restart-offer',679,247,[rect(-137,-56,274,112,C.paper),text('Restart civilization?',0,10,27,C.ink)],2,'The comic support suggestion; no actual reset or quantitative history is claimed.');
 put('old-record',569,369,[rect(-80,-68,160,137,C.wood),rect(-64,-55,128,105,C.paper)],2,'An imaginary record loses pages in the joke, rather than an animated planet being destroyed.');
 put('lost-pages',569,369,[rect(-56,-42,111,82,C.paper),path('M-36 -20H35M-36 0H35M-36 20H12',C.blue,3)],2,'The caller’s claim of previous data loss belongs to the explicitly fictional support exchange.');q.move('lost-pages',2,700,496,2700);q.hide('lost-pages',2);q.actions.find(x=>x.actor==='lost-pages'&&x.action==='disappear').offsetMs=4500;
 mood('caller',2,'surprised');storyGesture(q,'caller',2,'question');storyGesture(q,'support',2,'reflect');
 for(const id of ['caller','support','support-counter','handset','cord','empty-sleeve','restart-offer','old-record'])q.hide(id,3);
 put('lived-question',335,342,[rect(-204,-135,408,275,C.paper),text('How does life',0,-78,34,C.ink),text('feel meaningful?',0,-33,34,C.ink),...[0,1,2,3,4].map(k=>rect(-145+k*65,31,30,30,C.blue,2)),text('A question we can study',0,110,26,C.ink)],3,'Psychology studies experienced meaning; the boxes represent a questionnaire, not a displayed result.');
 put('cosmic-question',872,342,[rect(-204,-135,408,275,C.paper),text('Was life intended?',0,-65,34,C.ink),text('?',0,40,79,C.lilac),text('A different question',0,110,26,C.ink)],3,'An unresolved metaphysical question is not answered by the adjacent psychological instrument.');
 scenes[1].visual=q.finish('The actual Cosmic Customer Support interlude becomes an imaginary phone conversation with missing manual and data-loss complaint. It then yields to two distinct questions, preserving the difference between empirical lived meaning and cosmic intention without merging religious doctrines.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,bucket}=setup(q);
 put('house-cutaway',683,453,[path('M-231 -100V90H239V-100',C.wood,14),rect(-205,80,420,17,C.wood),rect(137,-79,75,111,C.paper),path('M174 -77V28',C.blue,4)],1,'A household interior provides the beneficiary and material consequence of the source’s roof example.');
 put('roof',683,269,[n('path',{d:'M-271 87L-31 -21L-49 15L-221 99Z',fill:C.papaya}),n('path',{d:'M-3 -9L267 87L218 99L7 21Z',fill:C.papaya}),path('M-225 98H220',C.wood,12)],1,'A missing tile leaves a visible opening, so fitting it will change what happens below.');
 person('repairer',830,337,{identity:'person-02-neutral',coat:C.blue,scale:.64});person('resident',513,535,{identity:'person-04-neutral',coat:C.papaya,scale:.55});
 bucket('bucket',667,506);put('leak',667,400,[path('M0 -102V-83M0 -42V-25M0 8V25M0 57V72',C.blue,5)],1,'Rain crosses the roof opening and reaches the bucket.');
 put('storm',244,227,[n('path',{d:'M-63 23Q-99 -12 -61 -30Q-45 -65 -11 -38Q31 -61 49 -22Q90 -19 72 20Z',fill:C.lilac}),path('M-41 51L-55 81M-2 51L-16 81M37 51L23 81',C.blue,5)],2,'Approaching weather gives the repair limited time and practical stakes.');q.move('storm',2,337,227,2500);
 put('replacement-tile',754,315,[n('path',{d:'M-34 -14L21 -32L45 -4L-11 17Z',fill:C.yellow}),path('M-24 -10L21 -24',C.wood,3)],1,'A matching repair tile is a task-specific object, not a formula for happiness.');
 storyGesture(q,'repairer',1,'reflect');storyGesture(q,'resident',2,'question');mood('repairer',2,'worried');storyGesture(q,'repairer',3,'explain');
 put('time-note',265,411,[text('Before the storm',0,0,29,'$ink')],4,'Finitude means not every possibility can be postponed.');storyGesture(q,'repairer',4,'reflect');
 q.move('replacement-tile',5,672,267,2600);q.hide('leak',5);q.actions.find(x=>x.actor==='leak'&&x.action==='disappear').offsetMs=2650;
 q.move('bucket',5,738,507,2500);q.actions.find(x=>x.actor==='bucket'&&x.action==='moveTo').offsetMs=2800;storyGesture(q,'repairer',5,'resolve');mood('resident',5,'relieved');
 scenes[2].visual=q.finish('One concrete roof repair explains the proposed FIRE dimensions: approaching storm gives stakes, understood commitment organizes action, a resident matters, and the fitted tile changes an actual condition. The scene is a conceptual example, not an experiment, psychological scale or roof-work instruction.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood}=setup(q);
 put('dry-room',335,372,[n('path',{d:'M-185 -86L0 -173L185 -86L171 -60L0 -136L-169 -60Z',fill:C.papaya}),path('M-164 -60V161H157V-61',C.wood,13)],1,'The repaired household is protected, but that fact alone cannot justify who is excluded.');
 person('resident',286,532,{identity:'person-04-neutral',coat:C.papaya,scale:.71});person('repairer',632,535,{coat:C.blue,scale:.81});
 put('other-eave',972,245,[n('path',{d:'M-144 20L-51 -24L36 -2L128 28L115 47H-139Z',fill:C.wood}),rect(-41,-7,28,41,C.paper,0)],2,'Another household remains exposed; no ethnicity, religion or diagnosis is assigned to the excluded person.');
 person('excluded',1003,535,{identity:'person-09-neutral',coat:C.yellow,scale:.73,b:2});put('rain',944,408,[path('M0 -100V-85M0 -56V-40M0 -10V7M0 39V56M0 86V99',C.blue,5)],2,'The question is whose suffering a coherent community leaves outside its care.');
 put('closed-entrance',777,443,[rect(-46,-84,93,174,C.lilac),path('M-31 -69V73M0 -69V73M31 -69V73',C.paper,4),dot(26,13,6,C.ink)],2,'A closed entrance illustrates exclusion, not a measured policy or a resolved fictional plot.');
 storyGesture(q,'repairer',2,'question');mood('repairer',2,'worried');mood('excluded',2,'worried');
 put('payment',492,430,[rect(-61,-35,122,72,C.paper),path('M-60 -33L0 8L61 -33',C.wood,3),text('Wages?',0,30,24,C.ink)],3,'The source demands fair material treatment before rhetorical praise; no amount or wage outcome is invented.');q.move('payment',3,407,430,2100);storyGesture(q,'repairer',3,'question');
 for(const id of ['dry-room','resident','excluded','other-eave','rain','closed-entrance','payment'])q.hide(id,4);
 q.move('repairer',4,252,535,2600);
 put('reading-table',818,474,[rect(-257,-13,515,21,C.wood),path('M-229 8V66M229 8V66',C.wood,12)],4,'The closing invites reading rather than pretending the examples settle philosophy.');
 put('book',818,354,[n('path',{d:'M-249 -135Q-121 -158 0 -130Q123 -158 249 -135V119Q125 96 0 121Q-126 96 -249 119Z',fill:C.paper}),path('M0 -130V120',C.wood,3),text('Those who need',-125,-72,28,C.ink),text('the question',-125,-30,28,C.ink),text('Eight ordinary',124,-72,29,C.ink),text('cosmologies',124,-30,29,C.ink),...[-1,1].map(d=>path(d<0?'M-213 21H-38M-213 55H-60':'M37 21H211M37 55H190',C.blue,4))],4,'Actual reading route to the chapter and explicitly fictional composite witnesses; no invented interview evidence.');
 storyGesture(q,'repairer',4,'invite');mood('repairer',5,'curious');
 scenes[3].visual=q.finish('The repaired roof is contrasted with another person left in rain, then with wages rather than symbolic dignity. No tradition is stereotyped and no reform or payment is resolved. The same ordinary-care example motivates the real book and its fictional witnesses.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
