// Book-owned staging for "A Mind Does Not Fit in a Feed".
// Identity (work/visual-bible.json): a column of short feed fragments is crossed
// by one continuous orange thread that gathers them. Shared helpers supply only
// drawing verbs; layouts, palette and referents below belong to this book.
import fs from 'node:fs';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
import {storyPerson, storyGesture} from '../../tools/shf/people-poses.mjs';

const file = new URL('./work/scenes.json', import.meta.url);
const scenes = JSON.parse(fs.readFileSync(file, 'utf8'));

// Cover palette plus tints of it. Navy is lifted in Night so it never vanishes.
const P = {orange: '#f2a65a', slate: '#4d6a8e', navy: '#0f2034', cream: '#fbf0de', mist: '#c9d6e4', rust: '#c9743a', sand: '#e6cfae'};
const NIGHT = {navy: '#c9d6e4', slate: '#7d9cc2'};
const READER = {identity: 'person-21-neutral', coat: P.slate, ink: P.navy};

function compose(index) {
 const a = stageAuthor(), {n, path, tint} = a;
 const rect = (x, y, w, h, fill, rx = 0, extra = {}) => n('rect', {x, y, width: w, height: h, fill, rx, ...extra});
 const night = (node, color) => tint(node, color);
 const words = (value, x, y, size = 26, color = '$ink', weight = 600, anchor = 'middle') => n('text', {x, y, 'font-size': size, 'font-weight': weight, 'letter-spacing': -0.3, 'text-anchor': anchor, fill: color}, value);
 const put = (id, x, y, kids, meaning, {beat, offsetMs = 250, scale = 1, anchors} = {}) => {
  const object = a.object(id, x, y, kids, meaning, scale);
  if (anchors) object.visual.anchors = anchors;
  a.add(object);
  if (beat) a.actions.push({actor: id, action: 'appear', beat, offsetMs, durationMs: 650});
  return id;
 };
 const hide = (id, beat, offsetMs = 250, durationMs = 700) => a.actions.push({actor: id, action: 'disappear', beat, offsetMs, durationMs});
 const move = (id, beat, x, y, offsetMs = 400, durationMs = 1100) => a.actions.push({actor: id, action: 'moveTo', beat, offsetMs, x, y, durationMs});
 const express = (id, beat, emotion, offsetMs = 150) => a.actions.push({actor: id, action: 'character.express', emotion, beat, offsetMs, durationMs: 700});
 const thread = (id, from, fromAnchor, to, toAnchor, beat, offsetMs, meaning, bend = 0) => {
  a.connections.push({id, from: {node: from, anchor: fromAnchor}, to: {node: to, anchor: toAnchor}, width: 7, color: P.orange, bend, meaning});
  a.actions.push({actor: id, action: 'connection.draw', beat, offsetMs, durationMs: 1100});
 };
 const cardAnchors = {left: [-55, 0], right: [55, 0], top: [0, -32], bottom: [0, 32]};
 // A short feed fragment: complete-looking surface, no visible premises.
 const fragment = (stripe, lines = [70, 46], mark) => [
  rect(-55, -32, 110, 64, P.cream, 10),
  rect(-55, -32, 12, 64, stripe, 6),
  ...lines.map((w, i) => path(`M-30 ${-10 + i * 20}H${-30 + w}`, P.navy, 6)),
  ...(mark ? [mark] : [])
 ];
 // Book-owned adjustments to the shared reader: the collar bar reads as a stray
 // stripe over the scarf, so it is removed; a few faces are re-authored so the
 // planned feeling is legible (open curiosity, end-of-day fatigue, friendly
 // encouragement); the chair frame keeps its own warm hue at Night; and a
 // reader whose referents sit to her left is mirrored so gestures address them.
 const SKIN = '#885A43';
 const FACES = {
  curious: {mouth: 'M-7 21 Q0 26 8 20', brows: 'M-17 -17 Q-11 -23 -5 -18 M7 -18 Q13 -23 20 -17'},
  tired: {mouth: 'M-7 24 Q0 23 7 24', brows: 'M-17 -8 L-5 -7 M7 -7 L20 -8', lids: true},
  determined: {mouth: 'M-9 19 Q0 27 9 19', brows: 'M-17 -15 L-5 -17 M7 -17 L20 -15'}
 };
 const reader = (id, x, y, {faceLeft = false, ...opts} = {}) => {
  storyPerson(a, id, x, y, {...READER, ...opts});
  const o = a.objects.find(item => item.id === id), v = o.visual;
  v.children = v.children.filter(c => !(c.type === 'rect' && c.attrs?.fill === '$page' && c.attrs.y === -167));
  const head = v.children.find(c => c.id === '$asset.head');
  for (const [state, face] of Object.entries(FACES)) {
   const g = head.children.find(c => c.id === '$asset.expression.' + state);
   g.children.find(c => c.id.endsWith('.mouth')).attrs.d = face.mouth;
   g.children.find(c => c.id.endsWith('.brows')).attrs.d = face.brows;
   if (face.lids) g.children.push(
    {id: g.id + '.lids', type: 'path', attrs: {d: 'M-17 -7.5H-3V1.5H-17ZM5 -7.5H19V1.5H5Z', fill: SKIN}},
    {id: g.id + '.lidline', type: 'path', attrs: {d: 'M-17 1.5H-3M5 1.5H19', fill: 'none', stroke: '$structural', 'stroke-width': 2, 'stroke-linecap': 'round'}});
  }
  if (opts.seated) for (const child of v.children[0].children || []) if (child.attrs?.stroke && child.attrs.stroke !== 'none') child.themeAttrs = {night: {stroke: '#d9b98c'}};
  if (faceLeft) {
   v.transform = {...v.transform, scaleX: -(v.transform?.scaleX || 1)};
   // lookAt computes its sign in world x, so a mirrored reader keeps a fixed,
   // authored gaze toward her referents instead.
   const eyes = head.children.find(c => c.id === '$asset.eyes'), pupils = eyes.children.find(c => c.id === '$asset.pupils');
   pupils.transform = {...pupils.transform, x: 3};
  }
  return id;
 };

 if (index === 0) {
  // Book lens: a reader at the end of a full day, a feed column, a field of
  // fragments, an idea left open, and the thread that finally crosses the column.
  reader('reader', 250, 540, {seated: true, scale: .95, chair: P.sand});
  put('feed', 600, 330, [
   night(rect(-75, -150, 150, 300, P.slate, 24), NIGHT.slate),
   rect(-58, -128, 116, 250, '#3e5776', 14),
   ...[[-104, 88, P.orange], [-62, 60, P.mist], [-20, 76, P.orange], [22, 50, P.mist], [64, 82, P.orange]].map(([y, w, c]) => rect(-44, y, w, 18, c, 9))
  ], 'A feed column: short fragments arriving one after another', {anchors: {left: [-75, -32], right: [75, -32], top: [0, -150], bottom: [0, 150]}});
  const field = [
   ['frag-1', 790, 190, P.orange, 1, 400], ['frag-2', 950, 172, P.slate, 1, 1100], ['frag-3', 1080, 228, P.rust, 1, 1800], ['frag-4', 770, 318, P.orange, 1, 2500],
   ['frag-5', 905, 300, P.slate, 2, 200], ['frag-6', 1065, 350, P.rust, 2, 900], ['frag-7', 800, 452, P.orange, 2, 1600], ['frag-8', 950, 440, P.slate, 2, 2300], ['frag-9', 1085, 470, P.orange, 2, 3000]
  ];
  for (const [id, x, y, stripe, beat, offsetMs] of field) {
   put(id, 600, 330, fragment(stripe, [[70, 46], [52, 64], [66, 38]][x % 3]), 'One short idea met during the day; its conclusion is visible, its reasoning is not', {beat, offsetMs, anchors: cardAnchors});
   move(id, beat, x, y, offsetMs + 200, 1000);
  }
  // The question that never developed: an orange loop with a visible gap.
  put('idea-open', 250, 182, [path('M0 -40A40 40 0 1 1 -40 0', P.orange, 10)], 'An idea begun but left unfinished', {beat: 1, offsetMs: 3400, anchors: {left: [-40, 0], right: [40, 0], top: [0, -40], bottom: [0, 40]}});
  // The impression of understanding: a confident check drawn only in outline.
  put('impression', 430, 196, [
   n('circle', {cx: 0, cy: 0, r: 42, fill: 'none', stroke: '$ink', 'stroke-width': 4, 'stroke-dasharray': '9 8'}),
   n('path', {d: 'M-20 0L-5 16L22 -16', fill: 'none', stroke: '$ink', 'stroke-width': 6, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-dasharray': '.16 .1'}),
   words('Impression', 0, 84, 32, '$ink', 700)
  ], 'The impression of understanding: a hollow, dashed confirmation with nothing inside', {beat: 3, offsetMs: 1500});
  // Contrast: the short form itself is not the adversary; it keeps a solid,
  // ordinary check, while the impression is only a hollow outline.
  put('short-form', 600, 528, [
   path('M-118 -2L-106 10L-88 -12', P.orange, 7),
   words('Short form', 10, 10, 32, '$ink', 700)
  ], 'The short form itself: an ordinary, solid check, not the adversary', {beat: 3, offsetMs: 200});
  hide('impression', 4, 150, 600);
  hide('short-form', 4, 150, 600);
  // Continuity: one thread crosses the feed column and stitches fragments,
  // including a contrasting one, into a single line of thought.
  thread('thread-1', 'idea-open', 'right', 'feed', 'left', 4, 500, 'The open question enters the feed instead of resetting', -40);
  put('stitch', 600, 330, [path('M-75 -32H75', P.orange, 7)], 'The same thread crosses the column of fragments, through the gap between them, and keeps going', {beat: 4, offsetMs: 1300, anchors: {left: [-75, -32], right: [75, -32], top: [0, -40], bottom: [0, -24]}});
  thread('thread-1b', 'stitch', 'right', 'frag-4', 'left', 4, 1600, 'Leaving the column whole, the thought carries on to the next fragment');
  thread('thread-2', 'frag-4', 'right', 'frag-5', 'left', 4, 2400, 'The thought develops from one fragment to the next');
  thread('thread-3', 'frag-5', 'right', 'frag-6', 'left', 4, 3200, 'It reaches a contrasting fragment and faces contradiction', 20);
  put('idea-close', 250, 182, [path('M-40 0A40 40 0 0 1 0 -40', P.orange, 10), a.dot(0, 0, 11, P.orange)], 'The loop closes: the idea has had time to develop', {beat: 4, offsetMs: 4100});
  storyGesture(a, 'reader', 2, 'question', 4900);
  storyGesture(a, 'reader', 4, 'resolve');
  express('reader', 1, 'tired');
  express('reader', 2, 'curious');
  express('reader', 3, 'skeptical');
  express('reader', 4, 'inspired');
  a.actions.push({actor: 'reader', action: 'lookAt', target: 'feed', beat: 1, offsetMs: 300, durationMs: 700});
  return a.finish('A seated reader faces a feed column that releases many short fragments; an orange idea above the reader stays open. A dashed, hollow check stands for the impression of understanding. Then one orange thread leaves the open idea, crosses the feed column and stitches three fragments, including a contrasting one, before the loop closes. Qualitative illustration of the book\'s argument for intellectual continuity.');
 }

 if (index === 1) {
  // Content lens: three chapter workbenches side by side, no person.
  const chapter = (id, x, number, beat) => put(id, x, 148, [a.dot(0, 0, 20, P.orange), words(String(number), 0, 9, 24, P.navy, 700)], `Chapter ${number} of the book`, {beat, offsetMs: 100});
  // Chapter One: a visible conclusion resting on reasoning the fragment omits.
  chapter('ch-1', 230, 1, 1);
  put('claim', 230, 210, [
   rect(-90, -34, 180, 68, P.cream, 10), rect(-90, -34, 180, 12, P.orange, 6),
   path('M-60 0H50M-60 18H20', P.navy, 6), rect(64, -12, 8, 22, P.rust, 3), a.dot(68, 18, 4, P.rust)
  ], 'A fragment\'s confident conclusion');
  const debt = [['premises', 'Premises', 1300], ['conditions', 'Conditions', 2100], ['alternatives', 'Alternatives', 2900]];
  debt.forEach(([id, value, offsetMs], i) => put(id, 230, 282 + i * 58, [
   n('rect', {x: -90, y: -22, width: 180, height: 44, rx: 8, fill: 'none', stroke: '$ink', 'stroke-width': 3, 'stroke-dasharray': '8 6'}),
   words(value, 0, 10, 28, '$ink', 700)
  ], `Hidden ${value.toLowerCase()} that the fragment does not show`, {beat: 1, offsetMs}));
  put('debt-label', 230, 476, [words('Context debt', 0, 0, 28, '$ink', 700)], 'The book\'s working concept for the missing reasoning, not a validated measure', {beat: 1, offsetMs: 3700});
  // Chapter Two: claims about attention sorted by kind, not by conviction.
  chapter('ch-2', 600, 2, 2);
  const slots = [['Findings', 215], ['Interpretations', 300], ['Recommendations', 385]];
  put('sorter', 600, 0, slots.flatMap(([value, y]) => [
   night(rect(-150, y - 34, 300, 68, P.slate, 14), NIGHT.slate), rect(-136, y - 22, 44, 44, '#3e5776', 10), words(value, 30, y + 9, 25, '#ffffff', 700)
  ]), 'Three separate trays: research findings, plausible interpretations, normative recommendations', {beat: 2, offsetMs: 150});
  const token = (id, kids, y, offsetMs, meaning) => {
   // Tokens rise along the slot column, never across the tray labels.
   put(id, 486, 478, [rect(-19, -19, 38, 38, P.cream, 8), ...kids], meaning, {beat: 2, offsetMs});
   move(id, 2, 486, y, offsetMs + 350, 900);
  };
  token('finding', [path('M-9 9V0M0 9V-9M9 9V-3', P.navy, 5)], 215, 600, 'A research finding about attention');
  token('interpretation', [path('M-9 3Q-4 -7 0 0T9 -3', P.navy, 5)], 300, 1400, 'A plausible interpretation of that finding');
  token('recommendation', [path('M-9 0H8M2 -7L9 0L2 7', P.navy, 5)], 385, 2200, 'A normative recommendation, kept apart from the evidence');
  // Chapter Three: the book itself examined for its own pathologies.
  chapter('ch-3', 965, 3, 3);
  put('volume', 965, 265, [
   night(n('path', {d: 'M-130 -78Q-65 -92 0 -70Q65 -92 130 -78V78Q65 64 0 84Q-65 64 -130 78Z', fill: P.cream, stroke: P.navy, 'stroke-width': 3}), P.cream),
   path('M0 -70V84', P.slate, 4),
   path('M-108 -46H-24M-108 -24H-30', P.navy, 4),
   path('M-108 2H-78M-58 2H-24', P.orange, 6), path('M-78 2Q-68 -10 -58 2', P.orange, 3),
   ...[-46, -34, -22, -10, 2, 14, 26, 38].map(y => path(`M22 ${y}Q60 ${y - 6} 108 ${y}`, P.slate, 3)),
   a.dot(102, -88, 18, P.rust), path('M94 -72L90 -52M110 -72L114 -52', P.rust, 6)
  ], 'An open book whose own weaknesses are examined: padded pages, a seam in its argument, a borrowed seal', {beat: 3, offsetMs: 100});
  put('lens', 1065, 168, [night(n('circle', {cx: 0, cy: 0, r: 30, fill: 'none', stroke: P.navy, 'stroke-width': 7}), NIGHT.slate), night(path('M21 21L46 46', P.navy, 10), NIGHT.slate)], 'A reader\'s critical examination', {beat: 3, offsetMs: 300});
  const pathology = [['padding', 'Padding', 1035, 270, 900], ['coherence', 'False coherence', 897, 262, 1800], ['authority', 'Borrowed authority', 1065, 172, 2700]];
  pathology.forEach(([id, value, x, y, offsetMs], i) => {
   if (i) move('lens', 3, x + 4, y - 2, offsetMs - 500, 600);
   else move('lens', 3, x, y, offsetMs - 500, 600);
   put(id, 965, 404 + i * 40, [words(value, 0, 0, 30, '$ink', 700)], `Pathology examined in Chapter Three: ${value.toLowerCase()}`, {beat: 3, offsetMs});
  });
  return a.finish('Three chapter workbenches. Chapter One: a confident fragment rests on dashed, hidden premises, conditions and alternatives, named context debt. Chapter Two: claims about attention are sorted into findings, interpretations and recommendations. Chapter Three: a magnifier examines an open book for padding, a false seam of coherence and a borrowed seal.');
 }

 // Reader lens: the same reader, now standing, turns agreement into one small
 // change, sees formats cooperate along the thread, and is invited to begin.
 reader('reader', 1015, 540, {scale: .95, faceLeft: true});
 put('change-card', 815, 318, [
  rect(-100, -52, 200, 104, P.cream, 12),
  n('rect', {x: -82, y: -30, width: 36, height: 36, rx: 6, fill: 'none', stroke: P.navy, 'stroke-width': 4}),
  words('One small', 38, -14, 22, P.navy, 700), words('change', 38, 14, 22, P.navy, 700),
  path('M-82 34H78', P.slate, 4)
 ], 'One small, verifiable change, proposed rather than proven', {beat: 1, offsetMs: 400, anchors: {left: [-100, 0], right: [100, 0], top: [0, -52], bottom: [0, 52]}});
 put('tick', 751, 306, [path('M-12 0L-3 10L14 -12', P.orange, 7)], 'The change is checked by the reader in practice, not proven by the book', {beat: 1, offsetMs: 3200});
 const format = (id, x, kids, value, offsetMs, meaning) => put(id, x, 250, [...kids, words(value, 0, 108, 24)], meaning, {beat: 2, offsetMs, anchors: {left: [-70, 0], right: [70, 0], top: [0, -70], bottom: [0, 70]}});
 format('blog', 170, [
  night(rect(-70, -66, 140, 132, P.slate, 10), NIGHT.slate), rect(-60, -40, 120, 96, P.cream, 6),
  ...[-48, -36, -24].map(x => a.dot(x, -53, 4, P.cream)),
  path('M-46 -22H40M-46 -4H28M-46 14H40M-46 32H10', P.navy, 4), path('M18 32H40', P.rust, 6)
 ], 'Blog', 300, 'A blog as research workshop and place for corrections');
 format('explainer', 380, [
  n('path', {d: 'M-62 -44H62V34H-6L-30 56V34H-62Z', fill: P.cream}), rect(-62, -44, 124, 12, P.orange, 6),
  path('M-42 -8H40M-42 12H14', P.navy, 5)
 ], 'Explainer', 1300, 'A short explanation that introduces a question');
 format('edition', 590, [
  night(rect(-50, -66, 100, 132, P.navy, 8), NIGHT.slate), rect(-50, -66, 14, 132, P.rust, 6),
  rect(-26, -40, 64, 26, P.cream, 4), words('Ed. 1', 6, -21, 18, P.navy, 700), path('M-24 40H36', P.orange, 5)
 ], 'Stable edition', 2300, 'A stable, numbered edition, so readers know which claim they examine');
 thread('coop-1', 'blog', 'right', 'explainer', 'left', 2, 1800, 'Blog and short explanation cooperate on the same question', -20);
 thread('coop-2', 'explainer', 'right', 'edition', 'left', 2, 2900, 'The question continues into a stable edition', -20);
 thread('earned', 'edition', 'right', 'change-card', 'left', 3, 300, 'Understanding is earned through the continuous thread, then applied', 30);
 put('understood', 905, 176, [
  n('path', {d: 'M-110 -34H110V30H40L64 54L10 30H-110Z', fill: P.cream, stroke: P.orange, 'stroke-width': 4}),
  words('“I understood.”', 0, 8, 28, P.navy, 700)
 ], 'Words the reader has now earned the right to say', {beat: 3, offsetMs: 500});
 for (const [id, offsetMs] of [['blog', 150], ['explainer', 250], ['edition', 350], ['understood', 150], ['change-card', 250], ['tick', 250]]) hide(id, 4, offsetMs, 600);
 // The real starting point: the prologue, with one question held open.
 put('prologue', 560, 318, [
  n('path', {d: 'M-250 -112Q-125 -136 0 -100Q125 -136 250 -112V126Q125 102 0 136Q-125 102 -250 126Z', fill: P.cream, stroke: P.navy, 'stroke-width': 3}),
  path('M0 -100V136', P.slate, 4),
  words('Prologue', -125, -44, 34, P.navy, 700),
  path('M-200 4H-50M-200 30H-70M-200 56H-60', P.slate, 4),
  words('A full day,', 125, -40, 26, P.navy, 700), words('an unfinished idea', 125, -8, 26, P.navy, 700),
  path('M60 34Q60 14 80 14Q100 14 100 30Q100 42 80 48V60', P.orange, 7), a.dot(80, 76, 5, P.orange),
  n('path', {d: 'M186 120V178L202 166L218 178V120Z', fill: P.orange})
 ], 'The book open at its prologue, “A full day, an unfinished idea”, with one question marked and a bookmark', {beat: 4, offsetMs: 1100});
 storyGesture(a, 'reader', 1, 'explain', 5600);
 storyGesture(a, 'reader', 3, 'reflect');
 storyGesture(a, 'reader', 4, 'invite');
 express('reader', 1, 'determined');
 express('reader', 2, 'curious');
 express('reader', 3, 'relieved');
 express('reader', 4, 'happy');
 return a.finish('The same reader, standing, proposes one small checked change. A blog, a short explanation and a stable edition are joined by the orange thread, which then reaches the reader\'s change; the reader can now say “I understood.” Finally the book opens at its prologue, “A full day, an unfinished idea”, with one question and a bookmark.');
}

scenes.forEach((scene, index) => { scene.visual = compose(index); });
fs.writeFileSync(file, JSON.stringify(scenes, null, 2) + '\n');
console.log('Staged ' + scenes.length + ' scenes: ' + scenes.map(s => s.id + ' (' + s.visual.objects.length + ' objects, ' + s.visual.actions.length + ' actions)').join(', '));
