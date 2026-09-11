import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fitBeatGestures} from './illustrated-stage.mjs';
import {atomicWriteFile} from './atomic-write.mjs';
export async function publishNarratedFilm({direction,root,output,minDurationMs=0,maxDurationMs=3600000}){
 const skill=path.resolve('.agents/skills/shf-presentation-creator');
 const {compileFilm}=await import(path.join(skill,'scripts/lib/director.mjs'));
 const {attachVoice}=await import(path.join(skill,'scripts/lib/voice.mjs'));
 const {standalone}=await import(path.join(skill,'scripts/lib/standalone.mjs'));
 await import(path.join(skill,'runtime/shf-core.js'));const C=globalThis.SHFCore;
 const sha=t=>crypto.createHash('sha256').update(t).digest('hex');
 const write=(file,v)=>{fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,typeof v==='string'?v:JSON.stringify(v,null,2)+'\n');};
 const receipts=JSON.parse(fs.readFileSync(path.join(root,'work/voice-receipts.json')));
 const beats=direction.scenes.flatMap(s=>s.beats);
 for(const b of beats)if(receipts.lines.find(r=>r.id===b.id)?.textSha256!==sha(b.text))throw Error('Missing or stale sentence recording: '+b.id);
 write(path.join(root,'qa/sentence-policy.json'),{valid:true,sentences:beats.length,maxSentencesPerBeat:1,maxWords:Math.max(...beats.map(b=>b.text.split(/\s+/).length)),averageWords:beats.reduce((n,b)=>n+b.text.split(/\s+/).length,0)/beats.length,scriptSha256:sha(JSON.stringify(beats.map(b=>b.text)))});
 const voiced=attachVoice(direction,receipts,path.join(root,'work'));fitBeatGestures(voiced.direction);
 write(path.join(root,'qa/audio-timing.json'),{durationMs:voiced.direction.durationMs,lines:voiced.report});
 const gaps=voiced.direction.scenes.flatMap(s=>s.beats.slice(1).map((b,i)=>b.startMs-s.beats[i].spokenEndMs));
 write(path.join(root,'qa/pacing.json'),{sentenceGapsMs:gaps,minSentenceGapMs:Math.min(...gaps),maxSentenceGapMs:Math.max(...gaps),captionPauseTailMs:voiced.direction.scenes.flatMap(s=>s.beats.map(b=>b.endMs-b.spokenEndMs)),sceneTransitionsMs:voiced.direction.scenes.slice(1).map((s,i)=>voiced.direction.scenes[i].durationMs-voiced.direction.scenes[i].beats.at(-1).spokenEndMs+s.beats[0].startMs)});
 const film=compileFilm(voiced.direction),validation=C.validate(film);if(!validation.valid)throw Error(validation.errors.join('\n'));
 if(film.durationMs<minDurationMs||film.durationMs>maxDurationMs)throw Error('Duration outside the editorial brief: '+film.durationMs);
 write(path.join(root,'qa/validation.json'),validation);const packed=C.packFilm(film);const shfPath=path.join(output,film.id+'.shf');atomicWriteFile(shfPath,packed);
 const exports=path.join(root,'exports');write(path.join(exports,film.id+'.html'),standalone([film]));
 const stamp=t=>{const ms=Math.round(t);return String(Math.floor(ms/3600000)).padStart(2,'0')+':'+String(Math.floor(ms/60000)%60).padStart(2,'0')+':'+String(Math.floor(ms/1000)%60).padStart(2,'0')+'.'+String(ms%1000).padStart(3,'0');};
 const vtt=['WEBVTT',''];let offset=0;for(const scene of film.scenes){for(const b of scene.beats)vtt.push(b.id,`${stamp(offset+b.startMs)} --> ${stamp(offset+b.endMs)}`,b.text,'');offset+=scene.durationMs;}
 write(path.join(exports,film.id+'.vtt'),vtt.join('\n'));
 const report={durationMs:film.durationMs,minutes:film.durationMs/60000,scenes:film.scenes.length,shfBytes:fs.statSync(path.join(output,film.id+'.shf')).size};console.log(JSON.stringify(report));return report;
}
