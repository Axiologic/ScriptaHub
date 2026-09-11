import {buildBookFilm} from '../../tools/shf/build-book-film.mjs';
import fs from 'node:fs';
import path from 'node:path';

// AssistOS uses the shared compiler; source, edition, production settings and
// approved scene direction remain book-owned in this directory.
await buildBookFilm(new URL('.', import.meta.url).pathname);

// The shared authoring verbs use source-N references. Keep this book's
// section metadata compatible with that direction contract without changing
// the shared compiler or the approved spoken plan.
const root = new URL('.', import.meta.url).pathname;
const directionFile = path.join(root, 'work/film.direction.json');
if (fs.existsSync(directionFile)) {
  const direction = JSON.parse(fs.readFileSync(directionFile, 'utf8'));
  direction.sources = direction.sources.map((source, index) => ({...source, id: `source-${index}`}));
  fs.writeFileSync(directionFile, JSON.stringify(direction, null, 2) + '\n');
}
