from __future__ import annotations

import json
from pathlib import Path

from decision_tree_model.validation import sha256_file, validate_schema

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "snapshots" / "r15_registered_candidate_2026_10_09"


def test_provisional_snapshot_is_manifest_backed() -> None:
    manifest = json.loads((SNAPSHOT / "manifest.json").read_text(encoding="utf-8"))
    validate_schema(manifest, "data-snapshot.schema.json")
    assert manifest["status"] == "provisional"
    assert len(manifest["files"]) == 29


def test_snapshot_files_match_manifest_hashes() -> None:
    manifest = json.loads((SNAPSHOT / "manifest.json").read_text(encoding="utf-8"))
    for record in manifest["files"]:
        path = SNAPSHOT / "files" / record["target_path"]
        assert path.is_file(), record["target_path"]
        assert sha256_file(path) == record["sha256"], record["target_path"]
