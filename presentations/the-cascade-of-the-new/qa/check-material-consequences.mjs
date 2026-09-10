import fs from 'node:fs/promises';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('..',import.meta.url).pathname.replace(/\/$/,'');
const c=await connect('file://'+root+'/exports/the-cascade-of-the-new-introduction.html');
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause()');
 const results=[];
 for(const theme of ['color','paper','night']){
  await c.evaluate(`p.setTheme('${theme}')`);
  const opening=[];
  for(const b of [0,5])opening.push(await c.evaluate(`(()=>{p.seek(p.film.scenes[0].beats[${b}].startMs+1600);return{caption:p.$('caption').textContent,warmth:Number(getComputedStyle(p.dom.get('mother-warmth')).opacity),preserved:Number(getComputedStyle(p.dom.get('mother-preserved')).opacity),cradlePaths:p.dom.get('hypothetical-cradle').querySelectorAll('path').length,playing:p.playing,audioContextOpen:!!p.audio.ctx}})()`));
  const routing=[];
  for(const b of [3,5])routing.push(await c.evaluate(`(()=>{const start=p.film.scenes.slice(0,2).reduce((a,s)=>a+s.durationMs,0);p.seek(start+p.film.scenes[2].beats[${b}].startMs+2900);return{caption:p.$('caption').textContent,nodes:['official-report','hidden-notebook'].map(id=>{const e=p.dom.get(id),m=e.getCTM();return{id,x:m.e,y:m.f,opacity:Number(getComputedStyle(e).opacity)}})}})()`));
  const x=(s,id)=>s.nodes.find(n=>n.id===id).x;
  const publicDx=x(routing[1],'official-report')-x(routing[0],'official-report'),privateDx=x(routing[1],'hidden-notebook')-x(routing[0],'hidden-notebook');
  const held=await c.evaluate(`(()=>{p.seek(p.film.scenes[0].durationMs+p.film.scenes[1].durationMs*.6);const hand=p.dom.get('kesh.armL').querySelector('circle'),point=p.svg.createSVGPoint();point.x=Number(hand.getAttribute('cx'));point.y=Number(hand.getAttribute('cy'));const h=point.matrixTransform(hand.getCTM()),r=p.dom.get('regulator').getCTM();return{distance:Math.hypot(h.x-r.e,h.y-r.f),hand:{x:h.x,y:h.y},regulator:{x:r.e,y:r.f}}})()`);
  const pass=held.distance<12&&opening[0].warmth>.99&&opening[1].warmth<.01&&opening[1].preserved>.3&&opening[1].cradlePaths>=3&&opening.every(x=>!x.playing&&!x.audioContextOpen)&&publicDx>20&&privateDx< -10;
  results.push({theme,pass,held,opening,publicDx,privateDx,routing});if(!pass)throw Error(JSON.stringify(results.at(-1)));
 }
 await fs.writeFile(root+'/qa/material-consequences-review.json',JSON.stringify({status:'pass',method:'Paused seeks verify the Sunday warmth layer diminishes while the preserved figure remains, the hypothetical empty cradle is drawn, and official versus private records travel in opposite directions. This is conceptual staging of threatened compatibility and documentary separation, not a completed withdrawal or simulated7D physics.',results,errors:c.errors,audiblePlayback:false},null,2)+'\n');console.log('Threatened Sunday and distinct record routing verified in all three themes.');
}finally{await c.close()}
