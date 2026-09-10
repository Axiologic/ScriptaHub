import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const blue='#456779',pale='#b9d8e6',terra='#a65540',tn='#e9aa95';
const seated=(id,x,y,coat,night)=>obj(id,x,y,[rect(-44,72,105,12,'#987c55','#d8c196'),path('M-35 84V144M53 84V144','$ink',9),fill('M-37 -28Q0 -45 35 -25L40 72H-38Z',coat,night),n('ellipse',{cx:0,cy:-76,rx:31,ry:38,fill:'#bd896c'}),fill('M-32 -85Q-41 -130 1 -119Q40 -125 32 -83L18 -99L-25 -98Z','#393333'),path('M-16 -80H-7M8 -80H17M-10 -52Q0 -47 12 -54','#241e1b',3),path('M-31 -10Q-51 41 39 42M32 -7L59 26L98 21',coat,14),path('M-22 73L36 85L46 135M25 73L83 85L91 135',coat,18),path('M43 135H65M90 135H114','$ink',10)],'A seated person works at the surface with feet below it');
const desk=()=>obj('desk',600,442,[fill('M-375 -10H375L343 24H-343Z',blue,pale),path('M-320 24V106M300 24V106','$ink',13)],'A shared workplace ties output to responsibility');
const pages=(id,x,y,count)=>obj(id,x,y,Array.from({length:count},(_,j)=>[rect(j*7,-j*9,116,74,'#f0e9d9','#d5d6cc',4),path(`M${18+j*7} ${22-j*9}h70M${18+j*7} ${40-j*9}h47`,blue,4)]).flat(),'Competent outputs multiply without increasing recognition automatically');
if(i===0||i===1){desk();seated('worker',382,405,terra,tn);pages('first-output',537,362,1);pages('more-output',759,316,6);a.reveal('more-output',3);obj('verification',684,376,[path('M-23 0L-4 19L30 -23',blue,9)],'A deliberate check rather than another generated output');a.reveal('verification',5);if(i===1){a.hide('more-output',5);a.move('worker',4,396,405);}}
else if(i===2){obj('conversation-table',612,427,[fill('M-230 -8Q0 -51 230 -8L195 26H-193Z',terra,tn),path('M-165 26V108M165 26V108','$ink',12)],'A human conversation has limited attention and material time');seated('person',348,394,blue,pale);obj('terminal',855,318,[rect(-65,-113,130,209,blue,pale,28),rect(-48,-88,96,150,'#f0e9d9','#293b43',10),path('M-22 -37Q0 -50 25 -36M-22 -12Q0 -25 25 -11M-22 13Q0 0 25 14',terra,7)],'Fast responsive display represents social timing, not proof of felt emotion');a.reveal('terminal',2);obj('human-cup',491,390,[fill('M-24 -14H24L18 21H-18Z',blue,pale),path('M24 -5Q43 -7 36 12H22',blue,5)],'The ordinary pause of a human reply');a.reveal('human-cup',4);}
else{obj('study',608,382,[fill('M-338 32L-268 -135L9 -102L268 -137L338 32L0 83Z',blue,pale),fill('M-311 15L-256 -112L-10 -83V60Z','#ede3ce','#b7c7c6'),fill('M15 -84L256 -115L307 15L15 60Z','#e3d6bd','#c5d4d2'),text('Evidence',-149,-31,35),text('Possibility',154,-31,35),path('M-232 0H-69M-227 24H-83M61 0H227M77 23H216',blue,4)],'Two distinctions remain available for careful comparison');a.move('study',4,608,369);}

if(i<2){const id='desk';const q=a.objects.findIndex(o=>o.id===id);if(q>=0)a.objects.push(a.objects.splice(q,1)[0]);}
s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
