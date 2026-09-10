import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const ink='#455c91',light='#adc1f1',clay='#a15e40',clayN='#e9b895';
for(const [index,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
const material=(d,c=ink,cn=light)=>tint(n('path',{d,fill:c}),cn);
const type=(id,value,x,y,size=42)=>a.label(id,value,x,y,size);

const bowl=(id,x,y,k=1)=>shape(id,x,y,[material('M-146 -22Q0 -59 146 -10L120 63Q0 131 -118 59Z',clay,clayN),tint(path('M-146 -22Q-5 28 146 -10',ink,8),light),path('M-118 0Q-100 15 -78 13','$ink',4)],'Mara’s uneven ash-glazed bowl',k);
const head=(id,x,y,c=ink,cn=light,k=1)=>shape(id,x,y,[material('M-58 116V60Q-91 34 -89 -21Q-92 -103 -12 -113Q63 -121 79 -50L103 -9L77 1L66 55L25 71V116Z',c,cn),path('M34 -47H51M36 29H64','$ink',5)],'A likeness whose relationship to its source remains unresolved',k);
const branch=(id,x,y,k=1)=>shape(id,x,y,[tint(n('rect',{x:-70,y:-100,width:140,height:200,rx:55,fill:ink}),light),path('M0 -70V55M0 -12L-37 19M0 18L35 45','$ink',7)],'A stored continuity branch, schematically represented',k);
const potter=(id,x,y,k=1)=>shape(id,x,y,[material('M-64 145Q-90 75 -68 -8Q-54 -45 -10 -35Q33 -29 41 6L18 145Z',clay,clayN),n('path',{d:'M-35 -23Q-71 -49 -57 -104Q-48 -147 -8 -143Q36 -132 25 -76L41 -55L18 -45L8 -19Z',fill:'#b68066'}),material('M-60 -71Q-81 -134 -39 -162Q13 -172 27 -127L16 -108Q-31 -113 -47 -69Z'),tint(dot(-61,-110,28,ink),light),path('M10 -85H20M12 -45H24','#2e2524',3),n('path',{d:'M-39 8Q-5 38 48 53L133 46L138 61L50 76Q-10 67 -54 45Z',fill:'#b68066'}),n('path',{d:'M18 13Q42 30 65 44L110 31L119 44L66 62Q33 53 9 41Z',fill:'#b68066'}),path('M-53 145V186M6 145V186','$ink',17)],'Mara at her bench, cupping and examining a hand-made vessel',k);
switch(index){
case 0:shape('workbench',569,423,[material('M-156 -7H203V14H-156Z'),path('M-127 14V119M172 14V119','$ink',12)],'The bowl rests on an ordinary craft bench');potter('mara',435,333,.86);bowl('bowl',565,398,.42);shape('kiln',1008,365,[material('M-67 115V-78Q0 -148 67 -78V115Z',clay,clayN),material('M-42 20V-51Q0 -80 42 -51V20Z'),path('M-36 49H36','$ink',7)],'A curved brick kiln behind the workbench');a.person('early-copy',824,323,{coat:ink,night:light,pose:'attentive',scale:.67});a.reveal('early-copy',5);break;
case 1:shape('bench',632,433,[material('M-237 -8H237V13H-237Z'),path('M-186 13V108M185 13V108','$ink',12)],'A close workshop view makes scale and handling visible');potter('mara',441,317,1.02);bowl('bowl',594,395,.56);shape('deviation',817,297,[path('M-42 -2Q0 -15 43 0','$ink',4),text('4 mm',0,43,34)],'The source’s measured rim deviation; a detail rather than a verdict');a.reveal('deviation',2);a.hide('deviation',5);break;
case 2:head('source',328,318);head('likeness',868,318,clay,clayN);a.reveal('likeness',3);type('a','Person',328,509);type('b','Echo',868,509);a.reveal('b',3);break;
case 3:branch('runtime',421,320,1.17);head('speaking',844,320,clay,clayN,.87);shape('speech',962,230,[path('M-19 -13Q28 -7 27 19M-10 -32Q53 -23 48 20','$ink',6)],'Speech from an active Echo');a.hide('speech',4);a.hide('speaking',4);shape('paused-body',844,320,[tint(path('M-56 102V49Q-90 26 -76 -53Q-45 -109 30 -79Q69 -61 75 -26L94 5L64 23V50L21 70V102',clay,5),clayN)],'The diagnostic pause removes the speaker while infrastructure remains');a.reveal('paused-body',4);break;
case 4:a.person('mara',308,326,{coat:clay,night:clayN,hairStyle:'long',pose:'concerned',scale:.86});a.person('partner',888,326,{coat:ink,night:light,pose:'open',scale:.86});bowl('shared',595,404,.66);a.move('partner',4,837,326);a.move('mara',5,336,326);break;
case 5:for(let i=0;i<4;i++){branch('archive'+i,260+i*220,280+i%2*55,.67);if(i)a.reveal('archive'+i,i+2);}shape('mars',986,478,[tint(dot(0,0,54,clay),clayN),path('M-35 -6Q0 -32 30 10','$ink',4)],'Distant settlement promises widen the investigation');a.reveal('mars',5);break;
case 6:head('question',595,329,ink,light,1.2);shape('open',822,338,[path('M-35 -70Q45 -113 67 -50Q75 -20 26 17V33','$ink',9),dot(25,62,7,'$ink')],'Uncertainty remains alongside a recognizable person');a.reveal('open',3);break;
case 7:bowl('rim',600,335,1.5);a.move('rim',5,610,338);break;
}

s.visual=a.finish('Cobalt and fired clay; asymmetric ceramic vessels, profile impressions and continuity stores.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
