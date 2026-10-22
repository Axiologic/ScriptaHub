// Book-owned staging for The Unfinished World: a tiled globe with open seams, a half-built
// bridge of commitment, and frontiers from an unmapped mind to a mostly-night universe.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),file=path.join(root,'work/scenes.json'),scenes=JSON.parse(fs.readFileSync(file,'utf8'));
// Visual bible palette (cover): amber dawn, coral, deep night navy, plus the cover's tile colours.
const C={amber:'#ffb35c',coral:'#c8604f',navy:'#0d1233',navyNight:'#222b62',rimNight:'#6d79bd',seam:'#8d97cf',teal:'#2fa79a',green:'#8cc46a',blue:'#4a8fd6',gold:'#f0b43c',cream:'#fbf1de',stone:'#e9dcc6',ground:'#e7c6a4',groundNight:'#2a3160'};
const TILES=[C.amber,C.teal,C.coral,C.green,C.blue,C.gold];

function compose(i){
 const q=stageAuthor(),{n,path:p,dot}=q;
 const night=(node,attrs)=>({...node,themeAttrs:{...node.themeAttrs,night:{...node.themeAttrs?.night,...attrs}}});
 const navy=(type,attrs)=>night(n(type,{...attrs,fill:C.navy}),{fill:C.navyNight});
 const line=(d,color,w=6,nightColor)=>nightColor?night(p(d,color,w),{stroke:nightColor}):p(d,color,w);
 // The player normalises path length to 1, so path dashes are given as fractions of an approximate length.
 const dashed=(d,color,w=3,dash='7 6',length=400)=>n('path',{d,fill:'none',stroke:color,'stroke-width':w,'stroke-dasharray':dash.split(' ').map(v=>(v/length).toFixed(4)).join(' '),'stroke-linecap':'round'});
 const words=(s,x,y,size=28,color='$ink',anchor='middle',weight)=>n('text',{x,y,'font-size':size,'font-weight':weight??(size>=32?700:600),'letter-spacing':-.3,'text-anchor':anchor,fill:color},s);
 const put=(id,x,y,kids,meaning,beat,offsetMs=250,scale=1,durationMs=900)=>{q.add(q.object(id,x,y,kids,meaning,scale));if(beat)q.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs});return id;};
 const hide=(id,beat,offsetMs=250,durationMs=900)=>q.actions.push({actor:id,action:'disappear',beat,offsetMs,durationMs});
 const move=(id,beat,x,y,offsetMs=300,durationMs=1500)=>q.actions.push({actor:id,action:'moveTo',beat,x,y,offsetMs,durationMs});
 const express=(id,beat,emotion,offsetMs=200)=>q.actions.push({actor:id,action:'character.express',emotion,beat,offsetMs,durationMs:700});
 const gesture=(id,beat,g,offsetMs=650,durationMs=1900)=>q.actions.push({actor:id,action:'character.gesture',gesture:g,beat,offsetMs,durationMs});
 const person=(id,x,y,{identity,coat,scale},beat,offsetMs=250)=>{storyPerson(q,id,x,y,{identity,coat,scale,ink:C.navy});if(beat)q.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs:900});return id;};
 // Orthographic tiled globe: filled tiles are made, dashed tiles are still open seams.
 const globe=(r,fill,seed=3)=>{
  const tilt=22*Math.PI/180,kids=[navy('circle',{cx:0,cy:0,r:r+r*.04})],cells=[];
  const proj=(lat,lon)=>{const la=lat*Math.PI/180,lo=lon*Math.PI/180,x=Math.cos(la)*Math.sin(lo),y=Math.sin(la),z=Math.cos(la)*Math.cos(lo);return{X:r*x,Y:-r*(y*Math.cos(tilt)-z*Math.sin(tilt)),Z:y*Math.sin(tilt)+z*Math.cos(tilt)};};
  let k=0;
  for(let lat=-80;lat<80;lat+=20)for(let lon=-90;lon<90;lon+=20){
   const ring=[[lat,lon],[lat,lon+10],[lat,lon+20],[lat+10,lon+20],[lat+20,lon+20],[lat+20,lon+10],[lat+20,lon],[lat+10,lon]].map(([a,b])=>proj(a,b));
   if(ring.some(v=>v.Z<.08))continue;
   const cx=ring.reduce((s,v)=>s+v.X,0)/ring.length,cy=ring.reduce((s,v)=>s+v.Y,0)/ring.length;
   const pts=ring.map(v=>`${(cx+(v.X-cx)*.84).toFixed(1)},${(cy+(v.Y-cy)*.84).toFixed(1)}`).join(' ');
   const noise=(((lat*7+lon*13+seed*31)%17+17)%17)/17-.5,u=(lon+90)/180,v=(lat+80)/160,made=.62*u+.48*v+.22*noise<fill;
   kids.push(made?n('polygon',{points:pts,fill:TILES[(k++)%TILES.length]}):n('polygon',{points:pts,fill:'none',stroke:C.seam,'stroke-width':Math.max(1.5,r/70),'stroke-dasharray':r>80?'6 5':'3 3'}));
   if(!made)cells.push({x:cx,y:cy,pts});
  }
  return {kids,cells};
 };
 const tile=(color,icon,s=56)=>[n('rect',{x:-s/2,y:-s/2,width:s,height:s,rx:9,fill:color}),...icon];
 const icons={
  life:[n('path',{d:'M0 16C-16 4 -14 -14 2 -18C16 -10 14 8 0 16Z',fill:C.navy}),p('M0 16V22',C.navy,4)],
  mind:[n('path',{d:'M-14 14V2Q-18 -16 0 -18Q16 -18 15 -2L19 4L14 6V14Z',fill:C.navy})],
  machine:[p('M-12 -10L12 -10L0 12Z',C.navy,4),dot(-12,-10,6,C.navy),dot(12,-10,6,C.navy),dot(0,12,6,C.navy)],
  society:[n('path',{d:'M-18 18V-2L-8 -10V-18H2V18ZM6 18V-6H18V18Z',fill:C.navy})],
  culture:[p('M-6 12V-14L14 -18V8',C.navy,4),dot(-10,12,6,C.navy),dot(10,8,6,C.navy)],
  space:[dot(0,0,10,C.navy),n('ellipse',{cx:0,cy:0,rx:20,ry:6,fill:'none',stroke:C.navy,'stroke-width':3})]
 };

 if(i===0){
  // Beat 1: the diagnosis — the future shrunk to a tiny, mostly unlit globe before a tired inheritor.
  person('inheritor',172,548,{identity:'person-07-neutral',coat:C.coral,scale:.8},1,100);
  // Intrigue, not a wave: he turns his head up toward the shrunken globe with a curious face.
  express('inheritor',1,'curious');q.actions.push({actor:'inheritor',action:'lookAt',target:'small-future',up:true,beat:1,offsetMs:900,durationMs:900});
  const small=globe(46,.18,5);
  put('small-future',620,288,small.kids,'The future reduced to a small globe: very few tiles made, the frame almost empty',1,500,1,1100);
  // Beat 2: inherited achievements stand nearby, yet the mood stays weary (wry recognition).
  express('inheritor',2,'skeptical',600);
  const helix=[];const pts=s=>Array.from({length:17},(_,j)=>{const y=-90+j*11.25;return `${j?'L':'M'}${(30*Math.sin(j*.55+s)).toFixed(1)} ${y}`;}).join('');
  for(let j=1;j<16;j+=2){const y=-90+j*11.25,x=30*Math.sin(j*.55);helix.push(p(`M${x.toFixed(1)} ${y}L${(-x).toFixed(1)} ${y}`,C.seam,4));}
  helix.push(line(pts(0),C.teal,7),line(pts(Math.PI),C.coral,7),n('path',{d:'M-22 -40L22 -40',stroke:C.amber,'stroke-width':6,fill:'none','stroke-linecap':'round'}));
  put('gene-helix',372,300,helix,'Inherited power to edit genes: a DNA double helix with one edited rung highlighted',2,700);
  put('far-world',990,190,[dot(0,0,40,C.coral),n('ellipse',{cx:0,cy:0,rx:66,ry:15,fill:'none',stroke:C.amber,'stroke-width':6}),dot(-14,-12,9,'#e07f6c')],'Another world already reached by human machines',2,1500);
  put('probe',850,330,[n('path',{d:'M0 -26L10 -6V16L0 10L-10 16V-6Z',fill:C.blue}),n('path',{d:'M-10 10L-18 22H-6ZM10 10L18 22H6Z',fill:C.amber}),dot(0,-4,5,C.cream)],'A probe sent outward from Earth',2,1500,1,700);
  move('probe',2,925,236,2300,1600);
  put('probe-trail',880,290,[dashed('M-30 40Q0 0 45 -54',C.amber,4,'4 8',125)],'The route already travelled toward another world',2,2400,1,700);
  // Beat 3: hope that does not deny danger — climate, war and concentrated power stay in view.
  put('climate-risk',470,492,[n('rect',{x:-11,y:-44,width:22,height:66,rx:11,fill:C.cream,stroke:C.navy,'stroke-width':3}),dot(0,24,17,C.coral),n('rect',{x:-5,y:-30,width:10,height:52,fill:C.coral}),p('M18 -30H28M18 -14H28M18 2H28',C.navy,3)],'Climate risk: a thermometer with a high reading',3,1700);
  put('war-risk',620,492,[n('path',{d:'M0 -42L34 -30V0Q34 26 0 42Q-34 26 -34 0V-30Z',fill:C.stone,stroke:C.navy,'stroke-width':3}),p('M2 -40L-8 -14L8 2L-6 22L2 40',C.coral,5)],'War: a protective shield split by a crack',3,2600);
  put('power-risk',770,492,[n('rect',{x:-50,y:12,width:24,height:28,fill:C.seam}),n('rect',{x:26,y:12,width:24,height:28,fill:C.seam}),n('rect',{x:-58,y:22,width:12,height:18,fill:C.seam}),navy('rect',{x:-16,y:-46,width:32,height:86}),n('rect',{x:-6,y:-34,width:12,height:12,fill:C.amber})],'Concentrated power: one tower rising over small houses',3,3400);
  // Sober honesty: a steady face and an open hand presenting the dangers, no raised hand.
  express('inheritor',3,'neutral');gesture('inheritor',3,'explain',1700,2400);
  // Beat 4: the starting fact — the world is large and still unfinished, with open seams.
  hide('small-future',4,200,700);
  // Slightly smaller and higher so it clears the helix and the row of risk icons.
  const big=globe(126,.56,3);
  put('unfinished-world',660,270,big.kids,'The unfinished world: a large tiled globe at dawn, many tiles made and many still dashed and open',4,500,1,1300);
  const target=big.cells.reduce((best,c)=>Math.hypot(c.x+30,c.y+20)<Math.hypot(best.x+30,best.y+20)?c:best,big.cells[0]);
  put('new-tile',470,140,[n('rect',{x:-16,y:-16,width:32,height:32,rx:4,fill:C.amber})],'A new piece of the world being added by human effort',4,1600,1,600);
  move('new-tile',4,660+target.x,270+target.y,2200,1700);
  express('inheritor',4,'inspired');gesture('inheritor',4,'release',900);
  return q.finish('A tired inheritor faces a shrunken future globe, inherited gene editing and space probes, and the named dangers; then the world reappears large, tiled and still open at its seams.');
 }

 if(i===1){
  // Two cliffs and an unfinished bridge: hope as commitment toward a possible good across uncertainty.
  put('near-cliff',0,0,[night(n('path',{d:'M80 470H522L506 560H80Z',fill:C.ground}),{fill:C.groundNight})],'The ground where the present stands');
  put('far-cliff',0,0,[night(n('path',{d:'M858 470H1120V560H874Z',fill:C.ground}),{fill:C.groundNight})],'The far side where a possible good might grow');
  const slot=j=>522+j*56+28;
  put('bridge-plan',0,0,[0,1,2,3,4,5].map(j=>n('rect',{x:slot(j)-25,y:470,width:50,height:22,rx:3,fill:'none',stroke:'$ink','stroke-width':2.5,'stroke-dasharray':'6 5'})),'Dashed outlines: the bridge is planned but not yet built');
  put('bridge-made',0,0,[n('rect',{x:slot(0)-25,y:470,width:50,height:22,rx:3,fill:C.amber}),n('rect',{x:slot(1)-25,y:470,width:50,height:22,rx:3,fill:C.coral})],'Pieces already laid by earlier effort');
  put('possible-good',1002,470,[p('M0 0V-62',C.green,6),n('path',{d:'M0 -40Q-34 -48 -36 -76Q-6 -74 0 -44Z',fill:C.green}),n('path',{d:'M0 -54Q30 -66 38 -92Q6 -94 -2 -58Z',fill:C.teal}),dot(0,-66,8,C.amber)],'A possible good: a young plant in flower on the far side',1,250);
  put('uncertainty',1002,420,[dashed('M-92 18Q-100 -46 -40 -56Q-10 -96 34 -66Q96 -70 92 -10Q104 48 40 52H-50Q-104 54 -92 18Z','$ink',3,'5 7',640)],'Uncertainty surrounds the outcome: a dashed mist, not a guarantee',1,250);
  person('builder',330,470,{identity:'person-11-neutral',coat:C.blue,scale:.72},1,100);express('builder',1,'curious');
  // Prediction appears as a crystal ball and is set aside; commitment places the next piece.
  put('prophecy',230,190,[n('circle',{cx:0,cy:0,r:40,fill:'#c9d6f2',stroke:C.navy,'stroke-width':3}),n('path',{d:'M-14 -16Q-4 -26 10 -22',fill:'none',stroke:'#ffffff','stroke-width':5,'stroke-linecap':'round'}),n('path',{d:'M-30 34H30L38 52H-38Z',fill:C.coral})],'Prediction: a fortune-teller crystal ball promising an outcome',1,250,1,600);
  put('prophecy-refused',230,196,[p('M-52 52L52 -52',C.coral,7)],'Hope is not prediction: the forecast is struck through',1,1500,1,400);
  hide('prophecy',1,2400);hide('prophecy-refused',1,2400);
  put('next-tile',378,396,[n('rect',{x:-25,y:-11,width:50,height:22,rx:3,fill:C.teal})],'The next piece, carried by the person who commits to building',1,250);
  // The builder carries the piece across the pieces earlier effort laid, then sets it down in the next slot.
  q.actions.push({actor:'builder',action:'walkTo',x:592,beat:1,offsetMs:900,durationMs:1900});
  move('next-tile',1,640,396,900,1900);move('next-tile',1,slot(2),481,2900,1000);
  gesture('builder',1,'invite',2800,1500);
  // Beat 2: three tests — possible, valuable, influenceable — checked in turn.
  [['Possible',160,1800],['Valuable',222,2700],['Influenceable',284,3600]].forEach(([word,y,at],j)=>{
   put('test-'+j,850,y,[n('circle',{cx:0,cy:0,r:19,fill:'none',stroke:'$ink','stroke-width':3}),words(word,34,12,34,'$ink','start',600)],`Hope test ${j+1}: is the outcome ${word.toLowerCase()}?`,2,at,1,500);
   put('check-'+j,850,y,[p('M-9 0L-2 8L11 -8',C.coral,5)],`The ${word.toLowerCase()} test is answered before acting`,2,at+500,1,400);
  });
  // Analytical focus: the builder steps back to the solid ground and weighs the three questions.
  q.actions.push({actor:'builder',action:'walkTo',x:396,beat:2,offsetMs:300,durationMs:1500});
  express('builder',2,'curious',400);gesture('builder',2,'question',2000,1900);
  // Beat 3: awe widens the horizon, agency finds a lever, fellowship makes effort endurable.
  put('awe',600,220,[dashed('M-160 40Q30 -170 230 60',C.amber,4,'2 12',480),dot(-150,-60,5,C.amber),dot(-60,-96,7,C.amber),dot(50,-100,4,C.amber),dot(150,-70,6,C.amber),dot(250,-10,5,C.amber)],'Awe: the horizon widens into a starry arc above the work',3,250,1,1300);
  put('lever',506,470,[n('path',{d:'M-14 0L0 -24L14 0Z',fill:C.stone,stroke:C.navy,'stroke-width':3}),line('M-52 -8L76 -40',C.coral,7)],'Agency: a simple lever, a reachable way to lift the next piece',3,1700,1,600);
  put('lever-tile',580,418,[n('rect',{x:-25,y:-11,width:50,height:22,rx:3,fill:C.green})],'A piece lifted by the lever',3,1700,1,600);
  move('lever-tile',3,slot(3),481,2500,1200);
  person('companion-a',165,470,{identity:'person-04-neutral',coat:C.amber,scale:.7},3,3500);
  person('companion-b',285,470,{identity:'person-16-neutral',coat:C.teal,scale:.68},3,3700);
  express('companion-a',3,'happy',3600);express('companion-b',3,'relieved',3800);
  gesture('companion-b',3,'invite',4300,1700);express('builder',3,'inspired',1500);
  return q.finish('A builder sets aside a crystal-ball forecast and lays a bridge piece toward a possible good in uncertain mist; three tests are checked, then a widening starry arc, a lever and arriving companions extend the still-unfinished bridge.');
 }

 // Scene 3: frontiers from an unmapped mind to a mostly-night universe; failure made survivable; the prologue.
 const headD='M-62 96V40Q-96 6 -92 -40Q-84 -104 -14 -112Q56 -114 78 -50L76 -30L100 6L80 14L86 44Q82 64 52 60H30V96Z';
 const mindKids=[navy('path',{d:headD})];
 [[-56,-62,1],[-24,-62,1],[8,-62,0],[40,-62,0],[-56,-30,0],[-24,-30,1],[8,-30,0],[40,-30,0],[-40,2,0],[-8,2,0],[24,2,0]].forEach(([x,y,made],j)=>mindKids.push(made?n('rect',{x,y,width:26,height:26,rx:4,fill:TILES[j%TILES.length]}):n('rect',{x,y,width:26,height:26,rx:4,fill:'none',stroke:C.seam,'stroke-width':2,'stroke-dasharray':'4 4'})));
 put('mind',210,300,mindKids,'An unmapped mind: a head whose interior map has only a few filled regions',1,250);
 put('mind-label',210,466,[words('Unmapped mind',0,0,36,'$ink','middle',600)],'The first frontier named in the sentence',1,900,1,500);
 const starsIn=[[-40,-60],[30,-90],[60,20],[-70,40],[10,70],[90,-30]].map(([x,y],j)=>dot(x,y,j%2?3:4.5,'#e6e9ff'));
 put('night',975,290,[navy('circle',{cx:0,cy:0,r:135}),n('path',{d:'M-95 -96A135 135 0 0 0 -95 96Q-122 0 -95 -96Z',fill:C.amber}),...starsIn,dot(-150,-130,4,C.amber),dot(120,-140,5,C.amber),dot(150,120,4,C.amber)],'A universe still mostly night: a dark sphere of space lit only along one thin edge',1,2600);
 put('night-label',975,466,[words('Mostly night',0,0,36,'$ink','middle',600)],'The farthest frontier named in the sentence',1,3200,1,500);
 put('frontier-route',590,250,[dashed('M-250 40Q0 -150 250 40','$ink',3,'6 8',600)],'One continuous route of open frontiers',1,900,1,1200);
 [['life',C.green,-170,-10],['machine',C.teal,-60,-60],['society',C.amber,60,-60],['culture',C.coral,170,-10]].forEach(([k,color,x,y],j)=>put('frontier-'+k,590+x,250+y,tile(color,icons[k],52),`An open frontier between mind and cosmos: ${k}`,1,1200+j*350,1,600));
 // Beat 2: institutions hold a net beneath an intelligent attempt, so failure is survivable.
 for(const id of ['frontier-route','frontier-life','frontier-machine','frontier-society','frontier-culture','mind-label','night-label'])hide(id,2,150,700);
 const column=(id,x,beat,at)=>put(id,x,420,[n('rect',{x:-30,y:-122,width:60,height:16,rx:2,fill:C.stone,stroke:C.navy,'stroke-width':3}),n('rect',{x:-20,y:-106,width:40,height:200,fill:C.stone,stroke:C.navy,'stroke-width':3}),p('M-6 -96V84M6 -96V84',C.seam,2),n('rect',{x:-34,y:94,width:68,height:14,rx:2,fill:C.stone,stroke:C.navy,'stroke-width':3})],'An institution: a stone column holding one end of the safety net',beat,at,1,800);
 column('institution-left',450,2,900);column('institution-right',770,2,900);
 // A sagging net: rim and floor ropes share the column ends; strands stop exactly on the floor rope.
 const sag=(depth,t)=>380+4*depth*t*(1-t),net=[line('M470 380Q610 500 750 380',C.coral,5)];
 for(const t of [1/7,2/7,3/7,4/7,5/7,6/7]){const x=470+280*t;net.push(p(`M${x.toFixed(0)} ${sag(8,t).toFixed(0)}V${(sag(60,t)-2).toFixed(0)}`,C.coral,2.5));}
 net.push(line('M470 380Q610 446 750 380',C.coral,2.5),line('M470 380Q610 396 750 380',C.coral,4));
 put('safety-net',0,0,net,'A safety net strung between the institutions: intelligent failure becomes survivable',2,1300,1,800);
 put('attempt-goal',770,276,[n('rect',{x:-20,y:-20,width:40,height:40,rx:5,fill:'none',stroke:'$ink','stroke-width':3,'stroke-dasharray':'5 5'})],'The open goal the attempt reaches for',2,1300,1,600);
 // Teal coat keeps the attempter distinct from scene 2's blue-coated builder.
 person('attempter',450,298,{identity:'person-09-neutral',coat:C.teal,scale:.5},2,900);
 express('attempter',2,'determined',1000);
 // A leap with arms flung out reaching for the goal, then a fall into the net's floor.
 gesture('attempter',2,'question',1600,1500);move('attempter',2,560,232,1700,650);move('attempter',2,610,440,2350,750);
 // Beat 3: the person survives the fall and stands again; the goal stays open and no ending is drawn.
 // He climbs back out of the net up to the column top, one arm reaching, then stands resolved.
 express('attempter',3,'relieved',200);q.actions.push({actor:'attempter',action:'reach',beat:3,offsetMs:400,durationMs:1700});move('attempter',3,498,400,500,800);move('attempter',3,450,298,1300,800);gesture('attempter',3,'resolve',2400,1500);
 put('open-route',790,256,[dashed('M0 0Q10 -106 70 -136',C.amber,4,'3 9',180)],'The route continues upward past the open goal with no ending drawn',3,3000,1,900);
 // Beat 4: clear the stage for the prologue and a frontier chosen by the reader.
 for(const id of ['mind','night','institution-left','institution-right','safety-net','attempter','open-route','attempt-goal'])hide(id,4,150,700);
 const pageInk=C.navy;
 put('prologue-book',600,330,[n('path',{d:'M-300 -120Q-150 -150 0 -112Q150 -150 300 -120V140Q150 112 0 150Q-150 112 -300 140Z',fill:C.coral}),n('path',{d:'M-286 -112Q-146 -136 0 -100Q146 -136 286 -112V126Q146 102 0 136Q-146 102 -286 126Z',fill:C.cream}),p('M0 -100V136',C.coral,4),
  words('Prologue',-146,-50,24,C.coral,'middle',600),words('We Are Too Early',-146,0,32,pageInk,'middle',700),words('to Give Up',-146,40,32,pageInk,'middle',700),p('M-226 80H-66M-226 100H-96',C.seam,3)
 ],'The book opened at its prologue, We Are Too Early to Give Up, beside a choice of frontiers',4,900,1,1100);
 // Right-page frontier tiles are separate objects so one can be marked as chosen.
 [['mind',C.blue,100,-36],['life',C.green,196,-36],['machine',C.teal,100,56],['space',C.gold,196,56]].forEach(([k,color,dx,dy])=>put('choice-'+k,600+dx,330+dy,tile(color,icons[k],62),`A frontier the reader may choose: ${k}`,4,1500,1,700));
 put('chosen-frontier',600+196,330+56,[n('rect',{x:-40,y:-40,width:80,height:80,rx:13,fill:'none',stroke:C.amber,'stroke-width':6})],'One frontier chosen as the reader begins',4,3200,1,600);
 put('bookmark',600-146,330+128,[n('path',{d:'M-14 -26H14V30L0 18L-14 30Z',fill:C.amber})],'A bookmark at the prologue: the place to begin',4,2600,1,600);
 return q.finish('Frontiers run from an unmapped mind to a mostly-night universe; stone institutions hold a net so an attempt can fail and climb back; the book opens at its prologue with one frontier chosen.');
}
for(let i=0;i<scenes.length;i++)scenes[i].visual=compose(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
