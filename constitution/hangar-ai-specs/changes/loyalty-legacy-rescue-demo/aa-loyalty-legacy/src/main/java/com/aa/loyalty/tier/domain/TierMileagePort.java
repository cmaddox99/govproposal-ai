package com.aa.loyalty.tier.domain;

/**
 * ENG-2.4 — ACL port: tier context's read-only view of mileage stats.
 * TierService depends on this interface, not on MileageRepository or MileageAccount.
 */
public interface TierMileagePort {
    MileageStatsView getMileageStats(String memberNumber);
}
