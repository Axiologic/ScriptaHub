// Shared book-introduction compiler. Narratives and art direction remain book-owned data.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {storyStage} from './story-stage.mjs';
import {publishNarratedFilm} from './publish-film.mjs';
export async function buildBookFilm(root){
 root=path.resolve(root);const read=file=>JSON.parse(fs.readFileSync(path.join(root,file),'utf8'));const write=(file,value)=>fs.writeFileSync(path.join(root,file),JSON.stringify(value,null,2)+'\n');
 const skill=path.resolve('.agents/skills/shf-presentation-creator');
 const {voiceTasks}=await import(path.join(skill,'scripts/lib/voice.mjs'));const {checkEditorial}=await import(path.join(skill,'scripts/check-editorial.mjs'));
 await import(path.join(skill,'runtime/shf-core.js'));const C=globalThis.SHFCore;
 const production=read('work/production.json'),scenes=read('work/scenes.json'),editorial=read('work/editorial.json'),sections=read('source/sections.json'),source=fs.readFileSync(path.join(root,'source/source.txt'),'utf8');
 const review=checkEditorial(editorial,source);if(!review.valid)throw Error(review.errors.join('\n'));write('qa/editorial-validation.json',review);
 for(const scene of scenes)for(const text of scene.lines)if(C.splitSentences(text,'en').length!==1)throw Error('Expected exactly one sentence: '+scene.id);
 const sourceSha256=crypto.createHash('sha256').update(source).digest('hex');
 const direction={format:'SHF-Direction',version:'0.4',id:production.id,title:production.title,language:'en',stage:{width:1200,height:760},description:editorial.readerInvitation.readerPromise,editorial:{purpose:editorial.purpose,sourceEdition:production.edition,sourceSha256,readerInvitation:editorial.readerInvitation,rights:editorial.rights},sources:sections.map(s=>({id:s.id,title:s.heading,edition:production.edition,locator:'en/full_content.html#'+s.anchor})),assets:{},voice:{id:'en_US-ljspeech-medium',provider:'Piper local CPU'},scenes:scenes.map(storyStage)};
 write('work/film.direction.json',direction);write('work/voice-tasks.json',voiceTasks(direction));
 if(process.argv.includes('--plan-only')){console.log('Validated source, editorial purpose and '+scenes.reduce((n,s)=>n+s.lines.length,0)+' single-sentence beats.');return;}
 if(scenes.some(s=>!s.visual?.objects?.length))throw Error('Every scene needs its authored visual composition.');
 const report=await publishNarratedFilm({direction,root,output:path.resolve(production.bookDirectory,'Animation'),minDurationMs:production.minDurationMs??0,maxDurationMs:production.maxDurationMs??900000});write('qa/build.json',report);return report;
}
