import fs from 'node:fs/promises';import assert from 'node:assert/strict';import {connect} from '../../tests/browser-session.mjs';
const catalogue=JSON.parse(await fs.readFile('docs/collection.json')),reports=[];
for(const id of ['bk-049d00ef0ab54f38','bk-97983c60498d4a09']){
 const book=catalogue.books.find(b=>b.id===id),base='http://127.0.0.1:8128/',c=await connect('about:blank');
 try{
  await c.send('Page.addScriptToEvaluateOnNewDocument',{source:`const define=customElements.define.bind(customElements);customElements.define=(name,C,...args)=>{if(name==='shf-player'){const connected=C.prototype.connectedCallback;C.prototype.connectedCallback=function(){this.setMuted(true);return connected.call(this)}}return define(name,C,...args)};`});
  await c.send('Page.navigate',{url:base+book.editions.ro.book+'?lang=ro'});await c.wait('!!document.querySelector("[data-animation-link]")');
  const link=await c.evaluate('document.querySelector("[data-animation-link]").href');assert.equal(new URL(link).searchParams.get('lang'),'ro');assert.ok(link.includes('/Animation/index.html'));
  await c.send('Page.navigate',{url:base+book.animation.page+'?lang=ro'});await c.wait('!!document.querySelector("shf-player")?.film');
  const result=await c.evaluate(`(()=>{const p=document.querySelector('shf-player');return {language:p.film.language,edition:p.film.editorial.sourceEdition,durationMs:p.durationMs,muted:p.muted,playing:p.playing,themeChoices:p.shadowRoot.querySelectorAll('[data-player-theme]').length,feedback:!!document.querySelector('.animation-feedback form'),overflow:document.documentElement.scrollWidth>innerWidth,back:new URL(document.querySelector('[data-animation-back]').href).searchParams.get('lang')}})()`);
  assert.equal(result.language,'en');assert.equal(result.edition,'edition-2');assert.equal(result.muted,true);assert.equal(result.playing,false);assert.equal(result.themeChoices,3);assert.equal(result.feedback,true);assert.equal(result.back,'ro');assert.equal(result.overflow,false);assert.ok(result.durationMs<=120000);assert.equal(c.errors.length,0);reports.push({id,...result});
 }finally{await c.close()}
}
await fs.writeFile('.book-work/ai-maintenance-20261111/public-integration.json',JSON.stringify({valid:true,books:reports,audiblePlayback:false},null,2)+'\n');console.log(JSON.stringify(reports));
