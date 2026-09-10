# RAG and EPR — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/rag/and/epr/bk-b5f873f3cb414ffc/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `5abee5f7cdfcf12b7589a92a68b499a9b272863a63918cb3bdbaad527de98bc1`.
- Duration: **2:36** (156124 ms), four chapters, 20 single-sentence narration clips.
- Voice: locally prepared Piper `en_US-ljspeech-medium`, pace 0.96, normal playback speed; English text and captions. No browser speech or API key.
- Pauses: measured clips followed by 1.35s authored silence plus 0.15s spacing; longer scene endings.
- Public film: `docs/books/rag/and/epr/bk-b5f873f3cb414ffc/Animation/rag-and-epr-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` contains this book's original vector staging. Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root:

```sh
node presentations/rag-and-epr/art.mjs
node presentations/rag-and-epr/render_voice.mjs
node presentations/rag-and-epr/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/rag-and-epr
```

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Validation passed: all 20 audio clips decoded in an OfflineAudioContext;36 sampled frames across all three themes;21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.

## Source-grounded visual revision

The source manuscript-review proposal now remains visible across repeated retrieval coverage, complementary component evidence, a finite portfolio and equal-budget comparison. Four evidence places are illustrative; roles remain provisional and no method is declared the winner. Nineteen recorded clips are preserved and one example sentence is replaced. Full revised script and evidence are in `review-revision/SCRIPT-AND-ART.md` and `work/editorial.json`. Prior public film, manifest and report are archived under `review-revision/before/`. Final silent QA passed 21 checks, 36 frames, 20 decoded clips and zero caption overlaps. Exact hashes and scoped visual-inspection limits are in `qa/targeted-revision-review.json`.
