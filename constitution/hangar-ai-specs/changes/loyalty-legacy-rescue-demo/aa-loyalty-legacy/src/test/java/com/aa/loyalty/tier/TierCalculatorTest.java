package com.aa.loyalty.tier;

// CHARACTERIZATION TEST — ENG-4.10
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TierCalculatorTest {

    private TierCalculator calc;

    @BeforeEach
    void setUp() { calc = new TierCalculator(); }

    // ── calculateNewTier ──────────────────────────────────────────────

    @Test
    void calculateNewTier_below25kEqm_returnsGeneral() {
        assertEquals("GENERAL", calc.calculateNewTier(10000, 5, 50000));
    }

    @Test
    void calculateNewTier_25kEqm_returnsGold() {
        assertEquals("GOLD", calc.calculateNewTier(25000, 5, 50000));
    }

    @Test
    void calculateNewTier_20kEqmWith30Eqs_returnsGold() {
        assertEquals("GOLD", calc.calculateNewTier(20000, 30, 50000));
    }

    @Test
    void calculateNewTier_50kEqm_returnsPlatinum() {
        assertEquals("PLATINUM", calc.calculateNewTier(50000, 5, 100000));
    }

    @Test
    void calculateNewTier_40kEqmWith60Eqs_returnsPlatinum() {
        assertEquals("PLATINUM", calc.calculateNewTier(40000, 60, 80000));
    }

    @Test
    void calculateNewTier_75kEqm_returnsPlatinumPro() {
        assertEquals("PLATINUM_PRO", calc.calculateNewTier(75000, 5, 150000));
    }

    @Test
    void calculateNewTier_50kEqmWith90Eqs_returnsPlatinumPro() {
        assertEquals("PLATINUM_PRO", calc.calculateNewTier(50000, 90, 100000));
    }

    @Test
    void calculateNewTier_100kEqm_returnsExecPlat() {
        assertEquals("EXECUTIVE_PLATINUM", calc.calculateNewTier(100000, 5, 200000));
    }

    // ── getEliteMilesBonus ────────────────────────────────────────────

    @Test
    void getEliteMilesBonus_general_returnsZero() {
        assertEquals(0.0, calc.getEliteMilesBonus("GENERAL"));
    }

    @Test
    void getEliteMilesBonus_null_returnsZero() {
        assertEquals(0.0, calc.getEliteMilesBonus(null));
    }

    @Test
    void getEliteMilesBonus_gold_returnsPointTwoFive() {
        assertEquals(0.25, calc.getEliteMilesBonus("GOLD"));
    }

    @Test
    void getEliteMilesBonus_platinum_returnsPointFive() {
        assertEquals(0.50, calc.getEliteMilesBonus("PLATINUM"));
    }

    @Test
    void getEliteMilesBonus_platinumPro_returnsPointSevenFive() {
        assertEquals(0.75, calc.getEliteMilesBonus("PLATINUM_PRO"));
    }

    @Test
    void getEliteMilesBonus_execPlat_returnsOne() {
        assertEquals(1.00, calc.getEliteMilesBonus("EXECUTIVE_PLATINUM"));
    }

    @Test
    void getEliteMilesBonus_conciergeKey_returnsOne() {
        assertEquals(1.00, calc.getEliteMilesBonus("CONCIERGE_KEY"));
    }

    // ── isUpgradeEligible ─────────────────────────────────────────────

    @Test
    void isUpgradeEligible_general25kEqm30Eqs_returnsTrue() {
        assertTrue(calc.isUpgradeEligible(25000, 30, "GENERAL"));
    }

    @Test
    void isUpgradeEligible_generalBelowThreshold_returnsFalse() {
        assertFalse(calc.isUpgradeEligible(10000, 10, "GENERAL"));
    }

    @Test
    void isUpgradeEligible_gold50kEqm_returnsTrue() {
        assertTrue(calc.isUpgradeEligible(50000, 5, "GOLD"));
    }

    @Test
    void isUpgradeEligible_platinum75kEqm_returnsTrue() {
        assertTrue(calc.isUpgradeEligible(75000, 5, "PLATINUM"));
    }

    @Test
    void isUpgradeEligible_execPlat_returnsFalseAlways() {
        assertFalse(calc.isUpgradeEligible(200000, 500, "EXECUTIVE_PLATINUM"));
    }

    // ── getUpgradeComplimentaryCount ──────────────────────────────────

    @Test
    void getUpgradeComplimentaryCount_general_returnsZero() {
        assertEquals(0, calc.getUpgradeComplimentaryCount("GENERAL"));
    }

    @Test
    void getUpgradeComplimentaryCount_gold_returnsTwo() {
        assertEquals(2, calc.getUpgradeComplimentaryCount("GOLD"));
    }

    @Test
    void getUpgradeComplimentaryCount_platinum_returnsFour() {
        assertEquals(4, calc.getUpgradeComplimentaryCount("PLATINUM"));
    }

    @Test
    void getUpgradeComplimentaryCount_platinumPro_returnsSix() {
        assertEquals(6, calc.getUpgradeComplimentaryCount("PLATINUM_PRO"));
    }

    @Test
    void getUpgradeComplimentaryCount_execPlat_returnsEight() {
        assertEquals(8, calc.getUpgradeComplimentaryCount("EXECUTIVE_PLATINUM"));
    }

    @Test
    void getEliteMilesBonus_conciergeKey_returnsOneHundredPercent() {
        assertEquals(1.00, calc.getEliteMilesBonus("CONCIERGE_KEY"), 0.001);
    }

    // ── Additional boundary tests to kill conditional mutations ───────

    @Test
    void calculateNewTier_justBelow100k_notExecPlat() {
        assertNotEquals("EXECUTIVE_PLATINUM", calc.calculateNewTier(99999, 5, 200000));
    }

    @Test
    void calculateNewTier_justBelow75k_withoutSegments_notPlatinumPro() {
        String tier = calc.calculateNewTier(74999, 5, 100000);
        assertNotEquals("PLATINUM_PRO", tier);
    }

    @Test
    void calculateNewTier_justBelow50k_notPlatinum() {
        String tier = calc.calculateNewTier(49999, 5, 80000);
        assertNotEquals("PLATINUM", tier);
    }

    @Test
    void calculateNewTier_40kEqmWith60Eqs_returnsPlatinum_v2() {
        assertEquals("PLATINUM", calc.calculateNewTier(40000, 60, 80000));
    }

    @Test
    void calculateNewTier_20kEqmWith30Eqs_returnsGold_v2() {
        assertEquals("GOLD", calc.calculateNewTier(20000, 30, 50000));
    }

    @Test
    void calculateNewTier_justBelow25k_notGold() {
        String tier = calc.calculateNewTier(24999, 5, 40000);
        assertNotEquals("GOLD", tier);
    }

    @Test
    void isUpgradeEligible_generalJustBelowMilesThreshold_returnsFalse() {
        assertFalse(calc.isUpgradeEligible(24999, 30, "GENERAL"));
    }

    @Test
    void isUpgradeEligible_generalJustBelowSegmentThreshold_returnsFalse() {
        assertFalse(calc.isUpgradeEligible(25000, 29, "GENERAL"));
    }

    @Test
    void isUpgradeEligible_goldJustBelowThreshold_returnsFalse() {
        assertFalse(calc.isUpgradeEligible(49999, 100, "GOLD"));
    }

    @Test
    void isUpgradeEligible_platinumJustBelowThreshold_returnsFalse() {
        assertFalse(calc.isUpgradeEligible(74999, 200, "PLATINUM"));
    }

    @Test
    void isUpgradeEligible_platinumPro100k_returnsTrue() {
        assertTrue(calc.isUpgradeEligible(100000, 5, "PLATINUM_PRO"));
    }

    @Test
    void isUpgradeEligible_platinumProJustBelow_returnsFalse() {
        assertFalse(calc.isUpgradeEligible(99999, 200, "PLATINUM_PRO"));
    }

    @Test
    void getEliteMilesBonus_unknownTier_returnsZero() {
        assertEquals(0.0, calc.getEliteMilesBonus("UNKNOWN_TIER"));
    }
}
