import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const ink='#725176',light='#d6b8d9',amber='#ad7c2e',amberN='#eacf90';
for(const [index,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
const material=(d,c=ink,cn=light)=>tint(n('path',{d,fill:c}),cn);
const type=(id,value,x,y,size=42)=>a.label(id,value,x,y,size);

const sheet=(id,x,y,k=1)=>shape(id,x,y,[material('M-98 -134H62L98 -98V134H-98Z'),...[-71,-28,15,58].map((y,i)=>tint(path(`M-62 ${y}H${i===3?11:62}`,amber,10),amberN))],'A written argument as an artifact for inspection',k);
const lens=(id,x,y,k=1)=>shape(id,x,y,[tint(n('circle',{cx:-11,cy:-18,r:77,fill:'none',stroke:amber,'stroke-width':18}),amberN),tint(path('M46 39L104 97',amber,24),amberN)],'A lens of interpretation, not a claim of empirical validation',k);
const seat=(id,x,y,k=1)=>shape(id,x,y,[material('M-65 -104H65V30H-65Z'),path('M-76 48H76M-55 48V125M55 48V125','$ink',10)],'An empty witness chair',k);
switch(index){
case 0:for(const [i,v]of ['Forgiveness','Witnesses','Meaning','Justice'].entries()){const x=305+i%2*562,y=239+Math.floor(i/2)*170;shape('argument'+i,x,y,[material('M-205 -58H205V58H-205Z',i%2?amber:ink,i%2?amberN:light),tint(text(v,0,14,43,i%2?'#302236':'#fff'),'#302236')],'One of the four connected philosophical experiments');if(i)a.reveal('argument'+i,i+2);}shape('qualification',595,324,[material('M-206 -28H206V28H-206Z','#d3c1b0','#5e535f'),text('Insight ≠ evidence',0,12,34,'#302236')],'Restoring the preface’s qualification interrupts confident generalization');a.reveal('qualification',6);break;
case 1:for(let i=0;i<4;i++){sheet('draft'+i,252+i*230,323,.58);if(i)a.reveal('draft'+i,2+i);}break;
case 2:seat('waiting',430,322,1.15);a.person('waiting-person',430,310,{coat:amber,night:amberN,pose:'concerned',scale:.65});a.move('waiting-person',5,631,354,3200);shape('door',860,329,[material('M-91 -136H91V136H-91Z',amber,amberN),material('M-57 -104H55V136H-57Z')],'A boundary can remain while the argument examines release');a.reveal('door',4);break;
case 3:a.person('self',673,330,{coat:ink,night:light,pose:'concerned',scale:.91});shape('gaze',274,314,[tint(path('M-74 0Q0 -73 74 0Q0 73 -74 0Z',amber,10),amberN),dot(0,0,20,'$ink')],'The witness whose interpretation matters');a.reveal('gaze',3);break;
case 4:shape('jurisdiction',425,333,[tint(n('circle',{cx:0,cy:0,r:118,fill:'none',stroke:ink,'stroke-width':14}),light),material('M-54 60V-48L0 -82L54 -48V60Z',amber,amberN)],'An interpretation can claim jurisdiction over ordinary life');sheet('meaning',882,334,.78);a.reveal('meaning',3);break;
case 5:a.person('appellant',370,286,{coat:amber,night:amberN,pose:'open',scale:.52});a.move('appellant',4,590,210,3100);shape('appeal',600,330,[material('M-204 113H-90V46H14V-20H118V-86H222V113Z'),tint(path('M-193 73L-140 73M-85 9L-35 9M23 -56H76',amber,12),amberN)],'An appeal permits another level to revise a judgment');break;
case 6:sheet('claim',346,329,.9);lens('evidence',855,328,1.1);a.reveal('evidence',3);type('unverified','Unverified',849,515,42);a.reveal('unverified',5);break;
case 7:shape('page',597,315,[material('M-297 -128H297V155H-297Z'),tint(text('A proposed lens',0,-56,48,'#fff'),'#251b2d'),tint(text('Scope • exceptions • evidence',0,18,33,'#fff'),'#251b2d'),tint(path('M-221 57H221',amber,8),amberN),tint(text('Keep the qualification attached',0,108,32,'#fff'),'#251b2d')],'Reading the claim with the preface’s limits keeps persuasion accountable');break;
}

s.visual=a.finish('Plum and amber editorial laboratory; written arguments, inspection lenses and distinct conceptual instruments without invented brain scans.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
