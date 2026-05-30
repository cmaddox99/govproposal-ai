package com.aa.loyalty.partner;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface PartnerRepository extends JpaRepository<Partner, Long> {
    Partner findByPartnerCode(String partnerCode);
    List<Partner> findByActive(Boolean active);
    List<Partner> findByPartnerType(String partnerType);
}
