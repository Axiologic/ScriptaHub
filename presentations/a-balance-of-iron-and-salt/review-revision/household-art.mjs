import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
// Book-owned staging: no generic layouts or new shared player code.
export function householdArt(index){
 const a=stageAuthor(),{n,path,text}=a;
 const colors={plaster:'#f5e5c9',iron:'#a24e35',sea:'#388b94',basalt:'#243945',canvas:'#dcb25d',green:'#71a18a'};
 const shape=(id,x,y,kids,meaning,scale=1)=>a.add(a.object(id,x,y,kids,meaning,scale));
 const rect=(x,y,w,h,fill,rx=0)=>n('rect',{x,y,width:w,height:h,fill,rx});
 const ink='#243945';
 const robot=(id,x,y,scale=.8)=>shape(id,x,y,[
  // Four distinct splayed feet, not two humanoid legs; stone head has no eyes.
  path('M-28 55L-66 90L-88 90M28 55L66 90L88 90M-14 61L-37 110L-57 110M14 61L37 110L57 110',ink,10),
  rect(-28,-30,56,92,colors.basalt,12),n('ellipse',{cx:0,cy:-58,rx:38,ry:25,fill:colors.basalt}),
  path('M-20 -51H20M-20 -45H20','#a7beb8',3),
  path('M-27 -20L-49 12L-39 42M27 -20L48 8L67 -4',ink,8),
  n('circle',{cx:-49,cy:12,r:5,fill:colors.canvas}),n('circle',{cx:48,cy:8,r:5,fill:colors.canvas})
 ],'Small eyeless four-footed shell with acoustic grille and articulated arms',scale);
 const kazi=(id,x,y,scale=1)=>shape(id,x,y,[rect(-43,0,85,95,'#688d8a',5),path('M-40 95V120M38 95V120',ink,8),rect(-30,-25,60,67,'#738f87',13),n('circle',{cx:0,cy:-48,r:23,fill:'#b58866'}),path('M-20 -60Q0 -76 21 -60','#bfc6bf',9),path('M-11 -50H-6M8 -50H13M-7 -34H8',ink,2),path('M-27 -15L-47 18M27 -15L54 -37',ink,6),path('M-20 40L-24 86L-39 99M20 40L26 86L41 99',ink,12),path('M-62 12V116',ink,5)],'Living Kazi seated; hand raised in objection, cane beside chair',scale);
 const house=(id,x,y,scale=1)=>shape(id,x,y,[rect(-120,-192,240,280,colors.plaster),rect(-75,-130,150,218,colors.iron),path('M-132 -192L0 -235L132 -192','$ink',8)],'Port Nacre doorway',scale);
 const city=(id,x,y)=>shape(id,x,y,[path('M-170 25H170L130 75H-120Z',ink,8),rect(-170,-8,340,38,colors.basalt),rect(-135,-70,58,62,colors.iron),rect(-62,-105,54,97,colors.basalt),rect(8,-51,90,43,colors.green),rect(23,-115,60,64,'#9cc5bf'),path('M23 -115L53 -135L83 -115M53 -135V-51','#527e7d',3),rect(116,-80,38,72,colors.iron),...[[-125,-53],[-45,-75],[126,-60],[-125,-26],[-45,-42],[126,-31]].map(([x,y])=>rect(x,y,10,15,colors.canvas)),path('M-107 40L-80 78M90 42L72 82',ink,8)],'Asterion assembled floating platforms, warm windows, ballast fins and glass garden',.75);
 if(index===0){
  shape('floor',590,500,[rect(-440,0,880,12,colors.green)],'Shared ground beneath house and cart');house('door',335,410);kazi('living',334,422,.65);
  a.person('jonah',165,430,{coat:colors.iron,night:'#d08c67',scale:.45,pose:'concerned'});
  shape('cart',880,470,[rect(-80,-3,160,10,colors.canvas),n('circle',{cx:-59,cy:17,r:13,fill:ink}),n('circle',{cx:59,cy:17,r:13,fill:ink})],'Municipal wheeled delivery cart');robot('shell',880,398,.62);
  shape('hood',880,405,[n('path',{d:'M-63 66V-54Q0 -91 63 -54V66Z',fill:colors.canvas}),path('M-37 -44V65M27 -50V65','#b08b43',2)],'Removable canvas cover');
  a.move('cart',1,697,470,2600);a.move('shell',1,697,398,2600);a.move('hood',1,697,405,2600);a.hide('hood',2);
  
 }else if(index===1){
  shape('room',602,320,[rect(-455,-136,910,325,colors.plaster),rect(126,-101,276,130,'#b9d7d4'),rect(-455,189,910,12,colors.iron)],'Kitchen and window overlooking the exchange water');city('offshore',883,282);a.move('offshore',4,823,282,3600);
  kazi('patient',404,418,.75);robot('waiting-shell',591,457,.48);
  a.person('amina',302,433,{coat:'#698d9a',night:'#698d9a',hair:'#aeb6b0',skin:'#b58866',scale:.5,pose:'open'});
  shape('case',224,488,[rect(-26,-5,52,25,colors.sea,5),path('M-10 -5V-15H10V-5',ink,3)],'Medical case rests on floor');
  for(const node of a.objects.find(o=>o.id==='amina').visual.children){if(node.attrs?.stroke==='$ink')node.attrs.stroke=ink;}
  a.objects.find(o=>o.id==='amina').visual.children=a.objects.find(o=>o.id==='amina').visual.children.filter(n=>!n.attrs?.d?.startsWith('M35 -9'));
  shape('care-hand',328,426,[path('M0 0L34 -9L51 -16','#b58866',7)],'Amina reaches toward Kazi’s wrist, prioritizing the living patient');a.reveal('care-hand',2);
  shape('sink',897,452,[rect(-91,-12,182,17,colors.green),path('M-84 4V55M84 4V55',ink,6),path('M-27 -12V-60Q-27 -79 -6 -79H12V-58',ink,7)],'Kitchen sink and tap');
  shape('cup',909,424,[rect(-17,0,34,22,colors.canvas,4),path('M17 5Q37 4 30 17H17',ink,3)],'Drinking cup rests below tap');
  shape('water',908,416,[rect(-2,-20,4,24,colors.sea)],'Tap fills cup without invented restriction');a.reveal('water',1);a.hide('water',2);
 }else if(index===2){
  shape('table',650,434,[rect(-355,-120,710,215,colors.plaster,12),path('M-330 95V130M330 95V130','$ink',8)],'One shared maintenance record on mediation table');
  a.person('sofia',166,383,{coat:'#697e8b',night:'#a1b5c2',hairStyle:'long',scale:.55,pose:'open'});
  shape('record',647,370,[rect(-265,-80,530,172,'#fff4dc',5),text('Pump maintenance record',0,-45,30,ink),path('M-226 24H226',ink,3),...[[-146,13],[-28,12],[98,14]].map(([x,w])=>rect(x,8,w,32,colors.iron)),text('Repeated events',-118,73,22,ink),text('Brief interruptions',133,73,22,ink)],'Same actual event history supports two differently selected statements');
  shape('events-window',647,377,[...[-146,-28,98].map(x=>path(`M${x-7} -8V-18H${x+22}V-8`,colors.sea,4))],'Three event brackets identify every failure in the same history');
  shape('duration-window',647,377,[...[-146,-28,98].map(x=>path(`M${x} 38V48H${x+13}V38`,colors.iron,4)),text('11 minutes in total',0,106,23,ink)],'Duration reading totals those same three failures; exact chapter figure, no invented risk score');
  a.reveal('events-window',3);a.reveal('duration-window',3);a.hide('events-window',4);a.hide('duration-window',4);
  shape('pump',930,254,[rect(-51,-24,102,48,colors.sea,8),n('circle',{cx:0,cy:0,r:18,fill:colors.canvas}),path('M-82 0H-51M51 0H82',ink,10)],'Physical pump whose service history is being discussed');
 }else{
  shape('book',639,360,[n('path',{d:'M-362 -125Q-170 -158 0 -105Q190 -158 362 -125V166Q177 135 0 178Q-177 135 -362 166Z',fill:colors.plaster,stroke:colors.green,'stroke-width':2}),path('M0 -105V178',colors.green,5)],'Open reading volume with scene at the doorway');
  shape('chapter',444,328,[text('The Man Who',0,-40,31,ink),text('Arrived Twice',0,4,31,ink),path('M-100 46H100M-100 62H84M-100 78H92',colors.green,3)],'Actual opening chapter, not a duplicate slide title');
  house('doorway',779,396,.57);kazi('kazi-return',779,390,.45);robot('shell-return',907,412,.29);
  shape('bookmark',470,483,[n('path',{d:'M-13 -20H13V29L0 18L-13 29Z',fill:colors.iron})],'Bookmark at the opening chapter');a.reveal('bookmark',4);
 }
 if(index===0){const shell=a.objects.find(o=>o.id==='shell');for(const node of shell.visual.children){const attrs={};if(node.attrs.fill===ink)attrs.fill='#9dbabe';if(node.attrs.stroke===ink)attrs.stroke='#9dbabe';if(Object.keys(attrs).length)node.themeAttrs={night:attrs};}}
 return a.finish('Port Nacre household theatre: source-faithful shell, embodied care and two truthful views of one pump record. Draft staging pending final action and layout review.');
}
