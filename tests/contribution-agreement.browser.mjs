import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {connect} from './browser-session.mjs';
const base='http://127.0.0.1:8012/',catalog=JSON.parse(await fs.readFile('docs/collection.json','utf8'));
const book=catalog.books.find(b=>b.id==='bk-409c27f5b4524932');
const c=await connect(base+'create/index.html');let checks=0;
try{
 await c.send('Page.addScriptToEvaluateOnNewDocument',{source:`document.addEventListener('scriptahub:contribution-submit',e=>{e.preventDefault();window.__capturedSubmission=e.detail})`});
 for(const lang of ['en','ro','fr','de','es','pt','it','pl'])for(const route of ['create/index.html','fork/index.html','feedback/index.html','animation-request/index.html',book.animation.page]){
  await c.send('Page.navigate',{url:base+route+'?lang='+lang+'&book='+encodeURIComponent(route===book.animation.page?catalog.books.find(b=>b.id!==book.id).directory:book.directory)});
  await c.wait(`!!document.querySelector('[data-workflow-form]')&&document.documentElement.lang==='${lang}'`);
  assert.equal(await c.evaluate('!!document.querySelector("[data-contract-accept]")'),false);
  await c.evaluate(`(()=>{const f=document.querySelector('[data-workflow-form]');f.elements.name.value='Test contributor';if(f.elements.prompt)f.elements.prompt.value='A specific derived-book instruction';if(f.elements.feedback)f.elements.feedback.value='Clarify this specific argument';if(f.elements.documents){const dt=new DataTransfer();dt.items.add(new File(['sample'],'source.txt'));f.elements.documents.files=dt.files;f.elements.documents.dispatchEvent(new Event('change'));}f.requestSubmit()})()`);
  await c.wait('location.pathname.endsWith("/agreement/index.html")&&!!document.querySelector("[data-agreement-form]")');
  assert.equal(await c.evaluate('document.documentElement.lang'),lang);
  assert.equal(await c.evaluate('document.querySelector("[data-contract-accept]").checked'),false);
  assert.equal(await c.evaluate('document.querySelector("[data-agreement-form] button").disabled'),true);
  assert(!await c.evaluate('location.search.includes("Test")'));
  await c.evaluate('document.querySelector("[data-agreement-form]").dispatchEvent(new Event("submit",{cancelable:true}))');
  assert(!await c.evaluate('!!window.__capturedSubmission'));
  if(lang==='en'&&route==='create/index.html'){
   await c.send('Page.navigate',{url:await c.evaluate('document.querySelector(".workflow-back a").href')});
   await c.wait('!!document.querySelector("[data-workflow-form]")');
   assert.equal(await c.evaluate('document.querySelector("[name=name]").value'),'Test contributor');
   assert((await c.evaluate('document.querySelector("[data-file-selection]").textContent')).includes('source.txt'));
   await c.evaluate('document.querySelector("[data-workflow-form]").requestSubmit()');
   await c.wait('!!document.querySelector("[data-agreement-form]")');
  }
  await c.evaluate('document.querySelector("[data-contract-accept]").click();document.querySelector("[data-agreement-form]").requestSubmit()');
  const sent=await c.evaluate('window.__capturedSubmission');
  assert(sent);const uri=new URL(sent.mailUrl);assert.equal(uri.pathname,'create@scriptahub.com');
  assert(uri.searchParams.get('body').includes('Contribution agreement accepted: yes'));
  assert(uri.searchParams.get('body').includes('Test contributor'));
  if(route!=='create/index.html')assert(uri.searchParams.get('body').includes(book.id));
  if(lang==='en')assert(sent.declaration.includes('on my own responsibility'));
  assert.equal(await c.evaluate('document.querySelectorAll("h1,h2").length'),1);
  if(route==='create/index.html'&&lang==='en')for(const w of [1366,393]){await c.size(w,950);assert(!await c.evaluate('document.documentElement.scrollWidth>innerWidth'));await c.capture('/tmp/agreement-'+w+'.png')}
  checks++;
 }
 // Translation requests also pass through consent; available readers stay direct.
 await c.send('Page.navigate',{url:base+'translate/index.html?lang=en&book='+encodeURIComponent(book.directory)+'&target=pl&format=read'});
 await c.wait('!!document.querySelector("[data-translation-form]")');
 await c.evaluate('document.querySelector("[name=name]").value="Translation tester";document.querySelector("[data-translation-form]").requestSubmit()');
 await c.wait('!!document.querySelector("[data-agreement-form]")');
 await c.evaluate('document.querySelector("[data-contract-accept]").click();document.querySelector("[data-agreement-form]").requestSubmit()');
 assert((await c.evaluate('window.__capturedSubmission.mailUrl')).includes('Translation%20tester'));checks++;
 await c.send('Page.navigate',{url:base+'fork/index.html?book=invalid&lang=en'});await c.wait('!!document.querySelector("h1")');assert(!await c.evaluate('!!document.querySelector("[data-workflow-form]")'));checks++;
 await c.send('Page.navigate',{url:base+'agreement/index.html?lang=en&draft=missing'});await c.wait('!!document.querySelector(".agreement-page")');assert(!await c.evaluate('!!document.querySelector("[data-agreement-form]")'));
 assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,missingDraftBlocked:true,mailIntercepted:true,errors:0}));
}finally{await c.close()}
