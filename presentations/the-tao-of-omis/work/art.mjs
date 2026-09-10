import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#526c91',cn='#b4ccea',o='#a56d4c',on='#e4b895';
const dusk=()=>obj('dusk-belt',602,370,[fill('M-424 95Q-257 -17 -59 83Q114 -1 424 87V176H-424Z',c,cn),n('ellipse',{cx:268,cy:-124,rx:88,ry:88,fill:o}),path('M-401 121Q-211 61 -66 112T245 92T401 113','#ccb58e',14)],'A habitable belt connects ecological dependence and finite lives');
const boat=(id,x,y)=>obj(id,x,y,[fill('M-99 -6H99L63 42H-61Z',o,on),path('M-24 -8V-81',c,8),fill('M-18 -74L45 -11H-18Z',c,cn)],'A practical rescue boat inhabits the current instead of symbolizing abstract harmony');
if(i<2){dusk();boat('rescue-boat',552,404);obj('memory-reeds',320,362,[...[-52,-22,11,43,67].map((x,j)=>path(`M${x} 108Q${x-35} ${-14-j*8} ${x+11} ${-90+j*14}`,o,7))],'Memory reeds and transport keep the relationship in a material ecology');a.move('rescue-boat',4,643,417);}
else if(i===2){obj('observer-aperture',395,332,[n('ellipse',{cx:0,cy:0,rx:176,ry:170,fill:c}),n('ellipse',{cx:0,cy:0,rx:121,ry:116,fill:o}),path('M-171 1H-120M121 1H173M0 -169V-119M0 119V170','$ink',8)],'Higher observational resolution does not capture a person’s possible futures');obj('unclaimed-path',806,362,[path('M-205 156Q-81 87 -18 19Q15 -20 150 -129',o,22),path('M-12 20Q72 49 177 104',c,22)],'The person’s future remains branching beyond the instrument’s view');a.person('finite-person',779,390,{coat:c,night:cn,pose:'open',scale:.65});a.reveal('unclaimed-path',3);}
else{dusk();boat('first-boat',417,410);boat('second-boat',796,423);a.move('first-boat',4,480,400);a.move('second-boat',4,735,434);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
