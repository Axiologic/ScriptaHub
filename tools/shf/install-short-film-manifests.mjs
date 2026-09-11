import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const plans=JSON.parse(fs.readFileSync(path.join(root,'.book-work/intake-20260911/short-film-plans.json'),'utf8'));
for(const plan of plans){
 const project=path.join(root,'presentations',plan.slug);
 const production=JSON.parse(fs.readFileSync(path.join(project,'work/production.json'),'utf8'));
 const timing=JSON.parse(fs.readFileSync(path.join(project,'qa/audio-timing.json'),'utf8'));
 const manifestPath=path.join(root,'docs',plan.directory,'manifest.json');
 const manifest=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
 manifest.animation={page:'Animation/index.html',shf:`Animation/${production.filmId}.shf`,language:'en',edition:production.edition,durationMs:timing.durationMs,status:'preview'};
 fs.writeFileSync(manifestPath,JSON.stringify(manifest,null,2)+'\n');
 console.log(plan.title,timing.durationMs);
}
