import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { audit, parseHtmlInventory } from '../tools/audit_internal_links.mjs';

function fixture(t, files = {}) {
  const folder = mkdtempSync(join(tmpdir(), 'scriptahub-links-'));
  t.after(() => rmSync(folder, { recursive: true, force: true }));
  const root = join(folder, 'docs');
  mkdirSync(root);
  function put(path, source) {
    const destination = join(root, path);
    mkdirSync(dirname(destination), { recursive: true });
    writeFileSync(destination, source);
    return destination;
  }
  for (const [path, source] of Object.entries(files)) put(path, source);
  return { folder, root, put };
}

test('HTML inventory decodes attributes, preserves tag lines, and ignores scripts, raw text and comments', () => {
  const inventory = parseHtmlInventory(`<!doctype html>\n<A ID="a&amp;b" NAME="legacy" HREF="next.html?x=1&amp;y=2#title">Read</A>\n<!-- <img src="missing-comment.png"> -->\n<script>const fake = '<a href="missing-script.html">';</script>\n<style>.x::after{content:'<img src="missing-style.png">'}</style>\n<textarea><a href="missing-textarea.html"></textarea>\n<img src='picture.webp' poster="cover.webp">`);
  assert.deepEqual([...inventory.anchors], ['a&b', 'legacy']);
  assert.deepEqual(inventory.links, [
    { value: 'next.html?x=1&y=2#title', line: 2, attribute: 'href' },
    { value: 'picture.webp', line: 7, attribute: 'src' },
    { value: 'cover.webp', line: 7, attribute: 'poster' },
  ]);
  assert.deepEqual(inventory.tags[0], { tagName: 'a', attrs: { id: 'a&b', name: 'legacy', href: 'next.html?x=1&y=2#title' }, line: 2 });
  assert.equal(inventory.tags.filter((tag) => tag.tagName === 'a').length, 1);
});

test('audit resolves percent-encoded paths, entities, query-only links, fragments and directory indexes', (t) => {
  const { root } = fixture(t, {
    'index.html': '<h1 id="local">Home</h1><a href="?lang=ro#local">Here</a><a href="chapters/a%20%26%20b.html?lang=ro&amp;x=2#caf%C3%A9">Chapter</a><a href="chapters/#start">Contents</a><a href="document.pdf#page=2">PDF</a>',
    'chapters/index.html': '<h1 id="start">Contents</h1><a href="/index.html#local">Home</a>',
    'chapters/a & b.html': '<h2 id="caf&#233;">Title</h2><a name="legacy"></a><a href="#legacy">Jump</a>',
    'document.pdf': 'PDF fixture',
  });
  assert.deepEqual(audit(root), []);
});

test('audit reports missing targets and anchors in stable source order with start-tag lines', (t) => {
  const { root } = fixture(t, {
    'index.html': '<a href="z.html">Missing</a>\n<img\n src="missing.png">\n<a href="other.html#absent">Anchor</a>\n<a href="empty/">Directory</a>',
    'other.html': '<p id="present">Existing</p>',
  });
  mkdirSync(join(root, 'empty'));
  assert.deepEqual(audit(root), [
    'index.html:1: missing local target: z.html',
    'index.html:2: missing local target: missing.png',
    'index.html:4: missing anchor #absent in other.html',
    'index.html:5: missing local target: empty/',
  ]);
});

test('srcset candidates preserve data URLs and ignore empty candidates while auditing local image alternatives', (t) => {
  const { root } = fixture(t, {
    'index.html': '<img srcset=", , data:image/svg+xml,%3Csvg%3E%3C/svg%3E 1x, small.png 2x, missing.png 3x,">',
    'small.png': 'image',
  });
  const inventory = parseHtmlInventory('<img srcset="first.png 1x,second.png 2x, third.png, fourth.png 4x">');
  assert.deepEqual(inventory.links.map((link) => link.value), ['first.png', 'second.png', 'third.png', 'fourth.png']);
  assert.deepEqual(audit(root), ['index.html:1: missing local target: missing.png']);
});

test('external schemes and network-relative links are ignored without contacting a server', (t) => {
  const { root } = fixture(t, {
    'index.html': ['https://example.invalid/nope', 'HTTP://example.invalid/nope', '//example.invalid/nope', 'mailto:reader@example.test', 'tel:+123', 'javascript:void(0)', 'data:text/plain,hello', 'ftp://example.invalid/book.pdf', 'file:///nope', 'custom:thing'].map((href) => `<a href="${href}">Link</a>`).join('\n'),
  });
  assert.deepEqual(audit(root), []);
});

test('path traversal, encoded traversal and symlink targets cannot escape the site root', (t) => {
  const { root, folder } = fixture(t, {
    'index.html': '<a href="../outside.html">Outside</a>\n<a href="%2e%2e/outside.html">Encoded</a>\n<a href="assets/secret.pdf">Symlink directory</a>\n<a href="out.pdf">Symlink file</a>\n<a href="dangling.pdf">Dangling symlink</a>\n<a href="chapter/">Index symlink</a>',
  });
  writeFileSync(join(folder, 'outside.html'), '<a href="not-scanned.html">Outside source</a>');
  writeFileSync(join(folder, 'secret.pdf'), 'outside');
  symlinkSync(folder, join(root, 'assets'));
  symlinkSync(join(folder, 'secret.pdf'), join(root, 'out.pdf'));
  symlinkSync(join(folder, 'missing.pdf'), join(root, 'dangling.pdf'));
  mkdirSync(join(root, 'chapter'));
  symlinkSync(join(folder, 'outside.html'), join(root, 'chapter/index.html'));
  const problems = audit(root);
  assert.equal(problems.length, 7);
  assert.ok(problems.every((problem) => problem.includes('escapes docs/')));
  assert.ok(problems.some((problem) => problem.includes('href escapes docs/: chapter/')));
  assert.ok(!problems.some((problem) => problem.includes('not-scanned')));
});

test('in-root symlink destinations are audited and symlink directory cycles are not traversed', (t) => {
  const { root } = fixture(t, {
    'index.html': '<a href="copy.html#target">Alias</a><a href="assets/page.html#target">Directory alias</a>',
    'real/page.html': '<h1 id="target">Target</h1>',
  });
  symlinkSync(join(root, 'real/page.html'), join(root, 'copy.html'));
  symlinkSync(join(root, 'real'), join(root, 'assets'));
  symlinkSync(root, join(root, 'real/cycle'));
  assert.deepEqual(audit(root), []);
});

test('malformed percent encodings and decoded nulls produce diagnostics instead of stopping the audit', (t) => {
  const { root } = fixture(t, {
    'index.html': '<a href="bad%ZZ.html">Literal percent</a>\n<a href="%FF.html">Bad UTF8</a>\n<a href="bad%00.html">Null</a>',
    'bad%ZZ.html': '<p>Literal filename</p>',
  });
  assert.deepEqual(audit(root), [
    'index.html:2: missing local target: %FF.html',
    'index.html:3: invalid local target: bad%00.html',
  ]);
});

test('CLI preserves report-only/check exit codes, help and missing-root diagnostics', (t) => {
  const { root, folder, put } = fixture(t, { 'index.html': '<a href="missing.html">Missing</a>' });
  const script = fileURLToPath(new URL('../tools/audit_internal_links.mjs', import.meta.url));
  const run = (...args) => spawnSync(process.execPath, [script, ...args], { encoding: 'utf8', cwd: folder });
  const report = run('--root', root);
  assert.equal(report.status, 0);
  assert.match(report.stdout, /missing local target: missing.html/);
  assert.match(report.stderr, /1 local-link problem\(s\) found/);
  assert.equal(run('--root', root, '--check').status, 1);
  const missing = run('--root', join(folder, 'absent'), '--check');
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /Missing site root/);
  assert.equal(run('--unknown').status, 2);
  assert.equal(run('--help').status, 0);
  put('missing.html', '<p>Added</p>');
  const valid = run('--root', root, '--check');
  assert.equal(valid.status, 0);
  assert.match(valid.stdout, /No broken local HTML links or fragment anchors/);
});
