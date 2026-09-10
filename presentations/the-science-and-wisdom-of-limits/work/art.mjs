import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#4e7867',cn='#b5d6bb',o='#a57c4c',on='#e1c38d';
const greenhouse=()=>obj('greenhouse',601,340,[fill('M-411 149V-108L0 -184L411 -108V149H386V-86L0 -157L-386 -86V149Z',c,cn),path('M-249 -127V139M-86 -157V139M88 -157V139M252 -127V139',c,6),fill('M-361 103H362V138H-361Z',o,on),...[-284,-164,-42,80,201,301].map((x,j)=>[path(`M${x} 97V12M${x} 56L${x-20} 32M${x} 36L${x+20} 17`,c,8),dot(x-23,34,13,o),dot(x+17,16,12,o)]).flat()],'Greenhouse irrigation is a visible system a child can inspect');
if(i<2){greenhouse();a.person('grandparent',344,371,{coat:o,night:on,pose:'open',scale:.67});a.person('matei',826,418,{coat:c,night:cn,pose:'attentive',scale:.47});obj('assignment',759,432,[fill('M-54 -45L41 -54L59 36L-40 48Z','#eee0c7','#cbd2c1'),path('M-32 -16H27M-27 5H18',c,4)],'The school assignment asks when a principle should be abandoned');a.reveal('assignment',3);}
else if(i===2){obj('inspectable-section',603,345,[fill('M-419 146V-84H-327V-131H-225V-56H-112V-98H-17V-151H94V-61H221V-117H317V-41H419V146Z',c,cn),rect(-419,155,838,32,o,on),path('M-337 137V85H-170V127H-5V51H173V111H341',o,11)],'The city has dependencies whose seams and switches can be inspected');obj('switch',625,444,[rect(-45,-35,90,75,'#e4d7bb','#394f52',7),path('M0 22L21 -16',c,11)],'A reachable point of correction exists within the larger system');a.reveal('switch',3);a.person('maintainer',838,397,{coat:o,night:on,pose:'open',scale:.63});}
else{greenhouse();obj('school-sheet',607,350,[rect(-153,-96,306,195,'#e8dec6','#becdbe',8),text('When would I',0,-31,35),text('change my mind?',0,16,35),path('M-94 55H94',c,5)],'The assignment’s condition for revision remains the reading standard');a.reveal('school-sheet',3);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
