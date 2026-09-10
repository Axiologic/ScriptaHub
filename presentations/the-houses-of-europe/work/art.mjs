import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#4d6977',cn='#b7d1de',o='#9b5944',on='#e3ad96';
const valley=()=>obj('valley',597,342,[fill('M-439 129L-307 -140L-172 69L-27 -81L124 109L302 -158L437 135V193H-439Z',c,cn),fill('M-424 150Q-165 95 17 152T419 152V205H-424Z','#b8aa85','#697569')],'A mountain clinic belongs to a vulnerable valley community');
const clinic=()=>obj('clinic',388,374,[fill('M-125 -36L0 -128L125 -36V117H-125Z',o,on),rect(-93,-4,49,65,'#e5d6b8','#384b55'),rect(45,-4,49,65,'#e5d6b8','#384b55'),rect(-23,28,46,89,c,cn),path('M-20 -46H20M0 -67V-26','#e5d6b8',9)],'Patients remain inside an ordinary local clinic');
const machine=()=>obj('reclaimer',852,354,[fill('M-91 -49Q0 -119 91 -49L66 28H-66Z',c,cn),path('M-74 -9L-134 49L-147 101M-50 15L-96 85L-98 115M-30 26L-42 107M74 -9L134 49L147 101M50 15L96 85L98 115M30 26L42 107',c,12),rect(-24,-49,48,12,o,on,5)],'A six-legged reclamation machine waits under a running operational deadline');
if(i<2){valley();clinic();machine();a.person('mayor',608,395,{coat:o,night:on,pose:'open',scale:.59});obj('appeal',633,383,[rect(-18,-30,47,62,'#e7dec9','#d7d2bd'),path('M-9 -9H17M-9 4H12',c,3)],'A pending paper appeal cannot itself pause the machine');a.reveal('appeal',3);obj('clock',834,215,[text('17:00',0,0,42)],'The source’s seventeen-minute reclamation deadline');a.reveal('clock',4);}
else if(i===2){obj('cooling-section',608,330,[fill('M-418 176L-335 -109L-112 -184L83 -132L303 -181L418 177Z',c,cn),rect(-318,-87,636,253,'#d4c7ac','#394a53'),...[-219,-71,76,221].map(x=>rect(x-38,-59,76,176,o,on,16)),path('M-266 151H267M-266 -92V151M267 -92V151',o,15)],'Shared cooling infrastructure serves hospitals and coercive systems together');obj('service-label',605,467,[text('Shared cooling',0,19,36)],'Maintenance is an intertwined responsibility, not a morally separate abstraction');a.reveal('service-label',3);}
else{valley();clinic();a.person('mayor',690,372,{coat:o,night:on,pose:'attentive',scale:.85});obj('appeal',732,382,[rect(-28,-55,65,93,'#e7dec9','#d7d2bd'),path('M-13 -29H25M-13 -10H16M-13 9H22',c,4)],'Return to the person who must make an appeal effective');a.reveal('appeal',3);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
