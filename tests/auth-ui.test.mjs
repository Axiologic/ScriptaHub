import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import vm from 'node:vm';

const source = await readFile(new URL('../src/auth.js', import.meta.url), 'utf8');
const clientImport = "import { authError, createAccountClient, normalizeConfig } from './auth-client.js';";
assert.ok(source.startsWith(clientImport), 'Update dependency injection if the UI client import changes');
const uiSource = source.slice(clientImport.length);
const tick = () => new Promise((resolve) => setImmediate(resolve));
const account = { sub: 'reader-1', roles: ['selfRegistered'] };

function ui({ parent, accountClient } = {}) {
  const documentListeners = new Map();
  const navigations = [];
  const newTabs = [];
  const downloads = [];
  const popups = [];
  const fetches = [];
  let currentUrl = 'https://scriptahub.com/reader/index.html?lang=en';
  const location = {
    get href() { return currentUrl; },
    set href(value) { currentUrl = new URL(value, currentUrl).href; navigations.push(currentUrl); },
    get origin() { return new URL(currentUrl).origin; },
  };

  class Element {
    constructor(tag) {
      this.tagName = tag.toUpperCase();
      this.children = [];
      this.attributes = new Map();
      this.listeners = new Map();
      this.dataset = {};
      this.programmaticClicks = 0;
    }
    append(...children) { for (const child of children) { child.parentNode = this; this.children.push(child); } }
    setAttribute(name, value) { this.attributes.set(name, String(value)); }
    removeAttribute(name) { this.attributes.delete(name); }
    hasAttribute(name) { return this.attributes.has(name); }
    addEventListener(type, handler, options = {}) {
      const handlers = this.listeners.get(type) || [];
      handlers.push({ handler, once: options.once });
      this.listeners.set(type, handlers);
    }
    emit(type, event) {
      for (const entry of [...this.listeners.get(type) || []]) {
        entry.handler(event);
        if (entry.once) this.listeners.get(type).splice(this.listeners.get(type).indexOf(entry), 1);
      }
    }
    closest() { return this.tagName === 'A' && this.href ? this : this.parentNode?.closest(); }
    showModal() { this.open = true; }
    close() { this.open = false; this.emit('close', { target: this }); }
    remove() { this.removed = true; if (this.parentNode) this.parentNode.children = this.parentNode.children.filter((child) => child !== this); }
    focus() { this.focused = true; }
    click() { this.programmaticClicks++; activate(this); }
  }

  const document = {
    currentScript: { src: 'https://scriptahub.com/assets/auth.js' },
    documentElement: { lang: 'en' },
    head: new Element('head'),
    body: new Element('body'),
    activeElement: new Element('button'),
    createElement: (tag) => new Element(tag),
    addEventListener(type, handler) {
      const handlers = documentListeners.get(type) || [];
      handlers.push(handler);
      documentListeners.set(type, handlers);
    },
  };
  function activate(element, options = {}) {
    const event = {
      type: 'click', button: 0, ctrlKey: false, metaKey: false, shiftKey: false, altKey: false,
      ...options, target: element, defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; },
    };
    element.emit(event.type, event);
    const pending = Promise.all((documentListeners.get(event.type) || []).map((handler) => handler(event)));
    if (!event.defaultPrevented && element.tagName === 'A') {
      if (element.hasAttribute('download')) downloads.push(element.href);
      else if (element.target === '_blank') newTabs.push(element.href);
      else location.href = element.href;
    }
    return { event, pending };
  }
  const window = {
    location,
    open(url, target, features) {
      const popup = { url, target, features, document: { body: { textContent: '' } }, closed: false, close() { this.closed = true; } };
      popups.push(popup);
      return popup;
    },
  };
  window.parent = parent || window;
  const client = accountClient || { hasSession: () => true, current: async () => account, signIn: async () => { throw new Error('A current account should not sign in again'); } };
  const context = vm.createContext({
    URL, location, window, document,
    AbortSignal: { timeout: () => undefined },
    sessionStorage: {},
    authError: (code) => Object.assign(new Error(code), { code }),
    normalizeConfig: (input) => input,
    createAccountClient: () => client,
    fetch: async (url) => { fetches.push(String(url)); return { ok: true, json: async () => ({ issuer: 'https://accounts.example/oidc', clientId: 'scriptahub-web' }) }; },
  });
  vm.runInContext(uiSource, context, { filename: 'src/auth.js' });
  function link(options = {}) {
    const element = new Element('a');
    element.href = options.href || 'https://scriptahub.com/books/example/book.pdf';
    element.target = options.target || '';
    if (options.action) element.dataset.authAction = options.action;
    if (options.download) element.setAttribute('download', '');
    document.body.append(element);
    return element;
  }
  return {
    window, document, link, activate, location, navigations, newTabs, downloads, popups, fetches,
    dialogs: () => document.body.children.filter((element) => element.tagName === 'DIALOG' && !element.removed),
  };
}

test('same-origin reader frames share the exact parent account function and pending sign-in', async () => {
  let finishSignIn;
  let signIns = 0;
  const top = ui({ accountClient: {
    hasSession: () => false,
    current: async () => null,
    signIn: () => { signIns++; return new Promise((resolve) => { finishSignIn = resolve; }); },
  } });
  const firstFrame = ui({ parent: top.window });
  const secondFrame = ui({ parent: top.window });
  assert.equal(firstFrame.window.ScriptaHubAuth.requireAccount, top.window.ScriptaHubAuth.requireAccount);
  assert.equal(secondFrame.window.ScriptaHubAuth.requireAccount, top.window.ScriptaHubAuth.requireAccount);
  const first = top.window.ScriptaHubAuth.requireAccount('feedback');
  const second = firstFrame.window.ScriptaHubAuth.requireAccount('download');
  const third = secondFrame.window.ScriptaHubAuth.requireAccount('download');
  assert.equal(second, first);
  assert.equal(third, first);
  await tick();
  assert.equal(signIns, 1);
  assert.equal(top.popups.length, 1);
  assert.equal(firstFrame.popups.length + secondFrame.popups.length, 0);
  assert.equal(firstFrame.fetches.length + secondFrame.fetches.length, 0);
  finishSignIn(account);
  assert.equal(await first, account);
  assert.equal(await second, account);
  assert.equal(await third, account);
  assert.equal(top.popups[0].closed, true);
});

test('cross-origin frames keep their own account function', async () => {
  const parent = { get location() { throw new Error('Cross-origin access denied'); }, ScriptaHubAuth: { requireAccount() { throw new Error('Must not share this API'); } } };
  const frame = ui({ parent });
  await tick();
  assert.notEqual(frame.window.ScriptaHubAuth.requireAccount, parent.ScriptaHubAuth.requireAccount);
  assert.equal(frame.fetches.length, 1);
  assert.equal(await frame.window.ScriptaHubAuth.requireAccount(), account);
});

test('middle, modified, and target-blank actions wait for a real Continue link without replacing the current page', async () => {
  const cases = [
    { type: 'auxclick', button: 1 }, { ctrlKey: true }, { metaKey: true }, { shiftKey: true }, { target: '_blank' },
  ];
  for (const options of cases) {
    const page = ui();
    await tick();
    const originalUrl = page.location.href;
    const original = page.link({ target: options.target });
    const activation = page.activate(original, options);
    assert.equal(activation.event.defaultPrevented, true);
    await tick();
    assert.equal(original.programmaticClicks, 0);
    assert.equal(page.location.href, originalUrl);
    assert.deepEqual(page.newTabs, []);
    assert.equal(page.dialogs().length, 1);
    const dialog = page.dialogs()[0];
    const actions = dialog.children.find((child) => child.tagName === 'DIV');
    const proceed = actions.children.find((child) => child.tagName === 'A');
    assert.equal(proceed.href, original.href);
    assert.equal(proceed.target, '_blank');
    assert.equal(proceed.rel, 'noopener noreferrer');
    assert.equal(proceed.textContent, 'Continue');
    const continuation = page.activate(proceed);
    assert.equal(continuation.event.defaultPrevented, false, 'The authenticated Continue link must bypass the gate');
    await Promise.all([activation.pending, continuation.pending]);
    assert.deepEqual(page.newTabs, [original.href]);
    assert.equal(page.location.href, originalUrl);
    assert.deepEqual(page.navigations, []);
    assert.equal(page.dialogs().length, 0);
    assert.equal(original.hasAttribute('aria-busy'), false);
    assert.equal(page.popups.length, 0);
  }
});

test('cancelling the new-tab continuation leaves the current page and requested link unchanged', async () => {
  const page = ui();
  await tick();
  const original = page.link({ target: '_blank' });
  const originalUrl = page.location.href;
  const activation = page.activate(original);
  await tick();
  const dialog = page.dialogs()[0];
  const cancel = dialog.children.find((child) => child.tagName === 'DIV').children.find((child) => child.tagName === 'BUTTON');
  await page.activate(cancel).pending;
  await activation.pending;
  assert.deepEqual(page.newTabs, []);
  assert.equal(page.location.href, originalUrl);
  assert.equal(original.programmaticClicks, 0);
  assert.equal(original.hasAttribute('aria-busy'), false);
  assert.equal(page.document.activeElement.focused, true);
});

test('normal same-page action replays exactly once after authentication', async () => {
  const page = ui();
  await tick();
  const original = page.link({ href: 'https://scriptahub.com/feedback/index.html?book=example', action: 'feedback' });
  const activation = page.activate(original);
  assert.equal(activation.event.defaultPrevented, true);
  assert.deepEqual(page.navigations, []);
  await activation.pending;
  assert.equal(original.programmaticClicks, 1);
  assert.deepEqual(page.navigations, [original.href]);
  assert.deepEqual(page.newTabs, []);
  assert.equal(page.dialogs().length, 0);
  assert.equal(original.hasAttribute('aria-busy'), false);
});

test('a download attribute keeps the requested download behavior after a modified click', async () => {
  const page = ui();
  await tick();
  const original = page.link({ download: true });
  await page.activate(original, { metaKey: true }).pending;
  assert.equal(original.programmaticClicks, 1);
  assert.deepEqual(page.downloads, [original.href]);
  assert.deepEqual(page.navigations, []);
  assert.deepEqual(page.newTabs, []);
  assert.equal(page.dialogs().length, 0);
});
