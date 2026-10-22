# Coherence Pressure — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/coherence/pressure/bk-5e790be3de5d4533/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `447e51829f4ea854ab5d56d2b89a1a024d1f810eb7d7d317a8567a9edc4638a8`.
- Duration: **1:04** (63929 ms), four chapters, 8 single-sentence narration clips.
- Voice: local Qwen3-TTS 1.7B CustomVoice / Ryan (see `work/production.json`); English text and captions. No browser speech or API key. The earlier 6:38 Piper film was replaced on 2026-10-22.
- Pauses: 1.35 s between sentences, 3.75 s scene transitions (`qa/pacing.json`).
- Public film: `docs/books/coherence/pressure/bk-5e790be3de5d4533/Animation/coherence-pressure-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` is this book's authoritative vector staging (round-4 repair; earlier versions are archived in `review-revision/round{1,2,3,4}-previous/`). Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root (staging only; this never touches the public book folder):

`art.mjs` is the single authoritative art entry. It regenerates every `scene.visual` in `work/scenes.json` and leaves narration lines and audio untouched. The superseded box-diagram generator and `layout-repair.mjs` are archived in `review-revision/round1-previous/` and must not be run.

```sh
node presentations/coherence-pressure/art.mjs
node presentations/coherence-pressure/build.mjs --output=/path/to/staging   # note the "=": a bare --output or no flag publishes to the book
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/coherence-pressure
```

A staging build still writes `exports/coherence-pressure-introduction.html`, `qa/build.json`, `qa/validation.json` and `work/film.direction.json` in this project; `qa-film` reads that export and writes `qa/browser-review.json` and `qa/screenshots/`. Running `build.mjs` without `--output=` publishes to `docs/books/…/Animation/` and is reserved for after the independent visual review passes.

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Historical (Piper 6:38 film) validation: all 54 audio clips decoded in an OfflineAudioContext; 81 sampled frames across all three themes; 21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.

## 2026-10-22 layout repair and publication

Expanded QA (every spoken-sentence midpoint) had found the scene 2 Question / Still uncertain card in the caption band. `layout-repair.mjs` re-laid out all four scenes: no boxes overlap, the child and reader figures and every card stay clear of two-line captions, the Shared room and Reading table subtitles are no longer covered, and the duplicated scene 1 record now reads Conversation / The original record. Narration text and voice clips are unchanged. Browser QA passed (23 checks, 48 frames, art `7e780caa…`); contact sheets for all three themes and the full-size sentence frames were inspected. The repair review is recorded in `qa/visual-plan-review.json`, which keeps the earlier independent review. The listening review is still pending.

## 2026-10-22 round-1 visual repair (staged, not published)

The independent reviewer failed the box-diagram art. `art.mjs` now redraws all four scenes as illustrated situations with the rigged person library (stable cast, per-sentence `character.express`, `character.gesture` and `lookAt`):

- Cast: parent (person-11, cobalt coat), child (person-15, rust coat, scale 0.66), reader (person-20, teal coat, grey hair). Each has its own Night coat, trouser and hair colours, so no two figures merge in Dark. The coat-placket hairline and ground shadow are removed.
- Scene 1: the parent by a family table with a tablet (unwanted app with a removal cross) and a phone of short videos. The connection is a dashed arc whose ends touch both devices, with a question-mark badge. There is no causal arrow. The child appears on sentence 2, recoils from the app, then turns happily back to the videos.
- Scene 2: the parent, seated, reads the model's reply on a laptop. A solid bridge whose ends touch the tablet and phone appears under the words "attention / choice"; on sentence 2 it opens into the dashed, questioned arc while the parent turns sceptical, hand raised. This makes five salient objects, and the outlined cards are gone.
- Scene 3: a worried reader with the questioned arc under a magnifying glass. On sentence 2 the book *Coherence Pressure* appears with a question sticker, and the same glass moves onto it. The floating arrow is removed.
- Scene 4: the reader holds the original conversation (chat bubbles) in one hand and the polished explanation (neat lines and a seal) in the other. The book lies open on a reading table. On sentence 2 the reader settles and a question mark rises. The arrow that ended in a gap is removed. The unimplemented finger cue was replaced in `work/presentation-plan.json` by this two-handed comparison.
- In-art text is limited to "attention / choice" (40 px) and the cover title (about 31 px effective). The central play overlay on phones now covers only empty stage.
- Plan keep/remove lists and cues were updated to these actors (the previous plan is archived). `sentencePerformance` gesture notes now match the staging. Spoken lines, voice clips and timings are unchanged (script hash `b65c9d4b…`).

Staged QA (muted, paused, OfflineAudioContext decode only): 23/23 checks, 48 frames, 8/8 clips, no caption or label collisions, art `d669d162…`. All 24 sentence frames in Color, Light and Dark, the first and last frames, and phone captures at 393 and 320 px were inspected. Contact sheets: `qa/{color,paper,night}-contact.png`. `qa/visual-plan-review.json` still records the failed review and must be refreshed by the independent reviewer before publication.

## 2026-10-22 round-2 visual repair (staged, not published)

The independent reviewer failed round 1 on expressions and gestures (transient rig gestures had returned to rest by each sentence midpoint, the library `curious` mouth reads as a frown, `reflect` raised the hand above the shoulder). `art.mjs` now:

- **Held arm poses.** Each person keeps empty `armL`/`armR` rig groups (for `lookAt` and faces). Every visible arm is its own top-level object (`<person>-arm-<l|r>-<pose>`) drawn on the person's x/y/scale/build and cross-faded between poses, so a pose is held for the whole sentence. No `character.gesture` actions remain. Plan `keep` lists include these arm objects.
- **Faces (book-local overrides of the dynamic expressions).** `curious`: raised brows, relaxed, slightly open mouth. `skeptical`: one arched brow, the other eye narrowed by a skin-coloured lid, flat mouth. `relieved` is used as a calm, attentive face. Brows are thicker so they read on darker skin.
- **Scene 1.** Sentence 1: the parent, curious, looks toward the phone and holds an open questioning hand toward the devices. Sentence 2: she turns to the child with a palm-up invitation. The child frowns and pushes the app away, then at the midpoint has turned head and gaze to the phone, smiling, stepping toward it and reaching. The white collar bar (`button` collar of person-15) is removed.
- **Scene 2.** Devices, bridge and words moved closer to the laptop. Sentence 1: the parent leans in with an explaining hand on the laptop reply, held through the midpoint, then looks up at the bridge. Sentence 2: sceptical face, hand under the chin with the other forearm folded, gaze up at the questioned arc.
- **Scene 3.** The reader stands between the questioned bridge (left) and the book (right). Sentence 1: worried, one arm points across at the magnified bridge, the other hand is open. Sentence 2: the book appears beside the reader; calm face, gaze and pointing hand on the book as the magnifier moves onto it. The magnifier handle no longer overlaps the phone.
- **Scene 4.** Sentence 2: arms and pages lower, the reader steps toward the open book and looks at it, curious, while the question mark rises. The open book's pages are cream (`#f0e0bd`) in the Light/paper theme.
- `sentencePerformance.gesture` notes and `work/presentation-plan.json` cues/keep lists match this staging; the round-1 plan and scenes are archived in `review-revision/round2-previous/`. Spoken lines, voice clips and timings are unchanged (script hash `b65c9d4b…`).

Staged QA (muted, paused, no audible playback): `build.mjs --output=<scratch>` then `qa-film`: 23/23 checks, 48 frames, 8/8 clips, no caption or label collisions, art `177698ae…`. All sentence midpoints plus first/last frames in Color, Light and Dark, the phone captures, close-ups of the faces, and transition frames (the child's push-away at about 1.1 s into scene 1 sentence 2) were inspected. Contact sheets: `qa/{color,paper,night}-contact.png` (columns: first, sentence 1, sentence 2, last). `qa/visual-plan-review.json` still records the failed review and must be refreshed by the independent reviewer before publication.

## 2026-10-22 round-3 visual repair (staged, not published)

Fixes for review r2-1 … r2-5; the round-2 `art.mjs`, `work/scenes.json` and `work/presentation-plan.json` are archived in `review-revision/round3-previous/`.

- **r2-1 Dashes.** `openBridge` derives `stroke-dasharray` from each curve's measured length (14 px dashes, 20 px gaps, so 13 px stay clear between the 7 px round caps). The scene 2 questioned arc now has clean dashes matching scenes 1 and 3.
- **r2-2 Warm smile.** Scene 4 sentence 1 uses the book-owned `inspired` face: a closed warm smile with softly raised, rounded brows (no open grin).
- **r2-3 Step to the table.** Scene 4 pages are placed from each hand position so the hand overlaps the page's inner edge at mid-height. In sentence 2 the reader lowers the pages and walks from x 400 to 552; the polished page reaches the reading table (x 755) and his gaze goes to the open book.
- **r2-4 Aim at the lens.** Scene 3 devices sit low and the questioned bridge arches high, with the magnifier over its apex (370, 164). The reader (x 790) raises an arm with an index finger aimed up at the lens past the phone, and `lookAt` targets the magnifier. Pupils are now centred in the eyes film-wide (the library offset them 2 px right), so left and upward gaze reads clearly. The book and sticker shift to x 985/997.
- **r2-5 Desk.** The scene 2 desk top is 252 px wide, wider than the 224 px laptop base.

Spoken lines, voice clips and timings are unchanged (script hash `b65c9d4b…`).

Reproduce (repository root): `node presentations/coherence-pressure/art.mjs`, then `node presentations/coherence-pressure/build.mjs --output=<scratch dir>`, then `SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/coherence-pressure`. Staged QA (muted, paused, no audible playback): 23/23 checks, 48 frames, 0 errors, art `6c810140…`. Sentence midpoints in Color, Light and Dark and face close-ups were inspected. `qa/visual-plan-review.json` still records the failed review and must be refreshed by the independent reviewer before publication.

## 2026-10-22 round-4 visual repair (staged, not published)

Fixes for review r3-1 and r3-2; the round-3 `art.mjs`, `work/scenes.json` and `work/presentation-plan.json` are archived in `review-revision/round4-previous/`.

- **r3-1 No ghost arms.** `swap()` no longer cross-fades. The old pose fades out in 120 ms, and the new pose starts 130 ms after the swap and fades in over at most 320 ms, so two poses of one arm are never visible together. This applies to every swap in all four scenes. A browser scan of every arm object at 20 ms steps over the whole film found no moment with two visible poses of the same arm.
- **r3-2 Inviting hand.** The scene 1 sentence 2 `invite` forearm now rises toward the child (who stands right of the tablet), and ends in an open, palm-up hand with a raised thumb instead of a closed round hand.

Spoken lines, voice clips and timings are unchanged (script hash `b65c9d4b…`). Staged QA (muted, paused, no audible playback): `art.mjs`, `build.mjs --output=<scratch dir>`, then `qa-film`: 23/23 checks, 48 frames, 0 errors, art `295e9b9b…`. Frames at 10, 20, 30 and 50% into every sentence were inspected in Color, Light and Dark. The public film in `docs/books/…/Animation/` was not rebuilt. `qa/visual-plan-review.json` must be refreshed by the independent reviewer before publication.

## 2026-10-22 round-5 visual repair (staged, not published)

Fixes the independent review's scene 3 sentence 2 defect; the round-4 `art.mjs`, `work/scenes.json` and `work/presentation-plan.json` are archived in `review-revision/round5-previous/`.

- **Magnifier path.** The glass no longer travels in a straight line through the reader. x and y are keyed separately. The glass rises to y 150 and crosses above the reader's head, then drops onto the book (x 997, y 447) only after it is past him. y 150 keeps the lens below the scene title and the handle above his head. A browser scan at 40 ms steps over the first 2.5 s of the sentence, in all three themes, found no overlap with the reader's head or body bounding boxes and none with the scene title. The minimum clearances were 14 px from the head and 13 px from the title.
- **Scene 1 sentence 1.** The parent's `ask` arm now ends in the same open, palm-up hand with a raised thumb as the `invite` pose, instead of a closed round hand.

Spoken lines, voice clips and timings are unchanged. Staged QA (muted, paused, no audible playback): `art.mjs`, `build.mjs --output=<scratch dir>`, then `qa-film`: 23/23 checks, 48 frames, 0 errors, art `2a60bde6…`. Transition frames and frames at 10–30% of the sentence were inspected in Color, Light and Dark. The public film was not rebuilt. `qa/visual-plan-review.json` must be refreshed by the independent reviewer before publication.

## 2026-10-22 publication of the round-5 art

The independent reviewer (`independent-reviewer-r5`) passed the round-5 art `2a60bde6…` with no major or moderate defects (`qa/visual-plan-review.json`). `node presentations/coherence-pressure/build.mjs` (no `--output`) installed `docs/books/coherence/pressure/bk-5e790be3de5d4533/Animation/coherence-pressure-introduction.shf`, SHA-256 `95c7ffe8dd7a695b65761ecb4eae82b0e566be80fafaa09bf11a5d44d5fbe68d`, identical to the reviewed staged build. Duration **1:04** (63929 ms), four scenes, 8 sentences. Browser QA after install (muted, paused, no audible playback): 23/23 checks, 48 frames, 0 errors, art `2a60bde6…`. Spoken lines, voice clips and timings are unchanged (script hash `b65c9d4b…`). `work/migration-state.json` marks the animation `published`.

Minor residual items (optional polish, not blocking):

- r5-1: during pose swaps an arm (and in scene 4 the held pages) is faint for about 140–160 ms before the new pose fades in.
- r5-2: during its 41.4–41.7 s descent the opaque lens briefly covers part of the cover word "Coherence"; at rest the title is clear.
- r5-3: at 393/320 px the in-art "attention / choice" label is about 10 px, legible and redundant with the caption.

The listening review is still pending.
