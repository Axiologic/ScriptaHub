# DS001: Coding style and dependencies

Use Node.js 22.12 or newer. New and changed executable tools use `.mjs`, four-space
indentation, explicit exports, relative imports with extensions, and `node:`
imports for built-ins. Resolve bundled files relative to `import.meta.url`.
Use async/await for asynchronous work and `node --test` with `node:assert/strict`.

Prefer built-ins and local code. Do not add packages, a build system, or another
runtime for convenience. Preserve public behavior, canonical reader assets,
edition history, and existing output formatting. Generated HTML and catalogue
JSON retain their established byte format; source indentation does not require
reformatting published assets or third-party data.

The optional `tools/keywords/local_nlp.py` worker retains NLTK extraction and
PyTorch/Marian inference. Native Node.js does not provide those trained models
or their tensor runtime. Node.js owns file operations, catalogue validation,
cache writes, and CLI dispatch. ImageMagick remains optional for cover encoding.
These exceptions and existing browser/build dependencies live in
[dependencies.md](../../dependencies.md).

Check runtime requirements before doing work. Check optional tools only when
their command is selected, and fail with an actionable error before creating
outputs. Never install packages or download models during startup. Update the
dependency inventory, commands, tests, and guidance together.

Run `npm run build`, `npm test`, syntax checks for changed modules, and
`git diff --check`. A tooling-only change must preserve generated book pages,
reader HTML/PDFs, authentication hooks, and historical editions.
