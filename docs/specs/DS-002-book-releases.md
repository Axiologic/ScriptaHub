# DS-002 — Incoming books, translations and releases

Status: active. Applies to `tasks/`, `.book-work/`, the canonical HTML readers,
manifests and edition history. DS-001 remains the product specification.

## Language policy

Prepare complete and ten-minute readers in English and Romanian for each new
book and release. Translate other languages only after a visitor/editor requests
that book and language. Eight-language interface and discovery metadata remain
available regardless of reader availability. Do not use a translated landing
page as evidence that a full reader exists.

## Intake and matching

Start book-maintenance work with:

```sh
python3 tools/book_tasks.py scan
python3 tools/book_tasks.py status
```

The scan accepts PDF, DOC and DOCX files recursively under `tasks/`, ignoring
temporary Word lock files and hidden work directories. Filename matching ignores
case, punctuation, spaces and underscores. A final `_v2`, `_v3`, etc. specifies
the source version, independently of the site's sequential edition number.
The first delivery normally has no suffix and means source version 1.

Match English titles, source IDs, title routes and recorded source aliases.
A unique match remains the same book; an unmatched title becomes a new book.
Ambiguous titles, two different source files with the same title/version, and
versions that do not advance must be resolved before installation. An identical
SHA-256 is already imported and must not create another edition. Keep deliveries.

```sh
python3 tools/book_tasks.py prepare tasks/AssistOs_v2.docx --source-language en
python3 tools/book_tasks.py prepare tasks/NEW_TITLE.docx --source-language ro --english-title 'New Title'
```

Staging is under `.book-work/<title>-v<version>-<hash>/`, outside the public
catalogue. `release.json` records source identity, intended book route, source
language, date, requested extra languages and EN/RO release notes. Preparing a
queued source again resumes its existing workspace and random book ID.

Read `tasks/RELEASE-PROGRESS.md` before continuing any existing work. Once basic
metadata and cover assets are prepared, expose the incoming book immediately:

```sh
python3 tools/book_tasks.py announce .book-work/WORKSPACE
python3 tools/build_books.py refresh
python3 tools/book_tasks.py status
```

New books get searchable landing pages marked **In preparation**. Existing
books get a pending entry in edition history while the current published
edition remains available. Initial draft entries may have 10–100 real keywords;
complete releases require 100. Do not withhold landing pages until translation
is finished. Pending entries have a start date, not a publication date, and
are promoted in place when the release is complete. The ledger records paths,
hashes, IDs, completed chunks and outstanding work; regenerate it after each
meaningful step and before a context switch or hand-off.

## Preparing the publication

1. Convert the original source to complete, reflowable HTML without dropping
   chapters, paragraphs, tables, figures, code or references. Preserve the source
   art and inspect its rendering. A DOCX is a source document, not a request to
   create another Word deliverable. Never translate PDF layout or PDF text
   directly: establish canonical HTML first.
2. For an English source, translate its full HTML to Romanian. For a Romanian
   source, preserve Romanian HTML and translate it to English. Use the
   `book-reader-translations` skill and `tools/html_translation_chunks.py`.
   Fill each translation directly as the agent; no external translation service.
   Use stable chunks and run `check` before `assemble`. Preserve identifiers,
   references, code and local asset links. Never publish unfinished chunks or
   label a summary as a complete translation.
3. Author a genuine ten-minute edition, then prepare its EN/RO versions through
   the same chunk workflow. Keep `full_content.html` and `short_content.html`
   in `book/en/` and `book/ro/`. Other reader files require an explicit language
   request recorded in `requestedLanguages`.
4. Refresh book-specific title, subtitle, short description and About Book
   paragraphs from this source. Update the manifest, including 100 distinct
   discovery terms and stable keyword identifiers. Ten shelf categories come
   from the build vocabulary; extract the remaining 90 from the new English
   short reader and translate the labels locally. Do not retain outdated terms
   just because an earlier release had them. Catalogue metadata remains in all
   eight supported interface languages.
   For an isolated staged release, use `python3 tools/build_books.py
   rebuild-keywords --manifest .book-work/WORKSPACE/book/manifest.json`.
   Inspection may save a `keywordReview` with the current source hash and 90
   selected phrases in the manifest. Rebuilds preserve that selection only
   while the hash matches and every phrase occurs in the current reader.
   Do not add book-specific vocabulary to the build code. Correct localised
   labels in the translation cache and rebuild when review finds mistranslations.
5. Inspect the cover in every incoming document, including revisions. Use
   `python3 tools/book_tasks.py cover .book-work/WORKSPACE EXTRACTED_COVER.png`
   to record its source and delivery hashes, retain it as `cover.png`, and
   produce `cover.webp` and `thumbnail.webp` for all language landing pages.
   Run `announce` again to expose the pending edition's cover, and
   `python3 tools/build_books.py refresh-covers` after installing new art.
   Do not silently reuse artwork from the previous release. Stage an English source PDF
   as `book/en/book.pdf`; never generate translated non-English PDFs.
6. Fill dated EN/RO release notes explaining the substantive changes. Verify
   source/translation completeness and local image/table rendering before
   installation. The automated stage check is a structural gate; it cannot
   establish literary fidelity or prove that no source chapter was omitted.

## Installing and preserving history

```sh
python3 tools/book_tasks.py check .book-work/WORKSPACE
python3 tools/book_tasks.py install .book-work/WORKSPACE
python3 tools/build_books.py refresh
python3 tools/build_books.py check
python3 tools/audit_internal_links.py --check
```

The installer validates before modifying current files. For an existing book it
archives the previous language assets under `edition-files/<old-edition>/`,
preserves the old PDF at `<language>.pdf`, rebases HTML asset links, and updates
the old history record. Archive metadata uses `book-manifest.json`, so it cannot
be mistaken for a live book manifest. Existing archives are never overwritten.
The new source document is retained under the new edition's `source/` directory.
Each history record has a `covers` map to its own immutable images in
`edition-files/<edition-id>/covers/`. The history displays these covers;
publication replaces the active book and catalogue images, not archived art.

Only the newly completed reader languages enter the current manifest. Other
previous translations remain available through their historical edition and
must not be labelled as translations of the new source. Append a dated record;
never replace the history list. A repeated source or a non-advancing source
version fails before installation. If installation is interrupted after the
archive is created, inspect and recover that snapshot; never delete or overwrite
it to force a retry.

## Visitor requests

Book pages and the reader offer all supported reading languages. Available
formats open directly; missing formats open `docs/translate/` with the book,
target language, requested format and interface language preserved. Selecting
the site interface language alone does not create a request.

The form prepares an email to `create@scriptahub.com`, including the current
edition identifier. The visitor reviews and sends it in their email application.
Record accepted requests against the requested book/release before translating
extra languages. Do not silently update all older translations when publishing
a new English/Romanian release.
