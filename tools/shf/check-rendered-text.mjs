import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL}from'node:url';
import {connect}from'../../tests/browser-session.mjs';import {findLabelOverflow}from'./text-bounds.mjs';
const project=process.argv[2];if(!project)throw Error('Provide project and optional private preview HTML path');
const production=JSON.parse(await fs.readFile(path.join(project,'work/production.json')));
const approved=JSON.parse(await fs.readFile(path.join(project,'work/scenes.json'))).map(s=>({id:s.id,lines:s.lines}));
const html=process.argv[3]||path.join(project,'exports',(production.filmId||production.id)+'.html');
const c=await connect(pathToFileURL(path.resolve(html)).href);const frames=[];
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause();document.fonts.ready');
 const loaded=await c.evaluate('p.film.scenes.map(s=>({id:s.id,lines:s.beats.map(b=>b.text)}))');
 if(JSON.stringify(loaded)!==JSON.stringify(approved)){
  const error='Preview does not contain the current approved script. Build a fresh private preview and pass its HTML path.';
  await fs.writeFile(path.join(project,'qa/label-bounds.json'),JSON.stringify({preview:html,valid:false,frames:[],error},null,2)+'\n');
  throw Error(error);
 }
 for(const theme of ['color','paper','night']){
  const result=await c.evaluate(`(()=>{p.setTheme('${theme}');let offset=0;const frames=[];for(const scene of p.film.scenes){for(const beat of scene.beats){p.seek(offset+(beat.startMs+beat.spokenEndMs)/2);frames.push({scene:scene.id,beat:beat.id,theme:'${theme}',issues:(${findLabelOverflow.toString()})(p.svg)});}offset+=scene.durationMs;}return frames;})()`);frames.push(...result);
 }
 const report={preview:html,scope:'Visible text overflowing sibling backing rectangles at sentence midpoints; not a semantic or full visual approval.',frames,valid:frames.every(frame=>!frame.issues.length)};
 await fs.writeFile(path.join(project,'qa/label-bounds.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({valid:report.valid,frames:frames.length,issues:frames.filter(frame=>frame.issues.length)}));if(!report.valid)process.exitCode=1;
}finally{await c.close()}
