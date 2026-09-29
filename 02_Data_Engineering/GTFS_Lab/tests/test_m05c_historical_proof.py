"""Regression against persisted M04 B1/B3 evidence (read-only)."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from gtfs_lab.historical_comparison import compare_historical_summaries


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "reports" / "evidence"


class M05CHistoricalProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.v1_path = EVIDENCE / "holdout_evaluation_v1" / "first_evaluation_summary.json"
        cls.v2_path = EVIDENCE / "holdout_evaluation_v2" / "evaluation_summary.json"
        cls.v1 = json.loads(cls.v1_path.read_text(encoding="utf-8"))
        cls.v2 = json.loads(cls.v2_path.read_text(encoding="utf-8"))
        cls.proof = compare_historical_summaries(
            cls.v1, cls.v2,
            refs={"baseline": cls.v1_path.as_posix(), "candidate": cls.v2_path.as_posix()},
        )
        cls.by_id = {row["dataset_id"]: row for row in cls.proof["datasets"]}

    def test_all_six_persisted_source_hashes_match(self) -> None:
        self.assertEqual(6, len(self.by_id))
        self.assertTrue(all(row["source_sha256"]["status"] == "MATCH" for row in self.by_id.values()))

    def test_006_parser_and_evaluator_change_has_unchanged_results(self) -> None:
        row = self.by_id["006"]
        self.assertEqual("UNCHANGED_STATUS", row["result_change"]["status"])
        self.assertFalse(row["result_change"]["changed"])
        self.assertEqual("MULTIPLE_CAUSES", row["attribution"])
        self.assertEqual({"PARSER_IMPLEMENTATION_CHANGE", "COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE"}, set(row["supported_causes"]))

    def test_008_keeps_b1_failure_and_fails_closed_without_results(self) -> None:
        row = self.by_id["008"]
        self.assertEqual("PIPELINE_FAILED", row["pipeline_status"]["baseline"])
        self.assertEqual("NOT_COMPARABLE", row["evidence_state"])
        self.assertEqual("NOT_COMPARABLE", row["attribution"])
        self.assertIn("RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0",
                      row["comparability"]["reasons"])
        self.assertIn("EMPTY_CSV_RECORD_IGNORED", row["historical_support"]["candidate_warnings"][0])
        self.assertIn("PARSER_IMPLEMENTATION_CHANGE", row["supporting_historical_interpretation"])

    def test_compliance_changes_are_reproduced_without_inventing_package_change(self) -> None:
        for dataset_id in ("013", "015", "017", "018"):
            row = self.by_id[dataset_id]
            self.assertTrue(row["result_change"]["changed"])
            self.assertIn("COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE", row["supported_causes"])
            self.assertNotIn("COMPLIANCE_PACKAGE_CHANGE", row["supported_causes"])
            self.assertEqual("PARTIAL", row["evidence_state"])

    def test_lineage_and_references_are_preserved(self) -> None:
        self.assertEqual(6, self.proof["lineage"]["dataset_count"])
        self.assertEqual(5, self.proof["lineage"]["independent_lineage_unit_count"])
        self.assertEqual("LINEAGE-013-015", self.by_id["013"]["lineage_unit"])
        self.assertEqual("LINEAGE-013-015", self.by_id["015"]["lineage_unit"])
        for row in self.by_id.values():
            self.assertEqual(2, len(row["evidence_refs"]))
            self.assertTrue(all(ref["json_pointer"].startswith("/datasets/") for ref in row["evidence_refs"]))


if __name__ == "__main__":
    unittest.main()
