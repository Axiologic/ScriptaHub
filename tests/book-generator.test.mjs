import assert from 'node:assert/strict';
import test from 'node:test';
import { existsSync, mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync, symlinkSync } from 'node:fs';
import path from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { ensureEditionsFile, planRefresh, refreshPages } from '../tools/build_books.mjs';

const sourceDocs = fileURLToPath(new URL('../docs/', import.meta.url));
const sourceCollection = JSON.parse(readFileSync(path.join(sourceDocs, 'collection.json'), 'utf8'));
function fixture(t) {
  const temp = mkdtempSync(path.join(tmpdir(), 'scripta-generator-'));
  t.after(() => rmSync(temp, { force: true, recursive: true }));
  const docsRoot = path.join(temp, 'docs');
  const listing = sourceCollection.books.find((book) => book.editions.en.pdf);
  const bookRoot = path.join(docsRoot, listing.directory);
  mkdirSync(bookRoot, { recursive: true });
  const manifest = JSON.parse(readFileSync(path.join(sourceDocs, listing.directory, 'manifest.json'), 'utf8'));
  const collection = { ...sourceCollection, books: [listing], bookCount: 1 };
  for (const { code } of collection.supportedLanguages) mkdirSync(path.join(bookRoot, code));
  writeFileSync(path.join(docsRoot, 'collection.json'), JSON.stringify(collection));
  writeFileSync(path.join(bookRoot, 'manifest.json'), JSON.stringify(manifest));
  return { temp, docsRoot, bookRoot, manifest, collection };
}

test('refresh creates eight pages and initial history, then becomes a no-op', (t) => {
  const f = fixture(t);
  const plan = planRefresh(f);
  assert.equal(plan.pages, 8);
  assert.equal(plan.files.length, 9);
  assert.equal(existsSync(path.join(f.bookRoot, 'editions.json')), false, 'planning must not write');
  assert.deepEqual(refreshPages(f), { books: 1, pages: 8, changedFiles: 9 });
  assert.deepEqual(refreshPages(f), { books: 1, pages: 8, changedFiles: 0 });
  const history = JSON.parse(readFileSync(path.join(f.bookRoot, 'editions.json'), 'utf8'));
  assert.equal(history.bookId, f.manifest.id);
  assert.equal(history.editions[0].pdf.en, f.manifest.editions.en.pdf);
  assert.equal(Object.keys(history.editions[0].changes).length, 8);
});

test('history preserves archives, current PDF decisions, and unknown metadata', (t) => {
  const f = fixture(t);
  ensureEditionsFile(f.bookRoot, f.manifest);
  const historyPath = path.join(f.bookRoot, 'editions.json');
  const history = JSON.parse(readFileSync(historyPath, 'utf8'));
  history.extra = { note: 'retain' };
  history.editions[0].pdf.en = 'edition-files/first/en.pdf';
  const initial = structuredClone(history.editions[0]);
  history.editions.push({ id: 'edition-2', number: 2, publishedAt: '2026-09-08', changes: { en: 'A second edition' }, pdf: { en: 'edition-files/current/en.pdf' }, custom: true });
  history.currentEdition = 'edition-2';
  writeFileSync(historyPath, JSON.stringify(history, null, 4) + '\n');
  const before = readFileSync(historyPath, 'utf8');
  ensureEditionsFile(f.bookRoot, f.manifest);
  assert.equal(readFileSync(historyPath, 'utf8'), before);
  assert.deepEqual(JSON.parse(before).editions[0], initial);
});

test('malformed edition history fails before writing any page or repairing history', (t) => {
  const f = fixture(t);
  const historyPath = path.join(f.bookRoot, 'editions.json');
  for (const invalid of ['{', '{}', 'null']) {
    writeFileSync(historyPath, invalid);
    assert.throws(() => refreshPages(f), /Malformed existing edition history/);
    assert.equal(readFileSync(historyPath, 'utf8'), invalid);
    assert.equal(existsSync(path.join(f.bookRoot, 'en/book.html')), false);
  }
});

test('invalid final-language input prevents partial writes of earlier planned pages', (t) => {
  const f = fixture(t);
  delete f.manifest.title.pl;
  writeFileSync(path.join(f.bookRoot, 'manifest.json'), JSON.stringify(f.manifest));
  assert.throws(() => refreshPages(f), /missing title.pl/);
  assert.equal(existsSync(path.join(f.bookRoot, 'en/book.html')), false);
  assert.equal(existsSync(path.join(f.bookRoot, 'editions.json')), false);
});

test('refresh rejects escaping output symlinks and forbidden keyword routes', (t) => {
  const f = fixture(t);
  const outside = path.join(f.temp, 'outside.html');
  writeFileSync(outside, 'untouched');
  symlinkSync(outside, path.join(f.bookRoot, 'en/book.html'));
  assert.throws(() => refreshPages(f), /Refusing non-file output/);
  assert.equal(readFileSync(outside, 'utf8'), 'untouched');
  mkdirSync(path.join(f.docsRoot, 'keywords'));
  assert.throws(() => refreshPages(f), /Legacy docs\/keywords/);
  assert.ok(existsSync(path.join(f.docsRoot, 'keywords')));
});

test('refresh CLI supports a dry run and reports bad input with a nonzero exit', (t) => {
  const f = fixture(t);
  const cli = fileURLToPath(new URL('../tools/build_books.mjs', import.meta.url));
  const result = spawnSync(process.execPath, [cli, 'refresh', '--docs', f.docsRoot, '--dry-run'], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /8 pages, 9 changed files/);
  assert.equal(existsSync(path.join(f.bookRoot, 'editions.json')), false);
  const bad = spawnSync(process.execPath, [cli, 'refresh', '--unknown'], { encoding: 'utf8' });
  assert.notEqual(bad.status, 0);
  assert.match(bad.stderr, /Unknown or incomplete option/);
});
