// The cheat panel's stylesheet. Markup and behaviour live elsewhere.
//
// Size system: body 12 / secondary 11 / label 10, control height 26 and 22 for the
// small ones. Note that the `font` shorthand cannot take `inherit` — the whole
// declaration would be void — so font-family and font-size are set separately.
(function (root) {
  'use strict';

  const CSS = `
  /* One size scale throughout: body 12, secondary 11, labels 10; controls 26 high,
     small ones 22. Note that inherit is not allowed in the font shorthand - it voids
     the whole declaration - so font-family and font-size are set separately. */
  #bd{--bg:#12151c;--bg2:#171b24;--line:#252b38;--fg:#dfe4ee;--dim:#7c879e;
    --accent:#4d9a6a;--accent2:#3a7a53;--input:#0b0d12;--warn:#d98b6a;
    --fs:12px;--fs-sm:11px;--fs-xs:10px;--h:26px;--h-sm:22px;--gap:6px;
    --ui:"Segoe UI","Malgun Gothic",sans-serif;
    --mono:ui-monospace,Consolas,"Courier New",monospace;
    position:fixed;top:14px;right:14px;width:352px;z-index:2147483647;
    background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:8px;
    font-family:var(--ui);font-size:var(--fs);line-height:1.5;
    box-shadow:0 10px 40px #0009;display:none}
  #bd.on{display:block}
  #bd *{box-sizing:border-box}
  #bd button,#bd input,#bd select,#bd textarea{
    font-family:var(--ui);font-size:var(--fs);line-height:1.4;color:var(--fg);margin:0}

  #bd .hd{display:flex;align-items:center;gap:var(--gap);height:34px;padding:0 10px;
    background:var(--bg2);border-bottom:1px solid var(--line);border-radius:8px 8px 0 0;
    cursor:move;user-select:none}
  #bd .hd b{font-weight:600;letter-spacing:.02em}
  #bd .hd small{color:var(--dim);font-size:var(--fs-sm);margin-left:auto;font-family:var(--mono)}
  #bd .hd button{background:none;border:0;color:var(--dim);cursor:pointer;
    width:20px;height:20px;padding:0;font-size:15px;line-height:1}
  #bd .hd button:hover{color:var(--fg)}

  #bd .strip{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;
    background:var(--line);border-bottom:1px solid var(--line)}
  #bd .strip div{background:var(--bg);padding:5px 8px;min-width:0}
  #bd .strip span{display:block;color:var(--dim);font-size:var(--fs-xs);letter-spacing:.04em}
  #bd .strip b{display:block;font-family:var(--mono);font-size:var(--fs);font-weight:600;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

  #bd .tabs{display:flex;background:var(--bg2);border-bottom:1px solid var(--line)}
  #bd .tabs button{flex:1;height:30px;padding:0 2px;background:none;border:0;
    border-bottom:2px solid transparent;color:var(--dim);cursor:pointer;white-space:nowrap}
  #bd .tabs button:hover{color:var(--fg)}
  #bd .tabs button.sel{color:var(--fg);border-bottom-color:var(--accent)}

  #bd .body{padding:10px;max-height:62vh;overflow-y:auto}
  #bd .grp{margin-bottom:14px}
  #bd .grp:last-child{margin-bottom:0}
  #bd h4{margin:0 0 6px;font-family:var(--ui);font-size:var(--fs-xs);font-weight:600;
    line-height:1;letter-spacing:.09em;text-transform:uppercase;color:var(--dim)}
  #bd .row{display:flex;gap:5px;align-items:center;margin-bottom:5px}
  #bd .row:last-child{margin-bottom:0}

  #bd input[type=text],#bd input[type=number],#bd select{
    flex:1;min-width:0;height:var(--h);padding:0 7px;font-family:var(--mono);
    background:var(--input);border:1px solid var(--line);border-radius:4px}
  #bd select{padding:0 4px}
  #bd textarea{width:100%;height:88px;padding:6px 7px;font-family:var(--mono);resize:vertical;
    background:var(--input);border:1px solid var(--line);border-radius:4px}
  #bd input:focus,#bd select:focus,#bd textarea:focus{outline:0;border-color:var(--accent2)}
  #bd input[type=range]{flex:1;height:var(--h);accent-color:var(--accent);padding:0}
  #bd input[type=checkbox]{width:14px;height:14px;accent-color:var(--accent)}

  #bd button.b{height:var(--h);padding:0 10px;background:#232a37;border:1px solid var(--line);
    border-radius:4px;cursor:pointer;white-space:nowrap}
  #bd button.b:hover{background:#2c3546}
  #bd button.b.p{background:var(--accent2);border-color:var(--accent)}
  #bd button.b.p:hover{background:var(--accent)}
  #bd button.b.on{background:var(--accent);border-color:var(--accent)}

  #bd .hint{color:var(--dim);font-size:var(--fs-sm);line-height:1.45;margin-top:5px}
  #bd .warn{color:var(--warn);font-size:var(--fs-sm);line-height:1.45;margin-top:5px}
  #bd label.ck{display:flex;align-items:center;gap:7px;cursor:pointer;user-select:none}

  #bd .list{border:1px solid var(--line);border-radius:5px;overflow:hidden}
  #bd .up{display:grid;grid-template-columns:1fr auto auto auto auto;gap:4px;
    align-items:center;padding:3px 6px;border-bottom:1px solid var(--line)}
  #bd .up:last-child{border-bottom:0}
  #bd .up.max{background:#161d18}
  #bd .up .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  #bd .up .nm i{color:var(--dim);font-style:normal;font-size:var(--fs-xs)}
  #bd .up .lv{min-width:46px;text-align:right;color:var(--dim);
    font-family:var(--mono);font-size:var(--fs-sm);font-weight:600}
  #bd .up button{width:var(--h-sm);height:var(--h-sm);padding:0;background:#232a37;
    border:1px solid var(--line);border-radius:3px;cursor:pointer}
  #bd .up button:hover{background:#2c3546}
  #bd .up button.mx{width:auto;padding:0 7px;font-size:var(--fs-sm)}

  #bd .res{display:grid;grid-template-columns:repeat(3,1fr);gap:3px 6px;margin-top:7px}
  #bd .res div{display:flex;justify-content:space-between;gap:5px;min-width:0;
    font-size:var(--fs-sm);color:var(--dim)}
  #bd .res b{color:var(--fg);font-family:var(--mono);font-weight:600;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

  #bd-toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:2147483647;
    max-width:70vw;padding:9px 14px;border-radius:6px;pointer-events:none;
    background:#1b1108ee;color:#f0d6b8;border:1px solid #6b4a24;
    font:12px/1.4 "Segoe UI","Malgun Gothic",sans-serif;
    box-shadow:0 6px 24px #0008;opacity:0;transition:opacity .25s}

  #bd .val{font-family:var(--mono);font-size:var(--fs-sm)}
  #bd .muted{color:var(--dim);font-size:var(--fs-sm)}
  `;

  const api = { CSS };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too. The usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== "undefined") {
    (window.__bd_cheat_mod = window.__bd_cheat_mod || {}).css = api;
  } else {
    (root.__bd_cheat_mod = root.__bd_cheat_mod || {}).css = api;
  }
  if (typeof module !== "undefined" && module.exports) module.exports = api;
}(typeof self !== "undefined" ? self : globalThis));
