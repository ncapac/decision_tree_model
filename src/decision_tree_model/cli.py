from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from decision_tree_model.presentation import build_round_notebook
from decision_tree_model.validation import ContractError, validate_round_manifest
from decision_tree_model.workflows.data_snapshot import import_data_snapshot
from decision_tree_model.workflows.indexing import build_data_index, build_round_index
from decision_tree_model.workflows.recovery import RecoveryPlan, recover_legacy_round


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dtm")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-round")
    validate.add_argument("--round", default="round_000")

    subparsers.add_parser("build-index")

    recover = subparsers.add_parser("recover-legacy")
    recover.add_argument("--round", default="round_000")
    recover.add_argument("--source-root", required=True, type=Path)
    recover.add_argument("--completion-record", required=True, type=Path)
    recover.add_argument("--execute", action="store_true")

    notebook = subparsers.add_parser("build-notebook")
    notebook.add_argument("--round", required=True)

    data = subparsers.add_parser("import-data")
    data.add_argument("--source-root", required=True, type=Path)
    data.add_argument("--plan", required=True, type=Path)
    data.add_argument("--execute", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = _project_root()

    if args.command == "validate-round":
        validate_round_manifest(root / "results" / args.round / "manifest.json")
        print(f"Validated {args.round}.")
    elif args.command == "build-index":
        print(build_round_index(root))
        print(build_data_index(root))
    elif args.command == "recover-legacy":
        recovery_result = recover_legacy_round(
            root,
            RecoveryPlan(
                round_id=args.round,
                source_root=args.source_root,
                completion_record=args.completion_record,
            ),
            execute=args.execute,
        )
        action = "Recovered" if recovery_result.executed else "Validated"
        print(
            f"{action} {recovery_result.artifact_count} artifacts for "
            f"{recovery_result.round_id}."
        )
    elif args.command == "build-notebook":
        print(build_round_notebook(root, args.round))
    elif args.command == "import-data":
        data_result = import_data_snapshot(
            root,
            args.source_root,
            args.plan,
            execute=args.execute,
        )
        action = "Imported" if data_result.executed else "Validated"
        print(
            f"{action} {data_result.file_count} files for {data_result.snapshot_id}: "
            f"{data_result.manifest_path}"
        )
    return 0


def entrypoint(argv: Sequence[str] | None = None) -> int:
    try:
        return main(argv)
    except ContractError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
