import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#46697b',B='#b56049',AN='#a7d0df',BN='#efb49f';
 const half=(id,x,y,right=false)=>add(object(id,x,y,[tint(path('M-145 0H145M-110 0V130M110 0V130',A,18),AN),tint(n('path',{d:right?'M-140 -85L140 -85L-140 0Z':'M-140 -85L140 0L140 -85Z',fill:B}),BN)],'A locally competent bridge component does not determine whether its interface is sound.'));
 const lens=(id,x,y)=>add(object(id,x,y,[tint(n('circle',{cx:0,cy:0,r:80,fill:'none',stroke:B,'stroke-width':14}),BN),tint(path('M55 55L115 120',B,20),BN)],'Focused expertise remains useful while its field of view is limited.'));
 const joint=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-45,y:-25,width:90,height:50,rx:7,fill:B}),BN),tint(dot(-25,0,7,A),AN),tint(dot(25,0,7,A),AN)],'Explicit interface ownership connects two responsibilities.'));
 switch(i){
 case 0:half('left',420,330);half('right',800,330,true);lens('inspection',605,210);reveal('inspection',3);move('inspection',4,610,310);break;
 case 1:half('left',350,320);half('right',870,320,true);for(let j=0;j<2;j++){add(object('local-check'+j,350+j*520,170,[tint(dot(0,0,43,A),AN),tint(path('M-20 0L-3 20L25 -20',B,10),BN)],'A passed local check leaves the unowned interface unresolved.'));reveal('local-check'+j,j+2);}break;
 case 2:half('left',420,330);half('right',800,330,true);lens('inspection',600,180);joint('joint',610,330);reveal('joint',3);move('inspection',4,990,180);break;
 case 3:half('left',420,370);half('right',800,370,true);joint('joint',610,370);lens('first-lens',330,200);lens('second-lens',900,200);reveal('second-lens',2);break;
 }
 s.visual=q.finish('Steel-blue precision workshop: correct local components leave an unowned seam; inspection and explicit joint ownership connect responsibilities without replacing specialist lenses.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
