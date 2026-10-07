"""Local storage roots; environment overrides precede the project configuration.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados."""
from __future__ import annotations

import json
import os
from pathlib import Path


def data_root() -> Path:
    if os.environ.get("TDL_DATA_ROOT"):
        return Path(os.environ["TDL_DATA_ROOT"])
    if os.environ.get("TDL_ROOT"):
        return Path(os.environ["TDL_ROOT"]) / "02_Data"
    config = Path(__file__).resolve().parents[3] / "config" / "tdl_paths.json"
    if config.is_file():
        return Path(json.loads(config.read_text(encoding="utf-8-sig"))["TDL_DATA_ROOT"])
    return Path("P:/TransitDataLab/02_Data")
