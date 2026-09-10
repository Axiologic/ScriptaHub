import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#27354f',indigo:'#667cac',saffron:'#dca34b',coral:'#ce796f',sage:'#7aa78a',paper:'#f4ead5',rose:'#eac7b7',violet:'#afa1c4',wood:'#b17c59'};
function setup(q){const {n,path,text,dot}=q;
 const rect=(x,y,width,height,fill,rx=0)=>n('rect',{x,y,width,height,fill,rx});
 const add=(id,x,y,children,meaning)=>q.add(q.object(id,x,y,children,meaning));
 const person=(id,x,y,{identity='person-04-neutral',coat=C.coral,scale=.95,seated=false}={})=>storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.violet});
 const expression=(id,beat,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat,durationMs:1100});
 const portrait=(id,x,y,w=90)=>add(id,x,y,[rect(-w/2,-w*.68,w,w*1.22,C.wood,5),rect(-w/2+8,-w*.68+8,w-16,w*1.22-16,'#ddd3bd'),dot(0,-w*.23,w*.17,'#ad866d'),n('path',{d:`M${-w*.29} ${w*.32}Q${-w*.24} 0 0 0Q${w*.25} 0 ${w*.29} ${w*.32}Z`,fill:C.indigo})],'An ordinary remembered ancestor portrait, not a sacred figure or identifiable historical person.');
 return {rect,add,person,expression,portrait};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,add,person,expression,portrait}=setup(q);
 // The family setting and meditative setting remain distinct; no universal ritual is invented.
 add('remembering-place',328,380,[rect(-116,-15,232,27,C.wood,6),path('M-95 12V115M95 12V115',C.wood,13)],'A domestic remembrance surface holds a portrait and offering.');
 portrait('ancestor',301,296,106);
 add('incense-bowl',397,356,[n('path',{d:'M-28 0H28Q23 30 0 28Q-25 29 -28 0Z',fill:C.saffron}),path('M-6 0L-13 -56M9 0L15 -49',C.wood,3),path('M-13 -60Q-25 -77 -15 -91Q-7 -105 -18 -117','#a6a3a1',3)],'Incense is one source-named practice of ancestor remembrance.');
 person('family-member',166,526,{coat:C.coral,scale:.98});person('family-member-two',530,522,{identity:'person-02-neutral',coat:C.indigo,scale:.83});q.reveal('family-member-two',2);
 add('offering',211,390,[n('ellipse',{cx:0,cy:10,rx:36,ry:9,fill:C.paper}),dot(-13,0,12,C.coral),dot(10,-1,14,C.saffron),dot(26,2,10,C.coral)],'A family member places a small offering at the remembered ancestor’s portrait.');q.move('offering',1,268,357,2800);
 storyGesture(q,'family-member',1,'invite');storyGesture(q,'family-member-two',2,'reflect');expression('family-member',2,'relieved');
 add('meditation-mat',930,502,[n('ellipse',{cx:0,cy:0,rx:136,ry:27,fill:C.sage})],'A floor mat belongs to the distinct seated meditation setting.');q.reveal('meditation-mat',3);
 person('monk',930,500,{identity:'person-07-neutral',coat:C.saffron,scale:.95});
 const monk=q.objects.find(o=>o.id==='monk');
 monk.visual.children=monk.visual.children.filter(x=>!['$asset.n19','$asset.n20','$asset.n21','$asset.n22','$asset.n23','$asset.n27','$asset.n28'].includes(x.id));
 const head=monk.visual.children.find(x=>x.id==='$asset.head');head.children=head.children.filter(x=>x.id!=='$asset.n4');
 monk.visual.children.push({...path('M-25 -168Q0 -124 34 -89','#b87932',5),id:'$asset.robe-fold'});
 for(const side of ['L','R']){const arm=monk.visual.children.find(x=>x.id==='$asset.arm'+side);arm.children=[{...path(side==='L'?'M-34 -157Q-58 -95 -2 -101':'M32 -156Q59 -102 7 -100',C.saffron,20),id:'$asset.arm'+side+'.resting'},{...dot(side==='L'?-2:7,-100,10,'#EFC7AE'),id:'$asset.arm'+side+'.hand'}];}

 for(const name of ['legL','legR']){const node=monk.visual.children.find(c=>c.id==='$asset.'+name);if(node)node.children=[{...path(name==='legL'?'M-18 -84Q-92 -18 -12 -17H39':'M19 -84Q92 -18 12 -17H-39',C.saffron,21),id:'$asset.'+name+'.folded'}];}
 q.reveal('monk',3);storyGesture(q,'monk',3,'reflect');expression('monk',3,'relieved');
 q.label('family-caption','Ancestor remembrance',319,573,31);q.label('practice-caption','Buddhist meditation',930,573,31);q.reveal('practice-caption',3);
 scenes[0].visual=q.finish('The source’s planetary composite is illustrated through distinct domestic ancestor remembrance and seated Buddhist meditation. Recognizable gestures and objects preserve different practices; the imagined observer is a comparative method, not a conscious oracle.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,add,person,expression}=setup(q);
 // Two environments, animated bodily coordination, then a change of scene rather than a row of labels.
 add('singing-floor',391,478,[n('ellipse',{cx:0,cy:0,rx:262,ry:39,fill:'#ded4c3'})],'A communal singing space gives participants a shared physical location.');
 const singers=[['singer-a',214,513,'person-02-neutral',C.indigo,.94],['singer-b',385,475,'person-09-neutral',C.saffron,.85],['singer-c',556,517,'person-04-neutral',C.coral,.94]];
 for(const [id,x,y,identity,coat,scale] of singers){person(id,x,y,{identity,coat,scale});storyGesture(q,id,1,id==='singer-b'?'explain':'reflect');expression(id,2,'happy');q.move(id,2,x+(x<385?58:x>385?-58:0),y,2200);storyGesture(q,id,2,'invite');}
 add('song-page',390,376,[rect(-51,-48,102,95,C.paper,4),path('M-31 -23H31M-31 -6H21M-31 11H31',C.ink,4)],'A held song page supports a communal chant; no invented sacred words or denominational rite.');
 q.label('chant-label','Sacred chant',381,566,34);
 add('festival-ground',896,482,[n('ellipse',{cx:0,cy:0,rx:212,ry:33,fill:'#a3b7a0'}),n('path',{d:'M-180 -2Q-157 -54 -148 -61L-138 -7M150 -4Q161 -44 178 -49L179 -2',fill:C.sage})],'A separate outdoor festival setting, with everyday clothing and shared singing.');q.reveal('festival-ground',3);
 for(const [id,x,y,identity,coat,scale] of [['festival-a',800,499,'person-08-neutral',C.violet,.8],['festival-b',970,509,'person-05-neutral',C.sage,.83]]){person(id,x,y,{identity,coat,scale});q.reveal(id,3);storyGesture(q,id,3,'invite');expression(id,3,'happy');q.move(id,4,x-18,y,1800);storyGesture(q,id,4,'explain');}
 add('guitar',1054,405,[n('ellipse',{cx:0,cy:0,rx:35,ry:46,fill:C.saffron}),n('ellipse',{cx:0,cy:-39,rx:27,ry:34,fill:C.saffron}),rect(-9,-135,18,107,C.wood,3),dot(0,-18,12,C.ink),path('M-3 -125V26M3 -125V26',C.paper,2)],'An ordinary musical instrument locates the secular refrain in a festival, without claiming music alone makes a religion.');q.reveal('guitar',3);
 q.label('festival-label','Festival refrain',928,566,34);q.reveal('festival-label',3);
 storyGesture(q,'singer-a',4,'explain');storyGesture(q,'singer-c',4,'invite');
 scenes[1].visual=q.finish('Participants visibly close their spacing and coordinate gestures in communal singing, followed by another group in an outdoor secular festival. Shared bodily mechanisms coexist with different stories and commitments; people remain distinct rather than becoming a literal collective consciousness.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,add,person,expression,portrait}=setup(q);
 // The same domestic threshold changes from practical support to interpersonal pressure.
 add('household-seat',305,429,[rect(-142,-63,284,118,C.violet,15),rect(-143,15,286,48,C.violet,12),path('M-125 64V98M126 64V98',C.wood,12)],'A household sofa grounds the source’s composite grief scene.');
 person('woman',283,527,{identity:'person-04-neutral',coat:C.indigo,scale:1.0,seated:true});q.objects.find(o=>o.id==='woman').visual.children.shift();expression('woman',1,'tired');storyGesture(q,'woman',1,'reflect');
 person('neighbor',571,521,{identity:'person-09-neutral',coat:C.sage,scale:1});
 add('meal',501,391,[n('ellipse',{cx:0,cy:0,rx:64,ry:13,fill:C.paper}),n('path',{d:'M-49 -2Q-41 -54 0 -55Q44 -53 49 -2Z',fill:C.saffron}),dot(0,-60,6,C.wood)],'A neighbor brings a covered meal, concrete care rather than an abstract support symbol.');q.move('meal',2,392,404,3200);storyGesture(q,'neighbor',2,'invite');expression('woman',2,'relieved');
 portrait('remembered-partner',180,215,80);
 add('ceremony',720,253,[rect(-97,-66,194,133,C.paper,5),text('Ceremony',0,-25,30,C.ink),path('M-65 6H65M-65 26H39M-65 46H56',C.ink,3)],'The community takes responsibility for ceremony arrangements.');q.reveal('ceremony',2);
 q.label('time-cue','Years later',599,163,33);q.reveal('time-cue',3);q.hide('meal',3);q.hide('ceremony',3);
 person('adult-daughter',836,526,{identity:'person-05-neutral',coat:C.coral,scale:1.02});q.reveal('adult-daughter',3);
 person('adult-partner',1036,526,{identity:'person-08-neutral',coat:C.saffron,scale:1.02});q.reveal('adult-partner',3);
 storyGesture(q,'neighbor',3,'resolve');expression('neighbor',3,'skeptical');storyGesture(q,'adult-daughter',3,'question');expression('adult-daughter',3,'worried');storyGesture(q,'adult-partner',3,'reflect');
 q.move('adult-daughter',4,787,526,2400);storyGesture(q,'woman',4,'question');expression('woman',4,'worried');storyGesture(q,'neighbor',5,'reflect');
 q.label('daughter-label','Adult daughter',821,576,31);q.reveal('daughter-label',3);
 scenes[2].visual=q.finish('A source-attributed composite: a grieving woman receives food and ceremony help. Years later her adult daughter stands between the same community and an adult partner, facing pressure about the relationship. No reason for its prohibition, partner identity category, or further outcome is invented.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,add,person,expression,portrait}=setup(q);
 // A private question exposes interpretive mediation; the closing shifts toward a real reading act.
 add('night-window',219,233,[rect(-99,-81,198,172,'#415275',9),dot(48,-35,23,'#efd9a2'),rect(-99,6,198,85,'#35425f')],'A quiet nighttime room for the source’s composite private question.');
 person('reader',438,521,{identity:'person-04-neutral',coat:C.indigo,scale:1.05,seated:true});storyGesture(q,'reader',1,'reflect');expression('reader',1,'tired');
 portrait('memory-portrait',161,437,75);
 add('phone',520,367,[rect(-35,-60,70,122,C.ink,9),rect(-28,-48,56,95,C.paper,4),dot(0,52,4,C.paper)],'A phone held close in a private conversation, not a sacred oracle.');
 add('question-display',881,311,[rect(-204,-127,408,256,C.indigo,16),rect(-191,-113,382,228,C.paper,9),text('Can the dead',0,-58,35,C.ink),text('hear us?',0,-16,35,C.ink),path('M-141 32H137M-141 52H111M-141 72H131',C.indigo,4)],'An enlarged view of the source-grounded question; the reply is represented as text texture, not an invented theological answer.');
 add('interpretation-source',865,406,[rect(-170,-50,340,113,'#d4e0d9',6),text('Interpretation',0,-13,31,C.ink),text('Source • Tradition',0,29,25,C.ink)],'The response’s interpretive origin is surfaced inside the device display. It does not claim neutral revelation.');q.reveal('interpretation-source',2);
 q.hide('question-display',4);q.hide('interpretation-source',4);
 add('opening-page',887,323,[n('path',{d:'M-199 -125Q-100 -153 0 -128Q102 -152 199 -126V134Q100 111 0 134Q-97 110 -199 134Z',fill:C.paper}),path('M0 -128V134',C.wood,3),text('Ten minutes',-102,-65,28,C.ink),text('before the gods',-102,-26,24,C.ink),...[-1,1].flatMap(sign=>[path(`M${sign<0?-169:28} 19H${sign<0?-26:169}M${sign<0?-169:28} 42H${sign<0?-41:149}M${sign<0?-169:28} 65H${sign<0?-26:169}`,C.ink,3)])],'An opening spread carrying the actual chapter title, rendered as a reading object rather than a second scene slogan.');q.reveal('opening-page',4);
 add('held-reading',498,379,[n('path',{d:'M-54 -30Q-25 -39 0 -31Q25 -39 54 -30V35Q25 25 0 35Q-25 25 -54 35Z',fill:C.paper}),path('M0 -30V35',C.wood,2)],'A small opening spread in the reader’s hands corresponds to the enlarged chapter view.');q.reveal('held-reading',4);q.hide('phone',4);storyGesture(q,'reader',4,'invite');expression('reader',4,'curious');storyGesture(q,'reader',5,'reflect');
 scenes[3].visual=q.finish('In the source’s nighttime composite, a private religious question reaches a chatbot. An enlarged device view reveals that fluent text has an interpretive origin. The scene then returns to an actual opening-chapter reading invitation, without a fabricated revelation or metaphysical verdict.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
