import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
export function ventureArt(i){
 const q=stageAuthor(),{n,path,text,object,add,label,reveal,hide,move,person}=q;
 const ink='#25384c',blue='#386b99',rust='#b86546',mint='#77b3a1',paper='#fff0d6',gold='#d8a443';
 const o=(id,x,y,nodes,meaning,scale=1)=>add(object(id,x,y,nodes,meaning,scale));
 const sheet=(id,x,y,title,sub='',scale=1)=>o(id,x,y,[n('path',{d:'M-110 -70H88L110 -48V90H-110Z',fill:paper}),path('M-109 -70V89',rust,9),text(title,0,-33,25,ink),...(sub?[text(sub,0,0,21,blue)]:[]),path('M-70 32H70M-70 51H45',blue,4)],title,scale);
 const screen=(id,x,y,title,scale=1)=>o(id,x,y,[n('rect',{x:-155,y:-116,width:310,height:202,rx:9,fill:blue}),n('rect',{x:-140,y:-101,width:280,height:170,fill:'#dce9ed'}),text(title,0,-65,25,ink),path('M0 86V121M-70 124H70','$ink',9)],title,scale);
 const bench=(id,x,y,w=900)=>o(id,x,y,[path(`M${-w/2} 0H${w/2}`,rust,11),path(`M${-w/2+25} 7V54M${w/2-25} 7V54`,'$ink',7)],'Physical work surface');
 const report=(id,x,y,scale=1)=>sheet(id,x,y,'Review report','Useful result',scale);
 const test=(id,x,y,scale=1)=>o(id,x,y,[n('rect',{x:-92,y:-54,width:184,height:112,rx:7,fill:mint}),text('Case R',0,-18,27,ink),text('Known exception',0,16,20,ink),path('M-57 37H57',ink,3)],'The same illustrative reusable evaluation case, not customer data.',scale);
 const box=(id,x,y,title,sub,fill=ink)=>o(id,x,y,[n('rect',{x:-130,y:-65,width:260,height:130,rx:9,fill}),text(title,0,-16,26,paper),text(sub,0,21,21,paper)],title);
 switch(i){
 case 0:
  screen('independent',310,282,'Independent tool');report('report',310,302,.57);
  person('buyer',700,390,{coat:rust,night:'#e3a387',scale:.55,pose:'open'});
  screen('suite',1010,282,'Existing suite',.76);reveal('suite',3);
  report('same-report',1010,307,.42);reveal('same-report',3);
  move('report',2,544,294);label('choice','Which supplier remains?',652,535,30);reveal('choice',4);
  break;
 case 1:
  screen('first',250,266,'Deployment 1',.85);screen('second',962,266,'Deployment 2',.85);
  report('r1',250,283,.5);report('r2',962,283,.5);
  
  sheet('private',254,473,'Customer records','Stay with customer',.9);reveal('private',3);
  test('case',575,403,.65);reveal('case',4);move('case',5,962,267,2200);hide('r2',5);
  sheet('check-result',950,450,'Replay result','Missing decision',.86);reveal('check-result',5);q.actions.at(-1).offsetMs=2650;
  label('reuse','A reusable check exposes a gap',625,558,26);reveal('reuse',5);q.actions.at(-1).offsetMs=2850;
  break;
 case 2:
  screen('workspace',530,291,'Persistent project',1.18);report('report',468,303,.52);
  sheet('approval',784,279,'Reviewer decision','Retained history',.82);reveal('approval',2);
  box('modelA',259,511,'Model A','Replaceable');reveal('modelA',1);hide('modelA',3);
  box('modelB',259,511,'Model B','Replaceable',blue);reveal('modelB',3);
  person('reviewer',1040,395,{coat:mint,night:'#a0cec0',scale:.55,pose:'open'});reveal('reviewer',2);
  label('baseline','A shared assurance promise',774,526,28);reveal('baseline',4);
  break;
 case 3:
  bench('meeting',565,422,580);
  person('member1',190,393,{coat:blue,night:'#8cb6d9',scale:.57,pose:'open'});
  person('member2',925,393,{coat:rust,night:'#e3a387',scale:.57,pose:'open'});
  sheet('method',545,284,'Shared method','By member A',1);reveal('method',2);
  sheet('rights',278,522,'Member rights','Voluntary · local',.76);reveal('rights',3);
  sheet('copy',545,284,'Method record','By member A',.72);reveal('copy',4);move('copy',4,955,270,2200);
  move('member2',4,1080,393,2200);
  label('limits','Shared identity has limits',674,550,27);reveal('limits',5);
  break;
 case 4:
  bench('research-bench',600,425,800);screen('evaluator',295,322,'Test evaluator',.83);
  test('shared-case',560,318,.65);
  box('business',294,154,'Business systems','Assurance',blue);box('social',912,154,'Social systems','Participation',rust);reveal('social',2);
  sheet('private',895,359,'Restricted data','Stays in its domain',.83);reveal('private',4);
  move('shared-case',3,295,335);label('fit','Reuse depends on fit and rights',612,553,29);reveal('fit',5);
  break;
 case 5:
  sheet('criterion',228,274,'Declared test','Preserve decision D1',.92);
  screen('trial',608,298,'Candidate trial',.9);
  sheet('decision',608,301,'Decision D1','Before replacement',.55);
  hide('decision',2);
  o('missing',608,315,[text('D1 missing',0,0,28,rust)],'Observed illustrative failure after a component replacement.');reveal('missing',2);q.actions.at(-1).offsetMs=1500;
  box('next',1012,298,'Next commitment','Held',rust);reveal('next',2);q.actions.at(-1).offsetMs=2400;
  sheet('record',378,500,'Failed trial','Evidence retained',.76);reveal('record',3);
  sheet('thesis',765,495,'Thesis revision','Previous version kept',.76);reveal('thesis',4);
  break;
 case 6:
  bench('reading',600,491,780);
  o('book',625,323,[n('path',{d:'M-219 -106Q-106 -139 0 -91Q115 -139 219 -106V125Q100 92 0 141Q-101 92 -219 125Z',fill:paper}),path('M0 -91V135',rust,4),text('The venture',-108,-57,28,ink),text('The institution',109,-57,28,ink),text('What remains?',-108,-7,24,blue),text('Who decides?',109,-7,24,blue),text('What can fail?',-108,39,24,blue),text('What can change?',109,39,23,blue)],'The invitation returns to this book’s underwriting and institutional questions.');
  report('opening-report',209,293,.55);reveal('opening-report',2);
  break;
 default:throw Error('Unknown venture scene '+i);
 }
 return q.finish('Source-grounded venture situations. The review tool, evaluation Case R and failed trial are schematic illustrations, not reported customers, measured outcomes or investment advice.');
}
