---
law_id: ENG-6.7
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 aggregate designated initializers for audit record construction. Transitional teams: use explicit struct constructor with all parameters.
avatar: cpp
---

# [ENG-6.7](laws/engineering/eng-6-security.md): Audit Trail — C++ Examples

## The Rule

Every domain event is an audit record — **no silent mutations**. Every state change must emit a timestamped event with actor identity, enabling full reconstruction of what happened, when, and by whom.

## When to Use

Apply to **every aggregate save, update, or delete** — not just "important" ones. In aviation, this is critical for **SOX compliance** (fare changes, revenue-impacting operations) and **FAA recordkeeping** (crew assignments, maintenance sign-offs).

## COMPLIANT: Domain Event Emission for Audit

```cpp
class BookingService {
public:
    Booking confirm_booking(BookingId id) {
        auto booking = repository_.find(id);
        booking.confirm();
        repository_.save(booking);

        // why: every mutation emits an auditable event with who/what/when
        event_publisher_.publish(BookingConfirmed{
            .booking_id = id,
            .timestamp  = Clock::now(),       // why: wall-clock for audit trail
            .actor      = current_user(),     // why: identity required for SOX compliance
            .fare_total = booking.fare()      // why: fare changes are revenue-impacting — SOX auditable
        });

        return booking;
    }

private:
    BookingRepository& repository_;
    EventPublisher& event_publisher_;
};
```

## NON-COMPLIANT: Silent State Mutation

```cpp
void confirm_booking(BookingId id) {
    auto booking = repository_.find(id);
    booking.confirm();
    repository_.save(booking);
    // ❌ No event, no log, no audit record
    // ❌ Impossible to determine who changed what and when
    // ❌ SOX violation if fare was modified during confirmation
}
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| Batch operations | Each individual mutation in a batch must emit its own event — don't aggregate into one "batch updated" event. |
| Event publishing failure | Use transactional outbox pattern: save event to DB in same transaction as the mutation, then publish asynchronously. Never lose an audit record. |
| Clock skew | Use monotonic IDs (UUID v7, ULID) in addition to timestamps for ordering. Wall clocks can drift across nodes. |
| Read-only operations | Reads of sensitive data (PII, fare rules) should also be logged per ENG-6.4 — "who viewed what" is auditable too. |
