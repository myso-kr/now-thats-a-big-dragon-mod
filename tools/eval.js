'use strict';
// Evaluates an expression inside the running game. For diagnosis.
//
//   node tools/eval.js "__bd_auto.state.phase"
//   node tools/eval.js "JSON.stringify(__bd_auto.calib(), null, 1)"
//
// No external dependencies - this repository runs on Node's built-ins alone, and
// lib/cdp.js already knows how to speak CDP.

const { CDP } = require('../lib/cdp');
const cfg = require('../config');

const expr = process.argv.slice(2).join(' ');
if (!expr) {
  console.error('usage: node tools/eval.js "<expression>"');
  process.exit(2);
}

(async () => {
  let cdp = null;
  try {
    const target = await CDP.findPageTarget(cfg.PORT, 5000);
    cdp = new CDP(target.webSocketDebuggerUrl);
    await cdp.connect();
    const res = await cdp.send('Runtime.evaluate', {
      expression: expr,
      returnByValue: true,
      awaitPromise: true,
    });
    if (res.exceptionDetails) {
      const d = res.exceptionDetails;
      console.error('exception:', (d.exception && d.exception.description) || d.text);
      process.exitCode = 1;
    } else {
      const v = res.result && res.result.value;
      console.log(v !== null && typeof v === 'object' ? JSON.stringify(v, null, 1) : String(v));
    }
  } catch (e) {
    console.error(`could not connect (port ${cfg.PORT}): ${e.message}`);
    console.error('Check that the game is running under the launcher.');
    process.exitCode = 1;
  } finally {
    if (cdp) cdp.close();
  }
})();
