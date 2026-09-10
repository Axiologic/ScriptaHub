import fs from 'node:fs/promises';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
export async function renderNarration(projectRoot){
const root=path.resolve(projectRoot);
const production=JSON.parse(await fs.readFile(path.join(root,'work/production.json'),'utf8').catch(()=>JSON.stringify({id:path.basename(root),title:'Narrated presentation'})));
const skill=path.resolve('.agents/skills/theatrical-audio');
const { render, auditBundle }=await import(path.join(skill,'src/render.mjs'));
const scenes=JSON.parse(await fs.readFile(path.join(root,'work/scenes.json'),'utf8'));
const segmenter=new Intl.Segmenter('en',{granularity:'sentence'});
const planCheck=spawnSync(process.execPath,[path.join(root,'build.mjs'),'--plan-only'],{encoding:'utf8'});
if(planCheck.status!==0)throw Error('Editorial preflight failed before audio generation: '+planCheck.stderr+planCheck.stdout);
console.log(planCheck.stdout.trim());
const beats=scenes.flatMap(s=>s.lines.map((text,i)=>{
 if([...segmenter.segment(text)].filter(s=>s.segment.trim()).length!==1)throw Error('One sentence per spoken beat is required: '+s.id);
 return {id:s.id+'-line-'+(i+1),type:'speech',speaker:'narrator',text,direction:{pace:production.voicePace??1}};
}));
const audioDir=path.join(root,'work/audio');await fs.mkdir(audioDir,{recursive:true});
console.log('Preparing',beats.length,'single-sentence clips in bounded batches; no audio playback.');
const results=[];
for(let offset=0;offset<beats.length;offset+=16){
 const id=production.id+'-batch-'+(offset/16+1);
 const score={format:'theatrical-audio/1',id,title:production.title,language:'en',voices:{narrator:{label:'Narrator',piperVoice:'en_US-ljspeech-medium'}},settings:{sampleRate:24000,tailSeconds:0},beats:beats.slice(offset,offset+16)};
 const scorePath=path.join(root,'work/scores',id+'.json');await fs.mkdir(path.dirname(scorePath),{recursive:true});await fs.writeFile(scorePath,JSON.stringify(score,null,2)+'\n');
 const out=path.join(root,'work/voice-bundles',id);
 const result=await render(scorePath,{engine:'piper',offline:true,'allow-degraded':true,'no-audition':true,out,cache:path.join(root,'work/voice-cache')});
 await auditBundle(out);results.push({result,out});console.log('Prepared',id);
}
const receipts={format:'SHF-VoiceReceipts',version:'1',provider:'local Piper 1.4.2 / en_US-ljspeech-medium',lines:[]};
const hash=b=>createHash('sha256').update(b).digest('hex');
for(const {result,out} of results)for(const e of result.timeline.events.filter(e=>e.kind==='speech')){
 const a=result.timeline.assets[e.dryAsset],dest=path.join(audioDir,e.id+'.mp3'),beat=beats.find(b=>b.id===e.id);
 const ff=spawnSync('ffmpeg',['-v','error','-y','-i',path.join(out,a.file),'-af',`atempo=${production.voiceTempo??1},alimiter=limit=0.95:level=false`,'-codec:a','libmp3lame','-b:a','64k',dest],{encoding:'utf8'});if(ff.status!==0)throw Error(ff.stderr);
 receipts.lines.push({id:e.id,file:'audio/'+e.id+'.mp3',sha256:hash(await fs.readFile(dest)),textSha256:hash(beat.text),voiceId:'en_US-ljspeech-medium',processing:`Piper pace ${production.voicePace??1}; ffmpeg atempo ${production.voiceTempo??1}; peak limiter 0.95; MP3 64 kbps`,quality:'requires-listening-review',alignmentQuality:'sentence-only',rights:'Source adaptation authorized by project editor. Piper model card identifies its training dataset as public domain; see qa/voice-model-card.txt.'});
}
await fs.writeFile(path.join(root,'work/voice-receipts.json'),JSON.stringify(receipts,null,2)+'\n');
await fs.writeFile(path.join(root,'qa/voice-render.json'),JSON.stringify({durationSeconds:results.reduce((n,{result})=>n+result.timeline.durationSeconds,0),batches:results.map(({result})=>result.evidence),sentences:beats.length,playback:false},null,2)+'\n');
console.log('Rendered',receipts.lines.length,'sentences; measured speech seconds:',results.reduce((n,{result})=>n+result.timeline.durationSeconds,0));

}
