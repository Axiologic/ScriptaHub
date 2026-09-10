import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const blue='#456779',pale='#b9d8e6',terra='#a65540',tn='#e9aa95';
const desk=()=>obj('desk',600,442,[fill('M-375 -10H375L343 24H-343Z',blue,pale),path('M-320 24V106M300 24V106','$ink',13)],'A shared workplace ties output to responsibility');
const pages=(id,x,y,count)=>obj(id,x,y,Array.from({length:count},(_,j)=>[rect(j*7,-j*9,116,74,'#f0e9d9','#d5d6cc',4),path(`M${18+j*7} ${22-j*9}h70M${18+j*7} ${40-j*9}h47`,blue,4)]).flat(),'Competent outputs multiply without increasing recognition automatically');
if(i===0||i===1){desk();a.person('worker',382,302,{coat:terra,night:tn,pose:'concerned',scale:.86});pages('first-output',537,362,1);pages('more-output',759,316,6);a.reveal('more-output',3);obj('verification',684,376,[path('M-23 0L-4 19L30 -23',blue,9)],'A deliberate check rather than another generated output');a.reveal('verification',5);if(i===1){a.hide('more-output',5);a.move('worker',4,418,302);}}
else if(i===2){obj('conversation-table',612,427,[fill('M-230 -8Q0 -51 230 -8L195 26H-193Z',terra,tn),path('M-165 26V108M165 26V108','$ink',12)],'A human conversation has limited attention and material time');a.person('person',367,319,{coat:blue,night:pale,pose:'attentive',scale:.86});obj('terminal',855,318,[rect(-65,-113,130,209,blue,pale,28),rect(-48,-88,96,150,'#f0e9d9','#293b43',10),path('M-22 -37Q0 -50 25 -36M-22 -12Q0 -25 25 -11M-22 13Q0 0 25 14',terra,7)],'Fast responsive display represents social timing, not proof of felt emotion');a.reveal('terminal',2);obj('human-cup',491,390,[fill('M-24 -14H24L18 21H-18Z',blue,pale),path('M24 -5Q43 -7 36 12H22',blue,5)],'The ordinary pause of a human reply');a.reveal('human-cup',4);}
else{obj('study',608,382,[fill('M-338 32L-268 -135L9 -102L268 -137L338 32L0 83Z',blue,pale),fill('M-311 15L-256 -112L-10 -83V60Z','#ede3ce','#b7c7c6'),fill('M15 -84L256 -115L307 15L15 60Z','#e3d6bd','#c5d4d2'),text('Evidence',-149,-31,35),text('Possibility',154,-31,35),path('M-232 0H-69M-227 24H-83M61 0H227M77 23H216',blue,4)],'Two distinctions remain available for careful comparison');a.move('study',4,608,369);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
