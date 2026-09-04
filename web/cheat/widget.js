// The cheat panel: its screens, and the wiring that gives the modules their
// dependencies. No game rules and no state handling live in this file.
//
//   widget/css.js           the stylesheet
//   widget/format.js        number formatting
//   widget/store.js         reaching the game's real per-slot state
//   widget/upgrades.js      moving upgrade levels
//   widget/achievements.js  keeping cheated progress off Steam
//   widget/speed.js         game speed, and backing off when it cannot keep up
//
// Panel text stays Korean: this ships with the Korean patch and its readers are the
// people using that. Console output is English, like the launcher's.
(() => {
  'use strict';
  if (window.__BD_CHEAT__) return;
  window.__BD_CHEAT__ = true;

  const TOGGLE_KEY = 'F8';

  const mod = (name) => (window.__bd_cheat_mod && window.__bd_cheat_mod[name]) || null;
  const REQUIRED = ['css', 'format', 'store', 'upgrades', 'achievements', 'speed'];
  const missing = REQUIRED.filter((n) => !mod(n));
  if (missing.length) {
    console.error(`[cheat] not loaded: ${missing.map((n) => `widget/${n}.js`).join(', ')}`);
    return;
  }

  const { num, fmt, short } = mod('format');
  const store = mod('store').create({ win: window });
  const upgrades = mod('upgrades').create({ win: window, slotStore: store.slotStore });
  const { levelTo, eachUpgrade, limitOf } = mod('upgrades');

  const state = { blockAchievements: true, open: false, tab: 'res', snapshot: null };

  const achievements = mod('achievements').create({
    win: window,
    blocked: () => state.blockAchievements,
  });

  const speed = mod('speed').create({
    win: window,
    doc: document,
    store,
    notify: (msg, top) => {
      console.warn('[cheat] speed adjusted:', msg, top);
      toast(`cheat: ${msg}`);
    },
  });
  const { MIN_SPEED, MAX_SPEED } = mod('speed');

  // Leaving a shortened tick in the save is the one lasting harm this widget can do,
  // so it is undone on every way out.
  addEventListener('beforeunload', speed.restoreTick);
  addEventListener('pagehide', speed.restoreTick);

  // ── Labels ───────────────────────────────────────────────────────
  const RESOURCES = [
    { key: 'gold', label: 'Gold' },
    { key: 'wood', label: 'Wood' },
    { key: 'ore', label: 'Ore' },
    { key: 'food', label: 'Food' },
    { key: 'mana', label: 'Mana' },
  ];

  const CATEGORIES = {
    click: 'Click', warrior: 'Warrior', wizard: 'Wizard', elf: 'Elf',
    thief: 'Thief', bard: 'Bard', cleric: 'Cleric', catapult: 'Catapult',
  };

  const TABS = [['res', 'Resources'], ['upg', 'Upgrades'], ['adv', 'Advanced']];

  // ── Panel shell ──────────────────────────────────────────────────
  let panel = null;
  const $ = (sel, root) => (root || panel).querySelector(sel);

  /** Visible even with the panel closed, so an automatic intervention is noticed. */
  let toastEl = null;
  let toastTimer = null;
  function toast(msg) {
    if (!document.body) return;
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.id = 'bd-toast';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.style.opacity = '1';
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { if (toastEl) toastEl.style.opacity = '0'; }, 6000);
  }

  function build() {
    const style = document.createElement('style');
    style.textContent = mod('css').CSS;
    document.head.appendChild(style);

    panel = document.createElement('div');
    panel.id = 'bd';
    panel.innerHTML = `
      <div class="hd"><b>Cheats</b><small>${TOGGLE_KEY}</small><button id="x" title="close">×</button></div>
      <div class="strip">
        <div><span>Chapter</span><b id="s-lvl">-</b></div>
        <div><span>Gold</span><b id="s-gold">-</b></div>
        <div><span>Speed</span><b id="s-ts">-</b></div>
      </div>
      <div class="tabs">${TABS.map(([k, t]) => `<button data-tab="${k}">${t}</button>`).join('')}</div>
      <div class="body"></div>`;
    document.body.appendChild(panel);

    panel.querySelectorAll('[data-tab]').forEach((b) => {
      b.onclick = () => { state.tab = b.dataset.tab; render(); };
    });
    $('#x').onclick = toggle;

    // Keystrokes inside the widget must not leak out and drive the game.
    for (const t of ['keydown', 'keyup', 'keypress']) {
      panel.addEventListener(t, (e) => { if (e.key !== TOGGLE_KEY) e.stopPropagation(); }, true);
    }
    makeDraggable(panel, $('.hd'));
    render();
  }

  function makeDraggable(el, handle) {
    let sx = 0; let sy = 0; let ox = 0; let oy = 0;
    handle.addEventListener('pointerdown', (e) => {
      if (e.target.tagName === 'BUTTON') return;
      const r = el.getBoundingClientRect();
      ox = r.left; oy = r.top; sx = e.clientX; sy = e.clientY;
      el.style.left = `${ox}px`; el.style.top = `${oy}px`; el.style.right = 'auto';
      const move = (ev) => {
        el.style.left = `${Math.max(0, Math.min(innerWidth - 60, ox + ev.clientX - sx))}px`;
        el.style.top = `${Math.max(0, Math.min(innerHeight - 40, oy + ev.clientY - sy))}px`;
      };
      const up = () => {
        removeEventListener('pointermove', move);
        removeEventListener('pointerup', up);
      };
      addEventListener('pointermove', move);
      addEventListener('pointerup', up);
    });
  }

  // ── Screens ──────────────────────────────────────────────────────
  function render() {
    panel.querySelectorAll('[data-tab]').forEach((b) => b.classList.toggle('sel', b.dataset.tab === state.tab));
    const body = $('.body');
    body.scrollTop = 0;
    if (state.tab === 'res') renderRes(body);
    else if (state.tab === 'upg') renderUpg(body);
    else renderAdv(body);
    refresh();
  }

  function renderRes(body) {
    const bridged = !!store.slotStore('currency');
    body.innerHTML = `
      <div class="grp">
        <h4>Resources</h4>
        <div class="row">
          <select id="r-key" style="flex:0 0 84px">
            ${RESOURCES.map((r) => `<option value="${r.key}">${r.label}</option>`).join('')}
          </select>
          <input type="text" id="r-in" placeholder="a value">
          <button class="b p" id="r-set">Set</button>
        </div>
        <div class="row">
          <button class="b" data-add="1000">+1k</button>
          <button class="b" data-add="100000">+100k</button>
          <button class="b" data-add="10000000">+10M</button>
          <button class="b" id="r-x10">×10</button>
        </div>
        <div class="res" id="r-now"></div>
        ${bridged ? '' : '<div class="warn">No store bridge. Resources can only be changed when the game is started by the launcher.</div>'}
      </div>
      <div class="grp">
        <h4>Game speed</h4>
        <div class="row">
          <input type="range" id="ts" min="${MIN_SPEED}" max="${MAX_SPEED}" step="0.25" value="${speed.value}">
          <b class="val" id="ts-v" style="flex:0 0 46px;text-align:right"></b>
        </div>
        <div class="row">
          <button class="b" data-ts="1">1×</button><button class="b" data-ts="2">2×</button>
          <button class="b" data-ts="4">4×</button><button class="b" data-ts="8">8×</button>
        </div>
        <div class="hint">Moves the display and the simulation (gold, events) together.
        It steps back down on its own when the game cannot keep up.</div>
        <div class="warn" id="sp-notice" hidden></div>
      </div>`;

    const key = () => $('#r-key').value;
    const bump = (fn) => { store.setRes(key(), fn(store.getRes(key()) || 0)); refresh(); };
    $('#r-set').onclick = () => {
      const n = num($('#r-in').value);
      if (n !== null) store.setRes(key(), n);
      refresh();
    };
    body.querySelectorAll('[data-add]').forEach((b) => {
      b.onclick = () => bump((v) => v + Number(b.dataset.add));
    });
    $('#r-x10').onclick = () => bump((v) => v * 10);

    const setTs = (v) => { speed.setSpeed(v); refresh(); };
    $('#ts').oninput = (e) => setTs(Number(e.target.value));
    body.querySelectorAll('[data-ts]').forEach((b) => { b.onclick = () => setTs(Number(b.dataset.ts)); });
    syncSpeedUI();
  }

  /** The guard can lower the speed on its own; the panel has to follow. */
  function syncSpeedUI() {
    if (!panel) return;
    const sl = $('#ts');
    if (sl && Number(sl.value) !== speed.value) sl.value = speed.value;
    const tv = $('#ts-v');
    if (tv) tv.textContent = `${speed.value}×`;
    panel.querySelectorAll('[data-ts]').forEach((b) => {
      b.classList.toggle('on', Number(b.dataset.ts) === speed.value);
    });
  }

  function renderUpg(body) {
    const tree = upgrades.tree();
    if (!tree) { body.innerHTML = '<div class="warn">No upgrade store found.</div>'; return; }
    body.innerHTML = `
      <div class="grp">
        <div class="row">
          <select id="u-cat" style="flex:0 0 96px">
            <option value="">All branches</option>
            ${Object.keys(tree).map((c) => `<option value="${c}">${CATEGORIES[c] || c}</option>`).join('')}
          </select>
          <input type="text" id="u-q" placeholder="search by name">
        </div>
        <div class="row">
          <button class="b" id="u-unlock">Unlock all</button>
          <button class="b" id="u-max">Max all</button>
          <button class="b" id="u-undo" disabled>Undo</button>
        </div>
        <div class="hint" id="u-count"></div>
      </div>
      <div class="list" id="u-list"></div>`;

    // Bulk changes are hard to undo by hand, so one step back is always available.
    const snap = () => { state.snapshot = structuredClone(upgrades.tree()); $('#u-undo').disabled = false; };

    $('#u-unlock').onclick = () => {
      snap();
      const s = store.slotStore('upgrades');
      if (s.getState().unlockAllUpgrades) s.getState().unlockAllUpgrades();
      else upgrades.applyLevels((t) => eachUpgrade(t, (u) => { u.isUnlocked = true; u.status = 'unlocked'; }));
      drawList();
    };
    $('#u-max').onclick = () => {
      snap();
      upgrades.applyLevels((t) => eachUpgrade(t, (u) => {
        // Unlimited upgrades have no maximum to go to.
        if (Number.isFinite(limitOf(u))) levelTo(u, limitOf(u));
      }));
      drawList();
    };
    $('#u-undo').onclick = () => {
      if (!state.snapshot) return;
      store.slotStore('upgrades').getState().setUpgrades(structuredClone(state.snapshot));
      state.snapshot = null;
      $('#u-undo').disabled = true;
      drawList();
    };
    $('#u-cat').onchange = drawList;
    $('#u-q').oninput = drawList;
    drawList();
  }

  function drawList() {
    const list = $('#u-list');
    if (!list) return;
    const tree = upgrades.tree();
    const cat = $('#u-cat').value;
    const q = $('#u-q').value.trim().toLowerCase();

    const rows = [];
    let owned = 0;
    let total = 0;
    eachUpgrade(tree, (u, id, c) => {
      total += 1;
      if (u.purchased > 0) owned += 1;
      if (cat && c !== cat) return;
      const name = upgrades.nameOf(id);
      if (q && !name.toLowerCase().includes(q) && !id.toLowerCase().includes(q)) return;
      rows.push({ u, id, cat: c, name });
    });

    $('#u-count').textContent = `${owned} of ${total} owned, ${rows.length} shown`;
    list.innerHTML = rows.map(({ u, id, cat: c, name }) => {
      const lim = limitOf(u);
      const limText = Number.isFinite(lim) ? lim : '∞';
      const maxed = u.purchased >= lim;
      return `<div class="up${maxed ? ' max' : ''}" data-c="${c}" data-i="${id}">
        <div class="nm">${name} <i>${CATEGORIES[c] || c}</i></div>
        <div class="lv">${u.purchased}/${limText}</div>
        <button data-d="-1" title="one less">−</button>
        <button data-d="1" title="one more">+</button>
        <button class="mx" data-d="max" title="maximum">Max</button>
      </div>`;
    }).join('') || '<div class="up"><div class="nm">Nothing matches</div></div>';

    list.querySelectorAll('.up button').forEach((b) => {
      b.onclick = () => {
        const el = b.closest('.up');
        const c = el.dataset.c;
        const id = el.dataset.i;
        const u = upgrades.tree()[c][id];
        const d = b.dataset.d;
        upgrades.setLevel(c, id, d === 'max' ? limitOf(u) : u.purchased + Number(d));
        drawList();
      };
    });
  }

  function renderAdv(body) {
    body.innerHTML = `
      <div class="grp">
        <h4>Progress</h4>
        <div class="row">
          <button class="b" id="v-pause">Pause</button>
          <button class="b" id="v-resume">Resume</button>
          <button class="b" id="v-save">Save</button>
        </div>
      </div>
      <div class="grp">
        <h4>Global variables (dialogue branching)</h4>
        <textarea id="v-json" spellcheck="false"></textarea>
        <div class="row" style="margin-top:5px">
          <button class="b" id="v-reload">Reload</button>
          <button class="b p" id="v-apply">Apply</button>
        </div>
      </div>
      <div class="grp">
        <h4>Fire an event</h4>
        <div class="row">
          <select id="v-ev"></select>
          <button class="b" id="v-fire">emit</button>
        </div>
      </div>
      <div class="grp">
        <label class="ck"><input type="checkbox" id="v-ach" ${state.blockAchievements ? 'checked' : ''}>
          <span>Block Steam achievements and stats</span></label>
        <div class="hint">Turn this off and cheated records go to Steam as they are.</div>
      </div>`;

    const act = () => store.gameStore().actions;
    $('#v-pause').onclick = () => act().pauseGame && act().pauseGame();
    $('#v-resume').onclick = () => act().resumeGame && act().resumeGame();
    $('#v-save').onclick = () => act().saveState && act().saveState();

    const load = () => { $('#v-json').value = JSON.stringify(store.vars().value, null, 2); };
    $('#v-reload').onclick = load;
    $('#v-apply').onclick = () => {
      try { store.vars().value = JSON.parse($('#v-json').value); } catch (e) { alert(`JSON error: ${e.message}`); }
    };
    load();

    const sel = $('#v-ev');
    try {
      const evs = store.bus().getEvents ? store.bus().getEvents() : null;
      const names = Array.isArray(evs) ? evs : Object.keys(evs || {});
      sel.innerHTML = names.map((n) => `<option>${n}</option>`).join('');
    } catch (_) { /* no list available; leave it empty */ }
    $('#v-fire').onclick = () => {
      try { store.bus().emit(sel.value); } catch (e) { console.warn('[cheat]', e); }
    };

    $('#v-ach').onchange = (e) => { state.blockAchievements = e.target.checked; };
  }

  // ── Periodic refresh (only the cheap parts) ──────────────────────
  function refresh() {
    if (!state.open || !panel) return;
    const g = store.gameStore();
    if (g) {
      const lv = g.state.currentLevel.value;
      const names = window.__bd_levelNames || {};
      $('#s-lvl').textContent = names[lv] || lv || '—';
    }
    $('#s-gold').textContent = fmt(store.getRes('gold'));
    $('#s-ts').textContent = `${speed.value}×`;
    syncSpeedUI();
    const nt = $('#sp-notice');
    if (nt) { nt.hidden = !speed.notice; nt.textContent = speed.notice; }

    const now = $('#r-now');
    if (now) {
      now.innerHTML = RESOURCES.map((r) => {
        const v = store.getRes(r.key);
        if (v === undefined) return '';
        return `<div title="${fmt(v)}"><span>${r.label}</span><b>${short(v)}</b></div>`;
      }).join('');
    }
  }

  function toggle() {
    if (!panel) build();
    state.open = !state.open;
    panel.classList.toggle('on', state.open);
    if (state.open) refresh();
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === TOGGLE_KEY) { e.preventDefault(); e.stopPropagation(); toggle(); }
  }, true);

  // A minimal control surface, so the same things can be done from the console.
  window.__bd_cheat = {
    state,
    getRes: store.getRes,
    setRes: store.setRes,
    setLevel: upgrades.setLevel,
    upgrades: upgrades.tree,
    slot: store.activeSlot,
    setSpeed: speed.setSpeed,
    restoreTick: speed.restoreTick,
    tickMs: speed.tickMs,
    healTick: speed.healTickOnBoot,
    diag: () => ({
      actors: speed.actorCount(),
      tick: speed.tickMs(),
      speed: speed.value,
      top: speed.actorHistogram(),
    }),
    guardLimits: mod('speed').LIMITS,
  };

  // The achievement handler and the game store both appear late, so this polls until
  // they do. Guarding Steam submission before the game can make any is the point.
  const boot = setInterval(() => {
    achievements.install();
    if (store.gameStore() && document.body) {
      clearInterval(boot);
      if (speed.healTickOnBoot()) {
        console.warn('[cheat] a shortened tick was left in the save; restored to 1000ms.');
      }
      setInterval(refresh, 500);
      console.log(`[cheat] ready - press ${TOGGLE_KEY}. (console: window.__bd_cheat)`);
    }
  }, 300);
})();
