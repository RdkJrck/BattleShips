# BattleShips: OverEngineered

Overengineer Battleships on purpose. Build it one layer at a time.
No AI slop. Handcrafted code, each layer there so you learn the tool under it.

The point is to practice Python and C on one small game. A playable board comes before the circus.

## Game rules

The server owns the board. The client sees only what its ships can see, and every command spends a budget.

- **Scale & MGRS.** One grid tile is `10 m × 10 m`. The UI displays and accepts MGRS coordinates, and every firing solution reports **azimuth** (0–360°) and **distance** in meters.
- **Terrain & elevation.** The map has a terrain layer (`0` = sea level, `> 0` = island height). Light ships fire on a flat trajectory and cannot shoot over hills; heavy ships have a higher firing arc.
- **Hull damage & sinking.** On the board, `+ship_id` marks an intact hull segment and `-ship_id` marks a damaged segment of that ship. A ship's mobility scales down as it takes hits, and if more than **50%** of its hull segments are hit, the entire ship sinks.
- **Fog of war.** The server sends the bot only the map segment inside the spot range of its surviving ships. A command aimed at an invisible target is dropped on the TCP connection before it reaches the game.
- **Turn budget.** The game is strictly turn-based. Each binary command (move or attack) must pass a resource check before the server lets it into the game core.
- **Ship tiers (Scout, Frigate, Destroyer).** Scout: small (`1×2`), fast, long spot range, single-tile shot. Frigate: medium (`2×3`), medium blast radius. Destroyer: heavy (`3×5`), slow, expensive movement, large Euclidean blast radius.
- **Area of effect.** A heavy shot hits all tiles inside its Euclidean blast radius. Later, that scan runs in C through `ctypes` over the board buffer.
- **Vector movement.** Ships move. The server walks the path point by point and rejects a move that leaves the map, hits an island, or collides with another ship.

## Testing

A layer is done when `pytest` is green, not when the code ran once by hand.

- Test pure logic without a socket: packets, ship stats, fog, budget, movement.
- A malformed packet raises a Python exception. An illegal move does too.
- C returns an integer code. Python turns that code into the exception. The C function does not abort the process.

## Build order

Each layer assumes the previous one works. Do not start a layer until the previous one is tested.

### 0. Bytes on the wire

- [ ] Binary protocol: `struct` only. No strings, no JSON. One packet you can encode and decode in a test.
- [ ] Tests for that codec: round-trip, truncated buffer, unknown message type.
- [ ] A malformed packet raises. It is not skipped.
- [ ] Raw TCP stream: `recv` in small pieces and stitch fragmented packets by hand.
- [ ] Ring buffer: fixed memory, rotating read and write pointers.
- [ ] Zero-copy: once the copying version works, keep the bytes in a `memoryview`.
- [ ] C library: one header, one `.c` file, a build command, called through `ctypes`. The first function is a checksum over the packet bytes. It returns `0` or an error code.

### 1. A game that can take a turn

- [ ] State machine: Handshake → Cipher → Battle → Terminate. No other transitions.
- [ ] Ships as objects: light and heavy, with the stats from the rules above.
- [ ] One legal turn: place, move, or fire, then the other side.
- [ ] An illegal turn raises. Tests cover one legal turn and one rejected turn.

### 2. Rules that make it Battleships

- [ ] Fog of war: responses contain only tiles inside the spot range.
- [ ] Turn budget: reject a command that does not fit the remaining resources.
- [ ] Vector movement: walk the path, stop on the map edge or another ship.
- [ ] Tests for fog, an over-budget command, a path that leaves the map, and a path that hits a ship.

### 3. Speed where it matters

- [ ] Same C library, second function: which tiles sit in a 3×3. Python maps the return code to hits or an exception.
- [ ] Tests call that function with a known board.
- [ ] Bloom filter: O(1) check of whether a tile was already fired on. Test a hit, a miss, and a false positive.

### 4. Later

These stay in the plan. They do not block the first playable game.

- [ ] Application-level ping/pong and ACK with a sliding window.
- [ ] Custom crypto: rotating XOR and a small Diffie–Hellman exchange.
- [ ] Merkle tree over the client and server boards, so the two matrices can be compared.
- [ ] Custom event loop on `select` / `epoll` and generators. No `asyncio`.
- [ ] Multiprocessing and IPC (`mmap` or pipes) to step around the GIL.
- [ ] Object pool for game instances, so the garbage collector stays quiet.
- [ ] Event sourcing: append-only binary log, board rebuilt by replay.
- [ ] Descriptors (`__get__`, `__set__`) for board checks, metaclasses for ship types.
- [ ] Hot reload (`importlib`): change weapon stats without dropping clients.
- [ ] AST sandbox: client macros parsed to a tree, unsafe nodes rejected.
