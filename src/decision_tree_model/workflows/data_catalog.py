from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any

from decision_tree_model.validation import (
    load_json,
    sha256_file,
    validate_data_snapshot_payload,
)


def _csv_profile(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        row_count = 0
        missing_by_column = {column: 0 for column in columns}
        first_date: str | None = None
        last_date: str | None = None
        date_column = (
            "date"
            if "date" in columns
            else ("observation_date" if "observation_date" in columns else None)
        )

        for row in reader:
            row_count += 1
            for column in columns:
                if not (row.get(column) or "").strip():
                    missing_by_column[column] += 1
            if date_column is not None:
                value = (row.get(date_column) or "").strip()
                if value:
                    first_date = first_date or value
                    last_date = value

    return {
        "format": "csv",
        "row_count": row_count,
        "column_count": len(columns),
        "columns": columns,
        "missing_by_column": missing_by_column,
        "date_column": date_column,
        "first_date": first_date,
        "last_date": last_date,
    }


def build_snapshot_report(project_root: Path, snapshot_id: str) -> Path:
    snapshot_root = project_root / "data" / "snapshots" / snapshot_id
    manifest_path = snapshot_root / "manifest.json"
    manifest = load_json(manifest_path)
    validate_data_snapshot_payload(manifest)

    files: list[dict[str, Any]] = []
    for record in manifest["files"]:
        path = snapshot_root / "files" / record["target_path"]
        profile: dict[str, Any]
        if path.suffix.lower() == ".csv":
            profile = _csv_profile(path)
        else:
            profile = {"format": path.suffix.lower().lstrip(".") or "binary"}
        files.append(
            {
                "target_path": record["target_path"],
                "role": record["role"],
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                **profile,
            }
        )

    report = {
        "schema_version": 1,
        "snapshot_id": snapshot_id,
        "status": manifest["status"],
        "manifest": str(manifest_path.relative_to(project_root)).replace("\\", "/"),
        "file_count": len(files),
        "files": files,
    }
    output = project_root / "data" / "catalog" / f"{snapshot_id}.report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".json.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    os.replace(temporary, output)
    return output
