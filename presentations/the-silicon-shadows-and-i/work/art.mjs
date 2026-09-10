import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const ink='#356587',light='#9ac4e3',coral='#a75a4a',coralN='#e7afa1';
for(const [index,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
const material=(d,c=ink,cn=light)=>tint(n('path',{d,fill:c}),cn);
const type=(id,value,x,y,size=42)=>a.label(id,value,x,y,size);

const cup=(id,x,y,k=1)=>shape(id,x,y,[material('M-72 -71H66L55 63Q0 91 -59 62Z',coral,coralN),tint(path('M66 -48Q139 -47 118 8Q100 45 59 33',coral,12),coralN),path('M-8 -69L7 -29L-12 1L9 31L1 65','$ink',5)],'The narrator’s cracked cup',k);
const robot=(id,x,y,k=1)=>shape(id,x,y,[material('M-41 -84Q0 -100 41 -84V91H-41Z'),path('M-41 -27Q-96 -4 -94 56M41 -27Q79 12 106 -15','$ink',12),tint(dot(-31,110,18,coral),coralN),tint(dot(31,110,18,coral),coralN)],'Miro: faceless central column, two arms and retractable wheels',k);
const boat=(id,x,y,k=1)=>shape(id,x,y,[material('M-170 23H170L125 94H-125Z'),material('M-91 23V-56H69V23Z',coral,coralN),path('M-65 -34H36','$ink',7)],'A vessel on the managed sea',k);
const coast=(id,x,y,k=1)=>shape(id,x,y,[material('M-178 113L-119 62V-20H-49V-79H21V-126H91V113Z',coral,coralN),material('M91 -25H159V113H91Z'),path('M-189 137Q-63 161 81 137T204 137','$ink',5)],'Terraced coastal settlement and its maintained shoreline',k);
switch(index){
case 0:shape('sea',792,334,[material('M-331 -2H331V53L-331 25Z','#afc5c8','#354655')],'A continuous sea horizon locates the distant maintained coast');coast('distant',993,233,.48);shape('terrace',589,494,[material('M-435 -17H435L480 16H-478Z',coral,coralN)],'The foreground terrace contains both the table and Miro');shape('table',363,407,[material('M-128 -8H128V9H-128Z'),path('M-94 9V87M94 9V87','$ink',10)],'The cup is on the table; the robot remains beside it');cup('cup',345,365,.53);robot('miro',684,377,.84);a.move('miro',4,640,377,2200);shape('drone',951,164,[material('M-45 -4L-8 -16L0 -37L8 -16L45 -4L8 8L0 28L-8 8Z')],'The arriving courier changes the scale of domestic consent');a.reveal('drone',5);a.move('drone',6,904,219,2500);break;
case 1:cup('fissure',419,371,1.15);a.person('narrator',216,326,{coat:coral,night:coralN,hairStyle:'long',pose:'concerned',scale:.68});robot('permission',883,332,.86);a.move('permission',4,913,332);break;
case 2:coast('port',599,320,1.3);shape('drone',956,190,[material('M-69 -7L-10 -22L0 -53L10 -22L69 -7L10 8L0 40L-10 8Z')],'The arriving courier drone');a.reveal('drone',5);a.move('drone',6,909,228);break;
case 3:coast('atlas',259,285,.7);boat('sea',609,365,.75);coast('soria',951,302,.59);type('one','Marsa Atlas',258,514,38);type('two','Cala Soria',949,514,38);a.reveal('soria',3);a.move('sea',5,649,365);break;
case 4:shape('room',603,477,[material('M-356 -22H356V22H-356Z',coral,coralN)],'An encounter makes recognition personal before the public hearing');a.person('narrator',339,310,{coat:coral,night:coralN,hairStyle:'long',pose:'concerned',scale:.94});a.person('derivative',878,310,{coat:ink,night:light,hairStyle:'long',pose:'attentive',scale:.94});shape('memory',578,268,[tint(n('ellipse',{cx:0,cy:-51,rx:30,ry:39,fill:coral}),coralN),material('M-37 -6Q0 -37 37 -6L49 80H-49Z',coral,coralN)],'A remembered likeness enters the living encounter');a.reveal('memory',3);a.hide('memory',5);a.move('derivative',6,824,310,2600);break;
case 5:a.person('traveller',350,349,{coat:coral,night:coralN,hairStyle:'long',pose:'concerned',scale:.62});a.move('traveller',5,685,385,3400);shape('exit',451,315,[material('M-110 -147H110V147H-110Z'),material('M-67 -112H67V147H-67Z',coral,coralN)],'A usable exit is a material condition of choice');boat('route',858,384,.7);a.reveal('route',4);a.move('route',6,887,384);break;
case 6:robot('care',318,327,1.05);shape('maintenance',858,322,[tint(n('circle',{cx:0,cy:0,r:89,fill:'none',stroke:coral,'stroke-width':23}),coralN),path('M-63 -63L63 63M-63 63L63 -63','$ink',12)],'A manual maintenance wheel makes the cost of choice concrete');a.reveal('maintenance',2);break;
case 7:cup('home',325,361,.95);robot('wait',848,329,1.02);a.move('wait',4,828,329);break;
}

s.visual=a.finish('Coastal travelogue in ultramarine and coral; terraced shore, faceless Miro, cracked cup and working vessels.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
