# Limits of Machine Intelligence — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/limits/of/machine/intelligence/bk-adbbc1dd07be455c/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `9fd18ab16f95f4ceb3b176405b673768c072ec0e841ec3a5fea06a8e0f23f874`.
- Duration: **2:36** (156168 ms), five chapters, 22 single-sentence narration clips.
- Voice: locally prepared Piper `en_US-ljspeech-medium`, pace 0.96, normal playback speed; English text and captions. No browser speech or API key.
- Pauses: measured clips followed by 1.35s authored silence plus 0.15s spacing; longer scene endings.
- Public film: `docs/books/limits/of/machine/intelligence/bk-adbbc1dd07be455c/Animation/limits-of-machine-intelligence-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` contains this book's original vector staging. Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root:

```sh
node presentations/limits-of-machine-intelligence/art.mjs
node presentations/limits-of-machine-intelligence/render_voice.mjs
node presentations/limits-of-machine-intelligence/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9237 node tools/shf/qa-film.mjs presentations/limits-of-machine-intelligence
```

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Validation passed: all 22 audio clips decoded in an OfflineAudioContext;45 sampled frames across all three themes;21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.

## Independent quality revision — 10 September 2026

The root agent approved the complete replacement script and all 15 Color frames before installation. A bounded ten-step toy controller, an eleventh-step counterexample and an explicitly changed stopping guard replace the former abstract qualification sequence. Five shots connect that distinction to the source’s propose/test/deploy permissions and a specific reading chapter. The controller is an original model, not an empirical source experiment. Its exact transition and invariant semantics are retained in `work/editorial.json` and `review-revision/SCRIPT-AND-ART.md`.

The final pass corrected the counterexample label inside its clear backing. All 45 theme/frame samples have no caption overlaps; all 21 browser checks and 22 offline audio decodes passed with no JavaScript errors. The source’s sole image was inspected: it is the cover and contributes no relevant verification diagram. Full listening review remains pending; publication retains preview status.

Installed SHF SHA-256: `05628b58a51995cb493bd2bfc4478b8cffebe28491d51e3d36775f0b44537e80`.
