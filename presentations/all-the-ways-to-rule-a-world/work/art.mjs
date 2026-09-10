import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url), scenes=JSON.parse(fs.readFileSync(file));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q;
 const ink='#35445c',blue='#547cb6',ochre='#dfa442',coral='#c97058',green='#558f7d',paper='#f6e9ce';
 const shape=(d,fill)=>n('path',{d,fill});
 const person=(id,x,y,identity,coat,seated=false,scale=.88)=>storyPerson(q,id,x,y,{identity,coat,seated,scale,ink,chair:green});
 const gesture=(id,beat,g)=>storyGesture(q,id,beat,g);
 function table(id,x,y,width=350){add(object(id,x,y,[shape(`M-${width} 0L-${width-30} -35H${width-30}L${width} 0V18H-${width}Z`,ochre),path(`M-${width-35} 18V110M${width-35} 18V110`,ink,14)],'A real shared hearing table supports the documents and separates public roles.'));}
 const sheet=(id,x,y,word,color=paper)=>add(object(id,x,y,[shape('M-76 -42H76V42H-76Z',color),text(word,0,9,25,ink)],'Illustrative request or decision document: '+word));
 function bridge(id,x,y,scale=1){add(object(id,x,y,[path('M-180 20Q-90 42 0 20T180 20','#83bfc5',27),path('M-165 -22H-42M42 -22H165',ink,14),path('M-143 -20V55M143 -20V55',ink,12),path('M-75 -25L-49 12M75 -25L49 12',coral,10),shape('M-160 -38V-70H-146V-38Z',ochre),shape('M146 -38V-70H160V-38Z',ochre)],'Conceptual bridge repair makes the decision concrete; this is authored staging, not a named case in the book.',scale));}
 switch(i){
 case 0:
  person('resident',335,370,'person-04-neutral',coral,true);person('chair',600,325,'person-09-neutral',blue,true);person('reviewer',865,370,'person-02-neutral',green,true);
  table('hearing',600,327,350);sheet('request',400,335,'Repair request');move('request',2,610,335,2300);gesture('resident',2,'explain');gesture('chair',3,'reflect');gesture('reviewer',4,'question');
  bridge('case',600,505,.85);reveal('case',2);label('case-caption','Illustrative hearing: bridge repair',600,585,28);reveal('case-caption',2);
  break;
 case 1:
  person('applicant',290,485,'person-04-neutral',coral,false,.95);person('administrator',815,380,'person-09-neutral',blue,true,.92);table('counter',805,330,185);
  sheet('request',395,340,'Repair request');move('request',2,600,340,2400);
  add(object('barrier',610,335,[path('M0 -145V122',coral,15),dot(0,-145,16,coral)],'An administrative obstruction remains despite a change in elected leadership.'));
  sheet('election',1020,140,'New leadership',ochre);reveal('election',1);gesture('applicant',2,'question');gesture('administrator',3,'reflect');
  add(object('appeal-path',610,340,[path('M-140 0V-125Q-140 -165 -100 -165H85Q120 -165 120 -130V-12',green,9),shape('M108 -24L120 0L132 -24Z',green)],'An independent appeal provides a route around the blocked administrative decision.'));reveal('appeal-path',4);hide('barrier',4);move('request',5,800,340,1800);gesture('administrator',5,'resolve');
  label('appeal-label','Independent appeal',550,115,30);reveal('appeal-label',4);bridge('repair',970,500,.48);reveal('repair',5);break;
 case 2:
  add(object('terrain',600,360,[shape('M-460 -120Q-320 -230 -100 -150Q100 -210 460 -70L410 130Q100 190 -210 135Z','#bdd4ae'),path('M-360 -125Q-80 -70 -40 0T320 135','#76b5c7',45)],'One watershed crosses several communities, making separate responsibilities physically visible.'));
  for(const [j,x,y,c]of [[0,310,280,coral],[1,565,340,blue],[2,865,430,ochre]]){add(object('town'+j,x,y,[shape('M-50 0V-67L0 -102L50 -67V0Z',c),shape('M-16 0V-42H16V0Z',paper),n('rect',{x:-33,y:-60,width:14,height:17,fill:paper}),n('rect',{x:20,y:-60,width:14,height:17,fill:paper})],'A community along the same river.'));}
  add(object('water-event',260,265,[dot(0,0,22,coral),dot(27,-7,12,ochre)],'A consequence moves downstream beyond the originating jurisdiction.'));move('water-event',2,830,470,4200);
  person('local-voice',180,485,'person-02-neutral',green,false,.58);person('future-voice',1040,470,'person-04-neutral',coral,false,.55);gesture('local-voice',3,'question');gesture('future-voice',4,'invite');
  label('watershed','Shared river, different authorities',600,535,30);break;
 case 3:
  person('reader',270,485,'person-02-neutral',green,false,1);gesture('reader',2,'explain');
  add(object('draft-table',760,420,[shape('M-270 -180H250L300 65H-250Z',ochre),path('M-225 65V150M265 65V150',ink,15),shape('M-235 -160H220L265 35H-215Z',paper)],'A reader uses the governance canvas as a working design document.'));
  add(object('canvas',760,345,[text('Bridge repair',0,-78,34,ink),path('M-155 -8H150',blue,5),dot(-150,-8,20,coral),dot(0,-8,20,green),dot(150,-8,20,blue),text('Request',-155,38,23,ink),text('Authority',0,38,23,ink),text('Appeal',150,38,23,ink),path('M150 55Q150 102 0 102Q-145 102 -150 55',green,5)],'A worked illustrative canvas asks who can authorize action and who can correct mistakes.'));reveal('canvas',2);
  sheet('annotation',755,495,'Who can revise it?');reveal('annotation',3);gesture('reader',4,'question');gesture('reader',5,'invite');break;
 }
 s.visual=q.finish('A colorful public hearing and drafting studio enacts political correction. Bridge repair is an authored illustrative decision, not a claimed historical example from the book.');
}fs.writeFileSync(file,JSON.stringify(scenes,null,2));
