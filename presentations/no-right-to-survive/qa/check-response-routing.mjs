import fs from 'node:fs/promises';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('..',import.meta.url).pathname.replace(/\/$/,'');
const c=await connect('file://'+root+'/exports/no-right-to-survive-introduction.html');
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause()');
 const results=[];
 for(const theme of ['color','paper','night']){
  await c.evaluate(`p.setTheme('${theme}')`);
  const samples=[];
  for(const beat of [1,6])samples.push(await c.evaluate(`(()=>{const b=p.film.scenes[0].beats[${beat-1}];p.seek(b.startMs+700);return{beat:${beat},caption:p.$('caption').textContent,nodes:['caregiver','child','equipment-order','maintenance-tray'].map(id=>{const e=p.dom.get(id),t=e.getCTM();return{id,x:t.e,y:t.f,opacity:Number(getComputedStyle(e).opacity)}}),playing:p.playing,audioContextOpen:!!p.audio.ctx}})()`));
  const x=(sample,id)=>sample.nodes.find(n=>n.id===id);const nurseDx=x(samples[1],'caregiver').x-x(samples[0],'caregiver').x,orderDy=x(samples[1],'equipment-order').y-x(samples[0],'equipment-order').y;
  const pass=nurseDx< -10&&orderDy>100&&x(samples[1],'maintenance-tray').opacity>.9&&samples.every(s=>!s.playing&&!s.audioContextOpen);
  results.push({theme,pass,nurseDx,orderDy,samples});if(!pass)throw Error(JSON.stringify(results.at(-1)));
 }
 await fs.writeFile(root+'/qa/response-routing-review.json',JSON.stringify({status:'pass',method:'Silent deterministic seek verifies the caregiver physically reaches the child while the animal report travels to the maintenance tray. This tests enacted routing, not moral equivalence or real treatment efficacy.',results,errors:c.errors,audiblePlayback:false},null,2)+'\n');console.log('Different care and maintenance routing verified in all three themes.');
}finally{await c.close()}
