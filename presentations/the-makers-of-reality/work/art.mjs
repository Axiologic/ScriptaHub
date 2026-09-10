import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#487980',cn='#aed7da',o='#b27d44',on='#e8c38d';
const shipment=()=>obj('shipment',600,383,[fill('M-147 -102L64 -133L165 -70V75L-45 111L-147 49Z',o,on),path('M-147 -102L-45 -40L165 -70M-45 -40V111',c,7),rect(-2,-77,95,51,'#e8dec6','#405962',3),text('Filters',44,-42,28),path('M-205 133H205',c,12)],'Urgently needed filters remain physically motionless');
if(i<2){shipment();obj('instruction-left',307,263,[path('M-50 0H65M65 0L39 -25M65 0L39 25',c,12),text('Valid',0,-38,34)],'One valid instruction directs movement');obj('instruction-right',895,263,[path('M50 0H-65M-65 0L-39 -25M-65 0L-39 25',c,12),text('Valid',0,-38,34)],'An incompatible valid instruction prevents the same movement');a.reveal('instruction-right',3);obj('waiting',600,557,[text('Still waiting',0,0,34)],'The drone complies by doing nothing');a.reveal('waiting',4,200);}
else if(i===2){obj('workshop',611,386,[fill('M-400 -128H-99V91H-400Z',c,cn),...[-83,-23,37].map(y=>rect(-374,y,245,12,o,on)),rect(-371,-116,75,27,o,on,8),rect(-268,-53,101,27,o,on,8),rect(-376,8,115,27,o,on,8),fill('M-29 56H387V88H-29Z',o,on),path('M1 88V158M345 88V158','$ink',13)],'A goods workshop provides access without eliminating the burdens behind it');a.person('allocator',766,375,{coat:c,night:cn,pose:'open',scale:.85});obj('burden',1038,288,[text('Water',0,-33,33),text('Time',0,16,33),text('Care',0,65,33)],'The allocation view uses consequences in place of a price');a.reveal('burden',3);}
else{obj('care-room',603,378,[fill('M-362 92H-69V-29H-342Z',o,on),rect(-354,-48,91,40,'#ded5c1','#485e64',15),path('M-328 91V159M-104 91V159','$ink',12)],'The New House reveals human attention that material supply does not replace');a.person('resident',384,336,{coat:c,night:cn,pose:'attentive',scale:.64});a.person('carer',711,326,{coat:o,night:on,pose:'open',scale:.89});a.move('carer',4,661,326);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
