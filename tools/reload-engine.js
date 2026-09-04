'use strict';

// Pushes the current web/autoplay engine into the running game, without restarting it.
//
//   node tools/reload-engine.js
//
// The launcher reads web/ once, at startup, so picking up a change to the engine used
// to mean closing the game and launching again. That is not free: the game autosaves
// continuously, and every restart in this session came back with the campaign reset to
// the tutorial. Evaluating the modules into the page that is already open costs
// nothing and keeps the save.
//
// It re-registers the modules on `window.__bd_mod` and rebuilds autoplay's own state
// from them, which is all the launcher does at inject time anyway.

const fs = require('fs');
const path = require('path');
const { CDP } = require('../lib/cdp');
const cfg = require('../config');

/** The engine modules and the entry file, in the order the launcher concatenates them. */
function engineSource() {
  const entry = cfg.PATHS.AUTO_ENGINE;
  const dir = entry.replace(/\.js$/, '');
  const parts = [];
  if (fs.existsSync(dir)) {
    for (const f of fs.readdirSync(dir).sort()) {
      if (!f.endsWith('.js') || f.endsWith('.test.js')) continue;
      parts.push(fs.readFileSync(path.join(dir, f), 'utf8'));
    }
  }
  parts.push(fs.readFileSync(entry, 'utf8'));
  parts.push(fs.readFileSync(cfg.PATHS.AUTO_PANEL, 'utf8'));
  return parts.join('\n');
}

(async () => {
  let cdp = null;
  try {
    const target = await CDP.findPageTarget(cfg.PORT, 5000);
    cdp = new CDP(target.webSocketDebuggerUrl);
    await cdp.connect();

    // Stop the old engine first: its timers would go on running beside the new one.
    await cdp.send('Runtime.evaluate', {
      expression: "(()=>{const a=window.__bd_auto;"
        + "const was=!!(a&&a.state.running);const cfg=a?Object.assign({},a.cfg):null;"
        + "if(was)a.stop('reloading the engine');"
        + "window.__bd_reload={was,cfg};return was})()",
      returnByValue: true,
    });

    const src = engineSource();
    const out = await cdp.send('Runtime.evaluate', { expression: src, returnByValue: true });
    if (out.exceptionDetails) {
      console.error('the engine did not evaluate:',
        out.exceptionDetails.exception?.description || out.exceptionDetails.text);
      process.exit(1);
    }

    // Put back whatever was running, with the settings it had.
    const back = await cdp.send('Runtime.evaluate', {
      expression: "(()=>{const r=window.__bd_reload||{};const a=window.__bd_auto;"
        + "if(!a)return 'no autoplay';if(r.cfg)Object.assign(a.cfg,r.cfg);"
        + "if(r.was)a.start();"
        + "return JSON.stringify({running:a.state.running,cfg:a.cfg,"
        + "modules:Object.keys(window.__bd_mod||{}).length})})()",
      returnByValue: true,
    });
    console.log(`${(src.length / 1024) | 0} KB evaluated`);
    console.log(back.result?.value);
  } catch (e) {
    console.error(`could not reach the game (port ${cfg.PORT}): ${e.message}`);
    console.error('It has to be running under the launcher.');
    process.exit(1);
  } finally {
    if (cdp) cdp.close();
  }
})();
