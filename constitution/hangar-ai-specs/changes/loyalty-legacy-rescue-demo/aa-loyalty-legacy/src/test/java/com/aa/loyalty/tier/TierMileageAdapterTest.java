package com.aa.loyalty.tier;

import com.aa.loyalty.mileage.domain.MileageAccount;
import com.aa.loyalty.mileage.domain.MileageRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import com.aa.loyalty.tier.infrastructure.TierMileageAdapter;
import com.aa.loyalty.tier.domain.MileageStatsView;

@ExtendWith(MockitoExtension.class)
class TierMileageAdapterTest {

    @Mock MileageRepository mileageRepository;
    @InjectMocks TierMileageAdapter adapter;

    @Test
    void getMileageStats_accountExists_returnsStats() {
        MileageAccount account = new MileageAccount("AA001");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(30);
        account.setTotalMiles(50000L);
        when(mileageRepository.findByMemberNumber("AA001")).thenReturn(account);
        MileageStatsView stats = adapter.getMileageStats("AA001");
        assertEquals(25000L, stats.getEliteQualifyingMiles());
        assertEquals(30, stats.getEliteQualifyingSegments());
        assertEquals(50000L, stats.getTotalMiles());
    }

    @Test
    void getMileageStats_accountNotFound_returnsZeroStats() {
        when(mileageRepository.findByMemberNumber("NONE")).thenReturn(null);
        MileageStatsView stats = adapter.getMileageStats("NONE");
        assertEquals(0L, stats.getEliteQualifyingMiles());
        assertEquals(0, stats.getEliteQualifyingSegments());
        assertEquals(0L, stats.getTotalMiles());
    }
}
