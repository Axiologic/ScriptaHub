import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';import{storyPerson,storyGesture}from'../../../tools/shf/people-poses.mjs';const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,path,text,dot,object,add,reveal,hide,move,label}=q,ink='#4e6252',green='#73a57d',light='#b6ce96',blue='#71abc0',red='#d37b60',gold='#dbaa52';const shape=(d,fill)=>n('path',{d,fill});
 function tree(id,x,y,scale=1){add(object(id,x,y,[path('M0 0V-125M0 -65L-32 -100M0 -92L35 -120','#8d7252',12),n('ellipse',{cx:0,cy:-145,rx:70,ry:65,fill:green}),n('ellipse',{cx:-47,cy:-125,rx:38,ry:43,fill:light}),...[[0,-163],[35,-129],[-37,-111]].map(([x,y])=>dot(x,y,10,red))],'One cared-for apple tree has a concrete place in the opening’s illustrative orchard.',scale));}
 const person=(id,x,y,coat=red,scale=.75)=>storyPerson(q,id,x,y,{identity:'person-02-neutral',coat,scale});const act=(id,b,g)=>storyGesture(q,id,b,g);
 function house(id,x,y){add(object(id,x,y,[shape('M-100 60V-40L0 -110L100 -40V60Z',gold),shape('M-25 60V-15H25V60Z',ink),n('rect',{x:-69,y:-20,width:30,height:32,fill:'#efe2c3'})],'A downstream home bears a consequence outside the orchard owner’s immediate frame.'));}
 switch(i){
 case 0:
  add(object('archivist-desk',600,500,[shape('M-420 0H420V26H-420Z',ink),path('M-370 26V112M370 26V112',ink,12)],'The archivist works at a material desk where the official record can be changed'));person('archivist',255,580,blue,.82);act('archivist',1,'reflect');
  add(object('older-map',385,270,[n('rect',{x:-170,y:-92,width:340,height:184,fill:'#efe2c3',stroke:ink,'stroke-width':4,rx:5}),text('DESTROYED VILLAGE',0,-25,22,red),text('same location',0,15,21,ink),path('M-110 55H103',red,4)],'The older map names the destroyed village while preserving its location'));reveal('older-map',1);
  add(object('official-map',815,270,[n('rect',{x:-170,y:-92,width:340,height:184,fill:'#efe2c3',stroke:ink,'stroke-width':4,rx:5}),text('ABANDONED SETTLEMENT',0,-25,20,green),text('same location',0,15,21,ink),path('M-110 55H103',green,4)],'The official replacement softens destruction into administrative abandonment'));reveal('official-map',2);
  add(object('archivist-hand',600,350,[path('M-135 0H135',gold,12),dot(0,0,16,red)],'The archivist hand remains between the older map and the official replacement'));reveal('archivist-hand',2);break;
 case 1:
  add(object('truthful-record',330,275,[n('rect',{x:-170,y:-92,width:340,height:184,fill:'#efe2c3',stroke:ink,'stroke-width':4,rx:5}),text('DESTROYED VILLAGE',0,-25,22,red),text('preserved record',0,15,21,ink),path('M-110 55H103',red,4)],'The truthful old map remains preserved'));reveal('truthful-record',1);
  add(object('archive-institution',650,235,[n('rect',{x:-145,y:-74,width:290,height:148,fill:blue,rx:8}),text('ARCHIVE',0,-18,28,'#f7efdc'),text('keeps the record',0,20,20,'#f7efdc')],'An institution can preserve a record'));reveal('archive-institution',1);
  add(object('decision-institution',965,235,[n('rect',{x:-145,y:-74,width:290,height:148,fill:gold,rx:8}),text('DECISION',0,-18,28,ink),text('route absent',0,20,20,ink)],'The route from preserved truth to usable decision remains absent'));reveal('decision-institution',2);
  add(object('missing-route',800,430,[path('M-180 0H180',red,8),path('M0 -18V18',red,5)],'A visible break keeps preservation separate from power to act'));reveal('missing-route',2);break;
 case 2:
  person('examiner',180,570,blue,.8);act('examiner',1,'question');
  add(object('evidence-table',650,500,[shape('M-390 0H390V22H-390Z',gold),path('M-350 22V110M350 22V110',ink,14)],'A usable hearing gives the examiner a place to test the public claim'));reveal('evidence-table',1);
  add(object('protected-archive',360,260,[n('rect',{x:-130,y:-86,width:260,height:172,fill:blue,rx:8}),text('PROTECTED',0,-22,25,'#f7efdc'),text('ARCHIVE',0,15,29,'#f7efdc')],'A protected archive needs resources that keep it usable'));reveal('protected-archive',1);
  add(object('claim',690,260,[n('rect',{x:-125,y:-82,width:250,height:164,fill:green,rx:8}),text('PUBLIC IDEAL',0,-8,27,'#f7efdc'),text('who sustains it?',0,28,20,'#f7efdc')],'A public declaration sits beside uncertain supporting arrangements'));reveal('claim',2);
  add(object('resources',970,260,[n('rect',{x:-120,y:-82,width:240,height:164,fill:gold,rx:8}),text('RESOURCES',0,-8,26,ink),text('people · funds',0,28,20,ink)],'Resources maintain both the archive and the hearing'));reveal('resources',2);break;
 case 3:
  person('reader',260,575,blue,.86);act('reader',1,'reflect');
  add(object('older-map',430,270,[n('rect',{x:-170,y:-92,width:340,height:184,fill:'#efe2c3',stroke:ink,'stroke-width':4,rx:5}),text('DESTROYED VILLAGE',0,-25,22,red),text('vulnerable record',0,15,21,ink),path('M-110 55H103',red,4)],'The older record remains vulnerable and visible'));reveal('older-map',1);
  add(object('official-map',820,270,[n('rect',{x:-170,y:-92,width:340,height:184,fill:'#efe2c3',stroke:ink,'stroke-width':4,rx:5}),text('ABANDONED SETTLEMENT',0,-25,20,green),text('replacement record',0,15,21,ink),path('M-110 55H103',green,4)],'The replacement map remains beside the older one'));reveal('official-map',2);
  add(object('preservation-choice',630,445,[path('M-200 0H200',gold,7),dot(-190,0,13,red),dot(190,0,13,green),text('preserve?',0,-18,23,ink)],'The choice about preservation remains unresolved'));reveal('preservation-choice',2);break;
 }s.visual=q.finish('An archivist’s maps, protected records, and unresolved preservation choice make the book’s political ecology concrete.');
}fs.writeFileSync(file,JSON.stringify(scenes,null,2));
