// Book-owned staging for "Coherence Pressure" (round-4 repair, 2026-10-22).
// Authoritative art entry: regenerates every scene.visual in work/scenes.json.
// Narration (scene.lines) and audio are never touched. Shared helpers supply
// drawing verbs and the rigged person library only; layouts, palette, cast,
// facial expressions, arm poses and referents below belong to this book.
// Superseded scripts are archived in review-revision/round{1,2,3}-previous/.
//
// Round 3: dashes are sized in pixels per path (equal on every bridge); a
// book-owned closed warm smile ('inspired'); pupils sit at the eye centres so
// lookAt reads in both directions; pointing hands carry an index finger; the
// scene 3 reader aims up at the lens past the phone; the scene 4 reader steps
// to the reading table holding the pages by their edges; the scene 2 desk is
// wider than the laptop.
//
// Identity (work/visual-bible.json): cobalt and rust; a provisional, dashed
// bridge that only ever appears with an open question mark. No outlined label
// cards, no sub-labels: devices, furniture, pages and people carry the meaning.
//
// Round 2: arms are authored, held poses rather than transient rig gestures.
// Each person keeps empty armL/armR rig groups (for lookAt and expressions);
// every visible arm is a separate top-level object placed on the person's own
// x/y/scale/build, so a pose (open hand, invite, point, hand to chin, push
// away, holding pages) is held for the whole sentence. Round 4: poses swap in
// sequence (old out in 120 ms, then new in), never cross-faded. No character.gesture actions are used.
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
 grey: '#c3ccd8', skyTile: '#9fb6e6', peachTile: '#f2b48f', mintTile: '#a8d8cc', cream: '#f0e0bd'
};

// Stable cast across the film. Coats, trousers and hair stay distinct in Dark.
const CAST = {
 parent: {identity: 'person-11-neutral', coat: P.cobalt, coatNight: P.cobaltNight, legNight: '#c9d3e6', hair: '#39272D', hairNight: '#8c6b5c'},
 child: {identity: 'person-15-neutral', coat: P.rust, coatNight: P.rustNight, legNight: '#f3dcb8', hair: '#39272D', hairNight: '#9a7462'},
 reader: {identity: 'person-20-neutral', coat: P.teal, coatNight: P.tealNight, legNight: '#d6e4df'}
};

// Book-owned face overrides. The library 'curious' mouth is a frown and its
// 'skeptical' mouth a smirk; 'relieved' is used here as a calm, attentive face.
const FACES = {
 // Warm, low-intensity smile: closed lips, softly raised rounded brows.
 inspired: {mouth: 'M-10 19 Q0 27 10 19', brows: 'M-17 -16 Q-11 -20 -5 -16 M7 -16 Q13 -20 20 -16', fill: 'none'},
 curious: {mouth: 'M-7 21 Q0 25 7 21', brows: 'M-17 -18 L-5 -21 M7 -21 L20 -18'},
 skeptical: {mouth: 'M-9 22 L9 22', brows: 'M-17 -21 Q-11 -27 -5 -21 M7 -12 L20 -12'},
 relieved: {mouth: 'M-7 21 Q0 24 7 21', brows: 'M-17 -15 L-5 -16 M7 -16 L20 -15'}
};

// Arm poses in rig-local units (shoulders at R 32,-156 and L -34,-157).
// Each pose: stroke path from the shoulder and the hand position.
const POSE = {
 rest: {R: ['M32 -156 Q48 -143 52 -117', [53, -108]], L: ['M-34 -157 Q-46 -132 -47 -107', [-46, -97]]},
 ask: {R: ['M32 -156 Q72 -150 104 -184', [112, -190]]},                     // open questioning hand, chest height
 invite: {R: ['M32 -156 Q50 -120 92 -128', [102, -131]]},                   // palm-up offer, forearm rising toward the child
 point: {R: ['M32 -156 Q82 -166 122 -184', [131, -187]]},                   // explaining hand toward an object
 chin: {R: ['M32 -156 Q58 -142 60 -124 Q44 -152 26 -176', [21, -181]],     // elbow on the forearm, hand under the chin
  L: ['M-34 -157 Q-48 -116 -6 -116 Q32 -118 54 -122', [62, -122]]},         // forearm folded under the elbow
 stop: {L: ['M-34 -157 Q-70 -162 -100 -186', [-108, -190]]},                // palm out: pushing the app away
 reach: {R: ['M32 -156 Q72 -160 104 -178', [112, -182]]},                   // reaching to the phone
 aim: {L: ['M-34 -157 Q-96 -184 -146 -213', [-152, -216]]},                // raised arm aimed up at the far lens
 palm: {R: ['M32 -156 Q50 -122 84 -118', [93, -118]]}                       // second open hand, waist height
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
 const look = (id, target, beat, offsetMs, up = false) => a.actions.push({actor: id, action: 'lookAt', target, beat, offsetMs, durationMs: 600, ...(up ? {up: true} : {})});
 const walk = (id, beat, x, offsetMs, durationMs) => a.actions.push({actor: id, action: 'walkTo', beat, x, offsetMs, durationMs});
 const cast = {};

 // Rigged library person with this film's identity, clothing, faces and Dark
 // contrast. Coat-placket hairline, ground shadow and the white collar bar are
 // removed; the arm groups stay as empty rig parts (arms are separate objects).
 const person = (id, x, y, role, {scale = .9, seated = false, chair = '#d9b98a'} = {}) => {
  const c = CAST[role];
  const v = ASSETS[c.identity]('$asset', {coat: c.coat, dynamicExpressions: true});
  const skin = v.children.find(p => p.id === '$asset.armR').children.find(p => p.type === 'circle' || p.type === 'ellipse').attrs.fill;
  v.children = v.children.filter(p => p.id !== '$asset.shadow' && p.attrs?.d !== 'M-8 -174 L-2 -72' && !(p.type === 'rect' && p.attrs?.width === 31 && p.attrs?.height === 6));
  const walkTree = (node, fn) => {fn(node); for (const ch of node.children || []) walkTree(ch, fn);};
  walkTree(v, node => {
   for (const key of ['fill', 'stroke']) {
    if (node.attrs?.[key] === c.coat) node.themeAttrs = {...node.themeAttrs, night: {...node.themeAttrs?.night, [key]: c.coatNight}};
    if (c.hairNight && node.attrs?.[key] === c.hair) node.themeAttrs = {...node.themeAttrs, night: {...node.themeAttrs?.night, [key]: c.hairNight}};
   }
   const m = /^\$asset\.expression\.(\w+)\.(mouth|brows)$/.exec(node.id || '');
   if (m && FACES[m[1]]) node.attrs.d = FACES[m[1]][m[2]];
   if (m && m[2] === 'mouth' && FACES[m[1]]?.fill) {node.attrs.fill = FACES[m[1]].fill; node.attrs['stroke-width'] = 3;}
   // Pupils centred in the eyes (the library offsets them 2 px right), so the
   // fixed lookAt shift reads equally clearly to the left, right and upward.
   if (node.id === '$asset.pupils') for (const [i, pupil] of node.children.entries()) {pupil.attrs.cx = i ? 12 : -10; pupil.attrs.cy = 2; pupil.attrs.r = 3.2;}
   if (m && m[2] === 'brows') node.attrs['stroke-width'] = 3.2;
   // Sceptical squint: a skin-coloured lid narrows one eye under the raised
   // brow, so doubt still reads on darker skin where brows are low-contrast.
   if (node.id === '$asset.expression.skeptical') node.children.push(n('path', {d: 'M4 -8 Q12 -12 20 -8 L20 0 Q12 -3 4 0Z', fill: skin}));
  });
  const legs = v.children.filter(p => p.id === '$asset.legL' || p.id === '$asset.legR');
  if (seated) {
   for (const [leg, d] of [[legs[0], 'M-20 -82L-46 -53L-40 -10H-60'], [legs[1], 'M18 -82L46 -53L43 -10H65']]) leg.children = [{...path(d, '$trouser', 20), id: leg.id + '.bent'}];
   v.children.unshift({...n('g'), children: [night(n('path', {d: 'M-76 -183Q0 -210 76 -183L70 -65H-70Z', fill: chair}), '#6f5d49'), night(path('M-80 -68H80M-70 -66V0M70 -66V0', '#7a5f43', 9), '#b49a7c')]});
  }
  for (const leg of legs) walkTree(leg, node => {for (const key of ['fill', 'stroke']) if (node.attrs?.[key] && node.attrs[key] !== 'none') node.themeAttrs = {...node.themeAttrs, night: {...node.themeAttrs?.night, [key]: c.legNight}};});
  for (const part of ['armL', 'armR']) v.children.find(p => p.id === '$asset.' + part).children = [];
  cast[id] = {x, y, scale, role, skin, build: v.transform?.scaleX ?? 1};
  return a.add({id, asset: 'custom', x, y, scale, visual: v, options: {rig: 'character'}, meaning: `Stable ${role} figure; expressive face and gaze follow the sentence.`});
 };
 // One held arm pose, drawn on the person's own transform. `initial` arms fade
 // in with the body (shared feet origin); later poses scale from the shoulder.
 const arm = (owner, side, pose, {initial = false, extra = [], tag = ''} = {}) => {
  const p = cast[owner], c = CAST[p.role], [d, [hx, hy]] = POSE[pose][side];
  const id = `${owner}-arm-${side.toLowerCase()}-${pose}${tag}`;
  const hand = side === 'L' && pose === 'stop'
   ? n('ellipse', {cx: hx, cy: hy, rx: 10, ry: 15, fill: p.skin})
   : ['invite', 'ask'].includes(pose)
    // Open palm facing up: a flat cupped palm, fingers extended forward, thumb raised.
    ? {...n('g'), children: [n('path', {d: `M${hx - 12} ${hy - 6}Q${hx + 2} ${hy + 10} ${hx + 26} ${hy - 4}Q${hx + 28} ${hy - 9} ${hx + 22} ${hy - 9}Q${hx + 6} ${hy - 4} ${hx - 6} ${hy - 12}Z`, fill: p.skin}), path(`M${hx - 2} ${hy - 9}L${hx + 2} ${hy - 20}`, p.skin, 7)]}
    : n('circle', {cx: hx, cy: hy, r: 12, fill: p.skin});
  // Pointing poses add an index finger continuing the forearm's direction.
  const finger = [];
  if (['point', 'aim'].includes(pose)) {
   const [cx, cy] = d.trim().split(/[ QML]+/).filter(Boolean).map(Number).slice(-4, -2), len = Math.hypot(hx - cx, hy - cy);
   const fx = hx + (hx - cx) / len * 22, fy = hy + (hy - cy) / len * 22;
   finger.push(path(`M${hx} ${hy}L${fx.toFixed(1)} ${fy.toFixed(1)}`, p.skin, 8));
  }
  // The person's scale and build sit on an inner group, so the root origin is in
  // stage units and a later pose cross-fades about the shoulder without drift.
  const limb = {...n('g'), transform: {scale: p.scale, scaleX: p.build}, children: [...extra, night(path(d, c.coat, 20), c.coatNight), ...finger, hand]};
  const o = a.object(id, p.x, p.y, [limb], `${owner}: ${pose} arm (${side === 'R' ? 'right' : 'left'} side of the figure)`, 1);
  const [sx, sy] = side === 'R' ? [32, -156] : [-34, -157];
  o.visual.origin = initial ? [0, 0] : [p.scale * p.build * sx, p.scale * sy];
  a.add(o);
  return id;
 };
 // Swap one held arm pose for another in sequence: the old arm is gone in
 // 120 ms before the new arm starts, so two poses of one arm never overlap.
 const swap = (from, to, beat, offsetMs, durationMs = 300) => {hide(from, beat, offsetMs, 120); appear(to, beat, offsetMs + 130, Math.min(durationMs, 320));};
 const showBody = (id, arms, beat, offsetMs = 0, durationMs = 600) => {for (const x of [id, ...arms]) appear(x, beat, offsetMs, durationMs);};

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
 // They are derived from each curve's real length: 14 px dashes and 20 px
 // gaps (13 px clear between the 7 px round caps) on every bridge.
 const dashes = d => {
  const [x0, y0, cx, cy, x1, y1] = d.match(/-?\d+(\.\d+)?/g).map(Number);
  let len = 0, px = x0, py = y0;
  for (let i = 1; i <= 200; i++) {const t = i / 200, u = 1 - t, x = u * u * x0 + 2 * u * t * cx + t * t * x1, y = u * u * y0 + 2 * u * t * cy + t * t * y1; len += Math.hypot(x - px, y - py); px = x; py = y;}
  return `${(14 / len).toFixed(4)} ${(20 / len).toFixed(4)}`;
 };
 const openBridge = (d, qx, qy, r = 30) => [
  night(n('path', {d, fill: 'none', stroke: P.cobalt, 'stroke-width': 7, 'stroke-linecap': 'round', 'stroke-dasharray': dashes(d)}), P.cobaltNight),
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
  // Sentence 1: a parent notices two things on the family table; with raised
  // brows and an open questioning hand she feels the pull of a connection,
  // drawn only as a dashed bridge with a question mark.
  // Sentence 2: the parent offers an open hand to the child, who pushes the
  // unwanted app away, then turns and steps toward the stream of short videos.
  put('desk', 680, 445, lowTable(330, 82), 'Family table holding the tablet and the phone');
  put('note-app', 470, 368, tabletApp(), 'Tablet with an unwanted app marked for removal, standing on the table');
  put('note-feed', 890, 343, phoneFeed(), 'Phone playing a stream of short videos, standing on the table');
  put('proposed-bracket', 690, 230, openBridge('M-160 73Q0 -110 160 23', 0, -38, 32), 'A tempting connection between the two observations, drawn dashed and questioned, never as a causal arrow');
  person('parent', 190, 528, 'parent', {scale: .9});
  const pL = arm('parent', 'L', 'rest', {initial: true}), pR = arm('parent', 'R', 'rest', {initial: true});
  const pAsk = arm('parent', 'R', 'ask'), pInvite = arm('parent', 'R', 'invite');
  person('child', 620, 530, 'child', {scale: .72});
  const cL = arm('child', 'L', 'rest', {initial: true}), cR = arm('child', 'R', 'rest', {initial: true});
  const cStop = arm('child', 'L', 'stop');
  // Arms that take over as the child turns and steps toward the phone.
  const cLAfter = arm('child', 'L', 'rest', {tag: '-after'}), cReach = arm('child', 'R', 'reach');
  showBody('parent', [pL, pR], 1); appear('desk', 1, 0, 600); appear('note-app', 1, 350); appear('note-feed', 1, 850);
  express('parent', 1, 'curious', 200); look('parent', 'note-feed', 1, 600);
  swap(pR, pAsk, 1, 900);
  appear('proposed-bracket', 1, 1500, 900);
  showBody('child', [cL, cR], 2, 100, 700);
  look('parent', 'child', 2, 200); express('parent', 2, 'relieved', 300); swap(pAsk, pInvite, 2, 400, 600);
  express('child', 2, 'worried', 300); look('child', 'note-app', 2, 300); swap(cL, cStop, 2, 450, 450);
  look('child', 'note-feed', 2, 1600); express('child', 2, 'happy', 1700);
  swap(cStop, cLAfter, 2, 1650, 400); swap(cR, cReach, 2, 1650, 500);
  walk('child', 2, 730, 1800, 700); for (const id of [cLAfter, cReach]) move(id, 2, 730, 530, 1800, 700);
  return a.finish('A parent stands by a family table with a tablet (an unwanted app with a removal cross) and a phone streaming short videos. With raised brows and an open hand she senses a connection: a dashed bridge with a question mark arcs between the devices. She offers an open hand to the child, who pushes the app away and then turns and steps toward the videos, reaching for the phone.');
 }

 if (index === 1) {
  // Sentence 1: the seated parent turns toward the laptop with interest and
  // points at the model's reply; a solid bridge joins the two observations
  // under the words "attention" and "choice".
  // Sentence 2: the shared words stay, but the bridge breaks open into a
  // dashed, questioned link while the parent turns sceptical, hand to chin.
  person('parent', 200, 528, 'parent', {scale: .9, seated: true});
  const pL = arm('parent', 'L', 'rest', {initial: true}), pR = arm('parent', 'R', 'rest', {initial: true});
  const pPoint = arm('parent', 'R', 'point'), pChin = arm('parent', 'R', 'chin'), pFold = arm('parent', 'L', 'chin');
  put('desk', 410, 430, lowTable(126, 98), 'Desk beside the parent, wider than the laptop standing on it');
  put('comparison-page', 410, 330, [
   night(rect(-95, -68, 190, 136, P.ink, 12), P.bezelNight), rect(-84, -57, 168, 114, P.screen, 6),
   rect(-70, -45, 92, 22, P.grey, 10), rect(-6, -15, 76, 22, P.skyTile, 10), rect(-70, 15, 110, 28, P.grey, 10),
   path('M-50 34Q-22 12 6 34', P.cobalt, 4), n('circle', {cx: -50, cy: 34, r: 5, fill: P.rust}), n('circle', {cx: 6, cy: 34, r: 5, fill: P.teal}),
   night(n('path', {d: 'M-112 68H112L100 88H-100Z', fill: P.ink}), P.bezelNight)
  ], 'Laptop showing the AI conversation; the model’s reply contains a small bridge');
  put('app-tile', 630, 255, tabletApp(), 'The tablet observation: an unwanted app', {scale: .62});
  put('feed-frame', 900, 255, phoneFeed(), 'The phone observation: short videos', {scale: .7});
  put('link-strip', 777, 235, [night(path('M-88 20Q0 -105 88 20', P.cobalt, 9), P.cobaltNight)], 'The model’s confident bridge joining both observations');
  put('vocabulary', 777, 362, [words('attention', 0, 0, 40), words('choice', 0, 48, 40)], 'The shared vocabulary the explanation uses for both observations');
  put('question', 777, 235, openBridge('M-88 20Q0 -105 88 20', 0, -42, 30), 'The same bridge, now open: shared words do not show a shared cause');
  // Arms draw over the laptop edge, so they follow it in paint order.
  for (const id of [pL, pR, pPoint, pChin, pFold]) {const i = a.objects.findIndex(o => o.id === id); a.objects.push(...a.objects.splice(i, 1));}
  showBody('parent', [pL, pR], 1); appear('desk', 1, 0, 600); appear('comparison-page', 1, 150);
  appear('app-tile', 1, 450); appear('feed-frame', 1, 650);
  express('parent', 1, 'curious', 200); look('parent', 'comparison-page', 1, 300);
  swap(pR, pPoint, 1, 600, 600);
  appear('link-strip', 1, 1000, 1000); appear('vocabulary', 1, 1400, 600);
  look('parent', 'link-strip', 1, 1700, true);
  express('parent', 2, 'skeptical', 300);
  swap(pPoint, pChin, 2, 1300, 700); swap(pL, pFold, 2, 1300, 700);
  hide('link-strip', 2, 1900, 700); appear('question', 2, 2200, 900);
  look('parent', 'question', 2, 2400, true);
  return a.finish('Seated at a laptop, the parent leans in with interest and points at the model’s reply. A solid bridge joins the tablet and phone under the words “attention” and “choice”; then the bridge opens into a dashed link with a question mark while the parent, one brow raised and mouth flat, rests her chin on her hand and eyes the questioned arc.');
 }

 if (index === 2) {
  // Sentence 1: a worried reader points across to the convincing bridge held
  // under a magnifying glass. Sentence 2: the book appears right beside the
  // reader with a question sticker; the reader turns, calm and attentive, and
  // points at it as the same glass moves onto the book.
  // Devices sit low; the questioned bridge arches high above them, so the
  // reader's raised arm aims up at the lens with nothing in between.
  put('note-app', 220, 392, tabletApp(), 'Tablet observation', {scale: .8});
  put('note-feed', 480, 392, phoneFeed(), 'Phone observation', {scale: .8});
  put('lifted-link', 375, 330, openBridge('M-105 10Q-10 -330 105 -10', -5, -166, 28), 'The convincing connection, still untested');
  put('working-title', 985, 528, [closedBookVisual('$asset.book', {color: P.rust}), words('Coherence', 9, -152, 23, '#ffffff'), words('Pressure', 9, -121, 23, '#ffffff')], 'The book Coherence Pressure, its own term as the title', {scale: 1.3});
  put('hypothesis', 997, 447, [n('circle', {cx: 0, cy: 0, r: 32, fill: P.gold}), n('text', {x: 0, y: 16, 'font-size': 46, 'font-weight': 700, 'text-anchor': 'middle', fill: P.ink}, '?')], 'A question sticker on the cover: the book’s own term is a working hypothesis');
  person('reader', 790, 528, 'reader', {scale: .92});
  const rL = arm('reader', 'L', 'rest', {initial: true}), rR = arm('reader', 'R', 'rest', {initial: true});
  const rAim = arm('reader', 'L', 'aim'), rPalm = arm('reader', 'R', 'palm');
  const rLAfter = arm('reader', 'L', 'rest', {tag: '-after'});
  const rPoint = arm('reader', 'R', 'point');
  put('magnifier', 370, 164, magnifier(), 'Magnifying glass: the same scrutiny applied to every connection');
  showBody('reader', [rL, rR], 1); appear('note-app', 1, 150); appear('note-feed', 1, 300);
  appear('lifted-link', 1, 700, 800); appear('magnifier', 1, 1200, 800);
  express('reader', 1, 'worried', 200); look('reader', 'lifted-link', 1, 400, true);
  look('reader', 'magnifier', 1, 1400, true);
  swap(rL, rAim, 1, 800, 600); swap(rR, rPalm, 1, 900, 600);
  appear('working-title', 2, 0, 700); appear('hypothesis', 2, 500, 600);
  express('reader', 2, 'relieved', 200); look('reader', 'working-title', 2, 300);
  swap(rAim, rLAfter, 2, 400, 500); swap(rPalm, rPoint, 2, 500, 600);
  // The glass travels high over the reader's head (x and y keyed separately),
 // never across his face or chest, then drops onto the book once it is past
 // him. y 150 keeps the lens below the scene title and its handle above his head.
 a.actions.push({actor: 'magnifier', action: 'moveTo', beat: 2, x: 997, offsetMs: 700, durationMs: 1200});
 a.actions.push({actor: 'magnifier', action: 'moveTo', beat: 2, y: 150, offsetMs: 700, durationMs: 600});
 a.actions.push({actor: 'magnifier', action: 'moveTo', beat: 2, y: 447, offsetMs: 1500, durationMs: 650});
  return a.finish('A worried reader raises his arm, index finger aimed up at a magnifying glass held over a high, dashed, questioned bridge between a tablet and a phone below, his eyes on the lens. The book Coherence Pressure appears beside the reader with a question sticker; the reader turns, calm and attentive, and points at it while the same glass moves onto the book.');
 }

 // Scene 4. Sentence 1: the reader, with a closed warm smile, holds the
 // original conversation (chat bubbles) in one hand beside the polished
 // explanation (neat lines and a seal) in the other; the book lies open on the
 // reading table. Sentence 2: arms and pages lower, the reader takes a step up
 // to the table, eyes on the open book, and an open question rises - nothing
 // is ticked yet. Each hand overlaps its page's inner edge, so pages are held.
 const W = 124, H = 164, GRIP = 14;
 // Page rectangle placed so the hand (hx, hy) covers its inner edge.
 const pageAt = (side, hx, hy) => [side === 'L' ? hx + GRIP - W : hx - GRIP, hy - 90];
 const transcript = (hx, hy) => {
  const [x, y] = pageAt('L', hx, hy);
  return [
   rect(x, y, W, H, P.page, 6, {stroke: '#b9a98a', 'stroke-width': 3}),
   rect(x + 12, y + 16, 72, 22, P.grey, 10), rect(x + 54, y + 46, 52, 22, P.skyTile, 10), rect(x + 12, y + 76, 76, 22, P.grey, 10),
   rect(x + 54, y + 106, 44, 22, P.skyTile, 10), rect(x + 12, y + 136, 60, 18, P.grey, 9)
  ];
 };
 const polished = (hx, hy) => {
  const [x, y] = pageAt('R', hx, hy), ys = [22, 38, 54, 70, 92, 108, 124], ends = [100, 100, 100, 84, 100, 100, 64];
  return [
   rect(x, y, W, H, P.page, 6, {stroke: '#b9a98a', 'stroke-width': 3}),
   path(ys.map((v, i) => `M${x + 26} ${y + v}H${x + ends[i] + 10}`).join(''), P.ink, 4),
   n('circle', {cx: x + 96, cy: y + 140, r: 12, fill: P.gold}), n('path', {d: `M${x + 89} ${y + 149}L${x + 85} ${y + 158}L${x + 95} ${y + 154}ZM${x + 103} ${y + 149}L${x + 107} ${y + 158}L${x + 97} ${y + 154}Z`, fill: P.gold})
  ];
 };
 POSE.holdHigh = {L: ['M-34 -157 Q-72 -150 -104 -128', [-108, -124]], R: ['M32 -156 Q70 -150 100 -128', [104, -124]]};
 POSE.holdLow = {L: ['M-34 -157 Q-60 -128 -84 -92', [-88, -86]], R: ['M32 -156 Q58 -128 80 -92', [84, -86]]};
 const hold = (side, pose, tag = '', initial = false) => {
  const [hx, hy] = POSE[pose][side][1];
  return arm('reader', side, pose, {initial, tag, extra: side === 'L' ? transcript(hx, hy) : polished(hx, hy)});
 };
 person('reader', 400, 528, 'reader', {scale: 1});
 const hL = hold('L', 'holdHigh', '', true), hR = hold('R', 'holdHigh', '', true);
 const lL = hold('L', 'holdLow'), lR = hold('R', 'holdLow');
 put('reading-table', 905, 438, lowTable(150, 90), 'Reading table');
 const book = openBookVisual('$asset.book', {color: P.rust});
 const cream = node => {if (node.attrs?.fill === '$page') node.themeAttrs = {...node.themeAttrs, paper: {...node.themeAttrs?.paper, fill: P.cream}}; for (const ch of node.children || []) cream(ch);};
 cream(book);
 put('open-copy', 915, 375, [book], 'Coherence Pressure lying open at its source case; cream pages in the paper theme', {scale: .8});
 put('question', 700, 190, [n('circle', {cx: 0, cy: 0, r: 34, fill: P.gold}), n('text', {x: 0, y: 17, 'font-size': 50, 'font-weight': 700, 'text-anchor': 'middle', fill: P.ink}, '?')], 'The open question the film leaves with the viewer, between the reader and the open book');
 showBody('reader', [hL, hR], 1, 0, 700); appear('reading-table', 1, 0, 600); appear('open-copy', 1, 300, 800);
 express('reader', 1, 'inspired', 250); look('reader', 'open-copy', 1, 2600);
 express('reader', 2, 'curious', 200);
 swap(hL, lL, 2, 300, 600); swap(hR, lR, 2, 300, 600);
 // A step up to the reading table: the lowered polished page reaches its edge.
 walk('reader', 2, 552, 700, 1100); for (const id of [lL, lR]) move(id, 2, 552, 528, 700, 1100);
 look('reader', 'open-copy', 2, 1000);
 appear('question', 2, 1600, 900);
 return a.finish('A reader with a closed, warm smile holds the original conversation (chat bubbles) beside the polished explanation (neat lines and a seal), gripping each page by its edge; the book lies open on the reading table. Then the reader lowers both pages and steps up to the table, eyes on the open book, and a question mark rises between them: what would you check?');
}

scenes.forEach((scene, index) => { scene.visual = compose(index); });
fs.writeFileSync(file, JSON.stringify(scenes, null, 2) + '\n');
console.log('Staged ' + scenes.length + ' scenes: ' + scenes.map(s => s.id + ' (' + s.visual.objects.length + ' objects, ' + s.visual.actions.length + ' actions)').join(', '));
