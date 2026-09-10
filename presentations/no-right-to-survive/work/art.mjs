import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [index,s]of scenes.entries()){
 const a=stageAuthor(),{n,path,text,tint,dot}=a,c={copper:'#c78160',blue:'#527995',plum:'#78617f',gold:'#c9a151',cream:'#f0e3cc',ink:'#334750',sage:'#8da99b'};
 const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
 const fill=(d,color,night=color)=>tint(n('path',{d,fill:color}),night);
 const rect=(x,y,w,h,color,night=color,r=0)=>tint(n('rect',{x,y,width:w,height:h,rx:r,fill:color}),night);
 const label=(v,x,y,size=28,color=c.ink)=>text(v,x,y,size,color);
 const action=(id,beat,verb,rest={})=>a.actions.push({actor:id,action:verb,beat,durationMs:1700,...rest});
 const gesture=(id,beat,g)=>storyGesture(a,id,beat,g,2400);
 const express=(id,beat,e)=>action(id,beat,'character.express',{emotion:e,durationMs:850});
 const look=(id,target,beat)=>action(id,beat,'lookAt',{target,durationMs:850});
 const person=(id,x,y,coat,identity='person-03-neutral',scale=.88,seated=false)=>{storyPerson(a,id,x,y,{coat,identity,scale,seated,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;};
 const desk=(id,x,y,w=540)=>obj(id,x,y,[fill(`M${-w/2+23} -11H${w/2-18}L${w/2+12} 14H${-w/2-12}Z`,c.copper),path(`M${-w/2+38} 15V100M${w/2-42} 15V100`,c.copper,13)],'A working surface supports the evidence and the reviewing action');
 const animal=(id,x,y,k=1)=>obj(id,x,y,[fill('M-87 -37Q-88 -86 -29 -91Q24 -99 59 -69L82 -55L91 -30Q63 -4 32 -18Q-28 2 -70 -18Z','#aa9a91','#bfaea2'),fill('M53 -65L54 -101L82 -84L74 -61Z','#aa9a91','#bfaea2'),n('ellipse',{cx:87,cy:-39,rx:25,ry:18,fill:c.copper}),dot(70,-65,4,c.ink),dot(87,-41,3,c.ink),tint(path('M-60 -16L-62 15M-19 -13L-22 16M35 -18L32 14M64 -24L62 12',c.ink,11),'#c6d1ce'),path('M-84 -48Q-106 -49 -100 -71Q-87 -78 -90 -61',c.plum,6)],'Interpretive generic farm-animal form; the source does not name an exact species',k);
 const patient=(id,x,y,k=1)=>obj(id,x,y,[rect(-101,-30,218,58,c.cream,'#d7dfd4',17),rect(-88,-32,67,43,'#e3d5b6','#c5cdbb',15),dot(-56,-32,24,'#dca987'),fill('M-40 -39Q6 -60 75 -35L108 -9V24H-33Z',c.blue,'#83acbc'),path('M-70 -36L-63 -33M-49 -34L-42 -37',c.ink,3),path('M-62 -18Q-54 -26 -43 -18',c.ink,3),path('M-19 -36L7 -15L33 -26','#dca987',10)],'A child grips the bedding; no wound or invasive procedure is depicted',k);
 const paper=(id,x,y,w,h,heading,color=c.plum)=>obj(id,x,y,[rect(-w/2,-h,w,h,c.cream,'#d5ded3',5),rect(-w/2,-h,w,27,color),label(heading,0,-h+62,28),path(`M${-w*.34} ${-h+83}H${w*.33}`,color,3)],'An administrative record stays tied to the observed subject');
 if(index===0){
  obj('ward-floor',337,496,[fill('M-210 -5H201L232 36H-222Z','#d9cdb2','#68797c')],'A pediatric care setting holds a particular patient');
  obj('bed',307,437,[rect(-151,-12,302,27,c.copper),path('M-131 15V62M123 15V62',c.copper,13),path('M-153 -89V14M146 -48V15',c.copper,12)],'The child’s bed has a supported mattress, headboard and footboard');patient('child',304,407,1.05);
  obj('care-stand',162,268,[path('M0 -47V203M-27 203H31',c.blue,9),path('M-25 -44H42',c.blue,7),rect(12,-33,47,64,'#c0d5d5','#a0c3c5',7),path('M34 31Q70 106 83 119',c.blue,4)],'An ordinary bedside infusion support anchors the source’s care failure without procedural detail');
  person('caregiver',539,541,c.copper,'person-04-neutral',.87);look('caregiver','child',1);express('caregiver',2,'worried');action('caregiver',2,'walkTo',{x:474,durationMs:2500});gesture('caregiver',3,'resolve');express('caregiver',3,'determined');
  obj('care-alert',309,268,[rect(-84,-35,168,64,c.cream,'#d8dfd3',6),label('Urgent care',0,6,28)],'The observed distress receives a care response');a.reveal('care-alert',2);
  obj('facility-floor',900,496,[fill('M-194 -5H192L219 36H-215Z','#a9bec2','#577584')],'A different institutional setting receives another distress report');
  obj('pen-back',925,413,[rect(-124,-120,248,140,'#c3cfd0','#819da3'),path('M-128 -131V90M125 -131V90M-129 -112H126M-130 -13H126',c.blue,12)],'A material partition limits the animal’s room to turn');animal('animal',908,477,.89);
  obj('pen-front',919,488,[path('M-129 -46V31M126 -46V31M-132 -33H128',c.blue,9)],'The enclosure is a source-relevant physical boundary, not a decorative frame');a.move('animal',2,930,477,2100);a.move('animal',4,916,477,2600);
  paper('equipment-order',1000,297,192,109,'Equipment',c.blue);a.reveal('equipment-order',3);obj('maintenance-tray',1070,541,[fill('M-67 -34H63L51 0H-60Z',c.blue),label('Maintenance',0,31,23,'$ink')],'The institution routes attention toward equipment rather than the subject');a.reveal('maintenance-tray',3);a.move('equipment-order',5,1100,520,2600);look('caregiver','care-alert',5);gesture('caregiver',6,'reflect');
 } else if(index===1){
  // The same evidence undergoes different administrative routing, viewed from the review desk.
  person('ethicist',588,548,c.plum,'person-03-neutral',1.04,true);desk('review-desk',603,450,720);
  paper('care-report',384,449,200,207,'Care response',c.copper);paper('facility-report',823,449,204,207,'Equipment risk',c.blue);
  patient('child-observation',384,380,.57);animal('animal-observation',823,393,.53);
  obj('care-receipt',260,445,[rect(-81,-52,162,59,'#d8d0b9','#c7d5ca',4),label('Care reached',0,-15,26)],'The first record returns an actual response to the affected subject');a.reveal('care-receipt',3);
  obj('work-order',968,380,[rect(-68,-50,136,90,c.cream,'#d1dbd2',4),label('Work order',0,-8,24),path('M-37 15H36',c.blue,3)],'The second record becomes a task for maintenance');a.reveal('work-order',2);
  obj('maintenance-box',1063,539,[fill('M-88 -52H83L67 10H-74Z',c.blue),path('M-17 -41L20 -75M12 -67Q-1 -83 14 -95L22 -79L37 -84L33 -101Q56 -96 45 -76L24 -59',c.copper,11)],'A maintenance tool and tray receive the work order');a.move('work-order',3,1057,525,2400);
  obj('caution',596,186,[rect(-104,-53,208,78,c.cream,'#d4ddd3',5),label('Comparable evidence',0,-17,22),label('Different experience',0,12,22)],'The comparison does not claim identical nervous systems or measured experiences');a.reveal('caution',4);
  look('ethicist','care-report',1);gesture('ethicist',2,'explain');look('ethicist','facility-report',3);express('ethicist',3,'worried');gesture('ethicist',4,'reflect');look('ethicist','animal-observation',5);express('ethicist',5,'curious');gesture('ethicist',6,'question');
 } else if(index===2){
  obj('inspection-light',0,0,[n('path',{d:'M450 287L900 215L930 425L475 327Z',fill:c.gold,opacity:.22})],'The audit lamp brings the judging instrument itself into the field of inspection');a.reveal('inspection-light',5);
  person('ethicist',301,548,c.plum,'person-03-neutral',.94);person('participant',998,548,c.copper,'person-02-neutral',.95);
  desk('audit-desk',625,444,546);
  obj('assessment-instrument',821,369,[rect(-91,-100,182,125,c.blue,'#6d92ad',9),rect(-76,-85,152,91,'#d9e2dc','#c6d9d8',3),label('Proposed',0,-47,27),label('judgment',0,-14,27),path('M-9 25V73M-63 74H66',c.blue,12)],'A fictional assessing instrument produces a revisable proposal, not an authorized moral oracle');
  paper('decision-record',610,443,167,150,'Under review',c.plum);a.reveal('decision-record',1);
  obj('lamp',391,424,[path('M-46 14H41M0 11V-78L78 -136',c.copper,11),fill('M57 -146L89 -152L117 -112L83 -85Z',c.gold)],'The reviewer can turn inspection toward the judging instrument itself');
  obj('pending-tray',714,446,[fill('M-107 -36H99L87 0H-95Z',c.plum),label('Not issued',0,-7,25,c.cream)],'No proposed judgment automatically becomes enforcement');a.reveal('pending-tray',4);
  look('ethicist','decision-record',1);gesture('participant',2,'question');express('participant',2,'skeptical');gesture('ethicist',3,'explain');look('participant','pending-tray',4);gesture('participant',4,'resolve');look('ethicist','assessment-instrument',5);gesture('ethicist',5,'question');express('ethicist',5,'skeptical');gesture('participant',6,'release');
 } else {
  // A close reading of the actual source exchange, not a second verdict.
  obj('reading-board',595,443,[fill('M-436 -213H407L448 64H-461Z','#b49b7e','#667d80'),fill('M-461 64H448V78H-461Z',c.copper)],'A reader’s sloped working surface supports the paired source records');
  paper('comparison-sheet',596,488,604,286,'Paired reports',c.plum);
  patient('reading-child',451,367,.59);animal('reading-animal',746,375,.55);
  obj('form-note',272,313,[rect(-99,-44,198,82,c.cream,'#d5dfd5',4),label('Form and evidence',0,-7,23),path('M-65 13H62',c.plum,3)],'The reading begins with the source’s statement of fictional/composite form');a.reveal('form-note',1);a.hide('form-note',3);
  obj('first-caution',419,433,[label('Resemblance',0,-9,25),label('is not equivalence',0,23,24)],'The ethicist’s warning preserves the difference between the experiences');
  obj('second-caution',748,433,[label('Difference',0,-9,25),label('is not insignificance',0,23,24)],'The narrator’s reply refuses to turn difference into negligible moral weight');a.reveal('first-caution',4);a.reveal('second-caution',4);
  obj('reader-hand',1007,484,[fill('M-34 45L-52 -1Q-60 -14 -51 -19Q-41 -24 -27 -6L-19 4L-22 -60Q-20 -82 -9 -79Q1 -79 -2 -59L4 -18Q25 -34 30 -19L32 30Z','#c89170')],'A reader holds the comparison open without issuing the judgment');a.move('reader-hand',2,982,483,2200);a.move('reader-hand',5,961,471,2100);a.move('reader-hand',6,980,479,2200);
 }
 s.visual=a.finish(s.adaptation.composition+' The source comparison concerns evidence of distress, not identical experience. All settings are interpretive staging of fictional/composite source scenes, and later verdicts remain undisclosed.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
