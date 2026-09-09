import { mkdir, unlink, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';
import {
    COPY, LANGUAGES, TOPICS, editionRecord, keywordIdentifier, keywordNormalise,
    readJson, readUtf8, titleRoute,
} from '../build_books.mjs';
import {
    bookId, cleanFragment, exists, hardlinkOrCopy, imageConverter, json, keywordSourceText,
    saveJson, slugify, subjectGroup, transfer,
} from './book-maintenance.mjs';

const codes = Object.keys(LANGUAGES);
const editorialAliases = {
    OpenDSU_Essential_Philosophy: 'opendsu',
    Trustworthy_AI_Engineering_Course: 'trustworthy-ai',
    The_Basilisk_Internal_Critique_of_Outfinitism: 'the-basilisks-internal-critique-of-outfinitism',
    FUTURE_RESEARCH_INFRASTRUCTURE: 'future-research-infrastructure',
};

function metadataFromPage(source, filename) {
    const one = (pattern, label) => {
        const value = source.match(pattern)?.[1];
        if (value === undefined) throw new Error(`Missing ${label} in ${filename}`);
        return cleanFragment(value);
    };
    const subtitle = source.match(/<p\s+class="edition-subtitle"[^>]*>(.*?)<\/p>/is)?.[1];
    return {
        title: one(/<h1[^>]*>(.*?)<\/h1>/is, 'title'),
        subtitle: subtitle === undefined ? 'Axiologic Research Edition' : cleanFragment(subtitle),
        description: one(/<p\s+class="edition-why"[^>]*>(.*?)<\/p>/is, 'description'),
        category: one(/<p\s+class="eyebrow edition-kicker"[^>]*>(.*?)<\/p>/is, 'category')
            .replace(' · Axiologic Research Editions', ''),
        cover: one(/class="[^"]*\bedition-cover\b[^"]*"[^>]*\bsrc="[^"]*\/([^/"\s]+)"/is, 'cover')
            .replace(/(?:%[\da-f]{2})+/gi, (value) => Buffer.from(value.replaceAll('%', ''), 'hex').toString('utf8')),
    };
}

export async function buildLegacy(context) {
    const { books, docs, sourceRoot, tools, keywordWorker } = context;
    await keywordWorker({ operation: 'check', translation: true, requireModels: true });
    const convert = context.convertImage ?? await imageConverter();
    const content = path.join(sourceRoot, 'content');
    const sourceIndex = readJson(path.join(content, 'index.json'));
    const sourceBooks = new Map(sourceIndex.books.map((book) => [book.id, book]));
    const { shelves } = readJson(new URL('../keywords/vocabulary.json', import.meta.url));
    const shelfTerms = new Set(Object.values(shelves).flatMap((group) => group.en.split('|').map((label) => keywordNormalise(label).trim())));
    const planned = [];
    for (const [sourceId, sourceBook] of [...sourceBooks].sort((first, second) => {
        return first[1].slug < second[1].slug ? -1 : first[1].slug > second[1].slug ? 1 : 0;
    })) {
        const legacyPage = path.join(sourceRoot, 'books', sourceBook.slug, 'index.html');
        const metadata = metadataFromPage(readUtf8(legacyPage), legacyPage);
        const group = subjectGroup(metadata.category, metadata.title, metadata.description);
        const editionSources = Object.fromEntries(sourceBook.editions.map((edition) => {
            const language = edition.language.toLowerCase();
            if (!Object.hasOwn(LANGUAGES, language)) throw new Error(`Unsupported source language: ${edition.language}`);
            return [language, edition];
        }));
        const readers = new Map();
        for (const edition of Object.values(editionSources)) {
            for (const key of ['html', 'tenMinuteHtml']) {
                if (!Object.hasOwn(edition, key)) continue;
                const filename = path.join(content, edition[key]);
                if (!readers.has(filename)) readers.set(filename, readUtf8(filename));
            }
        }
        const english = editionSources.en ?? {};
        const source = english.tenMinuteHtml || english.html;
        const sourceText = source ? keywordSourceText(readers.get(path.join(content, source))) : '';
        planned.push({ sourceId, metadata, group, editionSources, sourceText });
    }
    const candidates = await keywordWorker({
        operation: 'extract',
        records: planned.map(({ metadata, sourceText }) => ({
            title: metadata.title, description: metadata.description, sourceText, limit: 140,
        })),
    });
    for (const [index, book] of planned.entries()) {
        book.phrases = candidates[index].filter((phrase) => !shelfTerms.has(keywordNormalise(phrase).trim())).slice(0, 90);
        if (book.phrases.length < 90) throw new Error(`${book.metadata.title} yielded only ${book.phrases.length} source-derived keywords`);
    }
    await mkdir(books, { recursive: true });
    const manifests = [];
    let moved = 0;
    for (const { sourceId, metadata, group, editionSources, phrases } of planned) {
        const id = bookId();
        const route = titleRoute(metadata.title);
        const root = path.join(books, ...route, id);
        for (const language of codes) await mkdir(path.join(root, language), { recursive: true });
        for (const [language, edition] of Object.entries(editionSources)) {
            const target = path.join(root, language);
            for (const [sourceKey, filename] of [['pdf', 'book.pdf'], ['html', 'full_content.html'], ['tenMinuteHtml', 'short_content.html']]) {
                if (!Object.hasOwn(edition, sourceKey)) continue;
                const old = path.join(content, edition[sourceKey]);
                const destination = path.join(target, filename);
                if (await transfer(old, destination)) moved++;
                const assets = path.join(path.dirname(old), path.parse(old).name + '.assets');
                if (await exists(assets) && await transfer(assets, path.join(target, path.basename(assets)))) moved++;
                if (path.extname(destination) === '.html') await context.fixReader(destination, language);
            }
        }
        const englishCover = path.join(root, 'en', 'cover.png');
        const displayCover = path.join(root, 'en', 'cover.webp');
        const thumbnail = path.join(root, 'en', 'thumbnail.webp');
        if (await transfer(path.join(content, 'covers', metadata.cover), englishCover)) moved++;
        await convert(englishCover, displayCover);
        if (await transfer(path.join(content, 'thumbnails', path.parse(metadata.cover).name + '.webp'), thumbnail)) moved++;
        await convert(displayCover, thumbnail, true);
        for (const language of codes.filter((code) => code !== 'en')) {
            for (const [source, name] of [[englishCover, 'cover.png'], [displayCover, 'cover.webp'], [thumbnail, 'thumbnail.webp']]) {
                await hardlinkOrCopy(source, path.join(root, language, name));
            }
        }
        const editions = Object.fromEntries(codes.map((language) => [language, editionRecord(root, language)]));
        const keywords = Object.fromEntries(codes.map((language) => [language, [...shelves[group][language].split('|'), ...phrases]]));
        const keywordIds = [...shelves[group].en.split('|'), ...phrases].map(keywordIdentifier);
        const localise = (value) => Object.fromEntries(codes.map((language) => [language, typeof value === 'function' ? value(language) : value]));
        const manifest = {
            schemaVersion: 1, id, sourceId, route, category: metadata.category, group,
            title: localise(metadata.title), subtitle: localise(metadata.subtitle),
            shortDescription: localise((language) => COPY[language].description
                .replaceAll('{title}', metadata.title).replaceAll('{topic}', TOPICS[language][group])),
            keywords, keywordIds,
            coverUrl: localise((language) => editions[language].cover),
            thumbnailUrl: localise((language) => editions[language].thumbnail),
            editions,
            availableLanguages: codes.filter((language) => editions[language].fullContent || editions[language].shortContent).map((language) => LANGUAGES[language]),
        };
        await saveJson(path.join(root, 'manifest.json'), manifest);
        await tools.ensureEditionsFile(root, manifest);
        manifests.push({ ...manifest, directory: path.relative(docs, root).split(path.sep).join('/') });
    }
    const collection = tools.makeCollection(manifests);
    await saveJson(path.join(docs, 'collection.json'), collection);
    await writeFile(path.join(docs, 'collection.js'), `globalThis.SCRIPTA_COLLECTION = ${JSON.stringify(collection)};\n`);
    await context.repairReaderLinks();
    await context.rebuildKeywords();
    return { books: manifests.length, moved, keywords: Object.values(collection.keywords).reduce((total, entries) => total + entries.length, 0) };
}

export async function recoverLeftovers(context) {
    const { docs, sourceRoot } = context;
    const collection = await json(path.join(docs, 'collection.json'));
    const roots = new Map(collection.books.map((book) => [book.sourceId, path.join(docs, book.directory)]));
    let moved = 0;
    const updateManifest = async (sourceId, language, field, filename) => {
        const target = path.join(roots.get(sourceId), 'manifest.json');
        const manifest = await json(target);
        manifest.editions[language][field] = `${language}/${filename}`;
        manifest.availableLanguages = Object.entries(manifest.editions)
            .filter(([, edition]) => Object.hasOwn(edition, 'fullContent') || Object.hasOwn(edition, 'shortContent'))
            .map(([code]) => LANGUAGES[code]);
        await saveJson(target, manifest);
    };
    const moveEdition = async (source, sourceId, language, filename, field) => {
        const destination = path.join(roots.get(sourceId), language, filename);
        if (await transfer(source, destination)) moved++;
        const assets = path.join(path.dirname(source), path.parse(source).name + '.assets');
        if (await exists(assets) && await transfer(assets, path.join(path.dirname(destination), path.basename(assets)))) moved++;
        if (path.extname(destination) === '.html') await context.fixReader(destination, language);
        if (field) await updateManifest(sourceId, language, field, filename);
    };
    const content = path.join(sourceRoot, 'content');
    for (const [relative, sourceId, language, filename, field] of [
        ['htmls/ES/The_Thousand_Handed_Devil_ES.html', 'The_Thousand_Handed_Devil', 'es', 'full_content.html', 'fullContent'],
        ['10minutes/The_Schizoid_and_the_Oracle.html', 'The_Schizoid_and_the_Oracle', 'en', 'short_content.html', 'shortContent'],
        ['10minutes/PL/EXPLAINABLE_PL.html', 'EXPLAINABLE_AI', 'pl', 'short_content.html', 'shortContent'],
        ['htmls/FR/The_Fragmented_Future_FR(1).html', 'The_Fragmented_Future', 'fr', 'full_content.previous.html'],
        ['10minutes/ES/EXPLAINABLE_ES.html', 'EXPLAINABLE_AI', 'es', 'short_content.previous.html'],
        ['10minutes/IT/EXPLAINABLE_IT.html', 'EXPLAINABLE_AI', 'it', 'short_content.previous.html'],
        ['EN/The_Future_of_Research_Infrastructure.pdf', 'FUTURE_RESEARCH_INFRASTRUCTURE', 'en', 'book.previous-edition.pdf'],
    ]) {
        await moveEdition(path.join(content, relative), sourceId, language, filename, field);
    }
    const schizoid = path.join(roots.get('The_Schizoid_and_the_Oracle'), 'ro');
    for (const [relative, filename] of [
        ['covers/The_Schizoid_and_the_Oracle_RO.png', 'cover.png'],
        ['thumbnails/The_Schizoid_and_the_Oracle_RO.webp', 'thumbnail.webp'],
    ]) {
        const source = path.join(content, relative);
        if (!await exists(source)) continue;
        const destination = path.join(schizoid, filename);
        if (await exists(destination)) await unlink(destination);
        await transfer(source, destination);
        moved++;
    }
    await moveEdition(path.join(content, 'covers/Outfinitism_Third_Edition.png'), 'Outfinitism_Meta_Rationality', 'en', 'cover.previous-edition.png');
    await moveEdition(path.join(content, 'thumbnails/Outfinitism_Third_Edition.webp'), 'Outfinitism_Meta_Rationality', 'en', 'thumbnail.previous-edition.webp');
    await context.rebuild();
    return moved;
}

export async function recoverEditorialDescriptions(context, { fetchPage = globalThis.fetch, pause = delay } = {}) {
    let recovered = 0;
    const missing = [];
    for (const filename of await context.manifests()) {
        const manifest = await json(filename);
        const sourceId = String(manifest.sourceId);
        const candidates = new Set([editorialAliases[sourceId], slugify(String(manifest.title.en)), slugify(sourceId)].filter(Boolean));
        let description;
        for (const slug of candidates) {
            try {
                const response = await fetchPage(`https://www.axiologic.net/books/${slug}/`, {
                    headers: { 'User-Agent': 'ScriptaHub catalogue migration/1.0 (+https://www.axiologic.net)' },
                    signal: AbortSignal.timeout(12000),
                });
                if (!response.ok) continue;
                const source = await response.text();
                const match = source.match(/<p\s+class="edition-why"[^>]*>(.*?)<\/p>/is);
                if (match) {
                    description = cleanFragment(match[1]);
                    break;
                }
            } catch {
                continue;
            }
        }
        if (description) {
            if (manifest.shortDescription.en !== description) {
                manifest.shortDescription.en = description;
                await saveJson(filename, manifest);
                recovered++;
            }
        } else {
            missing.push(sourceId);
        }
        await pause(80);
    }
    await context.rebuild();
    return { recovered, missing };
}
