import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const ink='#315973',light='#94bed7',rust='#99563e',rustN='#eeb38f';
for(const [index,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
const material=(d,c=ink,cn=light)=>tint(n('path',{d,fill:c}),cn);
const type=(id,value,x,y,size=42)=>a.label(id,value,x,y,size);

const salt=(id,x,y,k=1)=>shape(id,x,y,[material('M-40 36L-24 -16L7 -50L39 -2L29 40Z','#b18868','#e8d0a5'),path('M-24 -16L8 12L39 -2M8 12L7 -50M8 12L29 40','$ink',3)],'A salt crystal; bodily material and corrosion',k);
const hammer=(id,x,y,k=1)=>shape(id,x,y,[material('M-13 -30H13V132H-13Z',rust,rustN),material('M-76 -82H68V-20H-76Z'),path('M-53 -63H40','$ink',5)],'Jonah’s forge hammer',k);
const city=(id,x,y,k=1)=>shape(id,x,y,[material('M-170 25H170L133 93H-136Z'),material('M-123 25V-41H-62V25M-36 25V-108H24V25M59 25V-65H125V25',rust,rustN),path('M-188 115Q-100 135 0 115T188 115','$ink',6)],'Asterion, a floating city with ballast below its towers',k);
const shell=(id,x,y,k=1)=>shape(id,x,y,[material('M-43 -70Q-45 -125 0 -133Q45 -125 43 -70L32 -42L43 86H-43L-32 -42Z'),path('M-19 -89H19M0 -64V-22M-21 86V132M21 86V132','$ink',7)],'Continuity shell, a simplified delivery form',k);
switch(index){
case 0:shape('sea',805,409,[material('M-310 -36H309V92L-310 16Z','#9cb3bd','#384f5c')],'The water links a shoreline family to the floating city');shape('shore',315,429,[material('M-245 30L-151 -3L-69 13L-3 -45L77 -20L214 52H-245Z',rust,rustN),material('M-188 -12V-156L-85 -202L19 -156V-12Z'),material('M-149 -12V-117H-52V-12Z',rust,rustN)],'Port Nacre’s workshop stands on the Atlantic shore');city('asterion',926,314,.6);a.move('asterion',5,868,314,3300);a.person('jonah',365,342,{coat:rust,night:rustN,pose:'concerned',scale:.55});hammer('forge',279,388,.38);shell('delivered',636,377,.49);a.reveal('delivered',5);a.move('delivered',6,524,377,3000);break;
case 1:a.person('jonah',338,344,{coat:rust,night:rustN,pose:'concerned',scale:.9});hammer('work',208,379,.52);shell('delivery',958,330,.9);a.reveal('delivery',3);a.move('delivery',4,791,330,3000);break;
case 2:shape('coast',287,326,[material('M-165 68L-132 12H-64V-58H-7V-7H55V-109H109V68Z',rust,rustN),path('M-170 100H170','$ink',5)],'Port Nacre’s settled coastline');city('floating',799,319,.95);a.move('floating',5,875,319,3000);type('port','Port Nacre',287,519);type('a','Asterion',868,519);a.reveal('a',2);break;
case 3:a.person('sofia',323,336,{coat:rust,night:rustN,pose:'concerned',scale:.89});for(const[i,v]of ['A','B','C'].entries()){shape('document'+i,804,239+i*101,[material('M-128 -35H128V35H-128Z',i===1?rust:ink,i===1?rustN:light),tint(text(v,0,14,40,'#fff'),'#152633')],'The same authentic document '+v);a.move('document'+i,4,804,[340,441,239][i],2800);}a.person('sofia-explains',323,336,{coat:rust,night:rustN,pose:'open',scale:.89});a.hide('sofia',5);a.reveal('sofia-explains',5);break;
case 4:shell('continuity',286,330,.9);a.person('family',662,343,{coat:rust,night:rustN,pose:'concerned',scale:.77});shape('hearth',995,338,[material('M-116 -34L0 -130L116 -34V100H-116Z',rust,rustN),material('M-65 100V-3H65V100Z'),path('M-20 53Q-36 30 0 8Q36 43 20 67','$ink',7)],'A household receives a reconstructed family member');a.move('continuity',3,443,330,2900);a.person('family-open',662,343,{coat:rust,night:rustN,pose:'open',scale:.77});a.hide('family',5);a.reveal('family-open',5);break;
case 5:shape('valve',370,311,[tint(n('circle',{cx:0,cy:0,r:105,fill:'none',stroke:rust,'stroke-width':22}),rustN),path('M-76 -76L76 76M-76 76L76 -76','$ink',13)],'Manual water valve');shape('water',846,327,[material('M0 -130C-34 -70 -93 -4 -93 48A93 93 0 0 0 93 48C93 -4 34 -70 0 -130Z')],'Water as a condition of political choice');a.reveal('water',2);a.move('valve',4,360,302);break;
case 6:shape('weights',595,335,[path('M0 -144V149M-100 149H100M-220 -91H220','$ink',13),path('M-180 -90L-230 52M-180 -90L-130 52M180 -90L130 52M180 -90L230 52','$ink',5),material('M-240 52H-120Q-180 130 -240 52Z',rust,rustN),material('M120 52H240Q180 130 120 52Z')],'Competing defensible reasons remain in balance');salt('burden',773,347,.45);a.reveal('burden',3);break;
case 7:hammer('return',360,320,.9);salt('last',822,358,1.7);a.reveal('last',3);break;
}

s.visual=a.finish('Ironwork and marine ballast; rust, salt and Atlantic blue. Eight varied source-specific material compositions.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
