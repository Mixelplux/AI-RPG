import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tools.import_region_pack_artifact import (
    ArtifactImportError,
    import_approved_artifact,
)


def sha256(content):
    return hashlib.sha256(content).hexdigest()


def temporary_import_files(directory):
    return list(Path(directory).glob(".destination.json.*.tmp"))


def test_imports_matching_artifact_with_exact_bytes():
    approved_bytes = b'{"name":"Bryn Shander","note":"caf\xc3\xa9 \xe2\x80\x94 \xe5\x8c\x97"}\r\n'

    with TemporaryDirectory() as temporary_directory:
        directory = Path(temporary_directory)
        source = directory / "approved-region.json"
        destination = directory / "destination.json"
        source.write_bytes(approved_bytes)

        import_approved_artifact(source, destination, sha256(approved_bytes))

        assert destination.read_bytes() == approved_bytes
        assert sha256(destination.read_bytes()) == sha256(approved_bytes)
        assert temporary_import_files(directory) == []


def test_source_hash_mismatch_rejects_before_destination_modification():
    with TemporaryDirectory() as temporary_directory:
        directory = Path(temporary_directory)
        source = directory / "approved-region.json"
        destination = directory / "destination.json"
        source.write_bytes(b"approved bytes")
        destination.write_bytes(b"existing repository bytes")

        try:
            import_approved_artifact(source, destination, sha256(b"different approved bytes"))
        except ArtifactImportError as error:
            assert "Source artifact SHA-256" in str(error)
        else:
            raise AssertionError("Expected source hash mismatch to reject the import.")

        assert destination.read_bytes() == b"existing repository bytes"
        assert temporary_import_files(directory) == []


def test_failed_copy_leaves_no_temporary_or_partial_destination():
    approved_bytes = b"approved bytes"

    with TemporaryDirectory() as temporary_directory:
        directory = Path(temporary_directory)
        source = directory / "approved-region.json"
        destination = directory / "destination.json"
        source.write_bytes(approved_bytes)

        with patch(
            "tools.import_region_pack_artifact._copy_as_bytes",
            side_effect=ArtifactImportError("simulated copy failure"),
        ):
            try:
                import_approved_artifact(source, destination, sha256(approved_bytes))
            except ArtifactImportError as error:
                assert "simulated copy failure" in str(error)
            else:
                raise AssertionError("Expected copy failure to reject the import.")

        assert not destination.exists()
        assert temporary_import_files(directory) == []


def main():
    test_imports_matching_artifact_with_exact_bytes()
    test_source_hash_mismatch_rejects_before_destination_modification()
    test_failed_copy_leaves_no_temporary_or_partial_destination()
    print("Region Pack artifact import tests passed.")


if __name__ == "__main__":
    main()
