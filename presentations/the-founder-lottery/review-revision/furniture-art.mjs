import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
export function furnitureArt(i){
 const a=stageAuthor(),blue='#3d668c',wood='#b98a5d',red='#bd6451',cream='#f1e4cf',gold='#dfb550',ink='#2c3e50';
 const put=(id,x,y,n,b=1,meaning=id,scale=1)=>{a.add(a.object(id,x,y,n,meaning,scale));a.reveal(id,b,950);};
 const rect=(x,y,w,h,fill)=>a.n('rect',{x,y,width:w,height:h,rx:5,fill});
 const txt=(s,x,y,z=29,c=ink)=>a.text(s,x,y,z,c);
 const bench=(id,x,y,b=1)=>put(id,x,y,[rect(-130,0,260,15,blue),a.path('M-100 16V88M100 16V88',wood,17)],b,'A maintained work surface supports the craft');
 const chair=(id,x,y,b=1,scale=1)=>put(id,x,y,[rect(-68,-115,136,76,wood),a.path('M-63 -38V0M63 -38V0M-79 0H79M-62 10V108M62 10V108',wood,16),a.dot(62,17,11,gold)],b,'Illustrative repairable chair with a replaceable fastened joint; no certified product',scale);
 const page=(id,x,y,title,b=1)=>put(id,x,y,[rect(-110,-94,220,188,cream),txt(title,0,-51,title.length>16?23:29),a.path('M-75 -13H75M-75 20H75M-75 54H43',blue,6)],b,'A concrete shared work record: '+title);
 const person=(id,x,y,b=1,other=false)=>{storyPerson(a,id,x,y,{identity:other?'person-09-neutral':'person-04-neutral',coat:other?blue:red,scale:.88});a.reveal(id,b);};
 const floor=(id,x,y,w=950)=>put(id,x,y,[rect(-w/2,0,w,8,cream)],1,'Quiet support line, not a decorative grid');
 if(i===0){
  floor('floor',600,545);person('maker',200,535);bench('bench',500,450);chair('chair',500,368,1,.68);
  put('joint',590,390,[a.path('M0 -35V35',wood,19),a.dot(0,-19,11,gold)],1,'A replacement part requires work, beyond public success stories');a.move('joint',3,542,383,1800);
  page('profile',990,235,'Winner profile',2);page('work-notes',790,444,'Unfinished work',3);
  storyGesture(a,'maker',3,'reflect');storyGesture(a,'maker',5,'explain');
 }
 if(i===1){
  floor('floor',600,550);page('profile',990,260,'Visible winner',1);
  for(let j=0;j<3;j++){const x=190+j*270;bench('work'+j,x,450,j+2);chair('chair'+j,x,391,j+2,.48);}
  person('maker',110,536,2);person('other',750,536,4,true);
  page('unpaid-time',525,225,'Time and costs',3);
  storyGesture(a,'maker',5,'reflect');storyGesture(a,'other',6,'question');
 }
 if(i===2){
  floor('floor',600,547);put('design',320,270,[rect(-185,-110,370,220,blue),txt('Design assistance',0,-68,31,cream),...[-95,0,95].map(x=>a.path(`M${x-27} -26H${x+27}V31H${x-27}Z`,cream,5))],1,'More producible designs do not by themselves supply customer trust');
  chair('chair',330,482,2,.6);chair('second-chair',535,482,3,.6);person('customer',1000,533,3,true);
  put('question',890,230,[txt('Can it be repaired?',0,0,33,'$ink')],3,'A specific customer question concerns dependable service');
  page('history',780,423,'Service history?',4);storyGesture(a,'customer',4,'question');
 }
 if(i===3){
  floor('floor',600,548);person('writer',170,539);bench('writing',350,444);
  put('maker-a',170,223,[txt('Maker A',0,0,28,'$ink')],1,'Illustrative contributor identity; not a real operator or study participant');
  put('instruction',350,335,[rect(-120,-96,240,192,cream),txt('Repair guide R1',0,-61,28),a.path('M-75 -29H25V-5M25 15V48',wood,13),a.path('M62 -18V32',gold,10),a.path('M-30 7H8M-2 0L8 7L-2 14',blue,3),rect(-112,57,224,32,blue),txt('Made by Maker A',0,80,23,cream)],1,'Conceptual guide R1 records an illustrated missing joint and retains Maker A’s credit during reuse');
  put('repair-chair',884,452,[rect(-68,-115,136,76,wood),a.path('M-63 -38V0M63 -38V0M-79 0H79M-62 10V108',wood,16),a.path('M62 10V25',gold,9)],3,'The second chair is genuinely missing its right lower member, so the copied instruction has an observable use',.86);
  person('repairer',1070,539,3,true);put('maker-b',1070,223,[txt('Maker B',0,0,28,'$ink')],3,'A distinct illustrative operator reuses the credited work');
  a.move('instruction',3,649,283,2100);a.move('repairer',3,792,539,2200);storyGesture(a,'repairer',3,'reflect');
  put('joint',1017,452,[a.path('M0 0V84',wood,15),a.dot(0,6,9,gold)],3,'The receiver has a matching part but consults the guide before fitting it');
  a.move('repairer',4,1060,539,2100);a.move('maker-b',4,1060,223,2100);a.move('joint',4,937.3,460.6,2100);storyGesture(a,'repairer',4,'resolve');storyGesture(a,'writer',4,'explain');
  put('responsibility',646,175,[txt('Who maintains guide R1?',0,0,33,'$ink')],5,'Authorship survives use, but responsibility for the next revision still needs governance');
 }
 if(i===4){
  floor('floor',600,546);bench('training',600,444);person('mentor',303,537);person('learner',904,537,2,true);
  put('mentor-label',303,228,[txt('Maker A',0,0,28,'$ink')],1,'The same illustrative contributor now teaches');put('learner-label',904,228,[txt('Maker B',0,0,28,'$ink')],2,'The receiving operator must practice, not merely stand beside a finished chair');
  put('joint-fixture',600,345,[rect(-114,-21,231,39,wood),a.path('M-77 23V96',wood,24),rect(29,16,41,18,cream),a.path('M50 19V29',gold,8)],1,'An enlarged chair corner on a practice bench has an actual missing lower member');
  put('demonstration',358,405,[a.path('M0 0V78',wood,28),a.dot(0,7,12,gold)],2,'The mentor demonstrates the matching removable member');
  a.move('demonstration',2,650,365,2200);storyGesture(a,'mentor',2,'explain');
  a.move('demonstration',3,839,400,1800);a.move('learner',3,815,537,1800);a.move('learner-label',3,815,228,1800);storyGesture(a,'learner',3,'reflect');
  put('turn',601,190,[txt('Now Maker B tries',0,0,31,'$ink')],3,'The assembly resets so the learner can independently repeat the demonstrated fit');
  a.move('demonstration',4,650,365,2100);storyGesture(a,'learner',4,'resolve');a.hide('turn',4);
  put('training-record',1066,300,[rect(-103,-75,206,150,cream),txt('Guide R1',0,-38,27),txt('Maker A taught',0,-1,23),txt('Maker B practiced',0,31,23)],4,'The same guide and a concrete teaching/practice record preserve usable institutional memory; no measured certification');
  storyGesture(a,'mentor',5,'invite');
 }
 if(i===5){
  floor('floor',600,550);put('promise',600,165,[txt('Repairable furniture',0,0,38,'$ink')],1,'The source’s illustrative narrow promise; displayed names and operators are conceptual');
  chair('chair-a',325,452,1,.86);person('operator-a',166,537);put('name-a',325,222,[rect(-116,-24,232,49,blue),txt('Shared Workshop',0,9,26,cream)],1,'Illustrative shared name, not a real brand or certification');
  chair('chair-b',829,452,2,.86);person('operator-b',1058,537,2,true);put('name-b',829,222,[rect(-116,-24,232,49,blue),txt('Shared Workshop',0,9,26,cream)],2,'A second independent operator initially uses the same proposed name');
  put('identity-a',166,260,[txt('Maker A',0,0,26,'$ink')],1,'Conceptual operator identity');put('identity-b',1058,260,[txt('Maker B',0,0,26,'$ink')],2,'The same receiving maker from the earlier scenes');
  put('registry',587,301,[rect(-116,-77,232,154,cream),txt('Example register',0,-44,25),txt('Maker A',0,-7,25),txt('Maker B',0,29,25)],2,'An illustrative operator register lets customers distinguish identities; no real authorization claim');
  put('guide-history',587,454,[rect(-127,-64,254,128,cream),txt('Repair guide R1',0,-31,26),txt('Made by Maker A',0,5,23),txt('Used by Maker B',0,40,23)],3,'The concrete record from the earlier repair persists rather than being replaced by a generic history label');
  put('joint',916,467,[a.path('M0 -21V77',wood,15),a.dot(0,-5,9,gold)],3,'The joint remains inspectable under the shared repair promise');a.move('joint',4,882.3,467,1400);
  a.hide('joint',5);a.move('chair-b',5,990,452,2500);a.move('operator-b',5,1110,537,2500);a.hide('identity-b',5);a.hide('name-b',5);
  put('fork-name',930,170,[rect(-122,-24,244,49,blue),txt('Workshop B branch',0,9,25,cream)],5,'A customer-facing distinct branch name appears while the original shared institution stays visible');
  put('carried-history',587,454,[rect(-127,-64,254,128,cream),txt('Repair guide R1',0,-31,26),txt('Made by Maker A',0,5,23),txt('Used by Maker B',0,40,23)],5,'A copy of the same credited history accompanies the exiting operator; the original copy remains');a.move('carried-history',5,930,269,2600);
  put('origin',587,205,[txt('From Shared Workshop',0,0,25,'$ink')],6,'Traceable origin makes the constitutional branch understandable without claiming a real institutional split');
 }
 if(i===6){
  floor('floor',600,549);person('maker',180,539);bench('bench',490,440);chair('chair',490,364,1,.7);
  page('manual-one',800,270,'Repair guide',1);page('manual-two',980,435,'Duplicate guide',1);
  a.hide('manual-two',3);put('maintained',800,411,[rect(-121,-27,242,54,blue),txt('Maintained together',0,10,25,cream)],3,'A shared maintained guide reduces duplication only if its coordination is worthwhile');
  storyGesture(a,'maker',4,'question');put('cost',500,183,[txt('Include coordination time',0,0,35,'$ink')],4,'The proposed cohort must compare real burdens, not assume a successful outcome');
 }
 if(i===7){
  floor('floor',600,548);bench('reading',600,447);person('reader',1000,537,1,true);
  put('book',590,326,[a.n('path',{d:'M-223 -100Q-108 -139 0 -93Q115 -139 223 -100V116Q115 89 0 131Q-115 89 -223 116Z',fill:cream}),a.path('M0 -93V131',gold,5),txt('The selection game',-114,-43,24),txt('Shared institutions',114,-43,24),a.path('M-189 0H-40M-189 36H-65M40 0H189M40 36H165',blue,6)],1,'Reading invitation joins the diagnosis to the proposed institutional alternative');
  put('joint',290,510,[a.path('M0 -45V35',wood,24),a.dot(0,-22,12,gold)],3,'The concrete repair example remains beside the book rather than an unrelated symbol');
  storyGesture(a,'reader',3,'reflect');storyGesture(a,'reader',7,'invite');
 }
 return a.finish('Conceptual repairable-furniture example from the source’s proposed shared-brand doctrine. Independent work, traceable instructions, teaching, narrow standards and constitutional exit acquire distinct visible actions. No measured business performance or real certification is claimed.');
}
