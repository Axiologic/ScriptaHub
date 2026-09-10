import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#73569c',cn='#c8b5e8',r='#a56952',rn='#e0b59a';
const nest=()=>obj('nest',590,330,[fill('M-292 55L-188 -133L-11 -47L146 -150L290 34L181 167L-14 95L-175 170Z',c,cn),fill('M-218 36L-151 -76L-15 -14L120 -82L212 31L144 106L-11 54L-137 109Z','#ccb995','#423850'),fill('M-62 14L-13 -80L63 -1L97 69L-3 103L-76 63Z',r,rn),path('M-18 -7L10 4M-20 25Q0 17 21 30','$ink',5)],'A vulnerable dimensional child is held by a failing folded support nest');
if(i===0||i===1){nest();obj('failing-support',583,483,[path('M-144 25L-103 -3L-50 18L-9 -24L39 10L104 -15L150 23',r,13)],'The support has gaps rather than functioning as limitless power');a.reveal('failing-support',3);if(i===1){a.move('nest',4,590,350);}}
else if(i===2){obj('clinic',600,338,[rect(-341,-159,373,294,c,cn,3),rect(-316,-134,146,244,'#d9d7ce','#3e5262'),rect(-145,-134,153,244,'#d0ccc4','#435265'),path('M-327 151H320M78 140V193M281 140V193',r,16)],'An ordinary clinic window makes contradictory perception concrete');obj('rain',440,316,Array.from({length:7},(_,j)=>path(`M${-118+j*38} -85l-12 32`,r,4)),'Rain falls outside the window');obj('reflection',440,416,Array.from({length:7},(_,j)=>path(`M${-118+j*38} 25l12 -32`,c,4)),'The reflected movement contradicts the weather');a.reveal('reflection',3);a.person('mara',843,328,{coat:r,night:rn,hairStyle:'long',pose:'concerned',scale:.83});}
else{nest();obj('human-window',951,336,[rect(-59,-103,118,216,r,rn),rect(-45,-88,90,184,'#d6cfbe','#46505f'),path('M-42 30H41',c,6)],'The human account remains a distinct vantage on the same dependence');a.reveal('human-window',3);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
