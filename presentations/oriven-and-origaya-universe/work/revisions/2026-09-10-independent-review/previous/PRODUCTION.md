# Oriven and Origaya Universe — English narrated introduction

Completed **2:48**, four scenes and 24 single-sentence clips. The public preview flag records pending user listening, not missing narration.

Source: `docs/books/oriven/and/origaya/universe/bk-86a238b1a6c34443/en/full_content.html`, `edition-1`, HTML SHA-256 `ae0ee6f7f958d9403ee412e47f403aefe8d8dbd9a9cb7634961e26306c59e8b7`. Full text was extracted and indexed; selected chapter-aligned openings, body passages and endings were inspected. This does not claim every word or every chapter was manually reviewed. Exact substantive UTF-16 evidence spans, source hash, chapter map and limitations are retained in working metadata.

Root reviewed the complete book-first WHY→HOW→WHAT script before voice. It establishes genre, distinctive source tension and a specific reading invitation. Fiction resolutions remain outside the film. English narration uses the prepared local Piper `en_US-ljspeech-medium`, pace0.94, no acceleration, measured 1.25-second ordinary gaps and longer scene transitions. Every clip has a text hash, measured audio and separate caption.

Original book-owned staging and choreography are in `work/art.mjs`; reusable typography, rendering and player controls remain shared. Source images were inspected. Covers, small complex conceptual diagrams and an emblem were omitted where they did not improve the enacted composition. Color, Light and Dark were checked; discovered table-position and contrast issues were corrected and rechecked.

All 21 shared silent browser checks passed, including offline decoding of all24 clips,36 first/middle/last frames across allthree themes, deterministic seeking, five caption/control widths, loaded Red Hat Display/Text fonts, source/emotion metadata and zero JavaScript errors. Screenshots are under `qa/screenshots/`. No audible background preview, subjective full listening review, physical-device test or audience study is claimed.

Delivery: `docs/books/oriven/and/origaya/universe/bk-86a238b1a6c34443/Animation/oriven-and-origaya-universe-introduction.shf`, plus only this book's manifest animation record. Root integration generates the shared-player entry page and aggregate catalogue. Readers and release workspaces were not modified.

```sh
node presentations/oriven-and-origaya-universe/work/art.mjs
node presentations/oriven-and-origaya-universe/render_voice.mjs
node presentations/oriven-and-origaya-universe/build.mjs
SCRIPTA_CDP_URL=http://127.0.0.1:9246 node tools/shf/qa-film.mjs presentations/oriven-and-origaya-universe
```

Local browser tests use a private muted instance with external resolution blocked and background services disabled. The visitor controls listening.
