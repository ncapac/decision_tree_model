from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_ROOT = PROJECT_ROOT / "config" / "schemas"


class ContractError(ValueError):
    """Raised when a project contract is internally inconsistent."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ContractError(f"Expected a JSON object: {path}")
    return value


def validate_schema(payload: dict[str, Any], schema_name: str) -> None:
    schema_path = SCHEMA_ROOT / schema_name
    schema = load_json(schema_path)
    registry = Registry()
    for candidate in SCHEMA_ROOT.glob("*.schema.json"):
        registered = load_json(candidate)
        registry = registry.with_resource(
            registered["$id"], Resource.from_contents(registered)
        )
    errors = sorted(
        Draft202012Validator(schema, registry=registry).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        details = "; ".join(
            f"{'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ContractError(details)


def validate_round_manifest(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    validate_schema(payload, "round-manifest.schema.json")

    if path.parent.name != payload["round_id"]:
        raise ContractError(
            f"Manifest round_id {payload['round_id']!r} does not match {path.parent.name!r}"
        )

    status = payload["status"]
    source = payload["source"]
    recovery = payload["recovery"]
    artifacts = payload["artifacts"]

    if status == "awaiting_source_completion":
        if source["completion_confirmed"]:
            raise ContractError("A pending round cannot confirm source completion")
        if recovery["started"] or recovery["completed"]:
            raise ContractError("A pending round cannot report recovery activity")
        if artifacts:
            raise ContractError("A pending round cannot contain recovered artifacts")

    if status == "recovered":
        required = (
            source["completion_confirmed"],
            source["repository_revision"],
            source["source_manifest_path"],
            source["source_manifest_sha256"],
            recovery["started"],
            recovery["completed"],
            recovery["imported_at_utc"],
            recovery["import_tool_version"],
            artifacts,
        )
        if not all(required):
            raise ContractError(
                "A recovered round must have complete source and recovery data"
            )

    return payload


def validate_source_completion(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    validate_schema(payload, "source-completion.schema.json")
    repository = payload["repository"]
    if repository["worktree_dirty"] and not repository["diff_sha256"]:
        raise ContractError("A dirty source worktree requires diff_sha256")
    if not repository["worktree_dirty"] and repository["diff_sha256"] is not None:
        raise ContractError("A clean source worktree must set diff_sha256 to null")
    return payload
