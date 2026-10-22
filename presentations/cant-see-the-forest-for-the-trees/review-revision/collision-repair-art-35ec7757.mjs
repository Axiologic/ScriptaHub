// Authoritative artwork entry for the current two-sentence-per-scene film.
// The accepted curiosity-v2 composition (art 3007afb5…) is preserved in
// review-revision/scenes.before-collision-repair-3007afb5.json; this script
// re-applies the 2026-10-22 collision/contrast repair to work/scenes.json.
// It only sets absolute positions, geometry and theme-aware stage-label ink,
// so it is idempotent. The superseded rail-yard generator is archived as
// review-revision/legacy-railyard-art.mjs and must not be run for this film.
// Layout rule: at the 1200-wide stage the caption text occupies roughly
// x 274–926, y 580–650, so artwork inside that x-range ends above y ≈ 565 and
// people stand fully outside it.
import fs from 'node:fs';import path from 'node:path';
const base=path.dirname(new URL(import.meta.url).pathname),file=path.join(base,'work/scenes.json');
const scenes=JSON.parse(fs.readFileSync(file,'utf8'));
const scene=id=>scenes.find(s=>s.id===id)||(()=>{throw Error('Missing scene '+id)})();
const object=(s,id)=>s.visual.objects.find(o=>o.id===id)||(()=>{throw Error(`Missing ${s.id}/${id}`)})();
const part=(o,suffix)=>o.visual.children.find(c=>c.id.endsWith('.'+suffix))||(()=>{throw Error(`Missing ${o.id}.${suffix}`)})();
const place=(s,id,x,y)=>Object.assign(object(s,id),{x,y});
const attrs=(s,id,suffix,values)=>Object.assign(part(object(s,id),suffix).attrs,values);
const moveTo=(s,actor,x,y)=>{const a=s.visual.actions.find(a=>a.actor===actor&&a.action==='moveTo');if(!a)throw Error(`Missing move ${s.id}/${actor}`);Object.assign(a,{x,y});};
// Labels drawn directly on the stage use the theme ink token so Night stays legible.
const stageInk=(s,id,suffix)=>attrs(s,id,suffix,{fill:'$ink'});
// Coral-coated people keep a distinct light coral coat in Night instead of the blue override.
const nightCoat=(s,id,suffix)=>{const p=part(object(s,id),suffix);p.themeAttrs={...p.themeAttrs,night:{...p.themeAttrs?.night,fill:'#e0a091'}};};

{const s=scene('scene-01');
 place(s,'author',200,505);
 place(s,'desk',600,465);attrs(s,'desk','part11',{x:-300,width:600});attrs(s,'desk','part12',{d:'M-250 28V86M250 28V86',stroke:'$ink'});
 for(const id of ['working-draft','sharp-question'])place(s,id,475,235);attrs(s,'sharp-question','part18',{x:-134,y:52});place(s,'smooth-line',850,235);
 place(s,'missing-edge',850,368);attrs(s,'missing-edge','part23',{d:'M-100 0H-40M-12 0H22M50 0H100'});attrs(s,'missing-edge','part24',{y:40});stageInk(s,'missing-edge','part24');
 // A closed cover beside the desk: the spine sits at the edge instead of striking through the title.
 place(s,'book',1066,470);attrs(s,'book','part25',{d:'M-104 -88H104Q112 -88 112 -80V80Q112 88 104 88H-104Q-112 88 -112 80V-80Q-112 -88 -104 -88Z'});attrs(s,'book','part26',{d:'M-92 -88V88'});
 attrs(s,'book','part27',{x:10});attrs(s,'book','part28',{x:10});
 object(s,'book').meaning='The book stands beside the same desk as the lived editing experience.';}

{const s=scene('scene-02');
 place(s,'writing-surface',505,345);place(s,'continued-draft',505,475);stageInk(s,'continued-draft','part5');
 place(s,'doubt-mark',305,205);place(s,'urgency-mark',505,205);place(s,'responsibility-mark',705,205);
 for(const [id,p] of [['doubt-mark','part10'],['urgency-mark','part12'],['responsibility-mark','part14']])stageInk(s,id,p);
 place(s,'retained-question',125,275);attrs(s,'retained-question','part6',{x:-100,width:200});moveTo(s,'retained-question',140,275);
 place(s,'proposal',935,330);moveTo(s,'proposal',920,330);place(s,'unknown',920,510);}

{const s=scene('scene-03');
 place(s,'upkeep-ledger',600,235);place(s,'specialist-a',282,265);place(s,'specialist-b',918,265);
 place(s,'planner',200,505);moveTo(s,'planner',215,505);place(s,'author',1040,505);moveTo(s,'author',1000,505);nightCoat(s,'author','part11');
 place(s,'unowned-consequence',440,420);attrs(s,'unowned-consequence','part31',{d:'M-150 0H-70M-40 0H40M70 0H150'});stageInk(s,'unowned-consequence','part32');
 place(s,'unpriced-option',790,430);place(s,'plan-question',790,520);attrs(s,'plan-question','part37',{y:38});stageInk(s,'plan-question','part37');}

{const s=scene('scene-04');
 place(s,'uncertainty-note',620,185);place(s,'polished-explanation',400,330);place(s,'real-conflict',820,330);
 place(s,'review-route',620,428);attrs(s,'review-route','part24',{y:40});stageInk(s,'review-route','part24');
 place(s,'both-versions',620,528);attrs(s,'both-versions','part33',{y:-34,height:68});attrs(s,'both-versions','part35',{y:-34,height:68});
 attrs(s,'both-versions','part34',{x:-140,y:8});
 place(s,'author',190,505);moveTo(s,'author',205,505);place(s,'operator',1010,505);moveTo(s,'operator',1000,505);nightCoat(s,'operator','part11');}

fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
const crypto=await import('node:crypto');
console.log('artSha256',crypto.createHash('sha256').update(JSON.stringify(scenes.map(s=>({id:s.id,visual:s.visual})))).digest('hex'));
