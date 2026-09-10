// Shared stage authoring for book presentations; content comes from scene data.
import {closedBookVisual} from '../../.agents/skills/shf-presentation-creator/scripts/lib/book-art.mjs';
let serial=0;
const node=(type,attrs={},text)=>({id:'$asset.n'+(++serial),type,attrs,...(text===undefined?{}:{text})});
const rect=(x,y,w,h,fill='$surface',rx=9)=>node('rect',{x,y,width:w,height:h,rx,fill,stroke:'$edge','stroke-width':2});
const line=(x1,y1,x2,y2,stroke='$pageLine',width=5)=>node('line',{x1,y1,x2,y2,stroke,'stroke-width':width,'stroke-linecap':'round'});
const txt=(x,y,text,size=31,fill='$ink',anchor='middle')=>node('text',{x,y,'font-size':size,fill,'text-anchor':anchor,'font-weight':600,'letter-spacing':-.3},text);
const circle=(cx,cy,r,fill)=>node('circle',{cx,cy,r,fill});
const curve=(d,fill='none',stroke='$teal',width=5)=>node('path',{d,fill,stroke,'stroke-width':width,'stroke-linejoin':'round','stroke-linecap':'round'});
const custom=(id,x,y,children,meaning,scale=1)=>({id,asset:'custom',x,y,scale,meaning,visual:{id:'$asset',type:'g',attrs:{},anchors:{left:[-106,-80],right:[106,-80],top:[0,-178],bottom:[0,18],center:[0,-80]},children}});
function label(text){return txt(0,49,text,32);}
function prop(id,kind,labelText,x,y,color='$teal',scale=1){
 if(kind==='book')return {...custom(id,x,y,[],`Book: ${labelText}`,scale),visual:closedBookVisual('$asset',{color,title:labelText})};
 const art=[];
 if(kind==='document'||kind==='report'){
  art.push(rect(-70,-186,140,194,'$page',4),curve('M34 -185 L70 -149 L34 -149 Z',color,'$edge',2));
  art.push(rect(-51,-164,57,11,color,2));
  for(let i=0;i<4;i++)art.push(line(-48,-125+i*26,i===3?12:48,-125+i*26,'$pageLine',5));
  if(kind==='report')art.push(rect(-49,-71,96,48,'$glass',3),line(-16,-71,-16,-23,'$reflect',2),line(15,-71,15,-23,'$reflect',2),line(-49,-47,47,-47,'$reflect',2));
 } else if(kind==='folder'){
  art.push(curve('M-96 -117 L-96 -151 L-29 -151 L-10 -131 L93 -131 L104 -5 L-96 -5 Z',color,'$edge',2),rect(-105,-110,210,113,'$surface',9),rect(-72,-81,110,10,color,2),line(-72,-47,70,-47),line(-72,-25,33,-25));
 } else if(kind==='chip'){
  for(let i=-2;i<=2;i++)art.push(line(i*24,-163,i*24,-187,color,7),line(i*24,-26,i*24,0,color,7),line(-88,-95+i*23,-111,-95+i*23,color,7),line(88,-95+i*23,111,-95+i*23,color,7));
  art.push(rect(-84,-168,168,144,'$surface',15),rect(-61,-145,122,98,color,9),txt(0,-82,'AI',40,'$white'));
 } else if(kind==='package'){
  art.push(curve('M-94 -137 L0 -180 L94 -137 L94 -18 L0 23 L-94 -18 Z',color,'$edge',3),curve('M-94 -137 L0 -91 L94 -137 M0 -91 L0 23','none','$white',3),curve('M-42 -160 L47 -113 L47 -56','none','$gold',16));
 } else if(kind==='browser'){
  art.push(rect(-119,-169,238,165,'$surface',12),rect(-119,-169,238,33,'$screenRim',10));
  for(let i=0;i<3;i++)art.push(circle(-98+i*16,-152,4,['$coral','$gold','$teal'][i]));
  art.push(rect(-98,-113,69,85,color,5),line(-11,-108,94,-108),line(-11,-79,70,-79),rect(-9,-42,92,19,'$glass',4));
 } else if(kind==='server'){
  for(let i=0;i<3;i++)art.push(rect(-90,-177+i*61,180,51,'$surface',7),circle(-63,-151+i*61,6,color),line(-35,-151+i*61,60,-151+i*61,'$pageLine',5));
 } else if(kind==='cloud'){
  art.push(curve('M-72 -22 C-146 -22 -141 -113 -79 -116 C-61 -207 52 -198 72 -122 C145 -131 156 -22 90 -22 Z','$surface',color,5));
  art.push(line(-40,-62,40,-62,color,5),circle(0,-110,15,color));
 } else if(kind==='check'){
  art.push(circle(0,-93,76,'$surface'),curve('M-38 -92 L-9 -63 L46 -125','none',color,14));
 } else if(kind==='lock'){
  art.push(curve('M-42 -110 L-42 -154 C-42 -212 42 -212 42 -154 L42 -110','none',color,14),rect(-71,-112,142,105,'$surface',15),circle(0,-70,13,color),line(0,-63,0,-38,color,9));
 } else if(kind==='clock'){
  art.push(circle(0,-90,78,'$surface'),circle(0,-90,66,'$backdrop'),line(0,-90,0,-140,color,7),line(0,-90,39,-66,color,7));
 } else if(kind==='question'){
  art.push(circle(0,-89,76,'$surface'),txt(0,-57,'?',92,color));
 }
 if(kind!=='book')art.push(label(labelText));return custom(id,x,y,art,`${kind}: ${labelText}`,scale);
}
const actor=(x=155,y=466)=>({id:'consultant',asset:'person-02-curious',x,y,scale:1.04,options:{color:'$blue',dynamicExpressions:true},meaning:'The same fictional consultant, representing the human reviewer.'});
const robot=(x,y,id='robot')=>({id,asset:'machine',x,y,scale:.66,meaning:'A schematic persistent software worker, not a physical robot.'});
const subtitle=(id,text,x,y,size=30)=>custom(id,x,y,[txt(0,0,text,size)],'Explanatory label');
export function stage(s,index,scenes){
 serial=0;
 const objects=[],actions=[],connections=[];
 const beatCue=(beat,offsetMs=0)=>({beatId:s.id+'-line-'+beat,edge:'start',offsetMs});
 // Four visual phases can span any number of short spoken sentences.
 const phaseBeat=phase=>s.visualPhases?.[phase-1]??(1+Math.round((phase-1)*(s.lines.length-1)/3));
 const cue=(phase,offsetMs=0)=>beatCue(phaseBeat(phase),offsetMs);
 const reveal=(id,beat)=>actions.push({actor:id,action:'appear',cue:cue(beat,200),durationMs:850});
 const move=(id,beat,x,y)=>actions.push({actor:id,action:'moveTo',x,y,cue:cue(beat,600),durationMs:1700});
 const connect=(a,b,beat,meaning,color='$teal')=>{const id='link-'+connections.length;connections.push({id,from:{node:a,anchor:'right'},to:{node:b,anchor:'left'},color,width:4,meaning});actions.push({actor:id,action:'connection.draw',cue:cue(beat,650),durationMs:1600});};
 // Repeated cast and material roles, varied causal compositions.
 const generic=(kinds)=>{objects.push(actor());kinds.forEach((kind,i)=>objects.push(prop('p'+i,kind,s.labels[i],[410,700,990][i],420,['$blue','$gold','$teal'][i],.85)));reveal('p1',2);reveal('p2',3);};
 switch(s.layout){
  case 'book-cover':
   objects.push(actor(250),prop('source-book','book',s.bookTitle,700,445,'$teal',1.45));break;
  case 'contrast':
   objects.push(prop('left-idea',s.propKinds?.[0]||'document',s.labels[1],330,425,'$blue',1.15),prop('right-idea',s.propKinds?.[1]||'folder',s.labels[2],870,425,'$teal',1.15));
   reveal('right-idea',2);break;
  case 'reading-route':
   objects.push(prop('source-book','book',s.bookTitle,250,440,'$teal',1.25),subtitle('near',s.labels[1],770,250,38),subtitle('deep',s.labels[2],770,410,38));
   reveal('deep',3);break;
  case 'workspace-focus':
   objects.push(prop('shared-space','browser',s.labels[1],600,380,'$blue',1.45));break;
  case 'question-focus':
   objects.push(prop('question','question','',600,360,'$gold',1.1),subtitle('question-one',s.labels[1],310,483,32),subtitle('question-two',s.labels[2],880,483,32));
   reveal('question-two',3);break;
  case 'book-focus':
   objects.push(actor(),prop('source-book','book',s.bookTitle,435,435,'$teal',1.05),prop('p1',s.propKinds?.[0]||'question',s.labels[1],740,423,'$gold',.78),prop('p2',s.propKinds?.[1]||'folder',s.labels[2],1020,423,'$blue',.78));
   reveal('p1',1);reveal('p2',2);break;
  case 'review':
   objects.push(actor(),prop('p0','document',s.labels[0],425,423,'$blue',.9),robot(690,433),prop('p1','report',s.labels[1],880,423,'$gold',.9),prop('decision','question',s.labels[2],1050,408,'$coral',.7));
   reveal('p1',1);reveal('decision',2);connect('p0','robot',1,'The Robot reads the proposals.');connect('robot','p1',2,'The task produces a report, not purchase authority.');break;
  case 'identity': case 'continuity':
   objects.push(actor(),prop('project','folder',s.labels[0],460,428,'$teal',.9),robot(747,440),prop('engineA','chip',s.labels[1],1040,370,'$blue',.7),prop('engineB','chip',s.labels[2],1040,370,'$gold',.7));
   reveal('engineA',1);actions.push({actor:'engineA',action:'disappear',cue:cue(3),durationMs:600});reveal('engineB',3);connect('project','robot',2,'The persistent project and worker retain their relationship.');connect('robot','engineB',3,'A replacement engine works within the existing role.');break;
  case 'package':
   objects.push(actor(),robot(420,423),subtitle('robot-label',s.labels[0],420,468,32),prop('p1','package',s.labels[1],710,423,'$gold',.85),prop('p2','chip',s.labels[2],1010,418,'$teal',.8));
   reveal('p1',1);reveal('p2',2);connect('robot','p1',1,'The persistent worker uses a deployable capability package.');connect('p1','p2',2,'The package provides agent software, tools or supporting services.');break;
  case 'workspace':generic(['folder','browser','browser']);connect('p0','p1',2,'Chat dispatch refers to project artifacts.');connect('p1','p2',3,'A conversation and a meeting share the approved project.');break;
  case 'team':
   objects.push(actor());[425,704,980].forEach((x,i)=>{objects.push(robot(x,406,'robot'+i),subtitle('role'+i,s.labels[i],x,460,34));if(i)reveal('robot'+i,i+1);});
   break;
  case 'browser':
   objects.push(actor(170),robot(460,422),prop('browser','browser','Shared session',780,429,'$blue',1.25),prop('control','lock','Human control',1080,363,'$gold',.55));
   reveal('control',2);actions.push({actor:'consultant',action:'walkTo',x:250,cue:cue(2),durationMs:1800});move('control',3,1000,405);break;
  case 'archive':case 'procedure':generic(['folder','document','check']);connect('p0','p1',2,'Sources and method are preserved in the project.');connect('p1','p2',3,'An artifact is associated with a review decision.');break;
  case 'versions':generic(['document','report','check']);connect('p0','p1',2,'A proposed revision derives from the original.','$gold');connect('p1','p2',3,'Acceptance applies to a specific reviewed version.');break;
  case 'checks':generic(['chip','report','check']);connect('p0','p1',2,'Model interpretation supplies explicit fields for ordinary computation.');connect('p1','p2',3,'Independent checks and human review inspect the result.');break;
  case 'repair':generic(['document','report','check']);connect('p0','p1',1,'The comparison depends on extracted inputs.');connect('p1','p2',1,'The final result depends on the comparison.');objects.push(prop('correction','question','Corrected input',410,220,'$coral',.45));reveal('correction',2);move('correction',3,700,220);break;
  case 'evaluation':generic(['folder','chip','check']);connect('p0','p1',2,'Representative examples test the candidate procedure.');connect('p1','p2',3,'Held-out evaluation judges outcomes, not fluent prose.');break;
  case 'ladder': {
   objects.push(actor());
   const count=s.labels.length,spacing=900/count,width=Math.min(226,spacing-32);
   s.labels.forEach((text,i)=>{const x=330+spacing*i+(count===3?90:35);objects.push(custom('step'+i,x,455,[rect(-width/2,-i*35-64,width,i*35+64,['$blue','$gold','$teal','$blue'][i%4],5),txt(0,-i*35-83,text,count>3?27:34)],'Task-specific authority: '+text));if(i)reveal('step'+i,Math.min(i+1,4));});break;
  }
  case 'boundary':generic(['folder','lock','server']);break;
  case 'recovery':generic(['question','document','folder']);connect('p0','p1',2,'A stop preserves externally meaningful evidence.','$coral');connect('p1','p2',3,'Evidence and versions support recovery where reversible.');break;
  case 'location':generic(['browser','server','cloud']);connect('p0','p1',2,'Execution can move to an approved private environment.');connect('p1','p2',3,'Remote service use must account for actual data movement.','$gold');break;
  case 'catalog':generic(['package','check','server']);connect('p0','p1',2,'A capability needs evaluation of its promised outcome.');connect('p1','p2',3,'Supported deployment includes maintenance and version management.');break;
  case 'pilot':generic(['clock','report','package']);break;
  case 'synthesis':generic(['folder','check','folder']);connect('p0','p1',1,'Delegated work produces an inspectable artifact.');connect('p1','p2',2,'Accepted work and its procedure remain available for reuse.');break;
  case 'comparison':generic(['document','document','question']);break;
  default:generic(['folder','document','report']);connect('p0','p1',2,'The assignment specifies source inputs and criteria.');connect('p1','p2',3,'The specified task produces a reviewable result.');
 }
 // The same actor performs the script's emotional arc through explicit cue-bound actions.
 let human=objects.find(o=>o.id==='consultant');
 if(human&&s.mascot){const original=human;human={id:'consultant',asset:'custom',x:original.x,y:original.y,scale:.92,options:{rig:'character'},visual:globalThis.ScriptaMascot.visual(s.emotionalPlan.states[0]),meaning:'The ScriptaHub librarian mascot guides the visitor.'};objects[objects.indexOf(original)]=human;}else if(human)human.asset='person-02-'+s.emotionalPlan.states[0];
 const gestures={neutral:'release',happy:'invite',curious:'question',worried:'recoil',sad:'reflect',angry:'recoil',surprised:'question',determined:'explain',tired:'reflect',skeptical:'reflect',relieved:'release',inspired:'resolve'};
 if(human)for(let beat=1;beat<=s.lines.length;beat++){
  const state=s.emotionalPlan.states[beat-1];
  actions.push({actor:'consultant',action:'character.express',emotion:state,cue:beatCue(beat,200),durationMs:500,meaning:s.emotionalPlan.purpose});
  actions.push({actor:'consultant',action:'character.gesture',gesture:gestures[state],cue:beatCue(beat,650),durationMs:2300,meaning:'A motivated '+state+' response to the current sentence.'});
 }
 if(human&&s.layout!=='browser'&&index%3===0){
  actions.push({actor:'consultant',action:'walkTo',x:human.x+35,cue:cue(2,500),durationMs:1800});
  actions.push({actor:'consultant',action:'walkTo',x:human.x,cue:cue(4,500),durationMs:1800});
 }
 const beats=[];let time=250;for(const [i,text]of s.lines.entries()){const duration=Math.ceil(text.split(/\s+/).length/165*60000);beats.push({id:s.id+'-line-'+(i+1),startMs:time,endMs:time+duration+200,spokenEndMs:time+duration,text,speakerId:'narrator',lens:s.beatLenses?.[i]||s.lens,sourceRefs:s.sources.map(i=>'section_'+i),performance:{delivery:'Clear documentary theatre; '+s.emotionalPlan.purpose+'.',targetWpm:165,emotion:s.emotionalPlan.states[i],intensity:s.emotionalPlan.intensities[i]}});time+=duration+350;}
 return {id:s.id,title:s.title,chapter:s.chapter,intent:s.lines[0],knownBefore:index?scenes[index-1].title:'A chatbot can produce a plausible answer.',knownAfter:s.lines.at(-1),lens:s.lens,emotion:s.emotionalPlan.arc,emotionalPlan:s.emotionalPlan,openQuestion:s.title,payoff:s.lines.at(-1),durationMs:time+600,setting:'minimal',sourceVisual:s.sourceVisual,objects,connections,actions,beats,alt:s.title+'. '+s.labels.join(', ')+'. Conceptual illustration of the source workflow.'};
}

// Shorter speech must not let one sentence's gesture compete with the next.
export function fitBeatGestures(direction){
 for(const scene of direction.scenes){
  for(const action of scene.actions||[]){
   if(action.action!=='character.gesture'||!action.cue)continue;
   const i=scene.beats.findIndex(b=>b.id===action.cue.beatId);
   if(i<0)continue;
   const start=scene.beats[i].startMs+(action.cue.offsetMs||0);
   const limit=(scene.beats[i+1]?.startMs??scene.durationMs)-150;
   action.durationMs=Math.max(1,Math.min(action.durationMs,limit-start));
  }
 }
 return direction;
}
