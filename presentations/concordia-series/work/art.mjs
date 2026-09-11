import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#685c8a',cn='#cbbde5',warm='#b57c47',wn='#e7bf85';
const seminar=(count=5)=>{obj('room',600,335,[fill('M-426 116Q0 270 426 116L389 -109Q0 -241 -389 -109Z',c,cn),fill('M-345 106Q0 213 345 106L323 -80Q0 -180 -323 -80Z','#dcd4c2','#38414f')],'A circular seminar makes participation a shared social space');for(let j=0;j<count;j++){a.person('student'+j,293+j*148,338+(j%2?24:0),{coat:j%2?c:warm,night:j%2?cn:wn,pose:j===2?'concerned':'attentive',scale:.43});}obj('table',600,432,[n('ellipse',{cx:0,cy:0,rx:324,ry:56,fill:c}),path('M-212 32V108M211 32V108','$ink',10)],'The seminar conversation has a physical center');};
if(i<2){seminar(2);a.reveal('room',1);a.reveal('student0',1);a.reveal('student1',1);a.reveal('table',1);
 const first=i===0;
 obj('formulation',608,240,[rect(-169,-35,338,75,'#e7ddc7','#44455c',12),text(first?'CARE RECEIVED':'HELPFUL ROUTE',0,13,32)],first?'Effective care is materially present before refusal becomes easy':'Assistance reaches medicine, learning and daily survival');
 a.reveal('formulation',2);
 obj('revision',608,240,[rect(-194,-37,388,79,'#e7ddc7','#44455c',12),text(first?'REFUSE CARE?':'CHOICE COST',0,12,32)],first?'The opt-out question remains visible beside a real benefit':'A person can consider refusal while the benefit remains visible');
 a.reveal('revision',2);a.hide('formulation',2);
}
else if(i===2){
 obj('assisted-classroom',600,420,[rect(-380,-60,760,18,'#685c8a','#cbbde5',9),path('M-286 -42V44M0 -42V44M286 -42V44','$ink',8)],'An ordinary classroom carries the shared assistance');
 a.person('assisted-student',330,390,{coat:c,night:cn,pose:'attentive',scale:.62});
 a.person('manual-student',870,390,{coat:warm,night:wn,pose:'concerned',scale:.62});
 obj('assisted-sentence',330,210,[rect(-180,-36,360,72,'#e7ddc7','#44455c',10),text('smoother wording',0,10,27)],'Assisted students receive a smoother sentence');
 obj('manual-sentence',870,210,[rect(-180,-36,360,72,'#f0d4b6','#8a5638',10),text('I will think it through.',0,10,25)],'One classmate works through an unassisted sentence');
 obj('wording-gap',600,210,[path('M-50 0H50M30 -16L50 0L30 16','#b57c47',7)],'The difference in wording keeps disagreement possible');
 a.reveal('assisted-classroom',1);a.reveal('assisted-student',1);a.reveal('manual-student',1);a.reveal('assisted-sentence',1);a.reveal('manual-sentence',1);a.reveal('wording-gap',2);
}
else{seminar(2);a.reveal('room',1);a.reveal('student0',1);a.reveal('student1',1);a.reveal('table',1);obj('empty-seat',600,336,[rect(-27,8,54,55,warm,wn,9),path('M-23 64V118M23 64V118','$ink',8)],'An available place for independent disagreement');a.reveal('empty-seat',2);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
