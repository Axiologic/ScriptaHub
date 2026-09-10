import fs from 'node:fs/promises';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('..',import.meta.url).pathname.replace(/\/$/,'');
const c=await connect('file://'+root+'/exports/solipsicon-introduction.html');
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause();p.$("centerPlay").style.visibility="hidden"');
 const meta=await c.evaluate('({offset:p.film.scenes[0].durationMs+p.film.scenes[1].durationMs,beats:p.film.scenes[2].beats})');
 const samples=[];
 for(const theme of ['color','paper','night'])for(const beat of [2,5]){
  await c.evaluate(`p.setTheme('${theme}')`);
  const pair=[];
  for(const add of [850,1350]){
   const time=meta.offset+meta.beats[beat-1].startMs+add;
   pair.push(await c.evaluate(`(()=>{p.seek(${time});const ids=['outside-b${beat}-0','reflection-b${beat}-0'];return{timeMs:${time},caption:p.$('caption').textContent,positions:ids.map(id=>{const e=p.dom.get(id),m=e.getCTM();return{id,y:m.f,opacity:Number(getComputedStyle(e).opacity)}}),audioContextOpen:!!p.audio.ctx,playing:p.playing}})()`));
   if(theme==='color'&&beat===2){await c.evaluate('document.fonts.ready.then(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))))');await c.capture(root+'/qa/rain-displacement-'+add+'.png');}
  }
  const dy=pair[1].positions.map((p,i)=>p.y-pair[0].positions[i].y);
  const pass=dy[0]>2&&dy[1]<-2&&pair.every(p=>!p.playing&&!p.audioContextOpen&&p.caption===meta.beats[beat-1].text&&p.positions.every(x=>x.opacity>.5));
  samples.push({theme,beat,pair,deltaY:dy,pass});if(!pass)throw Error('Actual rain movement/caption test failed: '+JSON.stringify(samples.at(-1)));
 }
 await fs.writeFile(root+'/qa/rain-motion-review.json',JSON.stringify({status:'pass',method:'Deterministic silent seek across the same 500ms interval; actual rendered group CTM y and current full caption, all themes, beats 2 and 5. Downward must be positive, upward negative.',samples,audiblePlayback:false,errors:c.errors},null,2)+'\n');console.log('Opposed rain motion passes in all six sampled theme/beat pairs.');
}finally{await c.close()}
