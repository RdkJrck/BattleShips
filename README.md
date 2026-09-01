# BattleShips:OverEngineered

Goal is overengineer battleships as much as possible.
Let implement it step by step.
No AI slop, just artisian handcrafted hell of code.


# Core logic:
Fog of War (Anti-Cheat): The server sends the bot only a map segment corresponding to the spot range of its surviving ships. Any attempt to interact with an invisible target is immediately and mercilessly dropped at the TCP layer.

Transactional Economy: Strict turn-based rate limiting is introduced. Every incoming binary command (move/attack) must pass a Resources budget validation before the server even allows it to reach the game core.

Ship Asymmetry (OOP Magic):

Light Ships: High mobility, low damage and firing range, medium spot range.

Heavy Ships: Slow and expensive vector movement, extreme firing and spotting range, massive damage.

Area of Effect (AoE via C-Extensions): A heavy ship's shot that damages multiple tiles at once (e.g., a 3x3 grid) will be offloaded from Python to a C library via ctypes. It will execute an instant bitmask operation over the memory space and return only the affected targets.

Vector Movement & Collisions: Ships are no longer static. The backend must trace the movement path point-by-point and verify collisions with the map boundaries and other vessels (a perfect use case for lightning-fast Bloom Filters).

# Impementation Plan: 
Low-Level I/O & Memory Management

[ ] Raw TCP Stream: Receiving data via recv(1) and manually stitching fragmented packets.

[ ] Ring Buffer: Fixed memory allocation with rotating manual read/write pointers.

[ ] Zero-Copy Manipulation: Handling network bytes exclusively via memoryview to eliminate dynamic allocation overhead.

[ ] Binary Serialization: Custom protocol handled strictly by the struct module (no strings or JSON).

Architecture & Security

[ ] Strict State Machine: Exact control over connection transitions (Handshake -> Cipher -> Battle -> Terminate).

[ ] Custom "Dirty" Cryptography: Bitwise operations, rotating XOR keys, and primitive Diffie-Hellman key exchange.

[ ] Application-Level Network Control: Custom ping/pong heartbeats and application-level ACK confirmations (Sliding Window).

[ ] Merkle Trees: Anti-cheat cryptographic hash verification of the client's and server's game matrices.

Concurrency & Performance

[ ] Custom Event Loop (Reactor): Non-blocking I/O loop built entirely on select/epoll and yield generators (boycotting asyncio).

[ ] Multiprocessing with IPC: Bypassing the GIL by spawning processes that communicate via shared memory (mmap) or Pipes.

[ ] Object Pooling: Manual recycling of game instances to limit Garbage Collector interventions.

[ ] Bloom Filters: Probabilistic data structures for lightning-fast O(1) lookups of your shooting history.

Absolute Over-Engineering (Python Magic)

[ ] Event Sourcing & WAL (Write-Ahead Logging): The game doesn't save the final state; it calculates the matrix in real-time by replaying an append-only binary event log.

[ ] C-Extensions (ctypes): Rewriting the heaviest computational or cryptographic logic into a compiled C library and calling it from Python.

[ ] Python Data Model: Deploying descriptors (__get__, __set__) for low-level matrix validation and metaclasses for dynamic ship generation.

[ ] Hot-Reloading (importlib): Modifying game rules and weapon stats at runtime without dropping active client connections.

[ ] AST Sandbox: Safe compilation of client macros (mini-scripts) by parsing them into an Abstract Syntax Tree and filtering out malicious commands.

[ ] Python Datový Model: Nasazení descriptorů (__get__, __set__) pro nízkoúrovňovou validaci matice a metatříd pro generování lodí.

[ ] Hot-Reloading (importlib): Úprava pravidel a statů zbraní za plného běhu serveru bez rozpojení klientů.

[ ] AST Sandbox: Bezpečná kompilace klientských maker (mini-skriptů) jejich rozsekáním na abstraktní syntaktický strom.

