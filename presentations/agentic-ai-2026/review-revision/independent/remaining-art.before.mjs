import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
export function remainingVisual(i){
 const a=stageAuthor(),paper='#edf1e9',blue='#278da3',ink='#213b4b',copper='#bc673d',gold='#d9b85d';
 const put=(id,x,y,n,b=1,m=id)=>{a.add(a.object(id,x,y,n,m));a.reveal(id,b,850);};
 const t=(s,x,y,z=28)=>a.text(s,x,y,z,ink),r=(x,y,w,h,c=paper)=>a.n('rect',{x,y,width:w,height:h,rx:7,fill:c});
 const person=(id,x,y,b=1)=>{storyPerson(a,id,x,y,{identity:'person-09-neutral',coat:blue,scale:.78});a.reveal(id,b);};
 const book=()=>[a.n('path',{d:'M-110 -120Q-55 -144 0 -119Q60 -145 110 -120V110Q55 91 0 115Q-55 91 -110 110Z',fill:paper}),a.path('M0 -118V115',blue,4),t('Agentic AI',-55,-55,23),t('2026',-55,-23,26),a.path('M-89 10H-23M-89 34H-23M-89 58H-23M24 -60H87M24 -30H87M24 0H87M24 30H75',blue,4)];
 const docket=(heading,lines)=>[r(-170,-125,340,250),t(heading,0,-79,31),...lines.map((s,k)=>t(s,0,-22+k*43,25))];
 if(i===0){
  person('reader',260,510);put('volume',475,340,book(),1,'This particular book, not a generic AI object');storyGesture(a,'reader',2,'question');
  put('task',920,335,docket('Requested action',['Refund the order','Payment unchanged']),2,'Illustrative delegation awaiting execution');
  put('review',920,435,[r(-143,-23,286,46,copper),a.text('Review required',0,8,26,'#fff')],4,'Proposal is not automatic permission');
  storyGesture(a,'reader',5,'explain');
 }
 if(i===2){
  put('plan',285,330,docket('Refund task',['Find order','Check eligibility','Prepare request']),1,'An explicit revisable plan for the earlier hypothetical task');
  put('record',835,330,docket('Order record',['Order located','Receipt incomplete']),2,'An observation changes what is known');
  put('check',835,443,[r(-150,-24,300,48,copper),a.text('More evidence needed',0,8,24,'#fff')],3,'Verification discovers missing evidence instead of declaring success');
  put('correction',285,435,[r(-158,-24,316,48,'#d8e5e3'),t('Request missing receipt',0,8,24)],4,'Plan now reflects the observation');
  put('handoff',580,490,[a.text('Review handoff',0,0,28,'$ink')],5,'Other agents or reviewers introduce coordination work');
 }
 if(i===5){
  // A work docket, not a quantitative chart: every sheet is an activity.
  put('docket',490,325,[r(-320,-151,640,306),t('Work behind one answer',0,-109,36),a.path('M-280 -77H280',blue,3)],1,'Qualitative operational work ledger; no fabricated price or scale');
  put('call',320,292,[r(-125,-33,250,66,'#d3e2e2'),t('Model response',0,8)],1);
  put('tool',645,292,[r(-130,-33,260,66,'#e4d8bd'),t('Order lookup',0,8)],2);
  put('retry',320,393,[r(-125,-33,250,66,'#ebd3c4'),t('Repeated lookup',0,8,26)],3);
  put('review',645,393,[r(-130,-33,260,66,'#d6d2e4'),t('Human review',0,8,27)],3);
  person('reviewer',970,510,3);storyGesture(a,'reviewer',3,'reflect');
  a.hide('retry',4);put('reused',320,393,[r(-125,-33,250,66,'#d3e2e2'),t('Reuse valid record',0,8,25)],4,'A constrained alternative can avoid repeating valid work');
  storyGesture(a,'reviewer',6,'question');
 }
 if(i===6){
  put('requests',300,315,docket('Customer request',['Return this order','I need a refund']),1,'Different wording can describe a similar operation');
  put('policy',855,330,[r(-205,-145,410,290),t('Action permissions',0,-96,33),t('Read order',-50,-32,28),t('Prepare request',-30,16,28),t('Issue refund',-44,65,28),a.path('M125 -41L135 -30L153 -53M125 7L135 18L153 -5',blue,5),r(119,43,34,32,copper)],2,'Interpretation may vary while external authority stays constrained');
  put('unfamiliar',300,394,[r(-158,-26,316,52,'#ead1bf'),t('A different problem',0,8,28)],3,'Open interpretation is needed for an unfamiliar request');
  a.hide('unfamiliar',4);put('escalate',300,394,[r(-158,-26,316,52,'#d3e2e2'),t('Ask for clarification',0,8,27)],4,'Useful fallback without granting broader payment authority');
  put('held',855,505,[a.text('Payment still requires approval',0,0,27,'$ink')],4);
 }
 if(i===7){
  put('stable',285,300,[r(-177,-132,354,264),t('Stable procedure',0,-82,32),a.path('M-135 -40H135M-135 0H70M-135 40H115',blue,6),t('Tested version',0,92,25)],1,'Reusable code with a known version and assurance history');
  put('generated',900,300,[r(-185,-132,370,264),t('Generated program',0,-82,31),a.path('M-133 -34L-155 -10L-133 14M133 -34L155 -10L133 14',copper,5),t('Run in isolation',0,12,26),t('Tests before use',0,86,25)],2,'Task-adapted code is untrusted and needs isolation and evaluation');
  a.hide('stable',4);a.hide('generated',4);
  put('named',600,320,[r(-365,-145,730,290),t('Named working state',0,-95,35),t('order_id',-220,-22,27),t('eligibility',0,-22,27),t('approval',220,-22,27),t('Known',-220,44,25),t('Needs receipt',0,44,25),t('Pending',220,44,25)],4,'Illustrative named intermediate values rather than a transcript; not a claimed MRP-VM product screen');
  put('question',600,520,[a.text('What improves under the same test?',0,0,30,'$ink')],5,'Comparative evidence remains necessary');
 }
 if(i===8){
  put('open-book',380,340,book(),1,'Reader returns to the actual book');
  person('reader',160,515);storyGesture(a,'reader',2,'reflect');
  put('case',865,325,docket('Your delegated task',['What can change?','What evidence is needed?','Who can approve?']),1,'Reading invitation applied to a consequential task');
  put('bookmark',380,455,[a.path('M18 -210V18L32 7L47 18V-210',copper,7)],2,'Return to architecture and evaluation chapters');
  storyGesture(a,'reader',5,'invite');
 }
 return a.finish('The source argument is staged through the continuing refund task, its real work and authority boundaries; runtime internals are illustrative named records, and no measured benchmark or product screen is invented.');
}
