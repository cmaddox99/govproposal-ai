package com.aa.loyalty.tier.infrastructure;

import com.aa.loyalty.mileage.domain.MileageAccount;
import com.aa.loyalty.mileage.domain.MileageRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import com.aa.loyalty.tier.domain.MileageStatsView;
import com.aa.loyalty.tier.domain.TierMileagePort;

/**
 * ENG-2.4 — ACL adapter: the single designated crossing point from tier → mileage context.
 */
@Component
public class TierMileageAdapter implements TierMileagePort {

    @Autowired
    private MileageRepository mileageRepository;

    @Override
    public MileageStatsView getMileageStats(String memberNumber) {
        MileageAccount account = mileageRepository.findByMemberNumber(memberNumber);
        if (account == null) return MileageStatsView.zero();
        return new MileageStatsView(
            account.getEliteQualifyingMiles(),
            account.getEliteQualifyingSegments(),
            account.getTotalMiles()
        );
    }
}
