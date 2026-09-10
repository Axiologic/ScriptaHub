import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const ink='#65508b',light='#c3b4ea',coral='#ac5768',coralN='#e9aab8';
for(const [index,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
const material=(d,c=ink,cn=light)=>tint(n('path',{d,fill:c}),cn);
const type=(id,value,x,y,size=42)=>a.label(id,value,x,y,size);

const child=(id,x,y,k=1)=>shape(id,x,y,[material('M-32 -130C-115 -142 -140 -41 -83 3C-148 38 -110 132 -35 104C-6 159 92 121 69 48C144 44 152 -63 75 -71C68 -137 19 -159 -32 -130Z'),material('M-52 -75C-101 -17 -55 64 -3 58C50 102 98 36 51 -13C94 -60 29 -100 -5 -54Z',coral,coralN),material('M-30 -48Q-2 -83 35 -47L48 13Q9 57 -24 14Z'),path(id.includes('need')||id==='alone'?'M-7 5Q11 -7 24 4':'M-7 -3Q8 7 24 -2','$ink',4)],'A folded dimensional child; curved surfaces carry vulnerability rather than a star icon',k);
const world=(id,x,y,k=1)=>shape(id,x,y,[tint(dot(0,0,92,coral),coralN),material('M-69 -55L-11 -74L23 -28L-8 9L-48 -6L-65 27L-88 5Z'),material('M29 8L76 -7L72 48L33 78L10 44Z')],'A human tess world as a schematic finite sphere',k);
const reward=(id,x,y,k=1)=>shape(id,x,y,[material('M0 -86L73 -44V44L0 86L-73 44V-44Z',coral,coralN),path('M0 -43V43M-22 -13H17Q43 -4 13 12H-17','$ink',7)],'Yield sustains the observer; symbolic reward token',k);
switch(index){
case 0:shape('alve',360,325,[material('M-196 -118L-62 -187L111 -142L195 -12L138 154L-27 185L-180 95L-106 56L-31 103L88 88L118 -4L61 -84L-58 -112L-136 -65Z')],'An unfolded habitation alve after the adults disappear');child('iri',357,326,.71);shape('fold',786,368,[material('M-196 29L-67 -110L186 -35L61 120Z',coral,coralN),material('M-196 29L-67 -110L-83 36Z'),material('M-83 36L186 -35L61 120Z')],'The tess is accessible along unfamiliar directions rather than an ordinary screen');world('lives',826,339,.59);a.reveal('lives',4);a.move('iri',5,384,327,2600);break;
case 1:child('alone',594,326,1.25);shape('absent',862,325,[path('M-21 -66Q32 -72 56 -22Q51 16 31 27','$ink',5)],'An incomplete trace of a vanished adult voice');a.reveal('absent',2);a.hide('absent',3);reward('instruction',881,408,.5);a.reveal('instruction',4);break;
case 2:world('human',422,342,1.27);child('observer',914,292,.69);a.reveal('observer',3);a.move('observer',5,879,321);break;
case 3:shape('support',378,456,[material('M-234 -42L-127 -101L47 -111L243 -14L88 58L-96 28Z')],'The child’s alve needs the reward to sustain its living space');child('need',323,321,.75);child('sustained',323,300,.88);a.hide('need',4);a.reveal('sustained',4);world('risk',890,331,.89);reward('yield',864,185,.34);a.reveal('yield',2);a.move('yield',3,488,336,3200);a.hide('yield',4);a.move('sustained',5,364,304,2700);break;
case 4:shape('shared-house',602,326,[material('M-379 -38L-244 -158L27 -180L346 -21L259 142L-62 176L-319 90L-257 42L-69 100L213 86L255 -14L14 -104L-205 -82L-297 3Z',coral,coralN)],'The children build a shared house in the vesh, a place before proof');child('iri',350,334,.59);child('oda',602,302,.67);child('kel',860,334,.59);a.reveal('oda',2);a.reveal('kel',3);a.move('iri',5,381,324,2500);a.move('kel',5,832,326,2500);break;
case 5:world('care',602,333,1.35);child('controller',255,245,.46);a.move('controller',3,363,291,2900);shape('boundary',600,333,[tint(path('M-145 -97Q-219 0 -145 97M145 -97Q219 0 145 97',ink,20),light)],'Care also defines limits around a world');a.reveal('boundary',3);break;
case 6:world('small',339,345,.8);child('middle',653,309,.94);shape('unknown',960,286,[material('M0 -108L78 -52L43 59L-34 114L-79 0Z',coral,coralN)],'An unexplained direction; does not reveal the novel’s later architecture');a.reveal('unknown',3);break;
case 7:child('iri-return',494,330,1.1);world('listen',869,379,.62);a.reveal('listen',3);a.move('iri-return',5,521,330);break;
}

s.visual=a.finish('Folded dimensional beings, violet and coral; scale and posture make power and vulnerability coexist without revealing late cosmology.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
