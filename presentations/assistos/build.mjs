import {buildBookFilm} from '../../tools/shf/build-book-film.mjs';
await buildBookFilm(new URL('.', import.meta.url).pathname);
