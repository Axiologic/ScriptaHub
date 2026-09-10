import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const C={ink:'#293d52',copper:'#b77853',paper:'#f2ede4',desk:'#d6d0c6',teal:'#328f99',skin:'#d5aa8b',muted:'#879395',blue:'#55778c'};
const obj=(q,id,x,y,kids,meaning,k=1)=>q.add(q.object(id,x,y,kids,meaning,k));
const f=(q,d,fill)=>q.n('path',{d,fill});
const show=(q,id,b,off=0,d=600)=>q.actions.push({actor:id,action:'appear',beat:b,offsetMs:off,durationMs:d});
const hide=(q,id,b,off=0,d=450)=>q.actions.push({actor:id,action:'disappear',beat:b,offsetMs:off,durationMs:d});
const mv=(q,id,b,x,y,d=1400,off=250)=>q.actions.push({actor:id,action:'moveTo',beat:b,x,y,durationMs:d,offsetMs:off});
const mood=(q,id,b,emotion)=>q.actions.push({actor:id,action:'character.express',beat:b,emotion,durationMs:1000});
function label(q,id,lines,x,y,size=25){return obj(q,id,x,y,lines.map((s,i)=>q.text(s,0,i*(size+5),size,C.ink)),'Text belongs to this physical record, not a duplicate slide slogan')}
function paper(q,id,x,y,w,h){return obj(q,id,x,y,[f(q,`M${-w/2} ${-h/2}H${w/2}V${h/2}H${-w/2}Z`,C.paper)],'A supported sheet of paper')}
function manuscript(q,id,x,y,k=1){obj(q,id,x,y,[f(q,'M-145 -142H145V143H-145Z',C.paper),f(q,'M132 -72H154V-29H132Z',C.copper),q.text('Manuscript',0,-107,25,C.ink),q.path('M-106 -77H102M-106 -59H80M-106 36H105M-106 54H105M-106 72H70',C.muted,4),...[-65,0,65].map((x,i)=>({...q.n('circle',{cx:x,cy:-8-[0,13,5][i],r:9,fill:C.teal}),id:'$asset.data-'+i})),q.path('M-106 103H65',C.ink,5)],'The same schematic manuscript: constant data marks, body strokes and copper tab; no real experiment or units',k)}
function person(q,id,x,y,identity,coat,k=1,seated=false){storyPerson(q,id,x,y,{identity,coat,scale:k,seated,chair:C.blue,ink:C.ink});const o=q.objects.at(-1);return o}
function arm(o,side,d,x,y){const n=o.visual.children.find(n=>n.id==='$asset.arm'+side);n.children[0].attrs.d=d;n.children[1].attrs.cx=x;n.children[1].attrs.cy=y;}
function crop(o){for(const n of o.visual.children)if(['$asset.legL','$asset.legR'].includes(n.id))n.children=[]}
function table(q,id,x,y,w=800){obj(q,id,x,y,[f(q,`M${-w/2} -85H${w/2}V20H${-w/2}Z`,C.desk),q.path(`M${-w/2+38} 20V95M${w/2-38} 20V95`,C.ink,12)],'A broad physical desktop with supporting legs')}
function pen(q,id,x,y){obj(q,id,x,y,[q.path('M-31 -28L5 5',C.copper,7),f(q,'M2 2L11 11L8 0Z',C.ink)],'Pen nib reaches a marked point on the supported record')}
// The first composition is an overhead submission desk, then a human close view.
{
 const q=stageAuthor();obj(q,'overhead-desk',0,0,[f(q,'M145 229H1075V553H145Z',C.desk)],'Desk surface supports the manuscript and removable affiliation slip');
 // A human close view stays behind the working paper rather than replacing it.
 const r=person(q,'reviewer-close',851,562,'person-20-neutral',C.ink,1.08);crop(r);arm(r,'L','M-32 -156Q-104 -165 -132 -133',-132,-133);arm(r,'R','M32 -156Q56 -104 15 -87',15,-87);show(q,'reviewer-close',4,0);mood(q,'reviewer-close',4,'surprised');mood(q,'reviewer-close',5,'curious');
 manuscript(q,'manuscript',477,393,1.02);
 paper(q,'known-slip',477,300,249,52);label(q,'known-label',['Known laboratory'],477,308,24);
 obj(q,'withheld-slip',477,300,[f(q,'M-125 -26H125V26H-125Z','#e1e8e6'),q.text('Identity withheld',0,8,24,C.ink)],'Only this detachable cover slip is lifted; the manuscript does not change');
 obj(q,'slip-hand',609,307,[q.path('M301 39Q168 55 28 5',C.ink,42),q.path('M29 5L7 0',C.skin,23),q.n('ellipse',{cx:-4,cy:0,rx:16,ry:11,fill:C.skin}),q.path('M-12 -4H3M-13 1H2',C.ink,1.5)],'An overhead forearm enters from the desk edge; fingers grip the actual slip edge');show(q,'slip-hand',3,0,300);
 mv(q,'withheld-slip',3,682,262,1500,450);mv(q,'slip-hand',3,814,269,1500,450);hide(q,'slip-hand',3,2400);hide(q,'withheld-slip',3,2400);
 obj(q,'lens',659,374,[q.n('circle',{cx:0,cy:0,r:30,fill:'none',stroke:C.teal,'stroke-width':7}),q.path('M23 23L47 46',C.ink,12)],'Inspection lens with handle at the reviewer’s left palm, never an approval seal');show(q,'lens',4,0);mv(q,'reviewer-close',4,800,561,1800,1500);mv(q,'lens',4,608,373,1800,1500);
 scenes[0].visual=q.finish('Same manuscript and turquoise marks stay fixed through the affiliation cover reveal; a human reviewer then leans toward the work without deciding its truth.');
}
// Lateral collaboration: one source insert, one manuscript, an explicitly pending note.
{
 const q=stageAuthor();
 const e=person(q,'elena',340,548,'person-11-neutral',C.copper,.98,true);arm(e,'R','M32 -156Q97 -146 128 -92',128,-92);arm(e,'L','M-32 -156Q-69 -124 -60 -84',-60,-84);
 const r=person(q,'reviewer',888,548,'person-20-neutral',C.ink,.98,true);arm(r,'L','M-32 -156Q-78 -113 -106 -91',-106,-91);arm(r,'R','M32 -156Q71 -119 54 -81',54,-81);
 table(q,'review-table',610,473,852);
 manuscript(q,'manuscript',494,429,.57);
 paper(q,'supporting-record',706,428,197,139);obj(q,'source-marks',705,436,[-54,0,54].map((x,i)=>q.n('circle',{cx:x,cy:-[0,13,5][i],r:8,fill:C.teal})),'Supporting record preserves schematic observations without units');label(q,'source-label',['Supporting','record'],706,391,22);
 for(const id of ['supporting-record','source-marks','source-label'])show(q,id,4,300);
 paper(q,'side-slip',314,473,159,47);label(q,'side-affiliation',['Known lab'],314,480,21);
 // Joined sleeve from reviewer shoulder to the source record; original arm disappears only during this inspection.
 obj(q,'tracing-arm',888,548,[q.path('M-32 -156Q-95 -159 -143 -119',C.ink,20),q.n('ellipse',{cx:-152,cy:-112,rx:12,ry:9,fill:C.skin}),q.path('M-161 -109L-183 -105',C.skin,9)],'Reviewer’s connected bent forearm and index finger end on the supporting record');show(q,'tracing-arm',4,300);hide(q,'reviewer.armL',4,300);
 obj(q,'record-pointer',625,451,[q.path('M25 -4Q-12 29 -100 0',C.teal,3)],'A thin source pointer joins the measured record to the manuscript statement, never to the author');show(q,'record-pointer',5,200);
 paper(q,'review-note',923,471,109,74);label(q,'note-heading',['Review'],923,456,19);obj(q,'review-question',923,486,[q.text('?',0,0,32,C.ink)],'Unresolved review question, no pass/fail stamp');show(q,'review-question',6,1200);
 pen(q,'review-pen',941,471);show(q,'review-pen',6,0);mv(q,'review-pen',6,932,477,900,300);
 mood(q,'elena',1,'curious');mood(q,'reviewer',3,'curious');mood(q,'reviewer',4,'determined');mood(q,'elena',6,'curious');
 scenes[1].visual=q.finish('Two people inspect an actual paper and supporting record, retaining affiliation at the edge; one relationship is inspected and a question remains pending.');
}
// Large selective annotation, then the paid/unpaid labor question enters the same desk.
{
 const q=stageAuthor();const r=person(q,'working-reviewer',928,552,'person-20-neutral',C.ink,1.04,true);arm(r,'L','M-32 -156Q-84 -132 -99 -83',-99,-83);arm(r,'R','M32 -156Q72 -95 37 -74',37,-74);show(q,'working-reviewer',3);
 obj(q,'annotation-desk',0,0,[f(q,'M139 214H1075V552H139Z',C.desk)],'Close-up working desk, gradually including verification labor');
 manuscript(q,'manuscript',401,390,1.06);label(q,'measurement-label',['Measurement'],401,348,23);label(q,'interpretation-label',['Interpretation'],401,473,23);
 obj(q,'annotation-bracket',540,461,[q.path('M0 -21H13V24H0',C.copper,5)],'The bracket encloses only interpretation, leaving measurement unchanged');show(q,'annotation-bracket',2,1400);
 label(q,'pending-interpretation',['Needs','review'],618,444,26);show(q,'pending-interpretation',2,2100);
 obj(q,'annotation-hand',564,432,[q.path('M278 -194Q95 -166 9 -6',C.ink,37),q.n('ellipse',{cx:0,cy:0,rx:14,ry:11,fill:C.skin}),q.path('M-7 -4L11 -1',C.skin,8),q.path('M-20 -29L-9 8',C.copper,7),f(q,'M-12 6L-7 17L-6 4Z',C.ink)],'Overhead cropped sleeve connects to a hand holding the annotating pen at the interpretation margin');show(q,'annotation-hand',2,0);mv(q,'annotation-hand',2,564,464,1200,400);hide(q,'annotation-hand',3);
 paper(q,'timesheet',839,424,277,209);label(q,'timesheet-heading',['Work record'],839,343,26);label(q,'labor-entry',['Verification'],822,391,26);label(q,'budget-label',['Time allocation'],839,449,23);obj(q,'empty-allocation',839,481,[q.path('M-99 0H99',C.muted,3)],'The time allocation field is visibly blank; funding has not been solved');
 for(const id of ['timesheet','timesheet-heading','labor-entry','budget-label','empty-allocation'])show(q,id,4,id==='labor-entry'?1300:0);
 obj(q,'clock',955,254,[q.n('circle',{cx:0,cy:0,r:37,fill:C.paper}),q.path('M0 0V-22M0 0H17',C.ink,4)],'A physical desk clock measures the work required, with no invented cost');show(q,'clock',4);obj(q,'clock-later',955,254,[q.n('circle',{cx:0,cy:0,r:37,fill:C.paper}),q.path('M0 0L13 -18M0 0H17',C.ink,4)],'Clock advances modestly while verification is recorded');show(q,'clock-later',4,2800);
 mood(q,'working-reviewer',3,'determined');mood(q,'working-reviewer',5,'worried');
 // Reviewer sits behind the desk but above the paperwork, not as an extra floating portrait.
 {const i=q.objects.findIndex(o=>o.id==='working-reviewer'),o=q.objects.splice(i,1)[0];q.objects.splice(1,0,o)}
 scenes[2].visual=q.finish('A precise marginal question retains the three data marks; the scene expands to a human reviewer and an unresolved allocation of time, not a completed reform.');
}
// Oblique tabletop reader, pending machine connection and concrete chapter route.
{
 const q=stageAuthor();const r=person(q,'reader',420,551,'person-03-neutral',C.blue,1.14,true);arm(r,'R','M32 -156Q97 -119 140 -97',140,-97);arm(r,'L','M-32 -156Q-43 -86 36 -53',36,-53);
 obj(q,'reading-table',0,0,[f(q,'M416 333L1091 301L1111 528L359 550Z',C.desk),q.path('M400 548V574M1059 531V574',C.ink,12)],'Oblique reading table supports a real open book, facsimile and peripheral screen');
 obj(q,'open-book',626,446,[f(q,'M-147 -79Q-70 -102 0 -72Q72 -103 150 -83L163 61Q80 50 0 75Q-65 50 -164 68Z',C.paper),q.path('M0 -72V73',C.copper,4)],'The actual book, supported on a tabletop rather than standing for an institution');
 manuscript(q,'facsimile',950,432,.53);
 obj(q,'screen',915,273,[f(q,'M-132 -61H132V54H-132Z',C.ink),f(q,'M-120 -51H120V42H-120Z','#d5e5e5'),q.path('M-68 -21H-28M28 10H72M-24 -21Q2 -22 23 10',C.teal,4),q.text('Check mapping',0,32,20,C.ink),q.path('M0 54V64M-56 65H56',C.ink,8)],'A small peripheral screen proposes a source-reference connection that the reader must check');hide(q,'screen',3);
 obj(q,'source-passage',694,430,[q.path('M-46 -30H45M-46 -13H45M-46 4H24',C.muted,4)],'Book passage remains available for checking the proposed extraction');hide(q,'source-passage',3);
 label(q,'opening-section',['The Paper','From Nowhere'],552,409,23);hide(q,'opening-section',4);
 label(q,'later-section',['Paying for','correction'],702,412,23);show(q,'later-section',4,1000);
 obj(q,'pencil-bookmark',580,444,[q.path('M-20 29L25 -24',C.copper,7),f(q,'M23 -25L32 -33L29 -20Z',C.ink)],'Pencil held by the reader reaches the book margin, then bookmarks the recommended later chapter');
 // Purposeful hand transition: initial arm is removed; a bent return pose maintains one hand.
 hide(q,'reader.armR',4);hide(q,'pencil-bookmark',4);
 obj(q,'chapter-hand',420,551,[q.path('M37 -179Q146 -185 180 -102',C.blue,23),q.n('ellipse',{cx:180,cy:-102,rx:13,ry:10,fill:C.skin}),q.path('M174 -106L195 -82',C.copper,7)],'The connected forearm carries the pencil beside the first section');show(q,'chapter-hand',4);hide(q,'chapter-hand',4,1050);
 obj(q,'chapter-hand-later',420,551,[q.path('M37 -179Q172 -157 240 -80',C.blue,23),q.n('ellipse',{cx:240,cy:-80,rx:13,ry:10,fill:C.skin}),q.path('M235 -84L243 -57',C.copper,7)],'A second bent pose keeps the same shoulder while the hand reaches the later page');show(q,'chapter-hand-later',4,1000);hide(q,'chapter-hand-later',4,2200);
 obj(q,'later-pencil',693,472,[q.path('M-30 22L25 -24',C.copper,7),f(q,'M23 -25L32 -30L28 -20Z',C.ink)],'Pencil now rests on the page, marking the concrete reading route');show(q,'later-pencil',4,2200);
 obj(q,'resting-arm',420,551,[structuredClone(r.visual.children.find(n=>n.id==='$asset.armR'))],'The reader’s resting forearm returns to the edge of the supported book',1.14);show(q,'resting-arm',5);
 {const i=q.objects.findIndex(o=>o.id==='resting-arm'),o=q.objects.splice(i,1)[0];q.objects.splice(q.objects.findIndex(o=>o.id==='open-book'),0,o)}
 mood(q,'reader',1,'curious');mood(q,'reader',2,'skeptical');mood(q,'reader',3,'curious');mood(q,'reader',5,'curious');
 scenes[3].visual=q.finish('An ordinary reader checks an automated connection against the text, then follows two real book sections; the unchanged manuscript remains alongside as the concrete reason to read.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');console.log('Borrowed Credibility original four-scene material art authored.');
