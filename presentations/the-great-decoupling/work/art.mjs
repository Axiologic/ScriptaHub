import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#355574',B='#889ca8',AN='#abcde8',BN='#d9e4e9';
 const page=(id,x,y,complete=false)=>add(object(id,x,y,[tint(n('path',{d:'M-95 -130H70L95 -105V130H-95Z',fill:complete?A:B}),complete?AN:BN),tint(path(complete?'M-60 -75H60M-60 -25H60M-60 25H60M-60 75H60':'M-60 -75H20M-60 -25H-10M-60 25H35',complete?B:A,10),complete?BN:AN)],complete?'A polished output can conceal uncertainty about its maker’s independent understanding.':'An incomplete explanatory sketch reveals what remains understood by the user.'));
 const printer=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-145,y:-70,width:290,height:140,rx:25,fill:A}),AN),tint(path('M-95 -30H95',B,14),BN),tint(dot(102,25,11,B),BN)],'An automated production system creates a useful artifact.'));
 switch(i){
 case 0:printer('machine',330,390);page('output',330,260,true);page('understanding',920,290);move('output',2,650,260);label('sketch','Explanation',920,480,31);reveal('understanding',2);reveal('sketch',2);break;
 case 1:page('polished',340,305,true);page('sketch',870,305);add(object('separation',610,300,[tint(path('M-45 -15H45M-45 15H45M-25 55L25 -55',A,10),AN)],'Artifact quality is no longer sufficient evidence of independent understanding.'));reveal('separation',3);break;
 case 2:add(object('practice-desk',600,410,[tint(path('M-230 0H230M-185 0V110M185 0V110',A,16),AN)],'A supervised practice space preserves the process of learning.'));page('sketch',520,280);add(object('pencil',815,300,[tint(n('path',{d:'M-18 -100H18V65L0 110L-18 65Z',fill:A}),AN)],'Practice remains active rather than being replaced by delivered output.'));reveal('pencil',2);move('pencil',4,675,295);break;
 case 3:printer('machine',300,400);page('output',300,245,true);page('explanation',900,285);add(object('answerability',600,445,[tint(path('M-130 0H130M-130 0L-105 -18M-130 0L-105 18',A,10),AN)],'Delegated output remains connected to an independent capacity to explain and correct it.'));reveal('answerability',3);break;
 }
 s.visual=q.finish('Prussian-blue drafting room contrasts polished production with an unfinished explanation, then restores a supervised practice space and answerability.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
