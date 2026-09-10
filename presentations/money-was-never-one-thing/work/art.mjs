import fs from 'node:fs';
import {mutualCreditArt} from '../review-revision/mutual-credit-art.mjs';
import {monetaryArt} from '../review-revision/monetary-objects-art.mjs';
const file=new URL('./scenes.json',import.meta.url),scenes=JSON.parse(fs.readFileSync(file));
for(const [i,s]of scenes.entries())s.visual=i===2?mutualCreditArt():monetaryArt(i);
fs.writeFileSync(file,JSON.stringify(scenes,null,2));
