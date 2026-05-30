package com.aa.loyalty.tier;

import org.springframework.stereotype.Component;

/**
 * VIOLATIONS:
 * - Elite bonus logic duplicated verbatim from MileageCalculator
 * - Tier thresholds hardcoded — should be configurable
 * - Method knows too much about member state
 */
@Component
public class TierCalculator {

    // VIOLATION: duplicate of MileageCalculator elite tier map
    public double getEliteMilesBonus(String tier) {
        if (tier == null || tier.equals("GENERAL")) return 0.0;
        if (tier.equals("GOLD")) return 0.25;
        if (tier.equals("PLATINUM")) return 0.50;
        if (tier.equals("PLATINUM_PRO")) return 0.75;
        if (tier.equals("EXECUTIVE_PLATINUM")) return 1.00;
        if (tier.equals("CONCIERGE_KEY")) return 1.00;
        return 0.0;
    }

    /**
     * VIOLATION: cyclomatic complexity ~18, all thresholds magic numbers
     */
    public String calculateNewTier(long eqm, int eqs, long totalMiles) {
        // EQM = Elite Qualifying Miles, EQS = Elite Qualifying Segments
        if (eqm >= 100000) {
            return "EXECUTIVE_PLATINUM";
        } else if (eqm >= 75000 || (eqm >= 50000 && eqs >= 90)) {
            return "PLATINUM_PRO";
        } else if (eqm >= 50000 || (eqm >= 40000 && eqs >= 60)) {
            return "PLATINUM";
        } else if (eqm >= 25000 || (eqm >= 20000 && eqs >= 30)) {
            return "GOLD";
        } else {
            return "GENERAL";
        }
    }

    // VIOLATION: duplicate of isEligibleForUpgrade in MileageService
    public boolean isUpgradeEligible(long eqm, int eqs, String currentTier) {
        if (currentTier.equals("GENERAL") && eqm >= 25000 && eqs >= 30) return true;
        if (currentTier.equals("GOLD") && eqm >= 50000) return true;
        if (currentTier.equals("PLATINUM") && eqm >= 75000) return true;
        if (currentTier.equals("PLATINUM_PRO") && eqm >= 100000) return true;
        return false;
    }

    public int getUpgradeComplimentaryCount(String tier) {
        // VIOLATION: magic numbers, not configurable
        if (tier.equals("EXECUTIVE_PLATINUM")) return 8;
        if (tier.equals("PLATINUM_PRO")) return 6;
        if (tier.equals("PLATINUM")) return 4;
        if (tier.equals("GOLD")) return 2;
        return 0;
    }
}
