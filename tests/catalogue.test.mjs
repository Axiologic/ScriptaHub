import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { checkCatalogue, keywordNormalise, LANGUAGES, slugify } from '../tools/check_catalogue.mjs';
import { casefold, keywordIdentifier } from '../tools/build_books.mjs';

const cli = fileURLToPath(new URL('../tools/build_books.mjs', import.meta.url));

function localise(value) {
    return Object.fromEntries(LANGUAGES.map((code) => [code, typeof value === 'function' ? value(code) : value]));
}

function saveJson(target, value) {
    writeFileSync(target, `${JSON.stringify(value, null, 2)}\n`);
}

function fixture(t) {
    const temp = mkdtempSync(path.join(tmpdir(), 'scripta-catalogue-'));
    t.after(() => rmSync(temp, { recursive: true, force: true }));
    const docs = path.join(temp, 'docs');
    const directory = 'books/a/fixture/bk-0123456789abcdef';
    const root = path.join(docs, directory);
    mkdirSync(root, { recursive: true });
    const ids = Array.from({ length: 100 }, (_, index) => `subject:${index}`);
    const manifest = {
        id: 'bk-0123456789abcdef', route: ['a', 'fixture'], keywordIds: ids,
        title: localise('A Fixture'), subtitle: localise(''), shortDescription: localise('Description'),
        keywords: localise(() => ids.map((_, index) => `Subject ${index}`)),
        coverUrl: localise((code) => `${code}/cover.webp`),
    };
    const collection = {
        bookCount: 1,
        books: [{
            id: manifest.id, directory, keywordIds: structuredClone(ids),
            editions: localise((code) => ({
                book: `${directory}/${code}/book.html`, cover: `${directory}/${code}/cover.webp`,
            })),
        }],
        keywords: localise(() => ids.map((id, index) => ({ id, label: `Subject ${index}`, count: 1 }))),
    };
    for (const language of LANGUAGES) {
        mkdirSync(path.join(root, language));
        writeFileSync(path.join(root, language, 'cover.webp'), 'fixture');
        const words = ids.map((id) => ({ href: `index.html?lang=${language}&keyword=${encodeURIComponent(id)}` }));
        writeFileSync(path.join(root, language, 'book.html'), `<script>const words=${JSON.stringify(words)};</script>`);
    }
    const history = {
        bookId: manifest.id, currentEdition: 'edition-1',
        editions: [{ id: 'edition-1', publishedAt: '2026-09-08', changes: localise('Initial'), pdf: {} }],
    };
    const save = () => {
        saveJson(path.join(docs, 'collection.json'), collection);
        saveJson(path.join(root, 'manifest.json'), manifest);
        saveJson(path.join(root, 'editions.json'), history);
    };
    save();
    const problems = () => checkCatalogue(docs).join('\n');
    return { temp, docs, root, manifest, collection, history, save, problems };
}

test('routes and keyword equivalence preserve ASCII removal and Unicode case folding', () => {
    assert.equal(slugify('Can’t See the World — Café'), 'cant-see-the-world-cafe');
    assert.equal(slugify('Maße'), 'mae');
    assert.equal(keywordNormalise('Maße'), keywordNormalise('MASSE'));
    assert.equal(keywordNormalise('ẞ').trim(), 'ss');
    assert.equal(keywordNormalise('Café'), keywordNormalise('Cafe\u0301'));
    assert.equal(keywordNormalise('ﬁeld').trim(), 'field');
    assert.equal(casefold('Straße'), 'strasse');
    assert.equal(casefold('Ꭰ'), 'Ꭰ');
    assert.equal(casefold('ꭰ'), 'Ꭰ');
    assert.equal(casefold('ﬀ'), 'ff');
    assert.equal(keywordIdentifier('Straße'), keywordIdentifier('STRASSE'));
    assert.equal(keywordIdentifier('ﬀ'), keywordIdentifier('ff'));
});

test('a valid catalogue passes in all eight languages', (t) => {
    assert.deepEqual(checkCatalogue(fixture(t).docs), []);
});

test('counts, metadata, normalized duplicate keywords, and incorrect keyword links fail', (t) => {
    const f = fixture(t);
    f.collection.bookCount = 2;
    f.collection.keywords.fr[0].count = 3;
    f.manifest.keywords.de.splice(0, 2, 'Maße', 'Masse');
    delete f.manifest.subtitle.ro;
    f.save();
    const page = path.join(f.root, 'it', 'book.html');
    writeFileSync(page, readFileSync(page, 'utf8').replace('keyword=subject%3A0', 'keyword=orphan'));
    const problems = f.problems();
    for (const expected of [
        'bookCount', 'fr: keyword count mismatch', 'de: expected 100 distinct keywords',
        'ro: missing subtitle', 'it: book-page keyword links',
    ]) {
        assert.ok(problems.includes(expected), `${expected}\n${problems}`);
    }
});

test('invalid history, a missing current edition, and PDF boundary errors fail', (t) => {
    const f = fixture(t);
    f.history.currentEdition = 'nonexistent';
    f.history.editions[0].pdf.en = '../../../../outside.pdf';
    f.save();
    assert.match(f.problems(), /current edition is missing/);
    assert.match(f.problems(), /unsafe historical PDF/);
    for (const invalid of ['{', 'null', '{}', '{"editions": null}']) {
        writeFileSync(path.join(f.root, 'editions.json'), invalid);
        assert.match(f.problems(), /invalid editions\.json/, invalid);
    }
});

test('historical and aggregate assets cannot escape through symlinks', (t) => {
    const f = fixture(t);
    const outside = path.join(f.temp, 'outside.pdf');
    writeFileSync(outside, 'public fixture');
    symlinkSync(outside, path.join(f.root, 'en', 'book.pdf'));
    f.history.editions[0].pdf.en = 'en/book.pdf';
    f.collection.books[0].editions.en.pdf = `${f.collection.books[0].directory}/en/book.pdf`;
    f.save();
    assert.match(f.problems(), /unsafe historical PDF: en\/book\.pdf/);
    assert.match(f.problems(), /unsafe edition asset/);
});

test('parent traversal inside a symlink target cannot hide an escaping PDF', (t) => {
    const f = fixture(t);
    const outside = path.join(f.temp, 'outside');
    mkdirSync(path.join(outside, 'subdir'), { recursive: true });
    writeFileSync(path.join(outside, 'private.pdf'), 'outside document');
    symlinkSync(path.join(outside, 'subdir'), path.join(f.root, 'link'), 'dir');
    symlinkSync('link/../private.pdf', path.join(f.root, 'alias.pdf'));
    f.history.editions[0].pdf.en = 'alias.pdf';
    f.collection.books[0].editions.en.pdf = `${f.collection.books[0].directory}/alias.pdf`;
    f.save();
    assert.match(f.problems(), /unsafe historical PDF: alias\.pdf/);
    assert.match(f.problems(), /unsafe edition asset/);
});

test('unlisted manifests and forbidden keyword routes fail', (t) => {
    const f = fixture(t);
    const orphan = path.join(f.docs, 'books', 'unlisted');
    mkdirSync(orphan);
    writeFileSync(path.join(orphan, 'manifest.json'), '{}');
    mkdirSync(path.join(f.docs, 'keywords'));
    assert.match(f.problems(), /manifest missing from collection/);
    assert.match(f.problems(), /legacy per-keyword pages/);
});

test('duplicate IDs, manifest mismatch, aggregate divergence, and missing languages fail', (t) => {
    const f = fixture(t);
    f.collection.books.push(structuredClone(f.collection.books[0]));
    f.manifest.id = 'bk-other';
    f.collection.books[0].keywordIds.reverse();
    delete f.collection.keywords.pl;
    f.save();
    const problems = f.problems();
    for (const expected of [
        'duplicate book ID', 'manifest ID mismatch', 'collection keyword IDs differ', 'pl: missing collection keywords',
    ]) {
        assert.ok(problems.includes(expected), `${expected}\n${problems}`);
    }
});

test('invalid JSON shapes and malformed entries report catalogue problems', (t) => {
    const f = fixture(t);
    for (const invalid of ['{', 'null', '[]', '{}', '{"books": null}']) {
        writeFileSync(path.join(f.docs, 'collection.json'), invalid);
        assert.ok(checkCatalogue(f.docs).length > 0, invalid);
    }
    f.save();
    for (const invalid of ['{', 'null', '[]']) {
        writeFileSync(path.join(f.root, 'manifest.json'), invalid);
        assert.match(f.problems(), /invalid manifest\.json/, invalid);
    }
    f.collection.books.push(null);
    f.collection.keywords.en.push(null);
    f.save();
    assert.match(f.problems(), /malformed collection keyword/);
    assert.match(f.problems(), /missing or unsafe manifest/);
});

test('a manifest path cannot escape the catalogue through a directory symlink', (t) => {
    const f = fixture(t);
    const outside = path.join(f.temp, 'outside');
    mkdirSync(outside);
    saveJson(path.join(outside, 'manifest.json'), f.manifest);
    symlinkSync(outside, path.join(f.docs, 'books', 'redirected'), 'dir');
    f.collection.books[0].directory = 'books/redirected';
    f.save();
    assert.match(f.problems(), /missing or unsafe manifest/);
});

test('the checker CLI exits zero for valid data, one for invalid data, and two for invalid arguments', (t) => {
    const f = fixture(t);
    const run = (...arguments_) => spawnSync(process.execPath, [cli, ...arguments_], {
        encoding: 'utf8', cwd: f.temp, timeout: 30000,
    });
    const valid = run('check', '--docs', f.docs);
    assert.equal(valid.status, 0, valid.stderr);
    writeFileSync(path.join(f.docs, 'collection.json'), 'null');
    const invalid = run('check', '--docs', f.docs);
    assert.equal(invalid.status, 1, invalid.stderr);
    assert.match(invalid.stderr, /books must be an array/);
    assert.equal(run('check', '--oops').status, 2);
});
