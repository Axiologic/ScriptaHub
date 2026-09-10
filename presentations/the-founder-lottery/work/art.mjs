import fs from 'node:fs';
import {furnitureArt} from '../review-revision/furniture-art.mjs';
const p=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(p,'utf8'));
scenes.forEach((s,i)=>s.visual=furnitureArt(i));fs.writeFileSync(p,JSON.stringify(scenes,null,2)+'\n');
