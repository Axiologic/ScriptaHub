import assert from 'node:assert/strict';
import {connect} from './browser-session.mjs';
import fs from 'node:fs/promises';
const collection=JSON.parse(await fs.readFile(new URL('../docs/collection.json',import.meta.url),'utf8'));
assert.ok(collection.books.some(b=>b.contributions?.some(e=>e.entries.some(x=>x.name==='Axiologic Research SRL'))));
for(const b of collection.books)for(const lang of collection.supportedLanguages){const html=await fs.readFile(new URL('../docs/'+b.editions[lang.code].book,import.meta.url),'utf8');assert.match(html,/data-book-contributors/);}
const book=collection.books[0];
const c=await connect(new URL('../docs/contributors/index.html?book='+encodeURIComponent(book.directory)+'&lang=en',import.meta.url).href);
try{
 await c.size(1400,1000);await c.wait('!!document.querySelector(".contributor-entry")');
 for(const lang of collection.supportedLanguages.map(x=>x.code)){
  await c.evaluate(`document.documentElement.lang=${JSON.stringify(lang)};document.dispatchEvent(new CustomEvent('scriptahub:language',{detail:{language:${JSON.stringify(lang)}}}))`);
  const result=await c.evaluate(`(()=>{const e=document.querySelector('.contributor-entry');return{author:e.querySelector('th a').textContent,url:e.querySelector('th a').href,project:e.querySelector('p a').href,text:e.querySelector('p').textContent,fields:e.querySelectorAll('input,label').length}})()`);
  assert.equal(result.author,'Axiologic Research SRL');assert.equal(result.url,'https://www.axiologic.net/');assert.equal(result.project,'https://www.achilles-project.eu/');assert.match(result.text,/SCRIPTA/);assert.equal(result.fields,0);
 }
 for(const width of [1400,768,393,320]){await c.size(width,1000);assert.equal(await c.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),true);}
 await c.evaluate(`(()=>{const b=SCRIPTA_COLLECTION.books.find(b=>b.directory===new URLSearchParams(location.search).get('book'));b.contributions.unshift({edition:'edition-test',number:99,label:{en:'Edition test'},entries:[{name:'A Person',url:'https://example.org/person',description:{en:'Specific feedback on the argument.'}},{name:'Unsafe <name>',url:'javascript:alert(1)',description:{en:['Literal <text> ',{label:'unsafe',url:'javascript:alert(1)'}]}}]});document.documentElement.lang='en';document.dispatchEvent(new CustomEvent('scriptahub:language',{detail:{language:'en'}}))})()`);
 assert.equal(await c.evaluate('document.querySelectorAll(".contribution-edition").length>=2'),true);
 assert.equal(await c.evaluate('[...document.links].filter(a=>a.protocol === "javascript:").length'),0);
 assert.equal(await c.evaluate('document.querySelectorAll(".contributor-entry th a").length'),2);
 assert.equal(c.errors.length,0);
 console.log(`Contributors:${collection.bookCount} books×8 links,8 localized pages,4 widths,file opening,multiple edition credits and escaped unsafe links passed.`);
}finally{await c.close()}
