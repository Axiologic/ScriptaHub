import fs from'node:fs';import{stageAuthor}from'../../../tools/shf/stage-authoring.mjs';const f=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(f));
for(const[i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#367b80',B='#bb8b3d',AN='#a0d9d6',BN='#efce91';
 const island=(id,x,y,variant=0)=>add(object(id,x,y,[tint(n('path',{d:['M-130 -20L-70 -110L35 -95L120 -20L75 95L-75 110Z','M-135 -45L-35 -100L85 -50L130 45L15 115L-90 70Z','M-125 0L-55 -115L70 -85L135 10L65 90L-65 65Z'][variant],fill:A}),AN)],'A conceptual local jurisdiction, not a forecast map of real territories.'));
 const workshop=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-60 45V-35L0 -80L60 -35V45Z',fill:B}),BN),tint(n('rect',{x:-20,y:-5,width:40,height:50,fill:A}),AN)],'Local productive and administrative capacity.'));
 const beacon=(id,x,y)=>add(object(id,x,y,[tint(path('M0 85V-75M-35 85H35',B,13),BN),tint(dot(0,-90,27,B),BN)],'A shared warning or coordination function serves risks crossing local boundaries.'));
 switch(i){
 case 0:island('a',280,330);island('b',890,290,1);workshop('wa',280,315);workshop('wb',890,275);beacon('shared',590,240);reveal('wb',2);reveal('shared',3);break;
 case 1:island('local',420,330,2);workshop('w',420,310);add(object('owner-key',900,280,[tint(n('circle',{cx:-45,cy:0,r:40,fill:'none',stroke:B,'stroke-width':14}),BN),tint(path('M-5 0H120M80 0V30M110 0V30',B,14),BN)],'Local capability can remain dependent on a distant owner’s permission.'));reveal('owner-key',2);add(object('link',680,360,[tint(path('M-110 0H110',A,12),AN)],'The dependency crosses the apparent local boundary.'));reveal('link',3);break;
 case 2:island('a',280,365);island('b',910,365,1);beacon('shared',600,230);add(object('warning-left',460,240,[tint(path('M50 0L-55 65M-55 65L-22 60M-55 65L-42 35',B,10),BN)],'Shared coordination reaches a local jurisdiction.'));add(object('warning-right',740,240,[tint(path('M-50 0L55 65M55 65L22 60M55 65L42 35',B,10),BN)],'A cross-boundary risk needs capacity beyond a single locality.'));reveal('warning-left',2);reveal('warning-right',2);break;
 case 3:island('a',270,340);island('b',950,340,1);island('c',610,200,2);workshop('wa',270,325);workshop('wb',950,325);workshop('wc',610,185);add(object('bridge',600,470,[tint(path('M-280 0Q0 90 280 0',B,13),BN)],'Shared obligations connect alternatives without abolishing their local differences.'));reveal('bridge',3);break;
 }
 s.visual=q.finish('Teal and amber archipelago study: local capability, external ownership and shared warning functions occupy different scales of conceptual geography.');
}fs.writeFileSync(f,JSON.stringify(scenes,null,2));
