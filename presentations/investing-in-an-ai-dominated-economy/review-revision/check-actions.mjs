import fs from 'node:fs/promises';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('../',import.meta.url),url=new URL('exports/investing-in-an-ai-dominated-economy-introduction.html',root).href;
const c=await connect(url),rows=[];
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
 await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause();p.setTheme("color");p.$("centerPlay").style.visibility="hidden"');
 for(const [scene,beat,offset,ids]of [[1,4,100,['case','check-result']],[1,4,1600,['case','check-result']],[1,4,4500,['case','check-result']],[5,1,100,['decision','missing','next']],[5,1,1800,['decision','missing','next']],[5,1,4500,['decision','missing','next']]]){
 const r=await c.evaluate(`(()=>{const start=p.film.scenes.slice(0,${scene}).reduce((n,s)=>n+s.durationMs,0);const t=start+p.film.scenes[${scene}].beats[${beat}].startMs+${offset};p.seek(t);return{timeMs:t,scene:${scene},offset:${offset},objects:${JSON.stringify(ids)}.map(id=>{const e=p.dom.get(id);return{id,transform:e.getAttribute('transform'),opacity:getComputedStyle(e).opacity}})}})()`);rows.push(r);
 await c.evaluate('new Promise(r=>setTimeout(r,150))');await c.capture(new URL(`action-${scene}-${offset}.png`,import.meta.url).pathname);
 }
 await fs.writeFile(new URL('action-review.json',import.meta.url),JSON.stringify({audiblePlayback:false,rows},null,2)+'\n');console.log(JSON.stringify(rows));
}finally{await c.close()}
