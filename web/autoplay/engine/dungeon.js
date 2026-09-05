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
    // `enemy_<kind>_<when>` is the sprite, and only the sprite counts as a hit; the
    // box beside it (`enemy_collision_...`) is what blocks the way, and a click that
    // lands on it does nothing at all.
    enemy: /^enemy_(?!collision_|debug_|mat_)/,
    enemyBox: /^enemy_collision_/,
    exit: /^exitDoor_\d+_\d+$/,
    // A locked door inside the maze, which is a different thing from the way out. It
    // is a ground tile plus a collision box, opened by a click from beside it, and it
    // costs a grey key. It was in none of these patterns, so it read as bare floor:
    // the driver planned straight through it, walked into it, saw nothing move and
    // wrote the cell down as a wall - permanently, for the rest of the run. Anything
    // behind it, chests included, was then unreachable and quietly left there.
    door: /^door_\d+_\d+$/,
    doorBox: /^doorCollision_\d+_\d+$/,
    // The people standing about down there. Mookie says it himself in his own dialogue
    // - "I'm not allowed off this tile" - and the rescue characters do not move either.
    // They are not monsters and there is nothing to be done about them; they are simply
    // where you cannot walk. Not knowing that, the driver planned straight through one,
    // bumped, and wrote the square off as a wall it had discovered - and a floor loses
    // its shape fast when the driver is inventing walls in the middle of it.
    npcBox: /^characterCollision_/,
    // The sprite, which is what a click has to land on. `character_mat_...` is its
    // material and picks up nothing.
    npc: /^character_(?!mat_)/,
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
    const doors = [];
    const folk = [];
    const sprites = [];
    const foes = [];
    const foeBoxes = [];
    const shut = new Map();
    const doorShut = new Map();
    let exit = null;
    let exitShut = true;

    for (const m of scene.meshes) {
      const n = m.name || '';
      const x = round(m.position.x);
      const z = round(m.position.z);
      if (NAME.floor.test(n)) { floors.push([x, z]); laid.add(`${x},${z}`); }
      else if (NAME.wall.test(n)) solid.add(`${x},${z}`);
      else if (NAME.enemy.test(n)) foes.push({ world: [x, z], mesh: m });
      else if (NAME.enemyBox.test(n)) foeBoxes.push([x, z]);
      else if (NAME.chest.test(n)) chests.push([x, z]);
      // A chest's collision box stops you entering its square, and the game turns that
      // off the moment it is opened - so it is both the obstacle and the "already had
      // this one" flag, with nothing of ours to keep in step with the level.
      else if (NAME.chestBox.test(n)) shut.set(`${x},${z}`, m.checkCollisions !== false);
      else if (NAME.exit.test(n)) exit = { at: [x, z], mesh: m };
      else if (NAME.exitBox.test(n)) exitShut = m.checkCollisions !== false;
      // Same shape as a chest, and the same "already done" signal: the game turns the
      // box's collisions off the moment the door opens.
      else if (NAME.npcBox.test(n)) folk.push([x, z]);
      else if (NAME.npc.test(n)) sprites.push([x, z]);
      else if (NAME.door.test(n)) doors.push([x, z]);
      else if (NAME.doorBox.test(n)) doorShut.set(`${x},${z}`, m.checkCollisions !== false);
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

    // The golden key is not a lottery. The game's reward generator hands it out on
    // `chestIndex === 0` and rolls for everything after, so it is always in the first
    // chest built - and Babylon keeps `scene.meshes` in creation order, so that is the
    // first chest we see. It matters because it is the only chest the run cannot do
    // without: no golden key, no way out, and a crawl that ends as a failure however
    // much gold the others held.
    const chestList = chests.map(([x, z], i) => ({
      cell: cellOf(x, z).map(Math.round),
      world: [x, z],
      shut: shut.get(`${x},${z}`) !== false,
      golden: i === 0,
    }));
    // A shut chest fills its cell: you stand next to one and open it, you do not walk
    // over it. Pathing to the chest's own square is what made the driver report the
    // cell walled and then refuse to plan through it at all.
    for (const ch of chestList) {
      if (ch.shut && blocked[ch.cell[0]]) blocked[ch.cell[0]][ch.cell[1]] = true;
    }

    // A shut door blocks its cell exactly as a chest does. Unlike a chest it is not
    // loot but road: it is worth a grey key only when something we still want is behind
    // it, which is what nextGoal decides. An open one is plain floor and stays walkable.
    const doorList = doors.map(([x, z]) => ({
      cell: cellOf(x, z).map(Math.round),
      world: [x, z],
      shut: doorShut.get(`${x},${z}`) !== false,
      isDoor: true,
    }));
    for (const d of doorList) {
      if (d.shut && blocked[d.cell[0]]) blocked[d.cell[0]][d.cell[1]] = true;
    }
    // Their boxes sit at the centre of a cell, where `solid` - which is keyed by the
    // finer square grid - would never find them. Blocked by cell, as chests are.
    //
    // And they are worth going to. The game's table gives mookie on level 4, the worker
    // on 8 and 10, and each hands over a torch - which on a floor with a burning clock
    // is not a nicety, it is more floor. Talking to one is a chest by another name:
    // stand beside it, face it, click it, `isPlayerFacing(5)`, once only.
    const blockedFolk = new Set();
    for (const [x, z] of folk) {
      const [r, c] = cellOf(x, z).map(Math.round);
      if (blocked[r]) blocked[r][c] = true;
      blockedFolk.add(`${r},${c}`);
    }
    // Only the ones standing in the maze. The rescue characters wait outside its walls,
    // have no collision box, and are not there to be talked to.
    const npcList = sprites
      .map(([x, z]) => ({ cell: cellOf(x, z).map(Math.round), world: [x, z], isNpc: true }))
      .filter((n) => blockedFolk.has(`${n.cell[0]},${n.cell[1]}`));

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
    // Its square is *not* blocked while it is shut, however much that looks like the
    // chest rule. The door hangs on the outer wall, past the last row, and its collision
    // box is in the wall - the cell it rounds onto is the square you stand on to use it,
    // not a square of its own. Blocking that is what had the player pacing in front of
    // the door forever, with "beside the door" and "where I am" the same place.

    // A monster in a corridor is a wall you can remove. Its box is what stops you, so
    // the box is what blocks the cell - and the sprite, which is what has to be
    // clicked, is a separate mesh sitting on the same square.
    const enemies = foes.map((f) => ({
      cell: cellOf(f.world[0], f.world[1]).map(Math.round),
      world: f.world,
      // The game hides the sprite until the fight starts, and only then will a click
      // register: `inBattle` gates the whole handler.
      inBattle: f.mesh.isVisible !== false,
      isEnemy: true,
    }));
    for (const [x, z] of foeBoxes) {
      const [r, c] = cellOf(x, z).map(Math.round);
      if (blocked[r]) blocked[r][c] = true;
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
      chests: chestList,
      doors: doorList,
      npcs: npcList,
      enemies,
      exit: door,
      open: (r, c) => r >= 0 && c >= 0 && r < rows && c < cols && !blocked[r][c],
    };
  }

  function round(n) { return Math.round(n * 1000) / 1000; }

  // Every decision of a run, kept so a run that went wrong can be read back rather than
  // reconstructed from the four warnings it happened to log. The autoplay log holds
  // sixty entries for the whole engine and a dungeon shares it with every purchase, so
  // by the time anyone looks the run is gone. This is the dungeon's own, and it is
  // cleared when a run starts.
  const MAX_TRACE = 600;
  let TRACE = [];

  function note(entry) {
    TRACE.push(entry);
    if (TRACE.length > MAX_TRACE) TRACE.shift();
  }

  // The trace of the run that just finished, kept after the live one is cleared - the
  // scene object lingers a moment after a run ends, so the next freshen wipes the very
  // trace anyone would want to read.
  let LAST_TRACE = [];

  /**
   * The run being driven now, and the one before it.
   *
   * Both, because by the time anyone asks, the next run has usually started: autoplay
   * buys another key and steps straight back in, `freshen` clears the live trace, and
   * an accessor that answered "the current one, or the last one if the current is
   * empty" answered with the empty new one every single time.
   */
  function trace() { return { now: TRACE.slice(), last: LAST_TRACE.slice() }; }
  function clearTrace() { if (TRACE.length) LAST_TRACE = TRACE; TRACE = []; }

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
  function findPath(maze, from, to, avoid) {
    const key = (r, c) => r * maze.cols + c;
    const goal = key(to[0], to[1]);
    const start = key(from[0], from[1]);
    if (!maze.open(to[0], to[1])) return null;
    if (start === goal) return [];
    const off = avoid || null;

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
        if (off && off.has(`${nr},${nc}`) && key(nr, nc) !== goal) continue;
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
   * What to do next on this floor.
   *
   * One rule, over one graph, replacing the pile of tiers this grew into. The floor is
   * cells. Some cells hold a thing that blocks the way *and can be removed*:
   *
   *   a shut chest    opened by a click from beside it - and it is also the loot
   *   a locked door   opened by a click from beside it, at the cost of a grey key
   *   a monster       killed by clicking it, once it has woken and engaged
   *
   * None of them is a wall, so none of them may be planned around as if it were. The
   * plan is made on the graph where all of them are already gone, because all of them
   * can be; then it is walked on the real one, and wherever the real one blocks the
   * way, the first thing standing in it becomes the job instead. That is the whole
   * algorithm, and everything the driver used to get wrong was a special case of
   * getting this one thing wrong:
   *
   *   - a sleeping monster was skipped, because it cannot be clicked until it engages.
   *     `inBattle` gates the game's whole handler. So it was left as a wall, and a
   *     corridor with a spider asleep in it cut the floor in half: one chest opened,
   *     three unreachable, home early. Walking up to it is the move - the game engages
   *     on proximity, and then it is a fight like any other.
   *   - a locked door was not read at all, so it was floor that would not be walked
   *     through, and the driver wrote the cell down as a wall for the rest of the run.
   *   - a chest behind either of those was "unreachable", and unreachable chests were
   *     silently dropped, which is what "opened one of three and left" was.
   *
   * The way out is not an obstacle: it is a tile that ends the floor when you stand on
   * it, and only once it is open. So it is never a stop on the route and never a square
   * to cross - it is where the route ends.
   */
  function nextGoal(maze, abandoned, keys) {
    const skip = abandoned || new Set();
    // A door costs a grey key, and with none in hand it will not open however long we
    // stand in front of it - the game's own handler returns false and emits DOOR_LOCKED.
    // So with none it is a wall, and whatever is behind it waits until a chest gives one
    // up. Unknown counts as plenty: the reader is the HUD, and a missing HUD should not
    // stop the driver opening doors it could have opened.
    // "No key in hand" is not the same as "will not open". The game's own handler
    // spends a grey key if there is one and *otherwise* falls through to a second
    // resource, failing only if that is empty too. So the count orders our preference -
    // do everything on this side first, because the chests here hand out the keys - but
    // it never forbids the door. When there is nothing else left, the door is tried
    // anyway: eight clicks is a cheap thing to be wrong about, and abandoning the run is
    // not. A floor whose every way on was a door came back "0 of 4 chests" for exactly
    // this reason.
    const noKeys = !!keys && keys.grey === 0;
    const at = (cell) => `${cell[0]},${cell[1]}`;
    const foeKey = (f) => `foe:${at(f.cell)}`;

    // A fight already on us comes before any plan. Its box fills the corridor, so
    // until it is down there may be no route to weigh at all.
    for (const foe of maze.enemies || []) {
      if (foe.inBattle && !skip.has(foeKey(foe))) {
        return { kind: 'fight', cell: maze.player, target: foe, path: [] };
      }
    }

    // Two kinds of thing stand in the way, and they are not the same kind.
    //
    // A chest and a monster cost nothing but the walk: the chest is the loot we came
    // for, and the monster wakes when we get near and dies to the same clicks. Both are
    // simply cleared on the way past, so the floor is planned as though they were
    // already gone.
    //
    // A door costs a grey key, and grey keys come out of chests. So a door is not part
    // of the plan at all until the part of the floor we can already stand in has been
    // emptied - every chest in it opened, every monster in it killed. Do that and the
    // keys arrive on their own; spend one early and it is spent on reaching a chest we
    // were going to reach anyway, from the other side.
    const obstacles = new Map();
    for (const ch of maze.chests) {
      if (ch.shut && !skip.has(at(ch.cell))) obstacles.set(at(ch.cell), { kind: 'chest', thing: ch });
    }
    for (const f of maze.enemies || []) {
      if (!skip.has(foeKey(f))) obstacles.set(at(f.cell), { kind: 'engage', thing: f });
    }
    // A person does not move for anyone - mookie says so himself - so they are not an
    // obstacle that can be cleared, only one to be talked to and then walked around.


    // The floor as it would be with all of those gone - which is to say, this side of
    // the doors. Planning here and walking on the real one is the whole trick: it never
    // plans around something it could simply move.
    const ideal = Object.assign({}, maze, {
      open: (r, c) => maze.open(r, c)
        || (r >= 0 && c >= 0 && r < maze.rows && c < maze.cols && obstacles.has(`${r},${c}`)),
    });

    // The way out fires on entry once open, so routes keep off it while there is still
    // anything to do. Shut, it is inert and going round it would only spend torch.
    const exit = maze.exit;
    const keepOff = exit && !exit.shut ? new Set([at(exit.cell)]) : null;

    /** Somewhere to stand beside `thing` in `world`, and the way to it. */
    const beside = (world, thing, avoid) => {
      let best = null;
      for (const [dr, dc] of STEPS) {
        const stand = [thing.cell[0] + dr, thing.cell[1] + dc];
        if (!world.open(stand[0], stand[1])) continue;
        if (avoid && avoid.has(at(stand))) continue;
        const path = findPath(world, world.player, stand, avoid);
        if (path && (!best || path.length < best.path.length)) best = { cell: stand, path };
      }
      return best;
    };

    /**
     * Get to `thing`, or to whatever is standing between us and it.
     *
     * Tries the real floor first. If that has no way, it asks the ideal one, takes the
     * first obstacle on that route, and goes and deals with *that* instead - which may
     * in turn be behind another. `seen` stops a ring of obstacles from looping.
     */
    const work = (kind, thing, seen) => {
      if (seen.has(at(thing.cell))) return null;
      seen.add(at(thing.cell));

      for (const avoid of [keepOff, null]) {
        const got = beside(maze, thing, avoid);
        if (got) return { kind, cell: got.cell, target: thing, path: got.path };
      }
      for (const avoid of [keepOff, null]) {
        const dream = beside(ideal, thing, avoid);
        if (!dream) continue;
        for (const cell of dream.path) {
          const blocker = obstacles.get(at(cell));
          if (!blocker || at(cell) === at(thing.cell)) continue;
          const step = work(blocker.kind, blocker.thing, seen);
          if (step) return step;
        }
      }
      return null;
    };

    // Someone to talk to comes before the loot. What they hand over is a torch, and a
    // torch is time - the one thing the floor is actually short of - so it is worth
    // most at the start and least at the end.
    for (const who of maze.npcs || []) {
      if (skip.has(at(who.cell))) continue;
      const step = work('talk', who, new Set());
      if (step) return step;
    }

    // Every chest still shut, in the order that costs least on the ideal floor - where
    // they are all reachable, so the order is over all of them rather than over the few
    // that happen to be in front of us. The golden key leads: the game puts it in the
    // first chest it builds, and a run that ends without it is a run that failed.
    const stops = order(ideal, maze.chests.filter((ch) => ch.shut && !skip.has(at(ch.cell))), exit);
    for (const ch of stops) {
      const step = work('chest', ch, new Set());
      if (step) return step;
    }

    // This side of the doors is empty, so now a door is worth a key. Which one is the
    // same question as for a chest: plan as though every door were open, and the first
    // door on the way to something we still want is the one to spend on.
    //
    // Asking it one door at a time - "would opening *this* one reach a chest" - is what
    // it did first, and it is wrong whenever doors come in sequence. A floor whose start
    // opened onto a door, and that door onto another, answered "nothing behind either"
    // for both and the run went home with six chests unopened.
    const shutDoors = (maze.doors || []).filter((d) => d.shut && !skip.has(at(d.cell)));
    if (shutDoors.length) {
      const behind = new Map(shutDoors.map((d) => [at(d.cell), d]));
      const withDoors = Object.assign({}, maze, {
        open: (r, c) => ideal.open(r, c) || behind.has(`${r},${c}`),
      });
      const wanted = maze.chests.filter((ch) => ch.shut && !skip.has(at(ch.cell)));
      const targets = wanted.length ? wanted : (exit && !skip.has('exit') ? [exit] : []);
      for (const thing of order(withDoors, wanted, exit).concat(targets)) {
        const dream = beside(withDoors, thing, null);
        if (!dream) continue;
        const first = dream.path.map((cell) => behind.get(at(cell))).find(Boolean);
        if (!first) continue;
        const step = work('door', first, new Set());
        if (step) return step;
      }
    }

    // The way out only opens to the golden key, and the game puts that in the first
    // chest it builds - so with every chest on the floor still shut we cannot have it,
    // and walking over to try is eight actions spent proving what we already know.
    //
    // This is not a rare corner. The game's own door placement picks corridor squares
    // at random and checks nothing: in a perfect maze every corridor square is a bridge,
    // so a door dropped beside the entrance seals the floor, and the grey keys that
    // would open it are in the chests behind it. Those floors cannot be finished by
    // anybody. Recognising one and leaving is the whole of what can be done about it.
    // Not "no chest opened" - "the chest with the key in it is still shut". A floor can
    // give up an ordinary chest and still be sealed away from the golden one, and that
    // run spent twenty-seven actions finding out what the flag already said.
    const golden = maze.chests.find((ch) => ch.golden);
    if (exit && exit.shut && golden && golden.shut) return null;

    // Nothing left to open. The way out is walked *to*, not stood beside, and standing
    // on it is what uses it.
    if (!exit || skip.has('exit')) return null;
    const out = findPath(maze, maze.player, exit.cell);
    if (out) return { kind: exit.shut ? 'exit' : 'leave', cell: exit.cell, target: exit, path: out };
    // Even the way out can be behind a door or a monster.
    const withDoors = Object.assign({}, maze, {
      open: (r, c) => ideal.open(r, c)
        || (maze.doors || []).some((d) => d.shut && d.cell[0] === r && d.cell[1] === c),
    });
    const dream = findPath(withDoors, withDoors.player, exit.cell);
    if (dream) {
      for (const cell of dream) {
        const blocker = obstacles.get(at(cell));
        if (!blocker) continue;
        const step = work(blocker.kind, blocker.thing, new Set());
        if (step) return step;
      }
    }
    return null;
  }

  /**
   * Every square we could stand on to work a thing, cheapest first from `from`.
   * Returns null when there is no way to any of them.
   */
  function reach(maze, from, thing, avoid) {
    let best = null;
    for (const [dr, dc] of STEPS) {
      const stand = [thing.cell[0] + dr, thing.cell[1] + dc];
      if (!maze.open(stand[0], stand[1])) continue;
      if (avoid && avoid.has(`${stand[0]},${stand[1]}`)) continue;
      const path = findPath(maze, from, stand, avoid);
      if (path && (!best || path.length < best.path.length)) best = { stand, path };
    }
    return best;
  }

  /**
   * The order to take the chests in, as an itinerary rather than a series of guesses.
   *
   * The torch is a deadline - when it burns out the crawl is failed, not merely ended -
   * so the order the chests are taken in is not a matter of taste. Nearest-first, which
   * is what asking "what is closest from here" every tick amounts to, is a greedy
   * heuristic and on a maze it is regularly worse than the best order by a wide margin:
   * the chest one step away can be down a dead end that costs twenty steps to leave.
   *
   * Levels are small - the game builds `e<=3 ? 2 : min(2+(e-3), 15)` chests - so for
   * the sizes that actually occur the best order is worth simply computing. Up to eight
   * it is exact, by held-karp over the pairwise distances. Beyond that it is
   * nearest-neighbour improved by 2-opt, which on a handful of points is within a few
   * per cent and costs nothing.
   *
   * Distances are real path lengths through the maze, not straight lines: a chest on
   * the far side of a wall is not near.
   */
  /**
   * The order to work the floor in: every chest, then out, walking as little as can be.
   *
   * The route has to end at the way out, so the last chest is the one nearest it - and
   * an order chosen without that in mind regularly finishes in the far corner and pays
   * the whole width of the maze to come back. The torch is a deadline, and that walk is
   * the difference between a crawl and a failed crawl.
   *
   * Distances are real path lengths in `world`, which is the floor with every removable
   * thing removed - a monster asleep in a corridor, a locked door, a shut chest. They
   * are all things the route will clear on its way past, so planning as though they
   * were already gone is what makes the order the true one rather than the one the
   * obstacles happen to allow. What it costs to clear them is paid in the same steps
   * either way: the door is on the path, so opening it is not a detour.
   *
   * Nothing is ever dropped. A stop with no route in `world` goes to the end of the
   * list instead of off it - it may open up once something in front of it is cleared,
   * and dropping it is how six chests became one and the run went home early.
   */
  function order(world, stops, exit) {
    if (stops.length < 2) return stops.slice();

    const reachFrom = (start) => stops.map((ch) => {
      let best = null;
      for (const [dr, dc] of STEPS) {
        const stand = [ch.cell[0] + dr, ch.cell[1] + dc];
        if (!world.open(stand[0], stand[1])) continue;
        const path = findPath(world, start, stand);
        if (path && (!best || path.length < best.cost)) best = { cost: path.length, stand };
      }
      return best;
    });

    const head = reachFrom(world.player);
    const live = stops.map((_, i) => i).filter((i) => head[i]);
    const lost = stops.map((_, i) => i).filter((i) => !head[i]);
    if (live.length < 2) return live.concat(lost).map((i) => stops[i]);

    const between = live.map((i) => reachFrom(head[i].stand));
    const cost = (a, b) => {
      const r = between[live.indexOf(a)][b];
      return r ? r.cost : Infinity;
    };
    const start = (i) => head[i].cost;
    // What it costs to leave from beside each chest. Without this the tour is shortest
    // to its last chest and says nothing about the walk home.
    const out = (i) => {
      if (!exit) return 0;
      const path = findPath(world, head[i].stand, exit.cell);
      return path ? path.length : 0;
    };

    // Levels are small - the game builds `e<=3 ? 2 : min(2+(e-3), 15)` chests - so for
    // the sizes that occur the best order is worth simply computing. Up to nine it is
    // exact, by held-karp with the way out fixed as the end; beyond that
    // nearest-neighbour improved by 2-opt, which on a handful of points is within a few
    // per cent and costs nothing.
    const best = live.length <= 9
      ? bestOrder(live, start, cost, out)
      : improve(greedy(live, start, cost), cost, start, out);
    return best.concat(lost).map((i) => stops[i]);
  }

  /** Exact shortest visiting order, by held-karp. Only called for small n. */
  function bestOrder(items, start, cost, out) {
    const n = items.length;
    const full = 1 << n;
    const best = new Array(full * n).fill(Infinity);
    const prev = new Array(full * n).fill(-1);
    for (let i = 0; i < n; i += 1) best[(1 << i) * n + i] = start(items[i]);
    for (let mask = 1; mask < full; mask += 1) {
      for (let last = 0; last < n; last += 1) {
        const here = best[mask * n + last];
        if (!(mask & (1 << last)) || here === Infinity) continue;
        for (let next = 0; next < n; next += 1) {
          if (mask & (1 << next)) continue;
          const to = mask | (1 << next);
          const c = here + cost(items[last], items[next]);
          if (c < best[to * n + next]) {
            best[to * n + next] = c;
            prev[to * n + next] = last;
          }
        }
      }
    }
    // The end is the one that leaves the shortest walk to the way out.
    let end = -1;
    let cheapest = Infinity;
    for (let i = 0; i < n; i += 1) {
      const total = best[(full - 1) * n + i] + (out ? out(items[i]) : 0);
      if (total < cheapest) { cheapest = total; end = i; }
    }
    // Every pairing is reachable in this world, so a finite tour exists; if the costs
    // said otherwise, fall back to the order they came in rather than to a short list.
    if (end < 0) return items.slice();
    const route = [];
    let mask = full - 1;
    let cur = end;
    while (cur >= 0 && route.length < n) {
      route.unshift(items[cur]);
      const p = prev[mask * n + cur];
      mask ^= 1 << cur;
      cur = p;
    }
    // A truncated walk-back means some leg was unreachable. Keep what it found and put
    // the rest after it, rather than losing them.
    if (route.length < n) {
      for (const i of items) if (!route.includes(i)) route.push(i);
    }
    return route;
  }

  /** Nearest-neighbour, for when exact would be silly. */
  function greedy(items, start, cost) {
    const left = items.slice();
    const out = [];
    let cur = null;
    while (left.length) {
      let bi = 0;
      for (let i = 1; i < left.length; i += 1) {
        const a = cur === null ? start(left[i]) : cost(cur, left[i]);
        const b = cur === null ? start(left[bi]) : cost(cur, left[bi]);
        if (a < b) bi = i;
      }
      cur = left.splice(bi, 1)[0];
      out.push(cur);
    }
    return out;
  }

  /** 2-opt: undo the crossings nearest-neighbour leaves behind. */
  function improve(order, cost, start, out) {
    const total = (o) => o.reduce((sum, x, i) => sum + (i ? cost(o[i - 1], x) : start(x)), 0)
      + (out && o.length ? out(o[o.length - 1]) : 0);
    let best = order.slice();
    let bestCost = total(best);
    for (let pass = 0; pass < 8; pass += 1) {
      let moved = false;
      for (let i = 0; i < best.length - 1; i += 1) {
        for (let j = i + 1; j < best.length; j += 1) {
          const trial = best.slice(0, i).concat(best.slice(i, j + 1).reverse(), best.slice(j + 1));
          const c = total(trial);
          if (c < bestCost - 1e-9) { best = trial; bestCost = c; moved = true; }
        }
      }
      if (!moved) break;
    }
    return best;
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

  /**
   * How long an action is given before it is called stuck.
   *
   * Not how long to wait: waiting a fixed time for something that takes a variable
   * time leaves dead air after every single action, and a level is a hundred of them.
   * The camera coming to rest is what ends an action - this is only the point at which
   * one that never started is given up on.
   */
  const ACTION_TIMEOUT_MS = 1200;

  /** How long a tap gets to start moving anything before it counts as a wall. */
  const START_GRACE_MS = 260;

  /** Give up on a level after this many actions rather than burn the torch in a loop. */
  const ACTION_BUDGET = 400;

  /**
   * How long nothing may change before the level is abandoned.
   *
   * Every way this used to stall came out the same on screen - the player standing
   * somewhere doing nothing, or turning on the spot, until the torch died. So there is
   * one notion of getting somewhere (a new square, a chest open, the door open) and one
   * answer when it stops happening. The game has a give-up button for exactly this, and
   * walking out with part of the loot beats burning the torch in a corner.
   */
  const STALL_MS = 25000;

  /** How many actions one chest or the door is worth before it is left alone. */
  const OPEN_ATTEMPTS = 8;

  /**
   * How many swings one monster is worth.
   *
   * Far more than a chest: a monster has several hearts and goes briefly untouchable
   * after each hit, so a good fight is a long run of clicks that mostly land on
   * nothing. Giving up at eight would abandon a fight that was going fine.
   */
  const FIGHT_ATTEMPTS = 120;

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
    // middle of the view. The camera sits above them and looks level, so they land
    // below centre and a click at the middle sails over.
    //
    // It answers whether it found anything to press. A click with nothing under it is
    // not a thing that will start working if repeated, and treating it as one is how
    // the driver used to stand in front of a chest pressing forever.
    const click = deps.click || (() => false);
    // Leaving is the last rung of the ladder. The game has a give-up button for exactly
    // this, and walking out with part of the loot beats burning the torch in a corner.
    const leave = deps.leave || (() => false);
    // How many grey keys are in hand, read off the same bar the player reads. Optional:
    // without it the driver behaves as it did, which is to try the door and find out.
    const keys = deps.keys || null;
    const now = deps.now || Date.now;
    const timeoutMs = deps.timeoutMs || ACTION_TIMEOUT_MS;
    const graceMs = deps.graceMs || START_GRACE_MS;
    const stallMs = deps.stallMs || STALL_MS;

    let startedAt = 0;
    let pending = null;        // { key, from: [x, z], cell: [r, c] }
    // Cells a tap proved solid. The maze is rebuilt from the scene on every step, so
    // marking one on that object lasts exactly one tick and the driver walks into the
    // same wall for as long as the torch holds out.
    let walled = new Set();
    // Squares a step failed on once. A second failure makes it a wall; the first only
    // makes it worth trying again.
    let refused = new Map();
    // Targets that would not open however we stood. Kept apart from `walled`: the cell
    // is fine, it is the thing on it we have given up on.
    let abandoned = new Set();
    let tries = new Map();     // target -> how many actions spent trying to open it
    let actions = 0;
    let lastScene = null;
    let progressAt = 0;
    let progressMark = '';
    let gaveUp = false;
    // What the run did, so that a run can be asked afterwards instead of guessed at.
    // Until now the driver logged only its failures, and a level that quietly left two
    // of three chests behind looked exactly like a level that had only one.
    let tally = null;

    /**
     * Everything about the level resets when the scene does.
     *
     * The scene object itself is the identity. Reading `window.__bd_dungeon` here
     * instead would have been the one place this file reached out of its own
     * dependencies - and it broke the tests the moment they ran without a browser,
     * which is exactly what that rule is for.
     */
    function freshen(sc, t) {
      if (lastScene === sc) return;
      lastScene = sc;
      walled = new Set();
      refused = new Map();
      abandoned = new Set();
      tries = new Map();
      actions = 0;
      pending = null;
      startedAt = 0;
      progressAt = t;
      progressMark = '';
      gaveUp = false;
      if (sc) clearTrace();
      tally = sc
        ? { chests: 0, opened: 0, doors: 0, doorsOpened: 0, golden: false, why: '' }
        : null;
    }

    const nameOf = (target) => {
      if (target.isExit) return 'exit';
      if (target.isEnemy) return `foe:${target.cell[0]},${target.cell[1]}`;
      return `${target.cell[0]},${target.cell[1]}`;
    };

    /**
     * Stand by without losing our place.
     *
     * Called for every tick the driver is not allowed to act on - a dialogue on screen,
     * mostly. Without it the stall timer counts that waiting as standing still, and a
     * long conversation ends the crawl the moment it is over.
     */
    function hold() {
      progressAt = now();
      pending = null;
    }

    /** One line when a run ends, whichever way it ended. */
    function report() {
      if (!tally) return;
      if (TRACE.length) LAST_TRACE = TRACE.slice();
      const left = tally.chests - tally.opened;
      const how = tally.why || 'the level ended';
      log('DGN', `run over: ${tally.opened}/${tally.chests} chests`
        + (tally.golden ? ' (golden key taken)' : ', NO GOLDEN KEY')
        + (tally.doors ? `, ${tally.doorsOpened}/${tally.doors} doors` : '')
        + `, ${actions} actions - ${how}`, left > 0 || !tally.golden ? 'warn' : '');
      tally = null;
    }

    /** Walk out, and say why. Once only - the button takes a moment to answer. */
    function giveUp(why) {
      if (gaveUp) return true;
      gaveUp = true;
      if (tally) tally.why = why;
      log('DGN', `leaving the dungeon: ${why}`, 'warn');
      leave();
      return true;
    }

    /**
     * One action, or nothing while the last one is still settling.
     * Returns false when there is no dungeon to drive.
     */
    function step() {
      const sc = scene();
      const maze = readMaze(sc);
      if (!maze) {
        pending = null;
        report();
        lastScene = null;
        return false;
      }
      const t = now();
      freshen(sc, t);

      // A level whose way out is shut and which has no chests in it at all is not a
      // level yet. The golden key that opens that door is in a chest - the game's own
      // door asks `hasGoldenKey()` and refuses otherwise - so a shut door with no chest
      // anywhere is not a hard puzzle, it is a scene still being built. Acting on one
      // is not hypothetical: a run went "entering the dungeon" -> "giving up on exit
      // after 8 tries" -> "leaving" in nine seconds, having planned in the moment
      // before the chests existed, with the only thing in sight a door that could not
      // open. Waiting costs a tick; acting cost the whole run.
      if (!maze.chests.length && maze.exit && maze.exit.shut) {
        progressAt = t;
        return true;
      }
      for (const at of walled) {
        const [r, c] = at.split(',').map(Number);
        if (maze.blocked[r]) maze.blocked[r][c] = true;
      }

      // What counts as getting somewhere: standing somewhere new, or a chest or the
      // door having opened. Everything else is effort, and effort that never turns into
      // one of these is the shape of every way this used to stall.
      const shut = maze.chests.filter((c) => c.shut).length;
      if (tally) {
        tally.chests = Math.max(tally.chests, maze.chests.length);
        tally.opened = Math.max(tally.opened, maze.chests.length - shut);
        const gold = maze.chests.find((c) => c.golden);
        if (gold && !gold.shut) tally.golden = true;
        const doors = maze.doors || [];
        tally.doors = Math.max(tally.doors, doors.length);
        tally.doorsOpened = Math.max(tally.doorsOpened,
          doors.filter((d) => !d.shut).length);
      }
      // A fight counts as getting somewhere even though the player does not move: what
      // changes is the monster, and it leaves the scene when it dies. Without this a
      // long fight looks exactly like a hang and the driver walks out of a level it
      // was winning.
      const foes = (maze.enemies || []).length;
      const mark = `${maze.player[0]},${maze.player[1]}|${shut}|${foes}`
        + `|${maze.exit && maze.exit.shut}`;
      if (mark !== progressMark) {
        progressMark = mark;
        progressAt = t;
      } else if (t - progressAt > stallMs) {
        return giveUp(`nothing has changed for ${Math.round(stallMs / 1000)}s`);
      }

      // Is the last action still playing out?
      //
      // An action ends when the camera stops, not when a timer says so. Both a step and
      // a turn animate, for about six tenths of a second, but waiting a fixed time for
      // them means dead air after every one - and a level is a hundred actions. So the
      // camera is watched instead: while it is still changing the action is running,
      // and the moment it holds still the next one goes out.
      if (pending) {
        const here = `${maze.at[0]},${maze.at[1]},${maze.facing.toFixed(3)}`;
        if (here !== pending.seen) {
          pending.seen = here;
          pending.moving = true;
          return true;                      // still going
        }
        // Held still. If it never moved at all, give the tap a moment to take effect
        // before concluding there is a wall in the way.
        if (!pending.moving && t - startedAt < graceMs) return true;
        if (pending.moving && t - startedAt < timeoutMs && !pending.settled) {
          // One more look: the animation can pause on a frame boundary.
          pending.settled = true;
          return true;
        }

        const done = pending;
        pending = null;
        if (done.kind === 'move') {
          const moved = done.from[0] !== maze.at[0] || done.from[1] !== maze.at[1];
          if (!moved) {
            // A step that moved nothing is *evidence* of a wall, not proof of one. The
            // game drops input while it is busy - the entry animation most of all - and
            // taking the first failure as fact was ruinous: the very first move of a run
            // would fail, the one square out of the start would be written off, and a
            // floor whose start has a single exit was over before it began. Two in a row
            // on the same square is a wall; one is a retry.
            const at = `${done.cell[0]},${done.cell[1]}`;
            const missed = (refused.get(at) || 0) + 1;
            refused.set(at, missed);
            if (missed < 2) return true;
            if (!walled.has(at)) {
              walled.add(at);
              log('DGN', `(${at}) is walled after all`, 'warn');
            }
            if (maze.blocked[done.cell[0]]) maze.blocked[done.cell[0]][done.cell[1]] = true;
            return true;
          }
          // It moved, so whatever refusal we had recorded was the game being busy.
          refused.clear();
        }
      }

      if (actions >= ACTION_BUDGET) {
        return giveUp(`${ACTION_BUDGET} actions without finishing`);
      }

      const goal = nextGoal(maze, abandoned, keys ? keys() : null);
      note({
        t,
        at: maze.player.join(','),
        facing: Math.round((maze.facing * 180) / Math.PI),
        goal: goal ? `${goal.kind}@${goal.target && goal.target.cell
          ? goal.target.cell.join(',') : '-'}` : 'none',
        steps: goal ? goal.path.length : -1,
        shut: maze.chests.filter((c) => c.shut).length,
        chests: maze.chests.length,
        doorsShut: (maze.doors || []).filter((d) => d.shut).length,
        exit: maze.exit ? (maze.exit.shut ? 'shut' : 'open') : 'none',
        foes: (maze.enemies || []).filter((f) => f.inBattle).length,
      });
      if (!goal) {
        // Nothing left that can be reached. If the door is open we are simply done and
        // the game will take us out; otherwise there is no way on and no reason to wait.
        return maze.exit && !maze.exit.shut ? true : giveUp('nothing left that can be reached');
      }

      // Standing beside the chest already, or in front of the door: face it, then open
      // it. Walking onto a chest is not a thing that can happen - its collision box
      // fills the square - so arriving is never what opens one, and the first driver
      // walked the whole route and came back with nothing.
      // A locked door is opened the same way a chest is: stand beside it, face it,
      // click it. The game's own handler is the same shape - a pick that hits the mesh
      // or its box, and `isPlayerFacing(5)`. What differs is that it can refuse: with
      // no grey key left `onTryOpen` returns false and the door simply stays shut, so
      // the attempts budget below is what stops the driver standing there forever.
      if ((goal.kind === 'chest' || goal.kind === 'door' || goal.kind === 'exit'
        || goal.kind === 'fight' || goal.kind === 'engage' || goal.kind === 'leave'
        || goal.kind === 'talk') && !goal.path.length) {
        const target = goal.target;
        const key = nameOf(target);
        const spent = (tries.get(key) || 0) + 1;
        tries.set(key, spent);
        // A door we have no grey key for gets two tries, not eight. One is worth
        // spending because the game has a second way to open one; the rest would be
        // torch burned on a locked door.
        const allowed = goal.kind === 'fight' ? FIGHT_ATTEMPTS
          : (goal.kind === 'door' && keys && keys() && keys().grey === 0) ? 2
            : OPEN_ATTEMPTS;
        if (spent > allowed) {
          // It would not open however we stood. The cell is fine; the thing on it is
          // what we are giving up on, so the door stays reachable through it.
          abandoned.add(key);
          log('DGN', `giving up on ${key} after ${allowed} tries`, 'warn');
          return true;
        }
        // A monster that has not woken cannot be clicked at all - the game hides its
        // sprite and its handler is gated on `inBattle`. What wakes it is being looked
        // at: `isPlayerFacingEnemy(1.05) && this.startBattle()`, in the enemy's own
        // update. So for one of those the answer is never a click, it is to turn until
        // we are facing it, which the code below does. Standing beside one and waiting
        // for it to notice us is how a run spent two hundred ticks doing nothing.
        // An open way out is not clicked either: it is *stood on*. The game's door
        // fires onEnterTile from its own update the moment the player's tile matches,
        // and the square the route ends on is not quite that tile - so the last thing a
        // finished floor needs is one more step into the doorway. Without it the driver
        // opened every chest, walked to the door, opened it, and then stood in front of
        // it until the torch went out.
        if (goal.kind !== 'engage' && goal.kind !== 'leave'
          && (goal.kind === 'fight' || canOpen(maze, target))) {
          // A click that found nothing under it will not start working if repeated.
          if (click(target)) {
            note({ t, act: 'click', why: nameOf(target) });
            // One word each. The game's own `hasTalked` closes the door behind us, so a
            // second click is an action spent on nothing.
            if (goal.kind === 'talk') abandoned.add(nameOf(target));
            actions += 1;
            startedAt = t;
            return true;
          }
          log('DGN', `nothing to click on ${key} from here`, 'warn');
        }
        // Not square enough on yet, or the click had no target. Turn towards it a
        // quarter at a time.
        //
        // From the world offset, not the difference of cells: the door rounds onto the
        // square you use it from, so that difference is (0,0) and there is nothing to
        // turn towards. `keyFor` reads (dRow, dCol) as (z, x), which is what these are.
        const act = keyFor(maze.facing, target.world[1] - maze.at[1], target.world[0] - maze.at[0]);
        // `keyFor` answers "how do I get there", and for something straight ahead or
        // straight behind the answer is to walk. Here we do not want to walk, we want
        // to look at it - and taking `KeyS` for a turn is how the player came to step
        // backwards away from a chest directly opposite and then fail to click it.
        //
        // Nor may it walk *forwards*. We are standing on the square the route chose,
        // which is next to the thing, and the thing's own square is solid - a chest
        // fills its cell, a shut door fills its cell, a monster's box fills its cell.
        // So the step cannot succeed, and the driver read the failure the only way it
        // knows: it wrote that cell down as a wall, for the rest of the run. Two of
        // those and the floor is in pieces - `(8,1) is walled after all` was the driver
        // walling off the very door it had come to open. The way out is the exception:
        // it is not solid, it is the square you stand on, so a step onto it is real.
        const closeUp = goal.kind !== 'exit' && goal.kind !== 'leave';
        const key2 = act.kind === 'move'
          ? (act.key === 'KeyW' && !closeUp ? 'KeyW' : 'KeyD')
          : act.key;
        note({ t, act: key2, why: `face ${nameOf(target)}` });
        pending = {
          kind: key2 === 'KeyW' ? 'move' : 'turn',
          key: key2,
          from: maze.at.slice(),
          cell: target.cell,
          seen: `${maze.at[0]},${maze.at[1]},${maze.facing.toFixed(3)}`,
        };
        tap(key2);
        actions += 1;
        startedAt = t;
        return true;
      }

      if (!goal.path.length) return true;
      const next = goal.path[0];
      const act = keyFor(maze.facing, next[0] - maze.player[0], next[1] - maze.player[1]);
      note({ t, act: act.key, why: `walk to ${next.join(',')}` });
      pending = {
        kind: act.kind,
        key: act.key,
        from: maze.at.slice(),
        cell: next,
        seen: `${maze.at[0]},${maze.at[1]},${maze.facing.toFixed(3)}`,
      };
      tap(act.key);
      actions += 1;
      startedAt = t;
      return true;
    }

    return {
      step,
      hold,
      /** For the panel and the tests: what it thinks it is doing. */
      report: () => ({
        actions,
        walled: [...walled],
        abandoned: [...abandoned],
        gaveUp,
        pending,
      }),
    };
  }

  const api = { create, readMaze, findPath, nextGoal, keyFor, canOpen,
    order, trace, clearTrace,
    SQUARE, CELL, STEPS, ACTION_TIMEOUT_MS, OPEN_RANGE, OPEN_DOT,
    STALL_MS, OPEN_ATTEMPTS, ACTION_BUDGET };

  // The game runs Electron with node_integration, so `module` exists in the renderer
  // too, and the usual "module exists, therefore Node" check is wrong here.
  if (typeof window !== 'undefined') {
    (window.__bd_mod = window.__bd_mod || {}).dungeon = api;
  } else {
    (root.__bd_mod = root.__bd_mod || {}).dungeon = api;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof self !== 'undefined' ? self : globalThis));
