// Site orientation compositions. Each scene shows the visitor's actual task.
import {closedBookVisual,openBookVisual} from '../../.agents/skills/shf-presentation-creator/scripts/lib/book-art.mjs';
let serial=0;
const n=(type,attrs={},text)=>({id:'$asset.n'+(++serial),type,attrs,...(text===undefined?{}:{text})});
const rect=(x,y,width,height,fill='$surface',rx=12)=>n('rect',{x,y,width,height,fill,rx});
const text=(x,y,t,size=27,color='$ink',anchor='start')=>n('text',{x,y,fill:color,'font-size':size,'font-weight':size>=30?700:600,'letter-spacing':-.35,'text-anchor':anchor},t);
const line=(x1,y1,x2,y2,color='$pageLine',width=2)=>n('line',{x1,y1,x2,y2,stroke:color,'stroke-width':width,'stroke-linecap':'round'});
const path=(d,stroke='$teal',fill='none',width=3)=>n('path',{d,stroke,fill,'stroke-width':width,'stroke-linecap':'round','stroke-linejoin':'round'});
const circle=(cx,cy,r,fill)=>n('circle',{cx,cy,r,fill});
const obj=(id,x,y,children,meaning)=>({id,asset:'custom',x,y,meaning,visual:{id:'$asset',type:'g',attrs:{},children}});
const book=(id,x,y,color,scale=.7)=>({id,asset:'custom',x,y,scale,visual:closedBookVisual('$asset',{color}),meaning:'A book in the collection, not the library itself.'});
export function libraryStage(s,index,scenes){
 serial=0;const objects=[],actions=[];
 const cue=(beat,offsetMs=0)=>({beatId:s.id+'-line-'+beat,edge:'start',offsetMs});
 const reveal=(id,beat)=>actions.push({actor:id,action:'appear',cue:cue(beat,250),durationMs:750});
 const mascot=(x,y,scale=.8)=>objects.push({id:'consultant',asset:'custom',x,y,scale,options:{rig:'character'},visual:globalThis.ScriptaMascot.visual(s.emotionalPlan.states[0]),meaning:'The ScriptaHub librarian guides the visitor.'});
 const shelf=(id,x,y)=>{const ns=[rect(-260,16,520,8,'$wood',2)];for(let i=0;i<12;i++){const bx=-246+i*41,h=98+(i*17)%53;ns.push(rect(bx,16-h,30,h,['$teal','$blue','$gold','$coral'][i%4],3),line(bx+8,30-h,bx+22,30-h,'$page',2),line(bx+8,4,bx+22,4,'$page',1));}objects.push(obj(id,x,y,ns,'Several different books on a library shelf.'));};
 switch(s.layout){
 case 'library':
  shelf('collection',400,383);mascot(940,456,.94);
  objects.push(obj('library-name',145,177,[text(0,0,'ScriptaHub.com',42,'$teal'),text(0,48,'Deep subjects · Small audiences',25)],'The virtual library identity, separate from its books.'));reveal('collection',1);break;
 case 'collaboration':
  objects.push(obj('expert-notes',90,140,[rect(0,0,430,310,'$page'),text(30,48,'Expert direction',30,'$structural'),text(30,112,'Questions',27,'$structural'),text(30,164,'Structure',27,'$structural'),text(30,216,'Corrections',27,'$structural'),line(30,260,345,260)],'Human editorial thinking directs the work.'));
  objects.push(obj('process',555,277,[path('M0 0 H90 M76 -13 L90 0 L76 13')],'Expert direction informs AI-assisted editions.'));
  objects.push(book('edition',850,444,'#23564f',1.15),obj('edition-label',850,155,[text(0,0,'AI-assisted editions',30,'$teal','middle')],'Books and revised editions carry the collaboration forward.'));
  reveal('edition',2);reveal('edition-label',2);break;
 case 'reuse':
  objects.push(book('shared-book',280,435,'#23564f',1.3),obj('shared-label',280,157,[text(0,0,'Developed once',31,'$teal','middle')],'A developed account of a subject.'));
  objects.push(obj('readers',710,176,[text(115,-20,'Many readers',31,'$teal','middle'),...Array.from({length:12},(_,i)=>{const x=(i%4)*77,y=Math.floor(i/4)*96;return [circle(x,y+30,16,['$teal','$blue','$gold'][i%3]),path(`M${x-24} ${y+77} Q${x-24} ${y+48} ${x} ${y+48} Q${x+24} ${y+48} ${x+24} ${y+77} Z`,'none',['$teal','$blue','$gold'][i%3],0)];}).flat()],'Reader pictograms represent reuse by many people, not a numeric savings claim.'));
  objects.push(obj('reuse-path',445,300,[path('M0 0 H180 M162 -14 L180 0 L162 14')],'Readers reuse the work invested in the book.'));reveal('readers',2);reveal('reuse-path',2);break;
 case 'literature':
  for(const [i,t] of ['Science fiction','Stories','Essays','Other voices'].entries()){
   const x=205+i*263;objects.push(book('volume-'+i,x,428,['#23564f','#435570','#815643','#4c6554'][i],1.05),obj('genre-'+i,x,482,[text(0,0,t,26,'$ink','middle')],'An example of literary diversity, not an actual book title.'));
   if(i>0){reveal('volume-'+i,Math.min(i+1,s.lines.length));reveal('genre-'+i,Math.min(i+1,s.lines.length));}
  }break;
 case 'search':
  mascot(215,461,.84);
  objects.push(obj('query',430,135,[text(0,-25,'Ask AI Librarian',31,'$teal'),rect(0,0,680,88),path('M25 33 A11 11 0 1 1 41 48 L50 57'),text(72,50,'What would you like to explore?',27)],'A visitor writes a recommendation request.'));
  objects.push(obj('matches',430,255,[rect(0,0,680,219),text(25,39,'Books from the collection',24,'$teal'),...['Your subject','Your interests','Your next book'].flatMap((t,i)=>[rect(26,65+i*48,22,32,['$blue','$gold','$teal'][i],2),text(69,88+i*48,t,24)])],'Catalogue recommendations reflect the reader request.'));reveal('matches',3);break;
 case 'contribution':
  mascot(230,463,.87);
  objects.push(obj('edit-action',460,143,[rect(0,0,620,130),text(27,48,'Suggest an Edit',32,'$teal'),text(27,94,'Improve an existing book',25)],'Corrections and expert guidance for an existing book.'));
  objects.push(obj('create-action',460,310,[rect(0,0,620,130),text(27,48,'Create',32,'$teal'),text(27,94,'Propose a book or contribute a document',25)],'Contribution intent is independent of its delivery channel.'));reveal('create-action',2);break;
 case 'reading':
  objects.push(obj('short-read',80,116,[rect(0,0,450,365),text(35,49,'10-minute edition',31,'$teal'),rect(35,83,380,223,'$page'),...Array.from({length:6},(_,i)=>line(63,113+i*28,i===5?290:385,113+i*28)),text(35,339,'A first look',22)],'A short reading edition.'));
  objects.push({id:'full-read',asset:'custom',x:850,y:300,scale:1.35,visual:openBookVisual('$asset'),meaning:'The complete book, shown as an open volume.'});
  objects.push(obj('full-label',850,147,[text(0,0,'Complete book',31,'$teal','middle'),text(0,328,'The full argument',22,'$ink','middle')],'Reading depth labels.'));
  reveal('short-read',2);reveal('full-read',3);reveal('full-label',3);break;
 case 'languages':
  mascot(230,465,.83);
  objects.push(obj('language-picker',450,130,[text(0,0,'Reading language',31,'$teal'),...['English','Română','Français','Deutsch','Español','Italiano','Português','Polski'].flatMap((t,i)=>[rect((i%2)*260,32+Math.floor(i/2)*65,240,51),text(18+(i%2)*260,66+Math.floor(i/2)*65,t,25)])],'The eight supported reading-language choices.'));
  objects.push(obj('availability',450,478,[text(0,0,'Open an edition or request a translation',24)],'Availability determines whether reading or a request opens.'));reveal('availability',3);break;
 case 'revision':
  objects.push(obj('passage',85,120,[rect(0,0,570,345,'$page'),text(35,51,'A passage worth checking',29,'$structural'),...Array.from({length:5},(_,i)=>line(35,96+i*28,510-(i%2)*62,96+i*28)),rect(30,139,492,37,'$glass',3),text(35,298,'Suggest an Edit',29,'#1a6157')],'A selected passage and the book feedback action.'));
  objects.push(obj('history',750,151,[text(0,0,'Edition History',31,'$teal'),line(10,52,10,241,'$pageLine',3),circle(10,65,8,'$teal'),circle(10,208,8,'$blue'),text(36,74,'Current edition',26),text(36,218,'Earlier releases',26)],'History preserves previous editions; feedback does not automatically change a book.'));reveal('history',4);break;
 case 'submission':
  mascot(965,465,.86);
  objects.push(obj('email',85,110,[rect(0,0,640,372),text(32,52,'Create',33,'$teal'),text(32,106,'Propose a book or document',28),line(32,135,608,135),rect(32,164,355,72,'$page',6),path('M55 184 L55 215 L76 215 L76 191 L68 184 Z','$teal'),text(98,209,'Your document',25,'$structural'),text(32,286,'Review the prepared email',25),text(32,331,'Attach your file · Send it',25,'$teal')],'Create prepares an email that the visitor reviews and sends.'));reveal('email',1);break;
 case 'invitation':
  mascot(300,455,.95);shelf('collection',810,406);
  objects.push(obj('next-step',810,183,[text(0,0,'Ask AI Librarian',35,'$teal','middle'),text(0,52,'Explore the collection',26,'$ink','middle')],'Two ways to find a book.'));break;
 default:throw Error('Unknown library tour composition: '+s.layout);
 }
 const guide=objects.find(o=>o.id==='consultant');
 if(guide)for(const [i,state] of s.emotionalPlan.states.entries()){
  actions.push({actor:'consultant',action:'character.express',emotion:state,cue:cue(i+1,100),durationMs:450});
  actions.push({actor:'consultant',action:'character.gesture',gesture:state==='curious'?'question':state==='happy'?'invite':'explain',cue:cue(i+1,500),durationMs:2400});
 }
 let time=650;
 const beats=s.lines.map((t,i)=>{const duration=Math.ceil(t.split(/\s+/).length/145*60000),pause=s.pauseAfterMs[i];const b={id:s.id+'-line-'+(i+1),startMs:time,spokenEndMs:time+duration,endMs:time+duration+pause,text:t,speakerId:'narrator',sourceRefs:s.sources.map(n=>'section_'+n),performance:{targetWpm:145,pauseAfterMs:pause,emotion:s.emotionalPlan.states[i],delivery:'Calm, conversational guidance; allow time to inspect the interface.'}};time=b.endMs+200;return b;});
 return {id:s.id,title:s.title,chapter:s.chapter,intent:s.lines[0],knownBefore:index?scenes[index-1].lines.at(-1):'A visitor has arrived at ScriptaHub.',knownAfter:s.lines.at(-1),durationMs:time+1000,setting:'minimal',objects,actions,connections:[],beats,emotionalPlan:s.emotionalPlan,alt:s.metaphor};
}
