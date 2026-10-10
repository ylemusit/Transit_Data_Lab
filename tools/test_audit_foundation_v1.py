"""Focused acceptance checks for engagement boundaries and crosswalk integrity."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from tools.audit_foundation_v1 import build_crosswalk, engagement_gate

ROOT = Path(__file__).resolve().parents[1]


class EngagementTests(unittest.TestCase):
    def example(self, name):
        return json.loads((ROOT / "reports/audit_foundation_v1" / name).read_text(encoding="utf-8"))

    def test_unknown_destination_and_real_service_block_claims(self):
        gate = engagement_gate(self.example("engagement_gtfs_synthetic.json"))
        self.assertIn("TECHNICAL_RESULTS", gate["eligible_categories"])
        self.assertIn("DESTINATION_SUITABILITY", gate["blocked_requested_categories"])
        self.assertIn("SERVICE_TRUTH", gate["blocked_requested_categories"])
        self.assertFalse(gate["positive_conclusion"])

    def test_schema_does_not_enable_profile_claim(self):
        data = self.example("engagement_netex_synthetic.json")
        data["reference"]["schema_sha256"] = "a" * 64
        gate = engagement_gate(data)
        self.assertIn("SCHEMA_RESULTS", gate["eligible_categories"])
        self.assertIn("PROFILE_RESULTS", gate["blocked_requested_categories"])

    def test_legal_and_certification_never_enabled_by_technical_reference(self):
        data = self.example("engagement_gtfs_synthetic.json")
        data["requested_claims"] = ["LEGAL_COMPLIANCE", "CERTIFICATION"]
        self.assertEqual(len(engagement_gate(data)["blocked_requested_categories"]), 2)

    def test_unsupported_format_rejected(self):
        data = self.example("engagement_gtfs_synthetic.json")
        data["format"] = "SIRI"
        with self.assertRaises(ValueError): engagement_gate(data)

    def test_unknown_control_rejected(self):
        data = self.example("engagement_gtfs_synthetic.json")
        data["included_controls"] = ["UNIMPLEMENTED-CONTROL"]
        with self.assertRaises(ValueError): engagement_gate(data)

    def test_schema_identity_must_be_a_sha256(self):
        data = self.example("engagement_netex_synthetic.json")
        data["reference"]["schema_sha256"] = "unknown"
        with self.assertRaises(ValueError): engagement_gate(data)


class CrosswalkTests(unittest.TestCase):
    def data(self):
        model = {"matrix": [{"rule_id": "GTFS-X", "status": "FAIL_TECHNICAL"}],
                 "cases": [{"case_id": "CASE-1", "occurrences": [{"rule_id": "GTFS-X"}]}],
                 "coverage": {"source_record_count": 1, "reconciled_event_count": 1}}
        rows = [{"rule_id": "GTFS-X", "result": "FAIL_TECHNICAL"}]
        view = [{"rule_id": "GTFS-X", "status": "FAIL_TECHNICAL", "case_ids": ["CASE-1"], "source": "source.json"}]
        return model, rows, view, {"entries": []}

    def test_source_projection_linked_to_case(self):
        result = build_crosswalk(*self.data())
        self.assertEqual(result["controls"][0]["case_ids"], ["CASE-1"])

    def test_orphan_control_rejected(self):
        args = self.data(); args[1][0]["rule_id"] = "ORPHAN"
        with self.assertRaises(ValueError): build_crosswalk(*args)

    def test_divergent_result_rejected(self):
        args = self.data(); args[2][0]["status"] = "PASS"
        with self.assertRaises(ValueError): build_crosswalk(*args)

    def test_missing_case_projection_rejected(self):
        args = self.data(); args[2][0]["case_ids"] = []
        with self.assertRaises(ValueError): build_crosswalk(*args)

    def test_orphan_normative_reference_rejected(self):
        args = self.data(); args[3]["entries"] = [{"id": "UE-X", "rules": ["ORPHAN"]}]
        with self.assertRaises(ValueError): build_crosswalk(*args)

    def test_unreviewed_duplicate_projection_rejected(self):
        args = self.data(); args[1].append(deepcopy(args[1][0]))
        with self.assertRaises(ValueError): build_crosswalk(*args)


if __name__ == "__main__":
    unittest.main()
