import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const palette={teal:'#258994',coral:'#cd725d',gold:'#d4a13c',violet:'#7964a7',paper:'#f1e4cf',wood:'#a87653',ink:'#304552'};
for(const [index,s]of scenes.entries()){
 const a=stageAuthor(),{n,path,text,tint,dot}=a,c=palette;
 const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
 const fill=(d,color,night=color)=>tint(n('path',{d,fill:color}),night);
 const rect=(x,y,w,h,color,night=color,r=0)=>tint(n('rect',{x,y,width:w,height:h,rx:r,fill:color}),night);
 const label=(v,x,y,size=28,col=c.ink)=>text(v,x,y,size,col);
 const action=(id,beat,action,rest={})=>a.actions.push({actor:id,action,beat,durationMs:1600,...rest});
 const look=(id,target,beat)=>action(id,beat,'lookAt',{target,durationMs:850});
 const expression=(id,emotion,beat)=>action(id,beat,'character.express',{emotion,durationMs:850});
 const gesture=(id,beat,g)=>storyGesture(a,id,beat,g,2400);
 const person=(id,x,y,coat,identity='person-02-neutral',scale=.8,seated=false)=>{storyPerson(a,id,x,y,{coat,identity,scale,seated,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;};
 const floor=(id,x,y,w,color=c.teal)=>obj(id,x,y,[fill(`M${-w/2} 0H${w/2}L${w/2-42} 25H${-w/2+22}Z`,color),fill(`M${-w/2+22} 25H${w/2-42}V38H${-w/2+22}Z`,c.wood,'#ba9275')],'A material support plane, not a decorative frame');
 const closed=(id,x,y,w,h,color,meaning)=>obj(id,x,y,[rect(-w/2,-h,w,h,color,color,5),rect(-w/2+7,-8,w-10,6,c.paper,'#dcd9c4',2),rect(-w/2,-h,10,h,color),path(`M${-w/2+16} ${-h+7}V-14`,c.paper,2),path(`M${-w*.12} ${-h*.65}H${w*.3}`,c.paper,3),rect(-w/2,-2,w,3,color),path(`M${-w/2+9} ${-h+14}V-16`,color,3)],meaning);
 const open=(id,x,y,w,h,color,words=[])=>obj(id,x,y,[fill(`M${-w/2-7} ${-h+7}Q-50 ${-h-10} 0 ${-h+16}Q50 ${-h-10} ${w/2+7} ${-h+7}V7Q55 -7 0 15Q-55 -7 ${-w/2-7} 7Z`,color),fill(`M${-w/2} ${-h}Q-54 ${-h-12} 0 ${-h+13}V4Q-55 -13 ${-w/2} 0Z`,c.paper,'#d4dfd5'),fill(`M0 ${-h+13}Q54 ${-h-12} ${w/2} ${-h}V0Q55 -13 0 4Z`,'#f7eddd','#e1e5d7'),path(`M0 ${-h+17}V0`,color,3),...[-.36,-.28,-.2].map(q=>path(`M${-w*.43} ${h*q}Q${-w*.22} ${h*q-8} ${-w*.05} ${h*q+2}`,color,2)),...words.map((v,j)=>label(v,w*.25,-h*.63+j*28,22,c.ink))],'A proportioned bound volume with curved pages and a visible spine');
 const clock=(id,x,y)=>{obj(id,x,y,[dot(0,0,38,c.gold),dot(0,0,31,c.paper),...[-1,1].map(k=>path(`M${k*25} 0H${k*29}`,c.ink,3)),path('M0 -29V-25M0 25V29',c.ink,3)],'Finite time remains scarce in the illustrated reading task');obj(id+'-hand',x,y,[path('M0 -21V0L16 7',c.ink,4)],'The clock advances while the available options increase');};
 if(index===0){
  // An inhabited model is an active encounter, not a static row of speculative icons.
  obj('workshop-support',595,432,[fill('M-230 0L95 -75L257 15L-63 92Z','#c4d8c8','#657f81'),fill('M-63 92L257 15V39L-63 117Z',c.teal,'#7dc2c5'),fill('M-230 0L-63 92V117L-230 25Z',c.wood),path('M-189 42V105M211 55V107',c.wood,14)],'A raised workshop model contains a route and people with their own activity');
  obj('model-walkway',577,433,[path('M-176 -4L-43 68L212 9','#f6dfab',24)],'The path carries an appointment between two inhabitants');
  obj('bench',699,417,[rect(-31,0,100,9,c.coral),path('M-18 9V42M52 9V42',c.ink,7),rect(-27,-36,93,11,c.coral),path('M-21 -30V0M52 -30V0',c.ink,5)],'An inhabitant waits at a meeting place');
  person('resident',687,469,c.coral,'person-03-neutral',.48);person('visitor',482,481,c.gold,'person-15-neutral',.48);
  person('aster',172,550,c.violet,'person-04-neutral',1.12);person('pupil',1004,542,c.teal,'person-15-neutral',.81);
  obj('aster-console',289,425,[fill('M-67 -76L40 -104L77 -30L-32 -4Z',c.teal),path('M-12 -3V93M-55 94H33',c.wood,11),path('M-39 -65L-2 -47L38 -73','#bfdcd7',5)],'Aster can adjust the model but its inhabitants are not reduced to the controls');
  obj('prediction',975,254,[rect(-80,-47,160,76,'#dfd4e9','#d0c7e0',9),label('Expected next',0,-17,23),path('M-32 7H33M33 7L20 -3M33 7L20 17',c.violet,5)],'A limited predicted next gesture is shown as a projection, not a magical mind-reading conclusion');a.reveal('prediction',3);a.hide('prediction',4);
  obj('analysis-slip',626,524,[rect(-89,-22,178,44,c.paper,'#d1ded5',4),label('Changed rule',0,7,25)],'A provisional description attaches to the model rather than replacing the people');a.reveal('analysis-slip',2);a.hide('analysis-slip',6);
  obj('detour',579,442,[path('M-102 13L-63 -6L9 32L52 21',c.coral,10)],'A changed route adds a detour to an inhabitant’s existing appointment');a.reveal('detour',5);
  look('aster','pupil',1);gesture('aster',2,'explain');expression('aster','tired',3);gesture('pupil',3,'question');expression('pupil','skeptical',4);gesture('pupil',4,'reflect');expression('aster','surprised',4);look('resident','visitor',2);gesture('resident',4,'question');a.move('visitor',5,589,499,3000);look('aster','resident',5);expression('aster','curious',6);gesture('aster',6,'release');
 } else if(index===1){
  // Shelf depth grows, but the reader still has one choice to make.
  // Books are drawn as real spines sitting on each shelf, with restrained variety.
  const shelves=(id,x,y,w,h,cols)=>{const children=[rect(-w/2,-h,w,h,'#c7d7ca','#4e6b72',4)];for(let row=0;row<3;row++){const bottom=-h+(row+1)*h/3-9;children.push(rect(-w/2,bottom,w,9,c.wood));for(let col=0;col<cols;col++){const bw=(w-24)/cols-4,bx=-w/2+12+col*(bw+4),bh=h/3-22-(col+row)%3*8,color=[c.teal,c.coral,c.gold,c.violet][(col+row)%4];children.push(rect(bx,bottom-bh,bw,bh,color,color,2),path(`M${bx+4} ${bottom-bh+7}H${bx+bw-4}`,c.paper,2));}}return obj(id,x,y,children,'Believable varied book spines rest on actual shelves');};
  shelves('left-shelves',216,470,260,302,7);shelves('right-shelves',1020,470,212,247,6);shelves('new-shelves',668,303,282,149,9);a.reveal('new-shelves',1);
  person('reader',565,551,c.teal,'person-03-neutral',1.06,true);
  obj('desk',596,443,[fill('M-244 -3H240L264 22H-275Z',c.wood),rect(-275,22,539,15,c.wood),path('M-224 37V109M220 37V109',c.wood,16)],'A reading desk grounds the hands and the finite selection task');
  open('candidate-a',456,440,125,68,c.coral);closed('candidate-b',711,439,110,64,c.violet,'A different candidate offers another possible route');
  obj('chosen-place',578,444,[rect(-65,-18,130,22,'#e7d8bb','#748b89',4)],'Only one useful reading can occupy the reader’s current attention');
  clock('time',900,183);obj('time-later',900,183,[path('M0 -21V0L-9 20',c.ink,4)],'Elapsed time makes the selection consequence visible');a.reveal('time-later',3);a.hide('time-hand',3);
  closed('extra-candidate',759,425,89,32,c.gold,'Additional choice does not automatically relieve the reader’s uncertainty');a.reveal('extra-candidate',4);
  obj('operation-note',199,525,[rect(-105,-26,210,43,c.paper,'#d1ded5',4),label('Scarcity shift',0,3,27)],'This label identifies the source’s operation shown by the shelves and decision');a.reveal('operation-note',5);
  expression('reader','happy',1);look('reader','candidate-a',2);gesture('reader',2,'question');look('reader','time',3);expression('reader','worried',3);gesture('reader',4,'reflect');look('reader','candidate-b',5);expression('reader','determined',5);a.move('candidate-b',6,578,444,3000);a.hide('chosen-place',6);expression('reader','relieved',6);gesture('reader',6,'release');
 } else if(index===2){
  // A shared earlier promise becomes a present relationship across different futures.
  obj('shared-room',603,443,[fill('M-434 -69L-147 -105L-15 -39L363 -93L435 22L61 68L-436 16Z','#c6d8ca','#536f74'),fill('M-436 16L61 68L435 22V43L61 90L-436 40Z',c.wood)],'One shared domestic past supports two diverging future appointments');
  obj('table',601,411,[fill('M-119 -5H127L147 25H-140Z',c.wood),path('M-103 25V104M110 25V104',c.wood,12)],'An earlier commitment remains on the common table');
  obj('shared-photograph',602,366,[rect(-62,-70,124,90,c.paper,'#d3ddd6',4),rect(-51,-59,102,68,'#b8d7d5','#739c9d',1),dot(-21,-36,12,c.coral),dot(23,-36,12,c.gold),fill('M-39 1V-14Q-22 -29 -4 -14V1Z',c.coral),fill('M7 1V-14Q24 -29 41 -14V1Z',c.gold)],'Both future people share this remembered relationship');
  person('future-a',319,491,c.teal,'person-02-neutral',.88);person('future-b',875,491,c.violet,'person-02-neutral',.88);a.reveal('future-b',1);
  person('waiting-person',448,548,c.coral,'person-03-neutral',.75);
  obj('appointment-a',213,225,[rect(-63,-39,126,88,c.paper,'#d9ded4',5),rect(-63,-39,126,22,c.teal),label('Tuesday',0,13,25),path('M-27 30H26',c.teal,4)],'One future already has a distinct practical commitment');
  obj('appointment-b',979,225,[rect(-63,-39,126,88,c.paper,'#d9ded4',5),rect(-63,-39,126,22,c.violet),label('Thursday',0,13,25),path('M-27 30H26',c.violet,4)],'The second future is not interchangeable with the first');a.reveal('appointment-a',2);a.reveal('appointment-b',2);
  obj('commitment',600,423,[rect(-84,-43,168,59,'#e7cf9c','#c6bd96',4),label('The same promise',0,-6,23)],'A pre-copy commitment addresses two people whose futures now differ');a.reveal('commitment',3);
  obj('visitor-note',956,415,[rect(-84,-42,168,90,c.paper,'#d4dfd5',5),label('Copying',0,-9,28),label('+ time',0,25,28)],'The analytical combination does not settle who owes the existing obligation');a.reveal('visitor-note',4);a.hide('visitor-note',6);
  look('future-a','shared-photograph',1);look('future-b','shared-photograph',1);look('future-a','appointment-a',2);look('future-b','appointment-b',2);gesture('future-a',2,'explain');gesture('future-b',2,'explain');look('future-a','waiting-person',3);look('future-b','waiting-person',3);gesture('waiting-person',3,'question');expression('future-a','worried',3);expression('future-b','skeptical',3);gesture('future-b',4,'explain');gesture('waiting-person',5,'resolve');expression('waiting-person','determined',5);gesture('future-b',6,'release');expression('future-b','curious',6);look('future-b','waiting-person',6);
 } else {
  // Reader-eye view: source taxonomy and lived encounter share a bound spread.
  obj('reading-surface',600,490,[fill('M-430 -212H422L484 51H-474Z','#d4c2a4','#596e73'),fill('M-474 51H484V67H-474Z',c.wood)],'A real reading surface supports the invitation to enter both forms of this book');
  open('reader-volume',600,475,780,266,c.teal);
  obj('atlas-page',407,321,[label('Scarcity shift',0,-30,28,c.ink),rect(-99,-7,43,92,c.violet),rect(-49,6,42,79,c.coral),rect(0,-15,39,100,c.gold),rect(46,-1,41,86,c.teal),path('M-107 94H91',c.wood,9),path('M-13 111H54M54 111L44 104M54 111L44 118',c.ink,4)],'A single readable worked operation stands for the atlas, not a miniature unreadable table');
  obj('story-page',793,299,[label('The first night',0,-11,29,c.ink),fill('M-133 137L36 92L144 137L-17 177Z','#9bc9bb','#779f95'),rect(69,83,45,35,c.coral),path('M72 118V139M108 118V131',c.wood,5)],'The facing page invites an encounter with inhabitants rather than another abstract classification');
  person('page-visitor',732,432,c.gold,'person-15-neutral',.39);person('page-resident',852,415,c.coral,'person-03-neutral',.43);
  obj('literary-origin',791,455,[label('Borges · Le Guin',0,0,23,c.ink)],'A restrained literary-origin inscription records an intellectual genealogy, not an endorsement');a.reveal('literary-origin',4);
  obj('provisional-note',655,360,[rect(-49,-31,98,52,'#d8d1e7','#a8abc5',3),path('M-31 -12H31M-31 2H18',c.violet,3)],'The visiting reader’s useful category remains revisable');a.reveal('provisional-note',3);a.hide('provisional-note',5);
  obj('left-hand',220,515,[fill('M-35 25L-15 -35Q-9 -56 1 -53Q10 -50 5 -31L3 -15L28 -55Q35 -66 42 -61Q49 -57 41 -41L31 -16Q44 -37 52 -29Q59 -22 47 -2L22 31Z','#c88969')],'The visitor is literally beginning to read');
  obj('right-hand',991,510,[fill('M-13 30L-29 -3L-43 -37Q-49 -52 -40 -54Q-32 -57 -25 -43L-12 -22L-16 -65Q-16 -82 -7 -82Q3 -82 3 -67L5 -23Q25 -45 34 -35Q41 -27 29 -10L17 28Z','#c88969')],'A hand is ready to turn the next page, leaving the narrative unresolved');
  a.move('left-hand',1,247,501,2000);a.move('right-hand',2,974,500,2200);look('page-visitor','page-resident',2);gesture('page-visitor',3,'explain');gesture('page-resident',3,'question');expression('page-resident','skeptical',3);a.move('page-resident',5,873,421,2200);expression('page-visitor','curious',5);gesture('page-visitor',6,'release');a.move('right-hand',6,945,489,2600);
 }
 s.visual=a.finish(s.adaptation.composition+' Each physical change is cue-bound to its sentence. This is conceptual visual staging of source-supported ideas, not a claim about additional named plot events.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
