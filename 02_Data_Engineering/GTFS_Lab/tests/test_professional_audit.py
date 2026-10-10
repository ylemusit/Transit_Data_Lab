from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

from gtfs_lab.professional_audit import build_model, closure_verified, technical_condition, validate_presentation
from gtfs_lab.interpretation.cases import sha256_json, validate_cases
import tests.test_audit_case_contract as fixtures


class ProfessionalAuditTests(unittest.TestCase):
    def fixture(self):
        case_model, interpretation = fixtures.AuditCaseContractTests().fixture()
        interpretation["execution_identity"]["engine_version"] = "synthetic-engine-1"
        interpretation["dataset_identity"]["dataset_id"] = "GTFS-test"
        case_model["execution_identity"]["engine_version"] = "synthetic-engine-1"
        case_model["source_interpretation"]["sha256"] = sha256_json(interpretation)
        case_model["technical_result"] = "FAIL_TECHNICAL"
        decisions = {"contract": "TDL_REVIEWED_DECISIONS", "version": "1.0.0", "case_contract": case_model,
                     "provenance": {"decision_version": "test-1", "criteria_version": "test-rule-1", "criteria_sources": ["synthetic criterion"],
                                    "review_type": "synthetic", "author": "test", "reviewed_at": "2026-10-08", "compatibility": "additive V1"},
                     "closure_profiles": {"C-1": {"criteria_version": "test-rule-1", "closure_checks": ["references_resolve", "intended_relations"]}},
                     "steps": [{"order": 1, "case_ids": ["C-1"], "action": "Revisar relaciones", "basis": "Referencia no resoluble", "missing": "Relación pretendida"}]}
        manifest = {"audit_id": "AUDIT-A", "dataset_identity": {"source_sha256": "a"*64}, "technical_status": "FAIL_TECHNICAL"}
        return manifest, interpretation, decisions

    def test_identity_derived_for_two_executions_and_preserves_technical_values(self):
        for suffix in ("A", "B"):
            manifest, interpretation, decisions = self.fixture()
            manifest["audit_id"] = "AUDIT-" + suffix
            interpretation["execution_identity"]["audit_execution_id"] = "ENGINE-" + suffix
            case_model = decisions["case_contract"]
            case_model["execution_identity"].update(client_audit_id=manifest["audit_id"], audit_execution_id="ENGINE-"+suffix)
            case_model["source_interpretation"]["sha256"] = sha256_json(interpretation)
            model = build_model(manifest, interpretation, "b"*64, "PRESENTATION-"+suffix, decisions)
            self.assertEqual(model["identity"]["audit_execution_id"], "ENGINE-"+suffix)
            self.assertEqual(model["identity"]["revision"], "PRESENTATION-"+suffix)
            self.assertEqual(model["cases"][0]["disposition"], "CORRECT")
            self.assertEqual(model["client_cases"][0]["disposition_text"], "Corregir")
            self.assertNotIn("FAIL_TECHNICAL", model["presentation"]["technical_text"])
            self.assertEqual(decisions["case_contract"]["technical_result"], "FAIL_TECHNICAL")

    def test_unknown_family_is_retained_as_pending_without_borrowing_decisions(self):
        manifest, interpretation, _ = self.fixture()
        interpretation["source_findings"][0]["rule_id"] = "UNKNOWN-FAMILY"
        model = build_model(manifest, interpretation, "b"*64, "PENDING")
        self.assertEqual(len(model["pending_records"]), 2)
        self.assertEqual(model["pending_records"][0]["rule_id"], "UNKNOWN-FAMILY")
        self.assertEqual(model["cases"], [])
        self.assertEqual(model["coverage"]["unclassified_record_count"], 2)
        self.assertIn("no evaluada", model["presentation"]["use_text"])

    def test_no_findings_does_not_imply_destination_approval(self):
        manifest, interpretation, _ = self.fixture()
        interpretation["source_findings"] = []
        manifest["technical_status"] = "PASS"
        model = build_model(manifest, interpretation, "b"*64, "EMPTY")
        self.assertEqual(model["coverage"]["source_record_count"], 0)
        self.assertEqual(model["case_contract"]["use_readiness"]["status"], "NOT_DETERMINED")
        manifest, interpretation, decisions = self.fixture()
        decisions["case_contract"]["use_readiness"]["status"] = "APTO"
        with self.assertRaisesRegex(ValueError, "declared destination"):
            build_model(manifest, interpretation, "b"*64, "UNDECLARED", decisions)

    def test_full_schema_rejects_nested_invalid_enum_and_additional_properties(self):
        manifest, interpretation, decisions = self.fixture()
        for key, value in (("producer_status", "CLAIMED_PASS"), ("unreviewed_override", True)):
            bad = copy.deepcopy(decisions)
            bad["case_contract"]["cases"][0][key] = value
            with self.assertRaises(Exception): build_model(manifest, interpretation, "b"*64, "R", bad)

    def test_missing_full_validator_blocks_delivery_mode(self):
        _, interpretation, decisions = self.fixture()
        import builtins
        original = builtins.__import__
        def blocked(name, *args, **kwargs):
            if name == "jsonschema": raise ImportError("deliberate missing runtime")
            return original(name, *args, **kwargs)
        with patch("builtins.__import__", side_effect=blocked), self.assertRaisesRegex(ValueError, "Full"):
            validate_cases(decisions["case_contract"], interpretation, require_full=True)

    def test_duplicate_case_and_changed_source_identity_are_rejected(self):
        manifest, interpretation, decisions = self.fixture()
        decisions["case_contract"]["cases"].append(copy.deepcopy(decisions["case_contract"]["cases"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate case_id"):
            build_model(manifest, interpretation, "b"*64, "R", decisions)
        _, _, decisions = self.fixture()
        interpretation["dataset_identity"]["sha256"] = "c"*64
        with self.assertRaises(ValueError): build_model(manifest, interpretation, "b"*64, "R", decisions)

    def test_linked_execution_and_producer_acceptance_cannot_close_case(self):
        profile = {"criteria_version": "v1", "closure_checks": ["technical_condition", "geometry_preserved"]}
        evidence = {"execution_id": "NEXT", "source_sha256": "b"*64, "correspondence_ref": "mapping.json", "criteria_version": "v1",
                    "auditor_evidence_ref": "checked.json", "checks": {"technical_condition": True, "geometry_preserved": True}}
        self.assertTrue(closure_verified(profile, evidence, "CURRENT"))
        for field in ("correspondence_ref", "auditor_evidence_ref", "source_sha256", "execution_id"):
            bad = copy.deepcopy(evidence); bad.pop(field)
            self.assertFalse(closure_verified(profile, bad, "CURRENT"), field)
        for change in ({"checks": {"technical_condition": True}}, {"criteria_version": "v2"}, {"execution_id": "CURRENT"}, {"checks": {"producer_accepts": True}}):
            self.assertFalse(closure_verified(profile, evidence | change, "CURRENT"))

    def test_case_specific_conditions_and_boundaries(self):
        self.assertTrue(technical_condition("color", ["", "AbC012"]))
        self.assertFalse(technical_condition("color", [" "]))
        self.assertTrue(technical_condition("reference", (True, {"P"}, ["", "P"])))
        self.assertFalse(technical_condition("reference", (True, {"P"}, [" "])))
        self.assertFalse(technical_condition("reference", (False, {"P"}, [""])))
        self.assertTrue(technical_condition("frequency", (0, 119, 60)))
        self.assertFalse(technical_condition("frequency", (0, 120, 60)))
        self.assertFalse(technical_condition("frequency", (0, 0, 60)))
        self.assertFalse(technical_condition("frequency", (0, 119, 0)))
        self.assertTrue(technical_condition("distance", [0., 1., 2.]))
        self.assertFalse(technical_condition("distance", [0., 1., 1.]))
        self.assertFalse(technical_condition("distance", [0., float("nan")]))

    def test_sequence_requires_all_reviewed_cases_and_valid_references(self):
        manifest, interpretation, decisions = self.fixture()
        for ids in ([], ["UNKNOWN"]):
            bad = copy.deepcopy(decisions); bad["steps"][0]["case_ids"] = ids
            with self.assertRaises(ValueError): build_model(manifest, interpretation, "b"*64, "R", bad)

    def test_client_projection_cannot_lose_case(self):
        manifest, interpretation, decisions = self.fixture()
        model = build_model(manifest, interpretation, "b"*64, "R", decisions)
        model["client_cases"] = []
        with self.assertRaises(ValueError): validate_presentation(model, interpretation)

    def test_review_mutations_identity_closure_pending_and_locator_rejected(self):
        manifest, interpretation, decisions = self.fixture()
        model = build_model(manifest, interpretation, "b"*64, "R", decisions)
        bad = copy.deepcopy(model); bad["identity"]["client_audit_id"] = "UNRELATED"
        with self.assertRaises(ValueError): validate_presentation(bad, interpretation)
        bad = copy.deepcopy(model); bad["client_cases"][0]["closure_criteria"] = "Producer accepts"
        with self.assertRaises(ValueError): validate_presentation(bad, interpretation)
        pending = build_model(manifest, interpretation, "b"*64, "R")
        pending["pending_records"] = []
        with self.assertRaises(ValueError): validate_presentation(pending, interpretation)
        interpretation["source_findings"][0]["row_locator"] = "data_row:4"
        decisions["case_contract"]["source_interpretation"]["sha256"] = sha256_json(interpretation)
        with self.assertRaisesRegex(ValueError, "locator mismatch"):
            build_model(manifest, interpretation, "b"*64, "R", decisions)

    def test_resolved_rejects_current_engine_and_unrelated_evidence(self):
        manifest, interpretation, decisions = self.fixture()
        case = decisions["case_contract"]["cases"][0]
        case["reaudit"] = {"status": "RESOLVED", "links": [{"relation": "RESOLVED", "execution_id": "NEXT", "evidence_ref": "verified.json"}]}
        good = {"execution_id": "NEXT", "source_sha256": "c"*64, "correspondence_ref": "mapping.json", "auditor_evidence_ref": "verified.json",
                "criteria_version": "test-rule-1", "checks": {"references_resolve": True, "intended_relations": True}}
        decisions["closure_verifications"] = {"C-1": good}
        build_model(manifest, interpretation, "b"*64, "R", decisions)
        for field, value in (("execution_id", "RUN-A"), ("auditor_evidence_ref", "other.json"), ("execution_id", "UNRELATED")):
            bad = copy.deepcopy(decisions); bad["closure_verifications"]["C-1"][field] = value
            with self.assertRaises(ValueError): build_model(manifest, interpretation, "b"*64, "R", bad)

    def test_source_origins_version_and_dataset_cannot_be_fabricated(self):
        manifest, interpretation, decisions = self.fixture()
        for area, field, value in (("coverage", "source_origins", {"FABRICATED": 2}), ("dataset_identity", "dataset_id", "OTHER"), ("execution_identity", "engine_version", "other-engine")):
            bad = copy.deepcopy(decisions); bad["case_contract"][area][field] = value
            with self.assertRaises(ValueError): build_model(manifest, interpretation, "b"*64, "R", bad)


if __name__ == "__main__": unittest.main()
