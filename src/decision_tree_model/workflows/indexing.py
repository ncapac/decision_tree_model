from __future__ import annotations

import json
import os
from pathlib import Path

from decision_tree_model.validation import (
    load_json,
    validate_data_snapshot_payload,
    validate_round_manifest,
)


def build_round_index(project_root: Path) -> Path:
    entries = []
    rounds_root = project_root / "results"
    for manifest_path in sorted(rounds_root.glob("round_*/manifest.json")):
        manifest = validate_round_manifest(manifest_path)
        entries.append(
            {
                "round_id": manifest["round_id"],
                "name": manifest["name"],
                "status": manifest["status"],
                "kind": manifest["kind"],
                "source_project": manifest["source"]["project"],
                "source_round": manifest["source"]["round"],
                "artifact_count": len(manifest["artifacts"]),
                "has_results": any(
                    artifact["path"].startswith(
                        f"results/{manifest['round_id']}/artifacts/"
                    )
                    for artifact in manifest["artifacts"]
                ),
            }
        )

    output = project_root / "results" / "index.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".json.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
        handle.write("\n")
    os.replace(temporary, output)
    return output


def build_data_index(project_root: Path) -> Path:
    entries = []
    snapshots_root = project_root / "data" / "snapshots"
    for manifest_path in sorted(snapshots_root.glob("*/manifest.json")):
        manifest = load_json(manifest_path)
        validate_data_snapshot_payload(manifest)
        entries.append(
            {
                "snapshot_id": manifest["snapshot_id"],
                "status": manifest["status"],
                "source_project": manifest["source"]["project"],
                "source_revision": manifest["source"]["repository_revision"],
                "source_superproject_revision": manifest["source"][
                    "superproject_revision"
                ],
                "file_count": len(manifest["files"]),
                "dataset_count": len(manifest["datasets"]),
                "manifest": str(manifest_path.relative_to(project_root)).replace(
                    "\\", "/"
                ),
            }
        )

    output = project_root / "data" / "catalog" / "index.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".json.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
        handle.write("\n")
    os.replace(temporary, output)
    return output
