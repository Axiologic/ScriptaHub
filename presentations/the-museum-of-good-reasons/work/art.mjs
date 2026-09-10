import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const C={ink:'#343044',aubergine:'#765074',brass:'#be923d',cream:'#eee8d9',ivory:'#faf4e7',stone:'#c7c7bd',teal:'#367d7f',green:'#529d77',red:'#bd6250',blue:'#527e98',skin:'#d8aa8b',wood:'#a6774e',rain:'#a0bec8'};
const obj=(q,id,x,y,kids,meaning,k=1)=>q.add(q.object(id,x,y,kids,meaning,k));
const fill=(q,d,c)=>q.n('path',{d,fill:c});
const show=(q,id,b,off=0,d=750)=>q.actions.push({actor:id,action:'appear',beat:b,offsetMs:off,durationMs:d});
const hide=(q,id,b,off=0)=>q.actions.push({actor:id,action:'disappear',beat:b,offsetMs:off,durationMs:600});
const mv=(q,id,b,x,y,d=1800,off=250)=>q.actions.push({actor:id,action:'moveTo',beat:b,x,y,durationMs:d,offsetMs:off});
const walk=(q,id,b,x,y,d=1800,off=250)=>{const previous=q._walkPositions?.[id]||q.objects.find(o=>o.id===id);q.actions.push({actor:id,action:'walkTo',beat:b,x,durationMs:d,offsetMs:off});if(y!==previous.y){const count=Math.max(2,Math.min(10,Math.round(d/420)))*2;for(let i=1;i<=count;i++)q.actions.push({actor:id,action:'moveTo',beat:b,y:previous.y+(y-previous.y)*i/count-(i<count&&i%2?4:0),durationMs:d/count,offsetMs:off+(i-1)*d/count});}q._walkPositions??={};q._walkPositions[id]={x,y};};
const mood=(q,id,b,emotion,gesture)=>{if(emotion==='reflective')emotion='curious';q.actions.push({actor:id,action:'character.express',beat:b,emotion,durationMs:1000});if(gesture)storyGesture(q,id,b,gesture,1800)};
function person(q,id,x,y,identity,coat,scale=.82,seated=false){storyPerson(q,id,x,y,{identity,coat,scale,seated,chair:C.teal,ink:C.ink});const o=q.objects.at(-1);const lower=n=>{for(const k of ['fill','stroke'])if(n.attrs?.[k]&&n.attrs[k]!=='none')n.themeAttrs={...n.themeAttrs,night:{...n.themeAttrs?.night,[k]:C.ink}};for(const c of n.children||[])lower(c)};for(const n of o.visual.children)if(n.id==='$asset.legL'||n.id==='$asset.legR')lower(n);return o}
function arm(o,side,d,x,y){let n=o.visual.children.find(n=>n.id==='$asset.arm'+side);n.children[0].attrs.d=d;n.children[1].attrs.cx=x;n.children[1].attrs.cy=y;}
function label(q,id,lines,x,y,size=29,color=C.ink){obj(q,id,x,y,lines.map((s,i)=>q.text(s,0,i*(size+6),size,color)),'Readable text attached to the physical evidence or book page')}
function ground(q,d,color=C.cream){obj(q,'physical-floor',0,0,[fill(q,d,color)],'Physical surface supporting actors and props; not a decorative background')}
function lamp(q,id,x,y,k=1){obj(q,id,x,y,[fill(q,'M-26 -5Q-24 17 0 18Q24 17 26 -5L19 -15H-18Z',C.brass),q.path('M-16 -17Q0 -21 17 -16',C.ink,3),q.path('M24 -8Q47 -23 35 -30Q27 -34 22 -23',C.brass,7),q.path('M0 -17V-28',C.ink,4),fill(q,'M0 -26Q-15 -40 2 -62Q5 -44 10 -40Q14 -29 0 -26Z','#e8b449')],'Cup-size brass oil lamp with wick and flame; not an electric lampshade',k)}
function page(q,id,x,y,w,h,meaning){obj(q,id,x,y,[fill(q,`M${-w/2} ${-h/2}H${w/2}V${h/2}H${-w/2}Z`,C.ivory)],meaning)}
// 1: lamp and label, with an explanatory opening through its marble pedestal.
{
const q=stageAuthor();ground(q,'M176 503Q590 469 1007 503V551H176Z');
const mara=person(q,'mara',444,535,'person-11-neutral',C.aubergine,.83);arm(mara,'R','M32 -156Q89 -141 135 -141',135,-141);
const orven=person(q,'orven',845,535,'person-20-neutral','#45414c',.86);arm(orven,'L','M-32 -156Q-95 -177 -122 -187',-122,-187);
obj(q,'pedestal',650,450,[fill(q,'M-112 -75H112V83H-112Z',C.stone),fill(q,'M-123 -87H123V-70H-123Z','#deddd2'),q.path('M-97 83V-71', '#b0b2ad',3)],'Marble pedestal physically supports a small brass lamp');
lamp(q,'brass-lamp',650,349,.8);
page(q,'label-card',650,407,205,62,'Physical museum exhibit label');label(q,'lamp-label',['Self-sufficient lamp'],650,414,24);
obj(q,'label-pencil',561,418,[q.path('M-12 -18L17 11',C.red,5),fill(q,'M14 8L21 15L17 4Z',C.ink)],'Mara’s pencil reaches the lower left corner of the label');
obj(q,'cutaway',650,484,[fill(q,'M-87 -37H87V46H-87Z','#e7dfcd'),fill(q,'M-28 10H29V37Q0 44 -28 36Z',C.brass),q.path('M0 -120V10',C.ink,7),q.path('M0 -119V10',C.brass,3),q.path('M-87 -37H87M-87 46H87',C.stone,4)],'Explanatory cutaway exposes the already concealed pipe and oil reservoir; this is not the later gallery reform');show(q,'cutaway',4);
for(let i=0;i<2;i++){obj(q,'oil-drop-'+i,650,489-i*27,[q.dot(0,0,4,C.red)],'A visible explanatory trace of oil already sustaining the lamp');show(q,'oil-drop-'+i,4,900+i*500);mv(q,'oil-drop-'+i,4,650,366,2300,1200+i*500);hide(q,'oil-drop-'+i,5)}
label(q,'cutaway-note',['Cutaway'],759,496,19,C.ink);show(q,'cutaway-note',4);mood(q,'mara',1,'curious');mood(q,'mara',2,'curious');mood(q,'orven',3,'curious');mood(q,'mara',4,'surprised');mood(q,'orven',5,'curious','question');hide(q,'label-pencil',6);mood(q,'mara',6,'reflective','reflect');
for(const id of ['cutaway','oil-drop-0','oil-drop-1']){const i=q.objects.findIndex(o=>o.id===id),o=q.objects.splice(i,1)[0];q.objects.splice(q.objects.findIndex(o=>o.id==='label-card'),0,o)}
scenes[0].visual=q.finish('A source-correct small oil lamp with a physical label and explanatory pedestal cutaway makes framing observable; no late transparent-pipe installation is represented.');
}
// 2: the source’s floor-projected route; first accounts move, then Mara retraces.
{
const q=stageAuthor();ground(q,'M54 244L1148 206V550H54Z','#e6e8df');
obj(q,'streets',0,0,[q.path('M330 435H1090M440 291V532M880 242V533','#c2cbc3',34),q.path('M650 264V533','#c2cbc3',90)],'Three physical junctions in the museum’s projected street plan');
obj(q,'shared-route',0,0,[q.path('M350 435H650V286',C.green,7)],'One route initially called shared, then turning at a junction');show(q,'shared-route',2);
obj(q,'alternative-route',0,0,[q.path('M650 435H1043M880 435V510',C.blue,6)],'The unchosen alternative remains visibly available; a following path reduces separation');show(q,'alternative-route',3);
obj(q,'umbrella-plinth',169,497,[fill(q,'M-90 -20H90V22H-90Z',C.stone)],'Base supports a museum umbrella exhibit');
obj(q,'umbrella',169,376,[fill(q,'M-82 -4Q-70 -82 0 -85Q70 -82 82 -4Q50 -25 30 -2Q0 -24 -30 -2Q-52 -23 -82 -4Z',C.teal),q.path('M0 -84V88Q-1 115 -27 99',C.wood,7),q.path('M0 -80Q-30 -46 -30 -2M0 -80Q34 -47 30 -2',C.ink,2),q.path('M-32 -47L-39 -24M32 -46L43 -19',C.brass,3)],'Green wooden-handled umbrella with two broken ribs, preserved as a material object');
for(let i=0;i<6;i++){obj(q,'drip-'+i,116+i*21,360+i%2*7,[q.path('M0 0L-3 16',C.rain,3)],'Water on the source’s wet umbrella; not decorative whole-stage rain');mv(q,'drip-'+i,2,114+i*21,458,2200,300+i*120)}
page(q,'pavel-account',112,257,115,57,'First written account');page(q,'mirena-account',239,257,115,57,'Second written account');label(q,'account-names',['Pavel'],112,263,24);label(q,'account-name-m',['Mirena'],239,263,24);for(const id of ['pavel-account','mirena-account','account-names','account-name-m'])show(q,id,2);
const pavel=person(q,'pavel',493,435,'person-08-neutral',C.blue,.62);const mirena=person(q,'mirena',575,435,'person-04-neutral',C.red,.62);show(q,'pavel',2);show(q,'mirena',2);mood(q,'pavel',2,'curious');mood(q,'mirena',2,'curious');
walk(q,'mirena',3,650,435,800,250);walk(q,'mirena',3,690,286,1500,1100);walk(q,'pavel',3,650,435,1600,1400);walk(q,'pavel',3,610,343,1000,3100);mood(q,'mirena',3,'worried');mood(q,'pavel',3,'curious');hide(q,'pavel',4);hide(q,'mirena',4);
const mara=person(q,'mara',440,435,'person-11-neutral',C.aubergine,.64);show(q,'mara',4,800);walk(q,'mara',4,650,435,1450,1300);walk(q,'mara',4,650,300,1300,2800);mood(q,'mara',4,'curious');mood(q,'mara',5,'reflective','question');
scenes[1].visual=q.finish('An oblique museum floor projection reconstructs the contrasting accounts at three junctions; Mirena’s distance briefly widens before Pavel follows, and Mara physically retraces the disputed turn.');
}
// 3: a file reenactment; workers carry the bench while the widower’s original place remains.
{
const q=stageAuthor();ground(q,'M56 453Q400 415 678 452Q947 417 1150 457V551H56Z','#e3ead5');
obj(q,'shade-tree',985,490,[q.path('M0 0L-12 -232M-9 -154L-76 -204M-7 -167L56 -217',C.wood,13),fill(q,'M-156 -202Q-190 -276 -93 -296Q-38 -344 29 -299Q116 -319 147 -250Q165 -189 76 -174L-92 -172Z','#81ad87')],'A real shade tree belongs to the bench’s new position');
obj(q,'new-shade',897,490,[fill(q,'M-130 -15Q5 -54 172 -11L148 52H-141Z','#c2d5b9')],'Quiet patch of shade physically surrounds the new bench position');
obj(q,'old-foot-marks',465,530,[q.path('M-109 0H-89M89 0H109',C.wood,5)],'Original bench feet leave a visible location without inventing a death scene');
const workerL=person(q,'worker-left',320,540,'person-02-neutral',C.teal,.8),workerR=person(q,'worker-right',612,540,'person-14-neutral',C.brass,.8);arm(workerL,'L','M-32 -156Q-60 -113 -46 -94',-46,-94);arm(workerR,'R','M32 -156Q58 -120 42 -98',42,-98);
for(const [o,side]of [[workerL,'R'],[workerR,'L']])o.visual.children.find(n=>n.id==='$asset.arm'+side).children=[];
obj(q,'bench',465,450,[q.path('M-114 -34V79M114 -34V79',C.ink,10),fill(q,'M-132 -47H132V-22H-132Z',C.wood),fill(q,'M-137 -5H137V12H-137Z',C.wood),q.path('M-118 15H118',C.ink,5)],'Park bench physically lifted and carried seven metres in an illustrative file reenactment');
for(const [id,x,coat,left]of [['carry-left',340,C.teal,true],['carry-right',590,C.brass,false]])obj(q,id,x,440,[q.path(left?'M2 -31Q-14 -13 0 0':'M4 -31Q18 -13 0 0',coat,17),q.dot(0,0,7,C.skin)],'Connected worker sleeve and palm grasp the bench near its seat');
for(const [id,x,y]of [['bench',465,450],['carry-left',340,440],['carry-right',590,440]]){mv(q,id,1,x,y-14,650,250);mv(q,id,1,x+252,y-14,1700,950);mv(q,id,1,x+252,y,600,2750)}
walk(q,'worker-left',1,572,540,1700,950);walk(q,'worker-right',1,864,540,1700,950);for(const id of ['worker-left','worker-right','carry-left','carry-right'])hide(q,id,2,300);
obj(q,'statue-base',465,505,[fill(q,'M-69 -54H69V22H-69Z',C.stone),fill(q,'M-83 -66H83V-52H-83Z','#d4d4ca')],'The source says the bench was moved to make room for a statue; only its cropped plinth is shown');show(q,'statue-base',2,800);
obj(q,'distance',700,210,[q.path('M-125 0H127M-125 -9V9M127 -9V9',C.ink,3),q.text('7 metres',0,-16,28,C.ink)],'Source distance annotation; this drawing is not a scaled engineering diagram');for(const n of q.objects.find(o=>o.id==='distance').visual.children)n.themeAttrs={night:n.type==='text'?{fill:C.cream}:{stroke:C.cream}};show(q,'distance',1,3200);
const widower=person(q,'widower',218,540,'person-20-neutral',C.blue,.85);arm(widower,'R','M32 -156Q73 -118 62 -93',62,-93);page(q,'complaint',267,452,66,68,'Widower’s complaint remains near the original place');
page(q,'official-reply',435,260,268,94,'The factually correct reply in the museum file');label(q,'reply-fields',['Better shade','Same seating'],435,249,27);for(const id of ['official-reply','reply-fields'])show(q,id,2);mood(q,'widower',3,'sad','reflect');
const parkIds=q.objects.map(o=>o.id);for(const id of parkIds)if(!['worker-left','worker-right','carry-left','carry-right'].includes(id))hide(q,id,4);
ground(q,'M288 485Q560 469 913 485V551H288Z',C.cream);q.objects.at(-1).id='reading-floor';show(q,'reading-floor',4,800);
const mara=person(q,'mara-file',509,537,'person-11-neutral',C.aubergine,.93);arm(mara,'R','M32 -156Q86 -116 107 -100',107,-100);show(q,'mara-file',4,850);
page(q,'file-open',684,439,223,160,'Mara reads the bench file without inventing a visit to the park');label(q,'file-facts',['Better shade','Same seating'],684,412,26);label(q,'letter-tab',['Complaint'],682,485,25);for(const id of ['file-open','file-facts','letter-tab'])show(q,id,4,850);obj(q,'paused-pencil',609,444,[q.path('M-6 -12L15 8',C.red,5)],'Mara’s supported hand pauses a pencil against the file');show(q,'paused-pencil',4,850);mood(q,'mara-file',4,'reflective');hide(q,'paused-pencil',5);mood(q,'mara-file',5,'reflective');
scenes[2].visual=q.finish('Conceptual enactment of the first-chapter bench complaint: supported workers move the bench into better shade, the original location still matters, then Mara returns to the file rather than visiting an invented park scene.');
}
// 4: reader, supported volume, the prologue’s two legitimate routes, ordinary opening selected.
{
const q=stageAuthor();
obj(q,'reading-chair',600,444,[fill(q,'M-124 -113Q0 -171 124 -113L139 82H-139Z',C.teal),fill(q,'M-151 67Q0 40 151 67V101H-151Z','#427b75')],'An upholstered chair supports the cropped reading pose');
const reader=person(q,'reader',600,570,'person-03-neutral',C.aubergine,1.3);for(const n of reader.visual.children)if(['$asset.legL','$asset.legR'].includes(n.id))n.children=[];arm(reader,'L','M-32 -156Q-104 -112 -120 -45',-120,-45);arm(reader,'R','M32 -156Q104 -112 120 -45',120,-45);
obj(q,'open-volume',600,454,[fill(q,'M-166 -67Q-84 -84 0 -57Q84 -84 166 -67V77Q80 59 0 84Q-85 59 -166 77Z',C.ivory),q.path('M0 -58V81',C.brass,4)],'Open volume rests on the reader’s lap, supported by connected arms and both hands');
for(const [id,x]of [['left-support',446],['right-support',754]])obj(q,id,x,512,[q.n('ellipse',{cx:0,cy:0,rx:12,ry:8,fill:C.skin}),q.path('M-5 -3L6 -2M-5 1L5 2',C.ink,1.5)],'Palm and fingers contact the book’s lower page corner while the forearm meets the lap');
label(q,'later-left',['Gifts'],518,424,29);label(q,'later-right',['Machines that','create time'],685,420,22);for(const id of ['later-left','later-right'])hide(q,id,3);mood(q,'reader',1,'curious');mood(q,'reader',2,'reflective');
label(q,'two-entrances',['Two Entrances'],600,415,25);label(q,'ordinary-route',['The Lamp’s','Label'],516,462,23);label(q,'alternate-route',['Whale Within','Whale'],684,462,23);for(const id of ['two-entrances','ordinary-route','alternate-route']){show(q,id,3);hide(q,id,4)}
// Three supported page-fold positions retain the gutter; this is a simplified page turn, not a free-floating card.
obj(q,'turning-page',600,454,[fill(q,'M0 -57Q82 -96 142 -70L131 73Q60 49 0 82Z','#e4d9c2')],'Right leaf lifts around the fixed book gutter');show(q,'turning-page',4);hide(q,'turning-page',4,700);
obj(q,'page-fold',600,454,[fill(q,'M0 -57Q-42 -91 -44 -34L-39 79Q-12 66 0 82Z','#e4d9c2')],'The raised page passes the fixed gutter before settling left');show(q,'page-fold',4,650);hide(q,'page-fold',4,1750);
obj(q,'turning-hand',600,454,[q.path('M42 -87Q80 -27 66 8Q38 5 10 -2',C.aubergine,21),q.n('ellipse',{cx:8,cy:-2,rx:12,ry:8,fill:C.skin})],'The reader’s connected bent forearm brings a thumb to the turning leaf at the gutter');show(q,'turning-hand',4);hide(q,'turning-hand',4,2100);hide(q,'reader.armR',4);hide(q,'right-support',4);obj(q,'restored-arm',600,570,[structuredClone(reader.visual.children.find(n=>n.id==='$asset.armR'))],'The resting forearm returns after the turn',1.3);show(q,'restored-arm',5);obj(q,'restored-support',754,512,[q.n('ellipse',{cx:0,cy:0,rx:12,ry:8,fill:C.skin})],'The support hand settles on the page corner again');show(q,'restored-support',5);
label(q,'opening-title',['The Lamp’s','Label'],518,430,27);show(q,'opening-title',4,2250);lamp(q,'page-lamp',679,462,.76);show(q,'page-lamp',4,2250);mood(q,'reader',4,'curious');mood(q,'reader',5,'reflective');
{const i=q.objects.findIndex(o=>o.id==='restored-arm'),o=q.objects.splice(i,1)[0];q.objects.splice(q.objects.findIndex(o=>o.id==='open-volume'),0,o)}
scenes[3].visual=q.finish('A prospective reader holds the physical book, sees the two entrances the prologue explicitly allows, and selects The Lamp’s Label; no late plot, reform or clinical revelation is pictured.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');console.log('Four original Museum material scenes authored.');
