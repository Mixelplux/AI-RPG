# Test-only legacy Bryn Shander fixture

`bryn_shander_legacy.json` preserves the authored baseline at `18b69f095a429cf00f83bad597fc381e1e9b03fe` solely to exercise existing atomic, causal, save, projection and time mechanisms. It is not an alternate ordinary-play reference pack. Current gameplay and new acceptance tests use `data/regions/bryn_shander.json`.

Tests use prefixed deterministic direct files under `.artifacts/` for the documented Windows temporary-directory cleanup fallback. `test_artifact_files.py` does not create temporary child directories or change ACLs.
