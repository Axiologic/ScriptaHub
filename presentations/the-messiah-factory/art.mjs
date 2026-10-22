// Book-owned staging for The Messiah Factory: an amplified podium, separated contests,
// an audience-built persona, and an open-ringed working group. Spoken lines stay untouched.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../tools/shf/people-poses.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),file=path.join(root,'work/scenes.json'),scenes=JSON.parse(fs.readFileSync(file,'utf8'));
// Cover-matched palette (work/visual-bible.json) plus the cover's dusty rule colour and a paper material.
const C={gold:'#d9a23a',grey:'#8a9097',ink:'#1b1d22',rose:'#b0766c',paper:'#f4efe4',pale:'#c9cdd1',nightInk:'#5f6672'};

function compose(i){
 const a=stageAuthor(),{n,path:p,text:t,dot}=a;
 const put=(id,x,y,nodes,beat,meaning,scale=1,offsetMs)=>{a.add(a.object(id,x,y,nodes,meaning,scale));if(beat)show(id,beat,offsetMs);return id;};
 const show=(id,beat,offsetMs=250,durationMs=900)=>a.actions.push({actor:id,action:'appear',beat,offsetMs,durationMs});
 const drop=(id,beat,offsetMs=250,durationMs=800)=>a.actions.push({actor:id,action:'disappear',beat,offsetMs,durationMs});
 const go=(id,beat,x,y,offsetMs=600,durationMs=1800)=>a.actions.push({actor:id,action:'moveTo',beat,x,y,offsetMs,durationMs});
 const feel=(id,beat,emotion,offsetMs=250)=>a.actions.push({actor:id,action:'character.express',emotion,beat,offsetMs,durationMs:900});
 // Dark material that would vanish on the Night stage gets a mid-grey night variant.
 const solid=(d,fill=C.ink)=>fill===C.ink?a.tint(n('path',{d,fill}),C.nightInk):n('path',{d,fill});
 const box=(x,y,w,h,fill,rx=6)=>fill===C.ink?a.tint(n('rect',{x,y,width:w,height:h,rx,fill}),C.nightInk):n('rect',{x,y,width:w,height:h,rx,fill});
 const line=(d,w=6)=>p(d,'$ink',w);
 const person=(id,x,y,{identity,coat,scale=.6,seated=false,beat=1,offsetMs,chair=C.grey})=>{storyPerson(a,id,x,y,{identity,coat,scale,seated,chair,ink:'#3a3f48'});
  // The asset's pale chest strip reads as a stray white bar under the scarf at this scale.
  const v=a.objects.find(o=>o.id===id).visual;v.children=v.children.filter(c=>!(String(c.id||'').includes('detail')&&c.attrs?.fill==='$page'));
  show(id,beat,offsetMs);return id;};
 // A leaf along a laurel branch: base point, direction (radians), length and width.
 const leaf=(x,y,ang,len=17,w=7,fill=C.gold)=>{const ux=Math.cos(ang),uy=Math.sin(ang),tx=x+ux*len,ty=y+uy*len,mx=x+ux*len*.5,my=y+uy*len*.5,px=-uy*w,py=ux*w,r=v=>v.toFixed(1);
  return n('path',{d:`M${r(x)} ${r(y)}Q${r(mx+px)} ${r(my+py)} ${r(tx)} ${r(ty)}Q${r(mx-px)} ${r(my-py)} ${r(x)} ${r(y)}Z`,fill});};
 // A laurel wreath: two leafy branches rising from a tied base, open at the top.
 const laurel=()=>{const nodes=[];for(const side of [-1,1]){const P=t=>{const u=1-t;return [u*u*(side*4)+2*u*t*(side*44)+t*t*(side*26),u*u*34+2*u*t*20+t*t*(-30)];};
   nodes.push(p(`M${side*4} 34Q${side*44} 20 ${side*26} -30`,C.gold,4));
   for(let k=1;k<=5;k++){const t=k/5.6,[x,y]=P(t),[x2,y2]=P(t+.02),dx=x2-x,dy=y2-y,base=Math.atan2(dy,dx);nodes.push(leaf(x,y,base+side*.75),leaf(x,y,base-side*.75,14,6));}}
  nodes.push(dot(0,36,6,C.rose));return nodes;};
 // The five contests share one icon vocabulary (scene 2 introduces them, scene 3 recalls them).
 const contestIcons=(ink=C.ink)=>[['Attention',[n('ellipse',{cx:0,cy:0,rx:30,ry:17,fill:'none',stroke:ink,'stroke-width':6}),dot(0,0,9,C.ink)]],
  ['Credibility',[p('M-22 0L-6 16L24 -18',C.gold,9)]],
  ['Authority',[dot(-12,0,15,C.gold),p('M2 0H32M22 0V12',C.gold,7)]],
  ['Performance',[n('path',{d:'M0 -24L7 -7H25L11 4L16 22L0 11L-16 22L-11 4L-25 -7H-7Z',fill:C.gold})]],
  ['Welfare',[n('path',{d:'M0 20C-30 0 -28 -24 -12 -24C-4 -24 0 -16 0 -12C0 -16 4 -24 12 -24C28 -24 30 0 0 20Z',fill:C.rose})]]];
 // A small audience figure: head and shoulders only, so it reads as a crowd member, not a cast role.
 const listener=(x,y,fill)=>[n('path',{d:`M${x-24} ${y+30}Q${x-24} ${y+2} ${x} ${y+2}Q${x+24} ${y+2} ${x+24} ${y+30}Z`,fill}),dot(x,y-14,14,fill)];
 const crowd=(spots)=>spots.flatMap(([x,y,c])=>listener(x,y,c));

 if(i===0){
  // Who gets heard: the amplified podium against a quiet, revising desk.
  put('podium',300,525,[box(-95,-150,190,150,C.ink,4),box(-95,-150,190,22,C.gold,4),box(-62,-104,124,66,C.grey,4)],1,'A raised podium: the place where a voice becomes audible to many');
  person('speaker',300,375,{identity:'person-11-neutral',coat:C.rose,scale:.6});
  put('waves',418,245,[0,38,76].map((dx,k)=>p(`M${dx} ${-34-k*10}Q${dx+26+k*4} 0 ${dx} ${34+k*10}`,C.gold,9)),1,'Amplification travels from the speaker toward the audience');
  put('crowd',705,492,crowd([[-120,-46,C.grey],[-60,-50,C.pale],[0,-46,C.grey],[60,-50,C.pale],[120,-46,C.grey],[-150,0,C.pale],[-75,4,C.grey],[0,0,C.pale],[75,4,C.grey],[150,0,C.pale]]),1,'An audience whose attention selects who is heard');
  put('answer',590,250,[box(-46,-38,92,76,C.ink,10),t('!',0,18,48,C.gold)],2,'A fixed, memorable answer carried by the amplification');
  go('answer',2,640,330,500,2200);go('crowd',2,640,492,900,2400);
  put('desk',1035,525,[box(-72,-98,144,14,C.grey,3),line('M-60 -84V0M60 -84V0',7)],1,'A plain desk for slow, revisable work');
  person('thinker',920,525,{identity:'person-06-neutral',coat:C.grey,scale:.55,seated:true,chair:C.pale});
  put('notebook',1035,410,[box(-58,-36,116,56,C.paper,4),p('M-44 -20H40M-44 -4H40M-44 12H22','#9aa0a6',4)],1,'An open notebook with a working draft');
  put('strike',1035,410,[p('M-48 -4H44',C.rose,5)],2,'One line struck through: thought that changes with evidence',1,900);
  put('rewrite',1035,410,[p('M-44 -28Q-10 -36 36 -28',C.gold,5)],2,'The struck line rewritten above it',1,2300);
  // A pencil travels along the strike, then along the rewrite, while the thinker reaches to the page.
  put('pencil',985,404,[n('path',{d:'M0 0L-7 -6L22 -40L30 -33Z',fill:C.rose}),n('path',{d:'M0 0L-7 -6L-4 6Z',fill:C.ink})],2,'The thinker\'s pencil revising the draft',1,500);
  go('pencil',2,1080,404,900,1100);go('pencil',2,990,380,2050,250);go('pencil',2,1072,380,2300,1100);
  a.actions.push({actor:'thinker',action:'reach',beat:2,offsetMs:400,durationMs:1200,untilMs:3800});
  put('laurel',920,322,laurel(),0,'The flattering ignored-genius crown, offered and then withdrawn');
  show('laurel',3,400,700);drop('laurel',3,2900,900);
  put('ring',640,492,[p('M-250 -40Q-210 -40 -180 -8',C.ink,6),n('ellipse',{cx:0,cy:0,rx:182,ry:62,fill:'none',stroke:C.gold,'stroke-width':6,'stroke-dasharray':'2 14','stroke-linecap':'round'})],4,'Coordination tied back to the podium encloses the group');
  a.objects.at(-1).visual.children[0]=a.tint(a.objects.at(-1).visual.children[0],C.pale);
  put('question',640,385,[dot(0,0,26,C.rose),t('?',0,12,36,'#ffffff')],4,'A question raised within the group',1,900);
  go('question',4,850,370,2200,1800);
  storyGesture(a,'speaker',1,'invite');storyGesture(a,'speaker',3,'explain');storyGesture(a,'thinker',3,'reflect');storyGesture(a,'speaker',4,'resolve');
  feel('speaker',1,'happy');feel('thinker',1,'curious');feel('thinker',3,'skeptical');feel('speaker',4,'determined');feel('thinker',4,'worried');
  return a.finish('A speaker on a podium sends amplified waves and a fixed "!" answer toward a crowd that drifts closer, while a quiet seated thinker strikes through and rewrites a line in a notebook with a pencil. A flattering leafy laurel wreath briefly crowns the thinker and is withdrawn; then a rope from the podium rings the crowd and a question is pushed outside it.');
 }
 if(i===1){
  // Audiences make prophets: five separate contests, then a persona built from audience reward.
  const contests=contestIcons('$ink').map(([label,icon],k)=>[label.toLowerCase(),[165,380,600,820,1035][k],130,[C.gold,C.grey,C.ink,C.rose,C.pale][k],icon,label]);
  contests.forEach(([id,x,h,fill,icon,label],k)=>{
   const iconNodes=icon.map(node=>node.attrs?.fill===C.ink?a.tint(node,C.pale):node);
   put(id,x,470,[box(-58,-h,116,h,fill,4),{...n('g'),transform:{x:0,y:-h-36},children:iconNodes},t(label,0,48,26)],1,`A separate contest: ${label}`,1,250+k*380);
   drop(id,2,0,450);
  });
  ['block-1','block-2','block-3','block-4'].forEach((id,k)=>{put(id,560,525-k*34,[box(-78,-34,156,32,k%2?C.rose:C.gold,4)],2,'Audience reward stacking into the speaker\'s platform',1,600+k*650);});
  person('prophet',560,525,{identity:'person-11-neutral',coat:C.rose,scale:.58,beat:2,offsetMs:400});
  go('prophet',2,560,391,700,2700);
  put('fans',945,500,crowd([[-90,-46,C.grey],[-30,-50,C.pale],[30,-46,C.grey],[90,-50,C.pale],[-60,0,C.pale],[0,4,C.grey],[60,0,C.pale]]),2,'Followers whose attention rewards some versions of the speaker',1,700);
  [0,1,2].forEach(k=>{const id='coin-'+k;put(id,890,410,[dot(0,0,17,C.gold),dot(0,0,8,C.paper)],2,'A unit of reward sent by the audience',1,1000+k*900);go(id,2,650,430-k*30,1200+k*900,1100);drop(id,2,2500+k*900,400);});
  put('mask',560,256,[n('path',{d:'M-30 -20Q0 -34 30 -20Q34 14 0 30Q-34 14 -30 -20Z',fill:C.gold}),p('M-20 -6L-7 -2M20 -6L7 -2',C.ink,5),p('M-12 14Q0 8 12 14',C.ink,4)],2,'The rewarded persona settles over the speaker\'s own face',1,5200);
  // Evidence arrives from the right, presses against the locked gauge and is pushed back off it.
  [['evidence-1',1110,195],['evidence-2',1110,265],['evidence-3',1110,335]].forEach(([id,x,y],k)=>{put(id,x,y,[box(-40,-28,80,56,C.paper,4),p('M-26 -10H26M-26 4H26M-26 16H8','#9aa0a6',4),p('M14 12L22 20L34 4',C.gold,5)],3,'Evidence offered against the center\'s authority',1,250+k*300);go(id,3,844,y,900+k*300,1300);go(id,3,960,y,2500+k*300,800);});
  put('gauge',775,260,[box(-26,-90,52,180,C.ink,8),box(-16,-80,32,160,C.gold,4),box(-20,-128,40,32,C.grey,6),p('M-12 -128V-142Q0 -158 12 -142V-128','$ink',6),t('Authority',0,130,26)],3,'The center\'s authority stays full and locked whatever evidence arrives',1,500);
  storyGesture(a,'prophet',2,'invite',2400);storyGesture(a,'prophet',3,'resolve');
  feel('prophet',2,'happy',1400);feel('prophet',3,'determined');
  return a.finish('Five equal pedestals show attention, credibility, authority, performance and welfare as separate contests. They clear; audience coins stack into a platform that lifts a speaker while a gold persona mask settles over the face. Evidence sheets press against a full, locked authority gauge and are pushed back while it stays full.');
 }
 // Cooperation without prophets: claims on a scale, an open ring of shared work, then the first chapter.
 put('scale',560,525,[line('M0 0V-300',9),line('M-70 0H70',9),line('M-190 -282L190 -298',8),line('M-170 -284L-200 -200M-170 -284L-140 -200M170 -297L140 -212M170 -297L200 -212',3),solid('M-232 -200H-108Q-120 -170 -170 -170Q-220 -170 -232 -200Z',C.grey),solid('M108 -212H232Q220 -182 170 -182Q120 -182 108 -212Z',C.grey)],1,'A balance that weighs contributions themselves');
 put('claim-left',390,300,[box(-36,-26,72,48,C.paper,4),p('M-22 -10H22M-22 4H14','#9aa0a6',4)],1,'A claim card on the scale');
 put('claim-right',730,288,[box(-36,-26,72,48,C.paper,4),p('M-22 -10H22M-22 4H14','#9aa0a6',4),dot(22,12,6,C.gold)],1,'A second claim with its provenance mark');
 [['name-left',390,262],['name-right',730,250]].forEach(([id,x,y],k)=>{put(id,x,y,[box(-38,-16,76,32,C.rose,8),t('Name',0,9,20,'#ffffff')],1,'A name tag lifted off the claim before weighing',1,250);go(id,1,170+k*100,505,1700+k*300,1500);});
 person('reviewer',985,525,{identity:'person-17-neutral',coat:C.gold,scale:.6});
 storyGesture(a,'reviewer',1,'question',2400);
 ['scale','claim-left','claim-right','name-left','name-right','reviewer'].forEach(id=>drop(id,2,0,450));
 put('arc',470,505,[p('M-190 -42A260 60 0 1 1 -236 22',C.gold,6)],2,'An open ring: the incomplete tribe leaves a gap for departure',1,500);
 put('build',470,520,[box(-110,-40,70,40,C.grey,3),box(-35,-40,70,40,C.gold,3),box(40,-40,70,40,C.grey,3),box(-72,-80,70,40,C.rose,3),box(2,-80,70,40,C.grey,3)],2,'The shared project the group builds together',1,600);
 put('old-block',470,440,[box(-35,-40,70,40,C.pale,3)],2,'A top piece that later proves wrong',1,600);
 person('m-left',290,525,{identity:'person-04-neutral',coat:C.grey,scale:.55,beat:2,offsetMs:700});
 person('m-right',650,525,{identity:'person-14-neutral',coat:C.rose,scale:.55,beat:2,offsetMs:900});
 person('leaver',215,525,{identity:'person-21-neutral',coat:C.gold,scale:.5,beat:2,offsetMs:800});
 go('leaver',2,95,525,3600,2200);
 put('differ',705,330,[n('path',{d:'M-34 -24H34V14H8L-4 28L-6 14H-34Z',fill:C.paper}),p('M-16 -10H16M-16 2H16M10 -18L-10 10',C.rose,4)],2,'A member openly disagrees inside the group',1,2400);
 drop('old-block',3,400,700);
 put('new-block',470,440,[box(-35,-40,70,40,C.gold,3),p('M-14 -20L-3 -9L15 -30','#ffffff',5)],3,'The corrected piece replaces the wrong one while work continues',1,1200);
 put('halo',470,318,[n('ellipse',{cx:0,cy:0,rx:62,ry:17,fill:'none',stroke:C.gold,'stroke-width':9}),...[-50,-25,0,25,50].map(dx=>p(`M${dx*1.25} ${-26-(dx?0:6)+Math.abs(dx)*.14}L${dx*1.5} ${-44-(dx?0:8)+Math.abs(dx)*.18}`,C.gold,5))],3,'An empty halo floating over no one: no messiah is waiting at the center',1,2200);
 // Outside ties: two people beyond the ring stay connected to members inside it.
 put('ties',800,496,[...[[-65,-8,50,-44],[-65,24,58,44]].map(([x1,y1,x2,y2])=>n('path',{d:`M${x1} ${y1}L${x2-26} ${y2}`,fill:'none',stroke:C.grey,'stroke-width':4,'stroke-dasharray':'2 10','stroke-linecap':'round'})),...listener(70,-44,C.pale),...listener(80,44,C.grey)],2,'Ties to people outside the group stay open',1,1600);
 drop('ties',4,0,450);
 // Callback for the closing question: the five contests, now asked of the viewer's own trusted voices.
 contestIcons().forEach(([label,icon],k)=>put('recall-'+k,100+k*66,205,[dot(0,0,28,C.paper),{...n('g'),transform:{x:0,y:0,scale:.62},children:icon}],4,`The ${label.toLowerCase()} contest, recalled`,1,1500+k*220));
 put('recall-ask',100+5*66,205,[dot(0,0,22,C.rose),t('?',0,10,30,'#ffffff')],4,'Which contest did your trusted voices win?',1,2700);
 storyGesture(a,'m-right',2,'question',2600);storyGesture(a,'m-left',3,'explain');storyGesture(a,'m-right',4,'invite');
 put('book',935,400,[n('path',{d:'M-150 -95Q-75 -112 0 -88Q75 -112 150 -95V95Q75 80 0 102Q-75 80 -150 95Z',fill:C.paper}),p('M0 -88V102','#9aa0a6',3),t('1',-75,-48,26,C.rose),t('Who Gets',-75,-12,26,C.ink),t('Heard',-75,18,26,C.ink),p('M-118 46H-32M-118 62H-44M32 -52H118M32 -34H112M32 -16H118M32 2H100M32 20H118M32 38H108','#aab0b5',3),n('path',{d:'M-30 -100H-12V-40L-21 -50L-30 -40Z',fill:C.rose})],4,'The book open at its first chapter, “Who Gets Heard”',1,400);
 feel('reviewer',1,'curious');feel('m-left',2,'happy',800);feel('m-right',2,'skeptical',2600);feel('m-left',3,'inspired');feel('m-left',4,'happy');feel('m-right',3,'relieved',1400);feel('m-right',4,'inspired');
 return a.finish('Name tags lift off two claim cards on a balance while a person examines it. The scale clears for an open gold ring around a shared build: one member disagrees, another leaves through the gap, and a wrong top block is replaced as work continues beneath an empty halo, while dotted ties reach two people outside the ring. The book opens at chapter one, “Who Gets Heard”, as the five contest icons return with a question.');
}

scenes.forEach((scene,i)=>{scene.visual=compose(i);});
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('Staged '+scenes.length+' scenes for The Messiah Factory.');
