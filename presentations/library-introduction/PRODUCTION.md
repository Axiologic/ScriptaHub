# ScriptaHub library tour

A concise English visitor orientation: 9 distinct compositions and 32 short
sentences, 3:01. The film explains a virtual library and its actual
visitor actions. It avoids presenting the site as one book or repeating AI
ambitions. The source snapshot and editorial map remain under source/ and work/.

The opening explains the niche-publishing gap, expert guidance and AI-assisted
revisions. It explains reuse of human thinking, conditional savings in energy
and cost, and the cultural value of niche science fiction and other literature.
Discovery starts through Ask AI Librarian. Reading choices, languages and
contribution actions follow; no temporary email transport is narrated.

The visual sequence includes a library collection, expert notes informing
editions, one book serving many readers, literary forms, recommendation input,
reading depths, languages and contribution actions. Books represent volumes;
the library is always a collection. The page and film use the same editable
robot identity. Book geometry is shared with the creation skill.

One short sentence is shown and spoken at a time. Local Piper narration uses
pace 0.94 with no tempo acceleration. Measured sentence gaps are 1.2–1.4 seconds;
scene boundaries leave longer pauses. Captions remain visible through their
pause. No music or background audio is started during authoring or testing.

Run from the repository root:

```sh
node presentations/library-introduction/render_voice.mjs
node presentations/library-introduction/build.mjs
node tests/home_librarian.browser.mjs
node tests/home_early_loading.browser.mjs
```

The public film is docs/assets/films/library-introduction.shf. Standalone HTML
and VTT are in the ignored exports/ directory. Reusable scene authoring and
narration/publication live in tools/shf/. The homepage shows no production notes.

QA distinguishes automated decoding and layout checks from listening. Tests
stub playback intent, decode clips through OfflineAudioContext, and close owned
tabs. Full listening and physical-device testing remain unperformed. See
qa/production-report.json for the exact final artifact and executed checks.

Typography uses bundled Red Hat Display 600/700 for visual labels and headings,
and Red Hat Text 400 for captions. Both installed and standalone players embed
the licensed fonts and await font loading; no external font service is needed.
