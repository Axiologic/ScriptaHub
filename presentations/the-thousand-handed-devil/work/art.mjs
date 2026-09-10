import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#435568',B='#b76e4c',AN='#b7cfe4',BN='#eabd9d';
 const desk=(id,x,y,word)=>{storyPerson(q,id+'-worker',x,y+24,{identity:id==='second'||id==='model'?'person-04-neutral':'person-02-neutral',coat:id==='second'||id==='model'?'#569a89':'#6388b6',seated:true,scale:.56});add(object(id,x,y,[n('path',{d:'M-135 25H135V43H-135Z',fill:'#d6a448'}),path('M-105 43V120M105 43V120',A,12),n('path',{d:'M-75 45H75V95H-75Z',fill:'#c97560'}),text(word,0,77,24,'#fff6e5')],'A staffed professional role handles part of a consequential case.'));storyGesture(q,id+'-worker',2,'explain');};
 const appeal=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-65,y:-42,width:130,height:84,rx:7,fill:B}),BN),tint(path('M-53 -32L0 8L53 -32',A,8),AN)],'A person’s appeal travels through a process without necessarily finding a remedy.'));
 switch(i){
 case 0:desk('first',275,250,'Decision');desk('second',925,250,'Review');desk('third',600,450,'Referral');appeal('appeal',275,250);move('appeal',2,925,250,1600);move('appeal',3,600,450,1600);move('appeal',4,275,250,1900);break;
 case 1:desk('clinical',270,260,'Clinical');desk('model',920,260,'Model');appeal('appeal',600,210);storyPerson(q,'person',600,520,{identity:'person-04-neutral',coat:'#d59c47',scale:.73});move('appeal',2,405,335);move('appeal',3,785,335);break;
 case 2:desk('owner',600,345,'Case owner');appeal('appeal',330,345);add(object('stop',960,250,[tint(n('path',{d:'M-40 -80H40L80 -40V40L40 80H-40L-80 40V-40Z',fill:B}),BN),tint(path('M-38 0H38',A,12),AN)],'Real authority can interrupt a harmful process.'));reveal('stop',2);move('appeal',3,600,345);break;
 case 3:desk('left',290,340,'Evidence');desk('right',930,340,'Remedy');appeal('appeal',290,340);move('appeal',3,930,340,2500);add(object('route',610,485,[tint(path('M-180 0H180M180 0L150 -22M180 0L150 22',B,10),BN)],'The route of responsibility reaches a usable remedy, not only another explanation.'));reveal('route',4);break;
 }
 s.visual=q.finish('Ink and rust relay desks: the same appeal circles among roles until a case owner has evidence and authority to interrupt the process.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
