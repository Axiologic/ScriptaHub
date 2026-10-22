# AI Adoption Beyond the Slop — English book introduction

The film introduces why this book exists, its distinctive argument, selected examples, limits and a specific reading route. It is not an exhaustive summary or a product demonstration.

- Source: `docs/books/ai/adoption/beyond/the/slop/bk-756d50ae3fc14da1/en/full_content.html`, active `edition-1`.
- Canonical HTML SHA-256: `72cce784935c8dd652477653d516639ee93a883d46e706568aab5244311aa30b`.
- Duration: **6:51** (411106 ms), nine chapters, 54 single-sentence narration clips.
- Voice: locally prepared Piper `en_US-ljspeech-medium`, pace 0.96, normal playback speed; English text and captions. No browser speech or API key.
- Pauses: measured clips followed by 1.35s authored silence plus 0.15s spacing; longer scene endings.
- Public film: `docs/books/ai/adoption/beyond/the/slop/bk-756d50ae3fc14da1/Animation/ai-adoption-beyond-the-slop-introduction.shf`.
- The generated minimal page and catalogue integration are managed by the parent agent; book folders contain no duplicated player or authoring library.

`source/` retains the complete text extraction, original section IDs, source hash and source-image inventory. `work/editorial.json` retains substantive source-body evidence and the book/content/reader plan; `work/scenes.json` holds editable sentences and timed visual direction. `art.mjs` contains this book's original vector staging. Shared compiler, runtime, Red Hat Display/Text fonts and narration tools are reused.

Rebuild from the repository root:

```sh
node presentations/ai-adoption-beyond-the-slop/art.mjs            # regenerates scene visuals only
node presentations/ai-adoption-beyond-the-slop/build.mjs --output=/ABSOLUTE/STAGING/DIR   # review build; writes exports/ and qa/build.json
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/ai-adoption-beyond-the-slop
```

Do not run `render_voice.mjs` unless spoken lines change (clips are cached by text hash). A build without `--output=` publishes into the book's `Animation/` and requires a passed independent review in `qa/visual-plan-review.json`.

Voice caching uses text hashes, so changed sentences must be rendered again. Standalone HTML and VTT exports are in `exports/`, outside the public book folder.

Validation passed: all 54 audio clips decoded in an OfflineAudioContext; 81 sampled frames across all three themes; 21 browser checks including actual bundled fonts, heading containment, all captions, transport controls at 320–1200px, and deterministic seeking. All three theme contact sheets were visually inspected and collision fixes rebuilt. Source and all voice hashes matched at hand-off. Browser tests were muted before any playback and owned tabs were closed.

Scope remains honest: no complete listening review, audible playback, physical-phone test, or independent verification of the book's bibliography. Source reading focused on the argument, selected substantive passages, methodological limits and conclusions; complete extraction is retained for audit. The manifest therefore uses the existing `preview` status.

## Independent revision, 2026-09-10

Replaced the nine symbolic slides with five concrete book-introduction scenes, 20 English sentences, measured 155047 ms. Canonical artwork command: `node presentations/ai-adoption-beyond-the-slop/art.mjs`. Review/staging evidence and prior version are under `review-revision/`. Final installed hash and all-theme verification: `qa/final-review.json`.

## Overlap repair and republication, 2026-10-22

Current film: four scenes, eight sentences, Qwen `Aiden` clips unchanged, measured 65865 ms. **`work/scenes.json` is now the canonical artwork.** `art.mjs` only validates it and prints the art hash; `review-revision/art.mjs` is a superseded five-scene generator and must not be re-run (it would overwrite the reviewed staging).

The paused, unreviewed position edit (archived as `review-revision/previous-public-2026-10-22/scenes.unreviewed-62cd94.json`, with the prior public SHF and its hash) still had overlaps at sentence midpoints: desk legs in the caption band, overlapping cards, the colleague and reviewer hidden behind cards, and the Next task card over both monitors. Those actors were repositioned within y=120…540, cards widened to 260 px, desk legs shortened, and Dark-theme coats given per-character tints (plum `#c3a3cf`, teal `#8ccbc6`, coral `#eea98e`) so people stay distinguishable.

Review: expanded `qa-film.mjs` passed (23 checks, 48 frames, art `614deb69…`). A separate shape-level check found no visible SVG shape or text intersecting the caption box at any sentence midpoint or scene edge, at 1200 and 393 px, in all three themes. All frames were inspected visually. Published from the reviewed staging build with `--output` into the book's `Animation/`; the installed SHF sha256 `d313ed55…` equals the reviewed candidate. Audio was not re-rendered and no listening review is claimed.

## Round-1 visual repair, 2026-10-22 (staged, not published)

Supersedes the statement above that `work/scenes.json` is hand-canonical and `art.mjs` only validates: **`art.mjs` is again the single canonical artwork generator.** It rewrites only each scene's `visual`, `emotionalPlan.performance` (additive per-sentence expression/gesture/gaze notes) and `marketingVisualRevision.status`; spoken lines, emotional states, pauses and audio are untouched (script hash `08ccc298…` unchanged, Qwen `Aiden` clips reused, 65865 ms). The pre-repair `scenes.json` and `art.mjs` are archived in `review-revision/round-1-2026-10-22/`.

Cast (shared `tools/shf/people-poses.mjs` `storyPerson`, rigged with dynamic expressions, gestures and gaze; coats and dark hair carry explicit Night variants): Elena, worker/first user, `person-11`, aubergine coat (scenes 1–4; `learner` in scene 4); Daniel, colleague, `person-16`, teal coat (scenes 1–3); Sam, hesitant newcomer, `person-07`, coral coat (scene 2); Eli, senior reviewer, `person-21`, ochre coat, grey curls, glasses (scene 3 only). Every monitor/laptop stands on a desk or table whose legs reach one floor line (y=528).

Scenes: (1) a sealed crate of AI licence key cards beside Elena quietly working; finished pages pile up while “Tried → Relied on” appears and Daniel arrives surprised, then pleased. (2) One shared table: licence card with receipt, a sparkling experiment flask, a weekly routine calendar; then Elena invites hesitant Sam (worried → relieved, reaching to try) and curious Daniel to her laptop. (3) Elena closes her private AI window when Daniel asks; then polished pages stream onto the review table while Eli, worried, examines a single page with a magnifier (no success mark). (4) Elena weighs where the AI mark belongs among her own tasks; the book opens at its adoption stages and a magnifier finds quiet everyday work beneath a loud showcase poster. In-art text is limited to “AI licences” (40) and “Tried”/“Relied on” (46).

Review: staging build `--output=<scratchpad>/staging-ai-adoption`, candidate SHF sha256 `3deafb4f…`, art `8426df31…`. `qa-film.mjs` passed (23 checks, 48 frames, no caption/label collisions, 0 JS errors); `check-visual-plan-implementation.mjs` reported no issues. Color, Light and Dark first/sentence/last frames and own 393 px captures at every sentence midpoint (Color and Dark) were inspected. Independent review and publication remain pending; no audible playback or listening review was performed.

## Round-2 visual repair, 2026-10-22 (staged, not published)

`art.mjs` remains the single canonical artwork generator (it only rewrites `work/scenes.json` visuals, `emotionalPlan.performance` and `marketingVisualRevision.status`; it does not build). Spoken lines, states, pauses and the Qwen `Aiden` clips are unchanged (script hash `08ccc298…`, 65865 ms). Round-1 `art.mjs`/`scenes.json` are archived in `review-revision/round-2-2026-10-22/`.

Reproduce the reviewed candidate from the repository root:

```sh
node presentations/ai-adoption-beyond-the-slop/art.mjs
node presentations/ai-adoption-beyond-the-slop/build.mjs --output=/ABSOLUTE/STAGING/DIR
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/ai-adoption-beyond-the-slop
node tools/shf/check-visual-plan-implementation.mjs presentations/ai-adoption-beyond-the-slop
```

Staging is never the book's `Animation/`; `qa-film` reads the export written to `exports/` by the same build.

Changes answering the round-1 independent review:
- People are drawn at scale 1.3 (was 0.95) with tighter staging, so faces are about 27 px tall at 393 px. Tables and desks are drawn before the people, so hands are never hidden behind a table top.
- Held poses are static rig rotations (`pose()` in `art.mjs`), which gestures compose with and return to. Magnifiers are drawn inside an arm group (`holdLoupe()`), so they move with the hand.
- Scene 1: the crate says “AI licenses” and is taped shut. Elena stays neutral and absorbed, with her hand on the keyboard and her gaze on the monitor; the angry-looking `determined` expression is gone. “Tried” and “Relied on” are now 36 px tags at the bottom and top of the growing page pile, joined by a small upward arrow. They no longer float as stage text.
- Scene 2: the laptop is drawn before the people. Elena's `invite` hand rises toward Sam in front of the laptop. Sam walks to the laptop, hesitates (worried, `recoil`), and his held left hand settles on the keyboard as he relaxes (relieved) before the midpoint. Daniel looks at the laptop with raised brows and an open mouth (`surprised` reads as interest; `curious` read as a frown at phone size), then smiles. Elena's sentence-1 expression is `skeptical`, a wry weighing, and she makes an `explain` gesture toward each object.
- Scene 3, sentence 1: Elena is curious and her gaze is on the monitor. Daniel reaches conversational distance by about 1.4 s and asks at 1.45 s. Elena turns, worried, recoils at 1.8 s, and the AI window closes at 1.8–2.3 s; the midpoint (2.8 s) shows all of this. The review table appears only in sentence 2.
- Scene 3, sentence 2: Daniel leaves before Eli appears. Each polished page appears behind the monitor at full opacity, slides past its right edge to the review table, and lands as a flat sheet on a growing pile. Eli holds the magnifier over the single checked page throughout, with his arm toward the table, head tilted down and pupils down-left; he looks worried and makes no upward gesture. The asset's detached white chest tab is removed for Eli.
- Scene 4: the stages book shows one continuous path rising across both pages. The showcase poster sits high on the right, where nobody covers it. Elena carries her magnifier, looks at the book, walks to the quiet pile beneath the poster and holds the magnifier over it (held `reach`, untilMs 14468), looking at the pile.

Desks were widened so every keyboard rests fully on its desk top, and landed pile sheets fade in within 280 ms. Evidence: art `ca92439e…`, staged SHF sha256 `889fe26f…` (deterministic rebuild). `qa-film` passed (23 checks, 48 frames, no caption or label collisions, 0 JS errors), and `check-visual-plan-implementation` reported no issues. Every sentence midpoint was inspected at 1200 px in Color, Light and Dark and at 393 px in Color and Dark, along with transition frames for scene 2 sentence 2, all of scene 3 and scene 4 sentence 2. The film still needs an independent review before publication. No audible playback or listening review was performed.

## Round-3 visual repair, 2026-10-22 (staged, not published)

`art.mjs` remains the single canonical artwork generator; spoken lines, emotional states, pauses and the Qwen `Aiden` clips are unchanged (65865 ms). Round-2 `art.mjs`/`scenes.json` are archived in `review-revision/round-3-2026-10-22/`. Reproduce from the repository root with the same commands as round 2 (`art.mjs`, then `build.mjs --output=/ABSOLUTE/STAGING/DIR`, `qa-film.mjs`, `check-visual-plan-implementation.mjs`); staging is never the book's `Animation/`.

Changes answering the round-2 independent review:
- All expression changes are now hard 140 ms cuts, never 500 ms cross-fades. Scene 1, sentence 2: Daniel stays `surprised` until 4300 ms (about 66% of the line) and then cuts to `happy`. His pupils carry a baked left/down bias for scene 1, so with `lookAt` Elena they point clearly left to the pile and Elena. His sentence gesture is a small surprised `recoil` (hands drawn in, head raised toward Elena) that peaks over the midpoint. He stops at x=1105.
- Scene 1: the “Tried” and “Relied on” tags are 44 stage units. The pile moved to x=725 and the monitor to x=540 so that the larger tags stay clear of Daniel.
- Scene 2: Daniel now appears in place at x=895 (no walk). The routine calendar is narrower (164 wide) and sits at x=1088 on a wider table (940), so Sam, Daniel and the calendar have visible gaps.
- Scene 3, re-blocked: Elena (x=360) stands at the left end of her desk with the monitor to her right (x=580). Daniel walks in from the left (to x=112) and leaves the same way. Polished pages leave from behind the monitor's free right edge on a short, low 480 ms path to the review table pile (x=822). No page is in flight between 2980 and 3500 ms, so a landed page shows at the midpoint (3117 ms) and no page crosses a person. Eli's salmon forehead and crow's-feet strokes (`detail.n2`) are removed. The checked page is a larger sheet lying flat in slight perspective. Eli holds a redesigned loupe by a visible wooden handle at an angle above that page. Its lens is translucent and light in every theme (Dark: light fill at 0.5 opacity), with a highlight and magnified text lines kept level on screen.
- Scene 4, re-blocked: Elena (x=160) stands left of her desk (x=550), so the AI mark hovers at eye height to her right. `lookAt` (raised head) and her pupils point at it, and the open-hands `question` gesture runs from 700 to 3700 ms, with its peak (2140–3040 ms) holding through the midpoint (2350 ms). Her pupils carry a baked downward bias for this scene, so they are level with the mark in sentence 1 and look down at the stages book and the pile in sentence 2. The showcase poster now hangs on the wall with two pins and no legs, and the low pile table (x=1000) stands clear beneath it. She walks in front of the desk to x=860 and holds the loupe over the pile. `inspired` cuts in at 3400 ms, away from the midpoint.

Evidence: art `5d120e21…`, staged SHF sha256 `bb5cfda9…`. `qa-film` passed (23 checks, 48 frames, 0 JS errors), and `check-visual-plan-implementation` reported no issues. Own captures at every changed sentence midpoint, at 30% points and at last frames were inspected in Color, Light and Dark at 1200 px, plus scene 1 at 320 px. The film still needs an independent review before publication. No audible playback was performed.

## Round-4 visual repair, 2026-10-22 (staged, not published)

`art.mjs` remains the single canonical artwork generator; spoken lines, emotional states, pauses and the Qwen `Aiden` clips are unchanged (script hash `08ccc298…`, 65865 ms). Round-3 `art.mjs`/`scenes.json` are archived in `review-revision/round-4-2026-10-22/`. Reproduce from the repository root with the round-2 commands (`art.mjs`, then `build.mjs --output=/ABSOLUTE/STAGING/DIR`, `SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs …`, `check-visual-plan-implementation.mjs`); staging is never the book's `Animation/`.

Rig notes behind these fixes: a `character.gesture` returns the head and arms to the values they had when it started, so a `lookAt` that overlaps a gesture is undone; `lookAt` with `up` sets the pupils' y offset and nothing resets it; pupils carry an intrinsic +2 right offset; and person assets scale x by their build (Elena and Sam 1.1, Eli 0.94), which `armPoint()` now includes.

Changes answering the round-3 independent review:
- Scene 4, re-blocked: desk and tasks moved to x=330 and Elena stands at x=620, between the desk and the quiet pile. She never crosses the desk, and the stages book (declared before her, so always drawn behind her) stays clear while the stages are named. In sentence 1 the AI mark hovers just above her tasks, slightly below eye height to her left; no upward look is used, so her baked down-bias pupils look down-left at it and, in sentence 2, down-left at the book and then down-right at the pile from her arrival (walk 1500–2200 ms) to the end. The loupe is now Eli's handled loupe (visible wooden handle). While her arm moves, its lens shows only a curved highlight. Level magnified lines (`loupe-text`) appear inside the lens only while the arm is held at −46° over the pile, from about 2420 ms until the hold ends at 14468 ms, so they are fully visible in the 96% last frame.
- Scene 3, sentence 1: Elena's short recoil (1550–2350 ms) and the window closing come first. She then turns to Daniel (`lookAt` 2350–2800 ms) with a left/down pupil bias, and her head and eyes stay on him through the midpoint (2839 ms) and to the end of the line. Daniel stops at x=150, so his outstretched hand stays inside the frame at 393 px.
- Scene 2, sentence 2: Sam fades in at 650 ms, after the license and flask have gone, and Daniel fades in at 1800 ms, after Sam has finished walking, so no figure appears as a ghost over another shape. Elena stops at x=220. Her open hand rises to shoulder height toward Sam (`explain`, peak 2130–3210 ms over the 2517 ms midpoint), clearly above the table and left of the laptop.

Evidence: art `c426d2d3…`, staged SHF sha256 `d494b2eb…`. `qa-film` passed (23 checks, 48 frames, 0 errors), and `check-visual-plan-implementation` reported no issues. Own captures at 10%, 30% and 50% of every sentence, plus scene 4's last frame, were inspected in Color, Light and Dark at 1200 px. The changed midpoints were also inspected at 393 px in Color and Dark. The film still needs an independent review before publication. No audible playback was performed.

## Round-5 visual repair, 2026-10-22 (staged, not published)

`art.mjs` remains the single canonical artwork generator; spoken lines, emotional states, pauses and the Qwen `Aiden` clips are unchanged (script hash `08ccc298…`, 65865 ms). Round-4 `art.mjs`/`scenes.json` are archived in `review-revision/round-5-2026-10-22/`. Reproduce with the round-2 commands; staging is never the book's `Animation/`.

Changes answering the round-4 independent review:
- Scenes 1 and 3: the keyboard (`keys`) now has a beat-1 appear at offset 0 over 800 ms, identical to the desk's fade. Sampled opacities match the desk exactly at every 50 ms from 0 to 1500 ms in all three themes, so the keyboard never stands alone on the empty stage or in the paused poster frame and never draws over a half-faded desk or Elena's arm.
- Scene 2, sentence 2: the laptop appears at 600 ms, after the license and flask have faded out (0–600 ms), so it never ghosts over them.
- Scene 4, sentence 2: Elena's reach starts at 1300 ms, 200 ms before her walk (1500–2200 ms). The loupe is already clear of her knee when her legs move. The reach is held to the last millisecond of the scene (`untilMs` = scene length − 1), so the loupe never swings down through the pile table. The level magnified lines appear at 2220 ms, after she arrives, and stay inside the held lens to the end.
