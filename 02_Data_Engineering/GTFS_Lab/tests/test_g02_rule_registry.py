from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from gtfs_lab.audit_contract import (
    AuditContractError, EngineRuleResult, ENGINE_RULE_RESULT_STATUSES, MANIFEST_VERSION,
    normalize_rule_result, validate_engine_status,
)
from gtfs_lab.audit_persistence import persist_audit
from gtfs_lab.change_attribution_v1_1 import compare as compare_v11
from gtfs_lab.core import DatasetIdentity, RunContext
from gtfs_lab.rule_registry import (
    ApplicabilityExpression as Expr, ApplicabilityOperator as Op,
    ApplicabilityTruth as Truth, CoverageState, RequirementKind, RuleAuthority,
    RuleCategory, RuleDefinition, RuleRegistry, RuleStatus, Severity,
    SpecificationReference, RuleCoverage, evaluate_applicability,
    SpecificationCondition as G01, SpecificationConditionOperator as G01Op,
    compile_specification_condition,
)


def rule(rule_id="GTFS-TEST", version="1.0.0", expression=None):
    return RuleDefinition(
        rule_id, version, RuleCategory.STRUCTURE,
        RuleAuthority.GTFS_REQUIRED, Severity.ERROR, RequirementKind.REQUIRED,
        ("stops.txt",), SpecificationReference("GTFS Schedule", "2026-04-27", "stops"),
        expression or Expr(Op.SIGNAL_PRESENT, signal="stops"), "test-evaluator/1", lambda _: None,
        ("stops",),
    )


def ca_snapshot(versions, status="NOT_APPLICABLE"):
    return {
        "audit_id": "audit-g02", "run_id": "run-g02", "timestamp": "2026-09-30T00:00:00Z",
        "change_attribution_contract_version": "1.1.0",
        "identity": {
            "dataset": {"source_sha256": "a" * 64, "dataset_id": "d", "lineage_id": "l"},
            "engine": {"parser_version": "p/1", "validator_version": "v/1", "gtfs_lab_version": "g/1"},
            "rules": {"ruleset_id": "registry", "rule_versions": versions},
            "compliance": {}, "configuration": {},
        },
        "result": {"rules": [{"rule_id": key, "status": status, "findings": []} for key in sorted(versions)]},
        "findings": [],
    }


class G02RegistryTests(unittest.TestCase):
    def test_register_duplicate_semver_and_deterministic_identity(self):
        registry = RuleRegistry()
        registry.register(rule("GTFS-Z"))
        registry.register(rule("GTFS-A", "2.1.3"))
        self.assertEqual(["GTFS-A", "GTFS-Z"], [item.rule_id for item in registry])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            registry.register(rule("GTFS-Z"))
        with self.assertRaises(RuntimeError):
            registry.identity_map()
        registry.freeze()
        self.assertEqual({"rule_versions": {"GTFS-A": "2.1.3", "GTFS-Z": "1.0.0"}}, registry.identity_map())
        for invalid in ("", "1", "01.2.3", "1.0.x", "1.0.0-01"):
            with self.subTest(version=invalid), self.assertRaises(ValueError):
                rule(version=invalid)

    def test_freeze_blocks_mutation_and_execution_before_freeze(self):
        registry = RuleRegistry([rule()])
        with self.assertRaises(RuntimeError):
            registry.execution_disposition(registry["GTFS-TEST"], {"stops": True})
        registry.freeze()
        self.assertTrue(registry.frozen)
        with self.assertRaisesRegex(RuntimeError, "frozen"):
            registry.register(rule("GTFS-OTHER"))
        decision, trace = registry.execution_disposition(registry["GTFS-TEST"], {"stops": True})
        self.assertEqual("EVALUATE", decision)
        self.assertEqual(Truth.TRUE, trace.truth)
        self.assertEqual(RuleStatus.NOT_APPLICABLE, registry.execution_disposition(registry["GTFS-TEST"], {"stops": False})[0])
        self.assertEqual(RuleStatus.NOT_EVALUABLE, registry.execution_disposition(registry["GTFS-TEST"], {})[0])

    def test_applicability_truth_table_and_evidence(self):
        present = Expr(Op.SIGNAL_PRESENT, signal="translations")
        equal = Expr(Op.SIGNAL_EQUALS, signal="feed_type", expected="fixed")
        cases = [
            (present, {"translations": True}, Truth.TRUE, None),
            (present, {"translations": False}, Truth.FALSE, RuleStatus.NOT_APPLICABLE),
            (present, {}, Truth.UNKNOWN, RuleStatus.NOT_EVALUABLE),
            (Expr(Op.ALL, conditions=(present, equal)), {"translations": True, "feed_type": "fixed"}, Truth.TRUE, None),
            (Expr(Op.ANY, conditions=(present, equal)), {"translations": False, "feed_type": "fixed"}, Truth.TRUE, None),
            (Expr(Op.NOT, conditions=(present,)), {"translations": False}, Truth.TRUE, None),
        ]
        for expression, signals, truth, status in cases:
            with self.subTest(truth=truth, expression=expression):
                result = evaluate_applicability(expression, signals)
                self.assertEqual(truth, result.truth)
                self.assertEqual(status, result.status)
                self.assertTrue(result.trace)
        self.assertIn("MISSING", str(evaluate_applicability(present, {}).trace))
        with self.assertRaises(ValueError):
            Expr("XOR", conditions=(present, equal))

    def test_unsupported_rule_metadata_rejected(self):
        for field, value in (("category", "OPERATOR_RULE"), ("authority", "CUSTOM"),
                             ("severity", "CRITICAL"), ("requirement", "MAY")):
            args = dict(rule().__dict__)
            args[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                RuleDefinition(**args)

    def test_g01_taxonomy_values_and_unsupported_values(self):
        self.assertEqual(10, len(RuleCategory))
        self.assertEqual({"STRUCTURE", "SCHEMA", "TYPE_FORMAT", "IDENTITY", "REFERENTIAL", "TEMPORAL", "SEQUENCE", "SPATIAL", "DATA_CONSISTENCY", "QUALITY"}, {x.value for x in RuleCategory})
        self.assertEqual({"GTFS_REQUIRED", "GTFS_CONDITIONAL", "GTFS_RECOMMENDED", "TDL_QUALITY"}, {x.value for x in RuleAuthority})
        self.assertEqual({"REQUIRED", "CONDITIONALLY_REQUIRED", "OPTIONAL", "RECOMMENDED", "PROHIBITED_WHEN"}, {x.value for x in RequirementKind})
        for field, values in (("category", RuleCategory), ("authority", RuleAuthority), ("requirement", RequirementKind)):
            for value in values:
                args = dict(rule().__dict__)
                args[field] = value.value
                RuleDefinition(**args)
        with self.assertRaises(ValueError):
            G01("NOT_A_G01_OPERATOR", subject="x")

    def test_g01_condition_translation_is_lossless_to_declared_signals(self):
        cases = [
            (G01(G01Op.FILE_PRESENT, subject="file:translations"), {"file:translations": True}, Truth.TRUE),
            (G01(G01Op.FILE_ABSENT, subject="file:calendar"), {"file:calendar": False}, Truth.TRUE),
            (G01(G01Op.FIELD_PRESENT, subject="field:routes.network_id"), {"field:routes.network_id": True}, Truth.TRUE),
            (G01(G01Op.FIELD_VALUE_EQUALS, subject="field:feed_info.feed_type", value="fixed"), {"field:feed_info.feed_type": "fixed"}, Truth.TRUE),
            (G01(G01Op.FIELD_VALUE_IN, subject="field:routes.route_type", values=("0", "1", "2")), {"field:routes.route_type": "2"}, Truth.TRUE),
            (G01(G01Op.ENTITY_EXISTS, subject="entity:locations.geojson"), {"entity:locations.geojson": True}, Truth.TRUE),
            (G01(G01Op.PARENT_ENTITY_EXISTS, subject="entity:parent_station"), {"entity:parent_station": True}, Truth.TRUE),
            (G01(G01Op.RELATED_FILE_PRESENT, subject="file:related"), {"file:related": True}, Truth.TRUE),
            (G01(G01Op.ONE_OF_FILES_PRESENT, subject="files:calendar_or_dates.any"), {"files:calendar_or_dates.any": True}, Truth.TRUE),
            (G01(G01Op.DEPENDENT_FIELDS, subject="fields:dependent.valid"), {"fields:dependent.valid": True}, Truth.TRUE),
            (G01(G01Op.ALL_SERVICE_DATES_DEFINED, subject="calendar_dates:all_service_dates_defined"), {"calendar_dates:all_service_dates_defined": True}, Truth.TRUE),
        ]
        for condition, signals, expected in cases:
            with self.subTest(operator=condition.operator):
                self.assertEqual(expected, evaluate_applicability(compile_specification_condition(condition), signals).truth)
        in_condition, _, _ = cases[4]
        self.assertEqual(Truth.FALSE, evaluate_applicability(compile_specification_condition(in_condition), {"field:routes.route_type": "99"}).truth)
        nested = G01(G01Op.ALL, conditions=(cases[0][0], G01(G01Op.NOT, conditions=(G01(G01Op.FILE_PRESENT, subject="file:optional"),))))
        self.assertEqual(Truth.TRUE, evaluate_applicability(compile_specification_condition(nested), {"file:translations": True, "file:optional": False}).truth)

    def test_engine_status_severity_and_legacy_warning_are_separate(self):
        self.assertIn("NOT_APPLICABLE", ENGINE_RULE_RESULT_STATUSES)
        self.assertEqual("NOT_APPLICABLE", validate_engine_status("NOT_APPLICABLE"))
        self.assertEqual("2.0.0", __import__("gtfs_lab.audit_contract", fromlist=["ENGINE_RULE_RESULT_CONTRACT_VERSION"]).ENGINE_RULE_RESULT_CONTRACT_VERSION)
        self.assertEqual("1.1.2", MANIFEST_VERSION)
        self.assertEqual("WARNING", normalize_rule_result({"status": "WARNING", "severity": "INFO"})["status"])
        EngineRuleResult("GTFS-T", "NOT_APPLICABLE", "ERROR")
        EngineRuleResult("GTFS-T", "FAIL_TECHNICAL", "WARNING")
        with self.assertRaises(AuditContractError):
            normalize_rule_result({"status": "NOT_APPLICABLE", "severity": "INFO"})
        with self.assertRaises(AuditContractError):
            validate_engine_status("WARNING")
        with self.assertRaises(AuditContractError):
            EngineRuleResult("GTFS-T", "PASS", "CRITICAL")

    def test_coverage_states_keep_deferred_out_of_rule_status(self):
        rows = [
            RuleCoverage("translations", "ABSENT", "NONE", CoverageState.FEATURE_NOT_PRESENT),
            RuleCoverage("stops", "PRESENT", "FULL", CoverageState.FEATURE_PRESENT_FULLY_AUDITED),
            RuleCoverage("fares", "PRESENT", "PARTIAL", CoverageState.FEATURE_PRESENT_PARTIALLY_AUDITED),
            RuleCoverage("fare_products", "PRESENT", "DEFERRED", CoverageState.FEATURE_PRESENT_DEFERRED),
        ]
        self.assertEqual("FEATURE_PRESENT_DEFERRED", rows[-1].state.value)
        self.assertNotIn("FAIL_TECHNICAL", [row.state.value for row in rows])
        with self.assertRaises(ValueError):
            RuleCoverage("fare_products", "PRESENT", "DEFERRED", CoverageState.FEATURE_PRESENT_FULLY_AUDITED)

    def test_change_attribution_1_1_maps_versions_independent_of_disposition(self):
        base = ca_snapshot({"GTFS-A": "1.0.0"})
        self.assertEqual([], compare_v11(base, ca_snapshot({"GTFS-A": "1.0.0"})) ["per_rule_changes"])
        self.assertEqual("RULE_SEMANTIC_CHANGE", compare_v11(base, ca_snapshot({"GTFS-A": "2.0.0"})) ["per_rule_changes"][0]["change"])
        self.assertEqual("RULE_ADDED", compare_v11(base, ca_snapshot({"GTFS-A": "1.0.0", "GTFS-B": "1.0.0"})) ["per_rule_changes"][0]["change"])
        self.assertEqual("RULE_REMOVED", compare_v11(base, ca_snapshot({})) ["per_rule_changes"][0]["change"])
        changed = compare_v11(base, ca_snapshot({"GTFS-A": "1.1.0"}))
        self.assertEqual("NOT_APPLICABLE", ca_snapshot({"GTFS-A": "1.1.0"})["result"]["rules"][0]["status"])
        self.assertEqual("RULE_SEMANTIC_CHANGE", changed["per_rule_changes"][0]["change"])

    def test_persistence_uses_explicit_registry_identity_for_zero_finding_rules(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "feed.zip"
            source.write_bytes(b"synthetic")
            digest = __import__("hashlib").sha256(b"synthetic").hexdigest()
            work = root / "run"
            work.mkdir()
            for name in ("run.json", "validation.json", "analysis.json", "report.md"):
                (work / name).write_text("{}", encoding="utf-8")
            (work / "exports").mkdir()
            ctx = RunContext("run-g02", DatasetIdentity("d", "feed.zip", digest, "2026-01-01T00:00:00Z", "p/1", "g/1"), source, work, {}, {})
            result_rules = [
                {"rule_id": rule_id, "version": version, "scope": "G02", "severity": "ERROR", "status": status, "findings": [], "evaluator_executed": executed}
                for rule_id, version, status, executed in (("GTFS-PASS", "1.0.0", "PASS", True), ("GTFS-FAIL", "1.0.1", "FAIL_TECHNICAL", True), ("GTFS-NA", "1.2.0", "NOT_APPLICABLE", False), ("GTFS-UNKNOWN", "2.0.0", "NOT_EVALUABLE", False), ("GTFS-ERROR", "2.1.0", "INSPECTION_ERROR", False), ("GTFS-ZERO", "3.0.0", "PASS", True))
            ]
            result = {"validation": {"rules": result_rules}, "dataset": ctx.dataset.__dict__, "gtfs_lab_version": "g/1", "validator_version": "v/1", "summary": {"status": "PASS"}}
            identities = {"rule_versions": {"GTFS-PASS": "1.0.0", "GTFS-FAIL": "1.0.1", "GTFS-NA": "1.2.0", "GTFS-UNKNOWN": "2.0.0", "GTFS-ERROR": "2.1.0", "GTFS-ZERO": "3.0.0", "GTFS-REGISTERED": "1.0.0"}}
            persisted = persist_audit(ctx, result, rule_identity_map=identities)
            manifest = json.loads((work / "audit" / "audit_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("ACCEPTED", persisted["manifest_status"])
            self.assertEqual(identities["rule_versions"], manifest["identity"]["rules"]["rule_versions"])
            self.assertEqual(identities["rule_versions"], manifest["registered_rule_versions"])
            self.assertEqual(sorted(identities["rule_versions"]), manifest["registered_rule_ids"])
            self.assertEqual({"GTFS-PASS": "1.0.0", "GTFS-FAIL": "1.0.1", "GTFS-ZERO": "3.0.0"}, manifest["executed_rule_versions"])
            self.assertEqual(["GTFS-FAIL", "GTFS-PASS", "GTFS-ZERO"], manifest["executed_rule_ids"])
            persist_audit(ctx, result)
            legacy_manifest = json.loads((work / "audit" / "audit_manifest.json").read_text(encoding="utf-8"))
            self.assertNotIn("identity", legacy_manifest)
            self.assertNotIn("registered_rule_versions", legacy_manifest)
            self.assertEqual(sorted(rule["rule_id"] for rule in result_rules), legacy_manifest["executed_rule_ids"])
            self.assertEqual({rule["rule_id"]: rule["version"] for rule in result_rules}, legacy_manifest["executed_rule_versions"])


if __name__ == "__main__":
    unittest.main()
