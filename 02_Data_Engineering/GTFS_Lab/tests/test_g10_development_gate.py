from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gtfs_lab.g10_development_gate import build_cross_dataset_comparison, evaluate_development_corpus
from gtfs_lab.g10_worker import _bounded_findings_evidence, _bounded_reason_evidence


class G10DevelopmentGateTests(unittest.TestCase):
    def test_g03_reason_evidence_groups_counts_and_caps_samples(self):
        evidence = _bounded_reason_evidence({
            "status": "NOT_EVALUABLE",
            "not_evaluable": [
                {"file": "routes.txt", "field": "route_type", "reason": "UNRESOLVED_TYPE_FORMAT"}
                for _ in range(8)
            ],
        }, sample_limit=3)
        self.assertEqual(8, evidence["not_evaluable_count"])
        self.assertEqual(1, len(evidence["reason_counts"]))
        self.assertEqual(8, evidence["reason_counts"][0]["count"])
        self.assertEqual(3, len(evidence["sample"]))

    def test_g03_findings_evidence_groups_rows_and_retains_file_status(self):
        evidence = _bounded_findings_evidence({
            "status": "PASS",
            "findings": [{"file": "stops.txt", "field": "stop_id", "rule_id": "GTFS-G03-FIELD-TYPE",
                           "observed": "private-value"} for _ in range(7)],
            "files_inspected": [{"file": "stops.txt", "status": "PASS", "data_rows": 7}],
        }, sample_limit=2)
        self.assertEqual(7, evidence["finding_count"])
        self.assertEqual(7, evidence["reason_counts"][0]["count"])
        self.assertEqual(2, len(evidence["sample"]))
        self.assertEqual("GTFS-G03-FIELD-TYPE", evidence["reason_counts"][0]["reason_code"])
        self.assertNotIn("observed", evidence["sample"][0])
        self.assertEqual("PASS", evidence["file_statuses"][0]["status"])
        self.assertEqual(7, evidence["file_statuses"][0]["row_count"])

    def test_cross_dataset_comparison_uses_rule_finding_counts(self):
        records = [{"execution_status": "COMPLETED", "stages": {
            "g03": {"status": "FAIL_TECHNICAL", "finding_counts_by_rule": {"GTFS-G03-X": 2},
                    "rules": [{"rule_id": "GTFS-G03-X", "status": "FAIL_TECHNICAL"}]},
        }}]
        comparison = build_cross_dataset_comparison(records)
        self.assertEqual({"FAIL_TECHNICAL": 1}, comparison["rule_status_counts"]["GTFS-G03-X"])
        self.assertEqual(2, comparison["finding_counts_by_rule"]["GTFS-G03-X"])

    def test_only_development_sources_are_opened_and_hash_checked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "sources"
            source_root.mkdir()
            payload = b"synthetic development source"
            (source_root / "dev.zip").write_bytes(payload)
            inventory = {
                "inventory_version": "1.0.0",
                "datasets": [
                    {"dataset_id": "DEV-001", "zip_relative_path": "dev.zip",
                     "zip_sha256": hashlib.sha256(payload).hexdigest()},
                    {"dataset_id": "HOLD-001", "zip_relative_path": "must-not-be-opened.zip",
                     "zip_sha256": "0" * 64},
                ],
            }
            split = {"split_id": "split-v1", "split_sha256": "a" * 64, "datasets": [
                {"dataset_id": "DEV-001", "assignment": "DEVELOPMENT"},
                {"dataset_id": "HOLD-001", "assignment": "HOLDOUT"},
            ]}
            inventory_path, split_path = root / "inventory.json", root / "split.json"
            lineage_path = root / "lineage.json"
            inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
            split_path.write_text(json.dumps(split), encoding="utf-8")
            lineage_path.write_text("{}", encoding="utf-8")

            def fake_run(source, work_root):
                return {"run_id": "run-1", "ingestion_status": "PASS",
                        "legacy_validation_status": "PASS", "legacy_finding_count": 0,
                        "engine_report_sha256": "b" * 64,
                        "stages": {stage: {"status": "PASS", "rules": []}
                           for stage in ("g03", "g04", "g05", "g06", "g07", "g08")}}

            with patch("gtfs_lab.g10_development_gate.validate_split", return_value="PASS") as split_gate, \
                    patch("gtfs_lab.g10_development_gate._run_isolated", side_effect=fake_run) as runner:
                report = evaluate_development_corpus(
                    inventory_path=inventory_path, split_path=split_path,
                    lineage_review_path=lineage_path, source_root=source_root,
                )
            split_gate.assert_called_once()
            self.assertEqual(2, runner.call_count)
            self.assertEqual("dev.zip", runner.call_args.args[0].name)
            self.assertFalse(report["holdout_accessed"])
            self.assertEqual("COMPLETED", report["corpus_execution_status"])
            self.assertEqual("PASS", report["stability_check"]["status"])
            self.assertEqual(["DEV-001"], [row["dataset_id"] for row in report["datasets"]])
            self.assertEqual(1, report["completed_dataset_count"])

    def test_development_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "sources"
            source_root.mkdir()
            (source_root / "dev.zip").write_bytes(b"not frozen")
            inventory_path, split_path = root / "inventory.json", root / "split.json"
            lineage_path = root / "lineage.json"
            inventory_path.write_text(json.dumps({"datasets": [{
                "dataset_id": "DEV-001", "zip_relative_path": "dev.zip", "zip_sha256": "0" * 64,
            }]}), encoding="utf-8")
            split_path.write_text(json.dumps({"datasets": [{
                "dataset_id": "DEV-001", "assignment": "DEVELOPMENT",
            }]}), encoding="utf-8")
            lineage_path.write_text("{}", encoding="utf-8")
            with patch("gtfs_lab.g10_development_gate.validate_split", return_value="PASS"):
                with self.assertRaisesRegex(ValueError, "hash mismatch"):
                    evaluate_development_corpus(inventory_path=inventory_path, split_path=split_path,
                                                lineage_review_path=lineage_path, source_root=source_root)


if __name__ == "__main__":
    unittest.main()
