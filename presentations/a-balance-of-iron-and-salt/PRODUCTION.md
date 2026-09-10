# A Balance of Iron and Salt — narrated SHF introduction

Finished English narration, **6:09**, eight scenes and 56 individual sentence clips. Public preview status records the pending user listening review, not unfinished audio.

- Canonical source: `docs/books/a/balance/of/iron/and/salt/bk-bc50aebc325a41a6/en/full_content.html`, `edition-1`. HTML SHA-256 `30c58448f95e7a1d63b92260b59fd4f76f3eea1984931397ab6d42103e15b344`; exact text hash and UTF-16 prose-span claims retained in source/editorial files.
- Reading scope: full semantic extraction and heading index; chapter-aligned opening/end coverage with selected deeper passages, including endings to protect discoveries. This does not claim every word was manually read. See `source/chapter-review-extracts.json`, `work/chapter-map.json`, and `qa/source-review.json`.
- Purpose: source-specific book-first WHY→HOW→WHAT invitation, with explicit genre, concrete opening, distinctive treatment and reading gains. Root reviewed all complete scripts before voice; repeated withholding boilerplate and generic instructions were revised.
- Art: original geometry and composition in `work/art.mjs`, with source-specific material vocabulary. Covers inspected; no interior source diagrams/photos were present. Foreground scale, spatial staging, consequential movement, and theme contrast received iterative review. Reusable typography, authoring primitives and runtime remain site-owned.
- Voice: local Piper `en_US-ljspeech-medium`, pace0.94, no tempo acceleration. Model card retained. Each recording has a text hash and measured duration; scores, receipts and editable English script remain in this workspace.
- Actual ordinary sentence gaps: **1400ms**; transitions are longer. Exactly one sentence per clip and caption. Final measured duration is within the requested5–10minutes.

## Verification

All 21 shared silent browser checks passed: all56 clips decoded using OfflineAudioContext,72 first/middle/last frames across Color/Light/Dark, deterministic seeking, loaded bundled Red Hat Display/Text, source and emotion metadata, five caption/control widths1200/720/540/393/320, and zero JavaScript errors. Per-frame screenshots and phone layouts are in `qa/screenshots/`. All-theme contact inspection checked staged compositions and exposed layering defects that were corrected and rechecked where applicable.

No audible background preview, full listening review, physical-device test or audience-comprehension study is claimed. The player remains paused for the visitor to start listening.

## Delivery and rebuilding

Only `docs/books/a/balance/of/iron/and/salt/bk-bc50aebc325a41a6/Animation/a-balance-of-iron-and-salt-introduction.shf` is published by this workspace, plus its own manifest's animation field. Root integration regenerates the shared-player entry page and aggregate catalogue. No reader, release workspace, historical source or unrelated manifest field was deliberately changed.

```sh
node presentations/a-balance-of-iron-and-salt/work/art.mjs
node presentations/a-balance-of-iron-and-salt/render_voice.mjs
node presentations/a-balance-of-iron-and-salt/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9246 node tools/shf/qa-film.mjs presentations/a-balance-of-iron-and-salt
```

Standalone HTML and VTT exports, speech audio and caches remain in ignored working outputs. Production metadata stays out of the public film shell.
