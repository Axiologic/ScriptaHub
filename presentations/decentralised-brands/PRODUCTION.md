# Decentralised Brands — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/decentralised/brands/bk-201d0531859c4e42/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `a5290be35cc2b16a7c28df240815dc82de05ba136b1386d41e2c5c45506bffca`.
- Duration: **2:43** (162646 ms), four chapters, 20 single-sentence narration clips.
- Voice: locally prepared Piper `en_US-ljspeech-medium`, pace 0.96, normal playback speed; English text and captions. No browser speech or API key.
- Pauses: measured clips followed by 1.35s authored silence plus 0.15s spacing; longer scene endings.
- Public film: `docs/books/decentralised/brands/bk-201d0531859c4e42/Animation/decentralised-brands-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` contains this book's original vector staging. Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root:

```sh
node presentations/decentralised-brands/art.mjs
node presentations/decentralised-brands/render_voice.mjs
node presentations/decentralised-brands/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/decentralised-brands
```

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Validation passed: all 20 audio clips decoded in an OfflineAudioContext;36 sampled frames across all three themes;21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.
