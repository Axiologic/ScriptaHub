import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {spawnSync} from 'node:child_process';
import {narrationDirection,narrationInputHash} from '../../tools/shf/narration-input.mjs';
import {requireMarketingBatch} from '../../tools/shf/marketing-review.mjs';
const specs=JSON.parse(fs.readFileSync('.book-work/ai-completion-20261111/film-specs.json')),worker=Number(process.argv[2]||0);
await requireMarketingBatch(specs.map(s=>({project:'presentations/'+s.slug})));
projects: for(const [i,spec]of specs.entries()){
 if(i%2!==worker)continue;
 const root='presentations/'+spec.slug;
 const receiptsFile=root+'/work/voice-receipts.json';
 if(fs.existsSync(receiptsFile)){
  const receipts=JSON.parse(fs.readFileSync(receiptsFile)),scenes=JSON.parse(fs.readFileSync(root+'/work/scenes.json')),production=JSON.parse(fs.readFileSync(root+'/work/production.json'));
  const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
  const beats=scenes.flatMap(scene=>scene.lines.map((text,index)=>({id:scene.id+'-line-'+(index+1),text,performance:narrationInputHash(narrationDirection(scene,index,production),production)})));
  if(receipts.lines.length===beats.length&&beats.every(beat=>{const line=receipts.lines.find(line=>line.id===beat.id);return line&&line.textSha256===hash(beat.text)&&line.performanceSha256===beat.performance&&fs.existsSync(root+'/work/'+line.file)&&hash(fs.readFileSync(root+'/work/'+line.file))===line.sha256})){console.log('PRESERVED CURRENT VOICE',spec.slug);continue;}
 }
 const bundles=root+'/work/voice-bundles';
 if(fs.existsSync(bundles))for(const folder of fs.readdirSync(bundles)){
  const file=path.join(bundles,folder,'.render.lock');if(!fs.existsSync(file))continue;
  const lock=JSON.parse(fs.readFileSync(file));let live=true;try{process.kill(lock.pid,0)}catch(e){if(e.code==='ESRCH')live=false;else throw e}
  if(live){console.log('SKIP LIVE RENDERER',spec.slug);continue projects;}
  fs.renameSync(file,file+'.interrupted-'+Date.now());
 }
 console.log('START',spec.slug,new Date().toISOString());
 const result=spawnSync(process.execPath,[root+'/render_voice.mjs'],{stdio:'inherit',env:process.env});
 if(result.status!==0){console.error('FAILED',spec.slug,result.status,result.signal);process.exit(result.status||1)}
 console.log('VOICE READY',spec.slug,new Date().toISOString());
}
