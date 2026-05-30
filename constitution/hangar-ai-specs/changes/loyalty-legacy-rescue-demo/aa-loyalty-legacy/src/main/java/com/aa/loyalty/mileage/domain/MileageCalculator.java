package com.aa.loyalty.mileage.domain;

import org.springframework.stereotype.Component;
import java.util.HashMap;
import java.util.Map;

/**
 * Mileage accrual calculator.
 * VIOLATIONS: High cyclomatic complexity (>30), long method, duplicate logic, magic numbers.
 */
@Component
public class MileageCalculator implements MileageCalculationPort {

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
        int distance = getBaseDistance(origin, destination);
        double classMultiplier = getBookingClassMultiplier(bookingClass);
        long baseMiles = Math.round(distance * classMultiplier);
        long eliteBonusMiles = Math.round(baseMiles * getEliteBonusFraction(memberTier));
        long partnerBonusMiles = calculatePartnerFlightBonus(partnerCode, baseMiles);
        long promoBonus = isPromo ? baseMiles : 0;
        long segmentBonus = flightSegments > 1 ? flightSegments * 100L : 0;

        long totalMiles = baseMiles + eliteBonusMiles + partnerBonusMiles + promoBonus + segmentBonus;

        if (totalMiles < 500 && classMultiplier > 0) {
            totalMiles = 500;
        }
        if (totalMiles > 100000) {
            totalMiles = 100000;
        }
        return totalMiles;
    }

    private int getBaseDistance(String origin, String destination) {
        String routeKey = origin + "-" + destination;
        String reverseKey = destination + "-" + origin;
        if (ROUTE_DISTANCES.containsKey(routeKey)) {
            return ROUTE_DISTANCES.get(routeKey);
        } else if (ROUTE_DISTANCES.containsKey(reverseKey)) {
            return ROUTE_DISTANCES.get(reverseKey);
        }
        // VIOLATION: silently returns minimum instead of throwing
        return 500;
    }

    private double getBookingClassMultiplier(String bookingClass) {
        if (bookingClass == null) return 0.0;
        switch (bookingClass) {
            case "F": case "A": return 1.5;
            case "J": case "C": case "D": return 1.5;
            case "Y": case "B": return 1.0;
            case "M": case "H": case "K": return 1.0;
            case "V": case "W": return 0.75;
            case "S": case "L": return 0.5;
            case "G": case "Q": return 0.5;
            case "N": case "O": return 0.0;
            default: return 0.5; // VIOLATION: default case for unknown booking class silently accrues
        }
    }

    private double getEliteBonusFraction(String memberTier) {
        if (memberTier == null) return 0.0;
        switch (memberTier) {
            case "GOLD": return 0.25;
            case "PLATINUM": return 0.50;
            case "PLATINUM_PRO": return 0.75;
            case "EXECUTIVE_PLATINUM": return 1.00;
            case "CONCIERGE_KEY": return 1.00;
            default: return 0.0;
        }
    }

    private long calculatePartnerFlightBonus(String partnerCode, long baseMiles) {
        if (partnerCode == null) return 0;
        if (partnerCode.equals("BA") || partnerCode.equals("IB")
                || partnerCode.equals("QF") || partnerCode.equals("CX")
                || partnerCode.equals("JAL") || partnerCode.equals("FJ")) {
            return Math.round(baseMiles * 0.10);
        }
        return 0;
    }

    // VIOLATION: nearly identical method duplicated below for "partner accrual"
    public long calculatePartnerMiles(String partnerCode, double spendAmount, String memberTier) {
        if (partnerCode == null) return 0;
        double ratePerDollar = getPartnerSpendRate(partnerCode);
        long baseMiles = Math.round(spendAmount * ratePerDollar);
        long eliteBonusMiles = Math.round(baseMiles * getEliteBonusFraction(memberTier));
        long total = baseMiles + eliteBonusMiles;
        if (total < 0) total = 0;
        return total;
    }

    private double getPartnerSpendRate(String partnerCode) {
        if (partnerCode.equals("HERTZ") || partnerCode.equals("AVIS") || partnerCode.equals("BUDGET")
                || partnerCode.equals("MARRIOTT") || partnerCode.equals("HILTON") || partnerCode.equals("HYATT")
                || partnerCode.equals("CITIBANK_VISA") || partnerCode.equals("BARCLAYS")) {
            return 1.0;
        }
        // VIOLATION: hardcoded partner rates; STARBUCKS and unknown partners earn 0.5 miles/dollar
        return 0.5;
    }
}
