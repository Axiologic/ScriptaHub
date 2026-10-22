// usage: node frames.mjs outdir themes(comma) scene beat fracs(comma)  [cropX cropY cropW cropH]
import fs from 'node:fs/promises';import {connect} from '../../../../tests/browser-session.mjs';
const [out,themes,s,b,fr,cx,cy,cw,ch]=process.argv.slice(2);await fs.mkdir(out,{recursive:true});
const c=await connect('file:///home/salboaie/work/axiologic/ScriptaHub/presentations/beyond-the-last-stone/exports/beyond-the-last-stone-introduction.html');
try{await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
for(const theme of themes.split(','))for(const f of fr.split(',')){
const ev=await c.evaluate(`(async()=>{const p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.setTheme('${theme}');await document.fonts.ready;const sc=p.film.scenes[${s}],bt=sc.beats[${b}];p.seek(p.film.scenes.slice(0,${s}).reduce((n,s)=>n+s.durationMs,0)+bt.startMs+Math.round((bt.endMs-bt.startMs)*${f}));p.$('centerPlay').style.visibility='hidden';await new Promise(r=>setTimeout(r,500));const r=p.svg.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()`);
const [x,y,w,h]=ev,k=w/1200;const clip=cx?{x:x+(+cx)*k,y:y+(+cy)*k,width:(+cw)*k,height:(+ch)*k,scale:2}:{x,y,width:w,height:h,scale:.6};
const r=await c.send('Page.captureScreenshot',{format:'png',clip});await fs.writeFile(`${out}/s${s}b${b}-${theme}-${f}.png`,Buffer.from(r.data,'base64'));}
}finally{await c.close()}
