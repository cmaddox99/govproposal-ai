#!/usr/bin/env python3
"""DDD Phase 5 Layered Architecture Refactoring Script"""
import os
import re

PROJECT = "/Users/979925/Repos/governance/hangar-ai-constitution/hangar-ai-specs/changes/loyalty-legacy-rescue-demo/aa-loyalty-legacy"
MAIN = os.path.join(PROJECT, "src/main/java/com/aa/loyalty")
SRC = os.path.join(PROJECT, "src")

# MOVES: (old_relative_to_MAIN, new_relative_to_MAIN, new_package)
MOVES = [
    # member/domain
    ("member/Member.java",                 "member/domain/Member.java",                 "com.aa.loyalty.member.domain"),
    ("member/Address.java",                "member/domain/Address.java",                "com.aa.loyalty.member.domain"),
    ("member/EmailAddress.java",           "member/domain/EmailAddress.java",           "com.aa.loyalty.member.domain"),
    ("member/MemberNumber.java",           "member/domain/MemberNumber.java",           "com.aa.loyalty.member.domain"),
    ("member/MemberRepository.java",       "member/domain/MemberRepository.java",       "com.aa.loyalty.member.domain"),
    ("member/MemberAdminPort.java",        "member/domain/MemberAdminPort.java",        "com.aa.loyalty.member.domain"),
    ("member/MemberCompliancePort.java",   "member/domain/MemberCompliancePort.java",   "com.aa.loyalty.member.domain"),
    ("member/MemberFraudPort.java",        "member/domain/MemberFraudPort.java",        "com.aa.loyalty.member.domain"),
    ("member/MemberSelfServicePort.java",  "member/domain/MemberSelfServicePort.java",  "com.aa.loyalty.member.domain"),
    ("member/EnrollmentRequest.java",      "member/domain/EnrollmentRequest.java",      "com.aa.loyalty.member.domain"),
    ("member/ProfileUpdateRequest.java",   "member/domain/ProfileUpdateRequest.java",   "com.aa.loyalty.member.domain"),
    # member/application
    ("member/MemberService.java",          "member/application/MemberService.java",          "com.aa.loyalty.member.application"),
    ("member/MemberManagementService.java","member/application/MemberManagementService.java","com.aa.loyalty.member.application"),
    # member/infrastructure
    ("member/MemberController.java",       "member/infrastructure/MemberController.java",    "com.aa.loyalty.member.infrastructure"),
    # mileage/domain
    ("mileage/MileageAccount.java",        "mileage/domain/MileageAccount.java",        "com.aa.loyalty.mileage.domain"),
    ("mileage/MileageTransaction.java",    "mileage/domain/MileageTransaction.java",    "com.aa.loyalty.mileage.domain"),
    ("mileage/AccountStatus.java",         "mileage/domain/AccountStatus.java",         "com.aa.loyalty.mileage.domain"),
    ("mileage/TransactionType.java",       "mileage/domain/TransactionType.java",       "com.aa.loyalty.mileage.domain"),
    ("mileage/AccountNotFoundException.java","mileage/domain/AccountNotFoundException.java","com.aa.loyalty.mileage.domain"),
    ("mileage/FrozenMileageAccount.java",  "mileage/domain/FrozenMileageAccount.java",  "com.aa.loyalty.mileage.domain"),
    ("mileage/MileageRepository.java",     "mileage/domain/MileageRepository.java",     "com.aa.loyalty.mileage.domain"),
    ("mileage/MileageCalculationPort.java","mileage/domain/MileageCalculationPort.java","com.aa.loyalty.mileage.domain"),
    ("mileage/MemberTierPort.java",        "mileage/domain/MemberTierPort.java",        "com.aa.loyalty.mileage.domain"),
    ("mileage/MileageCalculator.java",     "mileage/domain/MileageCalculator.java",     "com.aa.loyalty.mileage.domain"),
    # mileage/application
    ("mileage/MileageService.java",        "mileage/application/MileageService.java",        "com.aa.loyalty.mileage.application"),
    ("mileage/MileageAdminService.java",   "mileage/application/MileageAdminService.java",   "com.aa.loyalty.mileage.application"),
    ("mileage/AccrualService.java",        "mileage/application/AccrualService.java",        "com.aa.loyalty.mileage.application"),
    # mileage/infrastructure
    ("mileage/MileageController.java",     "mileage/infrastructure/MileageController.java",  "com.aa.loyalty.mileage.infrastructure"),
    ("mileage/MemberTierAdapter.java",     "mileage/infrastructure/MemberTierAdapter.java",  "com.aa.loyalty.mileage.infrastructure"),
    # tier/domain
    ("tier/TierStatus.java",               "tier/domain/TierStatus.java",               "com.aa.loyalty.tier.domain"),
    ("tier/TierBenefits.java",             "tier/domain/TierBenefits.java",             "com.aa.loyalty.tier.domain"),
    ("tier/MileageStatsView.java",         "tier/domain/MileageStatsView.java",         "com.aa.loyalty.tier.domain"),
    ("tier/TierMemberPort.java",           "tier/domain/TierMemberPort.java",           "com.aa.loyalty.tier.domain"),
    ("tier/TierMileagePort.java",          "tier/domain/TierMileagePort.java",          "com.aa.loyalty.tier.domain"),
    ("tier/TierCalculator.java",           "tier/domain/TierCalculator.java",           "com.aa.loyalty.tier.domain"),
    ("tier/TierBenefitCalculator.java",    "tier/domain/TierBenefitCalculator.java",    "com.aa.loyalty.tier.domain"),
    # tier/application
    ("tier/TierService.java",              "tier/application/TierService.java",              "com.aa.loyalty.tier.application"),
    # tier/infrastructure
    ("tier/TierController.java",           "tier/infrastructure/TierController.java",        "com.aa.loyalty.tier.infrastructure"),
    ("tier/TierMemberAdapter.java",        "tier/infrastructure/TierMemberAdapter.java",     "com.aa.loyalty.tier.infrastructure"),
    ("tier/TierMileageAdapter.java",       "tier/infrastructure/TierMileageAdapter.java",    "com.aa.loyalty.tier.infrastructure"),
    # redemption/domain
    ("redemption/Redemption.java",         "redemption/domain/Redemption.java",         "com.aa.loyalty.redemption.domain"),
    ("redemption/RedemptionStatus.java",   "redemption/domain/RedemptionStatus.java",   "com.aa.loyalty.redemption.domain"),
    ("redemption/RedemptionRepository.java","redemption/domain/RedemptionRepository.java","com.aa.loyalty.redemption.domain"),
    # redemption/application
    ("redemption/RedemptionService.java",  "redemption/application/RedemptionService.java",  "com.aa.loyalty.redemption.application"),
    # redemption/infrastructure
    ("redemption/RedemptionController.java","redemption/infrastructure/RedemptionController.java","com.aa.loyalty.redemption.infrastructure"),
    # partner/domain
    ("partner/Partner.java",               "partner/domain/Partner.java",               "com.aa.loyalty.partner.domain"),
    ("partner/PartnerRepository.java",     "partner/domain/PartnerRepository.java",     "com.aa.loyalty.partner.domain"),
    # partner/application
    ("partner/PartnerService.java",        "partner/application/PartnerService.java",        "com.aa.loyalty.partner.application"),
    # partner/infrastructure
    ("partner/PartnerController.java",     "partner/infrastructure/PartnerController.java",  "com.aa.loyalty.partner.infrastructure"),
]

# Global import substitutions (applied to ALL .java files in src/)
IMPORT_RENAMES = {
    "import com.aa.loyalty.member.Member;":                "import com.aa.loyalty.member.domain.Member;",
    "import com.aa.loyalty.member.Address;":               "import com.aa.loyalty.member.domain.Address;",
    "import com.aa.loyalty.member.EmailAddress;":          "import com.aa.loyalty.member.domain.EmailAddress;",
    "import com.aa.loyalty.member.MemberNumber;":          "import com.aa.loyalty.member.domain.MemberNumber;",
    "import com.aa.loyalty.member.MemberRepository;":      "import com.aa.loyalty.member.domain.MemberRepository;",
    "import com.aa.loyalty.member.MemberAdminPort;":       "import com.aa.loyalty.member.domain.MemberAdminPort;",
    "import com.aa.loyalty.member.MemberCompliancePort;":  "import com.aa.loyalty.member.domain.MemberCompliancePort;",
    "import com.aa.loyalty.member.MemberFraudPort;":       "import com.aa.loyalty.member.domain.MemberFraudPort;",
    "import com.aa.loyalty.member.MemberSelfServicePort;": "import com.aa.loyalty.member.domain.MemberSelfServicePort;",
    "import com.aa.loyalty.member.EnrollmentRequest;":     "import com.aa.loyalty.member.domain.EnrollmentRequest;",
    "import com.aa.loyalty.member.ProfileUpdateRequest;":  "import com.aa.loyalty.member.domain.ProfileUpdateRequest;",
    "import com.aa.loyalty.member.MemberService;":         "import com.aa.loyalty.member.application.MemberService;",
    "import com.aa.loyalty.member.MemberManagementService;":"import com.aa.loyalty.member.application.MemberManagementService;",
    "import com.aa.loyalty.member.MemberController;":      "import com.aa.loyalty.member.infrastructure.MemberController;",

    "import com.aa.loyalty.mileage.MileageAccount;":       "import com.aa.loyalty.mileage.domain.MileageAccount;",
    "import com.aa.loyalty.mileage.MileageTransaction;":   "import com.aa.loyalty.mileage.domain.MileageTransaction;",
    "import com.aa.loyalty.mileage.AccountStatus;":        "import com.aa.loyalty.mileage.domain.AccountStatus;",
    "import com.aa.loyalty.mileage.TransactionType;":      "import com.aa.loyalty.mileage.domain.TransactionType;",
    "import com.aa.loyalty.mileage.AccountNotFoundException;":"import com.aa.loyalty.mileage.domain.AccountNotFoundException;",
    "import com.aa.loyalty.mileage.FrozenMileageAccount;": "import com.aa.loyalty.mileage.domain.FrozenMileageAccount;",
    "import com.aa.loyalty.mileage.MileageRepository;":    "import com.aa.loyalty.mileage.domain.MileageRepository;",
    "import com.aa.loyalty.mileage.MileageCalculationPort;":"import com.aa.loyalty.mileage.domain.MileageCalculationPort;",
    "import com.aa.loyalty.mileage.MemberTierPort;":       "import com.aa.loyalty.mileage.domain.MemberTierPort;",
    "import com.aa.loyalty.mileage.MileageCalculator;":    "import com.aa.loyalty.mileage.domain.MileageCalculator;",
    "import com.aa.loyalty.mileage.MileageService;":       "import com.aa.loyalty.mileage.application.MileageService;",
    "import com.aa.loyalty.mileage.MileageAdminService;":  "import com.aa.loyalty.mileage.application.MileageAdminService;",
    "import com.aa.loyalty.mileage.AccrualService;":       "import com.aa.loyalty.mileage.application.AccrualService;",
    "import com.aa.loyalty.mileage.MileageController;":    "import com.aa.loyalty.mileage.infrastructure.MileageController;",
    "import com.aa.loyalty.mileage.MemberTierAdapter;":    "import com.aa.loyalty.mileage.infrastructure.MemberTierAdapter;",

    "import com.aa.loyalty.tier.TierStatus;":              "import com.aa.loyalty.tier.domain.TierStatus;",
    "import com.aa.loyalty.tier.TierBenefits;":            "import com.aa.loyalty.tier.domain.TierBenefits;",
    "import com.aa.loyalty.tier.MileageStatsView;":        "import com.aa.loyalty.tier.domain.MileageStatsView;",
    "import com.aa.loyalty.tier.TierMemberPort;":          "import com.aa.loyalty.tier.domain.TierMemberPort;",
    "import com.aa.loyalty.tier.TierMileagePort;":         "import com.aa.loyalty.tier.domain.TierMileagePort;",
    "import com.aa.loyalty.tier.TierCalculator;":          "import com.aa.loyalty.tier.domain.TierCalculator;",
    "import com.aa.loyalty.tier.TierBenefitCalculator;":   "import com.aa.loyalty.tier.domain.TierBenefitCalculator;",
    "import com.aa.loyalty.tier.TierService;":             "import com.aa.loyalty.tier.application.TierService;",
    "import com.aa.loyalty.tier.TierController;":          "import com.aa.loyalty.tier.infrastructure.TierController;",
    "import com.aa.loyalty.tier.TierMemberAdapter;":       "import com.aa.loyalty.tier.infrastructure.TierMemberAdapter;",
    "import com.aa.loyalty.tier.TierMileageAdapter;":      "import com.aa.loyalty.tier.infrastructure.TierMileageAdapter;",

    "import com.aa.loyalty.redemption.Redemption;":        "import com.aa.loyalty.redemption.domain.Redemption;",
    "import com.aa.loyalty.redemption.RedemptionStatus;":  "import com.aa.loyalty.redemption.domain.RedemptionStatus;",
    "import com.aa.loyalty.redemption.RedemptionRepository;":"import com.aa.loyalty.redemption.domain.RedemptionRepository;",
    "import com.aa.loyalty.redemption.RedemptionService;": "import com.aa.loyalty.redemption.application.RedemptionService;",
    "import com.aa.loyalty.redemption.RedemptionController;":"import com.aa.loyalty.redemption.infrastructure.RedemptionController;",

    "import com.aa.loyalty.partner.Partner;":              "import com.aa.loyalty.partner.domain.Partner;",
    "import com.aa.loyalty.partner.PartnerRepository;":    "import com.aa.loyalty.partner.domain.PartnerRepository;",
    "import com.aa.loyalty.partner.PartnerService;":       "import com.aa.loyalty.partner.application.PartnerService;",
    "import com.aa.loyalty.partner.PartnerController;":    "import com.aa.loyalty.partner.infrastructure.PartnerController;",
}

# New imports to add to specific files (keyed by new relative path under MAIN)
NEW_IMPORTS = {
    "member/infrastructure/MemberController.java": [
        "import com.aa.loyalty.member.application.MemberService;",
        "import com.aa.loyalty.member.domain.Address;",
        "import com.aa.loyalty.member.domain.EnrollmentRequest;",
        "import com.aa.loyalty.member.domain.Member;",
        "import com.aa.loyalty.member.domain.ProfileUpdateRequest;",
    ],
    "member/application/MemberService.java": [
        "import com.aa.loyalty.member.domain.Address;",
        "import com.aa.loyalty.member.domain.Member;",
        "import com.aa.loyalty.member.domain.MemberRepository;",
        "import com.aa.loyalty.member.domain.MemberSelfServicePort;",
    ],
    "member/application/MemberManagementService.java": [
        "import com.aa.loyalty.member.domain.Address;",
        "import com.aa.loyalty.member.domain.EnrollmentRequest;",
        "import com.aa.loyalty.member.domain.Member;",
    ],
    "mileage/application/MileageService.java": [
        "import com.aa.loyalty.mileage.application.AccrualService;",
        "import com.aa.loyalty.mileage.application.MileageAdminService;",
        "import com.aa.loyalty.mileage.domain.MileageAccount;",
        "import com.aa.loyalty.mileage.domain.MileageRepository;",
        "import com.aa.loyalty.mileage.domain.MileageTransaction;",
        "import com.aa.loyalty.mileage.domain.TransactionType;",
    ],
    "mileage/application/AccrualService.java": [
        "import com.aa.loyalty.mileage.domain.AccountStatus;",
        "import com.aa.loyalty.mileage.domain.MemberTierPort;",
        "import com.aa.loyalty.mileage.domain.MileageAccount;",
        "import com.aa.loyalty.mileage.domain.MileageCalculator;",
        "import com.aa.loyalty.mileage.domain.MileageRepository;",
        "import com.aa.loyalty.mileage.domain.MileageTransaction;",
        "import com.aa.loyalty.mileage.domain.TransactionType;",
    ],
    "mileage/application/MileageAdminService.java": [
        "import com.aa.loyalty.mileage.domain.AccountNotFoundException;",
        "import com.aa.loyalty.mileage.domain.AccountStatus;",
        "import com.aa.loyalty.mileage.domain.MileageAccount;",
        "import com.aa.loyalty.mileage.domain.MileageRepository;",
        "import com.aa.loyalty.mileage.domain.MileageTransaction;",
        "import com.aa.loyalty.mileage.domain.TransactionType;",
    ],
    "mileage/infrastructure/MileageController.java": [
        "import com.aa.loyalty.mileage.application.MileageService;",
    ],
    "mileage/infrastructure/MemberTierAdapter.java": [
        "import com.aa.loyalty.mileage.domain.MemberTierPort;",
    ],
    "tier/application/TierService.java": [
        "import com.aa.loyalty.tier.domain.MileageStatsView;",
        "import com.aa.loyalty.tier.domain.TierBenefitCalculator;",
        "import com.aa.loyalty.tier.domain.TierCalculator;",
        "import com.aa.loyalty.tier.domain.TierMemberPort;",
        "import com.aa.loyalty.tier.domain.TierMileagePort;",
        "import com.aa.loyalty.tier.domain.TierStatus;",
    ],
    "tier/infrastructure/TierController.java": [
        "import com.aa.loyalty.tier.application.TierService;",
    ],
    "tier/infrastructure/TierMemberAdapter.java": [
        "import com.aa.loyalty.tier.domain.TierMemberPort;",
        "import com.aa.loyalty.tier.domain.TierStatus;",
    ],
    "tier/infrastructure/TierMileageAdapter.java": [
        "import com.aa.loyalty.tier.domain.MileageStatsView;",
        "import com.aa.loyalty.tier.domain.TierMileagePort;",
    ],
    "redemption/application/RedemptionService.java": [
        "import com.aa.loyalty.redemption.domain.Redemption;",
        "import com.aa.loyalty.redemption.domain.RedemptionRepository;",
        "import com.aa.loyalty.redemption.domain.RedemptionStatus;",
    ],
    "redemption/infrastructure/RedemptionController.java": [
        "import com.aa.loyalty.redemption.application.RedemptionService;",
        "import com.aa.loyalty.redemption.domain.Redemption;",
    ],
    "partner/application/PartnerService.java": [
        "import com.aa.loyalty.partner.domain.Partner;",
        "import com.aa.loyalty.partner.domain.PartnerRepository;",
    ],
    "partner/infrastructure/PartnerController.java": [
        "import com.aa.loyalty.partner.application.PartnerService;",
        "import com.aa.loyalty.partner.domain.Partner;",
    ],
}


def get_package_from_path(new_rel_path):
    """Derive the package string from the new relative path."""
    for old_rel, new_rel, pkg in MOVES:
        if new_rel == new_rel_path:
            return pkg
    return None


def update_package_declaration(content, new_package):
    """Replace the package declaration line."""
    return re.sub(
        r'^(package\s+)[^;]+;',
        f'package {new_package};',
        content,
        count=1,
        flags=re.MULTILINE
    )


def apply_import_renames(content):
    """Apply global import substitutions."""
    for old_import, new_import in IMPORT_RENAMES.items():
        content = content.replace(old_import, new_import)
    return content


def add_new_imports(content, imports_to_add):
    """Insert new imports after the package line / existing imports block."""
    if not imports_to_add:
        return content

    lines = content.split('\n')

    # Find last import line index
    last_import_idx = -1
    package_idx = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('package '):
            package_idx = i
        if stripped.startswith('import '):
            last_import_idx = i

    # Collect existing import lines to avoid duplicates
    existing_imports = set()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import '):
            existing_imports.add(stripped)

    new_imports_filtered = [imp for imp in imports_to_add if imp not in existing_imports]
    if not new_imports_filtered:
        return content

    insert_after = last_import_idx if last_import_idx >= 0 else package_idx
    if insert_after < 0:
        return content

    new_lines = lines[:insert_after + 1] + new_imports_filtered + lines[insert_after + 1:]
    return '\n'.join(new_lines)


def remove_same_package_imports(content, package_name):
    """Remove imports of classes that are in the same package (Sonar S1128)."""
    lines = content.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import ') and stripped.startswith(f'import {package_name}.') and ';' in stripped:
            # Check it's a direct child (no further subpackage after the package name)
            rest = stripped[len(f'import {package_name}.'):]
            # If no dot in rest (before semicolon), it's a same-package import
            class_part = rest.rstrip(';')
            if '.' not in class_part:
                print(f"  Removing same-package import: {stripped}")
                continue
        result.append(line)
    return '\n'.join(result)


def deduplicate_imports(content):
    """Remove duplicate import lines."""
    lines = content.split('\n')
    seen_imports = set()
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import '):
            if stripped in seen_imports:
                print(f"  Removing duplicate import: {stripped}")
                continue
            seen_imports.add(stripped)
        result.append(line)
    return '\n'.join(result)


def collect_all_java_files(root):
    """Walk and collect all .java file paths."""
    java_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.java'):
                java_files.append(os.path.join(dirpath, filename))
    return java_files


def step1_create_dirs():
    """Create new directory structure."""
    print("\n=== Step 1: Creating directories ===")
    dirs = [
        "member/domain", "member/application", "member/infrastructure",
        "mileage/domain", "mileage/application", "mileage/infrastructure",
        "tier/domain", "tier/application", "tier/infrastructure",
        "redemption/domain", "redemption/application", "redemption/infrastructure",
        "partner/domain", "partner/application", "partner/infrastructure",
    ]
    for d in dirs:
        full = os.path.join(MAIN, d)
        os.makedirs(full, exist_ok=True)
        print(f"  Created: {full}")


def step2_move_files():
    """Read, update package, write to new location, delete old."""
    print("\n=== Step 2: Moving files with package updates ===")
    for old_rel, new_rel, new_package in MOVES:
        old_path = os.path.join(MAIN, old_rel)
        new_path = os.path.join(MAIN, new_rel)

        if not os.path.exists(old_path):
            print(f"  SKIP (not found): {old_rel}")
            continue

        with open(old_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = update_package_declaration(content, new_package)

        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(content)

        os.remove(old_path)
        print(f"  Moved: {old_rel} -> {new_rel} [pkg: {new_package}]")


def step3_update_imports_globally():
    """Apply global import substitutions to ALL .java files in src/."""
    print("\n=== Step 3: Updating imports globally ===")
    all_files = collect_all_java_files(SRC)
    changed = 0
    for fpath in all_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = apply_import_renames(content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed += 1
    print(f"  Updated imports in {changed} files")


def step4_add_new_imports():
    """Add within-context imports to specific files."""
    print("\n=== Step 4: Adding new within-context imports ===")
    for rel_path, imports in NEW_IMPORTS.items():
        fpath = os.path.join(MAIN, rel_path)
        if not os.path.exists(fpath):
            print(f"  SKIP (not found): {rel_path}")
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = add_new_imports(content, imports)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Added imports to: {rel_path}")
        else:
            print(f"  No new imports needed: {rel_path}")


def step5_cleanup_imports():
    """Remove same-package imports and deduplicate."""
    print("\n=== Step 5: Cleanup imports (same-package removal + dedup) ===")

    # Build a map of file -> package from the MOVES list
    file_to_package = {}
    for old_rel, new_rel, pkg in MOVES:
        new_path = os.path.join(MAIN, new_rel)
        file_to_package[new_path] = pkg

    all_files = collect_all_java_files(SRC)
    for fpath in all_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Deduplicate
        content = deduplicate_imports(content)

        # Remove same-package imports for moved files
        if fpath in file_to_package:
            pkg = file_to_package[fpath]
            content = remove_same_package_imports(content, pkg)

        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

    print("  Done")


def step6_verify():
    """Verify no old-style imports remain."""
    print("\n=== Step 6: Verifying no old-style flat imports remain ===")
    contexts = ["member", "mileage", "tier", "redemption", "partner"]
    all_files = collect_all_java_files(SRC)
    violations = []
    for fpath in all_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        for ctx in contexts:
            pattern = rf'import com\.aa\.loyalty\.{ctx}\.\w+;'
            for match in re.finditer(pattern, content):
                imp = match.group(0)
                # Allowed if it has domain/application/infrastructure subpackage
                if not any(sub in imp for sub in ['.domain.', '.application.', '.infrastructure.']):
                    violations.append(f"{fpath}: {imp}")

    if violations:
        print(f"  VIOLATIONS FOUND ({len(violations)}):")
        for v in violations:
            print(f"    {v}")
    else:
        print("  OK — no old-style flat imports remain")

    return violations


def main():
    step1_create_dirs()
    step2_move_files()
    step3_update_imports_globally()
    step4_add_new_imports()
    step5_cleanup_imports()
    violations = step6_verify()
    if violations:
        print("\nWARNING: Some violations remain. Review above.")
    else:
        print("\nRefactoring complete!")


if __name__ == '__main__':
    main()
