import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#6c6781',cn='#c8c1dc',o='#ac774d',on='#e8bf94';
const station=()=>obj('station',599,341,[fill('M-428 144V-151H427V144Z',c,cn),rect(-384,-109,244,205,'#ded3bc','#40505c',16),rect(-92,-109,244,205,'#ded3bc','#40505c',16),rect(201,-109,188,205,o,on,7),path('M-428 161H427',o,18)],'The commuter’s ordinary platform precedes the changed fortune');
if(i<2){station();a.person('commuter',840,319,{coat:c,night:cn,pose:'concerned',scale:.69});obj('fallen-person',395,463,[n('ellipse',{cx:-84,cy:-8,rx:25,ry:25,fill:o}),path('M-56 -1L18 16L82 -1M11 13L35 55L98 61M-36 2L-43 36L-102 27',o,20)],'An encounter that cannot be reduced to the mechanics of a wish');obj('door-leaf',832,335,[rect(-91,-105,183,207,o,on,6)],'The train door closes while an ordinary ethical decision remains');a.reveal('door-leaf',4);if(i===1)a.hide('door-leaf',6);}
else if(i===2){obj('conference',397,356,[fill('M-162 149V-143H153V149Z',c,cn),fill('M-109 121L-42 -23L100 11V122Z',o,on),text('Conference',0,-87,32)],'Maya’s professional recognition occupies a different social setting');obj('tram',865,355,[rect(-149,-138,298,287,o,on,30),rect(-114,-103,224,176,'#ded3bd','#40505c',12),path('M-99 98H99',c,14)],'Daniel’s ordinary day places altered possibility in another life');a.person('maya',394,349,{coat:o,night:on,hairStyle:'long',pose:'attentive',scale:.61});a.person('daniel',865,351,{coat:c,night:cn,pose:'concerned',scale:.58});a.reveal('tram',3);a.reveal('daniel',3);}
else{station();obj('open-door',835,341,[rect(-69,-111,138,228,'#eee1c8','#30444e',5)],'Return to the ordinary choice that gives later possibility its meaning');a.person('reader',589,382,{coat:o,night:on,pose:'attentive',scale:.74});a.move('reader',4,540,389);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
