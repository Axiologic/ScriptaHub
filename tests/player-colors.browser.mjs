import assert from 'node:assert/strict';import {connect} from './browser-session.mjs';
const c=await connect('http://127.0.0.1:8012/books/the/first/wake/bk-409c27f5b4524932/Animation/index.html?lang=en');let checks=0;
try{
 await c.wait('!!document.querySelector("shf-player")?.film');await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause()');
 for(const theme of ['light','orange','nord','dark'])for(const width of [1200,393]){
  await c.size(width,900);await c.evaluate(`document.documentElement.dataset.theme='${theme}'`);
  const result=await c.evaluate(`(()=>{const host=getComputedStyle(p),bar=getComputedStyle(p.$('transport')),progress=getComputedStyle(p.$('seek')),drawer=getComputedStyle(p.$('drawer'));const probe=document.createElement('span');p.append(probe);const resolved=name=>{probe.style.color=host.getPropertyValue(name);return getComputedStyle(probe).color};const expected={bg:resolved('--header'),ink:resolved('--ink'),accent:resolved('--green')};probe.remove();return {bar:bar.backgroundColor,ink:bar.color,accent:progress.accentColor,drawer:drawer.backgroundColor,expected,playing:p.playing,audio:!!p.audio.ctx}})()`);
  assert.equal(result.bar,result.expected.bg);assert.equal(result.ink,result.expected.ink);assert.equal(result.accent,result.expected.accent);assert.equal(result.drawer,result.expected.bg);assert.equal(result.playing,false);assert.equal(result.audio,false);checks++;
  await c.evaluate(`p.setTheme('paper');p.classList.add('cinema')`);assert.equal(await c.evaluate(`getComputedStyle(p.$('seek')).accentColor`),result.expected.accent);await c.evaluate(`p.classList.remove('cinema')`);checks++;
 }
 await c.size(1200,900);await c.evaluate(`document.documentElement.dataset.theme='orange';p.seek(2000)`);await c.capture('/tmp/player-orange-controls.png');
 await c.send('Page.navigate',{url:'http://127.0.0.1:8012/index.html?lang=en'});await c.wait('!!window.SHF?.Player&&!!document.querySelector("[data-mascot-start]")');
 // Exercise the actual dialog without scheduling audio or playback.
 await c.evaluate(`SHF.Player.prototype.play=async function(){this.setMuted(true);this.pause()};document.querySelector('shf-player').audio.unlock=async()=>{};document.querySelector('[data-mascot-start]').click()`);await c.wait('!!document.querySelector("shf-player")?.film');
 assert(await c.evaluate(`(()=>{const p=document.querySelector('shf-player');document.documentElement.dataset.theme='nord';return getComputedStyle(p.$('transport')).backgroundColor==='rgb(236, 230, 226)'&&!p.playing&&!p.audio.ctx})()`));checks++;
 assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,errors:0,audiblePlayback:false}));
}finally{await c.close()}
