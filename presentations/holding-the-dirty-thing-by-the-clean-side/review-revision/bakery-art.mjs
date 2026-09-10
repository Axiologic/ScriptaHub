import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';

// Book-specific illustration: an explicitly imagined night bakery, never a source case.
export function bakeryArt(index){
 const a=stageAuthor(),{n,path,text}=a;
 const ink='#283b52',cream='#f1dfb8',bread='#d9a14d',brick='#b76954',blue='#709aa8',plum='#776580';
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const solid=(d,fill)=>n('path',{d,fill});
 const obj=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
 const moon=(x,y,r=16)=>[n('circle',{cx:x,cy:y,r,fill:cream}),n('circle',{cx:x+8,cy:y-6,r:r-2,fill:ink})];
 const loaf=(x,y)=>[n('ellipse',{cx:x,cy:y,rx:24,ry:11,fill:bread}),path(`M${x-10} ${y-7}l-4 9M${x+4} ${y-8}l-4 9`,cream,2)];
 const floor=()=>obj('floor',600,544,[path('M-492 0H492',brick,7)],'Bakery floor supporting people and wheeled equipment');
 const worker=(id,x,y,{coordinator=false,scale=1,reach=false}={})=>{
  const k=scale*.9;
  storyPerson(a,id,x,y+136*scale,{identity:coordinator?'person-10-neutral':'person-18-neutral',coat:coordinator?plum:blue,scale:k,ink});
  const actor=a.objects.find(o=>o.id===id),v=actor.visual;
  if(!coordinator){
   // Apron and cap are attached to the existing expressive body/head rig.
   const apron=solid('M-21 -163H20L29 -80H-28Z',cream);
   v.children.splice(v.children.findIndex(c=>c.id==='$asset.armR'),0,apron,path('M-20 -112H20',blue,3));
   v.children=v.children.filter(c=>!['$asset.n27','$asset.n28'].includes(c.id));
   v.children.find(c=>c.id==='$asset.head').children.push(rect(-31,-40,62,15,cream,5));
  }
  if(reach){
   const arm=v.children.find(c=>c.id==='$asset.armR');
   arm.children=[path('M32 -156L75 -146L111 -132',blue,20),n('circle',{cx:111,cy:-132,r:10,fill:'#DCAF90'})];
  }
  const expressions=index===2?[[1,'tired'],[2,'relieved'],[3,'skeptical'],[4,'worried'],[5,'curious']]:[[1,coordinator?'neutral':'tired'],[3,'curious'],[5,'thoughtful']];
  for(const [beat,emotion] of expressions)a.actions.push({actor:id,action:'character.express',beat,emotion:emotion==='thoughtful'?'neutral':emotion,durationMs:600});
  if(index===2){storyGesture(a,id,1,'reflect');storyGesture(a,id,2,'release');storyGesture(a,id,4,'question');}
  if(index===1)storyGesture(a,id,3,'question');
  return id;
 };
 const rack=(id,x,y,scale=1)=>obj(id,x,y,[
  a.tint(path('M-80 81V-103H80V81M-80 -15H80M-80 31H80M-80 77H80',ink,6),'#b8c9d8'),
  ...[-35,35].flatMap(px=>[-24,22,68].flatMap(py=>loaf(px,py))),
  a.tint(n('circle',{cx:-66,cy:90,r:11,fill:ink}),'#b8c9d8'),a.tint(n('circle',{cx:66,cy:90,r:11,fill:ink}),'#b8c9d8')
 ],'Supported bread rack; same load retained despite changes in language',scale);
 const oven=(id,x,y,scale=1)=>obj(id,x,y,[rect(-90,-145,180,205,brick,10),rect(-66,-105,132,83,ink,8),path('M-53 -37H53',cream,5),rect(-58,0,116,20,cream,5),a.tint(path('M-66 61V75M66 61V75',ink,10),'#b8c9d8')],'Bakery oven, a real reason for coordinated morning work',scale);
 const smallRota=(id,x,y,scale=1)=>obj(id,x,y,[rect(-104,-85,208,169,cream,6),text('Night rota',0,-51,27,ink),path('M-87 -23H87M-87 27H87M-25 -23V67',blue,3),text('Baker',-62,10,19,ink),rect(-7,-13,36,31,ink,4),...moon(7,2,10),rect(42,-13,36,31,ink,4),...moon(57,2,10)],'Revised schedule with the same two baker night assignments',scale);
 if(index===0){
  floor();obj('night-window',204,270,[rect(-70,-83,140,151,ink,9),...moon(20,-30,27),path('M0 -79V65M-66 -2H66',blue,5)],'Night outside the bakery');
  oven('oven',949,476.5,.9);worker('coordinator',335,408,{coordinator:true});worker('baker',471,408,{reach:true});rack('rack',651,443);
  // The baker's hand meets the rack's left rail; both translate together.
  a.move('baker',3,559,544,2900);a.move('rack',3,739,443,2900);
  obj('shop-hatch',961,223,[rect(-106,-39,212,72,cream,7),text('Morning shop',0,7,27,ink)],'Useful destination of the bread');
 }else if(index===1){
  obj('rota-board',569,330,[rect(-329,-133,658,279,cream,9),path('M-300 -61H300M-300 16H300M-300 95H300M-127 -61V95M30 -61V95M186 -61V95',blue,3),text('Baker',-219,-11,30,ink),text('Colleague',-219,66,26,ink)],'One rota with two people; total work conserved during reassignment');
  obj('rota-name',569,221,[text('Night rota',0,0,33,ink)],'Ordinary name of the schedule');
  obj('efficiency-name',569,221,[text('Efficiency',0,0,33,ink)],'A changed managerial label, not a reduction of work');a.reveal('efficiency-name',4);a.hide('rota-name',4);
  const shift=(id,x,y)=>obj(id,x,y,[rect(-29,-24,58,48,ink,5),...moon(0,0,16)],'An allocated night shift, represented identically before and after');
  shift('existing-shift',517,318);shift('transferred-shift',677,397);a.move('transferred-shift',3,677,318,2300);
  obj('revision-label',569,509,[text('Revised allocation',0,0,25,'$ink')],'Changed schedule version, not just renamed work');a.reveal('revision-label',3);
  worker('baker',1015,438,{scale:.7});rack('same-rack',164,470,.65);
 }else if(index===2){
  floor();smallRota('unchanged-rota',241,300,.95);worker('baker',493,408);worker('coordinator',683,408,{coordinator:true});
  // A modest approach communicates listening; no schedule action accompanies it.
  a.move('coordinator',2,643,544,2400);
  obj('scheduling-screen',878,316,[rect(-101,-83,202,165,ink,9),text('AI proposal',0,-50,25,cream),rect(-76,-29,152,75,cream,4),text('Same rota',0,0,26,ink),text('Score-based',0,27,20,ink),path('M0 82V128M-56 129H56',blue,9)],'Conditional use of a score to repeat the existing allocation');a.reveal('scheduling-screen',4);
  obj('lift-proposal',916,339,[rect(-139,-111,278,213,cream,7),text('Proposed lift',0,-74,27,ink),path('M-70 61V-30H35V8M-90 62H-49M-27 23H83M-17 43H73',blue,6),path('M-17 24V43M73 24V43',blue,4),n('ellipse',{cx:29,cy:17,rx:30,ry:10,fill:bread})],'Illustrated proposal to reduce lifting, never an implemented benefit');a.reveal('lift-proposal',5);a.hide('scheduling-screen',5);
 }else{
  obj('worktop',600,382,[rect(-496,-190,992,377,brick,14)],'Overhead view of a supported bakery worktop');
  smallRota('same-rota',288,359,.95);
  obj('review-slip',566,341,[rect(-92,-100,184,200,cream,5),text('Review request',0,-55,24,ink),text('Night allocation',0,-14,22,ink),path('M-67 25H67M-67 46H48',blue,3),text('Pending',0,82,23,ink)],'A submitted challenge without an automatically changed schedule');
  obj('objection',300,371,[n('circle',{cx:0,cy:0,r:17,fill:plum}),text('?',0,10,28,cream)],'Baker questions their allocation');a.move('objection',2,566,356,2500);
  obj('book',858,352,[solid('M-155 -114Q-77 -135 0 -98Q80 -132 155 -114V134Q78 116 0 151Q-80 116 -155 134Z',cream),path('M0 -98V151',bread,4),text('The Clean-',-79,-35,24,ink),text('Side Rule',-79,0,26,ink),path('M-128 38H-32M-128 55H-44M30 16H125M30 34H114',blue,3),rect(94,-111,19,47,plum)],'Book opened at its actual introduction; emotional chapter marked for later reading');
  obj('reader-arm',862,530,[solid('M-30 15L-20 -59L18 -71L35 -57L12 -39L7 15Z','#b88769'),rect(-33,-4,47,40,blue,6)],'Connected hand and sleeve at the book edge');a.reveal('reader-arm',4);
 }
 return a.finish('Original hypothetical night bakery: unchanged physical work, reassigned night duty, renamed rota, calmer conversation and unresolved review; draft pending source and rendered-action review.');
}
