package com.aa.loyalty.tier.application;

import com.aa.loyalty.events.MilesAccruedEvent;
import com.aa.loyalty.events.TierChangedEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import com.aa.loyalty.tier.domain.MileageStatsView;
import com.aa.loyalty.tier.domain.TierBenefitCalculator;
import com.aa.loyalty.tier.domain.TierCalculator;
import com.aa.loyalty.tier.domain.TierMemberPort;
import com.aa.loyalty.tier.domain.TierMileagePort;
import com.aa.loyalty.tier.domain.TierStatus;

/**
 * ENG-2.4 — Bounded context: uses TierMemberPort and TierMileagePort (ACL) instead of
 * cross-context entity/repository imports.
 */
@Service
public class TierService {

    private static final Logger LOG = Logger.getLogger(TierService.class.getName());

    @Autowired
    private TierMemberPort tierMemberPort;

    @Autowired
    private TierMileagePort tierMileagePort;

    @Autowired
    private TierCalculator tierCalculator;

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    @Autowired
    private TierBenefitCalculator tierBenefitCalculator;

    @EventListener
    @Transactional
    public void onMilesAccrued(MilesAccruedEvent event) {
        recalculateTier(event.getMemberNumber());
    }

    @Transactional
    public void recalculateTier(String memberNumber) {
        TierStatus currentTier = tierMemberPort.getCurrentTier(memberNumber);
        MileageStatsView stats = tierMileagePort.getMileageStats(memberNumber);

        if (currentTier == TierStatus.GENERAL
                && stats.getEliteQualifyingMiles() == 0
                && stats.getEliteQualifyingSegments() == 0
                && stats.getTotalMiles() == 0) {
            return;
        }

        String newTier = tierCalculator.calculateNewTier(
            stats.getEliteQualifyingMiles(),
            stats.getEliteQualifyingSegments(),
            stats.getTotalMiles());

        TierStatus newTierEnum = TierStatus.valueOf(newTier);
        if (newTierEnum != currentTier) {
            LOG.log(Level.INFO, "Tier upgrade: {0} {1} -> {2}", new Object[]{memberNumber, currentTier, newTier});
            String benefitSummary = tierBenefitCalculator.getTierBenefitSummary(newTier);
            LOG.log(Level.INFO, "New benefits for {0}: {1}", new Object[]{memberNumber, benefitSummary});
            tierMemberPort.saveTier(memberNumber, newTierEnum);
            eventPublisher.publishEvent(new TierChangedEvent(memberNumber, currentTier, newTierEnum));
        }
    }

    @Scheduled(cron = "0 0 1 1 1 *")
    @Transactional
    public void yearEndTierReset() {
        List<String> allNumbers = tierMemberPort.getAllMemberNumbers();
        for (String memberNumber : allNumbers) {
            TierStatus current = tierMemberPort.getCurrentTier(memberNumber);
            TierStatus retained = retainTierAfterYearEnd(current);
            tierMemberPort.saveTier(memberNumber, retained);
        }
        LOG.log(Level.INFO, "Year-end tier reset complete for {0} members", allNumbers.size());
    }

    private TierStatus retainTierAfterYearEnd(TierStatus currentTier) {
        if (currentTier == TierStatus.EXECUTIVE_PLATINUM) return TierStatus.PLATINUM_PRO;
        if (currentTier == TierStatus.PLATINUM_PRO) return TierStatus.PLATINUM;
        if (currentTier == TierStatus.PLATINUM) return TierStatus.GOLD;
        if (currentTier == TierStatus.GOLD) return TierStatus.GENERAL;
        return TierStatus.GENERAL;
    }

    public String getTierStatus(String memberNumber) {
        return tierMemberPort.getCurrentTier(memberNumber).name();
    }
}
