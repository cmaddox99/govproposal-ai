package com.aa.loyalty.mileage.application;

import com.aa.loyalty.events.MilesExpiredEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.*;
import java.util.logging.Logger;
import com.aa.loyalty.mileage.domain.AccountNotFoundException;
import com.aa.loyalty.mileage.domain.AccountStatus;
import com.aa.loyalty.mileage.domain.MileageAccount;
import com.aa.loyalty.mileage.domain.MileageRepository;
import com.aa.loyalty.mileage.domain.MileageTransaction;
import com.aa.loyalty.mileage.domain.TransactionType;

/**
 * ENG-2.1 / ENG-3.1 — Phase 5 extraction from MileageService god class.
 * Responsible for: admin adjustments, miles expiry, and reporting.
 */
@Service
public class MileageAdminService {

    private static final Logger LOG = Logger.getLogger(MileageAdminService.class.getName());

    @Autowired
    private MileageRepository mileageRepository;

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    @Autowired
    private DataSource dataSource;

    @Transactional
    public void adminAdjustMiles(String memberNumber, long adjustment, String reason, String agentId) {
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);
        if (account == null) throw new AccountNotFoundException(memberNumber);

        account.setTotalMiles(account.getTotalMiles() + adjustment);
        if (account.getTotalMiles() < 0) account.setTotalMiles(0L);

        MileageTransaction txn = new MileageTransaction();
        txn.setAccount(account);
        txn.setTransactionType(TransactionType.ADJUSTMENT);
        txn.setMilesAmount(adjustment);
        txn.setTransactionDate(new Date());
        txn.setDescription("Agent adjustment by " + agentId + ": " + reason);
        account.getTransactions().add(txn);
        mileageRepository.save(account);
    }

    @Scheduled(cron = "0 0 2 * * ?")
    @Transactional
    public int expireMiles() {
        Date today = new Date();
        List<MileageAccount> expiring = mileageRepository.findExpiringAccounts(AccountStatus.ACTIVE.name(), today);
        int count = 0;
        for (MileageAccount account : expiring) {
            long expiredMiles = account.getTotalMiles();
            account.setTotalMiles(0L);
            account.setStatus(AccountStatus.MILES_EXPIRED);

            MileageTransaction txn = new MileageTransaction();
            txn.setAccount(account);
            txn.setTransactionType(TransactionType.EXPIRY);
            txn.setMilesAmount(-expiredMiles);
            txn.setTransactionDate(today);
            txn.setDescription("Miles expired due to inactivity");
            account.getTransactions().add(txn);

            mileageRepository.save(account);
            count++;

            eventPublisher.publishEvent(new MilesExpiredEvent(account.getMemberNumber(), expiredMiles));
        }
        return count;
    }

    public List<Map<String, Object>> getMileageSummaryReport(Date fromDate, Date toDate) {
        List<Map<String, Object>> results = new ArrayList<>();
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(
                 "SELECT ma.MEMBER_NUMBER, SUM(mt.MILES_AMOUNT) as TOTAL " +
                 "FROM MILEAGE_ACCOUNT ma " +
                 "JOIN MILEAGE_TRANSACTION mt ON mt.ACCOUNT_ID = ma.ID " +
                 "WHERE mt.TRANSACTION_DATE BETWEEN ? AND ? " +
                 "GROUP BY ma.MEMBER_NUMBER")) {
            ps.setDate(1, new java.sql.Date(fromDate.getTime()));
            ps.setDate(2, new java.sql.Date(toDate.getTime()));
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    Map<String, Object> row = new HashMap<>();
                    row.put("memberNumber", rs.getString("MEMBER_NUMBER"));
                    row.put("totalMiles", rs.getLong("TOTAL"));
                    results.add(row);
                }
            }
        } catch (Exception e) {
            LOG.severe("Report query failed: " + e.getMessage());
        }
        return results;
    }
}
