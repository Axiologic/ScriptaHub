import fs from 'node:fs';
import {bakeryArt} from '../review-revision/bakery-art.mjs';
const file=new URL('./scenes.json',import.meta.url);
const scenes=JSON.parse(fs.readFileSync(file));
scenes.forEach((scene,index)=>scene.visual=bakeryArt(index));
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
