import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#ad664e',B='#36798a',AN='#edb39c',BN='#92d1df';
 const house=(id,x,y,scale=1,door=true)=>add(object(id,x,y,[tint(n('path',{d:'M-120 100V-35L0 -125L120 -35V100Z',fill:A}),AN),tint(n('rect',{x:-82,y:-12,width:50,height:55,rx:4,fill:B}),BN),tint(n('rect',{x:32,y:-12,width:50,height:55,rx:4,fill:B}),BN),tint(n('rect',{x:-22,y:40,width:44,height:60,fill:door?B:A}),door?BN:AN)],'A home receiving useful services, not a claim about universal housing design.',scale));
 const sun=(id,x,y)=>add(object(id,x,y,[tint(dot(0,0,48,A),AN)],'Available energy potential.'));
 const water=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M0 -70C-95 25 -48 78 0 78C48 78 95 25 0 -70Z',fill:B}),BN)],'Usable water service.'));
 const panel=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-85 -55H65L95 45H-55Z',fill:B}),BN),tint(path('M-10 45V90M-60 90H40',A,10),AN)],'Built electricity infrastructure.'));
 switch(i){
 case 0:
 add(object('home-section',750,310,[tint(n('path',{d:'M-240 -120L0 -220L240 -120Z',fill:A}),AN),tint(path('M-215 -110V170H215V-110M-215 22H215M10 22V165',A,14),AN),tint(n('path',{d:'M-95 -180L20 -225L125 -183L15 -138Z',fill:B}),BN),tint(n('rect',{x:80,y:55,width:80,height:80,rx:12,fill:B}),BN),tint(n('circle',{cx:120,cy:95,r:23,fill:'none',stroke:A,'stroke-width':8}),AN),tint(path('M-175 105H-50M-150 108V158M-75 108V158',B,12),BN),tint(n('rect',{x:-165,y:-65,width:115,height:45,rx:6,fill:B}),BN),tint(path('M-140 -82V-103H-95V-82',B,10),BN)],'An inhabited home cutaway links electricity, water, food and washing as actual services.'));
 add(object('reservoir',200,310,[tint(n('path',{d:'M-65 -120H65V90Q0 130 -65 90Z',fill:B}),BN),tint(path('M-50 -30Q-20 -45 0 -30T50 -30',A,8),AN)],'Water capacity outside the home is distinct from delivery to it.'));
 add(object('pipe',390,365,[tint(path('M-125 0H30V-70H145',B,12),BN)],'A distribution connection makes an available resource usable inside a home.'));reveal('pipe',3);
 add(object('flow',275,365,[tint(dot(0,0,15,A),AN)],'The delivery path closes the gap between supply and household access.'));reveal('flow',4);move('flow',4,420,365,1200);move('flow',5,420,295,900);move('flow',6,535,295,1000);
 break;
 case 1:sun('potential',230,275);panel('capacity',600,275);house('access',975,285,.65);label('p','Potential',230,450);label('c','Capacity',600,450);label('a','Access',975,450);reveal('capacity',2);reveal('c',2);reveal('access',3);reveal('a',3);break;
 case 2:panel('panel',300,280);house('home',865,290);add(object('service',600,350,[tint(path('M-190 0H190',B,12),BN)],'A physical service connection, not a decorative background line.'));reveal('service',2);add(object('current',465,350,[tint(dot(0,0,17,A),AN)],'Energy becomes useful when delivered through built infrastructure.'));reveal('current',3);move('current',3,730,350,2500);sun('sun',470,165);reveal('sun',1);break;
 case 3:
 add(object('field',320,330,[tint(n('path',{d:'M-220 115L-130 20H135L220 115Z',fill:A}),AN),...[-110,-35,40,115].flatMap(x=>[tint(path(`M${x} 32V-75`,B,8),BN),tint(n('path',{d:`M${x} -35Q${x-55} -90 ${x-40} -25Q${x-15} 0 ${x} -35Z`,fill:B}),BN),tint(n('path',{d:`M${x} -65Q${x+55} -120 ${x+40} -50Q${x+15} -25 ${x} -65Z`,fill:B}),BN)])],'Food production depends on living systems, not merely an aggregate calorie count.'));
 add(object('table',890,355,[tint(path('M-120 45H120M-90 48V145M90 48V145',A,15),AN),tint(n('ellipse',{cx:0,cy:8,rx:68,ry:20,fill:B}),BN),tint(path('M-105 -8V30M105 -8V30',B,6),BN)],'Household food access remains separate from production in the field.'));
 add(object('delivery',540,420,[tint(n('path',{d:'M-75 -35H25V25H-75ZM25 -20H60L82 8V25H25Z',fill:B}),BN),tint(dot(-40,38,18,A),AN),tint(dot(52,38,18,A),AN)],'Distribution helps connect production with a meal.'));reveal('delivery',2);move('delivery',4,690,420,2500);
 add(object('meal',890,345,[tint(dot(-20,0,13,A),AN),tint(dot(15,-3,16,A),AN)],'Food becomes useful through access, rather than production alone.'));reveal('meal',5);break;
 case 4:house('home',890,295,.8);add(object('robot',340,300,[tint(n('rect',{x:-65,y:-110,width:130,height:100,rx:25,fill:B}),BN),tint(dot(-25,-63,10,A),AN),tint(dot(25,-63,10,A),AN),tint(path('M-35 20V90M35 20V90M-65 0L-100 50M65 0L100 50',B,22),BN),tint(n('rect',{x:-55,y:-5,width:110,height:65,rx:18,fill:A}),AN)],'A service robot whose useful work also requires maintenance and supervision.'));label('repair','Maintenance',600,490);reveal('repair',4);move('robot',3,480,300);break;
 case 5:add(object('clock',330,280,[tint(n('circle',{cx:0,cy:0,r:90,fill:'none',stroke:B,'stroke-width':16}),BN),tint(path('M0 -55V0L45 20',A,12),AN)],'Time remains limited.'));house('place',870,290,.9);label('time','Time',330,460);label('place-label','Place',870,460);add(object('hour',330,225,[tint(dot(0,0,12,A),AN)],'A passing hour cannot be reproduced by producing more goods.'));move('hour',3,385,280,2200);reveal('place',4);reveal('place-label',4);break;
 case 6:for(let j=0;j<3;j++){house('h'+j,270+j*330,300,.65);reveal('h'+j,j+1);}add(object('key',600,495,[tint(n('circle',{cx:-55,cy:0,r:25,fill:'none',stroke:B,'stroke-width':12}),BN),tint(path('M-30 0H70M40 0V25M65 0V25',B,12),BN)],'Ownership and institutional access determine who can use the capacity.'));reveal('key',4);break;
 case 7:house('home',600,295,1.35);sun('energy',250,200);water('water',980,360);reveal('energy',2);reveal('water',3);break;
 }
 s.visual=q.finish('Terracotta and sea-blue civic cutaway; one home connects energy, water, repair and access across changing scales.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2));
