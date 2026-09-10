import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {connect} from './browser-session.mjs';
const base=process.env.SCRIPTA_TEST_URL||'http://127.0.0.1:8012/';
const catalogue=JSON.parse(await fs.readFile(new URL('../docs/collection.json',import.meta.url),'utf8'));
const missing=catalogue.books.find(b=>!b.animation), ready=catalogue.books.find(b=>b.animation);
const c=await connect('about:blank');let checks=0;
let outgoing='';c.on('Page.frameRequestedNavigation',e=>{if(e.url.startsWith('mailto:'))outgoing=e.url});
try{
 for(const lang of ['en','ro','fr','de','es','pt','it','pl']){
  await c.size(lang==='ro'?393:1200,900);
  await c.send('Page.navigate',{url:base+missing.editions[lang].book+'?lang='+lang});await c.wait('!!document.querySelector("[data-fork-link]")');
  const links=await c.evaluate(`[...document.querySelectorAll('[data-animation-link],[data-fork-link]')].map(a=>a.href)`);
  assert.equal(links.length,2);
  for(const href of links){
   assert.equal(new URL(href).searchParams.get('book'),missing.directory);assert.equal(new URL(href).searchParams.get('lang'),lang);
   await c.send('Page.navigate',{url:href});await c.wait('!!document.querySelector("form")');
   const state=await c.evaluate(`(()=>{const f=document.querySelector('form');return {lang:document.documentElement.lang,heading:document.querySelector('h1').textContent,book:document.querySelector('[data-book-id]').dataset.bookId,back:document.querySelector('.workflow-back a').href,disabled:f.querySelector('[type=submit]').disabled,files:!!f.elements.documents,overflow:document.documentElement.scrollWidth>innerWidth+1}})()`);
   assert.equal(state.lang,lang);assert.equal(state.book,missing.id);assert.equal(new URL(state.back).pathname,'/'+missing.editions[lang].book);assert.equal(state.disabled,true);assert.equal(state.files,href.includes('/fork/'));assert.equal(state.overflow,false);checks++;
  }
 }
 // Exercise actual form serialization in this isolated headless browser. No email is sent.
 await c.evaluate(`(()=>{const f=document.querySelector('form');f.elements.name.value='QA';f.elements.prompt.value='New audience and narrower scope';f.elements.titles.value='Derived title';const d=new DataTransfer();d.items.add(new File(['source'],'context.txt',{type:'text/plain'}));f.elements.documents.files=d.files;f.elements.documents.dispatchEvent(new Event('change'));document.querySelector('[data-contract-accept]').click();f.requestSubmit()})()`);
 for(let i=0;!outgoing&&i<20;i++)await new Promise(r=>setTimeout(r,100));
 assert.ok(outgoing.startsWith('mailto:create@scriptahub.com'));const body=new URL(outgoing).searchParams.get('body');
 for(const value of [missing.id,missing.title.en,missing.directory,'context.txt','Derived title','New audience and narrower scope','Source edition:'])assert.ok(body.includes(value),value);checks++;
 await c.send('Page.navigate',{url:base+ready.animation.page+'?lang=ro&book='+encodeURIComponent(missing.directory)});await c.wait('!!document.querySelector("shf-player")?.film && !!document.querySelector("[data-workflow-form]")');
 const embedded=await c.evaluate(`(()=>{const p=document.querySelector('shf-player'),f=document.querySelector('[data-workflow-content]');return {below:f.getBoundingClientRect().top>=p.getBoundingClientRect().bottom,playing:p.playing,audio:!!p.audio.ctx,title:document.title,heading:f.querySelector('h2').textContent,kind:!!f.querySelector('[name=kind]')}})()`);
 assert.equal(embedded.below,true);assert.equal(embedded.playing,false);assert.equal(embedded.audio,false);assert.ok(embedded.title.includes(ready.title.ro||ready.title.en));assert.equal(embedded.heading,'Îmbunătățește prezentarea');assert.equal(embedded.kind,false);checks++;
 outgoing='';await c.evaluate(`(()=>{const f=document.querySelector('form');f.elements.name.value='QA';f.elements.feedback.value='Explain the central reading benefit earlier';document.querySelector('[data-contract-accept]').click();f.requestSubmit()})()`);
 for(let i=0;!outgoing&&i<20;i++)await new Promise(r=>setTimeout(r,100));
 const feedback=new URL(outgoing).searchParams.get('body');assert.ok(feedback.includes(ready.id));assert.ok(!feedback.includes(missing.id));assert.ok(feedback.includes(ready.animation.shf));assert.ok(feedback.includes('Animation improvement'));checks++;
 await c.send('Page.navigate',{url:base+'fork/index.html?book=invalid&lang=en'});await c.wait('!!document.querySelector("h1")');assert.equal(await c.evaluate('!!document.querySelector("form")'),false);checks++;
 assert.equal(c.errors.length,0,JSON.stringify(c.errors));console.log(JSON.stringify({checks,languages:8,audiblePlayback:false,emailSent:false}));
}finally{await c.close()}
