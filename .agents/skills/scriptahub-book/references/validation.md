# Validation and recovery

## Before promotion

Confirm source filename/version/hash and book ID against the ledger. Manifest
route and release directory must match English-title normalization. A private
Romanian-derived workspace must not be mistaken for a public route.

For each required EN/RO full and short reader verify:

- Correct document and inherited element language, complete translated prose,
  and intentional preservation of names, references, quotations and code.
- Full segment coverage, source structure, unique IDs, tables, inline formatting,
  readable notes, code and mathematics.
- Working local images, anchors and short-to-full links after relocation, including
  shared cross-language assets.
- Genuine short-edition chapter analysis, word budget and source evidence, without
  unsupported conclusions or strengthened empirical claims.

Compare the English PDF's text to the canonical English reader, accounting for
line-end hyphenation and running page numbers. Inspect rendered page sequence and
full-size representative pages: title, contents, chapter starts, dense prose,
tables/figures/math where present, bibliography and final page. Check clipping,
missing glyphs/content, unintended blank pages and orphan headings. File existence
and page counts alone are inadequate.

MathML text extraction does not prove correct mathematical layout. Inspect fraction
bars, scripts, operators and alignment in the actual PDF. If the print engine
flattens native MathML, render the exact canonical formulas with a capable local
browser and substitute them only in the print intermediate. Preserve source
MathML in HTML, record formula and rendered-image hashes, and check every formula
placement in the PDF for completeness, resolution and page bounds.

Review all eight metadata languages: six specific short description sentences,
valid About Book structure, 100 distinct corresponding keywords and the delivery's
cover derivatives. Set QA flags only after the relevant review.

Use local browser QA on desktop and narrow mobile layouts. Keep automated tests
muted and block external access for local-only pages. Launch owned browsers with
`--disable-background-networking --disable-component-update --disable-sync
--disable-extensions --metrics-recording-only --no-first-run --mute-audio`.
Check errors, broken images, horizontal overflow, navigation and links; inspect
screenshots rather than relying solely on DOM measurements. Close owned browsers
when done, never the user's browser.

After installation run `python3 tools/build_books.py check` and
`python3 tools/audit_internal_links.py --check`. The latter checks local HTML and
fragment targets without accessing the web. Repeat relevant checks after repairs.

## Recovery boundaries

- Completed chunks remain completed. Open recorded jobs and check missing segments;
  do not prepare replacement jobs for convenience.
- A changed source hash invalidates assumptions. Reconcile changes and translation
  memory; never use `--force` to disguise the mismatch.
- For a strictly CSS-only repair, retain old/new hashes and prove body markup and
  every translation slot are unchanged before updating the stable template and
  its manifest hashes. Revalidate completed chunks and affected layouts. Keep
  the repair receipt with downstream QA; never relabel an old PDF as rechecked
  unless its print input is demonstrably unchanged or it is checked again.
- Source-map links in a translated short reader must open its matching complete
  reader. Record relocation of inherited English links, including links without
  fragment IDs, so reassembly cannot silently undo integration.
- An installed source hash is not a new delivery. Verify history before cleanup.
- Never delete or overwrite an old archive to make installation pass. Inspect
  current files and snapshots after interruption, then recover using known hashes.
- Keep the previous edition active until replacement is complete. Pending updates
  belong in history, not a warning on the existing book's main page/card.
- Missing conversion/optimization dependencies do not justify claiming optimized
  or validated output. Record the conversion and QA route actually used. Respect
  current environment permissions and escalation rules.

Persist completed files, chunk counts, outstanding QA, exact paths, hashes and
known defects in workspace reports and regenerated progress ledgers. Landing-page
existence and metadata language coverage do not mean processing is finished.

Check the complete title and author remain visible in both cover derivatives.
For authored or regenerated covers, confirm the title is uppercase by default,
fits the visual composition, and has strong contrast with its background at
full size and at catalogue-thumbnail size.
Trim empty export margins, then fit the artwork into the portrait canvas; never
crop content to force 2:3. Preserve source `cover.png` and historical source art.
