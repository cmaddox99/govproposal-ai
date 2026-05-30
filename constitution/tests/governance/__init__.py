"""Constitution self-validation test package.

These tests verify internal consistency of the Hangar AI Constitution:
- Registry (_domain.yaml) titles match law file frontmatter.
- Non-negotiable flags sync between law files and domain registries.
- Every registered law ID either has a law file or is marked status:deferred.
- Cross-domain index.yaml is coherent with per-domain registries.
"""
