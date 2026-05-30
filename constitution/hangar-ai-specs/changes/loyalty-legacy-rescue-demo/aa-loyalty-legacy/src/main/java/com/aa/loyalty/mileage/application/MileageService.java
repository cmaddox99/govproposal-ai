package com.aa.loyalty.mileage.application;

import com.aa.loyalty.events.MilesRedeemedEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;
import com.aa.loyalty.mileage.domain.MileageAccount;
import com.aa.loyalty.mileage.domain.MileageRepository;
import com.aa.loyalty.mileage.domain.MileageTransaction;
import com.aa.loyalty.mileage.domain.TransactionType;

/**
 * ENG-3.1 / ENG-2.1 — Phase 5 refactor: MileageService is now a thin coordinator.
 * Accrual logic → AccrualService
 * Admin/expiry logic → MileageAdminService
 * Redemption stays here (interface contract used by RedemptionService and controllers).
 */
@Service
public class MileageService {

    private static final Logger LOG = Logger.getLogger(MileageService.class.getName());

    @Autowired
    private AccrualService accrualService;

    @Autowired
    private MileageAdminService mileageAdminService;

    @Autowired
    private MileageRepository mileageRepository;

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    // ── Delegation to AccrualService ─────────────────────────────────

    @Transactional
    public MileageAccount getOrCreateAccount(String memberNumber) {
        return accrualService.getOrCreateAccount(memberNumber);
    }

    @Transactional
    public long accrueFlightMiles(String memberNumber, String flightNumber,
                                  String origin, String destination,
                                  String bookingClass, Date flightDate,
                                  String ticketNumber) {
        return accrualService.accrueFlightMiles(
            memberNumber, flightNumber, origin, destination, bookingClass, flightDate, ticketNumber);
    }

    public MileageAccount getAccountByMemberNumber(String memberNumber) {
        return accrualService.getAccountByMemberNumber(memberNumber);
    }

    public Long getTotalMiles(String memberNumber) {
        return accrualService.getTotalMiles(memberNumber);
    }

    public boolean isEligibleForUpgrade(String memberNumber) {
        return accrualService.isEligibleForUpgrade(memberNumber);
    }

    public boolean isEligibleForGoldStatus(String memberNumber) {
        return accrualService.isEligibleForGoldStatus(memberNumber);
    }

    public List<MileageAccount> getAllActiveAccounts() {
        return accrualService.getAllActiveAccounts();
    }

    // ── Delegation to MileageAdminService ────────────────────────────

    @Transactional
    public void adminAdjustMiles(String memberNumber, long adjustment, String reason, String agentId) {
        mileageAdminService.adminAdjustMiles(memberNumber, adjustment, reason, agentId);
    }

    public int expireMiles() {
        return mileageAdminService.expireMiles();
    }

    public List<Map<String, Object>> getMileageSummaryReport(Date fromDate, Date toDate) {
        return mileageAdminService.getMileageSummaryReport(fromDate, toDate);
    }

    // ── Redemption (stays here — interface contract for RedemptionService) ──

    @Transactional
    public boolean redeemMiles(String memberNumber, long milesRequested, String redemptionType, String description) {
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);
        if (account == null) return false;

        if (account.getTotalMiles() < milesRequested) {
            LOG.info("Insufficient miles for " + memberNumber);
            return false;
        }

        account.setTotalMiles(account.getTotalMiles() - milesRequested);
        account.setLastActivityDate(new Date());

        MileageTransaction txn = new MileageTransaction();
        txn.setAccount(account);
        txn.setTransactionType(TransactionType.REDEMPTION);
        txn.setMilesAmount(-milesRequested);
        txn.setTransactionDate(new Date());
        txn.setDescription(description);
        account.getTransactions().add(txn);

        mileageRepository.save(account);

        eventPublisher.publishEvent(new MilesRedeemedEvent(memberNumber, milesRequested, redemptionType));

        return true;
    }
}

