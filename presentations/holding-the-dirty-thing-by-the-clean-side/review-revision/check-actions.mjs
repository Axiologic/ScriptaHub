import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('../',import.meta.url);
const url=new URL('exports/holding-the-dirty-thing-by-the-clean-side-introduction.html',root).href;
const cases=[
 [0,2,0,['baker','rack']], [0,2,3400,['baker','rack']],
 [1,2,0,['existing-shift','transferred-shift','rota-name','efficiency-name']],
 [1,2,2900,['existing-shift','transferred-shift','rota-name','efficiency-name']],
 [1,3,1900,['existing-shift','transferred-shift','rota-name','efficiency-name']],
 [2,0,2200,['unchanged-rota','baker','coordinator']],
 [2,2,1800,['unchanged-rota','baker','coordinator']],
 [2,3,2200,['unchanged-rota','coordinator','scheduling-screen','lift-proposal']],
 [2,4,2400,['unchanged-rota','coordinator','scheduling-screen','lift-proposal']],
 [3,0,1800,['same-rota','objection','review-slip']],
 [3,1,3100,['same-rota','objection','review-slip']]
];
const rows=[];
for(const theme of ['color','paper','night']){
 const c=await connect(url);
 try{
  await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
  await c.evaluate(`window.p=document.querySelector('shf-player');p.setMuted(true);p.pause();p.setTheme('${theme}');p.$('centerPlay').style.visibility='hidden'`);
  const samples=[];
  for(let i=0;i<cases.length;i++){
   const [scene,beat,offset,ids]=cases[i];
   const data=await c.evaluate(`(()=>{const start=p.film.scenes.slice(0,${scene}).reduce((n,s)=>n+s.durationMs,0);p.seek(start+p.film.scenes[${scene}].beats[${beat}].startMs+${offset});return ${JSON.stringify(ids)}.map(id=>{const e=p.dom.get(id),m=e.transform.baseVal.consolidate().matrix;return{id,x:m.e,y:m.f,opacity:Number(getComputedStyle(e).opacity),art:e.innerHTML}})})()`);
   samples.push(Object.fromEntries(data.map(o=>[o.id,o])));
   await c.evaluate('document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,200)))');
   await c.capture(new URL(`action-${theme}-${i}.png`,import.meta.url).pathname);
  }
  const [before,after]=samples;
  assert.ok(Math.abs((after.baker.x-before.baker.x)-(after.rack.x-before.rack.x))<.01);
  assert.equal(samples[2]['transferred-shift'].y,397);
  assert.equal(samples[3]['transferred-shift'].y,318);
  assert.equal(samples[3]['existing-shift'].y,318);
  assert.equal(samples[4]['transferred-shift'].y,318);
  assert.equal(samples[4]['rota-name'].opacity,0);
  assert.equal(samples[4]['efficiency-name'].opacity,1);
  assert.equal(samples[5]['unchanged-rota'].art,samples[6]['unchanged-rota'].art);
  assert.equal(samples[6]['unchanged-rota'].art,samples[8]['unchanged-rota'].art);
  assert.equal(samples[7]['scheduling-screen'].opacity,1);
  assert.equal(samples[8]['scheduling-screen'].opacity,0);
  assert.equal(samples[8]['lift-proposal'].opacity,1);
  assert.equal(samples[8].coordinator.opacity,1);
  assert.equal(samples[9]['same-rota'].art,samples[10]['same-rota'].art);
  assert.equal(samples[10].objection.x,566);
  rows.push({theme,checks:15,samples:samples.map(objects=>Object.fromEntries(Object.entries(objects).map(([id,{art,...state}])=>[id,state])))});
 }finally{await c.close();}
}
await fs.writeFile(new URL('action-review.json',import.meta.url),JSON.stringify({audiblePlayback:false,rows,screenshotInspection:'Separate visual inspection required; assertions do not establish artistry.'},null,2)+'\n');
console.log('15 action/continuity assertions passed in each theme;33 screenshots saved.');
