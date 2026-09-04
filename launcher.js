'use strict';

// The launcher, injecting from outside the game.
// It touches no game file. It attaches over CDP and:
//   1) intercepts the index-*.js response and swaps in the Korean i18n tables
//   2) appends a Korean fallback to the pixel fonts in style-*.css
//   2-1) swaps dialogs/en/*.ink for the Korean dialogue
//        (caught at the Response stage, which keeps the original body readable - a
//        later hash comparison will need it)
//   3) injects the cheat widget before the document loads.
//
// Usage:
//   node launcher.js            launch the game and attach to it
//   node launcher.js --attach   attach to a running game (one started from Steam)
//   node launcher.js --no-ko    cheat widget only (no Korean patch)
//   node launcher.js --no-cheat Korean patch only (no cheat widget)
//   node launcher.js --no-auto  no autoplay

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const cfg = require('./config');
const language = require('./lib/language');
const { CDP } = require('./lib/cdp');
const { patchBundle, patchCss } = require('./patch/bundle');
const { NAMESPACES } = require('./patch/i18n');
const ink = require('./lib/ink');

const argv = process.argv.slice(2);
const OPT = {
  attach: argv.includes('--attach'),
  ko: !argv.includes('--no-ko'),
  cheat: !argv.includes('--no-cheat'),
  auto: !argv.includes('--no-auto'),
  // --lang <code> overrides the system locale, including for a language the game
  // already supports.
  lang: (() => {
    const i = argv.indexOf('--lang');
    return i >= 0 ? argv[i + 1] : null;
  })(),
};

const log = (...a) => console.log('[launcher]', ...a);
const warn = (...a) => console.warn('[launcher] !', ...a);

const FONT_DIR = cfg.PATHS.FONTS;

/**
 * Which language to patch in. The system decides unless told otherwise.
 *
 * The game handles en/fr/de/pt/tr on its own; anything else falls back to `en`,
 * which is the slot we overwrite. So this only ever names a language the game does
 * not already have.
 */
function chooseLanguage() {
  if (!OPT.ko) return { lang: null, reason: 'disabled with --no-ko' };
  const catalogue = JSON.parse(fs.readFileSync(cfg.PATHS.LANGUAGES, 'utf8'));
  return language.resolve(catalogue, {
    requested: OPT.lang,
    locale: cfg.systemLocale(),
    available: cfg.availableLanguages(),
  });
}

/**
 * Answer a flag request with the PNG we ship for that language.
 *
 * `offered` is every language in the settings list, not just the one being applied:
 * the list shows all of them at once, so a flag we do not answer is drawn as a broken
 * image. The game's own five keep their own files and are not matched here.
 */
function loadFlag(url, offered) {
  const at = url.indexOf('/flags/');
  if (at < 0) return null;
  const name = url.slice(at + '/flags/'.length).split(/[?#]/)[0];
  if (!offered.some((f) => f === name)) return null;
  const p = path.join(cfg.PATHS.FLAGS, name);
  if (!fs.existsSync(p)) {
    warn(`flag file missing: ${p}`);
    return null;
  }
  return { name, data: fs.readFileSync(p) };
}

/** Answer the font requests planted in the CSS with the real files. */
function loadFont(url, L) {
  for (const f of (L ? L.fonts : [])) {
    if (!url.includes(f.url)) continue;
    const p = path.join(FONT_DIR, f.file);
    if (!fs.existsSync(p)) {
      warn(`font file missing: ${p}`);
      return null;
    }
    return { name: f.file, data: fs.readFileSync(p) };
  }
  return null;
}

/** Pull lang and id out of gemshell://index.html/dialogs/<lang>/<id>.ink. */
function parseDialogUrl(url) {
  const m = /\/dialogs\/([^/]+)\/([^/]+)\.ink(?:\?|$)/.exec(url);
  return m ? { lang: m[1], id: m[2] } : null;
}

/**
 * The translated dialogue for a request, if we have one.
 *
 * Which folder the game asks for follows the language it is running in. Adding our
 * language to its settings means it asks for ours — `dialogs/ko/intro.ink`, a path
 * the game's own assets do not have. Answering only the `en` folder left the game to
 * its own handler, which returned the string "Not found"; the game then typed that
 * out as the dialogue.
 *
 * A folder we carry is served in that language. `en` is served in the applied one,
 * which is the path taken when the settings integration failed and the translation
 * went over the en slot instead.
 */
function loadDialog(url, L) {
  if (!L) return null;
  const hit = parseDialogUrl(url);
  if (!hit) return null;
  const dir = cfg.availableLanguages().includes(hit.lang)
    ? cfg.language(hit.lang).dialogsDir
    : (hit.lang === 'en' ? L.dialogsDir : null);
  if (!dir) return null;
  const p = path.join(dir, `${hit.id}.ink`);
  if (!p.startsWith(dir) || !fs.existsSync(p)) return null;
  return { id: hit.id, text: fs.readFileSync(p, 'utf8') };
}

function loadTables(L) {
  if (!L) return null;
  if (!fs.existsSync(L.i18nPath)) {
    warn(`${path.basename(L.i18nPath)} is missing. Run \`node tools/extract-i18n.js\` first.`);
    return null;
  }
  return JSON.parse(fs.readFileSync(L.i18nPath, 'utf8'));
}

/**
 * With a game already running, this run can achieve nothing.
 * Electron's single-instance lock makes the new process hand its arguments to the
 * existing one and exit, and --remote-debugging-port never reaches the survivor.
 * The launcher still looks like it attached, so this has to be blocked up front.
 */
function findRunningGame() {
  const exe = path.basename(cfg.GAME_EXE);
  try {
    const out = require('child_process')
      .execSync(`tasklist /FI "IMAGENAME eq ${exe}" /FO CSV /NH`, { encoding: 'utf8' });
    return out.split(/\r?\n/)
      .map((l) => (l.match(/^"[^"]+","(\d+)"/) || [])[1])
      .filter(Boolean);
  } catch (_bd) { return []; }
}

function launchGame() {
  const running = findRunningGame();
  if (running.length) {
    throw new Error([
      `The game is already running (PID ${running.join(', ')}).`,
      'Because of the single-instance lock, launching now would not apply the patch.',
      'Close the game completely and run again, or use --attach.',
      `(--attach needs the game to be running with --remote-debugging-port=${cfg.PORT})`,
    ].join('\n'));
  }
  if (!fs.existsSync(cfg.GAME_EXE)) {
    throw new Error(`Could not find the game executable: ${cfg.GAME_EXE}\n` +
      'Set BIG_DRAGON_DIR to point at it.');
  }
  log(`launching the game (CDP port ${cfg.PORT})`);
  const child = spawn(cfg.GAME_EXE, [`--remote-debugging-port=${cfg.PORT}`], {
    cwd: cfg.GAME_DIR,
    detached: false,
    stdio: 'ignore',
  });
  child.on('exit', (code) => {
    log(`the game exited (code=${code}). Closing the launcher.`);
    process.exit(0);
  });
  return child;
}

function headersToList(obj) {
  // CDP wants [{name, value}]. content-length is dropped because we recompute it.
  return Object.entries(obj)
    .filter(([k]) => k.toLowerCase() !== 'content-length')
    .map(([name, value]) => ({ name, value: String(value) }));
}


/**
 * Watches the autoplay heartbeat (window.__bd_auto_beat) from outside the renderer.
 * A stopped heartbeat means the renderer has saturated, so autoplay is stopped and
 * the game speed is put back to 1x.
 */
function startWatchdog(cdp) {
  const STALL_MS = 6000;
  const POLL_MS = 2000;
  let lastBeat = 0;
  let lastSeen = Date.now();
  let recovering = false;

  const evaluate = (expr) => cdp.send('Runtime.evaluate', {
    expression: expr, returnByValue: true, awaitPromise: false,
  });

  // Periodically write the snapshots the engine keeps in memory out to disk.
  const snapDir = path.join(__dirname, 'snapshots');
  let savedUpTo = 0;
  setInterval(async () => {
    try {
      const r = await evaluate('JSON.stringify((window.__bd_auto&&window.__bd_auto.snapshots())||[])');
      const list = JSON.parse((r && r.result && r.result.value) || '[]');
      const fresh = list.filter((x) => x.at > savedUpTo).sort((a, b) => a.at - b.at);
      if (!fresh.length) return;
      fs.mkdirSync(snapDir, { recursive: true });
      for (const snap of fresh) {
        const name = `${new Date(snap.at).toISOString().replace(/[:.]/g, '-')}_${snap.level || 'x'}.json`;
        fs.writeFileSync(path.join(snapDir, name), JSON.stringify(snap, null, 1), 'utf8');
        savedUpTo = Math.max(savedUpTo, snap.at);
      }
      log(`${fresh.length} snapshots written to ${snapDir}`);
      // Keep at most twenty of the older ones.
      const files = fs.readdirSync(snapDir).filter((f) => f.endsWith('.json')).sort();
      for (const f of files.slice(0, Math.max(0, files.length - 20))) {
        try { fs.unlinkSync(path.join(snapDir, f)); } catch (_) { /* ignored */ }
      }
    } catch (_) { /* if the renderer cannot answer, the heartbeat watch below handles it */ }
  }, 60000);

  setInterval(async () => {
    let beat = null;
    try {
      const r = await evaluate('window.__bd_auto_beat||0');
      beat = r && r.result ? r.result.value : null;
    } catch (_) { /* if the evaluation itself is blocked, the stall handling below takes over */ }

    const now = Date.now();
    if (typeof beat === 'number' && beat !== lastBeat) {
      lastBeat = beat;
      lastSeen = now;
      recovering = false;
      return;
    }
    if (!lastBeat) return;                       // autoplay has not started yet
    if (now - lastSeen < STALL_MS || recovering) return;

    recovering = true;
    warn(`no autoplay heartbeat for ${Math.round((now - lastSeen) / 1000)}s - stopping it from outside.`);
    try {
      await evaluate('try{window.__bd_auto&&window.__bd_auto.stop("watchdog: heartbeat stopped");'
        + 'window.__bd_cheat&&window.__bd_cheat.setSpeed(1);}catch(e){}');
      log('watchdog done (autoplay stopped, speed back to 1x)');
    } catch (e) {
      warn(`the watchdog could not step in: ${e.message}. The renderer is not answering.`);
    }
  }, POLL_MS);
}

/**
 * Concatenates one entry file with the module directory beside it.
 *
 * The browser has no module system. `foo.js` has to come after the files in `foo/`
 * have run in name order - those files register themselves on `window`, and the entry
 * file takes them back off it. The file boundaries are there for a person to read;
 * they are not runtime boundaries.
 */
function concatModules(entryPath, label) {
  const dir = entryPath.replace(/\.js$/, '');
  const parts = [];
  if (fs.existsSync(dir)) {
    const mods = fs.readdirSync(dir)
      .filter((f) => f.endsWith('.js') && !f.endsWith('.test.js'))
      .sort();
    for (const f of mods) parts.push(fs.readFileSync(path.join(dir, f), 'utf8'));
    if (mods.length) log(`${label}: ${mods.length} modules - ${mods.join(', ')}`);
  }
  parts.push(fs.readFileSync(entryPath, 'utf8'));
  return parts.join('\n');
}

/** The option labels of the language in play, keyed by dialogue file. */
function dialogChoiceTable(L) {
  const dir = L && L.dialogsDir;
  if (!dir || !fs.existsSync(dir)) return {};
  return ink.choiceTable(
    (name) => fs.readFileSync(path.join(dir, name), 'utf8'),
    fs.readdirSync(dir),
  );
}

async function main() {
  const choice = chooseLanguage();
  const L = choice.lang ? cfg.language(choice.lang) : null;
  log(L ? `language: ${L.lang} (${L.name}) - ${choice.reason}`
        : `no language patch - ${choice.reason}`);
  const ko = loadTables(L);
  // What the bundle patcher needs to add this language to the game's own list.
  const langPatch = L && ko
    ? { code: L.lang, label: L.name, flagFile: L.flagFile }
    : null;
  // Every other language we ship files for. They all go into the settings list, so a
  // saved choice always resolves; only the default follows the system locale.
  const extraLangs = [];
  for (const code of cfg.availableLanguages()) {
    if (!L || code === L.lang) continue;
    try {
      const other = cfg.language(code);
      if (!fs.existsSync(other.i18nPath)) continue;
      extraLangs.push({
        code,
        label: other.name,
        flagFile: other.flagFile,
        tables: JSON.parse(fs.readFileSync(other.i18nPath, 'utf8')),
      });
    } catch (_) { /* a language with no catalogue entry is simply not offered */ }
  }
  // The flag files the settings screen will ask for — one per language we add.
  const offeredFlags = [langPatch, ...extraLangs]
    .filter(Boolean)
    .map((x) => x.flagFile)
    .filter(Boolean);

  const widgetSrc = OPT.cheat ? concatModules(cfg.PATHS.CHEAT, 'cheat widget') : null;

  // The upgrade names, the chapter names and the upgrade tree all now travel in front
  // of the patched bundle rather than in this prelude - see patch/bundle.js. The tree
  // is read out of the bundle itself, which is the only way the Rust launcher could
  // ever have it: the pre-generated file is derived from the game and not committed,
  // so the launcher that ships had no tree at all and autoplay stalled at twelve of
  // the eighty-eight upgrades.

  if (!OPT.attach) launchGame();

  await CDP.waitForEndpoint(cfg.PORT);
  const target = await CDP.findPageTarget(cfg.PORT);
  log(`attached to the page target: ${target.url}`);

  const cdp = await new CDP(target.webSocketDebuggerUrl).connect();

  // The game exiting closes this socket, and that is the end of the run. Without
  // this, the watchdog's own timers hold the event loop open and the launcher lives
  // on as an orphan — which then blocks the next launch, because the single-instance
  // guard sees a game that is no longer there to patch.
  cdp.onDisconnect = () => {
    log('the game exited. Closing the launcher.');
    process.exit(0);
  };

  const servedDialogs = new Set();
  const servedFonts = new Set();

  cdp.on('Fetch.requestPaused', async (p) => {
    const url = p.request.url;
    const done = { ok: false };
    try {
      const isJs = /\/assets\/index-[^/]*\.js(\?|$)/.test(url);
      const isCss = /\/assets\/style-[^/]*\.css(\?|$)/.test(url);

      // The game fetches a dialogue (.ink) when it needs one and compiles it at
      // runtime. There is nothing in the original to read, so ours is served straight back.
      const flag = loadFlag(url, offeredFlags);
      if (flag) {
        await cdp.send('Fetch.fulfillRequest', {
          requestId: p.requestId,
          responseCode: 200,
          responseHeaders: [
            { name: 'Content-Type', value: 'image/png' },
            { name: 'Cache-Control', value: 'no-store' },
          ],
          body: flag.data.toString('base64'),
        });
        return;
      }

      const font = loadFont(url, L);
      if (font) {
        await cdp.send('Fetch.fulfillRequest', {
          requestId: p.requestId,
          responseCode: 200,
          responseHeaders: [
            { name: 'Content-Type', value: 'font/woff2' },
            { name: 'Cache-Control', value: 'no-store' },
          ],
          body: font.data.toString('base64'),
        });
        if (!servedFonts.has(font.name)) {
          servedFonts.add(font.name);
          log(`serving font ${font.name} (${(font.data.length / 1024).toFixed(0)}KB)`);
        }
        return;
      }

      const dialog = loadDialog(url, L);
      if (dialog) {
        // This is the Response stage, so the original can be read
        // (Fetch.getResponseBody). It is replaced whole for now, but overlaying only
        // the prose and checking the rest against a hash of the original would need
        // it. Measured: 719 characters read back.
        await cdp.send('Fetch.fulfillRequest', {
          requestId: p.requestId,
          responseCode: 200,
          responseHeaders: [{ name: 'Content-Type', value: 'text/plain; charset=utf-8' }],
          body: Buffer.from(dialog.text, 'utf8').toString('base64'),
        });
        if (!servedDialogs.has(dialog.id)) {
          servedDialogs.add(dialog.id);
          log(`dialogue replaced: ${dialog.id}.ink (${servedDialogs.size} so far)`);
        }
        return;
      }

      // The cheat widget needs the bundle patch (the store bridge) too, so the JS is
      // intercepted when either of them is on.
      if ((isJs && (ko || widgetSrc)) || (isCss && ko)) {
        const res = await cdp.send('Fetch.getResponseBody', { requestId: p.requestId });
        const body = res.base64Encoded
          ? Buffer.from(res.body, 'base64').toString('utf8')
          : res.body;

        let patched = body;
        if (isJs) {
          const out = patchBundle(body, ko, langPatch, extraLangs);
          patched = out.code;
          if (ko) {
            log(`i18n: ${out.replaced.length}/${NAMESPACES.length} tables, `
              + `${out.i18n.translated}/${out.i18n.total} strings translated`);
            // `labels` is only set when the English Scale was rewritten. Adding our
            // own Scale reports `patched` with no labels, so it must not be read
            // unconditionally — doing so threw here once, and the catch below turned
            // that into the original bundle being served with no sign of why.
            if (out.timeScale.patched && out.timeScale.labels) {
              log(`time units rewritten: ${out.timeScale.labels.join(' / ')}`);
            } else if (!out.timeScale.patched) {
              warn('no time-unit Scale found; "minutes" and the rest stay English.');
            }
          }
          // Exposing the stores is the factory wrapper's job. The epilogue at the end
          // of the module is a fallback, and may be skipped silently (when the stores
          // sit inside a lazily loaded scope).
          if (out.added) {
            log(`languages added to the game's own list: ${out.added.langs.join(', ')}`
              + ` (list ${out.added.supported ? 'ok' : 'FAIL'},`
              + ` flags ${out.added.flag ? 'ok' : 'FAIL'},`
              + ` labels ${out.added.labels},`
              + ` scales ${out.added.timeScale}/${out.added.langs.length},`
              + ` fallback ${out.added.fallback ? 'ok' : 'FAIL'})`);
          } else if (ko) {
            warn('could not add the language; overwrote the en slot instead');
          }
          log(`dispatch bridge: ${out.dispatch.id || 'failed'} - stats bridge: ${out.statsBridge.id || 'failed'}`);
          if (out.stores.wrapped) {
            log(`store bridge: wrapped ${out.stores.wrapped} factories`);
          } else {
            warn('no store factory found. The resource cheats will not work.');
          }
        } else {
          const out = patchCss(body, L ? L.fonts : [], L ? L.fallback : []);
          patched = out.code;
          log(`fonts: ${out.faces} @font-face, ${out.hits} stacks`);
        }

        const headers = {};
        for (const h of (p.responseHeaders || [])) headers[h.name] = h.value;
        if (!Object.keys(headers).some((k) => k.toLowerCase() === 'content-type')) {
          headers['Content-Type'] = isJs ? 'application/javascript' : 'text/css';
        }

        await cdp.send('Fetch.fulfillRequest', {
          requestId: p.requestId,
          responseCode: p.responseStatusCode || 200,
          responseHeaders: headersToList(headers),
          body: Buffer.from(patched, 'utf8').toString('base64'),
        });
        done.ok = true;
      }
    } catch (err) {
      // Falling through to the original asset is the right recovery - the game keeps
      // working - but it has to be loud. A patch that silently does not apply looks
      // exactly like one that applied and did nothing, and that cost real time here.
      warn(`FAILED to patch ${url}: ${err.message}`);
      warn('  serving the original instead; this asset is NOT patched.');
      if (err.stack) warn(`  ${(err.stack.split(/\r?\n/)[1] || '').trim()}`);
    }
    if (!done.ok) {
      try { await cdp.send('Fetch.continueRequest', { requestId: p.requestId }); }
      catch (_) { /* already answered */ }
    }
  });

  await cdp.send('Page.enable');
  await cdp.send('Fetch.enable', {
    patterns: [
      { urlPattern: '*/assets/index-*.js*', requestStage: 'Response' },
      { urlPattern: '*/assets/style-*.css*', requestStage: 'Response' },
      // A dialogue needs nothing from the original, so ours is served at the request stage.
      { urlPattern: '*/dialogs/*.ink*', requestStage: 'Response' },
      { urlPattern: '*/fonts/bd-*', requestStage: 'Request' },
      { urlPattern: '*/flags/*', requestStage: 'Request' },
    ],
  });

  if (widgetSrc) {
    await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: widgetSrc });
    log('cheat widget queued (F8 to open it)');
  }

  if (OPT.auto) {
    // Autoplay names a dialogue option by where it sits in the .ink file, and needs
    // the labels of the language actually in play to find that option on screen.
    // Without them it recognises nothing, holds thirty seconds on every branching
    // dialogue, and then takes whatever came first.
    const choiceTable = dialogChoiceTable(L);
    const src = [
      `window.__bd_dialogChoices=${JSON.stringify(choiceTable)};`,
      concatModules(cfg.PATHS.AUTO_ENGINE, 'autoplay'),
      fs.readFileSync(cfg.PATHS.AUTO_PANEL, 'utf8'),
    ].join('\n');
    await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: src });
    log(`autoplay queued (F9 to open it, Shift+F9 to stop at once)`
      + ` - ${Object.keys(choiceTable).length} dialogues with options`);
  }

  // When the renderer freezes during unattended play, the watch inside the game dies
  // with it. The launcher is then the only thing left that can stop autoplay, so the
  // heartbeat is watched from out here.
  if (OPT.auto) startWatchdog(cdp);

  // The first load may already be past, so one reload makes sure it is intercepted.
  log('reloading the page...');
  await cdp.send('Page.reload', { ignoreCache: true });

  log('ready. Close this window and the patch is gone.');
  process.on('SIGINT', () => { cdp.close(); process.exit(0); });
}

main().catch((e) => {
  console.error('[launcher] error:', e.message);
  process.exit(1);
});
