import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#685c8a',cn='#cbbde5',warm='#b57c47',wn='#e7bf85';
const seminar=()=>{obj('room',600,335,[fill('M-426 116Q0 270 426 116L389 -109Q0 -241 -389 -109Z',c,cn),fill('M-345 106Q0 213 345 106L323 -80Q0 -180 -323 -80Z','#dcd4c2','#38414f')],'A circular seminar makes participation a shared social space');for(let j=0;j<5;j++){a.person('student'+j,293+j*148,338+(j%2?24:0),{coat:j%2?c:warm,night:j%2?cn:wn,pose:j===2?'concerned':'attentive',scale:.43});}obj('table',600,432,[n('ellipse',{cx:0,cy:0,rx:324,ry:56,fill:c}),path('M-212 32V108M211 32V108','$ink',10)],'The seminar conversation has a physical center');};
if(i<2){seminar();obj('formulation',608,240,[rect(-169,-35,338,75,'#e7ddc7','#44455c',12),text('My considered answer',0,13,32)],'A suggested formulation appears accepted by its speaker');a.reveal('formulation',2);obj('revision',608,240,[rect(-194,-37,388,79,'#e7ddc7','#44455c',12),text('Who framed the options?',0,12,32)],'A participant makes the origin of agreement discussable');a.reveal('revision',4);a.hide('formulation',4);}
else if(i===2){obj('sleeping-city',594,344,[fill('M-414 152V-20H-340V-122H-251V-8H-156V-77H-66V-141H38V-42H132V-112H235V-19H315V-81H414V152Z',c,cn),...Array.from({length:12},(_,j)=>rect(-382+j*65,53,32,7,warm,wn,3))],'A coordinated city becomes quiet during its common sleep');obj('balcony',884,451,[rect(-90,0,180,17,warm,wn),path('M-71 17V80M73 17V80','$ink',9)],'A waking reserve remains physically outside the coordinated sleep');obj('witness',870,349,[rect(-30,55,104,12,warm,wn),path('M-20 67V123M65 67V123','$ink',8),fill('M-22 -14Q0 -29 23 -13L29 54H-24Z',warm,wn),dot(0,-44,23,warm),path('M-16 55L27 70L33 115M20 55L66 73L70 115',warm,13),path('M-17 1L-37 36L19 36',warm,10)],'A seated waking witness stays apart from the sleeping collective');a.reveal('witness',3);obj('sleepers',567,381,[-191,-46,96].flatMap(x=>[rect(x-42,-46,127,61,'#ded6c3','#3c4953',7),n('ellipse',{cx:x-17,cy:-20,rx:17,ry:15,fill:warm}),fill(`M${x+2} -30Q${x+50} -45 ${x+72} -8H${x+2}Z`,warm,wn)]),'Sleeping bodies make the shared quiet legible');}
else{seminar();a.hide('student2',2);obj('empty-seat',600,336,[rect(-27,8,54,55,warm,wn,9),path('M-23 64V118M23 64V118','$ink',8)],'An available place for independent disagreement');a.reveal('empty-seat',2);a.move('student2',5,600,323);a.reveal('student2',5);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
