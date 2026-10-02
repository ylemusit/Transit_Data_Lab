"""Deterministic, synthetic end-to-end proof for Client Audit Workflow V1."""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from gtfs_lab.client_workflow import run_client_audit


FEED = {
    "agency.txt": "agency_id,agency_name,agency_url,agency_timezone\nA,Example Transit,https://example.test,Europe/Madrid\n",
    "stops.txt": "stop_id,stop_name,stop_lat,stop_lon\nS1,Stop One,40.4,-3.7\n",
    "routes.txt": "route_id,agency_id,route_short_name,route_type\nR1,A,1,3\n",
    "trips.txt": "route_id,service_id,trip_id\nR1,WK,T1\n",
    "stop_times.txt": "trip_id,arrival_time,departure_time,stop_id,stop_sequence\nT1,08:00:00,08:00:00,S1,1\n",
    "calendar.txt": "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\nWK,1,1,1,1,1,0,0,20261001,20261231\n",
}


def write_fixture(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in FEED.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, content.encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True, help="new JSON evidence path")
    args = parser.parse_args()
    evidence_path = args.evidence.resolve()
    if evidence_path.exists():
        raise SystemExit(f"refusing to overwrite evidence: {evidence_path}")
    with tempfile.TemporaryDirectory(prefix="tdl-client-workflow-e2e-") as folder:
        root = Path(folder)
        source = root / "unknown_gtfs.zip"
        write_fixture(source)
        source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
        runs = []
        engine_reports = []
        first_engine_run = None
        for audit_id in ("e2e-a", "e2e-b"):
            result = run_client_audit(source, root / audit_id, client_project_id="synthetic-development",
                                      audit_id=audit_id, source_provenance="SYNTHETIC")
            assert result["status"] in {"COMPLETED", "COMPLETED_WITH_LIMITATIONS", "COMPLETED_WITH_FINDINGS"}, result
            assert result["source_sha256"] == source_sha
            assert result["source_immutable"] and result["artifacts_sha256_verified"]
            delivery = Path(result["delivery_directory"])
            report = next((delivery / "engine_run").rglob("engine_report.json")).read_bytes()
            if first_engine_run is None:
                first_engine_run = next((delivery / "engine_run").rglob("audit_manifest.json")).parent.parent
            assert b"tdl-client-workflow-e2e-" not in report
            assert "\"artifacts_sha256_verified\": true" in (delivery / "audit_manifest.json").read_text(encoding="utf-8")
            runs.append({"audit_id": audit_id, "status": result["status"],
                         "manifest_sha256": result["audit_manifest_sha256"],
                         "delivery_artifact_count": result["artifact_count"],
                         "findings_count": result["findings_count"],
                         "source_immutable": result["source_immutable"],
                         "artifacts_sha256_verified": result["artifacts_sha256_verified"]})
            engine_reports.append(report)
        stable_engine_report = engine_reports[0] == engine_reports[1]
        assert stable_engine_report, "engine report changed across same-input replay"
        recurring = run_client_audit(source, root / "recurring", client_project_id="synthetic-development",
                                     audit_id="e2e-next", source_provenance="SYNTHETIC",
                                     audit_mode="RECURRING", baseline_run=first_engine_run)
        assert recurring["status"] in {"COMPLETED", "COMPLETED_WITH_LIMITATIONS", "COMPLETED_WITH_FINDINGS"}, recurring
        comparison = json.loads((Path(recurring["delivery_directory"]) / "reaudit_comparison.json").read_text(encoding="utf-8"))
        payload = {
            "evidence_contract": "TDL_CLIENT_AUDIT_WORKFLOW_E2E",
            "contract_version": "1.0.0",
            "corpus": "SYNTHETIC_UNKNOWN_GTFS",
            "source_filename": source.name,
            "source_sha256": source_sha,
            "source_size_bytes": source.stat().st_size,
            "runs": runs + [{"audit_id": "e2e-next", "status": recurring["status"],
                             "source_immutable": recurring["source_immutable"],
                             "artifacts_sha256_verified": recurring["artifacts_sha256_verified"],
                             "comparison_status": comparison.get("comparability", {}).get("status"),
                             "attribution": comparison.get("attribution")}],
            "same_input_engine_report_identical": stable_engine_report,
            "holdout_accessed": False,
            "client_data_accessed": False,
            "external_upload": False,
        }
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
