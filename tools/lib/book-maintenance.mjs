import { writeFile, readdir, mkdir, rename, copyFile, cp, link, unlink, rmdir, rm, stat, lstat, realpath } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { assertNodeVersion, runProcess } from './runtime.mjs';
import { LANGUAGES, titleRoute, keywordNormalise, keywordIdentifier, editionRecord, casefold, readUtf8, readJson } from '../build_books.mjs';
import { decodeHtmlEntities } from '../audit_internal_links.mjs';
import { buildLegacy, recoverLeftovers, recoverEditorialDescriptions } from './book-legacy.mjs';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const KEYWORDS = fileURLToPath(new URL('../keywords/', import.meta.url));
const CACHE = fileURLToPath(new URL('../keyword-translations.generated.json', import.meta.url));
const codes = Object.keys(LANGUAGES);
const json = async (filename) => readJson(filename);
const saveJson = async (filename, value) => writeFile(filename, JSON.stringify(value, null, 2) + '\n');
const relative = (target, start) => path.relative(start, target).split(path.sep).join('/');
const normalise = (value) => keywordNormalise(value).trim();
const slugify = (value) => value.normalize('NFKD').replace(/[^\x00-\x7f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'keyword';
const bookId = () => 'bk-' + randomUUID().replaceAll('-', '').slice(0, 16);

async function exists(filename) {
    try {
        await stat(filename);
        return true;
    } catch (error) {
        if (error.code === 'ENOENT' || error.code === 'ENOTDIR') return false;
        throw error;
    }
}

async function files(root) {
    const result = [];
    if (!await exists(root)) return result;
    for (const entry of await readdir(root, { withFileTypes: true })) {
        const target = path.join(root, entry.name);
        if (entry.isDirectory()) result.push(...await files(target));
        else if (entry.isFile()) result.push(target);
    }
    return result.sort();
}

export function cleanFragment(value) {
    return decodeHtmlEntities(value.replace(/<[^>]+>/g, ' ')).replace(/\s+/gu, ' ').trim();
}

export function subjectGroup(category, title, description = '') {
    const sample = `${category} ${title} ${description}`.toLowerCase();
    const has = (values) => values.some((value) => sample.includes(value));
    if (has(['literature', 'literary', 'science fiction', 'cosmic', 'political & social sf', 'human & philosophical sf', 'philosophical fiction', 'speculative fiction'])) return 'fiction';
    if (has(['business', 'startups', 'investment', 'economy'])) return 'business';
    if (category.toLowerCase() === 'essay' && has(['market', 'profitable', 'subscription', 'willingness to pay'])) return 'business';
    if (has(['outfinit', 'mathematics', 'meta-rational', 'philosophy', 'meaning'])) return 'philosophy';
    if (has(['power', 'institutions', 'society', 'civilization', 'civilisation', 'social', 'anthropology', 'emotion'])) return 'society';
    if (has(['research', 'science', 'executable', 'experiments'])) return 'science';
    return 'technology';
}

export function introductoryDescription(source) {
    const ignored = ['conversion notice', 'copyright', 'publishing rights', 'available for free', "author's note", 'all rights reserved', 'kdp', 'scriptahub', 'axiologic', 'achilles', 'outfinity'];
    for (const match of source.matchAll(/<p\b[^>]*>(.*?)<\/p>/gis)) {
        let text = cleanFragment(match[1]);
        if ([...text].length < 110 || ignored.some((word) => casefold(text).includes(word))) continue;
        if ([...text].length > 430) {
            const prefix = [...text].slice(0, 430).join('');
            const stop = Math.max(...['. ', '! ', '? ', '… '].map((mark) => prefix.lastIndexOf(mark)));
            text = [...prefix.slice(0, Math.max(stop, 0))].length > 160 ? prefix.slice(0, stop + 1) : [...text].slice(0, 427).join('').trimEnd() + '…';
        }
        return text;
    }
    return null;
}

export function keywordSourceText(source) {
    source = source.replace(/<(script|style)\b[^>]*>.*?<\/\1>/gis, ' ');
    source = source.match(/<main\b[^>]*>(.*?)<\/main>/is)?.[1] ?? source;
    source = source.replace(/<figure\b[^>]*>.*?<\/figure>/gis, ' ');
    source = source.replace(/<p\b[^>]*>(?:(?!<\/p>).)*(?:KDP|publishing rights|Author(?:&#x27;|&apos;|’|')s Note|available for free|ScriptaHub|all (?:the )?free books|Venture Studio)(?:(?!<\/p>).)*<\/p>/gis, ' ');
    source = source.replace(/<section\b[^>]*>\s*<h[1-4]\b[^>]*>\s*(?:why\s+read|reading\s+the\s+complete)[^<]*<\/h[1-4]>.*?<\/section>/gis, ' ');
    const ignored = new Set(['content', 'contents', 'copyright', 'author notes', 'authors notes', 'references', 'bibliography', 'selective bibliography']);
    const headings = [...source.matchAll(/<h[1-4]\b[^>]*>(.*?)<\/h[1-4]>/gis)].map((match) => cleanFragment(match[1]))
        .filter((value) => !ignored.has(normalise(value)) && !normalise(value).startsWith('copyright '));
    source = source.replace(/<\/(?:address|article|aside|blockquote|caption|dd|div|dl|dt|figcaption|footer|h[1-6]|header|li|main|nav|p|section|td|th|tr)\s*>/gi, '. ');
    return [...Array.from({ length: 5 }, () => headings).flat(), cleanFragment(source)].join(' ');
}

export async function runKeywordWorker(payload, { env = process.env } = {}) {
    const python = env.SCRIPTAHUB_KEYWORD_PYTHON || 'python3';
    let result;
    try {
        result = await runProcess(python, ['-B', path.join(KEYWORDS, 'local_nlp.py')], {
            input: JSON.stringify(payload), env, timeout: payload.operation === 'check' && !payload.requireModels ? 60000 : 60 * 60 * 1000,
        });
    } catch (error) {
        throw new Error(`Local keyword processing requires Python 3.10+ and its optional NLP packages. Set SCRIPTAHUB_KEYWORD_PYTHON to the project virtual environment interpreter; see dependencies.md. ${error.message}`);
    }
    if (result.code !== 0) throw new Error(result.stderr.trim() || `Keyword worker exited ${result.code}. See dependencies.md.`);
    if (result.stderr) process.stderr.write(result.stderr);
    return JSON.parse(result.stdout);
}

export async function imageConverter({ env = process.env } = {}) {
    for (const command of ['magick', 'convert']) {
        try {
            const probe = await runProcess(command, ['-version'], { env, timeout: 5000 });
            if (probe.code !== 0 || !/ImageMagick (?:6|7)\./.test(probe.stdout)) continue;
            const formats = await runProcess(command, ['-list', 'format'], { env, timeout: 5000 });
            if (formats.code !== 0 || !/^\s*WEBP\*?\s+WEBP\s+[^\r\n]*w/m.test(formats.stdout)) continue;
            return async (source, destination, thumbnail = false) => {
                await mkdir(path.dirname(destination), { recursive: true });
                const operations = thumbnail
                    ? ['-resize', '320x480!', '-strip', '-quality', '84']
                    : ['-fuzz', '3%', '-trim', '+repage', '-resize', '640x960^', '-gravity', 'center', '-extent', '640x960', '-quality', '90'];
                const result = await runProcess(command, [source, ...operations, destination], { env, timeout: 120000 });
                if (result.code !== 0) throw new Error(`ImageMagick could not create ${destination}: ${result.stderr.trim()}`);
            };
        } catch (error) {
            if (error.code !== 'ENOENT') continue;
        }
    }
    throw new Error('Cover generation requires ImageMagick 6 or 7 with WebP write support. Install it as described in dependencies.md; no catalogue files were changed.');
}

async function transfer(source, destination) {
    if (await exists(destination)) return false;
    if (!await exists(source)) throw new Error(`Source does not exist: ${source}`);
    await mkdir(path.dirname(destination), { recursive: true });
    try {
        await rename(source, destination);
    } catch (error) {
        if (error.code !== 'EXDEV') throw error;
        await cp(source, destination, { recursive: true, errorOnExist: true, force: false, preserveTimestamps: true, verbatimSymlinks: true });
        await rm(source, { recursive: true });
    }
    return true;
}

async function hardlinkOrCopy(source, destination) {
    if (await exists(destination)) return;
    await mkdir(path.dirname(destination), { recursive: true });
    try {
        await link(source, destination);
    } catch {
        await copyFile(source, destination);
    }
}

export async function createMaintenanceTools({ docsRoot, tools, sourceRoot = path.join(ROOT, 'old_content'), keywordWorker = runKeywordWorker, convertImage, cachePath = CACHE } = {}) {
    const docs = path.resolve(docsRoot ?? tools.docs);
    const books = path.join(docs, 'books');
    const manifests = async () => (await files(books)).filter((name) => path.basename(name) === 'manifest.json');
    const rebuild = async () => {
        await tools.rebuildCollectionFromManifests();
        await tools.refreshPages();
    };
    const fixReader = async (filename, language) => {
        let source = readUtf8(filename);
        const reader = relative(path.join(docs, 'reader'), path.dirname(filename));
        source = source.replace(/(["'])(?:\.\.\/)+reader\//g, (_, quote) => quote + reader + '/');
        if (await exists(path.join(path.dirname(filename), 'book.pdf'))) {
            source = source.replace(/(["'])(?:\.\.\/)+EN\/[^"']+\.pdf/g, (_, quote) => quote + 'book.pdf');
        }
        source = /<html\b[^>]*\blang=/i.test(source)
            ? source.replace(/(<html\b[^>]*\blang=["'])[^"']*/i, (_, prefix) => prefix + language)
            : source.replace(/<html\b/i, `<html lang="${language}"`);
        await writeFile(filename, source);
    };
    const repairReaderLinks = async () => {
        let changed = 0;
        const allFiles = await files(books);
        for (const filename of allFiles.filter((name) => ['full_content.html', 'short_content.html'].includes(path.basename(name)) || name.endsWith('.previous.html'))) {
            const source = readUtf8(filename);
            const directory = path.dirname(filename);
            const bookRoot = path.dirname(directory);
            const full = await exists(path.join(directory, 'full_content.html')) ? 'full_content.html' : 'book.html';
            let repaired = source.replace(/(["'])[^"']*htmls\/[A-Za-z]{2}\/[^"']+\.html\1/gi, (_, quote) => quote + full + quote);
            repaired = repaired.replace(/(["'])([^"']*(?:(?:htmls\/[A-Za-z]{2}\/)|(?:[./]+(?:EN|FR|DE|ES|PT|IT|RO|PL)\/))[^"']+\.assets\/([^/"']+))\1/gi, (match, quote, legacy, basename) => {
                const language = legacy.match(/(?:htmls\/|\/)(EN|FR|DE|ES|PT|IT|RO|PL)\//i)?.[1]?.toLowerCase();
                const preferred = language ? path.join(bookRoot, language) : directory;
                const candidates = allFiles.filter((name) => path.basename(name) === basename && name.startsWith(bookRoot + path.sep));
                const target = candidates.find((name) => name.startsWith(preferred + path.sep)) ?? candidates[0];
                return target ? quote + relative(target, directory) + quote : match;
            });
            if (repaired !== source) {
                await writeFile(filename, repaired);
                changed++;
            }
        }
        return changed;
    };
    const enrich = async () => {
        let changed = 0;
        for (const filename of await manifests()) {
            const manifest = await json(filename);
            for (const [language, edition] of Object.entries(manifest.editions)) {
                const candidate = edition.shortContent || edition.fullContent;
                if (!candidate) continue;
                const description = introductoryDescription(readUtf8(path.join(path.dirname(filename), candidate)));
                if (description && manifest.shortDescription[language] !== description) {
                    manifest.shortDescription[language] = description;
                    changed++;
                }
            }
            await saveJson(filename, manifest);
        }
        await rebuild();
        return changed;
    };
    const refreshCovers = async () => {
        const convert = convertImage ?? await imageConverter();
        let changed = 0;
        for (const filename of await manifests()) {
            const root = path.dirname(filename);
            if (!await exists(path.join(root, 'en/cover.png'))) continue;
            const display = path.join(root, 'en/cover.webp');
            const thumbnail = path.join(root, 'en/thumbnail.webp');
            await convert(path.join(root, 'en/cover.png'), display);
            await convert(display, thumbnail, true);
            const manifest = await json(filename);
            for (const language of codes) {
                if (language !== 'en') {
                    for (const [source, basename] of [[display, 'cover.webp'], [thumbnail, 'thumbnail.webp']]) {
                        const destination = path.join(root, language, basename);
                        if (await exists(destination)) await unlink(destination);
                        await hardlinkOrCopy(source, destination);
                    }
                }
                const edition = await editionRecord(root, language);
                if (!isDeepStrictEqual(manifest.editions[language], edition) || manifest.coverUrl[language] !== edition.cover) {
                    manifest.editions[language] = edition;
                    manifest.coverUrl[language] = edition.cover;
                    changed++;
                }
            }
            await saveJson(filename, manifest);
        }
        await rebuild();
        return changed;
    };
    const rebrand = async () => {
        const replace = (value) => {
            if (JSON.isRawJSON(value)) return value;
            if (typeof value === 'string') return value.replace(/www\\.axiologic\\.net/gi, 'ScriptaHub.com').replace(/Axiologic Research|Recherche Axiologique|Investigação Axiológica|Investigación Axiológica|Badania Aksjologiczne|Axiologic|\b(?:Achilles|Achille|Aquiles)\b/gi, 'ScriptaHub');
            if (Array.isArray(value)) return value.map(replace);
            if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, replace(item)]));
            return value;
        };
        let changed = 0;
        for (const filename of await manifests()) {
            const manifest = await json(filename);
            const updated = replace(manifest);
            if (!isDeepStrictEqual(updated, manifest)) {
                await saveJson(filename, updated);
                changed++;
            }
        }
        for (const filename of (await files(books)).filter((name) => name.endsWith('.html'))) {
            const source = readUtf8(filename);
            const updated = replace(source.replace(/https?:\/\/(?:www\.)?axiologic\.net/gi, 'https://ScriptaHub.com').replace(/www\.axiologic\.net/gi, 'ScriptaHub.com'));
            if (source !== updated) {
                await writeFile(filename, updated);
                changed++;
            }
        }
        await rebuild();
        return changed;
    };
    const rebuildKeywords = async () => {
        await keywordWorker({ operation: 'check', translation: true });
        const { shelves } = await json(path.join(KEYWORDS, 'vocabulary.json'));
        const shelfTerms = new Set(Object.values(shelves).flatMap((group) => group.en.split('|').map(normalise)));
        const records = [];
        for (const filename of await manifests()) {
            const manifest = await json(filename);
            const edition = manifest.editions.en ?? {};
            const source = edition.shortContent || edition.fullContent;
            const sourceFile = source ? path.join(path.dirname(filename), source) : null;
            records.push({ filename, manifest, title: manifest.title.en, description: manifest.shortDescription.en ?? '',
                sourceText: sourceFile && await exists(sourceFile) ? keywordSourceText(readUtf8(sourceFile)) : '', limit: 120 });
        }
        const candidates = await keywordWorker({ operation: 'extract', records });
        for (let index = 0; index < records.length; index++) {
            records[index].candidates = candidates[index].filter((phrase) => !shelfTerms.has(normalise(phrase)));
            if (records[index].candidates.length < 90) throw new Error(`${records[index].title} yielded only ${records[index].candidates.length} source-derived keywords`);
        }
        const phrases = [...new Set(records.flatMap((record) => record.candidates))];
        const translations = await keywordWorker({ operation: 'translate', phrases, cache: await exists(cachePath) ? await json(cachePath) : {} });
        const outputs = [];
        for (const { filename, manifest, candidates: choices, title, description } of records) {
            const group = subjectGroup(manifest.category, title, description);
            const localized = Object.fromEntries(codes.map((language) => [language, shelves[group][language].split('|')]));
            const identifiers = shelves[group].en.split('|').map(keywordIdentifier);
            const seen = Object.fromEntries(codes.map((language) => [language, new Set(localized[language].map(keywordNormalise))]));
            for (const phrase of choices) {
                const labels = Object.fromEntries(codes.map((language) => [language, translations[language][phrase]]));
                if (codes.some((language) => seen[language].has(keywordNormalise(labels[language])))) continue;
                identifiers.push(keywordIdentifier(phrase));
                for (const language of codes) {
                    localized[language].push(labels[language]);
                    seen[language].add(keywordNormalise(labels[language]));
                }
                if (identifiers.length === 100) break;
            }
            if (identifiers.length !== 100) throw new Error(`${title} has only ${identifiers.length} distinct translated keywords`);
            if (manifest.group !== group || !isDeepStrictEqual(manifest.keywordIds, identifiers) || !isDeepStrictEqual(manifest.keywords, localized)) {
                outputs.push([filename, { ...manifest, group, keywordIds: identifiers, keywords: localized }]);
            }
        }
        await saveJson(cachePath, { schemaVersion: 1, translations: Object.fromEntries(codes.filter((code) => code !== 'en').map((code) => [code, translations[code]])) });
        for (const [filename, manifest] of outputs) await saveJson(filename, manifest);
        await rebuild();
        return outputs.length;
    };
    const reorganizeRoutes = async () => {
        const collection = await json(path.join(docs, 'collection.json'));
        for (const listing of collection.books) {
            const oldRoot = path.join(docs, listing.directory);
            const manifest = await json(path.join(oldRoot, 'manifest.json'));
            const route = titleRoute(manifest.title.en);
            const id = bookId();
            const newRoot = path.join(books, ...route, id);
            if (await exists(newRoot)) throw new Error(`Destination already exists: ${newRoot}`);
            await transfer(oldRoot, newRoot);
            await saveJson(path.join(newRoot, 'manifest.json'), { ...manifest, id, route });
            for (const language of codes) {
                for (const filename of (await files(path.join(newRoot, language))).filter((name) => path.dirname(name) === path.join(newRoot, language) && name.endsWith('.html') && path.basename(name) !== 'book.html')) await fixReader(filename, language);
            }
        }
        const removeEmpty = async (root) => {
            for (const entry of await readdir(root, { withFileTypes: true })) {
                if (!entry.isDirectory()) continue;
                const directory = path.join(root, entry.name);
                await removeEmpty(directory);
                try { await rmdir(directory); } catch (error) { if (error.code !== 'ENOTEMPTY') throw error; }
            }
        };
        await removeEmpty(books);
        await rebuild();
        return collection.books.length;
    };
    const retireSource = async () => {
        const expected = path.join(ROOT, 'old_content');
        if (path.resolve(sourceRoot) !== expected || await realpath(sourceRoot) !== expected || (await lstat(sourceRoot)).isSymbolicLink()) throw new Error(`Refusing to retire anything except ${expected}`);
        const problems = await tools.check();
        if (problems.length) throw new Error('Cannot retire source while the new collection is invalid:\n' + problems.join('\n'));
        const keep = path.join(sourceRoot, 'unclassified');
        await mkdir(keep, { recursive: true });
        let retained = 0;
        for (const name of ['Idei_putine_si_fixe_RO_Draft_0_1.html', 'The Deep Canopy.html', 'Fortati_sa_Performam_RO_Draft_0_3.html']) {
            const draft = path.join(sourceRoot, 'content/htmls/RO', name);
            if (await exists(draft)) { await transfer(draft, path.join(keep, name)); retained++; }
        }
        for (const name of await readdir(sourceRoot)) if (name !== 'unclassified') await rm(path.join(sourceRoot, name), { recursive: true });
        return retained;
    };
    return { docs, books, manifests, rebuild, fixReader, repairReaderLinks, enrich, refreshCovers, rebrand, rebuildKeywords, reorganizeRoutes, retireSource, keywordWorker, convertImage, sourceRoot, tools };
}

export { files, json, saveJson, exists, transfer, hardlinkOrCopy, slugify, bookId };

export async function runMaintenance(command, options) {
    assertNodeVersion();
    const context = await createMaintenanceTools(options);
    const actions = {
        'repair-reader-links': [context.repairReaderLinks, (value) => `Repaired legacy reader links in ${value} edition file(s).`, false],
        'refresh-covers': [context.refreshCovers, (value) => `Regenerated portrait display covers for ${value} edition records.`],
        enrich: [context.enrich, (value) => `Enriched ${value} manifest values from published reader editions.`],
        rebrand: [context.rebrand, (value) => `Rebranded public metadata or reader content in ${value} files.`],
        'rebuild-keywords': [context.rebuildKeywords, (value) => `Rebuilt editorial discovery keywords for ${value} books.`],
        'reorganize-routes': [context.reorganizeRoutes, (value) => `Reorganized ${value} books into title-word routes with random IDs.`],
        'retire-source': [context.retireSource, (value) => `Retired processed legacy files; retained ${value} unclassified Romanian drafts in old_content/unclassified/.`, false],
        build: [() => buildLegacy(context), (value) => `Built ${value.books} books, moved ${value.moved} source entries, and indexed ${value.keywords} localised discovery terms.`],
        recover: [() => recoverLeftovers(context), (value) => `Recovered ${value} legacy source entries.`],
        'recover-editorial-descriptions': [() => recoverEditorialDescriptions(context), (value) => `Recovered ${value.recovered} editorial descriptions; ${value.missing.length} were unavailable.${value.missing.length ? '\nUnavailable: ' + value.missing.join(', ') : ''}`],
    };
    if (!Object.hasOwn(actions, command)) throw new Error(`Unknown maintenance command: ${command}`);
    const [action, message, validate = true] = actions[command];
    const result = await action();
    if (validate) {
        const problems = await options.tools.check();
        if (problems.length) { console.error(problems.join('\n')); return 1; }
    }
    console.log(message(result));
    return 0;
}
