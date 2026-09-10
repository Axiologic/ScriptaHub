import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#3f567e',B='#b17c55',AN='#b3c6ea',BN='#e7c0a1';
 const bell=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-95 80Q-50 30 -50 -50Q0 -135 50 -50Q50 30 95 80Z',fill:B}),BN),tint(path('M0 -105V-145M-45 -145H45',A,13),AN),tint(dot(0,103,19,A),AN)],'A resonant ritual object makes a bodily experience concrete without settling its interpretation.'));
 const footprint=(id,x,y,flip=1)=>add(object(id,x,y,[tint(n('ellipse',{cx:0,cy:0,rx:22,ry:48,fill:A}),AN),tint(dot(flip*12,-55,15,A),AN)],'A bodily practice has rhythm and orientation without making every tradition identical.'));
 const page=(id,x,y,word)=>add(object(id,x,y,[tint(n('path',{d:'M-130 -110H100L130 -80V110H-130Z',fill:A}),AN),tint(text(word,0,10,29,'white'),'#25314c')],'One explanatory layer is preserved separately from the others.'));
 switch(i){
 case 0:bell('bell',610,280);for(let j=0;j<4;j++){footprint('step'+j,[280,420,800,940][j],[440,465,465,440][j],j%2?-1:1);reveal('step'+j,j+2);}break;
 case 1:bell('experience',300,300);page('interpretation',880,300,'Interpretation');reveal('interpretation',3);add(object('space',600,310,[tint(path('M-40 -12H40M-40 12H40M-20 45L20 -45',B,10),BN)],'The mechanism and the metaphysical conclusion cannot simply be equated.'));reveal('space',4);break;
 case 2:page('practice',330,260,'Practice');page('authority',870,365,'Authority');add(object('door',620,425,[tint(path('M-65 95V-110H65V95',B,14),BN)],'A participant’s right to question or leave helps assess institutional authority.'));reveal('door',4);break;
 case 3:bell('bell',600,310);add(object('notebook',1010,330,[tint(n('path',{d:'M-70 -135H70V135H-70Z',fill:A}),AN),tint(path('M-40 -65H35M-40 0H15M-40 65H35',B,8),BN)],'The invented observer records provisional findings and unresolved questions.'));reveal('notebook',2);footprint('leaving',250,400);move('leaving',4,190,440);break;
 }
 s.visual=q.finish('Midnight and copper field study: bodily rhythm, resonant experience and separate interpretive records avoid treating religion as one generic object.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
