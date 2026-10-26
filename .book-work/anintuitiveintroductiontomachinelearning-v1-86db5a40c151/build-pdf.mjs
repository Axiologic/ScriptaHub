import {connect} from '../../tests/browser-session.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
const work=path.dirname(new URL(import.meta.url).pathname);
if(process.argv.includes('--qa')) { await import('./browser-qa.mjs'); process.exit(0); }
const hash=x=>createHash('sha256').update(x).digest('hex');
process.env.SCRIPTA_CDP_URL='http://127.0.0.1:9357';
const browser=spawn('chromium-browser',['--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--disable-component-update','--disable-sync','--disable-extensions','--metrics-recording-only','--no-first-run','--mute-audio','--host-resolver-rules=MAP * ~NOTFOUND','--remote-debugging-port=9357','--user-data-dir='+path.join(work,'qa/pdf-browser'),'about:blank'],{stdio:'ignore'});
let c;
try {
 for(let i=0;i<100;i++){try{await fetch(process.env.SCRIPTA_CDP_URL+'/json/version');break}catch{await new Promise(r=>setTimeout(r,200));}}
 c=await connect('about:blank');
 await c.send('Network.enable');await c.send('Network.setBlockedURLs',{urls:['http://*','https://*']});
 for(const lang of ['en','ro']){
  const source=path.join(work,'book',lang,'full_content.html');
  await c.send('Page.navigate',{url:pathToFileURL(source).href});
  await c.wait('document.readyState==="complete"');
  await c.evaluate('document.querySelectorAll("img").forEach(i=>i.loading="eager");document.fonts.ready');
  await c.wait('[...document.images].every(i=>i.complete&&i.naturalWidth>0)');
  const css=`@page{size:6in 9in;margin:.65in .62in .68in}html{color-scheme:light}body{background:white;color:#172b35;font:10.2pt/1.45 Georgia,serif}article{max-width:none;margin:0;padding:0}h1,h2,h3{font-family:Arial,sans-serif;line-height:1.2;break-after:avoid;color:#194f62}h1{font-size:20pt;margin:0 0 18pt;break-before:page}h2{font-size:14pt;margin:20pt 0 10pt}h3{font-size:11.5pt;margin:16pt 0 7pt}p{margin:0 0 8pt;orphans:3;widows:3;hyphens:auto}table{font-size:8pt;table-layout:fixed}td,th{padding:4pt;overflow-wrap:anywhere}thead{display:table-header-group}tr,img,math{break-inside:avoid}img{max-width:100%;max-height:6.7in;object-fit:contain}math{font-size:10pt;max-width:100%}annotation{display:none}.source-copyright{font-size:10pt;padding-top:1.0in;break-after:page}.source-copyright p{text-align:left;line-height:1.7}a{color:inherit}pre{font-size:8pt}`;
  await c.evaluate(`{const s=document.createElement('style');s.textContent=${JSON.stringify(css)};document.head.append(s)}`);
  const figures=await c.evaluate('({images:document.images.length,math:document.querySelectorAll("math").length,tables:document.querySelectorAll("table").length})');
  const pdf=await c.send('Page.printToPDF',{printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font:8px Arial;width:100%;text-align:center;color:#777"><span class="pageNumber"></span></div>',generateDocumentOutline:true,generateTaggedPDF:true});
  const bytes=Buffer.from(pdf.data,'base64');await fs.writeFile(path.join(work,'book',lang,'book.pdf'),bytes);
  await fs.mkdir(path.join(work,'publication',lang),{recursive:true});
  await fs.writeFile(path.join(work,'publication',lang,'pdf-build.json'),JSON.stringify({language:lang,engine:'Chromium native MathML print',sourceHtmlSha256:hash(await fs.readFile(source)),pdfSha256:hash(bytes),bytes:bytes.length,...figures},null,2)+'\n');
  console.log(lang,bytes.length,figures);
 }
}finally{if(c)await c.close();browser.kill('SIGTERM');}
