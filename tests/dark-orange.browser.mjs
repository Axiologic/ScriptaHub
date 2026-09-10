import assert from 'node:assert/strict';import {connect} from './browser-session.mjs';
const base='http://127.0.0.1:8012/';const c=await connect(base+'index.html');let checks=0;
try{
 await c.wait('!!document.querySelector("[data-theme-toggle]")');await c.evaluate(`localStorage.setItem('scripta-site-theme','dark-orange');localStorage.setItem('scripta-site-dark-theme','dark-orange')`);
 for(const route of ['index.html?lang=en','books/the/first/wake/bk-409c27f5b4524932/en/book.html?lang=en','create/index.html?lang=en','librarian/index.html?lang=en#request=science','legal/notice.html?lang=en']){
  await c.send('Page.navigate',{url:base+route});await c.wait(`document.querySelector('[data-theme-toggle]')?.dataset.themeCurrent==='dark-orange'`);
  if(route.startsWith('index'))await c.wait('!document.querySelector("[data-home-loading]")');
  for(const width of [1366,393]){await c.size(width,900);await c.wait('document.documentElement.scrollWidth<=innerWidth');
   const state=await c.evaluate(String.raw`(()=>{const root=getComputedStyle(document.documentElement),green=v=>{const m=v.match(/^rgba?\((.*)\)$/);if(!m)return false;const [r,g,b]=m[1].split(',').map(Number);return g>r*1.2&&g>b*1.08&&g-r>12};const bad=[];for(const e of document.querySelectorAll('body *')){if(!e.getBoundingClientRect().width||e.closest('svg'))continue;const s=getComputedStyle(e);for(const prop of ['color','backgroundColor','borderTopColor'])if(green(s[prop]))bad.push(e.tagName+'.'+e.className+':'+prop+'='+s[prop])}return {bad,canvas:root.getPropertyValue('--canvas').trim(),accent:root.getPropertyValue('--green').trim(),scheme:root.colorScheme}})()`);
   assert.deepEqual(state.bad,[],route);assert.equal(state.canvas,'#000000');assert.equal(state.accent,'#ff7900');assert.equal(state.scheme,'dark');checks++;
  }
 }
 await c.send('Page.navigate',{url:base+'index.html?lang=en'});await c.wait(`document.querySelector('[data-theme-toggle]')?.dataset.themeCurrent==='dark-orange'`);await c.size(1366,900);await c.wait('!document.querySelector("[data-home-loading]")');assert.equal(await c.evaluate("getComputedStyle(document.querySelector('.site-footer')).backgroundColor"),'rgb(255, 121, 0)');await c.capture('/tmp/dark-orange-home.png');
 await c.evaluate(`document.querySelector('[data-theme-toggle]').click()`);assert.equal(await c.evaluate('document.documentElement.dataset.theme'),'light');checks++;
 await c.evaluate(`localStorage.setItem('scripta-site-theme','dark')`);await c.send('Page.reload');await c.wait(`document.documentElement?.dataset.theme==='dark' && !!document.querySelector('[data-theme-toggle]')`);assert.equal(await c.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--canvas').trim()"),'#000000');assert.equal(await c.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--green').trim()"),'#9af2c6');await c.capture('/tmp/dark-green-home.png');checks++;
 await c.evaluate(`document.querySelector('[data-theme-toggle]').click()`);assert.equal(await c.evaluate('localStorage.getItem("scripta-site-theme")'),'dark-orange');checks++;
 await c.send('Page.navigate',{url:base+'books/the/first/wake/bk-409c27f5b4524932/en/book.html?lang=en'});await c.wait('!!document.querySelector("[data-reading-format=short]")');const reader=await c.evaluate('document.querySelector("[data-reading-format=short]").href');await c.send('Page.navigate',{url:reader});await c.wait(`document.querySelector('[data-reader-app]')?.dataset.theme==='night'`);
 assert.equal(await c.evaluate('document.querySelector("[data-reader-app]").dataset.darkAccent'),'dark-orange');await c.evaluate(`document.querySelector('[data-reader-theme]').click();document.querySelector('[data-reader-theme]').click()`);assert.equal(await c.evaluate('localStorage.getItem("scripta-site-theme")'),'dark-orange');checks++;
 assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,errors:0}));
}finally{await c.close()}
