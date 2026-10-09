from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from decision_tree_model.validation import (
    ContractError,
    load_json,
    sha256_file,
    validate_schema,
    validate_source_completion,
    validate_source_completion_payload,
)
from decision_tree_model.workflows.git_provenance import capture_git_provenance


@dataclass(frozen=True)
class CompletionRecordResult:
    source_project: str
    source_round: str
    artifact_count: int
    output_path: Path
    written: bool


def _resolve_beneath(root: Path, relative_path: str) -> Path:
    candidate = (root / relative_path).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ContractError(f"Path escapes its declared root: {relative_path}")
    return candidate


def _build_record(source_root: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    artifacts = []
    target_paths: set[str] = set()
    for artifact in inventory["artifacts"]:
        if artifact["target_path"] in target_paths:
            raise ContractError(
                f"Duplicate completion target: {artifact['target_path']}"
            )
        target_paths.add(artifact["target_path"])
        source_path = _resolve_beneath(source_root, artifact["source_path"])
        if not source_path.is_file():
            raise ContractError(
                f"Missing completion artifact: {artifact['source_path']}"
            )
        artifacts.append(
            {
                **artifact,
                "sha256": sha256_file(source_path),
            }
        )

    return {
        "schema_version": 1,
        "source_project": inventory["source_project"],
        "source_round": inventory["source_round"],
        "status": "complete",
        "repository": capture_git_provenance(source_root),
        "artifacts": artifacts,
    }


def create_completion_record(
    source_root: Path,
    inventory_path: Path,
    output_path: Path,
    *,
    execute: bool = False,
    confirm_source_complete: bool = False,
) -> CompletionRecordResult:
    inventory = load_json(inventory_path)
    validate_schema(inventory, "completion-inventory.schema.json")
    if not inventory["source_complete"]:
        raise ContractError("Inventory does not declare the source round complete")
    if not inventory["artifacts"]:
        raise ContractError("Completion inventory must contain at least one artifact")

    record = _build_record(source_root.resolve(), inventory)
    validate_source_completion_payload(record)

    if not execute:
        return CompletionRecordResult(
            inventory["source_project"],
            inventory["source_round"],
            len(record["artifacts"]),
            output_path.resolve(),
            False,
        )
    if not confirm_source_complete:
        raise ContractError(
            "Writing a completion record requires --confirm-source-complete"
        )

    output = output_path.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(f"{output.suffix}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2)
        handle.write("\n")
    os.replace(temporary, output)
    validate_source_completion(output)
    return CompletionRecordResult(
        inventory["source_project"],
        inventory["source_round"],
        len(record["artifacts"]),
        output,
        True,
    )
