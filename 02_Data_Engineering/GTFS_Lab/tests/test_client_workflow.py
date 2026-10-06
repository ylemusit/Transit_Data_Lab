from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from gtfs_lab.client_workflow import _finding_rows, _sanitize_delivery, run_client_audit


class ClientWorkflowTests(unittest.TestCase):
    def test_large_json_delivery_redaction_is_streamed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            delivery = root / "delivery"
            delivery.mkdir()
            private_path = str(root / "local" / "engine_run" / "run.json")
            artifact = delivery / "run.json"
            artifact.write_text(json.dumps({"artifact": private_path, "payload": "x" * 4096}), encoding="utf-8")

            with patch("gtfs_lab.client_workflow._LARGE_JSON_STREAM_THRESHOLD", 1):
                with patch.object(Path, "read_text", side_effect=AssertionError("large JSON must be streamed")):
                    streamed = _sanitize_delivery(delivery)

            self.assertIn(artifact.resolve(), streamed)
            sanitized = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertEqual(sanitized["artifact"], "[LOCAL_PATH_REDACTED]")
            self.assertEqual(sanitized["payload"], "x" * 4096)

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
                original_read_text = Path.read_text

                def reject_pipeline_run_reload(path: Path, *args: object, **kwargs: object) -> str:
                    if path.name == "run.json" and "engine_runs" in path.parts:
                        raise AssertionError("Client Workflow must reuse the mapping returned by pipeline.run")
                    return original_read_text(path, *args, **kwargs)

                with patch.object(Path, "read_text", reject_pipeline_run_reload):
                    result = run_client_audit(source, root / "workspace", client_project_id="client-a",
                                              audit_id="audit-001", source_provenance="SYNTHETIC")
                    rerun = run_client_audit(source, root / "workspace-rerun", client_project_id="client-a",
                                             audit_id="audit-002", source_provenance="SYNTHETIC")

            self.assertEqual(result["status"], "COMPLETED")
            self.assertTrue(result["source_immutable"])
            self.assertTrue(rerun["source_immutable"])
            self.assertTrue(rerun["artifacts_sha256_verified"])
            self.assertTrue(result["artifacts_sha256_verified"])
            self.assertEqual(source.read_bytes(), before)
            delivery = Path(result["delivery_directory"])
            self.assertTrue((delivery / "audit_manifest.json").is_file())
            self.assertTrue((delivery / "report" / "client_report.md").is_file())
            report_model = json.loads((delivery / "report" / "client_report.json").read_text(encoding="utf-8"))
            self.assertEqual("TDL_CLIENT_REPORT_V1", report_model["contract"])
            self.assertEqual(29, len(report_model["sections"]))
            self.assertIn("report/client_report.json", json.loads((delivery / "audit_manifest.json").read_text(encoding="utf-8"))["delivery_artifacts"])
            pdf_status = json.loads((delivery / "report" / "pdf_generation_status.json").read_text(encoding="utf-8"))
            pdf_path = delivery / "report" / "client_report.pdf"
            manifest = json.loads((delivery / "audit_manifest.json").read_text(encoding="utf-8"))
            if pdf_status["status"] == "GENERATED":
                self.assertTrue(pdf_path.is_file())
                self.assertIn("report/client_report.pdf", manifest["delivery_artifacts"])
            else:
                self.assertEqual(pdf_status["status"], "FAILED_NONBLOCKING")
                self.assertFalse(pdf_path.exists())
                self.assertNotIn("report/client_report.pdf", manifest["delivery_artifacts"])
            self.assertTrue((delivery / "GIS_QGIS_GUIDE.md").is_file())
            self.assertIn("GIS_QGIS_GUIDE.md", manifest["delivery_artifacts"])
            self.assertIn("report/pdf_generation_status.json", manifest["delivery_artifacts"])
            interpretation = json.loads((delivery / "AUDIT_CONSOLIDATED.json").read_text(encoding="utf-8"))
            self.assertEqual(interpretation["coverage"]["accounting_gap"], 0)
            self.assertIn("tdl_ref=", interpretation["provenance"]["deterministic_family_id_basis"])
            self.assertEqual(json.loads((delivery / "audit_interpretation_status.json").read_text(encoding="utf-8"))["status"], "INTERPRETATION_COMPLETED")
            self.assertIn("AUDIT_CONSOLIDATED.json", json.loads((delivery / "audit_manifest.json").read_text(encoding="utf-8"))["delivery_artifacts"])
            self.assertIn("- TDL ref:", (delivery / "AUDIT_CONSOLIDATED.md").read_text(encoding="utf-8"))
            self.assertIn("[LOCAL_PATH_REDACTED]", (delivery / "engine_run" / "path.txt").read_text(encoding="utf-8"))
            contract = json.loads((Path(__file__).parents[1] / "spec" / "client_audit_contract_v1.schema.json").read_text(encoding="utf-8"))
            identity = json.loads((delivery / "dataset_identity.json").read_text(encoding="utf-8"))
            self.assertEqual(set(identity) - set(contract["properties"]), set())
            with patch("gtfs_lab.client_workflow.run", side_effect=fake_run):
                with patch("gtfs_lab.client_pdf.write_professional_pdf", side_effect=OSError("synthetic renderer unavailable")):
                    failed_pdf = run_client_audit(source, root / "workspace-pdf-failure", client_project_id="client-a",
                                                  audit_id="audit-pdf-failure", source_provenance="SYNTHETIC")
            self.assertTrue(failed_pdf["status"].startswith("COMPLETED"))
            failed_delivery = Path(failed_pdf["delivery_directory"])
            pdf_status = json.loads((failed_delivery / "report" / "pdf_generation_status.json").read_text(encoding="utf-8"))
            self.assertEqual(pdf_status["status"], "FAILED_NONBLOCKING")
            self.assertTrue(failed_pdf["artifacts_sha256_verified"])

    def test_interpretation_failure_preserves_completed_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "synthetic.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("agency.txt", "agency_name\nSynthetic\n")

            def fake_run(path, output, *_args):
                run_dir = output / "RUN-SYNTHETIC"
                run_dir.mkdir(parents=True)
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                run_value = {"run_id": "RUN-SYNTHETIC", "dataset": {"dataset_id": "synthetic", "source_sha256": digest},
                    "summary": {"validation": "PASS", "compliance_v1": "PASS"},
                    "validation": {"findings": [], "rules": []}, "compliance_v1": {"findings": []},
                    "engine_report": {"technical_evaluation": {"findings": []}, "recommendation_findings": [], "known_gaps": [], "deferred_features": []}}
                (run_dir / "engine_report.json").write_text(json.dumps(run_value["engine_report"]), encoding="utf-8")
                return run_value

            with patch("gtfs_lab.client_workflow.run", side_effect=fake_run), \
                 patch("gtfs_lab.client_workflow.build_interpretation", side_effect=RuntimeError("synthetic interpreter error")):
                result = run_client_audit(source, root / "workspace", client_project_id="client-a", audit_id="audit-fail",
                                          source_provenance="SYNTHETIC")
            delivery = Path(result["delivery_directory"])
            self.assertTrue(result["status"].startswith("COMPLETED"))
            self.assertEqual(json.loads((delivery / "audit_interpretation_status.json").read_text())["status"], "INTERPRETATION_FAILED")
            self.assertTrue((delivery / "findings.json").is_file())
            self.assertFalse((delivery / "AUDIT_CONSOLIDATED.json").exists())

    def test_engine_failure_is_blocked_and_does_not_expose_successful_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "synthetic.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("agency.txt", "agency_name\nSynthetic\n")
            with patch("gtfs_lab.client_workflow.run", side_effect=RuntimeError("synthetic engine failure")):
                result = run_client_audit(source, root / "workspace", client_project_id="client-a",
                                          audit_id="audit-engine-failure", source_provenance="SYNTHETIC")
            self.assertEqual(result["status"], "BLOCKED_TECHNICAL")
            self.assertTrue(result["source_immutable"])
            root_path = root / "workspace" / "client-a" / "audit-engine-failure"
            self.assertTrue((root_path / "audit" / "workflow_result.json").is_file())
            self.assertFalse((root_path / "delivery" / "audit_manifest.json").exists())

    def test_rejects_path_navigation_in_client_identifier(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "feed.zip"
            with zipfile.ZipFile(source, "w"):
                pass
            with self.assertRaisesRegex(ValueError, "identificador local"):
                run_client_audit(source, root / "workspace", client_project_id="..", audit_id="audit")
            self.assertFalse((root / "workspace").exists())

    def test_existing_workspace_collision_is_rejected_without_modification(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "feed.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("agency.txt", "agency_name\nSynthetic\n")
            workspace = root / "workspace"
            workspace.mkdir()
            marker = workspace / "preserve.txt"
            marker.write_text("keep this output", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "workspace ya existe"):
                run_client_audit(source, workspace, client_project_id="client-a", audit_id="audit-collision",
                                 source_provenance="SYNTHETIC")
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep this output")
            self.assertEqual(list(workspace.iterdir()), [marker])


if __name__ == "__main__":
    unittest.main()
