# Aspirin, Viagra, and Coffins — book introduction

English narrated SHF preview, **12:11**, 14 chapters and 98 complete single-sentence narration clips. This is an invitation to read edition 1, with substantive samples and concrete starting points; it is not a complete summary or a product demonstration.

## Direction and source

The editable script and illustrations are in `work/scenes.json` and `work/art.mjs`. Source extraction, hashes and offset-indexed units are in `source/`. `work/editorial.json` records exact supporting spans, why/how/what, reader gains, retained qualifications and deliberate omissions. All canonical source text was extracted. Editorial reading covered the chapter map, chapter openings and endings, central argument, conclusion, strongest qualifications and selected supporting examples; it was not an independent audit of the bibliography.

Visual identity: Editorial market theatre. Flat Color, Light and Dark variants use the shared Red Hat Display and Red Hat Text fonts. Custom vectors keep semantic roles explicit and do not use a recurring human presenter or a copied book-film layout. Image inspection and adaptation decisions are recorded in `work/visual-bible.json`.

## Narration and timing

Prepared local Piper `en_US-ljspeech-medium`, pace 0.94, no tempo acceleration, MP3 64 kbps. Model card: `qa/voice-model-card.txt`. Receipts bind each recording to its text and file hash. The measured timeline leaves 1.55 seconds between sentences, with longer scene transitions; see `qa/pacing.json`. No music was added to compete with technical distinctions. Emotional changes are authored in wording, scene direction and purposeful visual reveals. Piper does not provide fine-grained acted delivery.

## Checks actually performed

- Source span/hash validation and 98 one-sentence clip checks.
- All 98 audio assets decoded using OfflineAudioContext, with no output device or audible playback.
- First/middle/last sampling for every scene in all three themes: 126 frames, finite geometry, resolved color tokens and connected ports.
- All 98 captions and transport bounds at 1200, 720, 393 and 320 CSS pixels.
- Deterministic A→B→A seeking and offline `file://` standalone loading.
- Visual inspection of all-scene middle contact sheets in Color, Light and Dark and representative phone frames; modified scenes received an additional first/middle/last pass.
- Final source, script, SHF and voice hash evidence in `qa/provenance-check.json`.

The automation and visual review passed. Human listening, full continuous viewing, physical-device testing and independent verification of the source bibliography remain unperformed. This package is marked **preview**, not independently certified publication-ready.

## Build and delivery

```sh
node presentations/aspirin-viagra-and-coffins/work/art.mjs
node presentations/aspirin-viagra-and-coffins/render_voice.mjs
node presentations/aspirin-viagra-and-coffins/build.mjs
node tools/shf/qa-film.mjs presentations/aspirin-viagra-and-coffins
```

The shared compiler/runtime live at site level. Public content is `docs/books/aspirin/viagra/and/coffins/bk-9a2dd3c2a55341db/Animation/aspirin-viagra-and-coffins-introduction.shf`; its minimal entry is generated from the manifest by the site build. Portable HTML and VTT are in ignored `exports/`. The book's canonical reader and other editions are unchanged.
