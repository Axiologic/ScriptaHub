import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);
const human=(id,x,y,coat,identity='person-02-neutral',seated=false,scale=.9)=>{storyPerson(a,id,x,y,{coat,identity,seated,scale,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;for(const [beat,emotion]of [[1,'curious'],[3,'worried'],[5,'skeptical'],[6,'curious']])a.actions.push({actor:id,action:'character.express',emotion,beat,durationMs:850});storyGesture(a,id,2,'question');storyGesture(a,id,4,'reflect');storyGesture(a,id,6,'invite');};

const teal='#248c99',tn='#8ad9df',coral='#d57651',cn='#f3b18e',gold='#d5a62d',gn='#f6d888',violet='#8170b7';
const kitchen=()=>obj('lake-window',606,297,[rect(-375,-144,750,257,teal,tn,16),rect(-355,-125,710,220,'#c8e7df','#335c6a',8),fill('M-355 64Q-146 31 29 68T355 66V95H-355Z','#62b4b8','#78b4c0'),...[-307,-229,-128,92,237].map((x,j)=>rect(x,-3-(j%3)*18,38,69+(j%3)*18,'#8aaea6','#8aaea6',4)),n('circle',{cx:241,cy:-68,r:38,fill:gold})],'Lake Geneva and visible maintenance infrastructure place the requests in an ordinary home');
const table=()=>obj('kitchen-table',621,438,[fill('M-330 -14H329L290 16H-292Z',coral,cn),path('M-262 16V100M264 16V100','$ink',13)],'A shared kitchen surface holds requests that cannot be optimized away');
const kite=(id,x,y)=>obj(id,x,y,[fill('M-42 -184Q0 -198 42 -184L28 -108L41 -49H-40L-26 -107Z',teal,tn),rect(-36,-245,72,57,'#ecddbb','#bed6d0',22),rect(-27,-228,54,15,'#356379','#356379',7),path('M-17 -169L-54 -112L-16 -96M26 -167L60 -134L101 -139',teal,13),path('M-22 -50L-31 -3M24 -50L33 -3','$ink',15),path('M-31 -2H-47M33 -2H49','$ink',10)],'Kite’s narrow folding body and careful hands belong to the household');
const bird=(id,x,y,k=1)=>obj(id,x,y,[fill('M-53 4Q-34 -27 -4 -9Q7 -39 32 -21L55 -9L31 1Q7 36 -28 25L-53 4Z',gold,gn),dot(25,-13,3,'#384958'),path('M-13 24V39M3 25V39',violet,5)],'The wooden bird is a particular household object, not a general technology icon',k);
if(i<2){kitchen();human('narrator',354,531,coral,'person-03-neutral',true,.93);kite('kite',860,517);table();obj('envelope',573,412,[fill('M-68 -28L64 -22L65 32L-70 28Z','#e9d9b5','#d9d6ba'),path('M-65 -24L-2 14L60 -18',violet,3)],'The mother’s handwritten request remains a decision, not a risk score');bird('bird',744,403,.66);a.reveal('envelope',2);a.reveal('bird',4);}
else if(i===2){obj('workbench',611,428,[rect(-357,0,714,26,coral,cn),path('M-298 26V112M296 26V112','$ink',13)],'A real craft bench supports the original and copy');human('maker',359,527,teal,'person-02-neutral',false,.89);for(let j=0;j<2;j++)obj('viola'+j,599+j*211,389,[fill('M-29 37Q-70 14 -44 -18Q-28 -32 -28 -57Q-45 -77 -19 -100H20Q46 -77 28 -57Q28 -32 43 -18Q69 15 28 37Z',j?gold:coral,j?gn:cn),rect(-7,-152,14,152,violet,'#c4b4e4'),path('M-12 -143V19M0 -143V19M12 -143V19','$ink',2)],'A handmade viola and technically superior copy preserve the problem of value');a.reveal('viola1',3);}
else{kitchen();human('narrator',352,530,coral,'person-03-neutral',true,.95);kite('kite',858,518);table();bird('bird',621,406,1);a.move('bird',4,636,406);}

s.visual=a.finish(s.lines[0]+' Original material staging, a richer foreground palette and expressive participants make the particular question visible.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
