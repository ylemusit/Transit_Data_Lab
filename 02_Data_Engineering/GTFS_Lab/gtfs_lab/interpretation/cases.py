"""Validation and report views for the additive audit-case contract V1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "spec" / "audit_case_contract_v1.schema.json"


def validate_cases(model: dict[str, Any], interpretation: dict[str, Any] | None = None, *, require_full: bool = False) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        if require_full:
            raise ValueError("Full audit-case validation requires jsonschema; delivery generation is blocked")
        _validate_minimal(model, schema)
    else:
        errors = sorted(Draft202012Validator(schema).iter_errors(model), key=lambda error: list(map(str, error.path)))
        if errors:
            error = errors[0]
            raise ValueError(f"audit-case schema validation failed at {list(error.path)}: {error.message}")
    coverage = model["coverage"]
    case_ids = [case["case_id"] for case in model["cases"]]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("duplicate case_id")
    if sum(coverage["source_origins"].values()) != coverage["source_record_count"]:
        raise ValueError("source origin counts do not reconcile to source_record_count")
    if coverage["reconciled_event_count"] + coverage["duplicate_source_reference_count"] != coverage["classified_record_count"]:
        raise ValueError("reconciled events and duplicate references do not reconcile to classified records")
    expected_gap = coverage["source_record_count"] - coverage["classified_record_count"] - coverage["unclassified_record_count"]
    if expected_gap < 0 or coverage["accounting_gap"] != expected_gap:
        raise ValueError("case coverage accounting_gap is inconsistent")
    for case in model["cases"]:
        if case["occurrence_count"] != len(case["occurrences"]):
            raise ValueError(f"occurrence_count mismatch in {case['case_id']}")
        if case["reconciled_event_count"] > case["occurrence_count"]:
            raise ValueError(f"reconciled_event_count exceeds source occurrences in {case['case_id']}")
        reaudited = case["reaudit"]["status"]
        links = case["reaudit"]["links"]
        expected_relation = {"RESOLVED": "RESOLVED", "PERSISTENT": "PERSISTENT", "REAPPEARED": "REAPPEARED"}.get(reaudited)
        if expected_relation and not any(link["relation"] == expected_relation and link["evidence_ref"].strip() for link in links):
            raise ValueError(f"reaudit status {reaudited} in {case['case_id']} requires a matching evidence link")
        if reaudited == "RESOLVED":
            current_ids = {model["execution_identity"]["audit_execution_id"], model["execution_identity"]["client_audit_id"]}
            if not any(link["relation"] == "RESOLVED" and link["evidence_ref"].strip() and link["execution_id"] not in current_ids for link in links):
                raise ValueError(f"reaudit status RESOLVED in {case['case_id']} requires evidence from a different execution")
    primary_ids: list[str] = []
    referenced_ids: set[str] = set()
    for case in model["cases"]:
        primary_count = 0
        for occurrence in case["occurrences"]:
            record_id = occurrence["source_record_id"]
            referenced_ids.add(record_id)
            if occurrence["assignment"] == "PRIMARY":
                primary_ids.append(record_id)
                primary_count += 1
        # Per-case event counts are assigned once to primary occurrences; related links add no event count.
        if case["reconciled_event_count"] > primary_count:
            raise ValueError(f"case {case['case_id']} event count exceeds its primary record references")
    if len(primary_ids) != len(set(primary_ids)):
        raise ValueError("a source_record_id has more than one PRIMARY case assignment")
    coverage = model["coverage"]
    if len(primary_ids) != coverage["classified_record_count"]:
        raise ValueError("PRIMARY case assignments do not cover classified_record_count")
    if len(model["unclassified_source_record_ids"]) != coverage["unclassified_record_count"]:
        raise ValueError("unclassified source record IDs do not match unclassified_record_count")
    if set(primary_ids) & set(model["unclassified_source_record_ids"]):
        raise ValueError("source records cannot be both classified and unclassified")
    if coverage["reconciled_event_count"] != sum(case["reconciled_event_count"] for case in model["cases"]):
        raise ValueError("per-case reconciled event counts do not match coverage")
    if interpretation is not None:
        from collections import Counter
        actual_origins = dict(Counter(str(item.get("origin") or item.get("stage") or "UNKNOWN") for item in interpretation.get("source_findings", [])))
        if coverage["source_origins"] != actual_origins:
            raise ValueError("source origins differ from V1 findings")
        for field in ("dataset_id",):
            if field in interpretation["dataset_identity"] and model["dataset_identity"][field] != interpretation["dataset_identity"][field]:
                raise ValueError("dataset identity differs from V1")
        if "engine_version" in interpretation["execution_identity"] and model["execution_identity"]["engine_version"] != interpretation["execution_identity"]["engine_version"]:
            raise ValueError("engine version differs from V1")
        if model["dataset_identity"]["sha256"] != interpretation["dataset_identity"]["sha256"]:
            raise ValueError("audit cases refer to a different source than V1 interpretation")
        if model["execution_identity"]["audit_execution_id"] != interpretation["execution_identity"]["audit_execution_id"]:
            raise ValueError("audit cases refer to a different execution than V1 interpretation")
        if model["source_interpretation"]["sha256"] != _sha256_json(interpretation):
            raise ValueError("audit cases interpretation digest does not match supplied V1 interpretation")
        source_findings = interpretation.get("source_findings")
        if not isinstance(source_findings, list):
            raise ValueError("supplied V1 interpretation has no source_findings array")
        source_by_id = {str(item.get("raw_finding_id")): item for item in source_findings}
        if len(source_by_id) != len(source_findings) or coverage["source_record_count"] != len(source_findings):
            raise ValueError("source finding identity/count mismatch")
        if set(primary_ids) | set(model["unclassified_source_record_ids"]) != set(source_by_id):
            raise ValueError("primary and unclassified source record IDs do not account for V1 source_findings")
        if referenced_ids - set(source_by_id):
            raise ValueError("audit case occurrence refers to a source_record_id absent from V1")
        for case in model["cases"]:
            for occurrence in case["occurrences"]:
                source = source_by_id[occurrence["source_record_id"]]
                expected_file = str(source.get("source_file") or source.get("file") or source.get("table") or "UNKNOWN")
                expected_origin = str(source.get("origin") or source.get("stage") or "UNKNOWN")
                if occurrence["origin"] != expected_origin or occurrence["rule_id"] != str(source.get("rule_id") or "UNKNOWN_RULE") or occurrence["source_file"] != expected_file:
                    raise ValueError(f"source_record_id {occurrence['source_record_id']} origin/rule/file mismatch against V1")
                native = source.get("record_locator") or source.get("row_locator") or source.get("locator")
                if native is not None:
                    if occurrence["native_locator"] != str(native) or occurrence["normalized_locator"] != normalize_locator(expected_file, str(native)):
                        raise ValueError(f"source_record_id {occurrence['source_record_id']} locator mismatch against V1")


def normalize_locator(source_file: str, native: str) -> str:
    """Preserve the historical row convention; normalize only evidenced legacy trips."""
    value = native
    if source_file == "trips.txt" and native.startswith("record:"):
        try:
            value = f"data_row:{int(native.split(':', 1)[1]) - 1}"
        except ValueError:
            pass
    return f"{source_file}:{value}"


def _validate_minimal(model: dict[str, Any], schema: dict[str, Any]) -> None:
    """Fail-closed core validation for minimal runtime installs without jsonschema."""
    def required(value: Any, definition: dict[str, Any], path: str) -> None:
        if not isinstance(value, dict):
            raise ValueError(f"{path} must be an object")
        missing = [key for key in definition.get("required", []) if key not in value]
        if missing:
            raise ValueError(f"{path} missing required fields: {', '.join(missing)}")
        for key, child in definition.get("properties", {}).items():
            if key not in value:
                continue
            if "const" in child and value[key] != child["const"]:
                raise ValueError(f"{path}.{key} has an incompatible contract value")
            if "enum" in child and value[key] not in child["enum"]:
                raise ValueError(f"{path}.{key} has an unsupported value")
            if child.get("type") == "object":
                required(value[key], child, f"{path}.{key}")

    required(model, schema, "audit_cases")
    for field in ("dataset_identity", "execution_identity", "source_interpretation", "coverage", "use_readiness"):
        required(model[field], schema["properties"][field], f"audit_cases.{field}")
    if not isinstance(model["cases"], list) or not isinstance(model["limitations"], list):
        raise ValueError("audit_cases cases and limitations must be arrays")
    if not isinstance(model["unclassified_source_record_ids"], list):
        raise ValueError("audit_cases.unclassified_source_record_ids must be an array")
    case_schema = schema["$defs"]["case"]
    for index, case in enumerate(model["cases"]):
        required(case, case_schema, f"audit_cases.cases[{index}]")
        required(case["reaudit"], case_schema["properties"]["reaudit"], f"audit_cases.cases[{index}].reaudit")
        if not isinstance(case["occurrences"], list):
            raise ValueError(f"audit_cases.cases[{index}].occurrences must be an array")
        occurrence_schema = schema["$defs"]["occurrence"]
        for occ_index, occurrence in enumerate(case["occurrences"]):
            required(occurrence, occurrence_schema, f"audit_cases.cases[{index}].occurrences[{occ_index}]")


def _sha256_json(value: dict[str, Any]) -> str:
    import hashlib
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def sha256_json(value: dict[str, Any]) -> str:
    """Return the canonical JSON digest used to link a lateral model to V1."""
    return _sha256_json(value)
