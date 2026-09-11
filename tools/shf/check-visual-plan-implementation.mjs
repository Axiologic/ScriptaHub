import fs from 'node:fs/promises';
import path from 'node:path';
import {scriptHash} from './marketing-review.mjs';

// Structural evidence only: semantic correspondence and visual quality still
// require inspection of the rendered scenes against each approved sentence cue.
export async function checkVisualPlan(project){
  const scenes=JSON.parse(await fs.readFile(path.join(project,'work/scenes.json'),'utf8'));
  const plan=JSON.parse(await fs.readFile(path.join(project,'work/presentation-plan.json'),'utf8'));
  const issues=[];
  if(plan.scriptSha256!==scriptHash(scenes))issues.push('Plan does not match current narration');
  for(const scene of scenes){
    const expected=plan.scenes.find(item=>item.sceneId===scene.id);
    if(!expected){issues.push(`${scene.id}: missing approved scene plan`);continue;}
    const objects=scene.visual?.objects||[];
    const ids=new Set(objects.map(object=>object.id));
    const actions=scene.visual?.actions||[];
    if(!objects.length)issues.push(`${scene.id}: no artwork`);
    for(const id of expected.remove||[])if(ids.has(id))issues.push(`${scene.id}: actor ${id} was planned for removal but remains`);
    for(const id of expected.keep||[])if(!ids.has(id))issues.push(`${scene.id}: planned retained actor ${id} is missing`);
    for(const action of actions){
      if(!Number.isInteger(action.beat)||action.beat<1||action.beat>scene.lines.length)issues.push(`${scene.id}: invalid action beat ${action.beat}`);
      if(action.actor&&!ids.has(action.actor))issues.push(`${scene.id}: action targets absent actor ${action.actor}`);
    }
    for(let line=1;line<=scene.lines.length;line++){
      if(!expected.cues?.some(cue=>cue.line===line&&cue.visualAction))issues.push(`${scene.id}: missing sentence ${line} visual cue`);
      if(!actions.some(action=>action.beat===line))issues.push(`${scene.id}: sentence ${line} has no staged action; verify deliberate stillness against its plan`);
    }
  }
  return {project,scriptSha256:scriptHash(scenes),issues,scope:'Actor retention/removal and sentence-action references only; does not certify artistic or semantic quality.'};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(import.meta.filename)){
  const projects=process.argv.slice(2);
  if(!projects.length)throw Error('Provide one or more presentation project directories');
  const reports=await Promise.all(projects.map(checkVisualPlan));
  console.log(JSON.stringify(reports,null,2));
  if(reports.some(report=>report.issues.length))process.exitCode=1;
}
