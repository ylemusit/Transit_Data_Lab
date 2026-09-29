"""Synthetic regression for portable preconditions and gate semantics."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from gtfs_lab.change_attribution_v1_1 import compare
from gtfs_lab.change_attribution import compare as compare_legacy
from gtfs_lab.audit_comparison import compare_audits
from gtfs_lab.ci_gate import classify

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from compliance_portable_gate import sources, portable_sql
from protected_resource_preflight import check_resource


def snapshot(versions, contract="1.1.0"):
    return {"audit_id": "A", "change_attribution_contract_version": contract,
            "identity": {"dataset": {"source_sha256": "a" * 64},
                         "engine": {"parser_version": "1", "validator_version": "1", "gtfs_lab_version": "1"},
                         "rules": {"ruleset_id": "synthetic", "ruleset_version": "1", "rule_versions": versions},
                         "compliance": {}, "configuration": {}},
            "result": {"rules": [{"rule_id": key, "status": "PASS", "findings": []} for key in sorted(versions)]},
            "findings": []}


class Preconditions(unittest.TestCase):
    def test_rule_semantic_change_resolves_legacy_result_uncertainty(self):
        base = snapshot({"R2": "1"})
        candidate = snapshot({"R2": "2"})
        candidate["result"]["rules"][0]["status"] = "FAIL_TECHNICAL"
        result = compare(base, candidate)
        self.assertEqual(["RULE_SEMANTIC_CHANGE"], result["supported_causes"])
        self.assertEqual("RULE_SEMANTIC_CHANGE", result["attribution"])
        self.assertEqual([], result["unresolved_reasons"])
        self.assertEqual("SUPPORTED", result["confidence_or_evidence_status"]["status"])

    def test_rule_semantic_change_keeps_unresolved_lineage_identity(self):
        base = snapshot({"R2": "1"})
        base["identity"]["dataset"]["lineage_id"] = "L1"
        candidate = snapshot({"R2": "2"})
        candidate["identity"]["dataset"]["lineage_id"] = "L2"
        candidate["result"]["rules"][0]["status"] = "FAIL_TECHNICAL"
        result = compare(base, candidate)
        self.assertEqual(["RULE_SEMANTIC_CHANGE", "UNATTRIBUTED_CHANGE"], result["supported_causes"])
        self.assertEqual("MULTIPLE_CAUSES", result["attribution"])
        self.assertEqual(["result changed without a supported identity cause"], result["unresolved_reasons"])
        self.assertEqual("SUPPORTED", result["confidence_or_evidence_status"]["status"])

    def test_rule_semantic_change_and_unresolved_lineage_without_result_change(self):
        base = snapshot({"R2": "1"})
        base["identity"]["dataset"]["lineage_id"] = "L1"
        candidate = snapshot({"R2": "2"})
        candidate["identity"]["dataset"]["lineage_id"] = "L2"
        result = compare(base, candidate)
        self.assertEqual(["RULE_SEMANTIC_CHANGE", "UNATTRIBUTED_CHANGE"], result["supported_causes"])
        self.assertEqual("MULTIPLE_CAUSES", result["attribution"])
        self.assertEqual(["dataset identity changed without a supported source change"], result["unresolved_reasons"])
        self.assertEqual("SUPPORTED", result["confidence_or_evidence_status"]["status"])

    def test_rule_semantic_and_supported_dataset_change(self):
        base = snapshot({"R2": "1"})
        candidate = snapshot({"R2": "2"})
        candidate["identity"]["dataset"]["source_sha256"] = "b" * 64
        candidate["identity"]["dataset"]["lineage_id"] = "L2"
        result = compare(base, candidate)
        self.assertEqual(["DATASET_CHANGE", "RULE_SEMANTIC_CHANGE"], result["supported_causes"])
        self.assertEqual("MULTIPLE_CAUSES", result["attribution"])
        self.assertEqual([], result["unresolved_reasons"])
        self.assertEqual("SUPPORTED", result["confidence_or_evidence_status"]["status"])

    def test_implementation_semantic_and_unresolved_identity_coexist(self):
        base = snapshot({"R2": "1"})
        base["identity"]["dataset"]["lineage_id"] = "L1"
        candidate = snapshot({"R2": "2"})
        candidate["identity"]["dataset"]["lineage_id"] = "L2"
        candidate["identity"]["engine"]["parser_version"] = "2"
        candidate["result"]["rules"][0]["status"] = "FAIL_TECHNICAL"
        result = compare(base, candidate)
        self.assertEqual(["PARSER_IMPLEMENTATION_CHANGE", "RULE_SEMANTIC_CHANGE", "UNATTRIBUTED_CHANGE"], result["supported_causes"])
        self.assertEqual("MULTIPLE_CAUSES", result["attribution"])
        self.assertEqual(["result changed without a supported identity cause"], result["unresolved_reasons"])
        self.assertEqual("SUPPORTED", result["confidence_or_evidence_status"]["status"])

    def test_missing_identity_and_legacy_contract_are_preserved(self):
        base = snapshot({"R2": "1"})
        candidate = snapshot({"R2": "2"})
        del base["identity"]["dataset"]["source_sha256"]
        result = compare(base, candidate)
        self.assertEqual(["RULE_SEMANTIC_CHANGE"], result["supported_causes"])
        self.assertEqual("MISSING_IDENTITY", result["confidence_or_evidence_status"]["status"])
        self.assertEqual(["baseline.dataset.source_sha256"], result["confidence_or_evidence_status"]["missing_identity"])
        legacy_base = snapshot({"R2": "1"}, "1.0.0")
        legacy_candidate = snapshot({"R2": "2"}, "1.0.0")
        self.assertEqual(compare_legacy(legacy_base, legacy_candidate), compare(legacy_base, legacy_candidate))

    def test_resource_missing_hash_and_ready(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "resource"
            spec = {"name": "test", "path": str(path.resolve()), "sha256": "a" * 64}
            self.assertEqual("RESOURCE_NOT_FOUND", check_resource(spec)["status"])
            path.write_bytes(b"x")
            self.assertEqual("RESOURCE_HASH_MISMATCH", check_resource(spec)["status"])
            import hashlib
            spec["sha256"] = hashlib.sha256(b"x").hexdigest()
            self.assertEqual("RESOURCE_READY", check_resource(spec)["status"])
            spec["kind"] = "duckdb"
            Path(str(path) + ".wal").write_bytes(b"pending")
            self.assertEqual("RESOURCE_WAL_PRESENT", check_resource(spec)["status"])

    def test_legal_sources_portable_and_fail_closed(self):
        self.assertEqual("PASS", sources(ROOT)["status"])
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual("RESOURCE_ERROR", sources(Path(temporary))["status"])
            manifest = json.loads((ROOT / "03_Compliance/legal_sources_portable_v1.json").read_text(encoding="utf-8"))
            for spec in manifest["sources"]:
                target = Path(temporary) / spec["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / spec["path"], target)
            self.assertEqual("PASS", sources(Path(temporary))["status"])
            command = [sys.executable, str(ROOT / "tools/compliance_portable_gate.py"), "--legal-root", temporary, "--sources-only"]
            self.assertEqual(3, subprocess.run(command, capture_output=True).returncode)
            self.assertEqual(0, subprocess.run(command + ["--allow-external-legal-root"], capture_output=True).returncode)
            first = Path(temporary) / manifest["sources"][0]["path"]
            first.write_bytes(first.read_bytes() + b"modified")
            self.assertEqual("RESOURCE_ERROR", sources(Path(temporary))["status"])
            self.assertEqual("RESOURCE_HASH_MISMATCH", sources(Path(temporary))["sources"][0]["status"])
        self.assertNotIn("LEGAL_HASH_", portable_sql())

    def test_ci_failure_and_policy(self):
        summary = dict.fromkeys(("ingestion", "integrity", "validation", "analysis", "gis", "database", "compliance_v1"), "PASS")
        summary["findings"] = 0
        self.assertEqual(0, classify(summary)["exit_code"])
        self.assertEqual(("FAIL_TECHNICAL", 2), tuple(classify(dict(summary, validation="FAIL_TECHNICAL"))[key] for key in ("status", "exit_code")))
        self.assertEqual(2, classify(dict(summary, validation="INSPECTION_ERROR"))["exit_code"])
        self.assertEqual(2, classify(dict(summary, database="FAIL_LOCAL"))["exit_code"])
        self.assertEqual(3, classify({})["exit_code"])
        self.assertEqual(3, classify({}, findings_policy="bad")["exit_code"])

    def test_per_rule_semantics_and_legacy_boundary(self):
        base = snapshot({"R1": "1", "R2": "1"})
        for versions, expected in (({"R1": "1", "R2": "2"}, ["R2"]),
                                   ({"R1": "2", "R2": "2"}, ["R1", "R2"]),
                                   ({"R1": "1", "R2": "1", "R3": "1"}, ["R3"]),
                                   ({"R1": "1"}, ["R2"])):
            result = compare(base, snapshot(versions))
            self.assertEqual(expected, [row["rule_id"] for row in result["per_rule_changes"]])
            self.assertTrue(result["rules_change"])
        candidate = snapshot({"R1": "1", "R2": "1"})
        candidate["identity"]["engine"]["parser_version"] = "2"
        self.assertEqual([], compare(base, candidate)["per_rule_changes"])
        candidate = snapshot({"R1": "1", "R2": "2"})
        candidate["result"]["rules"][1]["status"] = "FAIL_TECHNICAL"
        self.assertEqual("RULE_SEMANTIC_CHANGE", compare(base, candidate)["attribution"])
        legacy = snapshot({"R1": "1"}, "1.0.0")
        self.assertEqual("NOT_COMPARABLE", compare(legacy, base)["comparability"])
        self.assertEqual("NOT_COMPARABLE", compare(base, legacy)["comparability"])
        for left, right in ((legacy, base), (base, legacy)):
            l, r = dict(left, snapshot_contract="AuditComparisonSnapshot", snapshot_contract_version="1.0.0"), dict(right, snapshot_contract="AuditComparisonSnapshot", snapshot_contract_version="1.0.0")
            self.assertEqual("NOT_COMPARABLE", compare_audits(l, r)["comparability"]["status"])


if __name__ == "__main__":
    unittest.main()
