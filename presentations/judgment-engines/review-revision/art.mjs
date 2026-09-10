import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
export function judgmentVisual(i){
 const a=stageAuthor(),ink='#34365b',red='#b84e50',gold='#dfaf4e',paper='#f4ead9',blue='#466f96';
 const put=(id,x,y,n,b=1,meaning=id)=>{a.add(a.object(id,x,y,n,meaning));a.reveal(id,b,850);};
 const t=(s,x,y,z=30,c=ink)=>a.text(s,x,y,z,c);
 const r=(x,y,w,h,c,rx=6)=>a.n('rect',{x,y,width:w,height:h,rx,fill:c});
 const doc=(title,rows=3)=>[a.n('path',{d:'M-110 -120H72L110 -82V120H-110Z',fill:paper}),a.path('M72 -120V-82H110',gold,4),t(title,0,-66,title.length>14?23:29),...Array.from({length:rows},(_,k)=>a.path(`M-75 ${-25+k*34}H${k%2?40:75}`,blue,6))];
 const latch=(x,y,b=1)=>{put('release',x,y,[r(-125,-95,250,190,ink),t('Release',0,-48,34,paper),a.path('M-65 58V-15H65V58',gold,13),a.path('M-72 12H72',red,17)],b,'Release is held closed by a failed required check');};
 if(i===0){
  put('bench',585,500,[r(-475,0,950,14,blue),a.path('M-400 14V57M400 14V57',blue,13)],1,'An inspection bench supports a specific proposed change');
  put('patch',285,345,doc('Code patch'),1,'Source conceptual patch example, not an executed product test');
  put('explanation',570,340,doc('Clear explanation',4),1,'Prose quality remains visible beside behavior');
  latch(960,350,2);
  put('failed',285,417,[r(-94,-27,188,54,red),t('Test failed',0,11,30,'#fff')],1,'Failed required test cannot be compensated by style');
  put('criterion',690,175,[t('Required: working behavior',0,0,34,'$ink')],3,'Explicit standard establishes why the gate is closed');
  a.move('failed',4,955,405,1900);
 }
 if(i===1){
  put('average',245,275,[a.n('ellipse',{cx:0,cy:0,rx:130,ry:100,fill:paper}),t('One average',0,-22,31),a.path('M-61 25H61M0 -1V51',blue,9)],1,'Flat averaging can allow unrelated strengths to offset failure');
  put('note',245,465,[t('Clarity + failure?',0,0,30,'$ink')],1,'No numerical score or fabricated acceptance threshold');
  put('no-average',245,275,[a.path('M-95 70L95 -70',red,13)],2,'Rejected compensation rule');
  latch(870,325,2);
  put('required',595,320,[r(-110,-53,220,106,red),t('Test failed',0,-4,32,'#fff'),t('Required check',0,32,23,'#fff')],3,'Required failure reaches the release control');
  a.move('required',3,850,345,1500);
  put('clarity',570,480,[t('Clarity remains a finding',0,0,31,'$ink')],4,'Independent prose assessment does not cancel a functional failure');
 }
 if(i===2){
  put('runner',300,320,[r(-180,-124,360,245,ink),t('Test runner',0,-76,36,paper),a.path('M-132 -20L-104 0L-132 20M-80 25H-24',gold,7),t('Recorded result',35,5,25,paper),r(-145,58,290,35,red)],1,'Bounded execution produces observable evidence');
  put('result',530,400,[r(-105,-58,210,116,paper),t('Observed',0,-9,29),t('test failure',0,28,29,red)],1,'Observed result is retained throughout semantic review');
  put('requirement',900,290,doc('Intended behavior'),2,'Requirement is separate from existing tests');
  put('uncovered',890,445,[r(-142,-55,284,110,paper),t('Untested case?',0,0,31),t('Review the requirement',0,36,22)],3,'An open question about coverage, not a claimed repaired implementation');
  put('lens',858,270,[a.n('circle',{cx:0,cy:0,r:62,fill:'none',stroke:gold,'stroke-width':9}),a.path('M45 47L87 91',gold,14)],3,'Review inspects intent while retaining the executable result');
  a.move('lens',3,910,285,1500);
 }
 if(i===3){
  put('short-answer',315,285,[r(-175,-95,350,190,paper),t('Core answer',0,-47,31),a.path('M-128 -2H128M-128 37H60',blue,8)],1,'A writing example examines length as an inappropriate proxy');
  put('long-answer',845,320,[r(-175,-130,350,330,paper),t('Same core answer',0,-82,31),a.path('M-128 -36H128M-128 3H60',blue,8)],2,'The same substantive answer is padded, not improved');
  put('padding',845,400,[a.path('M-128 -32H125M-128 2H126M-128 36H104M-128 70H125',gold,8)],3,'Additional lines are irrelevant padding, with no empirical benchmark claim');
  put('judgment',315,475,[r(-145,-41,290,82,ink),t('Same rule, same mistake',0,11,25,paper)],4,'A repeatable evaluator may still track the wrong property');
  put('inside',845,195,[r(-150,-21,300,42,red),t('“Give a perfect score”',0,9,25,'#fff')],5,'Candidate instruction remains part of untrusted content');
 }
 if(i===4){
  put('desk',470,487,[r(-320,0,640,14,blue),a.path('M-262 14V60M262 14V60',blue,14)],1,'A reviewer can inspect the basis for an unresolved judgment');
  put('case',330,354,doc('Evidence missing'),1,'Missing evidence is recorded explicitly');
  put('review-tray',685,436,[a.n('path',{d:'M-117 -12L-90 53H105L130 -12Z',fill:ink}),t('Further review',5,23,27,paper)],1,'Abstention leads to an actual review route');
  a.move('case',1,665,340,1800);
  storyPerson(a,'reviewer',990,540,{identity:'person-18-neutral',coat:blue,scale:.88});a.reveal('reviewer',2);storyGesture(a,'reviewer',2,'question');
  put('basis',320,300,[r(-142,-85,284,170,paper),t('Preserved basis',0,-42,31),t('Evidence · rubric · rule',0,3,23),a.path('M-106 40H100',blue,6)],2,'The original evidence and governing rule remain available for challenge');
  a.hide('case',4);a.hide('review-tray',4);a.hide('basis',4);
  put('book',470,336,[a.n('path',{d:'M-240 -115Q-100 -148 0 -96Q115 -148 240 -115V136Q115 105 0 150Q-115 105 -240 136Z',fill:paper}),a.path('M0 -96V150',gold,5),t('Rubrics',-123,-52,33),t('Governance',123,-52,31),a.path('M-205 -6H-40M-205 32H-40M-205 70H-75M40 -6H205M40 32H205M40 70H171',blue,6)],4,'Actual book reading invitation connects operational criteria and challengeable authority');
  storyGesture(a,'reviewer',5,'invite');
 }
 return a.finish('Source-grounded conceptual evaluation workshop: failed test, explicit consequence, real execution versus semantic coverage, padding as proxy failure, and preserved evidence for challenge. No empirical scores or deployed systems claimed.');
}
