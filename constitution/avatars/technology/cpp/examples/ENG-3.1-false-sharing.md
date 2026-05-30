---
law_id: ENG-3.1
cpp_version_min: 17
cpp_version_note: "hardware_destructive_interference_size requires C++17 (<new>)."
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): False Sharing and Cache-Line Alignment (C++17)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), false sharing is a
silent performance defect: two threads writing *different* variables that
land on the same 64-byte cache line cause the CPU coherency protocol to
bounce the line between cores, serialising what should be independent writes.
**Always profile first** (`perf c2c`, VTune) before applying this pattern.

## COMPLIANT: Per-Thread Counter Padded to Cache Line

```cpp
#include <new>   // hardware_destructive_interference_size
#include <atomic>

// ✅ Each slot occupies its own 64-byte (or larger) cache line
struct alignas(std::hardware_destructive_interference_size) PaddedCounter {
    std::atomic<std::uint64_t> value{0};
};

// AA domain: per-thread fare-search hit/miss stats
std::vector<PaddedCounter> hits(std::thread::hardware_concurrency());

void record_hit(std::size_t tid) {
    hits[tid].value.fetch_add(1, std::memory_order_relaxed);  // ✅ no sharing
}
std::uint64_t total() {
    std::uint64_t n = 0;
    for (auto& c : hits) n += c.value.load(std::memory_order_relaxed);
    return n;
}
```

## NON-COMPLIANT: Adjacent Counters Share a Cache Line

```cpp
struct Stats {
    std::atomic<uint64_t> hits{0};    // ❌ same 64-byte line as misses
    std::atomic<uint64_t> misses{0};  // ❌ writer of misses invalidates hits' line
};
Stats stats;  // ❌ both threads bounce the same cache line
```

## Edge Cases & Warnings

| Pitfall | Guidance |
|---|---|
| Magic `64` instead of `hardware_destructive_interference_size` | Cache lines vary by CPU family; use the C++17 constant — it may be 128 on future ARMs |
| Applying without profiling | Padding wastes memory bandwidth on cold paths; always measure with `perf c2c` or VTune before adding |
| Over-padding read-only data | Use `hardware_constructive_interference_size` to pack read-only fields together for prefetcher benefit |
| MPMC queue node padding | Each node must be individually aligned — an array of unpadded nodes defeats the purpose |
