import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
 const a=stageAuthor(),{n,path,text,tint,dot}=a,c={plum:'#866c93',gold:'#cba557',coral:'#cf8168',blue:'#5789a6',silver:'#b6d8d5',ink:'#334355',paper:'#f0e3c9',green:'#75998a'};
 const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
 const fill=(d,col,night=col)=>tint(n('path',{d,fill:col}),night);
 const rect=(x,y,w,h,col,rx=0)=>n('rect',{x,y,width:w,height:h,rx,fill:col});
 const label=(v,x,y,size=27,col='$ink')=>text(v,x,y,size,col);
 const act=(id,beat,action,extra={})=>a.actions.push({actor:id,action,beat,durationMs:1900,...extra});
 const person=(id,x,y,coat,identity='person-03-neutral',scale=.88,seated=false)=>{storyPerson(a,id,x,y,{coat,identity,scale,seated,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;};
 const gesture=(id,b,g)=>storyGesture(a,id,b,g,2100);
 const look=(id,to,b)=>act(id,b,'lookAt',{target:to,durationMs:850});
 const expression=(id,b,e)=>act(id,b,'character.express',{emotion:e,durationMs:850});
 const table=(id,x,y,w=450)=>obj(id,x,y,[fill(`M${-w/2} -17Q0 -37 ${w/2} -17V7H${-w/2}Z`,c.gold),path(`M${-w/2+35} 8V90M${w/2-35} 8V90`,c.gold,15)],'A physically supported table holds particular objects and the people’s shared attention');
 const card=(id,x,y,w,h,lines,color=c.paper)=>obj(id,x,y,[rect(-w/2,-h,w,h,color,4),...lines.map((v,j)=>label(v,0,-h+36+j*32,25,c.ink))],'A particular written record remains connected to its source and its reader');
 const kesh=(id,x,y,k=1)=>{person(id,x,y,c.blue,'person-02-neutral',k);const o=a.objects.at(-1);o.meaning='Kesh in his6D body: work vest, translucent skin and visible luminous filaments; no ordinary opaque human substitute.';const walk=node=>{if(node.attrs?.fill&&['#c98e6b'].includes(node.attrs.fill.toLowerCase()))node.attrs.fill=c.silver;for(const child of node.children||[])walk(child)};walk(o.visual);o.visual.children.find(x=>x.id==='$asset.head').children.push(path('M-16 -18Q-6 -12 -14 11M12 -20Q1 -8 18 12',c.blue,2.4));for(const side of ['armL','armR']){const arm=o.visual.children.find(x=>x.id==='$asset.'+side);arm.children[0].attrs.stroke=c.silver;arm.children.push(path(side==='armL'?'M-36 -152Q-49 -132 -42 -113':'M35 -150Q48 -137 48 -119',c.blue,3));}};
 if(i===0){
  // A spatial translation of a silar, not literal7D architecture.
  person('taal',233,510,c.blue,'person-02-neutral',.85,true);
  person('mother-preserved',567,497,c.gold,'person-04-neutral',.89);a.objects.at(-1).visual.attrs.opacity=.42;a.objects.at(-1).visual.themeAttrs={night:{opacity:.64}};
  person('mother-warmth',567,497,c.gold,'person-04-neutral',.89);act('mother-warmth',2,'disappear',{durationMs:3300});
  person('sera',428,522,c.plum,'person-03-neutral',.95,true);
  obj('mother-hand',506,341,[path('M25 -4Q2 -7 -21 0','#d6a17f',11)],'The mother’s remembered hand rests on Sera’s shoulder; no literal death is depicted');
  table('sunday-table',338,435,410);obj('fruit',342,419,[n('ellipse',{cx:0,cy:0,rx:72,ry:17,fill:c.paper}),fill('M-43 -5Q-30 -43 -2 -6Z',c.coral),fill('M5 -5Q21 -37 43 -4Z',c.coral),path('M-25 -8L-20 -20M19 -7L22 -20',c.gold,3)],'Cut fruit anchors the source’s sensory Sunday rather than a generic memory icon');
  obj('two-cups',338,410,[-99,92].flatMap(x=>[rect(x-16,-31,31,32,c.silver,5),path(`M${x+15} -25Q${x+35} -24 ${x+16} -5`,c.silver,5)]),'Tactile tableware belongs to the opening meal, not the protected final second-cup scene');
  obj('hypothetical-cradle',893,422,[{...n('g',{opacity:.44}),themeAttrs:{night:{opacity:.78}},children:[path('M-96 -65Q0 -24 92 -65L65 10H-65Z',c.blue,8),path('M-77 -31L-85 49M77 -31L85 49M-108 52Q0 83 108 52',c.blue,8),path('M-53 -30V2M-20 -18V5M20 -18V5M53 -30V2',c.blue,4)]},label('Possible child',0,-116,29),label('Not yet created',0,108,24)],'A visibly faint empty cradle represents a hypothetical future person; no actual child exists in this configuration');a.reveal('hypothetical-cradle',3);
  obj('compatibility',783,235,[n('circle',{cx:0,cy:0,r:35,fill:c.paper}),path('M-18 0H18M0 -18V18',c.plum,5),label('Limited support',0,-60,26)],'A conceptual allocation cue makes the competition between compatibilities visible without using money or a stock market');a.reveal('compatibility',2);a.move('compatibility',3,838,237,2400);a.move('compatibility',4,806,237,1700);
  look('sera','mother-warmth',1);gesture('sera',2,'recoil');expression('sera',2,'worried');look('sera','hypothetical-cradle',3);gesture('sera',4,'resolve');expression('sera',4,'determined');gesture('taal',5,'reflect');gesture('sera',6,'reflect');
 }else if(i===1){
  obj('transfer-floor',574,512,[fill('M-420 -11H367L426 49H-443Z','#95b1b3')],'A maintained station surface makes the first embodied weight tangible');
  person('sera-unavailable',295,486,c.plum,'person-03-neutral',.86);a.objects.at(-1).visual.attrs.opacity=.20;a.objects.at(-1).visual.themeAttrs={night:{opacity:.40}};
  person('sera',435,522,c.plum,'person-03-neutral',1.02);kesh('kesh',749,515,.99);
  obj('support-rail',473,382,[path('M-80 -10H84M-65 -10V161M71 -10V161',c.blue,12)],'Sera braces against a fixed support as sensation arrives in one body');
  obj('regulator',696,414,Array.from({length:6},(_,j)=>n('ellipse',{cx:0,cy:0,rx:40-j*5,ry:49-j*6,fill:'none',stroke:j%2?c.gold:c.silver,'stroke-width':3})),'Kesh’s source-specific six-frame regulator mediates bodily continuity');a.move('regulator',2,701,414,2400);
  table('engineer-station',971,449,238);card('family-photo',972,428,174,126,[],c.silver);
  obj('family-in-photo',972,400,[...[-43,0,43].flatMap((x,j)=>[dot(x,j===2?-5:-20,j===2?12:16,c.paper),fill(`M${x-17} ${j===2?12:0}Q${x} ${j===2?2:-12} ${x+17} ${j===2?12:0}V28H${x-17}Z`,j===2?c.gold:c.blue)]),label('Kesh’s family',0,64,25)],'A deliberately simplified3D photograph of Kesh’s partners and daughter gives the engineer an independent stake');a.reveal('family-in-photo',3);
  obj('descent-band',486,361,[path('M-20 -9Q0 8 21 -7',c.ink,12),...[-15,-9,-3,3,9,15].map(x=>dot(x,-3+Math.cos(x/20)*3,2.4,c.gold))],'The descent band marks freedoms available here and unavailable below');a.reveal('descent-band',4);
  look('sera','support-rail',1);expression('sera',1,'surprised');gesture('sera',2,'reflect');look('kesh','sera',2);expression('kesh',2,'curious');look('sera','family-in-photo',3);look('kesh','family-in-photo',3);expression('kesh',3,'worried');expression('sera',4,'worried');gesture('sera',5,'question');expression('kesh',6,'determined');
 }else if(i===2){
  person('mira',590,533,c.green,'person-01-neutral',1.03,true);table('archive-desk',604,452,850);
  card('raw-report',351,430,210,211,['Nera Vil','Tom','Named guides']);
  card('official-report',858,430,236,211,['Public version','Unidentified','persons']);a.reveal('official-report',4);
  obj('instruction',887,163,[rect(-128,-46,256,80,c.paper,4),label('Authorized wording',0,-9,25,c.ink),path('M-90 14H90',c.plum,3)],'An official instruction changes how responsibility may be described');a.reveal('instruction',2);
  obj('pen',687,376,[path('M-22 29L15 -29',c.plum,9),fill('M-29 38L-25 23L-15 30Z',c.gold)],'The clerk’s pen pauses before complying with the authorized rewrite');a.move('pen',2,741,381,2300);a.move('pen',4,623,401,2400);
  obj('hidden-notebook',632,435,[rect(-74,-91,148,91,c.gold,4),rect(-65,-83,130,76,c.paper,2),label('Serad Tov',0,-54,20,c.ink),label('Parel Im',0,-27,20,c.ink)],'Mira retains the named agents in a small private notebook; later discoveries remain protected');a.reveal('hidden-notebook',4);a.move('hidden-notebook',5,572,436,2300);
  obj('sleeve',570,432,[fill('M-65 -14Q-8 -48 54 -4L44 27H-65Z',c.green)],'A work sleeve partly shields the private record while leaving enough of the retained names readable');a.reveal('sleeve',5);
  obj('public-tray',1035,442,[fill('M-106 -38H92L76 8H-98Z',c.blue),label('Public record',0,56,25)],'The authorized version travels outward while the named responsibility remains in a separate record');a.reveal('public-tray',4);a.move('official-report',5,1039,434,2600);
  look('mira','raw-report',1);gesture('mira',2,'reflect');expression('mira',2,'worried');look('mira','instruction',3);expression('mira',4,'determined');look('mira','hidden-notebook',4);gesture('mira',6,'reflect');
 }else{
  obj('case-volume',593,379,[fill('M-435 -137Q-210 -171 -5 -131Q197 -174 425 -136L446 153Q207 112 0 170Q-220 112 -448 152Z',c.plum),fill('M-424 -146Q-205 -177 -7 -139V150Q-216 112 -432 137Z',c.paper),fill('M8 -139Q199 -177 418 -146L431 137Q214 112 8 150Z','#f5ead3'),path('M0 -135V148',c.gold,4)],'An open case volume establishes the reader’s view without pretending the higher-dimensional home is a book-shaped room');
  obj('source-tabs',604,229,[rect(-345,-39,198,39,c.gold,3),label('The File',-246,-12,26,c.ink),rect(75,-39,204,39,c.silver,3),label('Descent',177,-12,26,c.ink)],'The source chapter tabs give a precise reading route');
  obj('meal-detail',370,353,[n('ellipse',{cx:0,cy:0,rx:93,ry:18,fill:c.gold}),path('M-65 10V75M63 10V75',c.gold,9),n('ellipse',{cx:0,cy:-6,rx:37,ry:9,fill:'#fff5df'}),fill('M-19 -9Q-10 -30 9 -9Z',c.coral),rect(-67,-35,20,27,c.silver,3),label('Compatible histories',0,127,24,c.ink)],'The opening household remains a particular unresolved compatibility');
  obj('bodily-detail',811,357,[path('M-71 55H66M-60 55V110M56 55V110',c.blue,9),fill('M-17 -39Q0 -50 21 -36L36 36H-34Z',c.plum),dot(1,-70,23,'#d7a380'),path('M-18 34L-30 80M20 34L32 80M-22 -25L-49 56',c.plum,10),label('Available freedoms',0,127,24,c.ink)],'A small body-height station illustration connects dimensions to available action');
  obj('testimony-foldout',673,362,[fill('M-60 -40H93L81 65H-74Z',c.paper),path('M-54 -27H67M-57 -4H57',c.plum,3),label('Nera Vil',9,24,19,c.ink),label('Tom',9,47,19,c.ink)],'The case’s particular names remain attached to the next page rather than becoming a decorative cosmos icon');a.reveal('testimony-foldout',3);
  obj('reader-finger',1070,476,[fill('M-21 50L-37 2Q-45 -11 -36 -18Q-28 -20 -17 -2L-11 8L-10 -56Q-6 -76 5 -70L8 -13L27 -20Q40 -16 31 45Z','#c79574')],'A reader follows the source terms to their consequences and leaves the later verdict unread');a.move('reader-finger',2,1021,466,2100);a.move('reader-finger',5,973,455,2200);
 }
 s.visual=a.finish(s.adaptation.composition+' The7D household is a spatial translation, its withdrawal remains provisional, no infant is born, and later case outcomes stay protected.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
