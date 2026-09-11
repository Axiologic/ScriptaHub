import {buildBookFilm} from '../../tools/shf/build-book-film.mjs';
import fs from 'node:fs';
import path from 'node:path';
await buildBookFilm(new URL('.',import.meta.url).pathname);
const root=new URL('.',import.meta.url).pathname;
const directionFile=path.join(root,'work/film.direction.json');
if(fs.existsSync(directionFile)){
  const direction=JSON.parse(fs.readFileSync(directionFile,'utf8'));
  direction.sources=direction.sources.map((source,index)=>({...source,id:`source-${index}`}));
  fs.writeFileSync(directionFile,JSON.stringify(direction,null,2)+'\n');
}
