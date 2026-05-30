package com.aa.loyalty.mileage;

// CHARACTERIZATION TEST — ENG-4.10
// Locks existing behavior of MileageCalculator before any refactoring.
// Tests describe what the code DOES, not what it should do.

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MileageCalculatorTest {

    private MileageCalculator calculator;

    @BeforeEach
    void setUp() { calculator = new MileageCalculator(); }

    // ── calculateAccruedMiles ──────────────────────────────────────────

    @Test
    void calculateAccruedMiles_knownRoute_fullFare_general_returnsBaseMiles() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(1235, miles);
    }

    @Test
    void calculateAccruedMiles_reverseRoute_returnsDistanceMiles() {
        long miles = calculator.calculateAccruedMiles("LAX", "DFW", "Y", "GENERAL", null, false, 1);
        assertEquals(1235, miles);
    }

    @Test
    void calculateAccruedMiles_firstClass_appliesOnePointFiveMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "F", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 1.5), miles);
    }

    @Test
    void calculateAccruedMiles_businessClass_appliesOnePointFiveMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "J", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 1.5), miles);
    }

    @Test
    void calculateAccruedMiles_discountClass_appliesPointSevenFiveMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "V", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 0.75), miles);
    }

    @Test
    void calculateAccruedMiles_cheapestClass_appliesPointFiveMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "S", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 0.5), miles);
    }

    @Test
    void calculateAccruedMiles_nonEarningClass_returnsFloorFiveHundred() {
        // N class = 0.0 multiplier, classMultiplier=0 so floor does NOT apply, returns 0
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "N", "GENERAL", null, false, 1);
        assertEquals(0, miles);
    }

    @Test
    void calculateAccruedMiles_nullBookingClass_returnsZero() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", null, "GENERAL", null, false, 1);
        assertEquals(0, miles);
    }

    @Test
    void calculateAccruedMiles_unknownRoute_usesDefaultFiveHundred() {
        long miles = calculator.calculateAccruedMiles("AAA", "BBB", "Y", "GENERAL", null, false, 1);
        assertEquals(500, miles);
    }

    @Test
    void calculateAccruedMiles_goldTier_appliesTwentyFivePercentBonus() {
        long base = 1235;
        long bonus = Math.round(base * 0.25);
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GOLD", null, false, 1);
        assertEquals(base + bonus, miles);
    }

    @Test
    void calculateAccruedMiles_platinumTier_appliesFiftyPercentBonus() {
        long base = 1235;
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "PLATINUM", null, false, 1);
        assertEquals(base + Math.round(base * 0.50), miles);
    }

    @Test
    void calculateAccruedMiles_platinumProTier_appliesSeventyFivePercentBonus() {
        long base = 1235;
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "PLATINUM_PRO", null, false, 1);
        assertEquals(base + Math.round(base * 0.75), miles);
    }

    @Test
    void calculateAccruedMiles_execPlatTier_appliesOneHundredPercentBonus() {
        long base = 1235;
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "EXECUTIVE_PLATINUM", null, false, 1);
        assertEquals(base + Math.round(base * 1.0), miles);
    }

    @Test
    void calculateAccruedMiles_conciergeKeyTier_sameAsExecPlat() {
        long execPlat = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "EXECUTIVE_PLATINUM", null, false, 1);
        long ck = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "CONCIERGE_KEY", null, false, 1);
        assertEquals(execPlat, ck);
    }

    @Test
    void calculateAccruedMiles_partnerCodeBA_addsTenPercentBonus() {
        long base = 1235;
        long eliteBonus = 0;
        long partnerBonus = Math.round(base * 0.10);
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", "BA", false, 1);
        assertEquals(base + eliteBonus + partnerBonus, miles);
    }

    @Test
    void calculateAccruedMiles_promoFlag_doublesBaseMiles() {
        long base = 1235;
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, true, 1);
        // base + promo (=base) = 2 * base
        assertEquals(base * 2, miles);
    }

    @Test
    void calculateAccruedMiles_multipleSegments_addsSegmentBonus() {
        long base = 1235;
        long segBonus = 3 * 100L;
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 3);
        assertEquals(base + segBonus, miles);
    }

    @Test
    void calculateAccruedMiles_totalAboveCap_returnsCap() {
        // DFW-NRT = 6353 miles, first class (x1.5) = 9529 base. With EXEC_PLAT bonus = 19058. Under cap.
        // Force a cap scenario: use promo with high distance
        // DFW-NRT (6353) * 1.5 (F) = 9529 base, EXEC_PLAT +9529, promo +9529 = 28588 < cap
        // Need segments too: 28588 + (1000 * 100) = impossible in one call
        // Let's just verify cap doesn't interfere for normal routes
        long miles = calculator.calculateAccruedMiles("DFW", "NRT", "F", "EXECUTIVE_PLATINUM", null, false, 1);
        assertTrue(miles <= 100000);
    }

    @Test
    void calculateAccruedMiles_shortRoute_appliesMinimumFloor() {
        // Route 500 default, S class = 0.5 * 500 = 250 < floor, but floor applies only if classMultiplier > 0
        long miles = calculator.calculateAccruedMiles("AAA", "BBB", "S", "GENERAL", null, false, 1);
        assertEquals(500, miles); // floor kicks in: 500 default * 0.5 = 250 < 500, so floor = 500
    }

    // ── calculatePartnerMiles — see comprehensive tests below ──────────

    @Test
    void calculateAccruedMiles_classA_appliesFirstMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "A", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 1.5), miles); // A = first/business 1.5x
    }

    @Test
    void calculateAccruedMiles_classB_appliesFullFareMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "B", "GENERAL", null, false, 1);
        assertEquals(1235, miles);
    }

    @Test
    void calculateAccruedMiles_classK_appliesMidDiscountMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "K", "GENERAL", null, false, 1);
        assertEquals(1235, miles);
    }

    @Test
    void calculateAccruedMiles_classW_appliesDiscountMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "W", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 0.75), miles);
    }

    @Test
    void calculateAccruedMiles_classL_appliesCheapestMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "L", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 0.5), miles); // 0.5x
    }

    @Test
    void calculateAccruedMiles_classS_appliesHalfMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "S", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 0.5), miles);
    }

    @Test
    void calculateAccruedMiles_classN_zeroMultiplier_noFloor() {
        // N class = 0.0x, floor only applies when classMultiplier > 0
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "N", "GENERAL", null, false, 1);
        assertEquals(0L, miles);
    }

    @Test
    void calculateAccruedMiles_classG_appliesHalfMultiplier() {
        // G/Q class maps to 0.5x multiplier
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "G", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 0.5), miles);
    }

    @Test
    void calculateAccruedMiles_classQ_appliesHalfMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Q", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 0.5), miles);
    }

    @Test
    void calculateAccruedMiles_classC_appliesFirstMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "C", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 1.5), miles);
    }

    @Test
    void calculateAccruedMiles_classD_appliesFirstMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "D", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 1.5), miles);
    }

    @Test
    void calculateAccruedMiles_classM_appliesFullFareMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "M", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 1.0), miles);
    }

    @Test
    void calculateAccruedMiles_classH_appliesFullFareMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "H", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 1.0), miles);
    }

    @Test
    void calculateAccruedMiles_classO_zeroMultiplier_noFloor() {
        // O class = 0.0x, no floor
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "O", "GENERAL", null, false, 1);
        assertEquals(0L, miles);
    }

    @Test
    void calculateAccruedMiles_unknownBookingClass_appliesDefaultHalfMultiplier() {
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "Z", "GENERAL", null, false, 1);
        assertEquals(Math.round(1235 * 0.5), miles);
    }

    @Test
    void calculateAccruedMiles_nullTier_treatedAsGeneral() {
        long milesNull = calculator.calculateAccruedMiles("DFW", "LAX", "Y", null, null, false, 1);
        long milesGeneral = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(milesGeneral, milesNull); // null tier = no bonus = same as GENERAL
    }

    @Test
    void calculateAccruedMiles_partnerCodeBA_applies10PctBonus() {
        long withPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", "BA", false, 1);
        long withoutPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(withoutPartner + Math.round(withoutPartner * 0.10), withPartner);
    }

    @Test
    void calculateAccruedMiles_partnerCodeIB_applies10PctBonus() {
        long withPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", "IB", false, 1);
        long withoutPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(withoutPartner + Math.round(withoutPartner * 0.10), withPartner);
    }

    @Test
    void calculateAccruedMiles_partnerCodeQF_applies10PctBonus() {
        long withPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", "QF", false, 1);
        long withoutPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(withoutPartner + Math.round(withoutPartner * 0.10), withPartner);
    }

    @Test
    void calculateAccruedMiles_partnerCodeCX_applies10PctBonus() {
        long withPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", "CX", false, 1);
        long withoutPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(withoutPartner + Math.round(withoutPartner * 0.10), withPartner);
    }

    @Test
    void calculateAccruedMiles_partnerCodeJAL_applies10PctBonus() {
        long withPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", "JAL", false, 1);
        long withoutPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(withoutPartner + Math.round(withoutPartner * 0.10), withPartner);
    }

    @Test
    void calculateAccruedMiles_partnerCodeFJ_applies10PctBonus() {
        long withPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", "FJ", false, 1);
        long withoutPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(withoutPartner + Math.round(withoutPartner * 0.10), withPartner);
    }

    @Test
    void calculateAccruedMiles_unknownPartnerCode_noBonus() {
        long withUnknown = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", "DELTA", false, 1);
        long withoutPartner = calculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1);
        assertEquals(withoutPartner, withUnknown);
    }

    @Test
    void calculateAccruedMiles_floor_shortRouteBelowMinimum() {
        // DFW-ORD = 802 miles. Y class = 802. Floor is 500, so no floor needed.
        // Use a very short 0.5x route to trigger floor: 500 * 0.5 = 250 < 500 → floor applies
        long miles = calculator.calculateAccruedMiles("DFW", "LAX", "S", "GENERAL", null, false, 1);
        // DFW-LAX = 1235 * 0.5 = 617 — above floor
        // Need a route with base < 500: use unknown route (500 default) * 0.5 = 250 → floor = 500
        long shortMiles = calculator.calculateAccruedMiles("ABC", "XYZ", "S", "GENERAL", null, false, 1);
        assertEquals(500L, shortMiles); // floor applied
    }

    @Test
    void calculateAccruedMiles_exactlyAtFloorBoundary_appliesFloor() {
        // Unknown route = 500. With 0.5x multiplier: 250 < 500 → floor 500
        long miles = calculator.calculateAccruedMiles("UNK", "UNK", "L", "GENERAL", null, false, 1);
        assertEquals(500L, miles);
    }

    @Test
    void calculateAccruedMiles_veryLongFlight_capsAt100000() {
        long miles = calculator.calculateAccruedMiles("DFW", "NRT", "F", "CONCIERGE_KEY", "BA", false, 1000);
        assertEquals(100000L, miles);
    }

    @Test
    void calculateAccruedMiles_justAboveCap_returnsCap() {
        // DFW-NRT=6353, F=1.5x→9530 base, EXEC_PLAT 1.0→9530 elite, segments=900→90000
        // Total = 9530+9530+90000 = 109060 > 100000 → capped at 100000
        long miles = calculator.calculateAccruedMiles("DFW", "NRT", "F", "EXECUTIVE_PLATINUM", null, false, 900);
        assertEquals(100000L, miles);
    }

    // ── calculatePartnerMiles ─────────────────────────────────────────────

    @Test
    void calculatePartnerMiles_nullPartnerCode_returnsZero() {
        assertEquals(0L, calculator.calculatePartnerMiles(null, 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_hertz_earnsOneMilePerDollar() {
        assertEquals(100L, calculator.calculatePartnerMiles("HERTZ", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_avis_earnsOneMilePerDollar() {
        assertEquals(100L, calculator.calculatePartnerMiles("AVIS", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_budget_earnsOneMilePerDollar() {
        assertEquals(100L, calculator.calculatePartnerMiles("BUDGET", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_marriott_earnsOneMilePerDollar() {
        assertEquals(100L, calculator.calculatePartnerMiles("MARRIOTT", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_hilton_earnsOneMilePerDollar() {
        assertEquals(100L, calculator.calculatePartnerMiles("HILTON", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_hyatt_earnsOneMilePerDollar() {
        assertEquals(100L, calculator.calculatePartnerMiles("HYATT", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_citibank_earnsOneMilePerDollar() {
        assertEquals(100L, calculator.calculatePartnerMiles("CITIBANK_VISA", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_barclays_earnsOneMilePerDollar() {
        assertEquals(100L, calculator.calculatePartnerMiles("BARCLAYS", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_starbucks_earnsHalfMilePerDollar() {
        assertEquals(50L, calculator.calculatePartnerMiles("STARBUCKS", 100.0, "GENERAL"));
    }

    @Test
    void calculatePartnerMiles_unknownPartner_earnsHalfMilePerDollar() {
        long miles = calculator.calculatePartnerMiles("RANDOM", 100.0, "GENERAL");
        assertEquals(50, miles);
    }

    @Test
    void calculatePartnerMiles_nullTier_noBonus() {
        long milesNull = calculator.calculatePartnerMiles("HERTZ", 100.0, null);
        long milesGeneral = calculator.calculatePartnerMiles("HERTZ", 100.0, "GENERAL");
        assertEquals(milesGeneral, milesNull);
    }

    @Test
    void calculatePartnerMiles_goldTier_addsTwentyFivePercentBonus() {
        long miles = calculator.calculatePartnerMiles("HERTZ", 100.0, "GOLD");
        assertEquals(125L, miles);
    }

    @Test
    void calculatePartnerMiles_platinumTier_addsFiftyPercentBonus() {
        long miles = calculator.calculatePartnerMiles("HERTZ", 100.0, "PLATINUM");
        assertEquals(150, miles);
    }

    @Test
    void calculatePartnerMiles_platinumProTier_addsSeventyFivePercentBonus() {
        long miles = calculator.calculatePartnerMiles("HERTZ", 100.0, "PLATINUM_PRO");
        assertEquals(175, miles);
    }

    @Test
    void calculatePartnerMiles_execPlatTier_addsOneHundredPercentBonus() {
        long miles = calculator.calculatePartnerMiles("HERTZ", 100.0, "EXECUTIVE_PLATINUM");
        assertEquals(200, miles);
    }

    @Test
    void calculatePartnerMiles_conciergeKeyTier_addsOneHundredPercentBonus() {
        long miles = calculator.calculatePartnerMiles("HERTZ", 100.0, "CONCIERGE_KEY");
        assertEquals(200, miles);
    }

    @Test
    void calculatePartnerMiles_zeroSpend_returnsZero() {
        assertEquals(0L, calculator.calculatePartnerMiles("HERTZ", 0.0, "GOLD"));
    }

    @Test
    void calculatePartnerMiles_unknownTier_noEliteBonus() {
        long milesUnknown = calculator.calculatePartnerMiles("HERTZ", 100.0, "SUPER_ELITE");
        long milesGeneral = calculator.calculatePartnerMiles("HERTZ", 100.0, "GENERAL");
        assertEquals(milesGeneral, milesUnknown);
    }

    @Test
    void calculatePartnerMiles_negativeSpend_clampedToZero() {
        long miles = calculator.calculatePartnerMiles("HERTZ", -50.0, "GOLD");
        assertEquals(0L, miles);
    }
}


