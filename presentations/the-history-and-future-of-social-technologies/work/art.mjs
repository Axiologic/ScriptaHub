import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#50585b',B='#ac7452',AN='#c2ced1',BN='#eac4a9';
 const loom=(id,x,y)=>add(object(id,x,y,[tint(path('M-170 175V-175H170V175M-195 -140H195M-195 140H195',A,17),AN),...[-100,-50,0,50,100].map(x=>tint(path(`M${x} -135V135`,B,5),BN))],'A loom represents composition of rules and capabilities; people are not mechanical threads.'));
 const shuttle=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-100 0L-60 -25H60L100 0L60 25H-60Z',fill:B}),BN)],'A transmissible pattern links material capacity with institutional rules.'));
 const ledger=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-95 -120H95V120H-95Z',fill:A}),AN),tint(path('M-60 -70H60M-60 -20H60M-60 30H60M-60 80H35',B,8),BN)],'A shared record carries obligations beyond one immediate interaction.'));
 switch(i){
 case 0:loom('loom',620,300);shuttle('shuttle',430,300);move('shuttle',2,750,300,1800);move('shuttle',4,500,350,1800);ledger('rule',1030,315);reveal('rule',3);break;
 case 1:ledger('record',580,300);add(object('coin',270,315,[tint(dot(0,0,85,B),BN),tint(n('circle',{cx:0,cy:0,r:50,fill:'none',stroke:A,'stroke-width':9}),AN)],'The physical money symbol relies on a surrounding institutional promise.'));add(object('seal',950,320,[tint(dot(0,0,65,B),BN),tint(path('M-30 0L-5 30L40 -30',A,12),AN)],'Recognition and enforcement make the recorded claim usable.'));reveal('record',2);reveal('seal',3);break;
 case 2:loom('loom',600,300);add(object('woven',600,325,[tint(n('rect',{x:-125,y:-90,width:250,height:180,fill:B}),BN),tint(path('M-90 -45H90M-90 0H90M-90 45H45',A,12),AN)],'A composed institution can work while preserving an opening for revision.'));reveal('woven',2);add(object('repair-opening',690,360,[tint(n('rect',{x:-35,y:-35,width:70,height:70,fill:A}),AN)],'A deliberately maintained revision point lets evidence change the arrangement.'));reveal('repair-opening',4);break;
 case 3:ledger('record',310,300);loom('loom',850,310);shuttle('revision',660,365);reveal('revision',3);move('revision',4,930,365,1800);break;
 }
 s.visual=q.finish('Graphite and copper civic loom: records, recognition and material capability compose a revisable institution rather than a deterministic machine.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
