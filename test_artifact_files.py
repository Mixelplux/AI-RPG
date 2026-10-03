"""Direct-file test contexts for the documented Windows sandbox fallback."""
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def artifact_files(prefix):
    root = Path(__file__).resolve().parent / ".artifacts"
    if not root.is_dir():
        raise AssertionError("Missing approved .artifacts root.")
    # Test filenames are explicitly prefixed by their owning script.
    existing = set(root.glob(prefix + "_*"))
    if existing:
        raise AssertionError("Existing test artifacts must be reviewed before reuse: " + prefix)
    try:
        yield str(root)
    finally:
        for path in root.glob(prefix + "_*"):
            if path.is_file():
                path.unlink()
