from __future__ import annotations

import json
from pathlib import Path

import pytest

from decision_tree_model.presentation import build_round_notebook
from decision_tree_model.validation import ContractError, validate_round_manifest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results" / "round_000" / "manifest.json"


def test_pending_round_manifest_is_valid() -> None:
    manifest = validate_round_manifest(MANIFEST)
    assert manifest["status"] == "awaiting_source_completion"
    assert manifest["source"]["completion_confirmed"] is False


def test_pending_round_cannot_claim_artifacts(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["round_id"] = "round_999"
    payload["artifacts"] = [
        {
            "kind": "summary",
            "path": "results/round_999/artifacts/summary.json",
            "sha256": "0" * 64,
            "origin": {
                "source_path": "summary.json",
                "source_sha256": "0" * 64,
            },
            "immutable": True,
            "description": "Invalid pending artifact.",
        }
    ]
    round_dir = tmp_path / "round_999"
    round_dir.mkdir()
    candidate = round_dir / "manifest.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ContractError, match="pending round cannot contain"):
        validate_round_manifest(candidate)


def test_pending_round_cannot_generate_results_notebook() -> None:
    with pytest.raises(ContractError, match="would be premature"):
        build_round_notebook(ROOT, "round_000")
