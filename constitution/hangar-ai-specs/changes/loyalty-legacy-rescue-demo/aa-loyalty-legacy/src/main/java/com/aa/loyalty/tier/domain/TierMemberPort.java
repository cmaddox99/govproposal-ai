package com.aa.loyalty.tier.domain;

import java.util.List;

/**
 * ENG-2.4 — ACL port: tier context's read/write view of member tier data.
 * TierService depends on this interface, not on MemberRepository or Member entity.
 */
public interface TierMemberPort {
    TierStatus getCurrentTier(String memberNumber);
    void saveTier(String memberNumber, TierStatus newTier);
    List<String> getAllMemberNumbers();
}
