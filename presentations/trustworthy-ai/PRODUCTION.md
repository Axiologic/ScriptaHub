# Trustworthy AI — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/trustworthy/ai/bk-d50cba248572411d/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `91f9e2731650496dfa95987ec514c0bb7d62d43e767765cb7e7afdb1241d9656`.
- Duration: **2:38** (157758 ms), five chapters, 21 single-sentence narration clips.
- Voice: locally prepared Piper `en_US-ljspeech-medium`, pace 0.96, normal playback speed; English text and captions. No browser speech or API key.
- Pauses: measured clips followed by 1.25s authored silence plus 0.15s spacing; longer scene endings.
- Public film: `docs/books/trustworthy/ai/bk-d50cba248572411d/Animation/trustworthy-ai-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` contains this book's original vector staging. Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root:

```sh
node presentations/trustworthy-ai/art.mjs
node presentations/trustworthy-ai/render_voice.mjs
node presentations/trustworthy-ai/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9237 node tools/shf/qa-film.mjs presentations/trustworthy-ai
```

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Validation passed: all 21 audio clips decoded in an OfflineAudioContext; 45 sampled frames across all three themes;21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.

## Source-specific quality revision

The new introduction follows the fictional Meridian course case through a policy-source fallback, a changed repository with unchanged model and stale evidence, an actual release hold, and a bounded assurance argument. It identifies the engineering reading gain in the opening scene. Source retrieval is not treated as proof of factual entailment, and renewed checks receive no pass stamp. Original peacock, apricot and coral workroom staging replaces generic prop arrangements. The prior public film, manifest and editable directions are retained in `review-revision/before/`.

The source scope, exact hash, approvals and validation limits are recorded in `review-revision/QA.json`. Final visual evidence uses uniquely named `verified-*-20260910-v4.png` contacts because overwritten JPG previews appeared incomplete while the same raw captures were intact. No runtime remedy was inferred from that preview artifact. Narration was decoded silently; no complete listening review or audible background playback occurred.
