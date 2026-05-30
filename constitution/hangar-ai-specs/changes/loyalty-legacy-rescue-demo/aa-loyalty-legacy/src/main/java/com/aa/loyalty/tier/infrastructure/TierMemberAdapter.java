package com.aa.loyalty.tier.infrastructure;

import com.aa.loyalty.member.domain.Member;
import com.aa.loyalty.member.domain.MemberRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;
import com.aa.loyalty.tier.domain.TierMemberPort;
import com.aa.loyalty.tier.domain.TierStatus;

/**
 * ENG-2.4 — ACL adapter: the single designated crossing point from tier → member context.
 */
@Component
public class TierMemberAdapter implements TierMemberPort {

    @Autowired
    private MemberRepository memberRepository;

    @Override
    public TierStatus getCurrentTier(String memberNumber) {
        Member member = memberRepository.findByMemberNumber(memberNumber);
        return member != null ? member.getTierStatus() : TierStatus.GENERAL;
    }

    @Override
    public void saveTier(String memberNumber, TierStatus newTier) {
        Member member = memberRepository.findByMemberNumber(memberNumber);
        if (member == null) return;
        member.setTierStatus(newTier);
        member.setLastUpdated(new Date());
        memberRepository.save(member);
    }

    @Override
    public List<String> getAllMemberNumbers() {
        return memberRepository.findAll().stream()
            .map(Member::getMemberNumber)
            .collect(Collectors.toList());
    }
}
