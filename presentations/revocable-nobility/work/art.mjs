import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#645074',B='#b58b3d',AN='#c7b6db',BN='#efd19a';
 const chair=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-75,y:-140,width:150,height:165,rx:45,fill:A}),AN),tint(path('M-90 50H90M-65 50V160M65 50V160',A,18),AN)],'An office exists separately from the person who temporarily occupies it.'));
 const sash=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-70 -120H-30L85 110H40Z',fill:B}),BN),tint(dot(53,73,26,B),BN)],'Honor is attached to a revocable mandate, not permanent personal jurisdiction.'));
 const record=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-75 -100H75V100H-75Z',fill:B}),BN),tint(path('M-40 -50H40M-40 0H40M-40 50H20',A,9),AN)],'Independent records make the office answerable beyond ceremonial review.'));
 switch(i){
 case 0:chair('office',580,300);sash('rank',580,300);record('record',970,300);reveal('record',3);move('rank',4,780,300,2200);break;
 case 1:chair('office',360,300);record('record',820,270);add(object('seal',820,270,[tint(dot(0,0,34,A),AN),tint(path('M-15 0L-2 15L20 -15',B,8),BN)],'Review needs evidence and fair conditions, not arbitrary removal.'));reveal('seal',3);add(object('bell',1040,460,[tint(n('path',{d:'M-50 20Q-30 -10 -30 -40Q0 -85 30 -40Q30 -10 50 20Z',fill:B}),BN),tint(dot(0,35,10,A),AN)],'Unending removal threats can undermine necessary decisions.'));reveal('bell',3);move('bell',3,1040,445,500);move('bell',4,1040,460,500);break;
 case 2:add(object('model',350,300,[tint(n('rect',{x:-145,y:-120,width:290,height:210,rx:18,fill:A}),AN),tint(path('M-95 20L-30 -40L35 -15L100 -65',B,12),BN),tint(path('M-75 105H75',A,18),AN)],'A model offers conditional interpretation; the line is illustrative, not reported data.'));record('human-review',890,300);label('conditional','Conditional model',350,475,31);label('judgment','Human judgment',890,475,31);break;
 case 3:chair('old',300,315);chair('new',940,315);sash('rank',300,315);record('record',615,270);move('rank',3,940,315,2800);break;
 }
 s.visual=q.finish('Plum and brass office theatre makes the mandate transferable while review records remain independent; model outputs do not certify political legitimacy.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
