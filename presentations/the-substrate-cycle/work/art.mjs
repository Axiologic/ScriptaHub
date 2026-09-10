import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#477681',cn='#aed4df',o='#af7849',on='#e8c18e';
const gate=()=>obj('waterfront',600,350,[fill('M-425 52Q-269 18 -109 50T205 52T425 52V194H-425Z',c,cn),rect(-86,-173,172,299,o,on),path('M-69 -160V118M-30 -160V118M12 -160V118M52 -160V118',c,8),fill('M-425 -41H-111V-10H-425ZM112 -41H425V-10H112Z',o,on)],'A flood gate joins collective decision to a physical waterfront');
if(i<2){gate();a.person('resident1',347,248,{coat:c,night:cn,pose:'concerned',scale:.62});a.person('resident2',832,248,{coat:o,night:on,pose:'open',scale:.62});obj('schedule',602,142,[text('08:40',0,0,43)],'A scheduled decision has an irreversible moment');a.reveal('schedule',3);obj('rising-water',605,476,[path('M-401 0Q-270 -21 -133 0T136 0T401 0',o,8)],'Costs arrive at particular places, not as an average experience');a.reveal('rising-water',4);}
else if(i===2){obj('inhabited-section',601,341,[fill('M-397 82L-190 -142L18 66L229 -151L396 87V133H-397Z',c,cn),rect(-397,138,794,49,o,on),rect(-397,196,794,22,c,cn),text('Rules of participation',0,173,34)],'The later story follows ownership into the substrate beneath inhabited reality');obj('revision',591,488,[fill('M-115 -15L-63 -57H116V48H-115Z','#d8c4a1','#445864'),path('M-73 -4H77M-73 22H39',c,5)],'The categories governing participation can themselves become contested');a.reveal('revision',4);}
else{gate();obj('observation-balcony',871,311,[rect(-116,112,232,22,o,on),path('M-89 134V204M89 134V204','$ink',12)],'The reader returns to the place where shared decisions land');a.person('resident',872,326,{coat:o,night:on,pose:'attentive',scale:.56});}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
