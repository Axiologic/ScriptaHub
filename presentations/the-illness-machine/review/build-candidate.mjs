import fs from 'node:fs/promises';
import path from 'node:path';
import {buildBookFilm} from '../../../tools/shf/build-book-film.mjs';
const root=path.resolve('presentations/the-illness-machine');
const filename=path.join(root,'work/production.json'),saved=await fs.readFile(filename,'utf8');
try { const p=JSON.parse(saved);p.bookDirectory=path.join(root,'review/candidate-book');await fs.writeFile(filename,JSON.stringify(p,null,2)+'\n');await buildBookFilm(root); }
finally {await fs.writeFile(filename,saved);}
