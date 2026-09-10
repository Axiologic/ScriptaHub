import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#365fb0',B='#c87360',AN='#aac5ff',BN='#f1b6a5';
 const host=(id,x,y,scale=1)=>add(object(id,x,y,[tint(n('rect',{x:-100,y:-110,width:200,height:220,rx:12,fill:A}),AN),...[0,1,2].map(j=>tint(n('rect',{x:-72,y:-78+j*66,width:144,height:40,rx:5,fill:B}),BN))],'A replaceable service provider.',scale));
 const archive=(id,x,y,scale=1)=>add(object(id,x,y,[tint(n('path',{d:'M-90 -65H-15L10 -40H95V95H-90Z',fill:B}),BN),tint(text('Memory',0,30,28,'white'),'#482c26')],'The community’s accumulated archive and relationships.',scale));
 const member=(id,x,y)=>add(object(id,x,y,[tint(dot(0,-23,20,B),BN),tint(n('path',{d:'M-40 45Q-40 0 0 0Q40 0 40 45Z',fill:B}),BN)],'A participant whose social contribution is not owned by a host.'));
 switch(i){
 case 0:
 host('host',950,290);archive('memory',470,290);
 for(let j=0;j<3;j++){member('participant'+j,180,170+j*145);reveal('participant'+j,j+1);}
 add(object('shared-work',285,290,[tint(n('path',{d:'M-32 -48H32V48H-32Z',fill:A}),AN),tint(path('M-18 -18H18M-18 5H18',B,6),BN)],'Participants build a common archive from their contributions.'));reveal('shared-work',2);move('shared-work',3,400,290);hide('shared-work',4);move('memory',4,700,290,2400);
 add(object('rules',950,475,[tint(n('rect',{x:-120,y:-38,width:240,height:76,rx:8,fill:B}),BN),tint(text('Provider rules',0,10,27,'white'),'#482c26')],'The host retains unilateral rule-making power over socially created value.'));reveal('rules',4);break;
 case 1:host('host',600,290,1.1);for(let j=0;j<4;j++){member('m'+j,[280,920,330,870][j],[180,180,460,460][j]);reveal('m'+j,j+1);}archive('archive',280,330,.6);reveal('archive',3);move('archive',4,470,330);break;
 case 2:host('a',270,340,.65);host('b',930,340,.65);archive('memory',350,160,.65);move('memory',3,850,160,3000);add(object('address',600,480,[tint(n('rect',{x:-150,y:-40,width:300,height:80,rx:40,fill:B}),BN),tint(text('Community',0,11,31,'white'),'#482c26')],'A persistent community identity remains distinct from either hosting provider.'));break;
 case 3:
 host('service',690,260,1.1);archive('commons',330,215,.8);
 add(object('workbench',690,405,[tint(path('M-240 0H240M-195 0V110M195 0V110',A,16),AN)],'A working service needs continuing repair and maintenance.'));
 add(object('repair',505,325,[tint(path('M-45 60L35 -35M15 -70Q80 -80 70 -15',B,18),BN)],'Maintainer work supports the service.'));reveal('repair',2);move('repair',3,575,310);
 add(object('discussion',1030,230,[tint(n('path',{d:'M-65 -65H65V40H-10L-45 75V40H-65Z',fill:B}),BN),tint(path('M-35 -25H35M-35 0H10',A,7),AN)],'Moderation and dispute work also require resources.'));reveal('discussion',3);
 add(object('funding',360,455,[tint(n('path',{d:'M-75 -45H75V45H-75Z',fill:B}),BN),tint(path('M-65 -35L0 10L65 -35',A,7),AN)],'Financial support carries dependencies that governance must examine.'));reveal('funding',4);break;
 case 4:add(object('dial',570,295,[tint(n('circle',{cx:0,cy:0,r:120,fill:'none',stroke:A,'stroke-width':22}),AN),tint(path('M0 0L65 -60',B,18),BN),tint(dot(0,0,18,B),BN)],'A user-visible recommendation policy dial.'));label('policy','Recommendation policy',570,500,32);for(let j=0;j<3;j++){member('candidate'+j,970,190+j*120);reveal('candidate'+j,j+1);}add(object('selection',675,245,[tint(dot(0,0,22,B),BN)],'The selected recommendation setting changes when the user revises policy.'));move('selection',3,650,375,1700);break;
 case 5:add(object('gate',650,280,[tint(path('M-70 -100V100M70 -100V100M-70 -90H70',A,16),AN),tint(n('rect',{x:-30,y:-30,width:60,height:60,rx:14,fill:B}),BN)],'A bounded introduction point precedes private communication.'));member('visitor',270,300);move('visitor',3,450,300);archive('private',1000,285,.8);reveal('private',4);break;
 case 6:for(let j=0;j<3;j++)host('host'+j,270+j*330,280,.6);archive('commons',600,490,.6);for(let j=0;j<3;j++)reveal('host'+j,j+1);break;
 case 7:archive('community',600,240,1.3);host('a',240,430,.45);host('b',960,430,.45);reveal('a',2);reveal('b',3);move('community',6,600,310);break;
 }
 s.visual=q.finish('Cobalt and coral network atlas: social memory travels between hosts, recommendation is adjustable, introductions precede private access.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2));
