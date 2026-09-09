#!/usr/bin/env node
/** Validate catalogue metadata and local assets without changing files. */
import path from 'node:path';
import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import {
    contained, isFile, isObject, keywordNormalise, manifestsUnder, pathExists,
    readJson, readUtf8, relativeAsset, resolveAssetPath, slugify, titleRoute,
} from './build_books.mjs';
import { assertNodeVersion } from './lib/runtime.mjs';

export { keywordNormalise, slugify };
export const LANGUAGES = ['en', 'fr', 'de', 'es', 'pt', 'it', 'ro', 'pl'];
export const DEFAULT_DOCS = fileURLToPath(new URL('../docs/', import.meta.url));
const mapping = value => isObject(value) ? value : {};
const sameSet = (first, second) => first.size === second.size && [...first].every(value => second.has(value));
const sameArray = (first, second) => Array.isArray(first) && first.length === second.length && first.every((value, index) => value === second[index]);

export function localFile(root, value) {
    try {
        return isFile(relativeAsset(value, root));
    } catch {
        return false;
    }
}

/** Return actionable validation failures rather than throwing for malformed records. */
export function checkCatalogue(docs = DEFAULT_DOCS) {
    docs = path.resolve(docs);
    const problems = [];
    const collectionFile = path.join(docs, 'collection.json');
    if (!isFile(collectionFile)) return ['missing docs/collection.json'];
    let collection;
    try {
        collection = readJson(collectionFile);
    } catch {
        return ['invalid docs/collection.json'];
    }
    if (!isObject(collection) || !Array.isArray(collection.books)) return ['collection books must be an array'];
    const books = collection.books;
    if (collection.bookCount !== books.length) problems.push('collection bookCount does not match books');
    const counts = new Map();
    for (const entry of books) {
        const book = mapping(entry);
        if (!Array.isArray(book.keywordIds) || book.keywordIds.some(value => typeof value !== 'string')) {
            problems.push(`${book.id ?? '(no ID)'}: malformed collection keyword IDs`);
            continue;
        }
        for (const id of book.keywordIds) counts.set(id, (counts.get(id) ?? 0) + 1);
    }
    const keywordSets = {};
    for (const language of LANGUAGES) {
        const entries = mapping(collection.keywords)[language];
        if (!Array.isArray(entries)) {
            problems.push(`${language}: missing collection keywords`);
            keywordSets[language] = new Set();
            continue;
        }
        const identifiers = [];
        for (const entry of entries) {
            if (!isObject(entry) || typeof entry.id !== 'string' || !entry.id) {
                problems.push(`${language}: malformed collection keyword entry`);
                continue;
            }
            identifiers.push(entry.id);
            if (!Number.isSafeInteger(entry.count) || entry.count !== (counts.get(entry.id) ?? 0)) {
                problems.push(`${language}: keyword count mismatch for ${entry.id}`);
            }
        }
        keywordSets[language] = new Set(identifiers);
        if (identifiers.length !== keywordSets[language].size) problems.push(`${language}: duplicate keyword IDs in collection`);
    }
    for (const language of LANGUAGES) {
        if (!sameSet(keywordSets[language], keywordSets.en)) problems.push(`${language}: keyword IDs do not match the language-independent English set`);
    }
    const listedManifests = new Set();
    const bookIds = new Set();
    for (const entry of books) {
        const book = mapping(entry);
        const directory = book.directory;
        if (typeof directory !== 'string' || !directory.startsWith('books/') || !localFile(docs, `${directory}/manifest.json`)) {
            problems.push(`missing or unsafe manifest: ${directory}/manifest.json`);
            continue;
        }
        const root = path.join(docs, directory);
        const manifestPath = path.join(root, 'manifest.json');
        listedManifests.add(realpathSync(manifestPath));
        let manifest;
        try {
            manifest = readJson(manifestPath);
            if (!isObject(manifest)) throw new Error('manifest must be an object');
        } catch {
            problems.push(`${book.id}: invalid manifest.json`);
            continue;
        }
        let identifier = book.id;
        if (typeof identifier !== 'string' || !identifier) {
            problems.push('missing or invalid book ID in collection');
            identifier = '(no ID)';
        }
        if (bookIds.has(identifier)) problems.push(`${identifier}: duplicate book ID in collection`);
        bookIds.add(identifier);
        if (manifest.id !== book.id) problems.push(`${identifier}: manifest ID mismatch`);
        const route = titleRoute(String(mapping(manifest.title).en ?? ''));
        if (!sameArray(manifest.route, route)) problems.push(`${identifier}: route does not match English title words`);
        if (directory !== path.posix.join('books', ...route, String(manifest.id ?? ''))) {
            problems.push(`${identifier}: directory does not match title route and random ID`);
        }
        if (!localFile(root, 'editions.json')) {
            problems.push(`${identifier}: missing or unsafe editions.json`);
        } else {
            try {
                const history = readJson(path.join(root, 'editions.json'));
                if (!isObject(history) || !Array.isArray(history.editions)) throw new Error('history must contain edition records');
                if (history.bookId !== book.id) problems.push(`${identifier}: editions.json bookId mismatch`);
                if (!history.editions.some(edition => isObject(edition) && edition.id === history.currentEdition)) {
                    problems.push(`${identifier}: editions.json current edition is missing`);
                }
                for (const edition of history.editions) {
                    if (!isObject(edition) || !edition.publishedAt || !isObject(edition.changes)
                        || (Object.hasOwn(edition, 'pdf') && !isObject(edition.pdf))) {
                        problems.push(`${identifier}: malformed edition history entry`);
                        continue;
                    }
                    for (const pdf of Object.values(edition.pdf ?? {})) {
                        if (!localFile(root, pdf)) problems.push(`${identifier}: missing or unsafe historical PDF: ${pdf}`);
                    }
                }
            } catch {
                problems.push(`${identifier}: invalid editions.json`);
            }
        }
        const identifiers = Array.isArray(manifest.keywordIds) && manifest.keywordIds.every(value => typeof value === 'string') ? manifest.keywordIds : [];
        const idSet = new Set(identifiers);
        if (identifiers.length !== 100 || idSet.size !== 100) problems.push(`${identifier}: expected 100 distinct keyword IDs, got ${identifiers.length}`);
        const missing = [...idSet].filter(id => !keywordSets.en.has(id));
        if (missing.length) problems.push(`${identifier}: keyword IDs missing from collection: ${missing.sort().join(', ')}`);
        if (!sameArray(book.keywordIds, identifiers)) problems.push(`${identifier}: collection keyword IDs differ from manifest`);
        for (const language of LANGUAGES) {
            const values = mapping(manifest.keywords)[language];
            const keywords = Array.isArray(values) ? values : [];
            const normalized = keywords.map(value => keywordNormalise(String(value)));
            if (keywords.length !== 100 || new Set(normalized).size !== 100) {
                problems.push(`${identifier} ${language}: expected 100 distinct keywords, got ${keywords.length}`);
            }
            if (normalized.includes(keywordNormalise(String(mapping(manifest.title)[language] ?? '')))) {
                problems.push(`${identifier} ${language}: book title used as a keyword`);
            }
            for (const field of ['title', 'subtitle', 'shortDescription', 'coverUrl']) {
                if (!Object.hasOwn(mapping(manifest[field]), language)) problems.push(`${identifier} ${language}: missing ${field}`);
            }
            if (!localFile(root, `${language}/book.html`)) {
                problems.push(`${identifier} ${language}: missing or unsafe book page`);
            } else {
                const source = readUtf8(path.join(root, language, 'book.html'));
                const pageIds = [...source.matchAll(/(?:&|&amp;)keyword=([^"&<\s]+)/g)].map(match => {
                    try { return decodeURIComponent(match[1]); }
                    catch { return match[1]; }
                });
                if (pageIds.length !== identifiers.length || !sameSet(new Set(pageIds), idSet)) {
                    problems.push(`${identifier} ${language}: book-page keyword links do not match the manifest`);
                }
            }
        }
        if (!isObject(book.editions)) {
            problems.push(`${identifier}: malformed collection editions`);
            continue;
        }
        for (const edition of Object.values(book.editions)) {
            if (!isObject(edition)) {
                problems.push(`${identifier}: malformed collection edition`);
                continue;
            }
            for (const asset of Object.values(edition)) {
                if (!localFile(docs, asset)) problems.push(`missing or unsafe edition asset: ${asset}`);
            }
        }
    }
    const booksRoot = path.join(docs, 'books');
    if (contained(resolveAssetPath(booksRoot), realpathSync(docs))) {
        for (const manifest of manifestsUnder(booksRoot)) {
            if (!listedManifests.has(resolveAssetPath(manifest))) problems.push(`manifest missing from collection: ${path.relative(docs, manifest).split(path.sep).join('/')}`);
        }
    } else {
        problems.push('Book directory escapes the documentation root');
    }
    if (pathExists(path.join(docs, 'keywords'))) problems.push('legacy per-keyword pages exist; discovery must use the client-side catalogue filter');
    return problems;
}

export function main(argv = process.argv.slice(2)) {
    assertNodeVersion(process.versions.node, 'ScriptaHub catalogue checker');
    let docs = DEFAULT_DOCS;
    if (argv.length) {
        if (argv.length !== 2 || !['--root', '--docs'].includes(argv[0])) {
            console.error('Usage: node tools/check_catalogue.mjs [--root docs]');
            return 2;
        }
        docs = argv[1];
    }
    try {
        const problems = checkCatalogue(docs);
        if (problems.length) {
            console.error(problems.join('\n'));
            return 1;
        }
        console.log('ScriptaHub collection is valid.');
        return 0;
    } catch (error) {
        console.error(`Unable to check catalogue: ${error.message}`);
        return 1;
    }
}

if (process.argv[1] && pathExists(process.argv[1]) && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
    try {
        process.exitCode = main();
    } catch (error) {
        console.error(error.message);
        process.exitCode = 1;
    }
}
