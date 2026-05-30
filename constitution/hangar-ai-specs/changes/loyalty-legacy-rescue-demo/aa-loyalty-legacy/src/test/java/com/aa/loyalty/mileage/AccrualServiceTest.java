package com.aa.loyalty.mileage;

// CHARACTERIZATION TEST — ENG-4.10 / ENG-4.11 (Phase 5 new class — IN_SCOPE immediately)
import com.aa.loyalty.member.Member;
import com.aa.loyalty.member.MemberRepository;
import com.aa.loyalty.mileage.MileageTransaction;
import com.aa.loyalty.notification.NotificationService;
import com.aa.loyalty.tier.TierService;
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
class AccrualServiceTest {

    @Mock MileageRepository mileageRepository;
    @Mock MileageCalculator mileageCalculator;
    @Mock MemberRepository memberRepository;
    @Mock NotificationService notificationService;
    @Mock TierService tierService;

    @InjectMocks AccrualService service;

    @Test
    void getOrCreateAccount_existing_returnsExisting() {
        MileageAccount account = new MileageAccount("AA001");
        when(mileageRepository.findByMemberNumber("AA001")).thenReturn(account);
        assertSame(account, service.getOrCreateAccount("AA001"));
        verify(mileageRepository, never()).save(any());
    }

    @Test
    void getOrCreateAccount_notFound_createsNew() {
        when(mileageRepository.findByMemberNumber("AA002")).thenReturn(null);
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        MileageAccount result = service.getOrCreateAccount("AA002");
        assertEquals("AA002", result.getMemberNumber());
        verify(mileageRepository).save(any(MileageAccount.class));
    }

    @Test
    void accrueFlightMiles_accountNotFound_returnsZero() {
        when(mileageRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertEquals(0L, service.accrueFlightMiles("NONE", "AA100", "DFW", "LAX", "Y", new Date(), null));
    }

    @Test
    void accrueFlightMiles_memberFound_calculatesAndSaves() {
        MileageAccount account = new MileageAccount("AA003");
        Member member = new Member();
        member.setTierStatus("GOLD");
        when(mileageRepository.findByMemberNumber("AA003")).thenReturn(account);
        when(memberRepository.findByMemberNumber("AA003")).thenReturn(member);
        when(mileageCalculator.calculateAccruedMiles("DFW", "LAX", "Y", "GOLD", null, false, 1)).thenReturn(1543L);
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        assertEquals(1543L, service.accrueFlightMiles("AA003", "AA100", "DFW", "LAX", "Y", new Date(), "TKT01"));
        verify(tierService).recalculateTier("AA003");
    }

    @Test
    void accrueFlightMiles_incrementsMilesCorrectly() {
        MileageAccount account = new MileageAccount("AA012");
        account.setTotalMiles(10000L);
        account.setQualifyingMiles(8000L);
        account.setEliteQualifyingMiles(6000L);
        Member member = new Member(); member.setTierStatus("GENERAL");
        when(mileageRepository.findByMemberNumber("AA012")).thenReturn(account);
        when(memberRepository.findByMemberNumber("AA012")).thenReturn(member);
        when(mileageCalculator.calculateAccruedMiles(any(), any(), any(), any(), any(), anyBoolean(), anyInt())).thenReturn(1500L);
        ArgumentCaptor<MileageAccount> captor = ArgumentCaptor.forClass(MileageAccount.class);
        when(mileageRepository.save(captor.capture())).thenAnswer(i -> i.getArgument(0));
        long result = service.accrueFlightMiles("AA012", "AA200", "DFW", "LAX", "Y", new Date(), null);
        assertEquals(1500L, result);
        MileageAccount saved = captor.getValue();
        assertEquals(11500L, saved.getTotalMiles());
        assertEquals(9500L, saved.getQualifyingMiles());
        assertEquals(7500L, saved.getEliteQualifyingMiles());
        assertNotNull(saved.getLastActivityDate());
    }

    @Test
    void accrueFlightMiles_verifiesTransactionFields() {
        MileageAccount account = new MileageAccount("AA013");
        Member member = new Member(); member.setTierStatus("GOLD");
        Date flightDate = new Date(1000000L);
        when(mileageRepository.findByMemberNumber("AA013")).thenReturn(account);
        when(memberRepository.findByMemberNumber("AA013")).thenReturn(member);
        when(mileageCalculator.calculateAccruedMiles("DFW", "LAX", "Y", "GOLD", null, false, 1)).thenReturn(1235L);
        ArgumentCaptor<MileageAccount> captor = ArgumentCaptor.forClass(MileageAccount.class);
        when(mileageRepository.save(captor.capture())).thenAnswer(i -> i.getArgument(0));
        service.accrueFlightMiles("AA013", "AA100", "DFW", "LAX", "Y", flightDate, "TKT99");
        MileageAccount saved = captor.getValue();
        assertFalse(saved.getTransactions().isEmpty());
        MileageTransaction txn = saved.getTransactions().get(0);
        assertEquals(account, txn.getAccount());
        assertEquals("ACCRUAL", txn.getTransactionType());
        assertEquals(1235L, txn.getMilesAmount());
        assertEquals("AA100", txn.getFlightNumber());
        assertEquals("DFW", txn.getOrigin());
        assertEquals("LAX", txn.getDestination());
        assertEquals(flightDate, txn.getFlightDate());
        assertEquals("TKT99", txn.getTicketNumber());
        assertEquals("Y", txn.getBookingClass());
        assertTrue(txn.getQualifying());
        assertNotNull(txn.getTransactionDate());
    }

    @Test
    void isEligibleForUpgrade_inactiveAccount_returnsFalse() {
        MileageAccount account = new MileageAccount("AA015");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(30);
        account.setStatus("INACTIVE");
        when(mileageRepository.findByMemberNumber("AA015")).thenReturn(account);
        assertFalse(service.isEligibleForUpgrade("AA015"));
    }

    @Test
    void accrueFlightMiles_memberNotFound_usesGeneralTier() {
        MileageAccount account = new MileageAccount("AA004");
        when(mileageRepository.findByMemberNumber("AA004")).thenReturn(account);
        when(memberRepository.findByMemberNumber("AA004")).thenReturn(null);
        when(mileageCalculator.calculateAccruedMiles("DFW", "LAX", "Y", "GENERAL", null, false, 1)).thenReturn(1235L);
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        assertEquals(1235L, service.accrueFlightMiles("AA004", "AA100", "DFW", "LAX", "Y", new Date(), null));
    }

    @Test
    void accrueFlightMiles_notificationFailure_doesNotRethrow() {
        MileageAccount account = new MileageAccount("AA005");
        Member member = new Member(); member.setTierStatus("GENERAL");
        when(mileageRepository.findByMemberNumber("AA005")).thenReturn(account);
        when(memberRepository.findByMemberNumber("AA005")).thenReturn(member);
        when(mileageCalculator.calculateAccruedMiles(any(), any(), any(), any(), any(), anyBoolean(), anyInt())).thenReturn(1000L);
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        doThrow(new RuntimeException("SMTP")).when(notificationService).sendMilesAccruedEmail(any(), anyLong(), any());
        assertDoesNotThrow(() -> service.accrueFlightMiles("AA005", "AA100", "DFW", "LAX", "Y", new Date(), null));
    }

    @Test
    void getTotalMiles_accountNotFound_returnsZero() {
        when(mileageRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertEquals(0L, service.getTotalMiles("NONE"));
    }

    @Test
    void getTotalMiles_accountFound_returnsMiles() {
        MileageAccount account = new MileageAccount("AA006");
        account.setTotalMiles(42000L);
        when(mileageRepository.findByMemberNumber("AA006")).thenReturn(account);
        assertEquals(42000L, service.getTotalMiles("AA006"));
    }

    @Test
    void getAccountByMemberNumber_delegatesToRepository() {
        MileageAccount account = new MileageAccount("AA007");
        when(mileageRepository.findByMemberNumber("AA007")).thenReturn(account);
        assertSame(account, service.getAccountByMemberNumber("AA007"));
    }

    @Test
    void isEligibleForUpgrade_accountNotFound_returnsFalse() {
        when(mileageRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertFalse(service.isEligibleForUpgrade("NONE"));
    }

    @Test
    void isEligibleForUpgrade_meetsThreshold_returnsTrue() {
        MileageAccount account = new MileageAccount("AA008");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(30);
        account.setStatus("ACTIVE");
        when(mileageRepository.findByMemberNumber("AA008")).thenReturn(account);
        assertTrue(service.isEligibleForUpgrade("AA008"));
    }

    @Test
    void isEligibleForUpgrade_insufficientMiles_returnsFalse() {
        MileageAccount account = new MileageAccount("AA009");
        account.setEliteQualifyingMiles(5000L);
        account.setEliteQualifyingSegments(30);
        account.setStatus("ACTIVE");
        when(mileageRepository.findByMemberNumber("AA009")).thenReturn(account);
        assertFalse(service.isEligibleForUpgrade("AA009"));
    }

    @Test
    void isEligibleForUpgrade_justBelowMilesThreshold_returnsFalse() {
        MileageAccount account = new MileageAccount("AA013");
        account.setEliteQualifyingMiles(24999L);
        account.setEliteQualifyingSegments(30);
        account.setStatus("ACTIVE");
        when(mileageRepository.findByMemberNumber("AA013")).thenReturn(account);
        assertFalse(service.isEligibleForUpgrade("AA013"));
    }

    @Test
    void isEligibleForUpgrade_insufficientSegments_returnsFalse() {
        MileageAccount account = new MileageAccount("AA014");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(29);
        account.setStatus("ACTIVE");
        when(mileageRepository.findByMemberNumber("AA014")).thenReturn(account);
        assertFalse(service.isEligibleForUpgrade("AA014"));
    }

    @Test
    void isEligibleForGoldStatus_accountNotFound_returnsFalse() {
        when(mileageRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertFalse(service.isEligibleForGoldStatus("NONE"));
    }

    @Test
    void isEligibleForGoldStatus_meetsThreshold_returnsTrue() {
        MileageAccount account = new MileageAccount("AA010");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(30);
        when(mileageRepository.findByMemberNumber("AA010")).thenReturn(account);
        assertTrue(service.isEligibleForGoldStatus("AA010"));
    }

    @Test
    void isEligibleForGoldStatus_justBelowMilesThreshold_returnsFalse() {
        MileageAccount account = new MileageAccount("AA015");
        account.setEliteQualifyingMiles(24999L);
        account.setEliteQualifyingSegments(30);
        when(mileageRepository.findByMemberNumber("AA015")).thenReturn(account);
        assertFalse(service.isEligibleForGoldStatus("AA015"));
    }

    @Test
    void isEligibleForGoldStatus_insufficientSegments_returnsFalse() {
        MileageAccount account = new MileageAccount("AA016");
        account.setEliteQualifyingMiles(25000L);
        account.setEliteQualifyingSegments(29);
        when(mileageRepository.findByMemberNumber("AA016")).thenReturn(account);
        assertFalse(service.isEligibleForGoldStatus("AA016"));
    }

    @Test
    void getAllActiveAccounts_delegatesToRepository() {
        List<MileageAccount> all = List.of(new MileageAccount("AA011"));
        when(mileageRepository.findAll()).thenReturn(all);
        assertEquals(all, service.getAllActiveAccounts());
    }
}
