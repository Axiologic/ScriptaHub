import fs from 'node:fs/promises';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('..',import.meta.url).pathname.replace(/\/$/,'');const c=await connect('file://'+root+'/exports/the-substrate-cycle-introduction.html');
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause()');const results=[];
 for(const theme of ['color','paper','night']){
  await c.evaluate(`p.setTheme('${theme}')`);const flood=[];
  for(const b of [0,5])flood.push(await c.evaluate(`(()=>{p.seek(p.film.scenes[0].durationMs+p.film.scenes[1].beats[${b}].startMs+900);return{caption:p.$('caption').textContent,nodes:['gate','water-front','local-home'].map(id=>{const e=p.dom.get(id),m=e.getCTM();return{id,x:m.e,y:m.f,opacity:Number(getComputedStyle(e).opacity)}}),playing:p.playing,audioContextOpen:!!p.audio.ctx}})()`));
  const at=(v,id)=>v.nodes.find(n=>n.id===id),gateDy=at(flood[1],'gate').y-at(flood[0],'gate').y,waterDx=at(flood[1],'water-front').x-at(flood[0],'water-front').x;
  const care=[];
  for(const time of [1100,2350])care.push(await c.evaluate(`(()=>{const start=p.film.scenes.slice(0,2).reduce((a,s)=>a+s.durationMs,0);p.seek(start+p.film.scenes[2].beats[2].startMs+${time});const m=p.dom.get('care-signal').getCTM(),r=p.dom.get('infant-event').getCTM();return{caption:p.$('caption').textContent,x:m.e,y:m.f,opacity:Number(getComputedStyle(p.dom.get('care-signal')).opacity),infantX:r.e,infantY:r.f,labels:[...p.dom.get('enabling-role').querySelectorAll('text')].map(t=>t.textContent),nila:[...p.dom.get('nila-label').querySelectorAll('text')].map(t=>t.textContent)}})()`));
  const pass=gateDy>40&&waterDx>150&&at(flood[1],'water-front').x>at(flood[1],'local-home').x&&flood.every(x=>!x.playing&&!x.audioContextOpen)&&care[1].y<care[0].y-20&&care.every(x=>x.opacity>.7&&x.caption.includes('older child'))&&care[1].labels.includes('Freed caregiver')&&care[1].nila.includes('Nila · Infant');
  results.push({theme,pass,gateDy,waterDx,flood,care});if(!pass)throw Error(JSON.stringify(results.at(-1)));
 }
 await fs.writeFile(root+'/qa/material-motion-review.json',JSON.stringify({status:'pass',method:'Silent deterministic seeks measure actual gate descent and connected water-front travel to the house, then inspect the indirect-care signal travelling beside the infant label through the Freed caregiver route. Nila’s infant label and the full older-child sentence remain distinct. This is conceptual staging, not a hydrological or care-credit model.',results,errors:c.errors,audiblePlayback:false},null,2)+'\n');console.log('Gate descent, water arrival and indirect enabling-care motion verified in all themes.');
}finally{await c.close()}
