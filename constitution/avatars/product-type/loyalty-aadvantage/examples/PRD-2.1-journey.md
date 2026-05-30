# PRD-2.1 — User Journey Map (AAdvantage Loyalty)

## Member Lifecycle — 5 Phases

```
[Enroll] → [First Earn] → [Active Earner] → [Redemption] → [Retention / Elite]
   ↑                                                              |
   └──────────────── Win-Back Campaign ◄─────────── [Churn Risk] ┘
```

## Journey by Persona

### Casual Member (majority of base)
- **Earns:** 1-2 flights/year + credit card spend
- **Pain:** Points expire before redemption opportunity. Discovery gap: members don't know expiration date.
- **Key touchpoint:** Post-flight earning confirmation email — highest open rate in lifecycle

### Frequent Traveler
- **Earns:** 6-12 flights/year + hotel/car partners
- **Pain:** Booking complexity — wants to see points value at search time, not after selection
- **Key touchpoint:** `mobile-airfare-search-bff` + `aa-ct-mobile-booking-bff` response — points display must be real-time, not cached

### Elite Member (EXP/PLT/GLD)
- **Earns:** 25K–100K+ miles/year
- **Pain:** Status match anxiety — tracks threshold monthly; one missed flight can cost a tier
- **Key touchpoint:** `aa-ct-fly-mobile-loyalty-bff` — status progress response latency directly visible to this persona

## BFF Layer Touchpoints

| Journey Phase | BFF Service | Quality Score | Known Issue |
|--------------|-------------|---------------|-------------|
| Search + Book | `aa-ct-mobile-booking-bff` | 7.4/10 ✅ | None — highest quality BFF |
| Loyalty status | `aa-ct-fly-mobile-loyalty-bff` | 5.3/10 🟡 | No deep-dive report |
| AAdvantage data | `mobile-aadvantage-bff` | 5.6/10 🟡 | No deep-dive report |

> Full journey details in `PRD-2.1-journey-detail.md`.
