"""Local PyInstaller proof entry point; never used by the production client."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def _runtime_setup() -> Path | None:
    if not getattr(sys, "frozen", False):
        return None
    runtime = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    duckdb = runtime / "duckdb.exe"
    if duckdb.is_file():
        os.environ["PATH"] = str(runtime) + os.pathsep + os.environ.get("PATH", "")
    return runtime


def main() -> int:
    runtime = _runtime_setup()
    if len(sys.argv) == 2 and sys.argv[1] == "--self-check":
        from gtfs_lab.compliance_adapter import ENGINE_PATH, SOURCES_DIR, _load_engine
        import gtfs_lab.pipeline  # noqa: F401
        import lxml
        import lxml.etree
        duckdb = shutil.which("duckdb")
        engine, _ = _load_engine()
        result = {"python_runtime": "BUNDLED" if runtime else sys.version,
                  "duckdb_cli": duckdb, "duckdb_version": None,
                  "gtfs_lab_import": "PASS", "compliance_engine": str(ENGINE_PATH),
                  "compliance_source_dir": str(SOURCES_DIR), "resource_hash_validation": "PASS",
                  "lxml_version": lxml.__version__,
                  "libxml2_version": ".".join(str(x) for x in lxml.etree.LIBXML_VERSION),
                  "runtime_root": str(runtime) if runtime else None}
        if duckdb:
            proc = subprocess.run([duckdb, "--version"], capture_output=True, text=True, check=True)
            result["duckdb_version"] = proc.stdout.strip()
        print(json.dumps(result))
        return 0 if duckdb and engine and Path(ENGINE_PATH).is_file() and Path(SOURCES_DIR).is_dir() else 2
    if len(sys.argv) == 4 and sys.argv[1] == "--audit":
        from gtfs_lab.pipeline import run
        result = run(Path(sys.argv[2]), Path(sys.argv[3]))
        print(json.dumps({"run_id": result["run_id"], "summary": result["summary"]}))
        return 0
    print("usage: --self-check | --audit FIXTURE.zip OUTPUT_DIR", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
