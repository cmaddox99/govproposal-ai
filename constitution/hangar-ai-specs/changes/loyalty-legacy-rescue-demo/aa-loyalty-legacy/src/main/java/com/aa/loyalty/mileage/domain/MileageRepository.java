package com.aa.loyalty.mileage.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.Date;
import java.util.List;
import java.util.UUID;

@Repository
public interface MileageRepository extends JpaRepository<MileageAccount, UUID> {

    MileageAccount findByMemberNumber(String memberNumber);

    // VIOLATION: Native SQL query with string concatenation risk if used incorrectly upstream
    @Query(value = "SELECT * FROM MILEAGE_ACCOUNT WHERE STATUS = :status AND MILES_EXPIRY_DATE < :expiryDate", nativeQuery = true)
    List<MileageAccount> findExpiringAccounts(@Param("status") String status, @Param("expiryDate") Date expiryDate);

    @Query("SELECT SUM(t.milesAmount) FROM MileageTransaction t WHERE t.account.memberNumber = :memberNumber AND t.transactionType = 'ACCRUAL'")
    Long sumAccruedMiles(@Param("memberNumber") String memberNumber);

    @Query("SELECT COUNT(t) FROM MileageTransaction t WHERE t.account.memberNumber = :memberNumber")
    Long countTransactions(@Param("memberNumber") String memberNumber);
}
