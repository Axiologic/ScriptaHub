// AssistOS-specific illustrated work situations; shared verbs live in tools/shf.
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const ink='#345069',blue='#436d97',teal='#228878',coral='#d97552',gold='#d5a840';
export function revisedVisual(scene){
 const q=stageAuthor(),{n,path,text,object,tint}=q;
 const put=(id,x,y,nodes,meaning)=>q.add(object(id,x,y,nodes,meaning));
 const sheet=(id,x,y,heading,lines,w=260)=>put(id,x,y,[tint(n('rect',{x:-w/2,y:-125,width:w,height:250,rx:6,fill:'#e8eee9'}),'#e8eee9'),text(heading,0,-79,29,ink),...lines.flatMap((line,i)=>[text(line,0,-22+i*58,25,ink)])],'Illustrative working document: '+heading);
 const desk=(id,x,y,w=660)=>put(id,x,y,[path(`M${-w/2} 0H${w/2}M${-w/2+30} 0V125M${w/2-30} 0V125`,blue,14)],'A shared working desk supporting the documents.');
 const participant=(id,x,y)=>storyPerson(q,id,x,y,{seated:true,identity:'person-02-neutral',coat:teal,chair:'#8aaba3',scale:.85});
 if(scene.id==='sample'){
  participant('reviewer',210,565);desk('desk',640,440,700);
  sheet('supplier-a',470,295,'Supplier A',['Monthly fee','Delivery date']);sheet('supplier-b',820,295,'Supplier B',['Annual fee','Condition missing']);
  put('unit-a',470,278,[n('rect',{x:-119,y:-22,width:238,height:37,fill:'none',stroke:coral,'stroke-width':4})],'Highlighted monthly basis.');
  put('unit-b',820,278,[n('rect',{x:-119,y:-22,width:238,height:37,fill:'none',stroke:coral,'stroke-width':4})],'Highlighted annual basis: these units cannot be compared directly.');
  q.reveal('unit-a',4,180);q.reveal('unit-b',4,180);storyGesture(q,'reviewer',4,'question');q.actions.push({actor:'reviewer',action:'character.express',emotion:'worried',beat:4,durationMs:500});
 }else if(scene.id==='acceptance'){
  participant('reviewer',200,560);desk('desk',480,435,430);sheet('report',450,290,'Comparison',['Version under review','Sources checked']);
  put('accepted',450,380,[n('rect',{x:-110,y:-22,width:220,height:44,rx:7,fill:teal}),text('Accepted version',0,8,24,'#fff')],'Human accepts this report version only.');q.reveal('accepted',3,200);storyGesture(q,'reviewer',3,'explain');
  sheet('purchase',930,325,'Purchase',['Separate decision','Not authorised'],280);
  put('stop',930,451,[path('M-106 0H106',coral,9)],'Purchase authority remains separate from accepting a report.');q.reveal('purchase',4,300);q.reveal('stop',4,200);
 }else if(scene.id==='procedure'){
  sheet('evidence',260,325,'Research',['Sources retained','Facts rechecked']);
  put('method',720,305,[path('M-225 -65H225M-225 0H225M-225 65H225',blue,5),text('Extract terms',0,-85,30),text('Match fee periods',0,-19,30),text('Review comparison',0,46,30)],'A reusable procedure: a correction updates a step while preserving valid work.');
  put('repair',720,303,[n('rect',{x:-237,y:-49,width:474,height:45,rx:6,fill:'none',stroke:coral,'stroke-width':5})],'A unit-check correction becomes part of the method.');q.reveal('repair',3,200);
  q.label('retained','Keep valid work',260,510,30);q.reveal('retained',4,200);
  put('next',720,485,[path('M-180 0H180M160 -18L180 0L160 18',teal,8),text('Next assignment',0,50,31)],'The revised method is reused for a new assignment with new facts.');q.reveal('next',6,250);
 }else if(scene.id==='sovereignty'){
  put('workspace',565,330,[path('M-325 125V-150H325V125',blue,10),text('Project workspace',0,-185,36),path('M-355 125H355M-300 125V190M300 125V190',blue,12)],'The project workspace remains while a capability provider changes.');
  sheet('records',460,305,'Project history',['Accepted work','Permissions'],240);
  put('model-a',805,260,[n('rect',{x:-85,y:-45,width:170,height:90,rx:14,fill:coral}),text('Model A',0,10,29,'#fff')],'Replaceable model capability.');
  put('model-b',1030,420,[n('rect',{x:-85,y:-45,width:170,height:90,rx:14,fill:teal}),text('Model B',0,10,29,'#fff')],'Alternative provider: availability and portability require implementation.');
  q.move('model-a',3,1030,205,1800);q.move('model-b',3,805,330,1800);
 }else return null;
 return q.finish('Conceptual AssistOS workplace illustration, not a product screenshot. '+scene.title);
}
