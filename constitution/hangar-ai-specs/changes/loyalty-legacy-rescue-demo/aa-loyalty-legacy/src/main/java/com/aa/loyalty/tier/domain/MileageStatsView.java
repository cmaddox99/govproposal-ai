package com.aa.loyalty.tier.domain;

/**
 * ENG-2.4 — Immutable view object: tier context's snapshot of mileage data.
 * ENG-3.2 — Immutability: all fields are final.
 * Prevents tier context from holding a reference to MileageAccount entity.
 */
public final class MileageStatsView {
    private final long eliteQualifyingMiles;
    private final int eliteQualifyingSegments;
    private final long totalMiles;

    public MileageStatsView(long eliteQualifyingMiles, int eliteQualifyingSegments, long totalMiles) {
        this.eliteQualifyingMiles = eliteQualifyingMiles;
        this.eliteQualifyingSegments = eliteQualifyingSegments;
        this.totalMiles = totalMiles;
    }

    public static MileageStatsView zero() {
        return new MileageStatsView(0L, 0, 0L);
    }

    public long getEliteQualifyingMiles() { return eliteQualifyingMiles; }
    public int getEliteQualifyingSegments() { return eliteQualifyingSegments; }
    public long getTotalMiles() { return totalMiles; }
}
