# Concordia Series — English narrated introduction

Current film: **1:19.9** (79,890 ms), four scenes and eight single-sentence clips, published 2026-10-22. It replaces the earlier 2:43 Piper preview (24 clips). The manifest status remains `preview`; no human listening review is claimed.

Source: `docs/books/concordia/series/bk-7a56d2d893d34260/en/full_content.html`, `edition-1`, HTML SHA-256 `2b811d97caa6dde9907b4470fd685ac37693be84fc7ad71f2b7de90e21515c84`. Selected chapter-aligned passages were inspected; evidence spans, chapter map and limitations are in working metadata. Fiction resolutions remain outside the film.

Narration: local Qwen3-TTS 1.7B CustomVoice / Ryan, directed pace 0.93, no acceleration; receipts in `work/voice-receipts.json`. Measured sentence gaps 1.35 s, scene transitions 3.75 s (`qa/pacing.json`). The older Piper clips `*-line-3..6.mp3` in `work/audio/` belong to the retired script and are not packaged.

ASR (`tools/shf/check-spoken-audio.py`, faster-whisper base.en, `qa/spoken-audio-review.json`): six clips exact; `inside-the-seminar-line-1` heard "it's" for "its" (homophone); `a-civilization-that-sleeps-together-line-1` heard "class may choose us" for "classmate chooses" with low word confidence (0.28/0.11); a prompted decode recognised "classmate chooses" over the same 4.42–5.42 s span. `who-frames-the-answer-line-2` has four comma pauses of 0.6–0.9 s inside the sentence. These are listening-review items, not verified defects.

Art (round-2 history; its arm gestures, recoil and face shapes are superseded by the round-3 repair below): book-owned staging in `work/art.mjs` (regenerates the `visual` of every scene in `work/scenes.json`; spoken lines, pauses and audio are untouched). Round-2 redesign (2026-10-22, after the independent review failure) replaced the seminar room ring, labelled cards and unrigged students:

- Continuous cast built from rigged library people with `dynamicExpressions` and per-character Dark coat/trouser tints: Len Aro (green coat, beard) and his daughter Nia in her clinic bed (SEED-9, Lacuna Ward), Nadir (amber coat, curls, manual mode), Mara (violet coat, long hair; assisted), Suri (blue, glasses, bun) and Lio (mustard). Concordia is a soft matte-blue circle with motes, never a face or machine.
- Every sentence has motivated `character.express`, `character.gesture` and `lookAt` cues: s1.1 Len relieved and reaching toward Nia as care particles appear, then worried with a hesitating hand; s1.2 Concordia appears and threads reach Nia's care and Mara's speech bubble, Len looks up curious; s2.1 medicine, book, speech and a warm bowl arrive clause by clause around a relieved Mara; s2.2 the remedy drifts to Nadir, who reaches, then recoils worried while Mara turns in concern; s3.1 three assisted classmates at individual desks receive smooth bubbles while Nadir, curious, thinks by hand; s3.2 the source pair “surveillance” → “systemic visibility” (Noema seminar, Quiet's recommendation for the general layer) with Nadir skeptical/questioning and Mara explaining; s4.1 a closer bedside, Len's relief turns to unease at the monitor's unfamiliar pale green; s4.2 Noema's classroom, Nadir pauses beside a hovering reformulation and invites with an open hand.
- Flat background in all themes; Light gives pale materials a visible tint, Dark hides decorative halos. Plan keep/remove lists and cues in `work/presentation-plan.json` were updated to the new actors.

Round-3 repair (2026-10-22, after the second independent review failure), all in `work/art.mjs`:

- Book-owned arms: each cast member’s library arms are emptied and replaced by arm objects (one top-level object per held pose, swapped with short `appear`/`disappear`), giving distinct one-arm poses: `tender`, `reach`, `chest`, `chin`, `palmUp`, `raised`, `point`, `offer`, `invite`, `desk`. The rig’s fixed two-arm gesture presets are no longer used. Sleeves have a darker coat-shade edge so a hand on the chest stays readable in all themes.
- Book-owned face shapes (the director only cross-fades groups by id): `curious` = both brows lifted + slight closed smile (interest, not a frown); `happy` = closed smile (no dark filled wedge, so no “goatee” and no grin ghost); `skeptical` = uncertain wavering mouth; pupils centred so `lookAt` reads left and right. Expression cross-fades are 200 ms.
- Collars: Nadir uses the plain scarf and Lio the open collar; the library `button` collar (a white bar) is gone.
- Sentence fixes: s1.2 Mara points her open hand up at her bubble; Len’s closing question is one palm-up hand, head tilted up to Concordia, uncertain face. s2.1 Nadir watches with interest; Mara opens both palms. s2.2 Mara goes neutral at sentence start and turns her gaze left to Nadir, worried by 1.3 s; the jar drops to Nadir’s hand height; he reaches with one arm (0.9 s) and pulls the hand to his chest (2.3 s), worried, while Mara offers an open hand. s3.2 the raw term sits on Nadir’s handwritten slip and the smoothed term in an assisted bubble (54 px); Nadir looks up with a raised open palm; Mara turns to him and explains palm-up; Suri and Lio go neutral. s4.2 Nadir looks up with interest and invites with an open palm, smiling.
- Larger framing for narrow screens: characters at scale 1.6–1.75 (two-person shots) and 1.15 (four-desk classroom). The player uses one fixed 1200×760 viewBox with no per-film camera, so the four-student shot remains small at 320 px; a phone-specific crop would need a shared runtime change.

Round-4 repair (2026-10-22, after the third independent review), `work/art.mjs` only:

- Arm swaps are an in-order handoff, not a cross-fade: `pose()` hides the old arm in 60 ms and the new arm appears 80 ms after the cue (60 ms fade). A DOM scan of the staged film at 20 ms steps found no moment with two visible arms on one shoulder.
- Scene 2: the “language” speech bubble moved from the top-right corner (under the chapter counter) to stage (805, 285), between the book and Mara’s face; top ≈ 197, right edge ≈ 853.
- Scene 1 s1.2: Len’s closing question uses a new `askUp` pose (palm raised and angled toward Concordia, about 100 px above the bed post) instead of `palmUp`, which landed on the post.
- Scene 3 phone legibility (minor): accepted, not changed. Four seated students need the 1.15 scale to fit desks in the fixed 1200×760 viewBox; faces stay small at 320 px until the shared runtime gains a phone crop.

Staging QA (candidate, not published): build with `--output=<scratch dir>` (round 4 used the session scratchpad `concordia-r4/stage/`), then `qa-film.mjs` passed 23/23 checks, 48 sampled frames in Color, Light and Dark with no caption overlaps or label overflow, offline decoding of 8 clips, zero JavaScript errors. Midpoint, gesture-peak and expression-transition frames (S2 s2 at 31.8–34.0 s), zoomed faces and 320/393 px phone frames were inspected. `qa/visual-plan-review.json` still records the previous art hash, so a publish build refuses until an independent visual review passes. No audible playback, physical-device test or audience study is claimed.

Delivery: `docs/books/concordia/series/bk-7a56d2d893d34260/Animation/concordia-series-introduction.shf` plus `manifest.animation.durationMs`.

```sh
node presentations/concordia-series/work/art.mjs
node tools/shf/check-visual-plan-implementation.mjs presentations/concordia-series
node presentations/concordia-series/build.mjs --output=/tmp/concordia-staging   # review build into any scratch dir (also refreshes exports/ that qa-film reads)
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/concordia-series
node presentations/concordia-series/build.mjs   # publish, only after qa/visual-plan-review.json passes for the current art hash
```
