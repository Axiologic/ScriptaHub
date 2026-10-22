// Book-owned staging for "Coherence Pressure" (round-1 repair, 2026-10-22).
// Authoritative art entry: regenerates every scene.visual in work/scenes.json.
// Narration (scene.lines) and audio are never touched. Shared helpers supply
// drawing verbs and the rigged person library only; layouts, palette, cast and
// referents below belong to this book. Superseded scripts are archived in
// review-revision/round1-previous/.
//
// Identity (work/visual-bible.json): cobalt and rust; a provisional, dashed
// bridge that only ever appears with an open question mark. No outlined label
// cards, no sub-labels: devices, furniture, pages and people carry the meaning.
import fs from 'node:fs';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {ASSETS} from '../../.agents/skills/shf-presentation-creator/scripts/lib/asset-library.mjs';
import {openBookVisual, closedBookVisual} from '../../.agents/skills/shf-presentation-creator/scripts/lib/book-art.mjs';

const file = new URL('./work/scenes.json', import.meta.url);
const scenes = JSON.parse(fs.readFileSync(file, 'utf8'));

// Palette. Fixed pale materials (screens, pages, tags) keep dark ink in every
// theme; anything dark that sits directly on the stage gets a Night override.
const P = {
 cobalt: '#3f62b0', cobaltNight: '#86a5ea', rust: '#cc6a3c', rustNight: '#f0935f',
 teal: '#2f8f83', tealNight: '#62c7b1', gold: '#e2a83c', page: '#fbf4e6', screen: '#e9f0f7',
 ink: '#2b3446', bezelNight: '#8d9cb4', wood: '#c99a5e', woodNight: '#9a7448',
 grey: '#c3ccd8', skyTile: '#9fb6e6', peachTile: '#f2b48f', mintTile: '#a8d8cc'
};

// Stable cast across the film. Coats, trousers and hair stay distinct in Dark.
const CAST = {
 parent: {identity: 'person-11-neutral', coat: P.cobalt, coatNight: P.cobaltNight, legNight: '#c9d3e6', hair: '#39272D', hairNight: '#8c6b5c'},
 child: {identity: 'person-15-neutral', coat: P.rust, coatNight: P.rustNight, legNight: '#f3dcb8', hair: '#39272D', hairNight: '#9a7462'},
 reader: {identity: 'person-20-neutral', coat: P.teal, coatNight: P.tealNight, legNight: '#d6e4df'}
};

function compose(index) {
 const a = stageAuthor(), {n, path} = a;
 const rect = (x, y, w, h, fill, rx = 0, extra = {}) => n('rect', {x, y, width: w, height: h, fill, rx, ...extra});
 const night = (node, value) => {const key = node.attrs.fill && node.attrs.fill !== 'none' ? 'fill' : 'stroke'; node.themeAttrs = {...node.themeAttrs, night: {...node.themeAttrs?.night, [key]: value}}; return node;};
 const words = (value, x, y, size, color = '$ink') => n('text', {x, y, 'font-size': size, 'font-weight': 700, 'letter-spacing': -0.3, 'text-anchor': 'middle', fill: color}, value);
 const put = (id, x, y, kids, meaning, {scale = 1, anchors} = {}) => {const o = a.object(id, x, y, kids, meaning, scale); if (anchors) o.visual.anchors = anchors; a.add(o); return id;};
 const appear = (id, beat, offsetMs = 250, durationMs = 700) => a.actions.push({actor: id, action: 'appear', beat, offsetMs, durationMs});
 const hide = (id, beat, offsetMs, durationMs = 700) => a.actions.push({actor: id, action: 'disappear', beat, offsetMs, durationMs});
 const move = (id, beat, x, y, offsetMs, durationMs = 1400) => a.actions.push({actor: id, action: 'moveTo', beat, x, y, offsetMs, durationMs});
 const express = (id, beat, emotion, offsetMs = 200) => a.actions.push({actor: id, action: 'character.express', emotion, beat, offsetMs, durationMs: 600});
 const gesture = (id, beat, g, offsetMs, durationMs = 1800) => a.actions.push({actor: id, action: 'character.gesture', gesture: g, beat, offsetMs, durationMs});
 const look = (id, target, beat, offsetMs) => a.actions.push({actor: id, action: 'lookAt', target, beat, offsetMs, durationMs: 600});

 // Rigged library person with this film's identity, clothing and Dark contrast.
 // The coat-placket hairline and ground shadow are removed (no stray torso line).
 const person = (id, x, y, role, {scale = .9, seated = false, chair = '#d9b98a', arms} = {}) => {
  const c = CAST[role];
  const v = ASSETS[c.identity]('$asset', {coat: c.coat, dynamicExpressions: true});
  v.children = v.children.filter(p => p.id !== '$asset.shadow' && p.attrs?.d !== 'M-8 -174 L-2 -72');
  const walk = (node, fn) => {fn(node); for (const ch of node.children || []) walk(ch, fn);};
  walk(v, node => {
   for (const key of ['fill', 'stroke']) {
    if (node.attrs?.[key] === c.coat) node.themeAttrs = {...node.themeAttrs, night: {...node.themeAttrs?.night, [key]: c.coatNight}};
    if (c.hairNight && node.attrs?.[key] === c.hair) node.themeAttrs = {...node.themeAttrs, night: {...node.themeAttrs?.night, [key]: c.hairNight}};
   }
  });
  const legs = v.children.filter(p => p.id === '$asset.legL' || p.id === '$asset.legR');
  if (seated) {
   for (const [leg, d] of [[legs[0], 'M-20 -82L-46 -53L-40 -10H-60'], [legs[1], 'M18 -82L46 -53L43 -10H65']]) leg.children = [{...path(d, '$trouser', 20), id: leg.id + '.bent'}];
   v.children.unshift({...n('g'), children: [night(n('path', {d: 'M-76 -183Q0 -210 76 -183L70 -65H-70Z', fill: chair}), '#6f5d49'), night(path('M-80 -68H80M-70 -66V0M70 -66V0', '#7a5f43', 9), '#b49a7c')]});
  }
  for (const leg of legs) walk(leg, node => {for (const key of ['fill', 'stroke']) if (node.attrs?.[key] && node.attrs[key] !== 'none') node.themeAttrs = {...node.themeAttrs, night: {...node.themeAttrs?.night, [key]: c.legNight}};});
  if (arms) for (const [part, kids] of Object.entries(arms)) v.children.find(p => p.id === '$asset.' + part).children = kids;
  return a.add({id, asset: 'custom', x, y, scale, visual: v, options: {rig: 'character'}, meaning: `Stable ${role} figure; expressive face, gaze and hands follow the sentence.`});
 };

 // A tablet showing an app grid; the unwanted app carries a removal cross.
 const tabletApp = () => [
  night(rect(-95, -65, 190, 130, P.ink, 18), P.bezelNight),
  rect(-85, -55, 170, 110, P.screen, 9), n('circle', {cx: 0, cy: -60, r: 2.5, fill: '#8193ad'}),
  ...[[-50, -22, P.teal], [0, -22, P.gold], [-50, 24, P.cobalt], [0, 24, P.teal], [50, 24, P.cobalt]].map(([x, y, f]) => rect(x - 17, y - 17, 34, 34, f, 8)),
  rect(31, -41, 38, 38, P.rust, 9),
  n('circle', {cx: 66, cy: -40, r: 14, fill: '#ffffff', stroke: P.rust, 'stroke-width': 3}),
  path('M60 -46L72 -34M72 -46L60 -34', P.rust, 4)
 ];
 // A phone streaming short vertical videos.
 const phoneFeed = () => [
  night(rect(-50, -90, 100, 180, P.ink, 18), P.bezelNight),
  rect(-43, -78, 86, 158, P.screen, 9), rect(-12, -86, 24, 4, '#8193ad', 2),
  rect(-34, -70, 68, 42, P.skyTile, 6), rect(-34, -21, 68, 48, P.peachTile, 6), rect(-34, 34, 68, 36, P.mintTile, 6),
  n('path', {d: 'M-8 -10L12 3L-8 16Z', fill: '#ffffff'}),
  path('M36 -60V60', '#8193ad', 3)
 ];
 // The proposed bridge: always dashed, always carrying an open question mark.
 // The player normalises every path to pathLength=1, so dashes are fractions.
 const openBridge = (d, qx, qy, r = 30) => [
  night(n('path', {d, fill: 'none', stroke: P.cobalt, 'stroke-width': 7, 'stroke-linecap': 'round', 'stroke-dasharray': '0.034 0.028'}), P.cobaltNight),
  n('circle', {cx: qx, cy: qy, r, fill: P.gold}),
  n('text', {x: qx, y: qy + r * .48, 'font-size': r * 1.45, 'font-weight': 700, 'text-anchor': 'middle', fill: P.ink}, '?')
 ];
 const magnifier = () => [
  n('circle', {cx: 0, cy: 0, r: 62, fill: '#cfe3f548'}),
  night(n('circle', {cx: 0, cy: 0, r: 62, fill: 'none', stroke: P.ink, 'stroke-width': 12}), '#c9d6e8'),
  path('M47 47L102 102', '#9a6a2e', 20)
 ];
 const lowTable = (half, legs = 78) => [night(rect(-half, -12, half * 2, 24, P.wood, 6), P.woodNight), night(path(`M${-half + 24} 12V${legs}M${half - 24} 12V${legs}`, '#8a6440', 14), '#c4a07a')];

 if (index === 0) {
  // Sentence 1: a parent notices two things on the family table and feels the
  // pull of a connection - drawn only as a dashed bridge with a question mark.
  // Sentence 2: the child arrives: recoils from the unwanted app, then turns
  // straight back to the stream of short videos.
  put('desk', 680, 445, lowTable(330, 82), 'Family table holding the tablet and the phone');
  put('note-app', 480, 368, tabletApp(), 'Tablet with an unwanted app marked for removal, standing on the table');
  put('note-feed', 880, 343, phoneFeed(), 'Phone playing a stream of short videos, standing on the table');
  put('proposed-bracket', 690, 230, openBridge('M-160 73Q0 -110 160 23', 0, -38, 32), 'A tempting connection between the two observations, drawn dashed and questioned, never as a causal arrow');
  person('parent', 175, 528, 'parent', {scale: .9});
  person('child', 690, 530, 'child', {scale: .66});
  appear('desk', 1, 0, 600); appear('parent', 1, 0, 600); appear('note-app', 1, 350); appear('note-feed', 1, 850);
  express('parent', 1, 'curious', 300); look('parent', 'note-feed', 1, 900);
  gesture('parent', 1, 'question', 1500, 1900);
  appear('proposed-bracket', 1, 1500, 900);
  appear('child', 2, 100, 800);
  look('parent', 'child', 2, 200); express('parent', 2, 'neutral', 300); gesture('parent', 2, 'invite', 500, 1800);
  express('child', 2, 'skeptical', 400); look('child', 'note-app', 2, 900); gesture('child', 2, 'recoil', 1000, 1500);
  look('child', 'note-feed', 2, 2900); express('child', 2, 'happy', 3000);
  return a.finish('A parent stands by a family table holding a tablet (an unwanted app with a removal cross) and a phone streaming short videos. A dashed bridge with a question mark arcs between the devices: the pull to connect. The child arrives, recoils from the app and turns back to the videos.');
 }

 if (index === 1) {
  // Sentence 1: the parent reads the model's answer on a laptop; a solid bridge
  // joins the two observations under the words "attention" and "choice".
  // Sentence 2: the shared words stay, but the bridge breaks open into a
  // dashed, questioned link while the parent turns sceptical, hand to chin.
  person('parent', 190, 528, 'parent', {scale: .9, seated: true});
  put('desk', 380, 430, lowTable(95, 98), 'Small desk beside the parent');
  put('comparison-page', 380, 330, [
   night(rect(-95, -68, 190, 136, P.ink, 12), P.bezelNight), rect(-84, -57, 168, 114, P.screen, 6),
   rect(-70, -45, 92, 22, P.grey, 10), rect(-6, -15, 76, 22, P.skyTile, 10), rect(-70, 15, 110, 28, P.grey, 10),
   path('M-50 34Q-22 12 6 34', P.cobalt, 4), n('circle', {cx: -50, cy: 34, r: 5, fill: P.rust}), n('circle', {cx: 6, cy: 34, r: 5, fill: P.teal}),
   night(n('path', {d: 'M-112 68H112L100 88H-100Z', fill: P.ink}), P.bezelNight)
  ], 'Laptop showing the AI conversation; the model’s reply contains a small bridge');
  put('app-tile', 690, 255, tabletApp(), 'The tablet observation: an unwanted app', {scale: .62});
  put('feed-frame', 1010, 255, phoneFeed(), 'The phone observation: short videos', {scale: .7});
  put('link-strip', 862, 230, [night(path('M-113 20Q0 -115 113 20', P.cobalt, 9), P.cobaltNight)], 'The model’s confident bridge joining both observations');
  put('vocabulary', 862, 330, [words('attention', 0, 0, 40), words('choice', 0, 48, 40)], 'The shared vocabulary the explanation uses for both observations');
  put('question', 862, 230, openBridge('M-113 20Q0 -115 113 20', 0, -47, 30), 'The same bridge, now open: shared words do not show a shared cause');
  appear('parent', 1, 0, 600); appear('desk', 1, 0, 600); appear('comparison-page', 1, 150);
  appear('app-tile', 1, 450); appear('feed-frame', 1, 650);
  express('parent', 1, 'curious', 250); look('parent', 'comparison-page', 1, 300);
  appear('link-strip', 1, 1000, 1000); appear('vocabulary', 1, 1500, 600);
  look('parent', 'link-strip', 1, 1900); gesture('parent', 1, 'explain', 2400, 1800);
  express('parent', 2, 'skeptical', 300); gesture('parent', 2, 'reflect', 2400, 3800);
  hide('link-strip', 2, 2000, 700); appear('question', 2, 2300, 900);
  return a.finish('Seated at a laptop, the parent reads the model’s explanation. A solid bridge joins the tablet and phone under the words “attention” and “choice”; then the bridge opens into a dashed link with a question mark while the parent turns sceptical, hand to chin.');
 }

 if (index === 2) {
  // Sentence 1: a reader holds the convincing bridge under a magnifying glass.
  // Sentence 2: the book itself arrives with its own term on a tag, and the
  // same glass moves onto it.
  person('reader', 160, 528, 'reader', {scale: .92});
  put('note-app', 380, 315, tabletApp(), 'Tablet observation', {scale: .8});
  put('note-feed', 690, 315, phoneFeed(), 'Phone observation', {scale: .8});
  put('lifted-link', 540, 250, openBridge('M-84 14Q0 -150 125 -7', 0, -66, 28), 'The convincing connection, still untested');
  put('working-title', 965, 528, [closedBookVisual('$asset.book', {color: P.rust}), words('Coherence', 9, -152, 23, '#ffffff'), words('Pressure', 9, -121, 23, '#ffffff')], 'The book Coherence Pressure, its own term as the title', {scale: 1.35});
  put('hypothesis', 980, 444, [n('circle', {cx: 0, cy: 0, r: 32, fill: P.gold}), n('text', {x: 0, y: 16, 'font-size': 46, 'font-weight': 700, 'text-anchor': 'middle', fill: P.ink}, '?')], 'A question sticker on the cover: the book’s own term is a working hypothesis');
  put('magnifier', 540, 190, magnifier(), 'Magnifying glass: the same scrutiny applied to every connection');
  appear('reader', 1, 0, 600); appear('note-app', 1, 150); appear('note-feed', 1, 300);
  appear('lifted-link', 1, 800, 800); appear('magnifier', 1, 1400, 800);
  express('reader', 1, 'worried', 250); look('reader', 'lifted-link', 1, 500); gesture('reader', 1, 'question', 1000, 1900);
  appear('working-title', 2, 0, 700); appear('hypothesis', 2, 600, 700);
  express('reader', 2, 'relieved', 200); look('reader', 'working-title', 2, 400);
  move('magnifier', 2, 980, 444, 900, 1400); gesture('reader', 2, 'explain', 1300, 1900);
  return a.finish('A reader looks worried at a dashed, questioned bridge between the tablet and phone under a magnifying glass. The book Coherence Pressure appears with a question sticker on its cover, and the same glass moves onto it.');
 }

 // Scene 4. Sentence 1: the reader holds the original conversation (chat
 // bubbles) in one hand beside the polished explanation (neat lines and a seal)
 // in the other; the book lies open on the reading table. Sentence 2: the
 // reader settles and an open question rises above - nothing is ticked yet.
 const transcript = [
  rect(-232, -222, 124, 164, P.page, 6, {stroke: '#b9a98a', 'stroke-width': 3}),
  rect(-220, -206, 72, 22, P.grey, 10), rect(-178, -176, 60, 22, P.skyTile, 10), rect(-220, -146, 84, 22, P.grey, 10),
  rect(-170, -116, 52, 22, P.skyTile, 10), rect(-220, -86, 64, 20, P.grey, 10)
 ];
 const polished = [
  rect(108, -222, 124, 164, P.page, 6, {stroke: '#b9a98a', 'stroke-width': 3}),
  path('M124 -200H216M124 -184H216M124 -168H216M124 -152H200M124 -130H216M124 -114H216M124 -98H180', P.ink, 4),
  n('circle', {cx: 198, cy: -80, r: 13, fill: P.gold}), n('path', {d: 'M190 -70L186 -60L196 -64ZM206 -70L210 -60L200 -64Z', fill: P.gold})
 ];
 const skin = '#C98E6B';
 person('reader', 470, 528, 'reader', {scale: 1, arms: {
  armL: [...transcript, night(path('M-34 -157Q-72 -150 -104 -124', P.teal, 20), P.tealNight), n('circle', {cx: -108, cy: -118, r: 11, fill: skin})],
  armR: [...polished, night(path('M32 -156Q70 -150 100 -124', P.teal, 20), P.tealNight), n('circle', {cx: 104, cy: -118, r: 11, fill: skin})]
 }});
 put('reading-table', 925, 438, lowTable(150, 90), 'Reading table');
 put('open-copy', 925, 375, [openBookVisual('$asset.book', {color: P.rust})], 'Coherence Pressure lying open at its source case', {scale: .8});
 put('question', 470, 196, [n('circle', {cx: 0, cy: 0, r: 34, fill: P.gold}), n('text', {x: 0, y: 17, 'font-size': 50, 'font-weight': 700, 'text-anchor': 'middle', fill: P.ink}, '?')], 'The open question the film leaves with the viewer');
 appear('reader', 1, 0, 700); appear('reading-table', 1, 0, 600); appear('open-copy', 1, 300, 800);
 express('reader', 1, 'happy', 250); look('reader', 'open-copy', 1, 2600);
 express('reader', 2, 'curious', 200); gesture('reader', 2, 'release', 600, 1600); appear('question', 2, 1100, 900);
 return a.finish('A reader holds the original conversation (chat bubbles) beside the polished explanation (neat lines and a seal); the book lies open on the reading table. Then the reader settles and a question mark rises: what would you check?');
}

scenes.forEach((scene, index) => { scene.visual = compose(index); });
fs.writeFileSync(file, JSON.stringify(scenes, null, 2) + '\n');
console.log('Staged ' + scenes.length + ' scenes: ' + scenes.map(s => s.id + ' (' + s.visual.objects.length + ' objects, ' + s.visual.actions.length + ' actions)').join(', '));
