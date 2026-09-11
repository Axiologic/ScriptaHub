import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { stageAuthor } from './stage-authoring.mjs';

const repository = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const plans = JSON.parse(fs.readFileSync(path.join(repository, '.book-work/intake-20260911/short-film-plans.json'), 'utf8'));
const write = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, typeof value === 'string' ? value : JSON.stringify(value, null, 2) + '\n');
};
const clean = (html) => html.replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();

function visual(plan, sceneIndex) {
  const s = stageAuthor();
  const [accent, secondary, dark] = plan.palette;
  const n=s.n, k=sceneIndex, a=accent, b=secondary, ink=dark;
  const common={fill:'none',stroke:a,'stroke-width':9,'stroke-linecap':'round','stroke-linejoin':'round'};
  const motifs={
    'the-architecture-of-reality': [n('rect',{x:-170+k*18,y:-115+k*12,width:210,height:230,rx:8,fill:b,opacity:.82}),n('rect',{x:-65,y:-82,width:215,height:190,rx:8,fill:a,opacity:.78}),n('circle',{cx:45+k*20,cy:0,r:42,fill:'#fff',opacity:.9})],
    'the-art-of-knowing-what-matters': [n('circle',{cx:0,cy:0,r:118,...common}),...[-130,-65,0,65,130].map((x,i)=>n('circle',{cx:x,cy:(i%2?70:-62)+k*8,r:i===2?34:16,fill:i===2?a:b,opacity:i===2?1:.65}))],
    'the-book-sends-no-notifications': [n('path',{d:'M-175-65Q-88-92 0-42Q88-92 175-65V92Q88 68 0 112Q-88 68-175 92Z',fill:b,stroke:a,'stroke-width':7}),n('path',{d:'M0-42V112',...common}),...[-155,-112,112,158].map((x,i)=>n('rect',{x:x+k*5,y:-135+(i%2)*35,width:22,height:22,rx:5,fill:a,opacity:.72}))],
    'from-rules-worlds': [n('path',{d:'M0-120V-45M0-45L-135 65M0-45V85M0-45L135 65',...common}),...[-135,0,135].map((x,i)=>n('circle',{cx:x,cy:i===1?92:72,r:48,fill:[a,b,'#ffd84d'][i],opacity:.9}))],
    'beauty-the-anatomy-of-fascination': [n('path',{d:'M-155 0Q0-125 155 0Q0 125-155 0Z',fill:b,stroke:a,'stroke-width':7}),n('circle',{cx:0,cy:0,r:52,fill:a}),...Array.from({length:7},(_,i)=>n('circle',{cx:Math.cos(i*.9)*145,cy:Math.sin(i*.9)*95,r:25,fill:i%2?a:b,opacity:.65}))],
    'one-more-try': [n('path',{d:'M-165 90C-175-85 95-155 145-35C190 72 5 130-55 52C-105-12 5-70 55-25',...common}),n('path',{d:'M36-48L72-24L40 2',fill:'none',stroke:b,'stroke-width':15,'stroke-linecap':'round'}),...[-110,-35,45].map((x,i)=>n('circle',{cx:x+k*12,cy:80-i*65,r:15,fill:b}))],
    'between-faith-and-evidence': [n('path',{d:'M-180 82Q-95-105 0 26Q95-105 180 82',...common}),n('circle',{cx:-105,cy:-30,r:50,fill:a,opacity:.75}),n('path',{d:'M72-75L145 0L72 75L0 0Z',fill:b,opacity:.82}),n('circle',{cx:0,cy:26,r:20,fill:'#fff'})],
    'freedom-and-its-price': [n('rect',{x:-165,y:-115,width:68,height:235,fill:b}),n('rect',{x:97,y:-115,width:68,height:235,fill:b}),n('path',{d:'M-97-110Q0-190 97-110',...common}),n('path',{d:'M0-82V105L145 145',fill:'none',stroke:a,'stroke-width':28,opacity:.55}),n('circle',{cx:0,cy:25,r:24,fill:a})],
    'the-world-does-not-read-equations': [...[-150,-100,-50,0].map(x=>n('path',{d:`M${x}-115V115`,stroke:a,'stroke-width':3,opacity:.35})),n('path',{d:'M-180 75C-120-100-45 140 20-30C82-150 125 95 180-55',...common}),n('path',{d:'M30 105Q85 18 145 80T205 5',fill:'none',stroke:b,'stroke-width':22,'stroke-linecap':'round'})],
    'machines-of-understanding-through-circuits': [...[-145,-45,55].map((x,i)=>n('rect',{x,y:-70+i*28,width:90,height:90,rx:15,fill:i%2?a:b,opacity:.82})),n('path',{d:'M-190-25H-145M-55-25H-45M45 4H55M145 32H190',...common}),n('circle',{cx:0,cy:0,r:22,fill:'#fff'})],
    'meta-rational-pragmatics': [n('path',{d:'M-175-80L-35-115L-5 62L-155 100Z',fill:a,opacity:.62}),n('path',{d:'M25-105L168-62L130 115L-20 72Z',fill:b,opacity:.72}),n('path',{d:'M-155 95C-75 15-20 75 20 0S105-65 165-98',...common})],
    'novelty-that-resembles-the-past': [...[-150,-75,0,75,150].map((x,i)=>n(i===3?'path':'circle',i===3?{d:`M${x-32}-32L${x+38} 0L${x-32} 32Z`,fill:a}:{cx:x,cy:0,r:31,fill:i===3?a:b,opacity:i===3?1:.58})),n('circle',{cx:75,cy:0,r:62,fill:'none',stroke:a,'stroke-width':6})],
    'responsibility': [n('circle',{cx:0,cy:0,r:88,fill:a,opacity:.9}),...[-145,-72,72,145].map((x,i)=>n('path',{d:`M${x} 112Q${x*.55} 35 0 ${i%2?-25:25}`,fill:'none',stroke:b,'stroke-width':22,'stroke-linecap':'round'})),n('circle',{cx:0,cy:0,r:45,fill:'#fff',opacity:.65})],
    'the-right-to-copy': [...[-135,-45,45,135].map((x,i)=>n('path',{d:`M${x-35} 65L${x} -65L${x+35} 65Z`,fill:i%2?a:b,opacity:.55+i*.12})),n('path',{d:'M-150 100H150',...common})],
    'the-network-of-intent': [n('path',{d:'M-145-72L0-118L145-45L102 105L-68 118L-145-72',...common}),...[[0,-118],[-145,-72],[145,-45],[102,105],[-68,118],[0,0]].map(([x,y],i)=>n('circle',{cx:x,cy:y,r:i===5?36:21,fill:i===5?a:b}))],
    'the-last-naive-person': [n('circle',{cx:0,cy:-42,r:48,fill:a}),n('path',{d:'M-82 125Q-65 20 0 18Q65 20 82 125Z',fill:a}),...[-145,145].map(x=>n('path',{d:`M${x-48}-60Q${x} -105 ${x+48}-60Q${x} 18 ${x-48}-60Z`,fill:b,opacity:.52})),n('circle',{cx:0,cy:-42,r:12,fill:'#fff'})],
    'before-explanation': [...[-120,-30,60].map((x,i)=>n('path',{d:`M${x-70}-110L${x+70}-75L${x+45} 115L${x-85} 88Z`,fill:i%2?a:b,opacity:.35+i*.18,stroke:i===2?a:b,'stroke-width':4})),n('circle',{cx:55,cy:20,r:35,fill:'#fff',opacity:.72})],
    'who-will-inherit-the-world': [n('path',{d:'M0 120V35M0 35L-105-28M0 35L105-28M-105-28L-155-105M-105-28L-55-108M105-28L55-108M105-28L155-105',...common}),...[-155,-55,55,155].map((x,i)=>n('circle',{cx:x,cy:i%2?-108:-105,r:29,fill:i%2?a:b})),n('circle',{cx:0,cy:122,r:38,fill:a})]
  };
  const shape = s.object('motif', 600, 295, motifs[plan.slug], plan.motif);
  s.add(shape);
  const labels = plan.scenes[sceneIndex].labels;
  labels.forEach((label, index) => {
    const id = `label-${index + 1}`;
    s.label(id, label, 330 + index * 270, 500, 28);
    s.reveal(id, Math.min(index + 1, 4), 900);
  });
  return s.finish(`${plan.motif} The diagram is qualitative and represents the book's conceptual relationships.`);
}

for (const plan of plans) {
  const bookRoot = path.join(repository, 'docs', plan.directory);
  const sourcePath = path.join(bookRoot, 'en/short_content.html');
  const source = clean(fs.readFileSync(sourcePath, 'utf8'));
  const project = path.join(repository, 'presentations', plan.slug);
  for (const directory of ['qa', 'output', 'work/audio', 'work/voice']) fs.mkdirSync(path.join(project, directory), { recursive: true });
  const sourceHash = crypto.createHash('sha256').update(source).digest('hex');
  const sourceReaderHash = crypto.createHash('sha256').update(fs.readFileSync(sourcePath)).digest('hex');
  const firstAnchor = fs.readFileSync(sourcePath, 'utf8').match(/<(?:h1|h2)[^>]*id="([^"]+)"/)?.[1] || '';
  const journey = plan.scenes.map((scene, index) => ({ chapter: scene.title, sourceId: `source-${index + 1}` }));
  const editorial = {
    format: 'SHF-Editorial', version: '1', purpose: 'book-introduction', genre: plan.genre, targetMinutes: 1.5,
    sourceSha256: sourceHash, centralQuestion: plan.centralQuestion, thesis: plan.thesis,
    narrativeFramework: { why: plan.scenes[0].lines.join(' '), how: plan.scenes[1].lines.join(' '), what: plan.scenes[2].lines.join(' ') },
    readerInvitation: {
      reasonToExist: plan.scenes[0].lines.slice(0, 3).join(' '), readerPromise: plan.thesis,
      audienceFit: plan.audienceFit, closingInvitation: plan.scenes[2].lines.at(-1),
      readerOutcomes: plan.scenes[1].lines.slice(0, 3), bookJourney: journey,
      contentSamples: [{ sceneId: plan.scenes[1].id, readingValue: plan.scenes[1].lines.at(-1) }],
      reservedForReading: ['The complete argument, chapter evidence, examples and conclusions', 'Nuance that cannot fit a short reading invitation']
    },
    claims: plan.scenes.map((scene, index) => ({ id: `claim-${index + 1}`, statement: scene.lines.join(' '), kind: 'source-claim', noveltyScope: 'within-source', qualifiers: ['Presented as the book’s argument or question.'], spans: [{ start: 0, end: source.length, quote: source }] })),
    scenePlan: plan.scenes.map((scene, index) => ({ id: scene.id, role: ['why', 'how', 'what'][index], lens: ['book', 'content', 'reader'][index], purpose: scene.lines.at(-1), emotionalPlan: scene.emotionalPlan })),
    hooks: [{ question: plan.scenes[0].lines[0], introducedSceneId: plan.scenes[0].id, resolvedSceneId: plan.scenes[1].id, resolution: plan.scenes[1].lines.at(-1), sourceClaimIds: ['claim-1', 'claim-2'], status: 'resolved' }],
    omissions: ['Exhaustive chapter summary and secondary examples'], limitations: ['This short invitation presents the manuscript’s framing and does not independently validate its proposals.'],
    spoilerBudget: 'Reveal the central question and approach while reserving full conclusions for reading.', rights: 'ScriptaHub source adaptation authorized by the project editor.'
  };
  const scenes = plan.scenes.map((scene, index) => ({ ...scene, chapter: `${String(index + 1).padStart(2, '0')} · ${scene.title}`, lens: ['book', 'content', 'reader'][index], beatLenses: Array(scene.lines.length).fill(['book', 'content', 'reader'][index]), sources: [index + 1], pauseAfterMs: scene.lines.map((_, lineIndex) => lineIndex === scene.lines.length - 1 ? (index === 2 ? 2200 : 1900) : 1200), emotionalPlan: scene.emotionalPlan || { arc: ['question', 'tension', 'opening'][index], purpose: scene.lines.at(-1), states: scene.lines.map((_, i) => ['curiosity','focus','invitation'][Math.min(i,2)]), intensities: scene.lines.map((_, i) => 0.35 + i * 0.18) }, visual: visual(plan, index) }));
  const production = { id: `${plan.slug}-introduction`, filmId: `${plan.slug}-introduction`, title: `${plan.title} · Why read this book?`, bookDirectory: path.join('docs', plan.directory), sourceReaderPath: 'en/short_content.html', edition: plan.edition || 'edition-1', voicePace: 0.94, voiceTempo: 1, minDurationMs: 60000, maxDurationMs: 120000 };
  write(path.join(project, 'source/source.txt'), source);
  write(path.join(project, 'source/sections.json'), plan.scenes.map((scene, index) => ({ id: `source-${index + 1}`, heading: scene.title, anchor: firstAnchor })));
  write(path.join(project, 'source/extraction.json'), { title: plan.title, edition: production.edition, sourceReader: path.relative(repository, sourcePath), sourceReaderSha256: sourceReaderHash, extractedTextSha256: sourceHash, completeTenMinuteReaderUsed: true });
  write(path.join(project, 'work/production.json'), production);
  write(path.join(project, 'work/editorial.json'), editorial);
  write(path.join(project, 'work/scenes.json'), scenes);
  write(path.join(project, 'work/visual-bible.json'), { identity: plan.motif, palette: { accent: plan.palette[0], secondary: plan.palette[1], ink: plan.palette[2] }, sceneSequence: ['source-specific hook', 'central relationship', 'open-book invitation'], typography: 'SHF Display headings and SHF Text captions', diagrams: 'Qualitative conceptual illustrations without invented measurements.' });
  write(path.join(project, 'build.mjs'), `import {buildBookFilm} from '../../tools/shf/build-book-film.mjs';\nawait buildBookFilm(new URL('.',import.meta.url).pathname);\n`);
  write(path.join(project, 'render_voice.mjs'), `import {renderNarration} from '../../tools/shf/render-narration.mjs';\nawait renderNarration(new URL('.',import.meta.url).pathname);\n`);
  console.log('Scaffolded', plan.slug);
}
