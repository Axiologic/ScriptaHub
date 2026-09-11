import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {connect} from './browser-session.mjs';

const data=JSON.parse(await fs.readFile('tasks/voice-migration-progress.json','utf8'));
for(const entry of data.entries){
  for(const url of [entry.bookPage,entry.animationPage]){
    assert.ok(url&&!url.startsWith('docs/')&&!url.startsWith('/'),'relative site route');
    await fs.access('docs/'+url.split('?')[0]);
  }
}
const c=await connect((process.env.SCRIPTA_TEST_URL||'http://127.0.0.1:8128')+'/status.html');
try{
  await c.send('Page.addScriptToEvaluateOnNewDocument',{source:`const realInterval=window.setInterval;window.setInterval=(fn,ms,...args)=>{if(ms===60000){window.__statusTick=fn;window.__statusInterval=ms;return 0;}return realInterval(fn,ms,...args)};`});
  await c.send('Page.reload',{ignoreCache:true});
  await c.wait(`!!window.__statusTick&&document.querySelectorAll('[data-status-book]').length===${data.entries.length}`);
  assert.equal(await c.evaluate('window.__statusInterval'),60000);
  const counters=await c.evaluate(`Object.fromEntries([...document.querySelectorAll('[data-production-count]')].map(el=>[el.dataset.productionCount,Number(el.querySelector('strong').textContent)]))`);
  assert.deepEqual(counters,data.productionCounts);
  await c.evaluate(`(()=>{const input=document.querySelector('[data-status-search]');input.value='smoothing';input.dispatchEvent(new Event('input'));document.querySelector('article:not([hidden]) details').open=true;window.__statusTick()})()`);
  await c.wait(`![...document.scripts].some(script=>script.src.includes('?t='))`);
  const result=await c.evaluate(`({books:document.querySelectorAll('[data-status-book]').length,visible:[...document.querySelectorAll('article:not([hidden])')].map(e=>e.dataset.statusBook),open:document.querySelector('article:not([hidden]) details').open,query:document.querySelector('[data-status-search]').value,tts:[...document.querySelectorAll('dt')].filter(e=>e.textContent==='Exact TTS direction').length,badLinks:[...document.querySelectorAll('.status-list a')].filter(e=>e.target!=='_blank'||e.getAttribute('href').startsWith('docs/')).length})`);
  assert.equal(result.books,data.entries.length);assert.equal(result.open,true);assert.equal(result.query,'smoothing');assert.equal(result.badLinks,0);assert.deepEqual(result.visible,['the smoothing']);assert.ok(result.tts>=data.entries.length*7);
  await c.size(1200,900);await c.capture('/tmp/status-plan-desktop.png');
  await c.size(393,900);assert.equal(await c.evaluate('document.documentElement.scrollWidth'),393);await c.capture('/tmp/status-plan-mobile.png');
  // Exercise active ordering even when no real production job happens to run.
  await c.evaluate(`window.SCRIPTA_VOICE_MIGRATION_STATUS.entries.forEach((entry,index,all)=>{entry.active=index>=all.length-2;if(entry.active)entry.stages.voice={status:'running'}});document.querySelector('[data-status-search]').value='';`);
  await c.evaluate(await fs.readFile('docs/assets/status.js','utf8'));
  const active=await c.evaluate(`({first:[...document.querySelectorAll('[data-status-book]')].slice(0,2).map(el=>el.dataset.workState),badges:[...document.querySelectorAll('.status-indicator-active')].map(el=>el.textContent.trim()),group:document.querySelector('.status-group').classList.contains('status-active'),overflow:document.documentElement.scrollWidth>innerWidth})`);
  assert.deepEqual(active.first,['active','active']);assert.equal(active.group,true);assert.equal(active.badges.length,2);assert.ok(active.badges.every(text=>text.includes('În lucru')&&text.includes('voce')));assert.equal(active.overflow,false);
  await c.capture('/tmp/status-active-mobile.png');
  assert.equal(c.errors.length,0);
  console.log(JSON.stringify({valid:true,...result,activeIndicatorsAndOrdering:true,refreshPreservesOpenScript:true,mobileOverflow:false}));
}finally{await c.close();}
