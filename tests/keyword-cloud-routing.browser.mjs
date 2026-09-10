import assert from 'node:assert/strict';
import {connect} from './browser-session.mjs';
const base=process.env.SCRIPTA_TEST_URL||'http://127.0.0.1:8012/';
const c=await connect('about:blank');let checks=0;
try {
 await c.size(1366,900);
 // Observe the real painted keyword locations, then send a real pointer click.
 await c.send('Page.addScriptToEvaluateOnNewDocument',{source:`(()=>{const proto=CanvasRenderingContext2D.prototype,original=proto.fillText,clear=proto.clearRect;proto.clearRect=function(...args){this.canvas.paintedWords=[];return clear.apply(this,args)};proto.fillText=function(text,x,y,...args){const point=new DOMPoint(x,y).matrixTransform(this.getTransform());(this.canvas.paintedWords??=[]).push({text,x:point.x,y:point.y});return original.call(this,text,x,y,...args)}})()`});
 for (const route of ['index.html?lang=en','books/the/first/wake/bk-409c27f5b4524932/ro/book.html?lang=ro']) {
  for (const mode of ['pointer','keyboard']) {
   await c.send('Page.navigate',{url:base+route});await c.wait('!!document.querySelector(".keyword-cloud canvas")');
   assert(await c.evaluate(`new URL(document.querySelector('.keyword-cloud nav a').href).searchParams.has('keyword')`));checks++;
   await c.evaluate(`document.querySelector('.keyword-cloud canvas').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}))`);
   await c.wait('!!document.querySelector(".keyword-cloud-modal canvas")?.paintedWords?.length');
   const language=new URL(base+route).searchParams.get('lang');let keyword;
   if(mode==='keyboard'){
    keyword=await c.evaluate(`(()=>{const a=document.querySelector('.keyword-cloud-modal nav a');const request=new URLSearchParams(new URL(a.href).hash.slice(1)).get('request');a.focus();return request})()`);
    await c.send('Input.dispatchKeyEvent',{type:'rawKeyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await c.send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
   }else{
    const point=await c.evaluate(`(()=>{const canvas=document.querySelector('.keyword-cloud-modal canvas'),r=canvas.getBoundingClientRect(),p=canvas.paintedWords.find(p=>p.x/canvas.width>.2&&p.x/canvas.width<.8&&p.y/canvas.height>.2&&p.y/canvas.height<.8);const a=[...canvas.parentElement.querySelectorAll('nav a')].find(a=>a.textContent===p.text);return {x:r.x+p.x*r.width/canvas.width,y:r.y+p.y*r.height/canvas.height,keyword:new URLSearchParams(new URL(a.href).hash.slice(1)).get('request')}})()`);
    keyword=point.keyword;await c.send('Input.dispatchMouseEvent',{type:'mousePressed',x:point.x,y:point.y,button:'left',clickCount:1});await c.send('Input.dispatchMouseEvent',{type:'mouseReleased',x:point.x,y:point.y,button:'left',clickCount:1});
   }
   await c.wait('location.pathname.endsWith("/librarian/index.html")&&!!document.querySelector(".librarian-results-list > *")');
   const result=await c.evaluate(`({lang:new URL(location.href).searchParams.get('lang'),query:new URLSearchParams(location.hash.slice(1)).get('request'),count:document.querySelector('.librarian-results-list').children.length,heading:document.querySelector('.librarian-results h1').textContent})`);
   assert.equal(result.lang,language);assert.equal(result.query,keyword);assert(result.count>0&&result.count<=10);assert(result.heading.includes(keyword));checks++;
  }
 }
 assert.equal(c.errors.length,0);console.log(JSON.stringify({checks,errors:0}));
} finally {await c.close()}
