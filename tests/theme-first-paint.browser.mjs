import assert from 'node:assert/strict';import {connect} from './browser-session.mjs';
const base='http://127.0.0.1:8012/';const c=await connect(base+'index.html');let checks=0;
const navigation=async(method,params={})=>{let resolve;const loaded=new Promise(r=>{resolve=r});c.on('Page.loadEventFired',()=>resolve());await c.send(method,params);let timer;try{await Promise.race([loaded,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('Navigation timeout')),30000)})]);}finally{clearTimeout(timer)}};
try{
 await c.send('Network.enable');await c.send('Network.setCacheDisabled',{cacheDisabled:true});
 // Leave synchronous inline bootstraps and CSS available, but prevent all application JS.
 await c.send('Network.setBlockedURLs',{urls:['*.js','*.js?*']});
 for(const theme of ['orange','nord','dark','dark-orange']){
  await c.evaluate(`localStorage.setItem('scripta-site-theme','${theme}');localStorage.setItem('scripta-site-scale-v2','1.5')`);
  for(const route of ['index.html','create/index.html','books/the/first/wake/bk-409c27f5b4524932/en/book.html','books/the/first/wake/bk-409c27f5b4524932/Animation/index.html','reader/index.html']){
   await navigation('Page.navigate',{url:base+route});await c.wait('document.readyState==="complete"');
   const state=await c.evaluate(`({font:parseFloat(getComputedStyle(document.documentElement).fontSize),theme:document.documentElement.dataset.theme,scheme:getComputedStyle(document.documentElement).colorScheme,appTheme:document.querySelector('[data-reader-app]')?.dataset.theme,appAccent:document.querySelector('[data-reader-app]')?.dataset.darkAccent})`);
   assert.equal(state.font,route.startsWith('reader/')?19.84:29.76,route+' saved size before application JS');assert.equal(state.theme,theme,route+' before application JS');assert.equal(state.scheme,theme.startsWith('dark')?'dark':'light');if(route.startsWith('reader/')){assert.equal(state.appTheme,theme.startsWith('dark')?'night':'paper');assert.equal(state.appAccent,theme)}checks++;
   await navigation('Page.reload',{ignoreCache:true});await c.wait('document.readyState==="complete"');assert.equal(await c.evaluate('document.documentElement.dataset.theme'),theme,route+' refresh before JS');checks++;
  }
 }
 console.log(JSON.stringify({checks,applicationScriptsBlocked:true,audiblePlayback:false}));
}finally{await c.evaluate("localStorage.setItem('scripta-site-scale-v2','1')");await c.close()}
