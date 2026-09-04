// Reading the dungeon and finding the way through it.
//
// The dungeon is a Babylon.js scene drawn to a canvas: no DOM tiles, and the scene is
// a `const` inside a React effect that no ref holds. The bundle patch hands it over as
// `window.__bd_dungeon` (patch/bridge.js), and everything below reads that scene.
//
// What the scene gives us, by mesh name:
//
//   f<chunk>_<i><j>   floor, one under every square, walkable or not
//   w<chunk>_<i><j>d  wall, two coplanar meshes per solid square
//   chest_<i>_<j>     a chest
//   exitDoor_<i>_<j>  the way out, sitting on a wall face rather than in a square
//
// Those squares are 2 world units and come in 2x2 blocks; the maze the player actually
// moves through has cells of 4. So a cell is derived from world coordinates rather than
// from the names, which encode the finer grid.
//
// It reaches for neither the game nor the DOM directly - the scene, the clock and the
// key sender are all injected, which is what makes it testable without the game.
// (engine/dungeon.test.js)
(function (root) {
  'use strict';

  /** World units per drawn square. The maze cell is two of these. */
  const SQUARE = 2;
  const CELL = SQUARE * 2;

  /** The four ways out of a cell, as [dRow, dCol]. */
  const STEPS = [[-1, 0], [0, 1], [1, 0], [0, -1]];

  const NAME = {
    floor: /^f\d+_\d+$/,
    wall: /^w\d+_\d+$/,
    chest: /^chest_\d+_\d+$/,
    chestBox: /^chestCollision_\d+_\d+$/,
    exitBox: /^exitDoorCollision_\d+_\d+$/,
    exit: /^exitDoor_\d+_\d+$/,
  };

  /**
   * The maze as a grid, from the scene's meshes.
   *
   * Every square has a floor, so a floor says nothing about whether you can stand
   * there; a square is solid exactly when it also carries a wall. Returns null when
   * there is no live scene - it is disposed on the way out of every dungeon, and a
   * disposed one still answers, with no meshes in it.
   */
  function readMaze(scene) {
    if (!scene || !scene.meshes || !scene.meshes.length || !scene.activeCamera) return null;

    const floors = [];
    const laid = new Set();
    const solid = new Set();
    const chests = [];
    const shut = new Map();
    let exit = null;
    let exitShut = true;

    for (const m of scene.meshes) {
      const n = m.name || '';
      const x = round(m.position.x);
      const z = round(m.position.z);
      if (NAME.floor.test(n)) { floors.push([x, z]); laid.add(`${x},${z}`); }
      else if (NAME.wall.test(n)) solid.add(`${x},${z}`);
      else if (NAME.chest.test(n)) chests.push([x, z]);
      // A chest's collision box stops you entering its square, and the game turns that
      // off the moment it is opened - so it is both the obstacle and the "already had
      // this one" flag, with nothing of ours to keep in step with the level.
      else if (NAME.chestBox.test(n)) shut.set(`${x},${z}`, m.checkCollisions !== false);
      else if (NAME.exit.test(n)) exit = { at: [x, z], mesh: m };
      else if (NAME.exitBox.test(n)) exitShut = m.checkCollisions !== false;
    }
    if (!floors.length) return null;

    // The origin is the centre of the first *cell*, which is half a square in from the
    // first floor square - the finer grid is offset from the one being walked.
    const x0 = Math.min(...floors.map((p) => p[0])) + SQUARE / 2;
    const z0 = Math.min(...floors.map((p) => p[1])) + SQUARE / 2;
    // The outermost floor is the *far* square of the last cell, half a cell past its
    // centre - so it is stepped back before counting, or the grid comes out a row and a
    // column too large. The empty edge that made looked open until a cell with no floor
    // was also called blocked, which hid this rather than fixing it.
    const xMax = Math.max(...floors.map((p) => p[0])) - SQUARE / 2;
    const zMax = Math.max(...floors.map((p) => p[1])) - SQUARE / 2;
    const cols = Math.round((xMax - x0) / CELL) + 1;
    const rows = Math.round((zMax - z0) / CELL) + 1;

    const cellOf = (x, z) => [(z - z0) / CELL, (x - x0) / CELL];
    const worldOf = (r, c) => [x0 + c * CELL, z0 + r * CELL];

    // A cell is blocked when any of its four squares is - a maze wall fills the cell,
    // so in practice they agree, and taking any square as enough is what keeps a
    // half-drawn cell from being walked into.
    //
    // A cell with no floor under it at all is blocked too, and that is not the same
    // check. The grid is sized from the outermost floor, so its far edge can include
    // squares the level never laid; without this they read as open, A* routes straight
    // through the outside of the maze, and the walk ends in a wall.
    const blocked = [];
    for (let r = 0; r < rows; r += 1) {
      const row = [];
      for (let c = 0; c < cols; c += 1) {
        const [x, z] = worldOf(r, c);
        let wall = false;
        let floor = false;
        for (const dx of [-SQUARE / 2, SQUARE / 2]) {
          for (const dz of [-SQUARE / 2, SQUARE / 2]) {
            const at = `${round(x + dx)},${round(z + dz)}`;
            if (solid.has(at)) wall = true;
            if (laid.has(at)) floor = true;
          }
        }
        row.push(wall || !floor);
      }
      blocked.push(row);
    }

    const chestList = chests.map(([x, z]) => ({
      cell: cellOf(x, z).map(Math.round),
      world: [x, z],
      shut: shut.get(`${x},${z}`) !== false,
    }));
    // A shut chest fills its cell: you stand next to one and open it, you do not walk
    // over it. Pathing to the chest's own square is what made the driver report the
    // cell walled and then refuse to plan through it at all.
    for (const ch of chestList) {
      if (ch.shut && blocked[ch.cell[0]]) blocked[ch.cell[0]][ch.cell[1]] = true;
    }

    // The way out wants the golden key, and that is in a chest - so leaving early is
    // not a trade of loot against time, it is not leaving at all.
    //
    // Unlike a chest, the door is not a square. It hangs on the outer wall, past the
    // last row, so it rounds onto the very square you stand on to use it. Treating it
    // as a chest - block that square, stand beside it - had the player pacing back and
    // forth in front of the door forever, because "beside the door" and "where I am"
    // were the same place. It is reached by distance and by looking at it, which is
    // also the game's own rule for opening it.
    const door = exit ? (() => {
      const raw = cellOf(exit.at[0], exit.at[1]).map(Math.round);
      // Hanging past the last row, its square can round clean outside the grid - and
      // then there is no path to it and the driver simply stops, chests all opened and
      // the way out three steps away. The square to stand on is the nearest open one.
      let cell = raw;
      if (!(raw[0] >= 0 && raw[1] >= 0 && raw[0] < rows && raw[1] < cols
        && !blocked[raw[0]][raw[1]])) {
        let bestD = Infinity;
        for (let r = 0; r < rows; r += 1) {
          for (let c = 0; c < cols; c += 1) {
            if (blocked[r][c]) continue;
            const [wx, wz] = worldOf(r, c);
            const d = (wx - exit.at[0]) ** 2 + (wz - exit.at[1]) ** 2;
            if (d < bestD) { bestD = d; cell = [r, c]; }
          }
        }
      }
      return { cell, world: exit.at, shut: exitShut, isExit: true };
    })() : null;

    const cam = scene.activeCamera;
    const player = cellOf(cam.position.x, cam.position.z).map(Math.round);

    return {
      rows,
      cols,
      blocked,
      cellOf,
      worldOf,
      player,
      facing: cam.rotation ? cam.rotation.y : 0,
      at: [round(cam.position.x), round(cam.position.z)],
      chests: chestList,
      exit: door,
      open: (r, c) => r >= 0 && c >= 0 && r < rows && c < cols && !blocked[r][c],
    };
  }

  function round(n) { return Math.round(n * 1000) / 1000; }

  /**
   * A* over the maze, returning the cells to walk through including the goal.
   *
   * A* rather than a plain breadth-first search because the torch is the real budget:
   * every square walked is torch spent, and the point is to reach the chests and the
   * way out on the shortest path there is, not merely to arrive. On a 4-connected grid
   * the Manhattan distance never overestimates, so the first path found is the shortest.
   *
   * `null` when the goal cannot be reached - a chest can be walled off behind a door
   * we have no key for, and walking at a wall until the torch dies is not an answer.
   */
  function findPath(maze, from, to) {
    const key = (r, c) => r * maze.cols + c;
    const goal = key(to[0], to[1]);
    const start = key(from[0], from[1]);
    if (!maze.open(to[0], to[1])) return null;
    if (start === goal) return [];

    const h = (r, c) => Math.abs(r - to[0]) + Math.abs(c - to[1]);
    const g = new Map([[start, 0]]);
    const cameFrom = new Map();
    // A binary heap would be faster, but these mazes are tens of cells across; the
    // clarity is worth more than the constant factor.
    const frontier = [[h(from[0], from[1]), start, from[0], from[1]]];

    while (frontier.length) {
      let best = 0;
      for (let i = 1; i < frontier.length; i += 1) {
        if (frontier[i][0] < frontier[best][0]) best = i;
      }
      const [, id, r, c] = frontier.splice(best, 1)[0];
      if (id === goal) {
        const path = [];
        let cur = id;
        while (cur !== start) {
          path.push([Math.floor(cur / maze.cols), cur % maze.cols]);
          cur = cameFrom.get(cur);
        }
        return path.reverse();
      }
      for (const [dr, dc] of STEPS) {
        const nr = r + dr;
        const nc = c + dc;
        if (!maze.open(nr, nc)) continue;
        const nid = key(nr, nc);
        const cost = g.get(id) + 1;
        if (g.has(nid) && g.get(nid) <= cost) continue;
        g.set(nid, cost);
        cameFrom.set(nid, id);
        frontier.push([cost + h(nr, nc), nid, nr, nc]);
      }
    }
    return null;
  }

  /**
   * Where to go next: the nearest chest we have not opened, then the way out.
   *
   * Every chest, not the nearest few. The way out is a locked door behind where you
   * start, and the golden key that opens it is in one of the chests - so leaving early
   * is not a trade of loot against time, it is not leaving at all. The loot bar the
   * game draws carries `hasGoldenKey` for exactly this.
   *
   * Chests are taken nearest-first rather than in the order they were found, and each
   * one is re-planned from where we actually are - which is what makes the route
   * through several of them short rather than a series of straight lines to each.
   */
  function nextGoal(maze) {
    let best = null;
    for (const ch of maze.chests) {
      if (!ch.shut) continue;
      // Stand beside it, not on it. Any of the four neighbours will do; the nearest one
      // is the one worth walking to.
      for (const [dr, dc] of STEPS) {
        const stand = [ch.cell[0] + dr, ch.cell[1] + dc];
        if (!maze.open(stand[0], stand[1])) continue;
        const path = findPath(maze, maze.player, stand);
        if (!path) continue;
        if (!best || path.length < best.path.length) {
          best = { kind: 'chest', cell: stand, target: ch, path };
        }
      }
    }
    if (best) return best;

    // Every chest taken; now the door - walked *to*, not stood beside.
    const door = maze.exit;
    if (!door) return null;
    const path = findPath(maze, maze.player, door.cell);
    if (!path) return null;
    return { kind: door.shut ? 'exit' : 'leave', cell: door.cell, target: door, path };
  }

  /**
   * Is the chest close enough and square enough on to open?
   *
   * The game's own rule, read off its click handler: within five world units, and
   * within sixty degrees of where the camera looks (`dot(forward, toChest) > 0.5`).
   * A cell is four units, so standing in the next cell along is inside the range with
   * nothing to spare - which is why facing has to be right rather than roughly right.
   */
  function canOpen(maze, chest) {
    const dx = chest.world[0] - maze.at[0];
    const dz = chest.world[1] - maze.at[1];
    const d2 = dx * dx + dz * dz;
    if (d2 > OPEN_RANGE * OPEN_RANGE) return false;
    if (d2 < 1e-6) return true;
    const len = Math.sqrt(d2);
    // The camera looks along (sin ry, cos ry), the same convention keyFor uses.
    const fx = Math.sin(maze.facing);
    const fz = Math.cos(maze.facing);
    return (fx * dx + fz * dz) / len > OPEN_DOT;
  }

  /** How far and how square-on the game lets you open a chest. */
  const OPEN_RANGE = 5;
  const OPEN_DOT = 0.5;

  /**
   * Which key to tap to get from where we are towards a neighbouring cell.
   *
   * The controls are a dungeon crawler's, not a shooter's: W and S walk forward and
   * back along the way the camera looks, and A and D *turn* rather than strafe. This
   * was measured, and the first version had it wrong - it treated all four as compass
   * directions, sent S to go north, and the player stood still while the torch burned.
   *
   * Turning costs a settle the torch is paying for, so a cell behind us is walked to
   * backwards rather than turned towards: S covers it in one action where a turn would
   * take two.
   *
   *   returns { key, kind }  kind is 'move' when it closes distance, 'turn' when it
   *                          only changes where we look.
   */
  function keyFor(facing, dRow, dCol) {
    // The camera looks along `(sin ry, cos ry)` in (x, z), and a step of
    // (dRow, dCol) is (dCol, dRow) in those same axes - so the heading that walks it
    // is atan2(dCol, dRow). Negating dRow here, as if 0 were north, mirrors the frame:
    // east and west still came out right, which is exactly why it took a live walk to
    // notice that north and south were swapped.
    const want = Math.atan2(dCol, dRow);
    const rel = norm(want - facing);
    const quarter = ((Math.round(rel / (Math.PI / 2)) % 4) + 4) % 4;
    // A lowers the rotation and D raises it, both by a quarter turn; measured, because
    // which of them reads as "left" depends on a sign convention that is not ours.
    return [
      { key: 'KeyW', kind: 'move' },
      { key: 'KeyD', kind: 'turn' },
      { key: 'KeyS', kind: 'move' },
      { key: 'KeyA', kind: 'turn' },
    ][quarter];
  }

  function norm(a) {
    let x = a;
    while (x <= -Math.PI) x += Math.PI * 2;
    while (x > Math.PI) x -= Math.PI * 2;
    return x;
  }

  /** A tap settles in about this long: one cell walked, or one quarter turned. */
  const SETTLE_MS = 700;

  /** Give up on a level after this many actions rather than burn the torch in a loop. */
  const ACTION_BUDGET = 400;

  /**
   * Drives the dungeon, one action per call.
   *
   * The controls turned out to be discrete, which is what makes this a state machine
   * rather than a control loop: a *tap* of W or S walks exactly one cell, and a tap of
   * A or D turns exactly a quarter, both settling in about 600ms. Holding a key is not
   * a longer version of the same thing - it starts a free spin that ends wherever the
   * animation happens to be, which is what the first attempt did.
   *
   * A tap that moves nothing is a wall. That is the only collision signal there is, and
   * it is worth having: the grid is read from meshes and can be wrong at the edges.
   *
   * @param deps
   *   scene   () => the live Babylon scene, or null
   *   tap     (code) => void, pressing and releasing that key
   *   click   ([x, z]) => void, a pointer press on that world position
   *   now     () => ms
   *   log     (tag, text, level?) => void
   *
   * `tap` rather than a raw event sender because the press has to last: a keydown and
   * a keyup in the same turn of the event loop is not a keypress as far as the game is
   * concerned, and the first driver sent exactly that - every move reported no movement
   * and the maze filled up with walls that were not there. How long to hold it is the
   * caller's business, not this file's, which is also what keeps the timer out of here.
   */
  function create(deps) {
    const { scene, log } = deps;
    const tap = deps.tap;
    // Opening a chest is a click on it, not a key: the game picks whatever mesh is
    // under the pointer and opens the one it finds. Which point on the canvas that is
    // needs the engine's own picking, so it belongs to the caller - and it is not the
    // middle of the view. The camera sits above the chest and looks level, so the
    // chest lands below centre and a click at the middle sails over it.
    const click = deps.click || (() => {});
    const now = deps.now || Date.now;
    const settleMs = deps.settleMs || SETTLE_MS;

    let busyUntil = 0;
    let pending = null;        // { key, from: [x, z], cell: [r, c] }
    // Cells a tap proved solid. The maze is rebuilt from the scene on every step, so
    // marking one on that object lasts exactly one tick and the driver walks into the
    // same wall for as long as the torch holds out.
    let walled = new Set();
    let actions = 0;
    let lastScene = null;

    /**
     * Everything about the level resets when the scene does.
     *
     * The scene object itself is the identity. Reading `window.__bd_dungeon` here
     * instead would have been the one place this file reached out of its own
     * dependencies - and it broke the tests the moment they ran without a browser,
     * which is exactly what that rule is for.
     */
    function freshen(sc) {
      if (lastScene === sc) return;
      lastScene = sc;
      walled = new Set();
      actions = 0;
      pending = null;
      busyUntil = 0;
    }

    /**
     * One action, or nothing while the last one is still settling.
     * Returns false when there is no dungeon to drive.
     */
    function step() {
      const sc = scene();
      const maze = readMaze(sc);
      if (!maze) { pending = null; return false; }
      freshen(sc);
      for (const at of walled) {
        const [r, c] = at.split(',').map(Number);
        if (maze.blocked[r]) maze.blocked[r][c] = true;
      }

      const t = now();
      if (t < busyUntil) return true;

      // Did the action that just settled do what it was for?
      if (pending) {
        const done = pending;
        pending = null;
        if (done.kind === 'move') {
          const moved = done.from[0] !== maze.at[0] || done.from[1] !== maze.at[1];
          if (!moved) {
            // A wall the grid did not know about. Remembered, not merely marked on this
            // tick's maze, so the next plan routes around it.
            const at = `${done.cell[0]},${done.cell[1]}`;
            if (!walled.has(at)) {
              walled.add(at);
              log('DGN', `(${at}) is walled after all`, 'warn');
            }
            if (maze.blocked[done.cell[0]]) maze.blocked[done.cell[0]][done.cell[1]] = true;
            return true;
          }
        }
      }

      if (actions >= ACTION_BUDGET) return true;

      const goal = nextGoal(maze);
      if (!goal) return true;

      // Standing beside the chest already: face it, then open it. Walking onto it is
      // not a thing that can happen - its collision box fills the square - so arriving
      // is never what opens one, and the first driver walked the whole route and came
      // back with nothing.
      if ((goal.kind === 'chest' || goal.kind === 'exit') && !goal.path.length) {
        const ch = goal.target;
        if (canOpen(maze, ch)) {
          // Nothing is recorded as opened here. The chest itself says so - the game
          // swaps its material and drops its collisions - and an earlier version that
          // ticked the box on its own account walked the whole level reporting chests
          // it had never opened.
          click(ch);
          actions += 1;
          busyUntil = t + settleMs;
          return true;
        }
        // Not square enough on yet. Turn towards it a quarter at a time.
        //
        // From the world offset, not the difference of cells: the door rounds onto the
        // square you use it from, so that difference is (0,0) and there is nothing to
        // turn towards. `keyFor` reads (dRow, dCol) as (z, x), which is what these are.
        const act = keyFor(maze.facing, ch.world[1] - maze.at[1], ch.world[0] - maze.at[0]);
        pending = { kind: 'turn', key: act.key, from: maze.at.slice(), cell: ch.cell };
        tap(act.key);
        actions += 1;
        busyUntil = t + settleMs;
        return true;
      }

      if (!goal.path.length) return true;
      const next = goal.path[0];
      const act = keyFor(maze.facing, next[0] - maze.player[0], next[1] - maze.player[1]);
      pending = { kind: act.kind, key: act.key, from: maze.at.slice(), cell: next };
      tap(act.key);
      actions += 1;
      busyUntil = t + settleMs;
      return true;
    }

    return {
      step,
      /** For the panel and the tests: what it thinks it is doing. */
      report: () => ({ actions, walled: [...walled], pending }),
    };
  }

  const api = { create, readMaze, findPath, nextGoal, keyFor, canOpen,
    SQUARE, CELL, STEPS, SETTLE_MS, OPEN_RANGE, OPEN_DOT };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too, and the usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).dungeon = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).dungeon = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));
