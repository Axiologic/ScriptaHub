import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {connect} from '../../tests/browser-session.mjs';
const root=process.argv[2],production=JSON.parse(await fs.readFile(root+'/work/production.json'));
const url=pathToFileURL(path.resolve(root,'exports',production.filmId+'.html')).href;
const scenes=JSON.parse(await fs.readFile(root+'/work/scenes.json'));
await fs.mkdir(root+'/qa/screenshots/fresh',{recursive:true});
for(const theme of ['color','paper','night'])for(let index=0;index<scenes.length;index++){
 const c=await connect(url);
 try{
  await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
  await c.evaluate(`window.p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.setTheme('${theme}');p.$('centerPlay').style.visibility='hidden';`);
  await c.evaluate(`(()=>{const s=p.film.scenes[${index}],b=s.beats.at(-1);p.seek(p.film.scenes.slice(0,${index}).reduce((n,s)=>n+s.durationMs,0)+(b.startMs+b.spokenEndMs)/2)})()`);
  await c.evaluate('document.fonts.ready');
  await c.evaluate('p.sceneIndex=-1;p.render(p.currentTimeMs);new Promise(r=>setTimeout(r,700))');
  await c.capture(root+`/qa/screenshots/fresh/${theme}-${index}.png`);
 }finally{await c.close()}
}
console.log('Fresh paused scene captures complete; no playback.');
