import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdir, mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { createBookTools, keywordIdentifier, LANGUAGES } from '../tools/build_books.mjs';
import { createMaintenanceTools, imageConverter, runKeywordWorker } from '../tools/lib/book-maintenance.mjs';
import { assertNodeVersion, runProcess } from '../tools/lib/runtime.mjs';

const codes = Object.keys(LANGUAGES);
const cli = fileURLToPath(new URL('../tools/build_books.mjs', import.meta.url));
const vocabulary = JSON.parse(await readFile(new URL('../tools/keywords/vocabulary.json', import.meta.url), 'utf8'));
const localize = (value) => Object.fromEntries(codes.map((code) => [code, typeof value === 'function' ? value(code) : value]));
const json = async (filename) => JSON.parse(await readFile(filename, 'utf8'));

async function put(filename, contents) {
    await mkdir(path.dirname(filename), { recursive: true });
    await writeFile(filename, contents);
}

async function save(filename, value) {
    await put(filename, JSON.stringify(value, null, 4) + '\n');
}

async function fingerprint(folder) {
    const records = [];
    async function visit(directory) {
        for (const entry of await readdir(directory, { withFileTypes: true })) {
            const filename = path.join(directory, entry.name);
            if (entry.isDirectory()) {
                await visit(filename);
            } else if (entry.isFile()) {
                records.push([path.relative(folder, filename), createHash('sha256').update(await readFile(filename)).digest('hex')]);
            }
        }
    }
    await visit(folder);
    return records.sort(([left], [right]) => left.localeCompare(right));
}

async function fixture(t) {
    const temp = await mkdtemp(path.join(tmpdir(), 'scripta-maintenance-'));
    t.after(() => rm(temp, { recursive: true, force: true }));
    const docs = path.join(temp, 'docs');
    const directory = 'books/a/fixture/book/bk-0123456789abcdef';
    const root = path.join(docs, directory);
    const manifestPath = path.join(root, 'manifest.json');
    const manifest = {
        id: 'bk-0123456789abcdef', sourceId: 'Fixture_Book', route: ['a', 'fixture', 'book'],
        category: 'Technology', group: 'technology', availableLanguages: ['English'],
        title: localize('A Fixture Book'), subtitle: localize('Original subtitle'),
        shortDescription: localize('Original description'),
        keywordIds: Array.from({ length: 100 }, (_, index) => `subject:${index}`),
        keywords: localize(() => Array.from({ length: 100 }, (_, index) => `Subject ${index}`)),
        coverUrl: localize((code) => `${code}/cover.webp`),
        thumbnailUrl: localize((code) => `${code}/thumbnail.webp`),
        editions: localize((code) => ({
            book: `${code}/book.html`, cover: `${code}/cover.webp`,
            sourceCover: `${code}/cover.png`, thumbnail: `${code}/thumbnail.webp`,
        })),
        custom: { retained: ['original'] },
    };
    for (const code of codes) {
        for (const basename of ['cover.png', 'cover.webp', 'thumbnail.webp']) {
            await put(path.join(root, code, basename), `${code} ${basename} untouched`);
        }
    }
    manifest.editions.en.fullContent = 'en/full_content.html';
    manifest.editions.en.shortContent = 'en/short_content.html';
    manifest.editions.en.pdf = 'en/book.pdf';
    await put(path.join(root, 'en/full_content.html'), '<main><h1>Full edition</h1><p>Full original reader.</p></main>');
    await put(path.join(root, 'en/short_content.html'), '<main><h1>Specific source concept</h1><p>Original short reader.</p></main>');
    await put(path.join(root, 'en/book.pdf'), '%PDF-original');
    await save(manifestPath, manifest);
    const tools = createBookTools({ docs });
    await tools.rebuildCollectionFromManifests();
    await tools.refreshPages();
    assert.deepEqual(tools.check(), []);
    const cachePath = path.join(temp, 'keyword-cache.json');
    const context = (options = {}) => createMaintenanceTools({ docsRoot: docs, tools, cachePath, ...options });
    return { temp, docs, root, manifestPath, manifest, tools, context, cachePath };
}

test('enrichment chooses the short reader, falls back to full content, and preserves source assets', async (t) => {
    const f = await fixture(t);
    const english = 'This short edition explains how concrete evidence changes a technical decision and gives readers enough detail to check the reasoning themselves.';
    const french = 'Cette édition présente une méthode précise pour examiner les résultats et comprendre comment les observations modifient les conclusions proposées.';
    const copyright = 'Copyright publishing rights. '.repeat(8);
    await put(path.join(f.root, 'en/short_content.html'), `<p>${copyright}</p><p>${english}</p>`);
    await put(path.join(f.root, 'en/full_content.html'), `<p>${'This full edition should not replace the short edition description. '.repeat(4)}</p>`);
    await put(path.join(f.root, 'fr/full_content.html'), `<p>${french}</p>`);
    f.manifest.editions.fr.fullContent = 'fr/full_content.html';
    await save(f.manifestPath, f.manifest);
    const originalReader = await readFile(path.join(f.root, 'en/full_content.html'));
    const context = await f.context();
    assert.equal(await context.enrich(), 2);
    const result = await json(f.manifestPath);
    assert.equal(result.shortDescription.en, english);
    assert.equal(result.shortDescription.fr, french);
    assert.equal(result.shortDescription.de, 'Original description');
    assert.deepEqual(result.custom, f.manifest.custom);
    assert.deepEqual(await readFile(path.join(f.root, 'en/full_content.html')), originalReader);
    assert.equal(await readFile(path.join(f.root, 'en/book.pdf'), 'utf8'), '%PDF-original');
    assert.equal((await json(path.join(f.docs, 'collection.json'))).books[0].shortDescription.en, english);
    assert.ok((await readFile(path.join(f.root, 'en/book.html'), 'utf8')).includes(english));
    assert.equal(await context.enrich(), 0);
    assert.deepEqual(f.tools.check(), []);
});

test('rebranding updates nested metadata and reader links while preserving unrelated words and files', async (t) => {
    const f = await fixture(t);
    f.manifest.subtitle.en = 'Axiologic Research';
    f.manifest.custom = { retained: ['Recherche Axiologique', { label: 'Achilles and Achillesian' }] };
    await save(f.manifestPath, f.manifest);
    await put(path.join(f.root, 'en/full_content.html'), '<a href="http://www.axiologic.net/books">Axiologic Research</a><p>Achille Aquiles Achillesian www.axiologic.net</p>');
    const context = await f.context();
    assert.ok(await context.rebrand() >= 2);
    const result = await json(f.manifestPath);
    assert.equal(result.subtitle.en, 'ScriptaHub');
    assert.deepEqual(result.custom, { retained: ['ScriptaHub', { label: 'ScriptaHub and Achillesian' }] });
    assert.equal(await readFile(path.join(f.root, 'en/full_content.html'), 'utf8'), '<a href="https://ScriptaHub.com/books">ScriptaHub</a><p>ScriptaHub ScriptaHub Achillesian ScriptaHub.com</p>');
    assert.equal(await readFile(path.join(f.root, 'en/book.pdf'), 'utf8'), '%PDF-original');
    assert.equal((await json(path.join(f.docs, 'collection.json'))).books[0].subtitle.en, 'ScriptaHub');
    assert.equal(await context.rebrand(), 0);
});

test('reader repair uses existing local editions and preferred-language assets without touching unrelated archives', async (t) => {
    const f = await fixture(t);
    const source = '<a href="../../content/htmls/EN/Old.html">Read</a><img src="../../htmls/FR/Old.assets/figure.png"><img src="../../htmls/FR/Old.assets/missing.png">';
    await put(path.join(f.root, 'en/short_content.html'), source);
    await put(path.join(f.root, 'en/full_content.previous.html'), source);
    await put(path.join(f.root, 'en/archived_full_content.html'), source);
    await put(path.join(f.root, 'en/assets/figure.png'), 'English figure');
    await put(path.join(f.root, 'fr/assets/figure.png'), 'French figure');
    await put(path.join(f.root, 'fr/short_content.html'), '<a href="../../content/htmls/FR/Old.html">Read</a>');
    const context = await f.context();
    assert.equal(await context.repairReaderLinks(), 3);
    const repaired = await readFile(path.join(f.root, 'en/short_content.html'), 'utf8');
    assert.match(repaired, /href="full_content\.html"/);
    assert.match(repaired, /src="\.\.\/fr\/assets\/figure\.png"/);
    assert.match(repaired, /Old\.assets\/missing\.png/);
    assert.equal(await readFile(path.join(f.root, 'en/full_content.previous.html'), 'utf8'), repaired);
    assert.equal(await readFile(path.join(f.root, 'en/archived_full_content.html'), 'utf8'), source);
    assert.equal(await readFile(path.join(f.root, 'fr/short_content.html'), 'utf8'), '<a href="book.html">Read</a>');
    assert.equal(await context.repairReaderLinks(), 0);
});

test('keyword rebuilding keeps ten shelf terms and ninety distinct localized source phrases with an isolated cache', async (t) => {
    const f = await fixture(t);
    const seedCache = { schemaVersion: 1, translations: { fr: { retained: 'Conserver' } } };
    await save(f.cachePath, seedCache);
    const phrases = Array.from({ length: 92 }, (_, index) => `specific source phrase ${index}`);
    const shelf = vocabulary.shelves.technology.en.split('|')[0];
    const operations = [];
    const worker = async (payload) => {
        operations.push(payload.operation);
        if (payload.operation === 'check') {
            assert.equal(payload.translation, true);
            return { ready: true };
        }
        if (payload.operation === 'extract') {
            assert.equal(payload.records.length, 1);
            assert.equal(payload.records[0].limit, 120);
            assert.match(payload.records[0].sourceText, /Specific source concept/);
            assert.doesNotMatch(payload.records[0].sourceText, /Full original reader/);
            return [[shelf, ...phrases]];
        }
        assert.equal(payload.operation, 'translate');
        assert.deepEqual(payload.phrases, phrases);
        if (operations.filter((operation) => operation === 'translate').length === 1) {
            assert.deepEqual(payload.cache, seedCache);
        }
        return localize((code) => Object.fromEntries(phrases.map((phrase, index) => [
            phrase, code === 'en' ? phrase : `${code} translated concept ${code === 'fr' && index === 1 ? 0 : index}`,
        ])));
    };
    const context = await f.context({ keywordWorker: worker });
    assert.equal(await context.rebuildKeywords(), 1);
    const result = await json(f.manifestPath);
    assert.equal(result.group, 'technology');
    assert.equal(result.keywordIds.length, 100);
    assert.deepEqual(result.keywordIds.slice(0, 10), vocabulary.shelves.technology.en.split('|').map(keywordIdentifier));
    assert.equal(result.keywordIds.includes(keywordIdentifier(phrases[1])), false, 'skip a phrase duplicated in one translation');
    assert.equal(result.keywordIds.at(-1), keywordIdentifier(phrases[90]));
    for (const code of codes) {
        assert.equal(result.keywords[code].length, 100, code);
        assert.equal(new Set(result.keywords[code]).size, 100, code);
    }
    const cached = await json(f.cachePath);
    assert.deepEqual(Object.keys(cached.translations), codes.filter((code) => code !== 'en'));
    assert.equal(cached.translations.fr[phrases[0]], 'fr translated concept 0');
    assert.deepEqual(result.custom, f.manifest.custom);
    assert.deepEqual(operations, ['check', 'extract', 'translate']);
    assert.deepEqual(f.tools.check(), []);
    assert.equal(await context.rebuildKeywords(), 0, 'repeating identical translations is idempotent');
});

test('insufficient keyword extraction and translation collisions fail before writing cache or metadata', async (t) => {
    for (const failure of ['extraction', 'translations']) {
        const f = await fixture(t);
        await save(f.cachePath, { schemaVersion: 1, translations: {} });
        const before = await fingerprint(f.temp);
        const phrases = Array.from({ length: 90 }, (_, index) => `distinct source phrase ${index}`);
        const worker = async (payload) => {
            if (payload.operation === 'check') {
                return {};
            }
            if (payload.operation === 'extract') {
                return [failure === 'extraction' ? phrases.slice(0, 89) : phrases];
            }
            assert.equal(failure, 'translations', 'do not translate after extraction failed');
            return localize((code) => Object.fromEntries(phrases.map((phrase) => [phrase, code === 'fr' ? 'same translation' : phrase])));
        };
        const context = await f.context({ keywordWorker: worker });
        await assert.rejects(context.rebuildKeywords(), failure === 'extraction' ? /only 89 source-derived keywords/ : /only 11 distinct translated keywords/);
        assert.deepEqual(await fingerprint(f.temp), before, failure);
    }
});

test('missing Python gives an actionable keyword error before changing catalogue files', async (t) => {
    const f = await fixture(t);
    const env = { ...process.env, PATH: '', SCRIPTAHUB_KEYWORD_PYTHON: path.join(f.temp, 'missing-python') };
    const before = await fingerprint(f.temp);
    const context = await f.context({ keywordWorker: (payload) => runKeywordWorker(payload, { env }) });
    await assert.rejects(context.rebuildKeywords(), (error) => {
        assert.match(error.message, /requires Python 3\.10\+/);
        assert.match(error.message, /SCRIPTAHUB_KEYWORD_PYTHON/);
        assert.match(error.message, /dependencies\.md/);
        return true;
    });
    assert.deepEqual(await fingerprint(f.temp), before);
});

test('missing ImageMagick fails cover generation before changing covers or metadata', async (t) => {
    const f = await fixture(t);
    const before = await fingerprint(f.temp);
    await assert.rejects(imageConverter({ env: { ...process.env, PATH: '' } }), /ImageMagick 6 or 7 with WebP write support.*dependencies\.md/);
    const previousPath = process.env.PATH;
    process.env.PATH = '';
    try {
        const context = await f.context();
        await assert.rejects(context.refreshCovers(), /ImageMagick.*no catalogue files were changed/);
    } finally {
        if (previousPath === undefined) {
            delete process.env.PATH;
        } else {
            process.env.PATH = previousPath;
        }
    }
    assert.deepEqual(await fingerprint(f.temp), before);
});

test('refresh and check work from another directory with Python and image tools unavailable', async (t) => {
    const f = await fixture(t);
    f.manifest.subtitle.en = 'Updated without optional tools';
    await save(f.manifestPath, f.manifest);
    const env = { ...process.env, PATH: '', SCRIPTAHUB_KEYWORD_PYTHON: path.join(f.temp, 'missing-python') };
    for (const command of ['refresh', 'check']) {
        const result = spawnSync(process.execPath, [cli, command, '--docs', f.docs], {
            cwd: f.temp, env, encoding: 'utf8', timeout: 30000,
        });
        assert.equal(result.status, 0, `${command}: ${result.stderr}`);
        assert.notEqual(result.stdout.trim(), '', `${command} must execute its CLI body`);
    }
    assert.match(await readFile(path.join(f.root, 'en/book.html'), 'utf8'), /Updated without optional tools/);
});

test('runtime prerequisites reject unsupported and malformed Node versions with installation guidance', () => {
    for (const version of ['22.12.0', '22.19.0', '24.0.0']) {
        assert.doesNotThrow(() => assertNodeVersion(version, 'Fixture command'));
    }
    for (const version of ['20.19.0', '22.11.0', '22.invalid', '22', 'invalid']) {
        assert.throws(() => assertNodeVersion(version, 'Fixture command'), /Fixture command requires Node\.js 22\.12 or newer.*dependencies\.md/);
    }
});

test('process execution preserves literal arguments, stdin, stderr, and exit status', async () => {
    const literal = '$(touch unwanted-file); spaces and `backticks`';
    const result = await runProcess(process.execPath, ['-e', "process.stdin.setEncoding('utf8');let input='';process.stdin.on('data',value=>input+=value);process.stdin.on('end',()=>{process.stdout.write(JSON.stringify({argument:process.argv[1],input}));process.stderr.write('diagnostic');process.exitCode=7;});", literal], {
        input: 'input with\nnewlines', timeout: 5000,
    });
    assert.equal(result.code, 7);
    assert.equal(result.stderr, 'diagnostic');
    assert.deepEqual(JSON.parse(result.stdout), { argument: literal, input: 'input with\nnewlines' });
    await assert.rejects(runProcess('scriptahub-command-that-does-not-exist', [], { env: { PATH: '' } }), { code: 'ENOENT' });
    await assert.rejects(runProcess(process.execPath, ['-e', "process.stdout.write('x'.repeat(8192))"], { maxBytes: 64, timeout: 5000 }), /output limit/);
});

test('a command deadline is enforced even when a descendant retains inherited output pipes', async (t) => {
    const temp = await mkdtemp(path.join(tmpdir(), 'scripta-deadline-'));
    const pidFile = path.join(temp, 'descendant.pid');
    t.after(async () => {
        try {
            const pid = Number(await readFile(pidFile, 'utf8'));
            if (Number.isInteger(pid) && pid > 1) {
                try {
                    process.kill(pid, 'SIGKILL');
                } catch (error) {
                    if (error.code !== 'ESRCH') {
                        throw error;
                    }
                }
            }
        } catch (error) {
            if (error.code !== 'ENOENT') {
                throw error;
            }
        } finally {
            await rm(temp, { recursive: true, force: true });
        }
    });
    const script = "const child=require('node:child_process').spawn(process.execPath,['-e','setTimeout(()=>{},10000)'],{stdio:'inherit'});require('node:fs').writeFileSync(process.argv[1],String(child.pid));setTimeout(()=>{},10000);";
    const started = performance.now();
    await assert.rejects(runProcess(process.execPath, ['-e', script, pidFile], { timeout: 800 }), /800 ms time limit/);
    assert.match(await readFile(pidFile, 'utf8'), /^\d+$/, 'the descendant must actually start');
    assert.ok(performance.now() - started < 3000, 'do not wait for the descendant to close inherited pipes');
});
