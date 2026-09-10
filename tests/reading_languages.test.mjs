import test from 'node:test';
import assert from 'node:assert/strict';
import '../docs/assets/reading.js';

const reading = globalThis.ScriptaReading;
const root = 'https://example.test/library/';
const book = { id: 'bk-test', currentEdition: 'edition-2', directory: 'books/a/bk-test', title: { en: 'A & B' }, editions: Object.fromEntries(reading.supported.map(code => [code, { book: `books/a/bk-test/${code}/book.html` }])) };
book.editions.en.fullContent = 'books/a/bk-test/en/full_content.html';
book.editions.en.shortContent = 'books/a/bk-test/en/short_content.html';
book.editions.en.pdf = 'books/a/bk-test/en/book.pdf';
book.editions.ro.pdf = 'books/a/bk-test/ro/old.pdf';
book.editions.ro.shortContent = 'books/a/bk-test/ro/short_content.html';

test('all interface and target combinations preserve the requested reading format and UI language', () => {
  for (const ui of reading.supported) for (const target of reading.supported) for (const format of ['read', 'short']) {
    const url = reading.readingUrl(book, target, format, ui, root, 'en');
    assert.equal(url.searchParams.get('lang'), ui);
    assert.equal(url.searchParams.get('format'), format);
    assert.equal(url.searchParams.get('book'), book.directory);
    assert.equal(url.pathname, '/library/reader/index.html');
    assert.equal(url.searchParams.get('language'), reading.available(book, target, format) ? target : 'en');
    assert.equal(url.searchParams.get('back'), `../books/a/bk-test/${ui}/book.html?lang=${ui}`);
    assert.match(url.searchParams.get('id'), /edition-2/);
    assert.equal(url.searchParams.get('pdf'), '../books/a/bk-test/en/book.pdf');

  }
});

test('short Romanian edition never substitutes for a missing full Romanian translation', () => {
  assert.equal(reading.readingUrl(book, 'ro', 'read', 'fr', root).searchParams.get('language'), 'en');
  assert.match(reading.readingUrl(book, 'ro', 'short', 'fr', root).pathname, /reader/);
});

test('structured mail safely encodes edition, languages and visitor text', () => {
  const url = new URL(reading.mailUrl(book, { target: 'pl', format: 'short', uiLanguage: 'ro', source: 'en', name: 'A&B', email: 'a+b@example.test', note: 'First?\nSecond & third #4' }));
  assert.equal(url.protocol, 'mailto:');
  assert.equal(url.pathname, 'create@scriptahub.com');
  const body = url.searchParams.get('body');
  for (const expected of ['Book: A & B', 'Edition: edition-2', 'Requested language: pl', 'Interface language: ro', '10-minute HTML', 'Name: A&B', 'First?\nSecond & third #4']) assert.ok(body.includes(expected), expected);
});

test('request paths also work with local files', () => {
  assert.equal(reading.requestUrl(book, 'de', 'read', 'ro', 'file:///library/docs/').protocol, 'file:');
});

test('missing English formats stay unavailable and request links remain explicit', () => {
  const draft = { ...book, editions: { ...book.editions, en: { book: book.editions.en.book } } };
  assert.equal(reading.readingUrl(draft, 'pt', 'read', 'pt', root), null);
  const url = reading.requestUrl(draft, 'pt', 'short', 'ro', root, 'en');
  assert.equal(url.searchParams.get('target'), 'pt');
  assert.equal(url.searchParams.get('format'), 'short');
  assert.equal(url.searchParams.get('lang'), 'ro');
  assert.equal(url.searchParams.get('source'), 'en');
  assert.equal(reading.unavailableMessage('pt'), 'Esta edição de leitura ainda não está disponível em Português.');
});
