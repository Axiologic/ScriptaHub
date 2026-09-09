import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseHtmlInventory } from '../tools/audit_internal_links.mjs';
import { bookPage } from '../tools/build_books.mjs';

const docs = fileURLToPath(new URL('../docs/', import.meta.url));
const collection = JSON.parse(readFileSync(path.join(docs, 'collection.json'), 'utf8'));
const languages = collection.supportedLanguages.map(({ code }) => code);
const keywordStats = Object.fromEntries(Object.entries(collection.keywords).map(([code, words]) => [
    code, Object.fromEntries(words.map(({ id, count }) => [id, { count }])),
]));

function elements(source) {
    const { tags } = parseHtmlInventory(source);
    return {
        links: tags.filter(({ tagName }) => tagName === 'a').map(({ attrs }) => attrs),
        scripts: tags.filter(({ tagName }) => tagName === 'script').map(({ attrs }) => attrs),
    };
}

function urlFor(href, page) {
    return new URL(href, pathToFileURL(page));
}

test('every published page matches generator bytes and gates only account actions', () => {
    let total = 0;
    for (const listing of collection.books) {
        const root = path.join(docs, listing.directory);
        const manifest = JSON.parse(readFileSync(path.join(root, 'manifest.json'), 'utf8'));
        const book = { ...manifest, directory: listing.directory, descriptions: manifest.shortDescription, keywordStats };
        for (const language of languages) {
            const page = path.join(root, language, 'book.html');
            const edition = manifest.editions[language];
            const generated = bookPage(book, language, page, 'fullContent' in edition || 'shortContent' in edition);
            assert.deepEqual(Buffer.from(generated), readFileSync(page), `${listing.id} ${language}: generated page changed`);
            const { links, scripts } = elements(generated);
            const gated = links.filter((link) => Object.hasOwn(link, 'data-auth-action'));
            assert.equal(gated.length, 1 + Number('pdf' in edition), page);
            for (const link of links) {
                const target = urlFor(link.href, page).pathname;
                const expected = target.endsWith('.pdf') ? 'download'
                    : target.endsWith('/feedback/index.html') ? 'feedback' : undefined;
                assert.equal(link['data-auth-action'], expected, `${page}: ${target}`);
            }
            const auth = scripts.filter((script) => script.src?.includes('/auth.js'));
            assert.equal(auth.length, 1, page);
            assert.ok(Object.hasOwn(auth[0], 'defer'), page);
            assert.equal(fileURLToPath(urlFor(auth[0].src, page)), path.join(docs, 'assets', 'auth.js'), page);
            total++;
        }
    }
    assert.equal(total, collection.bookCount * 8);
});

test('shared pages load authentication before their deferred interaction scripts', () => {
    for (const [relative, consumer] of [
        ['feedback/index.html', 'workflow.js'], ['editions/index.html', 'workflow.js'], ['reader/index.html', 'reader.js'],
    ]) {
        const { scripts } = elements(readFileSync(path.join(docs, relative), 'utf8'));
        const authIndex = scripts.findIndex((script) => script.src?.includes('/auth.js'));
        const consumerIndex = scripts.findIndex((script) => script.src?.includes(consumer));
        assert.ok(authIndex >= 0 && consumerIndex > authIndex, relative);
        assert.ok(Object.hasOwn(scripts[authIndex], 'defer'), relative);
        assert.ok(Object.hasOwn(scripts[consumerIndex], 'defer'), relative);
    }
});

test('canonical readers with PDF buttons load the shared runtime', () => {
    const files = readdirSync(path.join(docs, 'books'), { recursive: true });
    let checked = 0;
    for (const relative of files.filter((file) => /^(?:full|short)_content\.html$/.test(path.basename(file)))) {
        const page = path.join(docs, 'books', relative);
        const { links, scripts } = elements(readFileSync(page, 'utf8'));
        const pdfs = links.map((link) => {
            try {
                return new URL(link.href ?? '', 'https://scriptahub.com/');
            } catch {
                return null;
            }
        });
        if (pdfs.some((url) => url?.origin === 'https://scriptahub.com' && url.pathname.toLowerCase().endsWith('.pdf'))) {
            assert.ok(scripts.some((script) => /\/(standalone|auth)\.js$/.test(urlFor(script.src ?? '', page).pathname)), page);
            checked++;
        }
    }
    assert.ok(checked > 0, 'Canonical reader PDF coverage must not disappear');
});
