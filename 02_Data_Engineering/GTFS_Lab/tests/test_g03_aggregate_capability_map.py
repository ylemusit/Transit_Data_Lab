import json
import unittest
from pathlib import Path

from gtfs_lab.g03_capability_map import regenerate
from gtfs_lab.g03_structure import aggregate_g03_statuses


class G03AggregateTests(unittest.TestCase):
    def test_all_pass_is_full(self):
        result = aggregate_g03_statuses({"a": {"status": "PASS"}, "b": {"status": "PASS"}})
        self.assertEqual("PASS", result["status"])
        self.assertEqual("FULL", result["coverage"]["coverage_state"])
        self.assertEqual(2, result["coverage"]["evaluated_count"])

    def test_pass_and_not_evaluable_cannot_claim_pass(self):
        result = aggregate_g03_statuses({"a": {"status": "PASS"}, "b": {"status": "NOT_EVALUABLE"}})
        self.assertEqual("NOT_EVALUABLE", result["status"])
        self.assertEqual("PARTIAL", result["coverage"]["coverage_state"])
        self.assertEqual(1, result["coverage"]["not_evaluable_count"])

    def test_not_applicable_does_not_block_full_applicable_coverage(self):
        result = aggregate_g03_statuses({"a": {"status": "PASS"}, "b": {"status": "NOT_APPLICABLE"}})
        self.assertEqual("PASS", result["status"])
        self.assertEqual(1, result["coverage"]["total_applicable_count"])
        self.assertEqual(1, result["coverage"]["not_applicable_count"])

    def test_fail_and_not_evaluable_preserves_failure_and_partial_coverage(self):
        result = aggregate_g03_statuses({"a": {"status": "FAIL_TECHNICAL"}, "b": {"status": "NOT_EVALUABLE"}})
        self.assertEqual("FAIL_TECHNICAL", result["status"])
        self.assertEqual("PARTIAL", result["coverage"]["coverage_state"])

    def test_all_not_evaluable(self):
        result = aggregate_g03_statuses({"a": {"status": "NOT_EVALUABLE"}})
        self.assertEqual("NOT_EVALUABLE", result["status"])

    def test_zero_applicable_rows(self):
        result = aggregate_g03_statuses({"a": {"status": "NOT_APPLICABLE"}})
        self.assertEqual("NOT_APPLICABLE", result["status"])
        self.assertEqual("NO_APPLICABLE_CASES", result["coverage"]["coverage_state"])

    def test_capability_map_regenerates_byte_for_byte(self):
        artifact = Path(__file__).resolve().parents[1] / "spec" / "gtfs_schedule_field_capability_map_2026_04_27.json"
        self.assertEqual(regenerate(), artifact.read_bytes())
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        self.assertTrue(all(row["derivation_reason"] for row in payload["fields"]))
        self.assertEqual(len(payload["fields"]), sum(payload["primary_assessment_counts"].values()))
        self.assertTrue(payload["inputs"]["field_contract_sha256"])
        self.assertTrue(payload["output_sha256"])


if __name__ == "__main__":
    unittest.main()
