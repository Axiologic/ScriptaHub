import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#875a7e',cn='#d8b7d3',g='#50756b',gn='#b3d0bb';
const world=()=>obj('inhabited-world',610,367,[fill('M-398 122Q-268 -70 -89 21Q112 -138 393 106L393 151H-398Z',g,gn),fill('M-158 46L-101 -35L-32 45V123H-158Z',c,cn),rect(-95,65,34,58,'#ead9c2','#354246'),path('M-385 130Q-67 200 63 82Q138 30 367 136','#d1ae74',19)],'A world includes a home and a route whose users have their own purposes');
if(i===0){world();obj('threshold',611,285,[fill('M-285 140V-162H284V140H250V-131H-251V140Z',c,cn),text('Memorial',0,-82,38)],'The novel enters its atlas through literary inheritance');a.person('resident',521,376,{coat:c,night:cn,pose:'open',scale:.53});a.move('resident',4,643,400);}
else if(i===1){obj('gravity',582,355,[fill('M-385 117Q0 40 385 117L385 151H-385Z',g,gn),...[-180,-75,36,152].map((x,j)=>n('ellipse',{cx:x,cy:70-j*29,rx:32,ry:25,fill:c}))],'A changed physical operation changes how bodies can use a landscape');obj('crossing',825,357,[fill('M-26 65Q-70 7 -10 -90Q31 -133 56 -104Q-21 -6 15 65Z',c,cn)],'One altered rule changes a practical route');a.reveal('crossing',3);}
else if(i===2){world();a.person('visitor',871,319,{coat:c,night:cn,pose:'concerned',scale:.76});a.person('resident',440,378,{coat:g,night:gn,pose:'open',scale:.61});obj('classification',740,319,[rect(-90,-115,180,196,'#ddc8ad','#495457',8),text('Observed',0,-57,32),text('operation',0,-20,32),path('M-57 12H55M-57 37H39',c,5)],'A useful field description is visibly smaller than the lived place');a.hide('classification',4);a.move('resident',5,558,400);}
else{world();obj('open-gate',334,320,[fill('M-64 131V-137H63V131H39V-108H-40V131Z',c,cn),path('M-42 -101L17 -54V136',c,12)],'The entrance remains open to experience beyond the atlas');a.person('reader',761,375,{coat:c,night:cn,pose:'attentive',scale:.63});a.move('reader',4,636,387);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
