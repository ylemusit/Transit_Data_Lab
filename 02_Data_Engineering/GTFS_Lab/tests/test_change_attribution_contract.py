"""Deterministic synthetic proof for ChangeAttribution 1.0.0."""
from __future__ import annotations

import copy
import unittest

from gtfs_lab.change_attribution import compare

SHA_A = "a" * 64
SHA_B = "b" * 64


def snapshot(audit_id: str = "audit-a", *, source: str = SHA_A, parser: str = "parser/1", evaluator: str = "evaluator/1", rule_version: str = "1.0", status: str = "PASS", findings: list[dict] | None = None, timestamp: str = "2026-09-29T00:00:00Z") -> dict:
    findings = copy.deepcopy(findings or [])
    return {
        "audit_id": audit_id,
        "run_id": audit_id,
        "timestamp": timestamp,
        "identity": {
            "dataset": {"source_sha256": source, "dataset_id": "feed-a", "lineage_id": "lineage-a"},
            "engine": {"git_commit": "1111111", "parser_version": parser, "validator_version": "validator/1", "gtfs_lab_version": "gtfs-lab/1"},
            "rules": {"ruleset_id": "rules", "ruleset_version": "1", "rule_id": "R1", "rule_version": rule_version},
            "compliance": {"semantic_rule_version": "compliance-v1/1", "evaluator_version": evaluator, "evaluator_sha256": SHA_A, "package_sha256": SHA_A, "reference_sha256": SHA_A},
            "configuration": {"sha256": SHA_A},
        },
        "result": {"rules": [{"rule_id": "R1", "status": status, "findings": findings}]},
        "findings": findings,
    }


def finding(finding_id: str = "f-1", state: str = "DETECTED", evidence_note: str = "one") -> dict:
    return {"finding_id": finding_id, "lifecycle_state": state, "evidence_note": evidence_note}


class ChangeAttributionContractTests(unittest.TestCase):
    def test_ca001_identical_audits_are_no_change(self) -> None:
        result = compare(snapshot(), snapshot())
        self.assertEqual("NO_CHANGE", result["attribution"])
        self.assertFalse(result["result_change"]["changed"])

    def test_ca002_parser_change_is_implementation_only_if_result_stays_same(self) -> None:
        result = compare(snapshot(), snapshot(parser="parser/2"))
        self.assertEqual("PARSER_IMPLEMENTATION_CHANGE", result["attribution"])
        self.assertFalse(result["result_change"]["changed"])

    def test_ca003_compliance_evaluator_upgrade_keeps_rule_semantics_separate(self) -> None:
        result = compare(snapshot(), snapshot(evaluator="evaluator/2"))
        self.assertEqual("COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE", result["attribution"])
        self.assertFalse(result["rules_change"])

    def test_ca004_changed_source_hash_is_dataset_change(self) -> None:
        result = compare(snapshot(), snapshot(source=SHA_B))
        self.assertEqual("DATASET_CHANGE", result["attribution"])
        self.assertTrue(result["dataset_change"])

    def test_ca005_dataset_change_and_new_finding_are_both_reported(self) -> None:
        result = compare(snapshot(), snapshot(source=SHA_B, findings=[finding()]))
        self.assertEqual("DATASET_CHANGE", result["attribution"])
        self.assertEqual("NEW_FINDING", result["finding_change"]["changes"][0]["change"])

    def test_ca006_rule_version_change_and_result_change(self) -> None:
        result = compare(snapshot(), snapshot(rule_version="2.0", status="FAIL_TECHNICAL"))
        self.assertEqual("RULE_SEMANTIC_CHANGE", result["attribution"])
        self.assertTrue(result["rules_change"])
        self.assertEqual("STATUS_CHANGED", result["result_change"]["status"])

    def test_ca007_runtime_metadata_does_not_change_semantics(self) -> None:
        result = compare(snapshot("audit-a"), snapshot("audit-b", timestamp="2026-09-30T00:00:00Z"))
        self.assertEqual("RUNTIME_ONLY_CHANGE", result["attribution"])
        self.assertFalse(result["result_change"]["changed"])

    def test_ca008_disappearing_finding_is_resolved(self) -> None:
        result = compare(snapshot(findings=[finding()]), snapshot())
        self.assertEqual("RESOLVED_FINDING", result["finding_change"]["changes"][0]["change"])

    def test_ca009_dataset_and_ruleset_change_are_multiple_causes(self) -> None:
        candidate = snapshot(source=SHA_B)
        candidate["identity"]["rules"]["ruleset_version"] = "2"
        result = compare(snapshot(), candidate)
        self.assertEqual("MULTIPLE_CAUSES", result["attribution"])
        self.assertEqual(["DATASET_CHANGE", "RULESET_CHANGE"], result["supported_causes"])

    def test_ca010_result_change_with_equal_known_identity_is_unattributed(self) -> None:
        result = compare(snapshot(), snapshot(status="FAIL_TECHNICAL"))
        self.assertEqual("UNATTRIBUTED_CHANGE", result["attribution"])
        self.assertEqual("NO_CAUSAL_EVIDENCE", result["confidence_or_evidence_status"]["status"])

    def test_semantic_identity_change_is_not_implementation_change(self) -> None:
        result = compare(snapshot(), snapshot(rule_version="1.1"))
        self.assertEqual("RULE_SEMANTIC_CHANGE", result["attribution"])

    def test_package_reference_and_configuration_changes_are_distinct(self) -> None:
        for field, category in (("package_sha256", "COMPLIANCE_PACKAGE_CHANGE"), ("reference_sha256", "REFERENCE_CHANGE")):
            candidate = snapshot()
            candidate["identity"]["compliance"][field] = SHA_B
            self.assertEqual(category, compare(snapshot(), candidate)["attribution"])
        candidate = snapshot()
        candidate["identity"]["configuration"]["sha256"] = SHA_B
        result = compare(snapshot(), candidate)
        self.assertEqual("CONFIGURATION_CHANGE", result["attribution"])
        self.assertTrue(result["configuration_change"])

    def test_finding_lifecycle_and_evidence_changes_keep_stable_identity(self) -> None:
        baseline = snapshot(findings=[finding(state="DETECTED", evidence_note="before")])
        status_change = snapshot(findings=[finding(state="REPRODUCED", evidence_note="before")])
        result = compare(baseline, status_change)
        self.assertEqual("FINDING_STATUS_CHANGE", result["finding_change"]["changes"][0]["change"])
        evidence_change = snapshot(findings=[finding(state="DETECTED", evidence_note="after")])
        result = compare(baseline, evidence_change)
        self.assertEqual("FINDING_EVIDENCE_CHANGE", result["finding_change"]["changes"][0]["change"])

    def test_sha256_is_case_insensitive_and_invalid_values_reject(self) -> None:
        candidate = snapshot(source=SHA_A.upper())
        self.assertEqual("NO_CHANGE", compare(snapshot(), candidate)["attribution"])
        candidate["identity"]["dataset"]["source_sha256"] = "bad"
        with self.assertRaises(ValueError):
            compare(snapshot(), candidate)

    def test_result_finding_order_is_not_a_semantic_change(self) -> None:
        rows = [finding("f-a"), finding("f-b")]
        baseline = snapshot(findings=rows)
        candidate = snapshot(findings=list(reversed(rows)))
        result = compare(baseline, candidate)
        self.assertEqual("NO_CHANGE", result["attribution"])
        self.assertFalse(result["result_change"]["changed"])

    def test_missing_source_identity_is_explicit_and_fails_closed(self) -> None:
        baseline = snapshot()
        candidate = snapshot(status="FAIL_TECHNICAL")
        del baseline["identity"]["dataset"]["source_sha256"]
        del candidate["identity"]["dataset"]["source_sha256"]
        result = compare(baseline, candidate)
        self.assertEqual("UNATTRIBUTED_CHANGE", result["attribution"])
        self.assertEqual("MISSING_IDENTITY", result["confidence_or_evidence_status"]["status"])


if __name__ == "__main__":
    unittest.main()
