from __future__ import annotations

import json
import os
from pathlib import Path

from decision_tree_model.validation import ContractError, validate_round_manifest

PRESENTABLE_STATUSES = {"recovered", "complete", "closed"}


def build_round_notebook(project_root: Path, round_id: str) -> Path:
    round_dir = project_root / "results" / round_id
    manifest_path = round_dir / "manifest.json"
    manifest = validate_round_manifest(manifest_path)
    if manifest["status"] not in PRESENTABLE_STATUSES:
        raise ContractError(
            f"{round_id} has status {manifest['status']!r}; "
            "a results notebook would be premature"
        )

    artifact_rows = [
        [
            artifact["kind"],
            artifact["path"],
            artifact["sha256"],
            artifact["description"],
        ]
        for artifact in manifest["artifacts"]
    ]
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.13"},
        },
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {round_id}: {manifest['name']}\n",
                    "\n",
                    (
                        "This notebook presents persisted evidence only. It does not "
                        "fit, search, or regenerate research.\n"
                    ),
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from pathlib import Path\n",
                    "import json\n",
                    "\n",
                    f"ROUND_ID = {round_id!r}\n",
                    "root = Path.cwd()\n",
                    "while root != root.parent and not (root / 'pyproject.toml').exists():\n",
                    "    root = root.parent\n",
                    (
                        "manifest = json.loads((root / 'results' / ROUND_ID / "
                        "'manifest.json').read_text(encoding='utf-8'))\n"
                    ),
                    "manifest\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Artifact ledger\n",
                    "\n",
                    "| kind | path | sha256 | description |\n",
                    "|---|---|---|---|\n",
                    *[
                        f"| {kind} | `{path}` | `{sha256}` | {description} |\n"
                        for kind, path, sha256, description in artifact_rows
                    ],
                ],
            },
        ],
    }

    output = round_dir / "notebooks" / "results.ipynb"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".ipynb.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(notebook, handle, indent=2)
        handle.write("\n")
    os.replace(temporary, output)
    return output
