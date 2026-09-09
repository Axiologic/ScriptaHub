# Dependencies

This instruction-only skill owns no executable code, packages, or vendored data.
It requires no runtime to read or copy. It describes work in a ScriptaHub checkout;
its validation commands belong to that project and are not bundled skill tools.

The project validation commands require Node.js 22.12 or newer and use built-ins.
They check Node.js at startup and report installation guidance before outputs.
Use a supported Node.js release from https://nodejs.org/en/download, then run
the commands from the project root. No npm installation is required for the
three catalogue commands. Node.js is the runtime prerequisite, not an npm dependency.

The reader translation workflow uses no external translation service, Python,
or model package. The project's optional keyword NLP environment serves a
different task and is unnecessary here. Project-owned tools and browser
dependencies are inventoried in the repository's root `dependencies.md`.
