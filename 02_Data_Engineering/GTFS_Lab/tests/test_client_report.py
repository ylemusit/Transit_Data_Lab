from __future__ import annotations

import unittest
import json
from pathlib import Path

from gtfs_lab.client_report import REPORT_CONTRACT, SECTIONS, build_client_report, render_client_report


class ClientReportTests(unittest.TestCase):
    def fixture(self):
        manifest = {"audit_id": "A-1", "client_project_id": "C-1", "status": "COMPLETED",
                    "dataset_identity": {"dataset_id": "GTFS-1", "source_filename": "feed.zip",
                                         "source_sha256": "a" * 64, "source_size_bytes": 20,
                                         "ingestion_timestamp_utc": "2026-10-06T00:00:00Z"},
                    "audit_interpretation": {"status": "INTERPRETATION_COMPLETED"}}
        run = {"started_at_utc": "2026-10-06T00:00:00Z", "summary": {"validation": "PASS"},
               "engine_report": {"technical_evaluation": {"stages": [
                   {"stage": "G03", "rules": [
                       {"rule_id": "R-PASS", "status": "PASS", "findings": []},
                       {"rule_id": "R-NA", "status": "NOT_APPLICABLE", "findings": []},
                       {"rule_id": "R-NE", "status": "NOT_EVALUABLE", "findings": []}]},
               ]}}, "validation": {"rules": []},
               "compliance_v1": {"rule_id": "C1", "rule_version": "compliance-v1/1",
                                  "result": "PASS", "reference_sha256": "b" * 64,
                                  "evaluator_version": "compliance-v1/2"}, "gis": {}}
        interpretation = {"coverage": {"raw_finding_count": 0, "consolidated_occurrence_count": 0,
                                       "unclassified_occurrence_count": 0, "accounting_gap": 0},
                          "finding_families": []}
        return manifest, run, interpretation

    def test_contract_projects_full_rule_matrix_and_distinguishes_states(self):
        manifest, run, interpretation = self.fixture()
        report = build_client_report(manifest, run, [], interpretation,
                                     {"decision": "NOT_REMEDIABLE", "reason": "Sin hallazgos"}, None)
        self.assertEqual(REPORT_CONTRACT, report["contract"])
        self.assertEqual(29, len(report["sections"]))
        self.assertEqual({"R-PASS", "R-NA", "R-NE", "C1"},
                         {row["rule_id"] for row in report["validation_matrix"]})
        self.assertEqual("NOT_APPLICABLE", next(row for row in report["validation_matrix"]
                                                 if row["rule_id"] == "R-NA")["applicability"])
        self.assertEqual("NOT_EVALUABLE", next(row for row in report["validation_matrix"]
                                                if row["rule_id"] == "R-NE")["evaluability"])
        self.assertIsNone(next(row for row in report["validation_matrix"]
                               if row["rule_id"] == "R-PASS")["applicability"])
        self.assertEqual("NO ES POSIBLE EMITIR CONCLUSIÓN", report["summary"]["publication_readiness"])
        markdown = render_client_report(report)
        self.assertIn("## 29. Anexos técnicos", markdown)
        self.assertIn("VERSION_UNKNOWN", markdown)
        self.assertIn("NO DISPONIBLE EN ARTEFACTO", markdown)
        self.assertIn("certificación administrativa", markdown.lower())
        self.assertIn("R-NE", markdown)

    def test_publication_conclusion_requires_zero_accounting_gap(self):
        manifest, run, interpretation = self.fixture()
        run["engine_report"]["technical_evaluation"]["stages"][0]["rules"] = [
            {"rule_id": "R-PASS", "status": "PASS", "findings": []}]
        interpretation["coverage"]["accounting_gap"] = 1
        report = build_client_report(manifest, run, [], interpretation, {"decision": "NONE"}, None)
        self.assertEqual("NO ES POSIBLE EMITIR CONCLUSIÓN", report["summary"]["publication_readiness"])

    def test_contract_spec_matches_required_report_sections(self):
        spec = Path(__file__).parents[1] / "spec" / "client_report_contract_v1.json"
        payload = json.loads(spec.read_text(encoding="utf-8"))
        self.assertEqual("TDL_CLIENT_REPORT_V1", payload["contract"])
        self.assertEqual(SECTIONS, tuple(payload["required_sections"]))
        self.assertTrue(payload["rules"]["no_invented_severity_or_confidence"])

    def test_findings_are_linked_by_identity_without_invented_severity(self):
        manifest, run, interpretation = self.fixture()
        run["engine_report"]["technical_evaluation"]["stages"][0]["rules"] = [
            {"rule_id": "R-1", "status": "FAIL_TECHNICAL", "applicability": "APPLICABLE", "findings": []}]
        finding = {"origin": "AUDIT_ENGINE", "rule_id": "R-1", "stage": "G03",
                   "technical_status": "FAIL_TECHNICAL", "evidence": {"source_file": "stops.txt"}}
        report = build_client_report(manifest, run, [finding], interpretation,
                                     {"decision": "HUMAN_REVIEW"}, None)
        row = next(item for item in report["validation_matrix"] if item["rule_id"] == "R-1")
        self.assertEqual(["findings.json#/findings/0"], row["evidence_refs"])
        self.assertEqual("REQUIERE CORRECCIÓN ANTES DE PUBLICACIÓN",
                         report["summary"]["publication_readiness"])
        self.assertNotIn("severity", report["findings"][0])

    def test_bounded_publication_readiness_requires_explicit_matrix_applicability(self):
        manifest, run, interpretation = self.fixture()
        run["engine_report"]["technical_evaluation"]["stages"][0]["rules"] = [
            {"rule_id": "R-1", "status": "PASS", "applicability": "APPLICABLE", "findings": []}]
        report = build_client_report(manifest, run, [], interpretation,
                                     {"decision": "NOT_REMEDIABLE"}, None)
        self.assertEqual("APTO PARA PUBLICACIÓN SEGÚN ALCANCE EVALUADO",
                         report["summary"]["publication_readiness"])


if __name__ == "__main__":
    unittest.main()
