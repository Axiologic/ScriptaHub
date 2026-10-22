// usage: face.mjs outdir theme scene beat offset|mid stageX stageY [name]
import fs from 'node:fs/promises';import {connect} from '../../../../tests/browser-session.mjs';
const [out,theme,s,b,t,sx,sy,name]=process.argv.slice(2);await fs.mkdir(out,{recursive:true});
const c=await connect('file:///home/salboaie/work/axiologic/ScriptaHub/presentations/beyond-the-last-stone/exports/beyond-the-last-stone-introduction.html');
try{await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
const ev=await c.evaluate(`(async()=>{const p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.setTheme('${theme}');await document.fonts.ready;const sc=p.film.scenes[${s}],bt=sc.beats[${b}];const off='${t}'==='mid'?Math.round((bt.endMs-bt.startMs)/2):${t==='mid'?0:t};p.seek(p.film.scenes.slice(0,${s}).reduce((n,s)=>n+s.durationMs,0)+bt.startMs+off);p.$('centerPlay').style.visibility='hidden';await new Promise(r=>setTimeout(r,700));const r=p.svg.getBoundingClientRect();return [r.x,r.y,r.width]})()`);
const [x,y,w]=ev,k=w/1200;const crop=await c.send('Page.captureScreenshot',{format:'png',clip:{x:x+(+sx-110)*k,y:y+(+sy-90)*k,width:220*k,height:180*k,scale:4}});await fs.writeFile(`${out}/${name||theme}.png`,Buffer.from(crop.data,'base64'));
}finally{await c.close()}
