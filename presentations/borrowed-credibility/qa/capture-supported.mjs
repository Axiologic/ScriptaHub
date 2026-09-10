import fs from 'node:fs/promises';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('..',import.meta.url).pathname.replace(/\/$/,'');
await fs.mkdir(root+'/qa/supported-screenshots',{recursive:true});const frames=[];
for(const theme of ['color'])for(let i=0;i<4;i++)for(const [frame,ratio]of [['first',.08],['middle',.5],['last',.96]]){
 const c=await connect('file://'+root+'/exports/borrowed-credibility-introduction.html');
 try{await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');const rect=await c.evaluate(`(async()=>{const p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.$('centerPlay').style.visibility='hidden';p.setTheme('${theme}');await document.fonts.ready;p.seek(p.film.scenes.slice(0,${i}).reduce((a,s)=>a+s.durationMs,0)+p.film.scenes[${i}].durationMs*${ratio});p.svg.style.transform='translateZ(0)';p.svg.style.filter='opacity(1)';await new Promise(r=>setTimeout(r,600));const r=p.$('stage').getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height}})()`);const name=`${theme}-${String(i).padStart(2,'0')}-${frame}.png`;await c.capture(root+'/qa/supported-screenshots/'+name);frames.push({name,rect,jsErrors:c.errors});}finally{await c.close()}
}
await fs.writeFile(root+'/qa/supported-capture-review.json',JSON.stringify({reason:'Scaled CDP clip screenshots produced transient missing raster tiles; fresh tabs alone also reproduced missing tiles after theme changes although DOM shapes remained present; a QA-only translateZ(0) on the SVG forces a fresh compositor layer, followed by full-resolution viewport capture and local contact-sheet crop.',audiblePlayback:false,frames},null,2)+'\n');console.log('36 fresh full-resolution silent captures.');
