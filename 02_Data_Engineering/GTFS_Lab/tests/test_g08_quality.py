import unittest
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import zipfile

from gtfs_lab.g08_quality import RULES, evaluate_g08, evaluate_g08_run, register_g08_rules
from gtfs_lab.gate import create_fixtures
from gtfs_lab.pipeline import run
from gtfs_lab.rule_registry import RuleRegistry


class G08QualityTests(unittest.TestCase):
    def test_declared_recommended_fields_pass_without_findings(self):
        result = evaluate_g08(tuple(RULES.values()), g03_feed_info_status="PASS")

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["findings"], [])
        self.assertTrue(all(rule["status"] == "PASS" for rule in result["rules"]))

    def test_absent_recommended_headers_emit_informational_findings_only(self):
        result = evaluate_g08(("feed_publisher_name",), g03_feed_info_status="PASS")

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(result["findings"]), len(RULES))
        self.assertTrue(all(finding["severity"] == "INFO" for finding in result["findings"]))
        self.assertTrue(all(finding["authority"] == "GTFS_RECOMMENDED" for finding in result["findings"]))

    def test_file_absence_requires_g03_not_applicable_evidence(self):
        absent = evaluate_g08(None, g03_feed_info_status="NOT_APPLICABLE")
        uncertain = evaluate_g08(None, g03_feed_info_status="NOT_EVALUABLE")

        self.assertTrue(all(rule["status"] == "NOT_APPLICABLE" for rule in absent["rules"]))
        self.assertTrue(all(rule["status"] == "NOT_EVALUABLE" for rule in uncertain["rules"]))
        self.assertEqual(uncertain["status"], "NOT_EVALUABLE")

    def test_g03_source_evidence_unavailable_is_not_evaluable(self):
        result = evaluate_g08_run(SimpleNamespace(tables={}), {"status": "PASS"})
        self.assertEqual("NOT_EVALUABLE", result["status"])
        self.assertTrue(all(rule["status"] == "NOT_EVALUABLE" for rule in result["rules"]))

    def test_untrusted_structure_and_disabled_rule_are_not_evaluable(self):
        uncertain = evaluate_g08(tuple(RULES.values()), g03_feed_info_status="FAIL_TECHNICAL")
        disabled = evaluate_g08(tuple(RULES.values()), g03_feed_info_status="PASS", enabled_rule_ids=[])

        self.assertTrue(all(rule["status"] == "NOT_EVALUABLE" for rule in uncertain["rules"]))
        self.assertEqual(uncertain["findings"], [])
        self.assertEqual(disabled["status"], "NOT_EVALUABLE")
        self.assertEqual(disabled["findings"], [])

    def test_unknown_rule_id_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_g08((), g03_feed_info_status="PASS", enabled_rule_ids=["UNKNOWN"])

    def test_typed_registry_identity_and_registration_are_deterministic(self):
        first = register_g08_rules()
        second = register_g08_rules()
        self.assertTrue(first.frozen)
        self.assertEqual(first.identity_map(), second.identity_map())
        self.assertEqual(sorted(RULES), list(first.identity_map()["rule_versions"]))
        for definition in first:
            self.assertEqual("QUALITY", definition.category.value)
            self.assertEqual("GTFS_RECOMMENDED", definition.authority.value)
            self.assertEqual("INFO", definition.severity.value)
            self.assertEqual("RECOMMENDED", definition.requirement.value)
        mutable = RuleRegistry()
        self.assertIs(mutable, register_g08_rules(mutable))
        self.assertEqual(3, len(mutable))
        with self.assertRaises(ValueError):
            register_g08_rules(mutable)

    def test_recommendation_outcome_and_coverage_serialize_separately(self):
        result = evaluate_g08(("publisher_name",), g03_feed_info_status="PASS")
        self.assertEqual("PASS", result["status"])
        self.assertFalse(result["rules"][0]["recommendation_met"])
        self.assertEqual("FEATURE_PRESENT_FULLY_AUDITED", result["rules"][0]["coverage"]["state"])
        restored = json.loads(json.dumps(result, sort_keys=True))
        self.assertEqual(result, restored)

    def test_aggregation_keeps_inspection_limitation_visible(self):
        result = evaluate_g08((), g03_feed_info_status="PASS",
                              enabled_rule_ids=[next(iter(RULES))])
        self.assertEqual("NOT_EVALUABLE", result["status"])
        self.assertEqual(1, len(result["findings"]))
        self.assertEqual(2, sum(rule["status"] == "NOT_EVALUABLE" for rule in result["rules"]))
        self.assertEqual(1, sum(rule["status"] == "PASS" for rule in result["rules"]))

    def test_pipeline_integration_writes_g08_without_legacy_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = create_fixtures(root / "fixtures")["ORPHAN_ROUTE"]
            result = run(fixture, root / "runs")
            run_dir = root / "runs" / result["run_id"]
            self.assertIn("g08", result)
            self.assertEqual("NOT_APPLICABLE", result["g08"]["status"])
            self.assertTrue((run_dir / "g08.json").is_file())
            self.assertEqual(result["g08"], json.loads((run_dir / "g08.json").read_text(encoding="utf-8")))
            self.assertTrue((run_dir / "engine_report.json").is_file())
            self.assertTrue((run_dir / "engine_report.md").is_file())
            manifest = json.loads((run_dir / "audit" / "audit_manifest.json").read_text(encoding="utf-8"))
            self.assertNotIn("engine_report", manifest["artifacts"])
            self.assertNotIn("g08", manifest["run_outcome"])
            legacy_ids = {rule["rule_id"] for rule in result["validation"]["rules"]}
            self.assertTrue(legacy_ids.isdisjoint(RULES))
            report = (run_dir / "engine_report.md").read_text(encoding="utf-8")
            self.assertIn("GTFS Audit Engine V1", report)
            second = run(fixture, root / "runs")
            second_dir = root / "runs" / second["run_id"]
            self.assertEqual((run_dir / "engine_report.json").read_bytes(),
                             (second_dir / "engine_report.json").read_bytes())
            self.assertEqual((run_dir / "engine_report.md").read_bytes(),
                             (second_dir / "engine_report.md").read_bytes())

    def test_pipeline_keeps_unmet_recommendations_out_of_conformance_and_m02(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = create_fixtures(root / "fixtures")["ORPHAN_ROUTE"]
            target = root / "recommendation-absent.zip"
            with zipfile.ZipFile(source) as original, zipfile.ZipFile(target, "w") as modified:
                for member in original.infolist():
                    modified.writestr(member.filename, original.read(member.filename))
                modified.writestr("feed_info.txt",
                                  "feed_publisher_name,feed_publisher_url,feed_lang\n"
                                  "Synthetic Transit,https://example.org,en\n")
            result = run(target, root / "runs")
            run_dir = root / "runs" / result["run_id"]
            self.assertEqual("PASS", result["g08"]["status"])
            self.assertEqual(3, len(result["g08"]["findings"]))
            self.assertTrue(all(row["severity"] == "INFO" for row in result["g08"]["findings"]))
            self.assertTrue({row["rule_id"] for row in result["validation"]["rules"]}.isdisjoint(RULES))
            engine_report = json.loads((run_dir / "engine_report.json").read_text(encoding="utf-8"))
            self.assertEqual(3, len(engine_report["recommendation_findings"]))
            self.assertFalse(any(row["stage"] == "G08"
                                 for row in engine_report["technical_evaluation"]["findings"]))
            manifest = json.loads((run_dir / "audit" / "audit_manifest.json").read_text(encoding="utf-8"))
            normalized = json.loads((run_dir / "audit" / "findings.normalized.json").read_text(encoding="utf-8"))
            self.assertNotIn("g08", manifest["run_outcome"])
            self.assertNotIn("engine_report", manifest["artifacts"])
            self.assertFalse(any(row.get("rule_id") in RULES for row in normalized["findings"]))


if __name__ == "__main__":
    unittest.main()
