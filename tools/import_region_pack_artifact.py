"""Verify and byte-preservingly import one approved Region Pack artifact."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import tempfile


_COPY_BUFFER_SIZE = 1024 * 1024


class ArtifactImportError(RuntimeError):
    """Raised when an approved artifact cannot be safely imported."""


def _normalize_sha256(expected_sha256: str) -> str:
    normalized = expected_sha256.strip().lower()
    if len(normalized) != 64 or any(character not in "0123456789abcdef" for character in normalized):
        raise ArtifactImportError("Expected SHA-256 must be exactly 64 hexadecimal characters.")
    return normalized


def calculate_sha256(path: Path) -> str:
    """Return a file's SHA-256 without interpreting its bytes as text."""

    digest = hashlib.sha256()
    try:
        with path.open("rb") as artifact:
            for chunk in iter(lambda: artifact.read(_COPY_BUFFER_SIZE), b""):
                digest.update(chunk)
    except OSError as error:
        raise ArtifactImportError(f"Unable to read artifact: {path}") from error
    return digest.hexdigest()


def _verify_hash(path: Path, expected_sha256: str, label: str) -> None:
    actual_sha256 = calculate_sha256(path)
    if actual_sha256 != expected_sha256:
        raise ArtifactImportError(f"{label} SHA-256 does not match the approved SHA-256.")


def _copy_as_bytes(source: Path, destination: Path) -> None:
    try:
        with source.open("rb") as source_file, destination.open("wb") as destination_file:
            shutil.copyfileobj(source_file, destination_file, length=_COPY_BUFFER_SIZE)
            destination_file.flush()
            os.fsync(destination_file.fileno())
    except OSError as error:
        raise ArtifactImportError("Unable to copy artifact bytes.") from error


def import_approved_artifact(
    source_path: str | Path,
    destination_path: str | Path,
    expected_sha256: str,
) -> None:
    """Import one artifact only after source and copied-byte hash verification."""

    source = Path(source_path).expanduser().resolve()
    destination = Path(destination_path).expanduser().resolve()
    expected = _normalize_sha256(expected_sha256)

    if source == destination:
        raise ArtifactImportError("Source and destination must be different files.")
    if not source.is_file():
        raise ArtifactImportError(f"Source artifact is not a file: {source}")
    if not destination.parent.is_dir():
        raise ArtifactImportError(f"Destination directory does not exist: {destination.parent}")

    _verify_hash(source, expected, "Source artifact")

    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
        )
        os.close(descriptor)
        temporary_path = Path(temporary_name)
        _copy_as_bytes(source, temporary_path)
        _verify_hash(temporary_path, expected, "Copied artifact")
        os.replace(temporary_path, destination)
        temporary_path = None
        _verify_hash(destination, expected, "Repository destination")
    except ArtifactImportError:
        raise
    except OSError as error:
        raise ArtifactImportError("Unable to safely replace the destination artifact.") from error
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError as error:
                raise ArtifactImportError(
                    "Unable to remove the temporary artifact after a failed import."
                ) from error


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify and byte-preservingly import one approved Region Pack artifact."
    )
    parser.add_argument("--source", required=True, help="External artifact file path.")
    parser.add_argument("--destination", required=True, help="Repository artifact file path.")
    parser.add_argument(
        "--expected-sha256", required=True, help="Owner-recorded approved SHA-256."
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        import_approved_artifact(
            arguments.source, arguments.destination, arguments.expected_sha256
        )
    except ArtifactImportError as error:
        print(f"Import failed: {error}")
        return 1
    print("Artifact import verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
