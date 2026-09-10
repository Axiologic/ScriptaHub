import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#416879',cn='#b2d0df',o='#a77e49',on='#e4c58e';
const console=()=>obj('signal-console',600,354,[fill('M-348 -148H348L399 139H-398Z',c,cn),rect(-306,-109,612,192,'#d8cdb8','#344a58',7),path('M-355 112H355',o,15)],'An engineer compares a received signal with the public transmission');
if(i<2){console();obj('public-account',603,321,[path('M-261 22Q-226 -33 -192 22T-121 22T-51 22T19 22T90 22T162 22T234 22',o,8)],'The public account is coherent and reassuring');obj('authentic-signal',603,325,[path('M-262 17L-232 14L-229 -35L-221 53L-206 5L-145 13L-140 -19L-126 24L-89 21L-87 -45L-75 59L-66 19L-18 23L-9 -15L3 31L41 18L49 -39L63 58L76 18L139 23L145 -13L151 39L213 18L220 -30L232 27L264 22',c,6)],'The ragged authentic trace contradicts the maintained story');a.reveal('authentic-signal',3);a.hide('public-account',3);}
else if(i===2){obj('reservoir',610,366,[fill('M-387 -138H387V125L245 171H-253L-387 125Z',c,cn),fill('M-353 -109H350V103L225 139H-229L-353 103Z','#c5c7b4','#4d6b77'),path('M-331 -52H327',o,7),path('M-356 -121H350',o,14)],'A sealed reservoir has apparently exhaustive access, water and timing records');obj('body',603,414,[n('ellipse',{cx:-103,cy:-10,rx:27,ry:25,fill:c}),path('M-73 -3L15 10L93 -8M17 11L53 38L117 40M-37 1L-59 28L-94 23',c,23)],'The courier’s body is a concrete contradiction to the accounting');a.reveal('body',3);obj('depth',957,359,[text('0.90 m',0,0,32)],'The source’s shallow water makes the death a specific investigative problem');a.reveal('depth',4);}
else{console();a.person('investigator',367,399,{coat:o,night:on,pose:'concerned',scale:.64});obj('working-record',868,424,[fill('M-78 -87L88 -66L66 86L-99 63Z',o,on),path('M-55 -39L53 -26M-60 -7L40 5M-65 24L29 36',c,5)],'The reading follows the work of comparing evidence across powers');a.reveal('working-record',3);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
