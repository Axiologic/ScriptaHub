import {connect} from '../../../../tests/browser-session.mjs';
const c=await connect('file:///home/salboaie/work/axiologic/ScriptaHub/presentations/beyond-the-last-stone/exports/beyond-the-last-stone-introduction.html');
try{await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
console.log(await c.evaluate(`(async()=>{const p=document.querySelector('shf-player');p.setMuted(true);p.pause();const out=[];let base=0;
for(const [si,sc] of p.film.scenes.entries()){for(const [bi,bt] of sc.beats.entries())for(const f of [.1,.2,.3,.5]){p.seek(base+bt.startMs+Math.round((bt.endMs-bt.startMs)*f));await new Promise(r=>setTimeout(r,120));
for(const [id,e] of p.dom){if(/\\.expression\\.[a-z]+$/.test(id)){const o=+e.getAttribute('opacity');if(o>0.05&&o<0.95)out.push(si+'/'+bi+'@'+f+' '+id+' '+o.toFixed(2));}}}base+=sc.durationMs;}
return out.join('\\n')||'no partial expressions'})()`));
}finally{await c.close()}
