import assert from 'node:assert/strict';
import {connect} from './browser-session.mjs';
const base='http://127.0.0.1:8012/';
const routes=['index.html?lang=en','create/index.html?lang=en','books/the/first/wake/bk-409c27f5b4524932/en/book.html?lang=en'];
const c=await connect(base+routes[0]);let checks=0;
try{
 for(const route of routes){
  await c.send('Page.navigate',{url:base+route});
  await c.wait('!!document.querySelector("[data-create-link][aria-label]")');
  if(!route.startsWith('index'))await c.wait('!!document.querySelector("[data-header-librarian]")');
  for(const theme of ['light','orange','nord','dark','dark-orange'])for(const width of [320,393,650]){
   await c.size(width,900);await c.evaluate(`document.documentElement.dataset.theme=${JSON.stringify(theme)};new Promise(r=>requestAnimationFrame(r))`);
   const states=await c.evaluate(`([...document.querySelectorAll('.header-create,.header-librarian')].map(e=>{const s=getComputedStyle(e),i=getComputedStyle(e,'::before'),r=e.getBoundingClientRect();return {label:e.getAttribute('aria-label'),icon:i.content,font:parseFloat(i.fontSize),width:parseFloat(i.width),height:parseFloat(i.height),display:i.display,color:i.color,background:s.backgroundColor,inside:r.left>=0&&r.right<=innerWidth}}))`);
   assert.equal(states.length,route.startsWith('index')?1:2);
   for(const s of states){assert(s.label);assert(!['none','normal','""'].includes(s.icon));assert(s.font>=15);assert(s.width>=15&&s.height>=15);assert.notEqual(s.display,'none');assert.notEqual(s.color,s.background);assert(s.inside)}
   if(theme==='dark-orange'&&width===393&&!route.startsWith('index'))await c.capture('/tmp/mobile-header-icons-'+(route.startsWith('create')?'create':'book')+'.png');checks++;
  }
 }
 assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,errors:0,audiblePlayback:false}));
}finally{await c.close()}
