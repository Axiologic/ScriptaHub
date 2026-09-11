# Generation and release workflow

## Identify, stage and announce

Read both progress ledgers, run `scan`, inspect source titles/languages, and match
filenames against English titles, identifiers, aliases and routes. Ignore trailing
version suffixes for title matching. Equal hashes do not create new editions.
Process queued versions numerically; resolve ambiguous replacements explicitly.

```sh
python3 tools/book_tasks.py scan
python3 tools/book_tasks.py prepare tasks/ROMANIAN_TITLE.docx --source-language ro --english-title 'English Title'
```

Use the returned workspace. `prepare` establishes identity; it is not a content
converter and may leave a manifest to author. Prepare real draft metadata and
inspect the delivery cover before promptly exposing the pending book:

```sh
python3 tools/book_tasks.py cover .book-work/WORKSPACE .book-work/WORKSPACE/extracted-cover.png
python3 tools/book_tasks.py announce .book-work/WORKSPACE
python3 tools/build_books.py refresh
python3 tools/book_tasks.py status
```

New books become searchable with readers unavailable until completed. Existing
books retain their active edition and show preparation only in history.

## Establish complete canonical HTML

Convert the entire source, preserving reading order, headings, paragraphs,
notes, tables, images, links, code, mathematics and meaningful inline formatting.
Validate against the delivered document. Do not silently OCR/reinterpret image
text. Inspect diagrams and formulas in context. Save source hashes and extraction
evidence outside the installable `book/` tree.

For English originals, stage the validated original/converted English PDF and
translate HTML to Romanian. For Romanian originals, retain Romanian HTML, translate
it to English, and render the English PDF from complete English HTML. Any Romanian
PDF conversion used privately for fidelity checks remains private. Preserve
source artwork separately from English print styling.

Before preparing translation chunks, verify source title, language, IDs, anchors,
text and asset paths. After preparation, source bytes and the template are stable.
Do not force saved translations onto changed source bytes.

## Full and ten-minute translations

Read `book-reader-translations`. For example:

```sh
python3 tools/html_translation_chunks.py prepare .book-work/WORKSPACE/book/ro/full_content.html --destination .book-work/WORKSPACE/book/en/full_content.html --language en --workdir .book-work/WORKSPACE/translations/en/full --maximum-words 1800
python3 tools/html_translation_chunks.py check .book-work/WORKSPACE/translations/en/full
python3 tools/html_translation_chunks.py assemble .book-work/WORKSPACE/translations/en/full
```

Fill every segment's `translation` directly with the active LLM, keeping IDs and
source strings unchanged. Record bootstrap context, glossary and ambiguity choices.
Preserve qualified claims, references and genre. Translation is not permission to
fact-correct or rewrite the author. Resume complete chunks, and assemble only after
`check` passes. Use actual target language on inherited HTML language attributes.

Use `comprehensiveSummary` on a complete semantic HTML reader with `--minutes 10`.
Analyze every content chapter, synthesize its central and distinctive reasoning,
and pass the skill's build and independent validation. Translate that new HTML in
a separate stable chunk job. Preserve the collapsible source map and verify links
to the matching complete reader. An opening extract or generic description is not
a ten-minute edition.

## Metadata, discovery and artwork

Author titles, subtitles, six-sentence short descriptions and About Book copy in
all eight languages. Descriptions are specific, no more than 22 words per sentence,
and withhold answers/conclusions/fiction spoilers. Preserve editorial provenance.
About Book is shared `textShow` metadata, not automatic SHF production.

The builder supplies ten broad shelf categories. Extract the other 90 discovery
terms from the final English short reader. Select plausible search terms, not
broken phrases, the book title, process labels or a hard-coded global ontology.

```sh
python3 -m pip install -r tools/requirements-keywords.txt
python3 tools/build_books.py rebuild-keywords --manifest .book-work/WORKSPACE/book/manifest.json
```

Reuse installed dependencies when available. Localization runs locally and caches
labels in `tools/keyword-translations.generated.json`. Review all languages for
mistranslations, duplicates and sentence fragments. Save 90 source-occurring terms
in `keywordReview` with the current `sourceHash`, correct cache labels and rebuild.
If models are cached, offline model flags avoid update checks. This metadata
translator must never replace active-LLM translation of reader prose.

Select the cover from this delivery even when it resembles older artwork. Record
it with `cover`, preserving identical source artwork in all eight `cover.png`
files. When authoring or regenerating a cover, set the complete title in
uppercase by default, integrate it with the composition, and verify its contrast
against the actual background at both full and thumbnail sizes.
files. Derivatives are `cover.webp` and `thumbnail.webp`; edition snapshots belong
to their own release. The current edition snapshot must match its approved active
card cover after an editorial cover replacement. Refresh that current snapshot
in all eight languages, but never change a prior edition's known artwork. Never
use current artwork to fill unknown historical art.

Record explicit contribution credits from the delivery. When none are supplied,
install the default `axiologic-research` author credit with the `scripta-initial`
statement defined in `docs/contributors.json`.

## Validate and install

Fill dated substantive EN/RO `release.json.changes`, then record actual source,
translation, reader, PDF and metadata review evidence. Read
[Validation and recovery](validation.md); the stage gate is not proof of fidelity.

```sh
python3 tools/book_tasks.py check .book-work/WORKSPACE
python3 tools/book_tasks.py install .book-work/WORKSPACE
python3 tools/build_books.py refresh-covers
python3 tools/build_books.py refresh
python3 tools/build_books.py check
python3 tools/audit_internal_links.py --check
python3 tools/book_tasks.py status
```

Run `build_books.py rebrand` before refresh if imported metadata contains a retired
brand. Installation archives previous readers/assets/downloads, keeps the source
and covers, and promotes pending history. Historical translations are not current.

After validated conversion and installed PDF QA, verify that the retained source
archive has the same SHA-256 as the delivered DOCX, then remove that DOCX from
`tasks/` and record cleanup evidence. Keep unfinished sources and every archive.
Installation in `docs/` does not mean remote deployment or email delivery.
