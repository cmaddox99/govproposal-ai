package com.aa.loyalty.mileage.domain;

/**
 * ENG-2.4 — Anti-corruption layer port: mileage context's read-only view of member tier.
 * AccrualService depends on this interface, not on MemberRepository or Member entity.
 */
public interface MemberTierPort {
    /** Returns the tier name (e.g. "GOLD") for the given member, or "GENERAL" if not found. */
    String getTierStatus(String memberNumber);
}
