# AGENTS.md

## Cursor Cloud specific instructions

### Repository state

- The `main` branch currently contains only `README.md` (a placeholder for the "Abdelrhman-Soliman / Personal Website" project). There is **no application code, dependency manifest, test suite, or build system on `main`**, so there is nothing to install, build, run, or test from the base branch.
- Actual application code lives on unmerged feature branches, for example:
  - `cursor/file-translator-web-5e8f` — a Node.js/Express app (`server.js`, `public/`, `package.json`). Run with `npm install` then `npm start` (or `node server.js`).
  - `claude/proposal-template-generator-tZCAI` — a proposal/HTML document generator (Markdown + HTML assets, no npm dependencies).
- If you need to work on one of those apps, check out that branch first, then install its dependencies.

### Toolchain available in the environment

- Node.js `v22.x` and npm `10.x`
- Python `3.12`

### Update script

- The startup update script guards on the presence of a `package.json`, so it is a no-op on the current `main` branch and will run `npm install` automatically if a Node app is later merged. No other setup is required for `main`.
