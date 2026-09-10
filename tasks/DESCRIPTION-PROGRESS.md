# Catalogue descriptions and shared views — 2026-09-10

Scope: rewrite all 103 books in eight metadata languages. Latest user requirement:
5–10 short sentences conveying the subject and central message; use six consistently.
Keep fictional endings private. Do not translate canonical readers.

- Workspace: `.book-work/catalogue-descriptions-20260910/`.
- Source inventory and disjoint batches: `inventory.json`, `batch-1.json` through `batch-3.json`.
- Completed drafts: `descriptions-1.json` through `descriptions-3.json`.
- All 103 books now have six short sentences in each of eight languages: 824 descriptions.
- All three independent cross-reviews passed; corrections were applied before installation.
- `tools/catalogue_descriptions.py install` verified review hashes and installed all descriptions.
- Durable review evidence: `tasks/catalogue-descriptions-review.json`.
- Reviewed manifests carry `shortDescriptionEditorial`; legacy enrich/recover skips them.
- Shared `book-view.js` now owns card/page/context structure and textShow lifecycle.
- First text stays visible during loading; one readiness gate starts playback.
- Page descriptions loop; featured descriptions complete once before carousel rotation.
- Shared scripts/styles receive content fingerprints during catalogue refresh.
- Preserve existing translation/release workspaces. Run book_tasks.py status before hand-off.

Completed: catalogue refresh regenerated all 824 book pages and aggregate mirrors.
Catalogue validation and the internal HTML/fragment link audit passed. TextShow,
reading-language, editorial-description and generated-route tests passed. Browser
integration passed for 4,944 localized view variants, automatic mount/disposal,
loading fallback, continuous book-page playback and completion-gated home rotation.
Canonical reader editions and existing translation workspaces were preserved.
