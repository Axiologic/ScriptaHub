import fs from 'node:fs';import path from 'node:path';import {spawnSync} from 'node:child_process';
const skill=path.resolve('.agents/skills/shf-presentation-creator');
const {compileFilm}=await import(skill+'/scripts/lib/director.mjs'),{standalone}=await import(skill+'/scripts/lib/standalone.mjs');
const specs=JSON.parse(fs.readFileSync('.book-work/ai-completion-20261111/film-specs.json'));
for(const spec of specs){const root='presentations/'+spec.slug,result=spawnSync(process.execPath,[root+'/build.mjs','--plan-only'],{encoding:'utf8'});if(result.status)throw Error(result.stderr+result.stdout);const direction=JSON.parse(fs.readFileSync(root+'/work/film.direction.json'));const film=compileFilm(direction);fs.writeFileSync(root+'/qa/visual-draft.html',standalone([film]));console.log(spec.slug,film.durationMs)}
