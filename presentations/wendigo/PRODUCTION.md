# Wendigo — SHF production

English narrated book introduction, **11:47**, 14 scenes and 98 individually recorded sentences. The public film is a preview pending user-initiated listening review.

- Source: `docs/books/wendigo/bk-77cfd00121094963/en/full_content.html`, catalogue `edition-1`. HTML SHA-256: `04852453ac91c35ccbc928f538928b786806ab98d94cecfb5a0b90b4038121be`.
- Source review: chapter-aligned coverage and detailed selected passages, not a claim that every word was manually reviewed. See `work/chapter-map.json`, `source/chapter-review-extracts.json` and `qa/source-review.json`.
- Purpose: explain why this specific book deserves reading through book/content/reader lenses and a concrete opening chapter. Later fiction resolutions remain private.
- Art: original book-specific vector direction in `work/art.mjs`; imagery decisions and source adaptations in `work/visual-bible.json`. Shared Red Hat Display/Text fonts and player remain site-owned.
- Narration: prepared local Piper `en_US-ljspeech-medium`, pace 0.94, no tempo acceleration, MP3 64 kbps. Model rights card retained in `qa/voice-model-card.txt`. Piper does not implement detailed emotional acting instructions.
- Timing: actual decoded clips drive the final timeline; 1,550 ms between ordinary sentences including scheduling gap, longer scene changes. Exactly one sentence per clip and caption.

## Files and rebuild

Published essentials: `docs/books/wendigo/bk-77cfd00121094963/Animation/wendigo-introduction.shf` and generated shared-player entry page. Standalone HTML and VTT are in ignored `exports/`. Working source, script, editorial plan, direction, scores and voice receipts remain here; local model and audio caches stay ignored.

```sh
node presentations/wendigo/work/art.mjs
node presentations/wendigo/render_voice.mjs
node presentations/wendigo/build.mjs
node tools/shf/qa-film.mjs presentations/wendigo
```

The root integration agent regenerates the aggregate catalogue and entry pages once with `build_books.py refresh`; individual production agents do not race the generator.

## Verification

Source-hash/editorial validation, one-sentence checks, measured audio retiming and SHF structural validation passed. Silent standalone browser review decoded all 98 clips in an OfflineAudioContext, sampled 126 first/middle/last frames across Color/Light/Dark, checked captions and transport at 1200, 720, 540, 393 and 320 pixels, and checked deterministic seeking. No audible output was opened. Agent visual review inspected all-theme contact sheets and phone layout; per-frame screenshots and exact automation results are in `qa/`.

No full listening review, physical-device test, audience comprehension study or rights/citation audit is claimed. Existing catalogue/release work was preserved; only this book's animation manifest field was added.

Final integration also passed through each Romanian book page: the Animation action preserves `?lang=ro`, opens the dedicated page, and loads an English film paused without production boilerplate. Independent agent script review found no material narration, genre-fit or fiction-spoiler issue; its provenance findings were corrected without regenerating audio.
