import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#666389',cn='#c7c2e5',o='#ac7b4f',on='#e8c28e';
const room=()=>obj('folded-room',604,343,[fill('M-360 138L-303 -107L-46 -160L26 -41L291 -120L365 138L40 187Z',c,cn),fill('M-311 107L-270 -75L-62 -115L-2 4L256 -78L306 113L41 150Z','#d8c7ae','#414958'),path('M-2 4V143',o,9)],'Two supported household possibilities occupy a folded space');
if(i===0||i===1){room();obj('sunday',420,349,[rect(-84,-60,168,116,o,on,11),n('ellipse',{cx:-27,cy:-10,rx:21,ry:29,fill:c}),n('ellipse',{cx:32,cy:-10,rx:21,ry:29,fill:c}),path('M-29 23L-60 54M33 23L61 54',c,15)],'A cherished family memory needs support to remain available');obj('other-possibility',763,346,[fill('M-51 83Q-67 10 -31 -12Q0 -28 29 -12Q68 10 48 83Z',o,on),dot(0,-42,32,c)],'Another valued possible continuity cannot simply coexist without cost');a.hide('sunday',3);if(i===1){a.move('other-possibility',5,607,365);}}
else if(i===2){obj('laundry',597,395,[fill('M-371 108V-118H-220V108Z',c,cn),n('ellipse',{cx:-296,cy:-26,rx:49,ry:74,fill:o}),rect(-169,5,505,23,o,on),path('M-130 28V137M287 28V137','$ink',13)],'A lower-world laundry exposes ordinary maintenance and bodily discomfort');a.person('visitor',755,281,{coat:c,night:cn,pose:'concerned',scale:.86});obj('shoes',864,486,[fill('M-55 -4Q-24 -25 -6 -2L19 14H-55Z',c,cn),fill('M24 -4Q49 -25 65 -2L94 14H24Z',c,cn)],'The novel makes reduced freedom tangible through an unfamiliar body');a.reveal('shoes',3);}
else{room();obj('casefile',604,372,[fill('M-128 -69H-23L-7 -48H136V100H-128Z',o,on),text('Aster',0,11,42),path('M-73 47H73',c,5)],'The reading begins in a case whose inhabitants dispute its administrative description');a.reveal('casefile',3);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
