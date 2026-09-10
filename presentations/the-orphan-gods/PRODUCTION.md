# The Orphan Gods — narrated SHF introduction

Finished English narration, **6:05**, eight scenes and 56 individual sentence clips. Public preview status records the pending user listening review, not unfinished audio.

- Canonical source: `docs/books/the/orphan/gods/bk-724ce01f69434f48/en/full_content.html`, `edition-1`. HTML SHA-256 `6ddfcdc30510dac2a8f367e995b9aad1ed49c27cb9789a6be90e00ff137b996b`; exact text hash and UTF-16 prose-span claims retained in source/editorial files.
- Reading scope: full semantic extraction and heading index; chapter-aligned opening/end coverage with selected deeper passages, including endings to protect discoveries. This does not claim every word was manually read. See `source/chapter-review-extracts.json`, `work/chapter-map.json`, and `qa/source-review.json`.
- Purpose: source-specific book-first WHY→HOW→WHAT invitation, with explicit genre, concrete opening, distinctive treatment and reading gains. Root reviewed all complete scripts before voice; repeated withholding boilerplate and generic instructions were revised.
- Art: original geometry and composition in `work/art.mjs`, with source-specific material vocabulary. Covers inspected; no interior source diagrams/photos were present. Foreground scale, spatial staging, consequential movement, and theme contrast received iterative review. Reusable typography, authoring primitives and runtime remain site-owned.
- Voice: local Piper `en_US-ljspeech-medium`, pace0.94, no tempo acceleration. Model card retained. Each recording has a text hash and measured duration; scores, receipts and editable English script remain in this workspace.
- Actual ordinary sentence gaps: **1400ms**; transitions are longer. Exactly one sentence per clip and caption. Final measured duration is within the requested5–10minutes.

## Verification

All 21 shared silent browser checks passed: all56 clips decoded using OfflineAudioContext,72 first/middle/last frames across Color/Light/Dark, deterministic seeking, loaded bundled Red Hat Display/Text, source and emotion metadata, five caption/control widths1200/720/540/393/320, and zero JavaScript errors. Per-frame screenshots and phone layouts are in `qa/screenshots/`. All-theme contact inspection checked staged compositions and exposed layering defects that were corrected and rechecked where applicable.

No audible background preview, full listening review, physical-device test or audience-comprehension study is claimed. The player remains paused for the visitor to start listening.

## Delivery and rebuilding

Only `docs/books/the/orphan/gods/bk-724ce01f69434f48/Animation/the-orphan-gods-introduction.shf` is published by this workspace, plus its own manifest's animation field. Root integration regenerates the shared-player entry page and aggregate catalogue. No reader, release workspace, historical source or unrelated manifest field was deliberately changed.

```sh
node presentations/the-orphan-gods/work/art.mjs
node presentations/the-orphan-gods/render_voice.mjs
node presentations/the-orphan-gods/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9246 node tools/shf/qa-film.mjs presentations/the-orphan-gods
```

Standalone HTML and VTT exports, speech audio and caches remain in ignored working outputs. Production metadata stays out of the public film shell.
