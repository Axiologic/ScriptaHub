import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';
import {connect} from '../../tests/browser-session.mjs';import {findLabelOverflow} from '../../tools/shf/text-bounds.mjs';
const specs=JSON.parse(await fs.readFile('.book-work/ai-completion-20261111/film-specs.json')),summary=[];
const pass='pass-'+Date.now();
for(const spec of specs){const frames=[],folder='presentations/'+spec.slug+'/qa/draft-shots/'+pass;await fs.mkdir(folder,{recursive:true});
 for(const theme of ['color','paper','night']){
  const c=await connect(pathToFileURL(path.resolve('presentations',spec.slug,'qa/visual-draft.html')).href);
  try{
   await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');await c.evaluate(`window.p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.setTheme('${theme}');p.$('centerPlay').style.visibility='hidden';document.fonts.ready`);
   let offset=0;const scenes=await c.evaluate('p.film.scenes.map(s=>({durationMs:s.durationMs,beats:s.beats}))');
   for(let i=0;i<scenes.length;i++){
    for(let j=0;j<scenes[i].beats.length;j++){
     const b=scenes[i].beats[j];await c.evaluate(`p.seek(${offset+(b.startMs+b.spokenEndMs)/2});p.sceneIndex=-1;p.render(p.currentTimeMs);new Promise(r=>setTimeout(r,150))`);
     const geometry=await c.evaluate(`(()=>{const caption=p.$('caption').getBoundingClientRect();return {overflow:(${findLabelOverflow.toString()})(p.svg),captionCollisions:[...p.svg.querySelectorAll('text')].filter(t=>{let opacity=1;for(let a=t;a&&a!==p.svg.parentNode;a=a.parentNode)opacity*=Number(getComputedStyle(a).opacity);if(opacity<.1)return false;const r=t.getBoundingClientRect();return Math.min(r.right,caption.right)-Math.max(r.left,caption.left)>2&&Math.min(r.bottom,caption.bottom)-Math.max(r.top,caption.top)>2}).map(t=>t.textContent)}})()`);
     const file=`${folder}/${theme}-${i}-${j}.png`;frames.push({theme,scene:i,beat:j,...geometry,file});if(j===2)await c.capture(file);
    }offset+=scenes[i].durationMs;
   }
   await c.size(393,900);await c.evaluate('p.seek(1000);new Promise(r=>setTimeout(r,200))');await c.capture(`${folder}/${theme}-phone.png`);
   if(c.errors.length)throw Error(JSON.stringify(c.errors));
  }finally{await c.close()}
 }
 const failures=frames.filter(f=>f.overflow.length||f.captionCollisions.length);const result={slug:spec.slug,frames:frames.length,failures,folder};summary.push(result);await fs.writeFile('presentations/'+spec.slug+'/qa/draft-geometry.json',JSON.stringify({measuredAudio:false,valid:!failures.length,...result,checks:frames},null,2)+'\n');console.log(JSON.stringify(result));
}
await fs.writeFile('.book-work/ai-completion-20261111/draft-review.json',JSON.stringify(summary,null,2)+'\n');if(summary.some(r=>r.failures.length))process.exitCode=1;
