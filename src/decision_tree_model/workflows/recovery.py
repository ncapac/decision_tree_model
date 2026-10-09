from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from decision_tree_model import __version__
from decision_tree_model.validation import (
    ContractError,
    sha256_file,
    validate_round_manifest,
    validate_source_completion,
)
from decision_tree_model.workflows.git_provenance import capture_git_provenance


@dataclass(frozen=True)
class RecoveryPlan:
    round_id: str
    source_root: Path
    completion_record: Path


@dataclass(frozen=True)
class RecoveryResult:
    round_id: str
    artifact_count: int
    executed: bool


def _resolve_beneath(root: Path, relative_path: str) -> Path:
    candidate = (root / relative_path).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ContractError(f"Path escapes its declared root: {relative_path}")
    return candidate


def _verify_source(
    source_root: Path, completion: dict[str, Any]
) -> list[tuple[dict[str, Any], Path]]:
    repository = completion["repository"]
    actual = capture_git_provenance(source_root)
    if actual != repository:
        mismatches = sorted(
            key for key in repository if repository[key] != actual.get(key)
        )
        raise ContractError(
            "Source repository provenance mismatch: " + ", ".join(mismatches)
        )

    verified: list[tuple[dict[str, Any], Path]] = []
    for artifact in completion["artifacts"]:
        source_path = _resolve_beneath(source_root, artifact["source_path"])
        if not source_path.is_file():
            raise ContractError(f"Missing source artifact: {artifact['source_path']}")
        actual_sha256 = sha256_file(source_path)
        if actual_sha256 != artifact["sha256"]:
            raise ContractError(
                f"Hash mismatch for {artifact['source_path']}: "
                f"expected {artifact['sha256']}, found {actual_sha256}"
            )
        verified.append((artifact, source_path))
    return verified


def _atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp")
    shutil.copy2(source, temporary)
    os.replace(temporary, destination)


def _build_recovered_manifest(
    pending: dict[str, Any],
    completion_path: Path,
    completion: dict[str, Any],
    verified: list[tuple[dict[str, Any], Path]],
) -> dict[str, Any]:
    artifacts = [
        {
            "kind": artifact["kind"],
            "path": f"results/{pending['round_id']}/{artifact['target_path']}",
            "sha256": artifact["sha256"],
            "origin": {
                "source_path": artifact["source_path"],
                "source_sha256": artifact["sha256"],
            },
            "immutable": True,
            "description": artifact["description"],
        }
        for artifact, _ in verified
    ]

    completion_sha256 = sha256_file(completion_path)
    completion_target = f"results/{pending['round_id']}/source/source-completion.json"
    artifacts.append(
        {
            "kind": "source_completion",
            "path": completion_target,
            "sha256": completion_sha256,
            "origin": {
                "source_path": completion_path.name,
                "source_sha256": completion_sha256,
            },
            "immutable": True,
            "description": "Frozen source-round completion and export record.",
        }
    )

    return {
        **pending,
        "name": "recovered_legacy_round",
        "status": "recovered",
        "source": {
            **pending["source"],
            "completion_confirmed": True,
            "repository_revision": completion["repository"]["revision"],
            "source_manifest_path": completion_target,
            "source_manifest_sha256": completion_sha256,
        },
        "recovery": {
            "started": True,
            "completed": True,
            "imported_at_utc": datetime.now(UTC).isoformat(),
            "import_tool_version": __version__,
        },
        "artifacts": artifacts,
        "notes": [
            "Recovered from a source round explicitly marked complete.",
            "Imported evidence is immutable and is not a fresh model fit.",
        ],
    }


def recover_legacy_round(
    project_root: Path, plan: RecoveryPlan, *, execute: bool = False
) -> RecoveryResult:
    round_dir = project_root / "results" / plan.round_id
    manifest_path = round_dir / "manifest.json"
    pending = validate_round_manifest(manifest_path)
    if pending["status"] != "awaiting_source_completion":
        raise ContractError(f"{plan.round_id} is not awaiting source completion")

    completion_path = plan.completion_record.resolve()
    completion = validate_source_completion(completion_path)
    if completion["source_project"] != pending["source"]["project"]:
        raise ContractError("Source project does not match the reserved round")
    if completion["source_round"] != pending["source"]["round"]:
        raise ContractError("Source round does not match the reserved round")

    source_root = plan.source_root.resolve()
    verified = _verify_source(source_root, completion)
    recovered = _build_recovered_manifest(
        pending, completion_path, completion, verified
    )

    if not execute:
        return RecoveryResult(plan.round_id, len(verified), False)

    for artifact, source_path in verified:
        destination = _resolve_beneath(round_dir, artifact["target_path"])
        if destination.exists() and sha256_file(destination) != artifact["sha256"]:
            raise ContractError(f"Refusing to overwrite different file: {destination}")
        _atomic_copy(source_path, destination)

    completion_destination = round_dir / "source" / "source-completion.json"
    _atomic_copy(completion_path, completion_destination)

    temporary_manifest = manifest_path.with_suffix(".json.tmp")
    with temporary_manifest.open("w", encoding="utf-8") as handle:
        json.dump(recovered, handle, indent=2)
        handle.write("\n")
    os.replace(temporary_manifest, manifest_path)
    validate_round_manifest(manifest_path)
    return RecoveryResult(plan.round_id, len(verified), True)
