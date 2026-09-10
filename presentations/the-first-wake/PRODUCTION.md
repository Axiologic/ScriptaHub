# The First Wake narrated introduction

The film invites readers into the published English edition of The First Wake:
The Geometry of Becoming. It lasts 11:49.735, with 14 scenes and 98 recorded
English sentences. The opening asks what a next state means before a clock
exists, then introduces the novel's nonhuman minds, complementary investigators,
relationships and competing forms of time. It withholds the mystery's answers
and points readers to the Playfield opening.

The complete source was reviewed through its translator's note, prologue,
17 chapters and epilogue. `source/` retains extracted text, stable source spans
and provenance; `work/editorial.json` and `qa/editorial-review.json` record the
reading invitation and protected revelations. The source has no explanatory
diagrams selected for this adaptation; its cover is retained on the book page.

The original visual direction uses plum, copper and blue relational forms.
These are conceptual illustrations of processes, not literal nonhuman bodies.
Stable silhouettes, transformations, connections and deliberate stillness
express the story's tensions. Each scene's source references, emotional plan,
script and art live in `work/scenes.json`; `work/art.mjs` authors this book's
compositions. Shared compilation, narration and vector utilities live in
`tools/shf/`. The public Animation directory contains only the SHF and its
generated entry page, referencing the site's shared player.

Rebuild from the repository root:

```sh
node presentations/the-first-wake/work/art.mjs
node presentations/the-first-wake/render_voice.mjs
node presentations/the-first-wake/build.mjs
node tools/shf/qa-film.mjs presentations/the-first-wake
python3 tools/build_books.py refresh
```

The prepared local Piper en_US-ljspeech-medium voice uses pace 0.94 and no tempo
change. Clips are measured after conversion to 64 kbps MP3. Real inter-sentence
silence is 1.55 seconds, with longer scene transitions. All 98 captions contain
one sentence, averaging 12.9 words and never exceeding 16. Voice receipts cache
by text hash; changing a sentence requires a new matching recording.

QA sampled 126 frames across all three player themes, verified finite SVG
geometry and connection endpoints, and visually inspected the compositions.
Caption/transport checks passed at 1200, 720, 540, 393 and 320px. All 98 clips
decoded through OfflineAudioContext without output to speakers. Seeking was
deterministic and the standalone file loaded paused. The source adaptation is
registered as a preview: no full audible listening or audience review has been
performed. Piper does not provide guaranteed theatrical acting or pronunciation
of the novel's invented terms. Detailed evidence is in `qa/`.
