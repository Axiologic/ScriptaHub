import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#355d7d',cn='#a9cce5',g='#987544',gn='#ddc48e';
const seated=(id,x,y,coat,night)=>obj(id,x,y,[rect(-44,72,105,12,'#987c55','#d8c196'),path('M-35 84V144M53 84V144','$ink',9),fill('M-37 -28Q0 -45 35 -25L40 72H-38Z',coat,night),n('ellipse',{cx:0,cy:-76,rx:31,ry:38,fill:'#bd896c'}),fill('M-32 -85Q-41 -130 1 -119Q40 -125 32 -83L18 -99L-25 -98Z','#393333'),path('M-16 -80H-7M8 -80H17M-10 -52Q0 -47 12 -54','#241e1b',3),path('M-31 -10Q-51 41 39 42M32 -7L59 26L98 21',coat,14),path('M-22 73L36 85L46 135M25 73L83 85L91 135',coat,18),path('M43 135H65M90 135H114','$ink',10)],'A seated person works at the surface with feet below it');
const lab=()=>{obj('bench',614,459,[fill('M-378 -24H378V12H-378Z',c,cn),path('M-304 12V90M306 12V90','$ink',12)],'A laboratory exchange gives the metaphysical story a practical beginning');obj('colony',698,332,[n('ellipse',{cx:0,cy:0,rx:162,ry:106,fill:g}),...Array.from({length:13},(_,j)=>dot(Math.sin(j*2.1)*112,Math.cos(j*1.7)*67,8,c))],'A coordinated colony responds within an experimental setup');seated('albert',329,415,c,cn);};
if(i<2){lab();obj('timing',961,308,[rect(-45,-89,90,177,c,cn,14),...[-45,0,45].map(y=>rect(-23,y,46,13,g,gn,4))],'The response changes in relation to the investigator’s timing');a.reveal('timing',3);a.move('colony',4,714,330);}
else if(i===2){obj('realm-section',662,336,[fill('M-254 140V-36Q-254 -171 0 -177Q254 -171 254 -36V140Z',c,cn),fill('M-227 113V-31Q-223 -142 0 -151Q223 -142 227 -31V113Z','#d4c9ae','#41505c'),rect(-255,139,510,29,g,gn)],'A supported realm is an inhabited structure with maintained supply');a.person('continuing-person',704,330,{coat:g,night:gn,pose:'attentive',scale:.77});obj('pump',305,401,[rect(-73,-44,146,104,g,gn,14),n('ellipse',{cx:0,cy:0,rx:34,ry:34,fill:c}),path('M-16 0H16M0 -16V16',g,7),path('M74 12H113V61H296',g,15)],'A visible maintained supply supports an actual continuing person');a.person('maintainer',244,362,{coat:c,night:cn,pose:'open',scale:.6});a.reveal('pump',3);a.reveal('maintainer',3);}

else{obj('arrival',603,335,[fill('M-423 162L-255 -140H255L423 162H363L216 -102H-216L-362 162Z',c,cn),fill('M-182 161V-92H182V161H151V-64H-150V161Z',g,gn)],'An arrival corridor turns an observer into a person whose continuity is questioned');a.person('albert',605,377,{coat:c,night:cn,pose:'attentive',scale:.65});a.move('albert',4,605,354);}

if(i<2){const id='bench';const q=a.objects.findIndex(o=>o.id===id);if(q>=0)a.objects.push(a.objects.splice(q,1)[0]);}
s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
