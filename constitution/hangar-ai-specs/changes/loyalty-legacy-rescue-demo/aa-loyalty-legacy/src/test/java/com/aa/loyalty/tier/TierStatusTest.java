package com.aa.loyalty.tier;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.aa.loyalty.tier.domain.TierStatus;

class TierStatusTest {

    @Test
    void allSixValuesExist() {
        assertEquals(6, TierStatus.values().length);
    }

    @Test
    void valueOf_general_returnsGeneral() {
        assertEquals(TierStatus.GENERAL, TierStatus.valueOf("GENERAL"));
    }

    @Test
    void valueOf_gold_returnsGold() {
        assertEquals(TierStatus.GOLD, TierStatus.valueOf("GOLD"));
    }

    @Test
    void valueOf_platinum_returnsPlatinum() {
        assertEquals(TierStatus.PLATINUM, TierStatus.valueOf("PLATINUM"));
    }

    @Test
    void valueOf_platinumPro_returnsPlatinumPro() {
        assertEquals(TierStatus.PLATINUM_PRO, TierStatus.valueOf("PLATINUM_PRO"));
    }

    @Test
    void valueOf_executivePlatinum_returnsExecutivePlatinum() {
        assertEquals(TierStatus.EXECUTIVE_PLATINUM, TierStatus.valueOf("EXECUTIVE_PLATINUM"));
    }

    @Test
    void valueOf_conciergeKey_returnsConciergeKey() {
        assertEquals(TierStatus.CONCIERGE_KEY, TierStatus.valueOf("CONCIERGE_KEY"));
    }

    @Test
    void name_general_matchesDbString() {
        assertEquals("GENERAL", TierStatus.GENERAL.name());
    }

    @Test
    void name_gold_matchesDbString() {
        assertEquals("GOLD", TierStatus.GOLD.name());
    }

    @Test
    void name_platinum_matchesDbString() {
        assertEquals("PLATINUM", TierStatus.PLATINUM.name());
    }

    @Test
    void name_platinumPro_matchesDbString() {
        assertEquals("PLATINUM_PRO", TierStatus.PLATINUM_PRO.name());
    }

    @Test
    void name_executivePlatinum_matchesDbString() {
        assertEquals("EXECUTIVE_PLATINUM", TierStatus.EXECUTIVE_PLATINUM.name());
    }

    @Test
    void name_conciergeKey_matchesDbString() {
        assertEquals("CONCIERGE_KEY", TierStatus.CONCIERGE_KEY.name());
    }
}
