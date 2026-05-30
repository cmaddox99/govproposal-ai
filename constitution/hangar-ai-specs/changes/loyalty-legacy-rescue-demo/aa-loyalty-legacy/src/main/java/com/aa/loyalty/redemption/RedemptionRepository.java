package com.aa.loyalty.redemption;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface RedemptionRepository extends JpaRepository<Redemption, Long> {
    List<Redemption> findByMemberNumber(String memberNumber);
    List<Redemption> findByStatus(String status);

    @Query("SELECT r FROM Redemption r WHERE r.memberNumber = :memberNumber AND r.status = 'PENDING'")
    List<Redemption> findPendingByMember(@Param("memberNumber") String memberNumber);
}
