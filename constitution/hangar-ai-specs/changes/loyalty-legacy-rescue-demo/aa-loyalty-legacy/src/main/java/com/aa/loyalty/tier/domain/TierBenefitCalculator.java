package com.aa.loyalty.tier.domain;

import org.springframework.stereotype.Component;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * OCP-COMPLIANT REFACTOR (Phase 5): Tier benefit lookup now uses a registry map.
 * Adding a new tier requires only calling register() — this class is never modified.
 * Open for extension (via register), closed for modification (no if-else to edit).
 *
 * Before: massive if-else chain, every new tier = open this file and add a branch.
 * After: static registry, every new tier = call register() in configuration, done.
 */
@Component
public class TierBenefitCalculator {

    private static final Map<String, TierBenefits> REGISTRY = new LinkedHashMap<>();
    private static final String DEFAULT_TIER = TierStatus.GENERAL.name();

    static {
        register("EXECUTIVE_PLATINUM", TierBenefits.builder()
            .upgradeCertificates(8).loungeAccess(true).earlyBoarding(true).companionFare(true)
            .bonusMilesRate(0.11).priorityCheckIn(true).extraBaggage(3)
            .summary("EXECUTIVE_PLATINUM benefits: 8 upgrade certificates | Admirals Club lounge access"
                + " | early boarding Group 1 | companion fare certificate"
                + " | 11x EQM bonus | priority check-in | 3 free checked bags")
            .build());

        register("PLATINUM_PRO", TierBenefits.builder()
            .upgradeCertificates(6).loungeAccess(true).earlyBoarding(true).companionFare(false)
            .bonusMilesRate(0.09).priorityCheckIn(true).extraBaggage(3)
            .summary("PLATINUM_PRO benefits: 6 upgrade certificates | Admirals Club lounge access"
                + " | early boarding Group 1 | no companion fare"
                + " | 9x EQM bonus | priority check-in | 3 free checked bags")
            .build());

        register("PLATINUM", TierBenefits.builder()
            .upgradeCertificates(4).loungeAccess(false).earlyBoarding(true).companionFare(false)
            .bonusMilesRate(0.08).priorityCheckIn(true).extraBaggage(2)
            .summary("PLATINUM benefits: 4 upgrade certificates | no lounge access"
                + " | early boarding Group 1 | no companion fare"
                + " | 8x EQM bonus | priority check-in | 2 free checked bags")
            .build());

        register("GOLD", TierBenefits.builder()
            .upgradeCertificates(2).loungeAccess(false).earlyBoarding(true).companionFare(false)
            .bonusMilesRate(0.07).priorityCheckIn(false).extraBaggage(1)
            .summary("GOLD benefits: 2 upgrade certificates | no lounge access"
                + " | early boarding Group 4 | no companion fare"
                + " | 7x EQM bonus | no priority check-in | 1 free checked bag")
            .build());

        register(DEFAULT_TIER, TierBenefits.builder()
            .upgradeCertificates(0).loungeAccess(false).earlyBoarding(false).companionFare(false)
            .bonusMilesRate(0.00).priorityCheckIn(false).extraBaggage(0)
            .summary("GENERAL benefits: no upgrades | no lounge | standard boarding"
                + " | no companion fare | base miles only | no priority check-in | standard baggage")
            .build());
    }

    /**
     * Register a new tier benefit definition. Extension point — call this to add
     * a new tier without modifying any existing code (OCP).
     */
    public static void register(String tierName, TierBenefits benefits) {
        REGISTRY.put(tierName, benefits);
    }

    public Map<String, Object> getTierBenefits(String tierStatus) {
        TierBenefits benefits = REGISTRY.getOrDefault(tierStatus, REGISTRY.get(DEFAULT_TIER));
        return benefits.toMap();
    }

    public String getTierBenefitSummary(String tierStatus) {
        TierBenefits benefits = REGISTRY.getOrDefault(tierStatus, REGISTRY.get(DEFAULT_TIER));
        return benefits.getSummary();
    }
}
