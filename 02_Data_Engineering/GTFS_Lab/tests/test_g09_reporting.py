from __future__ import annotations

import json
import unittest

from gtfs_lab.g09_reporting import build_engine_report, render_engine_report


class G09ReportingTests(unittest.TestCase):
    def fixture(self):
        return {
            "dataset": {"dataset_id": "synthetic-1", "source_sha256": "a" * 64},
            "g03": {"status": "PASS", "rules": [
                {"rule_id": "GTFS-G03-CSV-STRUCTURE", "semantic_version": "1.0.0",
                 "applicability": "APPLICABLE", "description": "CSV row width",
                 "specification_reference": "GTFS Schedule Reference 2026-04-27",
                 "status": "NOT_EVALUABLE", "coverage": {"state": "FEATURE_PRESENT_PARTIALLY_AUDITED"},
                 "findings": [{"file": "stops.txt", "row_locator": "ROW:1", "technical_reason": "bad width"}]},
            ]},
            "g04": {"status": "PASS", "rules": [], "legacy_comparison": [{"legacy_rule_id": "legacy-a"}]},
            "g05": {"status": "NOT_APPLICABLE", "rules": []},
            "g06": {"status": "NOT_EVALUABLE", "rules": []},
            "g07": {"status": "PASS", "rules": []},
            "g08": {"status": "PASS", "rules": [
                {"rule_id": "GTFS-G08-REC", "semantic_version": "1.0.0", "authority": "GTFS_RECOMMENDED",
                 "severity": "INFO", "requirement": "RECOMMENDED", "status": "PASS",
                 "recommendation_met": False, "coverage": {"state": "FEATURE_PRESENT_FULLY_AUDITED"}, "findings": [
                     {"source_file": "feed_info.txt", "recommendation": "declare field"}],
            }]},
            "g03_file_catalog": {"members": [
                {"classification": "OFFICIAL_DEFERRED", "official_identity": "fare_attributes.txt"},
            ]},
            "validation": {"status": "PASS", "finding_count": 0, "findings": []},
        }

    def test_machine_and_human_outputs_preserve_stage_boundaries_and_gaps(self):
        source = self.fixture()
        report = build_engine_report(source)
        encoded = json.dumps(report, sort_keys=True, ensure_ascii=False)
        self.assertEqual(encoded, json.dumps(build_engine_report(source), sort_keys=True, ensure_ascii=False))
        self.assertIn("GTFS-G03-CSV-STRUCTURE", encoded)
        matrix_rule = report["technical_evaluation"]["stages"][0]["rules"][0]
        self.assertEqual("APPLICABLE", matrix_rule["applicability"])
        self.assertEqual("CSV row width", matrix_rule["description"])
        self.assertEqual("GTFS Schedule Reference 2026-04-27", matrix_rule["specification_reference"])
        self.assertEqual(False, report["recommendation_outcomes"][0]["recommendation_met"])
        self.assertEqual("GTFS_RECOMMENDED", report["recommendation_findings"][0]["authority"])
        self.assertIn("fare_attributes.txt", report["deferred_features"])
        self.assertEqual(18, len(report["deferred_features"]))
        self.assertTrue(report["known_gaps"])
        self.assertFalse(any("score" in key for key in report))
        self.assertFalse(report["persistence_boundary"]["m02_modified"])
        markdown = render_engine_report(report)
        self.assertIn("NOT_EVALUABLE", markdown)
        self.assertIn("No se calcula score global", markdown)
        self.assertIn("GTFS_RECOMMENDED", markdown)

    def test_missing_stage_is_explicitly_not_evaluable(self):
        source = {"dataset": {}, "g03": {}, "g03_file_catalog": {"members": []}, "validation": {}}
        report = build_engine_report(source)
        self.assertEqual("NOT_EVALUABLE", report["technical_evaluation"]["stages"][1]["status"])
        self.assertEqual("G04", report["known_gaps"][0]["stage"])
        self.assertNotIn("global_score", report)


if __name__ == "__main__":
    unittest.main()
