import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#704d57',cn='#d8b3bd',b='#57787d',bn='#b4d5d6';
const report=(id,x,y,response)=>obj(id,x,y,[rect(-157,-119,314,240,'#e5dcc9','#394c52',6),path('M-121 -58H116M-121 -30H100',b,5),path('M-119 47L-87 47L-70 10L-44 86L-16 20L4 47H117',c,7),...(response?[rect(-157,113,314,26,c,cn)]:[])],'Comparable suffering enters a different institutional response');
if(i<2){report('urgent',374,337,true);report('remote',826,337,false);obj('care-response',376,490,[path('M-60 0H60M0 -24V24',b,17),text('Immediate response',0,72,32)],'One report activates care');a.reveal('care-response',3);obj('unanswered',826,500,[text('No equivalent response',0,8,31)],'The comparison concerns unequal response, not opposition to reducing pain');a.reveal('unanswered',4);}
else if(i===2){obj('tribunal',598,375,[fill('M-348 -43L0 -125L348 -43V88H-348Z',c,cn),rect(-302,-21,604,79,b,bn),path('M-285 90V171M285 90V171','$ink',16)],'The machine’s judging position is itself subject to challenge');obj('assessor',601,237,[n('ellipse',{cx:0,cy:0,rx:104,ry:61,fill:b}),path('M-63 0H63M-39 -22V23M0 -22V23M39 -22V23',c,7)],'An invented assessor, not a depiction of an authoritative real system');a.person('witness',320,417,{coat:b,night:bn,pose:'open',scale:.62});a.reveal('witness',4);a.move('assessor',5,784,279);}
else{report('first',405,330,true);report('second',805,330,false);obj('comparison',604,505,[path('M-98 0H98M-98 0L-74 -19M-98 0L-74 19M98 0L74 -19M98 0L74 19',b,8)],'The reading compares premises and the limits of enforcement');a.reveal('comparison',3);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
