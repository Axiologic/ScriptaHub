# Book identity and folder structure

## Public route versus source name

`Arta_de_a_sti_ce_conteaza.docx`, written in Romanian, has English title
`The Art of Knowing What Matters`. Its public root is therefore
`docs/books/the/art/of/knowing/what/matters/bk-<random>/`.
Keep every English title word in order, including articles. Use
`tools/build_books.py:title_route` normalization and `book_tasks.py prepare` for
identity creation. Never reuse another book's random suffix.

The original filename remains in aliases and the source archive.
`.book-work/artadeasticeconteaza-v1-<hash>/` is a private progress path, not a
public route. Language folders belong after the book ID. Author, taxonomy,
source-language and arbitrary category directories never enter the title route.
Matching releases retain identity and route. Deliberate title/route changes use
the repository migration mechanism and link checks, not ad hoc directory renames.

## Published tree

```text
docs/books/<english-title-word>/…/bk-<random>/
  manifest.json                 Source book record; derived fields maintained by tools
  editions.json                 Version history; installer/builder owns transitions
  en/
    book.html                   Generated landing page
    full_content.html           Canonical complete English reader
    short_content.html          Canonical ten-minute English reader
    book.pdf                    Current English download
    cover.png                   Preserved selected source artwork
    cover.webp                  Generated portrait cover
    thumbnail.webp              Generated catalogue image
    assets/                     Reader dependencies, only when needed
  ro/
    book.html
    full_content.html
    short_content.html
    cover.png
    cover.webp
    thumbnail.webp
    assets/                     Only when this reader needs separate assets
  fr/ de/ es/ pt/ it/ pl/        Six separate sibling directories
    book.html                   Mandatory without implying reader availability
    cover.png
    cover.webp
    thumbnail.webp
    full_content.html           Only when requested translation is complete
    short_content.html          Only when requested translation is complete
  Animation/                    Only when a book film has been produced
    <film>.shf
    index.html                  Minimal generated page using shared assets
  edition-files/
    edition-<n>/
      source/<original-name>    Original filename and extension, hash-preserved
      covers/<language>.webp    This edition's own cover snapshots
      en.pdf                    Historical PDF once superseded
      en/                       Historical readers and local dependencies
      ro/                       Historical readers and local dependencies
      <other-language>/         Any translations belonging to that edition
      book-manifest.json        Archived manifest, never named manifest.json
      edition-history.json      History snapshot taken during replacement
```

The current edition archive initially contains its source and cover snapshots.
Its reader/PDF snapshots are added when it is superseded. Older historical paths
may differ: follow `editions.json`, never infer a path and overwrite it. Preserve
historical non-English downloads although newly generated PDFs are English only.

Assets can be shared through valid relative links. Do not duplicate an image just
because its surrounding prose was translated. The installer rebases archived
reader links. Keep shared reader/book-page UI in `docs/assets/`; no copied per-book
shell or runtime, second reading-language selector, or keyword HTML directories.

## Manifest and history

Inspect a valid current manifest and builder code rather than inventing a schema.
Core fields include `id`, `sourceId`, `sourceAliases`, `route`, `category`, `group`,
`title`, `subtitle`, `shortDescription`, `aboutBook`, `keywordIds`, `keywords`,
`coverUrl`, `thumbnailUrl` and `editions`.

- `route` is an array of normalized English title words, without `books` or ID.
- Metadata languages are `en`, `fr`, `de`, `es`, `pt`, `it`, `ro`, `pl`.
- Each `shortDescription` has six specific sentences, at most 22 words each.
  Preserve reviewed `shortDescriptionEditorial` provenance.
- `aboutBook` uses the existing builder schema and its length gate; inspect
  `about_book_section` for current constraints. It is not a film.
- Completed `keywordIds` and corresponding per-language label arrays contain
  exactly 100 distinct items. Drafts allow 10–100. `keywordSourceHash` identifies
  the English short reader. Optional `keywordReview` records that `sourceHash`
  and 90 reviewed source-occurring `phrases`.
- `editions.<code>` describes current relative paths: `book`, `cover`,
  `sourceCover`, `thumbnail`, plus available `fullContent`, `shortContent`, `pdf`.
  The builder derives these and available reader languages from files.
- `publicationStatus`, `currentEdition`, `pendingEdition` are managed through
  `announce` and `install`; do not fabricate availability.

`manifest.editions` lists current language assets. `editions.json` preserves
versioned source hashes, dates, change logs, covers, PDFs and archived readers.
Each edition also owns `contributors`. Explicit release credits take precedence;
without them, store the repository default `axiologic-research` / `scripta-initial`
credit so the Contributions page is never empty for a newly installed edition.
`book.html` is the landing page, never the complete book. `docs/collection.json`
and `docs/collection.js` are generated aggregate indexes, not authoring sources.

## Private workspace

```text
.book-work/<source-key>-v<version>-<hash>/
  release.json                  Source identity/hash, date, state, changes, QA
  book/                         Only files intended for installation into public root
    manifest.json
    en/ … ro/ … <metadata-languages>/
  translations/<target>/full/    Stable manifest, template, chunks and context
  translations/<target>/short/   Independent short-reader translation job
  <summary-job>/                Analyses, synthesis, draft and validation report
  <conversion-work>/            Source extraction and private intermediates
  qa/                           Renders, browser results and fidelity evidence
```

Workspace names outside `book/` are conventions, not public schema. Record actual
paths and resume them. Models, environments, credentials, caches, conversion
receipts and QA do not belong in published book folders.
