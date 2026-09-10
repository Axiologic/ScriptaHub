import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const C={ink:'#283849',water:'#4f8caa',deep:'#365d80',rust:'#ba624f',amber:'#d7ae64',cream:'#f2e5cd',reed:'#72b79b',plum:'#9a86b4',ice:'#bad5db'};
const gesture=(q,id,beat,emotion,pose)=>{q.actions.push({actor:id,action:'character.express',emotion,beat,durationMs:1100});if(pose)storyGesture(q,id,beat,pose,1900);};
const appear=(q,id,b,offset=0)=>q.actions.push({actor:id,action:'appear',beat:b,offsetMs:offset,durationMs:1100});
const vanish=(q,id,b,offset=0)=>q.actions.push({actor:id,action:'disappear',beat:b,offsetMs:offset,durationMs:900});
function table(q,id,x,y,w=430){q.add(q.object(id,x,y,[q.n('path',{d:`M${-w/2} -14H${w/2}L${w/2+20} 12H${-w/2-20}Z`,fill:C.amber}),q.tint(q.path(`M${-w/2+18} 12V72M${w/2-18} 12V72`,C.ink,10),'#a3b7ca')],'Supported table, not a floating presentation panel.'));}
function bowl(q,id,x,y,color=C.rust,cracked=false,scale=1){const {n,path,object}=q;q.add(object(id,x,y,[n('path',{d:'M-45 -16Q-38 30 0 31Q38 30 45 -16Z',fill:color}),n('ellipse',{cx:0,cy:-16,rx:45,ry:12,fill:C.cream}),path('M-44 -17Q0 1 44 -17',color,4),...(cracked?[path('M-20 -24L-14 -9L-20 4L-10 18',C.ink,2.7)]:[])],cracked?'Soren’s particular dark bowl has a visible hairline crack, not a moral defect.':'A ceramic bowl with a supported base.',scale));}
function cup(q,id,x,y,s=1){q.add(q.object(id,x,y,[q.n('path',{d:'M-21 -31H21L17 0H-17Z',fill:C.cream}),q.path('M21 -24Q43 -24 37 -11Q31 -5 21 -10',C.amber,5),q.n('ellipse',{cx:0,cy:-30,rx:21,ry:6,fill:C.rust})],'Root tea in a cup whose base meets its support.',s));}
function reeds(q,id,x,y,s=1){q.add(q.object(id,x,y,[...[-38,-10,20,42].flatMap((xx,i)=>[q.path(`M${xx} 0Q${xx-20} ${-50-i*10} ${xx+5} ${-110+i*6}`,C.reed,5),q.n('path',{d:`M${xx-5} ${-58-i*6}Q${xx+45} ${-100-i*4} ${xx+35} ${-50-i*5}Q${xx+4} ${-27-i*7} ${xx-5} ${-58-i*6}Z`,fill:i%2?C.amber:C.reed})])],'Living memory reeds, a fictional biological system.',s));}
function seated(q,id,x,y,identity,coat,scale=.7){storyPerson(q,id,x,y,{identity,coat,seated:true,scale});q.objects.at(-1).visual.children.shift();q.add(q.object(id+'-bench',x,y-68*scale,[q.n('rect',{x:-104,y:-7,width:208,height:14,rx:3,fill:C.amber}),q.tint(q.path('M-87 7V48M87 7V48',C.ink,7),'#a3b7ca')],'A bench supports the seated figure at the actual seated hip height.'));}
function hand(q,id,x,y,color,rotation=0){q.add(q.object(id,x,y,[q.n('path',{d:'M-60 -14H-15Q-3 -39 9 -24L13 -12H46Q57 -12 57 -2Q57 8 45 9H16Q8 25 -11 19L-24 10H-60Z',fill:color})],'An illustrative hand operates the working knot; role does not encode a fixed gender.'));}
// Opening: an actual crowded rescue at a readable bodily scale.
{
 const q=stageAuthor(),{n,path,dot,object}=q;
 q.add(object('lower-terrace',202,491,[n('path',{d:'M-153 -22H124V50H-153Z',fill:C.amber}),n('path',{d:'M-136 -29V-187H-38V-29Z',fill:C.rust}),n('rect',{x:-119,y:-161,width:60,height:83,fill:C.ice}),path('M-88 -161V-78',C.rust,5),n('path',{d:'M-8 -21V-92H23V-21Z',fill:C.ink})],'Flooded lower laboratory terrace in Vesper.'));
 q.add(object('bridge-pylon',384,479,[n('path',{d:'M-28 58V-218H0V-115L42 -75V58Z',fill:C.deep}),path('M-16 -140L3 -129L-7 -113L17 -99',C.cream,3)],'The bridge support is failing in the opening flood.'));
 q.add(object('boat-back',690,480,[n('path',{d:'M-423 -48Q-255 -66 346 -45L413 -23Q210 15 -363 0Z',fill:C.amber}),n('path',{d:'M-394 -35H365L330 -18H-373Z',fill:C.cream}),path('M-185 -44V-100H-116V-38',C.ink,8)],'A rescue boat with a long continuous deck and a pilot console.'));
 storyPerson(q,'mara-raised',261,563,{identity:'person-11-neutral',coat:C.rust,scale:.56});
 const mara=q.objects.at(-1);for(const [part,xx]of [['armL',-50],['armR',50]]){const arm=mara.visual.children.find(n=>n.id==='$asset.'+part);arm.children[0].attrs.d=`M${xx<0?-34:32} -157Q${xx*1.6} -250 ${xx} -315`;arm.children[1].attrs.cx=xx;arm.children[1].attrs.cy=-315;}
 storyPerson(q,'mara-aboard',362,495,{identity:'person-11-neutral',coat:C.rust,scale:.56});appear(q,'mara-aboard',3,3200);
 storyPerson(q,'sio',490,483,{identity:'person-07-neutral',coat:C.deep,scale:.62});
 storyPerson(q,'older-passenger',657,489,{identity:'person-20-neutral',coat:C.plum,seated:true,scale:.47});q.objects.at(-1).visual.children.shift();
 storyPerson(q,'child-passenger',778,493,{identity:'person-16-neutral',coat:C.ice,seated:true,scale:.36});q.objects.at(-1).visual.children.shift();
 storyPerson(q,'fungus-seller',933,492,{identity:'person-18-neutral',coat:C.reed,seated:true,scale:.48});q.objects.at(-1).visual.children.shift();
 q.add(object('wrist-wrap',634,437,[n('path',{d:'M-14 -5L14 -2L11 13L-15 10Z',fill:C.cream}),path('M-8 -3L-10 10M0 -2L-2 11M8 0L6 12',C.ice,2)],'The older passenger has a wrapped wrist.'));
 q.add(object('thermal-cloth',778,490,[n('path',{d:'M-23 -53Q0 -64 23 -53L33 8H-34Z',fill:C.ice}),path('M-20 -37L24 -13M-26 -14L26 7',C.cream,4)],'The child is wrapped in thermal cloth.'));
 q.add(object('six-baskets',1032,468,Array.from({length:6},(_,i)=>{let xx=(i%3)*36-45,yy=Math.floor(i/3)*27-16;const g=n('g');g.children=[n('path',{d:`M${xx-15} ${yy-14}H${xx+15}L${xx+11} ${yy+6}H${xx-11}Z`,fill:i%2?C.rust:C.amber}),path(`M${xx-11} ${yy-14}Q${xx} ${yy-39} ${xx+11} ${yy-14}`,C.ink,2),dot(xx,yy-16,7,C.reed)];return g;}),'Exactly six baskets of river fungi accompany the woman; source opening detail.'));
 q.add(object('research-case',261,374,[n('rect',{x:-55,y:-25,width:110,height:50,rx:8,fill:C.cream}),path('M-21 -25V-37H21V-25',C.amber,6),n('rect',{x:-14,y:-8,width:28,height:17,rx:3,fill:C.rust}),path('M-39 -24V24M39 -24V24',C.amber,3)],'Mara holds the sealed research case above her head; it later rests on the rescue deck.'));
 q.add(object('boat-front',690,483,[n('path',{d:'M-423 -16Q-210 4 413 -16L337 47Q12 81 -332 48Z',fill:C.rust}),path('M-371 19Q2 50 365 12',C.amber,5),n('ellipse',{cx:260,cy:19,rx:23,ry:29,fill:C.ink}),n('ellipse',{cx:260,cy:19,rx:11,ry:17,fill:C.rust})],'The continuous hull masks lower legs and supports all five people after the rescue.'));
 q.add(object('flood-water',600,548,[n('path',{d:'M-560 -36Q-455 -58 -359 -24Q-270 -3 -177 -20Q-67 -39 21 -17Q160 4 282 -21Q414 -47 552 -17V40H-560Z',fill:C.water}),path('M-498 -9Q-438 9 -387 -6M-161 8Q-81 21 -14 10M186 12Q278 0 343 11',C.ice,4)],'Water moves through the flooded terrace and around the hull.'));
 const boatIds=['boat-back','sio','older-passenger','child-passenger','fungus-seller','wrist-wrap','thermal-cloth','six-baskets','boat-front'];
 for(const id of boatIds){let o=q.objects.find(o=>o.id===id),x=o.x;o.x+=315;q.move(id,2,x,o.y,3000);}
 gesture(q,'mara-raised',1,'worried');gesture(q,'sio',2,'determined','resolve');
 q.move('mara-raised',3,362,495,2100);q.move('research-case',3,362,306,2100);vanish(q,'mara-raised',3,2700);q.actions.push({actor:'research-case',action:'moveTo',beat:3,offsetMs:2350,x:421,y:431,durationMs:1300});gesture(q,'sio',3,'determined','invite');
 gesture(q,'mara-aboard',4,'surprised','reflect');gesture(q,'sio',5,'curious','question');gesture(q,'mara-aboard',6,'curious','release');q.move('flood-water',3,619,548,2900);
 q.add(object('rescue-grip',468,386,[path('M0 0Q-20 5 -35 23Q-56 38 -74 25',C.deep,12),dot(-74,25,7,'#EFC7AE')],'Sio’s hand visibly reaches Mara’s field coat as she reaches the bow.'));appear(q,'rescue-grip',3,1900);vanish(q,'rescue-grip',3,3500);appear(q,'sio.armL',1);vanish(q,'sio.armL',3);appear(q,'sio.armL',4);
 scenes[0].visual=q.finish('The finite opening is enacted as Mara’s rescue into a crowded boat, preserving the research case, distinct passengers and different attentional habits.');
}
// Greenhouse conversation: supported bodies and objects, genuine change of scale.
{
 const q=stageAuthor(),{n,path,dot,object,text}=q;
 q.add(object('greenhouse',616,470,[n('path',{d:'M-400 21V-210Q0 -424 400 -210V21Z',fill:C.ice}),n('path',{d:'M-388 -202Q-205 -302 0 -305V13H-388Z',fill:C.amber}),n('path',{d:'M0 -305Q205 -302 388 -202V13H0Z',fill:C.deep}),n('path',{d:'M-403 12H403V40H-403Z',fill:C.reed}),path('M-392 10V-209Q0 -419 392 -209V10M0 -302V10',C.cream,10)],'A real greenhouse in the dusk belt mediates heat, cold and living plants.'));
 q.add(object('heat-shutter',407,194,[n('path',{d:'M-178 8Q-57 -42 132 -37L154 -8Q-29 -21 -166 42Z',fill:C.rust})],'Heat shutters move over the sunward glass in the opening greenhouse scene.'));q.move('heat-shutter',1,441,212,2700);
 q.add(object('hospice-ridge',894,263,[...[-72,-29,22,60].map((x,i)=>n('rect',{x,y:-i%2*18,width:25,height:94,rx:3,fill:C.ice})),path('M-91 94H112',C.cream,6)],'The hospice ridge sits beyond the nightward greenhouse glass.'));
 reeds(q,'left-plants',221,463,.9);reeds(q,'right-plants',1013,464,.85);
 seated(q,'mara',343,530,'person-11-neutral',C.rust,.7);seated(q,'sio',886,530,'person-07-neutral',C.deep,.7);
 table(q,'culture-table',615,460,352);cup(q,'tea',753,446,1);
 q.add(object('culture-tray',555,446,[n('path',{d:'M-78 -12H78L64 5H-65Z',fill:C.cream}),n('rect',{x:-56,y:-53,width:40,height:40,rx:8,fill:C.reed}),n('rect',{x:9,y:-68,width:39,height:55,rx:8,fill:C.ice}),path('M-33 -52V-20M29 -64V-20',C.amber,3)],'Mara’s reed cultures stand on their tray and table.'));
 q.add(object('folded-memory',607,307,[n('path',{d:'M-90 -20Q-35 -87 0 -21Q35 41 86 -21',fill:'none',stroke:C.reed,'stroke-width':17,'stroke-linecap':'round'}),n('path',{d:'M-69 8Q-12 72 16 8Q48 -53 88 10',fill:'none',stroke:C.amber,'stroke-width':12,'stroke-linecap':'round'}),n('rect',{x:-99,y:62,width:198,height:39,rx:4,fill:C.cream}),text('Memory reed',0,89,28,C.ink)],'A simplified fictional folded-memory demonstration, not a real genetic mechanism.'));appear(q,'folded-memory',3);gesture(q,'mara',3,'inspired','explain');gesture(q,'sio',3,'curious','reflect');
 gesture(q,'mara',4,'happy','invite');gesture(q,'sio',4,'happy','release');gesture(q,'sio',5,'curious','question');gesture(q,'mara',6,'curious','reflect');vanish(q,'folded-memory',6);
 scenes[1].visual=q.finish('Two differently attentive people share a greenhouse conversation, with tea, reed cultures, heat shutters and a visible hospice ridge grounding the book’s intimate questions.');
}
// Higher scale: particular bowls first, then a working interval under load.
{
 const q=stageAuthor(),{n,path,dot,object,text}=q;
 table(q,'examination-table',641,472,510);storyPerson(q,'soren',248,527,{identity:'person-01-neutral',coat:C.amber,scale:.72});
 q.add(object('pheron',1022,504,[...Array.from({length:5},(_,i)=>n('path',{d:`M${-75+i*14} ${-280+i*25}L${44+i*5} ${-315+i*34}L${65-i*4} ${-42+i*5}L${-42+i*3} ${-18-i*10}Z`,fill:[C.plum,C.ice,C.deep,C.plum,C.reed][i],opacity:.65})),...[-230,-162,-94].map((yy,i)=>path(`M-26 ${yy}Q12 ${yy-28} 43 ${yy+10}`,C.cream,3))],'Pheron’s source-described tall arrangement of translucent planes contains slower thought versions; no invented human anatomy.'));
 q.add(object('reconstructed-terrace',642,231,[n('path',{d:'M-232 40Q-55 -3 233 40V72H-232Z',fill:C.water}),path('M-215 15H215M-171 15V-61M-75 15V-73M75 15V-73M171 15V-61',C.amber,9),...[-159,-65,75].map(xx=>n('path',{d:`M${xx} 5Q${xx+26} -43 ${xx+52} 5`,fill:'none',stroke:C.cream,'stroke-width':4}))],'Asterion reproduces an Iria river terrace; a fictional reconstruction, not a proven psychological mechanism.'));q.label('reconstruction-label','Reconstructed Iria',642,155,29);
 bowl(q,'particular-bowl',450,427,C.deep,true,1.05);bowl(q,'replica-1',643,434,C.rust,false,.85);bowl(q,'replica-2',753,434,C.rust,false,.85);
 q.add(object('travel-towel',422,460,[n('path',{d:'M-73 -6H86L57 16H-81Z',fill:C.ice})],'The traveller carries his own bowls in a towel.'));
 gesture(q,'soren',1,'curious','reflect');q.move('replica-1',2,663,434,1700);q.move('replica-2',2,770,434,1700);gesture(q,'soren',2,'worried','question');q.move('particular-bowl',3,418,427,2200);q.move('soren',3,330,527,2200);gesture(q,'soren',3,'determined','resolve');
 const first=q.objects.map(o=>o.id);first.forEach(id=>vanish(q,id,3,5000));
 table(q,'knot-bench',602,485,710);
 q.add(object('working-knot',598,324,[path('M-215 0H-76C-26 0 -45 -56 0 -57C73 -57 70 39 2 39C-63 39 -67 -28 3 -28H190',C.amber,14),path('M-215 24H-104C-59 24 -39 64 18 59C86 55 65 -44 6 -43',C.reed,10)],'A working knot preserves a genuinely visible movable interval; explicit omis metaphor from the reader guide.'));
 q.objects.at(-1).visual.anchors.right=[190,-28];q.objects.at(-1).visual.anchors.left=[-215,0];
 q.add(object('load',821,410,[n('rect',{x:-29,y:-30,width:58,height:60,rx:7,fill:C.plum}),n('circle',{cx:0,cy:-25,r:8,fill:C.cream}),text('Load',0,11,21,C.ink)],'A small load makes commitment and retained slack visible.'));q.objects.at(-1).visual.anchors.top=[0,-30];
 q.connections.push({id:'load-line',from:{node:'working-knot',anchor:'right'},to:{node:'load',anchor:'top'},color:C.amber,width:9,meaning:'The committed line bears a load while the knot retains an interval.'});q.actions.push({actor:'load-line',action:'connection.draw',beat:4,durationMs:1100});
 hand(q,'open-hand',384,311,C.rust);hand(q,'commit-hand',879,320,C.reed);for(const id of ['knot-bench','working-knot','load','open-hand','commit-hand'])appear(q,id,4,0);
 q.move('load',5,821,444,2500);q.move('open-hand',5,405,317,2300);q.move('commit-hand',5,901,351,2300);
 q.label('interval-label','A movable interval',596,224,30);appear(q,'interval-label',5);q.move('open-hand',6,384,311,1800);q.move('commit-hand',6,879,320,1800);
 scenes[2].visual=q.finish('A traveller’s particular cracked bowl confronts an averaged reconstruction, then the scene clears for a working knot retaining an interval while bearing a load.');
}
// Reading destination: one unfolding triptych with connected, distinct settings.
{
 const q=stageAuthor(),{n,path,dot,object,text}=q;
 q.add(object('reading-support',605,507,[n('path',{d:'M-445 -21H445L470 8H-470Z',fill:C.amber}),q.tint(path('M-410 8V58M410 8V58',C.ink,10),'#a3b7ca')],'A continuous reading table supports the triptych.'));
 q.add(object('triptych',606,363,[n('path',{d:'M-425 -140Q-285 -159 -146 -118Q0 -154 146 -118Q285 -159 425 -140V138Q280 119 146 151Q0 116 -146 151Q-279 119 -425 138Z',fill:C.deep}),n('path',{d:'M-416 -149Q-285 -160 -151 -125V138Q-282 109 -416 128Z',fill:C.cream}),n('path',{d:'M-140 -125Q0 -160 140 -125V139Q0 108 -140 139Z',fill:C.cream}),n('path',{d:'M151 -125Q285 -160 416 -149V128Q282 109 151 138Z',fill:C.cream}),path('M-146 -118V143M146 -118V143',C.amber,4)],'One unfolding reading volume preserves three complete but related narrative spirals.'));
 q.label('guide-tab','Reader’s Compass',600,153,32);q.add(object('reading-marker',221,259,[n('path',{d:'M-23 -39H23V52L0 36L-23 52Z',fill:C.rust})],'The reading marker points to the finite beginning.'));
 q.add(object('finite-window',310,395,[n('path',{d:'M-87 37V-68Q0 -143 87 -68V37Z',fill:C.ice}),path('M-87 28H87M0 -105V25',C.amber,7),n('path',{d:'M-88 36H88V58H-88Z',fill:C.reed})],'First spiral: finite lives in the greenhouse.'));storyPerson(q,'mara-mini',277,438,{identity:'person-11-neutral',coat:C.rust,scale:.32});storyPerson(q,'sio-mini',357,438,{identity:'person-07-neutral',coat:C.deep,scale:.32});
 q.add(object('observer-window',607,390,[n('path',{d:'M-78 44H85L106 60H-94Z',fill:C.amber}),...[-52,0,51].map((xx,i)=>n('path',{d:`M${xx-18} -82L${xx+25} -96L${xx+14} 22L${xx-15} 33Z`,fill:[C.plum,C.ice,C.deep][i],opacity:.65}))],'Second spiral: observation across unequal power, with Pheron’s planar form.'));bowl(q,'traveller-mini-bowl',603,414,C.deep,true,.5);
 q.add(object('saphene-window',907,420,[...[-66,-15,42].flatMap((xx,i)=>[path(`M${xx} 20V${-82+i*18}`,C.plum,7),n('path',{d:`M${xx-23} ${-60+i*10}L${xx+4} ${-105+i*10}L${xx+29} ${-54+i*10}Z`,fill:[C.reed,C.ice,C.amber][i]}),path(`M${xx} 18Q${xx-42} 45 ${xx+29} 60`,C.reed,6)]),path('M-87 18Q0 49 89 18',C.amber,5)],'Third spiral: Saphene’s mineral roots carry civic signals and legal gardens model effects; no later outcome is shown.'));
 storyPerson(q,'lio-mini',871,461,{identity:'person-13-neutral',coat:C.plum,scale:.27});storyPerson(q,'esen-mini',966,461,{identity:'person-04-neutral',coat:C.reed,scale:.27});for(const id of ['lio-mini','esen-mini'])appear(q,id,5);gesture(q,'lio-mini',5,'curious','explain');gesture(q,'esen-mini',5,'curious','reflect');q.add(object('legal-garden-mini',988,449,[n('path',{d:'M-27 -10H27L22 9H-22Z',fill:C.rust}),path('M-12 -10V-31M8 -10V-27',C.reed,3),dot(-12,-32,7,C.amber),dot(8,-29,6,C.plum)],'A miniature living legal garden remains a particular activity beside the civic root network.'));appear(q,'legal-garden-mini',5);
 q.label('finite-label','Finite lives',307,266,27);q.label('observer-label','Unequal power',605,266,27);q.label('universe-label','A capable universe',905,266,26);
 for(const id of ['finite-label','observer-label','universe-label'])q.objects.find(o=>o.id===id).visual.children[0].attrs.fill=C.ink;
 for(const id of ['observer-window','traveller-mini-bowl','observer-label'])appear(q,id,3);for(const id of ['saphene-window','universe-label'])appear(q,id,5);
 gesture(q,'mara-mini',2,'curious','explain');gesture(q,'sio-mini',2,'curious','reflect');q.move('reading-marker',3,487,259,2400);q.move('reading-marker',5,780,259,2400);q.move('reading-marker',6,221,259,2700);
 scenes[3].visual=q.finish('The introduction ends at an actual reading destination: three connected narrative windows change power and scale, while the marker returns to the finite first chapter.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');console.log('Four distinct enacted Tao compositions authored.');
