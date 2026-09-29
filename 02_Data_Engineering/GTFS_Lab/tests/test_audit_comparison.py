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
    persist_comparison,
    render_comparison_report,
    verify_comparison_record,
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
        persisted = persist_comparison(self.root, first_snapshot, second_snapshot, source_artifacts={
            "baseline_run": str(first_dir), "baseline_manifest": str(first_dir / "audit" / "audit_manifest.json"),
            "candidate_run": str(second_dir), "candidate_manifest": str(second_dir / "audit" / "audit_manifest.json")})
        self.assertTrue(Path(persisted["path"]).is_file())
        self.assertTrue(Path(persisted["report_path"]).is_file())

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

    def test_pd001_to_pd011_persist_idempotence_integrity_refs_and_report(self) -> None:
        cases = [
            ("no-change", {}, "NO_CHANGE"), ("data", {"source": SHA_B}, "DATASET_CHANGE"),
            ("implementation", {"parser": "gtfs-lab-csv/2"}, "PARSER_IMPLEMENTATION_CHANGE"),
            ("multiple", {"source": SHA_B, "parser": "gtfs-lab-csv/2"}, "MULTIPLE_CAUSES"),
            ("not-comparable", {}, "NOT_COMPARABLE"),
            ("unattributed", {"status": "FAIL_TECHNICAL"}, "UNATTRIBUTED_CHANGE"),
        ]
        for name, options, expected_attribution in cases:
            with self.subTest(name=name):
                case_root = self.root / name
                case_root.mkdir()
                baseline_id = candidate_id = f"TDL-{name}-same" if name == "no-change" else None
                before_dir = write_audit(case_root, "baseline", audit_id=baseline_id or f"TDL-{name}-baseline")
                after_dir = write_audit(case_root, "candidate", audit_id=candidate_id or f"TDL-{name}-candidate", **options)
                before, after = build_audit_snapshot(before_dir), build_audit_snapshot(after_dir)
                if name == "not-comparable":
                    before["snapshot_contract_version"] = "unsupported"
                refs = {"baseline_run": str(before_dir), "baseline_manifest": str(before_dir / "audit" / "audit_manifest.json"),
                        "candidate_run": str(after_dir), "candidate_manifest": str(after_dir / "audit" / "audit_manifest.json")}
                first = persist_comparison(self.root, before, after, source_artifacts=refs)
                self.assertEqual(expected_attribution, first["record"]["comparison"]["attribution"])
                first_bytes = Path(first["path"]).read_bytes()
                report_bytes = Path(first["report_path"]).read_bytes()
                record_mtime = Path(first["path"]).stat().st_mtime_ns
                report_mtime = Path(first["report_path"]).stat().st_mtime_ns
                again = persist_comparison(self.root, before, after, source_artifacts=refs)
                self.assertEqual(first["path"], again["path"])
                self.assertEqual(first_bytes, Path(again["path"]).read_bytes())
                self.assertEqual(report_bytes, Path(again["report_path"]).read_bytes())
                self.assertEqual(record_mtime, Path(again["path"]).stat().st_mtime_ns)
                self.assertEqual(report_mtime, Path(again["report_path"]).stat().st_mtime_ns)
                self.assertEqual(render_comparison_report(first["record"]), Path(first["report_path"]).read_bytes())
                self.assertEqual(refs, first["record"]["source_artifacts"])
                record = json.loads(first_bytes)
                import hashlib
                expected_hash = hashlib.sha256((json.dumps(before, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
                self.assertEqual(expected_hash, record["integrity"]["baseline_snapshot_sha256"])
                self.assertEqual(True, verify_comparison_record(record, before, after))

    def test_pd008_same_comparison_id_different_payload_fails_closed(self) -> None:
        before, after = self.snapshots()
        refs = {"baseline_run": "baseline", "baseline_manifest": "baseline/audit/audit_manifest.json",
                "candidate_run": "candidate", "candidate_manifest": "candidate/audit/audit_manifest.json"}
        persist_comparison(self.root, before, after, source_artifacts=refs)
        changed = copy.deepcopy(after)
        changed["result"]["rules"][0]["status"] = "FAIL_TECHNICAL"
        with self.assertRaises(ComparisonError) as raised:
            persist_comparison(self.root, before, changed, source_artifacts=refs)
        self.assertEqual("COMPARISON_RECORD_CONFLICT", raised.exception.code)

    def test_pd011_tampered_snapshot_fails_hash_verification(self) -> None:
        before, after = self.snapshots()
        refs = {"baseline_run": "baseline", "baseline_manifest": "baseline/audit/audit_manifest.json",
                "candidate_run": "candidate", "candidate_manifest": "candidate/audit/audit_manifest.json"}
        record = persist_comparison(self.root, before, after, source_artifacts=refs)["record"]
        changed = copy.deepcopy(after)
        changed["identity"]["engine"]["parser_version"] = "tampered"
        with self.assertRaises(ComparisonError) as raised:
            verify_comparison_record(record, before, changed)
        self.assertEqual("COMPARISON_HASH_MISMATCH", raised.exception.code)

    def test_existing_record_tampering_is_rejected_on_repeat(self) -> None:
        before, after = self.snapshots()
        refs = {"baseline_run": "baseline", "baseline_manifest": "baseline/audit/audit_manifest.json",
                "candidate_run": "candidate", "candidate_manifest": "candidate/audit/audit_manifest.json"}
        saved = persist_comparison(self.root, before, after, source_artifacts=refs)
        path = Path(saved["path"])
        original_bytes = path.read_bytes()
        tampered = json.loads(path.read_text(encoding="utf-8"))
        tampered["comparison"]["evidence_status"] = "TAMPERED"
        path.write_bytes((json.dumps(tampered, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
        with self.assertRaises(ComparisonError) as raised:
            persist_comparison(self.root, before, after, source_artifacts=refs)
        self.assertEqual("COMPARISON_HASH_MISMATCH", raised.exception.code)
        path.write_bytes(original_bytes)
        tampered = json.loads(original_bytes)
        tampered["created_at_utc"] = "2000-01-01T00:00:00Z"
        path.write_bytes((json.dumps(tampered, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
        with self.assertRaises(ComparisonError) as raised:
            persist_comparison(self.root, before, after, source_artifacts=refs)
        self.assertEqual("COMPARISON_HASH_MISMATCH", raised.exception.code)

    def test_productive_record_is_durable_and_verifiable(self) -> None:
        area = Path(__file__).resolve().parents[1]
        baseline = build_audit_snapshot(area / "reports/evidence/m05d_productive_sources/baseline")
        candidate = build_audit_snapshot(area / "reports/evidence/m05d_productive_sources/candidate")
        record = compare_audits(baseline, candidate)
        path = area / "reports/evidence/comparisons" / record["comparison_id"] / "comparison.json"
        persisted = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(verify_comparison_record(persisted, baseline, candidate))
        self.assertEqual("DATASET_CHANGE", persisted["comparison"]["attribution"])
        self.assertEqual(render_comparison_report(persisted), path.with_name("report.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
