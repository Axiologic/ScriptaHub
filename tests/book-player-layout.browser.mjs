import assert from 'node:assert/strict';
import {connect} from './browser-session.mjs';
const base='http://127.0.0.1:8012/';
const c=await connect(base+'books/the/first/wake/bk-409c27f5b4524932/Animation/index.html?lang=en');let checks=0;
try{
 await c.wait('!!document.querySelector("shf-player")?.film');
 await c.evaluate('document.querySelector("shf-player").setMuted(true)');
 for(const width of [1920,1366,720,393,320]){
  await c.size(width,1000);await c.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
  const r=await c.evaluate(`(()=>{const p=document.querySelector('shf-player'),f=document.querySelector('.animation-player-floor'),b=document.querySelector('[data-animation-back]'),shell=document.querySelector('.animation-page'),box=e=>e.getBoundingClientRect().toJSON(),style=getComputedStyle(shell);return{host:box(p),stage:box(p.$('stage')),floor:box(f),close:box(b),available:shell.clientWidth-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight),overflow:document.documentElement.scrollWidth>innerWidth,playing:p.playing}})()`);
  assert(Math.abs(r.host.width-Math.min(1100,r.available))<2,`player fills host at ${width}: ${r.host.width}`);
  assert(r.stage.width>=r.host.width-2);assert(r.close.bottom<=r.stage.top+1);assert(Math.abs(r.close.right-r.host.right)<2);assert(!r.overflow);assert(!r.playing);
  if(width===1366||width===393)await c.capture('/tmp/book-player-fixed-'+width+'.png');checks++;
 }
 assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,errors:0,audiblePlayback:false}));
}finally{await c.close()}
