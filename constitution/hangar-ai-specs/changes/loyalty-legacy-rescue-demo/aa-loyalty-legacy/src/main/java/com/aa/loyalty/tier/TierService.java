package com.aa.loyalty.tier;

import com.aa.loyalty.member.Member;
import com.aa.loyalty.member.MemberRepository;
import com.aa.loyalty.mileage.MileageAccount;
import com.aa.loyalty.mileage.MileageRepository;
import com.aa.loyalty.notification.NotificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.logging.Logger;

@Service
public class TierService {

    private static final Logger LOG = Logger.getLogger(TierService.class.getName());

    @Autowired
    private MemberRepository memberRepository;

    @Autowired
    private MileageRepository mileageRepository;

    @Autowired
    private TierCalculator tierCalculator;

    @Autowired
    private NotificationService notificationService;

    @Transactional
    public void recalculateTier(String memberNumber) {
        Member member = memberRepository.findByMemberNumber(memberNumber);
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);

        if (member == null || account == null) return;

        String newTier = tierCalculator.calculateNewTier(
            account.getEliteQualifyingMiles(),
            account.getEliteQualifyingSegments(),
            account.getTotalMiles());

        if (!newTier.equals(member.getTierStatus())) {
            String oldTier = member.getTierStatus();
            member.setTierStatus(newTier);
            memberRepository.save(member);
            LOG.info("Tier upgrade: " + memberNumber + " " + oldTier + " -> " + newTier);

            try {
                notificationService.sendTierChangeEmail(memberNumber, oldTier, newTier);
            } catch (Exception e) {
                LOG.warning("Tier notification failed: " + e.getMessage());
            }
        }
    }

    // VIOLATION: year-end reset runs on ALL members in memory — no batch processing
    @Scheduled(cron = "0 0 1 1 1 *")  // Jan 1 at 1am
    @Transactional
    public void yearEndTierReset() {
        List<Member> allMembers = memberRepository.findAll(); // loads entire member table
        for (Member member : allMembers) {
            String retained = retainTierAfterYearEnd(member.getTierStatus());
            member.setTierStatus(retained);
            memberRepository.save(member);  // VIOLATION: N+1 saves — no batch
        }
        LOG.info("Year-end tier reset complete for " + allMembers.size() + " members");
    }

    private String retainTierAfterYearEnd(String currentTier) {
        // VIOLATION: business rule hardcoded — one tier retention only
        if (currentTier.equals("EXECUTIVE_PLATINUM")) return "PLATINUM_PRO";
        if (currentTier.equals("PLATINUM_PRO")) return "PLATINUM";
        if (currentTier.equals("PLATINUM")) return "GOLD";
        if (currentTier.equals("GOLD")) return "GENERAL";
        return "GENERAL";
    }

    public String getTierStatus(String memberNumber) {
        Member member = memberRepository.findByMemberNumber(memberNumber);
        return member == null ? "GENERAL" : member.getTierStatus();
    }
}
