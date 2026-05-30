package com.aa.loyalty.mileage;

import org.springframework.stereotype.Component;
import java.util.HashMap;
import java.util.Map;

/**
 * Mileage accrual calculator.
 * VIOLATIONS: High cyclomatic complexity (>30), long method, duplicate logic, magic numbers.
 */
@Component
public class MileageCalculator {

    // VIOLATION: hardcoded route distances — should be in database
    private static final Map<String, Integer> ROUTE_DISTANCES = new HashMap<>();
    static {
        ROUTE_DISTANCES.put("DFW-LAX", 1235);
        ROUTE_DISTANCES.put("DFW-JFK", 1391);
        ROUTE_DISTANCES.put("DFW-ORD", 802);
        ROUTE_DISTANCES.put("DFW-MIA", 1121);
        ROUTE_DISTANCES.put("DFW-LHR", 4751);
        ROUTE_DISTANCES.put("DFW-CDG", 4934);
        ROUTE_DISTANCES.put("DFW-NRT", 6353);
        ROUTE_DISTANCES.put("LAX-JFK", 2475);
        ROUTE_DISTANCES.put("LAX-ORD", 1745);
        ROUTE_DISTANCES.put("LAX-LHR", 5456);
        ROUTE_DISTANCES.put("JFK-LHR", 3450);
        ROUTE_DISTANCES.put("MIA-GRU", 4079);
        ROUTE_DISTANCES.put("DFW-MEX", 936);
        ROUTE_DISTANCES.put("ORD-LHR", 3941);
    }

    /**
     * VIOLATION: Method is 120+ lines, cyclomatic complexity ~35.
     * Does distance lookup, booking class multiplier, elite bonus, partner bonus,
     * promo bonus, minimum floor, expiry check, and cap — all in one method.
     */
    public long calculateAccruedMiles(String origin, String destination,
                                      String bookingClass, String memberTier,
                                      String partnerCode, boolean isPromo,
                                      int flightSegments) {
        // Step 1: get base distance
        String routeKey = origin + "-" + destination;
        String reverseKey = destination + "-" + origin;
        int distance = 0;

        if (ROUTE_DISTANCES.containsKey(routeKey)) {
            distance = ROUTE_DISTANCES.get(routeKey);
        } else if (ROUTE_DISTANCES.containsKey(reverseKey)) {
            distance = ROUTE_DISTANCES.get(reverseKey);
        } else {
            // VIOLATION: silently returns minimum instead of throwing
            distance = 500;
        }

        // Step 2: booking class multiplier — VIOLATION: magic numbers scattered
        double classMultiplier = 1.0;
        if (bookingClass == null) {
            classMultiplier = 0.0;
        } else if (bookingClass.equals("F") || bookingClass.equals("A")) {
            classMultiplier = 1.5;
        } else if (bookingClass.equals("J") || bookingClass.equals("C") || bookingClass.equals("D")) {
            classMultiplier = 1.5;
        } else if (bookingClass.equals("Y") || bookingClass.equals("B")) {
            classMultiplier = 1.0;
        } else if (bookingClass.equals("M") || bookingClass.equals("H") || bookingClass.equals("K")) {
            classMultiplier = 1.0;
        } else if (bookingClass.equals("V") || bookingClass.equals("W")) {
            classMultiplier = 0.75;
        } else if (bookingClass.equals("S") || bookingClass.equals("L")) {
            classMultiplier = 0.5;
        } else if (bookingClass.equals("G") || bookingClass.equals("Q")) {
            classMultiplier = 0.5;
        } else if (bookingClass.equals("N")) {
            classMultiplier = 0.0;
        } else if (bookingClass.equals("O")) {
            classMultiplier = 0.0;
        } else {
            classMultiplier = 0.5;  // VIOLATION: default case for unknown booking class silently accrues
        }

        long baseMiles = Math.round(distance * classMultiplier);

        // Step 3: elite tier bonus — VIOLATION: duplicated logic from TierCalculator
        double eliteBonus = 0.0;
        if (memberTier == null || memberTier.equals("GENERAL")) {
            eliteBonus = 0.0;
        } else if (memberTier.equals("GOLD")) {
            eliteBonus = 0.25;
        } else if (memberTier.equals("PLATINUM")) {
            eliteBonus = 0.50;
        } else if (memberTier.equals("PLATINUM_PRO")) {
            eliteBonus = 0.75;
        } else if (memberTier.equals("EXECUTIVE_PLATINUM")) {
            eliteBonus = 1.00;
        } else if (memberTier.equals("CONCIERGE_KEY")) {
            eliteBonus = 1.00;
        }

        long eliteBonusMiles = Math.round(baseMiles * eliteBonus);

        // Step 4: partner bonus
        long partnerBonusMiles = 0;
        if (partnerCode != null) {
            if (partnerCode.equals("BA") || partnerCode.equals("IB")) {
                partnerBonusMiles = Math.round(baseMiles * 0.10);
            } else if (partnerCode.equals("QF") || partnerCode.equals("CX")) {
                partnerBonusMiles = Math.round(baseMiles * 0.10);
            } else if (partnerCode.equals("JAL") || partnerCode.equals("FJ")) {
                partnerBonusMiles = Math.round(baseMiles * 0.10);
            } else {
                partnerBonusMiles = 0;
            }
        }

        // Step 5: promo multiplier
        long promoBonus = 0;
        if (isPromo) {
            // VIOLATION: hardcoded 2x promo — should be configurable
            promoBonus = baseMiles;
        }

        // Step 6: segment bonus
        long segmentBonus = 0;
        if (flightSegments > 1) {
            segmentBonus = flightSegments * 100L;  // VIOLATION: magic number 100
        }

        long totalMiles = baseMiles + eliteBonusMiles + partnerBonusMiles + promoBonus + segmentBonus;

        // Step 7: minimum floor  — VIOLATION: hardcoded 500 minimum
        if (totalMiles < 500 && classMultiplier > 0) {
            totalMiles = 500;
        }

        // Step 8: cap — VIOLATION: hardcoded 100,000 cap per transaction
        if (totalMiles > 100000) {
            totalMiles = 100000;
        }

        return totalMiles;
    }

    // VIOLATION: nearly identical method duplicated below for "partner accrual" 
    public long calculatePartnerMiles(String partnerCode, double spendAmount, String memberTier) {
        double ratePerDollar = 1.0;

        if (partnerCode == null) return 0;

        if (partnerCode.equals("HERTZ") || partnerCode.equals("AVIS") || partnerCode.equals("BUDGET")) {
            ratePerDollar = 1.0;
        } else if (partnerCode.equals("MARRIOTT") || partnerCode.equals("HILTON") || partnerCode.equals("HYATT")) {
            ratePerDollar = 1.0;
        } else if (partnerCode.equals("CITIBANK_VISA") || partnerCode.equals("BARCLAYS")) {
            ratePerDollar = 1.0;
        } else if (partnerCode.equals("STARBUCKS")) {
            ratePerDollar = 0.5;
        } else {
            ratePerDollar = 0.5;
        }

        long baseMiles = Math.round(spendAmount * ratePerDollar);

        // VIOLATION: copy-paste of elite bonus logic from calculateAccruedMiles
        double eliteBonus = 0.0;
        if (memberTier == null || memberTier.equals("GENERAL")) {
            eliteBonus = 0.0;
        } else if (memberTier.equals("GOLD")) {
            eliteBonus = 0.25;
        } else if (memberTier.equals("PLATINUM")) {
            eliteBonus = 0.50;
        } else if (memberTier.equals("PLATINUM_PRO")) {
            eliteBonus = 0.75;
        } else if (memberTier.equals("EXECUTIVE_PLATINUM")) {
            eliteBonus = 1.00;
        } else if (memberTier.equals("CONCIERGE_KEY")) {
            eliteBonus = 1.00;
        }

        long eliteBonusMiles = Math.round(baseMiles * eliteBonus);
        long total = baseMiles + eliteBonusMiles;
        if (total < 0) total = 0;
        return total;
    }
}
