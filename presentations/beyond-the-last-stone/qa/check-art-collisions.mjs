// Project-local silent collision probe for the reviewed art (muted, paused, own tab only).
// Reports, in stage units, visible text crossing people, other text, or foreign outlines,
// people's heads crossed by foreign outlines, and any art entering the caption band.
// Usage: SCRIPTA_CDP_URL=http://127.0.0.1:9235 node presentations/beyond-the-last-stone/qa/check-art-collisions.mjs [--boxes]
import fs from 'node:fs/promises';import {connect} from '../../../tests/browser-session.mjs';
const root=new URL('..',import.meta.url).pathname.replace(/\/$/,'');
const scenes=JSON.parse(await fs.readFile(root+'/work/scenes.json','utf8'));
const people=['ar','kee','karr','taan','lu'];
const c=await connect('file://'+root+'/exports/beyond-the-last-stone-introduction.html');const issues=[],boxes=[];
try{
 await c.size(1200,960);await c.wait('!!document.querySelector("shf-player")?.film');
 await c.evaluate('window.p=document.querySelector("shf-player");p.setMuted(true);p.pause();document.fonts.ready');
 let start=0;
 for(let i=0;i<scenes.length;i++){
  const ids=scenes[i].visual.objects.map(o=>o.id);
  const d=await c.evaluate(`p.film.scenes[${i}].durationMs`);
  const points=await c.evaluate(`[['first',${d}*.08],...p.film.scenes[${i}].beats.flatMap((b,n)=>[['s'+(n+1)+'-start',b.startMs+200],['s'+(n+1)+'-mid',(b.startMs+b.spokenEndMs)/2],['s'+(n+1)+'-end',b.endMs-50]]),['last',${d}*.96]]`);
  for(const [label,t] of points){
   const r=await c.evaluate(`(()=>{p.seek(${start+t});const S=p.svg.getBoundingClientRect(),k=1200/S.width;const st=r=>({x:(r.left-S.left)*k,y:(r.top-S.top)*k,w:r.width*k,h:r.height*k});
    const vis=n=>{let o=1;for(let a=n;a&&a!==p.svg.parentNode;a=a.parentNode){const cs=getComputedStyle(a);if(cs.display==='none'||cs.visibility==='hidden')return 0;o*=Number(cs.opacity)}return o};
    const ids=${JSON.stringify(ids)},people=${JSON.stringify(people)};const out={texts:[],people:[],outlines:[],cap:st(p.$('caption').getBoundingClientRect())};
    for(const id of ids){const g=p.dom.get(id);if(!g||vis(g)<.15)continue;
     for(const t of g.querySelectorAll('text'))if(vis(t)>=.15&&t.textContent.trim())out.texts.push({id,text:t.textContent,...st(t.getBoundingClientRect())});
     if(people.includes(id)){const b=st(g.getBoundingClientRect());const head=[...g.querySelectorAll('ellipse')].map(e=>st(e.getBoundingClientRect())).sort((a,b)=>a.y-b.y)[0];out.people.push({id,...b,head})}
     else{const pts=[];for(const s of g.querySelectorAll('path,line,polyline,ellipse,circle,rect')){if(vis(s)<.15||!s.getTotalLength)continue;let L;try{L=s.getTotalLength()}catch{continue}const M=s.getScreenCTM();for(let a=0;a<=L;a+=4){const q=s.getPointAtLength(a),pt=p.svg.createSVGPoint();pt.x=q.x;pt.y=q.y;const w=pt.matrixTransform(M);pts.push([(w.x-S.left)*k,(w.y-S.top)*k])}}const bb=st(g.getBoundingClientRect());out.outlines.push({id,pts,bb})}}
    return out})()`);
   const inside=(pt,b,m=0)=>pt[0]>b.x-m&&pt[0]<b.x+b.w+m&&pt[1]>b.y-m&&pt[1]<b.y+b.h+m;
   const ov=(a,b,m=0)=>Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>m&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>m;
   const at=`${i}:${label}`;
   if(process.argv.includes('--boxes'))boxes.push({at,texts:r.texts.map(t=>[t.id,t.text,Math.round(t.x),Math.round(t.y),Math.round(t.w),Math.round(t.h)]),people:r.people.map(q=>[q.id,Math.round(q.x),Math.round(q.y),Math.round(q.w),Math.round(q.h)]),objects:r.outlines.map(o=>[o.id,Math.round(o.bb.x),Math.round(o.bb.y),Math.round(o.bb.w),Math.round(o.bb.h)])});
   const capTop=r.cap.h>1?r.cap.y-6:Infinity;
   for(const t of r.texts){
    for(const q of r.people)if(ov(t,q,1))issues.push([at,'text-person',t.text,q.id]);
    for(const u of r.texts)if(u!==t&&u.text<t.text&&ov(t,u,0))issues.push([at,'text-text',t.text,u.text]);
    for(const o of r.outlines)if(o.id!==t.id&&o.pts.some(pt=>inside(pt,t,2)))issues.push([at,'line-through-text',t.text,o.id]);
    if(t.y+t.h>capTop)issues.push([at,'text-in-caption-band',t.text]);
   }
   for(const q of r.people){
    for(const o of r.outlines)if(q.head&&o.pts.some(pt=>inside(pt,q.head,3)))issues.push([at,'line-through-head',q.id,o.id]);
    for(const u of r.people)if(u.id<q.id&&ov(u,q,4))issues.push([at,'person-person',q.id,u.id]);
    if(q.y+q.h>capTop)issues.push([at,'person-in-caption-band',q.id,Math.round(q.y+q.h),Math.round(capTop)]);
   }
   for(const o of r.outlines)if(o.bb.y+o.bb.h>capTop&&o.bb.w>0)issues.push([at,'object-in-caption-band',o.id,Math.round(o.bb.y+o.bb.h),Math.round(capTop)]);
  }
  start+=d;
 }
}finally{await c.close()}
const uniq=[...new Map(issues.map(x=>[x.slice(1).join('|')+'|'+x[0].split(':')[0],x])).values()];
console.log(JSON.stringify({issues:uniq.length,list:uniq,boxes:boxes.length?boxes:undefined},null,1));
