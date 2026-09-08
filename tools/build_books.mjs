#!/usr/bin/env node
/** Refresh localized book pages and edition history from the existing manifests. */
import { createHash, randomUUID } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, realpathSync, renameSync, rmSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const DOCS = path.join(ROOT, 'docs');
const copyData = JSON.parse(readFileSync(new URL('./lib/book-page-copy.json', import.meta.url), 'utf8'));
export const LANGUAGES = Object.freeze(copyData.languages);
const { topics, copy, cloudInstructions, cloudPreviewInstructions, cloudCloseLabels, bookActions, shelfCategories } = copyData;
const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
const object = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
const relative = (target, start) => path.relative(start, target).split(path.sep).join('/') || '.';
const escape = (value) => String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#x27;' })[character]);
const queryValue = (value) => encodeURIComponent(String(value)).replace(/[!'()*]/g, (character) => `%${character.charCodeAt(0).toString(16).toUpperCase()}`).replace(/%20/g, '+');
const query = (values) => Object.entries(values).map(([key, value]) => `${queryValue(key)}=${queryValue(value)}`).join('&');

function inlineJson(value) {
  if (Array.isArray(value)) return `[${value.map(inlineJson).join(', ')}]`;
  if (object(value)) return `{${Object.entries(value).map(([key, entry]) => `${JSON.stringify(key)}: ${inlineJson(entry)}`).join(', ')}}`;
  return JSON.stringify(value);
}

function localized(book, field, language) {
  const value = book[field]?.[language];
  if (typeof value !== 'string') throw new Error(`${book.id}: missing ${field}.${language}`);
  return value;
}

function editionFor(book, language) {
  if (!own(LANGUAGES, language)) throw new Error(`Unsupported language: ${language}`);
  const edition = book.editions?.[language];
  if (!object(edition)) throw new Error(`${book.id}: missing ${language} edition`);
  return edition;
}

function shelfIds(group) {
  const labels = shelfCategories[group];
  if (!labels) throw new Error(`Unknown subject group: ${group}`);
  return new Set(labels.map((label) => {
    const normalized = label.toLowerCase().normalize('NFKD').replace(/[^\x00-\x7f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
    return `term:${createHash('sha256').update(normalized).digest('hex').slice(0, 20)}`;
  }));
}

export function readerHref(book, language, pagePath, formatName, { docsRoot = DOCS } = {}) {
  const edition = editionFor(book, language);
  const contentKey = formatName === 'short' ? 'shortContent' : 'fullContent';
  if (!own(edition, contentKey)) throw new Error(`${book.id} has no ${formatName} reader edition in ${language}`);
  if (!['short', 'read'].includes(formatName)) throw new Error(`Unsupported reading format: ${formatName}`);
  const readerDirectory = path.join(docsRoot, 'reader');
  const bookDirectory = path.resolve(docsRoot, book.directory);
  const params = {
    id: `${book.id}:${language}:${formatName}`,
    title: `${localized(book, 'title', language)} · ${copy[language][formatName]}`,
    html: relative(path.join(bookDirectory, edition[contentKey]), readerDirectory),
    mode: formatName === 'short' ? 'ten-minute' : 'full',
    back: relative(pagePath, readerDirectory),
    book: book.directory,
    language,
    format: formatName,
  };
  if (own(edition, 'pdf')) params.pdf = relative(path.join(bookDirectory, edition.pdf), readerDirectory);
  return `${relative(path.join(readerDirectory, 'index.html'), path.dirname(pagePath))}?${query(params)}`;
}

function siteFooter(start, language, docsRoot) {
  const legal = relative(path.join(docsRoot, 'legal'), start);
  const links = [
    ['terms.html', 'terms', 'Terms'], ['privacy.html', 'privacy', 'Privacy'],
    ['cookies.html', 'cookies', 'Cookies & local storage'], ['notice.html', 'notice', 'Legal notice'], ['ai.html', 'ai', 'AI transparency'],
  ];
  const navigation = links.map(([page, key, label]) => `<a data-footer-${key} data-legal-link href="${escape(`${legal}/${page}?lang=${language}`)}">${escape(label)}</a>`).join('');
  return `<footer class="site-footer"><a class="footer-wordmark" href="${escape(relative(path.join(docsRoot, 'index.html'), start))}">ScriptaHub.com</a><nav aria-label="Legal">${navigation}</nav><span class="footer-status">© 2026 ScriptaHub</span></footer>`;
}

export function bookPage(book, language, pagePath, hasContent, { docsRoot = DOCS } = {}) {
  const edition = editionFor(book, language);
  const words = copy[language];
  const title = localized(book, 'title', language);
  const subtitle = localized(book, 'subtitle', language);
  const topic = topics[language][book.group];
  if (!topic) throw new Error(`${book.id}: unknown subject group ${book.group}`);
  const description = localized({ ...book, descriptions: book.descriptions || book.shortDescription }, 'descriptions', language).replaceAll('Axiologic Research', 'ScriptaHub');
  const pageDirectory = path.dirname(pagePath);
  const asset = (...segments) => relative(path.join(docsRoot, ...segments), pageDirectory);
  const home = asset('index.html');
  const css = asset('assets', 'site.css');
  const collectionScript = asset('collection.js');
  const siteScript = asset('assets', 'site.js');
  const authScript = asset('assets', 'auth.js');
  const createPage = asset('create', 'index.html');
  const feedbackPage = asset('feedback', 'index.html');
  const editionsPage = asset('editions', 'index.html');
  const languageOptions = Object.entries(LANGUAGES).map(([code, name]) => `<option value="../${code}/book.html"${code === language ? ' selected' : ''}>${escape(name)}</option>`).join('\n');
  const actions = [];
  if (own(edition, 'shortContent')) actions.push(`<a class="button button-quiet" href="${escape(readerHref(book, language, pagePath, 'short', { docsRoot }))}">${escape(words.short)}</a>`);
  if (own(edition, 'fullContent')) actions.push(`<a class="button button-quiet" href="${escape(readerHref(book, language, pagePath, 'read', { docsRoot }))}">${escape(words.read)}</a>`);
  if (own(edition, 'pdf')) actions.push(`<a class="button button-quiet" href="book.pdf" data-auth-action="download">${escape(words.download)}</a>`);
  const workflowQuery = query({ book: book.directory, lang: language });
  actions.push(`<a class="button" href="${escape(`${feedbackPage}?${workflowQuery}`)}" data-auth-action="feedback">${escape(bookActions[language].feedback)}</a>`);
  actions.push(`<a class="button button-quiet" href="${escape(`${editionsPage}?${workflowQuery}`)}">${escape(bookActions[language].editions)}</a>`);
  const available = hasContent ?? (own(edition, 'fullContent') || own(edition, 'shortContent'));
  const availability = available ? '' : `<p class="edition-unavailable">${escape(words.unavailable.replace('{language}', LANGUAGES[language]))}</p>`;
  const identifiers = book.keywordIds;
  const labels = book.keywords?.[language];
  if (!Array.isArray(identifiers) || !Array.isArray(labels) || identifiers.length !== labels.length) throw new Error(`${book.id} ${language}: keyword IDs and labels must have matching lengths`);
  const shelves = shelfIds(book.group);
  const entries = identifiers.map((identifier, rank) => {
    const count = Number(book.keywordStats?.[language]?.[identifier]?.count);
    if (!Number.isSafeInteger(count) || count < 0) throw new Error(`${book.id} ${language}: missing or invalid keyword count for ${identifier}`);
    return { identifier, rank, count, label: String(labels[rank]) };
  });
  const byFrequency = (first, second) => second.count - first.count || first.rank - second.rank;
  const ordered = [entries.filter((entry) => !shelves.has(entry.identifier)).sort(byFrequency), entries.filter((entry) => shelves.has(entry.identifier)).sort(byFrequency)].flat();
  const keywordItems = ordered.map(({ identifier, count, label }) => ({ label, count, href: `${home}?${query({ lang: language, keyword: identifier })}` }));
  const keywordData = inlineJson(keywordItems).replaceAll('</', '<\\/');
  const keywordOptions = inlineJson({ ariaLabel: words.keywords, instruction: cloudPreviewInstructions[language], modalInstruction: cloudInstructions[language], closeLabel: cloudCloseLabels[language], showInstruction: false }).replaceAll('</', '<\\/');
  const cloudScript = asset('assets', 'keyword-cloud.js');
  const themeSwitcher = '<div class="theme-switcher"><button type="button" data-theme-toggle aria-label="Switch to dark appearance">☼</button></div>';
  return `<!doctype html>
<html lang="${language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escape(title)} · ScriptaHub</title>
  <meta name="description" content="${escape(description)}">
  <meta property="og:type" content="book">
  <meta property="og:title" content="${escape(title)}">
  <meta property="og:description" content="${escape(description)}">
  <meta property="og:image" content="cover.webp">
  <link rel="stylesheet" href="${escape(css)}">
  <script defer src="${escape(authScript)}?v=20260908-1"></script>
</head>
<body data-book-page="true" data-book-language="${language}">
  <main class="site-shell book-page">
    <header class="site-header"><a class="wordmark" href="${escape(home)}">ScriptaHub<span>.com</span></a><div class="header-tools"><a class="header-create" data-create-link href="${escape(createPage)}?lang=${language}">${escape(bookActions[language].create)}</a><div class="site-scale" aria-label="Site text size"><button type="button" data-site-smaller aria-label="Decrease site size">A−</button><button type="button" data-site-size aria-label="Reset site size">100%</button><button type="button" data-site-larger aria-label="Increase site size">A+</button></div>${themeSwitcher}<label class="language-picker"><span class="sr-only">Language</span><select onchange="location.href=this.value">${languageOptions}</select></label></div></header>
    <article class="book-hero">
      <a class="cover-link" href="cover.webp"><img src="cover.webp" alt="${escape(title)} cover"></a>
      <div class="book-details"><div class="book-copy"><p class="eyebrow">${escape(topic)} · ScriptaHub</p><h1>${escape(title)}</h1><p class="book-subtitle">${escape(subtitle)}</p><p class="lead">${escape(description)}</p></div><div class="book-actions">${actions.join('')}</div>${availability}</div>
      <aside class="book-keyword-widget" aria-label="${escape(words.keywords)}"><div class="keyword-cloud book-keyword-cloud" data-book-keyword-cloud></div></aside>
    </article>
    <section class="book-introduction"><div><p class="eyebrow">ScriptaHub</p><h2>${escape(words.read)}</h2><p>${escape(words.presentation)}</p></div></section>${siteFooter(pageDirectory, language, docsRoot)}
  </main>
  <script src="${escape(cloudScript)}"></script><script>globalThis.ScriptaKeywordCloud.mount(document.querySelector('[data-book-keyword-cloud]'), ${keywordData}, ${keywordOptions});</script><script src="${escape(collectionScript)}"></script><script src="${escape(siteScript)}"></script>
</body>
</html>
`;
}

function contained(candidate, boundary) {
  const rel = path.relative(boundary, candidate);
  return rel === '' || (!rel.startsWith(`..${path.sep}`) && rel !== '..' && !path.isAbsolute(rel));
}

function relativeAsset(value, bookRoot, label) {
  if (typeof value !== 'string' || !value || path.isAbsolute(value) || value.includes('\\') || value.split('/').some((part) => part === '..' || part === '') || !contained(path.resolve(bookRoot, value), bookRoot)) throw new Error(`${label}: unsafe relative asset path`);
}

function readJson(filename) {
  try { return JSON.parse(readFileSync(filename, 'utf8')); }
  catch (error) { throw new Error(`Cannot read valid JSON from ${filename}: ${error.message}`, { cause: error }); }
}

function validateOutput(filename, boundary) {
  if (!contained(path.resolve(filename), path.resolve(boundary)) || !contained(realpathSync(path.dirname(filename)), realpathSync(boundary))) throw new Error(`Refusing output outside book directory: ${filename}`);
  if (existsSync(filename)) {
    const stat = lstatSync(filename);
    if (!stat.isFile() || stat.isSymbolicLink()) throw new Error(`Refusing non-file output: ${filename}`);
  }
}

function validDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(`${value}T00:00:00Z`);
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

function validateHistory(payload, manifest, bookRoot, filename) {
  const invalid = () => { throw new Error(`Malformed existing edition history: ${filename}`); };
  if (!object(payload) || payload.schemaVersion !== 1 || payload.bookId !== manifest.id || typeof payload.currentEdition !== 'string' || !payload.currentEdition || !Array.isArray(payload.editions) || !payload.editions.length) invalid();
  const ids = new Set();
  for (const entry of payload.editions) {
    if (!object(entry) || typeof entry.id !== 'string' || !entry.id || ids.has(entry.id) || !Number.isSafeInteger(entry.number) || entry.number < 1 || !validDate(entry.publishedAt) || !object(entry.changes) || Object.values(entry.changes).some((value) => typeof value !== 'string')) invalid();
    ids.add(entry.id);
    if (own(entry, 'label') && (!object(entry.label) || Object.values(entry.label).some((value) => typeof value !== 'string'))) invalid();
    if (own(entry, 'pdf')) {
      if (!object(entry.pdf)) invalid();
      for (const asset of Object.values(entry.pdf)) relativeAsset(asset, bookRoot, filename);
    }
  }
  if (!ids.has(payload.currentEdition)) invalid();
}

/** Prepare a history update without touching existing files or edition records. */
export function prepareEditionsFile(bookRoot, manifest) {
  bookRoot = path.resolve(bookRoot);
  const filename = path.join(bookRoot, 'editions.json');
  validateOutput(filename, bookRoot);
  if (typeof manifest.id !== 'string' || !manifest.id) throw new Error(`${bookRoot}: missing manifest ID`);
  const existing = existsSync(filename) ? readFileSync(filename, 'utf8') : null;
  let payload;
  if (existing !== null) {
    try { payload = JSON.parse(existing); }
    catch (error) { throw new Error(`Malformed existing edition history: ${filename}`, { cause: error }); }
    validateHistory(payload, manifest, bookRoot, filename);
  } else {
    const manifestPath = path.join(bookRoot, 'manifest.json');
    const date = existsSync(manifestPath) ? statSync(manifestPath).mtime : new Date();
    payload = {
      schemaVersion: 1,
      bookId: manifest.id,
      currentEdition: 'edition-1',
      editions: [{
        id: 'edition-1', number: 1,
        label: Object.fromEntries(Object.keys(LANGUAGES).map((language) => [language, bookActions[language].editionLabel])),
        publishedAt: date.toISOString().slice(0, 10),
        changes: Object.fromEntries(Object.keys(LANGUAGES).map((language) => [language, bookActions[language].initial])),
        pdf: {},
      }],
    };
  }
  const before = JSON.stringify(payload);
  const current = payload.editions.find((entry) => entry.id === payload.currentEdition);
  if (!own(current, 'pdf')) current.pdf = {};
  for (const [language, edition] of Object.entries(manifest.editions || {})) {
    if (object(edition) && edition.pdf && !own(current.pdf, language)) {
      relativeAsset(edition.pdf, bookRoot, `${manifest.id} ${language}`);
      current.pdf[language] = edition.pdf;
    }
  }
  const content = existing !== null && before === JSON.stringify(payload) ? existing : `${JSON.stringify(payload, null, 2)}\n`;
  return { path: filename, content, kind: 'editions', changed: existing !== content };
}

function writeOutput(output) {
  if (!output.changed) return;
  const temporary = `${output.path}.tmp-${randomUUID()}`;
  let created = false;
  try {
    writeFileSync(temporary, output.content, { encoding: 'utf8', flag: 'wx' });
    created = true;
    renameSync(temporary, output.path);
  } finally {
    if (created && existsSync(temporary)) rmSync(temporary);
  }
}

export function ensureEditionsFile(bookRoot, manifest) {
  const output = prepareEditionsFile(bookRoot, manifest);
  writeOutput(output);
  return output;
}

/** Validate every input and output before a refresh writes any generated file. */
export function planRefresh({ docsRoot = DOCS } = {}) {
  docsRoot = realpathSync(docsRoot);
  if (existsSync(path.join(docsRoot, 'keywords'))) throw new Error('Legacy docs/keywords exists; refresh will not delete it. Discovery must use the catalogue filter.');
  const booksRoot = realpathSync(path.join(docsRoot, 'books'));
  if (!contained(booksRoot, docsRoot)) throw new Error('Book directory escapes the documentation root');
  const collection = readJson(path.join(docsRoot, 'collection.json'));
  if (!Array.isArray(collection.books)) throw new Error('Collection must contain a books array');
  const keywordStats = Object.fromEntries(Object.keys(LANGUAGES).map((language) => {
    if (!Array.isArray(collection.keywords?.[language])) throw new Error(`Collection is missing ${language} keywords`);
    return [language, Object.fromEntries(collection.keywords[language].map((keyword) => [keyword.id, { count: keyword.count }]))];
  }));
  const directories = new Set();
  const files = [];
  for (const listing of collection.books) {
    if (typeof listing.directory !== 'string' || !listing.directory.startsWith('books/') || listing.directory.includes('\\') || listing.directory.split('/').some((part) => !part || part === '.' || part === '..')) throw new Error(`Unsafe book directory: ${listing.directory}`);
    const bookRoot = path.resolve(docsRoot, listing.directory);
    const actualRoot = realpathSync(bookRoot);
    if (!contained(actualRoot, booksRoot) || actualRoot === booksRoot || directories.has(actualRoot)) throw new Error(`Unsafe or duplicate book directory: ${listing.directory}`);
    directories.add(actualRoot);
    const manifest = readJson(path.join(bookRoot, 'manifest.json'));
    if (manifest.id !== listing.id) throw new Error(`Manifest ID does not match collection: ${listing.directory}`);
    files.push(prepareEditionsFile(bookRoot, manifest));
    const book = { ...manifest, directory: listing.directory, descriptions: manifest.shortDescription, keywordStats };
    for (const language of Object.keys(LANGUAGES)) {
      const edition = editionFor(book, language);
      for (const value of Object.values(edition)) relativeAsset(value, bookRoot, `${manifest.id} ${language}`);
      const filename = path.join(bookRoot, language, 'book.html');
      validateOutput(filename, bookRoot);
      const content = bookPage(book, language, filename, own(edition, 'fullContent') || own(edition, 'shortContent'), { docsRoot });
      const existing = existsSync(filename) ? readFileSync(filename, 'utf8') : null;
      files.push({ path: filename, content, kind: 'page', changed: content !== existing });
    }
  }
  return { books: collection.books.length, pages: collection.books.length * Object.keys(LANGUAGES).length, files };
}

export function refreshPages({ docsRoot = DOCS, write = true } = {}) {
  const plan = planRefresh({ docsRoot });
  if (write) for (const output of plan.files) writeOutput(output);
  return { books: plan.books, pages: plan.pages, changedFiles: plan.files.filter((output) => output.changed).length };
}

export async function main(argv = process.argv.slice(2)) {
  if (argv[0] === 'check') {
    const { main: checkMain } = await import('./check_catalogue.mjs');
    return checkMain(argv.slice(1).map((argument) => argument === '--docs' ? '--root' : argument));
  }
  if (argv[0] !== 'refresh') throw new Error('Usage: node tools/build_books.mjs refresh [--docs PATH] [--dry-run] | check [--docs PATH]');
  let docsRoot = DOCS;
  let dryRun = false;
  for (let index = 1; index < argv.length; index++) {
    if (argv[index] === '--dry-run') dryRun = true;
    else if (argv[index] === '--docs' && argv[index + 1] && !argv[index + 1].startsWith('--')) docsRoot = path.resolve(argv[++index]);
    else throw new Error(`Unknown or incomplete option: ${argv[index]}`);
  }
  const result = refreshPages({ docsRoot, write: !dryRun });
  console.log(`${dryRun ? 'Would refresh' : 'Refreshed'} ${result.books} book roots (${result.pages} pages, ${result.changedFiles} changed files); keyword discovery remains client-side.`);
  return result;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().then((result) => { if (typeof result === 'number') process.exitCode = result; }).catch((error) => { console.error(error.message); process.exitCode = 1; });
}
