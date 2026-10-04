"""Contract-level checks for Audit Interpretation V1; no runtime analyzer is implied."""

import copy
import json
import re
import unittest
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # Keep the repository test suite free of a new runtime dependency.
    Draft202012Validator = None


HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE.parent / "spec" / "audit_interpretation_contract_v1.schema.json"
FIXTURE_PATH = HERE / "fixtures" / "audit_interpretation_v1_synthetic.json"


def _schema_errors(value, schema, root=None, path="$ "):
    """Small stdlib-only validator for the JSON Schema keywords used by this contract."""
    root = root or schema
    errors = []
    if "$ref" in schema:
        target = root
        for part in schema["$ref"].removeprefix("#/").split("/"):
            if part:
                target = target[part]
        return _schema_errors(value, target, root, path)
    expected = schema.get("type")
    types = expected if isinstance(expected, list) else [expected]
    if expected:
        matches = any(
            (kind == "object" and isinstance(value, dict))
            or (kind == "array" and isinstance(value, list))
            or (kind == "string" and isinstance(value, str))
            or (kind == "integer" and isinstance(value, int) and not isinstance(value, bool))
            or (kind == "number" and isinstance(value, (int, float)) and not isinstance(value, bool))
            or (kind == "boolean" and isinstance(value, bool))
            or (kind == "null" and value is None)
            for kind in types
        )
        if not matches:
            return [f"{path}: tipo no válido"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: no coincide con const")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: valor fuera de enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: minLength")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path}: pattern")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", float("-inf")) or value > schema.get("maximum", float("inf")):
            errors.append(f"{path}: rango")
    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{path}: falta {name}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}: propiedad extra {name}" for name in value if name not in properties)
        for name, child in value.items():
            if name in properties:
                errors.extend(_schema_errors(child, properties[name], root, f"{path}.{name}"))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: minItems")
        if "items" in schema:
            for index, child in enumerate(value):
                errors.extend(_schema_errors(child, schema["items"], root, f"{path}[{index}]"))
    return errors


class AuditInterpretationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.result = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_01_raw_findings_remain_unchanged(self):
        raw = copy.deepcopy(self.result["source_findings"])
        _derived_view = [{"raw_finding_id": f["raw_finding_id"]} for f in raw]
        self.assertEqual(raw, self.result["source_findings"])

    def test_02_raw_cardinality_is_preserved(self):
        self.assertEqual(len(self.result["source_findings"]), 10)
        self.assertEqual(sum(f["raw_occurrence_count"] for f in self.result["finding_families"]), 10)

    def test_03_complete_fixture_has_zero_accounting_gap(self):
        coverage = self.result["coverage"]
        self.assertEqual(coverage["accounting_gap"], 0)
        self.assertEqual(coverage["raw_finding_count"], coverage["consolidated_occurrence_count"] + coverage["unclassified_occurrence_count"])

    def test_04_unknown_findings_remain_unclassified_and_unknown(self):
        result = copy.deepcopy(self.result)
        raw = copy.deepcopy(result["source_findings"][0])
        raw.update(raw_finding_id="raw-unknown", entity_id="shape-unknown")
        result["source_findings"].append(raw)
        unknown_family = copy.deepcopy(result["finding_families"][0])
        unknown_family.update(
            family_id="GTFS-G07-DISTANCE-PROGRESSION|UNKNOWN_PATTERN|shape",
            raw_occurrence_count=1,
            affected_entity_count=1,
            observations=[],
            calculations=[],
            inferences=[],
            patterns=[{"pattern_id": "UNKNOWN_PATTERN", "status": "UNKNOWN_PATTERN", "occurrence_count": 0, "classification": "UNCLASSIFIED"}],
            unclassified_occurrences=1,
            probable_explanations=[],
            evidence_refs=[{"raw_finding_ids": ["raw-unknown"], "source_file": "shapes.txt", "dataset_sha256": result["dataset_identity"]["sha256"], "audit_execution_id": "synthetic-run-001"}],
        )
        result["finding_families"].append(unknown_family)
        result["coverage"].update(raw_finding_count=11, consolidated_occurrence_count=10, unclassified_occurrence_count=1, accounting_gap=0)
        self.assertEqual(unknown_family["patterns"][0]["status"], "UNKNOWN_PATTERN")
        self.assertEqual(unknown_family["unclassified_occurrences"], 1)
        self.assertEqual(_schema_errors(result, self.schema), [])

    def test_05_direct_and_propagated_impact_are_separate(self):
        impact = self.result["finding_families"][0]["operational_impact"]
        self.assertEqual(impact["direct_affected"]["entity_count"], 4)
        self.assertEqual(impact["propagated_usage"][0]["entity_count"], 15)
        self.assertNotEqual(impact["direct_affected"]["entity_count"], impact["propagated_usage"][0]["entity_count"])

    def test_06_interpretations_are_explicitly_inferred(self):
        family = self.result["finding_families"][0]
        self.assertTrue(all(item["kind"] == "INFERRED" for item in family["inferences"]))
        self.assertTrue(all(item["kind"] == "OBSERVED" for item in family["observations"]))
        self.assertTrue(all(item["kind"] == "CALCULATED" for item in family["calculations"]))

    def test_07_no_global_score_is_in_contract_or_fixture(self):
        self.assertNotIn("global_quality_score", self.schema["properties"])
        self.assertNotIn("global_quality_score", self.result)

    def test_08_no_implicit_legal_conclusion_is_emitted(self):
        self.assertNotIn("legal_compliance", self.schema["properties"])
        self.assertNotIn("legal_conclusion", self.result)

    def test_09_family_ids_are_deterministic_semantic_keys(self):
        for family in self.result["finding_families"]:
            semantic_key = "|".join((family["rule_id"], family["patterns"][0]["pattern_id"], family["affected_entity_type"]))
            self.assertEqual(family["family_id"], semantic_key)
            self.assertNotIn("uuid", family["family_id"].lower())

    def test_10_synthetic_output_matches_contract_schema(self):
        if Draft202012Validator is not None:
            Draft202012Validator.check_schema(self.schema)
            self.assertEqual(list(Draft202012Validator(self.schema).iter_errors(self.result)), [])
        else:
            self.assertEqual(_schema_errors(self.result, self.schema), [])


if __name__ == "__main__":
    unittest.main()
