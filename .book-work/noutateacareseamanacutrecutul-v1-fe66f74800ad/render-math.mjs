import {connect} from '../../tests/browser-session.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
const w=path.dirname(new URL(import.meta.url).pathname),out=path.join(w,'publication/en/math');await fs.mkdir(out,{recursive:true});
const source=await fs.readFile(path.join(w,'book/en/full_content.html'),'utf8'),math=[...source.matchAll(/<math\b[\s\S]*?<\/math>/g)].map(m=>m[0]);
const markup='<!doctype html><meta charset="utf-8"><style>body{margin:20px;background:white} .equation{display:table;margin:20px 0;padding:5px;font:16px "STIX Two Math","STIX Math",serif;color:black}math{font-size:16px}</style>'+math.map((s,i)=>`<div class="equation" id="eq${i}">${s}</div>`).join('');
const local=path.join(out,'formulas.html');await fs.writeFile(local,markup);
process.env.SCRIPTA_CDP_URL='http://127.0.0.1:9348';
const child=spawn('chromium-browser',['--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--disable-component-update','--disable-sync','--disable-extensions','--metrics-recording-only','--no-first-run','--mute-audio','--host-resolver-rules=MAP * ~NOTFOUND','--remote-debugging-port=9348','--user-data-dir='+path.join(w,'qa/math-browser'),'about:blank'],{stdio:'ignore'});
let c;try{
 for(let i=0;i<80;i++){try{await fetch(process.env.SCRIPTA_CDP_URL+'/json/version');break}catch{await new Promise(r=>setTimeout(r,200))}}
 c=await connect('about:blank');await c.send('Network.enable');await c.send('Network.setBlockedURLs',{urls:['http://*','https://*']});await c.send('Emulation.setDeviceMetricsOverride',{width:1400,height:1800,deviceScaleFactor:3,mobile:false});await c.send('Page.navigate',{url:pathToFileURL(local).href});await c.wait('document.readyState==="complete"');await c.evaluate('document.fonts.ready');
 const rows=[];
 for(let i=0;i<math.length;i++){
  const b=await c.evaluate(`(()=>{const e=document.getElementById('eq${i}'),b=e.getBoundingClientRect();return {x:b.x+scrollX,y:b.y+scrollY,width:b.width,height:b.height,text:e.textContent}})()`);
  const shot=await c.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:b.x,y:b.y,width:b.width,height:b.height,scale:1}});const bytes=Buffer.from(shot.data,'base64'),file=`formula-${String(i+1).padStart(2,'0')}.png`;await fs.writeFile(path.join(out,file),bytes);rows.push({index:i,file,width:b.width,height:b.height,text:b.text,mathML:math[i],mathSha256:createHash('sha256').update(math[i]).digest('hex'),imageSha256:createHash('sha256').update(bytes).digest('hex')});
 }
 await fs.writeFile(path.join(out,'receipt.json'),JSON.stringify({sourceHtmlSha256:createHash('sha256').update(source).digest('hex'),engine:'Chromium native MathML, device scale 3',formulas:rows},null,2)+'\n');console.log('Rendered',rows.length,'unchanged source MathML formulas');
}finally{if(c)await c.close();child.kill('SIGTERM')}
