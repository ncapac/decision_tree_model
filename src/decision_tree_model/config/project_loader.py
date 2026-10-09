from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_project_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML project config from disk."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data
