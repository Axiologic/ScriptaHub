#!/usr/bin/env node
// Keep a durable, verifiable record of the short-film local voice migration.
import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import {marketingReview} from './marketing-review.mjs';
import {narrationDirection,narrationInputHash} from './narration-input.mjs';

const root=process.cwd();
const readJson=file=>fs.readFile(file,'utf8').then(JSON.parse);
const exists=file=>fs.access(file).then(()=>true).catch(()=>false);
const rel=file=>path.relative(root,file).split(path.sep).join('/');
const webRel=file=>path.relative(path.join(root,'docs'),file).split(path.sep).join('/');
const hash=file=>fs.readFile(file).then(data=>crypto.createHash('sha256').update(data).digest('hex'));

async function walk(dir,name){
  const result=[];
  for(const item of await fs.readdir(dir,{withFileTypes:true})){
    const file=path.join(dir,item.name);
    if(item.isDirectory()) result.push(...await walk(file,name));
    else if(item.name===name) result.push(file);
  }
  return result;
}
async function loadFilm(shf){
  await import(path.resolve('.agents/skills/shf-presentation-creator/runtime/shf-core.js'));
  const data=await fs.readFile(shf);
  return SHFCore.loadFile(new File([data],path.basename(shf)));
}
async function loadFilmWithRetry(shf){
  let error;
  for(let attempt=0;attempt<4;attempt++){
    try{return {film:await loadFilm(shf),error:null};}
    catch(caught){
      error=caught;
      if(attempt<3)await new Promise(resolve=>setTimeout(resolve,125*(attempt+1)));
    }
  }
  return {film:null,error};
}
let projectIndex;
async function projectFor(bookDirectory){
  if(!projectIndex)projectIndex=(async()=>{
    const entries=await Promise.all((await fs.readdir('presentations')).map(async name=>{
      const project=path.join('presentations',name),file=path.join(project,'work/production.json');
      if(!await exists(file))return null;
      const production=await readJson(file);
      return production.bookDirectory?[path.resolve(production.bookDirectory),project]:null;
    }));
    return new Map(entries.filter(Boolean));
  })();
  return (await projectIndex).get(path.resolve(bookDirectory))||null;
}
async function hasRenderLock(project){
  const bundles=path.join(project,'work/voice-bundles');
  if(!await exists(bundles)) return false;
  const files=await walk(bundles,'.render.lock');
  for(const file of files){
    try{
      const {pid}=await readJson(file);
      if(!Number.isInteger(pid)||pid<=0)continue;
      const status=await fs.readFile(`/proc/${pid}/status`,'utf8');
      if(!/^State:\s+Z/m.test(status))return true;
    }catch{/* An abandoned lock does not establish an active render. */}
  }
  return false;
}
async function record(manifestFile){
  const manifest=await readJson(manifestFile), bookDirectory=path.dirname(manifestFile);
  if(!manifest.animation?.shf) return null;
  const publicShf=path.resolve(bookDirectory,manifest.animation.shf);
  if(!await exists(publicShf)) return null;
 const loaded=await loadFilmWithRetry(publicShf);
 const project=await projectFor(bookDirectory);
 if(!project) return {title:manifest.title.en,bookId:manifest.id,status:'untracked',bookDirectory:rel(bookDirectory)};
 if(!loaded.film)return {title:manifest.title.en,bookId:manifest.id,status:'publication-invalid',bookDirectory:rel(bookDirectory),project:rel(project),shf:rel(publicShf),publicationError:String(loaded.error?.message||loaded.error||'Unable to read published SHF after retries'),updatedAt:new Date().toISOString()};
 const film=loaded.film;
  const [production, receipts, build, locked]=await Promise.all([
    readJson(path.join(project,'work/production.json')),
    exists(path.join(project,'work/voice-receipts.json')).then(ok=>ok?readJson(path.join(project,'work/voice-receipts.json')):null),
    exists(path.join(project,'qa/build.json')).then(ok=>ok?readJson(path.join(project,'qa/build.json')):null),
    hasRenderLock(project)
  ]);
  const scenes=await readJson(path.join(project,'work/scenes.json'));
  const editorial=await marketingReview(project,scenes);
  const visualPlan=await fs.readFile(path.join(project,'work/presentation-plan.json'),'utf8').then(JSON.parse).catch(error=>{if(error.code==='ENOENT')return null;throw error;});
  const visualPlanCurrent=visualPlan?.scriptSha256===editorial.scriptSha256;
  const state=await fs.readFile(path.join(project,'work/migration-state.json'),'utf8').then(JSON.parse).catch(error=>{if(error.code==='ENOENT')return {stages:{}};throw error;});
  const expectedTexts=scenes.flatMap(scene=>scene.lines).map(text=>crypto.createHash('sha256').update(text).digest('hex'));
  const lines=receipts?.lines||[];
  const filesValid=lines.length>0 && await Promise.all(lines.map(async line=>{
    const audio=path.join(project,'work',line.file);
    return await exists(audio) && await hash(audio)===line.sha256;
  })).then(values=>values.every(Boolean));
  const textCurrent=lines.length===expectedTexts.length && lines.every((line,index)=>line.textSha256===expectedTexts[index]);
  const expectedPerformance=scenes.flatMap(scene=>scene.lines.map((_,index)=>narrationInputHash(narrationDirection(scene,index,production),production)));
  const performanceCurrent=lines.length===expectedPerformance.length&&lines.every((line,index)=>line.performanceSha256===expectedPerformance[index]);
  const publishedBeats=film.scenes.flatMap(scene=>scene.beats||[]);
  const publishedTextCurrent=publishedBeats.length===expectedTexts.length&&publishedBeats.every((beat,index)=>crypto.createHash('sha256').update(beat.text).digest('hex')===expectedTexts[index]);
  const publishedAudioCurrent=lines.length>0&&lines.every(line=>Object.values(film.assets||{}).some(asset=>asset.sha256===line.sha256));
  const voiceGenerated=/Qwen3-TTS/.test(receipts?.provider||'')&&filesValid&&textCurrent&&performanceCurrent;
  const artSha256=crypto.createHash('sha256').update(JSON.stringify(scenes.map(scene=>({id:scene.id,visual:scene.visual})))).digest('hex');
  const visualReview=await fs.readFile(path.join(project,'qa/visual-plan-review.json'),'utf8').then(JSON.parse).catch(error=>{if(error.code==='ENOENT')return null;throw error;});
  const animationCompleted=visualReview?.scriptSha256===editorial.scriptSha256&&visualReview?.artSha256===artSha256&&visualReview?.independentReview?.status==='passed';
  const qwen=/Qwen3-TTS/.test(film.voice?.provider||'') && voiceGenerated && publishedTextCurrent && publishedAudioCurrent && film.durationMs<=120000 && !!build && !locked;
  const piper=/Piper/i.test(receipts?.provider||'');
  const status=qwen?'qwen-complete':locked?'rendering':/Qwen3-TTS/.test(receipts?.provider||'')?'needs-rerender':piper?'pending-piper':'needs-render';
  const stages={
    text:{status:editorial.approved?'reviewed':editorial.current?'awaiting independent review':'rewrite pending'},
    voice:{status:filesValid&&textCurrent&&performanceCurrent?'generated; listening review pending':'generation pending'},
    animation:{status:publishedTextCurrent&&publishedAudioCurrent?'packaged; visual review pending':visualPlanCurrent?'planned; production pending':'visual plan pending'}
  };
  for(const [stage,value] of Object.entries(state.stages||{})){
    if(!stages[stage]||value.scriptSha256!==editorial.scriptSha256)continue;
    if(stage==='text'&&editorial.approved)continue;
    if(value.status==='running'&&value.pid){try{process.kill(value.pid,0);}catch{stages[stage]={...value,status:'interrupted'};continue;}}
    stages[stage]=value;
  }
  const active=Object.values(stages).some(stage=>['running','reviewing','rewriting'].includes(stage.status));
  return {
    title:manifest.title.en, bookId:manifest.id, status, durationMs:film.durationMs,
    stages,active,voiceGenerated,animationCompleted,
    publishedVoice:film.voice?.provider||'Unknown', publishedVoiceId:film.voice?.id||null,
    plannedVoice:production.voiceEngine==='qwen'?production.voiceProvider:null, plannedVoiceId:production.voiceEngine==='qwen'?production.voiceId:null,
    voice:receipts?.provider||production.voiceProvider||null, voiceId:receipts?.lines?.[0]?.voiceId||production.voiceId||null,
    bookDirectory:rel(bookDirectory), project:rel(project), shf:rel(publicShf), shfSha256:await hash(publicShf),
    bookPage:`${webRel(path.join(bookDirectory,'en/book.html'))}?lang=en`, animationPage:manifest.animation.page?webRel(path.resolve(bookDirectory,manifest.animation.page)):null,
    script:scenes.map(scene=>({id:scene.id,title:scene.title,lines:scene.lines,emotions:scene.emotionalPlan?.states||[],intensities:scene.emotionalPlan?.intensities||[],voiceDirections:scene.emotionalPlan?.voiceDirections||[],pausesMs:scene.pauseAfterMs||[]})),
    visualPlan:visualPlanCurrent?visualPlan:null,
    scriptWords:scenes.flatMap(scene=>scene.lines).join(' ').trim().split(/\s+/).length,
    targetDurationMs:120000,
    editorialStatus:editorial.approved?'reviewed':editorial.current?'independent-review-pending':'rewrite-pending',
    editorialReview:editorial.current?{hook:editorial.review.hook,readerPromise:editorial.review.readerPromise,distinctiveContribution:editorial.review.distinctiveContribution,visualPlan:editorial.review.visualPlan,independentReview:editorial.review.independentReview||null}:null,
    presentationPlan:{scenes:scenes.length,beats:expectedTexts.length,visualActions:scenes.reduce((count,scene)=>count+(scene.visual?.actions?.length||0),0),method:'Keep the book-specific visual scenes, retime their movements against the measured concise narration, and rebuild the SHF film.'},
    receiptLines:lines.length, audioReceiptsVerified:filesValid, narrationTextCurrent:textCurrent, publishedTextCurrent, publishedAudioCurrent, updatedAt:new Date().toISOString()
  };
}
async function acquire(lock){
  for(let attempt=0;attempt<120;attempt++) try{return await fs.open(lock,'wx');}catch(error){
    if(error.code!=='EEXIST') throw error;
    await new Promise(resolve=>setTimeout(resolve,250));
  }
  throw new Error(`Timed out waiting for ${lock}`);
}
const lock=path.join('tasks','.voice-migration-progress.lock'), handle=await acquire(lock);
try {
  const entries=(await Promise.all((await walk('docs/books','manifest.json')).map(record))).filter(Boolean).sort((a,b)=>a.title.localeCompare(b.title));
  const counts=Object.fromEntries(['qwen-complete','rendering','pending-piper','needs-render','needs-rerender','publication-invalid','untracked'].map(status=>[status,entries.filter(entry=>entry.status===status).length]));
  const editorialCounts={reviewed:entries.filter(entry=>entry.editorialStatus==='reviewed').length,awaitingReview:entries.filter(entry=>entry.editorialStatus==='independent-review-pending').length,awaitingRewrite:entries.filter(entry=>entry.editorialStatus==='rewrite-pending').length};
  const productionCounts={animations:entries.filter(entry=>entry.animationCompleted).length,voices:entries.filter(entry=>entry.voiceGenerated).length,published:counts['qwen-complete'],publicationInvalid:counts['publication-invalid']};
  const planned=entries.filter(entry=>entry.visualPlan).length;
  const productionPause=await readJson('tasks/production-paused.json').catch(error=>{if(error.code==='ENOENT')return null;throw error;});
  const data={productionPause,format:'ScriptaHub-animation-voice-migration',version:2,updatedAt:new Date().toISOString(),scope:'All book animations: engaging introductions of 1–2 minutes, maximum two minutes.',counts,editorialCounts,productionCounts,visualPlans:planned,conversionGate:editorialCounts.reviewed===entries.length&&planned===entries.length?'plans-reviewed':'all-plans-must-be-reviewed',entries};
  const json=path.join('tasks','voice-migration-progress.json');
  await fs.writeFile(`${json}.${process.pid}.tmp`,JSON.stringify(data,null,2)+'\n');
  await fs.rename(`${json}.${process.pid}.tmp`,json);
  const groups=[['qwen-complete','Voci Qwen finalizate'],['rendering','În conversie'],['pending-piper','Încă pe Piper'],['needs-render','Pregătite pentru conversie'],['needs-rerender','De refăcut după schimbarea textului'],['publication-invalid','Publicare SHF invalidă'],['untracked','Fără proiect asociat']];
  const lines=['# Progres migrare voci pentru animații','',`Actualizat: ${data.updatedAt}`, '', 'Acest registru este sursa de reluare: o intrare este „finalizată” numai când toate fișierele audio Qwen și SHF-ul public curent sunt verificate.', '', '## Situație','',...groups.map(([key,label])=>`- ${label}: **${counts[key]}**`),''];
  for(const [key,label] of groups){const items=entries.filter(entry=>entry.status===key);if(!items.length)continue;lines.push(`## ${label}`,'',...items.map(entry=>`- ${entry.title}${entry.voiceId?` — ${entry.voiceId}`:''}${entry.durationMs?` (${Math.round(entry.durationMs/1000)} s)`:''}`),'');}
  const markdown=path.join('tasks','VOICE-MIGRATION-PROGRESS.md');
  await fs.writeFile(`${markdown}.${process.pid}.tmp`,lines.join('\n'));
  await fs.rename(`${markdown}.${process.pid}.tmp`,markdown);
  const browserData={...data,entries:entries.map(({project,shf,shfSha256,audioReceiptsVerified,narrationTextCurrent,...entry})=>entry)};
  const browserFile=path.join('docs','assets','voice-migration-status.js');
  await fs.writeFile(`${browserFile}.${process.pid}.tmp`,`/* Generated by tools/shf/update-voice-migration-status.mjs. */\nwindow.SCRIPTA_VOICE_MIGRATION_STATUS=${JSON.stringify(browserData)};\n`);
  await fs.rename(`${browserFile}.${process.pid}.tmp`,browserFile);
  console.log(JSON.stringify({counts,entries:entries.length}));
} finally { await handle.close(); await fs.rm(lock,{force:true}); }
