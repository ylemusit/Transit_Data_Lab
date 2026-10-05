"""Packaged worker entry point for the Windows client GUI."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    if getattr(sys, "frozen", False):
        # DuckDB CLI ships beside the worker in PyInstaller's onedir runtime.
        runtime_dir = str(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
        os.environ["PATH"] = runtime_dir + os.pathsep + os.environ.get("PATH", "")

    # The GUI reads the worker result as UTF-8, including paths with accents.
    for _stream in (sys.stdout, sys.stderr):
        if _stream is not None and hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors="replace")

    from gtfs_lab.client_workflow import main as workflow_main

    return workflow_main()


if __name__ == "__main__":
    raise SystemExit(main())