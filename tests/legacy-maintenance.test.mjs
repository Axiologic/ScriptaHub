import assert from 'node:assert/strict';
import { copyFile, mkdir, mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { createBookTools, LANGUAGES } from '../tools/build_books.mjs';
import { createMaintenanceTools, exists, json, saveJson } from '../tools/lib/book-maintenance.mjs';
import { buildLegacy, recoverEditorialDescriptions, recoverLeftovers } from '../tools/lib/book-legacy.mjs';

const codes = Object.keys(LANGUAGES);

async function put(filename, content) {
    await mkdir(path.dirname(filename), { recursive: true });
    await writeFile(filename, content);
}

async function snapshot(directory) {
    const entries = [];
    const visit = async (root) => {
        for (const entry of (await readdir(root, { withFileTypes: true })).sort((first, second) => first.name.localeCompare(second.name))) {
            const filename = path.join(root, entry.name);
            entries.push([path.relative(directory, filename), entry.isDirectory() ? null : await readFile(filename)]);
            if (entry.isDirectory()) await visit(filename);
        }
    };
    await visit(directory);
    return entries;
}

async function fixture(t) {
    const temp = await mkdtemp(path.join(tmpdir(), 'scripta-legacy-'));
    t.after(() => rm(temp, { recursive: true, force: true }));
    const docs = path.join(temp, 'docs');
    const sourceRoot = path.join(temp, 'old_content');
    await mkdir(docs);
    const context = await createMaintenanceTools({ docsRoot: docs, tools: createBookTools({ docs }), sourceRoot });
    return { temp, docs, sourceRoot, context };
}

async function sourceBook(f) {
    const content = path.join(f.sourceRoot, 'content');
    await put(path.join(content, 'index.json'), JSON.stringify({ books: [{
        id: 'Original_Book', slug: 'original-book', editions: [{
            language: 'EN', pdf: 'EN/Original.pdf', html: 'htmls/EN/Original.html', tenMinuteHtml: '10minutes/Original.html',
        }],
    }] }));
    await put(path.join(f.sourceRoot, 'books/original-book/index.html'), `<html><h1>A Migrated Book</h1>
<p class="eyebrow edition-kicker">Research · Axiologic Research Editions</p>
<p class="edition-why">An editorial &amp; original description.</p>
<img class="edition-cover" src="../../covers/Original%20Cover.png"></html>`);
    await put(path.join(content, 'EN/Original.pdf'), '%PDF-original');
    const reader = '<html lang="EN"><head><script src="../../reader/standalone.js"></script></head><body><main><p>Source text for discovery.</p><img src="Original.assets/figure.png"><a href="../../EN/Original.pdf">PDF</a></main></body></html>';
    await put(path.join(content, 'htmls/EN/Original.html'), reader);
    await put(path.join(content, '10minutes/Original.html'), reader.replace('Source text', 'Short source text'));
    await put(path.join(content, 'htmls/EN/Original.assets/figure.png'), 'original figure');
    await put(path.join(content, 'covers/Original Cover.png'), 'original cover');
    await put(path.join(content, 'thumbnails/Original Cover.webp'), 'original thumbnail');
    return content;
}

test('legacy import preserves source assets, title routes, and all localized manifest records', async (t) => {
    const f = await fixture(t);
    const content = await sourceBook(f);
    const operations = [];
    f.context.keywordWorker = async (payload) => {
        operations.push(payload.operation);
        if (payload.operation === 'check') {
            assert.equal(payload.translation, true);
            assert.equal(payload.requireModels, true);
            assert.equal(await exists(f.context.books), false);
            return {};
        }
        assert.equal(await exists(f.context.books), false, 'extract before moving source files');
        assert.match(payload.records[0].sourceText, /Short source text/);
        assert.equal(payload.records[0].limit, 140);
        return [Array.from({ length: 100 }, (_, index) => `discovery phrase ${index}`)];
    };
    f.context.convertImage = async (source, destination) => copyFile(source, destination);
    let keywordRebuilds = 0;
    f.context.rebuildKeywords = async () => {
        keywordRebuilds++;
        await f.context.rebuild();
    };
    const result = await buildLegacy(f.context);
    assert.deepEqual(result, { books: 1, moved: 6, keywords: 800 });
    assert.deepEqual(operations, ['check', 'extract']);
    assert.equal(keywordRebuilds, 1);
    const collection = await json(path.join(f.docs, 'collection.json'));
    const listing = collection.books[0];
    assert.match(listing.directory, /^books\/a\/migrated\/book\/bk-[a-f0-9]{16}$/);
    const root = path.join(f.docs, listing.directory);
    const manifest = await json(path.join(root, 'manifest.json'));
    assert.equal(manifest.sourceId, 'Original_Book');
    assert.equal(manifest.subtitle.en, 'Axiologic Research Edition');
    assert.equal(manifest.group, 'science');
    assert.deepEqual(manifest.availableLanguages, ['English']);
    assert.equal(manifest.keywordIds.length, 100);
    for (const language of codes) {
        assert.equal(manifest.keywords[language].length, 100, language);
        assert.equal(await readFile(path.join(root, language, 'cover.png'), 'utf8'), 'original cover');
        assert.equal(await readFile(path.join(root, language, 'cover.webp'), 'utf8'), 'original cover');
        assert.ok(await exists(path.join(root, language, 'book.html')));
    }
    assert.equal(await readFile(path.join(root, 'en/book.pdf'), 'utf8'), '%PDF-original');
    assert.equal(await readFile(path.join(root, 'en/Original.assets/figure.png'), 'utf8'), 'original figure');
    const reader = await readFile(path.join(root, 'en/full_content.html'), 'utf8');
    assert.match(reader, /<html lang="en">/);
    assert.match(reader, /href="book\.pdf"/);
    assert.match(reader, /src="Original\.assets\/figure\.png"/);
    assert.equal(await exists(path.join(content, 'EN/Original.pdf')), false);
    assert.equal(await exists(path.join(content, 'covers/Original Cover.png')), false);
    assert.equal((await json(path.join(root, 'editions.json'))).bookId, manifest.id);
    assert.deepEqual(f.context.tools.check(), []);
});

test('missing optional keyword prerequisites fail before legacy import creates outputs', async (t) => {
    const f = await fixture(t);
    const content = await sourceBook(f);
    f.context.keywordWorker = async () => { throw new Error('optional keyword prerequisite unavailable'); };
    f.context.convertImage = async () => { assert.fail('conversion must not run'); };
    await assert.rejects(buildLegacy(f.context), /optional keyword prerequisite unavailable/);
    assert.equal(await exists(f.context.books), false);
    assert.deepEqual(await readdir(f.docs), []);
    assert.equal(await readFile(path.join(content, 'EN/Original.pdf'), 'utf8'), '%PDF-original');
});

test('insufficient source keywords fail before any legacy source is moved', async (t) => {
    const f = await fixture(t);
    const content = await sourceBook(f);
    f.context.keywordWorker = async (payload) => payload.operation === 'check' ? {} : [['one discovery phrase']];
    f.context.convertImage = async () => { assert.fail('conversion must not run'); };
    await assert.rejects(buildLegacy(f.context), /only 1 source-derived keywords/);
    assert.equal(await exists(f.context.books), false);
    assert.equal(await readFile(path.join(content, 'EN/Original.pdf'), 'utf8'), '%PDF-original');
    assert.equal(await readFile(path.join(content, 'covers/Original Cover.png'), 'utf8'), 'original cover');
});

for (const variant of ['legacy metadata', 'selected English keyword source', 'a later Polish reader']) {
    test(`invalid UTF-8 in ${variant} leaves all source files and documentation unchanged`, async (t) => {
        const f = await fixture(t);
        const content = await sourceBook(f);
        let filename;
        if (variant === 'legacy metadata') {
            filename = path.join(f.sourceRoot, 'books/original-book/index.html');
        } else if (variant === 'selected English keyword source') {
            filename = path.join(content, '10minutes/Original.html');
        } else {
            filename = path.join(content, 'htmls/PL/Original_PL.html');
            await put(filename, '<html lang="pl"><p>Polski tekst.</p></html>');
            const index = await json(path.join(content, 'index.json'));
            index.books[0].editions.push({ language: 'PL', html: 'htmls/PL/Original_PL.html' });
            await saveJson(path.join(content, 'index.json'), index);
        }
        await writeFile(filename, Buffer.concat([await readFile(filename), Buffer.from([0xff, 0xfe])]));
        const before = await snapshot(f.temp);
        f.context.keywordWorker = async (payload) => {
            assert.equal(payload.operation, 'check', 'malformed input must fail before keyword extraction');
            return {};
        };
        f.context.convertImage = async () => { assert.fail('malformed input must fail before cover conversion'); };
        await assert.rejects(buildLegacy(f.context), /not valid for encoding utf-8/i);
        assert.deepEqual(await snapshot(f.temp), before);
        assert.equal(await exists(f.context.books), false);
    });
}

test('legacy recovery restores indexed editions, keeps current alternatives, and leaves unknown drafts unpublished', async (t) => {
    const f = await fixture(t);
    const sourceIds = [
        'The_Thousand_Handed_Devil', 'The_Schizoid_and_the_Oracle', 'EXPLAINABLE_AI',
        'The_Fragmented_Future', 'FUTURE_RESEARCH_INFRASTRUCTURE', 'Outfinitism_Meta_Rationality',
    ];
    const roots = new Map();
    const listings = [];
    for (const [index, sourceId] of sourceIds.entries()) {
        const directory = `books/fixture/bk-${index}`;
        const root = path.join(f.docs, directory);
        roots.set(sourceId, root);
        listings.push({ sourceId, directory });
        for (const language of codes) await mkdir(path.join(root, language), { recursive: true });
        await saveJson(path.join(root, 'manifest.json'), {
            sourceId, custom: { retained: true }, editions: Object.fromEntries(codes.map((code) => [code, {}])), availableLanguages: [],
        });
    }
    await saveJson(path.join(f.docs, 'collection.json'), { books: listings });
    const content = path.join(f.sourceRoot, 'content');
    for (const relative of [
        'htmls/ES/The_Thousand_Handed_Devil_ES.html', '10minutes/The_Schizoid_and_the_Oracle.html',
        '10minutes/PL/EXPLAINABLE_PL.html', 'htmls/FR/The_Fragmented_Future_FR(1).html',
        '10minutes/ES/EXPLAINABLE_ES.html', '10minutes/IT/EXPLAINABLE_IT.html',
        'EN/The_Future_of_Research_Infrastructure.pdf', 'covers/The_Schizoid_and_the_Oracle_RO.png',
        'thumbnails/The_Schizoid_and_the_Oracle_RO.webp', 'covers/Outfinitism_Third_Edition.png',
        'thumbnails/Outfinitism_Third_Edition.webp',
    ]) {
        await put(path.join(content, relative), relative.endsWith('.html') ? '<html><p>Recovered reader</p></html>' : relative);
    }
    await put(path.join(content, 'htmls/ES/The_Thousand_Handed_Devil_ES.assets/figure.png'), 'figure');
    const draft = path.join(content, 'htmls/RO/Unknown_Draft.html');
    await put(draft, 'unpublished draft');
    const current = path.join(roots.get('The_Fragmented_Future'), 'fr/full_content.html');
    await put(current, 'reviewed current reader');
    await put(path.join(roots.get('The_Schizoid_and_the_Oracle'), 'ro/cover.png'), 'old Romanian cover');
    let rebuilt = 0;
    f.context.rebuild = async () => { rebuilt++; };
    assert.equal(await recoverLeftovers(f.context), 12);
    assert.equal(rebuilt, 1);
    assert.equal(await readFile(current, 'utf8'), 'reviewed current reader');
    assert.match(await readFile(path.join(roots.get('The_Fragmented_Future'), 'fr/full_content.previous.html'), 'utf8'), /Recovered reader/);
    assert.equal(await readFile(draft, 'utf8'), 'unpublished draft');
    assert.equal(await readFile(path.join(roots.get('The_Thousand_Handed_Devil'), 'es/The_Thousand_Handed_Devil_ES.assets/figure.png'), 'utf8'), 'figure');
    const recovered = await json(path.join(roots.get('The_Thousand_Handed_Devil'), 'manifest.json'));
    assert.equal(recovered.editions.es.fullContent, 'es/full_content.html');
    assert.deepEqual(recovered.availableLanguages, ['Español']);
    assert.deepEqual(recovered.custom, { retained: true });
    assert.equal(await readFile(path.join(roots.get('The_Schizoid_and_the_Oracle'), 'ro/cover.png'), 'utf8'), 'covers/The_Schizoid_and_the_Oracle_RO.png');
    assert.ok(await exists(path.join(roots.get('FUTURE_RESEARCH_INFRASTRUCTURE'), 'en/book.previous-edition.pdf')));
    assert.equal(await recoverLeftovers(f.context), 0, 'a repeated recovery keeps existing destinations');
});

test('editorial recovery uses aliases and fallbacks, preserves other metadata, and reports missing descriptions', async (t) => {
    const f = await fixture(t);
    const records = [
        { sourceId: 'OpenDSU_Essential_Philosophy', title: 'OpenDSU Essential Philosophy', previous: 'Before' },
        { sourceId: 'Fallback_ID', title: 'A Better Title', previous: 'Same recovered description' },
        { sourceId: 'Unavailable_Book', title: 'Unavailable Book', previous: 'Keep this description' },
    ];
    for (const [index, record] of records.entries()) {
        await put(path.join(f.context.books, String(index), 'manifest.json'), JSON.stringify({
            sourceId: record.sourceId, title: { en: record.title },
            shortDescription: { en: record.previous, fr: 'Conserver' }, custom: { retain: true },
        }));
    }
    const requests = [];
    const waits = [];
    let rebuilt = 0;
    f.context.rebuild = async () => { rebuilt++; };
    const result = await recoverEditorialDescriptions(f.context, {
        pause: async (milliseconds) => { waits.push(milliseconds); },
        fetchPage: async (url, options) => {
            requests.push(url);
            assert.equal(options.headers['User-Agent'], 'ScriptaHub catalogue migration/1.0 (+https://www.axiologic.net)');
            assert.ok(options.signal instanceof AbortSignal);
            if (url.endsWith('/opendsu/')) return new Response('<p class="edition-why">Recovered <b>editorial</b> &amp; source.</p>');
            if (url.endsWith('/a-better-title/')) throw new Error('fixture transport failure');
            if (url.endsWith('/fallback-id/')) return new Response('<p class="edition-why">Same recovered description</p>');
            return new Response('Missing', { status: 404 });
        },
    });
    assert.deepEqual(result, { recovered: 1, missing: ['Unavailable_Book'] });
    assert.deepEqual(requests, [
        'https://www.axiologic.net/books/opendsu/', 'https://www.axiologic.net/books/a-better-title/',
        'https://www.axiologic.net/books/fallback-id/', 'https://www.axiologic.net/books/unavailable-book/',
    ]);
    assert.deepEqual(waits, [80, 80, 80]);
    assert.equal(rebuilt, 1);
    const recovered = await json(path.join(f.context.books, '0', 'manifest.json'));
    assert.deepEqual(recovered.shortDescription, { en: 'Recovered editorial & source.', fr: 'Conserver' });
    assert.deepEqual(recovered.custom, { retain: true });
    assert.equal((await json(path.join(f.context.books, '2', 'manifest.json'))).shortDescription.en, 'Keep this description');
});
