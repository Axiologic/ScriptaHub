import assert from 'node:assert/strict';import {connect} from './browser-session.mjs';
const c=await connect('http://127.0.0.1:8012/books/the/first/wake/bk-409c27f5b4524932/en/book.html?lang=en');let checks=0;
try{
 await c.wait('!!document.querySelector(".book-side-actions")');
 for(const width of [1920,1366,1100,720,393,320]){
  await c.size(width,1000);await c.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
  const state=await c.evaluate(`(()=>{const primary=document.querySelector('.book-actions'),side=document.querySelector('.book-side-actions'),box=n=>{const r=n.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom}};return {first:primary.firstElementChild.hasAttribute('data-animation-link'),count:side.children.length,primary:box(primary),copy:box(document.querySelector(".book-copy")),side:box(side),buttons:[...side.children].map(box),overflow:document.documentElement.scrollWidth>innerWidth,clip:[...side.children].some(e=>e.scrollWidth>e.clientWidth+1)}})()`);
  assert.equal(state.first,true);assert.equal(state.count,3);assert.equal(state.overflow,false);assert.equal(state.clip,false);
  if(width>1100){assert.ok(Math.abs(state.side.y-state.copy.y)<1);assert.ok(state.side.x>=state.primary.right);assert.ok(state.buttons.every(b=>Math.abs(b.x-state.buttons[0].x)<1&&Math.abs(b.w-state.buttons[0].w)<1));assert.ok(state.buttons[1].y>=state.buttons[0].bottom);assert.ok(state.buttons[2].y>=state.buttons[1].bottom)}
  else assert.ok(state.side.y>=state.primary.bottom);
  if(width===1366||width===393)await c.capture('/tmp/book-actions-'+width+'.png');checks++;
 }
 assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,errors:0}));
}finally{await c.close()}
