// Deterministic layout repair for the reviewed Qwen/8-sentence film (2026-10-22).
// Source of truth is work/scenes.json; this script only sets absolute positions,
// moveTo endpoints, a few simplified paths and theme-aware label colours. It keeps
// every object id and action (presentation-plan.json) unchanged and is idempotent.
// The obsolete Piper-era generator is archived in work/archive/art-superseded-v1.mjs.
import fs from 'node:fs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
const NIGHT_INK={night:{fill:'#e7eef3'}};
const scene=id=>scenes.find(s=>s.id===id).visual;
const obj=(v,id)=>{const o=v.objects.find(o=>o.id===id);if(!o)throw Error('missing '+id);return o};
const place=(v,id,x,y,scale)=>{const o=obj(v,id);o.x=x;o.y=y;if(scale!==undefined)o.scale=scale;return o};
const part=(o,i)=>o.visual.children[i];
const text=o=>o.visual.children.find(n=>n.type==='text');
const move=(v,id,x,y)=>{const a=v.actions.find(a=>a.actor===id&&a.action==='moveTo');if(!a)throw Error('missing moveTo '+id);a.x=x;a.y=y};

// 1 · The missing herd: open horizon above the camp, empty route on the right,
// food beside the embers, people moving in to gather around it.
{const v=scene('reasons-before-certainty');
 part(place(v,'far-ridges',600,150),0).attrs.d='M-540 42L-330 -19L-120 24L100 -41L315 17L540 -4';
 const river=place(v,'river',1125,445,.6);part(river,0).attrs.d='M-20 -120Q20 -60 -15 0Q-50 60 -5 128';part(river,1).attrs.cx=45;
 place(v,'embers',230,500);
 const food=place(v,'food-hide',230,395);
 part(food,0).attrs.d='M-90 -30Q0 -50 90 -30V28Q0 46 -90 28Z';
 [[-48,0],[-16,-4],[16,3],[48,-3]].forEach(([cx,cy],i)=>Object.assign(part(food,i+1).attrs,{cx,cy}));
 Object.assign(text(food).attrs,{y:68});text(food).themeAttrs=NIGHT_INK;
 place(v,'ar',520,430);place(v,'kee',650,430);place(v,'karr',780,430);
 move(v,'ar',400,430);move(v,'kee',530,430);move(v,'karr',660,430);
 const camp=place(v,'camp-circle',530,290);part(camp,0).attrs.d='M-150 20Q0 -50 150 20';text(camp).attrs.y=-40;
 const route=place(v,'empty-route',905,250);text(route).attrs.y=95;}

// 2 · Which signs can guide us?: high ground left, track in old snow centre,
// routes on an upper row, remembered words beside the listeners.
{const v=scene('what-the-track-tells');
 place(v,'high-ground',290,220);
 const snow=place(v,'old-snow',700,480);part(snow,0).attrs.d='M-200 30Q-130 0 -60 22Q20 44 100 18Q140 6 170 22';part(snow,1).attrs.d='M-150 26L-112 20M-30 34L8 32M84 24L120 18';
 place(v,'old-track',700,430);
 place(v,'ar',420,430);move(v,'ar',400,430);
 const point=place(v,'ar-point',520,420);Object.assign(text(point).attrs,{x:45,y:-44});
 const words=place(v,'remembered-words',1010,275);Object.assign(part(words,0).attrs,{x:-150,width:300});
 place(v,'route-a',240,140);place(v,'route-b',1000,140);
 const box=place(v,'move-before-knowing',710,250);Object.assign(part(box,0).attrs,{x:-140,width:280});
 place(v,'taan',930,430);place(v,'karr',1080,430);}

// 3 · Thought beside the fire: one council ground with a small central fire,
// food, counting stones, roots and seeds in a readable row; words above.
{const v=scene('stones-do-not-feed-people');
 const ground=place(v,'council-ground',640,440);Object.assign(part(ground,0).attrs,{rx:400,ry:96});
 Object.assign(part(ground,1).attrs,{d:'M10 70Q-2 40 24 18Q26 40 38 32Q54 50 46 70Z',fill:'#d07a42',stroke:'none'});
 const food=place(v,'food-hide',400,420);part(food,0).attrs.d='M-70 -28Q0 -44 70 -28V28Q0 44 -70 28Z';
 [-35,0,35].forEach((cx,i)=>part(food,i+1).attrs.cx=cx);text(food).attrs.y=62;
 const stones=place(v,'counting-stones',570,420);
 // The label says six stones: keep exactly six visible stones.
 stones.visual.children=stones.visual.children.filter((n,i,all)=>n.type!=='circle'||all.filter(m=>m.type==='circle').indexOf(n)<6);
 stones.visual.children.filter(n=>n.type==='circle').forEach((n,i)=>n.attrs.cx=-75+i*30);
 const roots=place(v,'roots',790,395);text(roots).attrs.y=95;
 const seeds=place(v,'seeds',945,440);text(seeds).attrs.y=40;
 place(v,'track-mark',590,230);
 place(v,'lu',180,430);place(v,'kee',1110,430);move(v,'kee',1080,430);
 place(v,'fireside-words',290,240);place(v,'shared-question',880,230);}

// 4 · Join the River People: book between the two readers instead of behind
// them; open-route note and decision badge on separate upper rows.
{const v=scene('when-memory-needs-marks');
 place(v,'reading-cloth',380,400);
 const book=place(v,'opening-book',860,360,.9);part(book,0).attrs.fill='#f3e7d3';
 const titles=book.visual.children.filter(n=>n.type==='text');Object.assign(titles[1].attrs,{x:110,'font-size':22});
 place(v,'uncertainty-mark',500,190);
 place(v,'first-camp',200,165);
 place(v,'decision-space',900,150);
 place(v,'ar',130,430);place(v,'kee',610,430);place(v,'karr',1140,430);
 move(v,'ar',155,430);move(v,'kee',585,430);move(v,'karr',1125,430);}

fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');console.log('Beyond the Last Stone layout repair applied.');
