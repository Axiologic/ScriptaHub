# Anti-Trivialization Machines of the Future — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/anti/trivialization/machines/of/the/future/bk-41f22d81e81142ed/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `dfb9b1991df08c2d803402a5199d4d52945d590843f4d8ac514d13d8b9616228`.
- Duration: **2:59** (179331 ms), five chapters, 23 single-sentence narration clips.
- Voice: locally prepared Piper `en_US-ljspeech-medium`, pace 0.96, normal playback speed; English text and captions. No browser speech or API key.
- Pauses: measured clips followed by 1.20s authored silence plus 0.15s spacing; longer scene endings.
- Public film: `docs/books/anti/trivialization/machines/of/the/future/bk-41f22d81e81142ed/Animation/anti-trivialization-machines-of-the-future-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` contains this book's original vector staging. Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root:

```sh
node presentations/anti-trivialization-machines-of-the-future/art.mjs
node presentations/anti-trivialization-machines-of-the-future/render_voice.mjs
node presentations/anti-trivialization-machines-of-the-future/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/anti-trivialization-machines-of-the-future
```

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Validation passed: all 23 audio clips decoded in an OfflineAudioContext;45 sampled frames across all three themes;21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.

## Reviewed replacement — 2026-09-10

The approved replacement demonstrates a user-defined interruption policy before introducing inspectable assistant objectives and a future-impact ledger. Conditional proposal wording and user override remain explicit. The reading invitation names two actual chapters. Original art moves from a study alcove to a policy boundary, examination tutor, changing civic landscape and shared reading terrace.

All 45 settled Color/Light/Dark frames were visually inspected; 21 browser checks passed with zero caption overlaps or JavaScript errors. All 23 clips decoded without an audio device. The shared QA runner now creates a fresh owned player per theme and waits 220ms for the compositor after seeking, fixing stale screenshot tiles without changing player behavior. Source edition/hash still match. No listening-review claim; preview status preserved.

Installed SHF SHA-256: `d89528f4e0fb5a902034ccf31ecff3aa447038b3b4670601841a185ef58b508c`. Detailed provenance and review scope: `review-revision/QA.json`.
