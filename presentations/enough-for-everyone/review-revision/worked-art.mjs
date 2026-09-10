import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
export function workedVisual(i){
 const a=stageAuthor(),blue='#36798a',brick='#ad664e',cream='#f0e4d4',gold='#deb865';
 const put=(id,x,y,n,b=1,m=id)=>{a.add(a.object(id,x,y,n,m));a.reveal(id,b,900);};
 const txt=(v,x,y,size=28)=>a.text(v,x,y,size,'#2b4050');
 if(i===1){
  put('sun',175,180,[a.dot(0,0,50,gold)],1,'Physical solar flow');
  put('home',965,335,[a.n('path',{d:'M-183 -135L0 -222L183 -135Z',fill:brick}),a.n('rect',{x:-168,y:-125,width:336,height:295,fill:cream}),a.path('M-168 170H168',brick,14),a.path('M-132 95H-30M-105 95V165M-54 95V165',blue,12),a.path('M-77 95V-27',blue,7),a.n('path',{d:'M-122 -25H-32L-53 -77H-100Z',fill:gold})],1,'A real lamp and resident in the home are the service endpoint');
  storyPerson(a,'resident',1060,504,{identity:'person-04-neutral',coat:blue,scale:.63});a.reveal('resident',1);
  put('collector',300,320,[a.n('path',{d:'M-120 -65H85L130 60H-75Z',fill:blue}),a.path('M-70 -20H93M-49 25H112M-49 -65L-7 60M15 -65L57 60',cream,4),a.path('M10 62V133M-52 133H75',brick,12)],2,'Installed collector distinct from sunlight');
  put('distribution',575,405,[a.path('M-145 0H145',blue,12)],2,'Constructed distribution route to the service boundary');
  put('meter',650,310,[a.n('rect',{x:-80,y:-85,width:160,height:175,rx:9,fill:blue}),a.n('rect',{x:-58,y:-61,width:116,height:68,rx:6,fill:cream}),txt('Supply',0,-18,28),a.dot(0,48,16,gold)],2,'Working supply meter does not establish universal access');
  put('terms',775,505,[a.n('rect',{x:-112,y:-43,width:224,height:86,rx:4,fill:cream}),txt('Access terms',0,-3,27),txt('Who can afford it?',0,29,23)],3,'Affordability remains an institutional question, no fabricated bill amount');
  storyGesture(a,'resident',3,'question');
  put('flow',444,405,[a.dot(0,0,12,gold)],4,'Potential has become deliverable supply');a.move('flow',4,645,405,1800);
 }
 if(i===4){
  put('room',600,520,[a.n('path',{d:'M-470 30L-385 -36H370L470 30Z',fill:cream})],1,'One ordinary domestic cleaning task, not a robot performance claim');
  put('chair',880,425,[a.n('rect',{x:-57,y:-76,width:114,height:104,rx:10,fill:brick}),a.path('M-65 33H65M-52 35V108M52 35V108',brick,12)],1,'Ordinary household obstacle');
  put('spill',600,495,[a.n('ellipse',{cx:0,cy:0,rx:69,ry:20,fill:brick})],1,'A defined job to complete');
  put('robot',430,370,[a.n('rect',{x:-52,y:-99,width:104,height:83,rx:23,fill:blue}),a.dot(-20,-61,8,cream),a.dot(20,-61,8,cream),a.n('rect',{x:-51,y:-5,width:102,height:89,rx:20,fill:brick}),a.path('M-28 86V146M28 86V146M-53 17L-83 60M52 17L113 49',blue,20)],1,'Illustrative service robot, no product model or autonomy promise');
  put('mop',552,430,[a.path('M0 -12L45 78',blue,8),a.n('ellipse',{cx:48,cy:79,rx:57,ry:13,fill:blue})],1,'Cleaning tool follows the actual task');
  a.move('robot',2,480,370,1800);a.move('mop',2,602,430,1800);a.hide('spill',2);
  storyPerson(a,'supervisor',200,543,{identity:'person-14-neutral',coat:blue,scale:.81});a.reveal('supervisor',2);storyGesture(a,'supervisor',3,'reflect');
  put('service-kit',660,465,[a.n('rect',{x:-66,y:-15,width:132,height:72,rx:7,fill:brick}),a.path('M-28 -16V-37H28V-16',brick,9),a.path('M-23 12L24 37M-32 8L-22 0M26 36L39 28',cream,7)],3,'Maintenance and servicing are part of useful work');
  put('job',600,190,[a.text('Useful work + support',0,0,36,'$ink')],3,'Work and its support burden must be compared together');
  storyGesture(a,'supervisor',5,'explain');
 }
 return a.finish('Worked service illustrations distinguish solar flow, constructed supply and access; a completed household job retains supervision and maintenance costs. These are conceptual examples, not measured installations or products.');
}
