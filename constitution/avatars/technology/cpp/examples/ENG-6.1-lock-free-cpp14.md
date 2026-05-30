---
law_id: ENG-6.1
cpp_version_min: 11
cpp_version_note: >-
  Lock-free patterns for C++11/14: ABA mitigation and SPSC ring buffer
  using boostorg/lockfree. std::hazard_pointer is C++23 — unavailable.
avatar: cpp
rag_exclude: true  # placeholder — content pending CBF adoption; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Lock-Free Patterns — C++11/14

**Avatar:** C++ (Transitional C++11/14 — CWR / IOC_ALP)
**Pattern:** SPSC ring buffer + ABA-safe tagged pointer

## ⚠️ Performance Warning — Read Before Using Lock-Free

**Lock-free is not automatically faster than mutex-protected code.**
Cache-line contention between producer and consumer cores can make a
lock-free queue *slower* than `std::mutex` + `std::queue`. Always profile
with realistic workloads before replacing a mutex with lock-free structures.
Lock-free structures are appropriate for:
- Hard real-time threads where mutex blocking is unacceptable (e.g. audio).
- Provably single-producer / single-consumer hot paths (SPSC only).

For application-layer code (CWR flight query processing, IOC_ALP reservation
dispatch), prefer `std::mutex` + `std::queue` until profiling proves a
bottleneck.

## Context

Per [ENG-6.1](laws/engineering/eng-6-security.md), shared data accessed from
multiple threads must be protected. Lock-free structures use atomic
compare-exchange loops instead of mutexes — but introduce their own hazards:
the **ABA problem** and undefined behavior from misaligned atomic access.

[boostorg/lockfree](https://github.com/boostorg/lockfree) (Boost Software
License, Tim Blechmann) provides production-quality lock-free queues and
stacks for C++11/14. `std::hazard_pointer` (C++23) and `std::atomic_ref`
without alignment guarantees are not available on the target toolchains.

## COMPLIANT — SPSC Queue (boost::lockfree::spsc_queue)

```cpp
// flight_event_pipe.cpp  (CWR — C++11/14)
// Single producer thread (flight data feed) → single consumer thread (display).
#include <boost/lockfree/spsc_queue.hpp>

struct FlightEvent { std::string flight_id; int status_code; };

// Capacity must be a power of two; fixed at compile time.
// SPSC: exactly ONE producer and ONE consumer — violating this is UB.
boost::lockfree::spsc_queue<FlightEvent,
    boost::lockfree::capacity<1024>> event_pipe;

// Producer thread:
void produce_event(const FlightEvent& ev)
{
    // push() returns false if full — caller must handle backpressure.
    if (!event_pipe.push(ev)) {
        // queue full — drop or log; never block in producer
        log_dropped_event(ev);
    }
}

// Consumer thread:
void drain_events()
{
    FlightEvent ev;
    while (event_pipe.pop(ev)) {
        process_flight_event(ev);
    }
}
```

**Why `spsc_queue`:** The SPSC constraint (one producer, one consumer) allows
a wait-free implementation using a head/tail index pair without any CAS loop.
Performance is predictable. Violating the SPSC contract — e.g. two threads
calling `push()` concurrently — is undefined behavior.

## COMPLIANT — ABA Mitigation via Version Counter

When implementing a custom lock-free stack or freelist for C++11/14, pack a
version counter into the same atomic word to defeat the ABA problem:

```cpp
#include <atomic>
#include <cstdint>

// Tagged pointer: upper 32 bits = version counter, lower 32 bits = index.
// Fits in a single std::atomic<uint64_t> — always lock-free on x86-64/ARM64.
struct alignas(8) TaggedIndex {
    uint32_t version;  // increment on every pop to defeat ABA
    uint32_t index;    // index into node pool
};

static_assert(sizeof(TaggedIndex) == sizeof(uint64_t), "packing assumption");

std::atomic<uint64_t> head{0};  // packed TaggedIndex

bool try_pop(uint32_t& out_index)
{
    uint64_t old_raw = head.load(std::memory_order_acquire);
    while (true) {
        TaggedIndex old;
        std::memcpy(&old, &old_raw, sizeof(old));
        if (old.index == UINT32_MAX) return false;  // empty

        TaggedIndex next{old.version + 1, pool_next[old.index]};
        uint64_t next_raw;
        std::memcpy(&next_raw, &next, sizeof(next_raw));

        if (head.compare_exchange_weak(old_raw, next_raw,
                std::memory_order_release, std::memory_order_acquire)) {
            out_index = old.index;
            return true;
        }
        // old_raw updated by CAS failure — retry with fresh value
    }
}
```

**Why version counter:** Without the version, thread A could pop node X,
thread B pop and re-push X, and thread A's CAS would spuriously succeed
(seeing the same pointer value). The version increment makes each push of X
distinguishable, so A's CAS correctly fails.

## NON-COMPLIANT

```cpp
// WRONG 1: std::hazard_pointer — C++23, unavailable on C++11/14 toolchains.
// Do not forward-declare or polyfill — the memory model semantics require
// compiler and hardware support that cannot be emulated in C++11.
#include <hazard_pointer>  // ← does not exist in C++11/14 standard library
auto hp = std::make_hazard_pointer(std::default_delete<Node>{});

// WRONG 2: std::atomic_ref<T> without alignment guarantee.
// std::atomic_ref requires T to be aligned to alignof(T).
// Misaligned access is UB on ARMv7 and some MSVC configurations.
struct Misaligned { char pad; int value; };  // value not 4-byte aligned
Misaligned buf[4];
std::atomic_ref<int> ref(buf[0].value);  // UB: buf[0].value may be misaligned

// WRONG 3: multi-producer use of spsc_queue.
// spsc_queue is only safe with exactly one producer and one consumer.
// Two threads calling push() concurrently is undefined behavior.
void worker_a() { event_pipe.push({...}); }
void worker_b() { event_pipe.push({...}); }  // ← concurrent push: UB
```

## Edge Cases & Warnings

- **Cache-line contention — false sharing:** The head and tail indices of a
  queue should occupy separate cache lines. `boost::lockfree::spsc_queue`
  handles this internally with `alignas(64)`. If you implement your own
  queue, place producer state and consumer state in separate `alignas(64)`
  structs — otherwise both cores invalidate the same cache line on every
  operation, destroying throughput.

- **`spsc_queue` capacity is fixed at compile time:** The queue never
  allocates after construction. If the producer outpaces the consumer,
  `push()` returns `false`. Size the capacity to absorb the worst-case burst
  — typically 2× the expected burst size rounded up to the next power of two.

- **`compare_exchange_weak` retry loop:** `compare_exchange_weak` may fail
  spuriously on some architectures (LL/SC). The CAS updates `old_raw` on
  failure, so the retry immediately uses the latest value — this is correct
  and expected.

- **`alignas(8)` on `TaggedIndex`:** Without the alignment attribute,
  `std::memcpy` round-trips through an unaligned address, which is legal in
  C++ but may be slow. With `alignas(8)` the compiler uses a single 64-bit
  load/store. Verify with `-fsanitize=address,undefined` in debug builds.

Per [ENG-6.1](laws/engineering/eng-6-security.md): lock-free code requires
ABA mitigation, alignment guarantees, and strict SPSC/MPMC contract adherence.
Profile before adopting — mutex-protected queues are correct by default.
