# ScriptaHub working conventions

- `docs/specs/DS-001-site-product-rules.md` is the durable product and site
  specification. Preserve its invariants and update it in the same change when
  a deliberate product, routing, data, interaction, or presentation decision
  changes.
- `docs/collection.json` is the aggregate catalogue. Each book's source record
  is `docs/books/<title-word>/<title-word>/…/<bk-random-id>/manifest.json`.
  Create one lower-case, punctuation-normalised folder for every English title
  word, in title order; the final `bk-` identifier must be freshly random.
  Do not insert taxonomy, author, language, or arbitrary category folders into
  this route. Rebuild the aggregate instead of hand-editing it.
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
  Keep source files and all prior downloads. See `docs/specs/DS-002-book-releases.md`
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
  data, not routes. Keyword-cloud links target
  `index.html?lang=<code>&keyword=<stable-keyword-id>`, and the catalogue is
  filtered in the browser from `collection.js`. `docs/keywords/` is a forbidden
  legacy output; `python3 tools/build_books.py check` must fail if it exists.
- `cover.png` is preserved source art. Run `python3 tools/build_books.py
  refresh-covers` after adding or changing an artwork; it generates the
  portrait `cover.webp` displayed on a book page. Catalogue cards use only
  `thumbnail.webp`, never the source canvas, so a wide PDF/export canvas
  cannot make a cover look like a small icon inside a white frame.
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
  the green Create action before search in every generated site header.
- `docs/translate/` is the translation-request workflow, also in all eight
  interface languages. Book pages and the HTML reader offer all supported
  reading languages independently of the interface language. Opening an
  unavailable reading language/format opens this form with the book, target
  language, format and interface language preserved. Available editions open
  directly. Changing interface language alone is not a translation request.
  The form opens a structured email to `create@scriptahub.com`; it must say
  that the visitor reviews and sends the email, never claim automatic delivery.
