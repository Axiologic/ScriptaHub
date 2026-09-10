import fs from 'node:fs';
import {householdArt} from '../review-revision/household-art.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
scenes.forEach((s,i)=>s.visual=householdArt(i));
fs.writeFileSync(file,JSON.stringify(scenes,null,2)+'\n');
