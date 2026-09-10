import fs from 'node:fs';
import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('../work/scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const plum='#74506e',copper='#ab684a',cream='#f4e5cf',ink='#3f3448',mint='#7d9d89',skin='#bb8065';
for(const [i,s]of scenes.entries()){
 const a=stageAuthor(),{n,path,text,tint}=a;
 const obj=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
 const fill=(d,c)=>n('path',{d,fill:c});
 const label=(v,x,y,size=27,c=ink)=>text(v,x,y,size,c);
 const stroke=(d,c=ink,w=5)=>path(d,c,w);
 const paper=(x,y,w,h)=>n('rect',{x,y,width:w,height:h,rx:3,fill:cream});
 const desk=(id,x,y,w=820)=>obj(id,x,y,[n('rect',{x:-w/2,y:0,width:w,height:22,rx:5,fill:'#b6967e'}),tint(stroke(`M${-w/2+35} 22V125M${w/2-35} 22V125`,'#715c56',10),'#c6b5ab')],'A supported editorial work surface');
 const tabs=[['Forgiveness',plum],['Emotion',copper],['Meaning',mint],['Justice','#6b89a2']];
 const volume=(id,x,y,k=1)=>obj(id,x,y,[fill('M-155 -100Q-75 -125 0 -100Q80 -125 155 -100V112Q70 87 0 111Q-80 87 -155 112Z',plum),fill('M-148 -98Q-74 -117 -4 -96V100Q-74 80 -148 99Z',cream),fill('M4 -96Q75 -117 148 -98V99Q74 80 4 100Z',cream),stroke('M0 -99V107','#b8a18d',2)],'The actual book opened for reading, not a mind or society',k);
 const express=(id,beat,expression)=>a.actions.push({actor:id,action:'character.express',emotion:expression,beat,durationMs:700});
 const hand=(id,x,y,side=1)=>obj(id,x,y,[fill(`M${-25*side} ${i===3?48:80}L${-20*side} 33Q${-24*side} 15 0 5Q${10*side} -8 ${19*side} 0L${22*side} 31L${31*side} ${i===3?48:80}Z`,plum),fill(`M${-20*side} 31L${-18*side} 0Q${-16*side} -21 ${-8*side} -14L${-5*side} 2L${0} -19Q${6*side} -27 ${12*side} -17L${20*side} 7L${29*side} 4Q${43*side} 7 ${36*side} 19L${21*side} 36Z`,skin)],'A cropped editorial hand physically reaching the paper edge');
 switch(i){
 case 0:{
  storyPerson(a,'reader',240,535,{identity:'person-10-neutral',coat:plum,scale:.92,seated:true,chair:mint});
  desk('table',670,430,720);volume('book',535,358,.62);
  obj('proof',830,330,[paper(-164,-134,328,234),label('Ambition is often',0,-73,29),label('shame with a calendar',0,-29,27),stroke('M-131 5H131','#bd9678',2),label('A claim to examine',0,53,24)],'Exact source phrase presented for examination, with no truth certification');
  obj('margin',830,436,[paper(-164,-12,328,59),label('What does it explain?',0,27,25)],'The reader opens a question beside the unchanged source phrase');a.reveal('margin',2);
  tabs.forEach(([v,c],j)=>{obj('tab'+j,434+j*62,420,[n('rect',{x:-26,y:-6,width:53,height:11,rx:2,fill:c})],'Four chapter tabs attached to the actual book');a.reveal('tab'+j,3)});
  storyGesture(a,'reader',1,'reflect');express('reader',2,'skeptical');storyGesture(a,'reader',4,'question');express('reader',5,'curious');
  break;
 }
 case 1:{
  obj('worktop',600,333,[n('rect',{x:-455,y:-170,width:910,height:338,rx:18,fill:'#b6967e'}),n('rect',{x:-436,y:-152,width:872,height:301,rx:9,fill:'#d3b89e'})],'Overhead editorial desk; papers rest on its surface');
  obj('first',440,326,[paper(-117,-121,234,225),label('First draft',0,-74,28),label('Emotionally thin',0,-18,23),stroke('M-74 25H76',plum,3)],'First forgiveness draft rejected as emotionally thin');
  hand('left-hand',343,409);a.move('first',2,319,326,1800);a.move('left-hand',2,222,409,1800);
  obj('second',632,326,[paper(-110,-121,220,225),label('Second draft',0,-74,27),label('Cold',0,-18,25),stroke('M-72 25H72',copper,3)],'Second forgiveness draft rejected as cold');a.reveal('second',2);hand('right-hand',728,409,-1);a.reveal('right-hand',2);
  a.move('second',3,878,326,2100);a.move('right-hand',3,974,409,2100);
  obj('request',600,190,[paper(-172,-30,344,59),label('Bring emotional force',0,7,24)],'Paraphrase of the editorial revision request, not an invented exact prompt');a.reveal('request',3);
  obj('revision',599,363,[paper(-125,-111,250,228),label('Revised prose',0,-62,28),label('Retained for reading',0,-14,22),stroke('M-83 27H84',plum,3),n('rect',{x:99,y:46,width:12,height:55,fill:copper})],'The selected literary artifact, not scientific approval');a.reveal('revision',4);
  a.move('left-hand',5,488,446,1900);a.move('right-hand',5,710,446,1900);
  break;
 }
 case 2:{
  storyPerson(a,'illustrator',425,538,{identity:'person-10-neutral',coat:plum,scale:.91});
  obj('easel',710,407,[tint(stroke('M-82 -96L-125 131M77 -96L121 131M-97 42H100','#756058',10),'#c7b6a6'),fill('M-140 -198H140L123 28H-156Z','#b6967e'),fill('M-126 -183H126L111 14H-142Z',cream)],'An unfinished bird drawing on a physically supported slanted board');
  obj('bird',702,340,[fill('M-77 17Q-100 -42 -40 -62Q-12 -99 24 -68Q58 -74 72 -47L103 -33L70 -24Q49 27 -23 38L-79 72L-51 29Z','#86a29b'),n('circle',{cx:40,cy:-54,r:5,fill:ink}),stroke('M-17 36L-17 60M9 29L22 52',ink,3)],'The same recognisable unfinished bird throughout the imagined project');
  obj('wing',686,332,[stroke('M-46 6Q1 -24 41 -6Q15 23 -33 31',plum,4),stroke('M-25 13Q-2 9 20 -3M-21 23Q9 19 29 4',plum,3)],'A few deliberate drawing strokes add detail; no prize outcome is shown');a.reveal('wing',3,2200);
  obj('prize',918,234,[paper(-100,-63,200,127),label('Drawing prize',0,-22,26),label('30 June',0,22,28),n('circle',{cx:0,cy:-55,r:4,fill:copper})],'An imagined deadline pinned to the drawing stand, not a won award');
  obj('notice-support',918,413,[tint(stroke('M0 -120V124','#756058',7),'#c7b6a6')],'Support of the notice beside the same project');
  obj('memory',230,217,[paper(-115,-48,230,96),label('Remembered words',0,-12,20),label('Not serious enough',0,23,24)],'An imagined remembered dismissal; not narrator judgment');a.reveal('memory',2);
  // The pencil is held at the end of a custom reaching arm; both move together.
  const person=a.objects.find(o=>o.id==='illustrator');const arm=person.visual.children.find(c=>c.id==='$asset.armR');
  arm.children=[stroke('M32 -156Q82 -169 126 -190',plum,20),n('circle',{cx:130,cy:-191,r:10,fill:skin}),stroke('M131 -193L159 -213',copper,5)];
  obj('pencil-tip',570,344,[stroke('M0 0L58 -26',copper,5)],'Pencil reaching the bird paper rather than pointing to a floating symbol');a.reveal('pencil-tip',3);
  a.move('illustrator',3,477,538,2000);a.move('pencil-tip',3,622,344,2000);
  express('illustrator',2,'tired');express('illustrator',3,'inspired');express('illustrator',4,'curious');storyGesture(a,'illustrator',5,'reflect');
  break;
 }
 case 3:{
  obj('reading-desk',600,363,[n('rect',{x:-420,y:-194,width:840,height:362,rx:15,fill:'#b6967e'})],'Overhead reading surface');
  volume('volume',600,352,1.72);
  obj('chosen',468,309,[label('Ambition is often',0,-27,25),label('shame with',0,8,25),label('a calendar',0,43,25)],'The same actual source phrase in its book context');
  obj('context',730,343,[label('Reader’s note',0,-50,22),label('Lives can',0,-4,28),label('contain both',0,32,28),stroke('M-89 64H87',copper,2)],'Explicitly labelled reader paraphrase of the source qualification');a.reveal('context',2);
  tabs.forEach(([v,c],j)=>{obj('chapter-tab'+j,858,239+j*55,[n('rect',{x:-15,y:-12,width:32,height:35,rx:3,fill:c}),label(v,72,10,21)],'Chapter tab attached to the actual volume')});
  obj('preface',468,444,[label('Preface',0,0,27)],'Concrete starting place in the source volume');
  obj('bookmark',385,407,[fill('M-9 -27H9V25L0 17L-9 25Z',copper)],'A movable reading marker, not a completion badge');a.move('bookmark',3,385,459,1600);a.move('bookmark',4,385,375,1700);
  hand('reading-left',361,487);hand('reading-right',819,487,-1);a.move('reading-right',4,870,487,1700);
  break;
 }
 }
 if(i===2){const foreground=a.objects.filter(o=>['illustrator','pencil-tip'].includes(o.id));a.objects.splice(0,a.objects.length,...a.objects.filter(o=>!['illustrator','pencil-tip'].includes(o.id)),...foreground);}
 s.visual=a.finish(s.visual.meaning);
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
