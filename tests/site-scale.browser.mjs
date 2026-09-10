import assert from 'node:assert/strict';import {connect} from './browser-session.mjs';
const base='http://127.0.0.1:8012/',c=await connect(base+'index.html?lang=en');let checks=0;
try{
 for(const route of ['index.html?lang=en','books/the/first/wake/bk-409c27f5b4524932/en/book.html?lang=en','create/index.html?lang=en','books/the/first/wake/bk-409c27f5b4524932/Animation/index.html?lang=en']){
  await c.send('Page.navigate',{url:base+route});await c.wait('typeof document.querySelector("[data-site-larger]")?.onclick==="function"');
  for(const width of [1366,393,320])for(const scale of [1,1.5]){
   await c.size(width,1000);await c.evaluate(`document.querySelector('[data-site-size]').click();${scale===1.5?"for(let i=0;i<12;i++)document.querySelector('[data-site-larger]').click();":''}new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);
   const s=await c.evaluate(`(()=>{const rect=e=>e.getBoundingClientRect(),mark=rect(document.querySelector('.wordmark')),tools=rect(document.querySelector('.header-tools')),copy=document.querySelector('.book-copy'),actions=document.querySelector('.book-actions');return{font:parseFloat(getComputedStyle(document.documentElement).fontSize),label:document.querySelector('[data-site-size]').textContent,minus:document.querySelector('[data-site-smaller]').disabled,plus:document.querySelector('[data-site-larger]').disabled,overlap:Math.min(mark.right,tools.right)-Math.max(mark.left,tools.left)>1&&Math.min(mark.bottom,tools.bottom)-Math.max(mark.top,tools.top)>1,overflow:document.documentElement.scrollWidth>innerWidth,copyOverlap:copy&&actions&&innerWidth>1100?rect(copy).bottom>rect(actions).top+1:false,clipped:[...document.querySelectorAll('.book-actions .button')].some(e=>e.scrollWidth>e.clientWidth+1||e.scrollHeight>e.clientHeight+1)}})()`);
   assert(Math.abs(s.font-19.84*scale)<.02,JSON.stringify(s));assert.equal(s.label,scale===1?'100%':'150%');assert.equal(s.minus,scale===1);assert.equal(s.plus,scale===1.5);assert(!s.overlap&&!s.overflow&&!s.copyOverlap&&!s.clipped,route+' '+width+' '+scale+' '+JSON.stringify(s));
   if(route.includes('/en/book.html')&&width!==320)await c.capture('/tmp/site-scale-book-'+width+'-'+scale+'.png');checks++;
  }
 }
 await c.send('Page.reload',{ignoreCache:true});await c.wait('typeof document.querySelector("[data-site-larger]")?.onclick==="function"');assert.equal(await c.evaluate('document.querySelector("[data-site-size]").textContent'),'150%');
 await c.evaluate('document.querySelector("[data-site-size]").click()');assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,persistence:true,errors:0,audiblePlayback:false}));
}finally{await c.close()}
