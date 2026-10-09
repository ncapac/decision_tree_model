from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

from decision_tree_model.validation import ContractError
from decision_tree_model.workflows import recovery
from decision_tree_model.workflows.completion import create_completion_record
from decision_tree_model.workflows.recovery import (
    RecoveryPlan,
    recover_legacy_round,
)

ROOT = Path(__file__).resolve().parents[1]
PENDING_MANIFEST = ROOT / "results" / "round_000" / "manifest.json"


def _git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _configure_git(repository: Path) -> None:
    _git(repository, "config", "user.name", "Recovery Test")
    _git(repository, "config", "user.email", "recovery@example.invalid")


def _commit_all(repository: Path, message: str) -> None:
    _git(repository, "add", "--all")
    _git(repository, "commit", "-m", message)


@dataclass(frozen=True)
class RecoveryFixture:
    project_root: Path
    source_root: Path
    inventory_path: Path
    completion_path: Path
    round_id: str


@pytest.fixture
def recovery_fixture(tmp_path: Path) -> RecoveryFixture:
    origin = tmp_path / "source-origin"
    origin.mkdir()
    _git(origin, "init", "--initial-branch=main")
    _configure_git(origin)
    (origin / "summary.json").write_text('{"metric": 1.25}\n', encoding="utf-8")
    (origin / "returns.csv").write_text(
        "date,net_return\n2026-01-01,0.01\n", encoding="utf-8"
    )
    _commit_all(origin, "Bank source artifacts")

    superproject = tmp_path / "superproject"
    superproject.mkdir()
    _git(superproject, "init", "--initial-branch=main")
    _configure_git(superproject)
    subprocess.run(
        [
            "git",
            "-c",
            "protocol.file.allow=always",
            "-C",
            str(superproject),
            "submodule",
            "add",
            str(origin),
            "legacy-source",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    _commit_all(superproject, "Pin source submodule")
    source_root = superproject / "legacy-source"

    project_root = tmp_path / "new-project"
    round_id = "round_999"
    round_dir = project_root / "results" / round_id
    round_dir.mkdir(parents=True)
    pending = json.loads(PENDING_MANIFEST.read_text(encoding="utf-8"))
    pending["round_id"] = round_id
    pending["source"]["project"] = "legacy-project"
    pending["source"]["round"] = "R1"
    (round_dir / "manifest.json").write_text(json.dumps(pending), encoding="utf-8")

    inventory = {
        "schema_version": 1,
        "source_project": "legacy-project",
        "source_round": "R1",
        "source_complete": True,
        "artifacts": [
            {
                "kind": "round_summary",
                "source_path": "summary.json",
                "target_path": "artifacts/summary.json",
                "description": "Frozen result summary.",
            },
            {
                "kind": "heldout_returns",
                "source_path": "returns.csv",
                "target_path": "artifacts/returns.csv",
                "description": "Frozen held-out returns.",
            },
        ],
        "notes": [],
    }
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")

    return RecoveryFixture(
        project_root=project_root,
        source_root=source_root,
        inventory_path=inventory_path,
        completion_path=tmp_path / "completion.json",
        round_id=round_id,
    )


def _create_completion(fixture: RecoveryFixture) -> None:
    create_completion_record(
        fixture.source_root,
        fixture.inventory_path,
        fixture.completion_path,
        execute=True,
        confirm_source_complete=True,
    )


def _plan(fixture: RecoveryFixture) -> RecoveryPlan:
    return RecoveryPlan(
        fixture.round_id,
        fixture.source_root,
        fixture.completion_path,
    )


def test_completion_and_recovery_end_to_end(
    recovery_fixture: RecoveryFixture,
) -> None:
    _create_completion(recovery_fixture)

    dry_run = recover_legacy_round(
        recovery_fixture.project_root, _plan(recovery_fixture)
    )
    assert dry_run.executed is False
    assert dry_run.artifact_count == 2

    result = recover_legacy_round(
        recovery_fixture.project_root,
        _plan(recovery_fixture),
        execute=True,
    )
    assert result.executed is True
    round_dir = recovery_fixture.project_root / "results" / recovery_fixture.round_id
    assert (round_dir / "artifacts" / "summary.json").is_file()
    assert (round_dir / "artifacts" / "returns.csv").is_file()
    manifest = json.loads((round_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "recovered"
    assert len(manifest["artifacts"]) == 3


def test_recovery_retries_after_interrupted_copy(
    recovery_fixture: RecoveryFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    _create_completion(recovery_fixture)
    original = recovery._atomic_copy
    copy_count = 0

    def fail_second_copy(source: Path, destination: Path) -> None:
        nonlocal copy_count
        copy_count += 1
        if copy_count == 2:
            raise OSError("simulated interruption")
        original(source, destination)

    monkeypatch.setattr(recovery, "_atomic_copy", fail_second_copy)
    with pytest.raises(OSError, match="simulated interruption"):
        recover_legacy_round(
            recovery_fixture.project_root,
            _plan(recovery_fixture),
            execute=True,
        )

    pending = json.loads(
        (
            recovery_fixture.project_root
            / "results"
            / recovery_fixture.round_id
            / "manifest.json"
        ).read_text(encoding="utf-8")
    )
    assert pending["status"] == "awaiting_source_completion"

    monkeypatch.setattr(recovery, "_atomic_copy", original)
    result = recover_legacy_round(
        recovery_fixture.project_root,
        _plan(recovery_fixture),
        execute=True,
    )
    assert result.executed is True


def test_recovery_rejects_revision_mismatch(
    recovery_fixture: RecoveryFixture,
) -> None:
    _create_completion(recovery_fixture)
    completion = json.loads(
        recovery_fixture.completion_path.read_text(encoding="utf-8")
    )
    completion["repository"]["revision"] = "0" * 40
    recovery_fixture.completion_path.write_text(
        json.dumps(completion), encoding="utf-8"
    )

    with pytest.raises(ContractError, match="revision"):
        recover_legacy_round(
            recovery_fixture.project_root,
            _plan(recovery_fixture),
        )


def test_completion_rejects_source_path_escape(
    recovery_fixture: RecoveryFixture,
) -> None:
    inventory = json.loads(recovery_fixture.inventory_path.read_text(encoding="utf-8"))
    inventory["artifacts"][0]["source_path"] = "../outside.json"
    recovery_fixture.inventory_path.write_text(json.dumps(inventory), encoding="utf-8")

    with pytest.raises(ContractError, match="escapes"):
        create_completion_record(
            recovery_fixture.source_root,
            recovery_fixture.inventory_path,
            recovery_fixture.completion_path,
        )


def test_dirty_source_provenance_is_reconciled(
    recovery_fixture: RecoveryFixture,
) -> None:
    summary = recovery_fixture.source_root / "summary.json"
    summary.write_text('{"metric": 1.50}\n', encoding="utf-8")
    _create_completion(recovery_fixture)
    completion = json.loads(
        recovery_fixture.completion_path.read_text(encoding="utf-8")
    )
    repository = completion["repository"]
    assert repository["worktree_dirty"] is True
    assert repository["diff_sha256"] is not None
    assert len(repository["status_sha256"]) == 64

    result = recover_legacy_round(
        recovery_fixture.project_root,
        _plan(recovery_fixture),
        execute=True,
    )
    assert result.executed is True


def test_completion_record_requires_closed_source_and_confirmation(
    recovery_fixture: RecoveryFixture,
) -> None:
    inventory = json.loads(recovery_fixture.inventory_path.read_text(encoding="utf-8"))
    inventory["source_complete"] = False
    recovery_fixture.inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    with pytest.raises(ContractError, match="does not declare"):
        create_completion_record(
            recovery_fixture.source_root,
            recovery_fixture.inventory_path,
            recovery_fixture.completion_path,
        )

    inventory["source_complete"] = True
    recovery_fixture.inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    with pytest.raises(ContractError, match="confirm-source-complete"):
        create_completion_record(
            recovery_fixture.source_root,
            recovery_fixture.inventory_path,
            recovery_fixture.completion_path,
            execute=True,
        )
