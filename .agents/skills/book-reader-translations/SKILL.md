---
name: book-reader-translations
description: Translate book-reader HTML directly in stable chunks and rebuild full and 10-minute editions, without creating translated PDFs or using an external translation service.
---

# Book reader translations

Use this skill when the website's inline book readers need to be translated or
their multilingual coverage needs repair. Translate the chunk JSON directly as
the agent; do not call an external translation service. The English reader
edition is the canonical source for further translations. For an original
Romanian DOCX, retain its Romanian HTML and translate that HTML into English.
Never translate PDFs or create non-English PDF editions.

New books and releases get complete and ten-minute HTML in **English and
Romanian only** automatically. Every other language requires an explicit
visitor/editor request for that book. Interface and catalogue language support
does not authorise translating every reader. Preserve old translations under
their own edition in the publication history.

Prepare a source reader as stable chunks from the repository root:

```bash
python3 tools/html_translation_chunks.py prepare \
  .book-work/BOOK/book/en/full_content.html --language ro \
  --destination .book-work/BOOK/book/ro/full_content.html \
  --workdir .book-work/BOOK/translations/ro/full
```

Each `chunks/*.json` file has ordered `source` strings. Translate each one to
its `translation` string, retaining names, identifiers, URLs, code, and
citations exactly where they belong. Then rebuild only when every segment is
filled:

```bash
python3 tools/html_translation_chunks.py check \
  .book-work/BOOK/translations/ro/full
python3 tools/html_translation_chunks.py assemble \
  .book-work/BOOK/translations/ro/full
```

Prepare only English/Romanian or a specifically requested language. Run
`prepare` separately for `full_content.html` and `short_content.html` in the
staged `book/<language>/` directory. Existing-reader repairs use the canonical
`docs/books/<title-words>/<bk-id>/<language>/` path. The tool leaves
tags, assets, analytics, citations, and reader code untouched; it removes the
English PDF conversion notice before chunking. Retain canonical citations and
local asset links.

Before publishing, run:

```bash
python3 tools/book_tasks.py check .book-work/BOOK
python3 tools/build_books.py check
python3 tools/audit_internal_links.py --check
```

Existing work and destinations are left untouched unless `--force` is explicitly
requested. Never assemble partial translations. Follow the release procedure
in `docs/specs/DS-002-book-releases.md`.
