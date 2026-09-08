import assert from 'node:assert/strict';
import test from 'node:test';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { checkCatalogue, keywordNormalise, LANGUAGES, slugify } from '../tools/check_catalogue.mjs';

function fixture(t) {
  const temp = mkdtempSync(path.join(tmpdir(), 'scripta-catalogue-'));
  t.after(() => rmSync(temp, { recursive: true, force: true }));
  const docs = path.join(temp, 'docs');
  const directory = 'books/a/fixture/bk-0123456789abcdef';
  const root = path.join(docs, directory);
  mkdirSync(root, { recursive: true });
  const ids = Array.from({ length: 100 }, (_, n) => `subject:${n}`);
  const localise = (value) => Object.fromEntries(LANGUAGES.map((code) => [code, typeof value === 'function' ? value(code) : value]));
  const manifest = {
    id: 'bk-0123456789abcdef', route: ['a', 'fixture'], keywordIds: ids,
    title: localise('A Fixture'), subtitle: localise(''), shortDescription: localise('Description'),
    keywords: localise(() => ids.map((_, n) => `Subject ${n}`)), coverUrl: localise((code) => `${code}/cover.webp`),
  };
  const collection = {
    bookCount: 1, books: [{ id: manifest.id, directory, keywordIds: ids, editions: localise((code) => ({ book: `${directory}/${code}/book.html`, cover: `${directory}/${code}/cover.webp` })) }],
    keywords: localise(() => ids.map((id, n) => ({ id, label: `Subject ${n}`, count: 1 }))),
  };
  for (const language of LANGUAGES) {
    mkdirSync(path.join(root, language));
    writeFileSync(path.join(root, language, 'cover.webp'), 'fixture');
    writeFileSync(path.join(root, language, 'book.html'), `<script>const words=${JSON.stringify(ids.map((id) => ({ href: `index.html?lang=${language}&keyword=${encodeURIComponent(id)}` })))};</script>`);
  }
  const history = { bookId: manifest.id, currentEdition: 'edition-1', editions: [{ id: 'edition-1', publishedAt: '2026-09-08', changes: localise('Initial'), pdf: {} }] };
  const save = () => {
    writeFileSync(path.join(docs, 'collection.json'), JSON.stringify(collection));
    writeFileSync(path.join(root, 'manifest.json'), JSON.stringify(manifest));
    writeFileSync(path.join(root, 'editions.json'), JSON.stringify(history));
  };
  save();
  return { temp, docs, root, manifest, collection, history, save };
}

test('routes and keyword equivalence preserve ASCII removal and Unicode case folding', () => {
  assert.equal(slugify('Can’t See the World — Café'), 'cant-see-the-world-cafe');
  assert.equal(slugify('Maße'), 'mae');
  assert.equal(keywordNormalise('Maße'), keywordNormalise('MASSE'));
  assert.equal(keywordNormalise('ẞ'), 'ss');
  assert.equal(keywordNormalise('Café'), keywordNormalise('Cafe\u0301'));
  assert.equal(keywordNormalise('ﬁeld'), 'field');
});

test('valid catalogue uses inline keyword JSON and all eight languages', (t) => {
  assert.deepEqual(checkCatalogue(fixture(t).docs), []);
});

test('count, language metadata, normalized duplicate and keyword URL errors fail', (t) => {
  const f = fixture(t);
  f.collection.bookCount = 2;
  f.collection.keywords.fr[0].count = 3;
  f.manifest.keywords.de.splice(0, 2, 'Maße', 'Masse');
  delete f.manifest.subtitle.ro;
  f.save();
  const page = path.join(f.root, 'it/book.html');
  writeFileSync(page, readFileSync(page, 'utf8').replace('keyword=subject%3A0', 'keyword=orphan'));
  const problems = checkCatalogue(f.docs).join('\n');
  assert.match(problems, /bookCount/);
  assert.match(problems, /fr: keyword count mismatch/);
  assert.match(problems, /de: expected 100 distinct keywords/);
  assert.match(problems, /ro: missing subtitle/);
  assert.match(problems, /it: book-page keyword links/);
});

test('missing current history, malformed history, and unsafe PDF targets fail', (t) => {
  const f = fixture(t);
  f.history.currentEdition = 'nonexistent';
  f.history.editions[0].pdf.en = '../../../../outside.pdf';
  f.save();
  assert.match(checkCatalogue(f.docs).join('\n'), /current edition is missing/);
  assert.match(checkCatalogue(f.docs).join('\n'), /unsafe historical PDF/);
  writeFileSync(path.join(f.root, 'editions.json'), '{');
  assert.match(checkCatalogue(f.docs).join('\n'), /invalid editions.json/);
});

test('symlinked historical PDFs outside the book root fail', (t) => {
  const f = fixture(t);
  writeFileSync(path.join(f.temp, 'outside.pdf'), 'public fixture');
  symlinkSync(path.join(f.temp, 'outside.pdf'), path.join(f.root, 'en/book.pdf'));
  f.history.editions[0].pdf.en = 'en/book.pdf';
  f.save();
  assert.match(checkCatalogue(f.docs).join('\n'), /unsafe historical PDF: en\/book.pdf/);
});

test('unlisted manifests and forbidden keyword routes fail', (t) => {
  const f = fixture(t);
  mkdirSync(path.join(f.docs, 'books/unlisted'));
  writeFileSync(path.join(f.docs, 'books/unlisted/manifest.json'), '{}');
  mkdirSync(path.join(f.docs, 'keywords'));
  assert.match(checkCatalogue(f.docs).join('\n'), /manifest missing from collection/);
  assert.match(checkCatalogue(f.docs).join('\n'), /legacy per-keyword pages/);
});

test('checker CLI exits zero for valid data, one for invalid data, two for invalid arguments', (t) => {
  const f = fixture(t);
  const cli = fileURLToPath(new URL('../tools/check_catalogue.mjs', import.meta.url));
  const run = (...args) => spawnSync(process.execPath, [cli, ...args], { encoding: 'utf8' });
  assert.equal(run('--root', f.docs).status, 0);
  writeFileSync(path.join(f.docs, 'collection.json'), 'null');
  const invalid = run('--root', f.docs);
  assert.equal(invalid.status, 1);
  assert.match(invalid.stderr, /books must be an array/);
  assert.equal(run('--oops').status, 2);
});
