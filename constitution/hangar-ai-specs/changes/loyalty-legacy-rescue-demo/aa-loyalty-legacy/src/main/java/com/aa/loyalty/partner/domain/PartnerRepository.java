package com.aa.loyalty.partner.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.UUID;

@Repository
public interface PartnerRepository extends JpaRepository<Partner, UUID> {
    Partner findByPartnerCode(String partnerCode);
    List<Partner> findByActive(Boolean active);
    List<Partner> findByPartnerType(String partnerType);
}
