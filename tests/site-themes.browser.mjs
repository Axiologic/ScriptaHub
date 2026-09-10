import assert from 'node:assert/strict';import {connect} from './browser-session.mjs';
const base=process.env.SCRIPTA_TEST_URL||'http://127.0.0.1:8012/';const c=await connect('about:blank');let checks=0;
try{
 await c.send('Page.navigate',{url:base+'index.html?lang=en'});await c.wait('!!document.querySelector("[data-theme-toggle]")?.dataset.themeCurrent');
 await c.evaluate(`localStorage.setItem('scripta-site-theme','light')`);await c.send('Page.reload');await c.wait(`document.querySelector('[data-theme-toggle]')?.dataset.themeCurrent==='light'`);
 for(const theme of ['orange','nord','dark','light','orange']){
  await c.evaluate(`document.querySelector('[data-theme-toggle]').click()`);
  assert(await c.evaluate(`document.documentElement.dataset.theme==='${theme}'&&localStorage.getItem('scripta-site-theme')==='${theme}'&&document.querySelector('[data-theme-toggle]').getAttribute('aria-label').length>10`));checks++;
 }
 for(const theme of ['orange','nord']){
 await c.evaluate(`localStorage.setItem('scripta-site-theme','${theme}');localStorage.setItem('scripta-site-light-theme','${theme}')`);
 for(const route of ['index.html?lang=en','books/the/first/wake/bk-409c27f5b4524932/en/book.html?lang=en','create/index.html?lang=en','librarian/index.html?lang=en#request=consciousness','legal/notice.html?lang=en']){
  await c.send('Page.navigate',{url:base+route});await c.wait(`document.querySelector('[data-theme-toggle]')?.dataset.themeCurrent==='${theme}'&&document.querySelector('.brand-icon')?.src.includes('librarian-icon-${theme}.svg')`);
  for(const width of [1366,393,320]){
   await c.size(width,900);assert(await c.evaluate('document.documentElement.scrollWidth<=innerWidth'));checks++;
   const result=await c.evaluate(`(()=>{const green=v=>{if(!v.startsWith('rgb'))return false;const [r,g,b]=v.slice(v.indexOf('(')+1,-1).split(',').map(Number);return g>r*1.2&&g>b*1.08&&g-r>12};const bad=[];for(const e of document.querySelectorAll('body *')){if(!e.getBoundingClientRect().width||e.closest('svg'))continue;const s=getComputedStyle(e);for(const prop of ['color','backgroundColor','borderTopColor'])if(green(s[prop]))bad.push(e.tagName+'.'+e.className+':'+prop+'='+s[prop])}return bad})()`);
   assert.deepEqual(result,[],route+' '+theme+' UI');checks++;
  }
 }
 }
 await c.send('Page.navigate',{url:base+'books/the/first/wake/bk-409c27f5b4524932/en/book.html?lang=en'});await c.wait(`document.querySelector('[data-theme-toggle]')?.dataset.themeCurrent==='nord'`);
 const reader=await c.evaluate(`document.querySelector('[data-reading-format="short"]').href`);await c.send('Page.navigate',{url:reader});await c.wait(`document.querySelector('[data-reader-app]')?.dataset.accent==='nord'&&document.querySelector('[data-reader-app]').dataset.theme==='paper'&&!!document.querySelector('.reader-html-content')`);
 await c.wait(`getComputedStyle(document.querySelector('[data-reader-home]')).backgroundColor==='rgb(104, 70, 83)'`);checks++;

 await c.evaluate(`document.querySelector('[data-reader-theme]').click()`);assert(await c.evaluate(`localStorage.getItem('scripta-site-theme')==='dark'`));checks++;
 await c.send('Page.reload');await c.wait(`document.querySelector('[data-reader-app]')?.dataset.theme==='night'&&!!document.querySelector('.reader-html-content')`);
 await c.evaluate(`document.querySelector('[data-reader-theme]').click()`);assert(await c.evaluate(`localStorage.getItem('scripta-site-theme')==='nord'&&document.querySelector('[data-reader-app]').dataset.accent==='nord'`));checks++;
 assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,errors:0}));
}finally{await c.close()}
