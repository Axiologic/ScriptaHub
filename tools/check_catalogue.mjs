#!/usr/bin/env node
import { existsSync, readFileSync, realpathSync, statSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const LANGUAGES = ['en', 'fr', 'de', 'es', 'pt', 'it', 'ro', 'pl'];
export const DEFAULT_DOCS = fileURLToPath(new URL('../docs/', import.meta.url));
const readJson = (file) => JSON.parse(readFileSync(file, 'utf8'));
const isFile = (file) => { try { return statSync(file).isFile(); } catch { return false; } };
const sameSet = (a, b) => a.size === b.size && [...a].every((item) => b.has(item));
const ascii = (text) => String(text).normalize('NFKD').replace(/[^\x00-\x7F]/g, '');
export const slugify = (text) => ascii(text).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'keyword';
export const keywordNormalise = (text) => ascii(String(text).toLowerCase().replace(/ß/g, 'ss')).replace(/[^a-z0-9]+/g, ' ').trim();

function within(target, root) {
  const relative = path.relative(root, target);
  return relative !== '..' && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
}

function localFile(root, relative) {
  if (typeof relative !== 'string' || !relative || path.isAbsolute(relative)) return false;
  const target = path.resolve(root, relative);
  return within(target, root) && isFile(target) && within(realpathSync(target), realpathSync(root));
}

function manifestsUnder(root) {
  if (!existsSync(root)) return [];
  return readdirSync(root, { withFileTypes: true }).flatMap((entry) => {
    const target = path.join(root, entry.name);
    return entry.isDirectory() ? manifestsUnder(target) : entry.isFile() && entry.name === 'manifest.json' ? [target] : [];
  });
}

/** Validate the manifest catalogue and generated assets without changing them. */
export function checkCatalogue(docs = DEFAULT_DOCS) {
  docs = path.resolve(docs);
  const problems = [];
  const collectionFile = path.join(docs, 'collection.json');
  if (!isFile(collectionFile)) return ['missing docs/collection.json'];
  let collection;
  try { collection = readJson(collectionFile); } catch { return ['invalid docs/collection.json']; }
  if (!collection || !Array.isArray(collection.books)) return ['collection books must be an array'];
  const books = collection.books;
  if (collection.bookCount !== books.length) problems.push('collection bookCount does not match books');
  const counts = new Map();
  for (const book of books) for (const id of book?.keywordIds ?? []) counts.set(id, (counts.get(id) ?? 0) + 1);
  const keywordSets = {};
  for (const language of LANGUAGES) {
    const entries = collection.keywords?.[language];
    if (!Array.isArray(entries)) { problems.push(`${language}: missing collection keywords`); keywordSets[language] = new Set(); continue; }
    keywordSets[language] = new Set(entries.map((entry) => entry.id));
    if (keywordSets[language].size !== entries.length) problems.push(`${language}: duplicate keyword IDs in collection`);
    for (const entry of entries) if (entry.count !== (counts.get(entry.id) ?? 0)) problems.push(`${language}: keyword count mismatch for ${entry.id}`);
  }
  for (const language of LANGUAGES) if (!sameSet(keywordSets[language], keywordSets.en)) problems.push(`${language}: keyword IDs do not match the language-independent English set`);
  const listedManifests = new Set();
  const bookIds = new Set();
  for (const book of books) {
    if (!book || typeof book.directory !== 'string' || !localFile(docs, `${book.directory}/manifest.json`)) {
      problems.push(`missing or unsafe manifest: ${book?.directory ?? '(no directory)'}/manifest.json`); continue;
    }
    const root = path.resolve(docs, book.directory);
    const manifestPath = path.join(root, 'manifest.json');
    listedManifests.add(manifestPath);
    let manifest;
    try { manifest = readJson(manifestPath); } catch { problems.push(`${book.id}: invalid manifest.json`); continue; }
    if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) { problems.push(`${book.id}: invalid manifest.json`); continue; }
    if (bookIds.has(book.id)) problems.push(`${book.id}: duplicate book ID in collection`);
    bookIds.add(book.id);
    if (manifest.id !== book.id) problems.push(`${book.id}: manifest ID mismatch`);
    const route = slugify(manifest.title?.en ?? '').split('-');
    if (JSON.stringify(manifest.route) !== JSON.stringify(route)) problems.push(`${book.id}: route does not match English title words`);
    if (book.directory !== ['books', ...route, manifest.id].join('/')) problems.push(`${book.id}: directory does not match title route and random ID`);

    if (!localFile(root, 'editions.json')) problems.push(`${book.id}: missing editions.json`);
    else {
      try {
        const history = readJson(path.join(root, 'editions.json'));
        if (!history || !Array.isArray(history.editions)) throw new Error('invalid history');
        if (history.bookId !== book.id) problems.push(`${book.id}: editions.json bookId mismatch`);
        if (!history.editions.some((entry) => entry?.id === history.currentEdition)) problems.push(`${book.id}: editions.json current edition is missing`);
        for (const entry of history.editions) {
          if (!entry || !entry.publishedAt || !entry.changes || typeof entry.changes !== 'object' || Array.isArray(entry.changes)) { problems.push(`${book.id}: malformed edition history entry`); continue; }
          for (const pdf of Object.values(entry.pdf ?? {})) if (!localFile(root, pdf)) problems.push(`${book.id}: missing or unsafe historical PDF: ${pdf}`);
        }
      } catch { problems.push(`${book.id}: invalid editions.json`); }
    }
    const identifiers = Array.isArray(manifest.keywordIds) ? manifest.keywordIds : [];
    const idSet = new Set(identifiers);
    if (identifiers.length !== 100 || idSet.size !== 100) problems.push(`${book.id}: expected 100 distinct keyword IDs, got ${identifiers.length}`);
    const missing = [...idSet].filter((id) => !keywordSets.en.has(id));
    if (missing.length) problems.push(`${book.id}: keyword IDs missing from collection: ${missing.sort().join(', ')}`);
    if (JSON.stringify(book.keywordIds) !== JSON.stringify(identifiers)) problems.push(`${book.id}: collection keyword IDs differ from manifest`);
    for (const language of LANGUAGES) {
      const keywords = manifest.keywords?.[language] ?? [];
      const normalised = Array.isArray(keywords) ? keywords.map(keywordNormalise) : [];
      if (normalised.length !== 100 || new Set(normalised).size !== 100) problems.push(`${book.id} ${language}: expected 100 distinct keywords, got ${normalised.length}`);
      if (normalised.includes(keywordNormalise(manifest.title?.[language] ?? ''))) problems.push(`${book.id} ${language}: book title used as a keyword`);
      for (const field of ['title', 'subtitle', 'shortDescription', 'coverUrl']) if (!Object.hasOwn(manifest[field] ?? {}, language)) problems.push(`${book.id} ${language}: missing ${field}`);
      if (!localFile(root, `${language}/book.html`)) problems.push(`${book.id} ${language}: missing book page`);
      else {
        const source = readFileSync(path.join(root, language, 'book.html'), 'utf8');
        let pageIds;
        try { pageIds = [...source.matchAll(/(?:&|&amp;)keyword=([^"&<\s]+)/g)].map((match) => decodeURIComponent(match[1])); }
        catch { pageIds = []; }
        if (pageIds.length !== identifiers.length || !sameSet(new Set(pageIds), idSet)) problems.push(`${book.id} ${language}: book-page keyword links do not match the manifest`);
      }
    }
    for (const edition of Object.values(book.editions ?? {})) for (const asset of Object.values(edition ?? {})) if (!localFile(docs, asset)) problems.push(`missing or unsafe edition asset: ${asset}`);
  }
  for (const manifest of manifestsUnder(path.join(docs, 'books'))) if (!listedManifests.has(manifest)) problems.push(`manifest missing from collection: ${path.relative(docs, manifest)}`);
  if (existsSync(path.join(docs, 'keywords'))) problems.push('legacy per-keyword pages exist; discovery must use the client-side catalogue filter');
  return problems;
}

export function main(argv = process.argv.slice(2)) {
  let docs = DEFAULT_DOCS;
  if (argv.length) {
    if (argv.length !== 2 || argv[0] !== '--root') { console.error('Usage: node tools/check_catalogue.mjs [--root docs]'); return 2; }
    docs = argv[1];
  }
  try {
    const problems = checkCatalogue(docs);
    if (problems.length) { console.error(problems.join('\n')); return 1; }
    console.log('Catalogue is valid.'); return 0;
  } catch (error) { console.error(`Unable to check catalogue: ${error.message}`); return 2; }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) process.exitCode = main();
