import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
 const q=stageAuthor(),{n,tint,path,text,dot,object,add,reveal,hide,move,label}=q,A='#344e77',B='#bc5f49',AN='#a9c6ef',BN='#f3ae94';
 const person=(id,x,y,scale=1)=>{add({id,asset:(id==='other'||id==='b')?'person-09-neutral':'person-04-neutral',x,y,scale,options:{color:B,coat:(id==='other'||id==='b')?A:B,dynamicExpressions:true},meaning:'A capable builder; positions illustrate participation, not statistical samples.'});for(const b of (i<2?[1,3,5,7]:i<5?[1,4,7]:[2,5,7])){q.actions.push({actor:id,action:'character.express',beat:b,emotion:['curious','worried','skeptical','determined','relieved','neutral','curious'][b-1],durationMs:500});q.actions.push({actor:id,action:'character.gesture',beat:b,gesture:['question','reflect','recoil','resolve','release','explain','invite'][b-1],offsetMs:650,durationMs:2200});}};
 const bench=(id,x,y)=>add(object(id,x,y,[tint(n('rect',{x:-180,y:-12,width:360,height:35,rx:6,fill:A}),AN),tint(path('M-145 20V110M145 20V110',A,19),AN)],'A common workbench represents reusable institutional work.'));
 const tool=(id,x,y,scale=1)=>add(object(id,x,y,[tint(path('M-45 65L35 -25M15 -65Q90 -90 75 -10',B,20),BN)],'A reusable working resource, not a branded product.',scale));
 const name=(id,x,y)=>add(object(id,x,y,[tint(n('path',{d:'M-135 -60H135V60H-135Z',fill:A}),AN),tint(text('Shared name',0,12,32,'white'),'#233448')],'The common name is a promise governed through enforceable standards.'));
 switch(i){
 case 0:
 person('builder',300,520,.95);bench('individual-work',600,400);tool('effort',560,330,.9);
 add(object('press',975,280,[tint(n('path',{d:'M-95 -125H95V125H-95Z',fill:A}),AN),tint(n('rect',{x:-66,y:-88,width:132,height:90,fill:B}),BN),tint(text('Winner',0,-35,27,'white'),'#512c24'),tint(path('M-60 35H60M-60 65H45M-60 95H55',B,8),BN)],'A public success story selects the winner while overlooking the work outside it.'));
 reveal('press',2);move('effort',3,645,330);add(object('shared-leg',600,470,[tint(path('M0 -50V50',B,16),BN)],'The constructive direction changes what supports entrepreneurial work.'));reveal('shared-leg',5);break;
 case 1:person('visible',880,430,.7);for(let j=0;j<3;j++){person('others'+j,230+j*180,520,.58);reveal('others'+j,j+2);}add(object('spotlight',880,360,[tint(n('ellipse',{cx:0,cy:70,rx:75,ry:15,fill:A}),AN)],'A bounded public stage, not a chart of probabilities.'));break;
 case 2:person('builder',330,490,.86);add(object('belt',600,490,[tint(n('rect',{x:-320,y:-35,width:640,height:70,rx:35,fill:A}),AN),...[-240,-120,0,120,240].map(x=>tint(dot(x,0,15,B),BN))],'A repeated production race can accelerate without changing relative position.'));for(let j=0;j<3;j++){tool('output'+j,650+j*140,310,.55);reveal('output'+j,j+2);move('output'+j,5,520+j*140,310);}break;
 case 3:bench('bench',600,350);tool('tool',550,273);for(let j=0;j<3;j++){label('joint'+j,['Contribution','Reward','Exit'][j],300+j*300,525,30);reveal('joint'+j,j+2);}break;
 case 4:bench('bench',600,365);person('builder',250,530,.85);person('other',950,530,.85);name('name',600,180);reveal('name',3);break;
 case 5:name('name',600,225);add(object('standard',310,425,[tint(n('path',{d:'M-65 -65H65V65H-65Z',fill:B}),BN),tint(path('M-30 0L-5 25L38 -25',A,12),AN)],'Auditable standards make the shared name credible.'));add(object('fork',910,415,[tint(path('M-65 55V0H15M15 0L75 -60M15 0L75 60',A,12),AN)],'Fork and exit remain lawful routes when common governance fails.'));reveal('standard',3);reveal('fork',5);break;
 case 6:for(let j=0;j<3;j++){tool('duplicate'+j,260+j*330,250,.8);reveal('duplicate'+j,j+1);}bench('bench',600,425);reveal('bench',3);move('duplicate0',4,460,361);move('duplicate1',4,600,361);move('duplicate2',4,740,361);break;
 case 7:bench('bench',600,360);tool('shared',600,283);person('a',230,530,.82);person('b',980,530,.82);move('a',5,350,530);move('b',5,850,530);break;
 }
 s.visual=q.finish('Deep blue and vermilion workshop theatre: visible winner, repeated audition, production belt and governed shared workbench.');
}
fs.writeFileSync(file,JSON.stringify(scenes,null,2));
