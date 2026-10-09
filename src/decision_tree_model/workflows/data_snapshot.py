from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from decision_tree_model.validation import (
    ContractError,
    load_json,
    sha256_file,
    validate_data_snapshot_payload,
)


@dataclass(frozen=True)
class DataSnapshotResult:
    snapshot_id: str
    file_count: int
    executed: bool
    manifest_path: Path


def _resolve_beneath(root: Path, relative_path: str) -> Path:
    candidate = (root / relative_path).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ContractError(f"Path escapes its declared root: {relative_path}")
    return candidate


def _verify_plan(
    source_root: Path, plan: dict[str, Any]
) -> list[tuple[dict[str, Any], Path]]:
    target_paths: set[str] = set()
    verified = []
    for record in plan["files"]:
        target_path = record["target_path"]
        if target_path in target_paths:
            raise ContractError(f"Duplicate data target path: {target_path}")
        target_paths.add(target_path)

        source_path = _resolve_beneath(source_root, record["source_path"])
        if not source_path.is_file():
            raise ContractError(f"Missing data source file: {record['source_path']}")
        actual_sha256 = sha256_file(source_path)
        if actual_sha256 != record["sha256"]:
            raise ContractError(
                f"Hash mismatch for {record['source_path']}: "
                f"expected {record['sha256']}, found {actual_sha256}"
            )
        verified.append((record, source_path))
    return verified


def import_data_snapshot(
    project_root: Path,
    source_root: Path,
    plan_path: Path,
    *,
    execute: bool = False,
) -> DataSnapshotResult:
    plan = load_json(plan_path)
    validate_data_snapshot_payload(plan)
    if plan["imported_at_utc"] is not None:
        raise ContractError("An import plan must set imported_at_utc to null")

    verified = _verify_plan(source_root.resolve(), plan)
    snapshot_root = project_root / "data" / "snapshots" / plan["snapshot_id"]
    manifest_path = snapshot_root / "manifest.json"
    if manifest_path.exists():
        raise ContractError(f"Snapshot already exists: {plan['snapshot_id']}")

    if not execute:
        return DataSnapshotResult(
            plan["snapshot_id"], len(verified), False, manifest_path
        )

    files_root = snapshot_root / "files"
    for record, source_path in verified:
        destination = _resolve_beneath(files_root, record["target_path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(f".{destination.name}.tmp")
        shutil.copy2(source_path, temporary)
        os.replace(temporary, destination)

    imported = {
        **plan,
        "imported_at_utc": datetime.now(UTC).isoformat(),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_manifest = manifest_path.with_suffix(".json.tmp")
    with temporary_manifest.open("w", encoding="utf-8") as handle:
        json.dump(imported, handle, indent=2)
        handle.write("\n")
    os.replace(temporary_manifest, manifest_path)
    validate_data_snapshot_payload(imported)
    return DataSnapshotResult(plan["snapshot_id"], len(verified), True, manifest_path)
