// Caption-band and overlap repair for the reviewed box-diagram art in work/scenes.json.
// art.mjs is the pre-revision generator; do not re-run it (it would replace this art).
// This script only repositions/resizes existing visual objects; narration and plans are untouched.
// Usable art area: x 40-1160, y 110-540 (two-line captions start near stage y 557).
import fs from 'node:fs';import path from 'node:path';
const file=path.join(path.dirname(new URL(import.meta.url).pathname),'work/scenes.json');
const scenes=JSON.parse(fs.readFileSync(file,'utf8'));
const scene=id=>scenes.find(s=>s.id===id);
const obj=(s,id)=>{const o=scene(s).visual.objects.find(o=>o.id===id);if(!o)throw Error(`${s}: missing ${id}`);return o};
const place=(s,id,x,y,scale)=>{const o=obj(s,id);o.x=x;o.y=y;if(scale!==undefined)o.scale=scale;return o};
const rectWidth=(s,id,width)=>{const r=obj(s,id).visual.children.find(c=>c.type==='rect');r.attrs.width=width;r.attrs.x=-width/2};
const texts=(s,id,values)=>{const t=obj(s,id).visual.children.filter(c=>c.type==='text');values.forEach((v,i)=>{t[i].text=v})};

// Scene 1: conversation record, two separate observations joined by a proposed arrow, desk below.
place('scene-01','source-record',200,300);
texts('scene-01','source-record',['Conversation','The original record']);
place('scene-01','note-app',500,270);
place('scene-01','note-feed',1010,270);
place('scene-01','proposed-bracket',750,270,.85);
place('scene-01','desk',600,470);

// Scene 2: child and tablet on the room floor; records -> explanation on the right; question below.
place('scene-02','child',170,280);
place('scene-02','tablet',420,300);
rectWidth('scene-02','sofa',500);place('scene-02','sofa',330,490);
place('scene-02','app-tile',700,170);
place('scene-02','feed-frame',700,290);
place('scene-02','link-strip',860,230,.5);
place('scene-02','comparison-page',1035,230);
place('scene-02','feed-a',1035,350);
place('scene-02','question',860,470);

// Scene 3: observations around the comparison page, lifted link beneath, own term under the same check.
place('scene-03','note-app',200,230);
place('scene-03','comparison-page',600,240);
place('scene-03','note-feed',1000,230);
place('scene-03','lifted-link',600,380);
place('scene-03','working-title',420,470);
place('scene-03','hypothesis',780,470);

// Scene 4: reader beside the open book; source and later explanation compared on the right.
place('scene-04','reader',140,290);
place('scene-04','open-copy',420,270);
place('scene-04','comparison-link',705,270);
place('scene-04','source-case',970,190);
place('scene-04','explanation-case',970,360);
rectWidth('scene-04','reading-table',640);place('scene-04','reading-table',640,495);
const step=scene('scene-04').visual.actions.find(a=>a.actor==='reader'&&a.action==='moveTo');step.x=158;step.y=290;

fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
console.log('Layout repaired: '+file);
