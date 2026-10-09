from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import Any

from decision_tree_model.validation import ContractError


def git_text(repository: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def git_bytes(repository: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
    ).stdout


def capture_git_provenance(source_root: Path) -> dict[str, Any]:
    source_root = source_root.resolve()
    status = git_bytes(
        source_root, "status", "--porcelain=v1", "-z", "--untracked-files=all"
    )
    is_dirty = bool(status)
    diff = git_bytes(source_root, "diff", "--binary", "HEAD")

    superproject_root = git_text(
        source_root, "rev-parse", "--show-superproject-working-tree"
    )
    if not superproject_root:
        raise ContractError("Source repository is expected to be a submodule")

    return {
        "revision": git_text(source_root, "rev-parse", "HEAD"),
        "worktree_dirty": is_dirty,
        "status_sha256": hashlib.sha256(status).hexdigest(),
        "diff_sha256": hashlib.sha256(diff).hexdigest() if is_dirty else None,
        "superproject_revision": git_text(Path(superproject_root), "rev-parse", "HEAD"),
    }
