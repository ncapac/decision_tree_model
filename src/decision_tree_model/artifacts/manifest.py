from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ArtifactManifest:
    round_id: str
    kind: str
    relative_path: str
    sha256: str
    description: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "round_id": self.round_id,
            "kind": self.kind,
            "relative_path": self.relative_path,
            "sha256": self.sha256,
            "description": self.description,
        }

    @classmethod
    def from_file(cls, path: str | Path) -> ArtifactManifest:
        payload = {}
        import json

        with Path(path).open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        return cls(
            round_id=payload.get("round_id", ""),
            kind=payload.get("kind", ""),
            relative_path=payload.get("relative_path", ""),
            sha256=payload.get("sha256", ""),
            description=payload.get("description", ""),
        )
