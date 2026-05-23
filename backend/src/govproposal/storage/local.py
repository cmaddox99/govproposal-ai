"""Local filesystem storage backend.

Files are written under settings.upload_dir, organized by
{namespace}/{owner_id}/{uuid}_{safe_filename}. In production this directory
is expected to be a Railway volume mount (e.g. /data/uploads).
"""

from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4

from govproposal.config import settings


_SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_filename(name: str) -> str:
    """Strip path components and unsafe characters from a filename."""
    base = os.path.basename(name or "file")
    base = _SAFE_FILENAME_RE.sub("_", base).strip("._-")
    return base or "file"


@dataclass
class StoredFile:
    """A file written to local storage."""

    relative_path: str  # e.g. "opportunity_docs/<opp_id>/<uuid>_report.pdf"
    absolute_path: str
    original_filename: str
    content_type: str | None
    size_bytes: int


class LocalFileStorage:
    """Filesystem-backed storage. Suitable for a Railway volume."""

    def __init__(self, base_dir: str | None = None) -> None:
        self._base = Path(base_dir or settings.upload_dir).resolve()
        self._base.mkdir(parents=True, exist_ok=True)

    @property
    def base_dir(self) -> Path:
        return self._base

    def _target_dir(self, namespace: str, owner_id: str) -> Path:
        # Resolve and verify the target is within base_dir (prevents traversal
        # via crafted namespace/owner_id values, though both are server-side).
        target = (self._base / namespace / owner_id).resolve()
        if not str(target).startswith(str(self._base)):
            raise ValueError("Resolved storage path escapes base directory")
        target.mkdir(parents=True, exist_ok=True)
        return target

    def write(
        self,
        namespace: str,
        owner_id: str,
        source: BinaryIO,
        original_filename: str,
        content_type: str | None = None,
        max_bytes: int | None = None,
    ) -> StoredFile:
        """Stream source into local storage, enforcing max size.

        Raises ValueError if the file exceeds max_bytes.
        """
        limit = max_bytes if max_bytes is not None else settings.upload_max_bytes
        safe = _safe_filename(original_filename)
        target_dir = self._target_dir(namespace, owner_id)
        unique_name = f"{uuid4().hex}_{safe}"
        target_path = target_dir / unique_name

        size = 0
        try:
            with target_path.open("wb") as out:
                while True:
                    chunk = source.read(64 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > limit:
                        out.close()
                        target_path.unlink(missing_ok=True)
                        raise ValueError(
                            f"File exceeds maximum size of {limit} bytes"
                        )
                    out.write(chunk)
        except Exception:
            target_path.unlink(missing_ok=True)
            raise

        relative = str(target_path.relative_to(self._base)).replace(os.sep, "/")
        return StoredFile(
            relative_path=relative,
            absolute_path=str(target_path),
            original_filename=safe,
            content_type=content_type,
            size_bytes=size,
        )

    def open(self, relative_path: str) -> BinaryIO:
        """Open a stored file for reading. Caller must close."""
        target = (self._base / relative_path).resolve()
        if not str(target).startswith(str(self._base)):
            raise FileNotFoundError(relative_path)
        if not target.is_file():
            raise FileNotFoundError(relative_path)
        return target.open("rb")

    def absolute_path(self, relative_path: str) -> str:
        """Return the absolute path for a stored relative path."""
        target = (self._base / relative_path).resolve()
        if not str(target).startswith(str(self._base)):
            raise FileNotFoundError(relative_path)
        return str(target)

    def delete(self, relative_path: str) -> bool:
        """Delete a stored file. Returns True if removed, False if missing."""
        target = (self._base / relative_path).resolve()
        if not str(target).startswith(str(self._base)):
            return False
        if not target.is_file():
            return False
        target.unlink()
        return True

    def delete_owner(self, namespace: str, owner_id: str) -> None:
        """Remove all files for a given owner (e.g. on cascade delete)."""
        target = (self._base / namespace / owner_id).resolve()
        if not str(target).startswith(str(self._base)):
            return
        if target.is_dir():
            shutil.rmtree(target, ignore_errors=True)


_storage: LocalFileStorage | None = None


def get_storage() -> LocalFileStorage:
    """Return the process-wide storage instance."""
    global _storage
    if _storage is None:
        _storage = LocalFileStorage()
    return _storage
