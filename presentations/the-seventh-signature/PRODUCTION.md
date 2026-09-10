# The Seventh Signature — English narrated introduction

Completed **2:46**, four scenes and 24 single-sentence clips. The public preview flag records pending user listening, not missing narration.

Source: `docs/books/the/seventh/signature/bk-2f19951fbaf34354/en/full_content.html`, `edition-1`, HTML SHA-256 `ae9d71a0fe8f6a173e274547caae034fdad1aab387d5a75bf21c39a05bec1355`. Full text was extracted and indexed; selected chapter-aligned openings, body passages and endings were inspected. This does not claim every word or every chapter was manually reviewed. Exact substantive UTF-16 evidence spans, source hash, chapter map and limitations are retained in working metadata.

Root reviewed the complete book-first WHY→HOW→WHAT script before voice. It establishes genre, distinctive source tension and a specific reading invitation. Fiction resolutions remain outside the film. English narration uses the prepared local Piper `en_US-ljspeech-medium`, pace0.94, no acceleration, measured 1.25-second ordinary gaps and longer scene transitions. Every clip has a text hash, measured audio and separate caption.

Original book-owned staging and choreography are in `work/art.mjs`; reusable typography, rendering and player controls remain shared. Source images were inspected. Covers, small complex conceptual diagrams and an emblem were omitted where they did not improve the enacted composition. Color, Light and Dark were checked; discovered table-position and contrast issues were corrected and rechecked.

All 21 shared silent browser checks passed, including offline decoding of all24 clips,36 first/middle/last frames across allthree themes, deterministic seeking, five caption/control widths, loaded Red Hat Display/Text fonts, source/emotion metadata and zero JavaScript errors. Screenshots are under `qa/screenshots/`. No audible background preview, subjective full listening review, physical-device test or audience study is claimed.

Delivery: `docs/books/the/seventh/signature/bk-2f19951fbaf34354/Animation/the-seventh-signature-introduction.shf`, plus only this book's manifest animation record. Root integration generates the shared-player entry page and aggregate catalogue. Readers and release workspaces were not modified.

```sh
node presentations/the-seventh-signature/work/art.mjs
node presentations/the-seventh-signature/render_voice.mjs
node presentations/the-seventh-signature/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9246 node tools/shf/qa-film.mjs presentations/the-seventh-signature
```

Local browser tests use a private muted instance with external resolution blocked and background services disabled. The visitor controls listening.
