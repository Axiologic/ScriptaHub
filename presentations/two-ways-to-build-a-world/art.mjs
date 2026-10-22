// Book-owned staging for Two Ways to Build a World: the cover's stepped pyramid
// (domination) and teal lattice (partnership) become working diagrams of cost,
// relationship dimensions, convertible status, commons rules and AI's two paths.
// Only scene.visual is rewritten; the reviewed spoken lines stay untouched.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),file=path.join(root,'work/scenes.json');
const scenes=JSON.parse(fs.readFileSync(file,'utf8'));
const bible=JSON.parse(fs.readFileSync(path.join(root,'work/visual-bible.json'),'utf8')).palette;
// Cover palette (visual bible) plus cover cream/rust shades; night variants keep contrast on a black stage.
const C={rust:bible.secondary,rustDeep:'#a9481f',rustSoft:'#d9825e',teal:bible.accent,tealNight:'#53b5aa',ink:bible.ink,pale:'#d3dfdd',cream:'#f3e6d0',crate:'#e6d3b3',gold:'#d99a2b',goldEdge:'#9c6a14',slate:'#34474d',slateNight:'#5b7680'};

function compose(i){
 const q=stageAuthor(),{n,path:p,text:t,dot,tint}=q;
 const act=(actor,action,beat,offsetMs=250,durationMs=900,extra={})=>q.actions.push({actor,action,beat,offsetMs,durationMs,...extra});
 const put=(id,x,y,nodes,meaning,{beat,at=250,dur=900,scale=1}={})=>{q.add(q.object(id,x,y,nodes,meaning,scale));if(beat)act(id,'appear',beat,at,dur);return id;};
 const gone=(id,beat,at=250,dur=650)=>act(id,'disappear',beat,at,dur);
 const slide=(id,beat,x,y,at=250,dur=1500)=>act(id,'moveTo',beat,at,dur,{x,y});
 const inkLine=(d,w=6)=>tint(p(d,C.ink,w),C.pale);
 const tealLine=(d,w=6)=>tint(p(d,C.teal,w),C.tealNight);
 const tealDot=(x,y,r)=>tint(dot(x,y,r,C.teal),C.tealNight);
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const word=(s,x=0,y=0,size=28,anchor='middle')=>{const node=t(s,x,y,size,'$ink');node.attrs['text-anchor']=anchor;return node;};
 const arrowHead=(x,y,dx,dy,color,s=13)=>{const L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L;return n('path',{d:`M${x} ${y}L${x-ux*s*1.6-uy*s} ${y-uy*s*1.6+ux*s}L${x-ux*s*1.6+uy*s} ${y-uy*s*1.6-ux*s}Z`,fill:color});};
 const express=(id,beat,emotion,at=150)=>act(id,'character.express',beat,at,700,{emotion});
 // Cover pyramid: a wide base band of many (cream dots) carrying narrowing tiers to one apex.
 const pyramidTiers=(apex='ball')=>[
  [rect(-150,-46,300,46,C.rustDeep),...Array.from({length:11},(_,k)=>dot(-125+25*k,-23,6,C.cream))],
  [rect(-120,-92,240,46,C.rust)],[rect(-94,-138,188,46,C.rustDeep)],[rect(-68,-184,136,46,C.rust)],[rect(-20,-220,40,36,C.rust)],
  apex==='chip'?[rect(-34,-282,68,62,C.slate,10),...[-18,0,18].map(x=>p(`M${x} -282V-294M${x} -220V-208`,C.gold,5)),t('AI',0,-240,28,C.cream)]:[tint(dot(0,-244,25,C.ink),C.pale)]];
 // Cover lattice: alternating rows of four and three linked nodes, built from the base upward.
 const rows=[[0,[-135,-45,45,135]],[-77,[-90,0,90]],[-154,[-135,-45,45,135]],[-231,[-90,0,90]]];
 const latticeRows=(from,to,linkBelow=false)=>{const out=[],nodes=[];
  for(let r=from;r<=to;r++){const [y,xs]=rows[r];xs.slice(1).forEach((x,k)=>out.push(tealLine(`M${xs[k]} ${y}H${x}`)));
   if(r>from||linkBelow){const [py,pxs]=rows[r-1];for(const x of xs)for(const px of pxs)if(Math.abs(px-x)===45)out.push(tealLine(`M${px} ${py}L${x} ${y}`));}
   for(const x of xs)nodes.push(tealDot(x,y,15));}
  return [...out,...nodes];};
 const coins=k=>Array.from({length:k},(_,j)=>n('ellipse',{cx:0,cy:-11-14*j,rx:34,ry:11,fill:C.gold,stroke:C.goldEdge,'stroke-width':2}));

 if(i===0){
  // Beat 1: the two cover architectures are built, tier by tier and row by row, and named.
  pyramidTiers().forEach((nodes,k)=>put('pyramid-'+k,380,452,nodes,k?'Domination tier '+k+': fewer positions as the structure narrows':'Base band of many people carrying the structure',{beat:1,at:250+300*k,dur:600,scale:.8}));
  put('lattice-low',830,452,latticeRows(0,1),'Partnership lattice: lower linked rows',{beat:1,at:1000,dur:800,scale:.8});
  put('lattice-high',830,452,latticeRows(2,3,true),'Partnership lattice: upper rows linked to the rows below',{beat:1,at:1700,dur:800,scale:.8});
  put('partnership',830,505,[word('Partnership',0,0,32)],'Partnership names the lattice',{beat:1,at:3900});
  put('domination',380,505,[word('Domination',0,0,32)],'Domination names the pyramid',{beat:1,at:4600});
  // Beats 1-2: Eisler's peaceful golden age hangs over the contrast, then the book lets it fall away.
  put('golden-age',600,172,[...Array.from({length:8},(_,k)=>{const a=k*Math.PI/4;return p(`M${Math.cos(a)*44} ${Math.sin(a)*44}L${Math.cos(a)*58} ${Math.sin(a)*58}`,C.gold,6);}),dot(0,0,34,C.gold),word('Peaceful',0,84,23),word('golden age',0,109,23)],'The contested peaceful prehistoric golden age attached to the original contrast',{beat:1,at:2600,dur:1000});
  slide('golden-age',2,600,290,3500,1100);gone('golden-age',2,4200,700);
  // Beat 3: a history line with both patterns recurring in mixed order, belonging to no single period.
  put('history',600,160,[inkLine('M-430 0H420',3),inkLine('M408 -9L426 0L408 9',3)],'History as a line of periods',{beat:3,at:150,dur:700});
  ['P','L','L','P','L','P','P','L'].forEach((kind,k)=>{const x=-370+100*k;
   put('era-'+k,600+x,160,kind==='P'?[rect(-21,-12,42,12,C.rustDeep),rect(-14,-24,28,12,C.rust),rect(-7,-36,14,12,C.rustDeep)]:[tealLine('M-16 -6H16M-16 -6L0 -32L16 -6',4),tealDot(-16,-6,6),tealDot(16,-6,6),tealDot(0,-32,6)],(kind==='P'?'Domination':'Partnership')+' pattern recurring in another period',{beat:3,at:500+280*k,dur:500});});
  // Beat 4: technology and institutions arrive and the relative cost of the two ways changes.
  put('cost-pyramid-low',150,452,coins(2),'Coordinating by domination is cheap here',{beat:4,at:300,dur:700});
  put('cost-lattice-high',1050,452,coins(7),'Coordinating by partnership is expensive here',{beat:4,at:300,dur:700});
  put('tools-and-rules',600,260,[...Array.from({length:8},(_,k)=>{const a=k*Math.PI/4;return tint(p(`M${-38+Math.cos(a)*22} ${Math.sin(a)*22}L${-38+Math.cos(a)*32} ${Math.sin(a)*32}`,C.slate,9),C.slateNight);}),tint(dot(-38,0,22,C.slate),C.slateNight),dot(-38,0,8,C.cream),
   n('path',{d:'M10 -30L42 -48L74 -30Z',fill:C.teal}),rect(12,-28,60,6,C.teal),...[18,36,54].map(x=>rect(x,-20,8,34,C.teal)),rect(10,14,64,7,C.teal),
   word('Technology',0,62,22),word('and institutions',0,88,22)],'A gear for technology and a columned building for institutions');
  act('tools-and-rules','appear',4,1700,700);slide('tools-and-rules',4,600,320,1800,1300);
  gone('cost-pyramid-low',4,3800);gone('cost-lattice-high',4,3800);
  put('cost-pyramid-high',150,452,coins(7),'After the change, domination becomes the expensive way',{beat:4,at:3900,dur:800});
  put('cost-lattice-low',1050,452,coins(2),'After the change, partnership becomes the cheaper way',{beat:4,at:3900,dur:800});
  return q.finish('The cover pyramid and lattice are built and named; the peaceful golden age falls away; both patterns recur along history; technology and institutions swap which way is cheaper (coin stacks, qualitative).');
 }

 if(i===1){
  // A member of the measured relationship reacts to each question about their own position.
  storyPerson(q,'member',128,522,{identity:'person-11-neutral',coat:C.teal,scale:.78,ink:C.ink});
  express('member',1,'curious');storyGesture(q,'member',1,'explain');storyGesture(q,'member',2,'question');
  express('member',3,'worried');storyGesture(q,'member',3,'recoil');express('member',4,'relieved');storyGesture(q,'member',4,'release');
  // Beat 1: the binary box for a whole civilization is set aside for measured dimensions.
  put('civilization-box',560,330,[n('rect',{x:-160,y:-110,width:320,height:210,rx:8,fill:C.crate,stroke:C.ink,'stroke-width':4}),t('Whole civilization',0,-52,30,C.ink),
   n('rect',{x:-110,y:-20,width:80,height:80,rx:6,fill:'#fff6e6',stroke:C.ink,'stroke-width':3}),rect(-94,30,48,10,C.rustDeep),rect(-84,18,28,12,C.rust),rect(-76,6,12,12,C.rustDeep),
   n('rect',{x:30,y:-20,width:80,height:80,rx:6,fill:'#fff6e6',stroke:C.ink,'stroke-width':3}),p('M50 38H90M50 38L70 4L90 38',C.teal,4),dot(50,38,6,C.teal),dot(90,38,6,C.teal),dot(70,4,6,C.teal),
   p('M-104 4L-80 34L-36 -32',C.rust,9)],'A whole civilization forced into one of two boxes',{beat:1,at:100,dur:600});
  gone('civilization-box',1,2500,600);
  const cx=520,cy=322,R=140,ang=k=>(-90+72*k)*Math.PI/180,pt=(k,r)=>[cx+Math.cos(ang(k))*r,cy+Math.sin(ang(k))*r];
  const pentagon=r=>'M'+[0,1,2,3,4].map(k=>{const [x,y]=pt(k,r);return `${x-cx} ${y-cy}`;}).join('L')+'Z';
  put('dial',cx,cy,[inkLine(pentagon(R),2),inkLine(pentagon(R/2),2),...[0,1,2,3,4].map(k=>{const [x,y]=pt(k,R);return inkLine(`M0 0L${x-cx} ${y-cy}`,3);}),tint(dot(0,0,7,C.ink),C.pale)],'Coordinate system: five axes for one relationship, no numeric scale',{beat:1,at:2900,dur:1000});
  // Beat 2: each question becomes an axis, then a qualitative profile of the relationship appears.
  const names=['Leave','Speak','Appeal','Observe','Sanction'],speech=[1700,2150,2600,3100,4200];
  names.forEach((s,k)=>{const [x,y]=pt(k,R+30),c=Math.cos(ang(k)),anchor=c>.3?'start':c<-.3?'end':'middle';put('axis-'+k,x,k===0?y-4:y+10,[word(s,0,0,27,anchor)],'Question: who can '+s.toLowerCase(),{beat:2,at:speech[k],dur:600});});
  const profile=(id,vals,meaning,cue)=>{const pts=vals.map((v,k)=>{const [x,y]=pt(k,R*v);return [x-cx,y-cy];});
   const d='M'+pts.map(a=>a.join(' ')).join('L')+'Z';put(id,cx,cy,[tint(n('path',{d,fill:C.teal,opacity:.22}),C.tealNight),tealLine(d,4),...pts.map(([x,y])=>tealDot(x,y,8))],meaning,cue);};
  profile('profile-open',[.85,.7,.62,.74,.58],'Qualitative profile: exit, voice, appeal, visibility and sanction all available',{beat:2,at:4800,dur:900});
  // Beat 3: wealth, media, office and force convert into each other; the loop closes and exit collapses.
  const token=(id,x,y,nodes,label,ly,meaning,at)=>{put(id,x,y,[...nodes,word(label,0,ly,25)],meaning,{beat:3,at,dur:600});};
  token('wealth',830,250,[dot(0,0,30,C.gold),n('circle',{cx:0,cy:0,r:20,fill:'none',stroke:C.goldEdge,'stroke-width':3})],'Wealth',-46,'Wealth',1200);
  token('media',1040,250,[tint(n('path',{d:'M-32 -12H-6L22 -30V30L-6 12H-32Z',fill:C.ink}),C.pale),p('M30 -14Q40 0 30 14',C.rust,5)],'Media',-46,'Media: a megaphone',1700);
  token('office',1040,410,[rect(-24,-38,48,40,C.rustDeep,6),rect(-30,0,60,12,C.rust,3),p('M-24 12V34M24 12V34',C.rustDeep,7)],'Office',72,'Office: an official seat',2200);
  token('force',830,410,[tint(n('path',{d:'M0 -34L28 -24V2Q28 24 0 36Q-28 24 -28 2V-24Z',fill:C.slate}),C.slateNight),p('M0 -22V24',C.cream,4)],'Force',72,'Force: a shield',2700);
  const arrow=(id,d,hx,hy,dx,dy,at,meaning)=>put(id,0,0,[p(d,C.rust,6),arrowHead(hx,hy,dx,dy,C.rust)],meaning,{beat:3,at,dur:500});
  arrow('wealth-to-media','M876 250H986',994,250,1,0,3200,'Wealth converts into media');
  arrow('media-to-office','M1040 296V356',1040,364,0,1,3700,'Media converts into office');
  arrow('office-to-force','M994 410H884',876,410,-1,0,4200,'Office converts into force');
  arrow('force-to-wealth','M830 364V304',830,296,0,-1,5200,'Force converts back into wealth: the loop closes');
  gone('profile-open',3,5500,700);
  profile('profile-closed',[.08,.42,.3,.5,.3],'With every advantage convertible, exit collapses toward zero',{beat:3,at:5600,dur:900});
  put('leave-blocked',cx,cy-R-34,[p('M-46 -9H46',C.rust,6)],'Escape disappears: the exit question is struck through',{beat:3,at:5900,dur:500});
  // Beat 4: the loop is replaced by a bounded hierarchy with a door; exit returns on the dial.
  for(const id of ['wealth','media','office','force','wealth-to-media','media-to-office','office-to-force','force-to-wealth'])gone(id,4,150,600);
  put('bounded-hierarchy',845,456,[rect(-80,-40,160,40,C.rustSoft,3),rect(-56,-80,112,40,C.rust,3),rect(-30,-120,60,40,C.rustSoft,3),rect(-40,-36,26,36,C.ink),
   tint(n('circle',{cx:0,cy:-142,r:15,fill:C.ink}),C.pale)],'A hierarchy for a task: offices still differ in rank',{beat:4,at:700,dur:800,scale:1.3});
  put('exit-door',845,456,[rect(-40,-36,26,36,C.cream),n('path',{d:'M-14 -36L4 -30V6L-14 0Z',fill:C.teal})],'The exit door in the hierarchy opens',{beat:4,at:5000,dur:700,scale:1.3});
  ['Purpose','Scope','Duration','Review','Exit'].forEach((s,k)=>put('limit-'+k,972,232+52*k,[tealLine('M0 0L9 9L24 -10',5),word(s,36,10,26,'start')],s+' of the authority is clear',{beat:4,at:2900+500*k,dur:500}));
  gone('profile-closed',4,5200,600);gone('leave-blocked',4,5200,500);
  profile('profile-restored',[.82,.68,.66,.72,.6],'With clear limits and exit, the relationship profile reopens',{beat:4,at:5400,dur:900});
  return q.finish('A member stands beside a five-axis coordinate system (leave, speak, appeal, observe, sanction) that replaces a binary civilization box; wealth, media, office and force convert in a closing loop as exit collapses; a bounded hierarchy with listed limits and an open door restores the profile.');
 }

 // Scene 3, beat 1: a commons gains its teeth - boundary posts, monitoring, graduated sanctions, appeal.
 const commons=['pond','members','fence','fence-label','monitoring','sanctions','appeal'];
 put('pond',380,335,[n('ellipse',{cx:0,cy:0,rx:150,ry:68,fill:C.teal}),p('M-70 -38Q-58 -46 -46 -38T-22 -38M22 44Q34 36 46 44T70 44',C.cream,4),t('Commons',0,10,28,C.cream)],'A shared resource: the commons',{beat:1,at:150,dur:700});
 const member=(x,y)=>[tint(dot(x,y-28,9,C.ink),C.pale),tint(n('path',{d:`M${x-13} ${y}Q${x-13} ${y-16} ${x} ${y-16}Q${x+13} ${y-16} ${x+13} ${y}Z`,fill:C.ink}),C.pale)];
 put('members',0,0,[...member(196,350),...member(564,350),...member(380,436)],'Members who share and use the commons',{beat:1,at:600,dur:700});
 put('fence',380,330,Array.from({length:20},(_,k)=>{const a=k*Math.PI/10,x=Math.cos(a)*222,y=Math.sin(a)*124;return rect(x-5,y-15,10,30,C.rustDeep,3);}),'Boundary posts around the commons',{beat:1,at:3000,dur:700});
 put('fence-label',380,180,[word('Boundaries',0,0,27)],'Boundaries',{beat:1,at:3100,dur:600});
 put('monitoring',720,220,[tint(n('path',{d:'M-30 0Q0 -26 30 0Q0 26 -30 0Z',fill:C.ink}),C.pale),dot(0,0,10,C.teal),word('Monitoring',48,10,27,'start')],'Monitoring: members can see use of the commons',{beat:1,at:3600,dur:600});
 put('sanctions',720,338,[rect(-30,4,14,14,C.rustSoft,2),rect(-8,-10,14,28,C.rust,2),rect(14,-26,14,44,C.rustDeep,2),word('Graduated sanctions',48,10,27,'start')],'Graduated sanctions: small first responses before larger ones',{beat:1,at:4100,dur:600});
 put('appeal',720,452,[inkLine('M0 -30V14M-26 -22H26M-18 14H18',4),inkLine('M-26 -22L-34 -4H-18ZM26 -22L18 -4H34Z',3),word('Appeal',48,6,27,'start')],'Appeal: a balance for contesting a sanction',{beat:1,at:5000,dur:600});
 for(const id of commons)gone(id,2,150,600);
 // Beat 2: one AI chip forks toward an empire machine or toward cheaper partnership.
 put('ai',600,190,[rect(-40,-34,80,68,C.slate,12),...[-20,0,20].map(x=>p(`M${x} -34V-48M${x} 34V48`,C.gold,6)),...[-14,10].map(y=>p(`M-40 ${y}H-54M40 ${y}H54`,C.gold,6)),t('AI',0,12,32,C.cream)],'Artificial intelligence: one capability, two possible institutional paths',{beat:2,at:700,dur:700});
 q.objects.at(-1).visual.children[0]=tint(q.objects.at(-1).visual.children[0],C.slateNight);
 put('to-empire',0,0,[p('M548 222Q440 250 404 286',C.rust,6),arrowHead(398,292,-0.7,0.7,C.rust)],'Path toward concentration',{beat:2,at:1300,dur:600});
 put('empire',330,470,pyramidTiers('chip').flat(),'Empire machine: many base positions governed through one computational apex',{beat:2,at:1500,dur:800,scale:.72});
 put('empire-label',330,520,[word('Empire machine',0,0,28)],'Empire machine',{beat:2,at:1900,dur:600});
 put('to-partnership',0,0,[p('M652 222Q760 250 796 286',C.teal,6),arrowHead(802,292,0.7,0.7,C.teal)],'Path toward cheaper cooperation',{beat:2,at:3600,dur:600});
 q.objects.at(-1).visual.children=q.objects.at(-1).visual.children.map(c=>tint(c,C.tealNight));
 put('partnership-net',870,470,latticeRows(0,3),'Partnership lattice the same tools can support',{beat:2,at:3800,dur:800,scale:.72});
 put('partnership-label',870,520,[word('Cheaper partnership',0,0,28)],'Lower cost of partnership',{beat:2,at:4200,dur:600});
 for(const id of ['ai','to-empire','empire','empire-label','to-partnership','partnership-net','partnership-label'])gone(id,3,150,600);
 // Beat 3: the open book at Chapter 3, whose right page maps a relationship on the coordinate axes.
 put('book',600,345,[n('path',{d:'M0 -128Q-150 -160 -312 -134V154Q-150 128 0 162Q150 128 312 154V-134Q150 -160 0 -128Z',fill:C.teal}),
  n('path',{d:'M0 -118Q-140 -148 -294 -124V138Q-140 112 0 146Z',fill:'$page'}),n('path',{d:'M0 -118Q140 -148 294 -124V138Q140 112 0 146Z',fill:'$page'}),p('M0 -118V146',C.ink,2)],'The open book',{beat:3,at:400,dur:900});
 put('chapter',456,302,[t('Chapter 3',0,-38,26,C.rust),t('From Binary to',0,4,30,C.ink),t('Coordinate System',0,40,30,C.ink)],'The recommended starting chapter',{beat:3,at:1500,dur:600});
 const mini=k=>[Math.cos((-90+72*k)*Math.PI/180),Math.sin((-90+72*k)*Math.PI/180)];
 put('page-map',748,335,[...[0,1,2,3,4].map(k=>p(`M0 0L${mini(k)[0]*92} ${mini(k)[1]*92}`,C.ink,2)),p('M'+[0,1,2,3,4].map(k=>`${mini(k)[0]*92} ${mini(k)[1]*92}`).join('L')+'Z',C.ink,2)],'Reader-made coordinate map on the facing page',{beat:3,at:2600,dur:700});
 const pd='M'+[.8,.55,.7,.4,.65].map((v,k)=>`${mini(k)[0]*92*v} ${mini(k)[1]*92*v}`).join('L')+'Z';
 put('page-profile',748,335,[n('path',{d:pd,fill:C.teal,opacity:.3}),p(pd,C.teal,4),...[.8,.55,.7,.4,.65].map((v,k)=>dot(mini(k)[0]*92*v,mini(k)[1]*92*v,6,C.teal))],'Mapping who holds power in one relationship',{beat:3,at:4300,dur:900});
 put('bookmark',356,206,[n('path',{d:'M-12 0H12V56L0 44L-12 56Z',fill:C.rust})],'Bookmark at the starting chapter',{beat:3,at:1900,dur:600});
 return q.finish('A fenced commons with monitoring, graduated sanctions and appeal; an AI chip forking toward an empire-machine pyramid or a cheaper partnership lattice; the open book at Chapter 3 with a coordinate map being drawn.');
}
for(let i=0;i<scenes.length;i++)scenes[i].visual=compose(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('Wrote visuals for '+scenes.length+' scenes.');
