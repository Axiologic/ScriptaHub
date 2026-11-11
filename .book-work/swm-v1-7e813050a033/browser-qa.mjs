import {connect} from '../../tests/browser-session.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const work=path.resolve('.book-work/swm-v1-7e813050a033'),qa=path.join(work,'qa');
const final=process.argv.includes('--final'), staged=process.argv.includes('--staged'), results=[];
const book='docs/books/symbolic/world/models/bk-049d00ef0ab54f38';
const pages=staged?['ro','en'].flatMap(l=>['full','short'].map(f=>`${work}/book/${l}/${f}_content.html`)):final?[`${book}/ro/book.html`,`${book}/en/book.html`,'docs/all-books/index.html',...['ro','en'].flatMap(l=>['full','short'].map(f=>`${book}/${l}/${f}_content.html`))]:[`${book}/ro/book.html`,'docs/all-books/index.html',`${work}/book/ro/full_content.html`];
for (const [index,page] of pages.entries()){
 const c=await connect('about:blank');
 try{
  await c.send('Network.enable');await c.send('Network.setBlockedURLs',{urls:['http://*','https://*']});
  await c.send('Page.navigate',{url:pathToFileURL(path.resolve(page)).href+'?lang=ro'});
  await c.wait('document.readyState==="complete"');
  await c.evaluate('document.fonts.ready');
  await c.evaluate('[...document.images].forEach(i=>i.loading="eager")');
  await c.wait('[...document.images].every(i=>i.complete)');
  if(page.includes('full_content.html')){const eq=await c.evaluate('[...document.querySelectorAll("[role=math]")].map(e=>e.textContent)');if(eq.length!==2)throw Error('Expected two legible source equations: '+JSON.stringify(eq));results.push({page,equations:eq});}
  if(page.includes('all-books')){
   const info=await c.evaluate(`(()=>{const a=[...document.querySelectorAll('a')].find(a=>a.href.includes('bk-049d00ef0ab54f38'));return {exists:!!a,shelf:a?.closest('section')?.id,text:a?.textContent}})()`);
   if(!info.exists||info.shelf!=='ai-technology')throw Error(JSON.stringify(info));
   results.push({allBooks:info});
   await c.evaluate(`document.querySelector('input').value='Modele simbolice';document.querySelector('input').dispatchEvent(new Event('input',{bubbles:true}))`);
  }
  for(const width of [1280,390]){
   await c.size(width,900);
   const data=await c.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,title:document.title,brokenImages:[...document.images].filter(i=>!i.naturalWidth).length,htmlLanguage:document.documentElement.lang})');
   results.push({page,width,...data,errors:c.errors});
   if(data.scroll>width+1||data.brokenImages||c.errors.length)throw Error(JSON.stringify(results.at(-1)));
   await c.capture(path.join(qa,`${final?'final':'draft'}-${index}-${width}.png`));
  }
 }finally{await c.close()}
}
await fs.writeFile(path.join(qa,`${final?'final':'draft'}-browser-review.json`),JSON.stringify(results,null,2)+'\n');
console.log('Passed browser checks',results.length);

if(process.argv.includes('--close-browser')){const endpoint=process.env.SCRIPTA_CDP_URL;const v=await(await fetch(endpoint+'/json/version')).json();const ws=new WebSocket(v.webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r,{once:true}));ws.send(JSON.stringify({id:1,method:'Browser.close'}));await new Promise(r=>ws.addEventListener('close',r,{once:true}));}
