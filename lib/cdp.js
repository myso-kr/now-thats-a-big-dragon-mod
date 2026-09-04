'use strict';

// A minimal CDP client on Node 22+'s built-in WebSocket and fetch. No dependencies.

class CDP {
  /** How long any one request may go unanswered before it is treated as a stall. */
  static TIMEOUT_MS = 15000;

  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this._id = 0;
    this._pending = new Map();
    this._handlers = new Map();
    this.closed = false;
    /**
     * Called once when the connection goes away.
     *
     * The game exiting closes this socket, and that is how a run normally ends. Only
     * rejecting the in-flight requests is not enough: the launcher's own timers keep
     * the event loop alive, so without this hook it lingers as an orphan holding
     * nothing.
     */
    this.onDisconnect = null;
  }

  static async waitForEndpoint(port, timeoutMs = 30000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        const res = await fetch(`http://127.0.0.1:${port}/json/version`);
        if (res.ok) return await res.json();
      } catch (_) { /* not up yet */ }
      await new Promise((r) => setTimeout(r, 250));
    }
    throw new Error(`the CDP endpoint (:${port}) did not open within ${timeoutMs}ms.`);
  }

  static async findPageTarget(port, timeoutMs = 30000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
        const page = list.find((t) => t.type === 'page');
        if (page) return page;
      } catch (_) { /* retry */ }
      await new Promise((r) => setTimeout(r, 250));
    }
    throw new Error('no page target found.');
  }

  async connect() {
    this.ws = new WebSocket(this.wsUrl);
    await new Promise((resolve, reject) => {
      this.ws.onopen = resolve;
      this.ws.onerror = () => reject(new Error('the CDP websocket would not connect'));
    });
    this.ws.onmessage = (msg) => this._onMessage(msg);
    this.ws.onclose = () => {
      if (this.closed) return;
      this.closed = true;
      for (const { reject } of this._pending.values()) {
        reject(new Error('the CDP connection dropped.'));
      }
      this._pending.clear();
      if (typeof this.onDisconnect === 'function') this.onDisconnect();
    };
    return this;
  }

  _onMessage(msg) {
    let data;
    try { data = JSON.parse(msg.data); } catch (_) { return; }

    if (data.id !== undefined && this._pending.has(data.id)) {
      const { resolve, reject } = this._pending.get(data.id);
      this._pending.delete(data.id);
      if (data.error) reject(new Error(`${data.error.message} (${data.error.code})`));
      else resolve(data.result);
      return;
    }

    if (data.method) {
      const list = this._handlers.get(data.method);
      if (list) for (const fn of list) fn(data.params || {}, data.sessionId);
    }
  }

  on(method, fn) {
    if (!this._handlers.has(method)) this._handlers.set(method, []);
    this._handlers.get(method).push(fn);
    return this;
  }

  /**
   * A wedged renderer keeps the socket open and simply stops answering. Without a
   * deadline the promise never settles, the caller waits forever, and the launcher
   * looks healthy while doing nothing — so every request gets one.
   */
  send(method, params = {}, sessionId, timeoutMs = CDP.TIMEOUT_MS) {
    const id = ++this._id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this._pending.delete(id);
        reject(new Error(`${method} did not answer within ${timeoutMs}ms (renderer stalled?).`));
      }, timeoutMs);
      const done = (fn) => (v) => { clearTimeout(timer); fn(v); };
      this._pending.set(id, { resolve: done(resolve), reject: done(reject) });
      this.ws.send(JSON.stringify(payload));
    });
  }

  close() {
    try { this.ws && this.ws.close(); } catch (_) { /* noop */ }
  }
}

module.exports = { CDP };
