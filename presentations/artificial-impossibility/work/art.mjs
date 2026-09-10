import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#a76b18',B='#345866',AN='#efc178',BN='#9bced8';
 const gate=(id,x,y,word,open=false)=>{add(object(id,x,y,[tint(n('rect',{x:-100,y:-130,width:30,height:255,fill:B}),BN),tint(n('rect',{x:70,y:-130,width:30,height:255,fill:B}),BN),tint(n('rect',{x:-100,y:-145,width:200,height:25,fill:B}),BN),tint(path(open?'M0 -100L0 60':'M-60 0H60',A,20),AN),text(word,0,177,30)],'A selection gate with a specific institutional mandate.'));};
 const project=(id,x,y,scale=1)=>add(object(id,x,y,[tint(n('path',{d:'M-70 55V-35L0 -85L70 -35V55Z',fill:A}),AN),tint(n('rect',{x:-19,y:1,width:38,height:55,fill:B}),BN)],'An illustrated beneficial project seeking support, not a specific building.',scale));
 const mandate=(id,x,y,word)=>add(object(id,x,y,[tint(n('rect',{x:-110,y:-72,width:220,height:144,rx:7,fill:B}),BN),tint(text(word,0,10,30,'white'),'#132d36')],'A specific sponsor mandate.'));
 switch(i){
 case 0:
 add(object('workbench',420,435,[tint(n('rect',{x:-245,y:-15,width:490,height:28,rx:5,fill:B}),BN),tint(path('M-185 15V95M185 15V95',B,14),BN)],'A repair bench turns useful advice into another working appliance.'));
 add(object('kettle',420,355,[tint(n('path',{d:'M-75 65Q-95 -30 -55 -60H55Q95 -30 75 65Z',fill:A}),AN),tint(path('M60 -35Q150 -55 132 25Q125 58 80 45',B,15),BN),tint(n('path',{d:'M-65 -25L-135 -70L-115 -5L-76 15Z',fill:A}),AN),tint(path('M-50 -75H50M0 -75V-90',B,10),BN)],'A household kettle illustrates the source purchasing assistant choosing repair.'));
 add(object('fault',420,365,[tint(path('M-10 -40L8 -12L-8 13L12 45',B,7),BN)],'A repairable fault.'));
 add(object('tool',610,300,[tint(path('M-40 70L25 -20M10 -55Q80 -85 70 -5',B,16),BN)],'The assistant identifies repair instead of a new sale.'));reveal('tool',3);move('tool',5,470,325);hide('fault',5);hide('tool',6);
 add(object('receipt',940,285,[tint(n('path',{d:'M-80 -125H80V125L60 112L40 125L20 112L0 125L-20 112L-40 125L-60 112L-80 125Z',fill:B}),BN),tint(text('New sale',0,-57,27,'white'),'#17333d'),tint(path('M-42 -20H42M-42 12H25',A,8),AN)],'The sponsor earns revenue from new purchases.'));reveal('receipt',4);
 add(object('no-sale',940,338,[tint(path('M-38 0H38',A,14),AN)],'A successful repair creates no new sale for the sponsor.'));reveal('no-sale',5);
 label('sponsor-label','Purchase revenue',940,490,30);reveal('sponsor-label',4);break;
 case 1:project('p',320,300,1.1);mandate('sponsor',865,280,'More sales');reveal('sponsor',2);add(object('repair',570,280,[tint(path('M-22 -50L23 -5M10 15L-33 58',A,20),AN),tint(n('circle',{cx:35,cy:-40,r:29,fill:'none',stroke:A,'stroke-width':13}),AN)],'Repair avoids another purchase.'));reveal('repair',3);label('repair-label','Repair',570,420);reveal('repair-label',3);break;
 case 2:project('p',600,255,1.3);for(let j=0;j<3;j++){mandate('m'+j,280+j*320,490,['Benefit','Recipients','Mandates'][j]);reveal('m'+j,j+1);}break;
 case 3:
 add(object('test',330,270,[tint(path('M-110 105H100M-70 95V40Q-70 -5 -12 -30',B,15),BN),tint(n('path',{d:'M-20 -110L30 -90L-15 5L-65 -15Z',fill:A}),AN),tint(path('M-25 35H75',B,10),BN),tint(n('path',{d:'M35 35V-10H65V35Z',fill:A}),AN)],'A bounded laboratory experiment cannot run until resources are authorized.'));
 add(object('funding',880,295,[tint(n('rect',{x:-120,y:-70,width:240,height:160,rx:6,fill:B}),BN),tint(path('M-100 -45L0 25L100 -45',A,10),AN)],'Funding remains withheld while the sponsor requests evidence.'));
 add(object('funding-route',600,150,[tint(path('M260 0C170 -55 -170 -55 -260 0M-260 0L-220 3M-260 0L-247 -32',A,9),AN)],'The experiment first requires funding.'));
 add(object('results-route',600,440,[tint(path('M-260 0C-150 55 150 55 260 0M260 0L220 -3M260 0L247 32',A,9),AN)],'Funding first requires the result of that experiment.'));
 label('funding-condition','Funding to test',600,185,29);label('proof-condition','Results to fund',600,540,29);
 label('test-label','Experiment',330,425,29);label('fund-label','Authorization',880,425,29);
 reveal('funding-route',2);reveal('funding-condition',2);reveal('results-route',3);reveal('proof-condition',3);
 add(object('blocked',880,300,[tint(n('circle',{cx:0,cy:0,r:28,fill:A}),AN),tint(path('M-14 0H14',B,8),BN)],'The cycle prevents authorization; validation is not rejected in principle.'));reveal('blocked',3);break;
 case 4:project('commons',600,280,1.25);for(let j=0;j<4;j++){add(object('benefit'+j,260+j*225,490,[tint(dot(0,0,25,j%2?A:B),j%2?AN:BN)],'A distinct beneficiary; positions are conceptual, not data.'));reveal('benefit'+j,j+2);}label('public','Shared infrastructure',600,160,30);break;
 case 5:gate('rights',600,290,'Due process');project('project',260,310,.9);add(object('shield',930,290,[tint(n('path',{d:'M-65 -70Q0 -35 65 -70V15Q40 75 0 95Q-40 75 -65 15Z',fill:A}),AN)],'A protective boundary can deserve preservation.'));reveal('shield',3);move('project',4,365,310,1800);break;
 case 6:mandate('smooth',350,270,'Easy story');project('p',870,280);add(object('missing',600,400,[tint(path('M-60 0H-20M20 0H60',A,10),AN)],'The missing relationship in a polished explanation.'));label('relation','Missing relationship',600,500,30);reveal('missing',2);reveal('relation',2);move('smooth',4,260,270);move('p',4,940,280);break;
 case 7:gate('old',870,270,'Selection');q.objects.at(-1).visual.children.at(-1).attrs.y=230;project('p',340,280,1.1);add(object('route',600,410,[tint(path('M-180 20Q0 110 240 0M240 0L210 -5M240 0L220 25',A,9),AN)],'Reviewing the selection environment can reveal another route, without guaranteeing approval.'));reveal('route',5);break;
 }
 s.visual=q.finish('Amber architectural section theatre; project, mandate and protective gate remain distinct narrative objects.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2));
