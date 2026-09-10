import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const root=new URL('../',import.meta.url),file=new URL('work/scenes.json',root),scenes=JSON.parse(fs.readFileSync(file));
for(let i=0;i<scenes.length;i++){
 const a=stageAuthor(),ink='#333b59',plum='#76557f',coral='#cd785c',cream='#f0e6d8',teal='#427e83';
 const t=(s,x,y,z=28)=>a.text(s,x,y,z,ink),r=(x,y,w,h,fill=cream)=>a.n('rect',{x,y,width:w,height:h,rx:7,fill});
 const put=(id,x,y,n,b=1,m=id)=>{a.add(a.object(id,x,y,n,m));a.reveal(id,b,750);};
 const person=(id,x,y,b=1,seated=false,coat=plum,identity='person-18-neutral')=>{storyPerson(a,id,x,y,{identity,coat,seated,scale:.85,chair:coral});a.reveal(id,b);};
 const desk=(id,x,y,w,b=1)=>put(id,x,y,[r(-w/2,-12,w,24,coral),a.path(`M${-w/2+15} 12V122M${w/2-15} 12V122`,coral,13)],b,'A physical work surface');
 const screen=(title,lines)=>[r(-175,-110,350,215,ink),r(-158,-94,316,177,cream),t(title,0,-52,30),...lines.map((s,k)=>t(s,0,-8+k*35,25)),a.path('M0 108V134M-65 134H65',ink,13)];
 if(i===0){
  person('worker',260,555,1,true);desk('workbench',415,445,400);put('computer',530,330,screen('Work checked',['Tests passed','Draft revised']),1,'Illustrative verified private assistance');
  put('doorway',995,310,[a.path('M-110 200V-175H110V200',teal,20)],2,'Boundary between individual work and accepted workplace practice');
  person('colleague',1000,525,2,false,teal,'person-07-neutral');storyGesture(a,'worker',2,'reflect');storyGesture(a,'colleague',3,'question');
  put('question',700,178,[a.text('Can we rely on it?',0,0,33,'$ink')],3,'Legitimacy and responsibility remain unsettled');
 }
 if(i===1){
  put('public',285,300,[r(-210,-145,420,290,coral),r(-188,-125,376,245),t('Public post',0,-76,34),t('Citation not found',0,-17,29),a.path('M-140 32H140M-140 60H70',ink,5)],1,'Unspecified invented citation as source-described visible failure');
  put('tested',900,300,screen('Private work',['Code reviewed','Tests passed']),1,'Source describes tested code absorbed into the final product');
  put('share',285,490,[a.path('M-120 0H120M90 -22L120 0L90 22',coral,7),a.text('Circulates publicly',0,53,27,'$ink')],2,'Memorable failure spreads');
  a.hide('tested',2);put('result',900,300,[r(-160,-134,320,268),t('Finished work',0,-70,32),a.path('M-112 -25H112M-112 12H112M-112 50H65',teal,6)],2,'Useful assistance leaves no necessary public signature');
  put('uncertain',610,470,[a.text('An uneven sample',0,0,30,'$ink')],3,'A hypothesis about observation, not measured hidden success');
 }
 if(i===2){
  person('worker',290,540,1,false,plum);person('reviewer',965,540,1,false,teal,'person-07-neutral');
  desk('review-table',635,430,450);put('work',630,300,[r(-170,-130,340,260),t('Proposed practice',0,-82,32),t('Result checked',0,-25,28),t('Reviewer assigned',0,22,27),t('Data boundary agreed',0,69,25)],2,'Specific responsibilities behind social permission');
  storyGesture(a,'worker',1,'explain');storyGesture(a,'reviewer',2,'question');storyGesture(a,'worker',3,'resolve');
  put('decision',630,505,[a.text('Discuss the conditions',0,0,31,'$ink')],3,'People decide an accepted practice; no automatic approval');
 }
 if(i===3){
  person('learner',250,545,1,false,coral,'person-12-neutral');
  put('practice',790,305,[r(-260,-155,520,310),t('Assisted practice',0,-107,33),t('x + 3 = 7',0,-30,52),t('Answer: x = 4',0,47,32)],1,'Invented simple teaching example, not a task from the reported study');
  a.hide('practice',2);put('unaided',790,305,[r(-260,-155,520,310),t('Without assistance',0,-107,33),t('x + 5 = 12',0,-30,52),t('Explain your next step',0,51,28)],2,'Changed problem tests transfer, no score or result inferred');
  storyGesture(a,'learner',2,'reflect');a.hide('unaided',3);
  put('tutor',790,305,[r(-260,-155,520,310),t('Tutor prompt',0,-107,33),t('x + 5 = 12',0,-36,45),t('What keeps both sides equal?',0,30,28),t('Explain your next step',0,86,28)],3,'A teacher preserves a reasoned step rather than only delivering an answer');
  storyGesture(a,'learner',3,'explain');
 }
 if(i===4){
  person('reader',290,535,1,false,plum);desk('reading',495,425,280);
  put('book',495,320,[a.n('path',{d:'M-105 -110Q-45 -125 0 -106Q55 -125 105 -110V91Q50 80 0 104Q-55 82 -105 91Z',fill:cream}),a.path('M0 -104V102',plum,4),t('Adoption',-52,-52,24),t('states',-52,-20,24),t('Working',53,-52,24),t('practice',53,-20,24),a.path('M-87 18H-20M-87 46H-20M20 18H88M20 46H88',plum,4)],1,'Return to the actual book and its first chapter');
  put('case',920,310,[r(-170,-123,340,246),t('One real practice',0,-75,31),t('Repeatable?',0,-20,27),t('Acceptable?',0,22,27),t('Learning retained?',0,65,27)],2,'Reader applies the book to an actual practice of their choosing');
  storyGesture(a,'reader',2,'question');storyGesture(a,'reader',4,'invite');
 }
 scenes[i].visual=a.finish('Source-specific adoption introduction: verified private work, visible failed citation, negotiated responsibility, and assisted versus unaided learning; people and tasks are original illustrations, not reported experimental subjects.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
