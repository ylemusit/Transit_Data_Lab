from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from gtfs_lab.client_workflow import _finding_rows, run_client_audit


class ClientWorkflowTests(unittest.TestCase):
    def test_findings_preserve_origin_and_required_envelope(self) -> None:
        compliance_finding = {"rule_id": "C1", "table": "stop_times.txt", "row_locator": "ROW:1",
                              "field": "stop_id", "observed_value": "missing", "evidence": {"note": "x"}}
        rows = _finding_rows({
            "engine_report": {"technical_evaluation": {"findings": [{"rule_id": "G1", "semantic_version": "1.0",
                "stage": "G04", "source_file": "trips.txt", "record_locator": "row:2"}]},
                "recommendation_findings": []},
            "compliance_v1": {"rule_id": "C1", "rule_version": "compliance-v1/1", "result": "FAIL_TECHNICAL",
                               "findings": [compliance_finding]},
            "validation": {"status": "FAIL_TECHNICAL", "findings": [compliance_finding]},
        }, "a" * 64)
        self.assertEqual([row["origin"] for row in rows], ["AUDIT_ENGINE", "COMPLIANCE"])
        for row in rows:
            for key in ("rule_version", "authority", "severity", "requirement", "technical_status", "file",
                        "row_locator", "field", "observed_evidence", "recommendation", "remediation_eligibility", "provenance"):
                self.assertIn(key, row)

    def test_freeze_delivery_hashes_origins_and_local_path_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "unknown-feed.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("agency.txt", "agency_name,agency_url,agency_timezone\nA,https://example.test,Europe/Madrid\n")
            before = source.read_bytes()

            def fake_run(path: Path, output: Path, *_args: object) -> dict:
                run_id = "RUN-SYNTHETIC"
                run_dir = output / run_id
                run_dir.mkdir(parents=True)
                source_sha = hashlib.sha256(path.read_bytes()).hexdigest()
                run = {
                    "run_id": run_id,
                    "dataset": {"dataset_id": "GTFS-test", "source_filename": path.name,
                                "source_sha256": source_sha, "ingestion_timestamp_utc": "2026-10-02T00:00:00Z",
                                "files": {}},
                    "summary": {"validation": "PASS", "compliance_v1": "PASS"},
                    "validation": {"status": "PASS", "finding_count": 0, "findings": [],
                                   "rules": [{"rule_id": "L1", "version": "1", "findings": []}]},
                    "compliance_v1": {"result": "PASS", "findings": []},
                    "engine_report": {"technical_evaluation": {"findings": []}, "recommendation_findings": [], "known_gaps": [], "deferred_features": []},
                }
                (run_dir / "run.json").write_text(json.dumps(run), encoding="utf-8")
                (run_dir / "engine_report.json").write_text(json.dumps(run["engine_report"]), encoding="utf-8")
                (run_dir / "path.txt").write_text(str(path.resolve()), encoding="utf-8")
                return run

            with patch("gtfs_lab.client_workflow.run", side_effect=fake_run):
                result = run_client_audit(source, root / "workspace", client_project_id="client-a",
                                          audit_id="audit-001", source_provenance="SYNTHETIC")

            self.assertEqual(result["status"], "COMPLETED")
            self.assertTrue(result["source_immutable"])
            self.assertTrue(result["artifacts_sha256_verified"])
            self.assertEqual(source.read_bytes(), before)
            delivery = Path(result["delivery_directory"])
            self.assertTrue((delivery / "audit_manifest.json").is_file())
            self.assertTrue((delivery / "report" / "client_report.md").is_file())
            self.assertIn("[LOCAL_PATH_REDACTED]", (delivery / "engine_run" / "path.txt").read_text(encoding="utf-8"))
            contract = json.loads((Path(__file__).parents[1] / "spec" / "client_audit_contract_v1.schema.json").read_text(encoding="utf-8"))
            identity = json.loads((delivery / "dataset_identity.json").read_text(encoding="utf-8"))
            self.assertEqual(set(identity) - set(contract["properties"]), set())

    def test_rejects_path_navigation_in_client_identifier(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "feed.zip"
            with zipfile.ZipFile(source, "w"):
                pass
            with self.assertRaisesRegex(ValueError, "identificador local"):
                run_client_audit(source, root / "workspace", client_project_id="..", audit_id="audit")
            self.assertFalse((root / "workspace").exists())


if __name__ == "__main__":
    unittest.main()
