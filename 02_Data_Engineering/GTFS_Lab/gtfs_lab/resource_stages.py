"""Optional low-overhead stage markers for external resource profiling."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Callable


def mark(stage: str, state: str, metrics: dict | Callable[[], dict] | None = None) -> None:
    target = os.environ.get("TDL_RESOURCE_STAGE_FILE")
    if not target:
        return
    if callable(metrics):
        metrics = metrics()
    row = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "stage": stage, "state": state}
    if metrics:
        row["metrics"] = metrics
    try:
        with Path(target).open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, separators=(",", ":")) + "\n")
            stream.flush()
    except OSError:
        # Profiling is observational and must never change the audit result.
        return
