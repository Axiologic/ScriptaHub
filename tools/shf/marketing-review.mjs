import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

export const scriptHash=scenes=>crypto.createHash('sha256')
  .update(JSON.stringify(scenes.map(scene=>({id:scene.id,lines:scene.lines})))).digest('hex');

export async function marketingReview(project, scenes){
  const file=path.join(project,'work/marketing-review.json');
  const review=await fs.readFile(file,'utf8').then(JSON.parse).catch(error=>{
    if(error.code==='ENOENT')return null;
    throw error;
  });
  const hash=scriptHash(scenes);
  const current=review?.version==='curiosity-v2'&&review.scriptSha256===hash;
  const independent=review?.independentReview;
  const approved=current&&independent?.status==='passed'&&independent.scriptSha256===hash;
  return {review,current,approved,scriptSha256:hash};
}

// Review the entire requested batch before allowing even the first synthesis.
export async function requireMarketingBatch(entries){
  const pending=[];
  for(const entry of entries){
    const scenes=JSON.parse(await fs.readFile(path.join(entry.project,'work/scenes.json'),'utf8'));
    const result=await marketingReview(entry.project,scenes);
    const plan=await fs.readFile(path.join(entry.project,'work/presentation-plan.json'),'utf8').then(JSON.parse).catch(error=>{if(error.code==='ENOENT')return null;throw error;});
    const cuesValid=plan?.scriptSha256===result.scriptSha256&&scenes.every(scene=>{
      const planned=plan.scenes?.find(item=>item.sceneId===scene.id);
      return planned&&scene.lines.every((_,index)=>planned.cues?.some(cue=>cue.line===index+1&&cue.visualAction));
    });
    if(!result.approved||!cuesValid)pending.push(entry.title);
  }
  if(pending.length)throw new Error(`Complete the current marketing script, independent review and every visual cue for all books before voice conversion (${pending.length} pending): ${pending.join(', ')}`);
}
