from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from decision_tree_model.validation import validate_round_manifest


@dataclass
class RoundLifecycle:
    round_id: str
    root: str | Path

    def round_dir(self) -> Path:
        return Path(self.root) / "results" / self.round_id

    def results_dir(self) -> Path:
        return self.round_dir() / "artifacts"

    def notebooks_dir(self) -> Path:
        return self.round_dir() / "notebooks"

    def manifest_path(self) -> Path:
        return self.round_dir() / "manifest.json"

    def validate(self) -> None:
        if not self.round_dir().exists():
            raise FileNotFoundError(f"Missing round directory: {self.round_dir()}")
        if not self.manifest_path().exists():
            raise FileNotFoundError(f"Missing manifest for round: {self.round_id}")
        validate_round_manifest(self.manifest_path())
