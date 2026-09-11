import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#73536e',B='#b46c81',AN='#c9acce',BN='#efb4c3';
 const person=(id,x,y,scale=1)=>{add({id,asset:id==='other'?'person-09-neutral':'person-04-neutral',x,y,scale,options:{color:A,coat:id==='other'?B:A,dynamicExpressions:true},meaning:'A socially connected adult examining whose judgment governs ordinary life.'});for(const b of (i<2?[1,3,5,7]:i<5?[1,4,7]:[2,5,7])){q.actions.push({actor:id,action:'character.express',beat:b,emotion:['curious','worried','skeptical','determined','relieved','neutral','curious'][b-1],durationMs:500});q.actions.push({actor:id,action:'character.gesture',beat:b,gesture:['question','reflect','recoil','resolve','release','explain','invite'][b-1],offsetMs:600,durationMs:2200});}};
 const chair=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-50,y:-100,width:100,height:100,rx:20,fill:B}),BN),tint(path('M-65 15H65M-45 15V100M45 15V100',A,16),AN)],'A place for a real interlocutor, not an imagined crowd.'));
 const eye=(id,x,y,scale=1)=>add(object(id,x,y,[tint(n('path',{d:'M-100 0Q0 -100 100 0Q0 100 -100 0Z',fill:B}),BN),tint(dot(0,0,27,A),AN)],'An imagined observing audience.',scale));
 const door=(id,x,y)=>add(object(id,x,y,[tint(path('M-75 120V-130H75V120',A,15),AN),tint(n('path',{d:'M-55 -110L45 -80V100L-55 120Z',fill:B}),BN),tint(dot(22,15,7,A),AN)],'An open departure route; the teacher must become unnecessary.'));
 switch(i){
 case 0:person('self',340,520,1.05);eye('audience',920,215,.8);reveal('audience',2);
 add(object('desk',660,450,[tint(path('M-170 0H170M-135 0V85M135 0V85',A,15),AN)],'Ordinary decisions are made under an internalized audience.'));
 add(object('decision',660,365,[tint(n('path',{d:'M-75 -60H45L75 -30V60H-75Z',fill:B}),BN),tint(path('M-40 -20H30M-40 12H45',A,8),AN)],'A decision shifts toward imagined approval before authority is reclaimed.'));
 move('decision',3,750,365);move('decision',6,550,365);move('audience',6,1010,180);break;
 case 1:person('self',610,520);for(let j=0;j<3;j++){eye('e'+j,270+j*330,170,.42);reveal('e'+j,j+1);}hide('e1',5);hide('e2',6);break;
 case 2:chair('teacher',350,360);door('exit',860,300);reveal('exit',3);label('permission','Departure',860,505,30);reveal('permission',3);break;
 case 3:person('self',350,520);person('other',880,520,.93);reveal('other',2);move('self',5,460,520);move('other',5,780,520);chair('seat',605,405);reveal('seat',2);door('departure',1030,280);reveal('departure',5);break;
 case 4:person('self',390,520);add(object('bowl',850,350,[tint(n('path',{d:'M-100 0H100Q80 100 0 100Q-80 100 -100 0Z',fill:B}),BN)],'A modest ritual object represents practice without claims of supernatural or clinical proof.'));reveal('bowl',2);break;
 case 5:person('self',380,520);add(object('reply',850,285,[tint(n('path',{d:'M-115 -90H115Q135 -90 135 -65V45Q135 70 110 70H-50L-100 110V70H-115Q-135 70 -135 45V-65Q-135 -90 -115 -90Z',fill:A}),AN),...[-45,0,45].map(x=>tint(dot(x,-5,12,B),BN))],'A responsive synthetic audience is not the same relationship as reciprocal care.'));reveal('reply',1);break;
 case 6:person('self',600,520,.85);for(let j=0;j<4;j++){const x=[220,970,240,960][j],y=[220,220,440,440][j];label('judgment'+j,['Evidence','Consequence','Conscience','Relationship'][j],x,y,28);reveal('judgment'+j,j+1);}break;
 case 7:chair('teacher',260,375);person('self',650,520);door('exit',980,300);move('self',6,770,520);break;
 }
 s.visual=q.finish('Aubergine and rose chamber theatre: expressive adult, imagined audience, real interlocutor and permission to leave.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2));
await import('./normalize-scenes.mjs');
