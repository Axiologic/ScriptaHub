# AssistOS narrated presentation

The film introduces the canonical English AssistOS reader, edition 2, in 16 scenes
and 128 individually recorded sentences (13:47). Sentences average 11.8 words,
with a maximum of 14. The purpose is to help prospective readers understand why
the book exists, what perspective and contents it offers, and where to begin.
Four content samples support that invitation; the supplier example takes only
two scenes. The final scene invites reading with a real assignment in mind.

`work/positioning.json` owns the reading promise, audience fit, book journey,
selected samples, reserved reading depth and invitation. The creation skill’s
book-introduction contract is validated before compilation. The semantic review
in `qa/editorial-purpose-review.json` cites the script against seven reader questions;
it is an editorial assessment, not proof of audience engagement.

`work/scenes.json` owns the script, source references and emotional plan.
`build.mjs` assembles the book-specific adaptation using reusable stage authoring
in `tools/shf/illustrated-stage.mjs`. Character-led scenes alternate with close-ups, contrasts, reading routes and
focused objects. Characters retain identity while expressions
and gestures follow each short sentence; measured speech bounds gesture duration.
`work/editorial.json` retains source spans, why/how/what and hook payoffs.

All seven source images were inspected. Two diagrams are redrawn as restrained
vectors: Robot/package/agent relationships and four task-specific delegation
levels. `qa/source-images.json` records selections, omissions and source hashes.
The film does not embed raster photographs. All three themes use plain backgrounds
and one scene title; meaningful foreground relationships remain visible.

Run from the ScriptaHub root:

```sh
node .agents/skills/theatrical-audio/bin/audio.mjs setup piper --voice en_US-ljspeech-medium --download
node presentations/assistos/render_voice.mjs
node presentations/assistos/build.mjs
```

Skip setup when the private local model is already prepared. Rendering first validates the editorial plan and sentence tasks, then reuses
verified cached sentences and never plays sound. Scores use bounded batches;
text hashes prevent revised sentences from retaining stale recordings.

Piper generates English narration locally; its model card identifies the training
dataset as public domain. Output reuses Piper pace 1.04 recordings with a 0.94 tempo adjustment,
a peak limiter and 64 kbps MP3. Timing comes from the final audio files, with roughly 1.15 seconds of real
silence between sentences and longer scene transitions. Piper's
controls do not establish free-form emotional acting or correct pronunciation
of every technical name.

After a duration change, update `animation.durationMs` in the source manifest
from `qa/validation.json`, then run:

```sh
python3 tools/build_books.py refresh
python3 tools/build_books.py check
python3 tools/audit_internal_links.py --check
```

The book's Animation action opens
`docs/books/assistos/bk-c0f6d112218f4c52/Animation/index.html`.
That folder contains only the generated entry and SHF. Shared UI, styling and
player assets live under `docs/assets/`. Portable standalone HTML and captions
are generated under the ignored `presentations/assistos/exports/` directory.
The book film is not featured on the homepage; the separate site orientation is. The movie page ends at the player,
without production notes or duplicate duration/language badges. Provenance stays
in film metadata and working QA; navigation, transcript and themes stay inside
the player.

Skill changes live through ignored symlinks in the separate ScriptaSkillSet
repository. After changing its player, rebuild the skill distribution and copy
`assets/player/shf-player.js` into `docs/assets/shf/shf-player.js`, then regenerate
standalone exports. Incorporate reusable lessons from revisions automatically.

See `qa/production-report.json`, `qa/frame-audit.json` and `qa/silent-review.json`
for actual checks and limitations. All 128 clips were decoded without an audio
output device. Complete listening and physical-device reviews remain unperformed;
the catalogue state stays `preview`. Only the visitor starts audible playback.

Typography uses bundled Red Hat Display 600/700 for visual labels and headings,
and Red Hat Text 400 for captions. Both installed and standalone players embed
the licensed fonts and await font loading; no external font service is needed.
