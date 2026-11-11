import fs from 'node:fs';import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
function update(slug,callback){const root='presentations/'+slug,scenes=JSON.parse(fs.readFileSync(root+'/work/scenes.json'));callback(scenes);fs.writeFileSync(root+'/work/scenes.json',JSON.stringify(scenes,null,2)+'\n');const plan=JSON.parse(fs.readFileSync(root+'/work/presentation-plan.json'));for(const scene of scenes)plan.scenes.find(s=>s.sceneId===scene.id).keep=scene.visual.objects.map(o=>o.id);fs.writeFileSync(root+'/work/presentation-plan.json',JSON.stringify(plan,null,2)+'\n')}
update('meaning-as-a-path',scenes=>{const icon=scenes[1].visual.objects.find(o=>o.id==='item-0'),children=icon.visual.children;icon.visual.children=children.filter(n=>n.type!=='circle');icon.visual.children.push({id:'$asset.example-utterance',type:'text',attrs:{x:0,y:0,'font-size':18,'font-weight':600,'text-anchor':'middle',fill:'#183a41'},text:'Send the sample'});});
update('sleeper-agents-the-risks-of-deceptive-ais',scenes=>{const children=scenes[1].visual.objects.find(o=>o.id==='item-1').visual.children;children.find(n=>n.type==='circle').attrs.cx=44;children.find(n=>n.type==='path').attrs.d='M-52 0H-10';});
update('world-as-a-system',scenes=>{
 const s=stageAuthor(),scene=scenes[1];
 for(const [id,x,name]of [['cedar',240,'Cedar'],['pine',600,'Pine'],['alder',960,'Alder']]){const value=s.object(id,x,250,[s.n('circle',{r:28,fill:'#537b65'})],name);value.visual.anchors={left:[-28,0],right:[28,0],top:[0,-28],bottom:[0,28]};s.add(value);s.label(id+'-name',name,x,320,30);s.reveal(id,1);s.reveal(id+'-name',1);}
 s.link('first-east','cedar','pine',1,'One unit east.');s.link('second-east','pine','alder',1,'One more unit east.');
 s.label('first-unit','+1 east',420,205,26);s.label('second-unit','+1 east',780,205,26);s.reveal('first-unit',1);s.reveal('second-unit',1);
 s.label('sum','1 + 1 = 2',600,450,46);s.reveal('sum',2);s.label('result','Two steps east',950,460,29);s.reveal('result',2);
 const museum=s.object('museum',245,470,[s.n('path',{d:'M-75-25L0-65L75-25Z',fill:'#a36a38'}),s.path('M-80 60H80M-50-15V60M0-15V60M50-15V60','#537b65',8)],'A museum fact does not alter the given coordinates.',.6);s.add(museum);s.label('museum-note','Irrelevant museum fact',245,555,23);s.reveal('museum',3);s.reveal('museum-note',3);
 scene.visual=s.finish('The source’s Cedar → Pine → Alder case: compose two eastward moves, keep the unrelated museum outside the coordinate calculation.');
});
console.log('Added a literal incomplete instruction, an active trigger, and a worked two-move map. Narration unchanged.');
