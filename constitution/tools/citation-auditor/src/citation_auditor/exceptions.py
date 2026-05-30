"""Custom exceptions for aa-citation-audit.

Exit code mapping (cli.py responsibility):
  RegistryLoadError → sys.exit(2)
  AuditError        → sys.exit(2)
"""


class RegistryLoadError(Exception):
    """Raised by registry.py on any registry load failure."""


class AuditError(Exception):
    """Raised by auditor.py on internal verdict logic failure."""
