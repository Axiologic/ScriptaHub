# Eden Before Mars — narrated book introduction

Finished narrated preview: **2:35.512**, four authored scenes and 20 English single-sentence clips, each 8–16 words. The complete script passed authoring and parent editorial review before local voice generation. Its coherent book-level why/how/what introduces the source and provides a specific reason and starting point for reading.

Canonical reader: `docs/books/eden/before/mars/bk-63bbe297e4e640aa/en/full_content.html`; edition `edition-1`; SHA-256 `bbdc2d10ff88d880df540254ab43f32315bfbad5549ce058aba64aa25cc64e9b`. Source extraction, UTF-16 section offsets, chapter map, exact supporting spans and full editable script remain in `source/` and `work/`. Review covered the opening, chapter structure, conclusion, methodological limits and selected substantive passages; it does not certify every line or reference. Source claims remain the book’s arguments, not independently validated findings.

Art direction is authored in `work/art.mjs`, with scene-specific purposes in `work/scenes.json`. Original colorful compositions enact the source’s relationships; staged situations are not passed off as historical evidence. All 1 source images were inspected; their selection decisions and conceptual adaptations are recorded in `qa/source-review.json`. Shared typography uses bundled Red Hat Display headings and Red Hat Text captions. Expressive people retain faces, gestures and articulated poses; chair and lower-body contrast is preserved in Night.

Narration uses the already prepared local Piper `en_US-ljspeech-medium`. All 20 text and audio hashes match the receipts. Actual gaps between sentences are 1400–1400 ms; transitions allow additional breathing room. No external voice API, browser speech or audible automated preview was used.

Apply artwork with `node presentations/eden-before-mars/work/art.mjs`; rerender changed narration with `node presentations/eden-before-mars/render_voice.mjs`; build with `node presentations/eden-before-mars/build.mjs`. Unchanged voice receipts are reused. Public book content contains only the SHF and the site-generated minimal Animation entry page. Portable HTML and VTT remain in ignored `exports/`; production and QA stay outside the public book folder.

Silent browser QA passed 21 checks, decoded 20 clips through OfflineAudioContext, sampled 36 frames across all three themes, checked headings/captions/controls at five widths, and verified deterministic seeking with no JavaScript errors. All-theme contact sheets and targeted motion endpoints/phone captures were inspected. Automated QA used a muted owned browser, disabled background networking and a dead local external proxy; the user’s browser was not touched.

Full listening, continuous full-duration playback, physical-phone testing and audience validation remain unperformed. The final SHA-256 and bounded QA findings are in `qa/final-review.json`.
