---
law_id: ENG-6.1
cpp_version_min: 11
avatar: cpp
---

# ENG-6.1: volatile vs std::atomic — C++ Examples

## The Rule

`volatile` in C++ does NOT provide thread safety, atomicity, or memory ordering. For inter-thread communication, use `std::atomic`. This is the **#1 Java→C++ concurrency trap** — Java's `volatile` provides happens-before guarantees; C++'s `volatile` does not.

## When to Use

Any code doing inter-thread communication. **Java developers:** Replace your mental model entirely. C++ `volatile` is exclusively for memory-mapped I/O (hardware registers). For everything Java uses `volatile` for, C++ uses `std::atomic`.

| Java | C++ | Trap |
|------|-----|------|
| `volatile int count;` — thread-safe | `volatile int count;` — NOT thread-safe | Data race = UB |
| `volatile` provides happens-before | `volatile` prevents compiler reordering only — no CPU memory ordering | Broken on multi-core |
| `synchronized` block | `std::mutex` + `std::lock_guard` | Two objects, not one keyword |

## COMPLIANT: std::atomic for Thread Communication

```cpp
#include <atomic>
#include <mutex>

// why: std::atomic provides the memory ordering that Java volatile provides
std::atomic<bool> ready{false};
std::atomic<int> flight_count{0};

void producer() {
    prepare_data();
    ready.store(true, std::memory_order_release);  // why: release = "publish" to other threads
}

void consumer() {
    while (!ready.load(std::memory_order_acquire))  // why: acquire = "see" producer's writes
        ;
    use_data();  // safe — acquire/release guarantees data is visible
}

// why: mutex + lock_guard = Java's synchronized block
std::mutex mtx;
void updateShared() {
    std::lock_guard lock(mtx);  // why: RAII — automatically unlocks at scope exit
    shared_data++;              // safe — mutex provides exclusive access
}
```

## NON-COMPLIANT: volatile for Synchronization

```cpp
volatile bool ready = false;     // ❌ NOT thread-safe in C++
volatile int flight_count = 0;   // ❌ Increments are NOT atomic

void producer() {
    prepare_data();
    ready = true;    // ❌ No memory ordering — consumer may see ready=true but stale data
}

void consumer() {
    while (!ready);  // ❌ Data race — undefined behavior
    use_data();      // ❌ May see partially-written data
}
```

## Edge Cases & Warnings

- **volatile is only for hardware:** The only valid C++ use of `volatile` is memory-mapped I/O registers in embedded/driver code where reads and writes must not be optimized away.
- **Atomic increment ≠ volatile increment:** `volatile int x; x++;` is NOT atomic — it's a load, increment, store sequence that races. Use `std::atomic<int>` with `fetch_add`.
- **Java `synchronized` → `std::lock_guard`:** Java's `synchronized(obj)` locks on any object. C++ requires a dedicated `std::mutex` — you cannot lock on an arbitrary object.
- **`std::atomic<bool>` vs `std::atomic_flag`:** For simple flags, `std::atomic<bool>` is fine. `std::atomic_flag` is lock-free guaranteed but has a more limited API.
