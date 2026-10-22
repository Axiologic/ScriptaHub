// Round 5: 20 ms sampling around a moment, per theme. Reports arm/expression opacities and saves crops.
// usage: node swap-frames.mjs OUTDIR THEMES SCENE BEAT FROM_MS TO_MS STEP_MS X Y W H [ids,comma]
import fs from 'node:fs/promises';import {connect} from '../../../../tests/browser-session.mjs';
const [out,themes,s,b,from,to,step,cx,cy,cw,ch,ids='ar-chin-arm,ar-arm']=process.argv.slice(2);await fs.mkdir(out,{recursive:true});
const c=await connect('file:///home/salboaie/work/axiologic/ScriptaHub/presentations/beyond-the-last-stone/exports/beyond-the-last-stone-introduction.html');
const report=[];
try{await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
for(const theme of themes.split(','))for(let ms=+from;ms<=+to;ms+=+step){
 const ev=await c.evaluate(`(async()=>{const p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.setTheme('${theme}');await document.fonts.ready;
 const sc=p.film.scenes[${s}],bt=sc.beats[${b}];p.seek(p.film.scenes.slice(0,${s}).reduce((n,s)=>n+s.durationMs,0)+bt.startMs+${ms});p.$('centerPlay').style.visibility='hidden';
 await new Promise(r=>setTimeout(r,90));const r=p.svg.getBoundingClientRect();
 const op=id=>{const e=p.dom.get(id);if(!e)return null;let o=1;for(let n=e;n&&n!==p.svg;n=n.parentNode)if(n.getAttribute)o*=+(n.getAttribute('opacity')??1)*+(getComputedStyle(n).opacity);return +o.toFixed(3)};
 const objs=Object.fromEntries(${JSON.stringify(ids.split(','))}.map(i=>[i,op(i)]));
 const ex=[...p.dom].filter(([id])=>/^ar\\.expression\\.[a-z]+$/.test(id)).map(([id,e])=>[id.split('.').pop(),+(+e.getAttribute('opacity')).toFixed(3)]).filter(([,o])=>o>0.001);
 return {rect:[r.x,r.y,r.width,r.height],objs,ex}})()`);
 const [x,y,w]=ev.rect,k=w/1200;
 const shot=await c.send('Page.captureScreenshot',{format:'png',clip:{x:x+(+cx)*k,y:y+(+cy)*k,width:(+cw)*k,height:(+ch)*k,scale:1.5}});
 const name=`${theme}-${String(ms).padStart(5,'0')}.png`;await fs.writeFile(`${out}/${name}`,Buffer.from(shot.data,'base64'));
 report.push({theme,ms,...ev.objs,expressions:ev.ex});}
}finally{await c.close()}
await fs.writeFile(`${out}/report.json`,JSON.stringify(report,null,1));
const bad=report.filter(r=>{const v=Object.entries(r).filter(([k])=>!['theme','ms','expressions'].includes(k)).map(([,v])=>v);return v.some(o=>o>0.01&&o<0.99)||r.expressions.length!==1&&r.expressions.some(([,o])=>o<0.99);});
console.log(JSON.stringify({frames:report.length,partial:bad.map(r=>r.theme+'@'+r.ms+' '+JSON.stringify(r))},null,1));
