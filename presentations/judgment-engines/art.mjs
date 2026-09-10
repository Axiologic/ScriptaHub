import fs from 'node:fs';
import {judgmentVisual} from './review-revision/art.mjs';
const file=new URL('./work/scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file,'utf8'));
scenes.forEach((s,i)=>s.visual=judgmentVisual(i));
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
