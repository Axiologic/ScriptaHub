import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import vm from 'node:vm';

const workflowSource = await readFile(new URL('../docs/assets/workflow.js', import.meta.url), 'utf8');
const standaloneSource = await readFile(new URL('../docs/reader/standalone.js', import.meta.url), 'utf8');
const tick = () => new Promise((resolve) => setImmediate(resolve));

function workflow({ requireAccount, language = 'en', page = 'feedback' } = {}) {
  const listeners = {};
  const status = { textContent: '' };
  const submit = { disabled: true };
  const contract = { checked: true, addEventListener(type, handler) { listeners[`contract:${type}`] = handler; } };
  const values = new Map(Object.entries({ name: 'Reader', email: 'reader@example.com', feedback: 'Original draft', kind: 'Factual correction', sources: 'Chapter 3' }));
  const form = {
    isConnected: true,
    valid: true,
    reportValidity() { return this.valid; },
    querySelector(selector) { return selector === '[type=submit]' ? submit : status; },
    addEventListener(type, handler) { listeners[type] = handler; },
  };
  const list = { innerHTML: '' };
  const root = {
    innerHTML: '',
    querySelector(selector) {
      return selector === 'form' ? form : selector === '[data-contract-accept]' ? contract : selector === '[data-editions-list]' ? list : status;
    },
  };
  const openedMail = [];
  const location = { search: '?book=books/example/bk-test', set href(value) { openedMail.push(value); } };
  const context = vm.createContext({
    SCRIPTA_COLLECTION: {
      supportedLanguages: [{ code: 'en', name: 'English' }, { code: 'ro', name: 'Română' }],
      books: [{ id: 'bk-test', directory: 'books/example/bk-test', title: { en: 'Example book' }, shortDescription: { en: 'Description' }, thumbnailUrl: { en: 'cover.webp' }, editions: { en: { book: 'book.html' }, ro: { book: 'book.html' } } }],
    },
    ...(requireAccount ? { ScriptaHubAuth: { requireAccount } } : {}),
    document: { querySelector: () => root, documentElement: { lang: language }, body: { dataset: { workflowPage: page } }, addEventListener() {} },
    location,
    URLSearchParams,
    FormData: class { get(name) { return values.get(name); } },
    fetch: async () => ({ ok: true, json: async () => ({ currentEdition: 'ed-2', editions: [{ id: 'ed-2', number: 2, label: { en: 'Second edition' }, changes: { en: 'Correction' }, publishedAt: '2026-09-08', pdf: { en: 'en/book.pdf' } }, { id: 'ed-1', number: 1, publishedAt: '2026-09-01', pdf: { en: 'edition-files/ed-1/en.pdf' } }] }) }),
  });
  vm.runInContext(workflowSource, context);
  return { form, values, submit, status, contract, root, list, openedMail, submitForm: () => listeners.submit({ preventDefault() {} }), changeContract: () => listeners['contract:change']() };
}

test('direct feedback submission waits for an account, preserves editable draft, and deduplicates pending submission', async () => {
  let resolveAccount;
  let requests = 0;
  const gate = workflow({ requireAccount(action) { assert.equal(action, 'feedback'); requests++; return new Promise((resolve) => { resolveAccount = resolve; }); } });
  const pending = gate.submitForm();
  await gate.submitForm();
  assert.equal(requests, 1);
  assert.equal(gate.submit.disabled, true);
  assert.deepEqual(gate.openedMail, []);
  gate.values.set('feedback', 'Draft edited while registering');
  resolveAccount({ sub: 'reader-1', roles: ['selfRegistered'] });
  await pending;
  assert.equal(gate.openedMail.length, 1);
  const mail = new URL(gate.openedMail[0]);
  assert.equal(mail.protocol, 'mailto:');
  assert.equal(mail.pathname, 'create@scriptahub.com');
  assert.match(mail.searchParams.get('body'), /Draft edited while registering/);
  assert.match(mail.searchParams.get('body'), /Contribution agreement accepted: yes/);
  assert.equal(gate.submit.disabled, false);
});

test('cancelled registration leaves the feedback draft and form ready to retry', async () => {
  const gate = workflow({ requireAccount: async () => null });
  await gate.submitForm();
  assert.deepEqual(gate.openedMail, []);
  assert.equal(gate.values.get('feedback'), 'Original draft');
  assert.equal(gate.contract.checked, true);
  assert.equal(gate.submit.disabled, false);
});

test('feedback fails closed with localized status when the account bundle is unavailable', async () => {
  const gate = workflow({ language: 'ro' });
  await gate.submitForm();
  assert.deepEqual(gate.openedMail, []);
  assert.match(gate.status.textContent, /Autentificarea/);
  assert.equal(gate.values.get('feedback'), 'Original draft');
});

test('agreement withdrawal or detached form during registration cancels email creation', async () => {
  for (const change of [(gate) => { gate.contract.checked = false; gate.changeContract(); }, (gate) => { gate.form.isConnected = false; }, (gate) => { gate.form.valid = false; }]) {
    let resolveAccount;
    const gate = workflow({ requireAccount: () => new Promise((resolve) => { resolveAccount = resolve; }) });
    const pending = gate.submitForm();
    change(gate);
    resolveAccount({ sub: 'reader-1' });
    await pending;
    assert.deepEqual(gate.openedMail, []);
  }
});

test('invalid feedback and absent agreement do not start registration', async () => {
  let requests = 0;
  const gate = workflow({ requireAccount: async () => { requests++; return { sub: 'reader-1' }; } });
  gate.form.valid = false;
  await gate.submitForm();
  gate.form.valid = true;
  gate.contract.checked = false;
  await gate.submitForm();
  assert.equal(requests, 0);
  assert.deepEqual(gate.openedMail, []);
});

test('current and historical edition downloads carry the shared gate', async () => {
  const gate = workflow({ page: 'editions' });
  await tick();
  const links = gate.list.innerHTML.match(/<a\b[^>]+>/g);
  assert.equal(links.length, 2);
  assert.ok(links.every((link) => link.includes('data-auth-action="download"') && link.includes(' download')));
  assert.match(gate.list.innerHTML, /edition-files\/ed-1\/en.pdf/);
});

function standalone() {
  const listeners = {};
  const scripts = [];
  const status = [];
  const hrefs = ['https://scriptahub.com/books/test/book.pdf?edition=1', 'https://scriptahub.com/books/test/full_content.html', 'https://example.org/reference.pdf'];
  const links = hrefs.map((href) => ({ href, dataset: {}, clicks: 0, activations: [], dispatchEvent(event) { this.clicks++; this.activations.push(event); return true; }, after(node) { status.push(node); } }));
  const context = vm.createContext({
    URL,
    MouseEvent: class { constructor(type, init) { this.type = type; Object.assign(this, init); } },
    document: {
      currentScript: { src: 'https://scriptahub.com/reader/standalone.js' },
      documentElement: { lang: 'en' },
      querySelectorAll: (selector) => selector === 'a[href]' ? links : [],
      addEventListener(type, handler) { listeners[type] = handler; },
      createElement(tag) { return { tag, handlers: {}, addEventListener(type, handler) { this.handlers[type] = handler; }, setAttribute() {} }; },
      head: { append(script) { scripts.push(script); } },
    },
    window: { location: { href: 'https://scriptahub.com/books/test/full_content.html', pathname: '/books/test/full_content.html', origin: 'https://scriptahub.com' }, localStorage: { getItem: () => null }, addEventListener() {}, requestAnimationFrame() {} },
  });
  vm.runInContext(standaloneSource, context);
  function click(index = 0, type = 'click', button = 0, modifiers = {}) {
    const event = { type, button, buttons: 0, detail: 1, ctrlKey: false, metaKey: false, shiftKey: false, altKey: false, ...modifiers, defaultPrevented: false, stopped: false, target: { closest: () => links[index].dataset.authAction ? links[index] : null }, preventDefault() { this.defaultPrevented = true; }, stopImmediatePropagation() { this.stopped = true; } };
    return { event, pending: listeners[type](event) };
  }
  return { context, links, scripts, status, click };
}

test('standalone readers mark local PDFs and leave reading and external references public', async () => {
  const gate = standalone();
  assert.equal(gate.links[0].dataset.authAction, 'download');
  assert.equal(gate.links[1].dataset.authAction, undefined);
  assert.equal(gate.links[2].dataset.authAction, undefined);
  assert.equal(gate.scripts[0].src, 'https://scriptahub.com/assets/auth.js?v=20260908-1');
  const reading = gate.click(1);
  await reading.pending;
  assert.equal(reading.event.defaultPrevented, false);
});

test('early standalone PDF click waits for the auth bundle and replays once through the shared gate', async () => {
  const gate = standalone();
  const first = gate.click();
  const duplicate = gate.click();
  assert.equal(first.event.defaultPrevented, true);
  assert.equal(first.event.stopped, true);
  assert.equal(gate.links[0].clicks, 0);
  gate.context.ScriptaHubAuth = { requireAccount() {} };
  gate.scripts[0].handlers.load();
  await Promise.all([first.pending, duplicate.pending]);
  assert.equal(gate.links[0].clicks, 1);
  const loaded = gate.click();
  await loaded.pending;
  assert.equal(loaded.event.defaultPrevented, false);
});

test('standalone auth load failure keeps the PDF action pending and supports retry', async () => {
  const gate = standalone();
  const first = gate.click();
  gate.scripts[0].handlers.error();
  await first.pending;
  assert.equal(gate.links[0].clicks, 0);
  assert.match(gate.status[0].textContent, /currently unavailable/);
  const retry = gate.click();
  assert.equal(gate.scripts.length, 2);
  gate.context.ScriptaHubAuth = { requireAccount() {} };
  gate.scripts[1].handlers.load();
  await retry.pending;
  assert.equal(gate.links[0].clicks, 1);
  assert.equal(gate.status[0].textContent, '');
});

test('early middle click is gated while right click keeps its native context menu', async () => {
  const gate = standalone();
  const right = gate.click(0, 'auxclick', 2);
  await right.pending;
  assert.equal(right.event.defaultPrevented, false);
  const middle = gate.click(0, 'auxclick', 1);
  assert.equal(middle.event.defaultPrevented, true);
  gate.context.ScriptaHubAuth = { requireAccount() {} };
  gate.scripts[0].handlers.load();
  await middle.pending;
  assert.equal(gate.links[0].clicks, 1);
  assert.equal(gate.links[0].activations[0].type, 'auxclick');
  assert.equal(gate.links[0].activations[0].button, 1);
});

test('early standalone activations retain modifiers for the shared gate navigation decision', async () => {
  for (const modifiers of [{ ctrlKey: true }, { metaKey: true }, { shiftKey: true }, { altKey: true }, { ctrlKey: true, shiftKey: true }, { metaKey: true, altKey: true }]) {
    const gate = standalone();
    const activation = gate.click(0, 'click', 0, modifiers);
    gate.context.ScriptaHubAuth = { requireAccount() {} };
    gate.scripts[0].handlers.load();
    await activation.pending;
    assert.equal(gate.links[0].activations.length, 1);
    const replay = gate.links[0].activations[0];
    assert.equal(replay.type, 'click');
    assert.equal(replay.button, 0);
    assert.equal(replay.bubbles, true);
    assert.equal(replay.cancelable, true);
    for (const modifier of ['ctrlKey', 'metaKey', 'shiftKey', 'altKey']) {
      assert.equal(replay[modifier], Boolean(modifiers[modifier]), modifier);
    }
  }
});
