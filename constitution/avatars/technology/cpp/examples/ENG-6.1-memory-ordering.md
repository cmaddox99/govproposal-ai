---
law_id: ENG-6.1
cpp_version_min: 11
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `std::memory_order` (C++11)

Per [ENG-6.1](laws/engineering/eng-6-security.md), every `std::atomic` operation
must specify the weakest ordering that preserves correctness.

## Memory Order Reference

| Order | Guarantees | Typical use |
|-------|-----------|-------------|
| `relaxed` | Atomicity only — no ordering | Independent counters |
| `consume` | Dependent-load ordering (avoid — use `acquire`) | — |
| `acquire` | No reads/writes reorder before this load | Flag read, lock acquire |
| `release` | No reads/writes reorder after this store | Flag publish, lock release |
| `acq_rel` | acquire + release on one RMW | `fetch_sub` for ref-count |
| `seq_cst` | Total order across all threads | Default; always safe |

## COMPLIANT: Acquire/Release Producer-Consumer

```cpp
std::atomic<bool> ready{false};
FlightData payload{};

// Producer
void produce(FlightData d) {
    payload = d;
    ready.store(true, std::memory_order_release); // ✅ release: payload visible
}

// Consumer
void consume() {
    while (!ready.load(std::memory_order_acquire)) // ✅ acquire: happens-before
        std::this_thread::yield();                 //    with producer's release
    process(payload);  // safe: all writes before release are visible
}
```

`release` synchronises-with `acquire` — establishes **happens-before**: every
write before the release store is visible after the acquire load.

## COMPLIANT: Relaxed for Independent Counter

```cpp
std::atomic<uint64_t> booking_attempts{0};

void record_attempt() {
    booking_attempts.fetch_add(1, std::memory_order_relaxed); // ✅ no sync needed
}
```

## COMPLIANT: `acq_rel` for Read-Modify-Write

```cpp
std::atomic<int> ref_count{1};

void release_ref() {
    if (ref_count.fetch_sub(1, std::memory_order_acq_rel) == 1)
        destroy(); // ✅ acq_rel: last decrement synchronises-with all prior incs
}
```

## NON-COMPLIANT: Relaxed Load of Dependent Data

```cpp
// ❌ relaxed load — NO happens-before with producer's store
// payload may be stale or partially written on ARM/POWER
while (!ready.load(std::memory_order_relaxed)) {}
process(payload); // ❌ data race — undefined behaviour
```

## Edge Cases

### `seq_cst` Cost

`seq_cst` is the default. On ARM it emits `dmb ish` (full barrier) on every
store. Profile before assuming acceptable on paths >100k ops/s.

### Release Sequence

A chain of `fetch_add` RMWs (even `relaxed`) between a `release` store and
a final `acquire` load still establishes happens-before through the atomic
object. The synchronisation is on the atomic, not on each intervening RMW.
