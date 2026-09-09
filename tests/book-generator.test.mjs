import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
    cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync,
    rmdirSync, statSync, symlinkSync, unlinkSync, writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import {
    ensureEditionsFile, planRefresh, prepareEditionsFile, refreshPages,
} from '../tools/build_books.mjs';

const sourceDocs = fileURLToPath(new URL('../docs/', import.meta.url));
const cli = fileURLToPath(new URL('../tools/build_books.mjs', import.meta.url));
const sourceCollection = JSON.parse(readFileSync(path.join(sourceDocs, 'collection.json'), 'utf8'));
const languages = sourceCollection.supportedLanguages.map(({ code }) => code);

function saveJson(target, value) {
    writeFileSync(target, `${JSON.stringify(value, null, 2)}\n`);
}

function fixture(t) {
    const temp = mkdtempSync(path.join(tmpdir(), 'scripta-generator-'));
    t.after(() => rmSync(temp, { force: true, recursive: true }));
    const docsRoot = path.join(temp, 'docs');
    const listing = structuredClone(sourceCollection.books.find((book) => book.editions.en.pdf));
    const bookRoot = path.join(docsRoot, listing.directory);
    mkdirSync(bookRoot, { recursive: true });
    const manifest = JSON.parse(readFileSync(path.join(sourceDocs, listing.directory, 'manifest.json'), 'utf8'));
    const collection = { ...structuredClone(sourceCollection), books: [listing], bookCount: 1 };
    for (const language of languages) {
        mkdirSync(path.join(bookRoot, language));
    }
    saveJson(path.join(docsRoot, 'collection.json'), collection);
    const saveManifest = () => saveJson(path.join(bookRoot, 'manifest.json'), manifest);
    saveManifest();
    const assertNoGeneratedOutputs = () => {
        assert.equal(existsSync(path.join(bookRoot, 'en', 'book.html')), false);
        assert.equal(existsSync(path.join(bookRoot, 'editions.json')), false);
    };
    return { temp, docsRoot, bookRoot, manifest, collection, saveManifest, assertNoGeneratedOutputs };
}

test('refresh plans every page, is idempotent, and preserves canonical assets', (t) => {
    const f = fixture(t);
    const canonical = new Map(['book.pdf', 'full_content.html', 'short_content.html', 'cover.webp'].map((name) => [
        path.join(f.bookRoot, 'en', name), Buffer.from(`untouched ${name}`),
    ]));
    for (const [target, content] of canonical) {
        writeFileSync(target, content);
    }
    const plan = planRefresh(f);
    assert.equal(plan.pages, 8);
    assert.equal(plan.files.length, 9);
    f.assertNoGeneratedOutputs();
    assert.deepEqual(refreshPages(f), { books: 1, pages: 8, changedFiles: 9 });
    const mtimes = new Map(plan.files.map((output) => [output.path, statSync(output.path, { bigint: true }).mtimeNs]));
    assert.deepEqual(refreshPages(f), { books: 1, pages: 8, changedFiles: 0 });
    for (const [target, before] of mtimes) {
        assert.equal(statSync(target, { bigint: true }).mtimeNs, before, target);
    }
    for (const [target, content] of canonical) {
        assert.deepEqual(readFileSync(target), content, target);
    }
    const history = JSON.parse(readFileSync(path.join(f.bookRoot, 'editions.json'), 'utf8'));
    assert.equal(history.bookId, f.manifest.id);
    assert.equal(history.editions[0].pdf.en, f.manifest.editions.en.pdf);
    assert.deepEqual(Object.keys(history.editions[0].changes).sort(), [...languages].sort());
});

test('refresh regenerates stale and missing pages after manifest edits', (t) => {
    const f = fixture(t);
    refreshPages(f);
    f.manifest.title.pl = 'An updated localized title';
    f.saveManifest();
    unlinkSync(path.join(f.bookRoot, 'fr', 'book.html'));
    assert.equal(refreshPages(f).changedFiles, 2);
    assert.match(readFileSync(path.join(f.bookRoot, 'pl', 'book.html'), 'utf8'), /An updated localized title/);
    assert.ok(statSync(path.join(f.bookRoot, 'fr', 'book.html')).isFile());
});

test('history preserves archives, current PDF choices, unknown metadata, and unchanged bytes', (t) => {
    const f = fixture(t);
    ensureEditionsFile(f.bookRoot, f.manifest);
    const target = path.join(f.bookRoot, 'editions.json');
    const history = JSON.parse(readFileSync(target, 'utf8'));
    history.extra = { note: 'retain' };
    history.editions[0].pdf.en = 'edition-files/first/en.pdf';
    const initial = structuredClone(history.editions[0]);
    history.editions.push({
        id: 'edition-2', number: 2, publishedAt: '2026-09-08',
        changes: { en: 'A second edition' }, pdf: { en: 'edition-files/current/en.pdf' }, custom: true,
    });
    history.currentEdition = 'edition-2';
    const before = Buffer.from(`${JSON.stringify(history, null, 4)}\r\n`);
    writeFileSync(target, before);
    assert.equal(ensureEditionsFile(f.bookRoot, f.manifest).changed, false);
    assert.deepEqual(readFileSync(target), before);
    assert.deepEqual(JSON.parse(readFileSync(target, 'utf8')).editions[0], initial);
    delete history.editions[1].pdf.en;
    saveJson(target, history);
    assert.equal(ensureEditionsFile(f.bookRoot, f.manifest).changed, true);
    const extended = JSON.parse(readFileSync(target, 'utf8'));
    assert.deepEqual(extended.editions[0], initial);
    assert.equal(extended.editions[1].custom, true);
    assert.deepEqual(extended.extra, { note: 'retain' });
    assert.equal(extended.editions[1].pdf.en, f.manifest.editions.en.pdf);
});

test('refresh replaces an invalid UTF-8 generated page', (t) => {
    const f = fixture(t);
    refreshPages(f);
    const target = path.join(f.bookRoot, 'en', 'book.html');
    const expected = readFileSync(target);
    writeFileSync(target, Buffer.from([0xff, 0xfe, ...Buffer.from(' invalid generated output')]));
    assert.equal(refreshPages(f).changedFiles, 1);
    assert.deepEqual(readFileSync(target), expected);
});

test('invalid UTF-8 or a BOM in source JSON cannot be silently repaired during refresh', (t) => {
    for (const source of ['manifest', 'collection', 'history']) {
        const f = fixture(t);
        let target;
        let value;
        if (source === 'manifest') {
            target = path.join(f.bookRoot, 'manifest.json');
            value = structuredClone(f.manifest);
            value.title.pl = 'UTF8 marker';
        } else if (source === 'collection') {
            target = path.join(f.docsRoot, 'collection.json');
            value = structuredClone(f.collection);
            value.keywords.en[0].label = 'UTF8 marker';
        } else {
            target = path.join(f.bookRoot, 'editions.json');
            value = JSON.parse(prepareEditionsFile(f.bookRoot, f.manifest).content);
            value.editions[0].changes.en = 'UTF8 marker';
        }
        const valid = Buffer.from(JSON.stringify(value));
        const invalid = Buffer.from(valid);
        invalid[invalid.indexOf(Buffer.from('UTF8 marker'))] = 0xff;
        for (const content of [invalid, Buffer.concat([Buffer.from([0xef, 0xbb, 0xbf]), valid])]) {
            writeFileSync(target, content);
            assert.throws(() => refreshPages(f), undefined, source);
            assert.deepEqual(readFileSync(target), content, source);
            assert.equal(existsSync(path.join(f.bookRoot, 'en', 'book.html')), false, source);
            if (source !== 'history') {
                f.assertNoGeneratedOutputs();
            }
        }
    }
});

test('malformed history fails without repair or partial page writes', (t) => {
    const f = fixture(t);
    const valid = JSON.parse(prepareEditionsFile(f.bookRoot, f.manifest).content);
    const variants = ['{', '{}', 'null'];
    for (const mutate of [
        (history) => { history.currentEdition = 'missing'; },
        (history) => { history.bookId = 'wrong'; },
        (history) => { history.editions.push(structuredClone(history.editions[0])); },
        (history) => { history.editions[0].number = true; },
        (history) => { history.editions[0].publishedAt = '2026-02-30'; },
        (history) => { history.editions[0].pdf = []; },
        (history) => { history.editions[0].pdf = { en: '../outside.pdf' }; },
    ]) {
        const history = structuredClone(valid);
        mutate(history);
        variants.push(JSON.stringify(history));
    }
    for (const invalid of variants) {
        const target = path.join(f.bookRoot, 'editions.json');
        writeFileSync(target, invalid);
        assert.throws(() => refreshPages(f), undefined, invalid.slice(0, 80));
        assert.equal(readFileSync(target, 'utf8'), invalid);
        assert.equal(existsSync(path.join(f.bookRoot, 'en', 'book.html')), false);
    }
});

test('integer fields reject decimal and exponential JSON numbers without writing output', (t) => {
    for (const numeric of ['1.0', '1e0']) {
        const f = fixture(t);
        const target = path.join(f.bookRoot, 'editions.json');
        const valid = prepareEditionsFile(f.bookRoot, f.manifest).content;
        for (const field of ['schemaVersion', 'number']) {
            const invalid = valid.replace(new RegExp(`"${field}":\\s*1`), `"${field}": ${numeric}`);
            assert.notEqual(invalid, valid);
            writeFileSync(target, invalid);
            assert.throws(() => refreshPages(f), /Malformed existing edition history/);
            assert.equal(readFileSync(target, 'utf8'), invalid);
            assert.equal(existsSync(path.join(f.bookRoot, 'en', 'book.html')), false);
        }
        unlinkSync(target);
        const collection = path.join(f.docsRoot, 'collection.json');
        const invalid = readFileSync(collection, 'utf8').replace(/"count":\s*\d+/, `"count": ${numeric}`);
        writeFileSync(collection, invalid);
        assert.throws(() => refreshPages(f), /invalid en keywords/);
        f.assertNoGeneratedOutputs();
    }
});

test('extending history preserves unknown numeric metadata without rounding', (t) => {
    const f = fixture(t);
    const target = path.join(f.bookRoot, 'editions.json');
    const history = JSON.parse(prepareEditionsFile(f.bookRoot, f.manifest).content);
    delete history.editions[0].pdf.en;
    const original = JSON.stringify(history).replace('{', '{"largeInteger":9007199254740993123456789,"decimal":1.0000000000000001,');
    writeFileSync(target, original);
    assert.equal(ensureEditionsFile(f.bookRoot, f.manifest).changed, true);
    const extended = readFileSync(target, 'utf8');
    assert.match(extended, /"largeInteger":\s*9007199254740993123456789/);
    assert.match(extended, /"decimal":\s*1\.0000000000000001/);
    assert.equal(JSON.parse(extended).editions[0].pdf.en, f.manifest.editions.en.pdf);
});

test('an invalid final language prevents all generated writes', (t) => {
    const f = fixture(t);
    delete f.manifest.title.pl;
    f.saveManifest();
    assert.throws(() => refreshPages(f), /missing title\.pl/);
    f.assertNoGeneratedOutputs();
});

test('an invalid later book prevents writes to earlier books', (t) => {
    const f = fixture(t);
    const second = structuredClone(f.manifest);
    second.id = 'bk-second-fixture';
    const directory = `books/second/${second.id}`;
    const secondRoot = path.join(f.docsRoot, directory);
    mkdirSync(secondRoot, { recursive: true });
    for (const language of languages) {
        mkdirSync(path.join(secondRoot, language));
    }
    delete second.title.pl;
    saveJson(path.join(secondRoot, 'manifest.json'), second);
    f.collection.books.push({ id: second.id, directory });
    saveJson(path.join(f.docsRoot, 'collection.json'), f.collection);
    assert.throws(() => refreshPages(f), /missing title\.pl/);
    f.assertNoGeneratedOutputs();
    assert.equal(existsSync(path.join(secondRoot, 'editions.json')), false);
});

test('refresh rejects output symlinks, including dangling links', (t) => {
    const f = fixture(t);
    const outside = path.join(f.temp, 'outside.html');
    writeFileSync(outside, 'untouched');
    for (const [relative, target] of [
        ['en/book.html', outside], ['editions.json', outside], ['en/book.html', path.join(f.temp, 'absent.html')],
    ]) {
        const output = path.join(f.bookRoot, relative);
        symlinkSync(target, output);
        try {
            assert.throws(() => refreshPages(f), /Refusing non-file output|Unsafe relative asset path/);
            assert.equal(readFileSync(outside, 'utf8'), 'untouched');
            assert.equal(existsSync(path.join(f.bookRoot, 'fr', 'book.html')), false);
        } finally {
            unlinkSync(output);
        }
    }
    f.assertNoGeneratedOutputs();
});

test('a parent directory symlink cannot redirect generated output', (t) => {
    const f = fixture(t);
    const outside = path.join(f.temp, 'outside-language');
    mkdirSync(outside);
    rmdirSync(path.join(f.bookRoot, 'pl'));
    symlinkSync(outside, path.join(f.bookRoot, 'pl'), 'dir');
    assert.throws(() => refreshPages(f), /Unsafe relative asset path|outside book directory/);
    assert.deepEqual(readdirSync(outside), []);
    f.assertNoGeneratedOutputs();
});

test('forbidden keyword routes fail and remain untouched', (t) => {
    const f = fixture(t);
    const legacy = path.join(f.docsRoot, 'keywords');
    mkdirSync(legacy);
    writeFileSync(path.join(legacy, 'retain.html'), 'retain');
    assert.throws(() => refreshPages(f), /Legacy docs\/keywords/);
    assert.equal(readFileSync(path.join(legacy, 'retain.html'), 'utf8'), 'retain');
    f.assertNoGeneratedOutputs();
});

test('the refresh CLI dry run and argument failures do not write from another working directory', (t) => {
    const f = fixture(t);
    const run = (...arguments_) => spawnSync(process.execPath, [cli, ...arguments_], {
        encoding: 'utf8', cwd: f.temp, timeout: 30000,
    });
    const result = run('refresh', '--docs', f.docsRoot, '--dry-run');
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /8 pages, 9 changed files/);
    f.assertNoGeneratedOutputs();
    for (const arguments_ of [
        ['refresh', '--unknown'], ['check', '--dry-run'], ['build', '--docs', f.docsRoot],
    ]) {
        const invalid = run(...arguments_);
        assert.equal(invalid.status, 2, invalid.stderr);
    }
    f.assertNoGeneratedOutputs();
});

test('a copied Node tool tree resolves its bundled resources without the original working directory', (t) => {
    const f = fixture(t);
    const copyRoot = path.join(f.temp, 'copied-project');
    const sourceRoot = fileURLToPath(new URL('../', import.meta.url));
    for (const relative of ['tools', 'external']) {
        cpSync(path.join(sourceRoot, relative), path.join(copyRoot, relative), {
            recursive: true,
            filter: (source) => !source.endsWith('.py') && !source.split(path.sep).includes('__pycache__'),
        });
    }
    const copyLink = path.join(f.temp, 'copied-link');
    symlinkSync(copyRoot, copyLink, 'dir');
    const result = spawnSync(process.execPath, [
        path.join(copyLink, 'tools', 'build_books.mjs'), 'refresh', '--docs', f.docsRoot, '--dry-run',
    ], { encoding: 'utf8', cwd: tmpdir(), timeout: 30000 });
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /8 pages, 9 changed files/);
    const invalid = spawnSync(process.execPath, [path.join(copyLink, 'tools', 'check_catalogue.mjs'), '--oops'], {
        encoding: 'utf8', cwd: tmpdir(), timeout: 30000,
    });
    assert.equal(invalid.status, 2, invalid.stderr);
    f.assertNoGeneratedOutputs();
});
