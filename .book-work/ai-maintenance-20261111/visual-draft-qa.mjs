import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';
import {connect} from '../../tests/browser-session.mjs';import {findLabelOverflow} from '../../tools/shf/text-bounds.mjs';
const results=[];
try{
 for(const slug of ['symbolic-world-models','an-intuitive-introduction-to-machine-learning'])for(const theme of ['color','paper','night']){
  const c=await connect('about:blank');try{
   await c.send('Network.enable');await c.send('Network.setBlockedURLs',{urls:['http://*','https://*']});
   await c.send('Page.navigate',{url:pathToFileURL(path.resolve('presentations',slug,'qa/visual-draft.html')).href});
   await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
   await c.evaluate(`window.p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.setTheme('${theme}');p.$('centerPlay').style.visibility='hidden';document.fonts.ready`);
   let offset=0;const scenes=await c.evaluate('p.film.scenes.map(s=>({durationMs:s.durationMs,beats:s.beats}))');
   const folder=path.join('presentations',slug,'qa/draft-shots');await fs.mkdir(folder,{recursive:true});
   for(let index=0;index<scenes.length;index++){
    for(const [beatIndex,beat]of scenes[index].beats.entries()){
     await c.evaluate(`p.seek(${offset+(beat.startMs+beat.spokenEndMs)/2})`);
     await c.evaluate('new Promise(r=>setTimeout(r,180))');
     const data=await c.evaluate(`(()=>{const box=p.$('caption').getBoundingClientRect();return{overflow:(${findLabelOverflow.toString()})(p.svg),captionCollision:[...p.svg.querySelectorAll('text')].filter(t=>{let opacity=1;for(let a=t;a&&a!==p.svg.parentNode;a=a.parentNode){opacity*=Number(getComputedStyle(a).opacity)}if(opacity<.1)return false;const r=t.getBoundingClientRect();return Math.min(r.right,box.right)-Math.max(r.left,box.left)>2&&Math.min(r.bottom,box.bottom)-Math.max(r.top,box.top)>2}).map(t=>t.textContent),font:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)}})()`);
     results.push({slug,theme,scene:index,beat:beatIndex,...data});await c.capture(path.join(folder,`${theme}-${index}-${beatIndex}.png`));
    }offset+=scenes[index].durationMs;
   }
   await c.size(393,900);await c.evaluate('p.seek(1000)');await c.capture(path.join(folder,`${theme}-phone.png`));
   if(c.errors.length)throw Error(JSON.stringify(c.errors));
  }finally{await c.close()}
 }
 await fs.writeFile('.book-work/ai-maintenance-20261111/draft-geometry.json',JSON.stringify(results,null,2)+'\n');
 const failures=results.filter(r=>r.overflow.length||r.captionCollision.length);console.log(JSON.stringify({frames:results.length,failures},null,2));if(failures.length)process.exitCode=1;
}finally{
 const endpoint=process.env.SCRIPTA_CDP_URL;const v=await(await fetch(endpoint+'/json/version')).json();const ws=new WebSocket(v.webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r,{once:true}));ws.send(JSON.stringify({id:1,method:'Browser.close'}));await new Promise(r=>ws.addEventListener('close',r,{once:true}));
}
