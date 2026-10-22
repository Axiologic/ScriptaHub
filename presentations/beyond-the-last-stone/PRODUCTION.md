# Beyond the Last Stone — narrated book introduction

Installed English film (2026-10-22): **1:14 (74153 ms)**, four scenes, eight single-sentence clips narrated locally with Qwen3-TTS 1.7B CustomVoice / Ryan (see `work/production.json`, `work/voice-receipts.json`). It replaces the 2:31 Piper film (`e04fbd4c…`), archived with the pre-install manifest and production note in `review-revision/previous-version-2/`; the earlier Piper archive remains in `review-revision/previous-version/`.

Script SHA-256 (scene lines): `85e85962faf1d857c95d809f97a329a0bcf565af0f8dbea90029b29c67ba7819`. Installed art SHA-256: `5f03aea86887b025d4cd6917cd300d0c272e9d87645d4113955fecbd7d58b26a` (superseded in `work/scenes.json` by the staged round-5 art below). Installed `.shf` SHA-256: `3641b129919fda35c732510ad18e0b392a9efc6a90b88f5ff6ecde1c5a2d22ac`, byte-identical to the reviewed staging build.

Canonical source remains edition 1, `docs/books/beyond/the/last/stone/bk-718ccf0885654d25/en/full_content.html`; supporting passages are recorded in `review-revision/source-evidence.json`. Later deaths, crossings, accusations and resolutions stay protected.

## Art source of truth (repair round 5, staged — not installed)

`work/art.mjs` is the single authoritative art generator; it rewrites every scene's `visual` in `work/scenes.json` (spoken lines, audio, emotional plan and plan-required actor ids unchanged). The 2026-10-22 layout repair (`work/archive/repair-layout-superseded.mjs`) and the Piper-era generator (`work/archive/art-superseded-v1.mjs`) are archived; do not run them.

Round-1 changes answer the independent review: the cast uses the rigged library people (open eyes, `character.express`, `character.gesture`, `lookAt`) in prehistoric dress with a distinct coat per person in Color, Paper and Night (`work/visual-bible.json`); every sentence has an authored expression/gesture plan (`visual.performance` in each scene). Labels, text cards, the floating staff, east/west bars, duplicate food and the floating arc are gone: real bear prints in old snow, a forked unlabelled path, a river reaching the black rock, one fire and one food hide, Karr arguing toward Kee across the hearth while Lu lays six counting stones, and the book (cover title 50 stage px) beside the first camp. The only in-art text is the cover title.

Round-2 changes answer the second independent review (all in `work/art.mjs`; spoken lines and audio unchanged):
- Expressions: the library `skeptical` mouth (a smirk) is replaced in the cast's own rig by a flat, lopsided mouth with skin-coloured narrowed lids; the `curious` mouth (a frown arch) becomes a small interested smile.
- Scene 1: Ar starts and stays skeptical in line 1, head lifted toward the empty pass (`lookAt … up`); Kee's pupils are lowered to the food hide and she reaches toward it; the black rock is now an irregular dark-grey stone (lighter Night token, outline, facet and waterline).
- Scene 2: the remembered herd is three ochre cave-painting outlines (strokes only, low opacity) high in the sky, rising on story-smoke from Karr's raised hand after he looks up at it; it appears mid-line 1 and fades out before line 2. Taan is skeptical in line 2, eyeing the fork.
- Scene 3: a flat ridge band gives the scene ground; everyone stands on the shared baseline (Karr at full scale left of the hearth, Kee right of it with the food), the fire between them touching neither; Karr's explaining arm is held toward Kee through the line-1 midpoint.
- Scene 4: the trail emerges from the camp ground under the hearth, passes behind the cast and recedes, narrowing, into the ridge gap; the stray ridge sliver is replaced by a ridge continuing behind the book; Ar ends curious and hopeful (small smile) while Karr keeps the worried contrast.

Round-3 changes answer the third independent review (all in `work/art.mjs`; spoken lines, audio and script SHA unchanged; round-2 `art.mjs` and `scenes.json` archived in `review-revision/round-3/`):
- Rig (all cast): the library's skeptical base asset drew a permanent squint line through Ar's eyes (`M-17 0 L-4 0 M7 0 L20 0`); it is removed. Skeptical lids are lightened (only the eye under the lowered brow narrows, to y −4). Pupils are centred in the whites (the library baked a +2 rightward bias), so `lookAt` left visibly turns the eyes. The `inspired` mouth (a filled open grin) is now a closed, quiet smile. New `castMember` options: `gaze:{emotion:[dx,dy]}` draws whites and shifted pupils inside that expression group, holding an authored gaze while the expression shows; `chinHand` (removed in round 4) redrew the right arm bent with an outlined hand under the chin.
- Scene 1, line 1 (0:01–0:07): Ar's skeptical face holds pupils up-right toward the pass (`gaze.skeptical [3,−4]`); `lookAt empty-route` without `up` tilts his head toward the pass, settled by ~1 s and held through the midpoint.
- Scene 2, line 1: Karr's right hand rises to head height (`reflect`, 900 ms offset, 5600 ms) and holds from ~3.6 s; the story-smoke base and the `remembered-herd` object origin sit on that hand (≈ stage 980,362), so the memory grows out of it; his inspired face holds eyes up-right from ~2 s (`gaze.inspired`), quiet smile. Hand and memory come down before line 2.
- Scene 2, line 2: Karr's worried face looks left at Ar (centred pupils, `lookAt ar` at 600 ms) with a slight head turn by the midpoint.
- Scene 4, line 1: no `reflect` wave; Ar stands hand-to-chin, quiet inspired smile, eyes up-right (`gaze.inspired`); `far-path` origin moved to the ridge gap (790,330) — at 640 it equalled Ar's x and `lookAt` turned him left. Line 2 he looks left to Kee.

Round-4 changes answer the fourth independent review (all in `work/art.mjs`; spoken lines, audio and script SHA unchanged; round-3 `art.mjs` and `scenes.json` archived in `review-revision/round-4/`):
- Rig: Ar and Lu keep their near-black hair in Color/Paper but take a lighter warm brown on the Night stage (`nightHair`). Expression crossfades take 400 ms and every one finishes before 10% of its sentence, so an authored gaze overlay never shows two pairs of pupils in a reviewed frame (`qa/repair-r4/exprs.mjs` reports none at 10/20/30/50%). New `castMember` options: `kneel:{drop,lean}` (upper body lowered and leaning about the hem, shoes under the hem, right arm reaching to the ground) and `hideArmR`; `armObject` draws a person's right arm as its own object in front of them.
- Scene 1: Karr's open-palmed `invite` storytelling peaks ~2.8 s into line 1 and holds through the midpoint while he looks at Kee; in line 2 Kee's raised open palms (`question`) peak ~3.6 s and hold to ~5.4 s, her sad face holding eyes up-right on Karr.
- Scene 2: Ar's arm angles down at the snow patch (`reach` −46°, held with `untilMs` 7450 to ~6.8 s, past the ~4.4 s midpoint); his curious face holds eyes lowered right to the prints. The left fork (`route-a`) is drawn before the high ground and tapers to a point inside it, so it passes behind the ridge.
- Scene 3 relayout: Karr (170) left of the hearth (330) argues across fire, food, roots and seeds toward Kee (690); Lu kneels between Kee and Ar (1060), eyes lowered, and lays six stones with his right hand: each stone appears where his hand touches the ground, then his hand lifts (`release`) and he shuffles one stone-width left (`moveTo`); the stones are drawn in front of him and the last lands ~4.1 s. Line 2: Kee looks down-right at Lu and opens her arms toward him (`invite`, peak ~3.5 s, held to ~5.3 s past the ~4.7 s midpoint); Lu looks up at her; Ar looks down-left at Lu warmly.
- Scene 4: Ar's hand-to-chin arm is the object `ar-chin-arm` (a slightly darker sleeve tone, no outline, hand raised in front of the chin's right side), with his rig arm hidden; early in line 2 it fades out (150–400 ms) before the hanging arm `ar-arm` fades in (400–700 ms) as he turns to Kee, so the two arm poses never show together.

- Round 5 (answers the round-4 independent review; spoken lines, audio and script SHA unchanged): the scene 4 line 2 arm fade (ghost arm, then no arm, then a fading-in arm) is replaced by a hard cut on the beat-2 boundary, which is where clip 2 starts after 1350 ms of silence: `ar-chin-arm` drops from 1 to 0 and `ar-arm` rises from 0 to 1 within 1 ms (scene time 7753 → 7754 ms), and Ar's head turn to Kee starts with it. The inspired → curious change is a separate 1 ms cut 160 ms later. Any crossfade blends the inspired gaze overlay with the base pupils and doubles them. No other arm in the film has an opacity track. Lu's stone placing, Ar's `reach` and the gestures are rotations only. Round-4 `art.mjs` and `scenes.json` (art SHA `28dea0f5…`, reconstructed exactly from the replaced cues) are archived in `review-revision/round-5/`.

## Reproduce the staging build (from the repository root)

```
node presentations/beyond-the-last-stone/work/art.mjs
node presentations/beyond-the-last-stone/build.mjs --output=<staging-dir>
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node tools/shf/qa-film.mjs presentations/beyond-the-last-stone
SCRIPTA_CDP_URL=http://127.0.0.1:9235 node presentations/beyond-the-last-stone/qa/check-art-collisions.mjs
```

`--output=` needs the `=` form. A staging build also refreshes `exports/beyond-the-last-stone-introduction.html`, which qa-film reads; it never touches the installed `Animation/` film. A non-staging build stays blocked until `qa/visual-plan-review.json` records a passed review for the current art SHA-256 (round 5: `376a73303b39f4c1b1318cd0beab25aa266d1a216391a3e1cc909277214d8055`).

## QA of the round-5 staging build (2026-10-22)

- Staging `.shf` SHA-256 `a6d805aff1d13692227c8f97884ddc8a49beadfb8f9d3bc0b7592065cc5a95bf`, 74153 ms, unchanged script SHA and audio; art SHA-256 `376a7330…8055`.
- `tools/shf/qa-film.mjs`: valid, 23 checks, 48 frames, zero errors. Collision probe: the stacked cover-title line boxes plus the intended hand-to-chin overlap at the end of scene 4 line 1. `qa/repair-r4/exprs.mjs`: no partial expressions.
- Scene 4 line 2 was sampled every 20 ms from −200 to +1000 ms around the beat start in Color, Paper and Night (183 frames). Every frame has exactly one fully opaque right arm, Ar's rig arm stays hidden, and exactly one expression is fully shown. Evidence: `qa/repair-r5/s4l2/` (`report.json` plus crops), with the contact strip in `qa/repair-r5/s4l2-swap-strip.png`. To reproduce after a staging build: `SCRIPTA_CDP_URL=http://127.0.0.1:9235 node presentations/beyond-the-last-stone/qa/repair-r5/swap-frames.mjs OUTDIR THEMES SCENE BEAT FROM_MS TO_MS STEP_MS X Y W H [ids]`. Independent visual review is pending, and the installed film is unchanged.

## QA of the round-4 staging build (2026-10-22, superseded)

- Staging `.shf` SHA-256 `f1e780b515ab6458cc7185b83fe705354c6e380ee30dde1def7b09050d93f5d3`, 74153 ms, unchanged script SHA and audio; art SHA-256 `28dea0f5…9dc0`.
- `tools/shf/qa-film.mjs`: valid, 23 checks, 48 paused muted frames plus phone views, zero errors (`qa/browser-review.json`). Collision probe: the stacked cover-title line boxes plus the intended overlap of `ar-chin-arm`'s hand with Ar's chin at the start of scene 4 line 2 (before the swap).
- Frames at 10, 20, 30 and 50% of every sentence in Color, Paper and Night were inspected by the repairing agent (`qa/repair-r4/grid-THEME-sN.png`, plus zooms); reproduce with `SCRIPTA_CDP_URL=http://127.0.0.1:9235 node presentations/beyond-the-last-stone/qa/repair-r4/frames.mjs OUTDIR THEMES SCENE BEAT FRACS [X Y W H]` and `SCRIPTA_CDP_URL=http://127.0.0.1:9235 node presentations/beyond-the-last-stone/qa/repair-r4/exprs.mjs` after a staging build. Independent visual review (round 5) is pending; the installed film is unchanged.

## QA of the round-3 staging build (2026-10-22, superseded)

- Staging `.shf` SHA-256 `674089bc7000639342330f100c7442da55eace978227552d37f07c7729dc2d3c`, 74153 ms, unchanged script SHA and audio; art SHA-256 `cea295b4…6f81`.
- `tools/shf/qa-film.mjs`: valid, 23 checks, 48 paused muted frames plus 320/393 phone views, zero errors (`qa/browser-review.json`, `qa/screenshots/`). Collision probe unchanged (only the stacked cover-title line boxes).
- Face crops at the reviewer's timestamps in Color/Paper/Night were inspected by the repairing agent; evidence in `qa/repair-r3/` (reproduce with `SCRIPTA_CDP_URL=http://127.0.0.1:9235 node presentations/beyond-the-last-stone/qa/repair-r3/face-crop.mjs OUTDIR THEME SCENE BEAT OFFSET|mid STAGE_X STAGE_Y NAME` after a staging build). Superseded by round 4.

## QA of the round-2 staging build (2026-10-22, superseded)

- Staging `.shf` SHA-256 `9a44253eb983f61cf08c7591f9d247a422ebd38511d8c820e92e804f733c06d0`, 74153 ms, unchanged script SHA and audio; art SHA-256 `6ea581de…79b8`.
- `tools/shf/qa-film.mjs`: valid, 23 checks, 48 paused muted frames (Color/Paper/Night × first, each sentence midpoint, last) plus 320/393 phone views, zero errors (`qa/browser-review.json`, `qa/screenshots/`).
- Collision probe (`qa/art-collisions.json`): no person, head, line or caption-band intrusions; the only reports are the stacked cover-title line boxes inside the book object, whose glyphs do not touch.
- Frames, including 3× face crops at the reviewer's timestamps, were inspected by the repairing agent in all three themes and at phone width. Independent visual review (round 3) is pending; the installed film (`.shf` `3641b129…`) is unchanged.

No audible playback or human listening review has occurred; the Qwen clips were ASR-checked earlier with only minor 0–2 word differences (`qa/spoken-audio-review.json`).
