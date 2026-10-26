import {connect} from '../../tests/browser-session.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
const work=path.dirname(new URL(import.meta.url).pathname),repo=path.resolve(work,'../..'),qa=path.join(work,'qa/browser');
await fs.mkdir(qa,{recursive:true});
const server=spawn('python3',['-m','http.server','8796','--bind','127.0.0.1','--directory',path.join(repo,'docs')],{stdio:'ignore'});
process.env.SCRIPTA_CDP_URL='http://127.0.0.1:9358';
const browser=spawn('chromium-browser',['--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--disable-component-update','--disable-sync','--disable-extensions','--metrics-recording-only','--no-first-run','--mute-audio','--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1','--remote-debugging-port=9358','--user-data-dir='+path.join(qa,'profile'),'about:blank'],{stdio:'ignore'});
let c;const result=[];
try{
 for(let i=0;i<100;i++){try{await fetch(process.env.SCRIPTA_CDP_URL+'/json/version');await fetch('http://127.0.0.1:8796/');break}catch{await new Promise(r=>setTimeout(r,200));}}
 c=await connect('about:blank');await c.send('Network.enable');await c.send('Network.setCacheDisabled',{cacheDisabled:true});
 await c.send('Fetch.enable',{patterns:[{urlPattern:'*'}]});
 c.on('Fetch.requestPaused',async e=>{const url=e.request.url;await c.send(url.startsWith('http://127.0.0.1:8796/')||url.startsWith('data:')?'Fetch.continueRequest':'Fetch.failRequest',{requestId:e.requestId,...(url.startsWith('http://127.0.0.1:8796/')||url.startsWith('data:')?{}:{errorReason:'BlockedByClient'})});});
 for(const lang of ['en','ro'])for(const width of [1440,390]){
  await c.size(width,900);const book=`http://127.0.0.1:8796/books/an/intuitive/introduction/to/machine/learning/bk-97983c60498d4a09/${lang}/book.html?lang=${lang}`;
  await c.send('Page.navigate',{url:book});await c.wait('document.readyState==="complete" && !!document.querySelector(".book-actions a[download]")');
  await c.evaluate('document.fonts.ready');
  const actions=await c.evaluate('[...document.querySelectorAll(".book-actions a")].map(a=>({text:a.textContent,href:a.href,download:a.hasAttribute("download")}))');
  const download=actions.find(a=>a.download);const resp=await fetch(download.href);if(!resp.ok||!(resp.headers.get('content-type')||'').includes('pdf'))throw Error('PDF download failed '+lang);
  await c.capture(path.join(qa,`${lang}-${width}-book.png`));
  for(const format of ['short','read']){
   const a=actions.find(a=>new URL(a.href).searchParams.get('format')===format);if(!a)throw Error('Missing action '+format);
   await c.send('Page.navigate',{url:a.href});await c.wait('!!document.querySelector(".reader-html-content") && document.querySelector("[data-reader-loading]").hidden');
   await c.evaluate('document.querySelectorAll("img").forEach(i=>i.loading="eager");document.fonts.ready');
   await c.wait('[...document.images].every(i=>i.complete&&i.naturalWidth>0)');
   const state=await c.evaluate(`(()=>{const p=document.querySelector('.reader-html-content'),s=document.querySelector('[data-reader-stage]');return {language:document.documentElement.lang,textLength:p.textContent.length,images:p.querySelectorAll('img').length,math:p.querySelectorAll('math').length,map:p.querySelectorAll('details a').length,download:document.querySelector('[data-reader-download]').href,overflow:s.scrollWidth-s.clientWidth,documentOverflow:document.documentElement.scrollWidth-innerWidth}})()`);
   if(state.textLength<1000||state.documentOverflow>2||state.overflow>2||!state.download.endsWith(`/${lang}/book.pdf`))throw Error('Reader failure '+JSON.stringify(state));
   if(format==='short'&&state.map===0)throw Error('Missing short reader chapter map');
   await c.capture(path.join(qa,`${lang}-${width}-${format}.png`));result.push({lang,width,format,...state});
  }
 }
 const scales=[];
 await c.evaluate('document.querySelector("[data-reader-text-size]").click()');
 for(const target of [80,60,40]){
  await c.evaluate('for(let i=0;i<4;i++)document.querySelector("[data-reader-text-smaller]").click()');
  const actual=await c.evaluate('document.querySelector("[data-reader-text-size]").textContent');
  if(actual!==`${target}%`)throw Error('Reader scale '+actual);scales.push({surface:'reader',target,actual});
 }
 await c.send('Page.reload');await c.wait('!!document.querySelector(".reader-html-content")');
 if(await c.evaluate('document.querySelector("[data-reader-text-size]").textContent')!=='40%')throw Error('Reader preference not retained');
 await c.capture(path.join(qa,'reader-40.png'));
 await c.evaluate('document.querySelector("[data-reader-text-size]").click()');
 await c.send('Page.navigate',{url:'http://127.0.0.1:8796/index.html?lang=ro'});
 await c.wait('document.readyState==="complete" && !!document.querySelector("[data-site-smaller]").onclick');
 await c.evaluate('document.querySelector("[data-site-size]").click()');
 for(const target of [80,60,40]){
  await c.evaluate('for(let i=0;i<4;i++)document.querySelector("[data-site-smaller]").click()');
  const actual=await c.evaluate('document.querySelector("[data-site-size]").textContent');
  if(actual!==`${target}%`)throw Error('Site scale '+actual);scales.push({surface:'home',target,actual});
 }
 await c.send('Page.reload');await c.wait('document.readyState==="complete" && document.querySelector("[data-site-size]").textContent==="40%"');
 await c.capture(path.join(qa,'home-40.png'));await c.evaluate('document.querySelector("[data-site-size]").click()');
 await fs.writeFile(path.join(qa,'report.json'),JSON.stringify({status:'passed',externalRequestsBlocked:true,results:result,scales,exceptions:c.errors},null,2)+'\n');console.log(JSON.stringify({results:result,scales},null,2));
}finally{if(c)await c.close();browser.kill('SIGTERM');server.kill('SIGTERM');}
