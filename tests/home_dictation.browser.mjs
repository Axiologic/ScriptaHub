// Simulated recognition only: never opens a microphone or plays audio.
import assert from 'node:assert/strict';
import {connect} from './browser-session.mjs';
const base=process.env.SCRIPTA_TEST_URL||'http://127.0.0.1:8012/';
const s=await connect('about:blank');let checks=0;
try{
 await s.send('Page.addScriptToEvaluateOnNewDocument',{source:`window.mockRecognitions=[];window.SpeechRecognition=class{constructor(){mockRecognitions.push(this)}start(){this.onstart?.()}abort(){this.aborted=true;this.onend?.()}emit(text){this.onresult?.({results:[[{transcript:text}]]})}}`});
 await s.send('Page.navigate',{url:base+'index.html?lang=en#ask-librarian'});await s.wait('!!document.querySelector("[data-mascot-dictate]")');
 assert.equal(await s.evaluate('mockRecognitions.length'),0);checks++;
 for(const theme of ['light','orange','nord','dark'])for(const width of [1366,393,320]){
  await s.size(width,852);await s.evaluate(`document.documentElement.dataset.theme='${theme}'`);
  const g=await s.evaluate(`(()=>{const form=document.querySelector('.mascot-question').getBoundingClientRect(),input=document.querySelector('#mascot-query').getBoundingClientRect();return {form:form.toJSON(),input:input.toJSON(),buttons:[...document.querySelectorAll('.mascot-question-actions button')].map(b=>{const r=b.getBoundingClientRect(),v=b.querySelector('svg').getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,dx:(r.left+r.right-v.left-v.right)/2,dy:(r.top+r.bottom-v.top-v.bottom)/2}})}})()`);
  assert.equal(g.buttons.length,3);for(const b of g.buttons){assert.equal(b.x,g.buttons[0].x);assert.equal(b.w,32);assert.equal(b.h,32);assert(Math.abs(b.dx)<.1&&Math.abs(b.dy)<.1);assert(b.y>=g.form.top&&b.y+b.h<=g.form.bottom);assert(g.input.right<b.x)}
  assert(Math.abs((g.buttons[1].y-g.buttons[0].y)-(g.buttons[2].y-g.buttons[1].y))<.1);checks++;
 }
 await s.evaluate(`document.querySelector('#mascot-query').value='Books about';document.querySelector('[data-mascot-dictate]').click();mockRecognitions.at(-1).emit('different times')`);
 assert.equal(await s.evaluate('document.querySelector("#mascot-query").value'),'Books about different times');assert.equal(await s.evaluate('mockRecognitions.at(-1).lang'),'en-US');checks++;
 await s.evaluate(`mockRecognitions.at(-1).emit('different kinds of time')`);assert.equal(await s.evaluate('document.querySelector("#mascot-query").value'),'Books about different kinds of time');checks++;
 await s.evaluate(`window.previousRecognition=mockRecognitions.at(-1);document.querySelector('[data-mascot-cancel]').click();previousRecognition.emit('late unwanted result')`);
 assert(await s.evaluate(`previousRecognition.aborted&&document.querySelector('#mascot-question').hidden&&document.querySelector('#mascot-query').value==='Books about different kinds of time'`));checks++;
 await s.evaluate(`document.querySelector('[data-mascot-ask]').click();document.querySelector('[data-mascot-dictate]').click();ScriptaHomeLibrarian.localize('ro')`);assert(await s.evaluate(`mockRecognitions.at(-1).aborted&&document.querySelector('[data-mascot-dictate]').getAttribute('aria-pressed')==='false'`));checks++;
 await s.evaluate(`document.querySelector('[data-mascot-dictate]').click()`);assert.equal(await s.evaluate('mockRecognitions.at(-1).lang'),'ro-RO');checks++;
 await s.evaluate(`mockRecognitions.at(-1).onerror({error:'not-allowed'})`);assert(await s.evaluate(`document.querySelector('#mascot-speech-status').textContent.length>0&&document.querySelector('[data-mascot-dictate]').getAttribute('aria-pressed')==='false'`));checks++;
 await s.evaluate(`document.querySelector('[data-mascot-dictate]').click();window.finalRecognition=mockRecognitions.at(-1);document.querySelector('#mascot-query').value='   ';document.querySelector('#mascot-question').requestSubmit()`);assert(await s.evaluate('finalRecognition.aborted'));checks++;
 await s.evaluate(`window.SpeechRecognition=undefined;window.webkitSpeechRecognition=undefined;const form=document.createElement('form');form.innerHTML='<textarea></textarea><button></button><span></span>';document.body.append(form);ScriptaDictation.bind({input:form.querySelector('textarea'),button:form.querySelector('button'),status:form.querySelector('span'),language:'en'});window.unsupported=form.querySelector('button')`);assert(await s.evaluate(`unsupported.disabled&&unsupported.title.includes('unavailable')`));checks++;
 console.log(JSON.stringify({checks,errors:s.errors.length,microphoneOpened:false}));assert.equal(s.errors.length,0);
}finally{await s.close()}
