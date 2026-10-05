"""Re-run the onedir proof with only Windows system PATH entries available."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parents[4]
LAB = REPO / "02_Data_Engineering" / "GTFS_Lab"
sys.path.insert(0, str(LAB))
from tools.resource_measurement import _windows_process_snapshot, measure


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    app = args.dist.resolve() / "tdl-w00o-worker"
    exe, duckdb = app / "tdl-w00o-worker.exe", app / "_internal" / "duckdb.exe"
    output, temp = app / "synthetic-output-measured", app / "synthetic-temp-measured"
    output.mkdir(parents=True, exist_ok=True)
    child_env = {"PATH": str(Path(os.environ["SystemRoot"]) / "System32")}
    saved_cwd = Path.cwd()
    try:
        os.chdir(app)
        self_check = subprocess.run([str(exe), "--self-check"], capture_output=True,
                                    text=True, env={**os.environ, **child_env}, timeout=30)
        self_result = json.loads(self_check.stdout) if self_check.stdout else {}
        audit = measure([str(exe), "--audit", str(args.fixture.resolve()), str(output)],
                        output_dir=output, temp_dir=temp, interval=0.05,
                        env_overrides=child_env)
    finally:
        os.chdir(saved_cwd)
    run_files = list(output.rglob("run.json"))
    run = json.loads(run_files[0].read_text(encoding="utf-8")) if len(run_files) == 1 else {}
    process_ids = [row["pid"] for row in audit.get("processes", [])]
    snapshot = _windows_process_snapshot()
    orphans = [pid for pid in process_ids if pid in snapshot]
    package_bytes = sum(p.stat().st_size for p in app.rglob("*") if p.is_file()
                        and not any(part.startswith("synthetic-output") or part.startswith("synthetic-temp")
                                    for part in p.relative_to(app).parts))
    package_manifest = [{"path": p.relative_to(app).as_posix(), "size": p.stat().st_size,
                         "sha256": sha256(p)} for p in sorted(p for p in app.rglob("*") if p.is_file())
                        if not any(part.startswith("synthetic-output") or part.startswith("synthetic-temp")
                                   for part in p.relative_to(app).parts)]
    generated_artifacts = [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size}
                           for p in output.rglob("*") if p.is_file()]
    passed = (self_check.returncode == 0 and bool(duckdb.is_file()) and
              self_result.get("python_runtime") == "BUNDLED" and
              self_result.get("gtfs_lab_import") == "PASS" and
              self_result.get("resource_hash_validation") == "PASS" and
              audit.get("return_code") == 0 and run.get("database", {}).get("status") == "PASS" and
              bool(generated_artifacts) and not orphans)
    result = {
        "schema_version": "1.0", "status": "PASS" if passed else "FAIL",
        "pyinstaller_version": "6.22.3", "python_build_version": "3.12.10",
        "mode": "onedir", "tested_from_dist_directory": str(app),
        "developer_python_or_duckdb_path_available_to_worker": False,
        "clean_machine_validation": "PENDING",
        "bundled_python_runtime": self_result.get("python_runtime"),
        "duckdb_bundled": duckdb.is_file(), "duckdb_version": self_result.get("duckdb_version"),
        "duckdb_sha256": sha256(duckdb) if duckdb.is_file() else None,
        "tdl_imports": self_result.get("gtfs_lab_import"),
        "lxml_and_compliance_resource_hash_validation": self_result.get("resource_hash_validation"),
        "lxml_version": self_result.get("lxml_version"),
        "libxml2_version": self_result.get("libxml2_version"),
        "resource_paths": {"engine": self_result.get("compliance_engine"),
                           "sources": self_result.get("compliance_source_dir"),
                           "runtime_root": self_result.get("runtime_root")},
        "worker_self_check_exit_status": self_check.returncode,
        "synthetic_audit": {"exit_status": audit.get("return_code"),
                            "summary": run.get("summary"), "database": run.get("database"),
                            "wall_time_s": audit.get("wall_time_s"),
                            "cpu_time_s": audit.get("cpu_time_s"),
                            "peak_working_set_bytes_sampled": audit.get("working_set_bytes_peak_sampled"),
                            "peak_private_bytes_sampled": audit.get("private_bytes_peak_sampled"),
                            "process_tree": audit.get("processes"),
                            "artifact_bytes": sum(item["bytes"] for item in generated_artifacts),
                            "artifacts": generated_artifacts},
        "process_tree_absent_after_exit": not orphans,
        "orphan_processes": orphans,
        "dist_package_bytes_excluding_generated_output": package_bytes,
        "dist_package_file_count": len(package_manifest),
        "dist_package_manifest_sha256": hashlib.sha256(
            json.dumps(package_manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "limitations": ["Executed on the developer workstation with system PATH restricted to Windows System32.",
                        "A fresh Windows VM without Python/development tools remains untested.",
                        "The worker proof is local feasibility evidence, not an installer or signed release."],
    }
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
