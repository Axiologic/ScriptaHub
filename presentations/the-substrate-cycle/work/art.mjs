import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
import {ASSETS} from '../../../.agents/skills/shf-presentation-creator/scripts/lib/asset-library.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [index,s]of scenes.entries()){
 const a=stageAuthor(),{n,path,text,tint,dot}=a,c={blue:'#5389b2',water:'#77b6c8',plum:'#8a7297',gold:'#c7a05c',green:'#75998a',coral:'#cd826c',ink:'#324b59',cream:'#eee2c8',silver:'#b6cbd0'};
 const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
 const f=(d,col,night=col)=>tint(n('path',{d,fill:col}),night);
 const r=(x,y,w,h,col,rx=0)=>n('rect',{x,y,width:w,height:h,rx,fill:col});
 const label=(v,x,y,size=27,col='$ink')=>text(v,x,y,size,col);
 const act=(id,beat,action,extra={})=>a.actions.push({actor:id,action,beat,durationMs:1900,...extra});
 const person=(id,x,y,coat,identity='person-03-neutral',k=.85,seated=false)=>{storyPerson(a,id,x,y,{coat,identity,scale:k,seated,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;};
 const gesture=(id,b,g)=>storyGesture(a,id,b,g,2300);
 const look=(id,target,b)=>act(id,b,'lookAt',{target,durationMs:850});
 const express=(id,b,emotion)=>act(id,b,'character.express',{emotion,durationMs:850});
 const shortHair=(id,x,y,coat,skin,k=.9)=>{person(id,x,y,coat,'person-03-neutral',k);const o=a.objects.at(-1),alt=ASSETS['person-03-neutral']('$asset',{coat,dynamicExpressions:true,hair:'short',hairColor:'#37404a',skin});o.visual.children=o.visual.children.map(c=>c.id==='$asset.head'?alt.children.find(x=>x.id==='$asset.head'):c);};
 const crate=(id,x,y,k=1)=>obj(id,x,y,[f('M-96 -78Q0 -114 96 -78L67 -4H-68Z',c.cream),path('M-77 -17L-87 72M77 -17L87 72M-106 74Q0 109 106 74',c.gold,11),path('M-64 -61V-18M-24 -65V-13M22 -65V-13M63 -61V-18',c.gold,5)],'Nila’s empty infant cradle is an absence in an unresolved investigation',k);
 const citrus=(id,x,y,k=1)=>obj(id,x,y,[f('M-11 0L-7 -167H9L15 0Z',c.gold),...[-1,1].flatMap(d=>[f(`M0 -95Q${d*85} -206 ${d*99} -143Q${d*101} -96 0 -83Z`,c.green),dot(d*57,-128,12,c.gold)]),n('ellipse',{cx:0,cy:-185,rx:46,ry:65,fill:c.green}),dot(7,-211,12,c.gold)],'Medicinal citrus identifies the source’s winter garden as a lived common household',k);
 const threshold=(id,x,y,k=1)=>obj(id,x,y,[f('M-65 0V-134L0 -187L70 -132V0Z',c.gold),r(-39,-117,39,51,c.silver,2),r(21,-101,28,99,c.plum,2),path('M-39 -91H0M-19 -115V-68',c.cream,3)],'A vacated lower-street home gives the incoming sea a specific local threshold',k);
 const spider=(id,x,y,k=.8)=>obj(id,x,y,[n('ellipse',{cx:0,cy:0,rx:23,ry:14,fill:c.silver}),...[-1,1].flatMap(d=>[-1,0,1].map(j=>path(`M${d*16} ${j*5}L${d*31} ${j*13}L${d*41} ${j*13+9}`,c.ink,4))),dot(-6,-5,4,c.blue),dot(6,-5,4,c.blue)],'Sami’s palm-sized maintenance spider inspects pipes and refuses the berry-game deception',k);
 if(index===0){
  obj('coast-section',453,485,[f('M-352 -70Q-176 -90 -30 -64L24 4H-352Z',c.water),f('M-15 -8H420L459 55H-54Z','#b1b4a6'),path('M-341 -40Q-237 -63 -145 -36T-38 -41',c.blue,4)],'A physical gate separates sea from inhabited city rather than illustrating an abstract choice');
  obj('closed-gate',433,386,[r(-24,-133,48,227,c.blue),path('M-44 -132H44M-34 -107H35M-34 85H35',c.ink,8)],'The controlled eastern gate is held before the scheduled public decision');
  threshold('lower-house',628,481,.65);person('restoration-resident',699,528,c.blue,'person-02-neutral',.71);person('displaced-resident',827,526,c.coral,'person-04-neutral',.74);
  obj('black-cloth',857,397,[f('M-9 -21Q12 -33 31 -10L22 43L-5 20Z',c.ink,'#8393a5')],'Household cloth identifies dissent rooted in a home');
  obj('control-balcony',971,305,[f('M-121 0H117L129 19H-133Z',c.silver),path('M-100 19V177M93 19V178',c.blue,13)],'The decision occurs above the crowd at an actual flood-control balcony');person('liora',925,298,'#e4e7dd','person-04-neutral',.55);shortHair('mina',1064,298,c.plum,'#885a43',.52);
  obj('privacy-door',795,243,[r(-49,-106,98,170,c.plum,6),r(-33,-91,66,143,c.silver,3),dot(18,-9,5,c.gold)],'An unopened privacy-room door marks the suspicious death without showing a body or a culprit');a.reveal('privacy-door',3);
  obj('restoration-plan',253,202,[r(-111,-69,222,122,c.cream,8),path('M-83 25Q-53 -23 -13 -6T70 -32',c.blue,9),label('Inland protection',0,85,24)],'A planning surface identifies the wider beneficiaries of the local transformation');a.reveal('restoration-plan',4);gesture('displaced-resident',4,'question');express('displaced-resident',4,'worried');look('mina','privacy-door',3);
  const first=a.objects.map(x=>x.id);for(const id of first)a.hide(id,5);
  obj('winter-garden-floor',608,502,[f('M-397 -17H383L429 39H-429Z','#b5c4ad')],'The second case belongs to a later common household, not the same flood investigation');citrus('medicinal-citrus',200,492,.88);crate('nila-cradle',445,441,.72);shortHair('leila',668,528,c.coral,'#6a4437',.91);person('mara',900,528,c.plum,'person-03-neutral',.90);
  obj('infant-record',483,266,[r(-114,-61,228,100,c.cream,5),label('Nila · Missing',0,-20,27,c.ink),label('37 legal parents',0,17,24,c.ink)],'Nila is an infant with37 legal parents; she is not the six-year-old Sami');
  for(const o of a.objects.filter(x=>!first.includes(x.id)))a.reveal(o.id,5);look('mara','nila-cradle',5);gesture('leila',5,'question');express('leila',5,'tired');gesture('mara',6,'reflect');
 }else if(index===1){
  obj('section-floor',609,504,[f('M-474 -5H439V43H-474Z','#b4b5a5')],'A cross-section keeps sea, gate and lower streets in a physically continuous setting');
  obj('sea',316,416,[f('M-204 -58Q-75 -73 89 -57L224 -52V97H-204Z',c.water),path('M-190 -29Q-88 -44 11 -24T204 -27',c.blue,5)],'The sea presses against the held barrier');
  threshold('local-home',866,496,.95);
  obj('gate-well',530,481,[r(-42,-18,84,135,c.silver,3),path('M-42 -18V117H42V-18',c.blue,5)],'A receiving shaft supports the lowering gate beneath the street level in the engineering section');
  obj('gate',530,365,[r(-22,-133,44,266,c.blue),path('M-42 -134H43M-34 -108H35M-33 109H35',c.ink,9)],'The eastern gate physically lowers to admit water');a.move('gate',4,530,466,3200);
  obj('water-front',549,469,[f('M-380 -19Q-284 -32 -180 -19T-20 -12Q12 -1 19 21H-380Z',c.water),path('M-330 -6Q-201 -17 -102 -4T7 8',c.blue,4)],'A continuous shallow water front advances from the sea into already vacated lower streets');a.reveal('water-front',4);a.move('water-front',4,896,469,4000);
  person('supporter',716,279,c.blue,'person-02-neutral',.53);person('local-resident',966,284,c.coral,'person-04-neutral',.55);obj('safe-promenade',854,288,[f('M-188 -10H161V16H-194Z',c.silver),path('M-164 16V92M130 16V92',c.blue,12)],'Residents remain above the incoming water on a protected promenade');
  obj('household-photo',1009,222,[r(-31,-45,62,58,c.gold,3),r(-24,-39,48,42,c.cream,1),f('M-19 -5V-25L0 -37L19 -25V-5Z',c.coral)],'A remembered household object makes local loss particular');
  obj('consequence-plan',264,173,[r(-147,-65,294,114,c.cream,6),label('Wider protection',0,-26,27,c.ink),label('Local displacement',0,14,25,c.ink)],'Pando displays separate projected effects; no simulated emotion or universal net-benefit verdict');a.reveal('consequence-plan',3);
  gesture('supporter',2,'explain');gesture('local-resident',2,'question');look('local-resident','local-home',4);express('local-resident',4,'worried');gesture('local-resident',5,'reflect');gesture('supporter',6,'reflect');
 }else if(index===2){
  obj('garden-floor',361,500,[f('M-265 -17H227L260 40H-270Z','#b9c8b0')],'The winter garden is a maintained place of common living and care');citrus('citrus',179,463,.72);crate('nila-cradle',326,468,.51);shortHair('leila',435,517,c.coral,'#6a4437',.75);person('mara',590,517,c.plum,'person-03-neutral',.77);
  obj('nila-label',305,288,[label('Nila · Infant',0,-10,25),label('37 legal parents',0,22,24)],'The parent count belongs to the missing infant Nila');
  obj('care-ledger',893,359,[r(-174,-154,364,289,c.cream,6),label('Care attribution',12,-119,28,c.ink)],'Mara’s disputed attribution record separates actions, subjects and enabling care');
  obj('holding-role',794,303,[dot(0,-10,13,c.coral),path('M-19 9Q0 -3 20 10',c.coral,9),n('ellipse',{cx:7,cy:17,rx:15,ry:7,fill:c.silver}),label('Held Nila',0,53,20,c.ink)],'Recorded direct infant care: one adult held Nila');
  obj('milk-role',794,402,[r(-11,-28,22,43,c.silver,4),r(-8,-35,16,10,c.gold,3),path('M-8 -7H7',c.blue,3),label('Prepared milk',0,47,20,c.ink)],'Recorded direct infant care: another adult prepared milk');
  obj('infant-event',1012,329,[n('ellipse',{cx:0,cy:0,rx:35,ry:23,fill:c.silver}),dot(-13,-4,12,c.coral),label('Nila’s care',0,56,21,c.ink)],'The direct care roles concern the same infant event');
  obj('enabling-role',986,454,[label('Settled Sami',0,-2,20,c.ink),label('Freed caregiver',0,26,19,c.ink)],'Indirect enabling care: settling the older child allowed the infant care to proceed, not another direct act on Nila');
  obj('direct-links',0,0,[path('M824 305L970 321M823 405L970 343',c.blue,3)],'Two direct source-supported care routes connect to the infant event');
  obj('indirect-link',0,0,[path('M1048 433L1078 419V329H1051',c.plum,4),f('M1060 322L1049 329L1060 336Z',c.plum)],'Indirect route joins the infant event through caregiver availability, not an identical third infant task');
  obj('care-signal',1078,416,[dot(0,0,6,c.plum)],'A signal follows the enabling-care route into the shared infant-care record');a.move('care-signal',3,1078,329,1600);act('care-signal',3,'moveTo',{offsetMs:1900,x:1051,y:329,durationMs:700});act('care-signal',3,'disappear',{offsetMs:3100,durationMs:400});
  for(const id of ['holding-role','milk-role','infant-event','enabling-role','direct-links','indirect-link','care-signal'])a.reveal(id,3);
  obj('standing-entry',888,520,[r(-134,-22,268,42,c.silver,4),label('Standing · Disputed',0,6,25,c.ink)],'Governance standing can be contested; there is no cash payment or transfer between parents');a.reveal('standing-entry',4);
  obj('game-table',279,531,[r(-70,-17,140,13,c.gold,4),path('M-50 -4V32M50 -4V32',c.gold,7)],'Sami’s low game table is separate from Nila’s empty cradle');
  person('sami',153,555,c.blue,'person-03-neutral',.38);obj('berry-cups',273,506,[-28,16].flatMap(x=>[f(`M${x-10} -17H${x+10}L${x+14} 4H${x-14}Z`,c.cream),dot(x,-19,2,c.gold)]),'The older child’s two cups conceal a berry for the maintenance-spider game');spider('maintenance-spider',327,512,.43);a.move('maintenance-spider',6,301,512,2100);
  look('mara','care-ledger',1);express('leila',2,'tired');gesture('leila',2,'question');look('leila','enabling-role',3);gesture('mara',4,'reflect');express('mara',5,'curious');gesture('leila',5,'explain');look('sami','maintenance-spider',6);
 }else{
  obj('shared-world-volume',602,373,[f('M-434 -133Q-220 -178 -7 -130Q222 -178 421 -133L440 153Q230 111 0 166Q-219 111 -449 152Z',c.blue),f('M-424 -141Q-210 -177 -8 -135V147Q-220 110 -432 135Z',c.cream),f('M8 -135Q220 -177 412 -141L427 135Q212 110 8 147Z','#f4ead4'),path('M0 -131V147',c.gold,4)],'A reader-eye volume keeps the two source epochs and cases distinct while inviting comparison');
  obj('chapter-tabs',609,220,[r(-370,-39,257,43,c.gold,4),label('The City and the Sea',-241,-9,23,c.ink),r(79,-39,273,43,c.silver,4),label('Thirty-Seven Parents',215,-9,23,c.ink)],'Compact chapter-reference tabs guide the reader to the two actual openings');
  obj('waterfront-reading',381,375,[f('M-107 -19Q-60 -35 -7 -16V68H-107Z',c.water),r(-8,-84,18,153,c.blue),f('M30 68V-28L75 -69L119 -28V68Z',c.gold),r(63,9,28,59,c.plum,2),label('Unequal local cost',0,113,24,c.ink)],'The first opening keeps the imposed household cost visible beside the water-control benefit');
  obj('household-reading',826,371,[path('M-74 -55Q0 -80 74 -55L52 -2H-54Z',c.gold,8),path('M-60 -6L-69 43M61 -6L69 43',c.gold,8),r(-69,59,139,34,c.silver,3),label('Shared care',0,83,21,c.ink)],'The second opening concerns a particular infant’s care and disputed attribution');
  obj('reading-case',621,384,[r(-62,-49,126,116,c.cream,3),label('Nila',0,-17,23,c.ink),label('Care record',0,16,20,c.ink),path('M-35 40H36',c.plum,3)],'The case sheet connects the reading route without solving the infant disappearance');a.reveal('reading-case',3);
  obj('reader-hand',1079,478,[f('M-23 45L-40 -3Q-44 -18 -34 -19L-15 3L-13 -55Q-9 -74 1 -67L6 -11Q29 -29 34 -11L28 44Z','#c79672')],'The reader follows the comparison and leaves the later solutions unread');a.move('reader-hand',3,1036,472,2300);a.move('reader-hand',6,1007,465,2300);
 }
 if(index===1){for(const o of a.objects)if(o.id!=='consequence-plan')o.y-=50;for(const x of a.actions)if(x.y!==undefined&&x.actor!=='consequence-plan')x.y-=50;}
 s.visual=a.finish(s.adaptation.composition+' The two source epochs remain distinct, Nila is an infant and Sami an older child, indirect enabling care stays explicit, and the mysteries remain unresolved.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
