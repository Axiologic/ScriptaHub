import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#435568',B='#b76e4c',AN='#b7cfe4',BN='#eabd9d';
 const desk=(id,x,y,word)=>add(object(id,x,y,[tint(path('M-135 25H135M-105 25V120M105 25V120',A,16),AN),tint(n('path',{d:'M-80 -65H80V0H-80Z',fill:B}),BN),tint(text(word,0,-21,25,'white'),'#583621')],'A bounded professional role handles part of a consequential case.'));
 const appeal=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-65,y:-42,width:130,height:84,rx:7,fill:B}),BN),tint(path('M-53 -32L0 8L53 -32',A,8),AN)],'A person’s appeal travels through a process without necessarily finding a remedy.'));
 switch(i){
 case 0:desk('first',275,250,'Decision');desk('second',925,250,'Review');desk('third',600,450,'Referral');appeal('appeal',275,145);move('appeal',2,925,145,1600);move('appeal',3,600,345,1600);move('appeal',4,275,145,1900);break;
 case 1:desk('clinical',270,260,'Clinical');desk('model',920,260,'Model');appeal('appeal',600,210);add(object('person',600,470,[tint(dot(0,-55,29,B),BN),tint(n('path',{d:'M-55 55V0Q0 -60 55 0V55Z',fill:B}),BN)],'The affected person experiences one outcome while institutions divide responsibility.'));move('appeal',2,405,210);move('appeal',3,785,210);break;
 case 2:desk('owner',600,345,'Case owner');appeal('appeal',330,225);add(object('stop',960,250,[tint(n('path',{d:'M-40 -80H40L80 -40V40L40 80H-40L-80 40V-40Z',fill:B}),BN),tint(path('M-38 0H38',A,12),AN)],'Real authority can interrupt a harmful process.'));reveal('stop',2);move('appeal',3,600,235);break;
 case 3:desk('left',290,340,'Evidence');desk('right',930,340,'Remedy');appeal('appeal',290,220);move('appeal',3,930,220,2500);add(object('route',610,485,[tint(path('M-180 0H180M180 0L150 -22M180 0L150 22',B,10),BN)],'The route of responsibility reaches a usable remedy, not only another explanation.'));reveal('route',4);break;
 }
 s.visual=q.finish('Ink and rust relay desks: the same appeal circles among roles until a case owner has evidence and authority to interrupt the process.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
