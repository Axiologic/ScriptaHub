import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const ink='#326b6c',light='#a3d3cc',gold='#a57a26',goldN='#e5cd85';
for(const [index,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
const material=(d,c=ink,cn=light)=>tint(n('path',{d,fill:c}),cn);
const type=(id,value,x,y,size=42)=>a.label(id,value,x,y,size);

const lamp=(id,x,y,k=1)=>shape(id,x,y,[material('M-22 88H22L15 -7H-15Z'),material('M-94 -6L-56 -101H56L94 -6Z',gold,goldN),material('M-68 104H68V125H-68Z'),path('M0 -5V87','$ink',5)],'The first lamp in the museum',k);
const umbrella=(id,x,y,k=1)=>shape(id,x,y,[material('M-145 -15Q-122 -139 0 -140Q122 -139 145 -15Q107 -48 71 -14Q34 -45 0 -12Q-35 -43 -71 -14Q-108 -46 -145 -15Z'),path('M0 -130V108Q-2 162 -48 133','$ink',10)],'The borrowed umbrella with damaged ribs',k);
const key=(id,x,y,k=1)=>shape(id,x,y,[tint(n('circle',{cx:-72,cy:0,r:52,fill:'none',stroke:gold,'stroke-width':22}),goldN),tint(path('M-20 0H121V32M75 0V29',gold,22),goldN)],'A key represents actual access and permission',k);
const watch=(id,x,y,k=1)=>shape(id,x,y,[tint(n('circle',{cx:0,cy:0,r:85,fill:'none',stroke:gold,'stroke-width':16}),goldN),path('M0 -51V0L39 21','$ink',8),material('M-14 -90V-114H14V-90Z')],'A watch carries a personal history',k);
switch(index){
case 0:shape('wall',793,286,[material('M-285 -117H285V134H-285Z'),...[-159,0,159].map(x=>material(`M${x-47} 82V-29Q${x} -91 ${x+47} -29V82Z`,gold,goldN))],'Stone windows promise a view but provide none');shape('plinth',511,441,[material('M-83 -7H83V106H-83Z')],'The lamp stands on a museum plinth');lamp('lamp',510,342,.8);a.person('mara',290,354,{coat:gold,night:goldN,hairStyle:'long',pose:'concerned',scale:.77});shape('label',837,451,[material('M-125 -39H125V39H-125Z',gold,goldN),text('Inventory',0,12,37,'#233331')],'The official label gives an account of the object');a.reveal('label',4);a.move('mara',5,334,354,2200);break;
case 1:shape('facade',602,324,[material('M-305 -133H305V143H-305Z'),...[-208,-70,70,208].map(x=>material(`M${x-36} 73V-29Q${x} -90 ${x+36} -29V73Z`,gold,goldN))],'False windows carved into a sealed museum facade');lamp('controlled',1020,408,.39);a.reveal('controlled',3);break;
case 2:umbrella('umbrella',395,327,1.04);watch('object',883,375,.87);a.reveal('object',4);break;
case 3:key('access',276,381,.65);a.person('resident',577,349,{coat:gold,night:goldN,hairStyle:'long',pose:'concerned',scale:.68});a.move('access',3,737,454,2600);shape('door',845,325,[material('M-97 -147H97V147H-97Z'),material('M-66 -115H66V114H-66Z',gold,goldN)],'A door without a handle; care and restricted exit');a.reveal('door',4);break;
case 4:shape('floor',604,378,[material('M-373 -9H373V9H-373Z')],'A public floor separates visible benefit from the work sustaining it');watch('time',779,269,.83);a.person('worker',351,422,{coat:gold,night:goldN,pose:'concerned',scale:.58});shape('mechanism',610,442,[tint(n('circle',{cx:0,cy:0,r:59,fill:'none',stroke:gold,'stroke-width':13}),goldN),path('M-43 -43L43 43M-43 43L43 -43','$ink',8)],'Maintenance below the public floor');a.reveal('worker',3);a.reveal('mechanism',3);a.move('worker',5,431,422,2700);break;
case 5:for(const[i,v]of ['Care','Contract','Future'].entries()){shape('tag'+i,275+i*325,330,[material('M-112 -66H92L121 0L92 66H-112Z',i%2?gold:ink,i%2?goldN:light),text(v,-8,12,34,'#132928')],'A museum’s explanatory category: '+v);if(i)a.reveal('tag'+i,i+3);}break;
case 6:lamp('entrance',310,348,.85);shape('whale',851,330,[material('M-159 -22Q-149 -105 -35 -85Q58 -63 71 2Q113 -32 155 -72Q165 13 104 57Q32 125 -81 64Q-136 49 -159 -22Z'),dot(-115,-24,7,'#152b2c'),material('M-5 58L48 112L46 49Z',gold,goldN)],'Whale Within Whale is the source’s named alternative entrance');a.reveal('whale',3);break;
case 7:lamp('return',763,351,1.0);a.person('mara',367,342,{coat:ink,night:light,pose:'open',scale:.88});a.move('mara',5,421,342,2600);break;
}

s.visual=a.finish('Teal museum theatre with brass object silhouettes; lamp, umbrella, key and timepiece retain human histories.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
