import fs from 'node:fs/promises';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('..',import.meta.url).pathname.replace(/\/$/,'');
const c=await connect('file://'+root+'/exports/oriven-and-origaya-universe-introduction.html');
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause()');
 const results=[];
 for(const theme of ['color','paper','night']){
  await c.evaluate(`p.setTheme('${theme}')`);
  const samples=[];
  for(const t of [600,1800])samples.push(await c.evaluate(`(()=>{const start=p.film.scenes.slice(0,2).reduce((s,x)=>s+x.durationMs,0),b=p.film.scenes[2].beats[2];p.seek(start+b.startMs+${t});return{offsetMs:${t},caption:p.$('caption').textContent,nodes:['optical-finding','isolated-receiver','living-receiver'].map(id=>{const e=p.dom.get(id),m=e.getCTM();return{id,x:m.e,y:m.f,opacity:Number(getComputedStyle(e).opacity)}}),playing:p.playing,audioContextOpen:!!p.audio.ctx}})()`));
  const x=(s,id)=>s.nodes.find(n=>n.id===id),dx=x(samples[1],'optical-finding').x-x(samples[0],'optical-finding').x;
  const bridge=await c.evaluate(`(()=>{p.seek(p.film.scenes[0].durationMs+p.film.scenes[1].durationMs*.96);const o=p.dom.get('continuity-nursery');return{opacity:Number(getComputedStyle(o).opacity),pathCount:o.querySelectorAll('path').length,caption:p.$('caption').textContent}})()`);
  const pass=dx>20&&samples.every(s=>x(s,'optical-finding').opacity>.8&&!s.playing&&!s.audioContextOpen)&&x(samples[0],'isolated-receiver').x<x(samples[0],'optical-finding').x&&x(samples[1],'optical-finding').x<x(samples[1],'living-receiver').x&&bridge.opacity>.99;
  results.push({theme,pass,opticalSignalDx:dx,samples,bridge});if(!pass)throw Error(JSON.stringify(results.at(-1)));
 }
 await fs.writeFile(root+'/qa/observation-motion-review.json',JSON.stringify({status:'pass',method:'Paused deterministic seeks inspect actual rendered optical-signal positions, current full sentence, stationary separate receiver positions and visible intact nursery assembly in all themes. The optical gap is illustrative geometry; no material root crosses it. No claim of realistic biological simulation.',results,errors:c.errors,audiblePlayback:false},null,2)+'\n');console.log('Optical return motion and visible nursery continuity verified in all three themes.');
}finally{await c.close()}
