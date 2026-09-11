# ScriptaHub working conventions

- `docs/specs/DS-001-site-product-rules.md` is the durable product and site
  specification. Preserve its invariants and update it in the same change when
  a deliberate product, routing, data, interaction, or presentation decision
  changes.
- `docs/collection.json` is the aggregate catalogue. Each book's source record
  is `docs/books/<title-word>/<title-word>/…/<bk-random-id>/manifest.json`.
  Create one lower-case, punctuation-normalised folder for every English title
  word, in title order; the final `bk-` identifier must be freshly random.
  The route always uses the English translation of the book title, even when
  the delivered manuscript, cover title and filename are Romanian or another
  language. Establish `title.en` before preparing a new book; the original
  filename is provenance/an alias, never the public route. Source-based names
  under `tasks/` and `.book-work/` are private workflow paths, not book URLs.
  Do not insert taxonomy, author, language, or arbitrary category folders into
  this route. Rebuild the aggregate instead of hand-editing it.
- Use the project skill `scriptahub-book` at
  `.agents/skills/scriptahub-book/SKILL.md` for book intake, folder structure,
  staging, reader generation, discovery metadata and release maintenance.
  It coordinates the specialist skills and the repository-owned builders.
- Use `python3 tools/build_books.py check` after changing the catalogue. The
  migration script owns folder identifiers, reader-link rewrites, manifest
  generation, book pages, and the local-file-safe `collection.js` mirror.
  Also run `python3 tools/audit_internal_links.py --check` before hand-off; it
  validates local HTML targets and fragment anchors without contacting the web.
- Reader editions are canonical HTML files. For any repair or new translation,
  use the `book-reader-translations` skill and its chunk workflow. Do not
  translate PDFs and do not use an external translation service; PDFs remain
  English source editions only.
- Interface support is not a request to translate a whole book. For every new
  book or new release, automatically prepare complete and ten-minute HTML
  editions in **English and Romanian only**. Translate readers into `fr`, `de`,
  `es`, `pt`, `it`, or `pl` only following an explicit visitor/editor request
  for that book and language. Never queue all supported languages by default.
  Preserve existing translations; an older translation must stay associated
  with its old release until the current release is translated on request.
- Supported interface and metadata languages are `en`, `fr`, `de`, `es`,
  `pt`, `it`, `ro`, and `pl`. Every manifest must have exactly 100 distinct localised
  keywords, a localised short description, a cover URL, and `book.html` for
  each of them. These catalogue descriptions, About Book presentations and
  interface labels do not imply that the full book has been translated.
  A reader language may be unavailable until requested and completed.
- Short descriptions are authored metadata: six short, book-specific sentences
  per language, at most 22 words per sentence. Never use an extracted opening
  paragraph, table of contents, numbered headings or generic shelf boilerplate.
  Preserve `shortDescriptionEditorial` provenance; legacy enrichment must not
  overwrite reviewed copy. Use `docs/assets/book-view.js` for shared book views
  and the uniform `textShow` lifecycle rather than duplicating card markup.
- Before book maintenance, scan `tasks/` with `python3 tools/book_tasks.py scan`.
  Read `tasks/RELEASE-PROGRESS.md` and `tasks/release-progress.json` first and
  resume their existing workspaces and chunk files. Update them with
  `python3 tools/book_tasks.py status` after each meaningful step and before
  any hand-off or context switch; completed translations must never be restarted.
  Accept PDF, DOC and DOCX sources. Match the normalised filename against the
  English title, source identifier, aliases and existing route, ignoring a
  trailing `_v2`, `_v3`, etc. An unsuffixed new title is edition 1; `_v1` is
  unnecessary. Matching titles are releases of the same book, not new books.
  A new title gets the normal English-title route and a fresh random `bk-` ID.
  Resolve ambiguous matches explicitly; never guess a destructive replacement.
  Record the source filename, version and SHA-256 so an unchanged task cannot
  create duplicate releases. Process queued versions in numeric order.
  Prepare the complete EN/RO readers, ten-minute editions, refreshed metadata,
  100 discovery keywords and cover derivatives before installing a release.
  Keep archived source files and all prior downloads. After the complete conversion is validated and its PDF is installed, remove the delivered DOCX from `tasks/`, only after verifying an identical SHA-256 source copy in the edition archive. Keep unfinished deliveries in `tasks/`. See `docs/specs/DS-002-book-releases.md`
  for the staging, translation and release procedure.
- **Make incoming work visible immediately.** After identifying a source,
  create the new book's landing pages and searchable catalogue entry, or add
  the matching book's new edition-history record, marked **In preparation**
  (`În lucru`). Use `python3 tools/book_tasks.py announce WORKSPACE`, then
  `python3 tools/build_books.py refresh`. Do not wait for complete translations
  to expose these pages. Keep the previous published edition active until the
  replacement is ready. Draft books may temporarily have 10–100 real discovery
  keywords per language; a completed release still requires exactly 100.
  For existing published books, keep the pending-release status only in edition
  history; do not add a preparation notice to the book page or catalogue card.
- Keywords are reader discovery terms: specific fields, methods, problems,
  genres, and concepts that people would plausibly search for. The build code
  may author only the ten broad, real-world shelf categories per subject group.
  Never hardcode niche terms, title profiles, or a global topic ontology in a
  build script. The other 90 terms must be extracted from the English short
  read, translated locally, and stored in the manifest. Never use the book
  title or site-process/marketing labels. Install `tools/requirements-keywords.txt`,
  then run `python3 tools/build_books.py rebuild-keywords`; its generated
  translation cache makes subsequent runs incremental. Inspect representative
  samples after extraction, then run both catalogue and link checks.
- Never generate one HTML page or directory per keyword. Keywords are catalogue
  data, not routes. Embedded keyword-cloud links target
  `index.html?lang=<code>&keyword=<stable-keyword-id>`, and the catalogue is
  filtered in the browser from `collection.js`. `docs/keywords/` is a forbidden
  legacy output; `python3 tools/build_books.py check` must fail if it exists.
- `cover.png` is preserved source art. Run `python3 tools/build_books.py
  refresh-covers` after adding or changing an artwork; it generates the
  portrait `cover.webp` displayed on a book page. Catalogue cards use only
  `thumbnail.webp`, never the source canvas, so a wide PDF/export canvas
  cannot make a cover look like a small icon inside a white frame.
- Cover derivatives must preserve all artwork after trimming empty export margins.
  Fit it into the portrait canvas using the source background; never crop titles
  or authors to force the aspect ratio. Keep `cover.png` unchanged.
- Every new release must inspect and select the cover from its own delivered
  document, even if it resembles the previous cover. Record it with
  `python3 tools/book_tasks.py cover WORKSPACE EXTRACTED_COVER.png`; the release
  check verifies its source hash and all eight staged source covers. On release,
  replace the active cover and thumbnail everywhere. Each edition's `covers`
  map points to its own preserved images under `edition-files/<id>/covers/`;
  show these images in edition history. Never reuse the current book cover as
  a fallback for a historical edition whose artwork is unknown.
- Public metadata is branded as ScriptaHub. If imported manifest metadata
  contains a retired public brand, run `python3 tools/build_books.py rebrand`
  before `refresh`; it updates manifests, `collection.json`, and generated
  catalogue pages without touching reader-edition source files.
- The MVP is delivered as prebuilt assets with browser-side interactions. Keep
  delivery architecture such as “static”, “prebuilt”, “generated”, or “without
  a backend” out of public-facing copy. Search and discovery remain browser-side
  until a deliberate architecture change is recorded in the design spec. Keep
  the selected language in the URL (`?lang=`) and ensure browser-language
  detection keeps that language first in reading actions.
- Every book root owns an `editions.json`. Preserve all existing records and
  their downloadable PDFs. Before replacing a current PDF, archive it under
  `edition-files/<edition-id>/<language>.pdf`, change that edition record to
  the archived path, and append a new edition with its publication date and a
  localised change log; never overwrite historical edition files. Run
  `python3 tools/build_books.py refresh` to create the initial record for a new
  book and to expose the feedback and edition-history actions on `book.html`.
- Archive the complete previous reader assets as well as its PDF before
  changing current files. Historical translations are not current translations.
  A release is ready only when both complete EN/RO readers and their short
  editions have passed validation. Partial reader translations stay in staging;
  landing pages and pending edition records are visible immediately as in work.
- `docs/create/`, `docs/feedback/`, and `docs/editions/` are shared workflows
  rendered by `docs/assets/workflow.js` in all eight supported languages.
  Proposal forms must say that they open a structured email to
  `create@scriptahub.com`; selected documents must be attached by the user in
  the mail client because a browser `mailto:` link cannot attach files. Describe
  this user action without discussing the current delivery architecture. Keep
  the primary Create action before search in every generated site header.
- `docs/translate/` is the translation-request workflow in all eight interface
  languages. The header language is the preferred reading language; book pages
  have no additional reading-language selector. Reading actions open the selected
  format in that language when available, otherwise the same English format.
  Current PDF downloads always use the English source. Keep historical downloads.
  Missing translations are requested only by clicking the localised unavailability
  sentence, preserving book, target, format and interface language in the form URL.
  Never append “Request translation” to reading actions or language options.
  The form opens a structured email to `create@scriptahub.com`; it must say
  that the visitor reviews and sends the email, never claim automatic delivery.

## SHF presentations

- Use `shf-presentation-creator` and `theatrical-audio` for requested SHF book
  presentations. Default to English narration, English on-screen text and
  English transcripts, independent of the book or interface language. Do not
  generate Romanian or other presentation languages unless explicitly requested.
- Include audio by default; do not ask whether narration is wanted. Make a
  complete, source-grounded invitation to read the book, with chapter navigation,
  captions, transport controls and a measured duration (normally 5–10 minutes).
- Preserve an explicitly configured audio engine. When none is configured,
  report it, create the local configuration files/templates, and use a decent
  small neural English model, initially Piper `en_US-ljspeech-medium`. Private
  dependency installation and model download are authorized for this fallback;
  continue without another confirmation. Never require an API key when this
  local route works. Keep models, environments, credentials and caches ignored.
- Measure audio and retime animation against the actual clips. Never substitute
  browser speech or a silent presentation for the requested finished narration.
  Keep editable direction, source/edition provenance, voice receipts and QA.
- Embed the film in a dedicated page and expose an `Animation` action in the
  book page's action list; preserve interface `?lang=` while the film stays in
  English. Presentations live on their own page, reached through the book’s
  Animation action; do not feature or embed book films on the home page.
  Keep the presentation page focused on the film: no duplicate chapter list,
  transcript, downloads, production notes or duration/language badges around it. These controls
  belong inside the player. Expose Color, Light and Dark theme choices directly
  in the player’s bottom bar, including the copied project runtime.
- Skill code may be improved and tested in the separate ScriptaSkillSet
  repository through the symlinks. Keep those symlinks ignored in ScriptaHub;
  report skill changes separately so they can be committed in their own repo.

- Structure document presentations around source-grounded why, how and what,
  woven into the explanation. Focus on what distinguishes the document, retain
  its technical meanings, and remove filler, slogans and generic observations.
  Open with a source-supported novelty hook in the first one or two sentences;
  establish why the document exists and deserves attention within 20–30 seconds,
  then deliver the promised insight without claiming unsupported world-firsts.
- Use exactly one sentence per narration clip and per subtitle card. Show the
  whole current sentence, retime from measured audio, and invalidate recordings
  when their text changes. Never display two sentences together.
- Keep automated browser audio tests muted before playback starts. Do not run
  audible background previews; the user starts listening. Pause and close owned
  test players on completion or interruption.

- Author an emotional plan with the script, including each scene’s rise, tension,
  release and intended feeling, and each sentence’s expression and gesture.
  Make human characters expressive through face, gaze, posture, hands and motivated
  movement, with deliberate quiet contrasts. Preserve source accuracy and avoid
  invented drama; technical explanations must remain precise.

- Put each book’s animation in its own `Animation/` directory beside `en/`, `ro/`
  and the other language folders. It contains only the film SHF and a generated
  minimal `index.html` referencing common assets; no duplicated player or shell.
  Shared animation UI/runtime/styles live in `docs/assets/`, reusable authoring
  code in `tools/shf/`, and standalone exports stay outside published book folders.
- Use flat, uncluttered backgrounds in Color, Light and Dark: no decorative
  outlines, nested panels, frames or arbitrary lines. Use one short scene title
  in the player and no duplicate SVG/page headings. Separate titles, moving
  silhouettes, labels, captions and controls; check all three themes explicitly.

- Prefer short narration sentences, normally 8–16 words and one idea each;
  review sentences above 20 words and split dense clauses without losing meaning.
- Inspect source diagrams and photos. Integrate relevant ones only when they
  help explain a point, adapting their styling while preserving source meaning;
  omit unsuitable images. Record selections and adaptations in working QA.
- Automatically maintain the SHF creation skill with reusable lessons from
  presentation feedback and observed defects, within the already authorized
  scope. Reconcile old rules and verify changed behavior without another reminder.
- Show no production/source boilerplate or duration/language badges around
  the film. Keep provenance in metadata and QA; the player owns time controls.

- Default book-page SHF films to `book-introduction`, not a product demonstration
  or exhaustive summary. Establish why the book exists, its messages, contents
  and reader gains. Alternate explicit book/content/reader lenses in working
  plans; selected examples support the reading invitation. End with a specific
  reason to read and a source-grounded starting point. Review editorial fit
  before voice generation; technical subject matter must not override purpose.

- The homepage has a compact librarian mascot entrance with Ask AI Librarian first
  and What is ScriptaHub.com? second. Use its one shared vector asset in the site film.
  The site-orientation SHF may open from the homepage in a full-viewport closable
  dialog; book films stay book-local. Stop playback on close and cancel delayed
  starts. Librarian questions replace the choices beside the mascot, preserving the
  existing recommendation route and language. Keep the desktop entrance compact,
  the mascot about the choices’ height, with academic cues and no cast shadow.

- The librarian and featured book occupy matching aligned strips over the word
  cloud, with a 70% cloud veil, header-green foreground strips at 85% background opacity and recessed grey discovery choices in Light theme and no cast shadows. Site tours stay concise
  and useful; represent a library as a collection, never as one branded book.
  Vary slide compositions and use prominent bold scene headings. Narration
  includes real 1.0–1.5 second pauses between sentences and longer transitions;
  reduce content rather than accelerating speech. Preserve these defaults in
  the SHF creation skill automatically when further presentation lessons emerge.
- Keep the librarian interactive before the catalogue loads. Show loading only
  inside the featured-book strip. Its question form replaces the choices in
  place; a top-right close button restores them without moving the entrance.
- Presentation typography uses the bundled display font for headings and short
  labels, with a separate readable text face for captions. Preserve approved
  wording during visual revisions. Prefer natural sentence case and coherent
  weight/size hierarchy over widely spaced all-caps utility labels.

- Bound the entire site tower on wide screens through shared `--shell-width`,
  `--wide-screen-inset`, `--tower-gutter` and `--content-max` CSS tokens. Header,
  grey/cloud background and footer narrow together, with a modest inner gutter
  for content. Do not apply the wide-screen reduction twice or duplicate
  per-page width rules.

- Site appearances are Light Green, Light Orange, Light Linen and Dark. Preserve the same
  shared layout; Orange replaces green UI accents, including cloud and mascot,
  and persists into reader paper mode. Linen replaces the previous blue theme with ivory, greige and burgundy,
  with colours only changing (legacy storage key `nord`). Persist the last selected appearance and light
  variant through reader Night mode. SHF player themes remain independent.
- Fullscreen keyword selection opens AI Librarian recommendations with the
  localised term and interface language, from home or book pages. Embedded
  catalogue keyword links keep their stable keyword-ID URL contract.
- Standardize SHF delivery and quality, not a book's art direction. Each book
  gets its own source-grounded visual identity. Fiction films invite reading
  through premise and questions, without revealing later twists or resolutions.
- Align close, dictation and submit in the librarian form's right-hand column.
  Dictation starts only on explicit visitor action and stops on close, submit,
  language change or navigation; automated tests use a simulated recognizer.

- Every book exposes Animation and Fork. An absent animation opens a contextual
  animation proposal form; a ready animation has an improvement form below the
  player. This requested feedback form is the exception to the film-only page
  rule; retain the prohibition on production boilerplate. Fork proposes a derived
  book, preserving source identity and allowing additional document selection.
- Before generating voice, review the actual spoken script as a coherent book
  introduction: identify the book, why it deserves reading, its essential message
  and direction in the opening, then develop its approach and selected content
  through why → how → what. Do not approve isolated ideas just because hidden
  editorial metadata contains the right labels. Verify rendered display fonts,
  strong short headings and distinct visual identities for every new book.

- Theme selection includes `dark-orange` alongside `light`, `orange`, `nord`
  (Light Linen) and `dark` (Dark Green). Both dark variants share layout and a
  black surround; use #ff7900 for Dark Orange and preserve both remembered light
  and dark variants across reader toggles. SHF artwork themes stay independent.

- Default the site and reader to Dark Orange when no valid appearance preference
  is saved; preserve explicit preferences and apply the default before first paint.

- Book-associated forms use the shared compact `data-book-workflow` heading
  treatment, including new workflows; never introduce oversized marketing titles
  or unnecessary vertical hero spacing above these forms.

- Local browser QA must disable browser background networking, component updates,
  sync and extensions, remain muted, and close owned browsers when idle. Use
  `--disable-background-networking --disable-component-update --disable-sync
  --disable-extensions --metrics-recording-only --no-first-run --mute-audio`.
  Restrict external network access for local-only checks; never close user browsers.

- Maintain `docs/status.html` as the unlinked, noindex work dashboard for every
  book. Keep exact proposed narration under “Spoken script and film plan” and
  track Text, Animation and Voice separately. Record work starts, progress,
  failures and completion in each presentation's `work/migration-state.json`,
  and run `node tools/shf/update-voice-migration-status.mjs` after each meaningful
  change. Active work appears first, with an “În lucru” indicator beside the
  title naming the current task. The page refreshes its data every minute
  without closing open scripts. Do not mark a draft, recording or planned visual
  revision as a finished film; verify current text, packaged audio, measured
  duration and visual review separately. Review all requested scripts before
  batch voice generation. Current book-introduction scope is all books, with
  a source-grounded marketing hook and maximum two-minute measured duration.
