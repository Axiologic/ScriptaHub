# Bias in AI — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/bias/in/ai/bk-c0e43df73f514937/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `ac5bd7e756b3d45733fa98d252c618d334989bea994fd1165a6e20b045ea26a6`.
- Duration: **2:32** (151691 ms), four chapters, 20 single-sentence narration clips.
- Voice: locally prepared Piper `en_US-ljspeech-medium`, pace 0.96, normal playback speed; English text and captions. No browser speech or API key.
- Pauses: measured clips followed by 1.35s authored silence plus 0.15s spacing; longer scene endings.
- Public film: `docs/books/bias/in/ai/bk-c0e43df73f514937/Animation/bias-in-ai-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` contains this book's original vector staging. Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root:

```sh
node presentations/bias-in-ai/art.mjs
node presentations/bias-in-ai/render_voice.mjs
node presentations/bias-in-ai/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/bias-in-ai
```

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Validation passed: all 20 audio clips decoded in an OfflineAudioContext;36 sampled frames across all three themes;21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.

## Source-specific visual and proxy revision

The same matched service requests now reveal unequal research and human escalation behind similar responses. A conceptual clinic-access threshold then shows how spending records can miss care need. Four middle sentences replace the repeated fairness-criteria discussion; sixteen original audio files remain identical. No medical advice, demographic generalization or blanket claim against spending measures is introduced.

Final36theme frames and21browser checks passed with20offline audio decodes, zero caption overlaps and no JavaScript errors. Export uses the updated shared outlined subtitles and size control. Figures retain visible faces and appropriate Night contrast on pale floors. Root reviewed all12finalColorframes. See `review-revision/QA.json` for source scope/hash and limitations, and `before/` for the prior public film/manifest/editable state. No audible playback or complete listening review occurred.
