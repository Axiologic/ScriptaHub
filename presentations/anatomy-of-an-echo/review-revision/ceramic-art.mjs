import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
export function ceramicArt(index){
 const a=stageAuthor(),{n,path,text}=a, ink='#293b51',clay='#c98762',glaze='#384b78',brick='#a76650',paper='#f5e8cc',lake='#8dc0c4',copper='#c9944e';
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
 const solid=(d,fill)=>n('path',{d,fill});
 const bowl=(id,x,y,k=1)=>shape(id,x,y,[solid('M-138 -33Q-20 -14 135 -43Q120 85 15 103Q-95 103 -138 -33Z',clay),solid('M-135 -27C-138 -44 -77 -61 -2 -66C73 -71 133 -62 135 -41C137 -22 77 -7 2 -2C-73 3 -133 -8 -135 -27Z',paper),solid('M-135 -30Q-105 15 -45 5Q37 -13 126 -43Q137 -24 106 -6Q8 54 -87 26Q-120 14 -135 -30Z',glaze),path('M-105 46Q-64 84 -15 83',copper,4)],'Mara’s fired bowl with uneven lip and pooled ash glaze',k);
 const table=(id,x,y,w=720)=>shape(id,x,y,[rect(-w/2,-5,w,23,brick),path(`M${-w/2+23} 18V115M${w/2-23} 18V115`,'$ink',9)],'Physical brick worktable and supports');
 const hand=(id,x,y,k=1)=>shape(id,x,y,[path('M-70 5L-15 0L19 -12M-15 0L20 5M-10 1L18 18','#bf947b',14)],'Hand reaching for a real work object',k);
 const sleeve=(id,x,y,side='left',coat=glaze)=>shape(id,x,y,[solid(side==='left'?'M-155 -31Q-86 -30 -49 -21L-8 -13L-26 15L-89 5Q-118 0 -155 7Z':'M155 -31Q87 -30 47 -21L-9 -10L12 16L84 5Q111 0 155 7Z',coat),solid('M-23 -15Q-12 -19 3 -10L19 -5Q30 0 22 9L4 8Q-7 18 -25 9Z','#bf947b'),path('M-3 -6L11 -2M-4 1L11 4',ink,2)],'Continuous clothed forearm, wrist and grasping fingers attached to a workshop participant');
 const bust=(id,x,y,coat=glaze,old=false)=>shape(id,x,y,[solid('M-63 85Q-61 -35 -32 -46Q0 -61 33 -46Q67 -29 68 85Z',coat),n('ellipse',{cx:0,cy:-90,rx:28,ry:35,fill:'#bf947b'}),path('M-27 -109Q0 -138 27 -107',old?'#9fabae':'#443a34',12),path('M-13 -94H-7M8 -94H14M-8 -72Q0 -67 9 -72',ink,3)],'Workshop participant shown continuously from head and torso into working sleeve');
 const portrait=(id,x,y,old,k=.8)=>shape(id,x,y,[rect(-45,-81,90,134,paper,9),solid('M-38 48V14Q0 -8 38 14V48Z',old?'#799597':glaze),n('ellipse',{cx:0,cy:-28,rx:23,ry:30,fill:'#b58c72'}),path('M-21 -44Q0 -65 21 -44',old?'#abb3b5':'#353035',9),path('M-12 -31H-6M6 -31H12M-7 -9H8',ink,2),path('M21 23L38 1L42 -3M38 1L42 8',ink,4)],old?'Present biological Elias, older':'Recorded younger likeness of Elias',k);
 if(index===0){
  bust('mara-potter',230,373,glaze);table('brick-table',592,463,775);
  bowl('bowl',565,330,.85);
  shape('tongs',565,330,[path('M-223 -10L-122 -34Q-138 -18 -116 4M-223 -3L-90 41Q13 77 99 20L111 -20','$ink',8),n('circle',{cx:-205,cy:-6,r:6,fill:copper})],'Iron tong jaws grip opposing outer sides of the hot bowl');
  sleeve('mara-grip',348,326,'left',glaze);
  shape('toolbox',897,447,[rect(-73,-54,146,65,copper,7),path('M-27 -54V-72H27V-54',ink,5),path('M-47 -42L-35 -10M-15 -43V-7M12 -36L36 -9',ink,5)],'Elias’s wooden repair toolbox base meets brick table');
  for(const [id,x,y]of [['bowl',565,370.45],['tongs',565,370.45],['mara-grip',348,366.45]])a.move(id,3,x,y,2300);
  for(const [id,x,y]of [['tongs',485,405],['mara-grip',268,401]])a.actions.push({actor:id,action:'moveTo',beat:3,offsetMs:2900,x,y,durationMs:1800});
  for(const id of ['tongs','mara-grip'])a.actions.push({actor:id,action:'disappear',beat:3,offsetMs:4700,durationMs:400});
  shape('resting-tongs',386,451,[path('M-100 -3L14 0L61 -15M-100 2L14 5L62 1','$ink',7)],'Released iron tongs lie on the brick tabletop after the bowl has settled');a.actions.push({actor:'resting-tongs',action:'appear',beat:3,offsetMs:4800,durationMs:400});
 }else if(index===1){
  bust('elias-repairer',950,365,'#799597',true);bust('mara-workmate',570,375,glaze);
  table('workbench',596,455,850);bowl('kept-bowl',350,375.84,.72);
  shape('recycle-tray',255,450,[path('M-70 -17L-52 0H52L70 -17','$ink',5)],'Suggested recycling tray stays empty');
  sleeve('mara-keeping',448,375,'right',glaze);a.move('kept-bowl',1,390,375.84,2600);a.move('mara-keeping',1,488,375,2600);a.move('mara-workmate',1,610,375,2600);
  shape('sensor',829,441,[rect(-48,-35,96,43,lake,5),rect(-34,-25,68,26,glaze),path('M-64 9H64',ink,5)],'Opened old kiln temperature sensor with base resting on bench');
  shape('driver',829,349,[rect(-8,-36,16,36,copper,4),path('M0 0V57','$ink',5)],'Screwdriver tip engages sensor housing, handle enclosed by Elias fingers');
  sleeve('elias-grip',829,326,'right','#799597');
  shape('band',861,318,[solid('M-13 -12L3 -20L20 6L5 15Z',ink),solid('M-7 -10L2 -15L12 3L4 8Z','#e9b15d')],'Medical wrist band lies across Elias’s sleeve cuff');a.reveal('band',4);
  // Tool and closed fingers share a small engaged pressing motion before interruption.
  for(const [id,x,y]of [['driver',829,352],['elias-grip',829,329]])a.move(id,2,x,y,750);
  for(const [id,x,y]of [['driver',829,349],['elias-grip',829,326]])a.actions.push({actor:id,action:'moveTo',beat:2,offsetMs:1200,x,y,durationMs:750});
  // Tool and closed fingers have identical displacement until Mara receives it.
  for(const [id,x,y]of [['driver',722,392],['elias-grip',722,369],['band',754,361]])a.move(id,4,x,y,2400);
  sleeve('mara-receiving',722,379,'left',glaze);a.actions.push({actor:'mara-keeping',action:'disappear',beat:4,offsetMs:0,durationMs:350});a.actions.push({actor:'mara-receiving',action:'appear',beat:4,offsetMs:600,durationMs:1200});
  a.actions.push({actor:'elias-grip',action:'moveTo',beat:4,offsetMs:2900,x:829,y:326,durationMs:1200});
  a.actions.push({actor:'band',action:'moveTo',beat:4,offsetMs:2900,x:861,y:318,durationMs:1200});
  shape('consultation',607,332,[rect(-330,-112,660,245,paper,12),text('Advanced treatment',-161,-55,29,ink),text('Completed Continuity',151,-55,29,ink),path('M-40 4H40',copper,6),rect(-245,-28,156,88,lake,5),rect(89,-28,156,88,glaze,5),text('Palliative and emergency care remain',0,106,24,ink)],'Fictional allocation condition; basic care is not denied');a.reveal('consultation',5);
  for(const id of ['kept-bowl','driver','elias-grip','band','sensor','recycle-tray','mara-receiving','mara-workmate','elias-repairer'])a.hide(id,5);
 }else if(index===2){
  // The present person is an unframed body; only the younger likeness is mediated.
  bust('present-elias',470,405,'#799597',true);
  shape('supporting-palm',605,429,[solid('M-113 -67Q-74 -62 -43 -23L14 -9L31 -18L40 -10L27 11Q-8 17 -59 -3L-113 -32Z','#799597'),path('M-12 -8L17 -8L31 -18M17 -8L37 -3','#bf947b',13)],'Older biological Elias’s short continuous forearm supports the nearby projected recording');
  portrait('recorded-elias',658,280,false,1);
  shape('recording-frame',658,279,[path('M-70 -100H70V107H-70Z',lake,4),text('Recording',0,-119,29,'$ink'),path('M-52 90H52',copper,4),n('circle',{cx:-35,cy:90,r:5,fill:copper})],'The younger likeness alone is bounded by recording controls');
  shape('present-gesture',478,400,[solid('M-34 -24Q-23 -17 -14 -3L15 -3L18 13L-23 17Q-43 3 -44 -17Z','#799597'),path('M8 4L27 0L33 -14M27 0L39 -4M27 0L37 10','#bf947b',7)],'Present right thumb and forefinger make the same small habit visible within the recording');
  a.label('present-label','Elias, present',470,532,29);a.label('unresolved','Source unresolved',676,491,24);a.reveal('unresolved',4);
  a.actions.push({actor:'present-gesture',action:'moveTo',beat:3,x:480,y:399,durationMs:1000});
  a.actions.push({actor:'recorded-elias',action:'moveTo',beat:3,x:658,y:278,durationMs:1000});
 }else{
  table('reading-table',607,485,842);
  shape('volume',581,349,[solid('M-260 -106Q-135 -127 0 -87Q132 -127 260 -106V118Q130 89 0 131Q-130 89 -260 118Z',paper),path('M0 -87V131',copper,4),text('The Bowl',-126,-38,34,ink),text('That Listened',-126,7,31,ink),path('M-210 43H-48M-210 61H-75',lake,3)],'Actual book opening at the first chapter');
  bowl('original-bowl',972,440.86,.38);shape('reader-hand',352,466,[solid('M-500 -30Q-110 -30 -49 -21L-8 -13L-26 15L-110 4L-500 7Z',glaze),solid('M-23 -15Q-12 -19 3 -10L19 -5Q30 0 22 9L4 8Q-7 18 -25 9Z','#bf947b'),path('M-3 -6L11 -2M-4 1L11 4',ink,2)],'Reader forearm enters continuously from the left edge, pointing to the opening chapter');a.move('reader-hand',3,419,452,2400);
  shape('page-mark',678,426,[solid('M-12 -12H12V45L0 30L-12 45Z',glaze)],'First-chapter bookmark');a.reveal('page-mark',3);
 }
 return a.finish('Ceramic studio and mediated portrait: physical imperfections, treatment conditionality and a recorded likeness; quiet source-specific staging. Supported material actions and continuous workshop forearms; QA required.');
}
