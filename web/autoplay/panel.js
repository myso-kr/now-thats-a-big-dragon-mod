(() => {
  'use strict';
  if (window.__BD_AUTO_PANEL__) return;
  window.__BD_AUTO_PANEL__ = true;

  const TOGGLE_KEY = 'F9';
  const A = () => window.__bd_auto;

  const CSS = `
  /* Same size scale and palette as the cheat panel. inherit is not allowed in the
     font shorthand. */
  #bda{--bg:#12151c;--bg2:#171b24;--line:#252b38;--fg:#dfe4ee;--dim:#7c879e;
    --accent:#4d9a6a;--accent2:#3a7a53;--input:#0b0d12;--warn:#d98b6a;
    --fs:12px;--fs-sm:11px;--fs-xs:10px;--h:26px;--h-sm:22px;
    --ui:"Segoe UI","Malgun Gothic",sans-serif;
    --mono:ui-monospace,Consolas,"Courier New",monospace;
    position:fixed;top:14px;left:14px;width:352px;z-index:2147483646;
    background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:8px;
    font-family:var(--ui);font-size:var(--fs);line-height:1.5;
    box-shadow:0 10px 40px #0009;display:none}
  #bda.on{display:block}
  #bda *{box-sizing:border-box}
  #bda button,#bda input,#bda select{font-family:var(--ui);font-size:var(--fs);line-height:1.4;color:var(--fg);margin:0}

  #bda .hd{display:flex;align-items:center;gap:6px;height:34px;padding:0 10px;background:var(--bg2);
    border-bottom:1px solid var(--line);border-radius:8px 8px 0 0;cursor:move;user-select:none}
  #bda .hd b{font-weight:600;letter-spacing:.02em}
  #bda .hd small{color:var(--dim);font-size:var(--fs-sm);margin-left:auto;font-family:var(--mono)}
  #bda .hd button{background:none;border:0;color:var(--dim);cursor:pointer;width:20px;height:20px;padding:0;font-size:15px;line-height:1}
  #bda .hd button:hover{color:var(--fg)}

  #bda .master{display:flex;align-items:center;gap:8px;height:30px;padding:0 10px;
    background:var(--bg2);border-bottom:1px solid var(--line);cursor:pointer;user-select:none}
  #bda .master.on{background:#15221b;border-bottom-color:var(--accent2)}
  #bda .master.off{background:#221a17;border-bottom-color:var(--warn)}
  #bda .master .lbl{font-weight:600}
  #bda .master.on .lbl{color:var(--accent)}
  #bda .master.off .lbl{color:var(--warn)}
  #bda .master .sub{color:var(--dim);font-size:var(--fs-sm)}
  #bda .master .pips{margin-left:auto;display:flex;gap:3px}
  #bda .master .pip{width:9px;height:12px;background:var(--line);border-radius:1px}
  #bda .master .pip.on{background:var(--accent)}
  #bda .master .pip.risk{background:var(--warn)}
  #bda .master .cnt{font-family:var(--mono);font-size:var(--fs-sm);color:var(--dim);min-width:26px;text-align:right}

  #bda .strip{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border-bottom:1px solid var(--line)}
  #bda .strip div{background:var(--bg);padding:5px 8px;min-width:0}
  #bda .strip span{display:block;color:var(--dim);font-size:var(--fs-xs);letter-spacing:.04em}
  #bda .strip b{display:block;font-family:var(--mono);font-size:var(--fs);font-weight:600;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  #bda .strip b.run{color:var(--accent)}
  #bda .strip b.hold{color:var(--warn)}
  #bda .strip b.off{color:var(--warn)}

  #bda .tabs{display:flex;background:var(--bg2);border-bottom:1px solid var(--line)}
  #bda .tabs button{flex:1;height:30px;background:none;border:0;border-bottom:2px solid transparent;
    color:var(--dim);cursor:pointer;white-space:nowrap}
  #bda .tabs button.sel{color:var(--fg);border-bottom-color:var(--accent)}

  #bda .body{padding:10px;max-height:52vh;overflow-y:auto}
  #bda h4{margin:0 0 6px;font-family:var(--ui);font-size:var(--fs-xs);font-weight:600;line-height:1;
    letter-spacing:.09em;text-transform:uppercase;color:var(--dim)}
  #bda .sw{display:flex;align-items:center;gap:8px;height:var(--h);cursor:pointer;user-select:none}
  #bda .sw input{width:14px;height:14px;accent-color:var(--accent);margin:0}
  #bda .sw .nm{min-width:44px}
  #bda .sw .ds{color:var(--dim);font-size:var(--fs-sm);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  #bda .sw .st{margin-left:auto;color:var(--dim);font-size:var(--fs-sm);font-family:var(--mono)}
  #bda .sw.risk .nm{color:var(--warn)}
  #bda .grp{margin-bottom:12px}
  #bda .grp:last-child{margin-bottom:0}
  #bda .row{display:flex;gap:5px;align-items:center;margin-bottom:5px}
  #bda .row .lb{flex:0 0 66px;color:var(--dim);font-size:var(--fs-sm)}
  #bda .seg{display:flex;gap:4px;flex:1}
  #bda .seg button{flex:1;height:var(--h-sm);background:#232a37;border:1px solid var(--line);
    border-radius:4px;cursor:pointer;font-size:var(--fs-sm)}
  #bda .seg button.sel{background:var(--accent2);border-color:var(--accent)}
  #bda select.pick{flex:1;min-width:0;height:var(--h-sm);background:#232a37;
    border:1px solid var(--line);border-radius:4px;cursor:pointer;
    font-size:var(--fs-sm);font-family:inherit;color:inherit;padding:0 6px}
  #bda select.pick:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
  #bda .hint{color:var(--dim);font-size:var(--fs-sm);line-height:1.45;margin-top:6px}
  #bda .warn{color:var(--warn);font-size:var(--fs-sm);line-height:1.45;margin-top:6px}

  #bda .log{font-family:var(--mono);font-size:var(--fs-sm);line-height:1.6}
  #bda .log div{display:flex;gap:6px;white-space:nowrap}
  #bda .log .tg{color:var(--dim);flex:0 0 30px}
  #bda .log .tx{overflow:hidden;text-overflow:ellipsis}
  #bda .log .n{margin-left:auto;color:var(--dim)}
  #bda .log .w .tx{color:var(--warn)}
  `;

  // Chapter names ride in front of the patched bundle as __bd_levelNames; the id stands
  // in otherwise. Read on each call rather than once at load: this file is injected
  // before the document, so at load time the bundle - and the names with it - has not
  // run yet, and a value captured here would always be the fallback.
  const CHP_NM = () => {
    const m = (typeof window !== 'undefined' && window.__bd_levelNames) || {};
    return { campaign: m.mainGame || 'Campaign', dummy: m.dummy || 'Dummy',
      newGamePlus: m.newGamePlus || 'Resource management', infinite: m.infinite || 'Infinite',
      kingBattle: m.kingBattle || 'King' };
  };

  // State labels in Korean. Anything but RUNNING means nothing is happening, so it is coloured as a warning.
  const PHASE_NM = { STOPPED: 'off', RUNNING: 'running', IDLE: 'idle', HOLD: 'holding' };

  const SWITCHES = [
    { key: 'buy', nm: 'Buying', ds: 'units, upgrades, resources' },
    { key: 'combat', nm: 'Combat', ds: 'clicking, mana, inspiration' },
    { key: 'dialog', nm: 'Dialogue', ds: 'advancing, choices' },
  ];

  let panel = null;
  let tab = 'ctl';
  const $ = (s) => panel.querySelector(s);

  function build() {
    const st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    panel = document.createElement('div');
    panel.id = 'bda';
    panel.innerHTML = `
      <div class="hd"><b>Autoplay</b><small>${TOGGLE_KEY}</small><button id="x">×</button></div>
      <div class="master" id="m-row"><input type="checkbox" id="m-on">
        <span class="lbl" id="m-lbl">Autoplay</span><span class="sub" id="m-sub"></span>
        <span class="pips" id="m-pips"></span><span class="cnt" id="m-cnt"></span></div>
      <div class="strip">
        <div><span>State</span><b id="s-st">-</b></div>
        <div><span>Last</span><b id="s-la">-</b></div>
        <div><span>Session</span><b id="s-se">-</b></div>
      </div>
      <div class="tabs">
        <button data-tab="ctl">Control</button><button data-tab="log">Log</button>
      </div>
      <div class="body"></div>`;
    document.body.appendChild(panel);

    panel.querySelectorAll('[data-tab]').forEach((b) => { b.onclick = () => { tab = b.dataset.tab; render(); }; });
    $('#x').onclick = toggle;
    $('#m-on').onchange = (e) => { if (e.target.checked) A().start(); else A().stop(); refresh(); };
    panel.querySelector('.master').onclick = (e) => {
      if (e.target.id === 'm-on') return;
      $('#m-on').checked = !$('#m-on').checked;
      $('#m-on').dispatchEvent(new Event('change'));
    };
    for (const t of ['keydown', 'keyup', 'keypress']) {
      panel.addEventListener(t, (e) => { if (e.key !== TOGGLE_KEY) e.stopPropagation(); }, true);
    }
    drag(panel, panel.querySelector('.hd'));
    render();
  }

  function drag(el, handle) {
    handle.addEventListener('pointerdown', (e) => {
      if (e.target.tagName === 'BUTTON') return;
      const r = el.getBoundingClientRect();
      const ox = r.left; const oy = r.top; const sx = e.clientX; const sy = e.clientY;
      el.style.left = ox + 'px'; el.style.top = oy + 'px';
      const mv = (ev) => {
        el.style.left = Math.max(0, Math.min(innerWidth - 60, ox + ev.clientX - sx)) + 'px';
        el.style.top = Math.max(0, Math.min(innerHeight - 40, oy + ev.clientY - sy)) + 'px';
      };
      const up = () => { removeEventListener('pointermove', mv); removeEventListener('pointerup', up); };
      addEventListener('pointermove', mv); addEventListener('pointerup', up);
    });
  }

  function render() {
    panel.querySelectorAll('[data-tab]').forEach((b) => b.classList.toggle('sel', b.dataset.tab === tab));
    const body = $('.body');
    body.scrollTop = 0;
    if (tab === 'ctl') renderCtl(body); else renderLog(body);
    refresh();
  }

  function renderCtl(body) {
    const c = A().cfg;
    body.innerHTML = `
      <div class="grp"><h4>What it handles</h4>
        ${SWITCHES.map((s) => `
          <label class="sw${s.risk ? ' risk' : ''}">
            <input type="checkbox" data-sw="${s.key}" ${c[s.key] ? 'checked' : ''}>
            <span class="nm">${s.nm}</span><span class="ds">${s.ds}</span>
            <span class="st" data-st="${s.key}"></span>
          </label>`).join('')}
      </div>
      <div class="grp"><h4>Settings</h4>
        <div class="row"><span class="lb">Gold to keep</span>
          <span class="seg" id="seg-res">${[0, 10, 25, 50].map((v) => `<button data-res="${v}">${v}%</button>`).join('')}</span></div>
        <div class="row"><span class="lb">Choices</span>
          <span class="seg" id="seg-ask"><button data-ask="0">Decide</button><button data-ask="1">Ask me</button></span></div>
        <div class="row"><span class="lb">After a clear</span>
          <span class="seg" id="seg-chp">
            <button data-chp="off">Stop</button>
            <button data-chp="repeat">Repeat</button>
            <button data-chp="advance">Next chapter</button>
          </span></div>
        <div class="row" id="row-rep" ${c.chapterMode === 'repeat' ? '' : 'hidden'}>
          <span class="lb">Chapter to repeat</span>
          <select class="pick" id="sel-rep">
            <option value="">the current one</option>
            ${(A().CHAPTERS || []).map((x) =>
              `<option value="${x.id}">${CHP_NM()[x.id] || x.id}</option>`).join('')}
          </select></div>
        <div class="hint" id="chp-hint"></div>
        <div class="hint">The 25 units and 88 upgrades are handled for you.</div>
        <div class="warn" id="stop-why" hidden></div>
      </div>`;

    body.querySelectorAll('[data-sw]').forEach((el) => {
      el.onchange = () => {
        const a = A();
        a.cfg[el.dataset.sw] = el.checked;
        // Combat includes auto-clicking. Turning the switch off stops the clicking too.
        if (el.dataset.sw === 'combat' && a.state.running) {
          if (el.checked) a.startClick(); else a.stopClick();
        }
        refresh();
      };
    });
    body.querySelectorAll('[data-res]').forEach((b) => {
      b.onclick = () => { A().cfg.reservePct = Number(b.dataset.res); refresh(); };
    });
    body.querySelectorAll('[data-ask]').forEach((b) => {
      b.onclick = () => { A().cfg.askChoices = b.dataset.ask === '1'; refresh(); };
    });
    body.querySelectorAll('[data-chp]').forEach((b) => {
      b.onclick = () => {
        A().cfg.chapterMode = b.dataset.chp;
        const row = $('#row-rep');
        if (row) row.hidden = b.dataset.chp !== 'repeat';
        refresh();
      };
    });
    const sel = body.querySelector('#sel-rep');
    if (sel) {
      sel.value = A().cfg.repeatChapter || '';
      sel.onchange = () => { A().cfg.repeatChapter = sel.value || null; refresh(); };
    }
  }

  function renderLog(body) {
    body.innerHTML = '<div class="log" id="log"></div>';
    paintLog();
  }

  const ago = (t) => {
    if (!t) return '—';
    const s = Math.floor((Date.now() - t) / 1000);
    return s < 60 ? `${s}s` : `${Math.floor(s / 60)}m`;
  };

  function paintLog() {
    const el = $('#log');
    if (!el || tab !== 'log') return;
    el.innerHTML = A().log().map((r) => `<div class="${r.level === 'warn' ? 'w' : ''}">`
      + `<span class="tg">${r.tag}</span><span class="tx">${r.text}</span>`
      + `${r.n > 1 ? `<span class="n">×${r.n}</span>` : ''}</div>`).join('')
      || '<div class="tx" style="color:var(--dim)">nothing logged yet</div>';
  }

  function refresh() {
    if (!panel || !panel.classList.contains('on')) return;
    const a = A();
    if (!a) return;
    const s = a.state;
    const c = a.cfg;

    $('#m-on').checked = s.running;
    const on = SWITCHES.filter((x) => c[x.key]).length;
    $('#m-cnt').textContent = `${on}/${SWITCHES.length}`;
    $('#m-pips').innerHTML = SWITCHES.map((x) => `<span class="pip${c[x.key] ? (x.risk ? ' risk' : ' on') : ''}"></span>`).join('');

    const row = $('#m-row');
    row.classList.toggle('on', s.running);
    row.classList.toggle('off', !s.running);
    $('#m-lbl').textContent = s.running ? 'Autoplay is on' : 'Autoplay is off';
    $('#m-sub').textContent = s.running ? '' : 'press to start';

    const st = $('#s-st');
    st.textContent = s.running
      ? `${PHASE_NM[s.phase] || s.phase} ${on}/${SWITCHES.length}` : 'off';
    st.className = !s.running ? 'off'
      : (s.phase === 'RUNNING' ? 'run' : 'hold');
    $('#s-la').textContent = s.lastAction ? `${ago(s.lastActionAt)} ${s.lastAction}` : '—';
    $('#s-se').textContent = s.startedAt
      ? `${s.actions.toLocaleString()} · ${ago(s.startedAt)}` : '—';

    panel.querySelectorAll('[data-sw]').forEach((el) => { el.checked = c[el.dataset.sw]; });
    panel.querySelectorAll('[data-res]').forEach((b) => b.classList.toggle('sel', Number(b.dataset.res) === c.reservePct));
    panel.querySelectorAll('[data-ask]').forEach((b) => b.classList.toggle('sel', (b.dataset.ask === '1') === c.askChoices));
    panel.querySelectorAll('[data-chp]').forEach((b) => b.classList.toggle('sel', b.dataset.chp === c.chapterMode));
    const selRep = panel.querySelector('#sel-rep');
    if (selRep && selRep.value !== (c.repeatChapter || '')) selRep.value = c.repeatChapter || '';
    const repRow = panel.querySelector('#row-rep');
    if (repRow) repRow.hidden = c.chapterMode !== 'repeat';
    const hint = panel.querySelector('#chp-hint');
    if (hint) {
      hint.textContent = {
        off: 'Stops once the boss is down.',
        repeat: c.repeatChapter
          ? `Repeats the ${CHP_NM()[c.repeatChapter] || c.repeatChapter} chapter over and over.`
          : 'Repeats the current chapter over and over.',
        advance: 'Moves on to the next chapter, and repeats the current one when there is none.',
      }[c.chapterMode] || '';
    }
    const why = $('#stop-why');
    if (why) { why.hidden = !s.stopReason; why.textContent = s.stopReason; }
    paintLog();
  }

  function toggle() {
    if (!panel) build();
    const open = !panel.classList.contains('on');
    panel.classList.toggle('on', open);
    if (open) refresh();
  }

  addEventListener('keydown', (e) => {
    if (e.key !== TOGGLE_KEY) return;
    e.preventDefault(); e.stopPropagation();
    if (e.shiftKey) {                       // Stop at once, without opening the panel
      if (A() && A().state.running) { A().stop('stopped by the player'); }
      return;
    }
    toggle();
  }, true);

  const boot = setInterval(() => {
    if (window.__bd_auto && document.body) {
      clearInterval(boot);
      setInterval(refresh, 500);
      console.log(`[autoplay] panel ready - ${TOGGLE_KEY}`);
    }
  }, 300);
})();
