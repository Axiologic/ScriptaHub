// Shared silent integration checks; never opens an output audio device.
// Usage: node tools/shf/qa-film.mjs presentations/<book-slug>
import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';
import {connect} from '../../tests/browser-session.mjs';
const root=path.resolve(process.argv[2]||'');if(!process.argv[2])throw Error('Provide a presentation workspace.');
const production=JSON.parse(await fs.readFile(path.join(root,'work/production.json'),'utf8'));
const out=path.join(root,'qa'),shots=path.join(out,'screenshots');await fs.mkdir(shots,{recursive:true});
const c=await connect(pathToFileURL(path.join(root,'exports',production.id+'.html')).href);
const checks=[],frames=[];let audio;
const test=async(name,expression)=>{const result=await c.evaluate(expression);checks.push({name,pass:!!result});if(!result)throw Error(name);return result};
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
 await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause()');
 await test('English film starts paused without an audio output','p.film.language==="en"&&!p.playing&&!p.audio.ctx');
 await test('one sentence in every narration beat','p.film.scenes.every(s=>s.beats.every(b=>SHF.core.splitSentences(b.text,"en").length===1))');
 await test('book invitation and source evidence retained','p.film.editorial.purpose==="book-introduction"&&p.film.editorial.readerInvitation.readerOutcomes.length>0&&p.film.editorial.sourceSha256.length===64');
 await test('authored emotional plan retained','p.film.scenes.every(s=>s.emotionalPlan?.states.length===s.beats.length)');
 audio=await c.evaluate('(async()=>{p.audio.ctx=new OfflineAudioContext(1,1,24000);let clips=0;try{for(const scene of p.film.scenes)clips+=(await p.audio.prepare(scene)).clips.length;return {clips,mode:"OfflineAudioContext decode only",audiblePlayback:false};}finally{p.audio.clear();p.audio.ctx=null}})()');
 const sentences=await c.evaluate('p.film.scenes.reduce((n,s)=>n+s.beats.length,0)');if(audio.clips!==sentences)throw Error('Audio count does not match script');
 for(const theme of ['color','paper','night']){
  await c.evaluate(`p.setTheme('${theme}')`);const durations=await c.evaluate('p.film.scenes.map(s=>s.durationMs)');let start=0;
  for(let i=0;i<durations.length;i++){
   for(const [label,ratio]of [['first',.08],['middle',.5],['last',.96]]){
    const result=await c.evaluate(`(()=>{p.seek(${start+durations[i]*ratio});const invalid=[...p.svg.querySelectorAll('[transform]')].some(e=>/NaN|Infinity/.test(e.getAttribute('transform')));const unresolved=[...p.svg.querySelectorAll('[fill],[stroke]')].some(e=>((e.getAttribute('fill')||'')+(e.getAttribute('stroke')||'')).includes('$'));const inv=p.dom.get('$camera').getCTM().inverse();const connections=p.film.scenes[${i}].connections.every(c=>[[c.from,false],[c.to,true]].every(([port,last])=>{const xy=p.defs.get(port.node).anchors[port.anchor],pt=p.svg.createSVGPoint();pt.x=xy[0];pt.y=xy[1];const a=pt.matrixTransform(p.dom.get(port.node).getCTM()).matrixTransform(inv),line=p.dom.get(c.id)._shape,b=line.getPointAtLength(last?line.getTotalLength():0);return Math.hypot(a.x-b.x,a.y-b.y)<.1}));return {invalid,unresolved,connections}})()`);
    frames.push({theme,scene:i,frame:label,...result});
    const clip=await c.evaluate('(()=>{const r=p.$("stage").getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height,scale:.6}})()');
    await c.evaluate('document.fonts.ready.then(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))))');
    const shot=await c.send('Page.captureScreenshot',{format:'png',clip});await fs.writeFile(path.join(shots,`${theme}-${String(i).padStart(2,'0')}-${label}.png`),Buffer.from(shot.data,'base64'));
   }start+=durations[i];
  }
 }
 if(frames.some(f=>f.invalid||f.unresolved||!f.connections))throw Error('Invalid sampled geometry, token or connection');
 for(const width of [1200,720,540,393,320]){
  await c.size(width,960);
  await test('transport buttons fit '+width,'(()=>{const r=p.getBoundingClientRect();return [...p.shadowRoot.querySelectorAll(".controls button")].filter(b=>getComputedStyle(b).display!=="none").every(b=>{const a=b.getBoundingClientRect();return a.left>=r.left-1&&a.right<=r.right+1})})()');
  await test('captions match one whole sentence and fit '+width,'(()=>{let start=0;for(const s of p.film.scenes){for(const b of s.beats){p.seek(start+(b.startMs+b.spokenEndMs)/2);const cap=p.$("captionbox").getBoundingClientRect(),art=p.$("art").getBoundingClientRect(),bar=p.$("transport").getBoundingClientRect();if(p.$("caption").textContent!==b.text||(innerWidth<=720&&cap.top<art.bottom-1)||cap.bottom>bar.top+20)return false}start+=s.durationMs}return true})()');
  if(width===393||width===320){await c.evaluate('p.seek(2000)');await c.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');await c.capture(path.join(shots,'phone-'+width+'.png'))}
 }
 await c.evaluate('p.seek(20000);window.referenceSVG=p.captureSVG();p.seek(p.durationMs*.8);p.seek(20000)');await test('seeking A-B-A is deterministic','p.captureSVG()===referenceSVG');
 const report={durationMs:await c.evaluate('p.durationMs'),sentences,checks,audio,sampledFrames:frames.length,frames,jsErrors:c.errors,audiblePlayback:false,fullPlayback:false,completeListeningReview:false,visualInspection:'Screenshots produced for separate human/agent inspection; geometry checks do not certify visual quality.',physicalDeviceTesting:false};
 await fs.writeFile(path.join(out,'browser-review.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({durationMs:report.durationMs,sentences,checks:checks.length,sampledFrames:frames.length,errors:c.errors.length}));if(c.errors.length)process.exitCode=1;
}finally{await c.close()}
