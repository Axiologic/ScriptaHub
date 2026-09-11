---
name: scriptahub-book
description: Ingest, resume, generate and release books in ScriptaHub, including English-title routes, book folders, EN/RO readers, multilingual metadata, covers and preserved edition history. Use for incoming manuscripts and ScriptaHub book maintenance; coordinate repository builders and specialist document skills.
---

# ScriptaHub book processing

Run commands from the ScriptaHub repository root. Read `AGENTS.md`,
`docs/specs/DS-001-site-product-rules.md` and `docs/specs/DS-002-book-releases.md`
for current product rules. This skill coordinates existing tools, not a new
converter. Preserve user scope: book processing does not itself request remote
deployment, a narrated film or reader translations into every interface language.

## Start or resume

Read `tasks/RELEASE-PROGRESS.md` and `tasks/release-progress.json`, then run
`python3 tools/book_tasks.py scan`. Resume recorded workspaces and translation
chunks. Regenerate progress with `python3 tools/book_tasks.py status` after
meaningful steps and before context switches or handoff.

Read [Book structure](references/structure.md) for identity, folder layout and
file ownership; [Release workflow](references/workflow.md) for generation and
installation; [Validation and recovery](references/validation.md) before promotion
or when an operation fails.

## Essential decisions

- Public routes always use the **English translation of the title**, even when
  manuscript, cover and filename are Romanian. Establish `title.en` before
  preparing a new book. Source filenames are aliases and provenance; private
  `.book-work/` names may follow them. Let the builder normalize title words and
  create the random ID. Releases retain the existing book identity and route.
- Match titles, identifiers, aliases and existing routes first. Version suffixes
  denote successive releases. Equal source hashes must never create duplicates;
  resolve genuinely ambiguous replacements explicitly.
- Announce new landing pages immediately as **In preparation / În lucru**, then
  refresh the catalogue. Existing books keep their published readers active and
  show pending status only in edition history.
- Complete and ten-minute HTML readers are required in **English and Romanian**.
  French, German, Spanish, Portuguese, Italian and Polish reader translations
  require a specific request. All eight languages still have catalogue metadata,
  covers and landing pages; these do not establish reader availability.
- Use `book-reader-translations` and its stable repository chunk workflow for
  reader translations/repairs. The active LLM translates canonical HTML directly;
  never use a translation service or translate PDF text/layout. Local keyword
  translation is a separate metadata operation.
- Use `comprehensiveSummary` for a genuine ten-minute synthesis of every content
  chapter, then translate its HTML. Never install an incomplete reader or replace
  the full book with an extract or summary.
- Preserve the inspected cover from each delivery, including revisions, and all
  historical readers, assets and downloads. Do not borrow current artwork for
  historical editions whose cover is unknown.
- For authored or regenerated cover typography, use the full title in uppercase
  by default. Compose it as part of the artwork, choose color and placement for
  the actual background, and verify strong contrast at cover and thumbnail size.
- Keep the current edition's archived cover snapshot identical to the approved
  active card cover. When an editor replaces current artwork, refresh only that
  edition's `covers` files; never rewrite an older edition's known artwork.
- Every edition records contribution credit. Honor explicit delivery credits;
  when none are supplied, use the repository's `axiologic-research` author and
  `scripta-initial` statement from `docs/contributors.json`.
- Builders own generated book pages, aggregates and reader integration. Author
  staged sources and manifests; do not hand-edit `collection.json`, create keyword
  routes or duplicate shared UI.

## Specialist skills

For book-introduction films, use the canonical short reader to identify the
book's distinctive contribution before drafting. A new concept, proposed
technology or challenge to a familiar view belongs in the opening in plain
language, with proposal status preserved. Follow the SHF book-introduction
reference and the marketing skill's editorial principles. Keep exact narration,
sentence-level voice direction and concrete visual plans visible in the
project's maintenance dashboard before production when the editor requests it.

Use `doc2Pdf` for DOC/DOCX-to-PDF conversion and `pdf2html` for born-digital PDF
conversion where appropriate. Direct semantic DOCX extraction is acceptable when
validated against all source elements. Preserve tables, notes, hyperlinks, images,
code and mathematics. Use available PDF tooling for English print layout and
rendered-page QA. A Romanian source PDF used for fidelity review remains private;
create the English download only from complete canonical English content.

Use available editorial description skills when needed, applying the site's
six-sentence metadata requirements rather than generic defaults. About Book is
metadata rendered through shared `textShow`, not an SHF film. For requested films,
use `shf-presentation-creator` and `theatrical-audio`, English narration by default,
and the project `Animation/` structure.

## Completion

Finish readers, English PDF, reviewed metadata, 100 keywords per language, cover
provenance and QA before installation. Pass the stage gate, preserve history on
install, then pass catalogue and internal-link checks. Keep unfinished sources in
`tasks/`. Remove a delivered DOCX only after its installed edition contains an
identical SHA-256 source archive and the conversion/PDF are validated. Report
actual completion separately from remote deployment.
