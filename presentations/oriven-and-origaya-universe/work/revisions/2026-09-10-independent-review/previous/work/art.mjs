import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#4a7360',cn='#b5d4bd',och='#98794d',on='#ddc596';
const canopy=()=>obj('rooted-observer',570,325,[fill('M-95 90Q-58 -11 -85 -147Q-11 -223 87 -140Q52 -10 86 90L237 149L118 142L47 101L44 159H19L-7 106L-121 160L-227 148Z',c,cn),path('M-207 150Q-110 112 -83 48M-89 149Q-35 90 -28 -74M94 147Q34 71 26 -70M207 151Q89 98 79 45',och,10),...[-117,-44,40,111].map((x,j)=>n('ellipse',{cx:x,cy:-124-Math.abs(x)*.3,rx:76,ry:52,fill:c}))],'A rooted observer experiences memory and dependence through a living canopy');
if(i===0||i===1){canopy();obj('water',597,501,[path('M-346 0Q-225 -36 -95 0T188 0T356 0',och,14)],'Water and root dependence remain beneath deliberation');obj('distant-predator',944,304,[fill('M-71 4L-43 -18L13 -13L30 -37L51 -35L74 -14L54 3L34 4L12 20L-42 20L-60 42H-75L-57 10Z',och,on)],'The distant act interrupts a nonpredatory civilization’s categories');a.reveal('distant-predator',3);if(i===1)a.hide('distant-predator',5);}
else if(i===2){obj('two-ground-systems',607,401,[fill('M-409 90Q-239 -56 -38 59L-75 146H-409Z',c,cn),fill('M39 50Q245 -64 408 82V146H79Z',och,on),path('M-90 -103Q0 -151 92 -103',c,13)],'Different material environments are separated by a real boundary');obj('descending-seed',603,220,[fill('M0 -77Q81 -7 0 74Q-75 -8 0 -77Z',c,cn),path('M0 -49V50',och,7)],'An intervention approaches another world rather than already owning it');a.move('descending-seed',3,603,352);obj('limit',604,413,[path('M-62 0H62',och,12)],'The question of authority interrupts the descent');a.reveal('limit',4);}
else{canopy();obj('opening',912,336,[fill('M-43 129V-133H45V129H28V-108H-27V129Z',och,on)],'Return to the first contact through the observer’s own material dependence');a.reveal('opening',3);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
