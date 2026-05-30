package com.aa.loyalty.mileage;

// CHARACTERIZATION TEST — ENG-4.10 / ENG-4.11 (Phase 5 new class — IN_SCOPE immediately)
import com.aa.loyalty.notification.NotificationService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import javax.sql.DataSource;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class MileageAdminServiceTest {

    @Mock MileageRepository mileageRepository;
    @Mock NotificationService notificationService;
    @Mock DataSource dataSource;

    @InjectMocks MileageAdminService service;

    @Test
    void adminAdjustMiles_accountNotFound_throwsRuntimeException() {
        when(mileageRepository.findByMemberNumber("NONE")).thenReturn(null);
        assertThrows(RuntimeException.class,
            () -> service.adminAdjustMiles("NONE", 500L, "bonus", "AGENT01"));
    }

    @Test
    void adminAdjustMiles_positiveAdjustment_addsMiles() {
        MileageAccount account = new MileageAccount("AA001");
        account.setTotalMiles(5000L);
        when(mileageRepository.findByMemberNumber("AA001")).thenReturn(account);
        ArgumentCaptor<MileageAccount> captor = ArgumentCaptor.forClass(MileageAccount.class);
        when(mileageRepository.save(captor.capture())).thenAnswer(i -> i.getArgument(0));
        service.adminAdjustMiles("AA001", 1000L, "goodwill", "AGENT01");
        assertEquals(6000L, account.getTotalMiles());
        MileageAccount saved = captor.getValue();
        assertFalse(saved.getTransactions().isEmpty());
        MileageTransaction txn = saved.getTransactions().get(0);
        assertEquals(account, txn.getAccount());
        assertEquals("ADJUSTMENT", txn.getTransactionType());
        assertEquals(1000L, txn.getMilesAmount());
        assertNotNull(txn.getTransactionDate());
        assertNotNull(txn.getDescription());
        assertTrue(txn.getDescription().contains("AGENT01"));
    }

    @Test
    void adminAdjustMiles_exactlyZeroResult_staysZero() {
        MileageAccount account = new MileageAccount("AA005");
        account.setTotalMiles(500L);
        when(mileageRepository.findByMemberNumber("AA005")).thenReturn(account);
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.adminAdjustMiles("AA005", -500L, "exact zero", "AGENT02");
        assertEquals(0L, account.getTotalMiles());
    }

    @Test
    void adminAdjustMiles_negativeResultClampedToZero() {
        MileageAccount account = new MileageAccount("AA002");
        account.setTotalMiles(100L);
        when(mileageRepository.findByMemberNumber("AA002")).thenReturn(account);
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        service.adminAdjustMiles("AA002", -5000L, "correction", "AGENT01");
        assertEquals(0L, account.getTotalMiles());
    }

    @Test
    void expireMiles_noExpiring_returnsZero() {
        when(mileageRepository.findExpiringAccounts(eq("ACTIVE"), any(Date.class)))
            .thenReturn(Collections.emptyList());
        assertEquals(0, service.expireMiles());
    }

    @Test
    void expireMiles_oneAccount_zerosMilesAndSetsExpiredStatus() {
        MileageAccount account = new MileageAccount("AA003");
        account.setTotalMiles(3000L);
        when(mileageRepository.findExpiringAccounts(eq("ACTIVE"), any(Date.class)))
            .thenReturn(List.of(account));
        ArgumentCaptor<MileageAccount> captor = ArgumentCaptor.forClass(MileageAccount.class);
        when(mileageRepository.save(captor.capture())).thenAnswer(i -> i.getArgument(0));
        assertEquals(1, service.expireMiles());
        assertEquals(0L, account.getTotalMiles());
        assertEquals("MILES_EXPIRED", account.getStatus());
        MileageAccount saved = captor.getValue();
        assertFalse(saved.getTransactions().isEmpty());
        MileageTransaction txn = saved.getTransactions().get(0);
        assertEquals(account, txn.getAccount());
        assertEquals("EXPIRY", txn.getTransactionType());
        assertEquals(-3000L, txn.getMilesAmount());
        assertNotNull(txn.getTransactionDate());
        assertNotNull(txn.getDescription());
    }

    @Test
    void expireMiles_notificationFailure_doesNotRethrow() {
        MileageAccount account = new MileageAccount("AA004");
        account.setTotalMiles(1000L);
        when(mileageRepository.findExpiringAccounts(eq("ACTIVE"), any(Date.class)))
            .thenReturn(List.of(account));
        when(mileageRepository.save(any())).thenAnswer(i -> i.getArgument(0));
        doThrow(new RuntimeException("SMTP")).when(notificationService)
            .sendMilesExpiredEmail(any(), anyLong());
        assertDoesNotThrow(() -> service.expireMiles());
    }

    @Test
    void getMileageSummaryReport_dataSourceUnavailable_returnsEmptyList() {
        // CHARACTERIZATION: DataSource fails in test env (no DB), swallowed — returns []
        List<?> result = service.getMileageSummaryReport(new Date(), new Date());
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

    @Test
    void getMileageSummaryReport_withData_returnsRows() throws Exception {
        // Cover the JDBC success path using mocked Connection/PreparedStatement/ResultSet
        java.sql.Connection conn = mock(java.sql.Connection.class);
        java.sql.PreparedStatement ps = mock(java.sql.PreparedStatement.class);
        java.sql.ResultSet rs = mock(java.sql.ResultSet.class);

        when(dataSource.getConnection()).thenReturn(conn);
        when(conn.prepareStatement(anyString())).thenReturn(ps);
        doNothing().when(ps).setDate(anyInt(), any(java.sql.Date.class));
        when(ps.executeQuery()).thenReturn(rs);
        when(rs.next()).thenReturn(true, false);
        when(rs.getString("MEMBER_NUMBER")).thenReturn("AA001");
        when(rs.getLong("TOTAL")).thenReturn(12500L);

        List<Map<String, Object>> result = service.getMileageSummaryReport(new Date(), new Date());
        assertEquals(1, result.size());
        assertEquals("AA001", result.get(0).get("memberNumber"));
        assertEquals(12500L, result.get(0).get("totalMiles"));
    }
}
