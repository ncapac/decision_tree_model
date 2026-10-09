from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from decision_tree_model.validation import (
    ContractError,
    sha256_file,
    validate_data_snapshot_payload,
)

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "snapshots" / "r15_registered_candidate_2026_10_09"


def test_provisional_snapshot_is_manifest_backed() -> None:
    manifest = json.loads((SNAPSHOT / "manifest.json").read_text(encoding="utf-8"))
    validate_data_snapshot_payload(manifest)
    assert manifest["status"] == "provisional"
    assert len(manifest["files"]) == 29
    assert len(manifest["datasets"]) == 6


def test_snapshot_files_match_manifest_hashes() -> None:
    manifest = json.loads((SNAPSHOT / "manifest.json").read_text(encoding="utf-8"))
    for record in manifest["files"]:
        path = SNAPSHOT / "files" / record["target_path"]
        assert path.is_file(), record["target_path"]
        assert sha256_file(path) == record["sha256"], record["target_path"]


def test_every_file_requires_exactly_one_dataset() -> None:
    manifest = json.loads((SNAPSHOT / "manifest.json").read_text(encoding="utf-8"))
    missing = copy.deepcopy(manifest)
    missing["datasets"][0]["file_paths"].pop()
    with pytest.raises(ContractError, match="missing dataset metadata"):
        validate_data_snapshot_payload(missing)

    duplicated = copy.deepcopy(manifest)
    duplicated["datasets"][1]["file_paths"].append(
        duplicated["datasets"][0]["file_paths"][0]
    )
    with pytest.raises(ContractError, match="multiple datasets"):
        validate_data_snapshot_payload(duplicated)
