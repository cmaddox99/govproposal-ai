package com.aa.loyalty.redemption;

// CHARACTERIZATION TEST — ENG-4.10
import com.aa.loyalty.mileage.MileageService;
import com.aa.loyalty.notification.NotificationService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RedemptionServiceTest {

    @Mock RedemptionRepository redemptionRepository;
    @Mock MileageService mileageService;
    @Mock NotificationService notificationService;

    @InjectMocks RedemptionService service;

    @Test
    void bookAwardFlight_insufficientMiles_throwsRuntimeException() {
        when(mileageService.redeemMiles(eq("AA001"), anyLong(), eq("AWARD_FLIGHT"), any()))
            .thenReturn(false);
        assertThrows(RuntimeException.class,
            () -> service.bookAwardFlight("AA001", "DFW", "LAX", new Date(), "COACH"));
    }

    @Test
    void bookAwardFlight_dfwLaxCoach_verifiesAllRedemptionFields() {
        when(mileageService.redeemMiles("AA002", 12500L, "AWARD_FLIGHT",
            "Award flight DFW-LAX")).thenReturn(true);
        ArgumentCaptor<Redemption> captor = ArgumentCaptor.forClass(Redemption.class);
        when(redemptionRepository.save(captor.capture())).thenAnswer(i -> i.getArgument(0));
        Date travelDate = new Date(System.currentTimeMillis() + 86400000L);
        service.bookAwardFlight("AA002", "DFW", "LAX", travelDate, "COACH");
        Redemption saved = captor.getValue();
        assertEquals("AA002", saved.getMemberNumber());
        assertEquals("AWARD_FLIGHT", saved.getRedemptionType());
        assertEquals(12500L, saved.getMilesCost());
        assertEquals("CONFIRMED", saved.getStatus());
        assertNotNull(saved.getReservationCode());
        assertFalse(saved.getReservationCode().isEmpty());
        assertNotNull(saved.getRedemptionDate());
        assertEquals(travelDate, saved.getTravelDate());
        assertEquals("DFW", saved.getOrigin());
        assertEquals("LAX", saved.getDestination());
        assertEquals("COACH", saved.getCabinClass());
    }

    @Test
    void bookAwardFlight_dfwLhrBusiness_costs57500Miles() {
        when(mileageService.redeemMiles("AA003", 57500L, "AWARD_FLIGHT",
            "Award flight DFW-LHR")).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.bookAwardFlight("AA003", "DFW", "LHR", new Date(), "BUSINESS");
        verify(mileageService).redeemMiles("AA003", 57500L, "AWARD_FLIGHT", "Award flight DFW-LHR");
    }

    @Test
    void bookAwardFlight_dfwLhrFirst_costs70000Miles() {
        when(mileageService.redeemMiles("AA004", 70000L, "AWARD_FLIGHT",
            "Award flight DFW-LHR")).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.bookAwardFlight("AA004", "DFW", "LHR", new Date(), "FIRST");
        verify(mileageService).redeemMiles("AA004", 70000L, "AWARD_FLIGHT", "Award flight DFW-LHR");
    }

    @Test
    void bookAwardFlight_dfwLhrCoach_costs30000Miles() {
        when(mileageService.redeemMiles("AA008", 30000L, "AWARD_FLIGHT",
            "Award flight DFW-LHR")).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.bookAwardFlight("AA008", "DFW", "LHR", new Date(), "COACH");
        verify(mileageService).redeemMiles("AA008", 30000L, "AWARD_FLIGHT", "Award flight DFW-LHR");
    }

    @Test
    void bookAwardFlight_lhrDfw_reverseRoute_costs30000Miles() {
        when(mileageService.redeemMiles("AA009", 30000L, "AWARD_FLIGHT",
            "Award flight LHR-DFW")).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.bookAwardFlight("AA009", "LHR", "DFW", new Date(), "COACH");
        verify(mileageService).redeemMiles("AA009", 30000L, "AWARD_FLIGHT", "Award flight LHR-DFW");
    }

    @Test
    void bookAwardFlight_unknownRoute_costsDefaultMiles() {
        when(mileageService.redeemMiles(eq("AA005"), eq(25000L), any(), any())).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.bookAwardFlight("AA005", "AAA", "BBB", new Date(), "COACH");
        verify(mileageService).redeemMiles(eq("AA005"), eq(25000L), any(), any());
    }

    @Test
    void bookAwardFlight_dfwLaxBusiness_costs25000Miles() {
        when(mileageService.redeemMiles("AA006", 25000L, "AWARD_FLIGHT",
            "Award flight DFW-LAX")).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.bookAwardFlight("AA006", "DFW", "LAX", new Date(), "BUSINESS");
        verify(mileageService).redeemMiles("AA006", 25000L, "AWARD_FLIGHT", "Award flight DFW-LAX");
    }

    @Test
    void bookAwardFlight_nullCabinClass_treatedAsCoach() {
        when(mileageService.redeemMiles(eq("AA010"), eq(12500L), any(), any())).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.bookAwardFlight("AA010", "DFW", "LAX", new Date(), null);
        verify(mileageService).redeemMiles(eq("AA010"), eq(12500L), any(), any());
    }

    @Test
    void bookAwardFlight_laxDfw_reverseRoute_costs12500Miles() {
        when(mileageService.redeemMiles("AA011", 12500L, "AWARD_FLIGHT",
            "Award flight LAX-DFW")).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.bookAwardFlight("AA011", "LAX", "DFW", new Date(), "COACH");
        verify(mileageService).redeemMiles("AA011", 12500L, "AWARD_FLIGHT", "Award flight LAX-DFW");
    }

    @Test
    void getRedemptionHistory_delegatesToRepository() {
        List<Redemption> history = List.of(new Redemption());
        when(redemptionRepository.findByMemberNumber("AA006")).thenReturn(history);
        assertEquals(history, service.getRedemptionHistory("AA006"));
    }

    @Test
    void cancelRedemption_confirmedReservation_cancelsRefundsMilesAndReturnsTrue() {
        Redemption r = new Redemption();
        r.setReservationCode("ABC123");
        r.setStatus("CONFIRMED");
        r.setMemberNumber("AA001");
        r.setMilesCost(25000L);
        when(redemptionRepository.findAll()).thenReturn(List.of(r));
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        when(mileageService.redeemMiles(eq("AA001"), eq(-25000L),
            eq("CANCELLATION_REFUND"), any())).thenReturn(true);
        assertTrue(service.cancelRedemption("ABC123"));
        assertEquals("CANCELLED", r.getStatus());
        verify(mileageService).redeemMiles(eq("AA001"), eq(-25000L), eq("CANCELLATION_REFUND"), any());
    }

    @Test
    void cancelRedemption_alreadyCancelled_returnsFalse() {
        Redemption r = new Redemption();
        r.setReservationCode("XYZ789");
        r.setStatus("CANCELLED");
        when(redemptionRepository.findAll()).thenReturn(List.of(r));
        assertFalse(service.cancelRedemption("XYZ789"));
        verify(mileageService, never()).redeemMiles(any(), anyLong(), any(), any());
    }

    @Test
    void cancelRedemption_notFound_returnsFalse() {
        when(redemptionRepository.findAll()).thenReturn(Collections.emptyList());
        assertFalse(service.cancelRedemption("NOTEXIST"));
    }

    @Test
    void cancelRedemption_onlyMatchingCodeIsCancelled() {
        Redemption other = new Redemption();
        other.setReservationCode("OTHER1");
        other.setStatus("CONFIRMED");
        other.setMemberNumber("AA099");
        other.setMilesCost(12500L);
        Redemption target = new Redemption();
        target.setReservationCode("TARGET1");
        target.setStatus("CANCELLED");
        when(redemptionRepository.findAll()).thenReturn(List.of(other, target));
        assertFalse(service.cancelRedemption("TARGET1"));
        verify(mileageService, never()).redeemMiles(any(), anyLong(), any(), any());
        assertEquals("CONFIRMED", other.getStatus());
    }

    @Test
    void bookAwardFlight_returnsNonNullRedemption() {
        when(mileageService.redeemMiles(eq("AA050"), anyLong(), any(), any())).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        Redemption result = service.bookAwardFlight("AA050", "DFW", "LAX", new Date(), "COACH");
        assertNotNull(result);
        assertEquals("AA050", result.getMemberNumber());
        assertEquals("CONFIRMED", result.getStatus());
    }

    @Test
    void bookAwardFlight_notificationFailure_doesNotRethrow() {
        when(mileageService.redeemMiles(eq("AA007"), anyLong(), any(), any())).thenReturn(true);
        when(redemptionRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        doThrow(new RuntimeException("SMTP")).when(notificationService)
            .sendRedemptionConfirmationEmail(any(), anyLong(), any());
        assertDoesNotThrow(() -> service.bookAwardFlight("AA007", "DFW", "LAX", new Date(), "COACH"));
    }
}
