#!/usr/bin/env node
// Historical command name; now migrate all book films to introductions of at most two minutes.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import crypto from 'node:crypto';
import {requireMarketingBatch} from './marketing-review.mjs';
import {narrationDirection,narrationInputHash} from './narration-input.mjs';

await import(path.resolve('.agents/skills/shf-presentation-creator/runtime/shf-core.js'));
const limit=Number(process.env.SHF_MIGRATION_LIMIT||0);
const worker=Number(process.env.SHF_MIGRATION_WORKER||0);
const workers=Math.max(1,Number(process.env.SHF_MIGRATION_WORKERS||1));
const aiden=new Set([
  'AI Adoption Beyond the Slop','AI Agents','Anti-Idiocracy','Anti-Trivialization Machines of the Future','Artificial Impossibility','Bias in AI','Decentralised Brands','Egregnosis','Egregopathy','From Rules, Worlds','Investing in an AI-Dominated Economy','Judgment Engines','Limits of Machine Intelligence','Machines of Understanding Through Circuits','More Words Than Reality','MRP-VM','OpenDSU','RAG and EPR','The Blind Specialist','The Fragmented Future','The Future of Research Infrastructure','The Great Decoupling','The History and Future of Social Technologies','The Licence and the Shared Name','The Network of Intent','The Permission Paradox','The Smoothing','The Society That Selects Us','The Substrate Cycle','Too Convinced to Stop','Trustworthy AI','Vector-Symbolic Intelligence in Practice','What We Still Have to Solve','The Animal That Prays','The Art of Knowing What Matters','The Cascade of the New','The Gospel of the Basilisk','The Houses of Europe','The Last Naive Person','The Makers of Reality','The Necessary Mask','The Right Not to Be Saved','The Right to Help','The Science and Wisdom of Limits','The Sovereignty Archipelago','The Thousand-Handed Devil','The Voluptuous Apocalypse','The World Does Not Read Equations','Who Will Inherit the World?'
]);
const fiction=/universe|wish|eden|hunger|houses|predator|basilisk|oracle|devil|zodiac|echo|apocalypse|naive|animal|series/i;
const technical=/\bAI\b|machine|agents|infrastructure|network|vector|RAG|EPR|VM|OpenDSU|research|equations|circuits|intelligence|adoption|brands/i;
const reflective=/beauty|faith|freedom|meaning|reality|wisdom|tao|life|responsibility|copy|rights|prays|civilized|art of knowing/i;
const readJson=file=>fs.readFile(file,'utf8').then(JSON.parse);
const exists=file=>fs.access(file).then(()=>true).catch(()=>false);
const sha256=file=>fs.readFile(file).then(data=>crypto.createHash('sha256').update(data).digest('hex'));

async function alreadyComplete(entry){
  const [production,receipts,build,scenes]=await Promise.all([
    readJson(path.join(entry.project,'work/production.json')),
    exists(path.join(entry.project,'work/voice-receipts.json')).then(ok=>ok?readJson(path.join(entry.project,'work/voice-receipts.json')):null),
    exists(path.join(entry.project,'qa/build.json')).then(ok=>ok?readJson(path.join(entry.project,'qa/build.json')):null),
    readJson(path.join(entry.project,'work/scenes.json'))
  ]);
  const lines=receipts?.lines||[];
  const texts=scenes.flatMap(scene=>scene.lines).map(text=>crypto.createHash('sha256').update(text).digest('hex'));
  const textCurrent=lines.length===texts.length&&lines.every((line,index)=>line.textSha256===texts[index]);
  const performance=scenes.flatMap(scene=>scene.lines.map((_,index)=>narrationInputHash(narrationDirection(scene,index,production),production)));
  const performanceCurrent=lines.length===performance.length&&lines.every((line,index)=>line.performanceSha256===performance[index]);
  const audioValid=lines.length>0 && await Promise.all(lines.map(async line=>{
    const audio=path.join(entry.project,'work',line.file);
    return await exists(audio) && await sha256(audio)===line.sha256;
  })).then(values=>values.every(Boolean));
  if(!(production.voiceEngine==='qwen'&&/Qwen3-TTS/.test(receipts?.provider||'')&&textCurrent&&performanceCurrent&&audioValid&&build&&await exists(entry.shf)))return false;
  const film=await SHFCore.loadFile(new File([await fs.readFile(entry.shf)],path.basename(entry.shf)));
  const published=film.scenes.flatMap(scene=>scene.beats||[]);
  return film.durationMs<=120000&&published.length===texts.length&&published.every((beat,index)=>crypto.createHash('sha256').update(beat.text).digest('hex')===texts[index])&&lines.every(line=>Object.values(film.assets||{}).some(asset=>asset.sha256===line.sha256));
}

async function manifests(dir='docs/books'){
  const out=[]; for(const entry of await fs.readdir(dir,{withFileTypes:true})){
    const file=path.join(dir,entry.name);
    if(entry.isDirectory()) out.push(...await manifests(file));
    else if(entry.name==='manifest.json') out.push(file);
  } return out;
}
async function filmDuration(file){
  const data=await fs.readFile(file); const film=await SHFCore.loadFile(new File([data],path.basename(file))); return film.durationMs;
}
function profile(title){
  const kind=technical.test(title)?'technical':fiction.test(title)?'narrative':reflective.test(title)?'reflective':'analytic';
  const voice=aiden.has(title)?'Aiden':'Ryan';
  const open=kind==='narrative'?'Begin intimately and with quiet curiosity; let the question create interest without trailer-like drama.':kind==='technical'?'Open with focused curiosity and clean articulation; make the problem feel concrete, never promotional.':kind==='reflective'?'Open warmly and contemplatively; leave room for the question without sounding solemn.':'Open with a clear, considered question and restrained intellectual energy.';
  const middle=kind==='narrative'?'Continue with lucid storytelling and a gentle shift of emphasis; preserve mystery without exaggerating stakes.':kind==='technical'?'Explain with calm precision and deliberate emphasis on the key terms; keep the cadence human and unhurried.':kind==='reflective'?'Develop the idea with patient clarity and a natural conversational rhythm; let the thought breathe.':'Develop the argument plainly and steadily, with subtle emphasis only where the reasoning turns.';
  const close=kind==='narrative'?'Close with a warm, inviting curiosity; resolve softly rather than performing a dramatic finish.':kind==='technical'?'Close with measured confidence and a practical invitation; avoid sales language.':kind==='reflective'?'Close gently, with an open and personal invitation to continue reading.':'Close with a sober, inviting cadence and a small sense of discovery.';
  return {voice,kind,directions:[open,middle,close],intensities:kind==='narrative'?[.42,.45,.36]:kind==='technical'?[.38,.43,.36]:kind==='reflective'?[.36,.40,.34]:[.39,.43,.36]};
}
function updateProject(project,title){
  const pfile=path.join(project,'work/production.json'), sfile=path.join(project,'work/scenes.json');
  return Promise.all([readJson(pfile),readJson(sfile)]).then(async([production,scenes])=>{
    const p=profile(title); production.voiceEngine='qwen'; production.voiceId=p.voice; production.voiceRuntimeConfig='.agents/skills/theatrical-audio/runtime/qwen.json'; production.voiceProvider=`local Qwen3-TTS 1.7B CustomVoice / ${p.voice}`; production.voiceRights='Source adaptation and local neural narration authorized by the project editor.';
    production.voicePace=p.kind==='technical'?.95:p.kind==='narrative'?.93:.94;
    production.minDurationMs=0; production.maxDurationMs=120000;
    for(const [sceneIndex,scene] of scenes.entries()){
      const isClosing=sceneIndex===scenes.length-1; scene.pauseAfterMs=(scene.pauseAfterMs||scene.lines.map(()=>1200)).map((pause,lineIndex)=>Math.max(Number(pause)||0,lineIndex===scene.lines.length-1?(isClosing?2100:1950):1150));
      const sceneStyle=sceneIndex===0?0:sceneIndex===scenes.length-1?2:1;
      const existing=scene.emotionalPlan||{};
      const fallbackDirections=scene.lines.map((_,lineIndex)=>p.directions[Math.min(2,sceneStyle)] + (lineIndex===scene.lines.length-1?' Leave a quiet beat for the viewer to consider it.':''));
      scene.emotionalPlan={...existing,
        states:Array.isArray(existing.states)&&existing.states.length===scene.lines.length?existing.states:scene.lines.map((_,i)=>sceneIndex===0&&i===0?'curiosity':isClosing&&i===scene.lines.length-1?'invitation':'clarity'),
        intensities:Array.isArray(existing.intensities)&&existing.intensities.length===scene.lines.length?existing.intensities:scene.lines.map((_,i)=>Math.min(.55,p.intensities[Math.min(2,sceneStyle)]+(i===0?0:.02))),
        voiceDirections:Array.isArray(existing.voiceDirections)&&existing.voiceDirections.length===scene.lines.length?existing.voiceDirections:fallbackDirections};
    }
    await fs.writeFile(pfile,JSON.stringify(production,null,2)+'\n'); await fs.writeFile(sfile,JSON.stringify(scenes,null,2)+'\n'); return p;
  });
}
function run(cmd,args,env){return new Promise((resolve,reject)=>{const child=spawn(cmd,args,{stdio:'inherit',env:{...process.env,...env}});child.on('exit',code=>code===0?resolve():reject(new Error(`${cmd} exited ${code}`)));child.on('error',reject);});}
const all=[];for(const mf of await manifests()){const m=await readJson(mf);if(!m.animation?.shf)continue;const shf=path.resolve(path.dirname(mf),m.animation.shf);const candidates=(await fs.readdir('presentations')).map(n=>path.join('presentations',n));const project=(await Promise.all(candidates.map(async c=>({c,p:await exists(path.join(c,'work/production.json'))?await readJson(path.join(c,'work/production.json')):null})))).find(x=>path.resolve(x.p?.bookDirectory||'')===path.resolve(path.dirname(mf)))?.c;if(project)all.push({title:m.title.en,project,shf});}
const selected=all.sort((a,b)=>a.title.localeCompare(b.title)).filter((entry,i)=>process.env.SHF_MIGRATION_PROJECT?path.resolve(entry.project)===path.resolve(process.env.SHF_MIGRATION_PROJECT):i%workers===worker).slice(0,limit||Infinity);
if(process.env.SHF_MIGRATION_RENDER==='1')await requireMarketingBatch(all);
for(const entry of selected){
  if(await alreadyComplete(entry)){ console.log(`Already complete ${entry.title}; keeping its verified Qwen narration.`); continue; }
  const p=await updateProject(entry.project,entry.title); console.log(`Prepared ${entry.title}: ${p.voice}, ${p.kind}`);
  if(process.env.SHF_MIGRATION_RENDER==='1'){
    const cpus=process.env.SHF_MIGRATION_CPUS||'0,1'; const threads=String(Math.max(1,Number(process.env.SHF_MIGRATION_THREADS||2))); const env={OMP_NUM_THREADS:threads,MKL_NUM_THREADS:threads,OPENBLAS_NUM_THREADS:threads,NUMEXPR_NUM_THREADS:threads};
    await run('taskset',['-c',cpus,'node',path.join(entry.project,'render_voice.mjs')],env);
    if(process.env.SHF_MIGRATION_AUDIO_ONLY!=='1')await run('node',[path.join(entry.project,'build.mjs')],env);
  }
}
console.log(JSON.stringify({worker,workers,selected:selected.length,rendered:process.env.SHF_MIGRATION_RENDER==='1'}));
