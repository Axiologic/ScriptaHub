import fs from 'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#394b7e',B='#bb8831',AN='#adbae8',BN='#f1cc88';
 const window=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-80,y:-105,width:160,height:210,rx:70,fill:A}),AN),tint(dot(0,0,29,B),BN)],'A privately recognized signal is not yet mutually visible.'));
 const shutter=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-90,y:-110,width:180,height:220,rx:7,fill:B}),BN)],'A social visibility barrier, not a literal collective brain.'));
 const idea=(id,x,y,irregular=true)=>add(object(id,x,y,[tint(n('path',{d:irregular?'M-75 -110H55V-55H90V-5H55V110H-75Z':'M-75 -110H75V110H-75Z',fill:B}),BN),tint(path('M-45 -60H20M-45 -15H40M-45 30H25M-45 75H35',A,8),AN)],'An idea’s irregular detail can carry information rather than mere stylistic noise.'));
 switch(i){
 case 0:for(let j=0;j<3;j++){window('w'+j,300+j*300,300);shutter('s'+j,300+j*300,300);hide('s'+j,j+2);}break;
 case 1:for(let j=0;j<3;j++)window('w'+j,260+j*340,300);add(object('shared',600,500,[tint(path('M-340 0H340M-340 0V-65M0 0V-65M340 0V-65',B,9),BN)],'Mutual visibility changes expectations about what others may publicly do.'));reveal('shared',3);break;
 case 2:idea('irregular',280,310);add(object('roller',630,310,[tint(n('rect',{x:-55,y:-145,width:110,height:290,rx:55,fill:A}),AN)],'A fluent smoothing process can remove decision-relevant irregularity.'));idea('smooth',960,310,false);reveal('smooth',3);move('irregular',2,490,310);hide('irregular',3);label('loss','Lost distinction',630,525,28);reveal('loss',4);break;
 case 3:idea('idea',570,290);add(object('open-aperture',600,320,[tint(path('M-230 130V-170H-100M100 -170H230V130',A,16),AN)],'An institution can expose and revise its filters rather than guarantee every rejected idea is valuable.'));reveal('open-aperture',2);move('idea',4,600,315);break;
 }
 s.visual=q.finish('Ink and saffron observatory: private windows become mutually visible; a smoothing roller tests the difference between clarity and erased information.');
}fs.writeFileSync(file,JSON.stringify(scenes,null,2));
