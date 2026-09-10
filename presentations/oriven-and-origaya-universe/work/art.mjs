import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [index,s]of scenes.entries()){
 const a=stageAuthor(),{n,path,text,tint,dot}=a;
 const c={teal:'#357c80',mint:'#97c7b2',silver:'#bbd7d1',amber:'#d4a24b',coral:'#d57c6b',blue:'#608bbb',ink:'#293f53',paper:'#e9e0c9',plum:'#9679a7'};
 const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
 const f=(d,col,night=col)=>tint(n('path',{d,fill:col}),night);
 const r=(x,y,w,h,col,rx=0)=>n('rect',{x,y,width:w,height:h,rx,fill:col});
 const label=(v,x,y,size=27,col='$ink')=>text(v,x,y,size,col);
 const act=(id,beat,action,extra={})=>a.actions.push({actor:id,action,beat,durationMs:1800,...extra});
 const pulse=(id,x,y,toX,toY,beat,col=c.amber,dur=2400)=>{obj(id,x,y,[dot(0,0,7,col),n('circle',{cx:0,cy:0,r:13,fill:'none',stroke:col,'stroke-width':2})],'A measured signal travels along the depicted physical route');a.reveal(id,beat,200);a.move(id,beat,toX,toY,dur);act(id,beat,'disappear',{offsetMs:dur+150,durationMs:400});};
 const mirel=(id,x,y,k=1)=>obj(id,x,y,[
  ...[-3,-2,-1,1,2,3].map((j)=>path(`M${j*4} -7Q${j*21} 17 ${j*27} 22`,c.teal,8)),
  f('M-17 0Q-13 -63 -25 -100Q0 -120 23 -98Q12 -51 18 0Z',c.teal),
  ...[-1,1].flatMap(d=>[f(`M${d*7} -92Q${d*93} -154 ${d*100} -97Q${d*69} -81 ${d*9} -68Z`,c.silver),path(`M${d*11} -83L${d*88} -108`,c.teal,3),f(`M${d*7} -119Q${d*65} -199 ${d*61} -134L${d*10} -99Z`,c.silver)]),
  n('ellipse',{cx:0,cy:-125,rx:31,ry:23,fill:c.ink}),...[-18,18].map(x=>dot(x,-126,9,c.amber)),...[-41,0,41].map((x,j)=>f(`M${x} ${-186-(j===1?17:0)}l10 18 -10 16 -10 -16Z`,c.blue))
 ],'Mirel: six braided root-feet, a narrow stem, silver capture fronds, sensory lenses and a phase-crystal crown',k);
 const aethon=(id,x,y,k=1)=>obj(id,x,y,[f('M-70 0Q-23 -91 -41 -240Q-56 -310 -23 -324Q17 -343 42 -309Q15 -170 71 0L110 30H54L19 5L15 39H-17L-22 5L-80 34H-113Z',c.teal,'#73aaa1'),path('M-64 12Q-145 49 -190 21M58 12Q140 46 179 14M-6 31V61',c.teal,13),path('M-15 -279Q-31 -155 -3 -98M19 -276Q-3 -169 22 -101',c.mint,7),...[-270,-231,-192].map(y=>n('ellipse',{cx:2,cy:y,rx:24,ry:8,fill:'none',stroke:c.amber,'stroke-width':3}))],'Aethon’s speaking trunk is rooted into a larger distributed body, without a terrestrial tree crown or human face',k);
 const hunter=(id,x,y,k=1)=>obj(id,x,y,[f('M-76 -17Q-44 -60 9 -42L30 -69L61 -72L82 -48L59 -37L34 -28L15 5L-44 3L-95 18L-144 4L-98 0Z',c.coral),path('M-29 -1L-7 20L-24 43M15 -8L40 17L24 40',c.coral,11),path('M43 -34L53 -7',c.coral,7),dot(62,-57,3,c.ink)],'Distant Origayan hunter: balancing tail and powerful hind limbs; non-graphic observation',k);
 const prey=(id,x,y,k=1)=>obj(id,x,y,[f('M-39 -17Q-9 -48 25 -26L42 -31L51 -14L31 -4H-25Z',c.amber),path('M-29 -7L-33 13M-13 -6L-10 13M17 -7L13 12M32 -11L39 8',c.amber,6)],'Small low four-limbed observed animal; no feeding or injury spectacle',k);
 const nursery=(id,x,y,k=1)=>obj(id,x,y,[n('ellipse',{cx:0,cy:2,rx:99,ry:25,fill:c.teal}),n('ellipse',{cx:0,cy:-6,rx:90,ry:20,fill:c.blue}),path('M-67 -8Q-45 -61 -27 -9M-53 -11Q-42 -57 -16 -16M-65 -24L-22 -23M-58 -40L-29 -40',c.silver,5),path('M-21 -8Q18 -30 64 -27',c.silver,6),f('M58 -19Q45 -82 68 -107Q96 -78 75 -18Z',c.amber),path('M68 -91V-23',c.coral,4)],'Intact white mycelial continuity bridge joins an old lattice and a young amber ramet above a mineral nursery pool',k);
 if(index===0){
  obj('cultivated-floor',312,500,[f('M-218 0Q-110 -24 2 -6T265 -1L288 41H-239Z','#6a9693'),path('M-200 18Q-50 46 46 11T247 15',c.blue,12)],'A maintained living floor carries nutrients and attention to the rooted observers');
  aethon('aethon',299,470,.88);mirel('mirel',525,471,.82);
  obj('array-aperture',892,331,[n('ellipse',{cx:0,cy:0,rx:198,ry:153,fill:'#ced8c4'}),f('M-187 24Q-74 -29 41 16T190 34L178 95Q0 190 -175 93Z','#b6a284'),...[-1,1].map(d=>f(`M${d*215} -88Q${d*251} -139 ${d*242} -44Q${d*222} -44 ${d*215} -88Z`,c.silver)),path('M-216 -68L-191 -50M216 -68L191 -50',c.blue,4)],'Living mirrors resolve a remote plain; the observed animals are an image, not inside Oriven');
  hunter('hunter',821,361,.68);prey('prey',968,369,.65);a.move('hunter',3,906,361,2500);a.move('prey',3,1008,369,2500);a.hide('hunter',4);a.hide('prey',4);
  obj('observation-delay',884,535,[label('11 light-minutes',0,0,29)],'The source’s actual light delay limits immediate response');a.reveal('observation-delay',4);
  obj('local-frond',141,468,[f('M0 8Q-56 -44 -27 -69Q2 -58 0 -8Q18 -72 43 -54Q57 -23 0 8Z',c.coral),path('M0 8V34',c.teal,8)],'A nearby damaged frond is within reach of Oriven’s normal repair infrastructure');pulse('local-repair',232,515,142,499,2,c.mint);pulse('local-repair-again',232,515,142,499,5,c.mint);
  obj('distant-trace',893,331,[path('M-123 0H-58L-45 -22L-31 15L-19 0H111',c.coral,5)],'A received observation does not provide a physical rescue route');a.reveal('distant-trace',4);
  pulse('received-light',692,330,574,336,1,c.blue,2500);a.move('mirel',4,511,471,2200);a.move('mirel',6,519,471,2500);
 }else if(index===1){
  obj('canopy-cutaway',603,463,[f('M-478 -44Q-352 -94 -257 -42T-14 -24T233 -42T471 -28V64H-475Z','#739a91'),path('M-431 38Q-250 0 -73 37T422 26',c.blue,20),path('M-364 -8L-343 -184Q-330 -224 -315 -183L-298 -17M231 -20L250 -173Q269 -222 282 -172L299 -10',c.mint,20)],'Cultivated columns support the canopy and thermal channels feed its maintained rooms');
  aethon('distributed-archive',239,446,.58);
  obj('mineral-memory',243,521,[-40,-13,14,41].map((x,j)=>n('ellipse',{cx:x,cy:0,rx:18,ry:25-j*2,fill:'none',stroke:c.amber,'stroke-width':4})),'Memory persists in mineral rings beneath the speaking trunk');pulse('attention-route',239,409,243,515,1,c.amber);
  nursery('continuity-nursery',857,452,1.22);
  obj('pressure-reservoir',601,410,[f('M-93 -94Q0 -124 90 -90L71 57Q0 94 -76 57Z',c.silver),f('M-84 -47Q0 -29 81 -47L69 55Q0 78 -72 55Z',c.blue),path('M-45 -91L-53 -37M0 -99V-39M46 -90L51 -37',c.teal,5),label('Thermal water',0,114,26)],'A living reservoir membrane holds the water and pressure on which the nursery depends');
  obj('nethra',480,472,[...[-4,-3,-2,-1,1,2,3,4].map(j=>path(`M${j*8} -18Q${j*18} 10 ${j*20} 17`,c.teal,7)),f('M-65 -24Q-78 -84 -9 -90Q56 -91 65 -29L30 -1H-36Z',c.teal),...[-36,0,36].map(x=>n('ellipse',{cx:x,cy:-53,rx:15,ry:24,fill:c.silver,opacity:.8})),dot(49,-54,5,c.amber)],'Nethra: a low broad warm-water body with eight anchoring roots and transparent sampling bladders');
  pulse('water-pressure',650,501,787,496,5,c.blue,2300);obj('sampling-bladder',530,421,[n('ellipse',{cx:0,cy:0,rx:16,ry:27,fill:c.silver}),path('M0 26L-17 44',c.teal,6)],'Nethra takes a water sample rather than merely posing beside an abstract water icon');a.reveal('sampling-bladder',4);a.move('sampling-bladder',4,562,416,1700);
  obj('observation-lens',973,246,[n('ellipse',{cx:0,cy:0,rx:62,ry:34,fill:c.silver}),path('M-36 0H-16L-6 -12L5 11L13 0H35',c.coral,4)],'The distant observation enters a receiving lens at the edge of the nursery, without enacting the later transfer failure');a.reveal('observation-lens',3);a.hide('observation-lens',5);
  obj('bridge-focus',854,229,[label('Shared continuity',0,0,25)],'The introduction preserves the bridge rather than revealing its later crisis');a.reveal('bridge-focus',6);
 }else if(index===2){
  obj('cultivation-cradle',312,471,[f('M-190 -18Q-160 -63 -106 -27H119Q168 -54 185 -20L168 9H-179Z',c.teal),path('M-148 8V66M142 8V66',c.teal,14)],'The nonliving observation instrument remains supported on a preparation cradle');
  obj('descender',302,352,[f('M0 -83Q67 -5 0 88Q-59 0 0 -83Z',c.ink,'#9eb8c7'),path('M-5 -59V61',c.blue,6),f('M5 -8L-131 -70L-114 42Z',c.silver),f('M5 -8L129 -69L113 43Z',c.silver),path('M-117 -54L-102 28M114 -54L102 27',c.blue,3)],'A sterile black seed-shaped probe with a fine sail, no occupant and no living root connection');
  obj('isolated-receiver',607,425,[f('M-71 -19L-54 -104H44L72 -20L55 0H-51Z',c.blue),r(-44,-84,87,56,c.silver,5),path('M-26 -57H26',c.ink,5),path('M0 1V101M-54 102H57',c.blue,12),label('Isolated receiver',0,-136,26)],'Returning findings first enter a receiver materially separate from the living network');
  obj('living-receiver',900,435,[f('M-70 0Q-66 -94 1 -110Q68 -89 71 0L38 36H-43Z',c.teal),path('M-38 30Q-77 70 -84 89M31 32Q100 82 167 98',c.teal,14),n('ellipse',{cx:0,cy:-44,rx:41,ry:37,fill:c.silver}),path('M-26 -44H25',c.teal,5)],'A cultivated receiving organ keeps its living roots on its own side of the optical gap');
  obj('optical-gap',752,481,[label('Optical gap',0,58,26),path('M-57 -85H54',c.blue,3)],'Only light crosses the physical separation; the thin line denotes its beam, not a material root');a.reveal('optical-gap',3);
  pulse('returned-finding',354,333,607,365,1,c.blue,2700);pulse('optical-finding',660,394,852,394,3,c.amber,2800);
  obj('operator-balcony',1038,331,[f('M-82 -13Q-2 -35 80 -11L64 10H-76Z',c.teal),path('M49 8Q83 67 80 136',c.teal,12)],'A cultivated observation balcony supports Mirel above the receiving organ');mirel('mirel',1045,307,.51);a.move('mirel',2,1020,307,1900);
  obj('consent-membrane',1047,490,[f('M-15 -30Q-46 -80 -8 -97Q29 -81 19 -26L9 11H-8Z',c.coral),path('M-25 -47Q0 -61 25 -46',c.amber,5)],'A neighbouring recipient keeps its consent membrane closed; no automatic admission is implied');a.reveal('consent-membrane',4);
  obj('separate-controls',870,278,[path('M-29 0V-24M28 0V-24M-29 0Q-34 30 -15 63M28 0Q43 33 37 61',c.teal,6),n('ellipse',{cx:-29,cy:-32,rx:18,ry:10,fill:c.amber}),n('ellipse',{cx:28,cy:-32,rx:18,ry:10,fill:c.plum})],'Independent controls preserve divided responsibility for opening the receiving route');a.reveal('separate-controls',4);
 }else{
  obj('opening-book',602,374,[f('M-430 -130Q-251 -181 -9 -128Q195 -173 422 -128L444 145Q224 103 0 157Q-240 103 -442 145Z',c.teal),f('M-420 -138Q-210 -178 -7 -133V142Q-221 96 -426 130Z',c.paper),f('M7 -133Q219 -178 411 -139L430 129Q213 97 7 142Z','#f2e9d6'),path('M0 -128V144',c.amber,5)],'A well-proportioned open book supports the reader lens, rather than depicting the nonhuman civilization as human');
  obj('chapter-tabs',610,233,[r(-353,-43,220,44,c.amber,4),label('The First Death',-243,-14,25,c.ink),r(67,-43,232,44,c.mint,4),label('The Deep Canopy',183,-14,25,c.ink)],'Specific source chapter tabs give a clear place to start reading');
  aethon('opening-archive',387,446,.42);obj('memory-arc',387,458,[path('M-92 30Q-149 -49 -90 -129M-84 20Q-131 -47 -79 -113M-77 12Q-113 -45 -68 -99',c.amber,5)],'An unfinished mineral-memory arc marks the long deliberation without inventing a completed outcome');
  nursery('opening-nursery',830,427,.90);mirel('opening-mirel',946,449,.39);
  obj('reading-line',821,484,[label('Nursery continuity',0,0,24,c.ink)],'A marginal reading prompt remains attached to the actual ecology illustrated on the page');a.reveal('reading-line',3);
  pulse('interrupting-light',232,341,405,337,2,c.blue,2500);
  obj('next-page',1023,489,[f('M-53 12Q-12 -33 10 -64L-10 29Z','#fff5dd'),path('M-52 11Q-13 -7 10 -64',c.amber,3)],'An incomplete page turn leaves the series’ later consequences for the reader');a.reveal('next-page',5);a.move('next-page',6,1005,483,2200);
 }
 s.visual=a.finish(s.adaptation.composition+' Anatomy and material relationships follow the cited opening chapters; spatial staging is interpretive, the continuity bridge remains intact, and later revelations are withheld.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
