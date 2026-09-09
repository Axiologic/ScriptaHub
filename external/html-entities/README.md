# HTML named character references

`entities.json` is an unchanged copy of the WHATWG HTML Standard's named
character reference table, retrieved on 2026-09-09 from
https://html.spec.whatwg.org/entities.json.

Its SHA-256 is
`d741d877ac77c4194c4ad526b5b4a19aef8dfe411ab840a466891cdbb9f362e6`.
The table contains 2,231 references. It is local data used by the native Node.js
HTML inventory, with no network request or package installation at runtime.

`LICENSE` is the upstream WHATWG HTML license retrieved from
https://raw.githubusercontent.com/whatwg/html/main/LICENSE on the same date.
Its SHA-256 is
`85dc6f5ccb57a6fe8c33d158f9fc8fc7ee5655a5d3db2cdd131c6a3d0f48a864`.
The license states CC-BY-4.0, with BSD-3-Clause applying to portions incorporated
into source code. Preserve the bundled copyright and license when copying this
directory. No upstream source or data has been modified.

To update, download the table and license from those sources, inspect their
changes, record the new checksums here and in `dependencies.md`, and run
`node --test tests/internal-links.test.mjs` and `npm run test:catalogue`.
