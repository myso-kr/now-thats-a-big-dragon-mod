'use strict';
// The dungeon reader, A* and the driver, against a fake Babylon scene.
//
// The fake is built from a picture of a maze, so a test says what it means:
//
//   '#####'
//   '#@..X'      @ where the player stands   X the way out
//   '#.#$#'      $ a chest                   # solid
//
// Every square carries a floor and the solid ones carry a wall, which is how the game
// draws it - and getting that wrong is what let A* route through the outside of the
// maze the first time.

const test = require('node:test');
const assert = require('node:assert');
const D = require('./dungeon.js');

const { SQUARE, CELL } = D;

/** A scene whose meshes spell out the given picture. */
function sceneOf(picture, { facing = Math.PI } = {}) {
  const meshes = [];
  let player = null;
  const put = (name, x, z) => meshes.push({ name, position: { x, z, y: 0 } });

  picture.forEach((line, r) => {
    [...line].forEach((ch, c) => {
      // A cell is 2x2 squares; the first square of cell (r,c) sits at (1,1) in world.
      const x0 = 1 + c * CELL;
      const z0 = 1 + r * CELL;
      for (const dx of [0, SQUARE]) {
        for (const dz of [0, SQUARE]) {
          const i = meshes.length;
          put(`f00_${i}`, x0 + dx, z0 + dz);
          if (ch === '#') { put(`w00_${i}0`, x0 + dx, z0 + dz); put(`w00_${i}1`, x0 + dx, z0 + dz); }
        }
      }
      const cx = x0 + SQUARE / 2;
      const cz = z0 + SQUARE / 2;
      if (ch === '$') {
        put(`chest_${r}_${c}`, cx, cz);
        // The collision box is what makes a chest an obstacle, and the game turning its
        // collisions off is what marks it opened - so the fake needs both, or nothing
        // here behaves the way the dungeon does.
        const box = { name: `chestCollision_${r}_${c}`, position: { x: cx, z: cz, y: 1 },
          checkCollisions: true };
        meshes.push(box);
      }
      if (ch === 'M') {
        // Mookie, or one of the rescue characters: a collision box on a tile, and no
        // way to move it. The sprite is not what blocks - the box is.
        put(`character_mookie_${r}${c}`, cx, cz);
        put(`characterCollision_mookie_${r}${c}`, cx, cz);
      }
      if (ch === 'Z') {
        // A monster that has not engaged: its sprite is hidden, and the game will not
        // register a click on it until you come near and it wakes. Its box blocks the
        // way in the meantime.
        put(`enemy_spider_${r}${c}`, cx, cz);
        meshes[meshes.length - 1].isVisible = false;
        put(`enemy_collision_spider_${r}${c}`, cx, cz);
      }
      if (ch === 'D') {
        // A locked door: a ground tile plus a collision box, exactly as the game builds
        // one. Its box carries the open/shut signal the same way a chest's does.
        put(`door_${r}_${c}`, cx, cz);
        meshes.push({ name: `doorCollision_${r}_${c}`, position: { x: cx, z: cz, y: 1 },
          checkCollisions: true });
      }
      if (ch === 'X') {
        put(`exitDoor_${r}_${c}`, cx, cz);
        meshes.push({ name: `exitDoorCollision_${r}_${c}`, position: { x: cx, z: cz, y: 1 },
          checkCollisions: true });
      }
      if (ch === '@') player = [cx, cz];
    });
  });

  assert.ok(player, 'the picture needs an @');
  return {
    meshes,
    activeCamera: { position: { x: player[0], z: player[1], y: 2 }, rotation: { y: facing } },
  };
}

const SIMPLE = [
  '#####',
  '#@..X',
  '#.#$#',
  '#####',
];

test('a disposed scene reads as no maze rather than an empty one', () => {
  assert.strictEqual(D.readMaze(null), null);
  assert.strictEqual(D.readMaze({ meshes: [], activeCamera: {} }), null);
});

test('solid squares are the ones carrying a wall', () => {
  const m = D.readMaze(sceneOf(SIMPLE));
  assert.deepStrictEqual(m.blocked[0], [true, true, true, true, true]);
  // (2,3) holds a shut chest, which fills its square just as a wall does. The door at
  // (1,4) does not: it hangs on the wall past the square you stand on to use it, so
  // blocking that square would leave nowhere to stand.
  assert.deepStrictEqual(m.blocked[1], [true, false, false, false, false]);
  assert.deepStrictEqual(m.blocked[2], [true, false, true, true, true]);
});

test('an opened chest stops blocking its square', () => {
  const scene = sceneOf(SIMPLE);
  for (const x of scene.meshes) if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
  const m = D.readMaze(scene);
  assert.strictEqual(m.open(2, 3), true);
  assert.strictEqual(m.chests[0].shut, false);
});

test('the player, the chest and the way out land on the right cells', () => {
  const m = D.readMaze(sceneOf(SIMPLE));
  assert.deepStrictEqual(m.player, [1, 1]);
  assert.deepStrictEqual(m.chests.map((c) => c.cell), [[2, 3]]);
  assert.deepStrictEqual(m.exit.cell, [1, 4]);
  assert.strictEqual(m.exit.shut, true, 'locked until the golden key turns up');
});

test('a cell with no floor under it is blocked, not open', () => {
  // The grid is sized from the outermost floor, so its far edge can hold squares the
  // level never laid. Reading those as open sent A* through the outside of the maze.
  const scene = sceneOf(SIMPLE);
  scene.meshes = scene.meshes.filter((x) => !(x.position.x > 16 && x.position.z > 4));
  const m = D.readMaze(scene);
  assert.strictEqual(m.open(2, 4), false);
});

test('A* takes the shortest way and returns the cells to walk', () => {
  const m = D.readMaze(sceneOf(SIMPLE));
  assert.deepStrictEqual(D.findPath(m, [1, 1], [1, 3]), [[1, 2], [1, 3]]);
});

test('the door is walked to and clicked, not stood beside', () => {
  // It rounds onto the very square you use it from. Treating it as a chest - block
  // that square, stand beside it - had the player pacing in front of the door forever,
  // because "beside the door" and "where I am" were the same place.
  const scene = sceneOf(SIMPLE);
  for (const x of scene.meshes) if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
  const goal = D.nextGoal(D.readMaze(scene));
  assert.strictEqual(goal.kind, 'exit');
  assert.deepStrictEqual(goal.cell, [1, 4], 'the door square itself');
  assert.strictEqual(goal.target.shut, true);
});

test('once the door is open, walking through it is the goal', () => {
  const scene = sceneOf(SIMPLE);
  for (const x of scene.meshes) {
    if (/^(chest|exitDoor)Collision/.test(x.name)) x.checkCollisions = false;
  }
  const goal = D.nextGoal(D.readMaze(scene));
  assert.strictEqual(goal.kind, 'leave');
  assert.deepStrictEqual(goal.cell, [1, 4]);
});

test('A* refuses a goal that is walled in rather than walking at it', () => {
  const m = D.readMaze(sceneOf(['####', '#@.#', '####']));
  assert.strictEqual(D.findPath(m, [1, 1], [0, 0]), null);
});

test('A* going nowhere is an empty path, not a null one', () => {
  const m = D.readMaze(sceneOf(SIMPLE));
  assert.deepStrictEqual(D.findPath(m, [1, 1], [1, 1]), []);
});

test('A* rounds the corner rather than through it', () => {
  const m = D.readMaze(sceneOf(['#####', '#@#.#', '#...#', '#####']));
  const path = D.findPath(m, [1, 1], [1, 3]);
  assert.deepStrictEqual(path, [[2, 1], [2, 2], [2, 3], [1, 3]]);
});

test('every chest is taken before the way out, because the key is in one', () => {
  const m = D.readMaze(sceneOf(SIMPLE));
  const first = D.nextGoal(m);
  assert.strictEqual(first.kind, 'chest');
  // Beside the chest at (2,3), never on it.
  assert.deepStrictEqual(first.cell, [1, 3]);
  assert.deepStrictEqual(first.target.cell, [2, 3]);

  const scene = sceneOf(SIMPLE);
  for (const x of scene.meshes) if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
  assert.strictEqual(D.nextGoal(D.readMaze(scene)).kind, 'exit');
});

test('a route to a chest does not step on the way out', () => {
  // The game's own door fires on entry - `t === tileCol && i === tileRow` and it calls
  // onEnterTile, no click, no facing. So the corridor here is a trap: the shortest way
  // from the player to the chest runs straight over the door, and taking it ends the
  // floor with the chest still shut. That is the run this reproduces: golden key out of
  // the first chest, and out through the second chest's front door.
  const PIC = ['#####', '#@X$#', '#...#', '#####'];
  const scene = sceneOf(PIC);
  // Open, which is the only state in which standing on it does anything: the game's
  // door opens on a click and only with the golden key, and `update` fires onEnterTile
  // solely `if (this.isOpen)`.
  for (const x of scene.meshes) if (x.name.startsWith('exitDoorCollision')) x.checkCollisions = false;
  const m = D.readMaze(scene);
  assert.strictEqual(m.exit.shut, false, 'the fixture should have it open');
  const goal = D.nextGoal(m);
  assert.strictEqual(goal.kind, 'chest');
  const door = m.exit.cell.join(',');
  assert.ok(!goal.path.some((cell) => cell.join(',') === door),
    `the route ${JSON.stringify(goal.path)} steps on the door at ${door}`);
  // The way round is longer, and longer is the point.
  assert.ok(goal.path.length > 1, 'it should have gone the long way');

  // Shut, it is inert, and going round it would just be steps off the torch.
  const shutGoal = D.nextGoal(D.readMaze(sceneOf(PIC)));
  assert.strictEqual(shutGoal.kind, 'chest');
  assert.ok(shutGoal.path.length < goal.path.length,
    'a shut door is not a hazard and should not be walked round');
});

test('the golden key is known, even though it does not steer the route', () => {
  // The game hands it out on chestIndex === 0 and rolls for the rest, so it is always
  // the first chest built, and Babylon keeps scene.meshes in creation order. The run
  // summary says whether it was taken, which is the difference between a crawl that
  // counted and one that did not.
  const m = D.readMaze(sceneOf(ALCOVES));
  assert.strictEqual(m.chests.filter((c) => c.golden).length, 1);
  assert.deepStrictEqual(m.chests.find((c) => c.golden).cell, m.chests[0].cell);
});

test('a chest reachable only over the way out is still worth going for', () => {
  // One chest lost to an early exit beats every chest lost to standing still, so when
  // there is no way round, the driver takes the door route rather than giving up.
  const m = D.readMaze(sceneOf([
    '####',
    '#@X$',
    '####',
  ]));
  const goal = D.nextGoal(m);
  assert.strictEqual(goal.kind, 'chest', 'it should still go');
  assert.ok(goal.path.length, 'and it has to walk to get there');
});

/** What "take the nearest each time" actually does, re-asked from where you land. */
function nearestFirst(m) {
  const left = m.chests.filter((c) => c.shut).slice();
  const out = [];
  let from = m.player;
  while (left.length) {
    let bi = -1;
    let bp = null;
    for (let i = 0; i < left.length; i += 1) {
      for (const [dr, dc] of D.STEPS) {
        const stand = [left[i].cell[0] + dr, left[i].cell[1] + dc];
        if (!m.open(stand[0], stand[1])) continue;
        const path = D.findPath(m, from, stand);
        if (path && (!bp || path.length < bp.length)) { bp = path; bi = i; }
      }
    }
    if (bi < 0) break;
    out.push({ kind: 'chest', cell: left[bi].cell });
    left.splice(bi, 1);
    from = bp.length ? bp[bp.length - 1] : from;
  }
  return out;
}

/** Walk an order and total what it costs, so a plan can be weighed against another. */
function costOf(m, order) {
  let from = m.player;
  let total = 0;
  for (const stop of order) {
    let best = null;
    for (const [dr, dc] of D.STEPS) {
      const stand = [stop.cell[0] + dr, stop.cell[1] + dc];
      if (!m.open(stand[0], stand[1])) continue;
      const path = D.findPath(m, from, stand);
      if (path && (!best || path.length < best.length)) best = path;
    }
    if (!best) return Infinity;
    total += best.length;
    from = best.length ? best[best.length - 1] : from;
  }
  return total;
}

// Chests sit in alcoves off the corridor, which is where the game puts them. A shut
// chest blocks its own square, so one standing in a corridor walls the maze in half and
// the far side is unreachable until it is opened - which it cannot be, from the far
// side. That is a picture the game never draws, and it is not what these are testing.
const ALCOVES = [
  '#######',
  '#@....#',
  '#.#.#.#',
  '#$#$#$#',
  '#######',
];

// A maze that branches, which is what the game builds once a level is past its first
// few. Nearest-first commits to the near chest and pays for it on the way back out.
const BRANCHED = [
  '##########',
  '#@.......#',
  '#.#.####.#',
  '#.$.#..$.#',
  '#.###.##.#',
  '#....$...#',
  '##########',
];

test('planning the order beats taking the nearest, and measurably', () => {
  const m = D.readMaze(sceneOf(BRANCHED));
  const planned = costOf(m, D.order(m, m.chests.filter((c) => c.shut)));
  const naive = costOf(m, nearestFirst(m));
  assert.ok(planned < naive, `planned ${planned}, nearest-first ${naive} - no gain`);
  // 17 against 23 when this was written. Asserting the exact numbers would break on any
  // harmless change to the fixture; asserting a real margin is the point.
  assert.ok(naive - planned >= 4, `only ${naive - planned} steps saved`);
});

test('the route visits every chest that can be reached, once each', () => {
  const m = D.readMaze(sceneOf(ALCOVES));
  const plan = D.order(m, m.chests.filter((c) => c.shut));
  const cells = plan.map((p) => p.cell.join(','));
  assert.strictEqual(new Set(cells).size, cells.length, 'no chest twice');
  const reachable = m.chests
    .filter((c) => c.shut && costOf(m, [{ kind: 'chest', cell: c.cell }]) < Infinity)
    .map((c) => c.cell.join(','));
  assert.ok(reachable.length >= 3, 'the fixture should have chests to visit');
  assert.deepStrictEqual(cells.slice().sort(), reachable.slice().sort());
});

test('the planned order is never worse than taking the nearest each time', () => {
  // Which is the whole reason for planning it. Nearest-first is a guess made from
  // wherever you are standing; on a maze the chest one step away can be down a dead
  // end that costs twenty to leave again.
  const mazes = [
    ALCOVES,
    ['#########', '#@......#', '#.#.#.#.#', '#$#$#$#$#', '#########'],
    ['#########', '#..@....#', '#.#####.#', '#$.....$#', '#########'],
    ['#########', '#@......#', '#.#####.#', '#.$...$.#', '#.#####.#', '#......$#', '#########'],
    BRANCHED,
  ];
  for (const pic of mazes) {
    const m = D.readMaze(sceneOf(pic));
    const planned = costOf(m, D.order(m, m.chests.filter((c) => c.shut)));
    const naive = nearestFirst(m);
    assert.ok(planned <= costOf(m, naive),
      `planned ${planned} steps against nearest-first ${costOf(m, naive)} on ${pic.join('/')}`);
  }
});

test('the route leaves out chests already opened or given up on', () => {
  const scene = sceneOf(ALCOVES);
  for (const x of scene.meshes) if (x.name === 'chestCollision_3_1') x.checkCollisions = false;
  const m = D.readMaze(scene);
  const plan = D.order(m, m.chests.filter((c) => c.shut && c.cell.join(',') !== '3,3'));
  const cells = plan.map((p) => p.cell.join(','));
  assert.ok(!cells.includes('3,1'), 'an opened chest is not a stop');
  assert.ok(!cells.includes('3,3'), 'nor is one we gave up on');
  assert.deepStrictEqual(cells, ['3,5'], 'and the rest are still on the list');
});

test('the order is fixed for the floor, not re-guessed from where you stand', () => {
  // The old planner answered "which is nearest from here" every tick, so walking
  // between two chests could swap them and the route would restart. The order is now
  // computed over the floor once, so asking again from anywhere on it gives the same
  // answer for what is still shut.
  const m = D.readMaze(sceneOf(ALCOVES));
  const shut = m.chests.filter((c) => c.shut);
  const a = D.order(m, shut).map((c) => c.cell.join(','));
  const b = D.order(m, shut).map((c) => c.cell.join(','));
  assert.deepStrictEqual(a, b);
});

test('a run says what it did when it ends', () => {
  // The driver used to log only its failures, so a level that left two of three chests
  // behind read exactly like a level that had only one - which is how the early exit
  // went unnoticed. Every run now ends with a line saying what it actually took.
  const scene = sceneOf(['#####', '#@.$X', '#####']);
  const said = [];
  let live = scene;
  const d = D.create({
    scene: () => live,
    tap: () => {},
    click: () => true,
    now: () => 0,
    log: (tag, text, level) => said.push({ tag, text, level }),
  });
  d.step();
  live = null;                       // the way out of every dungeon: the scene goes
  assert.strictEqual(d.step(), false);
  const line = said.find((e) => e.text.startsWith('run over:'));
  assert.ok(line, `no summary in ${JSON.stringify(said)}`);
  assert.match(line.text, /0\/1 chests/);
  assert.strictEqual(line.level, 'warn', 'a chest left behind is worth a warning');
});

test('standing beside a chest, it turns rather than walking into it', () => {
  // A chest fills its own square, so a step forward from beside it cannot move - and
  // the driver reads a step that moved nothing as a wall it did not know about, and
  // writes that square off for the rest of the run. It was doing that to the very
  // chests and doors it had come to open: `(8,1) is walled after all` on a door.
  const scene = sceneOf(['#####', '#@$.#', '#####'], { facing: Math.PI / 2 });
  const sent = [];
  const d = D.create({
    scene: () => scene, tap: (k) => sent.push(k), click: () => false,
    now: () => 0, log: () => {},
  });
  for (let i = 0; i < 6; i += 1) d.step();
  assert.ok(sent.length, 'it should have done something');
  assert.ok(!sent.includes('KeyW'), `it walked into the chest: ${sent.join(',')}`);
});

test('a floor sealed behind a door it has no key for is left at once', () => {
  // The game places doors on random corridor squares and checks nothing. In a perfect
  // maze every corridor square is a bridge, so a door beside the entrance seals the
  // floor - and the grey keys that would open it are in the chests behind it. Nobody
  // can finish that floor. What can be done is to see it and go, rather than spend the
  // torch proving it: eight clicks at the door, then eight more at a way out that only
  // opens to a golden key we could not have.
  const m = D.readMaze(sceneOf([
    '#####',
    '#@D$#',
    '#####',
    'X####',
  ]));
  assert.ok(m.chests.every((c) => c.shut), 'nothing opened yet');
  assert.ok(m.exit.shut, 'and the way out is shut');

  // With a key, the door is worth a try.
  assert.strictEqual(D.nextGoal(m, new Set(), { grey: 1 }).kind, 'door');
  // Without one, the door is still tried - but once it has been given up on there is
  // nothing else, and in particular not the way out.
  const after = D.nextGoal(m, new Set(['1,2']), { grey: 0 });
  assert.strictEqual(after, null, 'no golden key is possible, so the exit is not a goal');

  // And it is the *golden* chest that decides it. A floor can hand over an ordinary
  // chest and still be sealed away from the one with the key.
  const two = sceneOf(['######', '#@$D$#', '######', 'X#####']);
  for (const x of two.meshes) if (x.name === 'chestCollision_1_4') x.checkCollisions = false;
  const m2 = D.readMaze(two);
  assert.ok(m2.chests.some((c) => !c.shut), 'one of them is open');
  assert.ok(m2.chests.find((c) => c.golden).shut, 'but not the one with the key');
  assert.strictEqual(D.nextGoal(m2, new Set(['1,2', '1,3']), { grey: 0 }), null);
});

test('a character is a wall to walk round and a person to talk to', () => {
  // The game's own table gives mookie on level 4 and the worker on 8 and 10, and each
  // hands over a torch - which on a floor with a burning clock is more floor. He is not
  // an obstacle to clear, though: he says himself he cannot leave his tile.
  const m = D.readMaze(sceneOf(['#####', '#@M$#', '#####']));
  assert.strictEqual(m.open(1, 2), false, 'his tile is not walkable');
  assert.strictEqual((m.enemies || []).length, 0, 'and he is not a monster to fight');
  assert.strictEqual(m.npcs.length, 1);
  assert.deepStrictEqual(m.npcs[0].cell, [1, 2]);

  // And he comes first: the torch is worth most at the start.
  const goal = D.nextGoal(m);
  assert.strictEqual(goal.kind, 'talk');
  assert.deepStrictEqual(goal.cell, [1, 1], 'stood beside him');

  // Once talked to, he is just scenery - and the chest behind him is still walled off.
  const after = D.nextGoal(m, new Set(['1,2']));
  assert.notStrictEqual(after && after.kind, 'talk');
});

test('the rescue characters outside the walls are not visited', () => {
  // They stand beyond the maze with no collision box at all, and there is nothing to
  // say to them - they are the developer, waiting for someone who clipped through.
  const scene = sceneOf(['#####', '#@.$#', '#####']);
  scene.meshes.push({ name: 'character_dungeon_rescue_LEFT_1', position: { x: -6, z: 18, y: 1.5 } });
  const m = D.readMaze(scene);
  assert.deepStrictEqual(m.npcs, [], 'no box in the maze, so not one of ours');
});

test('a sleeping monster is walked up to, not treated as a wall', () => {
  // This is the run the user kept seeing: one chest opened and home early. A spider
  // asleep in the corridor cut the floor in two, and because `inBattle` gates the
  // game's click handler the driver had nothing to do about it - so it planned around
  // it, found nothing, and went to the way out with three chests still shut.
  const m = D.readMaze(sceneOf(['#####', '#@Z$#', '#####']));
  assert.strictEqual(m.enemies.length, 1);
  assert.strictEqual(m.enemies[0].inBattle, false, 'asleep');
  assert.strictEqual(m.open(1, 2), false, 'and blocking the way while it sleeps');

  const goal = D.nextGoal(m);
  assert.strictEqual(goal.kind, 'engage', 'so it is what we go and do something about');
  assert.deepStrictEqual(goal.target.cell, [1, 2]);
  assert.deepStrictEqual(goal.cell, [1, 1], 'walked up to, from beside');
});

test('an opened way out is stepped through, not stood in front of', () => {
  // onEnterTile fires from the door's own update when the player's tile matches its
  // own, and the square the route ends on is not quite that tile. A run that opened
  // every chest, walked to the door and opened it then stood there until the torch
  // went out - one step short of finishing.
  const scene = sceneOf(['#####', '#@..X', '#####'], { facing: Math.PI / 2 });
  for (const x of scene.meshes) {
    if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
    if (x.name.startsWith('exitDoorCollision')) x.checkCollisions = false;
  }
  const m = D.readMaze(scene);
  assert.strictEqual(m.exit.shut, false, 'the fixture has it open');
  const sent = [];
  const d = D.create({
    scene: () => scene, tap: (k) => sent.push(k),
    click: () => { throw new Error('an open door is walked through, not clicked'); },
    now: () => 0, log: () => {},
  });
  for (let i = 0; i < 6; i += 1) d.step();
  assert.ok(sent.includes('KeyW'), `it has to walk: ${sent.join(',')}`);
});

test('a sleeping monster is turned towards, because that is what wakes it', () => {
  // The enemy's own update starts the battle on `isPlayerFacingEnemy(1.05)`, and its
  // click handler is gated on `inBattle` - so there is nothing to click until it has
  // woken, and nothing wakes it but being looked at. Standing beside one and waiting
  // was two hundred ticks of nothing and a stalled run.
  const scene = sceneOf(['#####', '#@Z$#', '#####'], { facing: 0 });
  const sent = [];
  const d = D.create({
    scene: () => scene, tap: (k) => sent.push(k),
    click: () => { throw new Error('a sleeping monster must not be clicked at'); },
    now: () => 0, log: () => {},
  });
  d.step();
  assert.ok(sent.length, 'it has to do something rather than wait');
  assert.ok(['KeyA', 'KeyD'].includes(sent[0]), `turned to face it, got ${sent[0]}`);
});

test('a monster that has woken is fought before anything else', () => {
  const scene = sceneOf(['#####', '#@Z$#', '#####']);
  for (const x of scene.meshes) if (/^enemy_spider/.test(x.name)) x.isVisible = true;
  const m = D.readMaze(scene);
  const goal = D.nextGoal(m);
  assert.strictEqual(goal.kind, 'fight');
  assert.strictEqual(goal.path.length, 0, 'it is on us; the click is the whole action');
});

test('with no key in hand a door waits, but it is not written off', () => {
  // The count orders the work - the chests on this side are where the keys come from,
  // so they come first. It does not forbid the door: the game spends a grey key if
  // there is one and otherwise falls through to a second resource. A floor whose every
  // way on was a door came back "0 of 4 chests" when this was a prohibition.
  const reachable = D.readMaze(sceneOf([
    '######',
    '#@$#D#',
    '####$#',
  ]));
  const first = D.nextGoal(reachable, new Set(), { grey: 0 });
  assert.strictEqual(first.kind, 'chest', 'the chest on this side comes first');

  const onlyDoor = D.readMaze(sceneOf(['#####', '#@D$#', '#####']));
  for (const keys of [{ grey: 1 }, { grey: 0 }, null]) {
    const g = D.nextGoal(onlyDoor, new Set(), keys);
    assert.strictEqual(g && g.kind, 'door',
      `with nothing else on the floor it should try the door (keys ${JSON.stringify(keys)})`);
  }
});

test('doors in sequence are opened one after the other, not written off', () => {
  // The start opens onto a door, and that door onto another. Asking "would opening
  // *this* door reach a chest" answers no for both, because each is only reachable
  // through the one before it - and a floor built that way came back with every chest
  // unopened. The question has to be asked of the floor with all of them open.
  const m = D.readMaze(sceneOf([
    '#######',
    '#@#####',
    '#D#####',
    '#.#####',
    '#D#####',
    '#$#####',
  ]));
  assert.strictEqual(m.doors.length, 2);
  const goal = D.nextGoal(m, new Set(), { grey: 1 });
  assert.strictEqual(goal.kind, 'door');
  assert.deepStrictEqual(goal.target.cell, [2, 1], 'the near one first');

  // With the near one open, the far one is next.
  const scene = sceneOf(['#######', '#@#####', '#D#####', '#.#####', '#D#####', '#$#####']);
  for (const x of scene.meshes) if (x.name === 'doorCollision_2_1') x.checkCollisions = false;
  const next = D.nextGoal(D.readMaze(scene), new Set(), { grey: 1 });
  assert.strictEqual(next.kind, 'door');
  assert.deepStrictEqual(next.target.cell, [4, 1]);
});

test('a locked door is read as a door, not as bare floor', () => {
  // It was in none of the name patterns, so it read as floor: the driver planned
  // through it, walked into it, saw nothing move and wrote the cell down as a wall for
  // the rest of the run. Everything behind it was then unreachable and left there.
  const m = D.readMaze(sceneOf(['#####', '#@D$#', '#####']));
  assert.strictEqual(m.doors.length, 1);
  assert.deepStrictEqual(m.doors[0].cell, [1, 2]);
  assert.strictEqual(m.doors[0].shut, true);
  assert.strictEqual(m.open(1, 2), false, 'a shut door blocks its cell');
});

test('an opened door is floor again', () => {
  const scene = sceneOf(['#####', '#@D$#', '#####']);
  for (const x of scene.meshes) if (x.name.startsWith('doorCollision')) x.checkCollisions = false;
  const m = D.readMaze(scene);
  assert.strictEqual(m.doors[0].shut, false);
  assert.strictEqual(m.open(1, 2), true);
  // And with the way through open, the chest behind it is the goal again.
  assert.strictEqual(D.nextGoal(m).kind, 'chest');
});

test('a door in the way of a chest is opened, and from beside it', () => {
  const m = D.readMaze(sceneOf(['#####', '#@D$#', '#####']));
  const goal = D.nextGoal(m);
  assert.strictEqual(goal.kind, 'door', 'the chest is behind it, so the key is worth it');
  assert.deepStrictEqual(goal.target.cell, [1, 2]);
  assert.deepStrictEqual(goal.cell, [1, 1], 'stood beside it, never on it');
});

test('a door with nothing behind it is left alone', () => {
  // Grey keys are finite. A door is road, not loot: opened for what is past it and
  // never for its own sake.
  const m = D.readMaze(sceneOf([
    '#####',
    '#@.D#',
    '#$###',
    '#####',
  ]));
  const goal = D.nextGoal(m);
  assert.strictEqual(goal.kind, 'chest', 'the reachable chest comes first');

  const done = sceneOf(['#####', '#@.D#', '#$###', '#####']);
  for (const x of done.meshes) if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
  const after = D.nextGoal(D.readMaze(done));
  // Nothing behind the door and no way out drawn, so there is simply nothing to do -
  // what matters is that it did not spend a key on the door.
  assert.notStrictEqual(after && after.kind, 'door');
});

test('the door opened is the first one on the way, not the nearest one anywhere', () => {
  //  @ . D . $      the chest is behind the first door
  //  . # # # #
  //  D              a second door, closer as the crow flies, leading nowhere
  const m = D.readMaze(sceneOf([
    '#######',
    '#@.D.$#',
    '#.#####',
    '#D#####',
    '#######',
  ]));
  const goal = D.nextGoal(m);
  assert.strictEqual(goal.kind, 'door');
  assert.deepStrictEqual(goal.target.cell, [1, 3], 'the one between us and the chest');
});

test('a door is given up on when it will not open, and the run goes on', () => {
  // With no grey key left the game's onTryOpen returns false and the door stays shut.
  // The driver has to stop asking and take what else there is.
  const m = D.readMaze(sceneOf(['######', '#@D$.X', '######']));
  const first = D.nextGoal(m);
  assert.strictEqual(first.kind, 'door');
  const gaveUp = new Set([`${first.target.cell[0]},${first.target.cell[1]}`]);
  const then = D.nextGoal(m, gaveUp);
  assert.notStrictEqual(then && then.kind, 'door', 'it should not come back to it');
});

test('the order is the one that walks least, and nothing is lifted out of it', () => {
  // Shortest first, by real path length. Pulling the golden-key chest to the front was
  // tried and taken back out - the route opens every chest anyway, so the key comes
  // either way, and forcing it first only lengthens the walk.
  const m = D.readMaze(sceneOf(['########', '#$..@.$#', '########']));
  const plan = D.order(m, m.chests.filter((c) => c.shut));
  assert.strictEqual(plan.length, 2);
  assert.deepStrictEqual(plan[0].cell, [1, 6], 'the near one, two steps off');
  assert.deepStrictEqual(plan[1].cell, [1, 1]);
});

test('a chest is opened from beside it, at the range the game allows', () => {
  // Five world units and sixty degrees, read off the game's own click handler. A cell
  // is four, so the next cell along is inside it with nothing to spare.
  const m = D.readMaze(sceneOf(['####', '#@$#', '####'], { facing: Math.PI / 2 }));
  const chest = m.chests[0];
  assert.strictEqual(D.canOpen(m, chest), true, 'facing it from the next cell');
  assert.strictEqual(D.canOpen({ ...m, facing: -Math.PI / 2 }, chest), false, 'back turned');
  assert.strictEqual(D.canOpen({ ...m, at: [-20, 0] }, chest), false, 'too far away');
});

test('a chest nothing can reach is passed over rather than aimed at', () => {
  const m = D.readMaze(sceneOf(['#####', '#@.#$', '#####']));
  const goal = D.nextGoal(m);
  assert.strictEqual(goal, null, 'and with no way out either, there is nothing to do');
});

// ── The controls ─────────────────────────────────────────────────
// Measured in a live dungeon: W and S walk exactly one cell, A and D turn exactly a
// quarter, and holding a key is not a longer version of either - it starts a free spin.
// The first version treated all four as compass directions, so it sent S to go north
// and the player stood still while the torch burned.

const N = Math.PI;         // facing north is ry = pi, because forward is (sin ry, cos ry)
const E = Math.PI / 2;

test('walking forward and back needs no turn at all', () => {
  assert.deepStrictEqual(D.keyFor(N, -1, 0), { key: 'KeyW', kind: 'move' });
  assert.deepStrictEqual(D.keyFor(N, 1, 0), { key: 'KeyS', kind: 'move' });
  assert.deepStrictEqual(D.keyFor(E, 0, 1), { key: 'KeyW', kind: 'move' });
  assert.deepStrictEqual(D.keyFor(E, 0, -1), { key: 'KeyS', kind: 'move' });
});

test('a cell to the side is a turn first', () => {
  assert.strictEqual(D.keyFor(N, 0, 1).kind, 'turn');
  assert.strictEqual(D.keyFor(N, 0, -1).kind, 'turn');
  assert.strictEqual(D.keyFor(E, -1, 0).kind, 'turn');
});

test('north and south are not mirrored', () => {
  // atan2(dCol, -dRow) gets east and west right and swaps north and south, which is
  // exactly why only a live walk caught it.
  assert.strictEqual(D.keyFor(N, -1, 0).key, 'KeyW', 'facing north, north is forward');
  assert.notStrictEqual(D.keyFor(N, -1, 0).key, 'KeyS');
});

test('a cell behind is walked to backwards rather than turned towards', () => {
  // Two turns cost two settles, and the torch is paying for them.
  assert.deepStrictEqual(D.keyFor(N, 1, 0), { key: 'KeyS', kind: 'move' });
});

// ── The driver ───────────────────────────────────────────────────

function driver(picture, opts = {}) {
  const sent = [];
  let clock = 0;
  const scene = sceneOf(picture, opts);
  const d = D.create({
    scene: () => scene,
    tap: (code) => sent.push(code),
    now: () => clock,
    log: () => {},
    graceMs: 100,
    timeoutMs: 300,
  });
  return { d, sent, scene, tick: (ms = 100) => { clock += ms; return d.step(); } };
}

test('one action per tap, and nothing until it has settled', () => {
  // The fake camera never moves, so every action here is one that did nothing: it gets
  // the grace period and no more, which is what stops a wall costing a full timeout.
  const r = driver(SIMPLE);
  r.tick(0);
  assert.strictEqual(r.sent.length, 1, 'one key');
  r.tick(10);
  assert.strictEqual(r.sent.length, 1, 'inside the grace period, so still one');
  r.tick(200);
  assert.strictEqual(r.sent.length, 2, 'grace is over, so the next one goes out');
});

test('an action ends when the camera stops, not when a timer runs out', () => {
  // The point of the whole thing: a step that settles early must not be followed by
  // dead air, because a level is a hundred of them.
  const scene = sceneOf(['#####', '#@..X', '#####', '#$###'], { facing: Math.PI / 2 });
  for (const x of scene.meshes) {
    if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
  }
  let clock = 0;
  const sent = [];
  const d = D.create({
    scene: () => scene,
    tap: (code) => {
      sent.push(code);
      // The game moves the camera a cell; here that happens at once.
      scene.activeCamera.position.x += code === 'KeyW' ? CELL : 0;
    },
    now: () => clock,
    log: () => {},
    graceMs: 100,
    timeoutMs: 5000,
  });
  d.step();                       // taps, camera jumps
  clock += 10; d.step();          // sees it moved
  clock += 10; d.step();          // sees it hold still - one more look
  clock += 10; d.step();          // settled, so the next action goes out
  assert.strictEqual(sent.length, 2, `settled in 30ms, not 5000: sent ${sent.join(',')}`);
});

test('a chest directly behind is turned towards, never backed away from', () => {
  // `keyFor` answers "how do I get there", and for something straight behind the answer
  // is to walk backwards. Taking that as a turn is how the player stepped away from a
  // chest right opposite and then could not click it - seen on screen, not here.
  const scene = sceneOf(['####', '#$@#', '####'], { facing: Math.PI / 2 });  // chest west, looking east
  let clock = 0;
  const sent = [];
  const d = D.create({
    scene: () => scene,
    tap: (code) => sent.push(code),
    click: () => sent.push('CLICK'),
    now: () => clock,
    log: () => {},
    graceMs: 50,
    timeoutMs: 200,
  });
  d.step();
  assert.ok(sent.length, 'it did something');
  assert.notStrictEqual(sent[0], 'KeyS', 'walking away from the chest is never the move');
  assert.ok(['KeyA', 'KeyD'].includes(sent[0]), `expected a turn, got ${sent[0]}`);
});

test('with no live scene it drives nothing and says so', () => {
  const d = D.create({ scene: () => null, tap: () => {}, now: () => 0, log: () => {} });
  assert.strictEqual(d.step(), false);
});

test('a move that changed nothing twice marks the cell walled, and it sticks', () => {
  // The only collision signal there is: the grid comes from meshes and can be wrong.
  // Facing east down a corridor, so the very first action is a move rather than a turn,
  // and the fake camera never moves because nothing here moves it.
  //
  // Twice, not once. The game drops input while it is busy - the entry animation above
  // all - and calling the first failure a wall ended runs on the spot: the first move
  // out of the start would fail, its one square would be written off, and the floor was
  // over before it began.
  const warned = [];
  const scene = sceneOf(['####', '#@.X', '####', '#$##'], { facing: Math.PI / 2 });
  for (const x of scene.meshes) {
    if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
  }
  let clock = 0;
  const d = D.create({
    scene: () => scene,
    tap: () => {},
    now: () => clock,
    log: (tag, text, level) => warned.push(level),
    graceMs: 100,
    timeoutMs: 300,
  });
  d.step();
  clock += 200;
  d.step();
  assert.deepStrictEqual(d.report().walled, [], 'one refusal is only a retry');

  clock += 200;
  d.step();
  clock += 200;
  d.step();
  assert.ok(warned.includes('warn'), 'and the second is said out loud');
  assert.deepStrictEqual(d.report().walled, ['1,2']);

  // It has to survive the maze being rebuilt from the scene, which happens every step.
  clock += 200;
  d.step();
  assert.deepStrictEqual(d.report().walled, ['1,2'], 'remembered, not re-discovered');
});

// ── Not getting stuck ────────────────────────────────────────────
// Every way this stalled looked the same on screen: the player standing there, or
// turning on the spot, until the torch died. Reported from the other side of the
// screen - "sometimes it just stops in the dungeon" - and every one of them was a
// branch that did nothing and returned as though it had.

function stuckDriver(picture, over = {}) {
    const scene = sceneOf(picture, over.opts || {});
    let clock = 0;
    const log = [];
    const left = [];
    const d = D.create({
        scene: () => scene,
        tap: over.tap || (() => {}),
        click: over.click || (() => true),
        leave: () => { left.push(clock); return true; },
        now: () => clock,
        log: (tag, text, level) => log.push(`${level || 'info'}: ${text}`),
        graceMs: 10,
        timeoutMs: 50,
        stallMs: over.stallMs || 1000,
    });
    return { d, scene, log, left, tick: (ms = 100) => { clock += ms; return d.step(); } };
}

test('a level where nothing changes is left rather than stood in', () => {
    // The fake camera never moves and no chest ever opens, so this is every stall at
    // once. The old driver returned true here for as long as the torch lasted.
    const r = stuckDriver(SIMPLE);
    for (let i = 0; i < 30; i += 1) r.tick(100);
    assert.strictEqual(r.left.length, 1, 'it left, once');
    assert.ok(r.log.some((l) => l.startsWith('warn: leaving the dungeon')), r.log.join(' | '));
});

test('a chest that will not open is given up on, and the door still gets a turn', () => {
    // A click with nothing under it will not start working if repeated. The cell is
    // fine - it is the thing on it we stop trying - so the way out stays reachable.
    // The stall clock is given room here: in the game it is twenty-five seconds and
    // eight attempts take about five, so the per-target ladder is what runs first.
    const r = stuckDriver(['#####', '#@$.X', '#####'],
        { opts: { facing: Math.PI / 2 }, click: () => false, stallMs: 60000 });
    for (let i = 0; i < 40; i += 1) r.tick(100);
    assert.ok(r.log.some((l) => l.includes('giving up on')), r.log.join(' | '));
});

test('a click that found nothing to press is said out loud, not repeated in silence', () => {
    const r = stuckDriver(['####', '#@$#', '####'],
        { opts: { facing: Math.PI / 2 }, click: () => false });
    r.tick(0);
    r.tick(100);
    assert.ok(r.log.some((l) => l.includes('nothing to click')), r.log.join(' | '));
});

test('with nothing reachable it leaves instead of waiting', () => {
    // A chest walled off and no way out: there is nothing to wait for.
    const r = stuckDriver(['#####', '#@.#$', '#####']);
    r.tick(0);
    assert.strictEqual(r.left.length, 1);
    assert.ok(r.log.some((l) => l.includes('nothing left that can be reached')), r.log.join(' | '));
});

test('leaving happens once, however many ticks follow', () => {
    const r = stuckDriver(['#####', '#@.#$', '#####']);
    for (let i = 0; i < 10; i += 1) r.tick(100);
    assert.strictEqual(r.left.length, 1, 'the button is pressed once');
    assert.strictEqual(r.d.report().gaveUp, true);
});

test('progress resets the stall clock', () => {
    // Moving counts, so a long level is not mistaken for a stuck one.
    const scene = sceneOf(['######', '#@...X', '######'], { facing: Math.PI / 2 });
    let clock = 0;
    const left = [];
    const d = D.create({
        scene: () => scene,
        tap: (code) => { if (code === 'KeyW') scene.activeCamera.position.x += CELL; },
        click: () => true,
        leave: () => left.push(clock),
        now: () => clock,
        log: () => {},
        graceMs: 10,
        timeoutMs: 50,
        stallMs: 500,
    });
    for (let i = 0; i < 12; i += 1) { clock += 100; d.step(); }
    assert.strictEqual(left.length, 0, 'it was getting somewhere, so it stayed');
});

// ── Monsters ─────────────────────────────────────────────────────
// Reported from the other side of the screen: it walks up to a monster and does
// nothing. It was doing nothing because monsters were never implemented - the driver
// knew about chests and the door and no third thing.

/** Put a monster on a cell: the sprite that must be clicked, and the box that blocks. */
function withFoe(scene, r, c, { inBattle = true } = {}) {
    const x = 2 + c * CELL;
    const z = 2 + r * CELL;
    scene.meshes.push({ name: `enemy_skeleton_${Date.now()}`, position: { x, z, y: 1 },
        isVisible: inBattle });
    scene.meshes.push({ name: `enemy_collision_7_${Date.now()}`, position: { x, z, y: 1 },
        isVisible: false });
    return scene;
}

test('a monster fills its cell, the way a shut chest does', () => {
    const m = D.readMaze(withFoe(sceneOf(['#####', '#@..X', '#####', '#$###']), 1, 2));
    assert.strictEqual(m.open(1, 2), false, 'its box is what stops you');
    assert.strictEqual(m.enemies.length, 1);
    assert.deepStrictEqual(m.enemies[0].cell, [1, 2]);
});

test('a monster in the way comes before the chest and the door', () => {
    const m = D.readMaze(withFoe(sceneOf(['#####', '#@..X', '#.#$#']), 1, 2));
    const goal = D.nextGoal(m);
    assert.strictEqual(goal.kind, 'fight');
    assert.strictEqual(goal.target.isEnemy, true);
});

test('a monster that has not engaged yet is not swung at', () => {
    // The game gates its whole click handler on `inBattle`, and hides the sprite until
    // then. Clicking early lands on nothing.
    const m = D.readMaze(withFoe(sceneOf(['#####', '#@..X', '#####']), 1, 3, { inBattle: false }));
    const goal = D.nextGoal(m);
    assert.notStrictEqual(goal && goal.kind, 'fight');
});

test('a fight is clicked, not walked into', () => {
    const scene = withFoe(sceneOf(['#####', '#@..X', '#####', '#$###']), 1, 2);
    for (const x of scene.meshes) {
      if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
    }
    let clock = 0;
    const sent = [];
    const clicked = [];
    const d = D.create({
        scene: () => scene,
        tap: (code) => sent.push(code),
        click: (t) => { clicked.push(t.isEnemy ? 'foe' : 'other'); return true; },
        now: () => clock,
        log: () => {},
        graceMs: 10,
        timeoutMs: 50,
        stallMs: 60000,
    });
    d.step();
    assert.deepStrictEqual(clicked, ['foe']);
    assert.deepStrictEqual(sent, [], 'no key was pressed at it');
});

test('a fight counts as progress, so a long one is not mistaken for a hang', () => {
    // The player stands still through a fight; what changes is the monster. Counting
    // only the player's square would walk out of a level it was winning.
    const scene = withFoe(sceneOf(['#####', '#@..X', '#####', '#$###']), 1, 2);
    for (const x of scene.meshes) {
      if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
    }
    let clock = 0;
    const left = [];
    const d = D.create({
        scene: () => scene,
        tap: () => {},
        click: () => true,
        leave: () => left.push(clock),
        now: () => clock,
        log: () => {},
        graceMs: 10,
        timeoutMs: 50,
        stallMs: 400,
    });
    for (let i = 0; i < 6; i += 1) { clock += 100; d.step(); }
    assert.strictEqual(left.length, 1, 'nothing changed at all, so it does leave');

    // Now let the monster die partway through: that is a change, and it stays.
    const scene2 = withFoe(sceneOf(['#####', '#@..X', '#####', '#$###']), 1, 2);
    for (const x of scene2.meshes) {
      if (x.name.startsWith('chestCollision')) x.checkCollisions = false;
    }
    let t2 = 0;
    const left2 = [];
    let swings = 0;
    const d2 = D.create({
        scene: () => scene2,
        tap: () => {},
        click: () => {
            swings += 1;
            if (swings === 3) scene2.meshes = scene2.meshes.filter((x) => !/^enemy_/.test(x.name));
            return true;
        },
        leave: () => left2.push(t2),
        now: () => t2,
        log: () => {},
        graceMs: 10,
        timeoutMs: 50,
        stallMs: 400,
    });
    for (let i = 0; i < 5; i += 1) { t2 += 100; d2.step(); }
    assert.strictEqual(left2.length, 0, 'the monster died, so the clock reset');
});
