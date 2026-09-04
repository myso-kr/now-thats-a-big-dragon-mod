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

test('the nearest chest is taken first, not the first one found', () => {
  // The standing cells have to differ, not the chests: beside is what gets walked to,
  // so two chests either side at the same remove is a tie, not a nearest.
  const m = D.readMaze(sceneOf(['########', '#$..@.$#', '########']));
  const goal = D.nextGoal(m);
  assert.deepStrictEqual(goal.target.cell, [1, 6], 'one step to its side, against two');
  assert.deepStrictEqual(goal.cell, [1, 5]);
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
    settleMs: 100,
  });
  return { d, sent, scene, tick: (ms = 100) => { clock += ms; return d.step(); } };
}

test('one action per tap, and nothing while the last is settling', () => {
  const r = driver(SIMPLE);
  r.tick(0);
  assert.strictEqual(r.sent.length, 1, 'one key');
  r.tick(10);
  assert.strictEqual(r.sent.length, 1, 'still settling, so still one');
  r.tick(200);
  assert.strictEqual(r.sent.length, 2);
});

test('with no live scene it drives nothing and says so', () => {
  const d = D.create({ scene: () => null, tap: () => {}, now: () => 0, log: () => {} });
  assert.strictEqual(d.step(), false);
});

test('a move that changed nothing marks the cell walled, and it sticks', () => {
  // The only collision signal there is: the grid comes from meshes and can be wrong.
  // Facing east down a corridor, so the very first action is a move rather than a turn,
  // and the fake camera never moves because nothing here moves it.
  const warned = [];
  const scene = sceneOf(['####', '#@.X', '####'], { facing: Math.PI / 2 });
  let clock = 0;
  const d = D.create({
    scene: () => scene,
    tap: () => {},
    now: () => clock,
    log: (tag, text, level) => warned.push(level),
    settleMs: 100,
  });
  d.step();
  clock += 200;
  d.step();
  assert.ok(warned.includes('warn'), 'and it is said out loud');
  assert.deepStrictEqual(d.report().walled, ['1,2']);

  // It has to survive the maze being rebuilt from the scene, which happens every step.
  clock += 200;
  d.step();
  assert.deepStrictEqual(d.report().walled, ['1,2'], 'remembered, not re-discovered');
});
