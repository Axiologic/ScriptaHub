import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {revisedTaskVisual} from './review-revision/task-art.mjs';
import {remainingVisual} from './review-revision/remaining-art.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const scenes=JSON.parse(fs.readFileSync(path.join(root,'work/scenes.json')));
for(let i=0;i<scenes.length;i++)scenes[i].visual=[1,3,4].includes(i)?revisedTaskVisual(i):remainingVisual(i);
fs.writeFileSync(path.join(root,'work/scenes.json'),JSON.stringify(scenes,null,2)+'\n');
