package com.aa.loyalty.partner;

// CHARACTERIZATION TEST — ENG-4.10 (Phase 5: updated to reflect PartnerService fix)
import com.aa.loyalty.mileage.MileageCalculator;
import com.aa.loyalty.mileage.MileageService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class PartnerServiceTest {

    @Mock PartnerRepository partnerRepository;
    @Mock MileageService mileageService;
    @Mock MileageCalculator mileageCalculator;

    @InjectMocks PartnerService service;

    @Test
    void getActivePartners_delegatesToRepository() {
        List<Partner> partners = List.of(new Partner());
        when(partnerRepository.findByActive(true)).thenReturn(partners);
        assertEquals(partners, service.getActivePartners());
    }

    @Test
    void getPartnerDetails_delegatesToRepository() {
        Partner p = new Partner();
        when(partnerRepository.findByPartnerCode("HERTZ")).thenReturn(p);
        assertSame(p, service.getPartnerDetails("HERTZ"));
    }

    @Test
    void processPartnerAccrual_unknownPartner_returnsZero() {
        when(partnerRepository.findByPartnerCode("UNKNOWN")).thenReturn(null);
        long miles = service.processPartnerAccrual("AA001", "UNKNOWN", 100.0, "TXN001");
        assertEquals(0L, miles);
    }

    @Test
    void processPartnerAccrual_inactivePartner_returnsZero() {
        Partner p = new Partner();
        p.setActive(false);
        when(partnerRepository.findByPartnerCode("INACTIVE")).thenReturn(p);
        long miles = service.processPartnerAccrual("AA001", "INACTIVE", 100.0, "TXN002");
        assertEquals(0L, miles);
    }

    @Test
    void processPartnerAccrual_activePartner_usesCalculatePartnerMiles() {
        Partner p = new Partner();
        p.setActive(true);
        p.setPartnerCode("HERTZ");
        p.setBaseEarnRate(2.0);
        when(partnerRepository.findByPartnerCode("HERTZ")).thenReturn(p);
        when(mileageCalculator.calculatePartnerMiles("HERTZ", 100.0, "GENERAL")).thenReturn(100L);
        when(mileageService.accrueFlightMiles(eq("AA001"), eq("TXN003"), eq("PARTNER"),
            eq("HERTZ"), isNull(), any(), eq("TXN003"))).thenReturn(100L);
        long miles = service.processPartnerAccrual("AA001", "HERTZ", 100.0, "TXN003");
        assertEquals(100L, miles);
        verify(mileageCalculator).calculatePartnerMiles("HERTZ", 100.0, "GENERAL");
    }

    @Test
    void processPartnerAccrual_zeroMilesCalculated_returnsZeroWithoutAccruing() {
        Partner p = new Partner();
        p.setActive(true);
        p.setPartnerCode("HERTZ");
        when(partnerRepository.findByPartnerCode("HERTZ")).thenReturn(p);
        when(mileageCalculator.calculatePartnerMiles("HERTZ", 0.0, "GENERAL")).thenReturn(0L);
        long miles = service.processPartnerAccrual("AA001", "HERTZ", 0.0, "TXN004");
        assertEquals(0L, miles);
        verify(mileageService, never()).accrueFlightMiles(any(), any(), any(), any(), any(), any(), any());
    }
}
