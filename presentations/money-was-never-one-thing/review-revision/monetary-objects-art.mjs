import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
export function monetaryArt(i){
 const q=stageAuthor(),{n,path,text,object,add,label,reveal,hide,move,person}=q;
 const A='#82495d',B='#317b78',ink='#293e49',cream='#f6ead4',wood='#be946e',gold='#d5a34a';
 const o=(id,x,y,nodes,meaning,scale=1)=>add(object(id,x,y,nodes,meaning,scale));
 const card=(id,x,y,name='Bank deposit',scale=1)=>o(id,x,y,[n('rect',{x:-98,y:-58,width:196,height:116,rx:10,fill:A}),n('rect',{x:-98,y:-27,width:196,height:18,fill:'#b897a5'}),text(name,0,27,24,'#fffdf6')],name+' is an institutional claim, not a universal guarantee.',scale);
 const ticket=(id,x,y,scale=1)=>o(id,x,y,[n('path',{d:'M-120 -53H120V-16Q101 0 120 16V53H-120V16Q-101 0 -120 -16Z',fill:cream}),path('M48 -36V36',A,2),text('Flight points',-20,-10,24,ink),text('Travel use',-20,25,21,B),path('M67 -5H97M78 -20L88 -5L78 10',B,4)],'Company-governed travel claim, illustrated without a real airline brand.',scale);
 const slip=(id,x,y,title,sub='',scale=1)=>o(id,x,y,[n('path',{d:'M-120 -60H120V57L100 48L80 57L60 48L40 57L20 48L0 57L-20 48L-40 57L-60 48L-80 57L-100 48L-120 57Z',fill:cream}),text(title,0,-19,25,ink),...(sub?[text(sub,0,17,20,B)]:[]),path('M-72 35H72',A,3)],title,scale);
 const wallet=(id,x,y,scale=1)=>o(id,x,y,[n('path',{d:'M-130 -78H105V-38H136V93H-130Z',fill:A}),n('rect',{x:55,y:-7,width:97,height:52,rx:6,fill:B}),n('circle',{cx:80,cy:19,r:7,fill:gold})],'A wallet holds claims with different permissions and acceptance.',scale);
 const surface=(id,x,y,width=700)=>o(id,x,y,[path(`M${-width/2} 0H${width/2}`,wood,14),path(`M${-width/2+32} 8V58M${width/2-32} 8V58`,'$ink',8)],'A real work surface supports the objects.');
 const laptop=(id,x,y,title)=>o(id,x,y,[n('rect',{x:-143,y:-100,width:286,height:178,rx:10,fill:ink}),n('rect',{x:-128,y:-85,width:256,height:148,fill:'#d6e8df'}),text(title,0,-47,26,ink),path('M-100 -18H100M-100 4H60M-100 26H80',B,5),n('path',{d:'M-143 78H143L180 108H-180Z',fill:'#718b92'})],title+' is conceptual rather than a deployed product.');
 const store=(id,x,y,name)=>o(id,x,y,[n('path',{d:'M-116 -72H116V102H-116Z',fill:cream}),n('path',{d:'M-126 -72H126L108 -111H-108Z',fill:B}),text(name,0,-39,24,ink),n('rect',{x:-84,y:-18,width:83,height:73,fill:'#aed3cd'}),n('rect',{x:28,y:-18,width:55,height:120,fill:wood})],name+' has real goods or services behind the payment.',.85);
 switch(i){
 case 0:
  surface('counter',650,453,680);person('merchant',1080,418,{coat:B,night:'#76b6a9',scale:.6});
  o('lunch',610,393,[n('ellipse',{cx:0,cy:15,rx:95,ry:16,fill:'#d9e2d9'}),n('path',{d:'M-60 2Q0 -56 60 2Z',fill:gold}),path('M-50 8H52',B,7)],'A lunch makes acceptance a concrete question.');
  wallet('wallet',254,377,.8);card('deposit',260,219);ticket('points',630,180);reveal('deposit',2);reveal('points',2);
  move('deposit',3,500,350);slip('accepted',815,315,'Lunch payment','Bank currency');reveal('accepted',3);
  move('points',5,265,220);hide('accepted',5);slip('rules',676,198,'Different promises','Who sets the rules?');reveal('rules',5);break;
 case 1:
  card('balance',269,281,'Bank deposit',1.05);ticket('travel',910,277,1.05);
  slip('issuer',269,451,'Bank issuer','Redemption terms');slip('company',910,451,'Company issuer','Travel conditions');reveal('issuer',2);reveal('company',2);
  o('gate',605,298,[path('M-90 112V-116H90V112','$ink',10),path('M-87 22H50',B,9),n('circle',{cx:50,cy:22,r:12,fill:gold})],'A travel gate makes a claim acceptance boundary visible.');reveal('gate',3);
  move('travel',3,780,287);label('question','What can the holder demand?',600,124,30);reveal('question',3);
  label('stress','If the promise fails, who bears the loss?',600,551,27);reveal('stress',5);break;
 case 3:
  surface('archive-table',600,465,900);
  o('metal',264,366,[n('ellipse',{cx:0,cy:36,rx:69,ry:21,fill:'#957449'}),n('rect',{x:-69,y:-5,width:138,height:42,fill:gold}),n('ellipse',{cx:0,cy:-5,rx:69,ry:21,fill:'#e0ba76'}),path('M-40 21H41','#957449',4)],'Commodity traditions concern material, standards and acceptance, not a universal first money.');
  o('ledger',603,343,[n('path',{d:'M-133 -87Q-60 -112 0 -77Q72 -112 133 -87V110Q65 87 0 121Q-65 87 -133 110Z',fill:cream}),path('M0 -77V115',A,3),text('A promise',-62,-34,23,ink),text('Recorded',64,-34,23,ink),path('M-111 -8H-20M-111 16H-32M22 -8H108M22 16H84',B,4)],'Recorded obligations express a different monetary relation.');reveal('ledger',2);
  slip('tax',940,340,'Public account','Taxes · settlement',.95);reveal('tax',3);
  label('plural','Overlapping traditions',600,144,32);reveal('plural',4);
  label('purpose','Different problems, different rules',600,555,27);reveal('purpose',6);break;
 case 4:
  surface('custody-table',635,473,800);laptop('code',415,331,'Programmed transfer');
  o('key',914,371,[n('rect',{x:-72,y:-22,width:144,height:47,rx:10,fill:A}),n('rect',{x:72,y:-13,width:34,height:29,fill:'#83959a'}),n('rect',{x:-47,y:-9,width:58,height:20,fill:'#d6e8df'})],'A hardware signing device adds a manufacturer and custody relationship.');reveal('key',2);
  label('device','Who controls the key?',927,291,25);reveal('device',3);
  slip('govern',439,168,'Code changes','Who authorizes them?');reveal('govern',4);
  slip('custody',930,153,'Exchange custody','Whose promise?');reveal('custody',5);
  label('trust','Reliance moves with the design',630,550,28);reveal('trust',6);break;
 case 5:
  store('local',230,313,'Local member');store('outside',981,313,'External supplier');
  slip('local-order',238,475,'Member order','Accepted here',.8);reveal('local-order',1);
  o('gateway',605,330,[n('rect',{x:-95,y:-132,width:190,height:212,rx:9,fill:ink}),n('rect',{x:-80,y:-115,width:160,height:167,fill:'#d6e8df'}),text('Convert',0,-66,27,ink),path('M-45 -19H45M22 -42L45 -19L22 3',B,7),n('rect',{x:-40,y:20,width:80,height:11,fill:ink})],'A conversion gateway connects otherwise different acceptance domains.');reveal('gateway',2);
  slip('conversion',605,472,'Conversion request','Outside payment',.8);reveal('conversion',2);move('conversion',3,640,173);
  hide('conversion',4);slip('unavailable',605,145,'Unavailable','Gateway failure',.8);reveal('unavailable',4);
  label('outside-wait','Outside order waits',970,508,25);reveal('outside-wait',4);
  label('local-remains','Member trade can remain local',306,551,24);reveal('local-remains',5);
  break;
 case 6:
  wallet('wallet',203,366,.8);
  o('router',604,324,[n('rect',{x:-136,y:-164,width:272,height:330,rx:20,fill:ink}),n('rect',{x:-119,y:-141,width:238,height:281,rx:4,fill:'#d6e8df'}),text('Payment assistant',0,-99,25,ink),text('Choose a route',0,111,22,ink)],'A proposed personal routing interface selects among claims under chosen objectives.');
  card('bank',994,190,'Bank currency',.8);ticket('points',995,328,.72);slip('local',995,458,'Local credit','Member network',.72);reveal('bank',2);reveal('points',2);reveal('local',2);
  o('fee',604,294,[text('Lowest fee?',0,0,23,ink)],'A possible routing objective, not a measured fee');reveal('fee',3);o('retention',604,350,[text('Keep value local?',0,0,23,ink)],'An alternative routing objective');reveal('retention',4);
  label('objective','Who chooses the objective?',605,550,29);reveal('objective',5);
  move('bank',6,979,190);break;
 case 7:
  surface('reading-table',600,487,850);
  o('book',600,339,[n('path',{d:'M-246 -126Q-117 -157 0 -108Q128 -157 246 -126V124Q131 91 0 140Q-126 91 -246 124Z',fill:cream}),path('M0 -108V135',A,3),text('Design grammar',-124,-76,29,ink),text('Under stress',127,-76,29,ink),text('Purpose',-125,-23,23,B),text('Acceptance',-125,16,23,B),text('Governance',-125,55,23,B),text('Which promise?',125,-23,23,B),text('Whose loss?',125,16,23,B)],'The reading route compares governing rules and failure conditions in the actual book.');
  ticket('ticket',220,216,.55);reveal('ticket',2);card('deposit',990,220,'Bank deposit',.65);reveal('deposit',2);
  break;
 default:throw Error('Unsupported money scene '+i);
 }
 return q.finish('Monetary objects and their actual use: lunch acceptance, travel gate, archival obligations, code and custody, interrupted conversion, routing objectives and a comparative reading surface. Conceptual examples, not historical transaction data or product guarantees.');
}
