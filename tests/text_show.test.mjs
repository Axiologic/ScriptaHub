import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const source = readFileSync(new URL('../docs/assets/text-show.js', import.meta.url), 'utf8');

function harness({ reduced = false, whenVisible = false, text = ['First.', 'Last.'], ...options } = {}) {
  let now = 0, id = 0, visibility;
  const timers = new Map(), listeners = new Map(), rendered = [], events = [];
  const document = { hidden: false, addEventListener: (type, fn) => listeners.set(type, fn), removeEventListener: type => listeners.delete(type) };
  const target = { textContent: 'Original', className: '', dataset: {}, isConnected: true, classList: { add() {}, toggle() {} }, querySelectorAll: () => [], dispatchEvent: e => events.push(e.type) };
  const context = vm.createContext({ Intl, document, performance: { now: () => now },
    setTimeout: (fn, ms) => { timers.set(++id, { fn, at: now + ms }); return id; }, clearTimeout: id => timers.delete(id),
    matchMedia: () => ({ matches: reduced }), CustomEvent: class { constructor(type) { this.type = type; } },
    IntersectionObserver: class { constructor(fn) { visibility = fn; } observe() {} disconnect() {} },
  });
  vm.runInContext(source, context);
  const player = context.textShow(target, { text, whenVisible, render: sentence => rendered.push(sentence), ...options });
  const tick = ms => {
    const end = now + ms;
    for (;;) {
      const next = [...timers.entries()].filter(([, v]) => v.at <= end).sort((a, b) => a[1].at - b[1].at)[0];
      if (!next) break;
      now = next[1].at; timers.delete(next[0]); next[1].fn();
    }
    now = end;
  };
  return { player, target, rendered, events, tick, timers, context,
    visible(value) { visibility([{ isIntersecting: value, intersectionRatio: value ? 1 : 0 }]); },
    hidden(value) { document.hidden = value; listeners.get('visibilitychange')?.(); },
  };
}

test('completion includes the final sentence hold and fires once', () => {
  const h = harness();
  const first = h.context.textShow.duration('First.');
  h.tick(first);
  assert.deepEqual(h.rendered, ['First.', 'Last.']);
  assert.equal(h.player.completed, false);
  h.tick(first - 1);
  assert.equal(h.player.completed, false);
  h.tick(1);
  assert.equal(h.player.completed, true);
  h.tick(100000);
  assert.deepEqual(h.events, ['textshow:complete']);
});

test('offscreen and hidden-tab time never consumes the remaining hold', () => {
  const h = harness({ whenVisible: true });
  h.tick(100000); assert.deepEqual(h.rendered, []);
  h.visible(true); h.tick(1000);
  const remaining = h.player.remaining;
  h.visible(false); h.tick(100000);
  assert.equal(h.player.remaining, remaining);
  h.visible(true); h.hidden(true); h.tick(100000);
  assert.equal(h.player.remaining, remaining);
  h.hidden(false); h.tick(remaining);
  assert.deepEqual(h.rendered, ['First.', 'Last.']);
});

test('pause, navigation and destruction cancel stale completion', () => {
  const h = harness();
  h.player.pause(); h.tick(100000);
  assert.equal(h.rendered.length, 1);
  h.player.show(1); h.tick(100000);
  assert.equal(h.player.completed, false);
  h.player.resume(); h.tick(100);
  h.player.destroy(); h.tick(100000);
  assert.equal(h.target.textContent, 'Original');
  assert.equal(h.context.textShow.get(h.target), undefined);
  assert.deepEqual(h.events, []);
  assert.equal(h.timers.size, 0);
});

test('long sentences have uncapped reading time after their last word animation', () => {
  const h = harness();
  assert.ok(h.context.textShow.duration('word '.repeat(200).trim()) >= 43740);
  assert.ok(h.context.textShow.words('<script> &').includes('&lt;script&gt;'));
  assert.equal(h.context.textShow.split('Un mesaj. Alt mesaj!', 'ro').length, 2);
});

test('single sentences complete and independent instances cannot cancel each other', () => {
  const h = harness({ text: ['Only.'] });
  const other = harness();
  other.player.pause();
  h.tick(h.player.remaining);
  assert.equal(h.player.completed, true);
  assert.equal(other.player.completed, false);
});

test('a loading gate retains the first frame and starts once the shared view is ready', () => {
  let ready = false;
  const h = harness({ ready: () => ready });
  h.tick(100000);
  assert.deepEqual(h.rendered, []);
  ready = true; h.player.refresh(); h.tick(1000);
  const remaining = h.player.remaining;
  ready = false; h.player.refresh(); h.tick(100000);
  assert.equal(h.player.remaining, remaining);
  ready = true; h.player.refresh(); h.tick(remaining);
  assert.deepEqual(h.rendered, ['First.', 'Last.']);
});

test('before intersection the default renderer keeps readable text instead of an empty card', () => {
  const h = harness({ whenVisible: true, render: null });
  assert.match(h.target.innerHTML, /class="text-show-frame is-current">First\./);
  assert.equal(h.target.dataset.textShowState, 'waiting');
  assert.equal(h.timers.size, 0);
});

test('looping book-page playback wraps while finite featured playback completes', () => {
  const looping = harness({ loop: true, duration: () => 100 });
  const finite = harness({ loop: false, duration: () => 100 });
  looping.tick(650); finite.tick(650);
  assert.deepEqual(looping.rendered, ['First.', 'Last.', 'First.', 'Last.', 'First.', 'Last.', 'First.']);
  assert.equal(looping.player.completed, false);
  assert.deepEqual(looping.events, []);
  assert.equal(finite.player.completed, true);
  assert.deepEqual(finite.events, ['textshow:complete']);
});

test('an empty presentation completes once without leaving a waiting lifecycle', () => {
  const h = harness({ text: [] });
  assert.equal(h.player.completed, true);
  assert.equal(h.target.dataset.textShowState, 'complete');
  h.player.refresh(); h.player.start(); h.tick(100000);
  assert.deepEqual(h.events, ['textshow:complete']);
});
