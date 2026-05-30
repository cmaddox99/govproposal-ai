package com.aa.loyalty.tier;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.tier.domain.TierBenefitCalculator;

/**
 * CHARACTERIZATION TEST (ENG-4.10) — locks current behavior of TierBenefitCalculator.
 * OCP VIOLATION: each test proves a hardcoded if-else branch exists.
 * After OCP fix, these same assertions verify the registry-based implementation
 * produces identical outputs — the behavior is preserved, the structure is fixed.
 */
class TierBenefitCalculatorTest {

    private final TierBenefitCalculator calc = new TierBenefitCalculator();

    @Test
    void getTierBenefits_gold_returnsExpectedBenefits() {
        Map<String, Object> benefits = calc.getTierBenefits("GOLD");
        assertEquals(2, benefits.get("upgradeCertificates"));
        assertEquals(false, benefits.get("loungeAccess"));
        assertEquals(true, benefits.get("earlyBoarding"));
        assertEquals(false, benefits.get("companionFare"));
        assertEquals(0.07, (Double) benefits.get("bonusMilesRate"), 0.001);
        assertEquals(false, benefits.get("priorityCheckIn"));
        assertEquals(1, benefits.get("extraBaggage"));
    }

    @Test
    void getTierBenefits_platinum_returnsExpectedBenefits() {
        Map<String, Object> benefits = calc.getTierBenefits("PLATINUM");
        assertEquals(4, benefits.get("upgradeCertificates"));
        assertEquals(false, benefits.get("loungeAccess"));
        assertEquals(true, benefits.get("earlyBoarding"));
        assertEquals(false, benefits.get("companionFare"));
        assertEquals(0.08, (Double) benefits.get("bonusMilesRate"), 0.001);
        assertEquals(true, benefits.get("priorityCheckIn"));
        assertEquals(2, benefits.get("extraBaggage"));
    }

    @Test
    void getTierBenefits_platinumPro_returnsExpectedBenefits() {
        Map<String, Object> benefits = calc.getTierBenefits("PLATINUM_PRO");
        assertEquals(6, benefits.get("upgradeCertificates"));
        assertEquals(true, benefits.get("loungeAccess"));
        assertEquals(true, benefits.get("earlyBoarding"));
        assertEquals(false, benefits.get("companionFare"));
        assertEquals(0.09, (Double) benefits.get("bonusMilesRate"), 0.001);
        assertEquals(true, benefits.get("priorityCheckIn"));
        assertEquals(3, benefits.get("extraBaggage"));
    }

    @Test
    void getTierBenefits_executivePlatinum_returnsExpectedBenefits() {
        Map<String, Object> benefits = calc.getTierBenefits("EXECUTIVE_PLATINUM");
        assertEquals(8, benefits.get("upgradeCertificates"));
        assertEquals(true, benefits.get("loungeAccess"));
        assertEquals(true, benefits.get("earlyBoarding"));
        assertEquals(true, benefits.get("companionFare"));
        assertEquals(0.11, (Double) benefits.get("bonusMilesRate"), 0.001);
        assertEquals(true, benefits.get("priorityCheckIn"));
        assertEquals(3, benefits.get("extraBaggage"));
    }

    @Test
    void getTierBenefits_unknownTier_returnsBaselineBenefits() {
        Map<String, Object> benefits = calc.getTierBenefits("CONCIERGE_KEY_EXTENDED");
        assertEquals(0, benefits.get("upgradeCertificates"));
        assertEquals(false, benefits.get("loungeAccess"));
        assertEquals(false, benefits.get("earlyBoarding"));
        assertEquals(false, benefits.get("companionFare"));
        assertEquals(0.00, (Double) benefits.get("bonusMilesRate"), 0.001);
        assertEquals(false, benefits.get("priorityCheckIn"));
        assertEquals(0, benefits.get("extraBaggage"));
    }

    @Test
    void getTierBenefits_nullTier_returnsBaselineBenefits() {
        Map<String, Object> benefits = calc.getTierBenefits(null);
        assertEquals(0, benefits.get("upgradeCertificates"));
        assertEquals(false, benefits.get("loungeAccess"));
    }

    @Test
    void getTierBenefits_general_returnsBaselineBenefits() {
        Map<String, Object> benefits = calc.getTierBenefits("GENERAL");
        assertEquals(0, benefits.get("upgradeCertificates"));
        assertEquals(false, benefits.get("loungeAccess"));
        assertEquals(false, benefits.get("earlyBoarding"));
        assertEquals(0.00, (Double) benefits.get("bonusMilesRate"), 0.001);
    }

    @ParameterizedTest
    @CsvSource({
        "GOLD, GOLD, upgrade",
        "EXECUTIVE_PLATINUM, EXECUTIVE_PLATINUM, lounge",
        "PLATINUM, PLATINUM, upgrade"
    })
    void getTierBenefitSummary_containsTierNameAndKeyword(String tier, String expectedTier, String expectedKeyword) {
        String summary = calc.getTierBenefitSummary(tier);
        assertNotNull(summary);
        assertTrue(summary.contains(expectedTier));
        assertTrue(summary.contains(expectedKeyword));
    }

    @Test
    void getTierBenefitSummary_platinumPro_containsExpected() {
        String summary = calc.getTierBenefitSummary("PLATINUM_PRO");
        assertNotNull(summary);
        assertTrue(summary.contains("PLATINUM_PRO"));
    }

    @Test
    void getTierBenefitSummary_unknown_returnsGeneralSummary() {
        String summary = calc.getTierBenefitSummary("DOES_NOT_EXIST");
        assertNotNull(summary);
        assertTrue(summary.contains("GENERAL") || summary.contains("base") || summary.contains("standard"));
    }
}
