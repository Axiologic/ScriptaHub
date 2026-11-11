import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {checkVisualPlan} from '../tools/shf/check-visual-plan-implementation.mjs';
import {scriptHash} from '../tools/shf/marketing-review.mjs';
const root=await fs.mkdtemp('.tmp/visual-plan-');
try{
 await fs.mkdir(root+'/work');
 const scenes=[{id:'example',lines:['A reason supports this conclusion.'],visual:{objects:[{id:'reason'},{id:'claim'}],connections:[{id:'support'}],actions:[{actor:'support',action:'connection.draw',beat:1}]}}];
 const write=async()=>fs.writeFile(root+'/work/scenes.json',JSON.stringify(scenes));
 await write();await fs.writeFile(root+'/work/presentation-plan.json',JSON.stringify({scriptSha256:scriptHash(scenes),scenes:[{sceneId:'example',keep:['reason','claim'],cues:[{line:1,visualAction:'Draw the support relationship.'}]}]}));
 assert.deepEqual((await checkVisualPlan(root)).issues,[]);
 scenes[0].visual.actions[0].actor='absent-relationship';await write();
 assert.ok((await checkVisualPlan(root)).issues.some(i=>i.includes('absent actor')));
 console.log('Connection animation targets validated; missing targets rejected.');
}finally{await fs.rm(root,{recursive:true,force:true})}
