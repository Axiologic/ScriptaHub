#!/usr/bin/env node
// Editorial guardrails for the deliberately concise public book-introduction films.
import fs from 'node:fs/promises';
import path from 'node:path';
import {marketingReview} from './marketing-review.mjs';

await import(path.resolve('.agents/skills/shf-presentation-creator/runtime/shf-core.js'));
const readJson=file=>fs.readFile(file,'utf8').then(JSON.parse);
const exists=file=>fs.access(file).then(()=>true).catch(()=>false);
async function walk(dir,name){const out=[];for(const item of await fs.readdir(dir,{withFileTypes:true})){const file=path.join(dir,item.name);if(item.isDirectory())out.push(...await walk(file,name));else if(item.name===name)out.push(file);}return out;}
async function duration(file){const data=await fs.readFile(file);return (await SHFCore.loadFile(new File([data],path.basename(file)))).durationMs;}
async function projectFor(book){for(const name of await fs.readdir('presentations')){const project=path.join('presentations',name),production=path.join(project,'work/production.json');if(await exists(production)&&path.resolve((await readJson(production)).bookDirectory||'')===path.resolve(book))return project;}return null;}
const issues=[], reviewed=[];
for(const manifestFile of await walk('docs/books','manifest.json')){
 const manifest=await readJson(manifestFile), book=path.dirname(manifestFile);if(!manifest.animation?.shf)continue;
 const shf=path.resolve(book,manifest.animation.shf);if(!await exists(shf))continue;
 const project=await projectFor(book);if(!project){issues.push(`${manifest.title.en}: no presentation project`);continue;}
 const scenes=await readJson(path.join(project,'work/scenes.json')), lines=scenes.flatMap(scene=>scene.lines);
 if(lines.length<7||lines.length>10)issues.push(`${manifest.title.en}: ${lines.length} beats (need 7–10)`);
 const totalWords=lines.join(' ').trim().split(/\s+/).length;
 if(totalWords<70||totalWords>160)issues.push(`${manifest.title.en}: ${totalWords} total words (need 70–160)`);
 for(const line of lines){const words=line.trim().split(/\s+/).filter(Boolean).length;if(words<5||words>24)issues.push(`${manifest.title.en}: ${words} words — ${line}`);if(SHFCore.splitSentences(line,'en').length!==1)issues.push(`${manifest.title.en}: not one sentence — ${line}`);}
 const titleWords=manifest.title.en.toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
 if(!lines.slice(0,2).some(line=>line.toLowerCase().replace(/[^a-z0-9]+/g,' ').includes(titleWords)))issues.push(`${manifest.title.en}: first two sentences do not identify the book title`);
 for(const scene of scenes){
   for(const action of scene.visual?.actions||[])if(!Number.isInteger(action.beat)||action.beat<1||action.beat>scene.lines.length)issues.push(`${manifest.title.en}: action references missing beat ${scene.id}/${action.beat}`);
   for(const [key,values] of Object.entries({pauseAfterMs:scene.pauseAfterMs,states:scene.emotionalPlan?.states,intensities:scene.emotionalPlan?.intensities,voiceDirections:scene.emotionalPlan?.voiceDirections}))if(!Array.isArray(values)||values.length!==scene.lines.length)issues.push(`${manifest.title.en}: ${scene.id} ${key} must match narration`);
 }
 const editorial=await marketingReview(project,scenes);
 if(!editorial.current)issues.push(`${manifest.title.en}: current marketing review missing`);
 if(editorial.review?.title&&editorial.review.title!==manifest.title.en)issues.push(`${manifest.title.en}: review belongs to ${editorial.review.title}`);
 if(process.argv.includes('--require-independent')&&!editorial.approved)issues.push(`${manifest.title.en}: independent review missing or stale`);
 reviewed.push({title:manifest.title.en,beats:lines.length,words:lines.reduce((n,line)=>n+line.trim().split(/\s+/).filter(Boolean).length,0)});
}
console.log(JSON.stringify({reviewed:reviewed.length,issues,films:reviewed},null,2));
if(issues.length)process.exitCode=1;
