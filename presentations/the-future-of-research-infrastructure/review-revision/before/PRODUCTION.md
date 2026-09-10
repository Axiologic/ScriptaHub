# The Future of Research Infrastructure — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/the/future/of/research/infrastructure/bk-8b99cea752394379/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `2e8eff4b86dcb7bf02e07285d071feb1ce01ad9a0ae2902eb276f71e7e85a9f1`.
- Duration: **2:44** (163840 ms), four chapters, 20 single-sentence narration clips.
- Voice: locally prepared Piper `en_US-ljspeech-medium`, pace 0.96, normal playback speed; English text and captions. No browser speech or API key.
- Pauses: measured clips followed by 1.35s authored silence plus 0.15s spacing; longer scene endings.
- Public film: `docs/books/the/future/of/research/infrastructure/bk-8b99cea752394379/Animation/the-future-of-research-infrastructure-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` contains this book's original vector staging. Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root:

```sh
node presentations/the-future-of-research-infrastructure/art.mjs
node presentations/the-future-of-research-infrastructure/render_voice.mjs
node presentations/the-future-of-research-infrastructure/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/the-future-of-research-infrastructure
```

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Validation passed: all 20 audio clips decoded in an OfflineAudioContext;36 sampled frames across all three themes;21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.
