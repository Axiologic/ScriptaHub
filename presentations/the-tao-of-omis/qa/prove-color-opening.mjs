import fs from 'node:fs/promises';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('..',import.meta.url).pathname.replace(/\/$/,'');
const dir=root+'/qa/color-opening-sequential-'+Date.now();await fs.mkdir(dir,{recursive:true});let frames=[];
for(const [name,ratio]of [['first',.08],['last',.96]]){
 const c=await connect('file://'+root+'/exports/the-tao-of-omis-introduction.html');
 try{await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
 const dom=await c.evaluate(`(async()=>{const p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.setTheme('color');await document.fonts.ready;p.seek(p.film.scenes[0].durationMs*${ratio});p.$('centerPlay').style.visibility='hidden';await new Promise(r=>setTimeout(r,1800));const box=e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height,visibility:getComputedStyle(e).visibility,opacity:getComputedStyle(e).opacity}};return{stage:box(p.$('stage')),svg:box(p.svg),texts:[...p.shadowRoot.querySelectorAll('text')].map(e=>({text:e.textContent,...box(e)})),html:p.shadowRoot.innerHTML.slice(-5000),sceneDuration:p.film.scenes[0].durationMs,time:p.film.scenes[0].durationMs*${ratio}}})()`);
 await c.capture(dir+'/'+name+'-raw.png');
 await c.evaluate(`(async()=>{const p=document.querySelector('shf-player');p.svg.style.transform='translateZ(0)';await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));await new Promise(r=>setTimeout(r,1200))})()`);
 await c.capture(dir+'/'+name+'-repaint.png');frames.push({name,dom,errors:c.errors});
 }finally{await c.close()}
}
await fs.writeFile(dir+'/dom-evidence.json',JSON.stringify({candidateSHA256:'ea884627eb7848ff88373dacd89b58be3ba83497178ccab25184871b9aa4903b',audiblePlayback:false,frames},null,2));await fs.writeFile(root+'/qa/latest-sequential-proof.json',JSON.stringify({dir},null,2));console.log(dir);
