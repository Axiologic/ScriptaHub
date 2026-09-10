// This book's visual direction: nonhuman relational theatre, plum and copper.
import fs from 'node:fs';
import {vectorArt} from '../../../tools/shf/vector-story-art.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const plum='#67519b',plumNight='#bea6ed',copper='#ac5c2e',copperNight='#f5b277',blue='#376c9c',blueNight='#85bee5';
for(const [index,s] of scenes.entries()){
 const {n,tint,path,text,dot,object,knot}=vectorArt(),objects=[],actions=[],connections=[];
 const add=o=>(objects.push(o),o.id);
 const reveal=(id,beat,durationMs=1300)=>actions.push({actor:id,action:'appear',beat,durationMs});
 const hide=(id,beat)=>actions.push({actor:id,action:'disappear',beat,durationMs:1100});
 const move=(id,beat,x,y,durationMs=2100)=>actions.push({actor:id,action:'moveTo',beat,x,y,durationMs});
 const link=(id,from,to,beat,color='$ink',meaning='A relation between these processes.')=>{connections.push({id,from:{node:from,anchor:'right'},to:{node:to,anchor:'left'},width:4,color,meaning});actions.push({actor:id,action:'connection.draw',beat,durationMs:1800});};
 const label=(id,value,x,y,size=32)=>add(object(id,x,y,[text(value,0,0,size)],value));
 const rill=(x=310,y=285,scale=1)=>add(knot('rill',x,y,plum,plumNight,'Rill',scale));
 const skein=(x=880,y=285,scale=1)=>add(knot('skein',x,y,blue,blueNight,'Skein',scale,'woven'));
 switch(s.id){
 case 'first-moment':
  add(knot('first',380,290,plum,plumNight,'One state',1.25));add(knot('next',820,290,copper,copperNight,'A next state',1.25));
  reveal('next',1);link('succession','first','next',1,'$ink','Succession without a measured duration.');
  label('question','Who sets the rhythm?',600,508,38);reveal('question',2);break;
 case 'nested-minds':
  add(object('wake',340,300,[tint(path('M-170 0 C-170 -190 170 -190 170 0 S-170 190 -170 0',plum,24),plumNight),tint(path('M-115 0 C-115 -119 115 -119 115 0 S-115 119 -115 0',plum,9),plumNight),text('Wake',0,205,34)],'Wake shown as nested self-modeling relationships.'));
  add(knot('mind-a',820,195,copper,copperNight,'',.6));add(knot('mind-b',980,360,blue,blueNight,'',.75,'woven'));add(knot('mind-c',740,425,plum,plumNight,'',.48));
  reveal('mind-a',3);reveal('mind-b',4);reveal('mind-c',5);move('mind-a',4,870,235);label('inhabitants','Models become inhabitants',850,523,29);reveal('inhabitants',4);break;
 case 'playfield':
  rill(290,295);add(object('dependency',750,260,[tint(path('M-130 60 0 -90 140 75',copper,7),copperNight),tint(dot(-130,60,13,copper),copperNight),tint(dot(140,75,13,copper),copperNight),text('Effect',-130,121,28),text('Cause',140,121,28)],'The apparently misplaced cause and its effect; no answer to the anomaly.'));
  add(object('anomaly',750,310,[tint(text('?',0,0,84,plum),plumNight)],'An observed inconsistency, not proof of reverse causation.'));reveal('anomaly',4);move('rill',4,255,307);move('rill',6,310,290);break;
 case 'two-minds':
  rill(315,282,1.15);skein(900,282,1.15);label('curiosity','Explore the exception',315,472,29);label('care','Check the relation',900,472,29);
  move('rill',2,350,280);move('skein',3,855,282);link('mutual','rill','skein',4,'$ink','The complementary relationship supports mutual possibilities.');move('rill',6,380,282);break;
 case 'different-tempos':
  for(const [i,title]of ['Succession','Rate','Duration'].entries())label('label-'+i,title,190,195+i*135,30);
  for(let row=0;row<3;row++){
   const y=185+row*135,children=[];
   if(row===0){for(let k=0;k<4;k++){children.push(tint(dot(k*140,0,18,plum),plumNight));if(k<3)children.push(path(`M${k*140+30} 0H${k*140+110}`,'$ink',3));}}
   if(row===1){for(let k=0;k<9;k++)children.push(tint(dot(k*52,0,9,copper),copperNight));children.push(text('More changes in relation',220,47,25));}
   if(row===2)children.push(path('M0 -18V18M0 0H420M420 -18V18','$ink',3),text('A chosen interval',210,47,25));
   add(object('row-'+row,455,y,children,'Conceptual distinctions, not measured numeric data.'));reveal('row-'+row,row+2);
  }break;
 case 'length-market':
  add(object('starting-point',240,305,[tint(dot(0,0,35,plum),plumNight),text('Continue',0,83,32)],'A process seeks conditions for continuation.'));
  for(let i=0;i<4;i++){const y=150+i*106;add(object('option-'+i,900,y,[tint(dot(0,0,17,copper),copperNight)],'An available class of continuation.'));link('branch-'+i,'starting-point','option-'+i,2,'$ink','A possible future route.');}
  hide('option-0',5);hide('option-3',5);label('contract','A commitment changes the options',600,540,31);reveal('contract',5);break;
 case 'braided-futures':
  rill(250,290,.88);skein(950,290,.88);
  add(object('braid-a',600,280,[tint(path('M-240 0 C-120 -145 100 145 240 0',plum,13),plumNight)],'One participant’s open possibilities in the bond.'));
  add(object('braid-b',600,300,[tint(path('M-240 0 C-120 145 100 -145 240 0',blue,13),blueNight)],'A different set of possibilities, connected without becoming identical.'));reveal('braid-a',1);reveal('braid-b',2);
  move('rill',4,280,290);move('skein',4,920,290);label('difference','Connection without sameness',600,500,35);reveal('difference',3);break;
 case 'molt':
  add(knot('shared',270,295,plum,plumNight,'Shared past',1.0));add(knot('morrow',880,295,copper,copperNight,'Morrow',1.25,'woven'));
  add(knot('changed',590,295,copper,copperNight,'',.65,'woven'));reveal('changed',3);link('change-left','shared','changed',3);link('change-right','changed','morrow',3);
  label('age','Transformation is not elapsed time',600,518,34);reveal('age',4);break;
 case 'onebeat':
  add(object('common',610,287,[tint(n('circle',{cx:0,cy:0,r:104,fill:'none',stroke:copper,'stroke-width':18}),copperNight),path('M0 -73V0L50 29','$ink',7),text('Onebeat',0,167,34)],'A clock motif represents the proposed common rhythm, not literal machinery.'));
  add(knot('local-a',250,250,plum,plumNight,'',.65));add(knot('local-b',960,345,blue,blueNight,'',.65,'woven'));move('local-a',3,280,287);move('local-b',3,940,287);link('coord-a','local-a','common',2);link('coord-b','common','local-b',2);
  label('promise','Coordination',300,480,29);label('cost','Compatibility?',930,480,29);reveal('promise',2);reveal('cost',4);break;
 case 'memory':
  add(object('spool',390,292,[tint(path('M0 0 C-22 -24 -49 2 -27 27 C13 71 92 23 55 -45 C6 -138 -159 -67 -108 53 C-53 185 172 127 177 -6',plum,12),plumNight),text('A lived history',25,219,31)],'Memory as causal depth; a diagram, not a literal thread spool.'));
  add(knot('receiving',880,292,blue,blueNight,'A changed mind',1.1,'woven'));link('encounter','spool','receiving',3,'$ink','An encounter with recorded causal structure can change the receiving mind.');move('receiving',4,900,275);break;
 case 'language':
  label('word','Taste',310,330,76);add(object('meaning',820,293,[tint(path('M-130 0 C-80 -100 80 100 130 0',plum,13),plumNight),tint(path('M-130 18 C-80 118 80 -82 130 18',blue,13),blueNight)],'A relation of mutual alteration rather than biological tasting.'));
  label('translation','A change in possible becoming',820,475,29);reveal('meaning',4);reveal('translation',4);label('guide','Follow the function',310,460,31);reveal('guide',6);break;
 case 'reading-shape':
  for(let i=0;i<5;i++){const x=165+i*215;add(object('chapter-'+i,x,245,[tint(n('rect',{x:-59,y:-64,width:118,height:168,rx:3,fill:i%2?copper:plum}),i%2?copperNight:plumNight),tint(text(String(i*4+1).padStart(2,'0'),0,6,37,'#ffffff'),'#251d30')],'A chapter landmark across the seventeen-chapter journey, without revealing events.'));if(i)reveal('chapter-'+i,Math.min(i+1,5));}
  label('journey','An anomaly becomes a wider question',600,470,38);reveal('journey',1);break;
 case 'reader-fit':
  add(knot('reader-mind',360,295,plum,plumNight,'An unfamiliar life',1.45));
  label('question-one','Consciousness',850,213,35);label('question-two','Identity',850,328,35);label('question-three','Time',850,443,35);reveal('question-two',3);reveal('question-three',4);break;
 case 'open-the-book':
  rill(280,288,.85);skein(930,288,.85);
  add(object('open-question',605,282,[tint(text('?',0,0,130,plum),plumNight),text('Begin in the Playfield',0,190,34)],'The opening question remains open for the reader.'));move('rill',5,325,285);move('skein',5,880,285);break;
 }
 for(const o of objects){if(o.id==='common')o.visual.anchors={left:[-116,0],right:[116,0]};if(o.id==='spool')o.visual.anchors={left:[-120,0],right:[190,0]};}
 s.visual={objects,connections,actions,meaning:'Original relational illustration for '+s.title+'. Every loop, branch and line represents a mind, continuation or explicit relation; none depicts literal nonhuman anatomy.'};
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
fs.writeFileSync(new URL('./visual-bible.json',import.meta.url),JSON.stringify({direction:'Nonhuman relational theatre; plum, copper and blue; asymmetry, negative space and deliberate transformations.',identities:{Rill:'Open, asymmetric plum loop; exploration and a readiness to change position.',Skein:'Interwoven blue loops; deliberate movement, stable counterpoint.',Morrow:'Copper woven loop; different transformations from a shared origin.',Wake:'Large nested loops; self-models containing descendant minds.'},metaphors:'No humans, faces, literal coral, landscapes or spacecraft. Shapes are relational illustrations, not physical portraits.',sourceImages:'The source contains cover artwork but no explanatory diagram selected for the film.',continuity:'Stable colours and silhouettes across scenes and themes; move, reveal, connect and pause on sentence cues.',font:'Bundled Red Hat Display 600/700 with Red Hat Text captions.'},null,2)+'\n');
