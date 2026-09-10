import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
export function ceramicArt(index){
 const a=stageAuthor(),{n,path,text}=a, ink='#293b51',clay='#c98762',glaze='#384b78',brick='#a76650',paper='#f5e8cc',lake='#8dc0c4',copper='#c9944e';
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
 const solid=(d,fill)=>n('path',{d,fill});
 const bowl=(id,x,y,k=1)=>shape(id,x,y,[solid('M-138 -33Q-20 -14 135 -43Q120 85 15 103Q-95 103 -138 -33Z',clay),n('ellipse',{cx:0,cy:-34,rx:135,ry:32,fill:paper,transform:'rotate(-3)'}),solid('M-135 -30Q-105 15 -45 5Q37 -13 126 -43Q137 -24 106 -6Q8 54 -87 26Q-120 14 -135 -30Z',glaze),path('M-105 46Q-64 84 -15 83',copper,4)],'Mara’s fired bowl with uneven lip and pooled ash glaze',k);
 const table=(id,x,y,w=720)=>shape(id,x,y,[rect(-w/2,-5,w,23,brick),path(`M${-w/2+23} 18V115M${w/2-23} 18V115`,'$ink',9)],'Physical brick worktable and supports');
 const hand=(id,x,y,k=1)=>shape(id,x,y,[path('M-70 5L-15 0L19 -12M-15 0L20 5M-10 1L18 18','#bf947b',14)],'Hand reaching for a real work object',k);
 const portrait=(id,x,y,old,k=.8)=>shape(id,x,y,[rect(-45,-81,90,134,paper,9),solid('M-38 48V14Q0 -8 38 14V48Z',old?'#799597':glaze),n('ellipse',{cx:0,cy:-28,rx:23,ry:30,fill:'#b58c72'}),path('M-21 -44Q0 -65 21 -44',old?'#abb3b5':'#353035',9),path('M-12 -31H-6M6 -31H12M-7 -9H8',ink,2),path('M21 23L38 1L42 -3M38 1L42 8',ink,4)],old?'Present biological Elias, older':'Recorded younger likeness of Elias',k);
 if(index===0){
  table('brick-table',592,463,775);bowl('bowl',565,368,.85);
  shape('tongs',412,384,[path('M-140 -22L4 3L36 -31M-140 -12L1 15L36 27',ink,8)],'Iron tongs beside the fired bowl');hand('mara-hand',238,361,.8);
  shape('toolbox',877,423,[rect(-73,-54,146,65,copper,7),path('M-27 -54V-72H27V-54',ink,5),path('M-47 -42L-35 -10M-15 -43V-7M12 -36L36 -9',ink,5)],'Elias’s wooden repair toolbox rests on worktable');
  a.move('tongs',3,356,410,2000);a.move('mara-hand',3,203,392,2000);
 }else if(index===1){
  table('workbench',596,455,850);bowl('kept-bowl',420,368,.72);
  shape('recycle-tray',255,453,[path('M-70 -17L-52 0H52L70 -17',ink,5)],'Suggested recycling tray stays empty');a.move('kept-bowl',1,532,368,2600);
  shape('sensor',849,421,[rect(-48,-35,96,43,lake,5),rect(-34,-25,68,26,glaze),path('M-64 9H64',ink,5)],'Opened old kiln temperature sensor');
  shape('driver',819,340,[rect(-8,-36,16,36,copper,4),path('M0 0V57',ink,5)],'Screwdriver engaged with the old sensor');hand('elias-hand',871,317,.75);
  shape('band',906,310,[rect(-10,-12,20,24,ink,3),rect(-6,-7,12,14,'#e9b15d')],'Medical wrist-band notification');a.reveal('band',4);a.move('driver',4,753,431,1900);a.move('elias-hand',4,886,375,1900);
  shape('consultation',607,332,[rect(-330,-112,660,245,paper,12),text('Advanced treatment',-161,-55,29,ink),text('Completed Continuity',151,-55,29,ink),path('M-40 4H40',copper,6),rect(-245,-28,156,88,lake,5),rect(89,-28,156,88,glaze,5),text('Palliative and emergency care remain',0,106,24,ink)],'Fictional allocation condition; basic care is not denied');a.reveal('consultation',5);
  for(const id of ['kept-bowl','driver','elias-hand','band','sensor','recycle-tray'])a.hide(id,5);
 }else if(index===2){
  portrait('present-elias',349,369,true,1.25);portrait('recorded-elias',797,322,false,1.35);
  shape('recording-frame',797,318,[path('M-90 -140H90V130H-90Z',lake,5),text('Recording',0,-153,29,'$ink'),path('M-67 103H67',copper,4),n('circle',{cx:-46,cy:103,r:6,fill:copper})],'Recorded projection, never a copied body walking into the room');
  hand('supporting-palm',794,485,.75);a.label('present-label','Elias, present',349,487,29);
  shape('gesture-detail',592,355,[path('M-34 16L-10 -16L6 -6M-10 -16L-2 -31M6 -6L21 -12M6 -6L20 5','#bf947b',10)],'Same thumb-and-forefinger habit provides recognition, not identity proof',1.2);a.reveal('gesture-detail',3);
  a.label('unresolved','Source unresolved',797,530,24);a.reveal('unresolved',4);
 }else{
  table('reading-table',607,485,842);
  shape('volume',581,362,[solid('M-260 -106Q-135 -127 0 -87Q132 -127 260 -106V118Q130 89 0 131Q-130 89 -260 118Z',paper),path('M0 -87V131',copper,4),text('The Bowl',-126,-38,34,ink),text('That Listened',-126,7,31,ink),path('M-210 43H-48M-210 61H-75',lake,3)],'Actual book opening at the first chapter');
  bowl('original-bowl',922,426,.38);hand('reader-hand',352,466,.68);a.move('reader-hand',3,419,452,2400);
  shape('page-mark',678,426,[solid('M-12 -12H12V45L0 30L-12 45Z',glaze)],'First-chapter bookmark');a.reveal('page-mark',3);
 }
 return a.finish('Ceramic studio and mediated portrait: physical imperfections, treatment conditionality and a recorded likeness; quiet source-specific staging. Draft pending visual QA.');
}
