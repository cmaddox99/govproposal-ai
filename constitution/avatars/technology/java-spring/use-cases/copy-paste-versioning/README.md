# Use Case: Copy-Paste Versioning → Abstract Base Class

**Avatar:** avatar-java-spring  
**Laws:** ENG-3.1 (Complexity Limits), ENG-2.1 (DDD / Single Responsibility)  
**AA Evidence:** mobile-travelhub-bff — `TravelHubResponseBuilderV2/V3/V4` (1,763 LOC combined)  
**Risk level:** High — V2/V3/V4 clones carry the same bugs. A fix in V2 never reaches V3/V4.

## Context

AA's BFF fleet handles API versioning by cloning entire classes:

| Pattern | Repos Affected | LOC Duplicated |
|---------|---------------|----------------|
| V2/V3/V4 full-class clones | travelhub-bff (3 builders), iu-bff (2 builders) | 1,763 + 600 LOC |
| Near-identical engine pairs | fly-checkin-bff (`WellnessCheckinEngine` ≅ `WellnessCheckinRulesEngine`) | ~530 LOC |
| Side-by-side analytics builders | mobile-iu-bff | ~600 LOC (7 duplicate methods) |

**Consequence:** The thread-safety critical bug (mutable `@Service` singleton) exists independently in V2, V3, and V4 because each is a separate class. Fixing V2 leaves V3 and V4 broken.

## The Migration

```java
// ❌ Current — 3 clones, each ~655 LOC
@Service class TravelHubResponseBuilderV2 { /* 655 LOC */ }
@Service class TravelHubResponseBuilderV3 { /* 653 LOC — 98% identical to V2 */ }
@Service class TravelHubResponseBuilderV4 { /* 612 LOC — 93% identical to V2 */ }

// ✅ Abstract base + version-specific overrides (~660 LOC total, 62% reduction)
abstract class TravelHubResponseBuilder {
    // Shared logic — fix once, applies to all versions
    protected abstract List<TravelSegment> buildVersionSpecificSegments(TravelData data);

    public final TravelHubResponse build(TravelData data) {
        // All @Service singleton state eliminated — method-scoped only
        var segments = buildVersionSpecificSegments(data);
        return TravelHubResponse.of(segments);
    }
}

@Service class TravelHubResponseBuilderV2 extends TravelHubResponseBuilder {
    @Override
    protected List<TravelSegment> buildVersionSpecificSegments(TravelData data) {
        // Only the 2% that actually differs between V2 and V3
    }
}
```

## Thread Safety Fix Bundled In

The abstract base class migration is the natural time to eliminate mutable instance fields:

```java
// Thread-safe by design — no instance state, all state is method-scoped
abstract class TravelHubResponseBuilder {
    public final TravelHubResponse build(TravelData data) {
        List<TravelSegment> segments = new ArrayList<>(); // local, not instance
        // ...
    }
}
```

## ENG-11.1 Gate

Create `hangar-ai-specs/PROPOSAL.md` before starting this refactor. The migration touches 3 production services; a PROPOSAL.md ensures the team reviews scope and rollback plan before any code changes.
