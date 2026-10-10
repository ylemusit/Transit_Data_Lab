from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from gtfs_lab.interpretation.cases import sha256_json, validate_cases


class AuditCaseContractTests(unittest.TestCase):
    def fixture(self):
        interpretation = {"dataset_identity": {"sha256": "a" * 64},
                          "execution_identity": {"audit_execution_id": "RUN-A"},
                          "source_findings": [
                              {"raw_finding_id": "finding-A", "origin": "AUDIT_ENGINE", "rule_id": "G04", "source_file": "trips.txt"},
                              {"raw_finding_id": "finding-B", "origin": "LEGACY", "rule_id": "G04", "source_file": "trips.txt"}]}
        model = {"contract": "TDL_AUDIT_CASES_V1", "version": "1.0.0",
                 "dataset_identity": {"dataset_id": "GTFS-test", "sha256": "a" * 64},
                 "execution_identity": {"audit_execution_id": "RUN-A", "client_audit_id": "AUDIT-A", "manifest_sha256": "b" * 64,
                                        "engine_version": "engine-test"},
                 "source_interpretation": {"contract_version": "1.0.0", "sha256": sha256_json(interpretation)},
                 "coverage": {"source_record_count": 2, "classified_record_count": 2,
                              "reconciled_event_count": 1, "duplicate_source_reference_count": 1,
                              "unclassified_record_count": 0, "accounting_gap": 0,
                              "source_origins": {"AUDIT_ENGINE": 1, "LEGACY": 1}},
                 "unclassified_source_record_ids": [],
                 "technical_result": "INSPECTION_ERROR",
                 "use_readiness": {"status": "NO_ES_POSIBLE_EMITIR_CONCLUSION", "declared_use": None,
                                    "basis": "Compliance inspection error"},
                 "cases": [{"case_id": "C-1", "title": "Caso", "observation": "Observado",
                            "criterion": "Criterio", "applicability": "APPLICABLE", "evaluability": "EVALUABLE",
                            "disposition": "CORRECT", "producer_status": "NO_RESPONSE", "priority": "UNASSESSED",
                            "impact_known": "No medido", "impact_potential": "Por determinar", "action": "Revisar",
                            "owner_suggestion": None, "closure_criteria": "Nueva fuente verificada",
                            "occurrence_count": 2, "reconciled_event_count": 1, "unique_entities": {"trip": 1}, "evidence": [], "limitations": [],
                            "occurrences": [{"assignment": "PRIMARY", "origin": "AUDIT_ENGINE", "rule_id": "G04", "source_file": "trips.txt",
                                             "native_locator": "G04 data_row:4", "normalized_locator": "trips.txt row:5",
                                             "source_record_id": "finding-A"},
                                            {"assignment": "PRIMARY", "origin": "LEGACY", "rule_id": "G04", "source_file": "trips.txt",
                                             "native_locator": "record:6", "normalized_locator": "trips.txt row:5",
                                             "source_record_id": "finding-B"}],
                            "reaudit": {"status": "NOT_REAUDITED", "links": []}}],
                 "limitations": ["V1 accounting is by source record"]}
        return model, interpretation

    def test_valid_lateral_contract_preserves_source_record_accounting(self):
        model, interpretation = self.fixture()
        validate_cases(model, interpretation)

    def test_rejects_occurrence_count_mismatch(self):
        model, interpretation = self.fixture()
        model["cases"][0]["occurrence_count"] = 3
        with self.assertRaisesRegex(ValueError, "occurrence_count mismatch"):
            validate_cases(model, interpretation)

    def test_rejects_v1_identity_mismatch(self):
        model, interpretation = self.fixture()
        interpretation = copy.deepcopy(interpretation)
        interpretation["dataset_identity"]["sha256"] = "c" * 64
        with self.assertRaisesRegex(ValueError, "different source"):
            validate_cases(model, interpretation)

    def test_producer_acceptance_does_not_change_technical_result(self):
        model, interpretation = self.fixture()
        model["cases"][0]["producer_status"] = "REPORTED_ACCEPTED"
        validate_cases(model, interpretation)
        self.assertEqual(model["technical_result"], "INSPECTION_ERROR")

    def test_pending_correction_is_not_verified_closure(self):
        model, interpretation = self.fixture()
        model["cases"][0]["producer_status"] = "REPORTED_CORRECTED"
        model["cases"][0]["reaudit"]["status"] = "NOT_REAUDITED"
        validate_cases(model, interpretation)

    def test_incomplete_source_coverage_remains_explicit(self):
        model, interpretation = self.fixture()
        model["coverage"].update({"source_record_count": 3, "classified_record_count": 2,
                                  "reconciled_event_count": 1, "duplicate_source_reference_count": 1,
                                  "unclassified_record_count": 1, "accounting_gap": 0,
                                  "source_origins": {"AUDIT_ENGINE": 2, "LEGACY": 1}})
        interpretation["source_findings"].append({"raw_finding_id": "finding-C", "origin": "AUDIT_ENGINE",
                                                   "rule_id": "G05", "source_file": "stops.txt"})
        model["unclassified_source_record_ids"] = ["finding-C"]
        model["technical_result"] = "INCOMPLETE"
        model["source_interpretation"]["sha256"] = sha256_json(interpretation)
        validate_cases(model, interpretation)

    def test_rejects_source_reference_missing_from_v1(self):
        model, interpretation = self.fixture()
        model["cases"][0]["occurrences"][0]["source_record_id"] = "unknown-source-record"
        with self.assertRaisesRegex(ValueError, "do not account for V1 source_findings"):
            validate_cases(model, interpretation)

    def test_related_case_reference_does_not_duplicate_primary_accounting(self):
        model, interpretation = self.fixture()
        related = dict(model["cases"][0]["occurrences"][0], assignment="RELATED")
        model["cases"][0]["occurrences"].append(related)
        model["cases"][0]["occurrence_count"] += 1
        validate_cases(model, interpretation)

    def test_resolved_requires_new_evidence_link(self):
        model, interpretation = self.fixture()
        model["cases"][0]["reaudit"]["status"] = "RESOLVED"
        model["cases"][0]["reaudit"]["links"] = [{"relation": "RESOLVED", "execution_id": "RUN-A", "evidence_ref": "evidence.json"}]
        with self.assertRaisesRegex(ValueError, "different execution"):
            validate_cases(model, interpretation)

    def test_resolved_accepts_evidence_from_a_distinct_execution(self):
        model, interpretation = self.fixture()
        model["cases"][0]["reaudit"]["status"] = "RESOLVED"
        model["cases"][0]["reaudit"]["links"] = [{"relation": "RESOLVED", "execution_id": "RUN-B", "evidence_ref": "evidence.json"}]
        validate_cases(model, interpretation)


if __name__ == "__main__":
    unittest.main()
