"""Explicitly bind hash-pinned Compliance V1 resources to packaged data."""
from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    from gtfs_lab import compliance_adapter

    root = Path(sys._MEIPASS) / "tdl_resources"  # type: ignore[attr-defined]
    compliance_adapter.ENGINE_PATH = root / "tools" / "compliance_v1_engine.py"
    sources = (root / "03_Compliance" / "reports" / "evidence" /
               "compliance_v1_20260928" / "sources")
    compliance_adapter.SOURCES_DIR = sources
    compliance_adapter.MANIFEST_PATH = sources.parent / "source_manifest.json"
