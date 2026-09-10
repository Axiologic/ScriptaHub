import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);
const human=(id,x,y,coat,identity='person-02-neutral',seated=false,scale=.9)=>{storyPerson(a,id,x,y,{coat,identity,seated,scale,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;for(const [beat,emotion]of [[1,'curious'],[3,'worried'],[5,'skeptical'],[6,'curious']])a.actions.push({actor:id,action:'character.express',emotion,beat,durationMs:850});storyGesture(a,id,2,'question');storyGesture(a,id,4,'reflect');storyGesture(a,id,6,'invite');};

const teal='#3a8998',tn='#a8d8df',coral='#d9785a',cn='#f1b7a0',gold='#e0b246',gn='#f4d794',violet='#8170b1';
const desk=()=>obj('office-desk',612,452,[fill('M-348 -18H346L318 15H-323Z',teal,tn),path('M-286 15V102M286 15V102','$ink',13)],'An ordinary office supplies the emotional pressure of an unending procedure');
const trays=(id,x,y,count)=>obj(id,x,y,Array.from({length:count},(_,j)=>[fill(`M-88 ${26-j*30}H88L68 ${44-j*30}H-71Z`,j%2?gold:coral,j%2?gn:cn),rect(-70,10-j*30,140,18,'#ebdfbf','#d3d6bd',2)]).flat(),'Successive review layers multiply the work without removing the original obligation');
if(i<2){human('worker',365,548,coral,'person-02-neutral',true,1);desk();trays('review-trays',768,396,i===0?4:7);obj('clock',924,230,[n('circle',{cx:0,cy:0,r:61,fill:gold}),path('M0 -37V0H-36',teal,7),text('09:00',0,105,36)],'Nine o’clock approaches independently of the value of the meeting');a.reveal('clock',3);if(i===1){obj('extra-tray',770,181,[fill('M-88 26H88L68 44H-71Z',violet,'#c4b9e1'),rect(-70,10,140,18,'#ebdfbf','#d3d6bd',2)],'A new evaluation becomes another layer');a.reveal('extra-tray',4);}}
else if(i===2){obj('removable-system',412,346,[rect(-170,-165,340,321,teal,tn,8),...[-113,51].map((y,j)=>[rect(-138,y,276,49,gold,gn,7),text(['Care','Water'][j],0,y+33,30,'#294f5b')]).flat()],'Specific institutional functions can be examined without treating everyone’s support as disposable');obj('old-procedure',412,346,[rect(-138,-31,276,49,coral,cn,7),text('Old procedure',0,2,30,'#294f5b')],'A specific obsolete layer can end while care and water remain');a.hide('old-procedure',4);obj('retired-procedure',615,442,[rect(-85,-33,170,66,coral,cn,7),text('Retired',0,10,32,'#294f5b')],'The question concerns ending a procedure while maintaining essential life');a.reveal('retired-procedure',4);human('resident',899,535,gold,'person-03-neutral',false,1);}
else{human('worker',365,548,coral,'person-02-neutral',true,1);desk();trays('remaining-work',799,411,2);obj('window',801,252,[rect(-150,-100,300,148,teal,tn,12),rect(-129,-79,258,107,'#bae1d5','#476b75',5),dot(74,-29,30,gold)],'The next day is still inhabited; ending institutions is not ending their people');a.reveal('window',3);}

s.visual=a.finish(s.lines[0]+' Original material staging, a richer foreground palette and expressive participants make the particular question visible.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
