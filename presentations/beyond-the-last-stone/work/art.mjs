import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const ink='#7b533b',light='#d9b298',ochre='#bd7928',ochreN='#efd294';
for(const [index,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
const material=(d,c=ink,cn=light)=>tint(n('path',{d,fill:c}),cn);
const type=(id,value,x,y,size=42)=>a.label(id,value,x,y,size);

const pebble=(id,x,y,k=1)=>shape(id,x,y,[material('M-34 4Q-39 -20 -6 -25Q36 -25 39 3Q33 28 0 27Q-32 26 -34 4Z')],'A movable counting stone',k);
const flame=(id,x,y,k=1)=>shape(id,x,y,[material('M-5 -113Q20 -65 7 -43Q64 -96 76 -11Q78 70 0 87Q-68 80 -68 18Q-73 -24 -26 -69Q-31 -28 -5 -113Z',ochre,ochreN),material('M0 -23Q37 36 0 65Q-33 47 0 -23Z')],'Shared fire',k);
const hand=(id,x,y,k=1)=>shape(id,x,y,[material('M-40 86L-58 29L-77 -1Q-81 -23 -61 -18L-39 10L-44 -62Q-42 -82 -27 -72L-14 -9L-14 -88Q-7 -106 5 -88L11 -11L27 -78Q39 -96 47 -76L36 -2L57 -51Q72 -62 76 -40L53 29L40 86Z',ochre,ochreN)],'A red hand mark preserves a trace without a complete explanation',k);
const grain=(id,x,y,k=1)=>shape(id,x,y,[tint(path('M0 103V-99',ink,9),light),...[-60,-10,40].flatMap(y=>[material(`M0 ${y}Q-63 ${y-39} -57 ${y-63}Q0 ${y-56} 0 ${y}Z`,ochre,ochreN),material(`M0 ${y+15}Q63 ${y-24} 57 ${y-48}Q0 ${y-41} 0 ${y+15}Z`,ochre,ochreN)])],'Stored grain changes time and obligation',k);
switch(index){
case 0:shape('cave',249,319,[material('M-105 204L-132 114L-151 -37L-137 -112L-67 -178L-5 -168L54 -128L103 -33L135 19L155 204H73L65 131L58 81L31 40L12 4L-15 34L-32 63L-36 141L-33 204Z')],'The cave mouth from which the empty path is watched');shape('ridge',846,381,[material('M-298 95L-249 59L-206 46L-181 2L-141 -18L-102 -8L-64 15L-24 9L32 -15L78 -46L132 -72L160 -38L216 5L241 28L303 95Z',ochre,ochreN)],'A bare ridge where no herd appears');flame('fire',452,422,.43);a.person('ar',567,369,{coat:ink,night:light,pose:'concerned',scale:.56});a.move('ar',5,604,365,2800);for(let i=0;i<3;i++)pebble('stone'+i,662+i*63,467,.46);break;
case 1:a.person('watch',402,386,{coat:ochre,night:ochreN,pose:'concerned',scale:.46});a.move('watch',5,471,365,2800);shape('ridge',596,330,[material('M-395 79L-252 -12L-122 24L29 -60L173 9L295 -34L395 79Z')],'The empty northern ridge');flame('camp',267,421,.42);a.reveal('camp',3);break;
case 2:shape('snow',703,384,[material('M-387 81L-327 -28L-189 -117L-73 -91L43 -138L193 -79L323 7L381 85Z','#d7c6b3','#565150')],'Old snow under a ridge carries distinct tracks');shape('tracks',668,346,[...[-70,-12,46,104].flatMap((y,i)=>[tint(n('ellipse',{cx:18+i*18,cy:y,rx:7,ry:18,fill:ink}),light),tint(n('ellipse',{cx:39+i*18,cy:y+5,rx:7,ry:18,fill:ink}),light)])],'Two-part hoof marks are observable evidence');a.person('tracker',365,332,{coat:ochre,night:ochreN,pose:'concerned',scale:.72});shape('point',483,398,[tint(path('M-90 -8Q-33 -46 23 -7',ink,7),light)],'The tracker directs attention toward the physical sign');a.reveal('point',3);a.move('tracker',5,408,342,2600);break;
case 3:for(let i=0;i<6;i++){pebble('count'+i,i===5?950:225+i*132,i===5?450:340,.94);if(i===5){a.reveal('count'+i,2);a.move('count'+i,3,885,340,2400)};}type('finite','6 stones',600,499,43);a.reveal('finite',2);break;
case 4:shape('rock',596,320,[material('M-349 167L-367 -92L-233 -152L-67 -134L103 -171L339 -97L368 146L169 177L-55 152Z','#d0bdab','#504b45')],'A cave wall carries hands from people no longer present');hand('old',374,317,1.16);hand('new',855,296,.71);a.reveal('new',3);shape('pouch',598,420,[material('M-46 -69Q0 -41 46 -69L64 53Q0 105 -64 53Z'),path('M-43 -52H43','$ink',7)],'Kee’s pouch links physical traces to remembered reasons');a.reveal('pouch',4);break;
case 5:grain('grain',245,314,.94);a.person('stranger',566,388,{coat:ochre,night:ochreN,pose:'concerned',scale:.57});a.move('stranger',4,641,388,2500);shape('granary',824,337,[material('M-138 108V-58L0 -135L138 -58V108Z'),material('M-36 108V-1H36V108Z',ochre,ochreN),path('M-100 -23H-56M56 -23H100','$ink',7)],'The grain house at Many Fires');a.reveal('granary',3);break;
case 6:grain('debt',374,335,.85);for(let i=0;i<4;i++){pebble('owed'+i,716+i*65,356,.62);if(i)a.reveal('owed'+i,3);}shape('tablet',813,452,[material('M-114 -24H114V24H-114Z',ochre,ochreN)],'A clay record assigns obligations');a.reveal('tablet',4);break;
case 7:flame('begin',351,345,1);pebble('one',825,389,1.8);a.reveal('one',4);break;
}

s.visual=a.finish('Ochre traces and warm stone; prehistoric material thought, no modern symbols or machines.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
