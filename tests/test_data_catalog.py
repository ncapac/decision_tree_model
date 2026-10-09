from __future__ import annotations

import json
from pathlib import Path

from decision_tree_model.workflows.data_catalog import build_snapshot_report

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_ID = "r15_registered_candidate_2026_10_09"


def test_snapshot_report_profiles_csv_inputs() -> None:
    output = build_snapshot_report(ROOT, SNAPSHOT_ID)
    report = json.loads(output.read_text(encoding="utf-8"))

    assert report["snapshot_id"] == SNAPSHOT_ID
    assert report["file_count"] == 29
    asset_indices = next(
        item
        for item in report["files"]
        if item["target_path"] == "panels/asset_indices.csv"
    )
    assert asset_indices["format"] == "csv"
    assert asset_indices["row_count"] > 0
    assert asset_indices["columns"][0] == "date"
    assert asset_indices["first_date"] is not None
    assert asset_indices["last_date"] is not None


def test_snapshot_report_profiles_non_csv_inputs() -> None:
    output = build_snapshot_report(ROOT, SNAPSHOT_ID)
    report = json.loads(output.read_text(encoding="utf-8"))

    archive = next(
        item
        for item in report["files"]
        if item["target_path"] == "r15_macro/fred/alfred/CFNAI_realtime.zip"
    )
    assert archive["format"] == "zip"
    assert archive["bytes"] > 0
