// Fresh, owned test tab; playback intent is stubbed, audio is decoded offline only.
import assert from 'node:assert/strict';import fs from 'node:fs/promises';import {connect} from './browser-session.mjs';
const site=process.env.SCRIPTA_TEST_URL||'http://127.0.0.1:8012/';
const out='presentations/library-introduction/qa';await fs.mkdir(out+'/screenshots',{recursive:true});
const script=JSON.parse(await fs.readFile('presentations/library-introduction/work/scenes.json','utf8'));const expectedClips=script.reduce((n,s)=>n+s.lines.length,0);
const c=await connect(site+'index.html?lang=en');const checks=[];
const check=async(name,code)=>{assert(await c.evaluate(code),name);checks.push(name);};
try{
 await c.size(1200,1000);await c.wait('!!document.querySelector("[data-mascot-start]")');
 await check('two choices, no old introduction or librarian popup','document.querySelectorAll(".mascot-choice").length===2&&!document.querySelector(".site-hero,.intro-presentation,[data-librarian-dialog],[data-header-librarian]")');
 await check('requested choice order','document.querySelector(".mascot-choice").matches("[data-mascot-ask]")&&document.querySelector("[data-mascot-start] [data-mascot-label]").textContent==="Why ScriptaHub.com?"');
 await check('question initially concealed','document.querySelector("#mascot-question").hidden');
 await c.wait('document.querySelector("[data-home-loading]")?.classList.contains("is-complete")||!document.querySelector("[data-home-loading]")');
 for(const [width,height] of [[1280,720],[1366,768],[1440,900]]){await c.size(width,height);await check('initial desktop fits viewport '+width+'x'+height,'document.documentElement.scrollHeight<=innerHeight&&document.documentElement.scrollWidth<=innerWidth');}
 await c.size(1366,768);
 await check('featured copy aligns with cover top and bottom','(()=>{const cover=document.querySelector(".mission-featured-cover").getBoundingClientRect(),top=document.querySelector(".featured-book-copy>.eyebrow").getBoundingClientRect(),bottom=document.querySelector(".featured-book-actions a").getBoundingClientRect();return Math.abs(top.top-cover.top)<2&&Math.abs(bottom.bottom-cover.bottom)<2})()');
 await c.capture(out+'/screenshots/home-desktop.png');
 await c.evaluate('document.querySelector("[data-mascot-ask]").click();document.querySelector("#mascot-query").value="AI workflows and research"');
 await check('input replaces choices and has close control','[...document.querySelectorAll(".mascot-choice")].every(e=>getComputedStyle(e).display==="none")&&document.querySelector("[data-mascot-cancel]")!==null');
 await check('question appears inline and receives focus','!document.querySelector("#mascot-question").hidden&&document.activeElement.id==="mascot-query"&&!document.querySelector("dialog[open]")');
 for(const width of [1200,720,393,320]){await c.size(width,1000);await check('controls fit '+width,'document.documentElement.scrollWidth<=innerWidth&&[...document.querySelectorAll(".mascot-choice,#mascot-question")].every(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth})');if(width===393)await c.capture(out+'/screenshots/home-mobile-question.png');}
 await c.evaluate('const picker=document.querySelector("[data-language-select]");picker.value="ro";picker.dispatchEvent(new Event("change",{bubbles:true}))');
 await check('language change preserves question and URL','document.querySelector("#mascot-query").value==="AI workflows and research"&&new URL(location.href).searchParams.get("lang")==="ro"&&document.querySelector("[data-mascot-ask] [data-mascot-label]").textContent.includes("bibliotecarul")');
 await c.evaluate('document.querySelector("#mascot-question").requestSubmit()');await c.wait('!!document.querySelector("[data-librarian-content]")');
 await check('question reaches existing recommendation flow','location.pathname.endsWith("/librarian/index.html")&&new URLSearchParams(location.hash.slice(1)).get("request")==="AI workflows and research"');
 await c.send('Page.navigate',{url:site+'index.html?lang=en#ask-librarian'});await c.wait('!!document.querySelector("[data-mascot-start]")');
 await check('deep link opens inline input','!document.querySelector("#mascot-question").hidden');
 await c.evaluate('document.querySelector("[data-mascot-cancel]").click()');
 await check('closing input restores choices','document.querySelector("#mascot-question").hidden&&document.activeElement.matches("[data-mascot-ask]")');
 await c.evaluate('window.p=document.querySelector("shf-player");window.starts=0;window.pauses=0;p.audio.unlock=async()=>{};p.play=async()=>{starts++};const pause=p.pause.bind(p);p.pause=()=>{pauses++;return pause()}');
 await c.evaluate('document.querySelector("[data-mascot-start]").click();document.querySelector("dialog").close()');
 await c.wait('!!p.film');await check('closing during load cancels automatic start','starts===0&&!document.querySelector("dialog").open&&!document.body.classList.contains("mascot-film-open")');
 await c.size(1200,1000);await c.evaluate('document.querySelector("[data-mascot-start]").click()');await c.wait('starts===1');
 await check('presentation opens full viewport with close control','document.querySelector("dialog").open&&document.querySelector("dialog").getBoundingClientRect().width>=innerWidth-1&&document.querySelector(".mascot-film-close").getBoundingClientRect().top>=0');
 await c.send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await c.send('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
 await check('Escape stops and restores focus','!document.querySelector("dialog").open&&pauses>0&&document.activeElement.matches("[data-mascot-start]")');
 const clips=await c.evaluate('(async()=>{p.setMuted(true);p.audio.ctx=new OfflineAudioContext(1,1,24000);try{let total=0;for(const s of p.film.scenes)total+=(await p.audio.prepare(s)).clips.length;return total;}finally{p.audio.clear();p.audio.ctx=null}})()');assert.equal(clips,expectedClips);
 await check('short sentences and real pauses','p.film.scenes.every(s=>s.beats.every(b=>SHF.core.splitSentences(b.text,"en").length===1&&b.text.split(/\s+/).length<=16&&b.endMs-b.spokenEndMs>=1000))');
 await c.evaluate('document.querySelector("[data-mascot-start]").click()');await c.wait('document.querySelector("dialog").open');
 const durations=await c.evaluate('p.film.scenes.map(s=>s.durationMs)');let sampled=0;
 for(const theme of ['color','paper','night']){let offset=0;for(let i=0;i<durations.length;i++){for(const ratio of [.08,.5,.96]){await c.evaluate(`p.setTheme('${theme}');p.seek(${offset+durations[i]*ratio})`);await check(`valid frame ${theme}/${i}/${ratio}`,'!p.captureSVG().includes("NaN")&&!p.captureSVG().includes("Infinity")');sampled++;}await c.capture(`${out}/screenshots/film-${theme}-${i}.png`);offset+=durations[i];}}
 for(const width of [1200,720,393,320]){await c.size(width,1000);await check('caption and close geometry '+width,'(()=>{let offset=0;for(const s of p.film.scenes){for(const b of s.beats){p.seek(offset+(b.startMs+b.spokenEndMs)/2);if(p.$("caption").textContent!==b.text)return false;const c=p.$("captionbox").getBoundingClientRect(),a=p.$("art").getBoundingClientRect();if(innerWidth<=720&&c.top<a.bottom-1)return false;}offset+=s.durationMs;}return document.querySelector(".mascot-film-close").getBoundingClientRect().right<=innerWidth})()');}
 await check('captions remain during thinking pauses','(()=>{let offset=0;for(const s of p.film.scenes){for(const b of s.beats){p.seek(offset+b.spokenEndMs+500);if(p.$("caption").textContent!==b.text)return false;}offset+=s.durationMs;}return true})()');
 await check('scene heading uses the bundled display face', `Number(getComputedStyle(p.$('sceneTitle')).fontWeight)>=700&&getComputedStyle(p.$('sceneTitle')).fontFamily.includes('SHF Display')&&document.fonts.check('700 24px "SHF Display"')`);
 await c.evaluate('document.querySelector("dialog").close()');assert.equal(c.errors.length,0);
 await fs.writeFile(out+'/browser-review.json',JSON.stringify({checks:checks.length,passed:true,decodedClips:clips,sampledFrames:sampled,playback:'Playback method stubbed for dialog lifecycle; clips decoded offline without any audio output.',jsErrors:c.errors},null,2)+'\n');console.log({checks:checks.length,clips,sampled});
}finally{await c.close()}
