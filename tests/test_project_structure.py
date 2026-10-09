import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_repo_has_core_directories() -> None:
    expected = [
        ROOT / "config",
        ROOT / "docs",
        ROOT / "data",
        ROOT / "src" / "decision_tree_model",
        ROOT / "results",
        ROOT / "tests",
    ]

    for directory in expected:
        assert directory.exists(), f"Missing expected directory: {directory}"


def test_round_000_manifest_exists() -> None:
    manifest = ROOT / "results" / "round_000" / "manifest.json"
    assert manifest.exists(), "Round 000 manifest is missing."

    content = json.loads(manifest.read_text(encoding="utf-8"))
    assert content["round_id"] == "round_000"
    assert content["status"] == "awaiting_source_completion"
    assert content["artifacts"] == []


def test_redundant_root_directories_are_absent() -> None:
    for name in ("rounds", "notebooks", "scratch", "scripts"):
        assert not (ROOT / name).exists()
