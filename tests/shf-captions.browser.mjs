import assert from 'node:assert/strict';
import {connect} from './browser-session.mjs';
const c=await connect('about:blank');
try {
 await c.send('Network.setCacheDisabled',{cacheDisabled:true});
 await c.send('Page.navigate',{url:'http://127.0.0.1:8012/index.html'});
 await c.wait('!!document.querySelector("shf-player")');
 await c.evaluate('window.p=document.querySelector("shf-player");window.oldCaptionScale=localStorage.getItem("shf-caption-scale");');
 assert(await c.evaluate('!!p.shadowRoot.getElementById("captionScale")'));
 assert(!await c.evaluate('!!p.shadowRoot.getElementById("rate")||!!p.shadowRoot.getElementById("reduced")'));
 await c.evaluate('(()=>{const s=p.shadowRoot.getElementById("captionScale");s.value="125";s.dispatchEvent(new Event("input"))})()');
 assert.equal(await c.evaluate('p.captionScale'),1.25);
 assert.equal(await c.evaluate('document.createElement("shf-player").captionScale'),1.25);
 await c.evaluate('p.setRate(1);p.setReducedMotion(true);p.setCaptionScale(1);');
 assert.equal(await c.evaluate('getComputedStyle(p.shadowRoot.getElementById("caption")).backgroundColor'),'rgba(0, 0, 0, 0)');
 assert.equal(await c.evaluate('getComputedStyle(p.shadowRoot.getElementById("caption")).textWrap'),'balance');
 for (const theme of ['color','paper','night']) {
  const style=await c.evaluate(`p.setTheme('${theme}');(()=>{const s=getComputedStyle(p.$('caption'));return {ink:s.color,outline:s.webkitTextStrokeColor,weight:s.fontWeight}})()`);
  assert.equal(style.ink,theme==='night'?'rgb(255, 255, 255)':'rgb(17, 24, 32)');
  assert.equal(style.outline,theme==='night'?'rgb(17, 24, 32)':'rgb(255, 255, 255)');
  assert.equal(style.weight,theme==='night'?'400':'600');
 }
 console.log('Subtitle control, persistence, balanced wrapping, theme contrast/weight and retained APIs passed.');
} finally {
 await c.evaluate('if(window.oldCaptionScale==null)localStorage.removeItem("shf-caption-scale");else localStorage.setItem("shf-caption-scale",oldCaptionScale)');
 await c.close();
}
