---
name: book-reader-translations
description: Translate canonical book-reader HTML in reviewed chunks, preserving complete and short editions, assets, citations, and English source PDFs.
---

# Book reader translations

Use this skill for new translations or repairs to a book's reader HTML. The
English reader is the canonical source. Translate text directly; do not call
an external translation service, translate PDFs, or create non-English PDFs.

Locate the book through `docs/collection.json`, then read its `manifest.json`
under `docs/books/<title-words>/<bk-id>/`. Current readers live in each language's
`full_content.html` and `short_content.html`; follow the manifest's edition paths.
Treat complete and short readers as separate translation jobs.

Work in stable, ordered chunks of at most 700 words. Keep a review record with
the source file, source hash, stable segment identifier, original text, and
translation for every segment. Keep tags, identifiers, links, code, citations,
assets, analytics, and reader scripts unchanged. Translate text nodes and
reader-facing accessibility labels, preserving their association with the
original elements. Do not publish a reader until all segments are filled and
reviewed against the source. Keep incomplete work outside published `docs/`.

The old `docs/content/tools/` chunk executables are absent from this checkout.
There is no automatic prepare/assemble command here. Do not invoke those retired
paths or assume the catalogue generator translates reader text. For manual
assembly, check segment order and count, inspect the resulting DOM and links,
and compare every non-text attribute and embedded script against the source.

Write completed HTML under the selected book and language, set the HTML language,
and use relative asset paths that resolve from that location. A translated
reader must not claim that its download is a translated PDF. Preserve access to
the English source PDF and existing account gates. Update only the affected
manifest's edition paths and `availableLanguages`; preserve other metadata and
edition history. Existing readers require an explicit repair or replacement
request before being overwritten.

After manifest edits, rebuild the aggregate and pages from the repository root:

```sh
node --input-type=module -e "import { rebuildCollectionFromManifests, refreshPages } from './tools/build_books.mjs'; rebuildCollectionFromManifests(); refreshPages();"
node tools/build_books.mjs check
node tools/audit_internal_links.mjs --check
npm run test:catalogue
```

Open both reader editions in a browser and inspect headings, paragraph order,
citations, assets, language selection, and reading/download actions. Automated
catalogue checks establish structure and links, not translation completeness or
linguistic quality. See [dependencies.md](dependencies.md) for prerequisites.
