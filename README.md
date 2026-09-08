# ScriptaHub
Public repository for scriptahub.com. GitHub Pages serves the prebuilt site from
`docs/`.

Reader account setup and browser build instructions are in
[docs/auth/README.md](docs/auth/README.md). Product rules are maintained in
[DS-001](docs/specs/DS-001-site-product-rules.md).

Use Node.js 22.12 or newer (Node.js 24 LTS recommended) for the current build and
validation workflow:

```sh
npm ci
npm run build
npm test
npm run test:catalogue
```

`build:auth` bundles the browser account flow. `build:books` regenerates book
pages from the existing manifests with the Node.js generator. `npm test` runs
the JavaScript unit and generated-page contract tests; `test:catalogue` checks
the catalogue, edition assets, local links, and fragment anchors.

The older Python import, cover, keyword extraction, and translation utilities
and their legacy tests remain in the repository. They are not dependencies of
this build or test workflow. After using a legacy content operation, finish with
`npm run build:books` to restore the current page template and account actions.
