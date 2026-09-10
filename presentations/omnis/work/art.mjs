import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#355d7d',cn='#a9cce5',g='#987544',gn='#ddc48e';
const lab=()=>{obj('bench',614,459,[fill('M-378 -24H378V12H-378Z',c,cn),path('M-304 12V90M306 12V90','$ink',12)],'A laboratory exchange gives the metaphysical story a practical beginning');obj('colony',698,332,[n('ellipse',{cx:0,cy:0,rx:162,ry:106,fill:g}),...Array.from({length:13},(_,j)=>dot(Math.sin(j*2.1)*112,Math.cos(j*1.7)*67,8,c))],'A coordinated colony responds within an experimental setup');a.person('albert',343,305,{coat:c,night:cn,pose:'concerned',scale:.88});};
if(i<2){lab();obj('timing',961,308,[rect(-45,-89,90,177,c,cn,14),...[-45,0,45].map(y=>rect(-23,y,46,13,g,gn,4))],'The response changes in relation to the investigator’s timing');a.reveal('timing',3);a.move('colony',4,714,330);}
else if(i===2){obj('realm-section',603,331,[fill('M-398 114L-273 -91H279L398 114V160H-398Z',c,cn),fill('M-267 -69L-348 90H348L270 -69Z','#d4c9ae','#41505c'),path('M-249 114V-30M-96 114V-30M97 114V-30M249 114V-30',g,22)],'An apparently extraordinary realm has maintained supports and allocated capacity');obj('allocation',602,366,[rect(-137,-81,274,116,g,gn,8),text('Continuity support',0,-10,34)],'Support must be assigned to lives rather than assumed limitless');a.reveal('allocation',3);}
else{obj('arrival',603,335,[fill('M-423 162L-255 -140H255L423 162H363L216 -102H-216L-362 162Z',c,cn),fill('M-182 161V-92H182V161H151V-64H-150V161Z',g,gn)],'An arrival corridor turns an observer into a person whose continuity is questioned');a.person('albert',605,377,{coat:c,night:cn,pose:'attentive',scale:.65});a.move('albert',4,605,354);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
