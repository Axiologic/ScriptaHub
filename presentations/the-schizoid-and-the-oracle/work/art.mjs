import fs from 'node:fs';import {stageAuthor} from '../../../tools/shf/stage-authoring.mjs';import {storyPerson,storyGesture} from '../../../tools/shf/people-poses.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries()){
const a=stageAuthor(),{n,path,text,tint,dot}=a;
const obj=(id,x,y,kids,meaning,k=1)=>a.add(a.object(id,x,y,kids,meaning,k));
const fill=(d,c,cn)=>tint(n('path',{d,fill:c}),cn||c);
const rect=(x,y,w,h,c,cn,rx=0)=>tint(n('rect',{x,y,width:w,height:h,rx,fill:c}),cn||c);
const human=(id,x,y,coat,identity='person-02-neutral',seated=false,scale=.9)=>{storyPerson(a,id,x,y,{coat,identity,seated,scale,chair:coat});a.objects.at(-1).options.dynamicExpressions=true;for(const [beat,emotion]of [[1,'curious'],[3,'worried'],[5,'skeptical'],[6,'curious']])a.actions.push({actor:id,action:'character.express',emotion,beat,durationMs:850});storyGesture(a,id,2,'question');storyGesture(a,id,4,'reflect');storyGesture(a,id,6,'invite');};

const coral='#d86b67',cn='#f1b0a7',teal='#258e9d',tn='#9edce4',gold='#e6b445',gn='#f6d78d',violet='#7b65b0';
const doorway=()=>obj('public-doorway',390,340,[fill('M-131 180V-149L0 -210L131 -149V180H99V-128L0 -173L-99 -128V180Z',coral,cn),path('M-157 184H155',gold,18)],'A public learning entrance raises a question about formation rather than hidden superior doctrine');
if(i===0||i===1){doorway();human('learner',588,535,teal,'person-03-neutral',false,.96);obj('answer-terminal',910,344,[rect(-108,-144,216,266,teal,tn,25),rect(-82,-117,164,196,'#efe2c3','#354f65',11),text('An answer',0,-51,31),path('M-55 -12H54M-55 17H31M-55 47H46',violet,5),path('M0 123V178M-52 180H52',teal,12)],'A ready answer does not supply the capacity to judge its scope');a.reveal('answer-terminal',3);}
else if(i===2){obj('assembly-floor',606,463,[fill('M-389 11Q0 -173 389 11L333 64Q0 -74 -333 64Z',teal,tn)],'An assembly’s seats leave a real entrance for a dissenting participant');human('speaker',604,521,coral,'person-02-neutral',false,.94);human('critic',306,541,gold,'person-03-neutral',false,.88);human('participant',908,541,violet,'person-01-neutral',false,.88);obj('open-path',613,520,[path('M-62 18Q-108 63 -143 72',gold,18)],'The framework needs an accessible route for criticism, not merely fluent interpreters');a.reveal('critic',3);}
else{doorway();obj('working-essay',847,428,[fill('M-182 -82L20 -106L176 -55L152 116L-13 78L-159 105Z',teal,tn),fill('M-154 -65L9 -83V59L-136 81Z','#f0e2c0','#cbd6c4'),fill('M28 -79L148 -40L130 87L28 56Z','#e7d4ae','#c5d1c4'),path('M-123 -30H-18M-121 -2H-25M49 -23L115 -6M49 6L112 21',violet,4)],'An open argument is available for use and criticism');human('reader',574,538,gold,'person-03-neutral',false,.96);}

s.visual=a.finish(s.lines[0]+' Original material staging, a richer foreground palette and expressive participants make the particular question visible.');}
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
