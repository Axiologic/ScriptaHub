import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const here=new URL('./',import.meta.url),scenes=JSON.parse(fs.readFileSync(new URL('scenes.json',here)));
const C={ink:'#33465b',blue:'#80a9c7',terra:'#d68d70',gold:'#dfb94f',paper:'#f5eedf',wood:'#ab8d70',lilac:'#aa94bd',mint:'#8cb7a4',red:'#b95f5c'};
function setup(q){const{n,path,text,dot}=q;const rect=(x,y,w,h,fill,rx=5)=>n('rect',{x,y,width:w,height:h,fill,rx});const put=(id,x,y,children,b=1,meaning=id)=>{q.add(q.object(id,x,y,children,meaning));q.reveal(id,b,1000);};const person=(id,x,y,{identity='person-02-neutral',coat=C.blue,scale=.82,b=1,seated=false}={})=>{storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.lilac});q.reveal(id,b);};const mood=(id,b,emotion)=>q.actions.push({actor:id,action:'character.express',emotion,beat:b,durationMs:1000});const delay=(id,action,ms)=>{q.actions.findLast(a=>a.actor===id&&a.action===action).offsetMs=ms;};const folio=(id,x,y,label,b=1,color=C.paper)=>put(id,x,y,[rect(-98,-49,196,99,color),path('M-47 -24H45M-47 -4H18',C.wood,3),text(label,0,34,23,C.ink)],b,'A work document, not a measurement or universal reputation score.');return{rect,put,person,mood,delay,folio};}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,delay}=setup(q);
 put('ancestry-board',598,366,[rect(-222,-162,444,318,C.paper),path('M0 66V14L-111 -49M0 14L115 -49',C.wood,8),dot(0,68,10,C.gold),text('Shared ancestor',0,123,27,C.ink),text('Humans',-111,-118,28,C.ink),text('Monkeys',111,-118,28,C.ink),dot(-111,-80,12,C.terra),path('M-111 -65V-31M-111 -55L-129 -44M-111 -55L-94 -44',C.terra,7),dot(115,-80,15,C.gold),dot(99,-82,7,C.gold),dot(131,-82,7,C.gold),path('M115 -64V-38Q145 -18 149 -42',C.gold,8)],1,'The opening source example requires a branching common ancestor, never a ladder from current monkeys to humans.');
 person('explainer',182,530,{identity:'person-04-neutral',coat:C.blue});person('interrupter',1019,530,{coat:C.terra});
 person('listener-left',312,530,{identity:'person-09-neutral',coat:C.gold,scale:.42});person('listener-right',882,530,{identity:'person-12-neutral',coat:C.mint,scale:.42});
 storyGesture(q,'explainer',1,'explain');storyGesture(q,'interrupter',2,'explain');mood('interrupter',2,'happy');mood('explainer',2,'worried');
 q.actions.push({actor:'listener-left',action:'lookAt',target:'interrupter',beat:2,durationMs:1200},{actor:'listener-right',action:'lookAt',target:'interrupter',beat:2,durationMs:1200});
 storyGesture(q,'explainer',3,'question');q.actions.push({actor:'listener-left',action:'lookAt',target:'ancestry-board',beat:3,durationMs:1500},{actor:'listener-right',action:'lookAt',target:'ancestry-board',beat:3,durationMs:1500});mood('interrupter',3,'curious');
 for(const id of ['ancestry-board','listener-left','listener-right'])q.hide(id,5);
 q.move('explainer',5,302,530,2200);q.move('interrupter',5,900,530,2200);
 person('member-a',510,530,{identity:'person-09-neutral',coat:C.gold,scale:.77,b:5});person('member-b',710,530,{identity:'person-12-neutral',coat:C.mint,scale:.77,b:5});
 put('meeting-token',850,383,[dot(0,0,22,C.gold),path('M0 -14V0L10 7',C.ink,3)],5,'A facilitator’s authority lasts for the meeting, not a permanent intellectual rank.');
 q.move('meeting-token',6,551,388,2400);storyGesture(q,'member-a',6,'question');storyGesture(q,'interrupter',6,'reflect');mood('explainer',6,'relieved');
 scenes[0].visual=q.finish('The book’s evolutionary-debate opening enacts attention rewarding a quick interruption rather than the branching explanation. Returning attention to the evidence leads into an equal-height voluntary circle; temporary facilitation passes away from the initially confident speaker. No dignity ranking or actual reported meeting.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,delay,folio}=setup(q);
 person('founder',177,534,{coat:C.terra});person('specialist',1035,529,{identity:'person-04-neutral',coat:C.blue,scale:.78});
 put('terminal',518,366,[rect(-180,-161,360,274,C.lilac),rect(-154,-140,308,158,C.paper),text('Candidate selection',0,-97,28,C.ink),path('M-118 -68H112M-118 -42H75',C.blue,4),rect(-165,129,330,22,C.wood),path('M-135 150V170M135 150V170',C.wood,12),rect(-100,65,200,28,C.wood)],1,'A specific recruiting system is the source’s hypothetical decision, not an actual deployed product or measured benchmark.');
 folio('application',476,384,'Application',2);q.move('application',2,518,407,1800);storyGesture(q,'founder',2,'explain');
 put('validation-drawer',516,454,[rect(-143,-39,286,78,C.paper),text('Validation population?',0,-2,24,C.ink),path('M-93 18H91',C.blue,4)],3,'The question is which population validated the predictions; no composition or discovered bias is fabricated.');q.move('validation-drawer',3,760,455,2300);storyGesture(q,'specialist',3,'question');
 q.hide('validation-drawer',4);q.hide('specialist',4);
 person('applicant',1002,531,{identity:'person-09-neutral',coat:C.gold,b:4,scale:.8});
 put('review-tray',806,453,[n('path',{d:'M-96 -14H96L112 35H-109Z',fill:C.mint}),text('Appeal?',0,18,27,C.ink)],4,'A question about where the rejected application can go, not an assurance an appeal exists.');
 put('returned-application',694,371,[rect(-56,-42,112,86,C.paper),path('M-39 -20H34M-39 1H12',C.blue,3),path('M-10 14L10 32M10 14L-10 32',C.red,4)],4,'The application has a questioned rejection; the mark is not a numerical result.');q.move('returned-application',4,806,414,2300);storyGesture(q,'applicant',4,'question');mood('applicant',4,'worried');
 for(const id of ['terminal','application','returned-application','review-tray'])q.hide(id,5);
 q.move('founder',5,162,535,1900);q.move('applicant',5,722,535,1900);
 put('small-terminal',379,417,[rect(-96,-98,192,145,C.lilac),rect(-76,-80,152,87,C.paper),text('AI route',0,-34,27,C.ink),path('M0 48V95M-60 95H60',C.wood,13)],5,'The automated option remains visible beside a separately questioned human route.');
 person('reviewer',1077,526,{identity:'person-04-neutral',coat:C.blue,scale:.65,b:5,seated:true});
 put('human-desk',990,476,[rect(-131,-30,261,24,C.wood),path('M-107 -6V57M107 -6V57',C.wood,10),text('Human route?',0,-48,27,'$ink')],5,'A non-automated route is a source question, not a promised institutional feature.');
 storyGesture(q,'applicant',5,'question');storyGesture(q,'reviewer',6,'reflect');storyGesture(q,'founder',6,'reflect');mood('applicant',6,'curious');
 scenes[1].visual=q.finish('The hypothetical recruiting case moves from an AI device to validation population, a rejected applicant’s missing appeal destination, and a possible human route. Different questions affect who may exercise authority. Nothing asserts a real population defect, implemented remedy or measured fairness outcome.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,delay,folio}=setup(q);
 person('originator',180,535,{coat:C.terra});person('contributor',1040,535,{identity:'person-09-neutral',coat:C.gold});
 put('workbench',607,504,[rect(-300,-29,600,23,C.wood),path('M-270 -6V33M270 -6V33',C.wood,12)],1,'A working editorial surface makes revision material rather than a badge of humility.');
 put('previous-edition',438,394,[rect(-83,-103,166,194,C.blue),rect(-68,-90,136,169,C.paper),text('Founding text',0,-52,25,C.ink),text('Edition 1',0,-14,27,C.ink),path('M-47 14H48M-47 36H30',C.blue,3)],1,'The previous edition remains available and legible beside the revised one.');
 put('annotation',439,414,[path('M-61 -28L-42 -44M-60 -28L-41 -10M-61 -28H-81',C.red,4),path('M22 19L59 19',C.red,4)],2,'A contributor can contest a founding assertion without losing their place.');
 put('revision',692,394,[rect(-84,-104,168,194,C.mint),rect(-69,-90,138,169,C.paper),text('Revised text',0,-52,25,C.ink),text('Edition 2',0,-14,27,C.ink),path('M-47 14H48M-47 36H30',C.mint,4)],2,'The change creates a new edition without silently rewriting the preserved past.');
 storyGesture(q,'contributor',2,'question');storyGesture(q,'originator',2,'reflect');mood('originator',2,'curious');
 for(const id of ['workbench','annotation'])q.hide(id,3);
 q.move('previous-edition',3,427,314,2100);q.move('revision',3,626,314,2100);
 q.move('contributor',3,955,535,2200);
 put('shelf',527,418,[rect(-220,-8,440,17,C.wood),path('M-198 9V40M198 9V40',C.wood,9)],3,'Both editions stay in shared memory when a contributor moves on.');
 put('private-envelope',564,492,[rect(-94,-34,188,66,C.lilac),path('M-94 -32L0 9L94 -32',C.ink,3),text('Private data',0,25,24,C.ink)],3,'Private information remains in the room and does not travel with the departing member.');
 put('work-evidence',787,416,[rect(-88,-64,176,128,C.paper),text('My contribution',0,-29,25,C.ink),text('Verified work',0,13,23,C.ink),path('M-44 34H45',C.mint,4)],3,'Only permitted evidence of the member’s own work travels, not private data or unrestricted shared property.');q.move('work-evidence',3,891,417,2500);q.move('contributor',3,1013,535,2500);delay('contributor','moveTo',1000);
 mood('contributor',3,'relieved');
 put('project-box',797,494,[rect(-72,-32,144,65,C.wood),path('M-72 -31L0 -12L72 -31',C.paper,3),text('Project closed',0,22,23,C.ink)],4,'A closed project can retain professional relationships without being sold as a success.');
 folio('recommendation',242,392,'Recommendation',4);q.move('recommendation',4,879,343,3200);storyGesture(q,'originator',4,'invite');
 storyGesture(q,'contributor',5,'invite');mood('originator',5,'relieved');
 scenes[2].visual=q.finish('Correction visibly preserves Edition 1 beside Edition 2. On departure a permitted contribution record and recommendation move toward the member; a labelled private envelope and both historical editions remain. A closed-project box makes the practical value of unstigmatized support visible, without promising clinical services or project success.');
}
{
 const q=stageAuthor(),{n,path,text,dot}=q,{rect,put,person,mood,delay}=setup(q);
 put('platform',599,467,[rect(-156,-17,312,85,C.lilac),path('M-183 49H-156M-202 69H-156',C.wood,10)],1,'Accumulated prestige can raise a founder beyond ordinary challenge; elevation means authority, not worth.');
 person('leader',601,449,{coat:C.terra,scale:.74});person('questioner',247,535,{identity:'person-09-neutral',coat:C.gold,scale:.76});person('reviewer',951,535,{identity:'person-04-neutral',coat:C.blue,scale:.76});
 put('lectern',600,401,[rect(-103,-31,206,19,C.wood),path('M-72 -12V45M72 -12V45',C.wood,10),text('Mandate expires',0,15,24,C.ink)],1,'A real endpoint to authority is written on the actual meeting lectern.');
 put('token',601,356,[dot(0,0,23,C.gold),path('M0 -14V0L11 7',C.ink,3)],1,'The temporary facilitation token can transfer to a different participant.');
 storyGesture(q,'questioner',1,'question');mood('questioner',1,'worried');storyGesture(q,'leader',1,'explain');
 q.move('platform',2,599,541,2600);q.hide('platform',2);delay('platform','disappear',2800);
 q.move('leader',2,602,532,2600);q.move('lectern',2,600,485,2600);q.move('token',2,904,412,2800);delay('token','moveTo',2800);
 storyGesture(q,'reviewer',2,'question');storyGesture(q,'leader',2,'reflect');
 q.hide('lectern',3);q.move('leader',3,566,535,1800);q.move('reviewer',3,821,535,1800);q.move('token',3,778,412,1800);mood('questioner',3,'relieved');storyGesture(q,'questioner',3,'explain');storyGesture(q,'leader',3,'reflect');
 for(const id of ['leader','reviewer','token'])q.hide(id,4);
 q.move('questioner',4,202,535,1700);
 put('reading-book',784,352,[n('path',{d:'M-253 -133Q-130 -153 0 -127Q131 -153 253 -133V145Q129 119 0 146Q-128 119 -253 145Z',fill:C.paper}),path('M0 -127V145',C.wood,4),text('A day in an',-129,-64,30,C.ink),text('Outfinitist circle',-129,-24,26,C.ink),text('Protections',129,-64,30,C.ink),text('against success',129,-24,27,C.ink),path('M-217 23H-40M-217 53H-68M39 23H217M39 53H177',C.blue,4)],4,'Two real source sections provide a concrete route into the larger book, not a recruitment demand.');
 put('book-rest',784,516,[rect(-271,-11,542,17,C.wood)],4,'A proportionate open volume rests on a surface, not a floating branded box.');storyGesture(q,'questioner',4,'invite');mood('questioner',5,'curious');
 scenes[3].visual=q.finish('Prestige makes questioning an elevated leader difficult. The conceptual proposed response actually lowers the platform, ends a mandate and moves facilitation to another person while the former leader keeps equal standing. Closing on the real circle and success-protections sections invites judging the proposal rather than joining it.');
}
fs.writeFileSync(new URL('scenes.json',here),JSON.stringify(scenes,null,2)+'\n');
