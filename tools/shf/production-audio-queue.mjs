#!/usr/bin/env node
import fs from 'node:fs/promises';
import {spawn,execFile} from 'node:child_process';
import {promisify} from 'node:util';
import crypto from 'node:crypto';
import {narrationDirection,narrationInputHash} from './narration-input.mjs';
const exec=promisify(execFile),sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const stateFile='tasks/production-audio-queue-state.json',lockFile='tasks/.production-audio-queue.lock';
// Measured production throughput is higher with three workers on this host.
const count=Number(process.env.SHF_AUDIO_WORKERS||3);
if(![3,4].includes(count))throw Error('Use three or four audio workers');
const ranges=count===4?['1-4','5-8','9-12','13-15']:['1-5','6-10','11-15'];
const cpus=value=>value.split(',').flatMap(part=>{const [a,b]=part.split('-').map(Number);return Array.from({length:(b??a)-a+1},(_,i)=>a+i)});
const groups=ranges.map((range,id)=>({id,cpus:range,threads:cpus(range).length}));
const jobs=JSON.parse(await fs.readFile('tasks/animation-production-queue.json')).jobs;
const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
const json=file=>fs.readFile(file,'utf8').then(JSON.parse);
const alive=async pid=>{try{return !/^State:\s+Z/m.test(await fs.readFile(`/proc/${pid}/status`,'utf8'))}catch{return false}};
async function liveJobs(){
 const {stdout}=await exec('ps',['-eo','pid=,args=']);
 const found=[];
 for(const line of stdout.split('\n')){
  const match=line.trim().match(/^(\d+)\s+(?:\S*\/)?node\s+(presentations\/[^\s]+)\/render_voice\.mjs(?:\s|$)/);
  if(!match)continue;
  try{const status=await fs.readFile(`/proc/${match[1]}/status`,'utf8');if(/^State:\s+Z/m.test(status))continue;
   found.push({pid:Number(match[1]),project:match[2],cpus:cpus(status.match(/^Cpus_allowed_list:\s*(.+)$/m)[1])});
  }catch{}
 }
 return found;
}
async function audioReady(job){
 try{
  const [scenes,production,receipts]=await Promise.all(['scenes','production','voice-receipts'].map(name=>json(`${job.project}/work/${name}.json`)));
  if(production.voiceEngine!=='qwen'||!/Qwen3-TTS/.test(receipts.provider||''))return false;
  const expected=scenes.flatMap(scene=>scene.lines.map((text,index)=>({text,performance:narrationInputHash(narrationDirection(scene,index,production),production)})));
  if(receipts.lines.length!==expected.length)return false;
  for(const [i,line]of receipts.lines.entries())if(line.textSha256!==sha(expected[i].text)||line.performanceSha256!==expected[i].performance||line.sha256!==sha(await fs.readFile(`${job.project}/work/${line.file}`)))return false;
  return true;
 }catch{return false;}
}
let lock;
for(let attempt=0;attempt<2;attempt++){
 try{lock=await fs.open(lockFile,'wx');await lock.writeFile(`${process.pid}\n`);break;}
 catch(error){if(error.code!=='EEXIST')throw error;const pid=Number((await fs.readFile(lockFile,'utf8')).trim());if(!pid||await alive(pid))throw Error(`Audio coordinator already owns lock: ${pid}`);await fs.rm(lockFile);}
}
if(!lock)throw Error('Could not acquire audio coordinator lock');
const state={version:2,coordinatorPid:process.pid,startedAt:new Date().toISOString(),workerCount:count,workers:{},jobs:{}};
const claimed=new Set(),completed=new Set(),failed=new Set();let serial=0,writeTail=Promise.resolve();
function save(){const snapshot=JSON.stringify({...state,updatedAt:new Date().toISOString()},null,2)+'\n';writeTail=writeTail.then(async()=>{const tmp=`${stateFile}.${process.pid}.${++serial}.tmp`;await fs.writeFile(tmp,snapshot);await fs.rename(tmp,stateFile)});return writeTail;}
async function runGroup(group){
 const log=`tasks/production-audio-worker-${group.id}.log`,handle=await fs.open(log,'a');
 state.workers[group.id]={status:'checking-live-jobs',...group,log};await save();
 try{
  while(true){
   const live=await liveJobs();
   const busy=live.filter(job=>job.cpus.some(cpu=>cpus(group.cpus).includes(cpu)));
   if(busy.length){state.workers[group.id]={...state.workers[group.id],status:'waiting-for-live-job',live:busy};await save();await sleep(5000);continue;}
   let selected;
   for(const job of jobs){
    if(completed.has(job.project)||failed.has(job.project)||claimed.has(job.project)||live.some(item=>item.project===job.project))continue;
    claimed.add(job.project);
    if(await audioReady(job)){completed.add(job.project);claimed.delete(job.project);state.jobs[job.project]={title:job.title,status:'verified-existing'};continue;}
    selected=job;break;
   }
   if(!selected){if(claimed.size||live.length){await sleep(5000);continue;}break;}
   const job=selected,started=Date.now();
   state.jobs[job.project]={title:job.title,status:'running',worker:group.id,startedAt:new Date(started).toISOString()};
   await fs.appendFile(log,`START ${job.title} ${new Date().toISOString()} CPUs ${group.cpus}\n`);
   const child=spawn(process.execPath,['tools/shf/migrate-short-film-qwen.mjs'],{env:{...process.env,SHF_MIGRATION_PROJECT:job.project,SHF_MIGRATION_RENDER:'1',SHF_MIGRATION_AUDIO_ONLY:'1',SHF_MIGRATION_CPUS:group.cpus,SHF_MIGRATION_THREADS:String(group.threads)},stdio:['ignore',handle.fd,handle.fd]});
   state.workers[group.id]={...group,status:'running',project:job.project,pid:child.pid,log};await save();
   const code=await new Promise(resolve=>{child.once('error',()=>resolve(-1));child.once('exit',value=>resolve(value??-1))});
   const verified=code===0&&await audioReady(job);
   (verified?completed:failed).add(job.project);claimed.delete(job.project);
   state.jobs[job.project]={...state.jobs[job.project],status:verified?'generated':'failed',exitCode:code,elapsedSeconds:Math.round((Date.now()-started)/1000),finishedAt:new Date().toISOString()};
   state.workers[group.id]={...group,status:'between-jobs',log};await save();
  }
  state.workers[group.id]={...group,status:'complete',log};await save();
 }finally{await handle.close();}
}
try{await Promise.all(groups.map(runGroup));state.finishedAt=new Date().toISOString();state.status=failed.size?'finished-with-errors':'complete';await save();}
finally{await writeTail;await lock.close();await fs.rm(lockFile,{force:true});}
