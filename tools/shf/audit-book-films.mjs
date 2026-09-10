// Inspect published SHF archives without opening a browser or audio output.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import '../../.agents/skills/shf-presentation-creator/runtime/shf-core.js';
const C=globalThis.SHFCore,sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const ledgerPath=process.argv[2]||'presentations/qa/2026-09-10-ninety-book-animations.json';
const ledger=read(ledgerPath),required=new Set(ledger.books.map(b=>b.bookId));
const works=new Map();
for(const entry of fs.readdirSync('presentations',{withFileTypes:true})){
 if(!entry.isDirectory())continue;
 const root=path.join('presentations',entry.name),file=path.join(root,'work/production.json');
 if(fs.existsSync(file)){const p=read(file);if(p.bookDirectory)works.set(path.resolve(p.bookDirectory),root)}
}
const books=read('docs/collection.json').books,results=[],errors=[];
for(const book of books){
 const manifest=read(path.join('docs',book.directory,'manifest.json')),animation=manifest.animation;
 if(!animation)continue;
 try{
  const file=path.join('docs',book.directory,animation.shf.startsWith('Animation/')?animation.shf:path.relative(book.directory,animation.shf));
  // Manifests use book-relative paths; aggregate records use site-relative paths.
  const candidate=fs.existsSync(file)?file:path.join('docs',animation.shf);
  const bytes=fs.readFileSync(candidate),film=await C.loadFile(new Blob([bytes]));
  const beats=film.scenes.flatMap(s=>s.beats);
  if(film.durationMs!==animation.durationMs)throw Error('Manifest duration differs from archive');
  if(required.has(book.id)&&(film.durationMs<120000||film.durationMs>180000))throw Error('New short film is outside 2–3 minutes');
  if(film.language!=='en'||beats.some(b=>C.splitSentences(b.text,'en').length!==1))throw Error('Language or one-sentence policy failed');
  const root=works.get(path.resolve('docs',book.directory));
  let sourceVerified=false,audioVerified=0,browserChecks=0;
  if(root){
   const extraction=path.join(root,'source/extraction.json');
   if(fs.existsSync(extraction)){
    const e=read(extraction),source=e.file||e.sourceHtml||e.path,expected=e.htmlSha256||e.sha256;
    if(!source||sha(fs.readFileSync(source))!==expected)throw Error('Canonical source hash mismatch');sourceVerified=true;
   }
   const receipts=path.join(root,'work/voice-receipts.json');
   if(fs.existsSync(receipts))for(const line of read(receipts).lines){
    const beat=beats.find(b=>b.id===line.id);
    if(!beat||sha(beat.text)!==line.textSha256||sha(fs.readFileSync(path.join(root,'work',line.file)))!==line.sha256)throw Error('Stale narration '+line.id);
    audioVerified++;
   }
   const qa=path.join(root,'qa/browser-review.json');
   if(fs.existsSync(qa)){const q=read(qa);if(q.durationMs!==film.durationMs||q.checks.some(c=>!c.pass)||q.jsErrors?.length)throw Error('Browser QA stale or failed');browserChecks=q.checks.length}
  }
  if(required.has(book.id)&&(!sourceVerified||audioVerified!==beats.length||browserChecks<21))throw Error('New film lacks source, narration or browser QA');
  results.push({bookId:book.id,title:book.title.en,durationMs:film.durationMs,shf:candidate,sha256:sha(bytes),sentences:beats.length,sourceVerified,audioVerified,browserChecks});
 }catch(e){errors.push({bookId:book.id,title:book.title.en,error:e.message})}
}
const missing=ledger.books.filter(b=>!results.some(r=>r.bookId===b.bookId)).map(b=>({bookId:b.bookId,title:b.title}));
const report={target:ledger.targetInstalledBooks,installedValid:results.length,newValid:results.filter(r=>required.has(r.bookId)).length,missing,errors,books:results,audiblePlayback:false};
fs.writeFileSync('presentations/qa/ninety-book-archive-audit.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({target:report.target,installedValid:results.length,newValid:report.newValid,missing:missing.length,errors},null,2));
if(errors.length||results.length<ledger.targetInstalledBooks||missing.length)process.exitCode=1;
