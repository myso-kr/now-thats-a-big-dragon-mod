## What does this change

<!-- A line or two -->

## Kind

- [ ] Translation (`translations/`)
- [ ] Launcher (`src/`, Rust)
- [ ] Injected scripts (`web/`)
- [ ] Bundle patching (`patch/`, `launcher.js`)
- [ ] Tooling and docs

## If this is a translation PR

- [ ] I edited `translations/`, not `locale/` — everything under `locale/` is generated
      from it, and `npm run translations:check` fails when the two disagree
- [ ] Every `{{placeholder}}` survives exactly as it is in the English
- [ ] I left the `# tags`, `VAR`, `{variables}`, `=== knots ===`, `-> diverts` and the
      `* + -` markers in the `.ink` files alone — one of them out of place and that
      whole dialogue fails to appear
- [ ] Length checked. The game's font is a pixel grid, and a translation is often wider
      than the English. I looked at the short strings — buttons, tooltips — on screen
- [ ] `python tools/build-translation.py <lang>` then `node tools/check-fonts.js <lang>`
      and `node tools/check-dialogs.js <lang>` all pass

## If this is a code PR

- [ ] `npm test` passes (injected-script unit tests)
- [ ] `cargo test` passes (launcher)
- [ ] `npm run dry-run` passes — needs the game installed
- [ ] I ran it against the real game
- [ ] If a bundle anchor changed, `docs/ANCHORS.md` changed with it

## Game version this was checked on

<!-- The first few lines of `npm run doctor` -->
