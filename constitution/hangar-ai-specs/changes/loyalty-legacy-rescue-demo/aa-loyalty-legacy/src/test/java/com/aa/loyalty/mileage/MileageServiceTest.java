package com.aa.loyalty.mileage;

// INTEGRATION-CHARACTERIZATION TEST — ENG-4.10 (Phase 5: behavior extracted to AccrualService/MileageAdminService)
// These tests now verify MileageService correctly DELEGATES to its extracted collaborators.
// Unit behavioral tests for AccrualService → AccrualServiceTest
// Unit behavioral tests for MileageAdminService → MileageAdminServiceTest
import com.aa.loyalty.notification.NotificationService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class MileageServiceTest {

    @Mock AccrualService accrualService;
    @Mock MileageAdminService mileageAdminService;
    @Mock MileageRepository mileageRepository;
    @Mock NotificationService notificationService;

    @InjectMocks MileageService service;

    // ── Delegation to AccrualService ─────────────────────────────────

    @Test
    void getOrCreateAccount_delegatesToAccrualService() {
        MileageAccount account = new MileageAccount("AA001");
        when(accrualService.getOrCreateAccount("AA001")).thenReturn(account);
        assertSame(account, service.getOrCreateAccount("AA001"));
        verify(accrualService).getOrCreateAccount("AA001");
    }

    @Test
    void accrueFlightMiles_delegatesToAccrualService() {
        when(accrualService.accrueFlightMiles(any(), any(), any(), any(), any(), any(), any())).thenReturn(1543L);
        long result = service.accrueFlightMiles("AA001", "AA100", "DFW", "LAX", "Y", new Date(), null);
        assertEquals(1543L, result);
        verify(accrualService).accrueFlightMiles(eq("AA001"), eq("AA100"), eq("DFW"), eq("LAX"), eq("Y"), any(), isNull());
    }

    @Test
    void getTotalMiles_delegatesToAccrualService() {
        when(accrualService.getTotalMiles("AA001")).thenReturn(42000L);
        assertEquals(42000L, service.getTotalMiles("AA001"));
        verify(accrualService).getTotalMiles("AA001");
    }

    @Test
    void getAccountByMemberNumber_delegatesToAccrualService() {
        MileageAccount account = new MileageAccount("AA001");
        when(accrualService.getAccountByMemberNumber("AA001")).thenReturn(account);
        assertSame(account, service.getAccountByMemberNumber("AA001"));
    }

    @Test
    void getAllActiveAccounts_delegatesToAccrualService() {
        List<MileageAccount> all = List.of(new MileageAccount("AA001"));
        when(accrualService.getAllActiveAccounts()).thenReturn(all);
        assertEquals(all, service.getAllActiveAccounts());
    }

    @Test
    void isEligibleForUpgrade_delegatesToAccrualService() {
        when(accrualService.isEligibleForUpgrade("AA001")).thenReturn(true);
        assertTrue(service.isEligibleForUpgrade("AA001"));
    }

    @Test
    void isEligibleForUpgrade_false_returnsFalse() {
        when(accrualService.isEligibleForUpgrade("AA001")).thenReturn(false);
        assertFalse(service.isEligibleForUpgrade("AA001"));
    }

    @Test
    void isEligibleForGoldStatus_delegatesToAccrualService() {
        when(accrualService.isEligibleForGoldStatus("AA001")).thenReturn(true);
        assertTrue(service.isEligibleForGoldStatus("AA001"));
    }

    @Test
    void isEligibleForGoldStatus_false_returnsFalse() {
        when(accrualService.isEligibleForGoldStatus("AA001")).thenReturn(false);
        assertFalse(service.isEligibleForGoldStatus("AA001"));
    }

    // ── Delegation to MileageAdminService ────────────────────────────

    @Test
    void adminAdjustMiles_delegatesToMileageAdminService() {
        doNothing().when(mileageAdminService).adminAdjustMiles("AA001", 500L, "bonus", "AGENT01");
        service.adminAdjustMiles("AA001", 500L, "bonus", "AGENT01");
        verify(mileageAdminService).adminAdjustMiles("AA001", 500L, "bonus", "AGENT01");
    }

    @Test
    void expireMiles_delegatesToMileageAdminService() {
        when(mileageAdminService.expireMiles()).thenReturn(3);
        assertEquals(3, service.expireMiles());
        verify(mileageAdminService).expireMiles();
    }

    @Test
    void getMileageSummaryReport_delegatesToMileageAdminService() {
        List<Map<String, Object>> report = List.of(Map.of("memberNumber", "AA001", "totalMiles", 5000L));
        when(mileageAdminService.getMileageSummaryReport(any(), any())).thenReturn(report);
        assertEquals(report, service.getMileageSummaryReport(new Date(), new Date()));
        verify(mileageAdminService).getMileageSummaryReport(any(), any());
    }

    // ── Redemption (stays in MileageService) ─────────────────────────

    @Test
    void redeemMiles_accountNotFound_returnsFalse() {
        when(mileageRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertFalse(service.redeemMiles("NONE", 5000L, "AWARD", "test"));
    }

    @Test
    void redeemMiles_insufficientMiles_returnsFalse() {
        MileageAccount account = new MileageAccount("AA002");
        account.setTotalMiles(1000L);
        when(mileageRepository.findByMemberNumber("AA002")).thenReturn(account);
        assertFalse(service.redeemMiles("AA002", 5000L, "AWARD", "test"));
    }

    @Test
    void redeemMiles_sufficientMiles_deductsAndReturnsTrue() {
        MileageAccount account = new MileageAccount("AA003");
        account.setTotalMiles(10000L);
        when(mileageRepository.findByMemberNumber("AA003")).thenReturn(account);
        org.mockito.ArgumentCaptor<MileageAccount> captor = org.mockito.ArgumentCaptor.forClass(MileageAccount.class);
        when(mileageRepository.save(captor.capture())).thenAnswer(i -> i.getArgument(0));
        assertTrue(service.redeemMiles("AA003", 5000L, "AWARD", "test"));
        assertEquals(5000L, account.getTotalMiles());
        MileageAccount saved = captor.getValue();
        assertNotNull(saved.getLastActivityDate());
        assertFalse(saved.getTransactions().isEmpty());
        MileageTransaction txn = saved.getTransactions().get(0);
        assertEquals("REDEMPTION", txn.getTransactionType());
        assertEquals(-5000L, txn.getMilesAmount());
        assertNotNull(txn.getTransactionDate());
        assertEquals("test", txn.getDescription());
        assertEquals(account, txn.getAccount());
    }

    @Test
    void redeemMiles_exactMilesAvailable_succeeds() {
        MileageAccount account = new MileageAccount("AA005");
        account.setTotalMiles(5000L);
        when(mileageRepository.findByMemberNumber("AA005")).thenReturn(account);
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        assertTrue(service.redeemMiles("AA005", 5000L, "AWARD", "exact"));
        assertEquals(0L, account.getTotalMiles());
    }

    @Test
    void redeemMiles_oneMoreThanAvailable_returnsFalse() {
        MileageAccount account = new MileageAccount("AA006");
        account.setTotalMiles(4999L);
        when(mileageRepository.findByMemberNumber("AA006")).thenReturn(account);
        assertFalse(service.redeemMiles("AA006", 5000L, "AWARD", "test"));
    }

    @Test
    void redeemMiles_notificationFailure_stillReturnsTrue() {
        MileageAccount account = new MileageAccount("AA004");
        account.setTotalMiles(10000L);
        when(mileageRepository.findByMemberNumber("AA004")).thenReturn(account);
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        doThrow(new RuntimeException("SMTP")).when(notificationService)
            .sendRedemptionConfirmationEmail(any(), anyLong(), any());
        assertTrue(service.redeemMiles("AA004", 5000L, "UPGRADE", "test"));
    }
}
