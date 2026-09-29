"""Productive comparison tests over realistic persisted M02 audit artifacts."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from gtfs_lab.audit_comparison import (
    ComparisonError,
    SNAPSHOT_CONTRACT_VERSION,
    build_audit_snapshot,
    compare_audit_directories,
    compare_audits,
)
from gtfs_lab.audit_contract import stable_finding_id
from gtfs_lab.gate import create_fixtures
from gtfs_lab.pipeline import run

SHA_A = "a" * 64
SHA_B = "b" * 64


def write_audit(root: Path, name: str, *, audit_id: str | None = None, source: str = SHA_A,
                parser: str = "gtfs-lab-csv/1", evaluator: str = "compliance-v1/2",
                evaluator_sha: str | None = SHA_A, rule_version: str = "1.0.0",
                status: str = "PASS", finding: dict | None = None,
                snapshot_version: str = "1.1.2") -> Path:
    run_dir = root / name
    audit_dir = run_dir / "audit"
    audit_dir.mkdir(parents=True)
    run_id = f"run-{name}"
    audit_id = audit_id or f"TDL-{run_id}"
    findings = [] if finding is None else [copy.deepcopy(finding)]
    rule = {"rule_id": "GTFS-TEST", "version": rule_version, "scope": "STRUCTURAL",
            "status": status, "finding_count": len(findings), "findings": findings}
    manifest = {
        "audit_id": audit_id, "manifest_version": snapshot_version, "created_at_utc": "2026-09-29T10:00:00+00:00",
        "run_id": run_id, "dataset_id": "dataset-1", "source_filename": "feed.zip", "source_sha256": source,
        "dataset_ingestion_timestamp_utc": "2026-09-29T09:00:00+00:00", "gtfs_lab_version": "1.0.0",
        "parser_version": parser, "validator_version": "1.0.0", "ruleset_id": "gtfs-lab-v1",
        "ruleset_version": "gtfs-lab-rules/1", "executed_rule_ids": ["GTFS-TEST"],
        "executed_rule_versions": {"GTFS-TEST": rule_version}, "scope": ["TECHNICAL"], "excluded": ["LEGAL"],
        "original_preserved": True,
        "preservation_evidence": {"verified": True, "source_sha256": source},
        "artifacts": {"run": "../run.json", "validation": "../validation.json", "findings_normalized": "findings.normalized.json"},
    }
    validation = {"status": status, "rules": [rule], "findings": findings}
    normalized_findings = [
        {**item, "audit_id": audit_id, "run_id": run_id, "dataset_id": "dataset-1", "source_sha256": source}
        for item in findings
    ]
    normalized = {"status": "NORMALIZED", "audit_id": audit_id, "run_id": run_id,
                  "dataset_id": "dataset-1", "source_sha256": source, "findings": normalized_findings}
    run = {"run_id": run_id, "gtfs_lab_version": "1.0.0", "validator_version": "1.0.0",
           "dataset": {"dataset_id": "dataset-1", "source_sha256": source}, "compliance_v1": {
               "rule_version": "compliance-v1/1", "evaluator_version": evaluator,
               "evaluator_sha256": evaluator_sha, "reference_sha256": SHA_A,
           }}
    (audit_dir / "audit_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (audit_dir / "findings.normalized.json").write_text(json.dumps(normalized), encoding="utf-8")
    (run_dir / "validation.json").write_text(json.dumps(validation), encoding="utf-8")
    (run_dir / "run.json").write_text(json.dumps(run), encoding="utf-8")
    return run_dir


def finding(identity: str, state: str = "DETECTED", evidence_note: str = "evidence", source: str = SHA_A) -> dict:
    value = {"rule_id": "GTFS-TEST", "table": "stops.txt", "row_locator": "record:2", "field": "stop_id",
             "observed_value": identity, "expected_condition": "synthetic test finding",
             "technical_message": evidence_note, "evidence": {"source_sha256": source}, "lifecycle_state": state}
    value["finding_id"] = stable_finding_id(value)
    return value


class AuditComparisonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def compare(self, baseline: dict, candidate: dict) -> dict:
        return compare_audits(baseline, candidate)

    def snapshots(self, **candidate_options):
        baseline_dir = write_audit(self.root, "baseline")
        candidate_dir = write_audit(self.root, "candidate", **candidate_options)
        return build_audit_snapshot(baseline_dir), build_audit_snapshot(candidate_dir)

    def test_pb001_same_persisted_audit_is_deterministic_no_change(self) -> None:
        run_dir = write_audit(self.root, "same")
        first = build_audit_snapshot(run_dir)
        second = build_audit_snapshot(run_dir)
        result = self.compare(first, second)
        self.assertEqual("NO_CHANGE", result["attribution"])
        self.assertEqual("PARTIALLY_COMPARABLE", result["comparability"]["status"])
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(SNAPSHOT_CONTRACT_VERSION, result["snapshot_contract_version"])

    def test_pipeline_persisted_artifacts_compare_productively_read_only(self) -> None:
        fixtures = create_fixtures(self.root / "pipeline-fixtures")
        first = run(fixtures["ORPHAN_TRIP"], self.root / "pipeline-run-a")
        second = run(fixtures["ORPHAN_TRIP"], self.root / "pipeline-run-b")
        first_dir = self.root / "pipeline-run-a" / first["run_id"]
        second_dir = self.root / "pipeline-run-b" / second["run_id"]
        first_snapshot = build_audit_snapshot(first_dir)
        second_snapshot = build_audit_snapshot(second_dir)
        self.assertEqual(first["dataset"]["source_sha256"], first_snapshot["identity"]["dataset"]["source_sha256"])
        self.assertEqual(second["dataset"]["source_sha256"], second_snapshot["identity"]["dataset"]["source_sha256"])
        result = compare_audit_directories(first_dir, second_dir)
        self.assertEqual("RUNTIME_ONLY_CHANGE", result["attribution"])
        self.assertEqual("PARTIALLY_COMPARABLE", result["comparability"]["status"])

    def test_pb002_different_audit_and_run_ids_are_runtime_only(self) -> None:
        baseline = build_audit_snapshot(write_audit(self.root, "baseline", finding=finding("stable-finding")))
        candidate = build_audit_snapshot(write_audit(self.root, "candidate", finding=finding("stable-finding")))
        result = self.compare(baseline, candidate)
        self.assertEqual("RUNTIME_ONLY_CHANGE", result["attribution"])

    def test_pb003_source_hash_change_is_dataset_change(self) -> None:
        baseline, candidate = self.snapshots(source=SHA_B)
        self.assertEqual("DATASET_CHANGE", self.compare(baseline, candidate)["attribution"])

    def test_pb004_parser_change_is_implementation_change(self) -> None:
        baseline, candidate = self.snapshots(parser="gtfs-lab-csv/2")
        self.assertEqual("PARSER_IMPLEMENTATION_CHANGE", self.compare(baseline, candidate)["attribution"])

    def test_pb005_evaluator_change_keeps_semantic_rule_constant(self) -> None:
        baseline, candidate = self.snapshots(evaluator="compliance-v1/3", evaluator_sha=SHA_B)
        result = self.compare(baseline, candidate)
        self.assertEqual("COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE", result["attribution"])
        self.assertFalse(result["result_change"]["changed"])

    def test_pb006_semantic_rule_change_is_distinct_from_implementation(self) -> None:
        baseline, candidate = self.snapshots(rule_version="2.0.0")
        result = self.compare(baseline, candidate)
        self.assertEqual("RULE_SEMANTIC_CHANGE", result["attribution"])
        self.assertEqual("PARTIALLY_COMPARABLE", result["comparability"]["status"])

    def test_pb007_new_normalized_finding(self) -> None:
        baseline = build_audit_snapshot(write_audit(self.root, "baseline"))
        candidate = build_audit_snapshot(write_audit(self.root, "candidate", finding=finding("finding-1", "DETECTED")))
        result = self.compare(baseline, candidate)
        self.assertEqual("NEW_FINDING", result["finding_change"]["changes"][0]["change"])

    def test_pb008_resolved_normalized_finding(self) -> None:
        baseline = build_audit_snapshot(write_audit(self.root, "baseline", finding=finding("finding-1")))
        candidate = build_audit_snapshot(write_audit(self.root, "candidate"))
        result = self.compare(baseline, candidate)
        self.assertEqual("RESOLVED_FINDING", result["finding_change"]["changes"][0]["change"])

    def test_pb009_dataset_and_rule_change_are_multiple_causes(self) -> None:
        baseline_dir = write_audit(self.root, "baseline")
        candidate_dir = write_audit(self.root, "candidate", source=SHA_B, rule_version="2.0.0")
        result = compare_audit_directories(baseline_dir, candidate_dir)
        self.assertEqual("MULTIPLE_CAUSES", result["attribution"])
        self.assertEqual(["DATASET_CHANGE", "RULE_SEMANTIC_CHANGE"], result["supported_causes"])

    def test_pb010_result_change_without_identity_change_is_unattributed(self) -> None:
        baseline, candidate = self.snapshots(status="FAIL_TECHNICAL")
        result = self.compare(baseline, candidate)
        self.assertEqual("UNATTRIBUTED_CHANGE", result["attribution"])
        self.assertEqual("NO_CAUSAL_EVIDENCE", result["evidence_status"])

    def test_pb011_required_identity_missing_fails_closed(self) -> None:
        baseline, candidate = self.snapshots()
        del baseline["identity"]["dataset"]["source_sha256"]
        result = self.compare(baseline, candidate)
        self.assertEqual("NOT_COMPARABLE", result["comparability"]["status"])
        self.assertEqual("NOT_COMPARABLE", result["attribution"])

    def test_pb012_incompatible_snapshot_version_is_not_comparable(self) -> None:
        baseline, candidate = self.snapshots()
        candidate["snapshot_contract_version"] = "2.0.0"
        result = self.compare(baseline, candidate)
        self.assertEqual("NOT_COMPARABLE", result["comparability"]["status"])
        self.assertTrue(any("SNAPSHOT_VERSION_UNSUPPORTED" in reason for reason in result["unresolved_reasons"]))

    def test_multi_rule_version_change_fails_closed_for_m05a_scalar_contract(self) -> None:
        baseline, candidate = self.snapshots()
        baseline["identity"]["rules"].update({"rule_version": None, "rule_versions": {"R1": "1", "R2": "1"}})
        candidate["identity"]["rules"].update({"rule_version": None, "rule_versions": {"R1": "1", "R2": "2"}})
        result = self.compare(baseline, candidate)
        self.assertEqual("NOT_COMPARABLE", result["comparability"]["status"])
        self.assertIn("RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0", result["unresolved_reasons"])

    def test_optional_identity_missing_means_partial_comparability(self) -> None:
        baseline, candidate = self.snapshots()
        self.assertEqual("PARTIALLY_COMPARABLE", self.compare(baseline, candidate)["comparability"]["status"])

    def test_duplicate_rule_identity_fails_closed(self) -> None:
        baseline, candidate = self.snapshots()
        candidate["result"]["rules"].append(copy.deepcopy(candidate["result"]["rules"][0]))
        with self.assertRaises(ComparisonError) as raised:
            self.compare(baseline, candidate)
        self.assertEqual("DUPLICATE_RULE_ID", raised.exception.code)

    def test_corrupt_evidence_is_explicit(self) -> None:
        run_dir = write_audit(self.root, "corrupt")
        (run_dir / "validation.json").write_text("{bad json", encoding="utf-8")
        with self.assertRaises(ComparisonError) as raised:
            build_audit_snapshot(run_dir)
        self.assertEqual("SNAPSHOT_INVALID", raised.exception.code)

    def test_findings_lifecycle_and_evidence_changes_keep_identity(self) -> None:
        baseline = build_audit_snapshot(write_audit(self.root, "baseline", finding=finding("finding-1", "DETECTED", "before")))
        lifecycle = build_audit_snapshot(write_audit(self.root, "lifecycle", finding=finding("finding-1", "REPRODUCED", "before")))
        evidence = build_audit_snapshot(write_audit(self.root, "evidence", finding=finding("finding-1", "DETECTED", "after")))
        self.assertEqual("FINDING_STATUS_CHANGE", self.compare(baseline, lifecycle)["finding_change"]["changes"][0]["change"])
        self.assertEqual("FINDING_EVIDENCE_CHANGE", self.compare(baseline, evidence)["finding_change"]["changes"][0]["change"])


if __name__ == "__main__":
    unittest.main()
