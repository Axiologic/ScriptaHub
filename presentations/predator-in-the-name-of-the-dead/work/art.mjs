import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#4d716a',cn='#b1d1bd',wax='#b88a40',wn='#ebce8e';
const flower=(x,y,k)=>[fill(`M${x-12*k} ${y}Q${x-24*k} ${y+110*k} ${x+17*k} ${y+215*k}`,c,cn),fill(`M${x-65*k} ${y-25*k}Q${x-49*k} ${y-133*k} ${x} ${y-122*k}Q${x+51*k} ${y-137*k} ${x+65*k} ${y-25*k}Q${x} ${y+19*k} ${x-65*k} ${y-25*k}Z`,wax,wn),tint(path(`M${x-62*k} ${y-25*k}Q${x} ${y-62*k} ${x+62*k} ${y-25*k}`,c,7),cn),fill(`M${x-14*k} ${y+121*k}Q${x-111*k} ${y+53*k} ${x-88*k} ${y+129*k}Q${x-49*k} ${y+164*k} ${x-14*k} ${y+143*k}Z`,c,cn),fill(`M${x-4*k} ${y+79*k}Q${x+79*k} ${y+4*k} ${x+85*k} ${y+65*k}Q${x+35*k} ${y+112*k} ${x-4*k} ${y+93*k}Z`,c,cn),path(`M${x} ${y-47*k}V${y+4*k}`,c,4),dot(x,y+5*k,7*k,c),path(`M${x-53*k} ${y-26*k}Q${x-26*k} ${y-4*k} ${x} ${y-20*k}Q${x+30*k} ${y-1*k} ${x+53*k} ${y-26*k}`,c,4)];
const forest=()=>obj('bell-canopy',600,350,[...flower(-242,-21,1.08),...flower(-50,51,.86),...flower(212,-14,1.17),fill('M-413 187Q-176 128 39 182Q264 117 413 180V207H-413Z',c,cn)],'Rain-catching bell flowers and living ground share one ecology');
const bee=(id,x,y)=>obj(id,x,y,[n('ellipse',{cx:0,cy:0,rx:24,ry:14,fill:wax}),n('ellipse',{cx:-9,cy:-20,rx:22,ry:13,fill:c}),n('ellipse',{cx:12,cy:-22,rx:22,ry:13,fill:c}),path('M-5 -10V9M8 -8V9','$ink',4)],'A beyri pollinator links flower sound to a wax civilization');
if(i===0){forest();obj('probe',892,220,[fill('M-63 -23H22L69 0L22 23H-63L-43 0Z',c,cn),path('M-22 -23V-52M-22 23V52',wax,8)],'An observer passes through a living system');a.move('probe',3,831,226);obj('trace',798,276,[dot(0,0,6,wax)],'A minute material trace stays after the probe');a.reveal('trace',4);}
else if(i===1){forest();bee('pollinator',339,315);a.move('pollinator',3,567,379,2600);obj('citadel',919,414,[fill('M-83 80V-7Q-30 -46 -32 -81Q11 -99 33 -60Q27 -19 69 0L91 80Z',wax,wn),path('M-57 21Q0 -3 55 23M-60 48Q0 24 59 51',c,6)],'Living wax architecture belongs to the same material ecology');a.reveal('citadel',4);}
else if(i===2){obj('measurement-bench',600,421,[rect(-353,-10,706,24,c,cn),path('M-271 14V102M271 14V102','$ink',13)],'A report begins in measurement and is understood retrospectively');obj('balance',607,300,[path('M0 115V-103M-160 -53H160M-160 -53V39M160 -53V39',c,10),fill('M-230 39Q-160 103 -90 39Z',wax,wn),fill('M90 39Q160 103 230 39Z',wax,wn),text('7.3 mg',0,-129,40)],'The source’s tiny probe mass deviation becomes consequential over time');a.move('balance',4,607,312);}
else{forest();bee('pollinator',844,347);a.move('pollinator',4,673,401);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
