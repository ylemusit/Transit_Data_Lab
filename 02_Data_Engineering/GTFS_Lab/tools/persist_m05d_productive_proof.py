"""Persist one M05-B pipeline comparison with compact durable source artifacts."""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gtfs_lab.audit_comparison import build_audit_snapshot, persist_comparison
from gtfs_lab.gate import create_fixtures
from gtfs_lab.pipeline import run

SOURCES = ROOT / "reports/evidence/m05d_productive_sources"
ARTIFACTS = ("run.json", "validation.json", "audit/audit_manifest.json", "audit/findings.normalized.json")


def _persist_source(source: Path, name: str) -> None:
    destination = SOURCES / name
    if destination.exists():
        raise RuntimeError(f"EVIDENCE_REFERENCE_INVALID: source already exists: {destination}")
    for relative in ARTIFACTS:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / relative, target)


def main() -> dict:
    baseline, candidate = SOURCES / "baseline", SOURCES / "candidate"
    if not baseline.exists() and not candidate.exists():
        with tempfile.TemporaryDirectory(prefix="m05d-pipeline-") as temp:
            temp_root = Path(temp)
            fixtures = create_fixtures(temp_root / "fixtures")
            first = run(fixtures["ORPHAN_TRIP"], temp_root / "runs")
            second = run(fixtures["ORPHAN_STOP"], temp_root / "runs")
            _persist_source(temp_root / "runs" / first["run_id"], "baseline")
            _persist_source(temp_root / "runs" / second["run_id"], "candidate")
    if not all((side / artifact).is_file() for side in (baseline, candidate) for artifact in ARTIFACTS):
        raise RuntimeError("EVIDENCE_REFERENCE_INVALID: incomplete productive source artifacts")
    prefix = "reports/evidence/m05d_productive_sources"
    refs = {"baseline_run": f"{prefix}/baseline", "baseline_manifest": f"{prefix}/baseline/audit/audit_manifest.json",
            "candidate_run": f"{prefix}/candidate", "candidate_manifest": f"{prefix}/candidate/audit/audit_manifest.json"}
    return persist_comparison(ROOT, build_audit_snapshot(baseline), build_audit_snapshot(candidate), source_artifacts=refs)


if __name__ == "__main__":
    result = main()
    print(result["path"])
