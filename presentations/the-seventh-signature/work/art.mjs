import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);

const c='#555a80',cn='#bfc4e6',o='#a9794a',on='#e3be8b';
const lectern=()=>obj('lectern',403,373,[fill('M-156 -92L109 -119L162 -58L-123 -29Z',c,cn),fill('M-76 -31L86 -48V139H-76Z',o,on),rect(-137,144,283,17,c,cn),fill('M-113 -90L93 -109L118 -72L-90 -48Z','#e7dcc4','#cbd0c5'),text('Rights',6,43,45)],'A declaration remains publicly legible while operational dependence shifts');
if(i<2){lectern();obj('infrastructure',900,359,[rect(-141,-164,282,326,c,cn,5),...[-103,-35,33,101].map((y,j)=>[rect(-113,y-24,226,50,o,on,4),text(['Identity','Energy','Transport','Compute'][j],0,y+11,31)]).flat()],'The operational dependencies behind the declaration have their own controllers');obj('service-cable',646,445,[path('M-83 0H0V-167H91',c,10)],'The same right depends on a functioning path through infrastructure');a.reveal('service-cable',3);}
else if(i===2){obj('contract-table',600,434,[fill('M-398 -27H398L366 17H-364Z',c,cn),path('M-319 17V98M322 17V98','$ink',13)],'An institutional middle composed of negotiated contracts');obj('continuity-contract',611,333,[fill('M-224 -132L226 -111L211 94L-242 72Z','#e2d5bc','#b9c9c7'),text('Continuity contract',0,-62,40,'#263943'),path('M-169 -19H160M-173 17H178M-179 53H59',c,6)],'Formal ownership remains while conditions accumulate in an operational agreement');obj('condition',875,397,[fill('M-92 -81H90V64H-92Z',o,on),text('Exit',0,-20,35,'#263943'),text('conditions',0,23,31,'#263943')],'The reader must inspect operational exit rather than legal words alone');a.reveal('condition',4,200);}
else{lectern();a.person('reader',815,334,{coat:c,night:cn,pose:'concerned',scale:1});obj('appeal-step',629,503,[path('M-120 0H0V-54H99',o,17)],'A right requires a reachable way to challenge the operating system');a.reveal('appeal-step',3);}

s.visual=a.finish(s.lines[0]+' The scene stages a material relationship and its change, rather than a row of topical symbols.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
