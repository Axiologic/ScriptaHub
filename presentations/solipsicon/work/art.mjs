import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const timing=JSON.parse(fs.readFileSync(new URL('../qa/audio-timing.json',import.meta.url))).lines;
for(const [index,s]of scenes.entries()){
 const a=stageAuthor(),{n,path,text,tint,dot}=a,c={plum:'#796397',mist:'#b8ccc2',teal:'#3f8796',coral:'#c98464',gold:'#d4a448',ink:'#304953',paper:'#ede2cb'};
 const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
 const fill=(d,col,night=col)=>tint(n('path',{d,fill:col}),night);
 const rect=(x,y,w,h,col,night=col,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:col}),night);
 const label=(v,x,y,size=28,col=c.ink)=>text(v,x,y,size,col);
 const action=(id,beat,verb,props={})=>a.actions.push({actor:id,action:verb,beat,durationMs:1500,...props});
 const express=(id,e,beat)=>action(id,beat,'character.express',{emotion:e,durationMs:850});
 const gesture=(id,beat,g)=>storyGesture(a,id,beat,g,2300);
 const look=(id,target,beat)=>action(id,beat,'lookAt',{target,durationMs:850});
 const person=(id,x,y,coat,identity,scale=.85,seated=false)=>{storyPerson(a,id,x,y,{coat,identity,scale,seated,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;};
 const nest=(id,x,y,k=1,cutaway=false)=>{
  obj(id+'-shell',x,y,[fill(cutaway?'M-181 71Q-244 -48 -150 -124Q-95 -192 17 -142Q166 -181 202 -44L174 -1Q147 -89 52 -93Q-50 -125 -118 -67Q-169 -24 -132 52Z':'M-192 4Q-187 -150 -30 -155Q85 -192 170 -86Q222 7 148 114Q42 195 -77 140Q-189 125 -192 4Z',c.mist,'#789a9e'),...(!cutaway?[fill('M-168 -1Q-151 -114 -25 -121Q73 -153 144 -69Q183 0 120 91Q36 149 -62 113Q-161 91 -168 -1Z','#dbe0cb','#4e6875')]:[])],'A simplified projection of a support membrane, not a documentary extra-dimensional body',k);
  if(!cutaway){const shell=a.objects.find(o=>o.id===id+'-shell').visual.children;shell[0].attrs.d+=' M-168 -1Q-151 -114 -25 -121Q73 -153 144 -69Q183 0 120 91Q36 149 -62 113Q-161 91 -168 -1Z';shell[0].attrs['fill-rule']='evenodd';shell.splice(1);}
  obj(id+'-core',x,y,[fill('M-54 13Q-89 -26 -33 -71Q-6 -103 28 -53Q87 -30 46 12Q96 68 25 64Q-14 110 -35 52Q-84 68 -54 13Z',c.plum,'#b5a4cd'),path('M-37 -19Q3 -68 30 -14Q-31 15 22 44',c.coral,10)],'The warm core is distributed through supported folds; no invented stable human mouth',k);
  const spots=[[-115,-34],[-72,-103],[39,-113],[117,-67],[120,34],[22,111],[-94,88]];
  for(const [j,[dx,dy]]of spots.entries()){
   const node=id+'-node-'+j;obj(node,x+dx*k,y+dy*k,[n('ellipse',{cx:0,cy:0,rx:19,ry:24,fill:[c.plum,c.teal,c.coral][j%3]}),n('ellipse',{cx:-3,cy:-5,rx:7,ry:11,fill:'#e2d3af'})],'One of the seven source-described growth nodes in a visual projection',k);
   a.objects.find(o=>o.id===node).visual.anchors.center=[0,0];a.objects.find(o=>o.id===id+'-core').visual.anchors.center=[0,0];
   a.connections.push({id:id+'-support-'+j,from:{node:id+'-core',anchor:'center'},to:{node,anchor:'center'},color:j%2?c.teal:c.plum,width:8*k,meaning:'A support filament stays attached to the moving growth node'});
  }
  return spots;
 };
 const window=(id,x,y,w=490,h=285)=>{
  obj(id,x,y,[rect(-w/2,-h,w,h,c.teal,'#8aafb9',8),rect(-w/2+13,-h+13,w-26,h-25,'#d0dfdf','#b7cfd0',3),fill(`M${-w/2+13} -107Q-103 -138 -10 -105T${w/2-13} -108V-12H${-w/2+13}Z`,'#84aebb','#6e96a8'),fill(`M${-w/2+13} -97Q-94 -64 31 -97T${w/2-13} -81V-12H${-w/2+13}Z`,'#a9c6c4','#7eaaaa'),path(`M${-w/2-7} 1H${w/2+7}`,c.coral,15)],'A single lake-facing clinic window; the reflected rain is on the glass, not a second weather system');
 };
 if(index===0){
  nest('kael',374,332,.97);
  obj('feeding',212,190,[path('M-75 43Q-93 -49 -12 -49H70Q107 -49 111 2',c.teal,20),path('M-75 43Q-88 -38 -12 -38H70',c.mist,5)],'A feeding conduit belongs to the supporting system');
  obj('leak',512,250,[path('M0 -29L-15 -3L7 12L-12 32','#f0d8b8',6)],'A fissure limits the child’s own support');a.reveal('leak',2);
  obj('loom-console',327,531,[rect(-107,-26,214,42,c.paper,'#cfdbd3',5),label('Support required',0,3,25)],'Continued support is a material condition, not a free choice');a.reveal('loom-console',2);
  window('human-view',923,427,322,207);
  person('human-observer',894,531,c.plum,'person-03-neutral',.83);obj('human-table',1022,445,[rect(-79,-7,164,15,c.plum,'#ab9bc7'),path('M-66 8V94M68 8V94',c.coral,10)],'A separate human viewpoint exists within an ordinary material room');
  a.reveal('human-view',3);a.reveal('human-observer',3);a.reveal('human-table',3);
  a.move('kael-node-0',2,247,288,2300);a.move('kael-node-4',2,506,375,2300);look('human-observer','human-view',3);express('human-observer','worried',4);gesture('human-observer',5,'reflect');a.move('kael-node-4',6,493,367,2400);gesture('human-observer',6,'release');
 } else if(index===1){
  // Macro cutaway: follow a failing supply path instead of repeating the overview.
  nest('cutaway',699,337,1.14,true);
  obj('conduit',339,246,[path('M-213 72H-136Q-84 72 -84 18V-31H190',c.teal,34),path('M-210 61H-133Q-95 60 -95 16V-41H178','#a7ccc6',6),rect(-194,51,37,43,c.coral),path('M-145 59L-126 75L-140 92',c.paper,7)],'The visible leak and conduit carry a failing supply toward the projected body');
  obj('meter',257,404,[rect(-127,-60,254,109,c.paper,'#d7ded2',8),label('Soma-Nectar',0,-19,28),label('31.8%',0,23,39),rect(-104,38,208,6,'#adad9d'),rect(-104,38,67,6,c.plum)],'The source’s opening supply level, not an invented success score');
  for(let j=0;j<3;j++){obj('mist-'+j,204+j*9,331,[fill('M-5 -12Q17 -23 16 -4Q19 11 4 12Q-10 8 -5 -12Z',j%2?c.plum:c.mist)],'Lost supply dissipates through a visible fissure',.6+j*.12);a.reveal('mist-'+j,1);a.move('mist-'+j,2,188+j*20,383+j*12,2600);a.hide('mist-'+j,3);}
  a.move('cutaway-node-2',2,757,190,2600);a.move('cutaway-node-6',2,576,450,2600);
  obj('instruction',993,462,[rect(-108,-49,216,87,c.paper,'#d0dbd3',6),label('Awaiting result',0,-7,27),path('M-64 16H60',c.plum,5)],'The Loom responds to results rather than the child’s observations');a.reveal('instruction',3);
  obj('world-window',440,469,[rect(-94,-45,188,80,c.teal,'#8aafb9',5),rect(-84,-35,168,60,'#bed0d0','#bdcccc'),path('M-61 26V-15M-61 1H49M49 1V25',c.coral,8)],'An observation opening keeps another lived world present beyond the support apparatus');a.reveal('world-window',4);
  a.move('cutaway-node-0',5,551,286,2400);a.move('cutaway-node-2',6,747,210,2200);
 } else if(index===2){
  window('clinic-window',387,407,490,270);
  obj('floor',672,534,[fill('M-516 0H457L489 26H-529Z','#c3d4ca','#4f6c73')],'The clinic’s ordinary shared floor remains stable during the perceptual disturbance');
  person('mara',817,545,c.plum,'person-03-neutral',.91,true);
  person('tomas',1040,513,c.teal,'person-20-neutral',.74,true);
  obj('mara-table',803,443,[fill('M-115 -5H103L123 15H-137Z',c.coral),path('M-112 15V106M87 15V106',c.coral,12)],'A real table supports Mara’s orange and peel');
  obj('orange',755,431,[dot(0,-16,19,c.gold),path('M-14 -26Q-3 -40 7 -26',c.coral,3),fill('M-2 6Q29 -16 43 7Q25 32 61 28L59 36Q16 44 26 17Q31 10 -2 15Z',c.gold)],'Mara’s ordinary sensory anchor is a peeled orange, explicitly in the source');
  obj('puzzle-table',1052,416,[rect(-91,-5,184,15,c.coral),path('M-72 10V99M77 10V99',c.coral,10)],'Tomas’s unfinished puzzle grounds the adjacent response');
  obj('puzzle',1037,406,[fill('M-51 -18H-25Q-28 -36 -14 -34Q2 -30 -7 -18H19V-1Q36 -13 35 4Q35 18 19 11V24H-13Q-5 7 -20 9Q-32 12 -26 24H-51Z',c.teal),fill('M26 -23H54V0H27Q43 -10 26 -23Z',c.plum)],'Large puzzle pieces belong to the man at the next table');
  obj('rain-key',384,450,[label('Outside',-107,0,24,'$ink'),label('Reflection',133,0,24,'$ink')],'Two labels locate observed rain and its reflection on the same pane');
  // Each batch travels one way, then fades before it could leave the pane.
  // New objects provide the next drops; no visible backward reset is possible.
  for(let beat=1;beat<=6;beat++){
   const spoken=timing.find(t=>t.id===s.id+'-line-'+beat).durationMs;
   const travel=Math.min(1850,Math.max(1200,spoken/2-400));
   for(let batch=0;batch<2;batch++)for(const kind of ['outside','reflection']){
    if(kind==='reflection'&&beat===1)continue;
    const id=`${kind}-b${beat}-${batch}`,x=kind==='outside'?278:514,y=kind==='outside'?182:372,sign=kind==='outside'?1:-1,offset=250+batch*(travel+550),col=kind==='outside'?'#447d9e':'#95698f';
    obj(id,x,y,Array.from({length:7},(_,j)=>path(`M${-77+j*24} ${sign*(j%3)*20}l-5 15`,col,4)),kind==='outside'?'Actual exterior droplets travel downward':'Impossible reflected droplets visibly travel upward');
    action(id,beat,'appear',{offsetMs:offset,durationMs:220});action(id,beat,'moveTo',{x,y:y+sign*125,offsetMs:offset+100,durationMs:travel});action(id,beat,'disappear',{offsetMs:offset+travel+150,durationMs:300});
   }
  }
  look('mara','orange',1);look('mara','clinic-window',2);express('mara','surprised',2);gesture('mara',2,'reflect');look('mara','orange',3);express('mara','worried',3);look('tomas','mara',4);express('tomas','skeptical',4);gesture('tomas',4,'question');look('mara','clinic-window',5);gesture('mara',5,'question');express('mara','curious',6);gesture('mara',6,'release');
 } else {
  // A deliberate juxtaposition of distinct strands, not a claim that Kael enters Mara.
  nest('closing-body',345,332,.86,true);
  obj('closing-conduit',229,212,[path('M-115 43Q-139 -51 -30 -51H62',c.teal,25),path('M-86 39Q-105 -20 -38 -20',c.mist,7)],'The child’s remaining support is still physically necessary');
  window('closing-window',920,382,316,226);
  person('mara-close',803,546,c.plum,'person-03-neutral',1.12,true);
  obj('close-table',922,444,[fill('M-112 -5H91L115 15H-132Z',c.coral),path('M-100 15V107M87 15V107',c.coral,13)],'The ending returns to Mara’s situated experience from a closer angle');
  obj('close-orange',903,429,[dot(0,-18,22,c.gold),fill('M13 4Q41 -12 52 9Q31 36 64 26L71 33Q19 52 39 13L12 13Z',c.gold)],'An ordinary orange remains the unresolved scene’s sensory anchor');
  obj('opening-tag',321,517,[rect(-134,-25,268,44,c.paper,'#d3ddd4',5),label('Those Who Press Down',0,4,25)],'The requested reading route begins with the actual source opening');
  look('mara-close','close-orange',1);gesture('mara-close',2,'reflect');a.move('closing-body-node-6',2,252,419,2300);look('mara-close','closing-window',3);express('mara-close','worried',3);gesture('mara-close',4,'question');a.move('closing-body-node-3',5,459,258,2500);express('mara-close','curious',6);gesture('mara-close',6,'release');
 }
 s.visual=a.finish(s.adaptation.composition+' Nonhuman forms are simplified projections. Juxtaposed human and child views are distinct narrative strands, not an identification of the clinic operator. All actions preserve the protected discoveries and outcomes.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
