import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const root=new URL('.',import.meta.url).pathname,scenes=JSON.parse(fs.readFileSync(root+'scenes.json'));
const C={teal:'#327f81',pale:'#b4d1c3',coral:'#db8169',ochre:'#d9af5f',plum:'#84678b',paper:'#f5ead5',ink:'#273f4b',blue:'#81b6ca'};
function house(q,id,x,y,{w=150,h=190,color=C.coral,kind='home',scale=1}={}){
 const {n,path,dot,text,object}=q,a=[];a.push(n('path',{d:`M${-w/2} 0V${-h}L0 ${-h-35}L${w/2} ${-h}V0Z`,fill:color}));
 a.push(n('path',{d:`M${-w/2-10} ${-h}L0 ${-h-43}L${w/2+10} ${-h}`,fill:'none',stroke:C.ink,'stroke-width':9,'stroke-linejoin':'round'}));
 for(let r=0;r<(h>160?2:1);r++)for(let c=0;c<2;c++){let xx=-w/2+22+c*(w-65),yy=-h+24+r*55;a.push(n('rect',{x:xx,y:yy,width:30,height:39,rx:3,fill:C.paper}),path(`M${xx+15} ${yy}V${yy+39}M${xx} ${yy+20}H${xx+30}`,color,3));}
 a.push(n('path',{d:'M-22 0V-53Q0 -75 22 -53V0Z',fill:C.ink}),dot(12,-25,3,C.ochre));
 if(kind==='care')a.push(n('rect',{x:-w/2-12,y:-h+5,width:w+24,height:30,rx:3,fill:C.pale}),text('Care',0,-h+28,24,C.ink));
 if(kind==='school')a.push(n('rect',{x:-w/2-8,y:-h+5,width:w+16,height:30,rx:3,fill:C.ochre}),text('School',0,-h+28,24,C.ink));
 if(kind==='work'){a.push(n('rect',{x:-w/2+10,y:-54,width:w-20,height:48,fill:C.blue}),path(`M${-w/2+10} -30H${w/2-10}`,C.ink,3));}
 return q.add(object(id,x,y,a,`An occupied ${kind} building in an illustrative neighbourhood; not a measured geographical case.`,scale));
}
function tree(q,id,x,y,s=.8){q.add(q.object(id,x,y,[q.path('M0 0V-70',C.ink,9),q.dot(-17,-78,29,C.pale),q.dot(15,-100,34,C.teal),q.dot(32,-67,25,C.pale)],'A planted courtyard tree.',s));}
function bench(q,id,x,y){q.add(q.object(id,x,y,[q.n('rect',{x:-72,y:-14,width:144,height:13,rx:4,fill:C.ochre}),q.path('M-59 0V32M59 0V32',C.ink,7)],'A bench supports a seated person.'));}
function bus(q,id,x,y,s=.7){q.add(q.object(id,x,y,[q.n('rect',{x:-75,y:-45,width:150,height:53,rx:13,fill:C.ochre}),...[-55,-15,25].map(xx=>q.n('rect',{x:xx,y:-36,width:30,height:25,rx:4,fill:C.ink})),q.dot(-46,8,13,C.ink),q.dot(46,8,13,C.ink),q.dot(-46,8,5,C.paper),q.dot(46,8,5,C.paper)],'The illustrated commute vehicle moves along its visible route.',s));}
function bag(q,id,x,y){q.add(q.object(id,x,y,[q.n('rect',{x:-15,y:-17,width:30,height:34,rx:5,fill:C.ochre}),q.path('M-8 -17V-24Q0 -31 8 -24V-17',C.ink,3)],'A school satchel changes hands when nearby care is available.'));}
function futurePlaces(q,id,x,y,s=1){q.add(q.object(id,x,y,[q.n('rect',{x:-75,y:-24,width:150,height:48,rx:14,fill:C.paper}),q.dot(-34,0,16,'none'),...[-34,34].map(xx=>q.n('circle',{cx:xx,cy:0,r:17,fill:'none',stroke:C.coral,'stroke-width':3,'stroke-dasharray':'4 4'})),q.path('M-59 -12V12M59 -12V12',C.ink,3)],'Two unoccupied future place settings depict the same stated wish, not actual children or a predicted birth.',s));}
function desk(q,id,x,y,w=580){q.add(q.object(id,x,y,[q.n('path',{d:`M${-w/2} -15H${w/2}L${w/2+30} 18H${-w/2-30}Z`,fill:C.ochre}),q.tint(q.path(`M${-w/2+25} 20V93M${w/2-25} 20V93`,C.ink,12),'#92a8b6')],'A real surface for comparing distinct research records.'));}
function leaf(q,id,x,y,label,color,w=210,h=150){q.add(q.object(id,x,y,[q.n('path',{d:`M${-w/2} ${-h/2}Q0 ${-h/2-10} ${w/2} ${-h/2}V${h/2}Q0 ${h/2-8} ${-w/2} ${h/2}Z`,fill:C.paper}),q.n('rect',{x:-w/2,y:-h/2,width:10,height:h,fill:color}),q.text(label,0,-h/2+33,25,C.ink),...(h>=120?[-12,12,36]:[20,37]).map(yy=>q.path(`M${-w/2+28} ${yy}H${w/2-25}`,color,3))],`Research page labelled ${label}; marks are illustrative layout, not empirical data.`));}
function gaze(q,id,beat,expression,gesture){q.actions.push({actor:id,action:'character.express',emotion:({confident:'determined',concerned:'worried',thoughtful:'curious',warm:'happy',hopeful:'inspired'})[expression]||expression,beat,durationMs:1000});if(gesture)storyGesture(q,id,beat,gesture);}
function hideSet(q,ids,beat){ids.forEach(id=>q.hide(id,beat));}
// 1: a workplace moves beyond the reach of an inhabited care courtyard.
{
 const q=stageAuthor(),{n,path,text,object}=q;
 q.add(object('courtyard',380,513,[n('path',{d:'M-240 -3Q-110 -25 10 -3L295 -3L335 30H-250Z',fill:C.pale}),path('M-215 -8H-52L-52 -57H25',C.paper,18)],'The home courtyard is a shared physical place, not a generic backdrop.'));
 house(q,'home',235,470,{color:C.coral,w:180,h:185});tree(q,'tree',118,501);house(q,'workplace',605,360,{color:C.teal,w:180,h:180,kind:'work'});
 q.add(object('stair',470,453,[n('path',{d:'M-115 0H-75V-30H-35V-60H5V-90H45V-120H85V0Z',fill:C.ochre})],'A career stair rises toward an occupied workplace.'));
 q.add(object('near-route',482,465,[path('M-160 0Q-45 -10 70 -86',C.blue,14)],'Initial connection between the professional route and home.'));
 q.add(object('long-route',690,463,[path('M-368 2H-218Q-190 2 -190 -26V-38H155V-100',C.blue,14)],'The longer connection visually enacts the increased journey, not a biological change.'));
 storyPerson(q,'professional',424,418,{identity:'person-09-neutral',coat:C.plum,scale:.48});storyPerson(q,'caregiver',320,513,{identity:'person-17-neutral',coat:C.teal,scale:.5});storyPerson(q,'child',372,516,{identity:'person-02-neutral',coat:C.ochre,scale:.28});bag(q,'satchel',349,441);
 q.label('work-label','Work',605,135,29);q.label('home-label','Home and care',248,218,29);
 const opening=q.objects.map(o=>o.id);q.hide('long-route',1);q.move('professional',1,520,332,2700);gaze(q,'professional',1,'confident','resolve');
 q.move('workplace',2,885,360,2600);q.move('work-label',2,885,135,2600);q.move('professional',2,800,332,2600);q.hide('near-route',2);q.reveal('long-route',2);gaze(q,'caregiver',2,'concerned','question');
 gaze(q,'professional',3,'thoughtful','reflect');
 hideSet(q,opening,4);desk(q,'study-desk',610,465,840);
 const labels=['Genetic','Cultural','Social','Demographic'];for(let i=0;i<4;i++){leaf(q,'ledger-'+i,280+i*220,349,labels[i],[C.coral,C.teal,C.plum,C.ochre][i],190,165);q.reveal('ledger-'+i,4,1000+i*220);}
 q.add(object('magnifier',870,425,[n('circle',{cx:0,cy:0,r:31,fill:'none',stroke:C.ink,'stroke-width':8}),path('M22 22L51 51',C.ink,12)],'A magnifier traverses separate records rather than merging their explanations.'));q.reveal('study-desk',4);q.reveal('magnifier',5);q.move('magnifier',5,433,424,2300);
 scenes[0].visual=q.finish('Inhabited home and care are pulled apart from professional opportunity, then the essay opens four distinct kinds of inquiry.');
}
// 2: equal wishes have physically different time and care arrangements.
{
 const q=stageAuthor(),{n,path,text,object}=q;
 for(const [id,x,color]of [['near',298,C.coral],['far',887,C.blue]]){
  q.add(object(id+'-room',x,442,[n('path',{d:'M-205 0V-210H190V0Z',fill:color}),n('rect',{x:-174,y:-180,width:92,height:100,rx:6,fill:C.paper}),path('M-128 -180V-80M-174 -130H-82',color,5),n('path',{d:'M-220 0H210L235 36H-245Z',fill:C.pale})],'An equally dignified domestic interior with room to compare logistics.'));
  futurePlaces(q,id+'-wish',x,203,1.1);
 }
 q.label('wish-label','A wish for two children',600,132,31);
 storyPerson(q,'near-parent',269,474,{identity:'person-09-neutral',coat:C.plum,scale:.5});storyPerson(q,'grandparent',429,471,{identity:'person-17-neutral',coat:C.teal,scale:.49});bag(q,'care-bag',404,398);
 storyPerson(q,'far-parent',816,473,{identity:'person-09-neutral',coat:C.plum,scale:.5});
 q.add(object('moving-box',967,445,[n('path',{d:'M-42 -45H40V23H-42Z',fill:C.ochre}),path('M0 -45V23',C.paper,5),n('path',{d:'M-42 -45L-61 -70H-8L0 -45L16 -64H61L40 -45Z',fill:C.paper})],'The unpacked box represents repeated relocation rather than low personal commitment.'));
 q.add(object('near-evening',285,530,[n('rect',{x:-175,y:-12,width:350,height:22,rx:6,fill:C.pale}),n('rect',{x:-175,y:-12,width:70,height:22,rx:6,fill:C.ochre}),text('Travel',-140,-22,22),text('Available time',42,-22,22)],'Short travel leaves a larger evening interval; proportions are illustrative, not measured data.'));
 q.add(object('far-evening',887,530,[n('rect',{x:-175,y:-12,width:350,height:22,rx:6,fill:C.pale}),n('rect',{x:-175,y:-12,width:248,height:22,rx:6,fill:C.ochre}),text('Long commute',-50,-22,22)],'The long commute occupies the evening region and stays unchanged through the scene.'));
 bus(q,'commute-bus',759,471,.55);q.reveal('grandparent',2);q.reveal('care-bag',2);q.move('care-bag',2,307,399,2400);gaze(q,'grandparent',2,'warm','invite');gaze(q,'near-parent',2,'warm','release');
 q.reveal('moving-box',3);q.reveal('commute-bus',3);q.move('commute-bus',3,1041,471,3200);q.reveal('far-evening',3);gaze(q,'far-parent',3,'concerned','reflect');gaze(q,'near-parent',4,'thoughtful','reflect');gaze(q,'far-parent',5,'thoughtful','question');
 scenes[1].visual=q.finish('Two equally valued people share a stated family wish; a care handoff and unequal travel time demonstrate the different obstacles, with no predicted births or barrier removal.');
}
// 3: a hinged scenario model reduces distance while preserving different uses.
{
 const q=stageAuthor(),{n,path,text,object}=q;
 q.add(object('model-table',650,501,[n('path',{d:'M-365 -45L225 -45L400 24L-185 24Z',fill:C.paper}),q.tint(path('M-300 20V77M330 25V80',C.ink,12),'#92a8b6')],'An explicitly hypothetical city model rests on a planning table.'));
 q.add(object('scenario-tab',392,160,[n('path',{d:'M-84 -20H77L95 19H-84Z',fill:C.ochre}),text('Scenario',0,7,26,C.ink)],'The model is a scenario rather than a forecast or implemented intervention.'));
 house(q,'model-home',470,470,{w:135,h:135,color:C.coral,scale:.85});house(q,'model-school',688,470,{w:130,h:145,color:C.ochre,kind:'school',scale:.85});house(q,'model-work',816,465,{w:130,h:125,color:C.teal,kind:'work',scale:.8});house(q,'model-care',1020,500,{w:140,h:140,color:C.blue,kind:'care',scale:.8});
 q.add(object('long-journey',720,510,[path('M-248 -20H-120V-44H175V-10H310',C.blue,12)],'A distant service requires a long journey through the original model.'));
 q.add(object('short-walk',573,492,[path('M-100 -23Q-48 6 44 -12',C.teal,12)],'Moving care into the courtyard creates a shorter walk without moving the household.'));
 storyPerson(q,'planner',132,515,{identity:'person-17-neutral',coat:C.teal,scale:.68});storyPerson(q,'parent',265,520,{identity:'person-09-neutral',coat:C.plum,scale:.56});bag(q,'model-bag',283,434);
 q.reveal('model-table',1);q.hide('short-walk',1);gaze(q,'planner',1,'thoughtful','explain');q.move('model-care',2,586,479,3100);q.hide('long-journey',2);q.reveal('short-walk',2);gaze(q,'planner',2,'warm','invite');
 futurePlaces(q,'future-table',637,515,.76);q.reveal('future-table',3);gaze(q,'parent',3,'hopeful','release');tree(q,'courtyard-tree',736,488,.47);q.reveal('courtyard-tree',4);gaze(q,'planner',4,'confident','explain');gaze(q,'parent',5,'thoughtful','reflect');
 // The three folded alternative plans remain a comparison, not resolved outcomes.
 for(let i=0;i<3;i++){let x=516+i*190;q.add(object('alternative-'+i,x,198,[n('path',{d:'M-72 -40H60L77 34H-60Z',fill:[C.blue,C.pale,C.plum][i]}),...(i===0?[n('path',{d:'M-27 20V-26H-3V20M9 20V-13H30V20',fill:C.paper})]:i===1?[-30,3,30].map(xx=>n('path',{d:`M${xx-10} 18V-3L${xx} -12L${xx+10} -3V18Z`,fill:C.paper})):[path('M-29 -15L30 16M-29 16L30 -15',C.paper,3),q.dot(-29,-15,6,C.paper),q.dot(30,16,6,C.paper),q.dot(-29,16,6,C.paper),q.dot(30,-15,6,C.paper)])],['Alternative dense megacity model','Alternative clustered community model','Alternative algorithmic matching model'][i]));q.reveal('alternative-'+i,6,1300+i*200);}
 scenes[2].visual=q.finish('A explicitly hypothetical neighbourhood model moves care closer to unchanged housing, preserving school and work, then opens comparison with other future arrangements.');
}
// 4: a reader opens the mechanisms and evidence, then sees varied lives in their context.
{
 const q=stageAuthor(),{n,path,text,object}=q;
 desk(q,'reading-table',635,470,780);
 q.add(object('open-book',643,344,[n('path',{d:'M-300 -125Q-160 -154 0 -107Q160 -154 300 -125V132Q154 104 0 139Q-154 104 -300 132Z',fill:C.teal}),n('path',{d:'M-287 -133Q-146 -150 -6 -112V125Q-145 98 -287 119Z',fill:C.paper}),n('path',{d:'M6 -112Q146 -150 287 -133V119Q145 98 6 125Z',fill:C.paper}),path('M0 -105V129',C.ochre,4)],'A correctly bound open volume supports the linked reading journey.'));
 q.add(object('book-print',643,344,[text('Chapter 4',-145,-75,31,C.ink),text('Chapter 18',145,-75,31,C.ink),text('Institutions',-145,-34,24,C.ink),text('Proximity',145,-34,24,C.ink),...[-145,145].flatMap(xx=>[-5,18,41,64,87].map(yy=>path(`M${xx-98} ${yy}H${xx+98}`,C.pale,4)))],'A correctly constructed open volume connects the explicitly recommended chapters.'));
 storyPerson(q,'reader',165,517,{identity:'person-09-neutral',coat:C.plum,seated:true,scale:.66});gaze(q,'reader',1,'thoughtful','reflect');
 leaf(q,'evidence-fold',648,166,'Evidence appendix',C.coral,540,92);q.reveal('evidence-fold',2);
 q.add(object('evidence-tabs',645,332,[...['Finding','Hypothesis','Test'].flatMap((s,i)=>[n('rect',{x:-234+i*160,y:-30,width:148,height:62,rx:6,fill:[C.pale,C.ochre,C.blue][i]}),text(s,-160+i*160,8,22,C.ink)])],'Distinct confidence categories on the evidence foldout; no fabricated study values.'));q.reveal('evidence-tabs',2);q.reveal('book-print',1);q.hide('book-print',2);q.reveal('book-print',5);q.hide('evidence-tabs',5);
 q.add(object('pencil',840,405,[path('M-52 19L45 -17',C.coral,8),n('path',{d:'M45 -21L62 -25L49 -12Z',fill:C.ink})],'The reader traces a specific line of inquiry rather than assigning a destiny to a person.'));q.reveal('pencil',3);q.move('pencil',3,489,405,2700);gaze(q,'reader',3,'concerned','question');gaze(q,'reader',4,'warm','release');q.move('pencil',5,496,291,2200);gaze(q,'reader',5,'curious','invite');
 hideSet(q,['evidence-fold','evidence-tabs','pencil','book-print'],6);
 q.add(object('courtyard-spread',644,392,[n('path',{d:'M-267 78V-68H-128V78M105 78V-100H266V78',fill:C.coral}),n('path',{d:'M-268 -68L-197 -103L-128 -68M105 -100L185 -135L266 -100',fill:'none',stroke:C.teal,'stroke-width':10}),n('rect',{x:-239,y:-46,width:43,height:60,fill:C.paper}),n('rect',{x:149,y:-75,width:43,height:59,fill:C.paper}),path('M-116 71H100',C.pale,35)],'The closing spread opens conceptually into multiple lives, not a claimed policy outcome.'));
 q.reveal('courtyard-spread',6);
 storyPerson(q,'artist',578,455,{identity:'person-05-neutral',coat:C.coral,scale:.39});storyPerson(q,'craft-worker',740,455,{identity:'person-17-neutral',coat:C.teal,scale:.39});q.reveal('artist',6);q.reveal('craft-worker',6);
 q.add(object('easel',524,452,[path('M-23 0L0 -109L25 0',C.ink,5),n('rect',{x:-28,y:-103,width:57,height:54,fill:C.ochre}),path('M-23 -62Q0 -86 23 -59',C.teal,5)],'An artist makes a particular picture in a continuing professional niche.'));q.reveal('easel',6);
 q.add(object('craft-bench',805,431,[n('rect',{x:-40,y:-9,width:80,height:14,fill:C.ochre}),path('M-30 4V28M30 4V28',C.ink,5),n('path',{d:'M-9 -10L-14 -30Q0 -43 14 -30L9 -10Z',fill:C.blue})],'A craft worker shapes a vessel at a supported bench.'));q.reveal('craft-bench',6);gaze(q,'artist',6,'warm','explain');gaze(q,'craft-worker',6,'confident','resolve');
 scenes[3].visual=q.finish('An actual open book links institutional filters to the proximity scenario, distinguishes evidence from hypotheses, and ends with varied activities rather than prescribed family outcomes.');
}
fs.writeFileSync(root+'scenes.json',JSON.stringify(scenes,null,2)+'\n');
console.log('Authored four original enacted architectural/readership compositions.');
