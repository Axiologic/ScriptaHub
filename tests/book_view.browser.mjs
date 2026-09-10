// Run against a local HTTP server and Chromium --remote-debugging-port=9222.
import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
const site = process.env.SCRIPTA_TEST_URL || 'http://127.0.0.1:8000/docs/';
const tabs = await (await fetch((process.env.SCRIPTA_CDP_URL || 'http://127.0.0.1:9222') + '/json/list')).json();
const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));
let id = 0; const pending = new Map(), errors = [];
ws.addEventListener('message', e => { const m = JSON.parse(e.data); if(m.id) { const p=pending.get(m.id); pending.delete(m.id); m.error ? p.reject(m.error) : p.resolve(m.result); } if(m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text); });
const call = (method, params={}) => new Promise((resolve,reject) => {pending.set(++id,{resolve,reject}); ws.send(JSON.stringify({id,method,params}));});
const evaluate = async expression => {const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true}); if(r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails)); return r.result.value;};
const wait = ms => new Promise(r=>setTimeout(r,ms));
try {
 await call('Runtime.enable'); errors.length = 0; await call('Page.enable');
 await call('Emulation.setEmulatedMedia',{features:[]});
 await call('Emulation.setDeviceMetricsOverride',{width:1280,height:1000,deviceScaleFactor:1,mobile:false});
 const navigate = async url => {
   await call('Page.navigate',{url});
   for(let i=0;i<100;i++) {await wait(50); if(await evaluate(`location.href === ${JSON.stringify(url)} && document.readyState === 'complete' && typeof ScriptaBookView === 'object'`)) return;}
   throw Error('Shared book view did not load: '+url);
 };
 await navigate(site+'index.html?lang=ro');
 const coverage = await evaluate(`(() => {
   let count = 0; const failures = [];
   for (const book of SCRIPTA_COLLECTION.books) for (const {code} of SCRIPTA_COLLECTION.supportedLanguages) {
     const data = ScriptaBookView.model(book, code);
     if (textShow.split(data.description,code).length !== 6) failures.push(book.id+':'+code+':sentence count');
     for (const variant of ['catalogue','featured','page','librarian','context','compact-context']) {
       const t = document.createElement('template');
       t.innerHTML = ScriptaBookView.markup(book,{variant,language:code,rank:1,relevance:90});
       const description = t.content.querySelector('[data-text-show]');
       if (!description || description.textContent !== book.shortDescription[code]) failures.push(book.id+':'+code+':'+variant+':description');
       if (description.dataset.textShowLoop !== String(variant === 'page')) failures.push(variant+':loop');
       if (t.content.querySelector('[data-intro-controls], [data-intro-read]')) failures.push(variant+':controls');
       count++;
     }
   }
   return {count,failures};
 })()`);
 assert.deepEqual(coverage.failures,[]);
 // Loading gates and dynamic insertion use the same observer, with no explicit mount call.
 await evaluate(`window.fixture = document.createElement('section'); fixture.style='position:fixed;top:150px;left:80px;width:430px;z-index:1000;background:white'; fixture.setAttribute('aria-busy','true'); document.body.append(fixture); fixture.innerHTML=ScriptaBookView.markup(SCRIPTA_COLLECTION.books[0],{language:'ro'}); window.fixtureText=fixture.querySelector('[data-text-show]')`);
 await wait(100);
 assert.equal(await evaluate('fixtureText.dataset.textShowState'),'waiting');
 assert.equal(await evaluate(`getComputedStyle(fixtureText.querySelector('.is-current')).visibility`),'visible');
 await evaluate(`fixture.setAttribute('aria-busy','false')`); await wait(100);
 assert.equal(await evaluate('fixtureText.dataset.textShowState'),'playing');
 await evaluate('fixture.remove()'); await wait(50);
 assert.equal(await evaluate('textShow.get(fixtureText) === undefined'),true);
 // Looping is enabled on an actual book page, using the same instance API.
 const book = await evaluate(`SCRIPTA_COLLECTION.books.find(b=>b.title.en.includes('Executable Natural Language'))`);
 await navigate(new URL(book.editions.ro.book+'?lang=ro',site).href);
 await evaluate(`window.pageText=document.querySelector('.book-copy [data-text-show]');pageText.scrollIntoView({block:'center'});window.player=textShow.get(pageText);`); await wait(100);
 assert.equal(await evaluate('pageText.dataset.textShowLoop'),'true');
 assert.equal(await evaluate('player.sentences.length'),6);
 await evaluate('player.show(5)');
 await wait(await evaluate('player.remaining')+100);
 assert.equal(await evaluate('player.index'),0);
 assert.equal(await evaluate('player.completed'),false);
 // The featured card completes exactly once and remains in place through the last hold.
 await navigate(site+'index.html?lang=ro');
 await evaluate(`document.querySelector('[data-featured-book]').scrollIntoView({block:'center'})`); await wait(150);
 const initial = await evaluate(`document.querySelector('[data-mission-book]').dataset.bookId`);
 await evaluate(`window.featured=textShow.get(document.querySelector('[data-featured-book] [data-text-show]'));featured.show(5)`);
 const remaining=await evaluate('featured.remaining');
 await wait(remaining-120);
 assert.equal(await evaluate(`document.querySelector('[data-mission-book]').dataset.bookId`),initial);
 await wait(700);
 assert.notEqual(await evaluate(`document.querySelector('[data-mission-book]').dataset.bookId`),initial);
 assert.deepEqual(errors,[]);
 console.log('PASS: '+coverage.count+' localized view variants; loading fallback, automatic mount/disposal, page looping and completion-gated carousel.');
} finally {ws.close();}
