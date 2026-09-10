import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#794555',B='#84785d',AN='#dba4b7',BN='#d9cbb0';
 const office=(id,x,y)=>add(object(id,x,y,[tint(path('M-155 30H155M-120 30V145M120 30V145',A,16),AN),tint(n('rect',{x:-65,y:-110,width:130,height:110,rx:35,fill:B}),BN)],'An institutional office persists across individual occupants.'));
 const plate=(id,x,y,word)=>add(object(id,x,y,[tint(n('path',{d:'M-85 -30H85V30H-85Z',fill:A}),AN),tint(text(word,0,10,25,'white'),'#35222a')],'A role holder can change without changing institutional incentives.'));
 const house=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-90 85V-30L0 -100L90 -30V85Z',fill:B}),BN),tint(n('rect',{x:-20,y:20,width:40,height:65,fill:A}),AN)],'An affected household stands outside the decision boundary.'));
 switch(i){
 case 0:office('office',310,275);plate('person1',310,280,'Holder A');plate('person2',310,280,'Holder B');reveal('person2',3);hide('person1',3);house('outside',940,325);add(object('outlet',600,430,[tint(path('M-165 0H120V-70H240',A,15),AN)],'The consequence route remains even when the office changes hands.'));reveal('outlet',2);break;
 case 1:office('office',400,275);house('outside',990,360);add(object('boundary',750,280,[tint(path('M0 -160V190',B,18),BN)],'A boundary separates received information from the consequence outside it.'));add(object('report',600,250,[tint(n('path',{d:'M-55 -70H55V70H-55Z',fill:A}),AN),tint(path('M-30 -30H30M-30 0H15',B,8),BN)],'Selected reports travel inward.'));move('report',2,480,250);break;
 case 2:add(object('manuscript',425,310,[tint(n('path',{d:'M-145 -165H115L150 -125V165H-145Z',fill:A}),AN),tint(path('M-95 -95H85M-95 -30H85M-95 35H45M-95 100H70',B,10),BN)],'The argument itself selects and organizes evidence.'));add(object('lens',860,285,[tint(n('circle',{cx:0,cy:0,r:95,fill:'none',stroke:B,'stroke-width':16}),BN),tint(path('M65 70L140 150',B,22),BN)],'The final critique examines category errors and rhetorical selection in the book itself.'));move('lens',3,610,285,2200);break;
 case 3:office('office',330,270);house('outside',910,340);add(object('return',630,450,[tint(path('M250 0Q0 110 -220 0M-220 0L-180 8M-220 0L-198 35',B,10),BN)],'Correction requires consequences to become actionable for those holding authority.'));reveal('return',3);break;
 }
 s.visual=q.finish('Burgundy institutional theatre: offices outlive occupants, consequence paths persist, and the book places its own explanatory lens under review.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
