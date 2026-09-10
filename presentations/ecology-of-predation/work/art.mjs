import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const r=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',r)));
const c={ink:'#24374b',paper:'#f5edda',jade:'#3d9c85',rose:'#dc806b',gold:'#e6b550',blue:'#658cb5',wood:'#b98363',lavender:'#ae9bc4'};
function env(q){
 const {n,path,text,dot,object}=q;
 const shape=(id,x,y,ch,meaning)=>q.add(object(id,x,y,ch,meaning));
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const paper=(id,x,y,title,{color=c.paper,w=156,h=145,scale=1,mark=false}={})=>q.add(object(id,x,y,[rect(-w/2,0,w,h,color,4),text(title,0,32,25,c.ink),path(`M${-w/2+20} 55H${w/2-20}M${-w/2+20} 73H${w/2-32}M${-w/2+20} 91H${w/2-23}`,c.ink,3),...(mark?[path('M-40 116L-22 127L8 104',c.jade,5)]:[])],`Physical working document: ${title}`,scale));
 const desk=(id,x,y,w=380)=>shape(id,x,y,[rect(-w/2,-14,w,27,c.wood,7),path(`M${-w/2+25} 13L${-w/2+12} 112M${w/2-25} 13L${w/2-12} 112`,c.wood,15)],'Work desk supporting the active documents.');
 const archive=(id,x,y)=>shape(id,x,y,[rect(-126,-160,252,286,c.blue,10),rect(-109,-132,218,105,c.paper,4),rect(-109,-10,218,105,c.paper,4),...[0,1,2,3,4].map((v)=>rect(-98+v*39,-112,27,68,[c.jade,c.rose,c.gold,c.lavender,c.blue][v],3)),path('M-60 38H62M-40 54H40',c.ink,6),text('Learned work',0,85,25,c.ink)],'Provider-managed working archive retains learned operational context.');
 const person=(id,x,y,scale=.95,coat=c.jade,seated=false)=>storyPerson(q,id,x,y,{identity:'person-04-neutral',coat,scale,seated,chair:c.lavender});
 const emotion=(id,beat,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat,durationMs:1000});
 return {shape,rect,paper,desk,archive,person,emotion};
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{shape,rect,paper,desk,archive,person,emotion}=env(q);
 // A coherent bureau: body behind the supported documents; service furniture is revealed later.
 shape('calendar',180,198,[rect(-65,-48,130,122,c.paper,6),rect(-65,-48,130,27,c.rose),text('2038',0,4,29,c.ink),text('October',0,40,23,c.ink)],'The book’s explicitly imagined October 2038 setting.');
 person('mara',320,520,1.04,c.jade,true);
 desk('workdesk',500,405,484);
 paper('contract',480,242,'Contract',{mark:false});
 paper('response',665,231,'Revision',{color:'#d1e5d8',mark:true});q.reveal('response',2);q.move('response',2,650,255,2000);
 shape('pencil',625,397,[path('M-37 1L27 -20',c.gold,9),path('M27 -20L39 -23',c.ink,4)],'The proposed wording is edited at the actual work desk.');
 archive('archive',944,340);q.reveal('archive',3);q.label('provider-label','Provider archive',944,145,32);q.reveal('provider-label',3);
 paper('saved-work',650,263,'Work history',{w:140,h:112,scale:.72,color:'#d5dfed'});q.reveal('saved-work',3);q.move('saved-work',3,935,227,3300);
 paper('new-terms',1110,326,'New terms',{w:154,h:108,color:'#f0c7b7'});q.reveal('new-terms',4);q.move('new-terms',4,735,365,3200);
 q.label('mara-label','Mara’s morning',320,567,31);
 storyGesture(q,'mara',1,'reflect');storyGesture(q,'mara',2,'explain');emotion('mara',2,'relieved');storyGesture(q,'mara',4,'question');emotion('mara',4,'worried');storyGesture(q,'mara',5,'reflect');
 scenes[0].visual=q.finish('Mara gains a stronger contract response at a real bureau, while useful work accumulates in a provider-controlled archive and changed terms return to her. The person and documents belong to the source’s prospective scenario.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{shape,rect}=env(q);
 // Rabbit habitat: changing a visible vector route, not merely changing a graph colour.
 shape('habitat',600,494,[n('path',{d:'M-490 0Q-340 -55 -160 -13Q28 -40 158 -7Q316 -51 493 -6L491 38H-489Z',fill:'#8aa986'}),...[-420,-330,-200,-40,160,320,440].flatMap(x=>[path(`M${x} 0q-18 -41 -29 -45M${x} 0q8 -48 23 -55`,c.jade,7)])],'A shared field habitat; greenery is food and ground, not a symbolic institutional plant.');
 const rabbit=(id,x,y,s=1,rest=false)=>q.add(q.object(id,x,y,[dot(-75,-25,21,'#d5c8b6'),n('ellipse',{cx:-20,cy:-40,rx:74,ry:48,fill:'#c1ad91'}),n('ellipse',{cx:43,cy:rest?-52:-81,rx:37,ry:35,fill:'#d8c7ad'}),n('ellipse',{cx:34,cy:rest?-106:-143,rx:13,ry:51,fill:'#d8c7ad'}),n('ellipse',{cx:60,cy:rest?-107:-147,rx:12,ry:49,fill:'#d8c7ad'}),path(rest?'M35 -111L29 -135M62 -113L66 -139':'M31 -164L37 -124M64 -174L58 -126','#b38d85',5),path('M-54 -3H-10M23 -7H65','#ddceba',15),dot(57,rest?-57:-87,4,c.ink),dot(78,rest?-43:-70,4,c.rose),path(rest?'M67 -37Q75 -32 80 -35':'M64 -57Q72 -52 77 -55',c.ink,2)],rest?'A less active sick host; non-graphic schematic, not a clinical image.':'A rabbit feeding in the field habitat.',s));
 rabbit('feeding-rabbit',330,477,1.05);rabbit('other-rabbit',888,473,.82);
 shape('food',413,470,[path('M0 0L30 -25M0 0L8 -36',c.jade,7),n('ellipse',{cx:19,cy:-27,rx:24,ry:11,fill:'#bed394'})],'The resistant host continues feeding.');
 q.label('episode','Australia · Myxoma',359,189,37);
 shape('field-note',923,255,[rect(-130,-61,260,131,c.paper,6),text('Field observation',0,-22,26,c.ink),path('M-94 7H93M-94 27H59M-94 47H82',c.ink,3)],'An observer’s notebook situates the book’s historical biological example.');
 q.label('resistance','Host resistance',326,263,31);q.reveal('resistance',2);q.move('feeding-rabbit',2,360,477,1800);
 rabbit('less-active-host',355,477,1.05,true);q.reveal('less-active-host',3);q.hide('feeding-rabbit',3);q.hide('resistance',3);
 const insect=(id,x,y)=>shape(id,x,y,[n('ellipse',{cx:-12,cy:-13,rx:21,ry:9,fill:'#bacbde'}),n('ellipse',{cx:13,cy:-15,rx:21,ry:9,fill:'#bacbde'}),n('ellipse',{cx:0,cy:1,rx:8,ry:16,fill:c.ink}),dot(0,-18,6,c.ink),path('M-4 0L-22 13M4 0L22 13M-3 8L-20 23M3 8L20 23M0 -22L7 -31',c.ink,3)],'A schematic insect vector carries infection between hosts; no species or numerical transmission rate is asserted.');
 insect('vector',380,361);q.reveal('vector',3);q.move('vector',4,915,358,4200);
 shape('vector-route',390,349,[path('M0 0Q260 -181 513 -3',c.rose,5),path('M494 -20L513 -3L490 1',c.rose,5)],'The changed transmission condition: a vector can carry infection even when the sick host is less mobile.');q.reveal('vector-route',4);
 q.label('vector-label','Vector transmission',620,260,34);q.reveal('vector-label',4);q.hide('field-note',4);
 q.label('cost-question','Who carries the cost?',636,551,34);q.reveal('cost-question',5);
 scenes[1].visual=q.finish('The book’s rabbit and myxoma episode: host resistance initially changes the interaction, then a moving insect carries infection from a less active host to another. This is a qualitative illustration of the cited mechanism, without invented populations, clinical pathology or anthropomorphic viral intent.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{shape,rect,paper,desk,archive,person,emotion}=env(q);
 archive('retained-archive',221,328);q.label('old-service','Original service',224,130,32);
 desk('replacement-desk',797,408,495);person('mara',806,526,.96,c.jade,true);
 // Foreground document surface supports the missing next step, distinct from the tall archive.
 paper('export',370,263,'Files',{color:c.paper,w:145,h:117});q.move('export',1,620,297,3300);
 shape('monitor',1014,313,[rect(-107,-79,214,133,c.blue,8),rect(-93,-65,186,104,c.paper,4),path('M0 55V83M-50 83H50',c.ink,10),text('Reply',0,-27,31,c.ink),text('Incomplete',0,12,24,c.ink)],'The alternative workstation has the records but cannot finish the same next negotiation step.');
 q.label('new-service','Alternative workspace',830,165,35);
 shape('memory-detail',228,451,[text('Context retained',0,24,26,'$ink')],'The original archive retains the learned operational context.');q.reveal('memory-detail',3);
 paper('due',1099,180,'Due today',{color:'#f1c5b8',w:164,h:100,scale:.85});q.reveal('due',4);q.move('due',4,991,417,2600);
 paper('notes',754,333,'Rebuild',{color:'#e6dcee',w:138,h:106,scale:.74});q.reveal('notes',4);
 q.label('files-arrived','Files arrived',610,562,30);q.reveal('files-arrived',2);
 storyGesture(q,'mara',1,'invite');emotion('mara',1,'happy');storyGesture(q,'mara',2,'question');emotion('mara',2,'worried');storyGesture(q,'mara',4,'reflect');emotion('mara',5,'determined');
 scenes[2].visual=q.finish('The same lawyer receives the exported files at an alternative desk. A real unfinished reply, retained operational context and arriving deadline show why possessing documents can differ from retaining the capability to continue work.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{shape,rect,paper,desk,archive,person,emotion}=env(q);
 // Collective review and apprenticeship are lived activities, not a parade of domain icons.
 shape('review-wall',363,254,[rect(-224,-76,448,154,'#d3e4dd',7),text('Shared case review',0,-32,34,c.ink),...[-140,-70,0,70,140].map((x,i)=>rect(x-24,-10,48,52,[c.paper,'#e8c5b7','#c6d7e9','#e4d6a4','#c3d8c4'][i],3)),path('M-140 49H140',c.jade,4)],'Several retained cases are compared together in a public or collective review setting.');
 person('reviewer',240,520,.76,c.blue);storyPerson(q,'learner',491,520,{identity:'person-09-neutral',coat:c.rose,scale:.8});
 desk('review-desk',365,420,380);paper('finding',360,320,'Finding',{w:142,h:98,scale:.85,color:'#d9e9d9'});q.reveal('finding',2);
 person('mara',857,518,.91,c.jade,true);desk('choice-desk',907,407,341);
 shape('permission-sheet',1065,289,[rect(-104,-68,208,152,c.paper,5),text('Permission',0,-28,29,c.ink),text('Recommend',-7,6,24,c.ink),text('Act',-50,43,24,c.ink),path('M58 2L68 12L84 -9',c.jade,4),rect(58,27,22,22,'none',3),path('M58 27H80V49H58Z',c.ink,2)],'Recommendation and execution are separately reviewed; action is not automatically authorized.');q.reveal('permission-sheet',4);
 paper('shared-finding',370,330,'Finding',{w:140,h:99,scale:.75,color:'#d9e9d9'});q.reveal('shared-finding',2);q.move('shared-finding',2,1067,323,4200);q.hide('shared-finding',4);
 q.label('practice','Reconstruct together',369,562,31);
 q.label('choice','Review before acting',914,562,31);q.reveal('choice',4);
 storyGesture(q,'reviewer',1,'explain');storyGesture(q,'learner',2,'question');storyGesture(q,'reviewer',4,'explain');storyGesture(q,'learner',4,'resolve');storyGesture(q,'mara',2,'reflect');storyGesture(q,'mara',4,'question');emotion('mara',4,'determined');storyGesture(q,'mara',6,'invite');emotion('mara',6,'relieved');
 scenes[3].visual=q.finish('A shared case review turns many retained observations into a usable finding; a learner actively reconstructs reasoning with a mentor. At the adjoining bureau Mara separately reviews recommendation and action permission. These are the book’s constructive proposals, not claims of deployed infrastructure.');
}
fs.writeFileSync(new URL('scenes.json',r),JSON.stringify(scenes,null,2)+'\n');
