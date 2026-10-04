"""Runtime validation and provenance helpers for interpretation contract V1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "spec" / "audit_interpretation_contract_v1.schema.json"


def validate_result(result: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        # Keep runtime dependency-free. The full contract is also checked by the
        # project test suite; these invariants fail closed in minimal installs.
        required = schema["required"]
        if not isinstance(result, dict) or any(key not in result for key in required):
            raise ValueError("interpretation result does not satisfy required contract fields")
        if result["contract_version"] != "1.0.0" or result["provenance"].get("raw_findings_immutable") is not True:
            raise ValueError("interpretation result has incompatible contract provenance")
    else:
        errors = sorted(Draft202012Validator(schema).iter_errors(result), key=lambda e: list(map(str, e.path)))
        if errors:
            first = errors[0]
            raise ValueError(f"interpretation schema validation failed at {list(first.path)}: {first.message}")
    coverage = result["coverage"]
    calculated_gap = coverage["raw_finding_count"] - coverage["consolidated_occurrence_count"] - coverage["unclassified_occurrence_count"]
    if coverage["accounting_gap"] != calculated_gap:
        raise ValueError("interpretation accounting_gap does not match source and derived counts")
    if result["interpretation_status"] != ("COMPLETE" if calculated_gap == 0 else "INCOMPLETE"):
        raise ValueError("interpretation_status conflicts with accounting_gap")
    if len(result["source_findings"]) != coverage["raw_finding_count"]:
        raise ValueError("source finding cardinality changed")
