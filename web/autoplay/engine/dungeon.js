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
    let exit = null;

    for (const m of scene.meshes) {
      const n = m.name || '';
      const x = round(m.position.x);
      const z = round(m.position.z);
      if (NAME.floor.test(n)) { floors.push([x, z]); laid.add(`${x},${z}`); }
      else if (NAME.wall.test(n)) solid.add(`${x},${z}`);
      else if (NAME.chest.test(n)) chests.push([x, z]);
      else if (NAME.exit.test(n)) exit = [x, z];
    }
    if (!floors.length) return null;

    // The origin is the centre of the first *cell*, which is half a square in from the
    // first floor square - the finer grid is offset from the one being walked.
    const x0 = Math.min(...floors.map((p) => p[0])) + SQUARE / 2;
    const z0 = Math.min(...floors.map((p) => p[1])) + SQUARE / 2;
    const xMax = Math.max(...floors.map((p) => p[0]));
    const zMax = Math.max(...floors.map((p) => p[1]));
    const cols = Math.round((xMax + SQUARE / 2 - x0) / CELL) + 1;
    const rows = Math.round((zMax + SQUARE / 2 - z0) / CELL) + 1;

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
      chests: chests.map(([x, z]) => cellOf(x, z).map(Math.round)),
      // The door sits on a wall face, so its cell rounds to the square it opens from.
      exit: exit ? cellOf(exit[0], exit[1]).map(Math.round) : null,
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
  function nextGoal(maze, opened) {
    const seen = opened || new Set();
    let best = null;
    for (const cell of maze.chests) {
      if (seen.has(`${cell[0]},${cell[1]}`)) continue;
      const path = findPath(maze, maze.player, cell);
      if (!path) continue;
      if (!best || path.length < best.path.length) best = { kind: 'chest', cell, path };
    }
    if (best) return best;
    if (!maze.exit) return null;
    const path = findPath(maze, maze.player, maze.exit);
    return path ? { kind: 'exit', cell: maze.exit, path } : null;
  }

  /**
   * Which key to hold to get from where we are towards a neighbouring cell.
   *
   * The controls are a dungeon crawler's, not a shooter's: W and S walk forward and
   * back along the way the camera looks, and A and D *turn* rather than strafe. This
   * was measured, and the first version had it wrong - it treated all four as compass
   * directions, sent S to go north, and the player stood still while the torch burned.
   *
   * Turning costs time the torch is paying for, so a cell behind us is walked to
   * backwards rather than turned towards: S covers it in one move where a turn would
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

  const api = { readMaze, findPath, nextGoal, keyFor, SQUARE, CELL, STEPS };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too, and the usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).dungeon = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).dungeon = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));
