package com.aa.loyalty.mileage.application;

import com.aa.loyalty.events.MilesAccruedEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Date;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import com.aa.loyalty.mileage.domain.AccountStatus;
import com.aa.loyalty.mileage.domain.MemberTierPort;
import com.aa.loyalty.mileage.domain.MileageAccount;
import com.aa.loyalty.mileage.domain.MileageCalculator;
import com.aa.loyalty.mileage.domain.MileageRepository;
import com.aa.loyalty.mileage.domain.MileageTransaction;
import com.aa.loyalty.mileage.domain.TransactionType;

/**
 * ENG-2.1 / ENG-3.1 — Phase 5 extraction from MileageService god class.
 * ENG-2.4 — Bounded context: uses MemberTierPort (ACL) instead of cross-context entity/repo imports.
 * Responsible for: flight mile accrual, account lookup/creation, eligibility checks.
 */
@Service
public class AccrualService {

    private static final Logger LOG = Logger.getLogger(AccrualService.class.getName());

    @Autowired
    private MileageRepository mileageRepository;

    @Autowired
    private MileageCalculator mileageCalculator;

    @Autowired
    private MemberTierPort memberTierPort;

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    @Transactional
    public MileageAccount getOrCreateAccount(String memberNumber) {
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);
        if (account == null) {
            account = new MileageAccount(memberNumber);
            mileageRepository.save(account);
        }
        return account;
    }

    @Transactional
    public long accrueFlightMiles(String memberNumber, String flightNumber,
                                  String origin, String destination,
                                  String bookingClass, Date flightDate,
                                  String ticketNumber) {
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);
        if (account == null) {
            LOG.log(Level.WARNING, "Account not found for accrual: {0}", memberNumber);
            return 0;
        }

        String tier = memberTierPort.getTierStatus(memberNumber);

        long miles = mileageCalculator.calculateAccruedMiles(
            origin, destination, bookingClass, tier, null, false, 1);

        MileageTransaction txn = new MileageTransaction();
        txn.setAccount(account);
        txn.setTransactionType(TransactionType.ACCRUAL);
        txn.setMilesAmount(miles);
        txn.setFlightNumber(flightNumber);
        txn.setOrigin(origin);
        txn.setDestination(destination);
        txn.setFlightDate(flightDate);
        txn.setTicketNumber(ticketNumber);
        txn.setBookingClass(bookingClass);
        txn.setQualifying(true);
        txn.setTransactionDate(new Date());

        account.setLastActivityDate(new Date());
        account.getTransactions().add(txn);

        if (account.getStatus() != AccountStatus.ACTIVE) {
            LOG.log(Level.WARNING, "Cannot accrue miles to non-active account: {0} ({1})", new Object[]{memberNumber, account.getStatus()});
            return 0;
        }
        account.addMiles(miles);  // ENG-2.1 — domain method preserves invariants

        mileageRepository.save(account);

        eventPublisher.publishEvent(new MilesAccruedEvent(memberNumber, miles, flightNumber, "FLIGHT"));

        return miles;
    }

    public MileageAccount getAccountByMemberNumber(String memberNumber) {
        return mileageRepository.findByMemberNumber(memberNumber);
    }

    public Long getTotalMiles(String memberNumber) {
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);
        return account == null ? 0L : account.getTotalMiles();
    }

    public boolean isEligibleForUpgrade(String memberNumber) {
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);
        if (account == null) return false;
        return account.getEliteQualifyingMiles() >= 25000 &&
               account.getEliteQualifyingSegments() >= 30 &&
               AccountStatus.ACTIVE == account.getStatus();
    }

    public boolean isEligibleForGoldStatus(String memberNumber) {
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);
        if (account == null) return false;
        return account.getEliteQualifyingMiles() >= 25000 &&
               account.getEliteQualifyingSegments() >= 30;
    }

    public List<MileageAccount> getAllActiveAccounts() {
        return mileageRepository.findAll();
    }
}
