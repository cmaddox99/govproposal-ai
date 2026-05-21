"""File storage abstraction."""

from govproposal.storage.local import LocalFileStorage, StoredFile, get_storage

__all__ = ["LocalFileStorage", "StoredFile", "get_storage"]
