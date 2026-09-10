#!/usr/bin/env node
// Refresh shared player code without rebuilding film content or narration.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {runtime} from '../../.agents/skills/shf-presentation-creator/scripts/lib/standalone.mjs';
const code=runtime();
fs.writeFileSync('docs/assets/shf/shf-player.js',code);
fs.writeFileSync('.agents/skills/shf-presentation-creator/assets/player/shf-player.js',code);
let exportsUpdated=0;
for(const dir of fs.readdirSync('presentations',{withFileTypes:true}).filter(x=>x.isDirectory())){
 const folder=path.join('presentations',dir.name,'exports');if(!fs.existsSync(folder))continue;
 for(const name of fs.readdirSync(folder).filter(x=>x.endsWith('.html'))){
  const file=path.join(folder,name),before=fs.readFileSync(file,'utf8');
  const start=before.indexOf('<script>'),end=before.indexOf('</script><script>\nconst films=');
  if(start<0||end<0)continue;
  const after=before.slice(0,start+8)+code.replace(/<\/script/gi,'<\\/script')+before.slice(end);
  fs.writeFileSync(file,after);exportsUpdated++;
 }
}
console.log(JSON.stringify({exportsUpdated,runtimeSha256:crypto.createHash('sha256').update(code).digest('hex'),filmContentAndAudioUnchanged:true}));
