---
cpp_version_min: 11
cpp_version_note: >-
  Advanced matcher and mock patterns require C++11 lambdas.
avatar: cpp
---

# C++ Avatar Reference: GoogleTest Advanced Patterns

---

## GTest Template Test Helper Pattern

> Per [ENG-4.1](laws/engineering/eng-4-testing.md): template helpers let one
> TDD cycle cover multiple type instantiations without duplicating test logic.
> Sourced from Folly's `ArenaSmartPtrTest.cpp` and `ConvTest.cpp`.

### Pattern: Template Helper → Called from TEST()

Write a `template<class Allocator>` helper function containing the assertions,
then call it from one or more `TEST()` macros with concrete types:

```cpp
// ArenaSmartPtrTest.cpp pattern
template <typename Allocator>
void testUniquePtrLifecycle(Allocator& allocator) {
    global_counter counter;
    EXPECT_EQ(counter.count(), 0);

    auto p = folly::allocate_unique<Foo>(allocator, counter);
    EXPECT_EQ(counter.count(), 1);

    p.reset();
    EXPECT_EQ(counter.count(), 0);
}

// One test per allocator type — each gets its own failure message
TEST(ArenaSmartPtr, UniquePtrSysArena) {
    SysArena arena;
    SysArenaAllocator<Foo> alloc(arena);
    testUniquePtrLifecycle(alloc);
}

TEST(ArenaSmartPtr, UniquePtrPoolAlloc) {
    PoolAlloc alloc;
    testUniquePtrLifecycle(alloc);
}
```

### AA Aviation Application: Testing Multiple CG Calculators

The same pattern applies when testing multiple implementations of a domain
interface (e.g., two ZFW calculators — legacy and new):

```cpp
template <class Calculator>
void verifyZfwCalculation(Calculator& calc) {
    EXPECT_NEAR(calc.computeZfw({.cargo=15000, .pax=42}), 87500.0, 0.5);
    EXPECT_THROW(calc.computeZfw({.cargo=-1}), CInvalidWeightException);
}

TEST(ZfwCalculator, LegacyImpl)  { LegacyZfwCalc c; verifyZfwCalculation(c); }
TEST(ZfwCalculator, ModernImpl)  { ModernZfwCalc c; verifyZfwCalculation(c); }
```

---

---

## GTest Fixture Deep Dive

> Per [ENG-4.1](laws/engineering/eng-4-testing.md) and
> [ENG-4.2](laws/engineering/eng-4-testing.md): fixtures express shared
> preconditions — not shared implementation. Sourced from Folly's
> `ChronoTest.cpp`, `DemangleTest.cpp`, and `ConcurrentSkipListTest.cpp`.

### Minimal Fixture (No State)

Folly frequently uses an empty fixture class just to group related `TEST_F`
cases under a common name — no `SetUp`/`TearDown` needed:

```cpp
// ChronoTest.cpp / DemangleTest.cpp pattern
class FlightTimerTest : public testing::Test {};

TEST_F(FlightTimerTest, RoundToNearestMinute) {
    using namespace std::chrono;
    auto t = minutes(6) + seconds(45);
    EXPECT_EQ(round<minutes>(t), minutes(7));
}
```

### Fixture with SetUp and TearDown

Use `SetUp()` for construction and `TearDown()` for cleanup that must happen
even if assertions fail (avoids resource leaks in test infrastructure):

```cpp
class FlightServiceTest : public testing::Test {
protected:
    void SetUp() override {
        db_ = std::make_unique<InMemoryDb>();
        service_ = std::make_unique<FlightService>(*db_);
    }

    void TearDown() override {
        service_.reset();
        db_.reset();
    }

    std::unique_ptr<InMemoryDb> db_;
    std::unique_ptr<FlightService> service_;
};

TEST_F(FlightServiceTest, LoadFlightReturnsDomainObject) {
    auto flight = service_->load(FlightId{"AA100"});
    EXPECT_EQ(flight.number(), "AA100");
}
```

### RAII Alternative to TearDown

For RAII resources, prefer data members with destructors over `TearDown()` —
the destructor runs unconditionally, and the code is self-documenting:

```cpp
class ScopedFileTest : public testing::Test {
protected:
    TempFile tmp_{"test_output.dat"};  // RAII: deleted in destructor
};
```

---

---

## GTest Concurrency Testing

> Per [ENG-4.1](laws/engineering/eng-4-testing.md): concurrent behavior is
> observable behavior — it requires its own TDD cycle. Sourced from Folly's
> `CancellationTokenTest.cpp` and `ConcurrentLazyTest.cpp`.

### Basic Thread + Join Pattern

Folly's `CancellationTokenTest::MultiThreadedPolling` spawns a thread, triggers
a condition on the main thread, then joins — the join serves as the implicit
assertion that the thread terminates:

```cpp
TEST(CancellationTokenTest, MultiThreadedPolling) {
    CancellationSource src;

    std::thread t1{[t = src.getToken()] {
        while (!t.isCancellationRequested()) {
            std::this_thread::yield();
        }
    }};

    src.requestCancellation();
    t1.join();  // test would hang (and time out) if cancellation didn't fire
}
```

### Atomic Counter Pattern

Use `std::atomic_int` for counters shared across threads — avoids data races
and ensures the assertion on the main thread sees the correct count:

```cpp
TEST(LazyInit, ComputedExactlyOnceUnderConcurrency) {
    std::atomic_int computeCount = 0;

    auto val = concurrent_lazy([&]() -> int {
        ++computeCount;
        return 42;
    });

    std::vector<std::thread> readers;
    for (int i = 0; i < 10; ++i) {
        readers.emplace_back([&] { val(); });
    }
    for (auto& t : readers) { t.join(); }

    EXPECT_EQ(val(), 42);
    EXPECT_EQ(computeCount.load(), 1);  // computed exactly once
}
```

### IOC_ALP Windows Threading Note

IOC_ALP uses `CRITICAL_SECTION` / Windows threads — not `std::thread`.
When writing new GTest tests for IOC_ALP code, simulate thread interactions
via `CRITICAL_SECTION` guards in the test setup, or use the `std::thread`
pattern above for any **new** code written to modern C++ standards.

For `CRITICAL_SECTION` RAII wrapper patterns that are GTest-fixture compatible,
see [Brownfield Configuration](ref-brownfield-config.md) § Windows Threading.

---
## See Also

- [Build & Toolchain](ref-build-toolchain.md)
- [Infrastructure & Operations](ref-infrastructure.md)


---

## See Also

- [CI Quality Toolchain Policy](ref-testing-ci-policy.md)
- [GoogleTest Core Patterns](ref-testing-gtest-core.md)
