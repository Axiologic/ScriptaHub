import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {stageAuthor} from '../../tools/shf/stage-authoring.mjs';
const base='.book-work/ai-completion-20261111',specs=JSON.parse(fs.readFileSync(base+'/film-specs.json'));
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const write=(p,d)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,typeof d==='string'?d:JSON.stringify(d,null,2)+'\n')};
function icon(s,name,id,x,y,colors){
 const {n,path:p,text:t,object:o,tint}=s,[a,b,c]=colors;
 const light=hex=>'#'+hex.slice(1).match(/../g).map(v=>Math.round(parseInt(v,16)*.55+255*.45).toString(16).padStart(2,'0')).join('');
 const line=(d,col=a,w=6)=>tint(p(d,col,w),light(col));
 const circle=(cx,cy,r,fill=a)=>n('circle',{cx,cy,r,fill});
 const rect=(x,y,width,height,fill=c)=>n('rect',{x,y,width,height,rx:8,fill,stroke:a,'stroke-width':5});
 const wave=(yy=0)=>line(`M-90 ${yy}Q-45 ${yy-45} 0 ${yy}T90 ${yy}`);
 let parts=[];
 switch(name){
 case 'book':parts=[n('path',{d:'M-70-100L65-115L85-90V95L-50 110L-70 90Z',fill:c,stroke:a,'stroke-width':6}),line('M-49-86V88'),circle(5,-18,35,b),line('M-25 51H50')];break;
 case 'probe':case 'compass':parts=[circle(0,0,78,c),n('path',{d:'M0-60L24 16L0 5L-24 16Z',fill:a}),n('path',{d:'M0 60L24 16L0 5L-24 16Z',fill:b}),circle(0,0,6,a)];break;
 case 'question':parts=[circle(0,0,65,c),t('?',0,20,76,a)];break;
 case 'speech':parts=[n('path',{d:'M-85-60H85V45H-20L-65 85V45H-85Z',fill:c,stroke:a,'stroke-width':5}),...[-40,0,40].map(x=>circle(x,-5,7,b))];break;
 case 'envelope':parts=[rect(-90,-60,180,120),line('M-90-60L0 10L90-60'),circle(0,10,15,b)];break;
 case 'switch':parts=[rect(-85,-35,170,70),circle(-44,0,25,b),line('M10 0H52')];break;
 case 'warning':parts=[n('path',{d:'M0-85L90 70H-90Z',fill:c,stroke:b,'stroke-width':6}),t('!',0,45,68,a)];break;
 case 'lens':case 'eye':parts=[circle(-15,-15,58,c),line('M28 29L90 91',a,12),circle(-15,-15,16,b)];break;
 case 'gate':parts=[rect(-70,-85,140,170),...[-35,0,35].map(x=>line(`M${x}-70V70`)),line('M-70-25H70',b)];break;
 case 'robot':parts=[rect(-65,-60,130,115),circle(-25,-15,10,a),circle(25,-15,10,a),line('M-25 22H25'),line('M0-60V-90'),circle(0,-99,8,b),line('M-65-5H-95M65-5H95')];break;
 case 'grain':parts=[line('M0 90V-90'),...[-65,-25,15,55].flatMap(y=>[n('ellipse',{cx:-22,cy:y,rx:23,ry:11,fill:b}),n('ellipse',{cx:22,cy:y-15,rx:23,ry:11,fill:a})])];break;
 case 'scale':parts=[line('M0-85V90M-70 90H70M-90-45H90'),line('M-65-45L-95 35H-35ZM65-45L35 35H95Z',b,5),circle(0,-45,10,a)];break;
 case 'route':case 'path':case 'paths':parts=[line(name==='paths'?'M-90 45H-25Q15 45 15 0T90-65M-25 45Q10 45 35 85H90':'M-90 60H-30V-45H90'),circle(-90,name==='paths'?45:60,12,b),circle(90,-45,12,b)];break;
 case 'basket':parts=[n('path',{d:'M-85-20H85L60 80H-60Z',fill:c,stroke:a,'stroke-width':5}),line('M-45-20Q0-110 45-20',b),...[-35,0,35].map(x=>line(`M${x}0V60`,a,3))];break;
 case 'battery':parts=[rect(-65,-90,130,180),rect(-25,-108,50,18,a),n('path',{d:'M10-65L-30 10H0L-10 65L35-15H5Z',fill:b})];break;
 case 'factory':parts=[n('path',{d:'M-90 80V-25L-30-65V-25L25-65V-25H90V80Z',fill:c,stroke:a,'stroke-width':5}),...[-50,10,65].map(x=>rect(x-13,10,26,40,b))];break;
 case 'cycle':case 'loop':parts=[line('M-65-40A75 75 0 1 1-70 35'),n('path',{d:'M-88-57L-43-57L-58-15Z',fill:b}),line('M-26 0L-3 25L40-25',b)];break;
 case 'school':parts=[n('path',{d:'M-90-30L0-95L90-30V85H-90Z',fill:c,stroke:a,'stroke-width':5}),rect(-18,25,36,60,b),...[-60,40].map(x=>rect(x,-15,20,30,a)),circle(0,-47,18,b)];break;
 case 'chart':parts=[line('M-90-80V80H90'),line('M-65 50L-25 15L10 30L60-55',b,8),circle(60,-55,9,a)];break;
 case 'tree':case 'network':parts=[line('M0-70V0M-65 70L0 0L65 70M-65-15H65'),...[[0,-70],[0,0],[-65,70],[65,70],[-65,-15],[65,-15]].map(([x,y])=>circle(x,y,18,b))];break;
 case 'river':case 'wave':case 'water':parts=[wave(-50),wave(0),wave(50)];break;
 case 'spiral':parts=[line('M-8 0C-5-20 30-20 30 5C30 50-40 50-40 5C-40-65 70-65 70 5C70 100-90 100-90 5',a,7)];break;
 case 'handshake':parts=[line('M-95-20L-25-50L10-30L65-48L95-10'),n('path',{d:'M-50-35L-15-5L5-20L60 30L35 60L-10 45L-62 0Z',fill:c,stroke:a,'stroke-width':5}),line('M-10 15L20 40',b)];break;
 case 'prototype':case 'scroll':case 'bookmark':parts=[n('path',{d:'M-65-90H40L70-60V90H-65Z',fill:c,stroke:a,'stroke-width':5}),line('M40-90V-60H70'),...[-25,5,35].map(y=>line(`M-38 ${y}H40`,b,5))];break;
 case 'masks':parts=[n('path',{d:'M-80-70H35V5Q-20 90-80 5Z',fill:c,stroke:a,'stroke-width':5}),n('path',{d:'M-20-35H85V40Q30 115-20 40Z',fill:b,stroke:a,'stroke-width':5}),line('M-65-35H-42M-5-35H16M-7 3H12M52 3H71')];break;
 case 'table':parts=[n('ellipse',{cx:0,cy:0,rx:100,ry:55,fill:c,stroke:a,'stroke-width':5}),...[-65,0,65].map(x=>circle(x,-80,17,b)),...[-65,0,65].map(x=>circle(x,80,17,a))];break;
 case 'symbols':parts=[t('P',-50,13,55,a),t('⇒',0,13,44,b),t('Q',55,13,55,a)];break;
 case 'cloud':parts=[n('path',{d:'M-70 10C-110-10-75-65-40-45C-25-100 45-85 50-40C105-50 115 15 70 20H-70Z',fill:c,stroke:a,'stroke-width':5}),...[-45,0,45].map(x=>line(`M${x}40L${x-15}80`,b))];break;
 case 'road':parts=[n('path',{d:'M-40-95H40L95 95H-95Z',fill:c,stroke:a,'stroke-width':5}),line('M0-70V-35M0 0V35M0 65V90',b,5),wave(100)];break;
 case 'clock':parts=[circle(0,0,85,c),line('M0-60V0L45 25'),circle(0,0,7,b)];break;
 case 'dots':parts=Array.from({length:9},(_,i)=>circle(i%3*55-55,Math.floor(i/3)*55-55,17,i%2?a:b));break;
 case 'bridge':parts=[line('M-100 40H100M-90 40V90M90 40V90'),line('M-90 40Q0-100 90 40',b),...[-60,-30,0,30,60].map(x=>line(`M${x}40V${-45+Math.abs(x)*.4}`,a,3))];break;
 case 'pen':parts=[n('path',{d:'M-90-16H65L100 0L65 16H-90Z',fill:b,stroke:a,'stroke-width':4}),line('M-65-16V16')];break;
 case 'planet':case 'globe':parts=[circle(0,0,85,c),n('ellipse',{cx:0,cy:0,rx:40,ry:85,fill:'none',stroke:a,'stroke-width':5}),line('M-85 0H85M-72-40H72M-72 40H72',b,4)];break;
 case 'sun':parts=[circle(0,0,45,b),...Array.from({length:8},(_,i)=>{const v=i*Math.PI/4;return line(`M${Math.cos(v)*65} ${Math.sin(v)*65}L${Math.cos(v)*95} ${Math.sin(v)*95}`,b,6)})];break;
 case 'crowd':parts=[...[-50,0,50].map((x,i)=>n('path',{d:`M${x-30} ${-50+i%2*45}h60v50h-15l-20 20v-20h-25Z`,fill:i%2?b:c,stroke:a,'stroke-width':4}))];break;
 case 'heart':parts=[n('path',{d:'M0 80L-70 5C-130-65-25-110 0-45C25-110 130-65 70 5Z',fill:b,stroke:a,'stroke-width':5})];break;
 case 'pause':parts=[rect(-65,-75,45,150,b),rect(20,-75,45,150,a)];break;
 case 'ear':parts=[line('M-50-5C-70-110 90-110 70-5C65 35 20 10 15 65C10 105-40 100-45 65'),line('M-20 0C-30-55 50-60 30-5',b,7)];break;
 case 'map':parts=[n('path',{d:'M-100-70L-30-90L35-65L100-85V80L35 100L-30 75L-100 95Z',fill:c,stroke:a,'stroke-width':5}),line('M-30-90V75M35-65V100',a,3),circle(-55,30,12,b),circle(65,-20,12,b),line('M-55 30H5V-20H65',b,5)];break;
 case 'museum':parts=[n('path',{d:'M-90-45L0-95L90-45Z',fill:b,stroke:a,'stroke-width':4}),line('M-95 85H95M-95 65H95'),...[-65,0,65].map(x=>line(`M${x}-35V65`,a,13))];break;
 case 'vote':parts=[rect(-85,-10,170,100),line('M-45 5H45',a,8),n('path',{d:'M-35-100H35V0H-35Z',fill:c,stroke:b,'stroke-width':5}),line('M-20-65L-2-45L23-80',a,5)];break;
 default:throw Error('Missing authored icon '+name);
 }
 const value=o(id,x,y,parts,name,1);value.visual.anchors={left:[-105,0],right:[105,0],top:[0,-110],bottom:[0,110]};s.add(value);return id;
}
function artwork(spec,scene,k,bookIndex){
 const s=stageAuthor(),[a,b,c]=spec.palette;
 const positions=k===0?[[250,315],[650,245],[990,425]]:k===1?(bookIndex%2?[[240,260],[610,410],[970,260]]:[[240,385],[605,225],[970,385]]):k===2?[[240,250],[610,405],[970,250]]:[[240,325],[650,240],[990,425]];
 scene.icons.forEach((type,i)=>{const [x,y]=positions[i];icon(s,type,'item-'+i,x,y,spec.palette);const label=scene.labels[i];s.label('label-'+i,label,x,y+135,label.length>18?22:27);s.reveal('item-'+i,Math.min(i+1,3),1100);s.reveal('label-'+i,Math.min(i+1,3),900)});
 // Motions carry semantic roles, with no invented numeric measurements.
 if(spec.slug==='world-as-a-system'&&k===1){s.move('item-1',2,650,225,1500);s.label('east','East + East',620,530,31);s.reveal('east',2);}
 if(spec.slug==='sleeper-agents-the-risks-of-deceptive-ais'&&k===1)s.move('item-1',2,630,390,1500);
 if(spec.slug==='meaning-as-a-path'&&k===1){s.link('interpretation','item-0','item-1',2,'The instruction is interpreted into roles, without authorizing execution.',a);}
 if(spec.slug==='top-ten-ways-to-improve-emotional-intelligence'&&k===1)s.move('item-1',2,610,360,1700);
 if(spec.slug==='planetary-sky-understanding-the-colors-above-us'&&k===1)s.move('item-0',2,240,190,1800);
 return s.finish(spec.identity+'; '+scene.lines.join(' '));
}
for(const [bi,spec]of specs.entries()){
 const root=path.join('presentations',spec.slug),source=fs.readFileSync(root+'/source/source.txt','utf8'),units=JSON.parse(fs.readFileSync(root+'/source/units.json'));
 const sourceUnits=units.filter(u=>['p','li','td','th'].includes(u.kind)&&u.text.split(/\s+/).length>12);
 if(!sourceUnits.length)throw Error('No substantive source evidence '+spec.slug);
 const scenes=spec.scenes.map((s,i)=>({...s,chapter:s.title,sources:[i+1],beatLenses:s.lines.map(()=>s.lens),pauseAfterMs:s.lines.map((_,j)=>j===s.lines.length-1?1900:1200),emotionalPlan:{arc:i===0?'curiosity → orientation':i===3?'clarity → invitation':'concrete encounter → distinction → useful intuition',purpose:s.lines.at(-1),states:s.lines.map((_,j)=>['curious','thoughtful','encouraging'][j]),intensities:[.4,.35,.35],voiceDirections:s.lines.map((_,j)=>`Calm conversational English, ${j===0?'curious and concrete':j===1?'careful and reflective':'warm and precise'}; retain qualifications and leave space for the idea.`)},visual:artwork(spec,s,i,bi)}));
 const scriptSha256=hash(JSON.stringify(scenes.map(s=>({id:s.id,lines:s.lines}))));
 const production={id:spec.slug+'-introduction',filmId:spec.slug+'-introduction',title:spec.title+' · Why read this book?',bookDirectory:'docs/'+spec.directory,sourceReaderPath:'en/short_content.html',edition:JSON.parse(fs.readFileSync('docs/'+spec.directory+'/editions.json')).currentEdition,voicePace:.95,voiceTempo:1,minDurationMs:50000,maxDurationMs:120000,voiceEngine:'qwen',voiceId:bi%2?'Aiden':'Ryan',voiceRuntimeConfig:'.agents/skills/theatrical-audio/runtime/qwen.json',voiceProvider:`local Qwen3-TTS 1.7B CustomVoice / ${bi%2?'Aiden':'Ryan'}`,voiceRights:'Source adaptation and local neural narration authorized by the project editor.'};
 const chapters=JSON.parse(fs.readFileSync(root+'/source/chapter-map.json'));
 const invitation={reasonToExist:scenes[0].lines[1],readerPromise:spec.identity,readerOutcomes:scenes.map(s=>s.lines.at(-1)),bookJourney:chapters,audienceFit:'Readers interested in the questions, distinctions and examples identified in the current source book.',contentSamples:scenes.slice(1,3).map(s=>({sceneId:s.id,readingValue:s.lines.at(-1)})),reservedForReading:[...scenes.at(-1).lines.slice(1)],closingInvitation:scenes.at(-1).lines[1]};
 // Each scene cites the complete short-reader argument. This deliberately broad
 // ledger preserves context; it is not an automated sentence-entailment claim.
 const spans=sourceUnits.map(u=>{const start=source.indexOf(u.text);return{start,end:start+u.text.length,quote:u.text}});
 const editorial={format:'SHF-Editorial',version:'1',purpose:'book-introduction',genre:spec.slug.startsWith('digital-delusions')?'satirical fiction':'nonfiction',targetMinutes:1.6,sourceSha256:hash(source),centralQuestion:spec.identity,thesis:scenes[0].lines[1],readerInvitation:invitation,claims:scenes.map((s,i)=>({id:'claim-'+(i+1),statement:s.lines.join(' '),kind:'source-claim',noveltyScope:'within-source',qualifiers:['Preserve proposals, fiction, analogy and evidence as different kinds of statement.','Spans retain the whole short-reader argument as context; editorial review, not lexical matching, checks the spoken claims.'],spans})),scenePlan:scenes.map((s,i)=>({id:s.id,role:i===0?'why':i===3?'what':'how',lens:s.lens,purpose:s.lines.at(-1)})),hooks:[{question:spec.identity,introducedSceneId:'why',resolvedSceneId:'read',resolution:scenes.at(-1).lines[0],sourceClaimIds:['claim-1','claim-2','claim-3','claim-4'],status:'resolved'}],omissions:['Full chapter arguments and secondary cases remain for reading.'],limitations:['Adaptation uses the complete canonical short reader and full chapter map; claims are attributed to the book, not independently established results.'],rights:production.voiceRights};
 const plan={version:'curiosity-v2',scriptSha256,productionStatus:'planned',scenes:scenes.map(s=>({sceneId:s.id,title:s.title,viewerPurpose:s.lines.at(-1),composition:s.icons.join(' → '),keep:s.visual.objects.map(o=>o.id),remove:[],addOrChange:s.lines,cues:s.lines.map((line,i)=>({line:i+1,visualAction:`Reveal ${s.labels[i]} as ${s.icons[i]}, supporting: ${line}`,emotion:s.emotionalPlan.states[i]}))}))};
 const review={version:'curiosity-v2',title:spec.title,purpose:'book-introduction',scriptSha256,hook:scenes[0].lines[0],readerPromise:spec.identity,distinctiveContribution:scenes[0].lines[1],visualPlan:plan.scenes.map(s=>s.composition),independentReview:{status:'pending',scriptSha256,reviewer:'Active LLM separate complete-source/script review pass; no independent human or second agent claimed.'}};
 for(const [file,data]of [['work/scenes.json',scenes],['work/production.json',production],['work/editorial.json',editorial],['work/presentation-plan.json',plan],['work/marketing-review.json',review],['source/sections.json',scenes.map((s,i)=>({id:'source-'+(i+1),heading:s.title,anchor:''}))],['work/visual-bible.json',{identity:spec.identity,palette:spec.palette,sceneMetaphors:scenes.map(s=>s.icons),humanCharacters:false,sourceVisualSelection:'Canonical full HTML contains no image elements; authored concept illustrations adapt the text rather than import unsuitable image evidence.'}]])write(root+'/'+file,data);
 if(!fs.existsSync(root+'/work/migration-state.json'))write(root+'/work/migration-state.json',{version:1,updatedAt:new Date().toISOString(),stages:{text:{status:'reviewing',scriptSha256},animation:{status:'planned',scriptSha256},voice:{status:'planned',scriptSha256}}});
 write(root+'/build.mjs',"import {buildBookFilm} from '../../tools/shf/build-book-film.mjs';\nawait buildBookFilm(new URL('.',import.meta.url).pathname);\n");write(root+'/render_voice.mjs',"import {renderNarration} from '../../tools/shf/render-narration.mjs';\nawait renderNarration(new URL('.',import.meta.url).pathname);\n");
 console.log(spec.slug,scenes.flatMap(s=>s.lines).join(' ').split(/\s+/).length+' words');
}
