// Book-owned staging for Incomplete Tribes. Spoken lines in work/scenes.json are final; only `visual` is rewritten.
// Visual grammar from the cover: a tribe is a ring left open (a gap for exit and other loyalties);
// a ring that closes is the "complete tribe" the book warns against. Scale grows scene by scene:
// a house of belonging (Prelude, Ch. 1, 6) -> one chess club (Ch. 9-11) -> an archipelago (Ch. 10, 14-16).
import fs from 'node:fs';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {storyPerson} from '../../tools/shf/people-poses.mjs';

const file=new URL('./work/scenes.json',import.meta.url);
const scenes=JSON.parse(fs.readFileSync(file,'utf8'));
// Palette from work/visual-bible.json (cover: amber, sage-teal, deep ink) plus two warm supports.
const C={amber:'#e9a23b',sage:'#7fb0a3',ink:'#112c36',teal:'#2f6f73',tealNight:'#8cc9bf',cream:'#eef0dc',clay:'#c96f4a',plum:'#86698c',slate:'#5d7f9e',coral:'#d9734f'};

function compose(index){
 const a=stageAuthor(),{n,path,text,dot}=a;
 const th=(node,themes)=>({...node,themeAttrs:themes});
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const put=(id,x,y,kids,meaning,beat=0,offsetMs=250,durationMs=700,scale=1)=>{a.add(a.object(id,x,y,kids,meaning,scale));if(beat)a.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs});return id;};
 const hide=(id,beat,offsetMs=250,durationMs=600)=>a.actions.push({actor:id,action:'disappear',beat,offsetMs,durationMs});
 const move=(id,beat,x,y,offsetMs=300,durationMs=1500)=>a.actions.push({actor:id,action:'moveTo',beat,x,y,offsetMs,durationMs});
 const walk=(id,beat,x,offsetMs=300,durationMs=2000)=>a.actions.push({actor:id,action:'walkTo',beat,x,offsetMs,durationMs});
 const gesture=(id,beat,g,offsetMs=500,durationMs=1900)=>a.actions.push({actor:id,action:'character.gesture',gesture:g,beat,offsetMs,durationMs});
 const express=(id,beat,emotion,offsetMs=200)=>a.actions.push({actor:id,action:'character.express',emotion,beat,offsetMs,durationMs:600});
 const person=(id,x,y,identity,coat,{scale=.7,seated=false,chair=C.sage,beat=1,offsetMs=250}={})=>{storyPerson(a,id,x,y,{identity,coat,scale,seated,chair,ink:C.ink});
  // Drop the library's white collar pill (person-03/12/18): on these coats it reads as a floating patch.
  const v=a.objects.find(o=>o.id===id).visual;v.children=v.children.filter(c=>!(c.type==='rect'&&c.attrs?.fill==='$page'&&c.id.startsWith('$asset.detail')));
  a.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs:700});return id;};
 // Night-only hair lift for very dark hair that disappears on the near-black stage.
 const nightHair=(id,fill)=>{const head=a.objects.find(o=>o.id===id).visual.children.find(c=>c.id==='$asset.head');const hair=head.children.find(c=>c.id==='$asset.n4');hair.themeAttrs={...hair.themeAttrs,night:{fill}};};
 // Elliptical ring with an opening; gapAt in degrees (0 = right, 90 = toward viewer/down).
 const openRing=(rx,ry,color,gapAt=0,gap=44,width=10)=>{
  const rad=d=>d*Math.PI/180,pt=d=>[+(rx*Math.cos(rad(d))).toFixed(1),+(ry*Math.sin(rad(d))).toFixed(1)];
  const [x1,y1]=pt(gapAt+gap/2),[x2,y2]=pt(gapAt+360-gap/2);
  return path(`M${x1} ${y1}A${rx} ${ry} 0 1 1 ${x2} ${y2}`,color,width);
 };
 // Arc of the same ellipse from angle `from` to `to` (degrees, increasing), so one ring can be split into a back arc
 // (painted behind people standing on it) and a front arc (painted in front of them).
 const ringArc=(rx,ry,color,from,to,width=10)=>{
  const rad=d=>d*Math.PI/180,pt=d=>[+(rx*Math.cos(rad(d))).toFixed(1),+(ry*Math.sin(rad(d))).toFixed(1)];
  const [x1,y1]=pt(from),[x2,y2]=pt(to);
  return path(`M${x1} ${y1}A${rx} ${ry} 0 ${to-from>180?1:0} 1 ${x2} ${y2}`,color,width);
 };
 const ringAnchors=(id,rx,ry)=>{const o=a.objects.find(v=>v.id===id);o.visual.anchors={left:[-rx,0],right:[rx,0],top:[0,-ry],bottom:[0,ry]};};

 if(index===0){
  // Hook: waiting for an ideal human vs. redesigning the house of belonging.
  put('civic-floor',600,546,[th(rect(-480,0,960,12,C.teal,3),{night:{fill:C.tealNight}})],'Shared civic floor on which every group stands (Ch. 6 building image)');
  person('host',245,540,'person-14-neutral',C.amber);
  person('builder',340,540,'person-05-neutral',C.clay,{offsetMs:450});nightHair('builder','#7d93a6');
  person('mourner',435,540,'person-10-neutral',C.slate,{offsetMs:650});
  put('plinth',860,540,[rect(-95,-58,190,58,C.sage,4),th(rect(-115,-70,230,14,C.teal,3),{night:{fill:C.tealNight}})],'Plinth reserved for a morally perfect human',1,900);
  put('ideal-human',860,470,[
   n('circle',{cx:0,cy:-210,r:34,fill:'none',stroke:'$ink','stroke-width':4,'stroke-dasharray':'9 9'}),
   n('path',{d:'M-46 -160Q0 -178 46 -160L56 -40H-56ZM-34 -40L-38 0M34 -40L38 0',fill:'none',stroke:'$ink','stroke-width':4,'stroke-dasharray':'0.018 0.018','stroke-linejoin':'round'}),
   n('ellipse',{cx:0,cy:-262,rx:30,ry:8,fill:'none',stroke:C.amber,'stroke-width':5})
  ],'Dashed, empty outline of an ideal human that civilization supposedly waits for; nobody stands in it',1,1300,900);
  put('question-mark',985,300,[text('?',0,0,78,'$ink')],'The book\'s opening question',1,1900);
  for(const id of ['host','builder','mourner'])express(id,1,'curious');
  gesture('host',1,'question',1500);gesture('mourner',1,'reflect',2100);
  // Beat 2: the pedestal goes; the same imperfect people get a better-designed home instead.
  for(const id of ['ideal-human','question-mark','plinth'])hide(id,2,150,500);
  put('home-left',330,540,[path('M-185 0V-245L0-330L185-245V-135',C.amber,10)],'A house of belonging, deep enough to shelter a group, with its door left open',2,800,1000);
  put('home-right',870,540,[path('M185 0V-245L0-330L-185-245V-135',C.sage,10)],'A neighbouring group\'s house, its door facing the shared street',2,1200,1000);
  person('neighbour',800,540,'person-03-neutral',C.sage,{beat:2,offsetMs:1500});
  person('neighbour-2',930,540,'person-18-neutral',C.plum,{beat:2,offsetMs:1700});
  express('host',2,'relieved');gesture('host',2,'explain',900);gesture('builder',2,'release',1300);
  // Beat 3: warmth inside the group ("We love, build and mourn"), then loyalty seals the door and raises a wall.
  express('host',3,'happy',100);express('builder',3,'happy',100);express('mourner',3,'relieved',100);
  gesture('host',3,'invite',200,1500);gesture('builder',3,'resolve',900,1500);
  express('mourner',3,'sad',1700);gesture('mourner',3,'reflect',1700,1500);
  put('sealed-door',330,540,[rect(177,-135,16,135,C.amber,3)],'Loyalty closes the open door: the group starts claiming everything',3,3300,500);
  put('wall',600,546,[n('path',{d:'M-34 0V-196L-17-222L0-196L17-222L34-196V0Z',fill:C.clay}),path('M-34 -65H34M-34 -130H34M0 0V-65M-17 -65V-130M17 -65V-130M0 -130V-196','#7a3a26',3)],'A wall rises in the street between neighbours',3,3700,700);
  express('host',3,'angry',3500);express('builder',3,'determined',3700);express('neighbour',3,'worried',3900);express('neighbour-2',3,'worried',3900);
  gesture('neighbour',3,'recoil',4000);gesture('neighbour-2',3,'recoil',4200);
  return a.finish('Ordinary, imperfect people wait beneath an empty dashed outline of an ideal human; the pedestal is removed and the same people are given open-doored houses of belonging on a shared floor. As the group gathers, loyalty seals its door and a wall rises against the neighbours. Metaphor for the book\'s question and architectural answer, not a historical scene.');
 }

 if(index===1){
  // Chapter Nine's own example: a chess club with real jurisdiction and real limits.
  put('club-ring',400,505,[openRing(270,40,C.amber,0,40)],'The chess club\'s jurisdiction: a ring drawn on the floor, deliberately left open',1,250,1100);ringAnchors('club-ring',270,40);
  put('club-sign',390,188,[rect(-118,-32,236,64,C.amber,10),text('Chess club',0,11,31,C.ink)],'Club sign naming the community',1,400);
  put('table',390,505,[th(rect(-112,-112,224,14,C.teal,4),{night:{fill:C.tealNight}}),th(path('M-92-98V0M92-98V0',C.teal,10),{night:{stroke:C.tealNight}})],'Club table');
  put('board',370,393,[rect(-74,-14,148,14,C.cream,2),...Array.from({length:8},(_,i)=>rect(-74+i*18.5,-14,18.5,7,i%2?C.cream:C.ink)),...Array.from({length:8},(_,i)=>rect(-74+i*18.5,-7,18.5,7,i%2?C.ink:C.cream)),
   n('path',{d:'M-42 -14L-36 -40H-48ZM-50 -42H-34M-42 -48V-60M-48 -54H-36',fill:'$ink',stroke:'$ink','stroke-width':3,'stroke-linejoin':'round'}),
   n('path',{d:'M26 -14Q30 -28 36 -30Q42 -28 46 -14Z',fill:C.clay}),dot(36,-34,7,C.clay)],'Chessboard with a king and a pawn mid-game');
  person('opponent',225,505,'person-07-neutral',C.slate,{seated:true,chair:C.sage,scale:.66});
  // The member stands inside the club ring (ring spans x 130-670, gap at the right end).
  person('member',545,505,'person-12-neutral',C.amber,{scale:.68,offsetMs:500});
  express('member',1,'neutral',300);gesture('member',1,'explain',800);
  // Beat 2: rules for tournament conduct inside the ring; love stays outside its reach.
  put('clock',462,393,[th(rect(-30,-40,60,40,C.teal,6),{night:{fill:C.tealNight}}),dot(-13,-21,10,C.cream),dot(13,-21,10,C.cream),path('M-13 -21V-28M13 -21L18 -26',C.ink,2),rect(-20,-48,12,8,C.clay,2),rect(8,-48,12,8,C.clay,2)],'Tournament clock: the conduct the club may govern',2,250);
  put('rules-label',390,262,[text('Tournament rules',0,0,30,'$ink')],'What falls within the club\'s jurisdiction',2,450);
  person('partner',925,505,'person-16-neutral',C.coral,{beat:2,offsetMs:2300,scale:.66});
  put('heart',800,262,[n('path',{d:'M0 22C-34 0-38-22-22-30C-10-36 0-26 0-18C0-26 10-36 22-30C38-22 34 0 0 22Z',fill:C.coral})],'A member\'s romantic life, outside the club ring',2,2700,600,1.25);
  express('member',2,'relieved',200);express('member',2,'happy',2600);gesture('member',2,'invite',2800,1700);gesture('opponent',2,'reflect',600);
  // Beat 3: other loyalties overlap at the member, as on the cover.
  // Split around the standing figures: the far arc and its open end sit behind the partner's and member's legs,
  // the near arc in front of their feet (gap 312-348 degrees, as before).
  put('home-ring-back',775,512,[ringArc(240,34,C.sage,180,312)],'Far side of the second ring, behind the people standing in it',3,300,1100);
  put('home-ring',775,512,[ringArc(240,34,C.sage,348,540)],'A second, overlapping belonging (partner and home) that also claims part of the member',3,300,1100);ringAnchors('home-ring',240,34);
  {const all=a.objects,back=all.splice(all.findIndex(o=>o.id==='home-ring-back'),1)[0];all.splice(all.findIndex(o=>o.id==='club-ring')+1,0,back);}
  express('member',3,'relieved',1500);gesture('partner',3,'release',1800);
  // Beat 4: dissent is spoken, then the member walks out through the gap; the club remains.
  put('dissent',625,258,[n('path',{d:'M-86 -26H86V20H-48L-64 40L-74 20H-86Z',fill:C.cream,stroke:'$ink','stroke-width':2,'stroke-linejoin':'round'}),text('I disagree',0,6,24,C.ink)],'Open dissent, spoken without being treated as betrayal',4,250,500);
  express('opponent',4,'neutral',800);gesture('opponent',4,'release',900,1500);
  hide('dissent',4,3300,500);walk('member',4,800,2900,2300);
  return a.finish('Chapter Nine\'s example as a scene: a member standing inside a chess club whose open floor ring covers tournament conduct, not the member\'s romantic life outside it. A second, overlapping ring around member and partner shows another loyalty; the member voices dissent and walks out through the gap while the club and opponent remain. Illustrative people, not portraits.');
 }

 // Scene 3: the epilogue's archipelago, then the reading invitation.
 const islands=[
  ['isle-a',180,330,95,48,C.amber],['isle-b',380,192,74,36,C.sage],['isle-c',420,452,112,52,C.sage],
  ['isle-d',652,300,106,54,C.amber],['isle-e',722,482,72,34,C.slate]
 ];
 const folk=(x,y,body,head='#c98e6b')=>[rect(x-6,y-14,12,16,body,5),dot(x,y-20,6,head)];
 const people={'isle-a':[[-55,C.sage],[-15,C.clay],[25,C.slate]],'isle-b':[[-18,C.amber],[18,C.clay]],'isle-c':[[-70,C.amber],[20,C.plum]],'isle-d':[[-70,C.sage],[-30,C.slate],[10,C.clay]],'isle-e':[[-16,C.amber],[18,C.sage]]};
 for(const [id,x,y,rx,ry,fill] of islands){
  put(id,x,y,[n('ellipse',{cx:0,cy:0,rx,ry,fill}),n('ellipse',{cx:rx*.35,cy:-ry*.32,rx:rx*.55,ry:ry*.6,fill}),...people[id].flatMap(([dx,c])=>folk(dx,-4,c))],'A distinct community: an island of its own size, with mixed members',1,250+islands.findIndex(v=>v[0]===id)*150,800);
 }
 const bridge=(id,d,offsetMs)=>put(id,0,0,[th(path(d,C.teal,8),{night:{stroke:C.tealNight}}),path(d,C.cream,2)],'A bridge between communities: a cross-cutting tie',1,offsetMs,700);
 bridge('bridge-ab','M236 296Q262 236 318 214',1300);bridge('bridge-ac','M252 362Q290 404 322 424',1500);
 bridge('bridge-bd','M452 204Q508 220 556 272',1700);bridge('bridge-cd','M512 420Q552 372 586 342',1900);
 bridge('bridge-ce','M532 462Q592 476 650 482',2100);bridge('bridge-de','M690 352Q712 398 716 448',2300);
 // The cut is drawn early, snags on every bridge it crosses, then breaks apart: the sort fails.
 put('sorting-line',0,0,[n('path',{d:'M515 140L570 545',fill:'none',stroke:C.clay,'stroke-width':5,'stroke-dasharray':'0.035 0.025','stroke-linecap':'round'})],'An attempt to cut the world into two clean camps, crossing too many bridges',1,900,500);
 const snags=[[529,240],[548,385],[561,470]];
 snags.forEach(([x,y],i)=>put('snag-'+i,x,y,[n('circle',{cx:0,cy:0,r:13,fill:'none',stroke:C.coral,'stroke-width':4})],'The cut snags on a bridge it cannot sever',1,1900+i*300,400));
 hide('sorting-line',1,3300,300);
 // Pieces knocked askew at each bridge so the failed cut is legible, not a clean division.
 const brokenLine=['M503 142L516 220','M546 262L552 360','M534 404L548 450','M582 492L586 545'];
 put('sorting-broken',0,0,[n('path',{d:brokenLine.join(''),fill:'none',stroke:C.clay,'stroke-width':5,'stroke-dasharray':'0.035 0.025','stroke-linecap':'round',opacity:.55})],'The sorting line falls apart where loyalties overlap: no clean enemy camps',1,3300,400);
 for(let i=0;i<snags.length;i++)hide('snag-'+i,2,150,500);
 hide('sorting-broken',2,150,600);
 // Beat 2: rivals contest; one loses its flag but keeps its island.
 put('pole-a',108,320,[path('M0 0V-92',C.ink,4)],'Flagpole of one rival community',2,250);
 put('flag-a',128,240,[n('path',{d:'M-18 -12H26L16 0L26 12H-18Z',fill:C.clay})],'Rival A\'s flag',2,250);
 put('pole-d',722,292,[path('M0 0V-92',C.ink,4)],'Flagpole of the other rival community',2,450);
 put('flag-d',742,212,[n('path',{d:'M-18 -12H26L16 0L26 12H-18Z',fill:C.slate})],'Rival D\'s flag',2,450);
 for(const pole of ['pole-a','pole-d'])a.objects.find(o=>o.id===pole).visual.children[0].themeAttrs={night:{stroke:C.cream}};
 // The rival loses: its flag comes all the way down and fades, while its island and people stay.
 move('flag-d',2,742,282,1000,1600);hide('flag-d',2,3000,700);
 put('kept-island',652,300,[openRing(126,70,C.teal,-56,40,4)],'The losing rival keeps its island: defeat without erasure',2,3100,800);
 // Gap centred on the rival's flagpole (x 722) so the bare pole never pierces the ring outline.
 a.objects.find(o=>o.id==='kept-island').visual.children[0].themeAttrs={night:{stroke:C.tealNight}};
 hide('kept-island',3,150,500);
 // Beat 3: an AI system offers to interpret one member's whole world; the closed ring is reopened.
 put('ai-screen',395,446,[th(rect(-26,-36,52,36,C.teal,6),{night:{fill:C.tealNight}}),rect(-20,-31,40,24,C.cream,3),dot(-9,-19,3,C.teal),dot(0,-19,3,C.teal),dot(9,-19,3,C.teal),path('M0 0V8M-10 8H10',C.ink,3)],'An intimate AI system speaking to one member',3,250);
 a.objects.find(o=>o.id==='ai-screen').visual.children.at(-1).themeAttrs={night:{stroke:C.cream}};
 put('closed-ring',420,446,[n('ellipse',{cx:0,cy:0,rx:140,ry:72,fill:'none',stroke:C.coral,'stroke-width':7})],'The AI as sole interpreter: a ring that closes around the island and cuts its bridges',3,2300,900);
 hide('closed-ring',3,4700,600);
 put('audited-ring',420,446,[openRing(140,72,C.amber,-20,62,7)],'The incompleteness test: the ring stays open toward outside comparison and exit',3,4900,800);
 // Beat 4: the reading invitation; the audit ring clears so the open book holds the final focus.
 hide('audited-ring',4,150,500);
 a.add({id:'prelude-book',asset:'book',x:985,y:372,scale:1.18,options:{color:C.amber},meaning:'Incomplete Tribes opened at its Prelude'});
 a.actions.push({actor:'prelude-book',action:'appear',beat:4,offsetMs:150,durationMs:600});
 a.actions.push({actor:'prelude-book',action:'book.open',beat:4,offsetMs:600,durationMs:1300});
 put('prelude-page',985,372,[rect(-138,-30,124,40,'$page',4),rect(12,-50,130,88,'$page',4),text('Prelude',-76,-4,24,C.ink),text('The Question',76,-26,18,C.ink),text('Beneath the',76,-4,18,C.ink),text('Question',76,18,18,C.ink)],'The Prelude\'s title on the open pages',4,1900,700,1.18);
 return a.finish('The epilogue\'s image: civilization as an archipelago of distinct islands joined by bridges so no island becomes the whole world. A dashed line snags on the bridges and breaks apart, failing to sort mixed members into two camps; a rival\'s flag comes down but it keeps its island; a closed ring around an AI-mediated island is reopened; the book opens at its Prelude. Qualitative metaphor without data.');
}

for(let i=0;i<scenes.length;i++)scenes[i].visual=compose(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('Staged '+scenes.length+' scenes: '+scenes.map(s=>s.id+'('+s.visual.objects.length+' objects, '+s.visual.actions.length+' actions)').join(', '));
