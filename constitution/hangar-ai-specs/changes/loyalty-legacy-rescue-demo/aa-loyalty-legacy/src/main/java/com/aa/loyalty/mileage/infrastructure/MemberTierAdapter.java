package com.aa.loyalty.mileage.infrastructure;

import com.aa.loyalty.member.domain.Member;
import com.aa.loyalty.member.domain.MemberRepository;
import com.aa.loyalty.tier.domain.TierStatus;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import com.aa.loyalty.mileage.domain.MemberTierPort;

/**
 * ENG-2.4 — ACL adapter: the single designated crossing point from mileage → member context.
 * Only this adapter is permitted to import Member and MemberRepository.
 */
@Component
public class MemberTierAdapter implements MemberTierPort {

    @Autowired
    private MemberRepository memberRepository;

    @Override
    public String getTierStatus(String memberNumber) {
        Member member = memberRepository.findByMemberNumber(memberNumber);
        return member != null ? member.getTierStatus().name() : TierStatus.GENERAL.name();
    }
}
