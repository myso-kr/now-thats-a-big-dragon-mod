'use strict';

const fs = require('fs');
const path = require('path');

const GAME_DIR = process.env.BIG_DRAGON_DIR
  || "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Now THAT'S a Big Dragon!";

const LOCALE = path.join(__dirname, 'locale');

/**
 * The system's language, however this platform reports it.
 *
 * Intl gives the OS locale on every platform Node runs on, and the environment
 * variables cover the case where it has been overridden for the shell.
 */
function systemLocale() {
  return process.env.BIG_DRAGON_LANG
    || process.env.LC_ALL
    || process.env.LANG
    || (() => {
      try { return Intl.DateTimeFormat().resolvedOptions().locale; } catch (_) { return ''; }
    })();
}

/** The languages we actually ship files for: a table and at least one dialogue file. */
function availableLanguages() {
  const langs = [];
  let entries = [];
  try { entries = fs.readdirSync(LOCALE); } catch (_) { return langs; }
  for (const f of entries) {
    const m = /^i18n\.(.+)\.json$/.exec(f);
    if (m) langs.push(m[1]);
  }
  return langs.sort();
}

module.exports = {
  GAME_DIR,
  // ── Repository layout ──────────────────────────────────────────
  // Paths live here and nowhere else, so moving a directory means editing one file.
  //
  //   locale/     written by people. The only place translators touch
  //   web/        runs in the browser, injected into the game page
  //   generated/  extracted from the game. Do not hand-edit (not committed)
  //   patch/      the code that patches the bundle
  PATHS: {
    LOCALE,
    LANGUAGES:   path.join(LOCALE, 'languages.json'),
    FONTS:       path.join(LOCALE, 'fonts'),
    FLAGS:       path.join(LOCALE, 'flags'),
    WEB:         path.join(__dirname, 'web'),
    CHEAT:       path.join(__dirname, 'web', 'cheat', 'widget.js'),
    AUTO_ENGINE: path.join(__dirname, 'web', 'autoplay', 'engine.js'),
    AUTO_PANEL:  path.join(__dirname, 'web', 'autoplay', 'panel.js'),
    GENERATED:   path.join(__dirname, 'generated'),
    EN_I18N:     path.join(__dirname, 'generated', 'i18n.en.json'),
    FINGERPRINT: path.join(__dirname, 'generated', 'fingerprint.json'),
    SNAPSHOTS:   process.env.BIG_DRAGON_SNAPSHOTS || path.join(__dirname, 'snapshots'),

    // Per language. The layout is the same for every one of them.
    i18n:    (lang) => path.join(LOCALE, `i18n.${lang}.json`),
    dialogs: (lang) => path.join(LOCALE, 'dialogs', lang),
  },

  GAME_EXE: path.join(GAME_DIR, 'now-thats-a-big-dragon.exe'),
  APP_DIR: path.join(GAME_DIR, 'resources', 'app'),
  NATIVE: path.join(GAME_DIR, 'resources', 'app', 'gemshell-native.node'),
  BUNDLE: path.join(GAME_DIR, 'resources', 'app', 'gemshell-assets'),

  // The CDP port, passed to the game as --remote-debugging-port.
  PORT: Number(process.env.BIG_DRAGON_PORT || 9223),

  systemLocale,
  availableLanguages,

  /**
   * Everything needed to patch one language in: its tables, its dialogue, and the
   * fonts that go with it. One call, so no caller has to assemble it itself.
   */
  language(lang) {
    const cat = JSON.parse(fs.readFileSync(path.join(LOCALE, 'languages.json'), 'utf8'));
    const def = (cat.languages || {})[lang];
    if (!def) throw new Error(`locale/languages.json has no entry for ${lang}`);
    return {
      lang,
      name: def.name || lang,
      i18nPath: path.join(LOCALE, `i18n.${lang}.json`),
      dialogsDir: path.join(LOCALE, 'dialogs', lang),
      fonts: def.fonts || [],
      fallback: def.fallback || ['sans-serif'],
      flagFile: def.flagFile || null,
      // Code point ranges this language deliberately leaves to the reader's own font
      // — a script no open pixel font covers. See tools/check-fonts.js.
      systemScripts: def.systemScripts || [],
    };
  },

  // ── About the fonts ────────────────────────────────────────────
  // The bundled fonts are served to the game directly, so they work uninstalled.
  // Which font goes with which language is data, in locale/languages.json.
  //
  // Both original fonts are pixel fonts, so "how many units is one design pixel" is a
  // fixed number. A bundled font only looks like the same font when its pixel size
  // matches, so size-adjust = our pxPerEm / the original's aligns the grids 1:1.
  //
  //   Everyday_Standard : upem 768,  1px=128units -> 6 px/em  (body)
  //   High_Birth        : upem 1152, 1px=128units -> 9 px/em  (headings)
  //   Galmuri7          : upem 800,  1px=100units -> 8 px/em
  //   Galmuri9          : upem 1000, 1px=100units -> 10 px/em
  //
  // The game's body sizes are 12/18/24/36px, so for design pixels to land on whole
  // numbers a bundled font also needs design pixel = font-size/6 (gcd is 6). Which
  // means more detail in the glyphs can only come with larger glyphs:
  //
  //   Galmuri7  (7px grid)  size-adjust 133.33% -> 1.17x a Latin capital. The default,
  //                                                and the most natural beside English
  //   Galmuri9  (9px grid)  size-adjust 166.67% -> 1.50x  crisper, but visibly larger
  //   Galmuri11 (11px grid) size-adjust 200%    -> 1.83x  crispest, and far too large
  //
  // Misaligning the grid looks like a way to get both size and detail (Galmuri9 at
  // 133%, 1.22x), but measured it raises partly-transparent pixels by 12-15 points and
  // visibly smears. So it is not used.
  //
  // ascentOverride/descentOverride pin line height to the original, so a larger font
  // does not disturb the UI's line spacing.
  //
  // Galmuri is SIL OFL 1.1 (Lee Minseo). See locale/fonts/OFL-Galmuri.txt.
};
