import fs from 'node:fs';
import {ventureArt} from '../review-revision/venture-art.mjs';
const file=new URL('./scenes.json',import.meta.url);
const scenes=JSON.parse(fs.readFileSync(file,'utf8'));
scenes.forEach((s,i)=>s.visual=ventureArt(i));
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
