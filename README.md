# ScriptaHub
Public repository for scriptahub.com. GitHub Pages serves the prebuilt site from
`docs/`.

Reader account setup and browser build instructions are in
[docs/auth/README.md](docs/auth/README.md). Product rules are maintained in
[DS-001](docs/specs/DS-001-site-product-rules.md).

Book generation and catalogue/link validation use Python 3.10 or newer and its
standard library:

```sh
python3 -B tools/build_books.py refresh
python3 -B tools/build_books.py check
python3 -B tools/audit_internal_links.py --check
```

The browser account flow remains JavaScript. Node.js 22.12 or newer is needed
only to bundle that code and run its browser-logic tests. The combined workflow is:

```sh
npm ci
npm run build
npm test
```

`build:auth` bundles the browser account flow. `build:books` runs the Python
generator. `npm test` runs the browser-logic tests and Python tool tests, then
checks the catalogue, edition assets, local links, and fragment anchors.

The same Python generator retains the import, cover, and keyword workflows.
Older tests named `test_book_html.py`, `test_content_layout.py`, and
`test_translate_books.py` target retired modules under `docs/content/tools/`
that are absent from this repository; they are not part of the current workflow.
