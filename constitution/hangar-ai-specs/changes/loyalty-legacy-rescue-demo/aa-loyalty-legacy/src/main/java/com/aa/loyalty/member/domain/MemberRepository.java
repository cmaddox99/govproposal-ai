package com.aa.loyalty.member.domain;

import com.aa.loyalty.tier.domain.TierStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.UUID;

@Repository
public interface MemberRepository extends JpaRepository<Member, UUID> {
    Member findByMemberNumber(String memberNumber);
    Member findByEmail(String email);
    List<Member> findByTierStatus(TierStatus tierStatus);

    // VIOLATION: query exposes full member record when only tier field needed
    @Query("SELECT m FROM Member m WHERE m.tierStatus IN ('GOLD','PLATINUM','PLATINUM_PRO','EXECUTIVE_PLATINUM','CONCIERGE_KEY') AND m.active = true")
    List<Member> findAllEliteMembers();

    @Query(value = "SELECT * FROM MEMBER WHERE UPPER(LAST_NAME) LIKE UPPER(:lastName) || '%'", nativeQuery = true)
    List<Member> searchByLastName(@Param("lastName") String lastName);
}
