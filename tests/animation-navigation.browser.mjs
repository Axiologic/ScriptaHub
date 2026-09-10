import assert from 'node:assert/strict';import fs from 'node:fs/promises';import {connect} from './browser-session.mjs';
const base=process.env.SCRIPTA_TEST_URL||'http://127.0.0.1:8012/';
const collection=JSON.parse(await fs.readFile(new URL('../docs/collection.json',import.meta.url),'utf8'));
const books=collection.books.filter(b=>b.animation);const c=await connect('about:blank');let checks=0;
try{
 await c.size(1200,900);
 for(const book of books){
  await c.send('Page.navigate',{url:base+book.editions.ro.book+'?lang=ro'});await c.wait('!!document.querySelector("[data-animation-link]")');
  const href=await c.evaluate('document.querySelector("[data-animation-link]").href');assert.equal(new URL(href).pathname,'/'+book.animation.page);assert.equal(new URL(href).searchParams.get('lang'),'ro');checks++;
  await c.send('Page.navigate',{url:href});await c.wait('!!document.querySelector("shf-player")?.film&&!!document.querySelector("[data-home-link]")&&!!document.querySelector(".brand-icon")');
  const state=await c.evaluate(`(()=>{const p=document.querySelector('shf-player');return {duration:p.durationMs,language:p.film.language,playing:p.playing,audio:!!p.audio.ctx,edition:p.film.editorial.sourceEdition,back:document.querySelector('[data-animation-back]').href,home:document.querySelector('[data-home-link]').href,notes:!!document.querySelector('.site-footer,[data-animation-meta],[data-animation-source]'),name:document.querySelector('.brand-icon').src}})()`);
  assert.equal(state.duration,book.animation.durationMs);assert.equal(state.language,'en');assert.equal(state.playing,false);assert.equal(state.audio,false);assert.equal(state.edition,book.animation.edition);assert.equal(new URL(state.back).searchParams.get('lang'),'ro');assert.equal(new URL(state.home).pathname,'/index.html');assert.equal(state.notes,false);checks++;
 }
 assert.equal(c.errors.length,0);console.log(JSON.stringify({books:books.length,checks,errors:0,audiblePlayback:false}));
}finally{await c.close()}
