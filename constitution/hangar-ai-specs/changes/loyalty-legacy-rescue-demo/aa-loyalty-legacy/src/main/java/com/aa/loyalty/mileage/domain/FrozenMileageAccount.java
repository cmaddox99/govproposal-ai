package com.aa.loyalty.mileage.domain;

/**
 * LSP FIX (Phase 5): FrozenMileageAccount no longer extends MileageAccount.
 *
 * ORIGINAL VIOLATION: This class extended MileageAccount but threw
 * IllegalStateException from addMiles() and deductMiles(), breaking the
 * Liskov Substitution Principle. Any code accepting MileageAccount could
 * receive a FrozenMileageAccount at runtime and crash with ISE.
 *
 * FIX APPLIED: Frozen state is now modeled as a boolean flag + freeze() method
 * on MileageAccount itself. The frozen check is part of the BASE CLASS contract —
 * no subtype surprises. AccrualService checks account.isFrozen() before calling
 * addMiles(). No subclass needed; no LSP violation.
 *
 * This class is kept as an empty marker for audit trail. It is no longer used.
 * @deprecated Use MileageAccount.freeze(reason) instead.
 */
@Deprecated
@SuppressWarnings("java:S1133")
public class FrozenMileageAccount {
    // Class intentionally empty — frozen state moved to MileageAccount.
    // See MileageAccount.freeze(), MileageAccount.isFrozen(), MileageAccount.getFreezeReason().
    private FrozenMileageAccount() {}
}
