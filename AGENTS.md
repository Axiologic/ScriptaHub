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
- Use `npm run test:catalogue` after changing the catalogue and before hand-off.
  The Node.js checker validates catalogue records and edition assets; the Node.js
  link auditor validates local HTML targets and fragment anchors without
  contacting the web. `tools/build_books.mjs` owns current book-page rendering
  and edition-history initialization; run `npm run build:books` after changing
  its templates or manifests. `npm test` runs the JavaScript contract tests.
  Legacy import/keyword/cover tools remain available for their existing content
  workflows, but must be followed by `npm run build:books` so their older page
  template cannot remove current account actions.
- Reader editions are canonical HTML files. For any repair or new translation,
  use the `book-reader-translations` skill and its chunk workflow. Do not
  translate PDFs and do not use an external translation service; PDFs remain
  English source editions only.
- Supported interface and metadata languages are `en`, `fr`, `de`, `es`,
  `pt`, `it`, `ro`, and `pl`. Every manifest must have exactly 100 distinct localised
  keywords, a localised short description, a cover URL, and `book.html` for
  each of them. A language can lack a complete reader only when no completed
  translation exists yet.
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
  legacy output; `npm run test:catalogue` must fail if it exists.
- `cover.png` is preserved source art. Run `python3 tools/build_books.py
  refresh-covers` after adding or changing an artwork; it generates the
  portrait `cover.webp` displayed on a book page. Catalogue cards use only
  `thumbnail.webp`, never the source canvas, so a wide PDF/export canvas
  cannot make a cover look like a small icon inside a white frame.
- Public metadata is branded as ScriptaHub. If imported manifest metadata
  contains a retired public brand, run `python3 tools/build_books.py rebrand`
  before `npm run build:books`; it updates manifests, `collection.json`, and generated
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
  `npm run build:books` to create the initial record for a new
  book and to expose the feedback and edition-history actions on `book.html`.
- `docs/create/`, `docs/feedback/`, and `docs/editions/` are shared workflows
  rendered by `docs/assets/workflow.js` in all eight supported languages.
  Proposal forms must say that they open a structured email to
  `create@scriptahub.com`; selected documents must be attached by the user in
  the mail client because a browser `mailto:` link cannot attach files. Describe
  this user action without discussing the current delivery architecture. Keep
  the green Create action before search in every generated site header.
